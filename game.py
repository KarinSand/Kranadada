from flask import Flask, render_template, jsonify, request
import sqlite3
import random
from database.init_db import init_db
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/highscore')
def highscore():
    return render_template('highscore.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/game_main')
def game_main():
    return render_template('game_main.html')

@app.route('/game_sport')
def game_sport():
    return render_template('game_sport.html')

@app.route('/game_war_politic')
def game_war_politic():
    return render_template('game_war_politic.html')

@app.route('/game_fun')
def game_fun():
    return render_template('game_fun.html')

@app.route('/game_inventings')
def game_inventings():
    return render_template('game_inventings.html')

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

class Card:
    """Klassen fungerar så att varje kort har ett namn, årtal och en liten beskrivning."""
    
    def __init__(self, name, year, description):
        self.name = name
        self.year = year
        self.description = description

    def to_dict(self):
        #Konverterar kortet till JSON format.

        return {
            "name": self.name,
            "year": self.year,
            "description": self.description
        }

def create_deck():
    """Skapar kortlek korten genererade via AI."""

    return [
        Card("Första månen", 1969, "Människan satte sin fot på månen."),
        Card("Berlinmurens fall", 1989, "Berlinmuren föll."),
        Card("Internet föds", 1983, "Det moderna internet föds."),
        Card("Facebook lanseras", 2004, "Sociala medier revolutioneras."),
        Card("Smartphone revolutionen", 2007, "Den första iPhone lanseras."),
        Card("COVID-19-pandemin", 2019, "Pandemin påverkar världen."),
        Card("Klimatavtal i Paris", 2015, "Världens länder enas om klimatavtal."),
        Card("AI blir mainstream", 2020, "Artificiell intelligens blir allmänt tillgänglig."),
        Card("Mars rover Perseverance", 2021, "Rover landar på Mars."),
        Card("Svenska folket röstar", 2022, "Svenska folket röstar i valet."),
    ]

def draw_card(deck):
    """Drar ett slumpmässigt kort från kortleken och tar bort det från leken."""

    card = random.choice(deck)
    deck.remove(card)
    return card

def is_correct_position(card, timeline, position):
    if not timeline:
        return True  # Första kortet – alltid korrekt

    if position == 0:
        return card.year <= timeline[0].year
    elif position == len(timeline):
        return card.year >= timeline[-1].year
    else:
        return timeline[position - 1].year <= card.year <= timeline[position].year

def has_won(deck):
    return len(deck) == 0

@app.route('/game_main')
def game_main():
    return render_template('game_main.html')

@app.route('/start_game', methods=['GET', 'POST'])
def start_game():
    if request.method == 'POST':
        deck = create_deck()
        timeline = []
        score = 0

        # Lägg ett första kort på tidslinjen
        first_card = deck.pop(0)
        timeline.append(first_card)

        return render_template('play.html', first_card=first_card.to_dict(), timeline=[first_card.to_dict()], score=score)

    # Om GET-anrop (t.ex. direkt från URL), visa bara formulär eller startsida
    return render_template('game_main.html')


@app.route('/draw_card', methods=['POST'])
def draw_card_route():
    data = request.json
    deck = [Card(**card) for card in data['deck']]
    card = draw_card(deck)
    timeline = [Card(**card) for card in data['timeline']]
    position = data['position']
    
    if is_correct_position(card, timeline, position):
        timeline.insert(position, card)
        return jsonify({
            'result': 'correct',
            'timeline': [card.to_dict() for card in timeline],
            'card': card.to_dict()
        })
    else:
        return jsonify({
            'result': 'incorrect',
            'card': card.to_dict()
        })

if __name__ == '__main__':
    app.run(debug=True)

