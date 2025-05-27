import pathlib, sqlite3, random
from flask import Flask, jsonify, request, send_from_directory, render_template_string, redirect, url_for, flash
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

BASE = pathlib.Path(__file__).resolve().parent
DB   = BASE / "database" / "cards_only.db"
DB.parent.mkdir(exist_ok=True)

app = Flask(__name__, static_folder="frontend")
app.secret_key = 'Quite-super-secret-key'  # required by Flask-Login

CORS(app, resources={r"/*": {"origins": "*"}})

# --- Flask-Login setup ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# In-memory user storeage
users = {
    'admin': {'id': '1', 'username': 'admin', 'password': 'secret'}
}

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def get(username):
        user = users.get(username)
        if user:
            return User(user['id'], user['username'], user['password'])
        return None

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user['id'] == user_id:
            return User(user['id'], user['username'], user['password'])
    return None

# Routes
# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.get(username)
        if user and user.password == password:
            login_user(user, remember=True)
            return redirect("/")
        flash("Fel användarnamn eller lösenord")
    return render_template_string('''
        <form method="POST">
            <label>Användarnamn: <input type="text" name="username"></label><br>
            <label>Lösenord: <input type="password" name="password"></label><br>
            <input type="submit" value="Logga in">
        </form>
    ''')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

def fetch_cards(category):
    """Hämtar alla kort i angiven kategori (eller alla om 'normal')."""
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        if category == "normal":
            cur.execute("SELECT NAME, YEAR FROM CARD")
        else:
            cur.execute("SELECT NAME, YEAR FROM CARD WHERE CATEGORY = ?", (category,))
        return [{"title": n, "year": y} for n, y in cur.fetchall()]
#categories
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
