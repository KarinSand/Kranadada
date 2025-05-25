from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/events")
def get_events():
    conn = sqlite3.connect("cards_only.db")
    cursor = conn.cursor()
    cursor.execute("SELECT NAME, YEAR FROM CARD")
    rows = cursor.fetchall()
    conn.close()
    events = [{"title": row[0], "year": row[1]} for row in rows]
    return jsonify(events)

# G07-199 - ledtrådar
@app.route("/hint/<title>")
def get_hint(title):
    print(f"[DEBUG] Hintförfrågan för: {title}")
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    title = title.rsplit(" (", 1)[0].strip()

    cursor.execute("SELECT YEAR FROM CARD WHERE LOWER(NAME) = LOWER(?)", (title.lower(),))
    row = cursor.fetchone()
    conn.close()

    if row:
        year = row[0]
        lower = year - 45
        upper = year + 45
        return jsonify({"hint": f"Händelsen inträffade mellan {lower} och {upper}."})
    else:
        return jsonify({"hint": "Ingen ledtråd hittades."}), 404


if __name__ == "__main__":
    app.run(debug=True)
