from Player_class import Player
from deck import Deck


class Game:

    def __init__(self):
        self.deck = Deck()  # implement so that it shuffles deck on initialization
        self.deck.shuffle()
        self._dealer = Player()
        self._player = Player(ishuman=True)
        self._stake = 0


    @property
    def dealer(self):
        return self._dealer

    @property
    def player(self):
        return self._player

    @property
    def stake(self):
        return self._stake

    @stake.setter
    def stake(self, value):
        if isinstance(value, int) and value >= 5:
            self._stake = value

    def game_winner(self):
        if self.player.HP <= 0:
            return "Dealer Wins!"

        elif self.dealer.HP <= 0:
            return "Player Wins!"

    def game_over(self):
        return '***Thanks for Playing***!'

    def hand_winner(self, winner, loser, stake):
        winner.increment(stake)
        loser.decrement(stake)
        bluebar = '\033[94m''\u2588'
        redbar = '\033[91m''\u2588'
        print(
            f"Your HP: {self.player.HP} {bluebar * round((self._player.HP // 10))}{redbar * round((self.dealer.HP // 10))}\033[0m"
            f" Dealer HP: {self.dealer.HP}")

    def compare(self, p1, p2):
        if 21 >= self.count(p1) > self.count(p2):
            print("--PLAYER WINS!--")
            self.hand_winner(p1, p2, self.stake)

        elif self.count(p1) == self.count(p2):
            print("ITS A TIE!")
            self.hand_winner(p1, p2, 0)

        elif self.count(p1) < self.count(p2) <= 21:
            if self.count(p2) == 21:
                print("\033[33m~~DEALER BLACKJACK~~\033[0m")
                self.hand_winner(p2, p1, self.stake*1.5)

            else:
                print("--DEALER WINS!--")
                self.hand_winner(p2, p1, self.stake)

    def surrender(self):
        print("Surrendered! \n")
        self.hand_winner(self.dealer, self.player, self.stake)

    def count(self, player):
        hand_value = 0
        # separate ace from non-ace and consider ace last when adding card values to know whether 1 or 11
        ace = [ace for ace in player.hand if isinstance(ace.ranks_to_values[ace.value], list)]
        not_ace = [not_ace for not_ace in player.hand if isinstance(not_ace.ranks_to_values[not_ace.value], int)]
        player.hand = not_ace + ace
        for c in player.hand:
            if not type(c.ranks_to_values[c.value]) == list:
                hand_value += c.ranks_to_values[c.value]
            else:
                if hand_value + c.ranks_to_values[c.value][1] > 21:
                    hand_value += c.ranks_to_values[c.value][0]
                else:
                    hand_value += c.ranks_to_values[c.value][1]
        return hand_value

    def dealermove(self, dealerturn):
        self.dealer.dealer_show(dealerturn)
        # If dealer has card count 17 or greater, they always stand
        if 21 >= self.count(self.dealer) >= 17:
            return dealerturn+1
            # dealer finishes move once they are within this range
        # If dealer has card count of 16 or less, dealer always hits
        elif self.count(self.dealer) <= 16:
            while self.count(self.dealer) < 17:
                new = self.deck.deckpop()
                self.dealer.hit(new)
                self.dealermove(dealerturn+1)
        elif self.checkbust(self.dealer):
            self.hand_winner(self.player, self.dealer, self.stake)

    def splithit(self, player, handone, handtwo):
        player.hand = handone
        self.selectedhit(player)
        countone = self.count(player)

        player.hand = handtwo
        self.selectedhit(self.player)
        counttwo = self.count(player)

        # as long as player has one hand in play
        if countone <= 21 or counttwo <= 21:
            print("DEALER REVEALS...")
            self.dealermove(1)
            if self.checkbust(self.dealer):
                if countone >= 21 or counttwo >= 21:
                    self.hand_winner(player, self.dealer, self.stake)
                else:
                    self.hand_winner(player, self.dealer, self.stake)
                    # not *2 because dealer move already take off 1x
            # account for when dealer gets blackjack and play may have blackjack
            elif self.BlackJack(self.dealer):
                if countone == 21 and counttwo == 21:
                    print('\033[32m-Both hands PUSH!-\033[0m]')
                    self.hand_winner(self.dealer, player, self.stake * 3) # player auto gets 1.5x stake when BJ,
                    # so must revert HP bars to initial status since the play became a push
                elif countone == 21 or counttwo == 21:
                    print('\033[32m-One hand PUSH!-\033[0m]')
                    self.hand_winner(self.dealer, player, self.stake * 1.5)

                else:
                    if countone > 21 or counttwo > 21:
                        self.hand_winner(self.dealer, player, self.stake)
                    else:
                        self.hand_winner(self.dealer, player, self.stake * 2)
            # change so if you hit blackjack on one hand it doesn't remove another stake if dealer hand loses again
            # will implement this with a condition after the dealer goes that checks if dealer busts and count one/two
            # is also over 21 the player RE-GAINS HP instead of just not losing any HP to simplify implementation
            else:
                if 21 >= countone >= self.count(self.dealer):
                    if countone == self.count(self.dealer):
                        print('\nHand 1 Ties!')
                        self.hand_winner(player, self.dealer, 0)
                    else:
                        print('\nHand 1 wins!')
                        self.hand_winner(self.player, self.dealer, self.stake)
                elif countone < self.count(self.dealer):
                    print('\nHand 1 loses!')
                    self.hand_winner(self.dealer, player, self.stake)

                if 21 >= counttwo >= self.count(self.dealer):
                    if counttwo == self.count(self.dealer):
                        print('\nHand 2 Ties!')
                        self.hand_winner(player, self.dealer, 0)
                    else:
                        print('\nHand 2 wins!')
                        self.hand_winner(player, self.dealer, self.stake)
                elif counttwo < self.count(self.dealer):
                    print('\nHand 2 loses!')
                    self.hand_winner(self.dealer, player, self.stake)
        return

    def BlackJack(self, player):
        if self.count(player) == 21:
            return True
        else:
            return False

    def checkbust(self, player):
        if self.count(player) < 21:
            return False
        elif self.count(player) > 21:
            if player.ishuman is False:
                print('~DEALER BUST!~')
            elif player.ishuman is True:
                print('~PLAYER BUST!~')
            return True

    def selectedhit(self, player):
        while not self.checkbust(player) and not self.BlackJack(player):
            try:

                self.player.show_hand()
                move = int(input(" | Stand (1) | Hit (2): "))
                if isinstance(move, int) and 0 < move <= 2:
                    if move == 1:
                        self.player.show_hand()
                        print('\n')
                        break
                    elif move == 2:
                        player.hit(self.deck.deckpop())

                else:
                    print("Invalid choice")

            except ValueError:
                print("Please enter a valid move")

        if self.BlackJack(player):
            print("--BlackJack!--")
            self.hand_winner(player, self.dealer, self.stake*1.5)
            return

        elif self.count(player) > 21:
            self.hand_winner(self.dealer, player, self.stake)
            return

    def newround(self):
        self.player.hand = []
        self.dealer.hand = []
        print(
            "------------------Feeling Lucky? Test your luck against the dealer!---------------------- ")  # move later
        print(f'Your HP: {self.player.HP}  Dealer HP: {self.dealer.HP}')  # move to newround

        while self.player.HP > 0 and self.dealer.HP > 0:
            # ask player for stakes
            try:

                dealerturn = 0  # keeps track of how many turns dealer has had
                if self.player.HP <= 0 or self.dealer.HP <= 0:
                    break
                stake = int(input("\nEnter your stake for this round (min. 5): "))
                if not isinstance(stake, int) or stake < 5 or stake > self.player.HP:
                    print('Invalid stake')
                else:
                    self.stake = stake
                    self.player.hit(self.deck.deckpop())
                    # first dealer card is face down
                    self.dealer.hit(self.deck.deckpop(facedown=True))

                    self.player.hit(self.deck.deckpop())
                    self.dealer.hit(self.deck.deckpop(facedown=True))
                    self.dealer.dealer_show(dealerturn)
                    self.player.show_hand()
                    if not self.BlackJack(self.player):
                        try:
                                move = int(input("\nStand (1) | Hit (2) | DoubleDown(3) | Split (4) | Surrender (5): "))

                                if move == 1:

                                    dealerturn += 1
                                    self.dealermove(dealerturn)
                                    self.compare(self.player, self.dealer)

                                elif move == 2:
                                    self.player.hit(self.deck.deckpop())
                                    self.selectedhit(self.player)
                                    if not self.BlackJack(self.player) and self.count(self.player) < 21:
                                        dealerturn += 1
                                        print('\033[36mVS.\033[0m\n')
                                        self.dealermove(dealerturn)
                                        self.compare(self.player, self.dealer)

                                elif move == 3:
                                    self.stake *= 2
                                    print(f"Your new bet for this round is: {self.stake}")
                                    self.player.hit(self.deck.deckpop())
                                    self.player.show_hand()
                                    print('\n')
                                    if self.checkbust(self.player):
                                        self.hand_winner(self.dealer, self.player, self.stake)
                                    elif self.BlackJack(self.player):
                                        self.hand_winner(self.player, self.dealer, self.stake)
                                    else:
                                        dealerturn += 1
                                        self.dealermove(dealerturn)
                                        self.compare(self.player, self.dealer)

                                elif move == 4:
                                    if self.player.hand[0].value != self.player.hand[1].value:
                                        print('Ineligible to split!')
                                    else:
                                        print(f"Your new bet for this round is: {self.stake*2}")
                                        one, two = self.player.split()
                                        self.splithit(self.player, one, two)

                                elif move == 5:
                                    self.surrender()

                                else:
                                    print("Please enter a valid number")
                                # ask to restart the game if dealer or player HP is 0
                                if self.player.HP <= 0 or self.dealer.HP <= 0:
                                    print(self.game_winner())
                                    restart = str(input('New game? (Y/N): '))
                                    if not isinstance(restart, str) or len(restart) > 1:
                                        print(self.game_over())
                                    elif ord(restart) == ord('y') or ord(restart) == ord('Y'):
                                        self.player.HP = 100
                                        self.dealer.HP = 100
                                        self.newround()
                                    else:
                                        print(self.game_over())
                                        self.player.HP = 0
                                        self.dealer.HP = 0
                                        break

                                else:
                                    self.newround()
                        except ValueError:
                            print("Please enter an integer")
                            continue

                    elif self.BlackJack(self.player):
                        print("\n\033[45m---PLAYER BLACKJACK!---\033[0m")
                        self.hand_winner(self.player, self.dealer, self.stake * 2)
                        self.newround()
            except ValueError:
                print("Please enter a valid stake (wager)")
                continue



new_game = Game()
new_game.newround()
