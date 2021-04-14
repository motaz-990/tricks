from cards import cards
import copy
import random


class trained_player_tricks:

    def __init__(self, name, trained):
        #games = ["tricks", "diamonds", "queens", "king", "jack"]
        games = ['tricks']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'A']
        self.suits = ['spade', 'heart', 'club', 'diamond']
        self.diamonds_left= []
        self.clubs_left = []
        self.hearts_left = []
        self.spade_left = []
        self.cards_left = []
        self.ai1_cards = []
        self.ai2_cards =[]
        self.ai3_cards = []
        self.suits_left_list =[self.spade_left,self.hearts_left,self.clubs_left,self.diamonds_left]
        self.players_cards = []
        self.players_cards_expected = []
        self.name = name
        self.players = [self.name, 'ai1', 'ai2', 'ai3']
        self.players_order = self.players.copy()
        self.score = 0
        self.subscore = 0
        self.hand = []
        self.games = games
        self.game = 'tricks'
        self.trained = trained
        #states: 1:'first_player',2:['second_same','second_different'],3:['third_same','third_different'],4:['fourth_same','fourth_different']
        #self.state_space = {1:0,2:{True:1,False:2},3:{True:3,False:4},4:{True:5,False:6}}
        #{0: {True: 'first low strong', False: 'first low weak'}, 1: {True: 'first mid strong', False: 'first mid weak'},
         #2: {True: 'first high strong', False: 'first high weak'}},

        self.state_space = {1:{0:'first end',1:'first mid',2:'first start'},
                            2: {True:{True:'second yes majority less',False:'second yes majority high'}, False: 'second no'},
                            3: {True:{True:'third yes majority less',False:'third yes majority high'}, False: 'third no'},
                            4: {True:{True:'fourth yes majority less',False:'fourth yes majority high'}, False: 'fourth no'}}
        self.states_list = {'first start':0,'first mid':1,'first end':2,'second yes majority less':3,'second yes majority high':4,
                            'second no':5,'third yes majority less':6,'third yes majority high':7,'third no':8,
                            'fourth yes majority less':9,'fourth yes majority high':10,'fourth no':11}
        self.state_space_length = 12
        #actions: 'low_card', 'mid_card','high_card'
        self.action_space =['low_card','mid_card' ,'high_card']
        self.action_space_first = ['first few strong low_card','first few strong mid_card','first few strong high_card',
                                   'first few weak low_card','first few weak mid_card','first few weak high_card',
                                   'first mid strong low_card','first mid strong mid_card','first mid strong high_card',
                                   'first mid weak low_card','first mid weak mid_card','first mid weak high_card',
                                   'first lot strong low_card','first lot strong mid_card','first lot strong high_card',
                                   'first lot weak low_card','first lot weak mid_card','first lot weak high_card']
        if self.name == 'Motaz':
            self.Q_table= self.create_Q_table()
        self.random_action = 90
        self.alpha = 0
        self.discount =0

    def cards_played(self,cards,index_my_card):
        cards_to_be_removed = self.extract_cards(cards,index_my_card)
        self.remove_cards(cards_to_be_removed)


    def cards_playedd(self,cards,future,index_my_card):
        #print('players cards: ',self.players_cards)
        #print('helllllllo')
        if not future:
            #print('indexxxxxxxxx: ',index_my_card)
            cards = self.extract_cards(cards, index_my_card)
        #print('cards to be removed: ', cards)
        for i in range(len(cards)):
            #print('card: ',cards[i])
            if cards[i][0]== 'heart' and not future:
                #print(self.name,' hearts left: ',self.hearts_left)
                self.hearts_left.remove(cards[i])

            elif cards[i][0]== 'diamond'and not future:
                #print(self.name,' diamond left: ', self.diamonds_left)
                self.diamonds_left.remove(cards[i])
            elif cards[i][0]== 'club'and not future:
                #print(self.name,' club left: ', self.clubs_left)
                self.clubs_left.remove(cards[i])
            elif not future:
                #print(self.name,' spade left: ', self.spade_left)
                self.spade_left.remove(cards[i])
            if not future:
                self.cards_left.remove(cards[i])
                self.ai1_cards.remove(cards[i])
                self.ai2_cards.remove(cards[i])
                self.ai3_cards.remove(cards[i])
                for j in range(len(self.players_cards)):
                    #print('players cards before: ', self.players_cards[j])
                    self.players_cards[j].remove(cards[i])
                    #print('players cards: ', self.players_cards[j])

                # print('players cards after: ', self.players_cards)


            for j in range(len(self.players_cards)):
                if j == index_my_card:
                    break
                else:
                    if not future:
                        break
                    elif cards[i][0] == self.name:
                        break
                    elif type(cards[i])==str:
                        if i==0:
                            #print('to be removed: ',cards)
                            self.players_cards[j].remove(cards)

                    else:
                        #print('to be removed: ',cards[i][1])
                        #print('players cards: ', self.players_cards)

                        self.players_cards[j].remove(cards[i][1])
        #if not future:
            #print('players cards: ', self.players_cards)

            #print('index: ', index_my_card)
            #print('my hand: ', self.hand)
            #print('ai cards: ', self.ai1_cards)
            #print('hearts cards: ', self.hearts_left)


    def extract_cards(self,cards,index_my_card):
        returned_card = []
        for i in range(len(cards)):
            if not i == index_my_card:
                returned_card.append(cards[i][1])
        return returned_card


    def make_copy(self,temp):
        #self.cards_left = temp.copy()
        #print('######################### make copy ##########################')
        #print('temp: ', temp)
        if type(temp[0])==list:
            temp = []
        #print('temp: ', temp)
        #print(len(self.players_cards),' players cards: ',self.players_cards)

        for i in range(len(self.players_cards)):

            self.players_cards[i] = temp.copy()
        #print(len(self.players_cards), ' players cards: ', self.players_cards)
        return temp.copy()

    def reset_players_cards(self):
        self.players_cards=[]
        self.players_cards.append(self.ai1_cards.copy())
        self.players_cards.append(self.ai2_cards.copy())
        self.players_cards.append(self.ai3_cards.copy())
        self.players_cards_expected = copy.deepcopy(self.players_cards)



    def remove_cards(self,cards):

        #print('cards:      ', cards)
        #print('suits:      ',self.suits_left)
        for i in cards:
            self.players_cards[0].remove(i)
            self.players_cards[1].remove(i)
            self.players_cards[2].remove(i)
            if i in self.players_cards_expected[0]:
                self.players_cards_expected[0].remove(i)
            if i in self.players_cards_expected[1]:
                self.players_cards_expected[1].remove(i)
            if i in self.players_cards_expected[2]:
                self.players_cards_expected[2].remove(i)
            #print('index: ',self.suits.index(i[0]))
            self.suits_left_list[self.suits.index(i[0])].remove(i)

        #print('suits after: ',self.suits_left)
        #print('players cards:    ',self.players_cards[0])
        #checked


    def reset_cards_left(self):
        self.cards_left.clear()
        for i in range(4):
            for j in range(13):
                if i == 0:
                    self.cards_left.append((self.suits[i], self.ranks[j]))
                    self.spade_left.append((self.suits[i], self.ranks[j]))
                if i == 1:
                    self.cards_left.append((self.suits[i], self.ranks[j]))
                    self.hearts_left.append((self.suits[i], self.ranks[j]))
                if i == 2:
                    self.cards_left.append((self.suits[i], self.ranks[j]))
                    self.clubs_left.append((self.suits[i], self.ranks[j]))
                if i == 3:
                    self.cards_left.append((self.suits[i], self.ranks[j]))
                    self.diamonds_left.append((self.suits[i], self.ranks[j]))

        self.players_cards.clear()
        self.players_cards_expected.clear()

        self.ai1_cards = self.cards_left.copy()
        self.players_cards.append(self.ai1_cards)
        self.ai2_cards = self.cards_left.copy()
        self.players_cards.append(self.ai2_cards)
        self.ai3_cards = self.cards_left.copy()
        self.players_cards.append(self.ai3_cards)
        self.players_cards_expected = copy.deepcopy(self.players_cards)

        self.remove_cards(self.hand)
        #checked

    def getKey(self,item):
        card_obj = cards()
        return card_obj.get_rank(item[1])



    def allowed_cards(self, suit,hand):
        allowed = []
        match = True
        for card in hand:
            if suit == card[0]:
                allowed.append(card)
        if len(allowed) == 0:
            match = False
            allowed = hand

        return allowed,match

    def receive_cards(self, cards):
        self.hand.clear()

        while len(cards) > 0 and len(self.hand) < 13:
            self.hand.append(cards.pop())

        sorted_hand = []
        hearts = []
        diamonds = []
        clubs = []
        for i in self.hand:
            if i[0]== 'heart':
                hearts.append(i)
            elif i[0]== 'diamond':
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
        #print('sorted hand: ',self.hand)




        print(self.name,'cards: ',self.hand)
        #print(len(cards), ' cards: ', cards)
        self.reset_cards_left()
        #checked


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
    def play(self, cards_played,play_order):
        self.players_order = play_order
        #print(self.name,'cards: ',self.hand,'  hearts left: ',self.hearts_left)
        if self.trained:
            # print('your cards: ', self.hand)
            if len(cards_played) > 0:
                print('------------------------')
                allowed_suit = cards_played[0][1][0]
                allowed ,match = self.allowed_cards(allowed_suit,self.hand)
                print('^^^^^^^^^^^^^^^^^^^^ AI options ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                for i in range(len(allowed)):
                    print(i + 1, ': ', allowed[i])
                print('^^^^^^^^^^^^^^^^^^^^ AI decision ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')

                card = self.Q_table_decision(cards_played,allowed,match)
                print('^^^^^^^^^^^^^^^^^^^^ end q decision ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                print('trained card: ',card)
                return self.played_card(card)


            else:
                print('^^^^^^^^^^^^^^^^^^^^ AI options ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                for i in range(len(self.hand)):
                    print(i + 1, ': ', self.hand[i])
                print('^^^^^^^^^^^^^^^^^^^^ AI decision ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                # allowed = self.allowed_cards(cards_played[1][0])
                # print(allowed)
                card = self.Q_table_decision(cards_played.copy(),self.hand,True)
                print('trained card: ', card)
                return self.played_card(card)
        else:
            if len(cards_played) > 0:
                allowed_cards,match = self.allowed_cards(cards_played[0][1][0],self.hand)
                action = random.randrange(3)
                if match:
                    actions,valid = self.valid_actions(allowed_cards,self.highest_card_played(cards_played))
                    #print('actions: ',actions)
                    action = actions[random.randrange(len(actions))]
                if len(cards_played)==3 and action == 1:
                    action = 2
                card = self.perform_action(cards_played.copy(),allowed_cards,action,match)
                return self.played_card(card)
            else:
                #always plays the highest card
                action = [random.randrange(3),random.randrange(3)]
                card = self.perform_action(cards_played.copy(), self.hand, action , False)
                return self.played_card(card)

    # need some check why ai players do not play the max card when they play a different suit

    def valid_actions(self,allowed_cards,highest_card):
        #print('*************** valid actions *************')
        #print('allowed_cards: ',allowed_cards)
        #print('highest: ',highest_card)
        card_obj = cards()
        if len(allowed_cards)==1:
            return [2],False
        if highest_card > card_obj.get_rank(allowed_cards[-1][1]):
            return [2],False
        if highest_card<card_obj.get_rank(allowed_cards[0][1]):
            return [1,2],True
        return [0,1,2],True


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
            action_space = self.action_space.copy()
            if i < len(self.state_space.get(1)) :
                action_space = self.action_space_first.copy()
            for j in range(len(action_space)):
                state.append(0)
            table.append(state)
        print('Q table: ',table)
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
        #print('mid card')
        card_obj = cards()
        if first:
            min = 3
        #print(min)
        card = allowed_cards[0]
        mid_rank = card_obj.get_rank(card[1])
        found_good_rank = min < mid_rank
        for i in range(1, len(allowed_cards)):
            #print('mid: ',mid_rank,'  min: ',min,'   rank: ',card_obj.get_rank(allowed_cards[i][1]))
            if not found_good_rank:
                #print('did not find')
                if card_obj.get_rank(allowed_cards[i][1]) > mid_rank:
                    #print('if', allowed_cards[i])
                    card = allowed_cards[i]
                    mid_rank = card_obj.get_rank(allowed_cards[i][1])
                    found_good_rank = min < mid_rank
            elif card_obj.get_rank(allowed_cards[i][1]) < mid_rank and card_obj.get_rank(allowed_cards[i][1]) > min:
                #print('elif',allowed_cards[i])
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


    def remove_player_cards(self,player,highest_rank,player_rank,suit,match,base_suit,trick):

        #print('remove player cards')
        new_cards = cards()
        index_player = 0
        for i in range(len(self.players)):
            if self.players[i] == player:
                index_player = i-1
                break
        card = copy.deepcopy(self.players_cards_expected[index_player])
        for i in trick:
            if i[1] in card:
                #print('to be removed: ',i[1])
                #print('cards to remove from: ',card)
                card.remove(i[1])
                #print('cards after remove: ', card)

        print(player,' ',highest_rank,' ',player_rank,' ',suit)
        print(len(self.hand),len(card),card)
        if match:
            for i in range(highest_rank-player_rank-1):
                if (suit,new_cards.get_rank_name(player_rank+i+1)) in card:
                    card.remove((suit,new_cards.get_rank_name(player_rank+i+1)))
        else:
            for i in range(14-player_rank):
                if (suit,new_cards.get_rank_name(player_rank+i)) in card:
                    card.remove((suit,new_cards.get_rank_name(player_rank+i)))

            print(len(card), card)
            counter = 0
            for i in range(len(card)):
                #print('len: ', len(card), '  suit: ', base_suit, '  i: ', i)
                #print(card)
                if card[i-counter][0] == base_suit:
                    card.pop(i-counter)
                    counter += 1

        print(len(self.hand),len(card),card)
        return copy.deepcopy(card),index_player

    def remove_higher_cards(self,player,rank,suit):
        new_cards = cards()
        index_player = 0
        #print(player)
        for i in range(len(self.players)):
            if self.players[i] == player:
                index_player = i - 1
                break
        card = copy.deepcopy(self.players_cards_expected[index_player])
        #print(len(card),'cards before process:     ', card)
        for i in range(13-rank):
            if (suit, new_cards.get_rank_name(rank + i+1)) in card:
                card.remove((suit, new_cards.get_rank_name(rank + i+1)))
        #print(len(card),'cards after process:      ', card)
        return copy.deepcopy(card),index_player


    def analyse_trick(self,previous_trick,trick_winner):

        new_cards = cards()
        #suit, rank = previous_trick[0][1][0], new_cards.get_rank(previous_trick[0][1][1])
        suit = previous_trick[0][1][0]
        #print('winnnnnnner: ',trick_winner)
        for i in range(len(previous_trick)):
            rank = self.highest_card_played(previous_trick[:i+1])
            if not previous_trick[i][0]== 'Motaz':
                #print('analyse trick')
                #print('player: ',previous_trick[i][0], ' ',previous_trick[i][1])
                player_rank = new_cards.get_rank(previous_trick[i][1][1])
                if previous_trick[i][1][0] == suit:
                    if player_rank < rank:
                        expected,index = self.remove_player_cards(previous_trick[i][0],rank,player_rank,suit,True,suit,previous_trick)
                        self.players_cards_expected[index]= expected
                else:
                    player_suit = previous_trick[i][1][0]
                    expected,index = self.remove_player_cards(previous_trick[i][0],rank,player_rank,player_suit,False,suit,previous_trick)
                    self.players_cards_expected[index] = copy.deepcopy(expected)
            if i == len(previous_trick)-1 and previous_trick[i][0] == trick_winner and trick_winner != 'Motaz':
                print('winner: ',trick_winner,'  player: ',previous_trick[i][0])
                expected, index = self.remove_higher_cards(previous_trick[i][0], rank, suit)
                self.players_cards_expected[index] = expected



    def number_of_cards(self):
        print('ai1 cards expected: ',len(self.players_cards_expected[0]))
        print('ai2 cards expected: ',len(self.players_cards_expected[1]))
        print('ai3 cards expected: ',len(self.players_cards_expected[2]))
        if len(self.players_cards_expected[0])<len(self.hand) or len(self.players_cards_expected[1])<len(self.hand) or len(self.players_cards_expected[2])<len(self.hand):
            if 4>self.hand:
                return 4

    def count_suits(self,cards):
        #print('cards to count: ',cards)
        suits_length = []
        count_index = 0
        suit_length = 0
        counted_suit = cards[0][0]
        for i in cards:
            if i[0]==counted_suit:
                suit_length+= 1
            else:
                suits_length.append(suit_length)
                counted_suit = i[0]
                suit_length = 1
        suits_length.append(suit_length)
        #print('counted suits: ',suits_length)
        return suits_length

    def remove_min_suit(self,cards,start_index,length,suits_count):
        '''
        print('remove min')
        print('cards: ',cards)
        print('start_index: ',start_index)
        print('length: ',length)
        print('suits count: ',suits_count)
        '''
        suits_count.remove(length)
        if start_index == 0:
            #print('returned: ',cards[start_index+length:])
            return cards[start_index+length:],suits_count
        elif start_index+length == len(cards):
            #print('elif')
            #print('returned: ', cards[:start_index])
            return cards[:start_index],suits_count
        else:
            first_part = cards[:start_index]
            second_part = cards[start_index+length:]
            new_cards = first_part+second_part
            #print('returned: ', new_cards)
            #print('new cards: ',new_cards)
            return new_cards,suits_count


    def choose_suit(self,cards,action,suits_count):
        '''
        print('choose suit')
        print('cards: ', cards)
        print('actio: ', action)
        print('suits count: ', suits_count)
        '''
        if len(suits_count)== 1:
            #print('it is only one suit')
            return cards

        min_suit_length = min(suits_count)
        min_suit_index = suits_count.index(min_suit_length)
        start_index = 0

        for j in range(min_suit_index):
            start_index += suits_count[j]

        if action == 0:
            return cards[start_index:start_index + min_suit_length]
        elif action == 1:
            if len(suits_count)==2:
                return cards[start_index:start_index + min_suit_length]
            else:
                cards,suits_count = self.remove_min_suit(cards,start_index,min_suit_length,suits_count)
                return self.choose_suit(cards,action-1,suits_count)
        else:
            if len(suits_count)==2:
                if start_index == 0:
                    #print('start index: ',start_index)
                    #print('min len: ',min_suit_length)
                    #print('returned card: ',cards[start_index+min_suit_length:])
                    return cards[start_index+min_suit_length:]
                else:
                    #print('returned card: ', cards[:start_index])
                    return cards[:start_index]
            else:
                cards,suits_count = self.remove_min_suit(cards,start_index,min_suit_length,suits_count)
                return self.choose_suit(cards, action, suits_count)
        #checked

    # require an alogritm to deal with the case of only one card left in a suit and you have the rest line 585
    def perform_action_first(self,action,allowed_cards):
        #print('&&&&&&&&&&&& valid &&&&&&&&&&&&&&&&&&')
        #print('my cards: ', allowed_cards)
        #print('action: ', action)
        print(self.action_space_first[action])
        number_of_cards_action = int((action - 1) / 6)
        #print('my hand before: ', allowed_cards)
        suits_count = self.count_suits(allowed_cards)
        if suits_count == 1:
            #print('suits count: ', suits_count)
            return -1, self.perform_action([], allowed_cards, 1, True)
        if number_of_cards_action == 1 and len(suits_count) < 3:
            #print(' count: ', suits_count)
            change = 6 - 12 * random.randrange(1)
            new_action = (action - change) % len(self.action_space_first)
            return self.perform_action_first(new_action, allowed_cards)

        allowed_cards = self.choose_suit(allowed_cards, number_of_cards_action, suits_count)

        if len(allowed_cards) == 1:
            return -1, allowed_cards[0]
        #print('my hand after: ', allowed_cards)
        strong = int(action / 3) % 2 == 0
        rank = action % 3
        #print('cards action: ', number_of_cards_action, '   strong: ', strong, '   rank: ', action % 3)
        if not self.free_suit(allowed_cards[0][0]) and strong == self.evaluate_suit(allowed_cards):
            return action, self.perform_action([], allowed_cards, rank, True)
        else:
            if strong:
                action = action + 3
            else:
                action = action - 3
            return action, self.perform_action([], allowed_cards, rank, True)







        #checked might require considering the case of performing different action than desired


    def perform_action (self,cards_played,allowed_cards,action,match):
        #print('cards played: ',cards_played)
        print('allowed: ',allowed_cards)
        #print('action: ',action,'   match: ',match)
        if not match:
            suits_count = self.count_suits(allowed_cards)
            #print('allowed original: ',allowed_cards)
            if type(action)==list:
                allowed_cards = self.choose_suit(allowed_cards, action[0], suits_count)
                #print('original action: ', action[0], 'suits count: ', suits_count)
                action = action[1]
            else:
                allowed_cards = self.choose_suit(allowed_cards, action, suits_count)
                #print('original action: ',action,'suits count: ',suits_count)
                action = 2
            #print('cards played: ',cards_played)
            #print('allowed: ',allowed_cards)
            #print('action:       ',action,'   match: ',match)
        if action == 0:
            if len(cards_played) == 0:
                return self.min_card(allowed_cards,True,0)
            return self.min_card(allowed_cards, False, self.highest_card_played(cards_played))

        elif action == 1:
            if len(cards_played) == 0:
                return self.mid_card(allowed_cards, True, 0)
            #print('midddd')
            return self.mid_card(allowed_cards,False,self.highest_card_played(cards_played))
        else :

            #print('the max card: ',self.max_card(allowed_cards))
            return self.max_card(allowed_cards)
        # checked (mid need to be corrected)

    def extract_suits(self,cards):
        my_cards = {}
        suit = cards[0][0]
        my_suit = []
        for i in cards:
            if i[0] == suit:
                my_suit.append(i)
            else:
                my_cards[suit]= my_suit.copy()
                suit = i[0]
                my_suit.clear()
                my_suit.append(i)
        my_cards[suit]=my_suit.copy()

        #print('my hand: ',cards)
        #print('my suits: ',my_cards)

        return my_cards.copy()
    # checked

    def majority_less(self,highest,allowed_cards):
        #print('majority less: ',highest)
        #print('allowed cards: ',allowed_cards)

        card_obj = cards()
        for i in range(len(allowed_cards)):
            if card_obj.get_rank(allowed_cards[i][1])> highest:
                return len(allowed_cards)-i<i
            if i == 3:
                return True
        return True


    def evaluate_suit(self,my_cards):
        #print('####### evalutae ##########')
        suit = my_cards[0][0]
        number_of_my_cards = len(my_cards)
        temp = []
        limit = 0
        for i in self.players_cards_expected:
            player_suit = self.extract_suits(i).get(suit)
            #print('type of suit: ',player_suit)
            if type(player_suit)==list:
                temp.append(len(player_suit))
                if temp[-1] > 0:
                    limit+=1


        number_of_players_cards = min(temp)
        temp = [number_of_my_cards,number_of_players_cards]
        number_of_cards_to_check = min(temp)
        #print('temp: ',temp)
        #print('number: ',number_of_cards_to_check)
        #print('players cards expected: ',number_of_players_cards)
        #print('my cards: ', my_cards)

        card_obj = cards()
        strong = True

        cards_left = self.suits_left(suit)
#self.extract_suits(my_cards).get(suit)
        #print('cards to check: ',my_cards)
        #print('cards to compare: ',cards_left)
        #print('cards checke: ',number_of_cards_to_check)
        #print('limit: ',limit)
        found = False
        for i in range(number_of_cards_to_check):
            my_rank = card_obj.get_rank(my_cards[i][1])
            for j in range(limit):
                if i*limit + j < len(cards_left):
                    rank_to_compare = card_obj.get_rank(cards_left[i*limit+j][1])
                    if rank_to_compare > my_rank:
                        found = True
                        break
                else:
                    found = True
                    break
            if not found:
                strong = found
                break
        #print('strong: ',strong)


        return(my_cards[0][0],strong)

    def suits_left(self,suit):
        #print('suit: ',suit)
        #print('suits left: ',self.suits_left_list[self.suits.index(suit)])
        return self.suits_left_list[self.suits.index(suit)]

    def free_suit(self, suit):
        if len(self.suits_left(suit)) == 0:
            print('free suit')
            return True
        return False


        '''
        for i in range(len(my_cards)):
            if my_cards[i][0][0]==suit:
                if len(my_cards[i])== self.suits_left(suit):
                    return True
                else:
                    return False
'''


    def suits_evaluation(self):
        evaluation = []
        my_cards = self.extract_suits()
        for i in range(len(my_cards)):
            evaluation.append(self.evaluate_suit(my_cards[0]))

    def state_of_the_game(self,tricks_left):
        return int(tricks_left/5.25)

    def current_state (self, cards_played,allowed_cards,match):

        #print('cards played: ', cards_played)
        #print(len(allowed_cards),'allwed cards: ',allowed_cards)
        if len(cards_played) == 0:
            state_of_the_game = self.state_of_the_game(len(self.hand))
            print('state:     ',self.state_space.get(1).get(state_of_the_game))
            return self.state_space.get(1).get(state_of_the_game)
        if match:
            highest = self.highest_card_played(cards_played)
            majority_less = self.majority_less(highest, allowed_cards)
            #print('majority less: ',majority_less)
            print('state:     ', self.state_space.get(len(cards_played) + 1).get(match).get(majority_less))
            return self.state_space.get(len(cards_played) + 1).get(match).get(majority_less)

        print('state:     ', self.state_space.get(len(cards_played)+1).get(match))
        return self.state_space.get(len(cards_played)+1).get(match)
    #checked


    def update_Q_table(self,state,action,reward):
        print('state: ',state)
        print('action',action)
        print('Q table: ',self.Q_table)
        print('state before: ', self.Q_table[self.states_list.get(state)][action])
        if self.Q_table[self.states_list.get(state)][action] == 0:
            self.Q_table[self.states_list.get(state)][action] = reward
        else:
            self.Q_table[self.states_list.get(state)][action] += reward - self.Q_table[self.states_list.get(state)][action]
        print('updated state: ', self.Q_table[self.states_list.get(state)][action])


    def moves_ahead(self):
        if len(self.hand)>2:
            return 1
        return len(self.hand)

    # check if I have a choice or I am forced to play a card
    def Q_table_decision(self,cards_played, allowed_cards,match):
        update_Qtable = True
        state = self.current_state(cards_played,allowed_cards, match)
        if(random.random()<self.random_action ):
            if state[0:5] == 'first':
                action = random.randrange(len(self.action_space_first))
                #print('yes it is first: ',action)
                action,card = self.perform_action_first(action,self.hand.copy())
                if action == -1:
                    print('do not update')
                    update_Qtable = False
                self.random_action -= 0.1
                print('action: ', action)
                reward = random.randrange(15)
                if update_Qtable:
                    self.update_Q_table(state, action, reward)

                return card

            actions, update_Qtable = self.valid_actions(allowed_cards, self.highest_card_played(cards_played))
            print('actions: ', actions ,'  update: ',update_Qtable)
            action = actions[random.randrange(len(actions))]
            card = self.perform_action(cards_played, allowed_cards, action, match)
            self.random_action -= 0.1
            reward = random.randrange(15)
            #print('action: ',action)
            if update_Qtable:
                self.update_Q_table(state, action, reward)
            else:
                print('do not update')
            return card
        else:
            # choose the max reward
            action = state.index(max(state))
            card = self.perform_action(cards_played, allowed_cards, action,match)
            print('best action: ',action)
            return card


    def add_trick(self,trick, plays, card_by_card):
        tricks = []

        if not card_by_card:
            for i in plays:
                trick.append(i)
            tricks.append(trick.copy())

        else:
            for i in plays:
                trick.append(i)
                tricks.append(trick.copy())
                trick.pop(-1)

        return tricks

    def possible_moves(self,plays, trick, first_time):
        tricks = []
        temp = trick.copy()
        if type(plays[0]) == list:
            first_time = False
            for i in plays:
                tricks += self.possible_moves(i, temp.copy(), first_time)
        else:
            tricks += self.add_trick(trick.copy(), plays.copy(), first_time)

        return tricks

    def possibl_cards(self,play_order,player_index):
        for i in range(len(self.players)):
            if self.players[i] == play_order[player_index]:
                return self.players_cards[i-1]




    def minimax(self,next_turn,my_turn,suit,play_order):
        '''
        print()
        print('&&&&&&&&&&&&&&&&& parameters minimax &&&&&&&&&&&&&&&&&&&&&&&&&')
        print('next_turn : ', next_turn)
        print('my_turn: ', my_turn)
        print('suit: ', suit)
        print('play order: ', play_order)
        '''
        if next_turn == 4:
            return []

        temp = self.possibl_cards(play_order,next_turn).copy()
        cards_to_play = temp.copy()
        #print('temp: ',temp)
        possible_trick = []
        possible_tricks = []
        possible_plays = []

        if next_turn == my_turn:
            my_cards, a = self.allowed_cards(suit,self.hand.copy())
            copy_my_card = my_cards.copy()
            #print('my cards: ',my_cards)
            for i in range(len(my_cards)):
                possible_trick.append((play_order[my_turn],my_cards.pop(i)))

                #print('possible_trick', possible_trick)
                if next_turn == 0 and suit == 'free':
                    suit = cards_to_play[i][0]
                possible_plays += (self.minimax(next_turn + 1, my_turn,suit,play_order))
                #print('&&&&&&&&&&&&&&&&& end subminimax &&&&&&&&&&&&&&&&&&&&&&&&&&')

                #self.cards_left = temp.copy()
                my_cards = copy_my_card.copy()

                if len(possible_plays) == 0:
                    possible_tricks.append(possible_trick[0])
                else:
                    # print('possible plays: ',possible_plays)
                    # print('possible tricks: ',possible_tricks)
                    # print('possible trick: ', possible_trick)

                    possible_tricks += self.possible_moves(possible_plays.copy(), possible_trick.copy(), True)

                possible_trick.pop(-1)
                possible_plays.clear()
        else :
            #print('cards left minimax: ',self.cards_left)
            for i in range(len(cards_to_play)):

                possible_trick.append((play_order[next_turn],cards_to_play.pop(i)))
                #print('temp[i]: ',temp[i])
                self.cards_played(temp[i],True,-1)
                if next_turn == 0 and suit == 'free':
                    suit = temp[i][0]

                #print('suit: ', suit)
                #print('possible_trick', possible_trick)


                possible_plays += self.minimax(next_turn + 1,my_turn,suit,play_order)
                #print('&&&&&&&&&&&&&&&&& end subminimax &&&&&&&&&&&&&&&&&&&&&&&&&&')
                #print('possible plays: ',possible_plays)
                cards_to_play = self.make_copy(temp.copy())

                if len(possible_plays) == 0:
                    possible_tricks.append(possible_trick[0])
                else:
                    '''
                    print('possible plays: ',possible_plays)
                    print('possible tricks: ',possible_tricks)
                    print('possible trick: ', possible_trick)
                    print('&&&&&&&&&&&&&&&&&  posssible moves &&&&&&&&&&&&&&&&&&&&&&&&&&')
                    '''
                    possible_tricks += self.possible_moves(possible_plays.copy(), possible_trick, True)
                    #print('&&&&&&&&&&&&&&&&& end posssible moves &&&&&&&&&&&&&&&&&&&&&&&&&&')
                # possible_tricks.append(possible_trick.copy())

                possible_trick.pop(-1)
                possible_plays.clear()
                # print('possible tricks',possible_tricks)

            # print('&&&&&&&&&&&&finished options&&&&&&&&&&&&&&&&')

        return possible_tricks.copy()



    def evaluate_trick(self,winner):
        if winner == self.name:
            return -15
        else:
            return 0


    def my_turn(self,play_order):
        for i in range(len(play_order)):
            if play_order[i] == self.name:
                return i




    def play_trick(self,cards_played,play_order):
        '''
        print()
        print('&&&&&&&&&&&&&&&&& parameters play trick &&&&&&&&&&&&&&&&&&&&&&&&&')
        print('cards played: ', cards_played)
        print('play order: ', play_order)
        print('players cards: ', self.players_cards)
'''
        suit = 'free'
        if len(cards_played) > 0:
            suit = cards_played[0][1][0]
        #print('suit: ',suit)
        #print('my cards: ',self.hand)
        #print(len(self.players_cards[0]),'cards left to play: ',self.players_cards[0])
        possible_tricks = self.minimax(len(cards_played),self.my_turn(play_order),suit,play_order)
        '''
        print('&&&&&&&&&&&&&&&&& end minimax &&&&&&&&&&&&&&&&&&&&&&&&&')
        print('possibl tricks: ',possible_tricks)
        print('possible_tricks length: ',len(possible_tricks))
'''
        #print('cards played: minimax ', cards_played)
        tricks = []
        temp = cards_played.copy()
        for i in range(len(possible_tricks)):
            if type(possible_tricks[i]) == list:

                for j in range(len(possible_tricks[i])):
                    #print('possibl tricks sub i : ',possible_tricks[i][j])
                    #print('before cards played: ',cards_played)
                    cards_played.append(possible_tricks[i][j])
                    #print('after cards played: ', cards_played)

            else:
                cards_played.append(possible_tricks[i])
            tricks.append(cards_played.copy())
            cards_played = temp.copy()

        if len(tricks) == 0:
            tricks = cards_played.copy()
        #print(len(tricks),'tricks: ', tricks)
        return tricks



    def trick_winner(self,cards_played):
        new_cards = cards()
        #print(cards_played)
        suit, rank = cards_played[0][1][0], new_cards.get_rank(cards_played[0][1][1])
        winner = 0
        for i in range(1, len(cards_played)):
            if cards_played[i][1][0] == suit and new_cards.get_rank(cards_played[i][1][1]) > rank:
                rank = new_cards.get_rank(cards_played[i][1][1])
                winner = i
        #print('winner is : ', cards_played[winner])
        return winner,cards_played[winner][0]

    def play_order(self,players, first_player):
        ordered = []
        for i in range(len(players)):
            ordered += [players[first_player % len(players)]]
            first_player += 1
        return ordered

    def set_play_order(self,players_order,cards_played):

        winner_index,winner_name = self.trick_winner(cards_played)
        players_order = self.play_order(players_order, winner_index)
        return players_order,winner_name


    def Q_reward(self,moves_ahead,cards_played,future_trick,play_order,players_cards):

        future_rewards = []
        '''
        print('&&&&&&&&&&&&&&&&& parameters Q reward &&&&&&&&&&&&&&&&&&&&&&&&&')
        print('moves: ',moves_ahead)
        print('cards played: ', cards_played)
        '''
        #print('future: ', future_trick)
        #print('play order: ', play_order)
        copy_my_hand = self.hand.copy()
        if moves_ahead == 0:
            #print('finnnnnnnnnnnneshed')
            return 0
        if future_trick :
            #delete your card

            self.players_cards = copy.deepcopy(players_cards)
            #print('play order: ', play_order)
            #print('my turn: ', self.my_turn(play_order))
            self.cards_played(cards_played,True,-1)
            #print('players_cards: ', self.players_cards[0])

            cards_played = []

        temp = copy.deepcopy(self.players_cards)
        #print('***************************************')
        if not future_trick:
            #print('cards played: ',cards_played,'    temp: ',temp)
            extracted_cards = self.extract_cards(cards_played,len(cards_played)-1)
            #extracted_cards.pop(len(extracted_cards)-1)
            for i in range(len(temp)):
                temp[i]+=extracted_cards


            #print('cards played: ', cards_played, '    temp: ', temp)
        #print('players cards O: ', temp)
        possible_tricks = self.play_trick(cards_played,play_order)
        self.players_cards = copy.deepcopy(temp.copy())
        '''
        print('***************************************')
        print('players cards O: ', temp)
        print('players cards c: ', self.players_cards)
        print('***************************************')
        '''
        my_turn = self.my_turn(play_order)

        #print('&&&&&&&&&&&&&&&&& end play trick &&&&&&&&&&&&&&&&&&&&&&&&&&')
        #print(len(possible_tricks),'possible tricks: ',possible_tricks)

        #print('cards played: play trick', cards_played)
        if type(possible_tricks[0]) == list:
            for i in range(len(possible_tricks)):
                play_order,winner = self.set_play_order(play_order, possible_tricks[i])
                #print('card to remove from my hand: ', possible_tricks[i][my_turn][1])
                #print('my hand: ', self.hand)
                self.hand.remove(possible_tricks[i][my_turn][1])
                #print('temp((((()))))): ',temp)
                future_rewards.append(self.Q_reward(moves_ahead-1,cards_played,True,play_order,copy.deepcopy(temp))+self.evaluate_trick(winner))
                self.hand = copy_my_hand.copy()
                #print('my hand after copy: ', self.hand)
                #print('&&&&&&&&&&&&&&&&& end sub Q reward &&&&&&&&&&&&&&&&&&&&&&&&&&')
        else :
            #print('type of possible tricks: ', type(possible_tricks),' possible tricks: ', possible_tricks)
            play_order, winner = self.set_play_order(play_order, possible_tricks)
            #print('card to remove from my hand: ', possible_tricks[my_turn][1])
            #print('my hand: ', self.hand)
            self.hand.remove(possible_tricks[my_turn][1])
            future_rewards.append(self.Q_reward(moves_ahead - 1, cards_played,True,play_order,copy.deepcopy(temp)) + self.evaluate_trick(winner))
            self.hand = copy_my_hand.copy()
            #print('my hand after copy: ', self.hand)
            #print('&&&&&&&&&&&&&&&&& end sub Q reward &&&&&&&&&&&&&&&&&&&&&&&&&&')

        '''
        if future_trick:
            return sum(future_rewards)  #* (self.discount * moves_ahead)
        else:
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            print('future rewards: ',future_rewards)
            print(len(possible_tricks),'possible tricks: ',possible_tricks)
            print('index: ',max(future_rewards))
            print(len(cards_played),'cards: ',cards_played)
            print('play order: ',play_order)
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

            if type(possible_tricks[0])==list:
                goal_trick = possible_tricks[future_rewards.index(max(future_rewards))]
                #print('goal trick: ',goal_trick)
            else:
                goal_trick = possible_tricks
                #print('goal trick: ',goal_trick)
            '''
        return sum(future_rewards)/len(future_rewards)

    def learned_Q_table(self):
        pass









'''
 print('^^^^^^^^^^^ first ^^^^^^^^^^^^^^^^^^^^^')
        print('action: ',action)
        print(self.action_space_first[action])

        number_of_cards_action = int((action-1)/6)
        print('my hand before: ',allowed_cards)
        suits_count = self.count_suits(allowed_cards)
        allowed_cards = self.choose_suit(allowed_cards, number_of_cards_action, suits_count)
        print('my hand after: ',allowed_cards)
        strong = int(action/3)%2==0
        print('cards action: ',number_of_cards_action,'   strong: ',strong,'   rank: ',action%3)
        if strong == self.evaluate_suit(allowed_cards):
            return action,self.perform_action([],allowed_cards,action % 3,True)
        else:
            action = action+3
            return action,self.perform_action([],allowed_cards,action % 3,True)
            '''