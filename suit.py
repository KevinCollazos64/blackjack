class Suits:

    description_to_symbol = {"Diamonds": '\033[91m♦\033[0m', "Clubs": "\033[30m♣\033[0m", "Hearts": "\033[91m♥\033[0m",
                             "Spades": "\033[30m♠\033[0m"}

    def __init__(self, description):
        self._description = description
        self.symbol = Suits.description_to_symbol[description]
