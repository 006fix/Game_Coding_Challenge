
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

    #the following two numbers are defined as such since higher = better

    #define the elite candidates
    num_elite = 10

    #define the breeding candidates
    num_breeding = 20

    #input file
    input_data = leaderboard_data.leaderboard_df[['name', 'res_rank']]

    #select our elite_rank names
    elite_candidates2 = input_data.sort_values(by='res_rank', ascending=False)
    elite_candidates3 = elite_candidates2.head(num_elite)
    elite_names = list(elite_candidates3['name'])

    #select our breeding_candidate names
    breeding_candidates2 = input_data.sort_values(by='res_rank', ascending=False)
    breeding_candidates3 = breeding_candidates2.head(num_breeding)
    breeding_names = list(breeding_candidates3['name'])

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


    ###harcoded fix just to force this stupid thing to work properly
    if len(elite_names) != 10:
        if len(elite_names) > 10:
            elite_names = elite_names[:10]
        else:
            diff = 10 - len(elite_names)
            for fix in range(diff):
                holdval = elite_names[-1]
                elite_names.append(holdval)
    if len(breeding_names) != 20:
        if len(breeding_names) > 20:
            breeding_names = breeding_names[:20]
        else:
            diff = 20 - len(breeding_names)
            for fix in range(diff):
                holdval = breeding_names[-1]
                breeding_names.append(holdval)



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
    split_num = 10
    output_population = []
    holder_population = []
    intermediary_population = []
    for key in chromosome_dict:
        holder_population.append(chromosome_dict[key])
        if key in elite_candidates:
            output_population.append(chromosome_dict[key])
    random.shuffle(holder_population)
    list1 = holder_population[:split_num]
    list2 = holder_population[split_num:]
    random.shuffle(holder_population)
    list3 = holder_population[:split_num]
    list4 = holder_population[split_num:]
    #generate first set of children
    for i in range(len(list1)):
        child1, child2 = breed_candidates(list1[i], list2[i])
        intermediary_population.append(child1)
        intermediary_population.append(child2)
    for i in range(len(list3)):
        child1, child2 = breed_candidates(list3[i], list4[i])
        intermediary_population.append(child1)
        intermediary_population.append(child2)

    #now mutate the children
    #twice

    for mut_loop in range(2):
        for chromosome in intermediary_population:
            holder_chromosome = []
            for val in chromosome:
                checkval = random.randint(1,100)
                if checkval > 98:
                    newval = round(random.gauss(val, (val / 2)), 3)
                    holder_chromosome.append(newval)
                else:
                    holder_chromosome.append(val)
            output_population.append(holder_chromosome)


    #control to account for the fact that this CONSTANTLY returns cases where there's the wrong number of chromosomes
    #if len(output_population) != num players, then pad it with the final value

    if len(output_population) != 9*len(elite_candidates):
        diff = (9*len(elite_candidates)) - len(output_population)
        for stupid_fix in range(diff):
            holdval = output_population[-1]
            output_population.append(holdval)

    return output_population










