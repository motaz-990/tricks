from cards import cards
from Player import Player
import random

#rename to trianing tricks

print('welcom to Tricks')

deck = cards()

# def __init__(self, name, score, hand, game,human):

player = Player('Motaz', True)
ai1 = Player('ai1', False)
ai2 = Player('ai2', False)
ai3 = Player('ai3', False)
players = [player, ai1, ai2, ai3]
temp_players = [player, ai1, ai2, ai3]
players_order = []

end_game = False
first_game = True
new_subgame = True
new_subgame = True
your_kingdom = True
sub_game_finished = False
games_left = 20
sub_games_left = 20
scores = [0, 0, 0, 0]
subscores = [0, 0, 0, 0]
game = 'diamond'

diamondBroken = False


def first_kingdom(players):
    for i in range(len(players)):
        if players[i].has_seven_hearts():
            return i


def play_order(players, first_player):
    if first_game:
        first_player = first_kingdom(players)

    ordered = []

    for i in range(len(players)):
        ordered += [players[first_player % len(players)]]
        first_player += 1
    return ordered


def deal_cards(players, cards):
    for i in players:
        i.receive_cards(cards)


def choose_game():
    game = 'tricks'
    for i in range(len(temp_players)):
        temp_players[i].set_game(game)


'''
def trick_winner(cards):
    suit = cards[0][1][0]
    winner , winner_card = 0, cards[0][1]
    for i in range (1,len(cards)):
        if cards[i][1][0] == suit:

            if int(cards[i][1][1]>int(winner_card[1])):
                winner_card = cards[i][1][1]
'''


def play():
    cards_played = []
    for i in range(len(players_order)):
        cards_played.append((players_order[i].name, players_order[i].play(cards_played)))
        print(cards_played[i][0], 'played', cards_played[i][1])
    # trick_winner(cards_played)

    return cards_played


def update_score(trick_winner, trick):

    trick_winner.update_score(trick)


    # subscores[i] =players[i].get_subscore()
    # scores[i]+= subscores[i]


def end_subgame():
    for i in range(len(players)):
        subscores[i] = players[i].get_subscore()
        scores[i] = players[i].get_score()
    print('subscores: ', subscores)
    print('scores: ', scores)
    '''
    update_score()
    print('score in this round: ',players[0].name,', ',players[1].name,', ',players[2].name,', ',players[3].name)
    print('score in this round: ',subscores[0],', ',subscores[0],', ',subscores[0],', ', subscores[0])
    print('overall score: ',players[0].name,', ',players[1].name,', ',players[2].name,', ',players[3].name)
    print('overall score: ',subscores[0],', ',subscores[0],', ',subscores[0],', ', subscores[0])
    '''
    if len(temp_players[0].games) == 0:
        temp_players.append(temp_players.pop(0))
        print('------------------')
        b = input('#############kingdom finished#######################')
        print('------------')
    return True


def trick_winner(cards_played):
    new_cards = cards()
    print(cards_played)
    suit, rank = cards_played[0][1][0], new_cards.get_rank(cards_played[0][1][1])
    winner = 0
    for i in range(1, len(cards_played)):
        if cards_played[i][1][0] == suit and new_cards.get_rank(cards_played[i][1][1]) > rank:
            rank = new_cards.get_rank(cards_played[i][1][1])
            winner = i
    print('winner is : ', cards_played[winner])
    return winner


while not end_game:

    if new_subgame:
        new_deck = deck.get_deck()
        deal_cards(players, new_deck)
        print('#################cards dealt################')
        new_subgame = False

        if first_game:
            players_order = play_order(players, 0)
            temp_players = play_order(players, 0)
            first_game = False

        choose_game()
        print('################game has been choosen to be: ',players[0].game ,'#########################')

    else:
        print('--------------')
        cards_played = play()
        players_order = play_order(players_order, trick_winner((cards_played)))
        update_score(players_order[0], cards_played)
        print('---------------')

        if len(players_order[-1].hand) == 11:
            new_subgame = end_subgame()
            games_left -= 1
            end_game = games_left == 0

    if end_game:
        winner = players[scores.index(max(scores))].name
        print('the winner is: ', winner)
        print("would you like to play another game?")

