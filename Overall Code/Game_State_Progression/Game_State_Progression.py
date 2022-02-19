
#make a function which iterates through every single interactable object, checks if they sleep
#if not, wake up, take action
#villages don't wake up, but the player themselves is woken up every time and refreshes all


#two functions - check all passive entities
#check all player entities

import Base_Data.map_data as map_data
import Base_Data.Players_Data as player_data
import Classes.AI_Classes.Rudimentary_AI as ai
import random
import Base_Data.Leaderboard_Data as leaderboard

#set game counter
#this is the master time counter, all else refers to here
game_counter = 0
#set turn counter
turn_counter = 0

#set difference from last game counter
time_elapsed = 0

#set next time until update
time_will_elapse = 0

#creating a global level last active
global_last_active = game_counter

def set_time_elapsed():
    global time_elapsed
    global time_will_elapse
    global global_last_active
    time_elapsed = time_will_elapse
    global_last_active = game_counter
    time_will_elapse = "Im a string because i should never remain a string"

#check passive entities

def check_passive():

    next_action_list = []
    for key in map_data.map_dict:
        holdval = map_data.map_dict[key]
        if holdval.type_square in ('habitable', 'oasis'):
            holder = holdval.next_update()
            if holder != True:
                next_action_list.append(holder)
        #need some kind of list that keeps a record of next active time and sets it to change the next update time
    return next_action_list


def check_players(calc_leaderboard, i):
    next_action_list = []

    global game_counter
    global global_last_active
    for key in player_data.player_dict:
        active_player = player_data.player_dict[key]
        wait_time = active_player.will_i_act(game_counter, global_last_active, calc_leaderboard, i)
        next_action_list.append(wait_time)

    return next_action_list


#i = game iteration
#j = i%j, so leaderboard update triggers every j turns
def simulate_time(i, j, gen):
    global game_counter
    global time_will_elapse
    global turn_counter
    set_time_elapsed()
    game_counter = game_counter + time_elapsed
    x1 = check_passive()
    #modification of the check_players function to allow for variance every x turns to allow for leaderboard generation
    if (i%j == 0) and (i>0):
        print(f"UPDATE OF THE LEADERBOARD HAS COMMENCED")
        calc_leaderboard = True
        #refresh the leaderboard
        leaderboard.new_leaderboard()
    else:
        calc_leaderboard = False
    x2 = check_players(calc_leaderboard, i)
    #now all players have been checked, generate the leaderboard
    #but only if calc_leaderboard is true
    if calc_leaderboard:
        leaderboard.produce_leaderboard(leaderboard.leaderboard, i, leaderboard.move_history, gen)
        print(leaderboard.leaderboard_df)
    #resumption of old code
    x3 = x1 + x2
    if len(x3) > 0:
        print("the range of options is as follows:")
        print(x3)
        min_elapsed = min(x3)
    else:
        min_elapsed = 1

    time_will_elapse = min_elapsed
    turn_counter += 1
    print(f"the current game duration is {game_counter}")
    print(f"the game will resume in {min_elapsed} seconds")
    print(f"there have been {turn_counter} turns so far")

