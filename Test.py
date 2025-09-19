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


# TIETOKANTAFUNKTIOT
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
    except mysql.connector.Error:
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


# PELIMEKANIIKKA FUNKTIOT
def get_european_countries(yhteys):
    """Hae kaikki Euroopan maat tietokannasta"""
    try:
        kursori = yhteys.cursor()

        # Kokeile eri kenttänimiä
        try:
            kursori.execute("SELECT iso_country, country_name FROM country WHERE continent = 'EU'")
            maat = kursori.fetchall()
        except mysql.connector.Error:
            try:
                kursori.execute("SELECT iso_country, name FROM country WHERE continent = 'EU'")
                maat = kursori.fetchall()
            except mysql.connector.Error:
                try:
                    kursori.execute("SELECT iso_country, iso_country FROM country WHERE continent = 'EU'")
                    maat = kursori.fetchall()
                except mysql.connector.Error:
                    # Jos mikään ei toimi, hae kaikki maat
                    kursori.execute("SELECT iso_country, iso_country FROM country LIMIT 47")
                    maat = kursori.fetchall()

        kursori.close()
        return maat if maat else []

    except mysql.connector.Error as err:
        print(f"Virhe maiden hakemisessa: {err}")
        return []


def save_child_locations(yhteys, kayttajanimi, lapsi_sijainnit):
    """Tallenna lasten sijainnit tietokantaan"""
    try:
        kursori = yhteys.cursor()

        # Poista vanhat sijainnit
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
                return True

            except mysql.connector.Error:
                return False
        else:
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
    except mysql.connector.Error:
        return []


def generate_child_locations(yhteys, kayttajanimi, on_uusi_peli):
    """Generoi tai lataa lasten sijainnit"""
    if not on_uusi_peli:
        # Lataa vanhan pelin sijainnit
        tallennetut_sijainnit = load_child_locations(yhteys, kayttajanimi)
        if tallennetut_sijainnit:
            print("Ladataan vanhan pelin sijainnit...")
            lapsi_sijainnit = []
            for lapsi_numero, iso_country, country_name, found in tallennetut_sijainnit:
                lapsi_sijainnit.append((iso_country, country_name, found))
            return lapsi_sijainnit

    # Luo uudet sijainnit
    print("Generoidaan uudet sijainnit lapsille...")
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


