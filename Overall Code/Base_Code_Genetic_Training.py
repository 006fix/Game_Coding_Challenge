
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
num_generations = 10
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

    #variable to control the number of turns
    num_turns = 5001

    #now lets try running time
    for i in range(num_turns):
        print(i)
        #modification of the simulate_time function to allow for leaderboard calculation every x turns
        #j serves as the i%j modifier, such that this will trigger every j turns
        j = 5000
        move_time.simulate_time(i, j, gen)

    #lets output our players and their build orders:

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

    outpath1 = r"C:\Users\pyeac\Desktop\Travian_Game\Output_Charts"
    outpath2 = r"\test2"
    outpath3 = r"\Genetic"

    savepath = outpath1+outpath2+outpath3+r"\\"

    #save figs every 10 runs
    if (gen%10 == 0) or (gen == num_generations-1):
        pop_name = "Population" + str(gen)
        cp_name = "Culture Points" + str(gen)
        res_name = "Resources" + str(gen)
        plt.plot(output_pop)
        plt.title(pop_name)
        plt.savefig(savepath+pop_name+".png")
        plt.clf()
        plt.plot(output_cp)
        plt.title(cp_name)
        plt.savefig(savepath+cp_name + ".png")
        plt.clf()
        plt.plot(output_res)
        plt.title(res_name)
        plt.savefig(savepath+res_name + ".png")
        plt.clf()


##output final results
textfile = open("test_text_file.txt", "w")
for element in new_generation:
    textfile.write(str(element) + "\n")
textfile.close()


