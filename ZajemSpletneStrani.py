import requests, re, os
import csv

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
    regex_url_slike = re.compile(r'promo_thumb_big.*\s*.+src="(.+jpg)')
    regex_navodila_recept = re.compile(r'contextual-text">.*\s*.*\s*(.*)')

    tekst = r.text
    for crka, prevod in prevedi.items():
        tekst = tekst.replace(crka, prevod)

    podatki = dict()
    podatki['ime_recepta'] = list(re.findall(regex_naslov, tekst))
    podatki['glavne_sestavine'] = list(re.findall(regex_gl_sest, tekst))
    podatki['sestavine'] = list(re.findall(regex_sestavine, tekst))
    podatki['tezavnost'] = list(re.findall(regex_tezavnost, tekst))
    podatki['cas_priprave'] = list(re.findall(regex_cas_priprave, tekst))
    podatki['url_slike'] = list(re.findall(regex_url_slike, tekst))
    podatki['url'] = [url]
    podatki['navodila'] = list(re.findall(regex_navodila_recept, tekst))
    return podatki

def data():

    glavni_podatki = []
    recept = []
    mere = set()
    sestavine = set()
    
    urls = open('url-naslovi-strani-receptov.txt', 'r')

    cnt = 0
    
    for url_naslov in urls:
        cnt += 1
        if cnt > 2:
            break
        try:
            url_naslov = url_naslov.strip().strip('"')
            podatki = zajemi_podatke(url_naslov)

            #Glavni podatki o receptu
            ime_recepta = podatki['ime_recepta'][0].replace(',', '')
            tezavnost = podatki['tezavnost'][0]
            cas_priprave = podatki['cas_priprave'][0].split(' ')[0]
            url_slike = podatki['url_slike'][0]
            url_recepta = podatki['url'][0]
            priprava = ' '.join(podatki['navodila'])
            glavni_podatki.append([ime_recepta, tezavnost,cas_priprave,url_slike,url_recepta,priprava])

            #Sestavine
            for kolicina, sestavina in podatki['sestavine']:
                k = kolicina
                m = None
                if 'label' in k:
                    k = ''
                kol = k
                if ' ' in k:
                    loceno = k.split(' ')
                    mere.add(loceno[1])
                    m = loceno[1]
                    kol = loceno[0]
                if ',' in sestavina:
                    pomozne = sestavina.split(',')
                    for delna in pomozne:
                        sestavine.add(delna)
                        recept.append([ime_recepta, sestavina, kol, m])
                else:
                    sestavine.add(sestavina)
                    recept.append([ime_recepta, sestavina, kol, m])
        except:
            pass
    return glavni_podatki, recept, mere, sestavine

def naredi_csv():
    
    glavni_podatki_o_receptu = open('glavni_recepti.csv', 'w')
    #glavni_podatki_o_receptu.write('ime recepta, tezavnost, cas_priprave [min], url_slike, url_recepta \n')
    
    recepti_sestavine = open('recepti-sestavine.csv', 'w')
    #recepti_sestavine.write('recept, sestavina, količina \n')

    razne_mere = open('razne_mere.csv', 'w')

    razne_sestavine = open('razne_sestavine.csv', 'w')
    
    glavni_podatki, recept, mere, sestavine = data()

    writer1 = csv.writer(razne_sestavine)
    for sest in sestavine:
        writer1.writerow([sest])

    writer2 = csv.writer(razne_mere)
    for m in mere:
        writer2.writerow([m])

    writer3 = csv.writer(recepti_sestavine)
    for vrstica in recept:
        writer3.writerow(vrstica)

    writer4 = csv.writer(glavni_podatki_o_receptu)
    for vrstica in glavni_podatki:
        writer4.writerow(vrstica)
        

    
    glavni_podatki_o_receptu.close()
    recepti_sestavine.close()
    razne_mere.close()
    razne_sestavine.close()

a = zajemi_podatke('/recept/rizevi-rezanci-s-svinjino-in-zelenjavo')
print(a)
#naredi_csv()
    
