from cards import cards
import copy
import random


class trained_player_jack:

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
        self.lowest_cards = []
        self.lowest_suits = []
        self.options = []
        self.strong = []
        self.advantages = []
        self.finished = False

        '''
        self.state_space = {1:{1:{5:'worst high',6:'worst block',11:'worst high block'},
                               2:{}}
                            
                            
                            
'''
        #block at the end
        self.states_list = ['worst high',#'worst block','worst high block',

                            'worst bad','worst bad high ', #'worst bad block','worst bad high block',
                            'worst bad good','worst bad good high', #'worst bad good block', 'worst bad good high block',
                            'worst bad best', 'worst bad best high', #'worst bad best block','worst bad best high block',
                            'worst bad good best', 'worst bad good best high',

                            'worst good', 'worst good high', #'worst good block', 'worst good high block',
                            'worst good best', 'worst good best high',

                            'worst best', 'worst best high',
                             ####

                            'bad high',#'bad block','bad high block',
                            'bad good', 'bad good high', #'bad good block','bad good high block',
                            'bad best', 'bad best high', #'bad best block','bad best high block',
                            'bad good best', 'bad good best high',

                            ###

                            'good high', 'worst good block', 'worst good high block',
                            'good best', 'good best high',

                            ###
                            'best high']

                            ###



        self.state_space_length = len(self.states_list)
        self.action_space_yes = ['low_card', 'mid_card', 'high_card']
        self.action_space_no = ['queen','strong','vulnerable', 'advantage']
        self.action_space_first = ['queen low', 'queen mid', 'queen high',
                                   'storng low', 'strong mid', 'strong high',
                                   'vulnerable low', 'vulnerable mid', 'vulnerable high',
                                   'advantage low', 'advantage mid', 'advantage high']

        if self.name == 'Motaz':
            self.Q_table = self.create_Q_table()
        self.random_action = 90
        self.alpha = 0
        self.discount = 0

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

        print('cards:      ', cards)
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

        self.options = ['worst', 'bad', 'good', 'best']
        self.lowest_cards.clear()
        self.sorted_lowest(self.suits.copy())
        self.finished = False

        # checked

    def getKey(self, item):
        card_obj = cards()
        return card_obj.get_rank(item[1])

    def allowed_cards(self, jack, hand):

        playing = True
        #print('hand: ',hand)
        #print('jack: ',jack)
        card_obj = cards()
        allowed_up = []
        allowed_down = []

        for i in range(len(jack[1])):
            #print('type down : ', type(jack[1][i]))
            if type(jack[1][i]) != tuple:
                rank_allowed = 10
            else:
                rank_allowed = card_obj.get_rank(jack[1][i][1])-1
            #print('rank allowed: ',rank_allowed,'   card: ',(jack[1][i][0],card_obj.get_rank_name(rank_allowed)))
            if rank_allowed != 0 and (self.suits[i],card_obj.get_rank_name(rank_allowed)) in hand:
                allowed_down.append((self.suits[i],card_obj.get_rank_name(rank_allowed)))
            #print('base rank: ',rank_allowed)


            #print('type up : ', type(jack[0][i]))
            if type(jack[0][i]) != tuple:
                if rank_allowed == 10:
                    rank_allowed = -1
                else:
                    rank_allowed = 11
            else:
                rank_allowed = card_obj.get_rank(jack[0][i][1]) + 1

            if rank_allowed != 14 and rank_allowed != -1 and (self.suits[i], card_obj.get_rank_name(rank_allowed)) in hand:
                #print('check me:',card_obj.get_rank_name(rank_allowed))
                #print('allowed rank: ',rank_allowed)
                allowed_up.append((self.suits[i], card_obj.get_rank_name(rank_allowed)))



        if len(allowed_down) == 0 and len(allowed_up) == 0:
            playing = False
        print('allowed up: ',allowed_up)
        print('allowed down: ',allowed_down)
        print('playing: ',playing)

        return allowed_up,allowed_down, playing

    def receive_cards(self, cards):
        self.hand.clear()

        while len(cards) > 0 and len(self.hand) < 13:
            self.hand.append(cards.pop())

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

        print(self.name, 'cards: ', self.hand)
        # print(len(cards), ' cards: ', cards)
        self.reset_cards_left()
        # checked

    def played_card(self, card):
        if card in self.hand:
            self.hand.remove(card)

        return card

        '''
        for i in range(len(self.hand)):
            if card == self.hand[i]:
                return self.hand.pop(i)
        '''
    # need some adjustments
    def get_score(self):
        self.subscore = 0
        return self.score

    # need some adjustments
    def get_subscore(self):
        return self.subscore

    # need some adjustments
    def play(self, jack, play_order,score_of_winner):
        just_finished = False
        if self.hand == 0:
            return just_finished,'finished'

        self.players_order = play_order
        # print(self.name,'cards: ',self.hand,'  hearts left: ',self.hearts_left)
        print('number of my cards: ',len(self.hand))
        if self.trained:
            # print('your cards: ', self.hand)

            print('------------------------')
            #allowed_suit = cards_played[0][1][0]
            allowed_up, allowed_down,playing = self.allowed_cards(jack, self.hand)
            if playing:
                print('^^^^^^^^^^^^^^^^^^^^ AI options ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                for i in range(len(allowed_up)+len(allowed_down)):
                    if i <len(allowed_up):
                        print(i + 1, ': ', allowed_up[i])

                    else:
                        print(i + 1, ': ', allowed_down[i-len(allowed_up)])



                if i == 0:
                    if len(allowed_up)>0:
                        card = allowed_up[0]
                    else:
                        card = allowed_down[0]
                else:
                    print('^^^^^^^^^^^^^^^^^^^^ AI decision ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                    print(i)
                    card = self.Q_table_decision(jack, allowed_up,allowed_down)
                    print('^^^^^^^^^^^^^^^^^^^^ end q decision ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            else:
                card = 'pass'
            print('trained card: ', card)
            self.played_card(card)
            if len(self.hand) == 0 and not self.finished:
                self.update_score(score_of_winner)
                self.finished = True
                just_finished = True
            return just_finished,card


        else:
            '''
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
                        print('hello queens: ', self.queens)
                        card = self.play_queen()
                    advantage = random.randrange(2) == 1
                    if advantage and len(self.advantages) > 0:
                        print('hello advantage: ', self.advantages)
                        card = self.play_advantage()
                    else:
                        action = random.randrange(3)
                        card = self.perform_action(cards_played.copy(), self.hand, (action,-1), False)
                    return self.played_card(card)

            else:
                action = [random.randrange(3), random.randrange(3)]
                card = self.perform_action(cards_played.copy(), self.hand, action, False)
            '''
            allowed_up, allowed_down, playing = self.allowed_cards(jack, self.hand)
            if len(allowed_up)!=0:
                if len(self.hand) == 1 and not self.finished:
                    self.update_score(score_of_winner)
                    self.finished = True
                    just_finished = True

                return just_finished,self.played_card(allowed_up[random.randrange(len(allowed_up))])
            elif len(allowed_down)!=0:
                if len(self.hand) == 1 and not self.finished:
                    self.update_score(score_of_winner)
                    self.finished = True
                    just_finished = True
                
                return just_finished,self.played_card(allowed_down[random.randrange(len(allowed_down))])

            return False,'pass'


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

    def update_score(self, score):

        self.subscore += score
        self.score += score
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
        print(max)
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

        print('remove player cards')
        new_cards = cards()
        index_player = 0
        for i in range(len(self.players)):
            if self.players[i] == player:
                index_player = i - 1
                break
        card = copy.deepcopy(self.players_cards_expected[index_player])
        for i in trick:
            if i[1] in card:
                print('to be removed: ',i[1])
                print('cards to remove from: ',card)
                card.remove(i[1])
                print('cards after remove: ', card)

        print(player,' ',highest_rank,' ',player_rank,' ',suit)
        print(len(self.hand),len(card),card)
        if match:
            for i in range(highest_rank - player_rank - 1):
                if (suit, new_cards.get_rank_name(player_rank + i + 1)) in card:
                    card.remove((suit, new_cards.get_rank_name(player_rank + i + 1)))
        else:
            for i in range(14 - player_rank):
                if (suit, new_cards.get_rank_name(player_rank + i)) in card:
                    card.remove((suit, new_cards.get_rank_name(player_rank + i)))

            print(len(card), card)
            counter = 0
            for i in range(len(card)):
                print('len: ', len(card), '  suit: ', base_suit, '  i: ', i)
                print(card)
                if card[i - counter][0] == base_suit:
                    card.pop(i - counter)
                    counter += 1

        print(len(self.hand),len(card),card)
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
        print('winnnnnnner: ',trick_winner)
        for i in range(len(previous_trick)):
            if safe:
                rank = 14
            else:
                rank = self.highest_card_played(previous_trick[:i + 1])
            print('rank: ',rank)
            if not previous_trick[i][0] == 'Motaz':
                print('analyse trick')
                print('player: ',previous_trick[i][0], ' ',previous_trick[i][1])
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
        print('ai1 cards expected: ', len(self.players_cards_expected[0]))
        print('ai2 cards expected: ', len(self.players_cards_expected[1]))
        print('ai3 cards expected: ', len(self.players_cards_expected[2]))
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

    # require an alogritm to deal with the case of only one card left in a suit and you have the rest line 585
    def perform_action_first(self, suits_eval, allowed_cards):
        print('allowed cards fir: ', allowed_cards)
        subaction = random.randrange(3)
        update,action,card = self.perform_action_no(allowed_cards,suits_eval,subaction)
        print('card: ',card)
        print('subaction: ',subaction)
        if update:
            print('action decided: ',self.action_space_first[action*3+subaction])

        return update,action*3+subaction,card




        # checked might require considering the case of performing different action than desired

    def perform_action(self, allowed_up, allowed_down, actions):
        action_index = random.randrange(len(actions))
        action = actions[action_index]
        if action == 'high':
            return action_index, allowed_up[0]
        suit = self.lowest_suits[self.options.index(action)]
        for i in allowed_down:
            if i[0] == suit:
                return action_index,i


    def perform_action_no(self, allowed_cards,suits_eval,action):
        print('allowed cards no: ',allowed_cards)
        print('suits eval: ',suits_eval)
        if suits_eval.get('free')!= None:
            return False,-1,allowed_cards[0]
        actions = []
        cards_to_play= []
        suits_dic = self.extract_suits(allowed_cards)
        vulnerabel_suits = []
        strong_suits = []
        if len(self.queens)>0:
            cards_to_play.append(self.decide_queen(suits_dic))
            #print('returned queen: ',cards_to_play[-1])
            actions.append(0)
        else:
            cards_to_play.append([])

        #print('cards to play: ',cards_to_play)
        for i in self.suits:
            if suits_eval.get(i) == False:
                vulnerabel_suits.append(suits_dic.get(i))
            if suits_eval.get(i) == True:
                vulnerabel_suits.append(suits_dic.get(i))
        if len(strong_suits)>0:
            cards_to_play.append(self.decide_card(strong_suits,action))
            actions.append(1)
        else:
            cards_to_play.append([])
        #print('cards to play: ', cards_to_play)
        if len(vulnerabel_suits)>0:
            cards_to_play.append(self.decide_card(vulnerabel_suits,action))
            actions.append(2)
        else:
            cards_to_play.append([])
        if len(self.advantages)>0:
            advantage = False
            for i in self.advantages:
                if len(i) > 0:
                    advantage = True
                    break
            if advantage:
                actions.append(3)
                cards_to_play.append(self.decide_card(self.advantages,action))
            else:
                cards_to_play.append([])
        else:
            cards_to_play.append([])


        #print('cards to play: ', cards_to_play)
        action = actions[random.randrange(len(actions))]
        #print('actions: ', actions)
        #print('len action :',len(actions))
        print('action: ',action)
        print('to play: ',cards_to_play)
        print('decided action: ',self.action_space_no[action])
        print('played: ',cards_to_play[action])

        return len(actions)==1,action,cards_to_play[action]


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






    def check_block(self,card):
        card_obj = cards()
        print('hand to check block: ',self.hand)
        print((card[0], card_obj.get_rank_name(card_obj.get_rank(card[1]) - 1)))
        print((card[0], card_obj.get_rank_name(card_obj.get_rank(card[1]) - 1)) in self.hand)
        return (card[0],card_obj.get_rank_name(card_obj.get_rank(card[1]) - 1)) in self.hand

    def block_to_the_end(self,card):
        card_obj = cards()
        if card_obj.get_rank(card[1]) == 1:
            return True
        if self.check_block(card):
            return self.block_to_the_end((card[0],card_obj.get_rank_name(card_obj.get_rank(card[1]) - 1)))
        return False

    def update_options(self):
        length = 4 - len(self.lowest_suits)
        print('$$ lowest suits: ',self.lowest_suits)
        for i in range(length):
            self.options.pop(-2)


    def available_options(self,allowed_down):
        print()
        print(self.hand)
        print('**** avaliable options ********** ')
        print('all options: ',self.options)
        print('lowest suits: ',self.lowest_suits)
        print('allowed down: ',allowed_down)
        options = []
        for i in allowed_down:
            options.append(self.lowest_suits.index(i[0]))
        options = sorted(options)
        print('index options: ',options)
        for i in range(len(options)):
            options[i] = self.options[options[i]]
        '''
        for i in allowed_down:
            options.append(self.options[self.lowest_suits.index(i[0])])
'''
        print('allowed options: ',options)
        return options




    #check if two suits have the same low_card
    def sorted_lowest(self,suits_names):
        card_obj = cards()
        print()
        print('my hand: ',self.hand)

        suits = self.extract_suits(self.hand)
        lowest_cards = []
        for i in suits_names:
            if suits.get(i)!= None and card_obj.get_rank(suits.get(i)[0][1])< 11:
                lowest_cards.append(suits.get(i)[0])
        lowest_cards = sorted(lowest_cards, key=self.getKey)
        print('lowest cards : ',lowest_cards)
        self.lowest_cards = lowest_cards
        self.lowest_suits = self.lowest_cards.copy()
        for i in range(len(self.lowest_cards)):
            self.lowest_suits[i] = self.lowest_cards[i][0]
        print('lowest suits : ', self.lowest_suits)
        print()
        self.update_options()

    def current_state(self, jack, allowed_up,allowed_down):

        print('jack: ',jack[0])
        print('jack: ',jack[1])
        print('my cards state',self.hand)
        print('allowed up: ', allowed_up)
        print('allowed down: ', allowed_down)
        high_card = len(allowed_up)>0
        print('have high card: ',high_card)
        state = ''
        options = self.available_options(allowed_down)
        print('state: ',state)
        print('options: ',options)
        for i in options:
            print('i: ',i)
            state += i+' '

        if high_card:
            state += 'high'
        else:
            state = state[:len(state)-1]
    
        return state

    # checked

    def update_Q_table(self, state, action, reward):
        print('state: ', state)
        print('action', action)
        print('Q table: ', self.Q_table)
        print('state before: ', self.Q_table[self.states_list.index(state)][action])
        if self.Q_table[self.states_list.index(state)][action] == 0:
            self.Q_table[self.states_list.index(state)][action] = reward
        else:
            self.Q_table[self.states_list.index(state)][action] += reward - self.Q_table[self.states_list.index(state)][
                action]
        print('updated state: ', self.Q_table[self.states_list.index(state)][action])

    # ,cards_expected,state_of_the_game
    def moves_ahead(self):
        # if self.temp:
        # self.temp = False
        # return 2
        if len(self.hand) > 2:
            return 2
        return 1  # len(self.hand)

    def extract_actions(self,state):
        #print('state to extract: ',state)
        actions = []

        while ' ' in state :
            actions.append(state[:state.index(' ')])
            state = state[state.index(' ')+1:]


        actions.append(state)
        print('extracted actions: ',actions)
        return actions

    # check if I have a choice or I am forced to play a card
    def Q_table_decision(self, jack, allowed_up,allowed_down):

        state = self.current_state(jack, allowed_up,allowed_down)
        if (random.random() < self.random_action) or True:
            print('state: ',state)
            actions = self.extract_actions(state)
            action, card = self.perform_action(allowed_up,allowed_down,actions)
            print('check card: ',card)
            self.random_action -= 0.1
            print('action: ', action)

            '''
                if update_Qtable and self.temp:
                    self.players_cards_minimax = copy.deepcopy(self.players_cards_expected)
                    for i in self.players_cards_minimax:
                        print(i)
                    my_hand = self.hand.copy()

                    reward = self.Q_reward(self.moves_ahead(), cards_played + [(self.name, card)], False,
                                           self.players_order, copy.deepcopy(self.players_cards_minimax), my_hand)
                    print('reward: ', reward)
                    # self.update_Q_table(state, action, reward)
'''
            return card



        #else:
            # choose the max reward
            #action = state.index(max(state))
            #card = self.perform_action(cards_played, allowed_cards, action, match)
            #print('best action: ', action)
            #return card


    def add_trick(self, trick, plays, card_by_card):
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

    def possible_moves(self, plays, trick, first_time):
        if len(plays) > 2:
            '''
            print()
            print('start debuging ')
            print('playes: ',plays)
            print('trick: ',trick)
            print('first time: ',first_time)
'''
        tricks = []
        temp = trick.copy()
        if type(plays[0]) == list:
            first_time = False
            for i in plays:
                tricks += self.possible_moves(i, temp.copy(), first_time)
        else:
            tricks += self.add_trick(trick, plays, first_time)
        if len(plays) > 2:
            # print('returned tricks: ',tricks)
            d = -1
        return tricks

    def possible_cards(self, play_order, player_index, players_cards):
        for i in range(len(self.players)):
            if self.players[i] == play_order[player_index]:
                return players_cards[i - 1]

    def remove_minimax_cards(self, players_cards, cards):
        if type(cards) == list:
            cards = self.extract_cards(cards)
        else:
            cards = [cards]
        for i in cards:
            for j in range(len(players_cards)):
                if i in players_cards[j]:
                    players_cards[j].remove(i)
        return players_cards

    def add_card_minimax(self, players_cards, card, play_order, player_index):
        for i in range(len(self.players)):
            if self.players[i] == play_order[player_index]:
                for j in range(len(self.players_cards_minimax)):
                    self.players_cards_minimax[j].append(card)

    def minimax(self, next_turn, my_turn, suit, play_order, players_cards, my_hand):
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

        # print(len(cards_to_play),' cards to play: ',cards_to_play)
        possible_trick = []
        possible_tricks = []
        possible_plays = []

        if next_turn == my_turn:
            my_cards, a = self.allowed_cards(suit, my_hand.copy())
            # copy_my_card = my_cards.copy()
            # print('my cards(): ',my_cards, ' my hand: ',my_hand)
            for i in range(len(my_cards)):
                possible_trick.append((play_order[my_turn], my_cards.pop(0)))

                # print('possible_trick', possible_trick)
                if next_turn == 0 and suit == 'free':
                    suit = possible_trick[-1][1][0]
                    # print('card is: ',possible_trick[-1],' and suit is: ',suit)
                possible_plays += self.minimax(next_turn + 1, my_turn, suit, play_order, players_cards, my_cards.copy())
                # print('&&&&&&&&&&&&&&&&& end subminimax &&&&&&&&&&&&&&&&&&&&&&&&&&')

                # self.cards_left = temp.copy()

                if len(possible_plays) == 0:
                    possible_tricks.append(possible_trick[0])
                else:
                    '''
                    print('possible plays: ',possible_plays)
                    print('possible tricks: ',possible_tricks)
                    print('possible trick: ', possible_trick)
'''
                    possible_tricks += self.possible_moves(possible_plays.copy(), possible_trick.copy(), True)

                possible_trick.pop(-1)
                possible_plays.clear()
        else:
            cards_to_play = self.possible_cards(play_order, next_turn, players_cards).copy()
            # print(len(cards_to_play),'cards left minimax: ',cards_to_play)
            for i in range(len(cards_to_play)):

                card = cards_to_play.pop(0)
                possible_trick.append((play_order[next_turn], card))
                # self.cards_played(cards_to_play[i],True,-1)
                if next_turn == 0 and suit == 'free':
                    if len(cards_to_play) == 0:
                        return []
                    suit = cards_to_play[i][0]

                # print('suit: ', suit)
                # print('possible_trick', possible_trick)

                temp = copy.deepcopy(players_cards)
                temp = self.remove_minimax_cards(temp, card)

                possible_plays += self.minimax(next_turn + 1, my_turn, suit, play_order, temp, my_hand)
                # self.add_card_minimax(players_cards,card)
                # print('&&&&&&&&&&&&&&&&& end subminimax &&&&&&&&&&&&&&&&&&&&&&&&&&')
                # print('possible plays: ',possible_plays)
                # cards_to_play = self.make_copy(temp.copy())

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
                    # print('&&&&&&&&&&&&&&&&& end posssible moves &&&&&&&&&&&&&&&&&&&&&&&&&&')
                # possible_tricks.append(possible_trick.copy())

                possible_trick.pop(-1)
                possible_plays.clear()
                # print('possible tricks',possible_tricks)

            # print('&&&&&&&&&&&&finished options&&&&&&&&&&&&&&&&')

        return possible_tricks.copy()

    def evaluate_trick(self, winner):
        if winner == self.name:
            return -15
        else:
            return 0

    def my_turn(self, play_order):
        for i in range(len(play_order)):
            if play_order[i] == self.name:
                return i

    # checked first iteration
    # checked minimax first iteration

    def check_trick(self, trick):
        print('trick to check: ', trick)
        temp = any(player in trick for player in self.players)
        print('temp: ', temp)
        return not temp

    def possible_trick(self, possible_trick):
        trick = []

        print('test: ', possible_trick)
        for i in range(len(possible_trick)):
            if possible_trick[i] == list:
                for j in range(len(possible_trick[i])):
                    if possible_trick[i][j] == tuple:
                        trick.append(possible_trick[i][j])
            elif possible_trick[i] == tuple:
                trick.append(possible_trick[i])
        print('returned: ', trick)
        return trick

    def play_trick(self, cards_played, play_order, players_cards, my_hand):

        print()
        print('&&&&&&&&&&&&&&&&& parameters play trick &&&&&&&&&&&&&&&&&&&&&&&&&')
        print('cards played: ', cards_played)
        print('play order: ', play_order)
        print('players cards: ', players_cards)

        suit = 'free'
        if len(cards_played) > 0:
            suit = cards_played[0][1][0]
            players_cards = self.remove_minimax_cards(players_cards, cards_played)

        print('suit: ', suit)
        print('my cards: ', my_hand)
        print(len(players_cards[0]), 'cards left to play: ', players_cards[0])
        print(len(players_cards[1]), 'cards left to play: ', players_cards[1])
        print(len(players_cards[2]), 'cards left to play: ', players_cards[2])

        possible_tricks = self.minimax(len(cards_played), self.my_turn(play_order), suit, play_order,
                                       copy.deepcopy(players_cards), my_hand.copy())
        '''
        print('&&&&&&&&&&&&&&&&& end minimax &&&&&&&&&&&&&&&&&&&&&&&&&')
        print('possibl tricks^^: ',possible_tricks)
        print('possible_tricks length: ',len(possible_tricks))
'''
        # print('cards played: minimax ', cards_played)
        tricks = []
        temp = cards_played.copy()
        '''
        print()
        print(len(players_cards[0]), 'cards left to play: ', players_cards[0])
        print(len(players_cards[1]), 'cards left to play: ', players_cards[1])
        print(len(players_cards[2]), 'cards left to play: ', players_cards[2])
        print()
        '''
        for i in range(len(possible_tricks)):
            if type(possible_tricks[i]) == list:

                for j in range(len(possible_tricks[i])):
                    # print('possibl tricks sub i : ',possible_tricks[i][j])
                    # print('before cards played: ',cards_played)
                    cards_played.append(possible_tricks[i][j])
                    # print('after cards played: ', cards_played)

            else:
                cards_played.append(possible_tricks[i])

            if len(cards_played) == 4 and self.check_trick(cards_played):
                tricks.append(cards_played.copy())
            else:

                # print('error: ',cards_played)
                cards_played = self.possible_trick(cards_played)
                if len(cards_played) == 4:
                    tricks.append(cards_played.copy())
                else:
                    a = 0
                    # print('error: ',cards_played)

            cards_played = temp.copy()

        if len(tricks) == 0:
            tricks = cards_played.copy()
        # print(len(tricks),'tricks: ', tricks)
        return tricks

    def trick_winner(self, cards_played):
        new_cards = cards()
        # print(cards_played)
        suit, rank = cards_played[0][1][0], new_cards.get_rank(cards_played[0][1][1])
        winner = 0
        for i in range(1, len(cards_played)):
            if cards_played[i][1][0] == suit and new_cards.get_rank(cards_played[i][1][1]) > rank:
                rank = new_cards.get_rank(cards_played[i][1][1])
                winner = i
        # print('winner is : ', cards_played[winner])
        return winner, cards_played[winner][0]

    def play_order(self, players, first_player):
        ordered = []
        for i in range(len(players)):
            ordered += [players[first_player % len(players)]]
            first_player += 1
        return ordered

    def set_play_order(self, players_order, cards_played):

        winner_index, winner_name = self.trick_winner(cards_played)
        players_order = self.play_order(players_order, winner_index)
        return players_order, winner_name

    def analyse_minimax(self, cards_played, trick_winner):

        # print()
        # print('trick: ', cards_played)

        # print('!!!!!!!!!!! analyse minimax !!!!!!!!!!!!!')
        # print('expected: ',self.players_cards_expected)
        copy_expected = copy.deepcopy(self.players_cards_expected)
        cards_to_be_removed = self.extract_cards(cards_played)
        # remove cards already played
        for i in cards_to_be_removed:
            if i in self.players_cards_expected[0]:
                self.players_cards_expected[0].remove(i)
            if i in self.players_cards_expected[1]:
                self.players_cards_expected[1].remove(i)
            if i in self.players_cards_expected[2]:
                self.players_cards_expected[2].remove(i)
        # remove cards based on the players chosen cards
        self.analyse_trick(cards_played, trick_winner)
        cards = copy.deepcopy(self.players_cards_expected)
        self.players_cards_expected = copy.deepcopy(copy_expected)
        # print('expected: ', self.players_cards_expected)
        # print('return: ', cards)
        return cards

    # checked

    def Q_reward(self, moves_ahead, cards_played, future_trick, play_order, players_cards, my_hand):

        future_rewards = []

        print('&&&&&&&&&&&&&&&&& parameters Q reward &&&&&&&&&&&&&&&&&&&&&&&&&')
        print('moves: ', moves_ahead)
        print('cards played: ', cards_played)

        print('future: ', future_trick)
        print('play order: ', play_order)

        if moves_ahead == 0:
            # print('finnnnnnnnnnnneshed')
            return 0
        if future_trick:
            # delete your card
            # print('trick to analyse: ', cards_played)
            # print('players card: ', players_cards)
            players_cards = copy.deepcopy(self.analyse_minimax(cards_played, play_order[0]))
            # print('players card after: ',players_cards)

            # print('play order: ', play_order)
            # print('my turn: ', self.my_turn(play_order))
            # self.cards_played(cards_played,True,-1)
            # print('players_cards: ', self.players_cards[0])

            cards_played = []

        # temp = copy.deepcopy(self.players_cards)
        # print('***************************************')
        # if not future_trick:
        # print('cards played: ',cards_played,'    temp: ',temp)
        # extracted_cards = self.extract_cards(cards_played,len(cards_played)-1)
        # print('extracted: ',extracted_cards)
        # extracted_cards.pop(len(extracted_cards)-1)
        # print('extracted: ',extracted_cards)
        # for i in range(len(temp)):
        # temp[i]+=extracted_cards

        # print('cards played: ', cards_played, '    temp: ', temp)
        # print('players cards O: ', temp)

        # checked first iteration
        possible_tricks = self.play_trick(cards_played, play_order, copy.deepcopy(players_cards), my_hand)

        my_turn = self.my_turn(play_order)

        # print('&&&&&&&&&&&&&&&&& end play trick &&&&&&&&&&&&&&&&&&&&&&&&&&')
        print(len(possible_tricks), 'possible tricks(): ', possible_tricks, 'moves ahead: ', moves_ahead)

        # print('cards played: ', cards_played)
        if len(possible_tricks) > 0:
            if type(possible_tricks[0]) == list:
                for i in range(len(possible_tricks)):
                    play_order, winner = self.set_play_order(play_order, possible_tricks[i])
                    # print('possible trick: ',possible_tricks[i])
                    # print('card to remove from my hand: ', possible_tricks[i][my_turn][1])
                    # print('my hand: ', my_hand)
                    copy_of_my_hand = my_hand.copy()
                    # print('copy_of_my_hand((((()))))): ', copy_of_my_hand)
                    copy_of_my_hand.remove(possible_tricks[i][my_turn][1])
                    # print('copy_of_my_hand((((()))))): ',copy_of_my_hand)
                    future_rewards.append(self.Q_reward(moves_ahead - 1, possible_tricks[i], True, play_order,
                                                        copy.deepcopy(players_cards),
                                                        copy_of_my_hand) + self.evaluate_trick(winner))
                # print('my hand after copy: ', self.hand)
                # print('&&&&&&&&&&&&&&&&& end sub Q reward &&&&&&&&&&&&&&&&&&&&&&&&&&')
            else:
                # print('type of possible tricks: ', type(possible_tricks),' possible tricks: ', possible_tricks)
                play_order, winner = self.set_play_order(play_order, possible_tricks)
                # print('card to remove from my hand: ', possible_tricks[my_turn][1])
                # print('my hand: ', self.hand)

                copy_of_my_hand = my_hand.copy()
                copy_of_my_hand.remove(possible_tricks[my_turn][1])
                future_rewards.append(
                    self.Q_reward(moves_ahead - 1, possible_tricks, True, play_order, copy.deepcopy(players_cards),
                                  copy_of_my_hand) + self.evaluate_trick(winner))

                # print('my hand after copy: ', self.hand)
                # print('&&&&&&&&&&&&&&&&& end sub Q reward &&&&&&&&&&&&&&&&&&&&&&&&&&')

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
        # print('card reward: ',cards_played)
        # print('reward: ',sum(future_rewards)/len(future_rewards))
        if len(future_rewards) == 0:
            return sum(future_rewards)
        return sum(future_rewards) / len(future_rewards)

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
        for i in range(1, len(content)):
            preprocessed.append(content[i][content[i].index(':') + 1:])
        return (preprocessed)

    def merge_table(self, table):
        for i in range(len(self.Q_table)):
            for j in range(len(self.Q_table[i])):
                self.Q_table[i][j] = self.Q_table[i][j] + table[i][j]

    def read_Q_table(self):
        # print('read table')
        # print()
        f = open("Q tables queens.txt", "r")
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