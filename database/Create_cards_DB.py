import sqlite3  # SQLite for the database

# Create and connect to the database
conn = sqlite3.connect('cards_only.db')
cursor = conn.cursor()

# Skapa tabell för kort
cursor.execute("""
CREATE TABLE IF NOT EXISTS CARD (
    CARD_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME VARCHAR(100) NOT NULL,
    YEAR INTEGER,
    DESCRIPTION TEXT
);
""")


# Lägger till kort med titel, årtal, beskrivning samt koppling till kategori/subkategori
cards = [
    ("First Moon Landing", 1969, "Humans set foot on the moon."),
    ("Fall of the Berlin Wall", 1989, "The Berlin Wall fell."),
    ("Birth of the Internet", 1983, "Modern internet is born."),
    ("Facebook Launch", 2004, "Social media revolution begins."),
    ("Smartphone Revolution", 2007, "The first iPhone is launched."),
    ("COVID-19 Pandemic", 2019, "Pandemic affects the world."),
    ("Paris Climate Agreement", 2015, "Nations agree on climate actions."),
    ("AI Goes Mainstream", 2020, "Artificial Intelligence becomes widely available."),
    ("Mars Rover Perseverance", 2021, "Rover lands on Mars."),
    ("Swedes Vote", 2022, "Swedes participate in the election.")

]
 
cursor.executemany("""
INSERT INTO CARD (NAME, YEAR, DESCRIPTION)
VALUES (?, ?, ?)
""", cards)

# Sparar och stänger anslutning
conn.commit()
conn.close()
