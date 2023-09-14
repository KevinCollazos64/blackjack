from card import Card


class Player:

    def __init__(self, ishuman = False):
        self._hand = []
        self._HP = 100
        self._ishuman = ishuman

    @property
    def hand(self):
        return self._hand

    @hand.setter
    def hand(self, value):
        if isinstance(value, list):

            self._hand = value
        else:
            raise ValueError ("Please enter a valid input")

    @property
    def HP(self):
        return self._HP

    @HP.setter
    def HP(self, value):
        self._HP = value

    def increment(self, value):
        self.HP += value

    def decrement(self, value):
        self.HP -= value

    @property
    def ishuman(self):
        return self._ishuman

    def show_hand(self):  # tweak after finishing card class
        if self.ishuman is True:
            for c in self.hand:
                print(c.full_desc, end=' ')
        elif self.ishuman is False:
            for c in self.hand:
                c.facedown=False
                print(c.full_desc, end=' ')

    def hit(self, new_card):
        # deck pops card into player hand
        if isinstance(new_card, Card):
            if self.ishuman is False and len(self.hand) >= 2:
                print(f"Dealer hit: {str(new_card.value) + new_card.symbol}")

            elif self.ishuman is False:
                new_card.facedown = True
                print("Dealer hit: ???")

            else:
                print(f"You hit: {str(new_card.value) + new_card.symbol}")

            self.hand.append(new_card)

        # then display new hand with new card (initially start with two)
        else:
            return "Invalid Card"

    def dealer_show(self, turn):
        if self.ishuman is False and turn == 0:
            first = self.hand[0]
            print(f"Dealer flips...{str(first.value)+first.symbol}, ???")
        elif self.ishuman is False and turn > 0:
           self.show_hand()

    def split(self):
        if len(self.hand) == 2:

            first = [self.hand[0]]
            second = [self.hand[1]]
            self.hand = [first] + [second]
            print(f"New hand 1: [{str(first[0].value)+first[0].symbol}]\nNew hand 2: [{str(second[0].value)+second[0].symbol}]")
            return first, second

        else:
            return "Ineligible to split!"

# face down attribute for Card class available to dealer only (create clone when fd, and fu)
# dealing could be 2 calls of hit, when round starts
# set round bet to input of player stake