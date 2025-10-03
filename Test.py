import os
import mysql.connector
import random
import time
from typing import Optional, Tuple, List
from dataclasses import dataclass


@dataclass
class Country:
    """Maa-dataluokka"""
    iso_country: str
    name: str


class Database:
    """MariaDB tietokantayhteyden hallinta"""

    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        """Yhdistä MariaDB tietokantaan"""
        try:
            self.connection = mysql.connector.connect(
                host='127.0.0.1',
                port=3306,
                database='flight_game',
                user='root',
                password='nooanooa',
                autocommit=True
            )
            self._init_tables()
            return True
        except mysql.connector.Error as err:
            print(f"❌ Tietokantayhteyden muodostaminen epäonnistui: {err}")
            return False

    def _init_tables(self):
        """Alusta tarvittavat taulut"""
        cursor = self.connection.cursor()

        # Luo pelaajataulu jos ei ole
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

        # Luo löydettyjen lasten taulu
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
        """Sulje tietokantayhteys"""
        if self.connection:
            self.connection.close()


class CountryManager:
    """Maiden hallinta - hakee maat suoraan tietokannasta"""

    def __init__(self, db: Database):
        self.db = db
        self.countries_cache = None

    def get_european_countries(self) -> List[Country]:
        """Hae kaikki Euroopan maat country-taulusta"""
        if self.countries_cache:
            return self.countries_cache

        cursor = self.db.connection.cursor()

        # Hae kaikki Euroopan maat suoraan country-taulusta
        cursor.execute("""
                       SELECT iso_country, name
                       FROM country
                       WHERE continent = 'EU'
                       ORDER BY name
                       """)

        results = cursor.fetchall()
        cursor.close()

        self.countries_cache = [Country(iso_country=row[0], name=row[1]) for row in results]
        return self.countries_cache

    def find_country(self, search_term: str) -> Optional[Country]:
        """Etsi maa hakusanalla"""
        search_term = search_term.strip()
        countries = self.get_european_countries()

        # Etsi täsmällisellä ISO-koodilla
        for country in countries:
            if country.iso_country.upper() == search_term.upper():
                return country

        # Etsi täsmällisellä nimellä
        for country in countries:
            if country.name.lower() == search_term.lower():
                return country

        # Etsi osittaisella nimellä
        search_lower = search_term.lower()
        for country in countries:
            if search_lower in country.name.lower():
                return country

        # Etsi nimen alusta
        for country in countries:
            if country.name.lower().startswith(search_lower):
                return country

        return None

    def get_country_count(self) -> int:
        """Hae maiden lukumäärä"""
        countries = self.get_european_countries()
        return len(countries)


class PlayerManager:
    """Pelaajien hallinta"""

    def __init__(self, db: Database):
        self.db = db

    def create_player(self, username: str) -> bool:
        """Luo uusi pelaaja"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("INSERT INTO players (username) VALUES (%s)", (username,))
            return True
        except mysql.connector.IntegrityError:
            return False
        except mysql.connector.Error as err:
            print(f"Virhe pelaajan luomisessa: {err}")
            return False
        finally:
            cursor.close()

    def player_exists(self, username: str) -> bool:
        """Tarkista onko pelaaja olemassa"""
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM players WHERE username = %s", (username,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] > 0 if result else False

    def get_player_id(self, username: str) -> Optional[int]:
        """Hae pelaajan ID"""
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT id FROM players WHERE username = %s", (username,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None

    def get_found_children_count(self, player_id: int) -> int:
        """Hae löydettyjen lasten määrä"""
        cursor = self.db.connection.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM found_children WHERE player_id = %s",
            (player_id,)
        )
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else 0

    def save_found_child(self, player_id: int, country_iso: str) -> bool:
        """Tallenna löydetty lapsi"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute(
                "INSERT INTO found_children (player_id, country_iso) VALUES (%s, %s)",
                (player_id, country_iso)
            )
            return True
        except mysql.connector.IntegrityError:
            return False  # Lapsi jo löydetty tästä maasta
        except mysql.connector.Error as err:
            print(f"Virhe lapsen tallennuksessa: {err}")
            return False
        finally:
            cursor.close()

    def is_child_found_in_country(self, player_id: int, country_iso: str) -> bool:
        """Tarkista onko lapsi jo löydetty tästä maasta"""
        cursor = self.db.connection.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM found_children WHERE player_id = %s AND country_iso = %s",
            (player_id, country_iso)
        )
        result = cursor.fetchone()
        cursor.close()
        return result[0] > 0 if result else False

    def get_found_countries(self, player_id: int) -> List[str]:
        """Hae lista maista joista on löydetty lapsi"""
        cursor = self.db.connection.cursor()
        cursor.execute(
            "SELECT country_iso FROM found_children WHERE player_id = %s",
            (player_id,)
        )
        results = cursor.fetchall()
        cursor.close()
        return [row[0] for row in results]


