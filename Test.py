import os
import mysql.connector
import random
import time
from typing import Optional, Tuple, List
from dataclasses import dataclass


@dataclass
class Country:
    """Maa-dataluokka - säilyttää maan tiedot"""
    iso_country: str
    name: str


class Database:
    """
    Tietokantayhteyden hallinta
    Vastaa yhteyden muodostamisesta MariaDB:hen ja taulujen alustamisesta
    """

    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        """
        Yhdistä MariaDB tietokantaan
        Käyttää flight_game tietokantaa joka sisältää lentoasematiedot
        """
        try:
            # Muodosta yhteys MariaDB:hen käyttäen annettuja tunnuksia
            self.connection = mysql.connector.connect(
                host='127.0.0.1',
                port=3306,
                database='flight_game',
                user='root',
                password='nooanooa',
                autocommit=True  # Autocommit päällä, jotta muutokset tallentuvat heti
            )

            # Alusta pelin tarvitsemat taulut
            self._init_tables()
            return True

        except mysql.connector.Error as err:
            print(f"❌ Tietokantayhteyden muodostaminen epäonnistui: {err}")
            return False

    def _init_tables(self):
        """
        Luo pelin tarvitsemat taulut jos niitä ei vielä ole
        - players: pelaajien tiedot
        - found_children: tieto löydetyistä lapsista per pelaaja
        """
        cursor = self.connection.cursor()

        # Luo pelaajataulu - tallentaa kaikki pelaajanimet
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS players
                       (
                           id
                           INT
                           AUTO_INCREMENT
                           PRIMARY
                           KEY,
                           username
                           VARCHAR
                       (
                           100
                       ) UNIQUE NOT NULL,
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                           )
                       """)

        # Luo taulu löydetyille lapsille
        # Unique key varmistaa ettei samaa lasta voi löytää kahdesti samasta maasta
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS found_children
                       (
                           id
                           INT
                           AUTO_INCREMENT
                           PRIMARY
                           KEY,
                           player_id
                           INT
                           NOT
                           NULL,
                           country_iso
                           VARCHAR
                       (
                           2
                       ) NOT NULL,
                           found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                           FOREIGN KEY
                       (
                           player_id
                       ) REFERENCES players
                       (
                           id
                       ),
                           UNIQUE KEY unique_player_country
                       (
                           player_id,
                           country_iso
                       )
                           )
                       """)

        cursor.close()

    def close(self):
        """Sulje tietokantayhteys ohjelman lopussa"""
        if self.connection:
            self.connection.close()


class CountryManager:
    """
    Maiden hallinta - hakee maat suoraan tietokannasta
    Käyttää olemassa olevaa country-taulua joka sisältää kaikki maailman maat
    """

    def __init__(self, db: Database):
        self.db = db
        self.countries_cache = None  # Välimuisti maille, ettei tarvitse hakea joka kerta

    def get_european_countries(self) -> List[Country]:
        """
        Hae kaikki Euroopan maat country-taulusta
        Palauttaa listan Country-objekteja
        """
        # Jos maat on jo haettu kerran, palauta välimuistista
        if self.countries_cache:
            return self.countries_cache

        cursor = self.db.connection.cursor()

        # Hae Euroopan maat (continent = 'EU')
        # Järjestä aakkosjärjestykseen nimen mukaan
        cursor.execute("""
                       SELECT iso_country,
                              name
                       FROM country
                       WHERE continent = 'EU'
                       ORDER BY name ASC
                       """)

        results = cursor.fetchall()
        cursor.close()

        # Muunna tulokset Country-objekteiksi ja tallenna välimuistiin
        self.countries_cache = [
            Country(iso_country=row[0], name=row[1])
            for row in results
        ]

        return self.countries_cache

    def find_country(self, search_term: str) -> Optional[Country]:
        """
        Etsi maa hakusanalla
        Tukee hakua ISO-koodilla tai maan nimellä (myös osittainen)
        """
        search_term = search_term.strip()
        countries = self.get_european_countries()

        # 1. Yritä ensin löytää tarkalla ISO-koodilla (esim. "FI", "SE")
        for country in countries:
            if country.iso_country.upper() == search_term.upper():
                return country

        # 2. Yritä löytää täsmällisellä nimellä
        for country in countries:
            if country.name.lower() == search_term.lower():
                return country

        # 3. Yritä löytää osittaisella nimellä (esim. "Fin" -> "Finland")
        search_lower = search_term.lower()
        for country in countries:
            if search_lower in country.name.lower():
                return country

        # 4. Yritä löytää nimen alusta (esim. "Swe" -> "Sweden")
        for country in countries:
            if country.name.lower().startswith(search_lower):
                return country

        # Ei löytynyt
        return None

    def get_country_count(self) -> int:
        """Palauta maiden kokonaismäärä"""
        countries = self.get_european_countries()
        return len(countries)


