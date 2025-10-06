import os
import mysql.connector
import random

def clear():
    # Detect operating system and run the right command
    os.system('cls' if os.name == 'nt' else 'clear')

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='salasana',
         autocommit=True,
         )


#pelin tarina
print("""Eräänä päivänä lentävä apina ja hänen kymmenen pientä lastaan olivat matkalla takaisin kotiin, Suomeen.
Taivas yllättäen tummui, ja heidän ylleen nousi raivokas myrsky.

Kovat tuulet tarttuivat pieniin apinanpoikasiin ja lennättivät heidät kauas, ympäri Euroopan maita.
Äitiapina kauhistui. Hän yritti tavoittaa lapsiaan, mutta tuulen voima oli liian suuri.
Kun myrsky vihdoin tyyntyi, jäljellä oli vain hiljainen taivas ja äidin sydäntä painava huoli.
Lentävä apina keräsi rohkeutensa ja hänen oli lähdettävä etsimään kadonneita lapsiaan.
Jokainen niistä saattoi olla missä päin Eurooppaa tahansa

Vain sinä voisit auttaa häntä tässä vaikeassa tilanteessa.
Auttaisitko häntä pelaaja?""")

input("Paina enter jaktaaksesi: ")
clear()
