from cards import cards
import copy
import random


class player_diamonds:

    def __init__(self, name, trained):
        # games = ["tricks", "diamonds", "queens", "king", "jack"]
        games = ['diamond']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'A']
        self.suits = ['spade', 'heart', 'club', 'diamond']
        self.diamonds_left = []
        self.clubs_left = []
        self.hearts_left = []
        self.spade_left = []
        self.cards_left = []
        self.ai1_cards = []
        self.ai2_cards = []
        self.ai3_cards = []
        self.suits_left_list = [self.spade_left, self.hearts_left, self.clubs_left, self.diamonds_left]
        self.players_cards = []
        self.players_cards_expected = []
        self.players_cards_minimax = []
        self.name = name
        self.players = [self.name, 'ai1', 'ai2', 'ai3']
        self.players_order = self.players.copy()
        self.score = 0
        self.subscore = 0
        self.hand = []
        self.games = games
        self.temp = True
        self.game = 'diamonds'
        self.trained = trained
        self.legal = False
        self.strong = True
        self.Q_table = self.read_Q_table()
        self.state_space = {1: {True: {True: {True: 'first legal strong vulnerable', False: 'first legal strong covered'},
                                       False: {True: 'first legal weak vulnerable', False: 'first legal weak covered'}},
                                False: {True: {True: 'first illegal strong vulnerable', False: 'first illegal strong covered'},
                                        False: {True: 'first illegal weak vulnerable', False: 'first illegal weak covered'}}},
                            2: {True: {0: 'second yes poisonous', 1: 'second yes possible', 2: 'second yes safe'},
                                False: {True: {True: 'second no strong vulnerable', False: 'second no strong covered'},
                                        False: {True: 'second no weak vulnerable', False: 'second no weak covered'}}},
                            3: {True: {0: 'third yes poisonous', 1: 'third yes possible', 2: 'third yes safe'},
                                False: {True: {True: 'third no strong vulnerable', False: 'third no strong covered'},
                                        False: {True: 'third no weak vulnerable', False: 'third no weak covered'}}},
                            4: {True: {0: 'fourth yes poisonous', 1: 'fourth yes possible', 2: 'fourth yes safe'},
                                False: {True: {True: 'fourth no strong vulnerable', False: 'fourth no strong covered'},
                                        False: {True: 'fourth no weak vulnerable', False: 'fourth no weak covered'}}}}

        self.state_space_length = 29
        self.states_list = ['first legal strong vulnerable', 'first legal strong covered', 'first legal weak vulnerable',
                            'first legal weak covered',
                            'first illegal strong vulnerable', 'first illegal strong covered', 'first illegal weak vulnerable',
                            'first illegal weak covered',
                            'second yes poisonous', 'second yes possible', 'second yes safe',
                            'second no strong vulnerable',
                            'second no strong covered', 'second no weak vulnerable', 'second no weak covered',
                            'third yes poisonous','third yes possible', 'third yes safe','third no strong vulnerable',
                            'third no strong covered','third no weak vulnerable', 'third no weak covered',
                            'fourth yes poisonous','fourth yes possible','fourth yes safe', 'fourth no strong vulnerable',
                            'fourth no strong covered','fourth no weak vulnerable', 'fourth no weak covered']

        self.action_space_yes = ['low_card', 'mid_card', 'high_card']
        self.action_space_no = ['diamond', 'vulnerable', 'strong']
        self.action_space_first = ['diamond low', 'diamond mid', 'diamond high',
                                   'vulnerable low', 'vulnerable mid', 'vulnerable high',
                                   'few low', 'few mid', 'few high',
                                   'lot low', 'lot mid', 'lot high']

        self.type_of_suit = ['diamond','vulnerable','few','lot']
        self.action_space = ['low_card', 'mid_card', 'high_card']
        self.covered = {True:'vulnerable',False:  'covered'}
        self.strongness = {True: 'strong', False: 'weak'}
        self.action_indexes_first = []

    def cards_played(self, cards, index_my_card):
        cards_to_be_removed = self.extract_cards(cards)
        self.remove_cards(cards_to_be_removed)

    def extract_cards(self, cards):
        returned_card = []
        for i in range(len(cards)):
            returned_card.append(cards[i][1])
        return returned_card


    def reset_players_cards(self):
        self.players_cards = []
        self.players_cards.append(self.ai1_cards.copy())
        self.players_cards.append(self.ai2_cards.copy())
        self.players_cards.append(self.ai3_cards.copy())
        self.players_cards_expected = copy.deepcopy(self.players_cards)

    def remove_cards(self, cards):

        #print('cards:      ', cards)
        #print('suits:      ',self.suits_left)
        for i in cards:
            if i in self.players_cards[0]:
                self.players_cards[0].remove(i)
            if i in self.players_cards[1]:
                self.players_cards[1].remove(i)
            if i in self.players_cards[2]:
                self.players_cards[2].remove(i)
            if i in self.players_cards_expected[0]:
                self.players_cards_expected[0].remove(i)
            if i in self.players_cards_expected[1]:
                self.players_cards_expected[1].remove(i)
            if i in self.players_cards_expected[2]:
                self.players_cards_expected[2].remove(i)
            # print('index: ',self.suits.index(i[0]))
            if i in self.suits_left_list[self.suits.index(i[0])]:
                self.suits_left_list[self.suits.index(i[0])].remove(i)

        # print('suits after: ',self.suits_left)
        # print('players cards:    ',self.players_cards[0])
        # checked

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
        #print('expected: ',self.players_cards_expected)
        self.remove_cards(self.hand)
        if self.trained:
            self.legal = False
            self.strong_diamond()
        # checked

    def getKey(self, item):
        card_obj = cards()
        return card_obj.get_rank(item[1])

    def allowed_cards(self, suit, hand):
        allowed = []
        match = True
        for card in hand:
            if suit == card[0]:
                allowed.append(card)
        if len(allowed) == 0:
            match = False
            allowed = hand

        return allowed, match

    def receive_cards(self, cards):
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
        #print('sorted hand: ',self.hand)

        #print(self.name, 'cards: ', self.hand)
        # print(len(cards), ' cards: ', cards)
        self.reset_cards_left()
        # checked

    def played_card(self, card):
        for i in range(len(self.hand)):
            if card == self.hand[i]:
                return self.hand.pop(i)

    # need some adjustments
    def get_score(self):
        self.subscore = 0
        return self.score

    # need some adjustments
    def get_subscore(self):
        return self.subscore

    # need some adjustments
    def play(self, cards_played, play_order):
        self.players_order = play_order
        # print(self.name,'cards: ',self.hand,'  hearts left: ',self.hearts_left)

        if len(cards_played) > 0:

            allowed_suit = cards_played[0][1][0]
            allowed, match = self.allowed_cards(allowed_suit, self.hand)
            '''
                print('^^^^^^^^^^^^^^^^^^^^ AI options ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                print('      your hand     ', '        allowed cards ')
                for i in range(len(self.hand)):
                    if i < len(allowed):
                        print(i + 1, ': ', self.hand[i], '   ', i + 1, ': ', allowed[i])
                    else:
                        print(i + 1, ': ', self.hand[i])
                print('^^^^^^^^^^^^^^^^^^^^ AI decision ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
'''
            card = self.Q_table_decision(cards_played, allowed, match)

            #print('trained card: ', card)
            print('allowed: ',allowed)
            return self.played_card(card)


        else:
            '''
                print('^^^^^^^^^^^^^^^^^^^^ AI options ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                for i in range(len(self.hand)):
                    print(i + 1, ': ', self.hand[i])
                print('^^^^^^^^^^^^^^^^^^^^ AI decision ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                '''
            # allowed = self.allowed_cards(cards_played[1][0])
            # print(allowed)
            card = self.Q_table_decision(cards_played.copy(), self.hand, True)
            #print('trained card: ', card)
            print('allowed: ', self.hand)
            return self.played_card(card)


    # need some check why ai players do not play the max card when they play a different suit

    def valid_actions(self, allowed_cards, highest_card):
        #print('*************** valid actions *************')
        #print('allowed_cards: ',allowed_cards)
        #print('highest: ',highest_card)
        card_obj = cards()
        if len(allowed_cards) == 1:
            return [2], False
        if highest_card > card_obj.get_rank(allowed_cards[-1][1]):
            return [2], False
        if highest_card < card_obj.get_rank(allowed_cards[0][1]):
            return [1, 2], True
        return [0, 1, 2], True

    def valid_action_diamond(self,suit,cards_played):
        counter = 0
        for i in cards_played:
            if i[1][0]== suit:
                counter+=1
        if len(self.suits_left(suit))-counter<6:
            return 0
        return 2



    def update_score(self, trick,game):

        trick_score = 0
        for i in trick:
            #print('suit: ',i[1][0])
            if i[1][0] == 'diamond':
                trick_score+=10
        self.subscore -= trick_score
        self.score -= trick_score


    def create_Q_table(self):

        table = []
        for i in range((self.state_space_length)):
            state = []
            if 'legal' in self.states_list[i]:
                actions = self.action_space_first
            elif 'yes' in self.states_list[i]:
                actions = self.action_space_yes
            elif ' no ' in self.states_list[i]:
                actions = self.action_space_no
            for j in range(len(actions)):
                state.append(0)
            table.append(state)
        return table

    def min_card(self, allowed_cards, first, max):
        card_obj = cards()

        if first:
            max = 5
        #print(max)
        card = allowed_cards[0]
        min_rank = card_obj.get_rank(card[1])
        found_lower_than_max = min_rank < max
        for i in range(1, len(allowed_cards)):
            if not found_lower_than_max:
                if card_obj.get_rank(allowed_cards[i][1]) < min_rank:
                    card = allowed_cards[i]
                    min_rank = card_obj.get_rank(allowed_cards[i][1])
                    found_lower_than_max = min_rank < max
            elif card_obj.get_rank(allowed_cards[i][1]) > min_rank and card_obj.get_rank(allowed_cards[i][1]) < max:
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

    def mid_card(self, allowed_cards, first, min):
        # print('mid card')
        card_obj = cards()
        if first:
            min = 2
        # print(min)
        card = allowed_cards[0]
        mid_rank = card_obj.get_rank(card[1])
        found_good_rank = min < mid_rank
        for i in range(1, len(allowed_cards)):
            # print('mid: ',mid_rank,'  min: ',min,'   rank: ',card_obj.get_rank(allowed_cards[i][1]))
            if not found_good_rank:
                # print('did not find')
                if card_obj.get_rank(allowed_cards[i][1]) > mid_rank:
                    # print('if', allowed_cards[i])
                    card = allowed_cards[i]
                    mid_rank = card_obj.get_rank(allowed_cards[i][1])
                    found_good_rank = min < mid_rank
            elif card_obj.get_rank(allowed_cards[i][1]) < mid_rank and card_obj.get_rank(allowed_cards[i][1]) > min:
                # print('elif',allowed_cards[i])
                card = allowed_cards[i]
                mid_rank = card_obj.get_rank(allowed_cards[i][1])

        return card

    def highest_card_played(self, cards_played):
        new_cards = cards()
        suit, rank = cards_played[0][1][0], new_cards.get_rank(cards_played[0][1][1])
        for i in range(1, len(cards_played)):
            if cards_played[i][1][0] == suit and new_cards.get_rank(cards_played[i][1][1]) > rank:
                rank = new_cards.get_rank(cards_played[i][1][1])
        return rank

    def remove_player_cards(self, player, highest_rank, player_rank, suit, match, base_suit, trick):

        #print('remove player cards')
        new_cards = cards()
        index_player = 0
        for i in range(len(self.players)):
            if self.players[i] == player:
                index_player = i - 1
                break
        card = copy.deepcopy(self.players_cards_expected[index_player])
        for i in trick:
            if i[1] in card:
                #print('to be removed: ',i[1])
                #print('cards to remove from: ',card)
                card.remove(i[1])
                #print('cards after remove: ', card)

        #print(player,' ',highest_rank,' ',player_rank,' ',suit)
        #print(len(self.hand),len(card),card)
        if match:
            for i in range(highest_rank - player_rank - 1):
                if (suit, new_cards.get_rank_name(player_rank + i + 1)) in card:
                    card.remove((suit, new_cards.get_rank_name(player_rank + i + 1)))
        else:
            for i in range(14 - player_rank):
                if (suit, new_cards.get_rank_name(player_rank + i)) in card:
                    card.remove((suit, new_cards.get_rank_name(player_rank + i)))

            #print(len(card), card)
            counter = 0
            for i in range(len(card)):
                #print('len: ', len(card), '  suit: ', base_suit, '  i: ', i)
                #print(card)
                if card[i - counter][0] == base_suit:
                    card.pop(i - counter)
                    counter += 1

        #print(len(self.hand),len(card),card)
        return copy.deepcopy(card), index_player

    def remove_higher_cards(self, player, rank, suit):
        new_cards = cards()
        index_player = 0
        # print(player)
        for i in range(len(self.players)):
            if self.players[i] == player:
                index_player = i - 1
                break
        card = copy.deepcopy(self.players_cards_expected[index_player])
        # print(len(card),'cards before process:     ', card)
        for i in range(13 - rank):
            if (suit, new_cards.get_rank_name(rank + i + 1)) in card:
                card.remove((suit, new_cards.get_rank_name(rank + i + 1)))
        # print(len(card),'cards after process:      ', card)
        return copy.deepcopy(card), index_player

    def analyse_trick_diamond(self,previous_trick,trick_winner):
        suit = previous_trick[0][1][0]
        if suit == 'diamond' or self.possible_diamond(previous_trick) != 2:
            self.analyse_trick(previous_trick,trick_winner,suit,False)
        else :
            self.analyse_trick(previous_trick,trick_winner,suit,True)

    def analyse_trick(self, previous_trick, trick_winner,suit,safe):

        new_cards = cards()
        #print('winnnnnnner: ',trick_winner)
        for i in range(len(previous_trick)):
            if safe:
                rank = 14
            else:
                rank = self.highest_card_played(previous_trick[:i + 1])
            #print('rank: ',rank)
            if not previous_trick[i][0] == 'Motaz':
                #print('analyse trick')
                #print('player: ',previous_trick[i][0], ' ',previous_trick[i][1])
                player_rank = new_cards.get_rank(previous_trick[i][1][1])
                if previous_trick[i][1][0] == suit:
                    if player_rank < rank:
                        expected, index = self.remove_player_cards(previous_trick[i][0], rank, player_rank, suit, True,
                                                                   suit, previous_trick)
                        self.players_cards_expected[index] = expected
                else:
                    player_suit = previous_trick[i][1][0]
                    expected, index = self.remove_player_cards(previous_trick[i][0], rank, player_rank, player_suit,
                                                               False, suit, previous_trick)
                    self.players_cards_expected[index] = copy.deepcopy(expected)
            if i == len(previous_trick) - 1 and previous_trick[i][0] == trick_winner and trick_winner != 'Motaz':
                # print('winner: ',trick_winner,'  player: ',previous_trick[i][0])
                expected, index = self.remove_higher_cards(previous_trick[i][0], rank, suit)
                self.players_cards_expected[index] = expected

    def number_of_cards(self):
        #print('ai1 cards expected: ', len(self.players_cards_expected[0]))
        #print('ai2 cards expected: ', len(self.players_cards_expected[1]))
        #print('ai3 cards expected: ', len(self.players_cards_expected[2]))
        if len(self.players_cards_expected[0]) < len(self.hand) or len(self.players_cards_expected[1]) < len(
                self.hand) or len(self.players_cards_expected[2]) < len(self.hand):
            if 4 > self.hand:
                return 4

    def count_suits(self, cards):
        # print('cards to count: ',cards)
        suits_length = []
        count_index = 0
        suit_length = 0
        counted_suit = cards[0][0]
        for i in cards:
            if i[0] == counted_suit:
                suit_length += 1
            else:
                suits_length.append(suit_length)
                counted_suit = i[0]
                suit_length = 1
        suits_length.append(suit_length)
        # print('counted suits: ',suits_length)
        return suits_length

    def remove_min_suit(self, cards, start_index, length, suits_count):
        '''
        print('remove min')
        print('cards: ',cards)
        print('start_index: ',start_index)
        print('length: ',length)
        print('suits count: ',suits_count)
        '''
        suits_count.remove(length)
        if start_index == 0:
            # print('returned: ',cards[start_index+length:])
            return cards[start_index + length:], suits_count
        elif start_index + length == len(cards):
            # print('elif')
            # print('returned: ', cards[:start_index])
            return cards[:start_index], suits_count
        else:
            first_part = cards[:start_index]
            second_part = cards[start_index + length:]
            new_cards = first_part + second_part
            # print('returned: ', new_cards)
            # print('new cards: ',new_cards)
            return new_cards, suits_count

    def choose_suit(self, cards, action, suits_count):
        '''
        print('choose suit')
        print('cards: ', cards)
        print('actio: ', action)
        print('suits count: ', suits_count)
        '''
        if len(suits_count) == 1:
            # print('it is only one suit')
            return cards

        min_suit_length = min(suits_count)
        min_suit_index = suits_count.index(min_suit_length)
        start_index = 0

        for j in range(min_suit_index):
            start_index += suits_count[j]

        if action == 0:
            return cards[start_index:start_index + min_suit_length]
        elif action == 1:
            if len(suits_count) == 2:
                return cards[start_index:start_index + min_suit_length]
            else:
                cards, suits_count = self.remove_min_suit(cards, start_index, min_suit_length, suits_count)
                return self.choose_suit(cards, action - 1, suits_count)
        else:
            if len(suits_count) == 2:
                if start_index == 0:
                    # print('start index: ',start_index)
                    # print('min len: ',min_suit_length)
                    # print('returned card: ',cards[start_index+min_suit_length:])
                    return cards[start_index + min_suit_length:]
                else:
                    # print('returned card: ', cards[:start_index])
                    return cards[:start_index]
            else:
                cards, suits_count = self.remove_min_suit(cards, start_index, min_suit_length, suits_count)
                return self.choose_suit(cards, action, suits_count)
        # checked



    def elimnate_invalid_actions(self, list_indexes, word):
            # print('elim: ',word)
            # print('action: ',self.action_space_first)
            # print('index: ',self.action_indexes_first)
        counter = 0
        for i in range(len(self.action_space_first)):
            if word in self.action_space_first[i]:
                list_indexes.pop(i - counter)
                counter += 1
        return list_indexes

    def keep_valid_actions(self, list_indexes, word):
        #print('keep: ',word)
        #print('action: ',self.action_space_first)
        #print('index: ',self.action_indexes_first)
        counter = 0
        for i in range(len(self.action_space_first)):
            if not word in self.action_space_first[i]:
                list_indexes.pop(i - counter)
                counter += 1

        #print('indexes: ', list_indexes)
        return list_indexes

    def check_valid_number_cards(self,word,suits_count):
        if word == 'few':
            return len(suits_count)>1
        if word == 'mid':
            return len(suits_count)>2
        return True

    def check_valid_strongness(self,word,allowed_cards):
        #print('word: ',word)
        #print('allowed: ',allowed_cards)
        if not self.free_suit(allowed_cards[0][0]):
            evaluation = self.evaluate_suit(allowed_cards)
            #print('evaluation: ',evaluation)
            return word == self.strongness.get(evaluation[1])
        return False

    def check_valid_rank_action(self,word,allowed_cards):
        #print('word: ', word)
        #print('allowed: ', allowed_cards)
        if word == 'mid_card':
            return len(allowed_cards)>2
        if word == 'high_card':
            return len(allowed_cards) > 1
        return True

    def play_good_card(self,allowed_cards):
        #print('check please')
        for i in allowed_cards:
            if not self.free_suit(i[0]):
                return i
        #print('you only have free suit')
        return allowed_cards[0]

    def suit_type(self,suits_dic,word,allowed_cards):

        #print('suits dic: ',suits_dic)
        #print('word: ',word)
        #print('allowed cards: ',allowed_cards)
        if word == 'diamond':
            if suits_dic.get('diamond') != None:
                return self.extract_suits(allowed_cards).get('diamond')
            else:
                return False

        elif word == 'vulnerable':
            for i in self.suits:
                #print('suits dic check: ',suits_dic)
                if suits_dic.get(i) != None and not suits_dic.get(i):
                    return self.extract_suits(allowed_cards).get(i)
            return False
        suits_count = self.count_suits(allowed_cards)
        #print('** suits count ** : ', suits_count)
        if word == 'few':
            suit = self.choose_suit(allowed_cards, 0, suits_count)
            if suit[0][0] == 'diamond':
                print('few diamond')
                print('allowed: ',allowed_cards)
                counter = 0
                for i in range(len(allowed_cards)):
                    if allowed_cards[i-counter][0] == 'diamond':
                        allowed_cards.pop(i)
                        counter+=1
                print('allowed: ', allowed_cards)
                return self.choose_suit(allowed_cards, 0, suits_count)
            return suit

        elif word == 'lot':
            return self.choose_suit(allowed_cards, 2, suits_count)




    '''
    'diamond low', 'diamond mid', 'diamond high',
    'vulnerable low', 'vulnerable mid', 'vulnerable high',
    'few low', 'few mid', 'few high',
    'lot low', 'lot mid', 'lot high']
    '''

    def perform_action_first(self, allowed_cards,actions,suits_dic):
        #print('allowed cards fir: ', allowed_cards)
        if len(actions) == 0:
            return self.play_good_card(allowed_cards)

        action = actions[0]
        number_of_type_action = int((action - 1) / 3)
        number_of_type_action = self.type_of_suit[number_of_type_action]
        print('type word: ',number_of_type_action)
        suit = self.suit_type(suits_dic,number_of_type_action,allowed_cards)
        print('check suit: ',suit)
        if type(suit) != list:
            actions.pop(0)
            return self.perform_action_first(allowed_cards,actions,suits_dic)
        print('type of card: ',action%3)
        card = self.perform_action([],suit,action%3,True)
        print('card returned: ',card)
        return card


        #print('valid number of cards')


        if not self.check_valid_strongness(strong_word, suit_to_play):
            actions.pop(0)
            return self.perform_action_first(actions, allowed_cards)
        # print('valid strongness ')

        if not self.check_valid_rank_action(rank_word, suit_to_play):
            actions.pop(0)
            return self.perform_action_first(actions, allowed_cards)

        return self.perform_action([], suit_to_play, rank, True)





        '''
        actions = []
        a, evaluation = self.suits_evaluation()
        #print('eval fir: ', evaluation)
        if type(evaluation.get('free'))!=None:
            return False,0,allowed_cards[0]
        suits = self.extract_suits(allowed_cards)
        diamond_suit = suits.get('diamond')
        vulnerable_suit = []
        strong_suit = []
        found_vulnerable = True
        action=2
        index_short = 0
        index_long = 1
        for i in self.suits:
            if type(evaluation.get(i)) == bool and i != 'diamond' and found_vulnerable and evaluation.get(i) :
                vulnerable_suit = suits.get(i)
                #print('vuln: ', vulnerable_suit)
                actions.append(1)
                found_vulnerable = False
            if type(evaluation.get(i)) == bool and i != 'diamond' and not evaluation.get(i):
                strong_suit.append(suits.get(i))
                #print('stro: ', strong_suit)
                actions.append(action)
                action+=1
        if len(strong_suit) == 2:
            if len(strong_suit[0])>len(strong_suit[1]):
                index_long = 0
                index_short = 1




        if type(diamond_suit) == list:
            actions.append(0)

        #print('actions fir: ', actions)
        action = actions[random.randrange(len(actions))]
        #print('action: ', action)

        suit_to_play = diamond_suit
        if action == 1:
            suit_to_play = vulnerable_suit
        elif action == 2:
            suit_to_play = strong_suit[index_short]
        elif action == 3:
            suit_to_play = strong_suit[index_long]

        #print('suit to play: ', suit_to_play)
        rank_action = random.randrange(3)
        #print('rank action: ',action*3+rank_action)
        #print('rank action: ',self.action_space_first[action*3+rank_action])



        return len(actions) > 1, action*3+rank_action, self.perform_action(cards_played, suit_to_play, rank_action, True)
'''
        # checked might require considering the case of performing different action than desired

    def perform_action(self, cards_played, allowed_cards, action, match):
        #print('cards played: ',cards_played)
        #print('allowed: ',allowed_cards,' action: ',action,' match: ',match)
        #print('action: ',action,'   match: ',match)
        if not match:
            suits_count = self.count_suits(allowed_cards)
            #print('allowed original: ',allowed_cards)
            #print('actions: ',action)
            if type(action) == list:
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
                return self.min_card(allowed_cards, True, 0)
            return self.min_card(allowed_cards, False, self.highest_card_played(cards_played))

        elif action == 1:
            if len(cards_played) == 0:
                return self.mid_card(allowed_cards, True, 0)
            # print('midddd')
            return self.mid_card(allowed_cards, False, self.highest_card_played(cards_played))
        else:
            #print('allowed: ',allowed_cards)
            #print('the max card: ',self.max_card(allowed_cards))
            return self.max_card(allowed_cards)
        # checked (mid need to be corrected)


    def perform_action_no(self, allowed_cards):
        #print('allowed cards no: ',allowed_cards)
        actions = []
        a, evaluation = self.suits_evaluation()
        print('eval no: ', evaluation)
        if type(evaluation.get('free'))!=None:
            return False,0,allowed_cards[0]
        suits = self.extract_suits(allowed_cards)
        diamond_suit = suits.get('diamond')
        vulnerable_suit = []
        strong_suit = []
        found_vulnerable = True
        for i in self.suits:
            if type(evaluation.get(i)) == bool and evaluation.get(i) and i != 'diamond' and found_vulnerable:
                vulnerable_suit = suits.get(i)
                print('vuln: ', vulnerable_suit)
                actions.append(1)
                found_vulnerable = False
            if type(evaluation.get(i)) == bool and not evaluation.get(i):
                strong_suit.append(suits.get(i))
                print('stro: ', strong_suit)
                actions.append(2)

        if type(diamond_suit) == list:
            actions.append(0)

        print('actions no: ', actions)
        action = actions[random.randrange(len(actions))]
        #print('action: ', action)
        suit_to_play = diamond_suit
        if action == 1:
            suit_to_play = vulnerable_suit
        elif action == 2:
            suit_to_play = strong_suit[0]

        #print('suit to play: ', suit_to_play)
        return len(actions) > 1, action, suit_to_play[-1]


    def extract_suits(self, cards):
        my_cards = {}
        suit = cards[0][0]
        my_suit = []
        for i in cards:
            if i[0] == suit:
                my_suit.append(i)
            else:
                my_cards[suit] = my_suit.copy()
                suit = i[0]
                my_suit.clear()
                my_suit.append(i)
        my_cards[suit] = my_suit.copy()

        #print('my hand: ',cards)
        #print('my suits: ',my_cards)

        return my_cards.copy()

    # checked

    def majority_less(self, highest, allowed_cards):
        # print('majority less: ',highest)
        # print('allowed cards: ',allowed_cards)

        card_obj = cards()
        for i in range(len(allowed_cards)):
            if card_obj.get_rank(allowed_cards[i][1]) > highest:
                return len(allowed_cards) - i < i
            if i == 3:
                return True
        return True

    def evaluate_suit(self, my_cards):
        #print('####### evalutae ##########')
        suit = my_cards[0][0]
        number_of_my_cards = len(my_cards)
        temp = []
        limit = 0
        #print(self.players_cards_expected)
        for i in self.players_cards_expected:
            player_suit = self.extract_suits(i).get(suit)
            #print('type of suit: ',player_suit)
            if type(player_suit) == list:
                temp.append(len(player_suit))
                if temp[-1] > 0:
                    limit += 1

        number_of_players_cards = min(temp)
        temp = [number_of_my_cards, number_of_players_cards]
        number_of_cards_to_check = min(temp)
        # print('temp: ',temp)
        # print('number: ',number_of_cards_to_check)
        # print('players cards expected: ',number_of_players_cards)
        # print('my cards: ', my_cards)

        card_obj = cards()
        strong = True

        cards_left = self.suits_left(suit)
        # self.extract_suits(my_cards).get(suit)
        # print('cards to check: ',my_cards)
        # print('cards to compare: ',cards_left)
        # print('cards checke: ',number_of_cards_to_check)
        # print('limit: ',limit)
        found = False
        for i in range(number_of_cards_to_check):
            my_rank = card_obj.get_rank(my_cards[i][1])
            for j in range(limit):
                if i * limit + j < len(cards_left):
                    rank_to_compare = card_obj.get_rank(cards_left[i * limit + j][1])
                    if rank_to_compare > my_rank:
                        found = True
                        break
                else:
                    found = True
                    break
            if not found:
                strong = found
                break
        # print('strong: ',strong)

        return (my_cards[0][0], strong)

    def suits_left(self, suit):
        # print('suit: ',suit)
        # print('suits left: ',self.suits_left_list[self.suits.index(suit)])
        return self.suits_left_list[self.suits.index(suit)]

    def free_suit(self, suit):
        if len(self.suits_left(suit)) == 0:
            #print('free suit: ',self.suits_left(suit))
            return True
        return False

    def strong_diamond(self):
        if self.free_suit('diamond'):
            #print('free diamond')
            return False
        suit = self.extract_suits(self.hand).get('diamond')
        #print(type(suit),' suit: ',suit)
        if type(suit)==list:
            a, strong = (self.evaluate_suit(suit))
            #print(strong)
            self.strong = strong
        else:
            self.strong = True
        #self.extract_suits()

    def suits_evaluation(self):
        evaluation = {}
        my_cards = self.extract_suits(self.hand)
        vulnerable = False
        #print('my cardss: ',my_cards)
        for i in self.suits:
            if not self.free_suit(i):
                suit = my_cards.get(i)
                #print('suit: ',suit)
                if type(suit) == list:
                    a, eval=self.evaluate_suit(suit)
                    if not eval:
                        vulnerable = True
                    evaluation[i]=(eval)
        if len(evaluation)==0:
            evaluation['free']=my_cards
            #print('hey')
        #print('eval: ',evaluation)
        return vulnerable,evaluation

    def state_of_the_game(self, tricks_left):
        return int(tricks_left / 5.25)

    def analyse_different(self,cards_played,cards):
        counter = 0
        for i in range(len(cards_played)):
            if cards_played[i][1] in cards:
                cards.remove(cards_played[i][1])
                counter+=1
        return cards,counter


    def potential_different(self,suit,cards,cards_played):

        #print(suit, '  pot cards: ',cards)
        cards, cards_removed= self.analyse_different(cards_played,cards)
        #print(suit, '  pot cards: ', cards)
        suit_player = self.extract_suits(cards).get(suit)
        #print('cards removed: ',cards_removed)
        #print('suit player: ',suit_player)
        if type(suit_player)!=list:
            return True
        suit_left = len(suit_player)
        #print('left suit: ',suit_left)
        if suit_left-cards_removed<4:
            return True
        return (len(self.suits_left(suit))-cards_removed)-suit_left >3

    def possible_diamond(self,cards_played):
        #print('possible diamond')
        #print(cards_played)
        cards = self.extract_cards(cards_played)
        #print(cards)
        for i in cards:
            if i[0]=='diamond':
                return 0
        players_left = 4-(len(cards_played)+1)
        for i in range(players_left):
            if self.potential_different(cards_played[0][1][0],self.players_cards_expected[i],cards_played):
                #print('hello')
                return 1

        return 2

    def current_state(self, cards_played, allowed_cards, match):

        #print('cards played: ', cards_played)
        #print(len(allowed_cards),'allwed cards: ',allowed_cards)
        vulnerable, suits_dic = self.suits_evaluation()
        if len(cards_played) == 0:
            #print('leg: ',self.legal,'  str: ',self.strong,'  vul: ',vulnerable)
            return self.state_space.get(1).get(self.legal).get(self.strong).get(vulnerable),suits_dic

        if match:
            #print('mat: ', match, '  str: ', self.possible_diamond(cards_played))
            return self.state_space.get(len(cards_played) + 1).get(match).get(self.possible_diamond(cards_played)),suits_dic

        #print('mat: ', match, '  str: ', self.strong, '  vul: ', vulnerable)
        return self.state_space.get(len(cards_played) + 1).get(match).get(self.strong).get(vulnerable),suits_dic

    # checked
    def best_action(self,valid_actions,possible_actions):
        print('valid acti: ',valid_actions)
        print('poss acti: ',possible_actions)

        for i in range(len(possible_actions)):
            print('max: ',max(possible_actions))
            print('possible best: ',possible_actions.index(max(possible_actions)))
            best_action = possible_actions.index(max(possible_actions))
            print('best to check: ',best_action)
            if best_action in valid_actions:
                print('best: ',best_action)
                return best_action
            possible_actions[best_action]= -1000


    def best_actions_indexes(self,possible_actions):
        temp_actions = possible_actions.copy()
        possible_actions = sorted(possible_actions)
        ab = []
        for i in range(len(possible_actions)):
            ab.append(i)
        #print('original actions: ',temp_actions)
        #print('         indexes: ',ab)
        #print('sorted actions: ',possible_actions)
        indexes = []
        for i in range(len(possible_actions)):

            indexes.append(temp_actions.index(possible_actions[-(i+1)]))
        #print('indexes: ',indexes)
        return indexes


    # check if I have a choice or I am forced to play a card
    def Q_table_decision(self, cards_played, allowed_cards, match):
        state,suits_dic = self.current_state(cards_played, allowed_cards, match)

        print('state: ',state)
        if state[0:5] == 'first':
                # print('yes it is first: ',action)
            actions = self.best_actions_indexes(self.Q_table[self.states_list.index(state)])

            return self.perform_action_first(self.hand,actions,suits_dic)

        if not match:
            suits = self.extract_suits(self.hand)
            if suits.get('diamond')!= None:
                return self.perform_action([], suits.get('diamond'), 2, True)
            return self.perform_action([], self.hand, 0, match)

        actions, have_choice = self.valid_actions(allowed_cards, self.highest_card_played(cards_played))
        print('actions: ', actions)

        if not have_choice:
            print(len(self.Q_table),'Q table: ',self.Q_table)
            print('check actions: ',self.Q_table[self.states_list.index(state)])
            action = self.best_action(actions, self.Q_table[self.states_list.index(state)].copy())
            print('best action: ',action)
        else:
            action = 2
            # print('forced action')
        return self.perform_action(cards_played, allowed_cards, action, match)



            # print('action: ',action)



    def my_turn(self, play_order):
        for i in range(len(play_order)):
            if play_order[i] == self.name:
                return i

    # checked first iteration
    # checked minimax first iteration


    def rewards_to_string(self, actions):
        rewards_string = ''
        for i in actions:
            rewards_string += str(i) + ', '
        # print(rewards_string)
        return rewards_string

    def extract_rewards(self, reward):
        return reward[-1]

    def preprocess(self, content):

        preprocessed = []
        for i in range(len(content)):

            preprocessed.append(content[i][content[i].index(':') + 1:])
        return (preprocessed)

    def merge_table(self, table):
        for i in range(len(self.Q_table)):
            for j in range(len(self.Q_table[i])):
                self.Q_table[i][j] = self.Q_table[i][j] + table[i][j]

    def read_Q_table(self):
        # print('read table')
        # print()
        f = open("diamonds tables.txt", "r")
        content = self.preprocess(f.readlines())
        print('finished preprocessing')
        print('after',content)
        for i in range(len(content)):
            content_list = content[i].split(",")
            # print(content_list)
            content_list.pop(len(content_list) - 1)
            for j in range(len(content_list)):
                content_list[j] = (float(content_list[j]))

            content[i] = content_list

        print('########## content list ############# ', content)
        # print(content_list)

        f.close()
        return content

    def learned_Q_table(self, first_line):

        print('########## content list ############# ', self.Q_table)
        new_table = self.read_Q_table().copy()
        self.merge_table(new_table)
        print('########## content list ############# ', self.Q_table)

        f = open("Q tables.txt", "w")
        f.write(first_line)
        for i in range(len(self.states_list)):
            line_to_write = self.states_list[i] + ': ' + self.rewards_to_string(self.Q_table[i])
            line_to_write += '\n'
            f.write(line_to_write)
        f.close()

        # open and read the file after the appending:

        # print(f.read())