class GameUI:
    """Pelin käyttöliittymä"""

    @staticmethod
    def clear_screen():
        """Tyhjennä näyttö"""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def print_header(text: str, width: int = 60):
        """Tulosta otsikko"""
        print("=" * width)
        print(text.center(width))
        print("=" * width)

    @staticmethod
    def print_story():
        """Tulosta pelin tarina"""
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
        """Itkevä apina animaatio"""
        frames = [
            "(T_T)", "(T^T)", "(T_T)", "(T~T)",
            "(T_T)  *", "(T^T)  **", "(T~T)  ***"
        ]

        for i in range(20):
            GameUI.clear_screen()
            print(frames[i % len(frames)])
            print(f"\n{message}")
            time.sleep(0.15)

    @staticmethod
    def list_countries(countries: List[Country], found_countries: List[str] = None):
        """Listaa maat"""
        GameUI.print_header("EUROOPAN MAAT")

        if not countries:
            print("Ei maita saatavilla!")
            return

        found_countries = found_countries or []

        # Järjestä maat aakkosjärjestykseen
        sorted_countries = sorted(countries, key=lambda x: x.name)

        # Tulosta maat 2 sarakkeessa
        mid = (len(sorted_countries) + 1) // 2

        for i in range(mid):
            left = sorted_countries[i]
            left_marker = "✓" if left.iso_country in found_countries else " "
            left_str = f"{i + 1:2d}. [{left_marker}] {left.name[:25]:25} ({left.iso_country})"

            if i + mid < len(sorted_countries):
                right = sorted_countries[i + mid]
                right_marker = "✓" if right.iso_country in found_countries else " "
                right_str = f"{i + mid + 1:2d}. [{right_marker}] {right.name[:25]:25} ({right.iso_country})"
                print(f"{left_str}  {right_str}")
            else:
                print(left_str)

        print("=" * 60)
        print(f"Yhteensä {len(countries)} Euroopan maata")
        if found_countries:
            print(f"✓ = Lapsi löydetty ({len(found_countries)} maata)")


