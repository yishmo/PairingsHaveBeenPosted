from Player import Player
'''
Created on Feb 1, 2018

@author: Yishan McNabb
'''
import prompt

def drop_player(players):
    while True:
        dropping = prompt.for_string("Enter the name of player who is dropping or (d)one", is_legal= lambda x : x in [y.name for y in players] or x == 'd', error_message='Invalid player name.')
        if dropping == 'd':
            break;
        for i in range(len(players)):
            if dropping == players[i]:
                del players[i]

a = Player('a')
b = Player('b')
c = Player('a')
d = Player('b')

a.wins.append(b)
a.wins.append(c)
b.losses.append(a)
b.losses.append(c)

drop_player([a,b,c,d])

