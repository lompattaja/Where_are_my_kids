import os
import mysql.connector
import random
import time


def clear():
    # Detect operating system and run the right command
    os.system('cls' if os.name == 'nt' else 'clear')


def crying_ape(prompt: str):
    frames = [
        "(T_T)",
        "(T^T)",
        "(T_T)",
        "(T~T)",
        "(T_T)  *",
        "(T^T)  **",
        "(T~T)  ***",
    ]

    for i in range(30):  # repeat animation
        clear()
        print(frames[i % len(frames)])
        print("\n" + prompt)
        time.sleep(0.15)


def connect_to_database():
    """Yhdistä tietokantaan turvallisesti"""
    try:
        yhteys = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            database='flight_game',
            user='root',
            password='nooanooa',
            autocommit=True,
        )
        return yhteys
    except mysql.connector.Error as err:
        print(f"Tietokantayhteyden muodostaminen epäonnistui: {err}")
        return None


def print_story():
    """Tulosta pelin tarina"""
    print("""Eräänä päivänä lentävä apina ja hänen kymmenen pientä lastaan olivat matkalla takaisin kotiin, Suomeen.
Taivas yllättäen tummui, ja heidän ylleen nousi raivokas myrsky.

Kovat tuulet tarttuivat pieniin apinanpoikasiin ja lennättivät heidät kauas, ympäri Euroopan maita.
Äitiapina kauhistui. Hän yritti tavoittaa lapsiaan, mutta tuulen voima oli liian suuri.
Kun myrsky vihdoin tyyntyi, jäljellä oli vain hiljainen taivas ja äidin sydäntä painava huoli.
Lentävä apina keräsi rohkeutensa ja hänen oli lähdettävä etsimään kadonneita lapsiaan.
Jokainen niistä saattoi olla missä päin Eurooppaa tahansa.

Vain sinä voisit auttaa häntä tässä vaikeassa tilanteessa.
Auttaisitko häntä pelaaja?""")


def get_european_countries(yhteys):
    """Hae kaikki Euroopan maat tietokannasta"""
    try:
        kursori = yhteys.cursor()

        # Kokeile eri kenttänimiä - flight_game tietokannassa kentät voivat olla eri nimiset
        try:
            # Ensimmäinen yritys: country_name
            kursori.execute("SELECT iso_country, country_name FROM country WHERE continent = 'EU'")
            maat = kursori.fetchall()
        except mysql.connector.Error as err:
            if "Unknown column 'country_name'" in str(err):
                try:
                    # Toinen yritys: name
                    kursori.execute("SELECT iso_country, name FROM country WHERE continent = 'EU'")
                    maat = kursori.fetchall()
                except mysql.connector.Error as err2:
                    if "Unknown column 'name'" in str(err2):
                        try:
                            # Kolmas yritys: pelkkä iso_country (käytetään sitä myös nimeksi)
                            kursori.execute("SELECT iso_country, iso_country FROM country WHERE continent = 'EU'")
                            maat = kursori.fetchall()
                        except mysql.connector.Error as err3:
                            # Jos mikään ei toimi, kokeile ilman continent-ehtoa
                            try:
                                kursori.execute("SELECT iso_country, iso_country FROM country LIMIT 50")
                                maat = kursori.fetchall()
                                print("Varoitus: Käytetään kaikkia maita, koska continent-kenttää ei löydy")
                            except mysql.connector.Error as err4:
                                print(f"Virhe: Ei voitu hakea maita tietokannasta. Tarkista country-taulun rakenne.")
                                print(f"Virhe: {err4}")
                                kursori.close()
                                return []
                    else:
                        raise err2
            else:
                raise err

        kursori.close()

        # Jos ei löydy maita, yritä hakea kaikki maat
        if not maat:
            print("Varoitus: Euroopan maita ei löytynyt, haetaan kaikki maat...")
            try:
                kursori = yhteys.cursor()
                kursori.execute("SELECT iso_country, iso_country FROM country LIMIT 47")
                maat = kursori.fetchall()
                kursori.close()
            except mysql.connector.Error as err:
                print(f"Virhe maiden hakemisessa: {err}")
                return []

        return maat

    except mysql.connector.Error as err:
        print(f"Virhe maiden hakemisessa: {err}")
        return []


