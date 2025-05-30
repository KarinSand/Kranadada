import pathlib, sqlite3, random
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
#------------  Grundläggande setup
BASE = pathlib.Path(__file__).resolve().parent
DB   = BASE / "database" / "cards_only.db"
DB.parent.mkdir(exist_ok=True)

app = Flask(__name__, static_folder="frontend")  
CORS(app, resources={r"/*": {"origins": "*"}})  

def fetch_cards(category):
    """Hämtar alla kort i angiven kategori (eller alla om 'blandat')."""
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        if category == "blandat":
            cur.execute("SELECT NAME, YEAR FROM CARD")
        else:
            cur.execute("SELECT NAME, YEAR FROM CARD WHERE CATEGORY = ?", (category,))
        return [{"title": n, "year": y} for n, y in cur.fetchall()]

@app.route("/categories")
def categories():
    return jsonify(["sport", "historia", "blandat"])

@app.route("/questions")
def questions():
    cat = request.args.get("cat", "sport").lower()
    n   = int(request.args.get("n", 5))
    pool = fetch_cards(cat)
    if not pool:
        return jsonify({"error": "Kategori saknas"}), 404
    return jsonify(random.sample(pool, min(n, len(pool))))

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:f>")
def static_files(f):
    return send_from_directory(app.static_folder, f)

# G07-199 - ledtrådar
from flask import request, jsonify
import sqlite3

@app.route("/hint/<title>")
def get_hint(title):
    # Rensa bort ev. suffix
    clean = title.rsplit(" (", 1)[0].strip()
    

    # Använd samma DB-väg som övriga API:t
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT YEAR FROM CARD WHERE LOWER(NAME) = LOWER(?)",
        (clean.lower(),)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"hint": "Ingen ledtråd hittades."}), 404

    year  = row[0]
    lower = year - 25
    upper = year + 25
    hint  = f"Händelsen inträffade mellan {lower} och {upper}."
    return jsonify({"hint": hint})
if __name__ == "__main__":
    app.run(debug=True, port=8000)
