import os
import mysql.connector
import random
import time


def clear():
    """Tyhjennä näyttö"""
    os.system('cls' if os.name == 'nt' else 'clear')


def crying_ape(prompt: str):
    """Itkevä apina animaatio"""
    frames = [
        "(T_T)",
        "(T^T)",
        "(T_T)",
        "(T~T)",
        "(T_T)  *",
        "(T^T)  **",
        "(T~T)  ***",
    ]

    for i in range(30):
        clear()
        print(frames[i % len(frames)])
        print("\n" + prompt)
        time.sleep(0.15)


def connect_to_database():
    """Yhdistä MariaDB tietokantaan"""
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
    """Hae Euroopan maat airport-taulusta"""
    kursori = yhteys.cursor()
    kursori.execute(
        "SELECT DISTINCT iso_country FROM airport WHERE iso_country IS NOT NULL AND LENGTH(iso_country) = 2 ORDER BY iso_country")
    kaikki_maat = kursori.fetchall()

    # Euroopan maiden ISO-koodit
    euroopan_isot = {
        'AD', 'AL', 'AT', 'BA', 'BE', 'BG', 'BY', 'CH', 'CZ', 'DE', 'DK', 'EE',
        'ES', 'FI', 'FR', 'GB', 'GR', 'HR', 'HU', 'IE', 'IS', 'IT', 'LI', 'LT',
        'LU', 'LV', 'MC', 'MD', 'ME', 'MK', 'MT', 'NL', 'NO', 'PL', 'PT', 'RO',
        'RS', 'SE', 'SI', 'SK', 'SM', 'UA', 'XK', 'CY', 'TR'
    }

    # Suomenkieliset nimet
    suomeksi = {
        'AD': 'Andorra', 'AL': 'Albania', 'AT': 'Itävalta', 'BA': 'Bosnia ja Hertsegovina',
        'BE': 'Belgia', 'BG': 'Bulgaria', 'BY': 'Valko-Venäjä', 'CH': 'Sveitsi',
        'CZ': 'Tšekki', 'DE': 'Saksa', 'DK': 'Tanska', 'EE': 'Viro',
        'ES': 'Espanja', 'FI': 'Suomi', 'FR': 'Ranska', 'GB': 'Iso-Britannia',
        'GR': 'Kreikka', 'HR': 'Kroatia', 'HU': 'Unkari', 'IE': 'Irlanti',
        'IS': 'Islanti', 'IT': 'Italia', 'LI': 'Liechtenstein', 'LT': 'Liettua',
        'LU': 'Luxemburg', 'LV': 'Latvia', 'MC': 'Monaco', 'MD': 'Moldova',
        'ME': 'Montenegro', 'MK': 'Pohjois-Makedonia', 'MT': 'Malta',
        'NL': 'Alankomaat', 'NO': 'Norja', 'PL': 'Puola', 'PT': 'Portugali',
        'RO': 'Romania', 'RS': 'Serbia', 'SE': 'Ruotsi', 'SI': 'Slovenia',
        'SK': 'Slovakia', 'SM': 'San Marino', 'UA': 'Ukraina', 'XK': 'Kosovo',
        'CY': 'Kypros', 'TR': 'Turkki'
    }

    maat = []
    for (iso_code,) in kaikki_maat:
        if iso_code in euroopan_isot:
            maat.append((iso_code, suomeksi[iso_code]))

    kursori.close()
    return maat