def save_child_locations(yhteys, kayttajanimi, lapsi_sijainnit):
    """Tallenna lasten sijainnit tietokantaan"""
    try:
        kursori = yhteys.cursor()

        # Poista vanhat sijainnit (jos pelaaja aloittaa uuden pelin)
        kursori.execute("DELETE FROM child_locations WHERE screen_name = %s", (kayttajanimi,))

        # Tallenna uudet sijainnit
        for lapsi_numero, (iso_country, country_name) in enumerate(lapsi_sijainnit, 1):
            kursori.execute(
                "INSERT INTO child_locations (screen_name, child_number, iso_country, country_name, found) VALUES (%s, %s, %s, %s, %s)",
                (kayttajanimi, lapsi_numero, iso_country, country_name, False)
            )

        kursori.close()
        return True
    except mysql.connector.Error as err:
        # Jos child_locations taulu ei ole olemassa, luodaan se
        if "doesn't exist" in str(err):
            try:
                print("Luodaan child_locations taulu...")
                kursori = yhteys.cursor()
                kursori.execute("""
                                CREATE TABLE child_locations
                                (
                                    id           INT PRIMARY KEY AUTO_INCREMENT,
                                    screen_name  VARCHAR(50)  NOT NULL,
                                    child_number INT          NOT NULL,
                                    iso_country  VARCHAR(2)   NOT NULL,
                                    country_name VARCHAR(100) NOT NULL,
                                    found        BOOLEAN DEFAULT FALSE
                                )
                                """)

                # Tallenna sijainnit uuteen tauluun
                for lapsi_numero, (iso_country, country_name) in enumerate(lapsi_sijainnit, 1):
                    kursori.execute(
                        "INSERT INTO child_locations (screen_name, child_number, iso_country, country_name, found) VALUES (%s, %s, %s, %s, %s)",
                        (kayttajanimi, lapsi_numero, iso_country, country_name, False)
                    )

                kursori.close()
                print("child_locations taulu luotu ja sijainnit tallennettu!")
                return True

            except mysql.connector.Error as create_err:
                print(f"Virhe taulun luomisessa: {create_err}")
                return False
        else:
            print(f"Virhe lasten sijaintien tallentamisessa: {err}")
            return False


def load_child_locations(yhteys, kayttajanimi):
    """Lataa lasten sijainnit tietokannasta"""
    try:
        kursori = yhteys.cursor()
        kursori.execute(
            "SELECT child_number, iso_country, country_name, found FROM child_locations WHERE screen_name = %s ORDER BY child_number",
            (kayttajanimi,)
        )
        sijainnit = kursori.fetchall()
        kursori.close()
        return sijainnit
    except mysql.connector.Error as err:
        print(f"Virhe lasten sijaintien lataamisessa: {err}")
        return []


def generate_child_locations(yhteys, kayttajanimi, on_uusi_peli):
    """Generoi tai lataa lasten sijainnit"""
    if not on_uusi_peli:
        # Lataa vanhan pelin sijainnit
        tallennetut_sijainnit = load_child_locations(yhteys, kayttajanimi)
        if tallennetut_sijainnit:
            print(f"\nLadataan vanhan pelin sijainnit...")
            lapsi_sijainnit = []
            for lapsi_numero, iso_country, country_name, found in tallennetut_sijainnit:
                lapsi_sijainnit.append((iso_country, country_name, found))
            return lapsi_sijainnit

    # Luo uudet sijainnit
    print(f"\nGeneroidaan uudet sijainnit lapsille...")
    euroopan_maat = get_european_countries(yhteys)

    if len(euroopan_maat) < 10:
        print("Virhe: Tietokannassa ei ole tarpeeksi Euroopan maita!")
        return []

    # Arvo 10 satunnaista maata
    valitut_maat = random.sample(euroopan_maat, 10)
    lapsi_sijainnit = [(iso_country, country_name, False) for iso_country, country_name in valitut_maat]

    # Tallenna sijainnit tietokantaan
    if save_child_locations(yhteys, kayttajanimi, valitut_maat):
        print("Lasten sijainnit generoitu ja tallennettu!")
    else:
        print("Virhe sijaintien tallentamisessa!")

    return lapsi_sijainnit


