
#import Specific_Functions.Map_Creation as map_creation
import random

holder_dict = {}
#because of the order things work, you can't map village data to the player dict until after the player
#has made their first village. So store it here, then transfer it over later.

player_dict = {}


#new function to just generate player lists of a given_size
letter_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z']
loc_list = ['+', '-']

def create_players(num_players):
    name_list = []
    location_list = []
    race_list = []
    for i in range(num_players):
        letter = i%26
        name = letter_list[letter] + str(i)

        loc_ran1 = random.randint(0,1)
        loc_ran2 = random.randint(0,1)
        loc1 = loc_list[loc_ran1]
        loc2 = loc_list[loc_ran2]
        location = [loc1, loc2]
        race = random.randint(1,3)

        name_list.append(name)
        location_list.append(location)
        race_list.append(race)

    return name_list, location_list, race_list





#trial data for tests

# player_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
#                'u', 'v', 'w', 'x', 'y', 'z', 'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1', 'i1', 'j1', 'k1',
#                'l1', 'm1', 'n1', 'o1', 'p1', 'q1', 'r1', 's1', 't1', 'u1', 'v1', 'w1', 'x1', 'y1', 'z1',
#                'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2', 'i2', 'j2', 'k2',
#                'l2', 'm2', 'n2', 'o2', 'p2', 'q2', 'r2', 's2', 't2', 'u2', 'v2', 'w2', 'x2', 'y2', 'z2',
#                'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3', 'i3', 'j3', 'k3',
#                'l3', 'm3', 'n3', 'o3', 'p3', 'q3', 'r3', 's3', 't3', 'u3', 'v3', 'w3', 'x3', 'y3', 'z3'
#                ]
# loc_list = [
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['-', '-']
# ]
# race_list = [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2,
#              3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1,
#              2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2,
#              3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1]

#semi complex version

# player_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm']
# loc_list = [
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+']
# ]
#
# race_list = [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1]

#simpler trial

# player_list = ['a', 'b', 'c']
# loc_list = [['+', '-'], ['-', '-'], ['+', '-']]
# race_list = [1, 2, 3]

#simplest trial

# player_list = ['a']
# loc_list = [['+', '+']]
# race_list = [1]
