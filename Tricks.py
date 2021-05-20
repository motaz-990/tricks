from cards import cards
from Player import Player
import random

print('welcom to Tricks')
player_name = input('enter your name: ')
deck = cards()

# def __init__(self, name, score, hand, game,human):

player = Player(player_name, True)
ai1 = Player('Motaz', False)
ai2 = Player('Tameem', False)
ai3 = Player('Omar', False)
players = [player, ai1, ai2, ai3]
kingdoms_order = [player, ai1, ai2, ai3]
players_order = []
order_of_play = [player_name,'Motaz','Tameem','Omar']


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
suits = ['spade', 'heart', 'club', 'diamond']
up_cards = [' ',' ',' ',' ']
down_cards = [' ',' ',' ',' ']
jack = [up_cards,down_cards]
cards_left = 52
score_of_winner = 200
new_player = True



def add_new_player(name):
    #print('add new player')
    f = open("players.txt", "a")
    line = name+': 0P(0), 1M(0), 2T(0), 3O(0) \n'
    f.write(line)
    f.close()


def players_names(name):
    #print('players names')
    f = open("players.txt", "r")
    content = (f.readlines())
    #print('content: ', content)

    exist = False
    name = name+':'
    for i in content:
        if name in i:
            exist = True
    if exist:
        new_player = input('is this the first time you play? enter [Y/N]: ')
        if new_player == 'Y' or new_player == 'y':
            last_name = input('enter your last name: ')
            name = name+' '+last_name
            add_new_player(name)
    else:
        add_new_player(name)

    return name

def update_winner(name,winner):

    #print('############# update winner #################')
    f = open("players.txt", "r")
    content = (f.readlines())
    #print('content: ', content)
    f = open("players.txt", "w")
    name = name+':'
    line_to_write = ''
    for i in range(len(content)):
        #print('name: ',name)
        #print('content[i]: ',content[i])
        if name in content[i]:
            original_line = content[i]
            print('original_line: ',original_line)
            first_part = original_line[:original_line.index(winner)+3]
            print('first_part: ', first_part)
            original_line = original_line[len(first_part):]

            wins = original_line[:original_line.index(')')]
            print('wins: ',wins)
            updated_wins = int(wins)+1

            content[i] = first_part+str(updated_wins)+original_line[len(wins):]
        line_to_write+= content[i]
    #print(line_to_write)
    f.write(line_to_write)
    f.close()



player_name = players_names(player_name)


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
    print('kingdoms order: ',order_of_play)
    print('king: ', order_of_play[0])
    game = kingdoms_order[0].choose_game()

    '''
    ["tricks", "diamonds", "queens", "king", "jack"]
    copy the game you want from line 75 and paste it in line 78
    '''
    for i in range(len(kingdoms_order)):
        kingdoms_order[i].set_game('tricks')





def play():
    cards_played = []
    for i in range(len(players_order)):
        cards_played.append((players_order[i].name, players_order[i].play(cards_played, order_of_play,0)))
        print(cards_played[i][0], 'played', cards_played[i][1])
        print()
    #print('^^^^^^^^^^^^^ end play ^^^^^^^^^^^^^')
    # trick_winner(cards_played)

    for i in range(len(players_order)):
        if not players_order[i].human:
            players_order[i].cards_played(cards_played,players_order[i].my_turn(order_of_play))
    print('$$$$$$$ cards played $$$$$$$$$$$ : ',cards_played)
    input('press enter to proceed: ')



    winner = trick_winner(cards_played)
    finish = False
    if players[0].game == 'king':
        #print('finished king: ',players[0])
        finish = players[0].contains_king(cards_played)

    return cards_played,winner,finish


def play_jack(cards_left,score_of_winner):

    for i in range(len(players_order)):
        finished, played_card = players_order[i].play(jack,order_of_play,score_of_winner)
        cards_left = update_jack(players_order[i].name,played_card ,cards_left)
        if finished:
            print('score:: ',score_of_winner)
            score_of_winner -= 50
            #print('score:: ', score_of_winner)

    return score_of_winner,cards_left