def flying_animation():
    """Animaatio lentävästä apinasta pilvien ohitse"""
    frames = [
        "                  ☁️              ☁️",
        "         🐒    ☁️                  ☁️",
        "           🐒 ☁️                      ☁️",
        "  ☁️         🐒        ☁️",
        "     ☁️        🐒         ☁️",
        "        ☁️       🐒",
        "           ☁️      🐒    ☁️",
        "              ☁️    🐒      ☁️",
        "                ☁️  🐒        ☁️",
        "                  ☁️🐒          ☁️",
    ]

    for i in range(20):  # toista animaatio
        clear()
        print("LENTÄMÄSSÄ...")
        print()
        print(frames[i % len(frames)])
        print()
        print("Äitiapina lentää määränpäähänsä...")
        time.sleep(0.2)


def get_country_ascii_art(country_name, lapsi_loydetty):
    """Palauta ASCII art maalle ja tieto löytyikö lapsi"""
    ascii_arts = {
        'ruotsi': {
            'art': """
    🏰 TUKHOLMAN VANHA KAUPUNKI 🏰

           ⛪️
          /|\\
         / | \\
        /  |  \\
       🏠🏠🏠🏠🏠
      🌊🌊🌊🌊🌊🌊
     🚢      🦆🦆
    """,
            'with_child': "🐒 LÖYSIT KADONNEESTA APINAPOIKASESTA! 🐒",
            'without_child': "Ei apinaa täällä... 😔"
        },

        'iso-britannia': {
            'art': """
    🇬🇧 BIG BEN - LONTOO 🇬🇧

         🕐
        |---|
        |   |
        |   |
        |   |
        |   |
     🏛️🏛️🏛️🏛️🏛️
    🚌     👑
    """,
            'with_child': "🐒 LÖYSIT KADONNEESTA APINAPOIKASESTA! 🐒",
            'without_child': "Ei apinaa täällä... 😔"
        },

        'ranska': {
            'art': """
    🇫🇷 EIFFEL-TORNI - PARIISI 🇫🇷

        ⭐
       /|\\
      / | \\
     /  |  \\
    |   |   |
    |   |   |
   🏛️🏛️🏛️🏛️🏛️
   🥐    🎨
    """,
            'with_child': "🐒 LÖYSIT KADONNEESTA APINAPOIKASESTA! 🐒",
            'without_child': "Ei apinaa täällä... 😔"
        },

        'espanja': {
            'art': """
    🇪🇸 SAGRADA FAMILIA - BARCELONA 🇪🇸

      ⛪️  ⛪️  ⛪️
     /|\\ /|\\ /|\\
    🏗️🏗️🏗️🏗️🏗️
    |  SAGRADA  |
    |  FAMILIA  |
   🌮    💃    🎭
    """,
            'with_child': "🐒 LÖYSIT KADONNEESTA APINAPOIKASESTA! 🐒",
            'without_child': "Ei apinaa täällä... 😔"
        },

        'default': {
            'art': f"""
    🌍 {country_name.upper()} 🌍

       🏛️  🏰  🏛️
      🌳🌳🌳🌳🌳
     🏠🏠🏠🏠🏠🏠
    🛤️  🚶‍♂️   🚗  🛤️
    """,
            'with_child': "🐒 LÖYSIT KADONNEESTA APINAPOIKASESTA! 🐒",
            'without_child': "Ei apinaa täällä... 😔"
        }
    }

    # Hae maan ASCII art tai käytä oletusta
    country_key = country_name.lower()
    art_data = ascii_arts.get(country_key, ascii_arts['default'])

    result = art_data['art']
    if lapsi_loydetty:
        result += f"\n{art_data['with_child']}"
    else:
        result += f"\n{art_data['without_child']}"

    return result


