from cards import cards
import copy
import random
from player_tricks import player_tricks
from human_player import human_player
from player_diamonds import player_diamonds
from player_queens import player_queens
from player_king import player_king
from player_jack import player_jack

class Player:

    def __init__(self, name,human):

        #games = ['tricks']
        self.name = name
        self.score = 0
        self.subscore = 0
        self.hand = []
        self.games = ["tricks", "diamonds", "queens", "king", "jack"]
        self.game = ' '
        self.human = human

        self.game_player = 0


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
            game = self.games[int(game)-1]
            self.games.remove(game)
            self.game = game
            return game
        else:
            game = self.games[random.randrange(len(self.games))]
            self.games.remove(game)
            self.game = game
            return game

    def set_game(self, game):
        #print('set game: ',game)
        #print('original hand: ',self.name,' ',self.hand)
        self.game = game
        if self.human:
            self.game_player = human_player(self.name)
        else:
            if self.game == 'tricks':
                self.game_player = player_tricks(self.name, not self.human)

            elif self.game == 'diamonds':
                self.game_player = player_diamonds(self.name, not self.human)

            elif self.game == 'queens':
                self.game_player = player_queens(self.name, not self.human)

            elif self.game == 'king':
                self.game_player = player_king(self.name, not self.human)
            else:
                self.game_player = player_jack(self.name, not self.human)


        self.game_player.receive_cards(self.hand)
        #print('sorted hand: ', self.game_player.hand)

    def cards_played(self, cards, index_my_card):
        self.game_player.cards_played(cards, index_my_card)

    def my_turn(self, play_order):
        for i in range(len(play_order)):
            if play_order[i] == self.name:
                return i

    def contains_king(self, cards_played):
        return self.game_player.contains_king(cards_played)

    def played_card(self, card):
        for i in range (len(self.hand)) :
            if card == self.hand[i] :
                return self.hand.pop(i)


    def get_score(self):
        #print(self.name,' check score: ',self.score)
        self.score += self.game_player.get_score()
        #print(self.name,' check score: ',self.score)

        return self.score

    def get_subscore(self):
        return self.game_player.get_subscore()


    def play(self,cards_played,play_order,score_of_winner):
            print('^^^^^^^^^^^^ ',self.name,' turn ^^^^^^^^^^^^^^^')
            if self.game == 'jack':
                #print(self.name, 'jack playing with ', len(self.hand), ' ', self.hand)
                just_finished, card = self.game_player.play_jack(cards_played, play_order, score_of_winner)
                self.played_card(card)
                #print('finished playing')
                return just_finished,card
            else:
                #print(self.name,' ', self.game,' playing with ',len(self.hand),' ',self.hand)
                card = self.game_player.play(cards_played, play_order)
                self.played_card(card)
                #print('finished playing')
                return card







    def update_score(self,trick):
        print(self.name)
        self.game_player.update_score(trick,self.game)
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

