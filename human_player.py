import random
from cards import cards


class human_player:

    def __init__(self, name):
        games = ["tricks", "diamonds", "queens", "king", "jack"]
        #games = ['tricks']
        self.name = name
        self.score = 0
        self.hand = []
        self.games = games
        self.game = ' '
        self.score = 0
        self.subscore = 0
        self.suits = ['spade', 'heart', 'club', 'diamond']
        self.finished = False


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

    def getKey(self,item):
        card_obj = cards()
        return card_obj.get_rank(item[1])

    def receive_cards(self,cards):
        self.hand.clear()
        self.hand = cards

        sorted_hand = []
        hearts = []
        diamonds = []
        clubs = []
        for i in self.hand:
            if i[0] == 'heart':
                hearts.append(i)
            elif i[0] == 'diamond':
                diamonds.append(i)
            elif i[0] == 'club':
                clubs.append(i)
            else:
                sorted_hand.append(i)
        sorted_hand = sorted(sorted_hand, key=self.getKey)
        sorted_hand += sorted(hearts, key=self.getKey)
        sorted_hand += sorted(clubs, key=self.getKey)
        sorted_hand += sorted(diamonds, key=self.getKey)

        self.hand = sorted_hand.copy()

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
        self.game = game

    def played_card(self, card):
        if card in self.hand:
            self.hand.remove(card)

        return card

    def allowed_cards_jack(self, jack, hand):

        playing = True
        # print('hand: ',hand)
        # print('jack: ',jack)
        card_obj = cards()
        allowed_up = []
        allowed_down = []

        for i in range(len(jack[1])):
            # print('type down : ', type(jack[1][i]))
            if type(jack[1][i]) != tuple:
                rank_allowed = 10
            else:
                rank_allowed = card_obj.get_rank(jack[1][i][1]) - 1
            # print('rank allowed: ',rank_allowed,'   card: ',(jack[1][i][0],card_obj.get_rank_name(rank_allowed)))
            if rank_allowed != 0 and (self.suits[i], card_obj.get_rank_name(rank_allowed)) in hand:
                allowed_down.append((self.suits[i], card_obj.get_rank_name(rank_allowed)))
            # print('base rank: ',rank_allowed)

            # print('type up : ', type(jack[0][i]))
            if type(jack[0][i]) != tuple:
                if rank_allowed == 10:
                    rank_allowed = -1
                else:
                    rank_allowed = 11
            else:
                rank_allowed = card_obj.get_rank(jack[0][i][1]) + 1

            if rank_allowed != 14 and rank_allowed != -1 and (
            self.suits[i], card_obj.get_rank_name(rank_allowed)) in hand:
                # print('check me:',card_obj.get_rank_name(rank_allowed))
                # print('allowed rank: ',rank_allowed)
                allowed_up.append((self.suits[i], card_obj.get_rank_name(rank_allowed)))

        if len(allowed_down) == 0 and len(allowed_up) == 0:
            playing = False
        #print('allowed up: ', allowed_up)
        #print('allowed down: ', allowed_down)
        #print('playing: ', playing)

        return allowed_up, allowed_down, playing






    def play(self,cards_played, play_order):

            #print('your cards: ', self.hand)
            if len(cards_played) >0:
                allowed = self.allowed_cards(cards_played[0][1][0])
                print('      your hand     ', '        allowed cards ')
                for i in range(len(self.hand)):
                    if i < len(allowed) and len(allowed)<len(self.hand):
                        print(i + 1, ': ', self.hand[i], '   ', i + 1, ': ', allowed[i])
                    else:
                        print(i + 1, ': ', self.hand[i])
                index_card = 14
                while int(index_card)>len(allowed):
                    index_card = input('enter the number of the card you want to play (e.g 1): ')
                    if (not index_card.isnumeric()) or int(index_card)>len(allowed):
                        print('enter a valid number')
                        index_card = 14
                card = allowed[int(index_card)-1]

                return self.played_card(card)
            else :

                for i in range(len(self.hand)):
                    print(i + 1, ': ', self.hand[i])
                #allowed = self.allowed_cards(cards_played[1][0])
                #print(allowed)
                index_card = 14
                while int(index_card) > len(self.hand) :
                    index_card = input('enter the number of the card you want to play (e.g 1): ')
                    if (not index_card.isnumeric()) or int(index_card) > len(self.hand):
                        print('enter a valid number')
                        index_card = 14
                return self.hand.pop(int(index_card) - 1)


    def play_jack3(self,cards_played, play_order,score_of_winner):

            #print('your cards: ', self.hand)
            if len(cards_played) >0:
                allowed = self.allowed_cards(cards_played[0][1][0])
                print('      your hand     ', '        allowed cards ')
                for i in range(len(self.hand)):
                    if i < len(allowed) and len(allowed)<len(self.hand):
                        print(i + 1, ': ', self.hand[i], '   ', i + 1, ': ', allowed[i])
                    else:
                        print(i + 1, ': ', self.hand[i])
                index_card = input('enter the number of the card you want to play (e.g 1): ')
                card = allowed[int(index_card)-1]

                return self.played_card(card)
            else :

                for i in range(len(self.hand)):
                    print(i + 1, ': ', self.hand[i])
                #allowed = self.allowed_cards(cards_played[1][0])
                #print(allowed)
                card = input('enter the number of the card you want to play (e.g 1): ')
                return self.hand.pop(int(card) - 1)

    def play_jack(self, jack, play_order, score_of_winner):
        just_finished = False
        if self.hand == 0:
            return just_finished, 'finished'

        self.players_order = play_order
        # print(self.name,'cards: ',self.hand,'  hearts left: ',self.hearts_left)
        # print('number of my cards: ', len(self.hand))

            # print('your cards: ', self.hand)

            # allowed_suit = cards_played[0][1][0]
        allowed_up, allowed_down, playing = self.allowed_cards_jack(jack, self.hand)
        allowed = allowed_up+allowed_down
        print('allowed: ',allowed, '   up: ',allowed_up,'      down: ',allowed_down)
        print('      your hand     ', '        allowed cards ')

        if playing:
            for i in range(len(self.hand)):
                if i < len(allowed) and len(allowed) <= len(self.hand):
                    print(i + 1, ': ', self.hand[i], '   ', i + 1, ': ', allowed[i])
                else:
                    print(i + 1, ': ', self.hand[i])
            index_card = input('enter the number of the card you want to play (e.g 1): ')
            card = allowed[int(index_card) - 1]
                # print('^^^^^^^^^^^^^^^^^^^^ AI options ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            '''
            for i in range(len(allowed_up) + len(allowed_down)):
                if i < len(allowed_up):
                    print(i + 1, ': ', allowed_up[i])
                    a = 9
                else:
                    print(i + 1, ': ', allowed_down[i - len(allowed_up)])
                    a = 8
            '''

        else:
            card = 'pass'
            for i in range(len(self.hand)):
                print(i + 1, ': ', self.hand[i])
            input('you do not have a valid card to play, press enter to proceed: ')
            # print('trained card: ', card)
        self.played_card(card)
        if len(self.hand) == 0 and not self.finished:
            self.update_score(score_of_winner,'jack')
            self.finished = True
            just_finished = True
        return just_finished, card





    def contains_king(self,cards_played):
        for i in cards_played:
            if i[1][1] == 'k' and i[1][0]=='heart':
                return True
        return False

    def get_subscore(self):
        return self.subscore

    def get_score(self):
        self.subscore = 0
        return self.score

    def update_score(self,trick,game):
        print('game to update: ',game)
        trick_score = 0
        if game == 'tricks':
            self.subscore -= 15
            self.score -= 15
        elif game == 'diamonds':
            for i in trick:
                if i[1][0] == 'diamond':
                    trick_score += 10
            self.subscore -= trick_score
            self.score -= trick_score
        elif game == 'queens':
            for i in trick:
                if i[1][1] == 'q':
                    trick_score += 25
            self.subscore -= trick_score
            self.score -= trick_score
        elif game == 'king':
            if self.contains_king(trick):
                self.subscore -= 75
                self.score -= 75



