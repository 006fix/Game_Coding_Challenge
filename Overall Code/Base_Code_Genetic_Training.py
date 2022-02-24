
import Specific_Functions.Map_Creation as map_creation
import Specific_Functions.Populate_Players as populate_players
import Game_State_Progression.Game_State_Progression as move_time
import Base_Data.Leaderboard_Data as leaderboard_data
import Specific_Functions.Genetic_Algorithm as genetic_algorithm
import pandas as pd
import matplotlib.pyplot as plt
import Base_Data.Players_Data as player_data
import Base_Data.Leaderboard_Data as leaderboard

#below just so i can easily see it
import Base_Data.map_data as map_data

#trial

#num players
num_players = 550
output_pop = []
output_res = []
output_cp = []

new_generation = 0

#create a loop to run the genetic algorithm
num_generations = 500
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
    #this is likely depreciated with the modification of the game to run for a given number of seconds
    #therefore, we will now retain it, but at a high number, and add a new variable below
    num_turns = 300001
    # j serves as the i%j modifier, such that this will trigger every j turns
    j=500
    # modified here to simply output once, at the very end
    #j = num_turns - 1


    #new variable for game length
    num_seconds = 1500000

    #now lets try running time
    for i in range(num_turns):
        print(i)
        #modification of the simulate_time function to allow for leaderboard calculation every x turns
        keep_going = move_time.simulate_time(i, j, num_seconds)
        if not keep_going:
            break

    #lets output our players and their build orders:

    #print(leaderboard_data.rank_pop_base)
    #print(leaderboard_data.raw_pop_base)
    produce_graphs = True

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
    if (gen%1 == 0) or (gen == num_generations-1):
        pop_name = "Population"
        cp_name = "Culture Points"
        res_name = "Resources"
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


    # extra code to output move history
    move_dataset = {}
    for key in player_data.player_dict:
        active_player = player_data.player_dict[key]
        move_dataset[key] = active_player.building_history


    source_string = "player_build_order_gen_" + str(gen) + ".txt"
    textfile = open(source_string, "w")
    for key in move_dataset:
        outfile = move_dataset[key]
        textfile.write(key + "\n")
        textfile.write(str(outfile) + "\n")
    textfile.close()

    best_pop = leaderboard.leaderboard_df.loc[leaderboard.leaderboard_df['pop_rank'].idxmax()]['name']
    best_cp = leaderboard.leaderboard_df.loc[leaderboard.leaderboard_df['cp_rank'].idxmax()]['name']
    best_res = leaderboard.leaderboard_df.loc[leaderboard.leaderboard_df['res_rank'].idxmax()]['name']
    best_total = leaderboard.leaderboard_df.loc[leaderboard.leaderboard_df['total_rank'].idxmax()]['name']

    pop_string = "best_pop_per_gen" + ".txt"
    cp_string = "best_cp_per_gen" + ".txt"
    res_string = "best_res_per_gen" + ".txt"
    total_string = "best_total_per_gen" + ".txt"

    # only need to try one of them to know what to do
    try:
        textfile = open(pop_string)
        file_exists = True
    except:
        file_exists = False

    if file_exists:
        for key in move_dataset:
            if key == best_pop:
                textfile = open(pop_string, "a")
                outfile = move_dataset[key]
                header = f"This is gen {gen}"
                textfile.write(header + "\n")
                textfile.write(str(outfile) + "\n")
                textfile.close()
            if key == best_cp:
                textfile = open(cp_string, "a")
                outfile = move_dataset[key]
                header = f"This is gen {gen}"
                textfile.write(header + "\n")
                textfile.write(str(outfile) + "\n")
                textfile.close()
            if key == best_res:
                textfile = open(res_string, "a")
                outfile = move_dataset[key]
                header = f"This is gen {gen}"
                textfile.write(header + "\n")
                textfile.write(str(outfile) + "\n")
                textfile.close()
            if key == best_total:
                textfile = open(total_string, "a")
                outfile = move_dataset[key]
                header = f"This is gen {gen}"
                textfile.write(header + "\n")
                textfile.write(str(outfile) + "\n")
                textfile.close()
    else:
        for key in move_dataset:
            if key == best_pop:
                textfile = open(pop_string, "w")
                outfile = move_dataset[key]
                header = f"This is gen {gen}"
                textfile.write(header + "\n")
                textfile.write(str(outfile) + "\n")
                textfile.close()
            if key == best_cp:
                textfile = open(cp_string, "w")
                outfile = move_dataset[key]
                header = f"This is gen {gen}"
                textfile.write(header + "\n")
                textfile.write(str(outfile) + "\n")
                textfile.close()
            if key == best_res:
                textfile = open(res_string, "w")
                outfile = move_dataset[key]
                header = f"This is gen {gen}"
                textfile.write(header + "\n")
                textfile.write(str(outfile) + "\n")
                textfile.close()
            if key == best_total:
                textfile = open(total_string, "w")
                outfile = move_dataset[key]
                header = f"This is gen {gen}"
                textfile.write(header + "\n")
                textfile.write(str(outfile) + "\n")
                textfile.close()


##output final results
textfile = open("test_text_file.txt", "w")
for element in new_generation:
    textfile.write(str(element) + "\n")
textfile.close()


