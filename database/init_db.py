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


# Lägger till kort med titel, årtal, beskrivning samt koppling till kategori/subkategori
kort = [
    ("Första månen", 1969, "Människan satte sin fot på månen.", 3, 1),
    ("Berlinmurens fall", 1989, "Berlinmuren föll.", 2, 9),
    ("Internet föds", 1983, "Det moderna internet föds.", 1, 2),
    ("Facebook lanseras", 2004, "Sociala medier revolutioneras.", 1, 3),
    ("Smartphone revolutionen", 2007, "Den första iPhone lanseras.", 1, 4),
    ("COVID-19-pandemin", 2019, "Pandemin påverkar världen.", 4, 5),
    ("Klimatavtal i Paris", 2015, "Världens länder enas om klimatavtal.", 4, 6),
    ("AI blir mainstream", 2020, "Artificiell intelligens blir allmänt tillgänglig.", 1, 7),
    ("Mars rover Perseverance", 2021, "Rover landar på Mars.", 3, 1 ),
    ("Svenska folket röstar", 2022, "Svenska folket röstar i valet.", 2, 8) 
]
 
cursor.executemany("""
INSERT INTO KORT (NAMN, ÅRTAL, BESKRIVNING, KATEGORI_ID, SUBKATEGORI_ID)
VALUES (?, ?, ?, ?, ?)
""", kort)   

# Sparar och stänger anslutning
conn.commit()
conn.close()
