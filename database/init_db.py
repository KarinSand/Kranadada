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
            ("Columbus upptäcker Amerika", 1492, ""),
            ("Vasaskeppet sjunker", 1628, ""),
            ("Franska revolutionen", 1789, ""),
            ("Första världskriget börjar", 1914, ""),
            ("Kvinnlig rösträtt införs i Sverige", 1921, ""),
            ("Andra världskriget slutar", 1945, ""),
            ("Första månpromenaden", 1969, ""),
            ("Berlinmurens fall", 1989, ""),
            ("Terroattacken 9/11", 2001, ""),
            ("Covid-19 förklaras som pandemi", 2020, "")
        ]
        cursor.executemany("INSERT INTO CARD (NAME, YEAR, DESCRIPTION) VALUES (?, ?, ?)", cards)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
