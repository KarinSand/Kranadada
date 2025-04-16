import sqlite3  # SQLite för databasen

# Skapa databasen och kopplar upp
conn = sqlite3.connect('min_databas.db')
cursor = conn.cursor()

# Skapa tabellen för huvudkategorier
cursor.execute("""
CREATE TABLE IF NOT EXISTS KATEGORI (
    KATEGORI_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAMN VARCHAR(50) NOT NULL
);
""")

# Skapa tabellen för underkategorier
cursor.execute("""
CREATE TABLE IF NOT EXISTS SUBKATEGORI (
    SUBKATEGORI_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAMN VARCHAR(50) NOT NULL,
    KATEGORI_ID INTEGER,
    FOREIGN KEY (KATEGORI_ID) REFERENCES KATEGORI(KATEGORI_ID)
);
""")