def find_country_by_name(yhteys, syotetty_maa):
    """Etsi maa tietokannasta suomenkielisellä tai englanninkielisellä nimellä"""
    maat = get_european_countries(yhteys)
    syotetty_maa = syotetty_maa.lower().strip()

    # Etsi ISO-koodilla
    for iso_code, suomi_nimi in maat:
        if syotetty_maa == iso_code.lower():
            return iso_code, suomi_nimi

    # Etsi suomenkielisellä nimellä
    for iso_code, suomi_nimi in maat:
        if syotetty_maa == suomi_nimi.lower():
            return iso_code, suomi_nimi

    # Etsi osittaisella suomenkielisellä nimellä
    for iso_code, suomi_nimi in maat:
        if syotetty_maa in suomi_nimi.lower() or suomi_nimi.lower().startswith(syotetty_maa):
            return iso_code, suomi_nimi

    # Englanninkieliset synonyymit suomenkielisille nimille
    englanti_suomi_map = {
        'germany': 'saksa', 'france': 'ranska', 'spain': 'espanja', 'italy': 'italia',
        'sweden': 'ruotsi', 'norway': 'norja', 'denmark': 'tanska', 'finland': 'suomi',
        'poland': 'puola', 'belgium': 'belgia', 'netherlands': 'alankomaat',
        'austria': 'itävalta', 'switzerland': 'sveitsi', 'greece': 'kreikka',
        'portugal': 'portugali', 'hungary': 'unkari', 'czech': 'tšekki',
        'bulgaria': 'bulgaria', 'croatia': 'kroatia', 'slovakia': 'slovakia',
        'slovenia': 'slovenia', 'estonia': 'viro', 'latvia': 'latvia',
        'lithuania': 'liettua', 'united kingdom': 'iso-britannia', 'britain': 'iso-britannia',
        'ireland': 'irlanti', 'iceland': 'islanti'
    }

    # Etsi englanninkielisellä nimellä
    for englanti_nimi, suomi_vastine in englanti_suomi_map.items():
        if englanti_nimi in syotetty_maa or syotetty_maa in englanti_nimi:
            # Etsi suomenkielinen vastine
            for iso_code, suomi_nimi in maat:
                if suomi_vastine in suomi_nimi.lower():
                    return iso_code, suomi_nimi

    return None, None


def list_european_countries(yhteys):
    """Listaa kaikki Euroopan maat"""
    maat = get_european_countries(yhteys)

    print("\n" + "=" * 50)
    print("EUROOPAN MAAT")
    print("=" * 50)

    maat_jarjestetty = sorted(maat, key=lambda x: x[1])

    for i, (iso_country, country_name) in enumerate(maat_jarjestetty, 1):
        print(f"{i:2d}. {country_name} ({iso_country})")

    print("=" * 50)
    print(f"Yhteensä {len(maat)} Euroopan maata")


def save_found_child(yhteys, pelaaja_nimi, iso_country):
    """Tallenna löydetty lapsi tietokantaan"""
    kursori = yhteys.cursor()
    kursori.execute(
        "INSERT INTO child_locations (screen_name, child_number, iso_country, country_name, found) VALUES (%s, 1, %s, %s, TRUE) ON DUPLICATE KEY UPDATE found = TRUE",
        (pelaaja_nimi, iso_country, iso_country)
    )
    kursori.close()


def get_found_children_count(yhteys, pelaaja_nimi):
    """Laske montako lasta on löydetty"""
    kursori = yhteys.cursor()
    kursori.execute("SELECT COUNT(*) FROM child_locations WHERE screen_name = %s AND found = TRUE", (pelaaja_nimi,))
    tulos = kursori.fetchone()
    kursori.close()
    return tulos[0] if tulos else 0


def is_child_found(yhteys, pelaaja_nimi, iso_country):
    """Tarkista onko lapsi jo löydetty tästä maasta"""
    kursori = yhteys.cursor()
    kursori.execute(
        "SELECT found FROM child_locations WHERE screen_name = %s AND iso_country = %s",
        (pelaaja_nimi, iso_country)
    )
    tulos = kursori.fetchone()
    kursori.close()
    return tulos[0] if tulos else False


def check_user_exists(yhteys, kayttaja_nimi):
    """Tarkista onko käyttäjä olemassa"""
    try:
        kursori = yhteys.cursor()
        kursori.execute("SELECT COUNT(*) FROM game WHERE screen_name = %s", (kayttaja_nimi,))
        tulos = kursori.fetchone()
        kursori.close()
        return tulos[0] > 0
    except mysql.connector.Error:
        return False


