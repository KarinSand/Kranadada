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

Förutsättningar: Python 3.7 eller nyare samt Git bör finnas installerat.
Klona projektet från GitHub:
git clone https://github.com/KarinSand/Kranadada.git
cd Kranadada

Skapa och aktivera ett virtuellt Python-miljö (valfritt men rekommenderat):
python3 -m venv venv
source venv/bin/activate   # på Windows: venv\Scripts\activate

Installera Python-beroenden:
pip install flask flask-cors

Initiera databasen (om den inte redan finns eller om du vill uppdatera datan):
python3 database/init_db.py
Detta skapar eller uppdaterar cards_only.db i mappen database/ med exempeldata.

Starta Flask-servern:
python3 app.py
Öppna webbläsaren och navigera till http://127.0.0.1:8000. Spelet laddas då upp.


**Mappstruktur** – så här ska filerna ligga:

Kranadada/
├── app.py               # Huvudprogram (Flask-server)
├── cards_only.db        # (valfri databas-kopia i projektets rot, ej nödvändig)
├── database/
│   ├── cards_only.db    # SQLite-databas med händelsekort (används av spelet)
│   └── init_db.py       # Skript för att skapa/populera databasen
├── frontend/
│   ├── index.html       # Spel-HTML (huvudsidan)
│   ├── script.js        # Spel-logik (JavaScript)
│   └── style.css        # Styling (CSS)
├── .gitignore           # Ignorerade filer för Git
└── README.md            # Denna dokumentation

Användning

Kategorival: Välj en kategori genom att klicka på knappen (Sport, Historia, Blandat eller Fritid).
Svårighetsgrad: Efter kategorivalet väljs svårighetsgrad (Lätt, Svår eller Normal). Normal blandar enkla och svåra kort.

Spelstart: Läs instruktionerna (instruktionsfönstret) och klicka sedan för att starta spelet. Första kortet dras automatiskt in i tidslinjen.

Dra och släpp: Dra det synliga kortet från högen och släpp det på en ledig plats på tidslinjen. Kom ihåg: äldsta händelsen längst till vänster, nyaste till höger.

Poäng och liv: Rätt placering ger +1 poäng. Felplacering ger -1 poäng (minst 0) och räknas som ett misstag för det kortet. Efter två fel på samma kort visas en ledtråd. Om 3-livsläge är aktiverat (knapp 3-livsläge) förlorar spelaren ett liv vid varje felplacering. Spelet slutar om liven tar slut.

Gamble-läge: Klicka på Aktivera gamble-läge för att börja samla flera kort på tidslinjen utan omedelbar kontroll. Efter att ha placerat önskat antal kort klickar du på Kolla kort för att kontrollera alla. Om alla är rätt får du bonuspoäng (2 poäng per kort); om något är fel förlorar du de placerade korten tillbaka till leken och ett liv.

Andra knappar: Välj annan kategori tar dig tillbaka till startsidan för att välja kategori på nytt. Omstart börjar om spelet med samma inställningar.

Spelavslut: Spelet avslutas automatiskt efter 10 kort (en hel omgång) eller när liven tar slut. Ett resultatfönster visas med totalpoängen.
Mappstruktur