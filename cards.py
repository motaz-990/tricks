import random


class cards:

    def __init__(self):
        self.suits = ['heart', 'diamond', 'spade', 'club']
        self.ranksNames = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'A']
        self.ranks = {'2':1 ,'3': 2,'4':3 ,'5': 4, '6': 5,'7': 6,'8': 7,'9': 8,'10': 9,'j': 10,'q': 11,'k': 12, 'A':13}
        self.Cards = []



    def get_deck(self):

        for i in range(4):
            for j in range(2):
                self.Cards.append((self.suits[i], self.ranksNames[j]))
        random.shuffle(self.Cards)
        return self.Cards

    def get_rank (self,card):
        return self.ranks[card]










