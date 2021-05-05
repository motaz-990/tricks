from cards import cards
from Player import Player
import random

print('welcom to Tricks')

deck = cards()

# def __init__(self, name, score, hand, game,human):

player = Player('Motaz', True)
ai1 = Player('ai1', False)
ai2 = Player('ai2', False)
ai3 = Player('ai3', False)
players = [player, ai1, ai2, ai3]
kingdoms_order = [player, ai1, ai2, ai3]
players_order = []
order_of_play = ['Motaz','ai1','ai2','ai3']


end_game = False
first_game = True
new_subgame = True
new_subgame = True
your_kingdom = True
sub_game_finished = False
games_left = 10
sub_games_left = 10
scores = [0, 0, 0, 0]
subscores = [0, 0, 0, 0]
game = 'diamond'

diamondBroken = False


def first_kingdom(players):
    for i in range(len(players)):
        if players[i].has_seven_hearts():
            return i


def play_order(players, order_of_play ,first_player):
    if first_game:
        first_player = first_kingdom(players)

    ordered_players = []
    ordered_names = []

    for i in range(len(players)):
        ordered_players += [players[first_player % len(players)]]
        ordered_names += [order_of_play[first_player % len(players)]]
        first_player += 1


    return ordered_players, ordered_names



def deal_cards(players, cards):
    for i in players:
        i.receive_cards(cards)


def choose_game():
    game = kingdoms_order[0].choose_game()
    for i in range(len(kingdoms_order)):
        kingdoms_order[i].set_game(game)





def play():
    cards_played = []
    for i in range(len(players_order)):
        cards_played.append((players_order[i].name, players_order[i].play(cards_played, order_of_play)))
        print(cards_played[i][0], 'played', cards_played[i][1])
    print('^^^^^^^^^^^^^ end play ^^^^^^^^^^^^^')
    # trick_winner(cards_played)

    winner = trick_winner(cards_played)

    return cards_played,winner


def update_score(trick_winner,trick):
    trick_winner.update_score(trick)

    # subscores[i] =players[i].get_subscore()
    # scores[i]+= subscores[i]


def end_subgame():

    for i in range(len(players)):

        subscores[i] = players[i].get_subscore()
        scores[i] = players[i].get_score()
    print('subscores   : ', subscores)
    print('scores      : ', scores)

    if len(kingdoms_order[0].games) == 0:
        kingdoms_order.append(kingdoms_order.pop(0))
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

            players_order,order_of_play = play_order(players,order_of_play, 0)
            kingdoms_order = players_order
            first_game = False

        choose_game()
        print('################game has been choosen to be: ', players[0].game, '#########################')

    else:
        print('--------------')
        cards_played,winner = play()
        players_order, order_of_play = play_order(players_order, order_of_play,winner)
        update_score(players_order[0],cards_played)
        #update_score(players_order[0], cards_played)
        print('---------------')

        if len(players_order[-1].hand) == 0:
            new_subgame = end_subgame()
            games_left -= 1
            end_game = games_left == 0


    if end_game:
        print('scores: ',scores)
        winner = players[scores.index(max(scores))].name
        print('the winner is: ', winner)
        print("would you like to play another game?")

