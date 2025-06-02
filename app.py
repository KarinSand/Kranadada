import pathlib, sqlite3, random
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

BASE = pathlib.Path(__file__).resolve().parent
DB   = BASE / "database" / "cards_only.db"
DB.parent.mkdir(exist_ok=True)

app = Flask(__name__, static_folder="frontend")  
CORS(app, resources={r"/*": {"origins": "*"}})  

def fetch_cards(category, difficulty=None):
    """Hämtar kort i angiven kategori och svårighetsgrad."""
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        if category == "normal":
            if difficulty in (0, 1):
                cur.execute("SELECT NAME, YEAR FROM CARD WHERE DIFFICULTY = ?", (difficulty,))
            elif difficulty == 2 or difficulty is None:
                cur.execute("SELECT NAME, YEAR FROM CARD WHERE DIFFICULTY IN (0, 1)")
            else:
                cur.execute("SELECT NAME, YEAR FROM CARD")
        else:
            if difficulty in (0, 1):
                cur.execute(
                    "SELECT NAME, YEAR FROM CARD WHERE CATEGORY = ? AND DIFFICULTY = ?",
                    (category, difficulty)
                )
            elif difficulty == 2 or difficulty is None:
                cur.execute(
                    "SELECT NAME, YEAR FROM CARD WHERE CATEGORY = ? AND DIFFICULTY IN (0, 1)",
                    (category,)
                )
            else:
                cur.execute("SELECT NAME, YEAR FROM CARD WHERE CATEGORY = ?", (category,))
        return [{"title": n, "year": y} for n, y in cur.fetchall()]


@app.route("/categories")
def categories():
    return jsonify(["sport", "fritid", "historia", "normal"])

@app.route("/questions")
def questions():
    cat = request.args.get("cat", "sport").lower()
    n = int(request.args.get("n", 5))
    try:
        difficulty = int(request.args.get("difficulty", 2))
    except ValueError:
        difficulty = 2

    pool = fetch_cards(cat, difficulty)

    if not pool:
        return jsonify({"error": "Inga kort hittades"}), 404

    return jsonify(random.sample(pool, min(n, len(pool))))

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:f>")
def static_files(f):
    return send_from_directory(app.static_folder, f)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