class PlayerManager:
    """
    Pelaajien hallinta
    Vastaa pelaajien luomisesta, kirjautumisesta ja pelitilan tallentamisesta
    """

    def __init__(self, db: Database):
        self.db = db

    def create_player(self, username: str) -> bool:
        """
        Luo uusi pelaaja tietokantaan
        Palauttaa True jos onnistui, False jos nimi on jo käytössä
        """
        try:
            cursor = self.db.connection.cursor()

            # Lisää uusi pelaaja players-tauluun
            cursor.execute(
                "INSERT INTO players (username) VALUES (%s)",
                (username,)
            )

            return True

        except mysql.connector.IntegrityError:
            # Nimi on jo käytössä (UNIQUE constraint)
            return False

        except mysql.connector.Error as err:
            print(f"Virhe pelaajan luomisessa: {err}")
            return False

        finally:
            cursor.close()

    def player_exists(self, username: str) -> bool:
        """Tarkista onko pelaaja olemassa tietokannassa"""
        cursor = self.db.connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM players WHERE username = %s",
            (username,)
        )

        result = cursor.fetchone()
        cursor.close()

        return result[0] > 0 if result else False

    def get_player_id(self, username: str) -> Optional[int]:
        """
        Hae pelaajan ID nimen perusteella
        Tarvitaan muissa kyselyissä viittaamaan pelaajaan
        """
        cursor = self.db.connection.cursor()

        cursor.execute(
            "SELECT id FROM players WHERE username = %s",
            (username,)
        )

        result = cursor.fetchone()
        cursor.close()

        return result[0] if result else None

    def get_found_children_count(self, player_id: int) -> int:
        """
        Laske montako lasta pelaaja on löytänyt
        Käytetään edistymisen seuraamiseen
        """
        cursor = self.db.connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM found_children WHERE player_id = %s",
            (player_id,)
        )

        result = cursor.fetchone()
        cursor.close()

        return result[0] if result else 0

    def save_found_child(self, player_id: int, country_iso: str) -> bool:
        """
        Tallenna löydetty lapsi tietokantaan
        Unique constraint estää saman lapsen löytämisen kahdesti samasta maasta
        """
        try:
            cursor = self.db.connection.cursor()

            # Lisää löydetty lapsi tietokantaan
            cursor.execute("""
                           INSERT INTO found_children (player_id, country_iso)
                           VALUES (%s, %s)
                           """, (player_id, country_iso))

            return True

        except mysql.connector.IntegrityError:
            # Lapsi on jo löydetty tästä maasta (UNIQUE constraint)
            return False

        except mysql.connector.Error as err:
            print(f"Virhe lapsen tallennuksessa: {err}")
            return False

        finally:
            cursor.close()

    def is_child_found_in_country(self, player_id: int, country_iso: str) -> bool:
        """
        Tarkista onko lapsi jo löydetty tietystä maasta
        Estää turhan matkustamisen samaan maahan
        """
        cursor = self.db.connection.cursor()

        cursor.execute("""
                       SELECT COUNT(*)
                       FROM found_children
                       WHERE player_id = %s
                         AND country_iso = %s
                       """, (player_id, country_iso))

        result = cursor.fetchone()
        cursor.close()

        return result[0] > 0 if result else False

    def get_found_countries(self, player_id: int) -> List[str]:
        """
        Hae lista maista joista pelaaja on löytänyt lapsen
        Käytetään help-komennossa merkitsemään löydetyt maat
        """
        cursor = self.db.connection.cursor()

        cursor.execute("""
                       SELECT country_iso
                       FROM found_children
                       WHERE player_id = %s
                       """, (player_id,))

        results = cursor.fetchall()
        cursor.close()

        # Palauta lista ISO-koodeista
        return [row[0] for row in results]


