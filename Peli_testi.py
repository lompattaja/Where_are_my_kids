import mysql.connector
import os
import time
import random

# Muodostetaan tietokantayhteys
yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='salasana',
         autocommit=True
         )

# Funktio, joka tyhjentää näytön (windows)
def tyhjennä():
    os.system("cls")

def jatka():
    print(input("""
    
Paina enter jatkaaksesi."""))
    os.system("cls")

# time.sleep(1) -> voi käyttää jos haluaa pitää taukoa

# Pelin tarina
print("Eräänä päivänä lentävä apina ja hänen kymmenen lastaan olivat matkalla takaisin kotiin.")
jatka()
print("Kovat tuulet tarttuivat pieniin apinanpoikasiin ja lennättivät heidät kauas pois, ympäri Euroopan maita.")
jatka()
print("""Äitiapina kauhistui.
Hän yritti tavoittaa lapsiaan, mutta tuulen voima oli liian suuri.""")
jatka()

print("Kun myrsky vihdoin tyyntyi, jäljellä oli vain hiljainen taivas ja äidin sydäntä painava huoli.")
jatka()
print("Lentävä apina keräsi rohkeutensa ja hänen oli lähdettävä etsimään kadonneita lapsiaan.")
jatka()
print("""Jokainen niistä saattoi olla missä päin Eurooppaa tahansa
ja vain sinä voisit auttaa häntä tässä vaikeassa tilanteessa.""")
jatka()

# Itkevä apina animaatio
itkevä_kuvat = [
    r"""        
                    ..::+*******+.:..               
                .:********************:.            
            .******************************.        
       :+********=---------++---------=********+:   
     :***+++***=------------------------=***+++***: 
    -**==+++**------++=----------=++------**++++=**-
    **=--=++*+----######*------+######----+*+==---**
    **=--=+**+----===--------------====---+**+=---**
    -**+++****----===--------------====---****++=**-
    .:*********=--===---=#*--+#+---====-=*********:.
       :+*******--===--------------====-*******+:.. 
        .******---===----+*==*+----====--******.    
         +****=---===---#*++++*#---====--=*****.     
           :****+=+++=---*#**#*---=+++=+****:.      
               ..=++++**++====++***+++=....         
    """,
    r"""
                    ..::+*******+.:..               
                .:********************:.            
            .******************************.        
       :+********=---------++---------=********+:   
     :***+++***=------------------------=***+++***: 
    -**==+++**------++=----------=++------**++++=**-
    **=--=++*+----######*------+######----+*+==---**
    **=--=+**+----------------------------+**+=---**
    -**+++****----===--------------====---****++=**-
    .:*********=--===---=#*--+#+---====-=*********:.
       :+*******--===--------------====-*******+:.. 
        .******---===----+*==*+----====--******.    
         +****=---===---#*++++*#---====--=*****.     
           :****+=+++=---*#**#*---=+++=+****:.      
               ..=++++**++====++***+++=....         
    """,
    r"""
                    ..::+*******+.:..               
                .:********************:.            
            .******************************.        
       :+********=---------++---------=********+:   
     :***+++***=------------------------=***+++***: 
    -**==+++**------++=----------=++------**++++=**-
    **=--=++*+----######*------+######----+*+==---**
    **=--=+**+----===--------------====---+**+=---**
    -**+++****----------------------------****++=**-
    .:*********=--===---=#*--+#+---====-=*********:.
       :+*******--===--------------====-*******+:.. 
        .******---===----+*==*+----====--******.    
         +****=---===---#*++++*#---====--=*****.     
           :****+=+++=---*#**#*---=+++=+****:.      
               ..=++++**++====++***+++=....         
    """,
    r"""
                    ..::+*******+.:..               
                .:********************:.            
            .******************************.        
       :+********=---------++---------=********+:   
     :***+++***=------------------------=***+++***: 
    -**==+++**------++=----------=++------**++++=**-
    **=--=++*+----######*------+######----+*+==---**
    **=--=+**+----===--------------====---+**+=---**
    -**+++****----===--------------====---****++=**-
    .:*********=--------=#*--+#+--------=*********:.
       :+*******--===--------------====-*******+:.. 
        .******---===----+*==*+----====--******.    
         +****=---===---#*++++*#---====--=*****.     
           :****+=+++=---*#**#*---=+++=+****:.      
               ..=++++**++====++***+++=....         
    """,
    r"""
                    ..::+*******+.:..               
                .:********************:.            
            .******************************.        
       :+********=---------++---------=********+:   
     :***+++***=------------------------=***+++***: 
    -**==+++**------++=----------=++------**++++=**-
    **=--=++*+----######*------+######----+*+==---**
    **=--=+**+----===--------------====---+**+=---**
    -**+++****----===--------------====---****++=**-
    .:*********=--===---=#*--+#+---====-=*********:.
       :+*******------------------------*******+:.. 
        .******---===----+*==*+----====--******.    
         +****=---===---#*++++*#---====--=*****.     
           :****+=+++=---*#**#*---=+++=+****:.      
               ..=++++**++====++***+++=....         
    """,
    r"""
                    ..::+*******+.:..               
                .:********************:.            
            .******************************.        
       :+********=---------++---------=********+:   
     :***+++***=------------------------=***+++***: 
    -**==+++**------++=----------=++------**++++=**-
    **=--=++*+----######*------+######----+*+==---**
    **=--=+**+----===--------------====---+**+=---**
    -**+++****----===--------------====---****++=**-
    .:*********=--===---=#*--+#+---====-=*********:.
       :+*******--===--------------====-*******+:.. 
        .******----------+*==*+----------******.    
         +****=---===---#*++++*#---====--=*****.     
           :****+=+++=---*#**#*---=+++=+****:.      
               ..=++++**++====++***+++=....         
    """,
    r"""
                    ..::+*******+.:..               
                .:********************:.            
            .******************************.        
       :+********=---------++---------=********+:   
     :***+++***=------------------------=***+++***: 
    -**==+++**------++=----------=++------**++++=**-
    **=--=++*+----######*------+######----+*+==---**
    **=--=+**+----===--------------====---+**+=---**
    -**+++****----===--------------====---****++=**-
    .:*********=--===---=#*--+#+---====-=*********:.
       :+*******--===--------------====-*******+:.. 
        .******---===----+*==*+----====--******.    
         +****=---------#*++++*#---------=*****.     
           :****+=+++=---*#**#*---=+++=+****:.      
               ..=++++**++====++***+++=....         
    """,
]

