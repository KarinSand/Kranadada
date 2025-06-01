#!/usr/bin/env python3
"""
Initierar (eller uppgraderar) SQLite-filen `cards_only.db`.

* Tabell: CARD(id, name, year, category, description)
* Kategorier som front-end förväntar: sport, fritid, historia
"""

import sqlite3, pathlib

BASE = pathlib.Path(__file__).resolve().parent
DB   = BASE / "cards_only.db"
DB.touch(exist_ok=True)

with sqlite3.connect(DB) as conn:
    cur = conn.cursor()

    # Skapa tabell om den inte finns
    cur.execute("""
    CREATE TABLE IF NOT EXISTS CARD(
      CARD_ID     INTEGER PRIMARY KEY AUTOINCREMENT,
      NAME        TEXT NOT NULL,
      YEAR        INTEGER NOT NULL,
      CATEGORY    TEXT NOT NULL,
      DESCRIPTION TEXT
    );""")

    # Lägg till CATEGORY-kolumn om tabellen saknar den (äldre filer)
    cur.execute("PRAGMA table_info(CARD)")
    if "CATEGORY" not in [row[1].upper() for row in cur.fetchall()]:
        cur.execute("ALTER TABLE CARD ADD COLUMN CATEGORY TEXT DEFAULT 'historia'")

    # Kolla om kort redan finns
    cur.execute("SELECT COUNT(*) FROM CARD")
    if cur.fetchone()[0]:
        print("Databasen innehåller redan kort – inget mer att göra.")
        exit(0)

    cards = [
    #SPORT 12 st
    ("Första moderna OS",                          1896, "sport",    ""),
    ("OS i Stockholm",                             1912, "sport",    ""),
    ("Första Vasaloppet",                          1922, "sport",    ""),
    ("Sverige brons i fotbolls-VM",                1994, "sport",    ""),
    ("Sverige vinner VM i bandy",                  1987, "sport",    ""),
    ("Maradona – 'Guds hand'",                     1986, "sport",    ""),
    ("Michael Phelps tar 8 guld i Peking-OS",      2008, "sport",    ""),
    ("Sverige hockeyguld i Turin-OS",              2006, "sport",    ""),
    ("Usain Bolt springer 9.58 s (100 m)",         2009, "sport",    ""),
    ("Zlatans bicykleta mot England",              2012, "sport",    ""),
    ("Damlandslaget tar VM-silver",                2003, "sport",    ""),
    ("Första Super Bowl spelas",                   1967, "sport",    ""),
    ("Sverige tar guld i fotbolls-OS",              1948, "sport",    ""),
    ("Björn Borg vinner Wimbledon första gången",   1976, "sport",    ""),
    ("Ingemar Stenmark vinner två OS-guld",         1980, "sport",    ""),
    ("Carolina Klüft vinner OS-guld i sjukamp",     2004, "sport",    ""),
    ("Sverige vinner VM-guld i ishockey på hemmaplan",  1962, "sport", ""),
    ("Första kvinnliga maratonloppet i OS",         1984, "sport",    ""),
    ("Tony Rickardsson vinner sin sjätte VM-titel i speedway", 2005, "sport", ""),
    ("Sverige vinner Davis Cup i tennis",           1984, "sport",    ""),
    ("Pernilla Wiberg vinner OS-guld i slalom",     1992, "sport",    ""),
    ("Anja Pärson tar sju VM-guld i alpint",         2001, "sport",    ""),
    ("Sveriges damer vinner EM-guld i handboll",    2010, "sport",    ""),
    ("Henrik Larsson dominerar i EM 2004",          2004, "sport",    ""),
    ("Sverige slår ut Italien ur VM-kvalet",        2017, "sport",    ""),
    ("Therese Alshammar tar VM-guld i simning",     2001, "sport",    ""),
    ("Daniel Ståhl vinner OS-guld i diskus",        2021, "sport",    ""),
    ("Sverige vinner mixedstafett i skidskytte-VM", 2023, "sport",    ""),
    ("Sarah Sjöström sätter världsrekord på 100 m fjäril", 2016, "sport", ""),
    ("Första damturneringen i Wimbledon",           1884, "sport",    ""),
    ("USA vinner basketguldet i OS med Dream Team", 1992, "sport",    ""),
    ("Messi vinner sitt första VM-guld",            2022, "sport",    ""),
    ("Pelé vinner sitt första VM-guld",                   1958, "sport", ""),
    ("Sverige spelar VM-final i fotboll",                 1958, "sport", ""),
    ("Cassius Clay blir världsmästare i boxning",         1964, "sport", ""),
    ("Nadia Comaneci får 10.0 i OS-gymnastik",            1976, "sport", ""),
    ("Diego Maradona gör 'Århundradets mål'",             1986, "sport", ""),
    ("Stefan Holm vinner OS-guld i höjdhopp",             2004, "sport", ""),
    ("Zlatan debuterar i landslaget",                     2001, "sport", ""),
    ("Patrik Sjöberg slår svenskt rekord i höjdhopp",     1987, "sport", ""),
    ("Mats Sundin draftas först i NHL",                   1989, "sport", ""),
    ("Tiger Woods vinner sin första Masters",             1997, "sport", ""),
    ("Usain Bolt vinner trippeltrippeln i OS",            2016, "sport", ""),
    ("Simone Biles dominerar i OS",                       2016, "sport", ""),
    ("Mo Farah vinner dubbelguld på 5 000/10 000 m",       2012, "sport", ""),
    ("Roger Federer vinner sin 20:e Grand Slam",          2018, "sport", ""),
    ("Serena Williams tar sin 23:e Grand Slam-titel",     2017, "sport", ""),
    ("Lotta Schelin gör målrekord i damlandslaget",       2014, "sport", ""),
    ("Sveriges damer tar brons i fotbolls-VM",            2019, "sport", ""),
    ("Sverige vinner EM-guld i herrhandboll",             2002, "sport", ""),
    ("Sverige chockar Holland i EM 2004",                 2004, "sport", ""),
    ("Sverige slår ut USA i OS-fotbollen",                2021, "sport", ""),
    ("Jan-Ove Waldner vinner OS-guld i bordtennis",       1992, "sport", ""),
    ("Gunde Svan tar 4 OS-guld i längdskidor",            1984, "sport", ""),
    ("Sven Tumba blir svensk hockeyikon",                 1957, "sport", ""),
    ("Lennart Johansson blir UEFA-president",             1990, "sport", ""),
    ("Foppa gör 'Foppastraffen' i OS-finalen",            1994, "sport", ""),
    ("Christiano Ronaldo vinner sin femte Ballon d'Or",   2017, "sport", ""),
    ("Lionel Messi gör 91 mål på ett år",                 2012, "sport", ""),
    ("Michael Jordan återvänder till NBA",                1995, "sport", ""),
    ("Shaquille O'Neal och Kobe Bryant vinner trippel",   2002, "sport", ""),
    ("LeBron James vinner sin första NBA-titel",          2012, "sport", ""),
    ("Conor McGregor blir dubbel UFC-mästare",            2016, "sport", ""),
    ("Khabib besegrar McGregor i UFC",                    2018, "sport", ""),
    ("Formel 1: Schumacher vinner sin sjunde VM-titel",   2004, "sport", ""),
    ("Lewis Hamilton tangerar Schumacher med 7 titlar",   2020, "sport", ""),
    ("Allyson Felix blir mest OS-medaljerade friidrottaren", 2021, "sport", ""),
    ("Marit Bjørgen blir mest OS-dekorerade vinteridrottare", 2018, "sport", ""),
    ("Charlotte Kalla tar tre medaljer i Pyeongchang",    2018, "sport", ""),
    ("Stina Nilsson spurtar hem OS-guld",                 2018, "sport", ""),
    ("Frida Karlsson slår igenom i skid-VM",              2019, "sport", ""),
    ("Therese Johaug dominerar skid-VM",                  2021, "sport", ""),
    ("Mondo Duplantis sätter världsrekord i stav",        2020, "sport", ""),
    ("Sverige tar EM-guld i innebandy",                   1996, "sport", ""),
    ("Innebandy-VM: Sverige vs Finland-klassiker",        2012, "sport", ""),
    ("Sverige vinner VM-guld i ridsport fälttävlan",      2022, "sport", ""),
    ("Sarah Sjöström tar OS-guld i 100 m fjäril",         2016, "sport", ""),
    ("Sverige tar lagguld i OS i hästhoppning",           2021, "sport", ""),
    ("Sverige vinner curlingguld med Team Hasselborg",    2018, "sport", ""),
    ("Niklas Edin vinner VM-guld i curling",              2023, "sport", ""),
    ("USA vinner historiskt damfotbolls-VM",              1999, "sport", ""),
    ("Frankrike vinner fotbolls-VM på hemmaplan",         1998, "sport", ""),
    ("Italien vinner EM i fotboll efter straffdrama",     2021, "sport", ""),

    #FRITID 12 st
    ("LEGO lanseras",                              1958, "fritid",   ""),
    ("Rubiks kub uppfinns",                        1974, "fritid",   ""),
    ("Nintendo Game Boy släpps",                   1989, "fritid",   ""),
    ("Spotify lanseras",                           2008, "fritid",   ""),
    ("Pokémon GO-febern",                          2016, "fritid",   ""),
    ("Minecraft släpps",                           2011, "fritid",   ""),
    ("Första iPhone visas",                        2007, "fritid",   ""),
    ("Facebook lanseras",                          2004, "fritid",   ""),
    ("Instagram lanseras",                         2010, "fritid",   ""),
    ("Netflix börjar med streaming",               2007, "fritid",   ""),
    ("TikTok lanseras globalt",                    2018, "fritid",   ""),
    ("Första Harry Potter-boken ges ut",           1997, "fritid",   ""),

    #HISTORIA 18 st
    ("Slaget vid Hastings",                        1066, "historia", ""),
    ("Första korståget inleds",                    1096, "historia", ""),
    ("Jerusalem intas av korståget",               1099, "historia", ""),
    ("Tredje korståget med Richard Lejonhjärta",   1189, "historia", ""),
    ("Magna Carta undertecknas",                   1215, "historia", ""),
    ("Hundraårskriget inleds",                     1337, "historia", ""),
    ("Digerdöden når Europa",                      1347, "historia", ""),
    ("Kalmarunionen bildas",                       1397, "historia", ""),
    ("Jan Hus bränns på bål",                      1415, "historia", ""),
    ("Slaget vid Agincourt",                       1415, "historia", ""),
    ("Joan of Arc befriar Orléans",                1429, "historia", ""),
    ("Gutenbergs tryckpress",                      1440, "historia", ""),
    ("Leonardo da Vinci föds",                     1452, "historia", ""),
    ("Columbus upptäcker Amerika",                 1492, "historia", ""),
    ("Reformationen inleds av Martin Luther",      1517, "historia", ""),
    ("Stockholms blodbad",                         1520, "historia", ""),
    ("Sverige blir protestantiskt",                1527, "historia", ""),
    ("Slaget vid Lepanto",                         1571, "historia", ""),
    ("Trettiåriga kriget börjar",                  1618, "historia", ""),
    ("Mayflower anländer till Nordamerika",        1620, "historia", ""),
    ("Vasaskeppet sjunker",                        1628, "historia", ""),
    ("Newton publicerar Principia Mathematica",    1687, "historia", ""),
    ("Slaget vid Poltava",                         1709, "historia", ""),
    ("Svenska tryckfrihetsförordningen",           1766, "historia", ""),
    ("Boston Tea Party",                           1773, "historia", ""),
    ("Amerikanska självständigheten",              1776, "historia", ""),
    ("Franska stormningen av Bastiljen",           1789, "historia", ""),
    ("Franska revolutionen",                       1789, "historia", ""),
    ("Slaget vid Trafalgar",                       1805, "historia", ""),
    ("Slaget vid Waterloo",                        1815, "historia", ""),
    ("Darwin publicerar 'Om arternas uppkomst'",   1859, "historia", ""),
    ("Tysklands enande under Bismarck",            1871, "historia", ""),
    ("Första telefonen konstrueras av Bell",       1876, "historia", ""),
    ("Bolsjevikrevolutionen i Ryssland",           1917, "historia", ""),
    ("Kvinnlig rösträtt införs i Sverige",         1921, "historia", ""),
    ("Berlinmurens fall",                          1989, "historia", ""),
    ("Terroattacken 11 september",                 2001, "historia", "")

]

    cur.executemany(
        "INSERT INTO CARD(NAME, YEAR, CATEGORY, DESCRIPTION) VALUES (?,?,?,?)",
        cards
    )
    conn.commit()
    print(f"Initierade databasen med {len(cards)} kort.")
