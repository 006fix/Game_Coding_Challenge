
#this area will hold the various functions required for the functioning of the genetic algorithm

#basic logic will work like this:

#input file = leaderboard produced at the very end of the run of the code

#we shall initially try with 90 players

#top 10 players are retained, directly copied into the next game

#top 20 players, including the top 10 retained, are then selected for breeding

#2 random runs of breeding will be conducted - this will produce an additional 40 players

#these 40 players will then be duplicated, and each one subjected to a run of mutations.

#this will produce 90 players, ready for seeding within the next round.

import Base_Data.Leaderboard_Data as leaderboard_data
import Base_Data.Players_Data as player_data
#import Classes.AI_Classes.Hardcoded_AI.Rudimentary_AI as rudimentary_AI
import random

def genetic_prerun():

    #this lets us use pop size way down as a control
    global pop_size

    #the following two numbers are defined as such since higher = better

    #define the elite candidates
    num_elite = 10

    #define the breeding candidates
    num_breeding = 60

    #define the population size
    #(this is currently 9*num_breeding + num_elite)
    pop_size = 550

    #input file
    input_data = leaderboard_data.leaderboard_df[['name', 'res_rank', 'cp_rank', 'pop_rank']]
    input_data2 = input_data.sort_values(by=['res_rank', 'cp_rank', 'pop_rank'], ascending = [False, False, False])

    #new variation to attempt to preferentially select for diversity as well as score
    #old code commented out below

    #get all names in sorted order
    all_names = list(input_data2['name'])
    #create a storage file to hold series of actions used
    currently_used_actions = []
    #and some to hold the names of elites and breeders
    elite_names = []
    breeding_names = []
    #now loop through names one by one, pull out their actions, check the list, if not present, use
    #use a while loop
    keep_looking = True
    index_counter = 0
    while keep_looking:
        #control for if we've already found enough
        if len(breeding_names) == num_breeding:
            keep_looking = False
        else:
            active_name = all_names[index_counter]
            active_player = player_data.player_dict[active_name]
            action_list = active_player.building_history
            if action_list not in currently_used_actions:
                breeding_names.append(active_name)
                #also add to the elite if elite < 10
                if len(elite_names) < num_elite:
                    elite_names.append(active_name)
        index_counter += 1


    #old code, left to later use, functional code replicating function is above
    #select our elite_rank names
    #elite_candidates3 = input_data2.head(num_elite)
    #elite_names = list(elite_candidates3['name'])

    #select our breeding_candidate names
    #breeding_candidates3 = input_data2.head(num_breeding)
    #breeding_names = list(breeding_candidates3['name'])

    #control for if the above hasn't worked
    if (len(elite_names) != num_elite) or (len(breeding_names) != num_breeding):
        raise ValueError("An improper number of candidates have been created, please rectify")

    #find our best candidate for pop, res, and cp
    input_data2 = leaderboard_data.leaderboard_df[['name', 'pop', 'cp', 'single_num_res']]
    #sort them
    pop_sort = input_data2.sort_values(by='pop', ascending=False)
    cp_sort = input_data2.sort_values(by='cp', ascending=False)
    res_sort = input_data2.sort_values(by='single_num_res', ascending=False)
    #get the best
    pop_best = pop_sort.head(1)
    cp_best = cp_sort.head(1)
    res_best = res_sort.head(1)
    #extract the values
    pop_val = pop_best['pop'].values
    cp_val = cp_best['cp'].values
    res_val = list(res_best['single_num_res'].values)
    #generate output
    output_data = [pop_val, cp_val, res_val]


    #remove later if not needed

    # ###harcoded fix just to force this stupid thing to work properly
    # if len(elite_names) != 10:
    #     if len(elite_names) > 10:
    #         elite_names = elite_names[:10]
    #     else:
    #         diff = 10 - len(elite_names)
    #         for fix in range(diff):
    #             holdval = elite_names[-1]
    #             elite_names.append(holdval)
    # if len(breeding_names) != 20:
    #     if len(breeding_names) > 20:
    #         breeding_names = breeding_names[:20]
    #     else:
    #         diff = 20 - len(breeding_names)
    #         for fix in range(diff):
    #             holdval = breeding_names[-1]
    #             breeding_names.append(holdval)



    return breeding_names, elite_names, output_data

#now that we have our names, we need to extract the associated AI chromosomes
#to do this, we will reference back to our player dictionary, get the associated player object,
#then get the associated self.AI object,
#then get the associated chromosome

#we only need to do this for the breeding candidates, since our elite candidates are already within that set.


def create_candidates():
    chromosome_dict = {}
    #we don't use output data here, but we'll bring it in anyway
    breeding_candidates, elite_candidates, output_data = genetic_prerun()
    for name in breeding_candidates:
        associated_player = player_data.player_dict[name]
        associated_chromosome = associated_player.AI.chromosome
        chromosome_dict[name] = associated_chromosome

    return chromosome_dict, elite_candidates, output_data

def breed_candidates(chromosome1, chromosome2):
    #only works if chromosomes are the same length
    breeding_sequence = []
    for val in range(len(chromosome1)):
        output = random.randint(0,1)
        breeding_sequence.append(output)

    child1 = []
    child2 = []
    for val in range(len(breeding_sequence)):
        if breeding_sequence[val] == 0:
            holdval1 = chromosome1[val]
            holdval2 = chromosome2[val]
        else:
            holdval1 = chromosome2[val]
            holdval2 = chromosome1[val]
        child1.append(holdval1)
        child2.append(holdval2)


    return child1, child2

def create_population(chromosome_dict, elite_candidates):

    #this is just here for the final control check on chromosome length
    global pop_size


    split_num = int(len(chromosome_dict)/2)
    output_population = []
    holder_population = []
    intermediary_population = []
    for key in chromosome_dict:
        holder_population.append(chromosome_dict[key])
        if key in elite_candidates:
            output_population.append(chromosome_dict[key])
    for j in range(9):
        random.shuffle(holder_population)
        list1 = holder_population[:split_num]
        list2 = holder_population[split_num:]
        for i in range(len(list1)):
            child1, child2 = breed_candidates(list1[i], list2[i])
            intermediary_population.append(child1)
            intermediary_population.append(child2)

    #now mutate the children
    #twice
    #why on earth was i doing this twice???

    for chromosome in intermediary_population:
        holder_chromosome = []
        for val in chromosome:
            checkval = random.randint(1,100)
            if checkval > 98:
                newval = val * random.uniform(0.90, 1.10)
                holder_chromosome.append(newval)
            else:
                holder_chromosome.append(val)
        output_population.append(holder_chromosome)


    if len(output_population) != pop_size:
        raise ValueError("Why has this returned the wrong number of chromosomes")

    return output_population










