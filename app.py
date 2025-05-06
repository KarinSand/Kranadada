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
    cursor.execute("SELECT NAME, YEAR FROM CARD")  # Använd "CARD" istället för "events"
    rows = cursor.fetchall()
    conn.close()
    events = [{"title": row[0], "year": row[1]} for row in rows]
    return jsonify(events)


if __name__ == "__main__":
    app.run(debug=True)
