# Kranadada
Krånådådå

Terminal spel (test.py)
Behöver ej ladda ner något, går att köra koden direkt i terminalen


# Tidslinjespelet – Flask Web App (game.py)

Det här är ett webbaserat kortspel byggt med **Flask** där spelaren ska placera historiska händelser i rätt ordning på en tidslinje. Projektet är inspirerat av spelet "Timeline".

## 🃏 Funktionalitet

- Flask används för att skapa en webbserver med flera routes.
- Användaren kan spela ett spel där kort med historiska händelser placeras i kronologisk ordning.
- Korten genereras som Python-objekt och innehåller namn, årtal och en kort beskrivning.
- Webbsidor som `index.html`, `game.html`, `game_main.html`, etc. används för olika delar av spelet.

## 🚀 Kom igång

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

# Mappstrukturen ska se ut såhär
/
├── templates/
│   ├── index.html
│   ├── contact.html
│   ├── highscore.html
│   ├── game.html
│   ├── game_main.html
│   ├── game_sport.html
│   ├── game_fun.html
│   ├── game_war_politic.html
│   ├── game_inventings.html
│   └── play.html
├── static/
│   ├── script.js
│   ├── style.css
├── game.py
└── README.md