def list_european_countries(yhteys):
    """Listaa kaikki Euroopan maat"""
    maat = get_european_countries(yhteys)
    if not maat:
        print("Virhe: Euroopan maita ei voitu hakea tietokannasta!")
        return

    print("\n" + "=" * 50)
    print("EUROOPAN MAAT")
    print("=" * 50)

    for i, (iso_country, country_name) in enumerate(maat, 1):
        print(f"{i:2d}. {country_name} ({iso_country})")

    print("=" * 50)
    print(f"Yhteensä {len(maat)} maata")


def find_country_by_name(yhteys, syotetty_maa):
    """Etsi maa nimellä tai ISO-koodilla"""
    maat = get_european_countries(yhteys)

    # Normalisoi syöte
    syotetty_maa = syotetty_maa.lower().strip()

    for iso_country, country_name in maat:
        if (syotetty_maa == country_name.lower() or
                syotetty_maa == iso_country.lower()):
            return iso_country, country_name

    return None, None


def mark_child_found(yhteys, kayttajanimi, iso_country):
    """Merkitse lapsi löydetyksi"""
    try:
        kursori = yhteys.cursor()
        kursori.execute(
            "UPDATE child_locations SET found = TRUE WHERE screen_name = %s AND iso_country = %s",
            (kayttajanimi, iso_country)
        )
        kursori.close()
        return True
    except mysql.connector.Error as err:
        print(f"Virhe lapsen merkitsemisessä löydetyksi: {err}")
        return False


def get_found_children_count(yhteys, kayttajanimi):
    """Hae löydettyjen lasten määrä"""
    try:
        kursori = yhteys.cursor()
        kursori.execute(
            "SELECT COUNT(*) FROM child_locations WHERE screen_name = %s AND found = TRUE",
            (kayttajanimi,)
        )
        tulos = kursori.fetchone()
        kursori.close()
        return tulos[0]
    except mysql.connector.Error as err:
        print(f"Virhe löydettyjen lasten laskemisessa: {err}")
        return 0


def is_child_in_country(yhteys, kayttajanimi, iso_country):
    """Tarkista onko lapsessa tietyssä maassa"""
    try:
        kursori = yhteys.cursor()
        kursori.execute(
            "SELECT COUNT(*) FROM child_locations WHERE screen_name = %s AND iso_country = %s",
            (kayttajanimi, iso_country)
        )
        tulos = kursori.fetchone()
        kursori.close()
        return tulos[0] > 0
    except mysql.connector.Error as err:
        print(f"Virhe lapsen etsimisessä: {err}")
        return False


