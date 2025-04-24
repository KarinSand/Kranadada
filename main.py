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
class Timeline:
   """Manages the list of cards placed in the correct order."""
  
   def __init__(self):
       self.cards = []

   def add_card(self, card):
       """Add a card to the correct position based on the year."""
       position = self.find_correct_position(card)
       self.cards.insert(position, card)


   def find_correct_position(self, card):
       """Find the correct index to insert the card."""
       for i, existing_card in enumerate(self.cards):
           if card.year < existing_card.year:
               return i
       return len(self.cards)

   def is_correct_position(self, card, position):
       """Check if the card fits correctly at the chosen position."""
       if not self.cards:
           return True
       if position == 0:
           return card.year <= self.cards[0].year
       elif position == len(self.cards):
           return card.year >= self.cards[-1].year
       else:
           return self.cards[position - 1].year <= card.year <= self.cards[position].year

   def show(self):
       """Print all cards in the timeline."""
       if not self.cards:
           print("Timeline is empty.")
           return
       print("Timeline:")
       for idx, card in enumerate(self.cards):
           print(f"{idx}: {card.name} ({card.year})")

def clear_screen():
   os.system('cls' if os.name == 'nt' else 'clear')

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

def show_timeline(timeline):
  if not timeline:
      print("Tidslinjen är tom.")
      return
  print("Tidslinje:")
  for idx, card in enumerate(timeline):
      print(f"{idx}: {card.name} ({card.year})")

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

def start_game():
  deck = create_deck()
  timeline = []
  score = 0

  # Lägg ett första kort på tidslinjen
  first_card = deck.pop(0)  # Dra första kortet
  timeline.append(first_card)
  print(f"Startkort: {first_card.name} ({first_card.year}) har lagts på tidslinjen.")

  while deck:
       clear_screen()
       card = draw_card(deck)
       print(f"Beskrivning: {card.description}")


       show_timeline(timeline)
       position = int(input("Placera kortet på tidslinjen (ange index): "))


       if is_correct_position(card, timeline, position):
          print("Rätt!")
          timeline.insert(position, card)
          score += 1
       else:
          print(f"Fel! Kortet var från {card.year}.")
          # Ev. visa rätt plats, eller avsluta spelet

       if has_won(deck):
          print("Du vann!")
          break

  print("Spelet är slut.")

start_game()

