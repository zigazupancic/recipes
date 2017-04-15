import requests, re, os

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
    glavni_url = 'http://okusno.je/recepti/#/recepti/page:'
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

    