def play_main_game(yhteys, kayttajanimi):
    """Pelin pääsilmukka"""
    print("\n" + "=" * 60)
    print("ETSINTÄ ALKAA!")
    print("=" * 60)
    print("Olet nyt Suomessa. Äitiapina on valmis lentämään etsimään lapsiaan.")
    print("💡 Vinkki: Kirjoita '/help' nähdäksesi kaikki Euroopan maat")

    # Näytä pelaajan pistemäärä
    pistemäärä = get_completion_score(yhteys, kayttajanimi)
    if pistemäärä > 0:
        print(f"🏆 Läpäisypisteitäsi: {pistemäärä}")
        if pistemäärä >= 10:
            print("👑 MESTARIN TASO SAAVUTETTU!")

    # Tarkista onko pelaajalla jo lapsia löytynyt (jatkuva peli)
    alkuperaiset_loydetyt = get_found_children_count(yhteys, kayttajanimi)
    if alkuperaiset_loydetyt > 0:
        print(f"📊 Jatkat peliä - sinulla on jo {alkuperaiset_loydetyt}/10 lasta löydetty")

    while True:
        loydetyt_lapset = get_found_children_count(yhteys, kayttajanimi)

        print(f"\n📊 Edistyminen: {loydetyt_lapset}/10 lasta löydetty")

        if loydetyt_lapset >= 10:
            # PELI LÄPÄISTY!
            clear()

            # Päivitä läpäisypisteet
            uusi_pistemäärä = update_completion_score(yhteys, kayttajanimi)

            print("=" * 60)
            print("🎉 ONNITTELUT! LÖYSIT KAIKKI LAPSET! 🎉")
            print("=" * 60)
            print("Äitiapina on onnellinen - kaikki hänen lapsensa ovat turvassa!")
            print("Perhe on jälleen yhdessä!")

            # Näytä voitto ASCII art
            victory_art = victory_ascii_art().format(uusi_pistemäärä)
            print(victory_art)

            # Tarkista saavutettiinko 10 läpäisyä
            if uusi_pistemäärä == 10:
                input("\nPaina enter nähdäksesi erikoisyllätyksen...")
                champion_celebration_animation()
                clear()
                print("\n🎖️ OLET SAAVUTTANUT MESTARIN TASON! 🎖️")
                print("Tämä oli 10. läpäisysi - uskomaton saavutus!")

            elif uusi_pistemäärä > 10:
                print(f"\n👑 MESTARI! Tämä oli {uusi_pistemäärä}. läpäisysi!")

            print(f"\n🏆 Sait yhden läpäisypisteen! Yhteensä: {uusi_pistemäärä}")

            # Kysyy haluaako pelata uudelleen
            print("\n" + "=" * 60)
            uusi_peli = input("Haluatko pelata uudelleen? (k/e): ").lower().strip()

            if uusi_peli in ['k', 'kyllä', 'yes', 'y']:
                # Nollaa pelin tila ja aloita alusta
                if reset_game_progress(yhteys, kayttajanimi):
                    clear()
                    print("🔄 Aloitetaan uusi seikkailu!")
                    print("Myrsky iskee jälleen ja hajottaa perhe...")
                    input("Paina enter jatkaaksesi...")

                    # Generoi uudet sijainnit
                    lapsi_sijainnit = generate_child_locations(yhteys, kayttajanimi, True)
                    if not lapsi_sijainnit:
                        print("Virhe: Uutta peliä ei voitu aloittaa!")
                        break

                    clear()
                    print("🌪️ Uusi myrsky, uudet sijainnit - seikkailu jatkuu!")
                    continue
                else:
                    print("Virhe uuden pelin aloittamisessa.")
                    break
            else:
                print("\n👋 Kiitos pelaamisesta! Näkemiin!")
                break

        # Kysy minne mennä
        print(f"\n🌍 Minne Euroopan maahan haluat mennä?")
        vastaus = input("Syötä maan nimi (tai /help listalle): ").strip()

        # Tarkista komennot
        if vastaus.lower() == '/help':
            list_european_countries(yhteys)
            continue

        if not vastaus:
            print("Syötä maan nimi!")
            continue

        # Etsi maa
        iso_country, country_name = find_country_by_name(yhteys, vastaus)

        if not iso_country:
            print(f"❌ Maata '{vastaus}' ei löytynyt. Tarkista kirjoitusasu tai käytä /help")
            continue

        # Lentämisanimaatio
        print(f"\n🛫 Lentämässä maahan: {country_name}")
        flying_animation()

        clear()

        # Tarkista onko lapsista tässä maassa
        lapsi_maassa = is_child_in_country(yhteys, kayttajanimi, iso_country)

        # Näytä ASCII art
        print("=" * 60)
        print(f"SAAVUIT MAAHAN: {country_name.upper()}")
        print("=" * 60)

        ascii_art = get_country_ascii_art(country_name, lapsi_maassa)
        print(ascii_art)

        if lapsi_maassa:
            # Merkitse lapsi löydetyksi
            mark_child_found(yhteys, kayttajanimi, iso_country)
            loydetyt_lapset += 1
            print(f"\n🎉 Mahtavaa! Löysit yhden lapsistasi!")
            print(f"📊 Nyt olet löytänyt {loydetyt_lapset}/10 lasta")
        else:
            print(f"\n😔 Ei löytynyt lasta täältä. Jatka etsimistä!")

        input("\nPaina enter jatkaaksesi...")
        clear()


