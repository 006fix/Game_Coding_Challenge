

import Classes.Village as village
import Base_Data.map_data as map_data
import random
import Specific_Functions.Map_Creation as map_creation
import Base_Data.Players_Data as player_data

def Can_i_make_a_village(loop1, loop2, owner):
    Keep_Looking = True
    if loop1 == True:
        if loop2 == True:
            x1 = 0
            x2 = map_data.map_xmax
            y1 = 0
            y2 = map_data.map_ymax
        else:
            x1 = 0
            x2 = map_data.map_xmax
            y1 = map_data.map_ymin
            y2 = 0
    else:
        if loop2 == True:
            x1 = map_data.map_xmin
            x2 = 0
            y1 = 0
            y2 = map_data.map_xmax
        else:
            x1 = map_data.map_xmin
            x2 = 0
            y1 = map_data.map_ymin
            y2 = 0

    while Keep_Looking:
        location_trial_x = random.randint(x1, x2)
        location_trial_y = random.randint(y1, y2)
        trial_loc = str([location_trial_x, location_trial_y])
        check_loc = map_data.map_dict[trial_loc]
        breaking_statement = True
        if check_loc.type_square == 'habitable':
            if check_loc.type_hab == [4, 4, 4, 6]:
                print(check_loc.type_hab)
                new_obj = village.Village(trial_loc, check_loc.type_hab,
                                  check_loc.field_list_dict, owner)
                map_data.map_dict[trial_loc] = new_obj
                Keep_Looking = False
                breaking_statement = False
                player_data.holder_dict[owner] = trial_loc
                print(f"Player {owner} has made a village at {trial_loc}")
        if breaking_statement:
            holdval = check_loc.type_square
            print(f"Attempt to make a village failed since {trial_loc} was {holdval}")
            # to flag in if habitable failure
            try:
                v1 = check_loc.type_hab
                print(f"Although habitabe, it was a {v1} village")
            except:
                pass
    return trial_loc