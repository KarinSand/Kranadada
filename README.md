# Kranadada
Krånådådå

# Tidslinjespelet – Flask Web App (game.py)

Det här är ett webbaserat kortspel byggt med **Flask** där spelaren ska placera historiska händelser i rätt ordning på en tidslinje. Projektet är inspirerat av spelet "Timeline" och "Chronological".

**Funktionalitet**
-Flask används för att servera webbsidan och hämta kortdata via en API-route (/events)
-Händelserna sparas i en SQLite-databas (cards_only.db)
-Spelaren drar och släpper kort till rätt plats i en tidslinje
-Poängsystem för rätt/fel placeringar

## Kom igång
Förutsättningar: 
Python 3.7 eller nyare
Flask

===Installera Flask genom att skriva detta i terminalen:
pip install flask===

### Starta spelet
Klona projektet (om du inte redan gjort det):
git clone https://github.com/KarinSand/Kranadada.git
cd Kranadada

Gå till mappen där dina projektfiler ligger.
Kör detta kommando för att skapa databasen med historiska händelser:
python3 database/init_db.py
Kör följande kommando i terminalen från projektmappen:
python3 app.py

**När servern startas:** 
Öppna webbläsaren och gå till den adress som visas, det bör vara:
http://127.0.0.1:8000/

Spelet ska nu laddas i webbläsaren.

**Mappstruktur** – så här ska filerna ligga:

kranadada/
├── app.py
├── init_db.py
├── cards_only.db         (skapas automatiskt, gitignore)
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js 
├── .gitignore
└── README.md
