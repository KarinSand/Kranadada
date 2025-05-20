import pathlib, sqlite3, random
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

BASE = pathlib.Path(__file__).resolve().parent
DB   = BASE / "database" / "cards_only.db"
DB.parent.mkdir(exist_ok=True)



app = Flask(__name__, static_folder="frontend")  
CORS(app, resources={r"/*": {"origins": "*"}})  

def fetch_cards(category):
    """Hämtar alla kort i angiven kategori (eller alla om 'normal')."""
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        if category == "normal":
            cur.execute("SELECT NAME, YEAR FROM CARD")
        else:
            cur.execute("SELECT NAME, YEAR FROM CARD WHERE CATEGORY = ?", (category,))
        return [{"title": n, "year": y} for n, y in cur.fetchall()]

@app.route("/categories")
def categories():
    return jsonify(["sport", "fritid", "historia", "normal"])

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

if __name__ == "__main__":
    app.run(debug=True, port=8000)