def check_user_exists(yhteys, kayttajanimi):
    """Tarkista onko käyttäjä jo olemassa tietokannassa"""
    try:
        kursori = yhteys.cursor()
        kursori.execute("SELECT COUNT(*) FROM game WHERE screen_name = %s", (kayttajanimi,))
        tulos = kursori.fetchone()
        kursori.close()
        return tulos[0] > 0
    except mysql.connector.Error as err:
        print(f"Virhe tietokannassa: {err}")
        return False


def update_completion_score(yhteys, kayttajanimi):
    """Päivitä pelaajan läpäisypisteet"""
    try:
        kursori = yhteys.cursor()

        # Tarkista onko completions-kenttä olemassa
        try:
            # Lisää läpäisypiste
            kursori.execute(
                "UPDATE game SET completions = completions + 1 WHERE screen_name = %s",
                (kayttajanimi,)
            )

            # Hae uusi pistemäärä
            kursori.execute(
                "SELECT completions FROM game WHERE screen_name = %s",
                (kayttajanimi,)
            )
            tulos = kursori.fetchone()
            pistemäärä = tulos[0] if tulos else 1

        except mysql.connector.Error as col_err:
            if "Unknown column 'completions'" in str(col_err):
                # Completions-kenttä puuttuu, lisätään se
                print("Lisätään completions-kenttä tietokantaan...")
                kursori.execute("ALTER TABLE game ADD COLUMN completions INT DEFAULT 0")

                # Asetetaan tälle pelaajalle 1 piste
                kursori.execute(
                    "UPDATE game SET completions = 1 WHERE screen_name = %s",
                    (kayttajanimi,)
                )
                pistemäärä = 1
            else:
                raise col_err

        kursori.close()
        return pistemäärä

    except mysql.connector.Error as err:
        print(f"Virhe pistemäärän päivittämisessä: {err}")
        return 1


def get_completion_score(yhteys, kayttajanimi):
    """Hae pelaajan läpäisypisteet"""
    try:
        kursori = yhteys.cursor()

        try:
            kursori.execute(
                "SELECT completions FROM game WHERE screen_name = %s",
                (kayttajanimi,)
            )
            tulos = kursori.fetchone()
            kursori.close()
            return tulos[0] if tulos else 0

        except mysql.connector.Error as col_err:
            if "Unknown column 'completions'" in str(col_err):
                # Completions-kenttä puuttuu, palautetaan 0
                kursori.close()
                return 0
            else:
                kursori.close()
                raise col_err

    except mysql.connector.Error as err:
        print(f"Virhe pistemäärän hakemisessa: {err}")
        return 0


def champion_celebration_animation():
    """Erikoisanimaatio 10 läpäisyn jälkeen"""
    frames = [
        """
    🎆🎆🎆 MESTARI! 🎆🎆🎆

         👑
        🐒✨
       /   \\
      🏆   🏆

    🎉🎊🎉🎊🎉🎊🎉🎊🎉
        """,
        """
    🎆🎆🎆 MESTARI! 🎆🎆🎆

         👑
        ✨🐒
       /   \\
      🏆   🏆

    🎊🎉🎊🎉🎊🎉🎊🎉🎊
        """,
        """
    🎆🎆🎆 MESTARI! 🎆🎆🎆

         👑
        🐒⭐
       /   \\
      🏆   🏆

    🎉🎊🎉🎊🎉🎊🎉🎊🎉
        """,
        """
    🎆🎆🎆 MESTARI! 🎆🎆🎆

         👑
        ⭐🐒✨
       /   \\
      🏆   🏆

    🎊🎉🎊🎉🎊🎉🎊🎉🎊
        """
    ]

    for i in range(25):  # toista animaatio
        clear()
        print(frames[i % len(frames)])
        print("\n🎖️  OLET SAAVUTTANUT MESTARIN TASON!  🎖️")
        print("10 PELIÄ LÄPÄISTY - USKOMATON SUORITUS!")
        print("\n🌟 Äitiapina on ikuisesti kiitollinen avustasi! 🌟")
        time.sleep(0.3)


