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
      DIFFICULTY  INTEGER
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
    #SPORT 50 st
    ("Första moderna OS",                         1896, "sport", 1),
    ("OS i Stockholm",                            1912, "sport", 1),
    ("Sverige spelar VM-final i fotboll",         1958, "sport", 0),
    ("Pelé vinner sitt första VM-guld",           1958, "sport", 1),
    ("Sven Tumba blir svensk hockeyikon",         1957, "sport", 0),
    ("Cassius Clay blir världsmästare i boxning", 1964, "sport", 1),
    ("Första Super Bowl spelas",                  1967, "sport", 1),
    ("Björn Borg vinner Wimbledon första gången", 1976, "sport", 1),
    ("Nadia Comaneci får 10.0 i OS-gymnastik",    1976, "sport", 1),
    ("Ingemar Stenmark vinner två OS-guld",       1980, "sport", 0),
    ("Gunde Svan tar 4 OS-guld i längdskidor",    1984, "sport", 1),
    ("Första kvinnliga maratonloppet i OS",       1984, "sport", 1),
    ("Sverige vinner Davis Cup i tennis",         1984, "sport", 0),
    ("Maradona – 'Guds hand'",                    1986, "sport", 1),
    ("Patrik Sjöberg slår svenskt rekord",        1987, "sport", 0),
    ("Sverige vinner VM i bandy",                 1987, "sport", 0),
    ("Mats Sundin draftas först i NHL",           1989, "sport", 1),
    ("Sverige brons i fotbolls-VM",               1994, "sport", 0),
    ("Foppa gör 'Foppastraffen' i OS-finalen",    1994, "sport", 0),
    ("Tiger Woods vinner sin första Masters",     1997, "sport", 1),
    ("Pernilla Wiberg vinner OS-guld",            1992, "sport", 0),
    ("Jan-Ove Waldner vinner OS-guld",            1992, "sport", 0),
    ("Sverige EM-guld i herrhandboll",            2002, "sport", 0),
    ("Anja Pärson tar sju VM-guld",               2001, "sport", 1),
    ("Carolina Klüft vinner OS-guld",             2004, "sport", 0),
    ("Henrik Larsson i EM 2004",                  2004, "sport", 0),
    ("Formel 1: Schumacher vinner 7:e titel",     2004, "sport", 1),
    ("Tony Rickardsson vinner sin sjätte titel",  2005, "sport", 1),
    ("Hockeyguld i Turin-OS",                     2006, "sport", 0),
    ("Michael Phelps tar 8 guld i OS",            2008, "sport", 1),
    ("Usain Bolt springer 9.58",                  2009, "sport", 0),
    ("Zlatans bicykleta mot England",             2012, "sport", 0),
    ("Lionel Messi gör 91 mål",                   2012, "sport", 1),
    ("Serena Williams 23:e Grand Slam",           2017, "sport", 1),
    ("LeBron James vinner första NBA-titel",      2012, "sport", 1),
    ("Sarah Sjöström tar OS-guld",                2016, "sport", 0),
    ("Usain Bolt trippeltrippel",                 2016, "sport", 1),
    ("Lotta Schelin målrekord",                   2014, "sport", 0),
    ("Charlotte Kalla tar tre medaljer",          2018, "sport", 0),
    ("Daniel Ståhl vinner OS-guld",               2021, "sport", 0),
    ("Therese Johaug dominerar skid-VM",          2021, "sport", 1),
    ("Sverige slår ut USA i OS-fotbollen",        2021, "sport", 0),
    ("Zlatan debuterar i landslaget",             2001, "sport", 0),
    ("Roger Federer 20:e Grand Slam",             2018, "sport", 1),
    ("Christiano Ronaldo vinner 5:e Ballon d'Or", 2017, "sport", 1),
    ("Niklas Edin vinner VM-guld curling",        2023, "sport", 0),
    ("Messi vinner sitt första VM-guld",          2022, "sport", 0),
    ("Frida Karlsson slår igenom",                2019, "sport", 0),
    ("Innebandy-VM: Sverige vs Finland",          2012, "sport", 1),
    ("USA vinner damfotbolls-VM",                 1999, "sport", 1),

    #FRITID 50 st
    ("LEGO lanseras",                             1958, "fritid", 0),
    ("Rubiks kub uppfinns",                       1974, "fritid", 1),
    ("Nintendo Game Boy släpps",                  1989, "fritid", 0),
    ("Första Harry Potter-boken ges ut",          1997, "fritid", 0),
    ("Första iPhone visas",                       2007, "fritid", 0),
    ("Spotify lanseras",                          2008, "fritid", 1),
    ("Instagram lanseras",                        2010, "fritid", 0),
    ("Minecraft släpps",                          2011, "fritid", 0),
    ("Pokémon GO-febern",                         2016, "fritid", 0),
    ("TikTok lanseras globalt",                   2018, "fritid", 0),
    ("Facebook lanseras",                         2004, "fritid", 0),
    ("Netflix börjar med streaming",              2007, "fritid", 0),
    ("Tamagotchi släpps",                         1996, "fritid", 1),
    ("Myspace lanseras",                          2003, "fritid", 1),
    ("PlayStation lanseras",                      1994, "fritid", 0),
    ("YouTube grundas",                           2005, "fritid", 0),
    ("Wii blir populärt partyspel",               2006, "fritid", 1),
    ("Second Life lanseras",                      2003, "fritid", 1),
    ("Wordle tar internet med storm",             2022, "fritid", 0),
    ("Animal Crossing slår rekord",               2020, "fritid", 1),
    ("Tetris lanseras i Sovjet",                  1984, "fritid", 1),
    ("Fortnite blir globalt fenomen",             2017, "fritid", 1),
    ("Clubhouse får genomslag",                   2021, "fritid", 1),
    ("E-sport blir stor globalt",                 2013, "fritid", 1),
    ("Candy Crush succé på mobilen",              2012, "fritid", 0),
    ("Snapchat lanseras",                         2011, "fritid", 0),
    ("Google lanseras",                           1998, "fritid", 0),
    ("Wikipedia grundas",                         2001, "fritid", 0),
    ("iPod revolutionerar musik",                 2001, "fritid", 0),
    ("Reddit grundas",                            2005, "fritid", 1),
    ("Netflix originalserie 'House of Cards'",    2013, "fritid", 1),
    ("The Sims släpps",                           2000, "fritid", 1),
    ("HBO Max lanseras",                          2020, "fritid", 1),
    ("Spotify Wrapped blir viralt",               2019, "fritid", 1),
    ("Google Maps revolutionerar navigation",     2005, "fritid", 1),
    ("Zoom-boomen under pandemin",                2020, "fritid", 0),
    ("Among Us blir viralt",                      2020, "fritid", 0),
    ("Netflix släpper Stranger Things",           2016, "fritid", 0),
    ("TikTok utmanar YouTube",                    2023, "fritid", 1),
    ("Spotify köper Joe Rogan-podden",            2020, "fritid", 1),
    ("Cyberpunk 2077 lanseras",                   2020, "fritid", 0),
    ("Elden Ring vinner 'Årets spel'",            2022, "fritid", 1),
    ("Facebook byter namn till Meta",             2021, "fritid", 0),
    ("Oculus Quest 2 släpps",                     2020, "fritid", 1),
    ("Super Mario Bros lanseras",                 1985, "fritid", 0),
    ("Netflix avskaffar lösenordsdelning",        2023, "fritid", 1),
    ("Spotify lanserar AI DJ",                    2023, "fritid", 1),
    ("Google Earth visas",                        2005, "fritid", 1),
    ("First-person shooters tar över",            1999, "fritid", 1),
    ("Netflix introducerar interaktiva filmer",   2018, "fritid", 1),
    ("Streaming går om linjär-TV",                2022, "fritid", 1),

    #HISTORIA 50 st
    ("Slaget vid Hastings",                        1066, "historia", 1),
    ("Första korståget inleds",                    1096, "historia", 1),
    ("Jerusalem intas av korståget",               1099, "historia", 0),
    ("Tredje korståget med Richard Lejonhjärta",   1189, "historia", 0),
    ("Magna Carta undertecknas",                   1215, "historia", 1),
    ("Hundraårskriget inleds",                     1337, "historia", 1),
    ("Digerdöden når Europa",                      1347, "historia", 0),
    ("Kalmarunionen bildas",                       1397, "historia", 1),
    ("Jan Hus bränns på bål",                      1415, "historia", 1),
    ("Joan of Arc befriar Orléans",                1429, "historia", 0),
    ("Gutenbergs tryckpress",                      1440, "historia", 0),
    ("Leonardo da Vinci föds",                     1452, "historia", 0),
    ("Columbus upptäcker Amerika",                 1492, "historia", 1),
    ("Reformationen inleds",                       1517, "historia", 1),
    ("Sverige blir protestantiskt",                1527, "historia", 0),
    ("Trettiåriga kriget börjar",                  1618, "historia", 1),
    ("Mayflower anländer till Amerika",            1620, "historia", 1),
    ("Vasaskeppet sjunker",                        1628, "historia", 0),
    ("Newton publicerar 'Principia Mathematica'",  1687, "historia", 1),
    ("Slaget vid Poltava",                         1709, "historia", 1),
    ("Tryckfrihetsförordningen i Sverige",         1766, "historia", 1),
    ("Boston Tea Party",                           1773, "historia", 1),
    ("Amerikanska självständigheten",              1776, "historia", 1),
    ("Franska revolutionen börjar",                1789, "historia", 1),
    ("Slaget vid Trafalgar",                       1805, "historia", 0),
    ("Slaget vid Waterloo",                        1815, "historia", 1),
    ("Darwin publicerar evolutionsteorin",         1859, "historia", 1),
    ("Tysklands enande",                           1871, "historia", 0),
    ("Bell konstruerar telefonen",                 1876, "historia", 0),
    ("Bolsjevikrevolutionen",                      1917, "historia", 1),
    ("Kvinnlig rösträtt i Sverige",                1921, "historia", 0),
    ("Berlinmurens fall",                          1989, "historia", 0),
    ("11 september-attackerna",                    2001, "historia", 0),
    ("Hitlers maktövertagande",                    1933, "historia", 1),
    ("Andra världskriget inleds",                  1939, "historia", 1),
    ("D-dagen: Invasionen i Normandie",            1944, "historia", 1),
    ("Förintelsen avslöjas",                       1945, "historia", 1),
    ("FN bildas",                                  1945, "historia", 0),
    ("Kalla kriget inleds",                        1947, "historia", 1),
    ("Kubakrisen",                                 1962, "historia", 1),
    ("Neil Armstrong går på månen",                1969, "historia", 0),
    ("Watergate-skandalen",                        1972, "historia", 1),
    ("Olof Palme mördas",                          1986, "historia", 0),
    ("Nelson Mandela blir president",              1994, "historia", 1),
    ("Terrorattack i London",                      2005, "historia", 0),
    ("Finanskrisen startar",                       2008, "historia", 1),
    ("Arabiska våren börjar",                      2010, "historia", 1),
    ("Brexit omröstningen",                        2016, "historia", 0),
    ("Ryssland invaderar Ukraina",                 2022, "historia", 1)

]

    cur.executemany(

        "INSERT INTO CARD(NAME, YEAR, CATEGORY, DIFFICULTY) VALUES (?,?,?,?)",
        cards
    )
    conn.commit()
    print(f"Initierade databasen med {len(cards)} kort.")