class GameUI:
    """
    Pelin käyttöliittymä
    Vastaa tekstin tulostamisesta ja animaatioista
    """

    @staticmethod
    def clear_screen():
        """Tyhjennä konsoli - toimii sekä Windowsissa että Linuxissa"""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def print_header(text: str, width: int = 60):
        """
        Tulosta korostettu otsikko
        Käytetään pelin eri vaiheissa selkeyttämään käyttöliittymää
        """
        print("=" * width)
        print(text.center(width))
        print("=" * width)

    @staticmethod
    def print_story():
        """Tulosta pelin tarina - näytetään pelin alussa"""
        story = """
        🐵 LENTÄVÄ APINA 🐵

        Eräänä päivänä lentävä apina ja hänen kymmenen pientä lastaan 
        olivat matkalla takaisin kotiin, Suomeen. Taivas yllättäen tummui, 
        ja heidän ylleen nousi raivokas myrsky.

        Kovat tuulet tarttuivat pieniin apinanpoikasiin ja lennättivät 
        heidät kauas, ympäri Euroopan maita. Äitiapina kauhistui. 
        Hän yritti tavoittaa lapsiaan, mutta tuulen voima oli liian suuri.

        Kun myrsky vihdoin tyyntyi, jäljellä oli vain hiljainen taivas 
        ja äidin sydäntä painava huoli. Lentävä apina keräsi rohkeutensa 
        ja hänen oli lähdettävä etsimään kadonneita lapsiaan.

        Jokainen niistä saattoi olla missä päin Eurooppaa tahansa.
        Vain sinä voisit auttaa häntä tässä vaikeassa tilanteessa.

        Auttaisitko häntä pelaaja?
        """
        print(story)

    @staticmethod
    def crying_ape_animation(message: str):
        """
        Itkevä apina animaatio
        Näytetään tarinan jälkeen tunnelman luomiseksi
        """
        frames = [
            "(T_T)", "(T^T)", "(T_T)", "(T~T)",
            "(T_T)  *", "(T^T)  **", "(T~T)  ***"
        ]

        # Toista animaatio 20 kertaa
        for i in range(20):
            GameUI.clear_screen()
            print(frames[i % len(frames)])  # Valitse frame kierroksella
            print(f"\n{message}")
            time.sleep(0.15)  # Pieni viive animaation välillä

    @staticmethod
    def list_countries(countries: List[Country], found_countries: List[str] = None):
        """
        Listaa kaikki maat kahdessa sarakkeessa
        Näyttää ✓-merkin jos lapsi on löydetty kyseisestä maasta
        """
        GameUI.print_header("EUROOPAN MAAT")

        if not countries:
            print("Ei maita saatavilla!")
            return

        found_countries = found_countries or []

        # Järjestä maat aakkosjärjestykseen nimen mukaan
        sorted_countries = sorted(countries, key=lambda x: x.name)

        # Laske keskikohta kahta saraketta varten
        mid = (len(sorted_countries) + 1) // 2

        # Tulosta maat kahdessa sarakkeessa
        for i in range(mid):
            # Vasen sarake
            left = sorted_countries[i]
            left_marker = "✓" if left.iso_country in found_countries else " "
            left_str = f"{i + 1:2d}. [{left_marker}] {left.name[:25]:25} ({left.iso_country})"

            # Oikea sarake (jos on)
            if i + mid < len(sorted_countries):
                right = sorted_countries[i + mid]
                right_marker = "✓" if right.iso_country in found_countries else " "
                right_str = f"{i + mid + 1:2d}. [{right_marker}] {right.name[:25]:25} ({right.iso_country})"
                print(f"{left_str}  {right_str}")
            else:
                # Jos oikeaa saraketta ei ole, tulosta vain vasen
                print(left_str)

        print("=" * 60)
        print(f"Yhteensä {len(countries)} Euroopan maata")

        # Näytä montako maata on käyty läpi
        if found_countries:
            print(f"✓ = Lapsi löydetty ({len(found_countries)} maata)")


