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