def victory_ascii_art():
    """ASCII art pelin päättyessä"""
    return """
    🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉

           KIITOS AVUSTA!
        OLET OLLUT SUURI APU!

              👑
             😉🐒    <- Vinkkaa silmää
            /  |  \\
           🏆  |  🏆  <- Pokaali molemmissa käsissä
              / \\
             👟 👟

        ✨ KAIKKI LAPSET PELASTETTU! ✨

    🏆 Läpäisypisteitä yhteensä: {} 🏆

    🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
    """


def reset_game_progress(yhteys, kayttajanimi):
    """Nollaa pelin edistyminen uutta peliä varten"""
    try:
        kursori = yhteys.cursor()
        # Poista vanhat lasten sijainnit
        kursori.execute("DELETE FROM child_locations WHERE screen_name = %s", (kayttajanimi,))
        kursori.close()
        return True
    except mysql.connector.Error as err:
        print(f"Virhe pelin nollaamisessa: {err}")
        return False


def create_new_user(yhteys, kayttajanimi):
    """Luo uusi käyttäjä tietokantaan"""
    try:
        kursori = yhteys.cursor()

        try:
            # Yritä ensin ilman id:tä (olettaen että se on AUTO_INCREMENT)
            kursori.execute("INSERT INTO game (screen_name) VALUES (%s)", (kayttajanimi,))

        except mysql.connector.Error as insert_err:
            if "doesn't have a default value" in str(insert_err) and "id" in str(insert_err):
                # ID-kenttä ei ole AUTO_INCREMENT, generoidaan satunnainen ID
                import random
                random_id = random.randint(1, 999999)

                # Tarkista ettei ID ole jo käytössä
                kursori.execute("SELECT COUNT(*) FROM game WHERE id = %s", (random_id,))
                if kursori.fetchone()[0] > 0:
                    # Jos ID on käytössä, kokeile muutama kerta
                    for _ in range(10):
                        random_id = random.randint(1, 999999)
                        kursori.execute("SELECT COUNT(*) FROM game WHERE id = %s", (random_id,))
                        if kursori.fetchone()[0] == 0:
                            break

                # Lisää käyttäjä ID:n kanssa
                kursori.execute("INSERT INTO game (id, screen_name) VALUES (%s, %s)", (random_id, kayttajanimi))
            else:
                # Jokin muu virhe
                raise insert_err

        kursori.close()
        return True

    except mysql.connector.Error as err:
        print(f"Virhe käyttäjän luomisessa: {err}")
        return False


def get_user_progress(yhteys, kayttajanimi):
    """Hae käyttäjän edistyminen tietokannasta"""
    try:
        kursori = yhteys.cursor()
        # Tarkista onko pelaajalla tallennettuja lapsia
        kursori.execute("SELECT COUNT(*) FROM child_locations WHERE screen_name = %s", (kayttajanimi,))
        tulos = kursori.fetchone()
        kursori.close()
        return 1 if tulos[0] > 0 else 0  # Jos lapsia löytyy, peli on aloitettu
    except mysql.connector.Error as err:
        print(f"Virhe edistymisen hakemisessa: {err}")
        return 0


