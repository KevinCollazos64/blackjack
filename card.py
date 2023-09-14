from suit import Suits


class Card:

    ranks_to_values = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, "Jack": 10, "Queen": 10, "King": 10,
                       "Ace": [1, 11]}           # maps values according to blackjack rules

    def __init__(self, value, suit, facedown=False):
        self._value = value
        self._suit = suit
        self._facedown = facedown
        self.symbol = Suits.description_to_symbol[suit]
        self.full_desc = str(self.value) + self.symbol

    @property
    def value(self):
        return self._value

    @property
    def facedown(self):
        return self._facedown

    @facedown.setter
    def facedown(self, value):
        if value is type(bool):
            self.facedown = value


    @property
    def suit(self):
        return self._suit

    def show(self):
        if self.facedown is True:
            return "? of ?"
        else:
            print(f"{self.value} of {Suits.description_to_symbol[self.suit]}")




