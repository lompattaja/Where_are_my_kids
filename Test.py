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


# Pelin tarina
print("""

    Eräänä päivänä lentävä apina ja hänen kymmenen lastaan olivat matkalla takaisin kotiin.""")
jatka()
print("""

    Kovat tuulet tarttuivat pieniin apinanpoikasiin ja lennättivät heidät kauas pois, ympäri Euroopan maita.""")
jatka()
print("""

    Äitiapina kauhistui.
    Hän yritti tavoittaa lapsiaan, mutta tuulen voima oli liian suuri.""")
jatka()
print("""

    Kun myrsky vihdoin tyyntyi, jäljellä oli vain hiljainen taivas ja äidin sydäntä painava huoli.""")
jatka()
print("""

    Lentävä apina keräsi rohkeutensa ja hänen oli lähdettävä etsimään kadonneita lapsiaan.""")
jatka()
print("""

    Jokainen niistä saattoi olla missä päin Eurooppaa tahansa
    ja vain sinä voisit auttaa häntä tässä vaikeassa tilanteessa.""")
jatka()

# Itkevä apina animaatio
itkevä_kuvat = [
    """        
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
    """
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
    """
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
    """
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
    """
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
    """
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
    """
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
print("""

    Auttaisitko häntä?""")
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
    nimimerkki = nimimerkki.lower()  # Tallennetaan aina pienillä kirjaimilla
    sql = f"insert into game (id, screen_name) values ('{uusi_id}', '{nimimerkki}')"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    print(f"""
    Kiitos, kun autat minua {nimimerkki}.""")


# Tarkistaa onko pelaajan antama nimimerkki jo käytössä
# Palauttaa True jos löytyy ja False jos ei löydy
def nimimerkki_käytössä(nimimerkki):
    sql = f"select count(*) from game where lower(screen_name) = lower('{nimimerkki}')"  # count(*) kertoo monta riviä löytyy sillä nimimerkillä
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos[0] > 0  # sql palauttaa taas tuplen niin otetaan eka arvo numerona


# PÄÄOHJELMA NIMIMERKIN TALLENTAMISEEN:
print("""
    Tervetuloa peliin.""")

# Kysytään onko uusi vai vanha pelaaja
# Jos vanha pelaaja niin jatketaan vanhasta pelistä ellei pelaaja halua aloittaa uutta peliä
# Jos on uusi pelaaja niin aloitetaan uusi peli
while True:
    vastaus = input("""
    Oletko uusi pelaaja? (kyllä/ei): """).strip().lower()
    tyhjennä()
    if vastaus == "kyllä":  # eli uusi pelaaja
        while True:
            nimimerkki = input("""
    Anna lentävälle apinalle nimimerkki: """).strip()
            tyhjennä()
            if nimimerkki_käytössä(nimimerkki):
                print("""
    Nimimerkki on jo käytössä, valitse toinen.""")
                tyhjennä()
            else:
                lisää_pelaaja(nimimerkki)
                break
        break

    elif vastaus == "ei":  # eli vanha pelaaja
        while True:
            jatka_peliä = input("""
    Haluatko jatkaa mihin jäit? (kyllä/ei): """).strip().lower()
            if jatka_peliä == "kyllä":
                nimimerkki = input("""
    Anna vanha nimimerkkisi: """).strip()
                tyhjennä()
                if nimimerkki_käytössä(nimimerkki):
                    print(f"""
    Tervetuloa takaisin peliin, {nimimerkki}!""")
                    break
                else:
                    print("""
    Nimimerkkiä ei löytynyt.""")
            elif jatka_peliä == "ei":
                while True:
                    nimimerkki = input("""
    Anna uusi nimimerkki: """).strip()
                    if nimimerkki_käytössä(nimimerkki):
                        print("""
    Nimimerkki on jo käytössä, valitse toinen.""")
                    else:
                        lisää_pelaaja(nimimerkki)
                        break
                break

            else:
                print('''
    Väärä syöte, kirjoita vain "kyllä" tai "ei".''')
        break


    else:
        print('''
    Väärä syöte, kirjoita vain "kyllä" tai "ei".''')


# Funktio, joka hakee pelin id:n annetun nimimerkin perusteella
def hae_game_id(nimimerkki):
    sql = f"select id from game where lower(screen_name) = lower('{nimimerkki}')"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos[0]


# Funktio, joka hakee EU-maat
def hae_eu_maat():
    kursori = yhteys.cursor()
    sql = "select name from country where continent = 'EU'"
    kursori.execute(sql)
    kaikki_maat = []
    for rivi in kursori.fetchall():
        kaikki_maat.append(rivi[0].lower())
    kursori.close()
    return kaikki_maat


# Funktio, joka arpoo 10 eri EU-maata ja tallentaa ne tietokantaan, jos ei ole jo tallennettu
def arvo_apinoiden_maat(game_id):
    kursori = yhteys.cursor()

    # Tarkistetaan onko pelaajalla jo arvottuja maita
    sql = f"select country_name from kadonneet_lapset where game_id = '{game_id}'"
    kursori.execute(sql)
    olemassa_olevat_maat = kursori.fetchall()

    if olemassa_olevat_maat:
        maat = []
        for rivi in olemassa_olevat_maat:
            maat.append(rivi[0])
        return maat

    # Haetaan kaikki EU-maat käyttämällä valmista funktiota (vältetään koodin toistoa)
    kaikki_maat = hae_eu_maat()
    # Muutetaan takaisin isoiksi kirjaimiksi arvontaa varten
    kaikki_maat = [maa.title() for maa in kaikki_maat]

    # Arvotaan 10 eri EU-maata
    valitut_maat = random.sample(kaikki_maat, 10)

    # Tallennetaan ne tietokantaan käyttäen game_id parametria
    for maa in valitut_maat:
        sql = f"insert into kadonneet_lapset (game_id, country_name) values ('{game_id}', '{maa}')"
        kursori.execute(sql)

    yhteys.commit()
    return valitut_maat


# Funktio /help-komennolle
def help_komento(game_id):
    kursori = yhteys.cursor()

    # Haetaan kaikki EU-maat käyttämällä valmista funktiota (vältetään koodin toistoa)
    kaikki_maat = hae_eu_maat()
    # Muutetaan takaisin isoiksi kirjaimiksi näyttöä varten
    kaikki_maat = [maa.title() for maa in kaikki_maat]

    # Haetaan maat joissa pelaaja on jo käynyt
    sql = f"select country_name from käydyt_maat where game_id = '{game_id}' and käyty = 1"
    kursori.execute(sql)
    käydyt_maat = []
    for rivi in kursori.fetchall():
        käydyt_maat.append(rivi[0].lower())

    # Tulostetaan kaikki EU-maat ja merkitään mitkä on jo käyty
    print("""Kaikki EU-maat:
    """)
    for maa in kaikki_maat:
        if maa.lower() in käydyt_maat:
            merkki = "x"
        else:
            merkki = " "
        print(f"{maa} [{merkki}]")


# Funktio joka tarkistaa monta poikasta on löydetty
def kadonneet_lapset_määrä(game_id):
    sql = f"select count(*) from kadonneet_lapset where game_id = '{game_id}' and löydetyt_lapset = 1"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    löydetyt = kursori.fetchone()[0]
    return löydetyt


# Funktio, joka tarkistaa onko lapsi löydetty valitusta maasta
def tarkista_maa(game_id, maa):
    sql = f"select löydetyt_lapset from kadonneet_lapset where game_id = '{game_id}' and country_name = '{maa}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()

    # Päivitetään, että lapsi on löytynyt
    if tulos and tulos[0] == 0:
        sql = f"update kadonneet_lapset set löydetyt_lapset = 1 where game_id = '{game_id}' and country_name = '{maa}'"
        kursori.execute(sql)
        yhteys.commit()
        return True
    return False


# Funktio, joka merkitsee tietyn maan käydyksi tietokannassa
def merkitse_käydyksi(game_id, maa):
    sql = f"insert into käydyt_maat (game_id, country_name, käyty) values ('{game_id}', '{maa}', 1)"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    yhteys.commit()


# Funktio lentävä apina animaatiolle
def lentävä_animaatio():
    lentävä_kuvat = [
        """
                                                 *@@-=#:
                                                  #%@%=@+
                                                 +*@@@#@*:
                      =+.:@@=                  +-@@@@@@@@@+
                     :..%@@@-:@+               *@@@@@@@@@@%
                    :%@@@@@@@@@@@#            :%@@@@@@@@@@##
                   #@@@@@@@@@@@@@@@@+:        #@@@@@@@@@@@=
                    #@@@@@@@@@@@@@@@@@@+      @@@@@@@@@@#
                      +@@@@@@@@@@@@@@@@@@@@@@-:@@@@@@@@:
                       :+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                          %@@@@@@@@@@@@@@@@@@@@@@@@@-   :%@@@%
                            :%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+
                                -#@@@@@@@@@@@@@@@@@@@@@@@@@@@@=
                                     *@@=: %@@@@@@@@@@@@@@@@@%
                                          %@@@@@@@@@@@@@@@ :
                                         #@@@@@%*#- %@@#@@*
                                        =@@@@@@@@@@#+@@+#@@@@*:
                                       :@@@@@@@@@@@@:@@@@*%#@@@@@-
                                      :@@*: %#@@@@+  =  *@@    +@@-
                            :%@@-     %@#-   *@@@@@%%*:   =@@-  *%+
                           #%**   :%@@:      %@@#+*-#@@#  #+
                           =@@#@@@%=           =%@@% -=@*
        """,
        """

                                                   *@@@@@@@@@@%
                        :%@@@@@@@@@@@#            :%@@@@@@@@@@##
                       #@@@@@@@@@@@@@@@@+:        #@@@@@@@@@@@=@#
                      #@@@@@@@@@@@@@@@@@@@@+      @@@@@@@@@@# @@@+
                    +@@@@@@@@@@@@@@@@@@@@@@@@@@@@-:@@@@@@@@: +@@+
                     +@@@@@+ :+@@@@@@@@@@@@@@@@@@@@@@@@@@@
                     =.:@@@=  %@@@@@@@@@@@@@@@@@@@@@@@@@-   :%@@@%
                      .:@       :%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+
                                    -#@@@@@@@@@@@@@@@@@@@@@@@@@@@@=
                                         *@@=: %@@@@@@@@@@@@@@@@@%
                                              %@@@@@@@@@@@@@@@ :
                                             #@@@@@%*#- %@@#@@*
                                            =@@@@@@@@@@#+@@+#@@@@*:
                                           :@@@@@@@@@@@@:@@@@*%#@@@@@-
                                          :@@*: %#@@@@+  =  *@@    +@@-
                                          %@#-   *@@@@@%%*:   =@@-  *%+
                                      :%@@:      %@@#+*-#@@#  #+
                          @@@=@@@@#@@@%=          =%@@% -=@*

        """
    ]

    i = 0
    kierrokset = 3

    while i < kierrokset:
        for kuva in lentävä_kuvat:
            tyhjennä()
            print(kuva)
            time.sleep(0.5)
        i += 1
    return


# Funktio pelin lopettamiseen
def lopeta_peli(game_id):

    löydetyt_lapset = kadonneet_lapset_määrä(game_id)
    print(f"""
    PELI LOPETETTU
    Löysit {löydetyt_lapset}/10 lasta.
    Kiitos pelaamisesta!
    Toivottavasti tulet pian takaisin!
    Äitiapina toivottaa sinulle hyvää päivän jatkoa.
    """)
    yhteys.close()  # Suljetaan tietokantayhteys
    exit()  # Lopetetaan ohjelma


# Pääpeli
game_id = hae_game_id(nimimerkki)
eu_maat = hae_eu_maat()
arvo_apinoiden_maat(game_id)

löydetyt_lapset = kadonneet_lapset_määrä(game_id)

while löydetyt_lapset < 10:
    print("""
    Mihin maahan haluaisit lentää? (Kirjoita maan nimi englanniksi. /help näyttää kaikki EU-maat. /lopeta lopettaa pelin.)
    """)
    maa = input("""
    Valitse maa: """).strip()

    # Tarkista lopetuskomento
    if maa.lower() == "/lopeta":
        varmistus = input("""
    Haluatko varmasti lopettaa pelin? (kyllä/ei): """).strip().lower()
        if varmistus == "kyllä":
            lopeta_peli(game_id)
        else:
            print("""
    Jatketaan peliä!""")
            continue

    if maa.lower() == "/help":
        help_komento(game_id)
    else:
        if maa.lower() not in eu_maat:
            print(f"""
    {maa} ei ole EU-maa tai se on kirjoitettu väärin. Valitse toinen maa.""")
        else:
            sql = f"select count(*) from käydyt_maat where game_id = '{game_id}' and lower(country_name) = '{maa.lower()}'"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            tulos = kursori.fetchone()

            if tulos[0] == 0:
                lentävä_animaatio()

                löytyi = tarkista_maa(game_id, maa)

                merkitse_käydyksi(game_id, maa)

                löydetyt_lapset = kadonneet_lapset_määrä(game_id)

                if löytyi:
                    print(f"""
    Löysit kadonneen apinanpoikasen! Löydetty {löydetyt_lapset}/10.""")
                else:
                    print(f"""
    Ei löytynyt poikasta. Tähän mennessä löydetty {löydetyt_lapset}/10.""")
            else:
                print("""
    Olet jo käynyt siellä. Valitse toinen maa.""")

    if löydetyt_lapset == 10:
        print("""
    JIPPII!! Kaikki kadonneet poikaset on löydetty!

    FUN FACT! EU-maiden välisen lennon päästöt ovat keskimäärin noin ... per matkustaja.
    Tässä pelissä ei kuitenkaan synny päästöjä, koska lentävä apina on satuhahmo.
    Hän liikkuu ympäristöystävällisesti mielikuvituksen siivin!
    """)
        jatka()

        vinkkaava_kuvat = [
            """
                        ..::+*******+.:..               
                    .:********************:.            
                .******************************.        
           :+********=---------++---------=********+:   
         :***+++***=------------------------=***+++***: 
        -**==+++**------++=----------=++------**++++=**-
        **=--=++*+-----####----------####-----+*+==---**
        **=--=+**+----#----#--------#----#----+**+=---**
        -**+++****-----####----------####-----****++=**-
        .:*********=--------=#*--+#+--------=*********:.
           :+*******------------------------*******+:.. 
            .******----------+*==*+----------******.    
             +****=---------#*++++*#---------=*****.     
               :****+=+++=---*#**#*---=+++=+****:.      
                   ..=++++**++====++***+++=....         

            ,--. ,--.,--.,--.  ,--.                 
            |  .'   /`--'`--',-'  '-. ,---.  ,---.  
            |  .   ' ,--.,--.'-.  .-'| .-. |(  .-'  
            |  |\   \|  ||  |  |  |  ' '-' '.-'  `) 
            `--' '--'`--'`--'  `--'   `---' `----'     
        """,

            """
                            ..::+*******+.:..                                    ....-+-    
                        .:********************:.                           .-*%@@@@%%%.@.   
                    .******************************.                ...#@@@@@**@@@@*  .@.   
               :+********=---------++---------=********+:        .+#%#@@@@@@+-.%@@@+ .%=    
             :***+++***=------------------------=***+++***:      .@-#%=::@@@@@.-#@@=-@:.    
            -**==+++**------++=----------=++------**++++=**-     :@@=*@#*.%@@%%@@@@@+       
            **=--=++*+-----####-------------------+*+==---**     .@@@*%**#@%@@@@@%.         
            **=--=+**+----#----#--------######----+**+=---**      @@@@@@:.....:%@-          
            -**+++****-----####-------------------****++=**-     =@@#-%.       .#:          
            .:*********=--------=#*--+#+--------=*********:.  .%%=:*%@@.       .%@*-.       
               :+*******------------------------*******+:..  .+@@@@@@%+.      .#*#@@@@:     
                .******----------+*==*+----------******.     -@@@@@@@@@.     :@@@@@@#:=%:   
                 +****=---------#*++++*#---------=*****.    .@@@@@@@@@:     .:=-*@@%=..     
                   :****+=+++=---*#**#*---=+++=+****:.	*@@@@@@@@%      .=:.      
                       ..=++++**++====++***+++=....		   ...........                      

                ,--. ,--.,--.,--.  ,--.                 
                |  .'   /`--'`--',-'  '-. ,---.  ,---.  
                |  .   ' ,--.,--.'-.  .-'| .-. |(  .-'  
                |  |\   \|  ||  |  |  |  ' '-' '.-'  `) 
                `--' '--'`--'`--'  `--'   `---' `----'  
            """,

            """
                            ..::+*******+.:..                                    ....-+-    
                        .:********************:.                           .-*%@@@@%%%.@.   
                    .******************************.                ...#@@@@@**@@@@*  .@.   
               :+********=---------++---------=********+:        .+#%#@@@@@@+-.%@@@+ .%=    
             :***+++***=------------------------=***+++***:      .@-#%=::@@@@@.-#@@=-@:.    
            -**==+++**------++=----------=++------**++++=**-     :@@=*@#*.%@@%%@@@@@+       
            **=--=++*+-----####----------####-----+*+==---**     .@@@*%**#@%@@@@@%.         
            **=--=+**+----#----#--------#----#----+**+=---**      @@@@@@:.....:%@-          
            -**+++****-----####----------####-----****++=**-     =@@#-%.       .#:          
            .:*********=--------=#*--+#+--------=*********:.  .%%=:*%@@.       .%@*-.       
               :+*******------------------------*******+:..  .+@@@@@@%+.      .#*#@@@@:     
                .******----------+*==*+----------******.     -@@@@@@@@@.     :@@@@@@#:=%:   
                 +****=---------#*++++*#---------=*****.    .@@@@@@@@@:     .:=-*@@%=..     
                   :****+=+++=---*#**#*---=+++=+****:.	*@@@@@@@@%      .=:.      
                       ..=++++**++====++***+++=....		   ...........                      

                ,--. ,--.,--.,--.  ,--.                 
                |  .'   /`--'`--',-'  '-. ,---.  ,---.  
                |  .   ' ,--.,--.'-.  .-'| .-. |(  .-'  
                |  |\   \|  ||  |  |  |  ' '-' '.-'  `) 
                `--' '--'`--'`--'  `--'   `---' `----'  
            """,
        ]

        for kuva in vinkkaava_kuvat:
            tyhjennä()
            print(kuva)
            time.sleep(1)
        break