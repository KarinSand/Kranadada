# Kranadada
Krånådådå

För att starta filen behöver flask vara installerat på datorn via Pip.


Exekvera filen för att starta spelet.

Skriv in följande i terminal:

Invoke-WebRequest -Uri http://127.0.0.1:5000/start

Dra kort.
Invoke-WebRequest -Uri http://127.0.0.1:5000/draw

Placera kort på tidslinje, skall upprepas 10 gånger för att check_win ska visa att ni har vunnit.
Invoke-WebRequest -Uri http://127.0.0.1:5000/place_card -Method POST

Kan köras efter varje place_card har körts.
Invoke-WebRequest -Uri http://127.0.0.1:5000/check_win
