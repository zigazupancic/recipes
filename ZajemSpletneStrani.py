import requests, re, os

prevedi = { 'Å¾' : 'ž',
           'Ä\x8d' : 'č',
           'Å¡' : 'š',
            'Å\xa0' : 'Š',
            'Ä\x8c' : 'Č',
            'Ã¶' : 'ö',
            'Å½' : 'Ž',
            'Ã¨' : 'è',
            'Ã»' : 'û',
            'Ã©' : 'é'}

def shrani(url, ime_dat):
    r = requests.get(url)
    lokacija = os.getcwd()
    dat = os.path.dirname(lokacija + '"\"' + ime_dat)
    if dat:
        os.makedirs(dat, exist_ok = True)
    with open(ime_dat, "w") as file:
        tekst = str(r.text.encode('ascii', 'ignore'))
        file.write(tekst)
        print("Shranjeno: ", url)

def zajemi_naslove():
    #glavni_url = 'http://okusno.je/recepti/#/recepti/page:'
    glavni_url = 'http://okusno.je/lbin/ajax_okusno_search.php?tab_clicked=true&search=/recepti/page:'
    f = open('url-naslovi-strani-receptov.txt' , 'w')
    rel_urls = re.compile(r'recipe-item" href=(".*")')
    for i in range(1, 100):
        url = glavni_url + str(i) + r'/'
        r = requests.get(url)
        naslovi = re.findall(rel_urls, r.text)
        for naslov in naslovi:
            f.write(naslov + '\n')
        #print(i, naslovi)
        print(url)

def zajemi_podatke(url_recept):
    url = 'http://okusno.je' + url_recept
    r = requests.get(url)
    regex_naslov = re.compile(r'<h2.*">(.*)<')
    regex_gl_sest = re.compile(r'main_ing.*">(.*)<')
    regex_sestavine = re.compile(r'rel=.*?><\/div>\s*?<label>\s*(.*)\s*.*\s*.*\s*.*?>(.*)<')
    regex_tezavnost = re.compile(r'cook-diff.*?(\d)')
    regex_cas_priprave = re.compile(r'cook-sum-time.*\s*.*\s*.*\s*.*\s*.*\s*(.*)')
    # TO DO regex_navodila_recept = re.compile()

    tekst = r.text
    for crka, prevod in prevedi.items():
        tekst = tekst.replace(crka, prevod)

    podatki = dict()
    podatki['ime_recepta'] = list(re.findall(regex_naslov, tekst))
    podatki['glavne_sestavine'] = list(re.findall(regex_gl_sest, tekst))
    podatki['sestavine'] = list(re.findall(regex_sestavine, tekst))
    podatki['tezavnost'] = list(re.findall(regex_tezavnost, tekst))
    podatki['cas_priprave'] = list(re.findall(regex_cas_priprave, tekst))
    return podatki

def naredi_csv():
    
    glavni_podatki_o_receptu = open('glavni_recepti.csv', 'w')
    glavni_podatki_o_receptu.write('id; ime sestavine; tezavnost; cas_priprave \n')
    
    recepti_sestavine = open('recepti-sestavine.csv', 'w')
    recepti_sestavine.write('recept; sestavina; količina \n')
    urls = open('url-naslovi-strani-receptov.txt', 'r')

    ID = 1
    for url_naslov in urls:
        if ID > 10:
            break
        try:
            url_naslov = url_naslov.strip().strip('"')
            podatki = zajemi_podatke(url_naslov)
            
            #Glavni podatki o receptu
            ime_recepta = podatki['ime_recepta'][0]
            tezavnost = podatki['tezavnost'][0]
            cas_priprave = podatki['cas_priprave'][0]
            line = '{0}; {1}; {2}; \n'.format(ime_recepta, tezavnost, cas_priprave)
            glavni_podatki_o_receptu.write(line)

            #Sestavine - zaenkrat dodamo samo vse sestavine
            for kolicina, sestavina in podatki['sestavine']:
                k = kolicina
                if 'label' in k:
                    k = ''
                line = '{0}; {1}; {2}; \n'.format(ime_recepta, sestavina, k)
                recepti_sestavine.write(line)
            ID += 1
            print(ID, ime_recepta)
        except:
            print(podatki)
            print('ERROR : ###################################')
    
    glavni_podatki_o_receptu.close()
    recepti_sestavine.close()

a = zajemi_podatke('/recept/rizevi-rezanci-s-svinjino-in-zelenjavo')
print(a)
naredi_csv()
    