def update_score(trick_winner,trick):
    trick_winner.update_score(trick)

    # subscores[i] =players[i].get_subscore()
    # scores[i]+= subscores[i]

def update_jack(player,card,cards_left):
    card_obj = cards()
    #print('up: ',up_cards)
    #print('down: ',down_cards)
    #print(player,' played: ',card)
    #print('card: ',card)
    if type(card)!= str:
        index = suits.index(card[0])
        if card_obj.get_rank(card[1])>10:
            up_cards[index]=card
        else:
            down_cards[index]=card
        cards_left -= 1

    print('cards played so far: ')
    print(up_cards)
    print(down_cards)
    jack[0] = up_cards
    jack[1] = down_cards
    return cards_left

def update_wins(scores):
    #winner = players[scores.index(max(scores))].name
    winner = scores.index(max(scores))
    temp = scores.copy()
    temp.pop(winner)
    winner2 = temp.index(max(temp))
    if scores[winner2] == scores[winner]:
        winner = winner2+1

    #print('scores check: ',scores)
    #print(player_name,' updates: ', order_of_play[winner])

    update_winner(player_name,str(winner))


def end_subgame():

    for i in range(len(players)):

        subscores[i] = players[i].get_subscore()
        scores[i] = players[i].get_score()
    print('subscores   : ', subscores)
    print('scores      : ', scores)

    update_wins(subscores)
    input('finished the subgame, press enter to proceed: ')
    if len(kingdoms_order[0].games) == 0:
        kingdoms_order.append(kingdoms_order.pop(0))
        print()
        input('############# kingdom finished ######################')
        print('############# next kingdom  ######################')
        print()
        input('finished the kingdom, press enter to proceed: ')

    return True


def trick_winner(cards_played):
    new_cards = cards()
    #print(cards_played)
    suit, rank = cards_played[0][1][0], new_cards.get_rank(cards_played[0][1][1])
    winner = 0
    for i in range(1, len(cards_played)):
        if cards_played[i][1][0] == suit and new_cards.get_rank(cards_played[i][1][1]) > rank:
            rank = new_cards.get_rank(cards_played[i][1][1])
            winner = i
    print('winner is : ', cards_played[winner])
    return winner


counter_tricks = 1
while not end_game:

    if new_subgame:
        new_deck = deck.get_deck()
        deal_cards(players, new_deck)
        print('################# cards dealt for subgame: ',21-games_left,' ################')

        new_subgame = False
        if first_game:

            players_order,order_of_play = play_order(players,order_of_play, 0)
            kingdoms_order = players_order
            first_game = False

        choose_game()
        print('################ the game has been chosen to be: ', players[0].game, ' #########################')

    else:
        print()

        if players_order[0].game == 'jack':
            score_of_winner, cards_left = play_jack(cards_left, score_of_winner)
            if cards_left == 0:
                cards_left = 52
                score_of_winner = 200
                up_cards = [' ', ' ', ' ', ' ']
                down_cards = [' ', ' ', ' ', ' ']
                jack = [up_cards, down_cards]
                new_subgame = end_subgame()
                games_left -= 1
                end_game = games_left == 0
        else:
            print('################ kingdom: ', 4-int((sub_games_left-1)/5))
            print('################ start of trick: ', counter_tricks, '################ ')
            counter_tricks += 1
            cards_played,winner,finish = play()
            players_order, order_of_play = play_order(players_order, order_of_play,winner)
            update_score(players_order[0],cards_played)
            #update_score(players_order[0], cards_played)
            print()


            if len(players_order[-1].hand) == 0 or finish:
                new_subgame = end_subgame()
                games_left -= 1
                end_game = games_left == 0
                counter_tricks = 1


    if end_game:
        print('scores: ',scores)
        winner = players[scores.index(max(scores))].name
        print('the winner is: ', winner)
        print('Thanks for playing the game!!!!')