class FlyingApeGame:
    """
    Pääpeliluokka
    Yhdistää kaikki osat ja pyörittää pelisilmukkaa
    """

    def __init__(self):
        # Alusta kaikki komponentit
        self.db = Database()
        self.player_manager = PlayerManager(self.db)
        self.country_manager = CountryManager(self.db)
        self.ui = GameUI()

        # Pelaajakohtaiset tiedot
        self.player_id = None
        self.username = None
        self.children_to_find = 10  # Tavoite: löydä 10 lasta

    def run(self):
        """
        Pelin pääsilmukka
        Käynnistää pelin ja hoitaa virheenkäsittelyn
        """
        try:
            self.ui.clear_screen()
            self.ui.print_header("🚀 LENTÄVÄ APINA - PELI KÄYNNISTYY 🚀")

            print("\n📡 Yhdistetään tietokantaan...")

            # Tarkista että tietokantayhteys toimii
            if not self.db.connection:
                print("❌ Tietokantayhteyttä ei voitu muodostaa!")
                return

            print("✅ Tietokantayhteys OK")

            # Tarkista että maita löytyy tietokannasta
            country_count = self.country_manager.get_country_count()
            print(f"📍 Löydettiin {country_count} Euroopan maata tietokannasta")

            if country_count == 0:
                print("❌ Virhe: Maita ei löytynyt tietokannasta!")
                print("Tarkista että 'country' taulu sisältää Euroopan maat (continent = 'EU')")
                return

            time.sleep(2)

            # Näytä tarina ja animaatio
            self.ui.print_story()
            input("\nPaina Enter jatkaaksesi...")

            self.ui.crying_ape_animation("Äitiapina itkee kadonneita lapsiaan...")

            # Kirjaudu sisään ja aloita peli
            if self.login():
                self.play()

        except KeyboardInterrupt:
            # Käyttäjä keskeytti pelin (Ctrl+C)
            print("\n\n👋 Peli keskeytetty!")

        except Exception as e:
            # Muu virhe
            print(f"\n❌ Virhe: {e}")

        finally:
            # Sulje tietokantayhteys aina lopuksi
            self.db.close()
            print("\n🎮 Kiitos pelaamisesta!")

    def login(self) -> bool:
        """
        Käyttäjän kirjautuminen
        Kysyy onko uusi vai vanha pelaaja
        """
        self.ui.clear_screen()
        self.ui.print_header("KÄYTTÄJÄTIEDOT")

        while True:
            choice = input("\nOletko uusi pelaaja? (k/e): ").lower().strip()

            if choice in ['k', 'kyllä', 'y', 'yes']:
                # Uusi pelaaja
                if self.create_new_player():
                    return True

            elif choice in ['e', 'ei', 'n', 'no']:
                # Vanha pelaaja
                if self.login_existing_player():
                    return True

            else:
                print("Vastaa 'k' (kyllä) tai 'e' (ei)")

    def create_new_player(self) -> bool:
        """
        Luo uusi pelaaja
        Kysyy nimimerkin ja tarkistaa ettei se ole jo käytössä
        """
        print("\n--- Uuden pelaajan luominen ---")

        while True:
            username = input("Syötä haluamasi nimimerkki: ").strip()

            # Validoi syöte
            if not username:
                print("❌ Nimimerkki ei voi olla tyhjä!")
                continue

            if len(username) > 100:
                print("❌ Nimimerkki on liian pitkä (max 100 merkkiä)!")
                continue

            # Yritä luoda pelaaja
            if self.player_manager.create_player(username):
                self.username = username
                self.player_id = self.player_manager.get_player_id(username)
                print(f"✅ Tervetuloa peliin, {username}!")
                input("\nPaina Enter jatkaaksesi...")
                return True
            else:
                print(f"❌ Nimimerkki '{username}' on jo käytössä!")

    def login_existing_player(self) -> bool:
        """
        Kirjaudu olemassa olevalla pelaajalla
        Näyttää myös pelaajan edistymisen
        """
        print("\n--- Kirjautuminen ---")

        while True:
            username = input("Syötä nimimerkkisi: ").strip()

            if not username:
                print("❌ Nimimerkki ei voi olla tyhjä!")
                continue

            # Tarkista löytyykö pelaaja
            if self.player_manager.player_exists(username):
                self.username = username
                self.player_id = self.player_manager.get_player_id(username)

                # Näytä edistyminen
                found = self.player_manager.get_found_children_count(self.player_id)
                print(f"✅ Tervetuloa takaisin, {username}!")

                if found > 0:
                    print(f"📊 Olet löytänyt {found}/{self.children_to_find} lasta")
                else:
                    print("🆕 Aloitat uuden seikkailun!")

                input("\nPaina Enter jatkaaksesi...")
                return True
            else:
                print(f"❌ Käyttäjää '{username}' ei löytynyt!")
                retry = input("Haluatko yrittää uudelleen? (k/e): ").lower()
                if retry not in ['k', 'kyllä', 'y', 'yes']:
                    return False

    def play(self):
        """
        Varsinainen pelisilmukka
        Kysyy minne maahan pelaaja haluaa matkustaa
        """
        self.ui.clear_screen()
        self.ui.print_header("SEIKKAILU ALKAA!")

        # Näytä pelin aloitustiedot
        print(f"\n🐵 Pelaaja: {self.username}")
        print("📍 Olet nyt Suomessa")
        print("✈️  Äitiapina on valmis lentämään etsimään lapsiaan")
        print("\n💡 Komennot:")
        print("   • 'help' - Näytä kaikki maat")
        print("   • 'lopeta' - Lopeta peli")
        print("   • Maan nimi tai ISO-koodi - Lennä maahan")

        input("\nPaina Enter aloittaaksesi...")

        # Pelin pääsilmukka
        while True:
            self.ui.clear_screen()

            # Tarkista onko kaikki lapset löydetty
            found = self.player_manager.get_found_children_count(self.player_id)

            if found >= self.children_to_find:
                # Peli voitettu!
                self.win_game()
                break

            # Näytä tilanne
            self.ui.print_header(f"ETSINTÄ - {found}/{self.children_to_find} LASTA LÖYDETTY")

            if found > 0:
                remaining = self.children_to_find - found
                print(f"\n🔍 Vielä {remaining} lasta etsittävänä!")

            # Kysy minne mennään
            destination = input("\n🌍 Minne maahan haluat lentää? ").strip()

            # Käsittele komennot
            if destination.lower() in ['lopeta', 'quit', 'exit', 'q']:
                if self.confirm_quit():
                    break
                continue

            if destination.lower() in ['help', 'h', '?']:
                # Näytä maalista merkiten löydetyt
                found_countries = self.player_manager.get_found_countries(self.player_id)
                countries = self.country_manager.get_european_countries()
                self.ui.list_countries(countries, found_countries)
                input("\nPaina Enter jatkaaksesi...")
                continue

            if not destination:
                print("❌ Syötä maan nimi!")
                time.sleep(2)
                continue

            # Matkusta maahan
            self.travel_to_country(destination)

    def travel_to_country(self, destination: str):
        """
        Matkusta valittuun maahan
        Tarkistaa onko lapsi jo löydetty ja arpoo löytyykö uusi
        """
        # Etsi maa tietokannasta
        country = self.country_manager.find_country(destination)

        if not country:
            # Maata ei löytynyt
            print(f"\n❌ Maata '{destination}' ei löytynyt!")
            print("💡 Vinkki: Kirjoita 'help' nähdäksesi kaikki maat")
            print("💡 Voit käyttää maan nimeä tai ISO-koodia (esim. FI, DE, FR)")
            time.sleep(3)
            return

        # Tarkista onko lapsi jo löydetty tästä maasta
        if self.player_manager.is_child_found_in_country(self.player_id, country.iso_country):
            print(f"\nℹ️  Olet jo löytänyt lapsen maasta {country.name}!")
            print("🔍 Etsi muista maista!")
            time.sleep(3)
            return

        # Näytä lentoanimaatio
        print(f"\n✈️  Lennät maahan: {country.name} ({country.iso_country})")
        self.flight_animation()

        # Arvo löytyykö lapsi (25% todennäköisyys)
        child_found = random.random() < 0.25

        self.ui.clear_screen()
        self.ui.print_header(f"SAAVUIT: {country.name.upper()}")

        if child_found:
            # Lapsi löytyi!
            success = self.player_manager.save_found_child(self.player_id, country.iso_country)

            if success:
                found = self.player_manager.get_found_children_count(self.player_id)

                print("\n🎉 MAHTAVAA! LÖYSIT YHDEN LAPSISTASI! 🎉")
                print("🐵 Pieni apinanpoika juoksee luoksesi!")
                print(f"📊 Nyt olet löytänyt {found}/{self.children_to_find} lasta")

                if found < self.children_to_find:
                    print(f"🔍 Vielä {self.children_to_find - found} lasta etsittävänä!")
        else:
            # Ei löytynyt
            print("\n😔 Ei löytynyt lasta täältä...")
            print("🔍 Jatka etsimistä muista maista!")
            print(f"💡 Vihje: Todennäköisyys löytää lapsi on 25%")

        input("\nPaina Enter jatkaaksesi...")

    def flight_animation(self):
        """
        Näytä lentoanimaatio
        Luo tunnelmaa matkustamiseen
        """
        frames = ["✈️ ", " ☁️", "  🌤", " ☁️", "✈️ "]

        # Toista animaatio kahdesti
        for _ in range(2):
            for frame in frames:
                print(f"\r{frame * 8}", end="", flush=True)
                time.sleep(0.2)
        print()  # Rivinvaihto lopuksi

    def win_game(self):
        """
        Voittoruutu
        Näytetään kun kaikki 10 lasta on löydetty
        """
        self.ui.clear_screen()
        self.ui.print_header("🎉 ONNITTELUT! 🎉")

        print("""
        LÖYSIT KAIKKI LAPSET!

            🏆
           🐵
          /|\\
         / | \\
          / \\

        ✨ KAIKKI 10 LASTA PELASTETTU! ✨

        Äitiapina ja lapset ovat jälleen yhdessä!
        Kiitos avustasi, sankari!

        🐵🐵🐵🐵🐵🐵🐵🐵🐵🐵
        """)

        # Näytä pelitilastot
        countries = self.country_manager.get_european_countries()
        print(f"\n📊 Tilastot:")
        print(f"   • Pelaaja: {self.username}")
        print(f"   • Käytit {len(countries)} maasta löytääksesi kaikki lapset")

        input("\nPaina Enter lopettaaksesi...")

    def confirm_quit(self) -> bool:
        """
        Varmista pelin lopetus
        Näyttää myös nykyisen edistymisen
        """
        found = self.player_manager.get_found_children_count(self.player_id)

        if found > 0:
            print(f"\n⚠️  Olet löytänyt {found}/{self.children_to_find} lasta.")
            print("Pelisi tallentuu automaattisesti.")

        choice = input("\nHaluatko varmasti lopettaa? (k/e): ").lower()
        return choice in ['k', 'kyllä', 'y', 'yes']


def main():
    """
    Pääfunktio
    Luo peli-instanssin ja käynnistää sen
    """
    game = FlyingApeGame()
    game.run()


if __name__ == "__main__":
    main()