for kuva in itkevä_kuvat:
    tyhjennä()
    print(kuva)
    time.sleep(0.6)             # kuvat tulee 0.6 sekunnin välein (näyttää kuin apina itkee)

tyhjennä()

# Pelin alku
print("Auttaisitko häntä?")
jatka()

# Haetaan game-taulusta suurin id-arvo ja palautetaan se suurin arvo +1. (koska id:llä ei ole auto_increment)
# id on varchar eli se on tekstikenttä ei numero, eli pitää palauttaa merkkijonona (str)
def luo_uusi_id():
    sql = "select max(id) from game"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()      # palauttaa yhden rivin
    suurin_id = tulos[0]            # ylempi palauttaa tuplen eli esim. ('3',) ja halutaan vain se eka arvo eli pelkkä numero 3
    uusi_id = int(suurin_id) + 1    # muutetaan suurin_id kokonaisluvuksi, koska se on string
    return str(uusi_id)             # muutetaan se takaisin stringiksi

# Lisätään uusi rivi game-tauluun kohtaan (id ja screen_name)
def lisää_pelaaja(nimimerkki):
    uusi_id = luo_uusi_id()         # hakee seuraavan id:n luo_uusi_id funktion avulla
    nimimerkki = nimimerkki.lower() # Tallennetaan aina pienillä kirjaimilla
    sql = f"insert into game (id, screen_name) values ('{uusi_id}', '{nimimerkki}')"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    print(f"Kiitos, kun autat minua {nimimerkki}.")

# Tarkistaa onko pelaajan antama nimimerkki jo käytössä
# Palauttaa True jos löytyy ja False jos ei löydy
def nimimerkki_käytössä(nimimerkki):
    sql = f"select count(*) from game where lower(screen_name) = lower('{nimimerkki}')"    # count(*) kertoo monta riviä löytyy sillä nimimerkillä
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos[0] > 0         # sql palauttaa taas tuplen niin otetaan eka arvo numerona

