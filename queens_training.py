from cards import cards
from trained_player_queens import trained_player_queens
import random

#rename to trianing tricks

print('welcom to diamonds')

deck = cards()

# def __init__(self, name, score, hand, game,human):

player = trained_player_queens('Motaz', True)
ai1 = trained_player_queens('ai1', False)
ai2 = trained_player_queens('ai2', False)
ai3 = trained_player_queens('ai3', False)
players = [player, ai1, ai2, ai3]
temp_players = [player, ai1, ai2, ai3]
players_order = players
order_of_play = ['Motaz','ai1','ai2','ai3']

end_game = False
first_game = True
new_subgame = True
new_subgame = True
your_kingdom = True
sub_game_finished = False
games_left = 1
sub_games_left = 1
scores = [0, 0, 0, 0]
subscores = [0, 0, 0, 0]
game = 'queens'



'''
def first_kingdom(players):
    for i in range(len(players)):
        if players[i].has_seven_hearts():
            return i
'''

def play_order(players,order_of_play ,first_player):
    #if first_game:
     #   first_player = first_kingdom(players)

    ordered_players = []
    ordered_names = []

    for i in range(len(players)):
        ordered_players += [players[first_player % len(players)]]
        ordered_names += [order_of_play[first_player % len(players)]]
        first_player += 1

    return ordered_players,ordered_names


def deal_cards(players, cards):
    for i in players:
        i.receive_cards(cards)

'''
def choose_game():
    game = 'tricks'
    for i in range(len(temp_players)):
        temp_players[i].set_game(game)
'''


def play():

    cards_played = []

    for i in range(len(players_order)):
        cards_played.append((players_order[i].name, players_order[i].play(cards_played,order_of_play)))
        #print('((((((((((((((((((((((((((((( end play )))))))))))))))))))))))))))))))))))))))')
        #print(cards_played)
        print(cards_played[i][0], 'played', cards_played[i][1])
    # trick_winner(cards_played)

    for i in range(len(players_order)):
        '''
        print('((((((((((((((((((((((((((((( end play )))))))))))))))))))))))))))))))))))))))')
        print('cards played: ', cards_played)
        print('player: ', order_of_play[i])
        print('players_order[i].my_turn(order_of_play) : ', players_order[i].my_turn(order_of_play))
        '''
        players_order[i].cards_played(cards_played,players_order[i].my_turn(order_of_play))
    print('$$$$$$$ cards played $$$$$$$$$$$ : ',cards_played)
    winner = trick_winner(cards_played)
    players[0].analyse_trick_diamond(cards_played,cards_played[winner][0])
    players[0].number_of_cards()


    return cards_played,winner


def update_score(trick_winner, trick):

    trick_winner.update_score(trick)



def end_subgame():
    for i in range(len(players)):
        subscores[i] = players[i].get_subscore()
        scores[i] = players[i].get_score()
    print('subscores: ', subscores)
    print('scores: ', scores)

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

counter = 1
while not end_game:

    if new_subgame:
        new_deck = deck.get_deck()
        deal_cards(players, new_deck)
        print('################# start of game number : ',counter,'################')
        counter+=1
        new_subgame = False

        players_order,order_of_play = play_order(players_order,order_of_play, random.randrange(4))



    else:
        print('--------------')
        #print('players order: ', players_order)
        cards_played, winner = play()
        #print('players order: ', players_order)
        players_order, order_of_play = play_order(players_order, order_of_play,winner)
        print('^^^^^^^^^^^^^^^^^^^^ end play ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        #print('players order: ', players_order)
        update_score(players_order[0], cards_played)
        #print('^^^^^^^^^^^^^^^^^^^^ end update score ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        print('---------------')

        if len(players_order[-1].hand) == 0:
            new_subgame = end_subgame()
            games_left -= 1
            end_game = games_left == 0

    if end_game:
        winner = players[scores.index(max(scores))].name
        print('the winner is: ', winner)
        print("would you like to play another game?")