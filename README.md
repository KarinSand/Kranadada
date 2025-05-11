# Kranadada
Krånådådå

Terminal spel (test.py)
Behöver ej ladda ner något, går att köra koden direkt i terminalen


# Tidslinjespelet – Flask Web App (game.py)

Det här är ett webbaserat kortspel byggt med **Flask** där spelaren ska placera historiska händelser i rätt ordning på en tidslinje. Projektet är inspirerat av spelet "Timeline".

## Funktionalitet

- Flask används för att skapa en webbserver med flera routes.
- Användaren kan spela ett spel där kort med historiska händelser placeras i kronologisk ordning.
- Korten genereras som Python-objekt och innehåller namn, årtal och en kort beskrivning.
- Webbsidor som `index.html`, `game.html`, `game_main.html`, etc. används för olika delar av spelet.

## Kom igång

### Förutsättningar

- Python 3.7+
- Flask

Installera Flask (om du inte redan gjort det):

```bash
pip install flask

Kör följande kommando i terminalen från projektmappen:
python app.py

Öppna sedan webbläsaren och gå till:
http://127.0.0.1:5000/

kranadada/
├── app.py
├── init_db.py
├── cards_only.db         # skapas automatiskt
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js 
