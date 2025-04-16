import sqlite3  # SQLite för databasen

# Skapa databasen och kopplar upp
conn = sqlite3.connect('min_databas.db')
cursor = conn.cursor()

# Skapa tabell för huvudkategorier
cursor.execute("""
CREATE TABLE IF NOT EXISTS KATEGORI (
    KATEGORI_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAMN VARCHAR(50) NOT NULL
);
""")

# Skapa tabell för underkategorier
cursor.execute("""
CREATE TABLE IF NOT EXISTS SUBKATEGORI (
    SUBKATEGORI_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAMN VARCHAR(50) NOT NULL,
    KATEGORI_ID INTEGER,
    FOREIGN KEY (KATEGORI_ID) REFERENCES KATEGORI(KATEGORI_ID)
);
""")
# Skapa tabell för spelkorten
cursor.execute("""
CREATE TABLE IF NOT EXISTS KORT (
    KORT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAMN VARCHAR(100) NOT NULL,
    ÅRTAL INTEGER,
    BESKRIVNING TEXT,
    HUR VARCHAR(200),
    KATEGORI_ID INTEGER,
    SUBKATEGORI_ID INTEGER,
    FOREIGN KEY (KATEGORI_ID) REFERENCES KATEGORI(KATEGORI_ID),
    FOREIGN KEY (SUBKATEGORI_ID) REFERENCES SUBKATEGORI(SUBKATEGORI_ID)
);
""")


# Lägger till huvudkategorier – Teknik, Politik osv.
kategorier = [('Teknik',), ('Politik',), ('Vetenskap',), ('Samhälle',)]
cursor.executemany("INSERT INTO KATEGORI (NAMN) VALUES (?)", kategorier)

# Hämtar KATEGORI_ID för varje kategori baserat på namn
cursor.execute("SELECT KATEGORI_ID FROM KATEGORI WHERE NAMN = 'Teknik'")
teknik_ID = cursor.fetchone()[0]

cursor.execute("SELECT KATEGORI_ID FROM KATEGORI WHERE NAMN = 'Politik'")
politik_ID = cursor.fetchone()[0]

cursor.execute("SELECT KATEGORI_ID FROM KATEGORI WHERE NAMN = 'Vetenskap'")
vetenskap_ID = cursor.fetchone()[0]

cursor.execute("SELECT KATEGORI_ID FROM KATEGORI WHERE NAMN = 'Samhälle'")
samhälle_ID = cursor.fetchone()[0]

# Lägger till subkategorier och koppla dem huvudkategori
subkategorier = [
    ('Rymden', vetenskap_ID),
    ('Internet', teknik_ID),
    ('Sociala medier', teknik_ID),
    ('Mobilteknologi', teknik_ID),
    ('Pandemier', samhälle_ID),
    ('Klimat', samhälle_ID),
    ('AI', teknik_ID),
    ('Val', politik_ID),
    ('Historia', politik_ID)
]
cursor.executemany("INSERT INTO SUBKATEGORI (NAMN, KATEGORI_ID) VALUES (?, ?)", subkategorier)
