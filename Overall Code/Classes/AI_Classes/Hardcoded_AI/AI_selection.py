
#this file exists to provide a function to instantiate the specific AI classes to the rudimentary AI
#this makes it easier to modify things as new AI's are added

import random

#import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_baseclass as base_hardcoded
import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_Storage.Full_Random1 as full_random
import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_Storage.Field_Focus_Random2 as field_random
import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_Storage.Field_Focus_Lowest_lvl3 as field_lowest_lvl
import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_Storage.Main_Building6 as main_building_focus
import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_Storage.Level_by_Level10a as level_by_level
import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_Storage.Level_by_Level_mod11a as level_by_level_mod
import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_Storage.Early_Field_Focus7a as early_field_focus

#provide a list of AIs to be chosen from at random

x1 = full_random.Full_Random_1
x2 = field_random.Field_Focus_2
x3 = field_lowest_lvl.Field_Focus_lowest_level_3
x4 = main_building_focus.Main_Building_Focus_6
x5 = level_by_level.level_by_level_10a
x6 = level_by_level_mod.level_by_level_mod_11a
x7 = early_field_focus.Early_Field_Focus_7a


AI_possibles = [x1, x2, x3, x4, x5, x6, x7]
import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_Storage.Genetic_Generic99 as genetic_generic
x8 = genetic_generic.Genetic_Generic_1

genetic_AI_possibles = [x8]

numeric_ai_possibles = len(AI_possibles) - 1

def provide_ai(randint, owning_player):

    AI_chosen = AI_possibles[randint](owning_player)
    print(f"AI_chosen for player {owning_player} = {AI_chosen}")

    return AI_chosen

def provide_ai_gentest(randint, owning_player):

    test_chromosome = []
    for i in range(84):
        holdval1 = random.randint(0,4)
        holdval2 = round(2*random.random(), 3)
        holdval3 = round(3*random.random(), 3)
        holdval4 = random.randint(1,10)/10
        test_chromosome.append(holdval1)
        test_chromosome.append(holdval2)
        test_chromosome.append(holdval3)
        test_chromosome.append(holdval4)

    randchecker = random.randint(1,2)
    if randchecker >= 0:
        AI_chosen = genetic_AI_possibles[0](owning_player, test_chromosome)
    #if randchecker == 2:
        #AI_chosen = AI_possibles[3](owning_player)
    print(f"AI_chosen for player {owning_player} = {AI_chosen}")

    return AI_chosen

#new function for genetic algorithm breeding

def provide_ai_genloop(chromosome, owning_player):
    if chromosome == 0:
        test_chromosome = []
        for i in range(84):
            holdval1 = random.randint(0, 4)
            holdval2 = round(2 * random.random(), 3)
            holdval3 = round(3 * random.random(), 3)
            holdval4 = random.randint(1, 10) / 10
            test_chromosome.append(holdval1)
            test_chromosome.append(holdval2)
            test_chromosome.append(holdval3)
            test_chromosome.append(holdval4)
        AI_chosen = genetic_AI_possibles[0](owning_player, test_chromosome)
    else:
        AI_chosen = genetic_AI_possibles[0](owning_player, chromosome)
    print(f"AI_chosen for player {owning_player} = {AI_chosen}")

    return AI_chosen
