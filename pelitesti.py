import mysql.connector
import os
import time
import random

# Muodostetaan tietokantayhteys
yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='salis20',
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
    time.sleep(0.6)  # kuvat tulee 0.6 sekunnin välein (näyttää kuin apina itkee)

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
    tulos = kursori.fetchone()  # palauttaa yhden rivin
    suurin_id = tulos[0]  # ylempi palauttaa tuplen eli esim. ('3',) ja halutaan vain se eka arvo eli pelkkä numero 3
    uusi_id = int(suurin_id) + 1  # muutetaan suurin_id kokonaisluvuksi, koska se on string
    return str(uusi_id)  # muutetaan se takaisin stringiksi


# Lisätään uusi rivi game-tauluun kohtaan (id ja screen_name)
def lisää_pelaaja(nimimerkki):
    uusi_id = luo_uusi_id()  # hakee seuraavan id:n luo_uusi_id funktion avulla
    sql = f"insert into game (id, screen_name) values ('{uusi_id}', '{nimimerkki}')"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    print(f"Kiitos, kun autat minua {nimimerkki}.")


# Tarkistaa onko pelaajan antama nimimerkki jo käytössä
# Palauttaa True jos löytyy ja False jos ei löydy
def nimimerkki_käytössä(nimimerkki):
    sql = f"select count(*) from game where screen_name = '{nimimerkki}'"  # count(*) kertoo monta riviä löytyy sillä nimimerkillä
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos[0] > 0  # sql palauttaa taas tuplen niin otetaan eka arvo numerona


# PÄÄOHJELMA:
print("Tervetuloa peliin.")

# Kysytään onko uusi vai vanha pelaaja
# Jos vanha pelaaja niin jatketaan vanhasta pelistä ellei pelaaja halua aloittaa uutta peliä
# Jos on uusi pelaaja niin aloitetaan uusi peli
while True:
    vastaus = input("Oletko uusi pelaaja? (kyllä/ei): ")
    if vastaus == "kyllä":  # eli uusi pelaaja
        while True:
            nimimerkki = input("Anna lentävälle apinalle nimimerkki: ")
            if nimimerkki_käytössä(nimimerkki):
                print("Nimimerkki on jo käytössä, valitse toinen.")
            else:
                lisää_pelaaja(nimimerkki)
                break
        break

    elif vastaus == "ei":  # eli vanha pelaaja
        while True:
            jatka_peliä = input("Haluatko jatkaa mihin jäit? (kyllä/ei): ")
            if jatka_peliä == "kyllä":
                nimimerkki = input("Anna vanha nimimerkkisi: ")
                if nimimerkki_käytössä(nimimerkki):
                    print(f"Tervetuloa takaisin peliin, {nimimerkki}!")
                    break
                else:
                    print("Nimimerkkiä ei löytynyt.")
            elif jatka_peliä == "ei":
                while True:
                    nimimerkki = input("Anna uusi nimimerkki: ")
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


# ARVOTAAN KYMMENEN SATUNNAISTA EUROOPAN MAATA
# TALLENTAA NE 10 MAATA kadonneet_lapset-TAULUUN LIITETTYNÄ KYSEISEEN PELAAJAN ID:HEN

def arvo_apinoiden_maat(nimimerkki):
    kursori = yhteys.cursor()

    # Haetaan pelaajan id
    sql = f"select id from game where screen_name = '{nimimerkki}'"
    kursori.execute(sql)
    id = kursori.fetchone()[0]

    # haetaan euroopan maat
    sql = ('select name from country where continent = "EU"')
    kursori.execute(sql)
    kaikki_maat = kursori.fetchall() # hakee kaikki rivit sql:stä eli kaikki EU maat (yht. 50)

    # arvotaan 10 eri maata
    satunnaiset_maat = random.sample(kaikki_maat, 10)  # random.sample(lista_josta_arvotaan, monta)

    # Tallennetaan tauluun kadonneet_lapset
    for maa in satunnaiset_maat:
        sql = f"insert into kadonneet_lapset (game_id, country_name) values ({id}, '{maa}')"
        kursori.execute(sql)[0]

    return satunnaiset_maat

# APU KOMENTO FUNKTIONA

def näytä_help(kadonneet, löydetyt):
    print("Nämä maat ovat vielä käymättä: ")
    for maa in kadonneet:
        if maa not in löydetyt:
            print("-", maa)
    print()


# FUNKTIO JOKA TARKISTAA VALITUN MAAN

def lentää_maahan(nimimerkki, maa):
    kursori = yhteys.cursor()

    # Haetaan pelaajan id
    sql = f"select id from game where screen_name = {nimimerkki}"
    kursori.execute(sql)
    id = kursori.fetchone()

    # Onko tässä maassa apina?
    sql = f"select id, loydetty from kadonneet_lapset where game_id = {nimimerkki} and country_name = '{maa}'"
    kursori.execute(sql)
    tulos = kursori.fetchone()

    if not tulos:
        print("Täältä ei löytynyt apinanpoikasta.")
        return False

    if tulos[1] == 1:
        print(f"Olet jo käynyt {maa}-maassa.")
        return False

    # Jos kadonnut lapsi löytynyt, merkitään löydetyksi
    sql = f"update kadonneet_lapset set loydetty = true where game_id = {nimimerkki}"
    kursori.execute(sql)
    print(f"Mahtavaa! Löysit kadonneen lapsen {maa}-maasta!")
    return True


# PELIN ALOITUS KYSYMYS:
def pelaa(kadonneet):
    löydetyt = []           # luodaan tyhjä lista, johon tallenetaan löydetyt maat

    while len(löydetyt) < len(kadonneet):           # silmukka niin kauan kuin löydetyt maat < kadonneet maat
        arvaus = input("Minne maahan haluat lentää? ")

        if arvaus == "/help":
            print("Nämä EU:n maat vielä käymättä: ")
            for maa in kadonneet:
                if maa not in löydetyt:
                    print(maa)

        elif arvaus in kadonneet:                    # tarkistetaan, onko käyttäjän kirjoittama maa listassa kadonneet
            if arvaus in löydetyt:
                print(f"Olet jo käynyt {arvaus}-maassa.")
            else:
                print(f"Löysit kadonneen apinanpoikasen! 🐒")
                löydetyt.append(arvaus)            # lisätään maa löydettyjen listaan
                print(f"Sinulla on vielä {len(kadonneet) - len(löydetyt)} löydettävää maata jäljellä!")
        else:
            print("Tämä maa ei ole Eurooppa listalla. Kokeile uudelleen. ")
    print("Hienoa! Olet löytänyt kaikki apinanpoikaset!")

# PÄÄOHJELMA

löydetyt = 0

arvo_apinoiden_maat(nimimerkki)

while löydetyt < 10:
    komento = input("Mihin EU maahan haluat lentää? (jos tarvitset apua kirjoita /help): ")

    if komento == "/help":
        näytä_help(nimimerkki)
    else:
        if lentää_maahan(nimimerkki, komento):
            löydetyt += 1
            print(f"Löydettyjä apinanpoikasia: {löydetyt}/10.")

print("Löysit kaikki apinat!")
