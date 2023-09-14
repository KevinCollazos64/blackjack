from suit import Suits
from card import Card
import random


class Deck:

    def __init__(self):
        self._deck = []
        self.build()

    @property
    def deck(self):
        return self._deck

    @deck.setter
    def deck(self, value):
        if isinstance(value, list):
            self.deck = value
        else:
            raise TypeError("Please give the deck a correct format")

    def build(self):
        for suit in Suits.description_to_symbol:
            for rank in Card.ranks_to_values:
                self.deck.append(Card(rank, suit))

    def shuffle(self):
        return random.shuffle(self.deck)

    def show(self):
        for card in self.deck:
            print(card.show())

    def deckpop(self, facedown=False):
        if not self.deck:
            self.build()

        card = self.deck.pop()
        if facedown is True:
            card.facedown = True
        return card





