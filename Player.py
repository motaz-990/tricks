from cards import cards
import copy
import random
from player_tricks import player_tricks
class Player:

    def __init__(self, name,human):
        games = ["tricks", "diamonds", "queens", "king", "jack"]
        #games = ['tricks']
        self.name = name
        self.score = 0
        self.subscore = 0
        self.hand = []
        self.games = games
        self.game = ' '
        self.human = human

        self.game_player = 0
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
            if i == ('heart','7'):
                return True

        return False
    def receive_cards(self,cards):
        self.hand.clear()
        while len(cards)>0 and len(self.hand)<13:
            self.hand.append(cards.pop())

    def choose_game(self):

        if self.human:
            for i in range (len(self.games)):
                print(i+1,': ',self.games[i])
            game = input('enter the number of the game you would like to play: ')
            self.set_game(self.games.pop(int(game)-1))
            return self.game
        else:
            self.set_game(self.games.pop())
            return self.game

    def set_game(self, game):
        #print('set game: ',game)
        #print('original hand: ',self.name,' ',self.hand)
        self.game = game
        if True or self.game == 'tricks':
            #print('check ')
            #print(self.game_player.hand)
            self.game_player = player_tricks(self.name, self.human)

            #print(self.game_player.hand)
        self.game_player.receive_cards(self.hand)

    def played_card(self, card):
        for i in range (len(self.hand)) :
            if card == self.hand[i] :
                return self.hand.pop(i)


    def get_score(self):
        print(self.name,' check score: ',self.score)
        self.score += self.game_player.get_score()
        print(self.name,' check score: ',self.score)

        return self.score

    def get_subscore(self):
        return self.game_player.get_subscore()


    def play(self,cards_played,play_order):
        if True or self.game == 'tricks':
            #print(self.name,' playing with ',self.hand)
            card = self.game_player.play(cards_played, play_order)
            self.played_card(card)
            #print('finished playing')
            return card





    def update_score(self):

        self.game_player.update_score()
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