def create_new_user(yhteys, kayttaja_nimi):
    """Luo uusi käyttäjä"""
    try:
        kursori = yhteys.cursor()

        try:
            kursori.execute("INSERT INTO game (screen_name) VALUES (%s)", (kayttaja_nimi,))
        except mysql.connector.Error as insert_err:
            if "doesn't have a default value" in str(insert_err) and "id" in str(insert_err):
                random_id = random.randint(1, 999999)
                kursori.execute("SELECT COUNT(*) FROM game WHERE id = %s", (random_id,))
                if kursori.fetchone()[0] > 0:
                    for _ in range(10):
                        random_id = random.randint(1, 999999)
                        kursori.execute("SELECT COUNT(*) FROM game WHERE id = %s", (random_id,))
                        if kursori.fetchone()[0] == 0:
                            break

                kursori.execute("INSERT INTO game (id, screen_name) VALUES (%s, %s)", (random_id, kayttaja_nimi))
            else:
                raise insert_err

        kursori.close()
        return True

    except mysql.connector.Error:
        return False


def get_user_progress(yhteys, kayttaja_nimi):
    """Hae käyttäjän edistyminen"""
    try:
        kursori = yhteys.cursor()
        kursori.execute("SELECT COUNT(*) FROM child_locations WHERE screen_name = %s", (kayttaja_nimi,))
        tulos = kursori.fetchone()
        kursori.close()
        return 1 if tulos[0] > 0 else 0
    except mysql.connector.Error:
        return 0


def handle_user_login(yhteys):
    """Käsittele käyttäjän kirjautuminen"""
    clear()

    while True:
        print("=" * 50)
        print("KÄYTTÄJÄTIETOJEN HALLINTA")
        print("=" * 50)

        vastaus = input("Oletko uusi käyttäjä? (k/e): ").lower().strip()

        if vastaus in ['k', 'kyllä', 'yes', 'y']:
            print("\n--- Uuden käyttäjän luominen ---")
            while True:
                nimi = input("Syötä haluamasi nimimerkki: ").strip()

                if not nimi:
                    print("Nimimerkki ei voi olla tyhjä!")
                    continue

                if check_user_exists(yhteys, nimi):
                    print(f"Käyttäjänimi '{nimi}' on jo käytössä.")
                    continue

                if create_new_user(yhteys, nimi):
                    print(f"Tervetuloa peliin, {nimi}!")
                    return nimi, 0
                else:
                    print("Virhe käyttäjän luomisessa.")

        elif vastaus in ['e', 'ei', 'no', 'n']:
            print("\n--- Vanhan käyttäjän kirjautuminen ---")
            while True:
                nimi = input("Syötä nimimerkkisi: ").strip()

                if not nimi:
                    print("Nimimerkki ei voi olla tyhjä!")
                    continue

                if check_user_exists(yhteys, nimi):
                    edistyminen = get_user_progress(yhteys, nimi)
                    print(f"Tervetuloa takaisin, {nimi}!")
                    return nimi, edistyminen
                else:
                    print(f"Käyttäjänimeä '{nimi}' ei löytynyt.")
                    uusi_yritys = input("Haluatko yrittää uudelleen? (k/e): ").lower().strip()
                    if uusi_yritys not in ['k', 'kyllä', 'yes', 'y']:
                        break
        else:
            print("Vastaa 'k' (kyllä) tai 'e' (ei).")


