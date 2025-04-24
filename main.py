from flask import Flask, jsonify, request
import random

class Card:
  """Klassen fungerar så att varje kort har ett namn, årtal och en liten beskrivning."""
   def __init__(self, name, year, description):
      self.name = name
      self.year = year
      self.description = description

    def to_dict(self):
        """Konverterar kortet till JSON format."""
        return {
            "name": self.name,
            "year": self.year,
            "description": self.description
        }


class Node:
    """Noder för den länkade listan."""
    
    def __init__(self, card):
        self.card = card
        self.next = None


class LinkedList:
    """En länkad lista för att hålla korten i ordning."""
    
    def __init__(self):
        self.head = None

    def add(self, card):
        """"Lägg till ett kort i den länkade listan i ordning efter årtal."""
        new_node = Node(card)
        if not self.head:
            self.head = new_node
            return True

        current = self.head
        prev = None

        while current:
            if card.year < current.card.year:
                if prev:
                    prev.next = new_node
                else:
                    self.head = new_node
                new_node.next = current
                return True
            prev = current
            current = current.next
        
        prev.next = new_node
        return True

    def get_cards(self):
        """Returnerar en lista med alla kort i den länkade listan."""
        cards = []
        current = self.head
        while current:
            cards.append(current.card)
            current = current.next
        return cards


class Game:
    """Logik för spelet."""
    
    def __init__(self):
        self.deck = self.create_deck()
        random.shuffle(self.deck)
        self.timeline = LinkedList()
        self.current_card = None
        self.draw_card()
        self.add_initial_card()

    def create_deck(self):
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

    def draw_card(self):
        """Dra ett kort från kortleken."""
        if self.deck:
            self.current_card = self.deck.pop(0)
        else:
            self.current_card = None

    def add_initial_card(self):
        """Lägger till det första kortet i tidslinjen."""
        if self.current_card:
            self.timeline.add(self.current_card)

    def place_card(self):
        """Lägger ett kort på tidslinjen."""
        if self.timeline.add(self.current_card):
            year = self.current_card.year
            self.draw_card()
            return year
        return None

    def check_win(self):
        """Kollar om spelaren har vunnit eller inte."""
        return len(self.timeline.get_cards()) >= 10


game = Game()

@app.route('/start', methods=['GET'])
def start_game():
    """Starta nytt spel."""
    game.__init__()  # Reset game
    return jsonify({
        "message": "Spelet har startat!",
        "timeline": [card.to_dict() for card in game.timeline.get_cards()],
        "current_card": game.current_card.to_dict() if game.current_card else None
    })


@app.route('/draw', methods=['GET'])
def draw():
    """Dra ett nytt kort."""
    game.draw_card()
    if game.current_card:
        return jsonify({
            "current_card": game.current_card.to_dict(),
            "timeline": [card.to_dict() for card in game.timeline.get_cards()]
        })
    return jsonify({"message": "Inga kort kvar i kortleken."})


@app.route('/place_card', methods=['POST'])
def place_card():
    """Försök att lägga kortet på tidslinjen."""
    year = game.place_card()
    if year is not None:
        return jsonify({
            "message": f"Kortet har lagts till! Årtal: {year}",
            "timeline": [card.to_dict() for card in game.timeline.get_cards()]
        })
    return jsonify({"message": "Kortet kan inte läggas till på tidslinjen, försök igen."})


@app.route('/check_win', methods=['GET'])
def check_win():
    """Kollar om spelet är vunnit."""
    if game.check_win():
        return jsonify({"message": "Grattis! Du har vunnit spelet!", "timeline": [card.to_dict() for card in game.timeline.get_cards()]})
    return jsonify({"message": "Spelet pagar, fortsatt spela!"})


if __name__ == '__main__':
    app.run(debug=True)
