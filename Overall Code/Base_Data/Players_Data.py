
import Specific_Functions.Map_Creation as map_creation

holder_dict = {}
#because of the order things work, you can't map village data to the player dict until after the player
#has made their first village. So store it here, then transfer it over later.

player_dict = {}


#trial data for tests

# player_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
# loc_list = [
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
#     ['+', '+'],
#     ['+', '-'],
#     ['-', '+'],
#     ['-', '-'],
# ]
# race_list = [1, 2, 3, 1, 2, 3, 1, 2]

#simpler trial

player_list = ['a', 'b', 'c']
loc_list = [['+', '-'], ['-', '-'], ['+', '-']]
race_list = [1, 2, 3]

#simplest trial

# player_list = ['a']
# loc_list = [['+', '+']]
# race_list = [1]
