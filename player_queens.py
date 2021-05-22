from cards import cards
import copy
import random


class player_queens:

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
        self.queens = []
        self.strong = []
        self.advantages = []
        self.state_space = {1: {True: {True: {True:{True:'first with strong vulnerable advantage',False:'first with strong vulnerable disadvantage'},
                                            False:{True:'first with strong covered advantage',False:'first with strong covered disadvantage'}},
                                       False:{True:{True:'first with weak vulnerable advantage',False:'first with weak vulnerable disadvantage'},
                                            False:{True:'first with weak covered advantage',False:'first with weak covered disadvantage'}}},
                                False:{True: {True:{True:'first without strong vulnerable advantage',False:'first without strong vulnerable disadvantage'},
                                            False:{True:'first without strong covered advantage',False:'first without strong covered disadvantage'}},
                                       False:{True:{True:'first without weak vulnerable advantage',False:'first without weak vulnerable disadvantage'},
                                            False:{True:'first without weak covered advantage',False:'first without weak covered disadvantage'}}}},

                            2: {True: {0: 'second yes poisnonous', 1: 'second yes possible', 2: 'second yes safe'},
                                False: {True:{True: {True: {True: 'second no with strong vulnerable advantage',False: 'second no with strong vulnerable disadvantage'},
                                                     False: {True: 'second no with strong covered advantage',False: 'second no with strong covered disadvantage'}},
                                                False: {True: {True: 'second no with weak vulnerable advantage', False: 'second no with weak vulnerable disadvantage'},
                                                        False: {True: 'second no with weak covered advantage',False: 'second no with weak covered disadvantage'}}},
                                        False:{True: {True: {True: 'second no without strong vulnerable advantage',False: 'second no without strong vulnerable disadvantage'},
                                                     False: {True: 'second no without strong covered advantage',False: 'second no without strong covered disadvantage'}},
                                                False: {True: {True: 'second no without weak vulnerable advantage', False: 'second no without weak vulnerable disadvantage'},
                                                        False: {True: 'second no without weak covered advantage',False: 'second no without weak covered disadvantage'}}}}},

                            3: {True: {0: 'third yes poisnonous', 1: 'third yes possible', 2: 'third yes safe'},
                                False: {True: {True: {True: {True: 'third no with strong vulnerable advantage',False: 'third no with strong vulnerable disadvantage'},
                                                      False: {True: 'third no with strong covered advantage',False: 'third no with strong covered disadvantage'}},
                                               False: {True: {True: 'third no with weak vulnerable advantage',False: 'third no with weak vulnerable disadvantage'},
                                                       False: {True: 'third no with weak covered advantage',False: 'third no with weak covered disadvantage'}}},
                                        False: {True: {True: {True: 'third no without strong vulnerable advantage',False: 'third no without strong vulnerable disadvantage'},
                                                       False: {True: 'third no without strong covered advantage',False: 'third no without strong covered disadvantage'}},
                                                False: {True: {True: 'third no without weak vulnerable advantage', False: 'third no without weak vulnerable disadvantage'},
                                                        False: {True: 'third no without weak covered advantage',False: 'third no without weak covered disadvantage'}}}}},

                            4: {True: {0: 'fourth yes poisnonous', 1: 'fourth yes possible', 2: 'fourth yes safe'},
                                False: {True: {True: {True: {True: 'fourth no with strong vulnerable advantage',False: 'fourth no with strong vulnerable disadvantage'},
                                                      False: {True: 'fourth no with strong covered advantage', False: 'fourth no with strong covered disadvantage'}},
                                               False: {True: {True: 'fourth no with weak vulnerable advantage',False: 'fourth no with weak vulnerable disadvantage'},
                                                       False: {True: 'fourth no with weak covered advantage', False: 'fourth no with weak covered disadvantage'}}},
                                        False: {True: {True: {True: 'fourth no without strong vulnerable advantage',False: 'fourth no without strong vulnerable disadvantage'},
                                                       False: {True: 'fourth no without strong covered advantage',False: 'fourth no without strong covered disadvantage'}},
                                                False: {True: {True: 'fourth no without weak vulnerable advantage', False: 'fourth no without weak vulnerable disadvantage'},
                                                        False: {True: 'fourth no without weak covered advantage',False: 'fourth no without weak covered disadvantage'}}}}}}


        self.states_list = ['first with strong vulnerable advantage','first with strong vulnerable disadvantage',
                            'first with strong covered advantage', 'first with strong covered disadvantage',
                            'first with weak vulnerable advantage', 'first with weak vulnerable disadvantage',
                            'first with weak covered advantage', 'first with weak covered disadvantage',
                            'first without strong vulnerable advantage', 'first without strong vulnerable disadvantage',
                            'first without strong covered advantage', 'first without strong covered disadvantage',
                            'first without weak vulnerable advantage', 'first without weak vulnerable disadvantage',
                            'first without weak covered advantage', 'first without weak covered disadvantage',

                            'second yes poisnonous', 'second yes possible', 'second yes safe',
                            'second no with strong vulnerable advantage', 'second no with strong vulnerable disadvantage',
                            'second no with strong covered advantage', 'second no with strong covered disadvantage',
                            'second no with weak vulnerable advantage', 'second no with weak vulnerable disadvantage',
                            'second no with weak covered advantage', 'second no with weak covered disadvantage',
                            'second no without strong vulnerable advantage','second no without strong vulnerable disadvantage',
                            'second no without strong covered advantage', 'second no without strong covered disadvantage',
                            'second no without weak vulnerable advantage', 'second no without weak vulnerable disadvantage',
                            'second no without weak covered advantage', 'second no without weak covered disadvantage',

                            'third yes poisnonous', 'third yes possible', 'third yes safe',
                            'third no with strong vulnerable advantage', 'third no with strong vulnerable disadvantage',
                            'third no with strong covered advantage', 'third no with strong covered disadvantage',
                            'third no with weak vulnerable advantage', 'third no with weak vulnerable disadvantage',
                            'third no with weak covered advantage', 'third no with weak covered disadvantage',
                            'third no without strong vulnerable advantage','third no without strong vulnerable disadvantage',
                            'third no without strong covered advantage', 'third no without strong covered disadvantage',
                            'third no without weak vulnerable advantage', 'third no without weak vulnerable disadvantage',
                            'third no without weak covered advantage', 'third no without weak covered disadvantage',

                            'fourth yes poisnonous','fourth yes possible','fourth yes safe',
                            'fourth no with strong vulnerable advantage', 'fourth no with strong vulnerable disadvantage',
                            'fourth no with strong covered advantage', 'fourth no with strong covered disadvantage',
                            'fourth no with weak vulnerable advantage', 'fourth no with weak vulnerable disadvantage',
                            'fourth no with weak covered advantage', 'fourth no with weak covered disadvantage',
                            'fourth no without strong vulnerable advantage','fourth no without strong vulnerable disadvantage',
                            'fourth no without strong covered advantage', 'fourth no without strong covered disadvantage',
                            'fourth no without weak vulnerable advantage', 'fourth no without weak vulnerable disadvantage',
                            'fourth no without weak covered advantage', 'fourth no without weak covered disadvantage',
                            ]

        self.state_space_length = len(self.states_list)
        self.action_space_yes = ['low_card', 'mid_card', 'high_card']
        self.action_space_no = ['queen','strong','vulnerable', 'advantage']
        self.action_space_first = ['queen low', 'queen mid', 'queen high',
                                   'storng low', 'strong mid', 'strong high',
                                   'vulnerable low', 'vulnerable mid', 'vulnerable high',
                                   'advantage low', 'advantage mid', 'advantage high']




        self.Q_table = self.read_Q_table()
        #print('Q table check: ',self.Q_table)

    def cards_played(self, cards, index_my_card):
        cards_to_be_removed = self.extract_cards(cards)
        self.remove_cards(cards_to_be_removed)

    def extract_cards(self, cards):
        returned_card = []
        for i in range(len(cards)):
            returned_card.append(cards[i][1])
        return returned_card

    def make_copy(self, temp):
        # self.cards_left = temp.copy()
        # print('######################### make copy ##########################')
        # print('temp: ', temp)
        if type(temp[0]) == list:
            temp = []
        # print('temp: ', temp)
        # print(len(self.players_cards),' players cards: ',self.players_cards)

        for i in range(len(self.players_cards)):
            self.players_cards[i] = temp.copy()
        # print(len(self.players_cards), ' players cards: ', self.players_cards)
        return temp.copy()

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
            if i in self.queens:
                index = self.queens.index(i)
                self.queens.remove(i)
                self.strong.pop(index)
            if len(self.advantages)>0:
                for j in range(len(self.advantages)):
                    if len(self.advantages[j]) >0 and i[0] == self.advantages[j][0][0]:
                        if i in self.advantages[j]:
                            self.advantages[j].remove(i)
                            if len(self.advantages[j]) == 0:
                                self.advantages.pop(j)
                            break




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
        self.queens.clear()
        self.have_queen()
        for i in range(len(self.queens)):
            self.strong_queen(self.queens[i])
            #print('iii')
            # print(self.queens[i],' ',self.strong[i])
        self.advantages.clear()
        self.have_advantages()

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
        if self.trained:
            # print('your cards: ', self.hand)
            if len(cards_played) > 0:

                allowed_suit = cards_played[0][1][0]
                allowed, match = self.allowed_cards(allowed_suit, self.hand)
                '''
                print('^^^^^^^^^^^^^^^^^^^^ AI options ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                print('      your hand     ','        allowed cards ')
                for i in range(len(self.hand)):
                    if i < len(allowed):
                        print(i + 1, ': ', self.hand[i],'   ',i + 1, ': ', allowed[i])
                    else:
                        print(i + 1, ': ', self.hand[i])
                print('^^^^^^^^^^^^^^^^^^^^ AI decision ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
'''
                card = self.Q_table_decision(cards_played, allowed, match)
                print('allowed: ',allowed)
                #print('^^^^^^^^^^^^^^^^^^^^ end q decision ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                #print('trained card: ', card)
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
        else:
            if len(cards_played) > 0:
                allowed_cards, match = self.allowed_cards(cards_played[0][1][0], self.hand)
                action = random.randrange(3)
                if match:
                    if self.contains_queen(cards_played):
                        action = 0
                    else:
                        action = self.valid_action_queens(cards_played[0][1][0],cards_played)
                    card = self.perform_action(cards_played.copy(), allowed_cards, (action, -1), match)
                    return self.played_card(card)

                else:
                    queen = random.randrange(2) == 1
                    if queen and len(self.queens) > 0:
                        #print('hello queens: ', self.queens)
                        card = self.play_queen()
                    advantage = random.randrange(2) == 1
                    if advantage and len(self.advantages) > 0:
                        #print('hello advantage: ', self.advantages)
                        card = self.play_advantage()
                    else:
                        action = random.randrange(3)
                        card = self.perform_action(cards_played.copy(), self.hand, (action,-1), False)
                    return self.played_card(card)

            else:
                action = [random.randrange(3), random.randrange(3)]
                card = self.perform_action(cards_played.copy(), self.hand, action, False)
                return self.played_card(card)

    # need to check why ai players do not play the max card when they play a different suit

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

    def valid_action_queens(self,suit,cards_played):
        counter = 0
        if len(cards_played)==3:
            return 2
        for i in cards_played:
            if i[1][0]== suit:
                counter+=1
        if len(self.suits_left(suit))-counter<6:
            return 0
        return 1

    def contains_queen(self,cards_played):
        for i in cards_played:
            if i[1][1] == 'q':
                return True
        return False


    def have_queen(self):
        #print('check for queen: ',self.hand)

        for i in self.hand:
            if i[1] == 'q':
                self.queens.append(i)
        #print(self.queens)

    def play_queen(self):

        for i in range(1,len(self.strong)):
            if not self.strong[i]:
                return self.queens[i]
        return self.queens[0]

    def play_advantage(self):
        lenght = len(self.advantages[0])
        card = self.advantages[0][-1]
        for i in range(1,len(self.advantages)):
            if len(self.advantages[i])<lenght and len(self.advantages[i])>0:
                lenght = len(self.advantages[i])
                card = self.advantages[i][-1]
        return card

    def have_advantages(self):
        suits = self.extract_suits(self.hand)
        for i in self.suits:
            if type(suits.get(i)) == list:
                if len(suits.get(i)) <3:
                    self.advantages.append(suits.get(i))

    def update_score(self, trick,game):

        trick_score = 0
        for i in trick:
            #print('rank: ', i[1][1])
            if i[1][1] == 'q':
                trick_score += 25
        self.subscore -= trick_score
        self.score -= trick_score


    def create_Q_table(self):

        table = []
        '''
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
            '''
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
            min = 3
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

    def pick_queen(self,cards):
        for i in cards:
            if i[1] == 'q':
                return i

    def remove_suit(self,cards,suit):
        i = 0
        print('cars removed: ', cards)
        while i <len(cards):
            if cards[i][0] == suit:
                cards.pop(i)
                i-=1
            i+=1
        print('cars removed: ',cards)




    def suit_type(self, suits_dic, word, allowed_cards,match):

        #print('suits dic: ',suits_dic)
        print('word: ',word)
        #print('allowed cards: ',allowed_cards)
        if word == 'queen':
            if len(self.queens)>0:
                return self.queens[0]
            else:
                return False

        elif word == 'vulnerable':
            for i in self.suits:
                # print('suits dic check: ',suits_dic)
                #print('kkkk: ',suits_dic.get(i) != None,not suits_dic.get(i),((i,'q') not in self.queens))
                if suits_dic.get(i) != None and not suits_dic.get(i) and ((i,'q') not in self.queens):
                    return self.extract_suits(allowed_cards).get(i)
            return False

        # print('** suits count ** : ', suits_count)
        if word == 'strong':
            for i in self.suits:
                # print('suits dic check: ',suits_dic)
                #print('kkkk: ',suits_dic.get(i) != None,not suits_dic.get(i),((i,'q') not in self.queens))
                if suits_dic.get(i) != None and suits_dic.get(i) and ((i,'q') not in self.queens):
                    return self.extract_suits(allowed_cards).get(i)
            return False

        elif word == 'advantage':
            print('hand advantage: ',self.hand)
            have_advantage, suit = self.decide_advantage()
            print('suit: ',suit)
            if have_advantage:
                return suit
            else:
                return False

    #['queen', 'strong', 'vulnerable', 'advantage']

    def play_good_card(self,allowed_cards):
        #print('check please')
        for i in allowed_cards:
            if not self.free_suit(i[0]):
                return i
        #print('you only have free suit')
        return allowed_cards[0]


    def perform_action_first(self, allowed_cards,actions,suits_dic):

        if len(actions) == 0:
            return self.play_good_card(allowed_cards)
        print('actions: ',actions)
        action = actions[0]
        number_of_type_action = int((action) / 3)
        #print('number of type action check: ', number_of_type_action)
        number_of_type_action = self.action_space_no[number_of_type_action]
        #print('type word: ',number_of_type_action)
        suit = self.suit_type(suits_dic,number_of_type_action,allowed_cards.copy(),True)
        #print('check suit: ',suit)
        if type(suit) != list:
            actions.pop(0)
            return self.perform_action_first(allowed_cards,actions,suits_dic)
        #print('type of card: ',action%3)
        card = self.perform_action([],suit,action%3,True)
        #print('card returned: ',card)
        return card







    def perform_action(self, cards_played, allowed_cards, action, match):
        card_obj = cards()
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
                if type(action) == tuple:
                    card = self.pick_queen(allowed_cards)
                    if card != None:
                        return card
                action = 2
            #print('cards played: ',cards_played)
            #print('allowed: ',allowed_cards)
            #print('action:       ',action,'   match: ',match)
        elif type(action) == tuple:
            action = action[0]
            if action == 1:
                #print('check here',allowed_cards)
                for i in range(1,len(allowed_cards)):
                    if card_obj.get_rank(allowed_cards[-1][1])>10:
                        allowed_cards.pop(-1)
                    else:
                        break
                action = 2



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

    def decide_queen(self,suits_dic):
        #print('queens: ',self.queens)
        #print('suits dic: ',suits_dic)
        length = len(suits_dic.get(self.queens[0][0]))
        strong = self.strong[0]
        queen = self.queens[0]
        if not strong:
            return self.queens[0]
        for i in range(1,len(self.queens)):
            if self.strong[i] != strong:
                return self.queens[i]
            elif len(suits_dic.get(self.queens[i][0]))<length:
                length = len(suits_dic.get(self.queens[i][0]))
                queen = self.queens[i]
        return queen

    def decide_card(self,suits_to_decide,action):
        #print('suits to decide: ',suits_to_decide)
        suit = suits_to_decide[0]
        length = len(suits_to_decide[0])
        for i in range(1,len(suits_to_decide)):
            if len(suits_to_decide[i])<length and len(suits_to_decide[i])>0:
                #print('suit to decide loop: ',suits_to_decide[i],'  length: ',length)
                suit = suits_to_decide[i]
                length = len(suits_to_decide[i])

        if (suit[0][0],'q') in suit and action == 2:
            #print('returned card: ', suit[-1])
            return (suit[0][0],'q')

        if action == 0:
            #print('returned card: ', self.min_card(suit,True,0))
            return self.min_card(suit,True,0)
        if action == 1:
            #print('returned card: ', self.mid_card(suit,True,0))
            return self.mid_card(suit,True,0)
        if action == 2:
            #print('returned card: ',self.max_card(suit))
            return self.max_card(suit)

    def perform_action_no(self, allowed_cards,actions,suits_dic):
        if len(actions) == 0:
            return self.play_good_card(allowed_cards)
        #print('actions: ',actions)
        action = actions[0]
        #print('number of type action check: ', number_of_type_action)
        number_of_type_action = self.action_space_no[action]
        #print('type word: ',number_of_type_action)
        suit = self.suit_type(suits_dic,number_of_type_action,allowed_cards.copy(),False)
        #print('check suit: ',suit)
        if type(suit) != list:
            actions.pop(0)
            return self.perform_action_no(allowed_cards,actions,suits_dic)
        #print('type of card: ',action%3)
        card = self.perform_action([],suit,2,True)
        #print('card returned: ',card)
        return card


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
        suit = my_cards[0][0]
        number_of_my_cards = len(my_cards)
        temp = []
        limit = 0
        #print(self.players_cards_expected)
        for i in self.players_cards_expected:
            player_suit = self.extract_suits(i).get(suit)
            # print('type of suit: ',player_suit)
            if type(player_suit) == list:
                temp.append(len(player_suit))
                if temp[-1] > 0:
                    limit += 1

        number_of_players_cards = min(temp)
        temp = [number_of_my_cards, number_of_players_cards]
        number_of_cards_to_check = min(temp)
        '''
        print('temp: ',temp)
        print('number: ',number_of_cards_to_check)
        print('players cards expected: ',number_of_players_cards)
        print('my cards: ', my_cards)
'''
        card_obj = cards()
        strong = True

        cards_left = self.suits_left(suit)
        self.extract_suits(my_cards).get(suit)
        '''
        print('cards to check: ',my_cards)
        print('cards to compare: ',cards_left)
        print('cards checke: ',number_of_cards_to_check)
        print('limit: ',limit)
        '''
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
        #print('strong: ',strong)

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

    def evaluate_queen(self,suit,my_cards,rank):
        #print('####### evalutae queen ##########')
        suit_left = self.suits_left(suit)
        number_of_my_cards = len(my_cards)
        if number_of_my_cards <3:
            return my_cards[0][0], True,2
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
        number_of_cards_to_check = len(my_cards)
        '''
        print('temp: ',temp)
        print('number: ',number_of_cards_to_check)
        print('players cards expected: ',number_of_players_cards)
        print('my cards: ', my_cards)
'''
        card_obj = cards()
        strong = True

        cards_left = self.suits_left(suit)
        self.extract_suits(my_cards).get(suit)
        '''
        print('cards to check: ',my_cards)
        print('cards to compare: ',cards_left)
        print('cards checke: ',number_of_cards_to_check)
        print('limit: ',limit)
'''
        found = False

        counter = 0
        stop = True
        for i in range(number_of_cards_to_check):
            for j in range(limit):
                if i * limit + j < len(cards_left):
                    counter += 1
                    rank_to_compare = card_obj.get_rank(cards_left[i * limit + j][1])
                    #print('rank to compare: ',rank_to_compare)
                    if rank_to_compare > rank:
                        found = True
                        break
                    if (counter == number_of_players_cards  or counter == 6) and stop:
                        limit -=1
                        stop = False
                else:
                    found = True
                    break
        if not found:
            strong = found
        #print('strong: ',strong)
        if not stop:
            limit +=1

        return my_cards[0][0], strong,limit

    def strong_queen(self,queen):
        #print('strong queen check')
        suit = queen[0]
        if self.free_suit(suit):
            #print('free ',suit)
            return False
        suit_card = self.extract_suits(self.hand).get(suit)
        #print(type(suit),' suit: ',suit)
        if type(suit_card)==list:
            a, strong ,li= (self.evaluate_queen(suit,suit_card,11))
            #print(strong)
            self.strong.append(strong)
        else:
            self.strong.append([])
        #self.extract_suits()

    def queen_played(self,suit):
        suit_left = self.suits_left(suit)
        return not (suit,'q') in suit_left

    def suits_evaluation_queen(self):
        card_obj = cards()
        evaluation = {}
        #print(self.queens)
        #print(self.strong)
        #print('queen eval: ')
        my_cards = self.extract_suits(self.hand)
        vulnerable = False
        eval = True
        #print('my cardss: ',my_cards)
        for i in self.suits:
            #print('evaluation: ',evaluation)
            #print()
            if not self.free_suit(i):
                suit_card = my_cards.get(i)
                #print('suit: ',suit_card)
                if type(suit_card) == list:
                    eval = True
                    rank = card_obj.get_rank(suit_card[-1][1])
                    #print('rank: ',rank)
                    limit = 3

                    if rank >10:
                        a, eval, limit = self.evaluate_queen(suit_card[0][0], suit_card, rank)
                       # print('eval: ',eval)
                    #print('lowest: ', (self.suits_left(i)), '  my lowest: ',my_cards.get(i)[0])
                    if not eval or ((limit-1<len(self.suits_left(i)))and(card_obj.get_rank(self.suits_left(i)[limit-1][1])<card_obj.get_rank(my_cards.get(i)[0][1]))):
                        eval = False

                    if not eval:
                        vulnerable = True
                    evaluation[i]=(eval)
        if len(evaluation)==0:
            evaluation['free']=my_cards
            #print('hey')
        #print('eval: ',evaluation)
        return vulnerable,evaluation

    def suits_evaluation(self):
        evaluation = {}
        my_cards = self.extract_suits(self.hand)
        vulnerable = False
        #print('my cardss: ', my_cards)
        for i in self.suits:
            if not self.free_suit(i):
                suit = my_cards.get(i)
                #print('suit: ', suit)
                if type(suit) == list:
                    a, eval = self.evaluate_suit(suit)
                    if not eval:
                        vulnerable = True
                    evaluation[i] = (eval)
        if len(evaluation) == 0:
            evaluation['free'] = my_cards
            # print('hey')
        #print('eval: ',evaluation)
        return vulnerable, evaluation

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
        if suit_left-cards_removed<6:
            return True
        return (len(self.suits_left(suit))-cards_removed)-suit_left >3

    def possible_queen(self,cards_played):
        print('possible queen')
        print(cards_played)
        cards = self.extract_cards(cards_played)
        #print(cards)
        if  (cards_played[0][1][0],'q') in self.hand:
            print('I have the queen')
            return 2
        for i in cards:
            if i[1]=='q':
                print('pois')
                return 0
        players_left = 4-(len(cards_played)+1)
        print('players left: ',players_left)
        if players_left == 0:
            print('safe')
            return 2
        for i in range(players_left):
            if (cards_played[0][1][0],'q') in self.players_cards_expected[i]:
                return 1
            if self.potential_different(cards_played[0][1][0],self.players_cards_expected[i],cards_played):
                print('poss')
                return 1

        print('safe')
        return 2


    def decide_advantage(self):
        if len(self.advantages)>0:
            for i in self.advantages:
                if len(i)>0:
                    return True, i
        return False, []



    def current_state(self, cards_played, allowed_cards, match):

        #print('my cards state',self.hand)
        vulnerable, suits_dic = self.suits_evaluation_queen()
        advantage, cards = self.decide_advantage()
        #print('cards played: ', cards_played)
        #print(len(allowed_cards), 'allwed cards: ', allowed_cards)
        #print('vul: ',vulnerable)
        #print('suit dic: ',suits_dic)
        #print('cards: ',cards)
        strong = False not in self.strong
        #print('strong: ',strong,'     stronglist: ',self.strong)
        queen = True
        if len(self.queens) == 0:
            queen = False
            strong, suits_dic = self.suits_evaluation()

        if len(cards_played) == 0:

            #print('que: ',queen,'  str: ',strong,'  vul: ',vulnerable,' advantage: ',advantage)
            return self.state_space.get(1).get(queen).get(strong).get(vulnerable).get(advantage),suits_dic

        if match:
            #print('mat: ', match, '  str: ', self.possible_queen(cards_played))
            return self.state_space.get(len(cards_played) + 1).get(match).get(self.possible_queen(cards_played)),suits_dic

        #print('mat: ', match, '  str: ', strong, '  vul: ', vulnerable,' advantage: ',advantage)
        return self.state_space.get(len(cards_played) + 1).get(match).get(queen).get(strong).get(vulnerable).get(advantage),suits_dic

    # checked

    def update_Q_table(self, state, action, reward):
        #print('state: ', state)
        #print('action', action)
        #print('Q table: ', self.Q_table)
        #print('state before: ', self.Q_table[self.states_list.index(state)][action])
        if self.Q_table[self.states_list.index(state)][action] == 0:
            self.Q_table[self.states_list.index(state)][action] = reward
        else:
            self.Q_table[self.states_list.index(state)][action] += reward - self.Q_table[self.states_list.index(state)][
                action]
        #print('updated state: ', self.Q_table[self.states_list.index(state)][action])

    # ,cards_expected,state_of_the_game
    def moves_ahead(self):
        # if self.temp:
        # self.temp = False
        # return 2
        if len(self.hand) > 2:
            return 2
        return 1  # len(self.hand)





    def best_action(self,valid_actions,possible_actions):
        #print('valid acti: ',valid_actions)
        #print('poss acti: ',possible_actions)

        for i in range(len(possible_actions)):
            #print('max: ',max(possible_actions))
            #print('possible best: ',possible_actions.index(max(possible_actions)))
            best_action = possible_actions.index(max(possible_actions))
            #print('best to check: ',best_action)
            if best_action in valid_actions:
                #print('best: ',best_action)
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


    def Q_table_decision(self, cards_played, allowed_cards, match):
        state,suits_eval = self.current_state(cards_played, allowed_cards, match)

        print('state: ',state)
        #print('suits eval: ',suits_eval)
        if state[0:5] == 'first':
            # print('yes it is first: ',action)
            actions = self.best_actions_indexes(self.Q_table[self.states_list.index(state)])
            return self.perform_action_first(self.hand, actions, suits_eval)

        if not match:
            actions = self.best_actions_indexes(self.Q_table[self.states_list.index(state)])
            return self.perform_action_first(self.hand, actions, suits_eval)

        else:
            actions, have_choice = self.valid_actions(allowed_cards, self.highest_card_played(cards_played))
            # print('actions: ', actions)

            if have_choice:
                # print(len(self.Q_table),'Q table: ',self.Q_table)
                # print('check actions: ',self.Q_table[self.states_list.index(state)])
                action = self.best_action(actions, self.Q_table[self.states_list.index(state)].copy())
                # print('best action: ',action)
            else:
                action = 2
                # print('forced action')
            card_obj = cards()
            temp = allowed_cards.copy()
            if card_obj.get_rank('q') < self.highest_card_played(cards_played) and (allowed_cards[0][0], 'q') in allowed_cards:
                print('got rid of queen')
                return (allowed_cards[0][0],'q')
            elif len(allowed_cards)>1 and (allowed_cards[0][0], 'q') in allowed_cards:
                print('avoided playing queen')
                temp.remove((allowed_cards[0][0], 'q'))
            return self.perform_action(cards_played, temp, action, match)






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
        f = open("queens table.txt", "r")
        content = self.preprocess(f.readlines())
        # print('finished preprocessing')
        # print('after',content)
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