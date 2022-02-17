
import Specific_Functions.Map_Creation as map_creation
import Specific_Functions.Populate_Players as populate_players
import Game_State_Progression.Game_State_Progression as move_time
import Base_Data.Leaderboard_Data as leaderboard_data
import Specific_Functions.Genetic_Algorithm as genetic_algorithm
import pandas as pd
import matplotlib.pyplot as plt


#below just so i can easily see it
import Base_Data.map_data as map_data

#trial

#num players
num_players = 90
output_pop = []
output_res = []
output_cp = []

new_generation = 0

#create a loop to run the genetic algorithm
num_generations = 50
for gen in range(num_generations):
    #reset the game data
    move_time.game_counter = 0
    move_time.turn_counter = 0
    move_time.time_elapsed = 0
    move_time.time_will_elapse = 0
    move_time.global_last_active = move_time.game_counter


    #create the base map
    map_creation.map_creation()
    #modify the base map to include oasis, wilderness, habitable
    map_creation.modify_base_map()

    #import a list of trial players
    populate_players.populate_players(num_players, new_generation)
    #update the player dict with their new village locations
    populate_players.update_player_dict()

    #now lets try running time
    for i in range(1001):
        print(i)
        #modification of the simulate_time function to allow for leaderboard calculation every x turns
        #j serves as the i%j modifier, such that this will trigger every j turns
        j = 1000
        move_time.simulate_time(i, j)

    #print(leaderboard_data.rank_pop_base)
    #print(leaderboard_data.raw_pop_base)
    produce_graphs = False

    if produce_graphs:
        leaderboard_data.produce_final_outputs()
    print(move_time.game_counter)

    x1, x2, results = genetic_algorithm.create_candidates()
    new_generation = genetic_algorithm.create_population(x1, x2)

    output_pop.append(results[0][0])
    output_cp.append(results[1][0])
    output_res.append(results[2][0])

plt.plot(output_pop)
plt.title("Population")
plt.show()
plt.plot(output_cp)
plt.title("Culture Points")
plt.show()
plt.plot(output_res)
plt.title("Resources")
plt.show()