class FlyingApeGame:
    """Pääpeliluokka"""

    def __init__(self):
        self.db = Database()
        self.player_manager = PlayerManager(self.db)
        self.country_manager = CountryManager(self.db)
        self.ui = GameUI()
        self.player_id = None
        self.username = None
        self.children_to_find = 10

    def run(self):
        """Käynnistä peli"""
        try:
            self.ui.clear_screen()
            self.ui.print_header("🚀 LENTÄVÄ APINA - PELI KÄYNNISTYY 🚀")

            print("\n📡 Yhdistetään tietokantaan...")

            if not self.db.connection:
                print("❌ Tietokantayhteyttä ei voitu muodostaa!")
                return

            print("✅ Tietokantayhteys OK")

            # Tarkista maiden määrä
            country_count = self.country_manager.get_country_count()
            print(f"📍 Löydettiin {country_count} Euroopan maata tietokannasta")

            if country_count == 0:
                print("❌ Virhe: Maita ei löytynyt tietokannasta!")
                print("Tarkista että 'country' taulu sisältää Euroopan maat (continent = 'EU')")
                return

            time.sleep(2)

            self.ui.print_story()
            input("\nPaina Enter jatkaaksesi...")

            self.ui.crying_ape_animation("Äitiapina itkee kadonneita lapsiaan...")

            if self.login():
                self.play()

        except KeyboardInterrupt:
            print("\n\n👋 Peli keskeytetty!")
        except Exception as e:
            print(f"\n❌ Virhe: {e}")
        finally:
            self.db.close()
            print("\n🎮 Kiitos pelaamisesta!")

    def login(self) -> bool:
        """Käyttäjän kirjautuminen"""
        self.ui.clear_screen()
        self.ui.print_header("KÄYTTÄJÄTIEDOT")

        while True:
            choice = input("\nOletko uusi pelaaja? (k/e): ").lower().strip()

            if choice in ['k', 'kyllä', 'y', 'yes']:
                if self.create_new_player():
                    return True
            elif choice in ['e', 'ei', 'n', 'no']:
                if self.login_existing_player():
                    return True
            else:
                print("Vastaa 'k' (kyllä) tai 'e' (ei)")

    def create_new_player(self) -> bool:
        """Luo uusi pelaaja"""
        print("\n--- Uuden pelaajan luominen ---")

        while True:
            username = input("Syötä haluamasi nimimerkki: ").strip()

            if not username:
                print("❌ Nimimerkki ei voi olla tyhjä!")
                continue

            if len(username) > 100:
                print("❌ Nimimerkki on liian pitkä (max 100 merkkiä)!")
                continue

            if self.player_manager.create_player(username):
                self.username = username
                self.player_id = self.player_manager.get_player_id(username)
                print(f"✅ Tervetuloa peliin, {username}!")
                input("\nPaina Enter jatkaaksesi...")
                return True
            else:
                print(f"❌ Nimimerkki '{username}' on jo käytössä!")

    def login_existing_player(self) -> bool:
        """Kirjaudu olemassa olevalla käyttäjällä"""
        print("\n--- Kirjautuminen ---")

        while True:
            username = input("Syötä nimimerkkisi: ").strip()

            if not username:
                print("❌ Nimimerkki ei voi olla tyhjä!")
                continue

            if self.player_manager.player_exists(username):
                self.username = username
                self.player_id = self.player_manager.get_player_id(username)
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
        """Pelaa peliä"""
        self.ui.clear_screen()
        self.ui.print_header("SEIKKAILU ALKAA!")

        print(f"\n🐵 Pelaaja: {self.username}")
        print("📍 Olet nyt Suomessa")
        print("✈️  Äitiapina on valmis lentämään etsimään lapsiaan")
        print("\n💡 Komennot:")
        print("   • 'help' - Näytä kaikki maat")
        print("   • 'lopeta' - Lopeta peli")
        print("   • Maan nimi tai ISO-koodi - Lennä maahan")

        input("\nPaina Enter aloittaaksesi...")

        while True:
            self.ui.clear_screen()
            found = self.player_manager.get_found_children_count(self.player_id)

            if found >= self.children_to_find:
                self.win_game()
                break

            self.ui.print_header(f"ETSINTÄ - {found}/{self.children_to_find} LASTA LÖYDETTY")

            if found > 0:
                remaining = self.children_to_find - found
                print(f"\n🔍 Vielä {remaining} lasta etsittävänä!")

            destination = input("\n🌍 Minne maahan haluat lentää? ").strip()

            if destination.lower() in ['lopeta', 'quit', 'exit', 'q']:
                if self.confirm_quit():
                    break
                continue

            if destination.lower() in ['help', 'h', '?']:
                found_countries = self.player_manager.get_found_countries(self.player_id)
                countries = self.country_manager.get_european_countries()
                self.ui.list_countries(countries, found_countries)
                input("\nPaina Enter jatkaaksesi...")
                continue

            if not destination:
                print("❌ Syötä maan nimi!")
                time.sleep(2)
                continue

            self.travel_to_country(destination)

    def travel_to_country(self, destination: str):
        """Matkusta maahan"""
        country = self.country_manager.find_country(destination)

        if not country:
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

        # Lennä maahan
        print(f"\n✈️  Lennät maahan: {country.name} ({country.iso_country})")
        self.flight_animation()

        # Tarkista löytyykö lapsi (25% todennäköisyys)
        child_found = random.random() < 0.25

        self.ui.clear_screen()
        self.ui.print_header(f"SAAVUIT: {country.name.upper()}")

        if child_found:
            success = self.player_manager.save_found_child(self.player_id, country.iso_country)
            if success:
                found = self.player_manager.get_found_children_count(self.player_id)

                print("\n🎉 MAHTAVAA! LÖYSIT YHDEN LAPSISTASI! 🎉")
                print("🐵 Pieni apinanpoika juoksee luoksesi!")
                print(f"📊 Nyt olet löytänyt {found}/{self.children_to_find} lasta")

                if found < self.children_to_find:
                    print(f"🔍 Vielä {self.children_to_find - found} lasta etsittävänä!")
        else:
            print("\n😔 Ei löytynyt lasta täältä...")
            print("🔍 Jatka etsimistä muista maista!")
            print(f"💡 Vihje: Todennäköisyys löytää lapsi on 25%")

        input("\nPaina Enter jatkaaksesi...")

    def flight_animation(self):
        """Lentoanimaatio"""
        frames = ["✈️ ", " ☁️", "  🌤", " ☁️", "✈️ "]
        for _ in range(2):
            for frame in frames:
                print(f"\r{frame * 8}", end="", flush=True)
                time.sleep(0.2)
        print()

    def win_game(self):
        """Voita peli"""
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

        # Näytä tilastot
        countries = self.country_manager.get_european_countries()
        print(f"\n📊 Tilastot:")
        print(f"   • Pelaaja: {self.username}")
        print(f"   • Käytit {len(countries)} maasta löytääksesi kaikki lapset")

        input("\nPaina Enter lopettaaksesi...")

    def confirm_quit(self) -> bool:
        """Vahvista pelin lopetus"""
        found = self.player_manager.get_found_children_count(self.player_id)
        if found > 0:
            print(f"\n⚠️  Olet löytänyt {found}/{self.children_to_find} lasta.")
            print("Pelisi tallentuu automaattisesti.")

        choice = input("\nHaluatko varmasti lopettaa? (k/e): ").lower()
        return choice in ['k', 'kyllä', 'y', 'yes']


def main():
    """Pääfunktio"""
    game = FlyingApeGame()
    game.run()


if __name__ == "__main__":
    main()