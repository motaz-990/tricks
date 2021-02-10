import random


class Player:

    def __init__(self, name, trained):
        games = ["tricks", "diamonds", "queens", "king", "jack"]
        # games = ['tricks']
        self.name = name
        self.score = 0
        self.subscore = 0
        self.hand = []
        self.games = games
        self.game = ' '
        self.trained = trained
        self.stateSpace = []
        self.actionSpace =[]

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
        self.game = game

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

                allowed = self.allowed_cards(cards_played[0][1][0])
                print('^^^^^^^^^^^^^^^^^^^^ AI options ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                for i in range(len(allowed)):
                    print(i + 1, ': ', allowed[i])
                print('^^^^^^^^^^^^^^^^^^^^ AI decision ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')

                card = self.Q_table(cards_played)

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
    def update_Q_table(self, card):
        pass

    def Q_table(self,cards_played, allowed_cards):

        if(random.random()>90):
            card = allowed_cards[0]
            self.update_Q_table(card)
            return card
        else:
            #choose the max reward
            pass

