
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
    elite_rank = 70
    num_elite = 10

    #define the breeding candidates
    breeding_rank = 60
    num_breeding = 20

    #input file
    input_data = leaderboard_data.leaderboard_df[['name', 'total_rank']]

    #select our elite_rank names
    elite_candidates = input_data.loc[input_data['total_rank'] >= elite_rank]
    elite_candidates2 = elite_candidates.sort_values(by='total_rank', ascending=False)
    elite_candidates3 = elite_candidates2.head(num_elite)
    elite_names = list(elite_candidates3['name'])

    #select our breeding_candidate names
    breeding_candidates = input_data.loc[input_data['total_rank'] >= breeding_rank]
    breeding_candidates2 = breeding_candidates.sort_values(by='total_rank', ascending=False)
    breeding_candidates3 = breeding_candidates.head(num_breeding)
    breeding_names = list(breeding_candidates3['name'])

    return breeding_names, elite_names

#now that we have our names, we need to extract the associated AI chromosomes
#to do this, we will reference back to our player dictionary, get the associated player object,
#then get the associated self.AI object,
#then get the associated chromosome

#we only need to do this for the breeding candidates, since our elite candidates are already within that set.


def create_candidates():
    chromosome_dict = {}
    breeding_candidates, elite_candidates = genetic_prerun()
    for name in breeding_candidates:
        associated_player = player_data.player_dict[name]
        associated_chromosome = associated_player.AI.chromosome
        chromosome_dict[name] = associated_chromosome

    return chromosome_dict, elite_candidates

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

    for chromosome in intermediary_population:
        holder_chromosome = []
        for val in chromosome:
            checkval = random.randint(1,100)
            if checkval > 95:
                newval = round(random.gauss(val, (val / 2)), 3)
                holder_chromosome.append(newval)
            else:
                holder_chromosome.append(val)