# YKSINKERTAINEN PELISILMUKKA
def play_simple_game(yhteys, kayttajanimi):
    """Yksinkertainen toimiva pelisilmukka"""
    print("\n" + "=" * 60)
    print("ETSINTÄ ALKAA!")
    print("=" * 60)
    print("Olet nyt Suomessa. Äitiapina on valmis lentämään etsimään lapsiaan.")
    print("💡 Vinkki: Kirjoita maan nimi tai 'lopeta' lopettaaksesi")

    # Hae maat listalle help-toimintoa varten
    maat = get_european_countries(yhteys)
    maan_nimet = [maa[1] for maa in maat] if maat else ['Saksa', 'Ranska', 'Italia', 'Espanja', 'Ruotsi']

    loydetyt_lapset = 0

    while loydetyt_lapset < 10:
        print(f"\n📊 Edistyminen: {loydetyt_lapset}/10 lasta löydetty")
        print(f"\n🌍 Minne Euroopan maahan haluat mennä?")

        vastaus = input("Syötä maan nimi (tai 'help'/'lopeta'): ").strip()

        if vastaus.lower() in ['lopeta', 'quit', 'exit']:
            print("\n👋 Kiitos pelaamisesta!")
            break

        if vastaus.lower() == 'help':
            print("\nSaatavilla olevat maat:")
            for i, maa in enumerate(maan_nimet[:20], 1):  # Näytä 20 ensimmäistä
                print(f"{i:2d}. {maa}")
            if len(maan_nimet) > 20:
                print(f"... ja {len(maan_nimet) - 20} muuta")
            continue

        if not vastaus:
            print("Syötä maan nimi!")
            continue

        # Simuloi lentämistä
        print(f"\n🛫 Lentämässä maahan: {vastaus}")
        print("✈️  🌤️  ☁️  🌤️  ✈️")
        time.sleep(1)

        # Simuloi löytämistä (25% mahdollisuus löytää lapsi)
        lapsi_loydetty = random.random() < 0.25

        clear()
        print("=" * 60)
        print(f"SAAVUIT MAAHAN: {vastaus.upper()}")
        print("=" * 60)

        if lapsi_loydetty:
            loydetyt_lapset += 1
            print("🎉 MAHTAVAA! LÖYSIT YHDEN LAPSISTASI! 🎉")
            print("🐒 Pieni apinapoika juoksee luoksesi itkien ilosta!")
            print(f"📊 Nyt olet löytänyt {loydetyt_lapset}/10 lasta")
        else:
            print("😔 Ei löytynyt lasta täältä...")
            print("🔍 Jatka etsimistä toisesta maasta!")

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
       🏆  |  🏆  <- Pokaali molemmissa käsissä
          / \\
         👟 👟

    ✨ KAIKKI LAPSET PELASTETTU! ✨
        """)
        print("Äitiapina ja hänen lapsensa ovat onnellisia!")


def main():
    """Pelin pääfunktio"""
    print("🚀 [DEBUG] Peli käynnistyy...")

    # Yhdistä tietokantaan
    yhteys = connect_to_database()
    if yhteys is None:
        print("Peliä ei voida käynnistää ilman tietokantayhteyttä.")
        return

    print("✅ [DEBUG] Tietokantayhteys OK")

    # Näytä pelin tarina
    print_story()

    # Odota pelaajan syötettä
    input("Paina enter jatkaaksesi: ")

    # Näytä itkevä apina -animaatio
    crying_ape("Äitiapina itkee kadonneita lapsiaan...")

    clear()

    # Käsittele käyttäjän kirjautuminen
    print("🔑 [DEBUG] Käyttäjän kirjautuminen...")
    kayttajanimi, edistyminen = handle_user_login(yhteys)
    print(f"👤 [DEBUG] Kirjautui: {kayttajanimi}, edistyminen: {edistyminen}")

    clear()
    print("=" * 50)
    print("SEIKKAILU ALKAA!")
    print("=" * 50)
    print(f"Pelaaja: {kayttajanimi}")

    # Generoi tai lataa lasten sijainnit
    on_uusi_peli = (edistyminen == 0)
    lapsi_sijainnit = generate_child_locations(yhteys, kayttajanimi, on_uusi_peli)

    if not lapsi_sijainnit:
        print("⚠️ Varoitus: Käytetään yksinkertaistettua peliä")

    if on_uusi_peli:
        print("Aloitat uuden seikkailun!")
        print("\nMyrsky hajotti äitiapina ja hänen lapsensa ympäri Eurooppaa.")
        print("10 pientä apinanpoikasta odottaa pelastustaan eri maissa...")
    else:
        print("Jatkat keskeneräistä peliäsi!")
        print("\nJatkat etsimään kadonneita lapsia sieltä, missä jäit...")

    print("\nÄitiapina on valmis lähtemään etsimään lapsiaan...")
    input("Paina enter aloittaaksesi pelin...")

    clear()

    # KÄYNNISTÄ PELI
    print("🎮 [DEBUG] Käynnistetään peli...")

    try:
        play_simple_game(yhteys, kayttajanimi)
        print("✅ [DEBUG] Peli päättyi normaalisti")
    except Exception as e:
        print(f"❌ [DEBUG] Virhe pelissä: {e}")
        import traceback
        traceback.print_exc()

    # Sulje tietokantayhteys
    if yhteys:
        yhteys.close()

    print("👋 [DEBUG] Ohjelma päättyy")


if __name__ == "__main__":
    main()