# PÄÄOHJELMA:
print("Tervetuloa peliin.")

# Kysytään onko uusi vai vanha pelaaja
# Jos vanha pelaaja niin jatketaan vanhasta pelistä ellei pelaaja halua aloittaa uutta peliä
# Jos on uusi pelaaja niin aloitetaan uusi peli
while True:
    vastaus = input("Oletko uusi pelaaja? (kyllä/ei): ").strip().lower()
    if vastaus == "kyllä":      # eli uusi pelaaja
        while True:
            nimimerkki = input("Anna lentävälle apinalle nimimerkki: ").strip()
            if nimimerkki_käytössä(nimimerkki):
                print("Nimimerkki on jo käytössä, valitse toinen.")
            else:
                lisää_pelaaja(nimimerkki)
                break
        break

    elif vastaus == "ei":       # eli vanha pelaaja
        while True:
            jatka_peliä = input("Haluatko jatkaa mihin jäit? (kyllä/ei): ").strip().lower()
            if jatka_peliä == "kyllä":
                nimimerkki = input("Anna vanha nimimerkkisi: ").strip()
                if nimimerkki_käytössä(nimimerkki):
                    print(f"Tervetuloa takaisin peliin, {nimimerkki}!")
                    break
                else:
                    print("Nimimerkkiä ei löytynyt.")
            elif jatka_peliä == "ei":
                while True:
                    nimimerkki = input("Anna uusi nimimerkki: ").strip()
                    if nimimerkki_käytössä(nimimerkki):
                        print("Nimimerkki on jo käytössä, valitse toinen.")
                    else:
                        lisää_pelaaja(nimimerkki)
                        break
                break

            else:
                print('Väärä syöte, kirjoita vain "kyllä" tai "ei".')
        break


    else:
        print('Väärä syöte, kirjoita vain "kyllä" tai "ei".')

# Funktio, joka hakee pelin id:n annetun nimimerkin perusteella
def hae_game_id(nimimerkki):
    sql = f"select id from game where lower(screen_name) = lower('{nimimerkki}')"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos[0]

# Funktio, joka arpoo 10 eri EU-maata ja tallentaa ne tietokantaan
def arvo_kymmenen_maata(game_id):
    sql = f"select country_name from country where continent = 'EU'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    maat = []
    for rivi in kursori.fetchall():
        maat.append(rivi[0])

    # Arvotaan 10 eri EU-maata
    valitut_maat = random.sample(maat,10)

    # Tallennetaan ne tietokantaan
    for maa in valitut_maat:
        sql = f"insert into kadonneet_lapset (game_id, iso_country, löydetyt_lapset) values ('{game_id}', '{maa}', 0)"
        kursori = yhteys.cursor()
        kursori.execute(sql)

    return valitut_maat

# /help-komento
def help_komento(game_id):
    # Haetaan kaikki EU-maat
    sql = "select country_name from country where continent = 'EU'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    kaikki_maat = []
    for rivi in kursori.fetchall():
        kaikki_maat.append(rivi[0])

    # Haetaan maat joissa pelaaja on jo käynyt
    sql = f"select iso_country from kadonneet_lapset where game_id = '{game_id}' and käydyt_maat = 1"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    käydyt_maat = []
    for rivi in kursori.fetchall():
        käydyt_maat.append(rivi[0])

    # Tulostetaan lista EU-maista ja merkitään mitkä on jo käyty
    print("""
    Kaikki EU-maat:
    """)
    for maa in kaikki_maat:
        if maa in käydyt_maat:
            merkki = "x"
        else:
            merkki = " "
    print(f"{maa} [{merkki}]")

# Funktio, joka tarkistaa löytyykö lapsi kyseisestä maasta
def tarkista_maa(game_id, maa):
    sql = f"select löydetyt_lapset from kadonneet_lapset where game_id = 'game_id' and iso_country = '{maa}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    if not tulos:
        print(f"Kadonnutta apinanpoikasta ei löytynyt.")
        return False

    löydetty = tulos[0]
    if löydetty == 1:
        print()