def play_simple_game(yhteys, pelaaja_nimi):
    """Yksinkertainen pelisilmukka"""
    print("\n" + "=" * 60)
    print("ETSINTÄ ALKAA!")
    print("=" * 60)
    print("Olet nyt Suomessa. Äitiapina on valmis lentämään etsimään lapsiaan.")
    print("💡 Vinkki: Kirjoita 'help' nähdäksesi kaikki maat")

    # Tarkista kuinka monta lasta on jo löydetty
    loydetyt_lapset = get_found_children_count(yhteys, pelaaja_nimi)

    while loydetyt_lapset < 10:
        print(f"\n📊 Edistyminen: {loydetyt_lapset}/10 lasta löydetty")
        print(f"\n🌍 Minne Euroopan maahan haluat mennä?")

        vastaus = input("Syötä maan nimi (tai 'help'/'lopeta'): ").strip()

        if vastaus.lower() in ['lopeta', 'quit', 'exit']:
            print("\n👋 Kiitos pelaamisesta!")
            break

        if vastaus.lower() == 'help':
            list_european_countries(yhteys)
            continue

        if not vastaus:
            print("Syötä maan nimi!")
            continue

        iso_country, country_name = find_country_by_name(yhteys, vastaus)

        if not iso_country:
            print(f"❌ Maata '{vastaus}' ei löytynyt!")
            print("💡 Kirjoita 'help' nähdäksesi kaikki maat")
            continue

        # Tarkista onko lapsi jo löydetty tästä maasta
        if is_child_found(yhteys, pelaaja_nimi, iso_country):
            print(f"ℹ️ Olet jo löytänyt lapsen maasta {country_name}!")
            continue

        print(f"\n🛫 Lentämässä maahan: {country_name}")
        print("✈️  🌤️  ☁️  🌤️  ✈️")
        time.sleep(1)

        lapsi_loydetty = random.random() < 0.25

        clear()
        print("=" * 60)
        print(f"SAAVUIT MAAHAN: {country_name.upper()}")
        print("=" * 60)

        if lapsi_loydetty:
            # Tallenna löydetty lapsi
            save_found_child(yhteys, pelaaja_nimi, iso_country)
            loydetyt_lapset = get_found_children_count(yhteys, pelaaja_nimi)
            print("🎉 MAHTAVAA! LÖYSIT YHDEN LAPSISTASI! 🎉")
            print("🐒 Pieni apinapoika juoksee luoksesi!")
            print(f"📊 Nyt olet löytänyt {loydetyt_lapset}/10 lasta")
        else:
            print("😔 Ei löytynyt lasta täältä...")
            print("🔍 Jatka etsimistä!")

        input("\nPaina enter jatkaaksesi...")
        clear()

    if loydetyt_lapset >= 10:
        print("\n" + "=" * 60)
        print("🎉 ONNITTELUT! LÖYSIT KAIKKI LAPSET! 🎉")
        print("=" * 60)
        print("""
    KIITOS AVUSTA!
    OLET OLLUT SUURI APU!

          👑
         😉🐒    <- Vinkkaa silmää
        /  |  \\
       🏆  |  🏆  <- Pokaali
          / \\
         👟 👟

    ✨ KAIKKI LAPSET PELASTETTU! ✨
        """)
        print("Äitiapina ja lapset ovat onnellisia!")


def main():
    """Pelin pääfunktio"""
    print("🚀 Peli käynnistyy...")

    yhteys = connect_to_database()
    if yhteys is None:
        print("Peliä ei voida käynnistää ilman tietokantayhteyttä.")
        return

    print("✅ Tietokantayhteys OK")

    print_story()
    input("Paina enter jatkaaksesi: ")

    crying_ape("Äitiapina itkee kadonneita lapsiaan...")
    clear()

    pelaaja_nimi, edistyminen = handle_user_login(yhteys)

    clear()
    print("=" * 50)
    print("SEIKKAILU ALKAA!")
    print("=" * 50)
    print(f"Pelaaja: {pelaaja_nimi}")

    if edistyminen == 0:
        print("Aloitat uuden seikkailun!")
        print("\nMyrsky hajotti äitiapina ja lapset ympäri Eurooppaa.")
        print("10 pientä apinanpoikasta odottaa pelastustaan...")
    else:
        print("Jatkat peliäsi!")

    print("\nÄitiapina on valmis lähtemään...")
    input("Paina enter aloittaaksesi pelin...")

    clear()

    try:
        play_simple_game(yhteys, pelaaja_nimi)
        print("✅ Peli päättyi normaalisti")
    except Exception as e:
        print(f"❌ Virhe pelissä: {e}")
        import traceback
        traceback.print_exc()

    if yhteys:
        yhteys.close()

    print("👋 Ohjelma päättyy")


if __name__ == "__main__":
    main()