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
    ("Första korståget inleds",                    1096, "historia", ""),
    ("Jerusalem intas av korståget",               1099, "historia", ""),
    ("Tredje korståget med Richard Lejonhjärta",   1189, "historia", ""),
    ("Digerdöden når Europa",                      1347, "historia", ""),
    ("Kalmarunionen bildas",                       1397, "historia", ""),
    ("Jan Hus bränns på bål",                      1415, "historia", ""),
    ("Leonardo da Vinci föds",                     1452, "historia", ""),
    ("Gutenbergs tryckpress",                      1440, "historia", ""),
    ("Joan of Arc befriar Orléans",                1429, "historia", ""),
    ("Columbus upptäcker Amerika",                 1492, "historia", ""),
    ("Stockholms blodbad",                         1520, "historia", ""),
    ("Sverige blir protestantiskt",                1527, "historia", ""),
    ("Vasaskeppet sjunker",                        1628, "historia", ""),
    ("Trettiåriga kriget börjar",                  1618, "historia", ""),
    ("Amerikanska självständigheten",              1776, "historia", ""),
    ("Franska revolutionen",                       1789, "historia", ""),
    ("Berlinmurens fall",                          1989, "historia", ""),
    ("Terroattacken 11 september",                 2001, "historia", ""),
    
    #SAMTID 10–15 senaste åren
    ("Brexit folkomröstning",                      2016, "samtid", ""),
    ("Game of Thrones-finalen visas",              2019, "samtid", ""),
    ("Suezkanalen blockeras av Ever Given",        2021, "samtid", ""),
    ("Joe Biden blir president",                   2021, "samtid", ""),
    ("Putin invaderar Ukraina",                    2022, "samtid", ""),
    ("Oppenheimer och Barbie släpps samma dag",    2023, "samtid", "")


]

    cur.executemany(
        "INSERT INTO CARD(NAME, YEAR, CATEGORY, DESCRIPTION) VALUES (?,?,?,?)",
        cards
    )
    conn.commit()
    print(f"Initierade databasen med {len(cards)} kort.")
