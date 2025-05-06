import sqlite3

def init_db():
    conn = sqlite3.connect('cards_only.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS CARD (
        CARD_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME TEXT NOT NULL,
        YEAR INTEGER NOT NULL,
        DESCRIPTION TEXT
    );
    """)

    cursor.execute("SELECT COUNT(*) FROM CARD")
    if cursor.fetchone()[0] == 0:
        cards = [
            ("Gutenbergs tryckpress", 1440, ""),
            ("Stockholms blodbad", 1520, ""),
            ("Columbus upptäcker Amerika", 1492, ""),
            ("Vasaskeppet sjunker", 1628, ""),
            ("Franska revolutionen", 1789, ""),
            ("Första världskriget börjar", 1914, ""),
            ("Kvinnlig rösträtt införs i Sverige", 1921, ""),
            ("Andra världskriget slutar", 1945, ""),
            ("Första månpromenaden", 1969, ""),
            ("Digerdöden når Europa", 1347, ""),
            ("Kalmarunionen bildas", 1397, ""),
            ("GameStop-aktien exploderar p.g.a. Reddit", 2021, "")
            ("FIFA grundas", 1904, ""),
            ("Jan Hus bränns på bål", 1415, ""),
            ("Joan of Arc befriar Orléans", 1429, ""),
            ("Tredje korståget med Richard Lejonhjärta", 1189, ""),
            ("Sverige blir protestantiskt", 1527, ""),
            ("Berlinmurens fall", 1989, ""),
            ("Röntgen upptäcker röntgenstrålning", 1895, ""),
            ("Marie Curie isolerar radioaktivt material", 1898, ""),
            ("Einstein publicerar relativitetsteorin", 1905, ""),
            ("Penicillin upptäcks av Alexander Fleming", 1928, ""),
            ("Första korståget inleds", 1096, ""),
            ("Jerusalem intas av korsfarare", 1099, ""),
            ("Terroattacken 9/11", 2001, ""),
            ("Amerikanska självständighetsförklaringen", 1776, ""),
            ("Covid-19 förklaras som pandemi", 2020, ""),
            ("Titanic sjunker", 1912, ""),
            ("Kärnkraftsolyckan i Tjernobyl", 1986, ""),
            ("Barack Obama blir president", 2008, ""),
            ("Sveriges inträde i EU", 1995, ""),
            ("Mordet på Olof Palme", 1986, ""),
            ("Leonardo da Vinci föds", 1452, ""),
            ("Trettiåriga kriget börjar", 1618, ""),
        ]
        cursor.executemany("INSERT INTO CARD (NAME, YEAR, DESCRIPTION) VALUES (?, ?, ?)", cards)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