def handle_user_login(yhteys):
    """Käsittele käyttäjän sisäänkirjautuminen tai rekisteröityminen"""
    clear()

    while True:
        print("=" * 50)
        print("KÄYTTÄJÄTIETOJEN HALLINTA")
        print("=" * 50)

        vastaus = input("Oletko uusi käyttäjä? (k/e): ").lower().strip()

        if vastaus in ['k', 'kyllä', 'yes', 'y']:
            # Uusi käyttäjä
            print("\n--- Uuden käyttäjän luominen ---")
            while True:
                kayttajanimi = input("Syötä haluamasi nimimerkki: ").strip()

                if not kayttajanimi:
                    print("Nimimerkki ei voi olla tyhjä!")
                    continue

                if check_user_exists(yhteys, kayttajanimi):
                    print(f"Käyttäjänimi '{kayttajanimi}' on jo käytössä. Kokeile toista nimimerkkiä.")
                    continue

                # Luo uusi käyttäjä
                if create_new_user(yhteys, kayttajanimi):
                    print(f"Tervetuloa peliin, {kayttajanimi}!")
                    return kayttajanimi, 0  # uusi käyttäjä, edistyminen = 0
                else:
                    print("Virhe käyttäjän luomisessa. Yritä uudelleen.")

        elif vastaus in ['e', 'ei', 'no', 'n']:
            # Vanha käyttäjä
            print("\n--- Vanhan käyttäjän kirjautuminen ---")
            while True:
                kayttajanimi = input("Syötä nimimerkkisi: ").strip()

                if not kayttajanimi:
                    print("Nimimerkki ei voi olla tyhjä!")
                    continue

                if check_user_exists(yhteys, kayttajanimi):
                    edistyminen = get_user_progress(yhteys, kayttajanimi)
                    print(f"Tervetuloa takaisin, {kayttajanimi}!")
                    if edistyminen > 0:
                        print(f"Jatkat peliä vaiheesta {edistyminen}.")
                    return kayttajanimi, edistyminen
                else:
                    print(f"Käyttäjänimeä '{kayttajanimi}' ei löytynyt.")
                    uusi_yritys = input("Haluatko yrittää uudelleen? (k/e): ").lower().strip()
                    if uusi_yritys not in ['k', 'kyllä', 'yes', 'y']:
                        break

        else:
            print("Vastaa 'k' (kyllä) tai 'e' (ei).")
            continue


def main():
    """Pelin pääfunktio"""
    # Yhdistä tietokantaan
    yhteys = connect_to_database()
    if yhteys is None:
        print("Peliä ei voida käynnistää ilman tietokantayhteyttä.")
        return

    # Näytä pelin tarina
    print_story()

    # Odota pelaajan syötettä
    input("Paina enter jatkaaksesi: ")

    # Näytä itkevä apina -animaatio
    crying_ape("Äitiapina itkee kadonneita lapsiaan...")

    clear()

    # Käsittele käyttäjän kirjautuminen
    kayttajanimi, edistyminen = handle_user_login(yhteys)

    clear()
    print("=" * 50)
    print("SEIKKAILU ALKAA!")
    print("=" * 50)
    print(f"Pelaaja: {kayttajanimi}")

    # Generoi tai lataa lasten sijainnit
    on_uusi_peli = (edistyminen == 0)
    lapsi_sijainnit = generate_child_locations(yhteys, kayttajanimi, on_uusi_peli)

    if not lapsi_sijainnit:
        print("Virhe: Lasten sijainteja ei voitu luoda!")
        yhteys.close()
        return

    if on_uusi_peli:
        print("Aloitat uuden seikkailun!")
        print("\nMyrsky hajotti äitiapina ja hänen lapsensa ympäri Eurooppaa.")
        print("10 pientä apinanpoikasta odottaa pelastustaan eri maissa...")
    else:
        print(f"Jatkat vaiheesta: {edistyminen}")
        print("\nJatkat etsimään kadonneita lapsia sieltä, missä jäit...")

    # Näytä lasten sijainnit (vain kehittäjänäkymä - normaalisti piilotettu!)
    kehittaja_nakoyma = input("\nHaluatko nähdä lasten sijainnit? (VAIN TESTAUSTA VARTEN) (k/e): ").lower().strip()
    if kehittaja_nakoyma in ['k', 'kyllä', 'yes', 'y']:
        display_child_locations(lapsi_sijainnit)

    print("\nÄitiapina on valmis lähtemään etsimään lapsiaan...")
    print("Seikkailu jatkuu...")

    # Tähän voit jatkaa pelin varsinaista pelilogiikkaa

    # Muista sulkea tietokantayhteys lopuksi
    if yhteys:
        yhteys.close()


if __name__ == "__main__":
    main()