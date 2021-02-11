from cards import cards
import random


class trained_player_tricks:

    def __init__(self, name, trained):
        #games = ["tricks", "diamonds", "queens", "king", "jack"]
        games = ['tricks']
        self.name = name
        self.score = 0
        self.subscore = 0
        self.hand = []
        self.games = games
        self.game = 'tricks'
        self.trained = trained
        #states: 1:'first_player',2:['second_same','second_different'],3:['third_same','third_different'],4:['fourth_same','fourth_different']
        self.state_space = {1:0,2:[1,2],3:[3,4],4:[5,6]}
        self.state_space_length = 7
        #actions: 'low_card', 'high_card'
        self.action_space =['low_card','mid_card' ,'high_card']
        self.Q_table= self.create_Q_table()
        self.random_action = 90
        self.alpha = 0
        self.discount =0


    def allowed_cards(self, suit):
        allowed = []
        match = True
        for card in self.hand:
            if suit == card[0]:
                allowed.append(card)
        if len(allowed) == 0:
            match = False
            allowed = self.hand

        return allowed,match

    def receive_cards(self, cards):
        self.hand.clear()
        while len(cards) > 0 and len(self.hand) < 13:
            self.hand.append(cards.pop())
    '''
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
        self.game = game
    '''
    def played_card(self, card):
        for i in range(len(self.hand)):
            if card == self.hand[i]:
                return self.hand.pop(i)

#need some adjustments
    def get_score(self):
        self.subscore = 0
        return self.score

    # need some adjustments
    def get_subscore(self):
        return self.subscore

    # need some adjustments
    def play(self, cards_played):
        if self.trained:
            # print('your cards: ', self.hand)
            if len(cards_played) > 0:
                print('------------------------')
                allowed_suit = cards_played[0][1][0]
                allowed ,match = self.allowed_cards(allowed_suit)
                print('^^^^^^^^^^^^^^^^^^^^ AI options ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                for i in range(len(allowed)):
                    print(i + 1, ': ', allowed[i])
                print('^^^^^^^^^^^^^^^^^^^^ AI decision ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')

                card = self.Q_table_decision(cards_played,allowed,match)
                print('trained card: ',card)
                return self.played_card(card)


            else:
                print('^^^^^^^^^^^^^^^^^^^^ AI options ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                for i in range(len(self.hand)):
                    print(i + 1, ': ', self.hand[i])
                print('^^^^^^^^^^^^^^^^^^^^ AI decision ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                # allowed = self.allowed_cards(cards_played[1][0])
                # print(allowed)
                card = self.Q_table_decision(cards_played,self.hand,True)
                print('trained card: ', card)
                return self.played_card(card)
        else:
            if len(cards_played) > 0:
                return self.played_card(self.allowed_cards(cards_played[0][1][0])[0][0])
            else:
                return self.hand.pop()

    # need some adjustments
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


    def create_Q_table(self):

        table = []
        for i in range((self.state_space_length)) :
            state = []
            for j in range(len(self.action_space)):
                state.append(0)
            table.append(state)
        return table

    def min_card(self, allowed_cards,first,max):
        card_obj = cards()

        if first:
            max = 5
        print(max)
        card = allowed_cards[0]
        min_rank = card_obj.get_rank(card[1])
        found_lower_than_max = min_rank<max
        for i in range(1,len(allowed_cards)):
            if not found_lower_than_max:
                if card_obj.get_rank(allowed_cards[i][1]) < min_rank:
                    card = allowed_cards[i]
                    min_rank = card_obj.get_rank(allowed_cards[i][1])
                    found_lower_than_max = min_rank<max
            elif card_obj.get_rank(allowed_cards[i][1]) > min_rank and card_obj.get_rank(allowed_cards[i][1])<max:
                card = allowed_cards[i]
                min_rank = card_obj.get_rank(allowed_cards[i][1])

        return card


    def max_card(self, allowed_cards):
        card_obj = cards()
        card = allowed_cards[0]
        max_rank = card_obj.get_rank(card[1])
        for i in range(1, len(allowed_cards)):
            if card_obj.get_rank(allowed_cards[i][1]) > max_rank:
                    card = allowed_cards[i]
                    max_rank = card_obj.get_rank(allowed_cards[i][1])
        return card

    def mid_card(self,allowed_cards,first,min):

        card_obj = cards()
        if first:
            min = 6
        print(min)
        card = allowed_cards[0]
        mid_rank = card_obj.get_rank(card[1])
        print('mid rank: ',mid_rank)
        found_good_rank = min < mid_rank
        for i in range(1, len(allowed_cards)):
            if not found_good_rank:
                if card_obj.get_rank(allowed_cards[i][1]) > mid_rank:
                    card = allowed_cards[i]
                    mid_rank = card_obj.get_rank(allowed_cards[i][1])
                    found_good_rank = min < mid_rank
            elif card_obj.get_rank(allowed_cards[i][1]) < mid_rank and card_obj.get_rank(allowed_cards[i][1]) > min:
                print('elif',i)
                card = allowed_cards[i]
                mid_rank = card_obj.get_rank(allowed_cards[i][1])

        return card


    def highest_card_played(self,cards_played):
        new_cards = cards()
        suit, rank = cards_played[0][1][0], new_cards.get_rank(cards_played[0][1][1])
        for i in range(1, len(cards_played)):
            if cards_played[i][1][0] == suit and new_cards.get_rank(cards_played[i][1][1]) > rank:
                rank = new_cards.get_rank(cards_played[i][1][1])
        return rank



    def perform_action (self,cards_played,allowed_cards,action):
        if action == 0:
            if len(cards_played) == 0:
                return self.min_card(allowed_cards,True,0)
            return self.min_card(allowed_cards, False, self.highest_card_played(cards_played))
        elif action == 1:
            if len(cards_played) == 0:
                return self.mid_card(allowed_cards, True, 0)
            return self.min_card(allowed_cards,False,self.highest_card_played(cards_played))
        else :
            return self.max_card(allowed_cards)


    def current_state (self, cards_played,match):
        index = 0
        if not match :
            index = 1

        if len(cards_played) == 0:
            return self.state_space.get(1)

        return self.state_space.get(len(cards_played)+1)[index]


    def update_Q_table(self, card,match):
        pass

    def Q_table_decision(self,cards_played, allowed_cards,match):
        state = self.Q_table[self.current_state(cards_played,match)]
        if(random.random()<self.random_action):
            action = random.randrange(3)
            card = self.perform_action(cards_played,allowed_cards,action)
            self.update_Q_table(card,match)
            self.random_action -=0.1
            print(action)
            return card
        else:
            #choose the max reward
            action = state.index(max(state))
            card = self.perform_action(cards_played,allowed_cards,action)
            self.update_Q_table(card)
            print(action)
            return card


