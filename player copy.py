from cards import cards
import copy
import random
from player_tricks import player_tricks


class Player:

    def __init__(self, name, human):
        games = ["tricks", "diamonds", "queens", "king", "jack"]
        # games = ['tricks']
        self.name = name
        self.score = 0
        self.subscore = 0
        self.hand = []
        self.games = games
        self.game = ' '
        self.human = human
        self.tricks_player = player_tricks(name, human)
        self.diamonds_player = 0
        self.queens_player = 0
        self.king_player = 0
        self.jack_player = 0

    def allowed_cards(self, suit):
        allowed = []
        for card in self.hand:
            if suit == card[0]:
                allowed.append(card)
        if len(allowed) == 0:
            allowed = self.hand

        return allowed

    def has_seven_hearts(self):
        for i in self.hand:
            if i == ('heart', '7'):
                return True

        return False

    def receive_cards(self, cards):
        self.hand.clear()
        while len(cards) > 0 and len(self.hand) < 13:
            self.hand.append(cards.pop())

    def choose_game(self):

        if self.human:
            for i in range(len(self.games)):
                print(i + 1, ': ', self.games[i])
            game = input('enter the number of the game you would like to play: ')
            self.set_game(self.games.pop(int(game) - 1))
            return self.game
        else:
            self.set_game(self.games.pop())
            return self.game

    def set_game(self, game):
        # print('set game: ',game)
        # print('original hand: ',self.name,' ',self.hand)
        self.game = game
        if True or self.game == 'tricks':
            # print('check ')
            # print(self.tricks_player.hand)
            self.tricks_player.receive_cards(self.hand)
            print(self.tricks_player.hand)

    def played_card(self, card):
        for i in range(len(self.hand)):
            if card == self.hand[i]:
                return self.hand.pop(i)

    def get_score(self):
        self.subscore = 0
        return self.score

    def get_subscore(self):
        return self.subscore

    def play(self, cards_played):
        if self.human:
            # print('your cards: ', self.hand)
            if len(cards_played) > 0:
                print('------------------------')

                allowed = self.allowed_cards(cards_played[0][1][0])
                for i in range(len(allowed)):
                    print(i + 1, ': ', allowed[i])
                index_card = input('enter the number of the card you want to play (e.g 1): ')
                card = allowed[int(index_card) - 1]

                return self.played_card(card)


            else:

                for i in range(len(self.hand)):
                    print(i + 1, ': ', self.hand[i])
                # allowed = self.allowed_cards(cards_played[1][0])
                # print(allowed)
                card = input('enter the number of the card you want to play (e.g 1): ')
                return self.hand.pop(int(card) - 1)
        else:
            if len(cards_played) > 0:

                return self.played_card(self.allowed_cards(cards_played[0][1][0])[0])
            else:

                return self.hand.pop()

    def update_score(self, trick):

        self.subscore -= 15
        self.score -= 15
        '''
        if self.game == 'tricks':
            self.subscore -= 15
            self.score -= 15

        elif self.game == 'diamond':
            self.subscore -= 15
            self.score -= 15

        elif self.game == 'king of hearts':
            self.subscore -= 15
            self.score -= 15

        elif self.game == 'queens':
            self.subscore -= 15
            self.score -= 15

        elif self.game == 'jack':
            self.subscore -= 15
            self.score -= 15
        '''


def diamond_play(self):
    pass


def tricks_play(self):
    pass


def king_play(self):
    pass


def queen_play(self):
    pass


def jack_play(self):
    pass


if True or self.game == 'tricks':
    self.tricks_player.play(cards_played, play_order)