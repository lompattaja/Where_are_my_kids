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

    # Tarkistetaan onko pelaajalla jo kadonneita maita
    sql = (f"select country_name from kadonneet_lapset where game_id = '{id}'")
    kursori.execute(sql)
    olemassa_olevat_maat = kursori.fetchall()

    if olemassa_olevat_maat:
        return [maa for maa, in olemassa_olevat_maat]

    # Jos pelaajalla ei ole jo kadonneita maita:
    # Haetaan euroopan maat
    sql = ('select name from country where continent = "EU"')
    kursori.execute(sql)
    kaikki_maat = kursori.fetchall() # hakee kaikki rivit sql:stä eli kaikki EU maat (yht. 50)

    # ja arvotaan 10 eri maata merkkijonona
    satunnaiset_maat = [maa for maa, in random.sample(kaikki_maat, 10)]  # random.sample(lista_josta_arvotaan, monta)

    # Tallennetaan tauluun kadonneet_lapset
    for maa in satunnaiset_maat:
        sql = f"insert into kadonneet_lapset (game_id, country_name) values ('{id}', '{maa}')"
        kursori.execute(sql)

    yhteys.commit()
    return satunnaiset_maat


# APU KOMENTO FUNKTIONA
# - ei toimi (se ei päivitä kun esimerkiksi kirjoittaa maan ja sen jälkeen /help niin ei kumita juuri kirjoitettua maata)
def näytä_help(nimimerkki):
    kursori = yhteys.cursor()

    # Haetaan pelaajan id
    sql = f"select id from game where screen_name = '{nimimerkki}'"
    kursori.execute(sql)
    id = kursori.fetchone()[0]

    # Haetaan kaikki Euroopan maat
    sql = "select name from country where continent = 'EU'"
    kursori.execute(sql)
    kaikki_maat = kursori.fetchall()  # lista tuplia: [('Finland',), ('Sweden',) ...]

    # Haetaan maat, joissa pelaaja on jo käynyt (löytänyt tai yrittänyt)
    sql = f"select country_name from kadonneet_lapset where game_id = '{id}'"
    kursori.execute(sql)
    kaydyt_maat = kursori.fetchall()

    # Luodaan lista maista, joissa pelaaja ei ole vielä käynyt
    ei_käydyt_maat = []
    for maa_rivi in kaikki_maat:
        maa = maa_rivi[0]
        if (maa,) not in kaydyt_maat:  # tarkistetaan tuplana, koska fetchall palauttaa tuplan
            ei_käydyt_maat.append(maa)

    if not ei_käydyt_maat:
        print("Olet jo käynyt kaikissa Euroopan maissa.")
    else:
        print("Nämä maat ovat vielä käymättä: ")
        for maa in ei_käydyt_maat:
            print("-", maa)




# FUNKTIO JOKA TARKISTAA VALITUN MAAN

def lentää_maahan(nimimerkki, maa):
    kursori = yhteys.cursor()

    # Haetaan pelaajan id
    sql = f"select id from game where screen_name = '{nimimerkki}'"
    kursori.execute(sql)
    id = kursori.fetchone()[0]

    # sql vastaa kysymykseen onko tässä maassa apina?
    sql = f"select id, loydetty from kadonneet_lapset where game_id = '{id}' and country_name = '{maa}'"
    kursori.execute(sql)
    tulos = kursori.fetchone()

    if not tulos:
        print("Täältä ei löytynyt apinanpoikasta.")
        return False

    if tulos[1] == 1:
        print(f"Olet jo käynyt {maa}-maassa.")
        return False

    # Jos kadonnut lapsi löytynyt, merkitään löydetyksi
    sql = f"update kadonneet_lapset set loydetty = true where game_id = '{id}' and country_name = '{maa}'"
    kursori.execute(sql)
    print(f"Mahtavaa! Löysit kadonneen lapsen {maa}-maasta!")
    return True


# Haetaan pelaajan id ja jo löydettyjen apinanpoikasten määrä
kursori = yhteys.cursor()
sql = f"select id from game where screen_name = '{nimimerkki}'"
kursori.execute(sql)
id = kursori.fetchone()[0]

sql = f"select count(*) from kadonneet_lapset where game_id = '{id}' and loydetty = true"
kursori.execute(sql)
löydetyt = kursori.fetchone()[0]  # Tämä on jo löydettyjen määrä



# PÄÄOHJELMA silmukka
satunnaiset_maat = arvo_apinoiden_maat(nimimerkki)

while löydetyt < len(satunnaiset_maat):
    komento = input("Mihin EU maahan haluat lentää? (jos tarvitset apua kirjoita /help): ")

    if komento == "/help":
        näytä_help(nimimerkki)
    else:
        if lentää_maahan(nimimerkki, komento):
            löydetyt += 1
            print(f"Löydettyjä apinanpoikasia: {löydetyt}/{len(satunnaiset_maat)}.")

print("Kiitos! Löysit kaikki apinanpoikaset!")
