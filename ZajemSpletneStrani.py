import requests, re, os

prevedi = { 'Å¾' : 'ž',
           'Ä\x8d' : 'č',
           'Å¡' : 'š'}

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
    id_n = 1
    glavni_podatki_o_receptu = open('glavni_recepti.txt', 'w')
    recepti_sestavine = open('recepti-sestavine.txt', 'w')
    urls = open('url-naslovi-strani-receptov.txt', 'r')
    for url_naslov in urls:
        url_naslov = url_naslov.strip().strip('"')
        podatki = zajemi_podatke(url_naslov)
        print(id_n, podatki)
        id_n += 1

a = zajemi_podatke('/recept/rizevi-rezanci-s-svinjino-in-zelenjavo')
print(a)

    
