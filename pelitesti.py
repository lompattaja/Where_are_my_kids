import os
import mysql.connector
import random

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='salis20',
         autocommit=True,
         )

# ARVOTAAN KYMMENEN SATUNNAISTA EUROOPAN MAATA

def arvo_apinoiden_maat():
    kursori = yhteys.cursor()

    # haetaan euroopan maat
    sql = ('select name from country where continent = "EU"')
    kursori.execute(sql)
    rivit = kursori.fetchall() # hakee kaikki rivit sql:stä eli kaikki EU maat (yht. 50)

    maat = []               # luodaan tyhjä lista
    for rivi in rivit:      # käydään läpi kaikki rivit
        nimi = rivi[0]      # otetaan rivin ensimmäinen sarake
        maat.append(nimi)   # lisätään listaan

    # arvotaan 10 eri maata
    satunnaiset_maat = random.sample(maat, 10)  # random.sample(lista_josta_arvotaan, monta)

    return satunnaiset_maat


# PELIN ALOITUS KYSYMYS:
def pelaa(kadonneet):
    löydetyt = []           # luodaan tyhjä lista, johon tallenetaan löydetyt maat

    while len(löydetyt) < len(kadonneet):           # silmukka niin kauan kuin löydetyt maat < kadonneet maat
        kysymys = input("Minne maahan haluat lentää? ")

        if kysymys in kadonneet:                    # tarkistetaan, onko käyttäjän kirjoittama maa listassa kadonneet
            if kysymys in löydetyt:
                print(f"Olet jo käynyt {kysymys}-maassa.")
            else:
                print(f"Löysit kadonneen apinanpoikasen! 🐒")
                löydetyt.append(kysymys)            # lisätään maa löydettyjen listaan
                print(f"Sinulla on vielä {len(kadonneet) - len(löydetyt)} löydettävää maata jäljellä!")
        else:
            print("Tämä maa ei ole Eurooppa listalla. Kokeile uudelleen. ")
    print("Hienoa! Olet löytänyt kaikki apinanpoikaset!")


def apu_komento(kysymys, kadonneet, löydetyt):
    if kysymys == "/help":
        print("Seuraavat EU:n maat ovat vielä käymättä: ")

        ei_löydetyt = []
        for maa in kadonneet:
            if maa not in löydetyt:
                ei_löydetyt.append(maa)

        if ei_löydetyt:
            for maa in ei_löydetyt:
                print(f"{maa}")

