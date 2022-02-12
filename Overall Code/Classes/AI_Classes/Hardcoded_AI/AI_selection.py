
#this file exists to provide a function to instantiate the specific AI classes to the rudimentary AI
#this makes it easier to modify things as new AI's are added

#import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_baseclass as base_hardcoded
import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_Storage.Full_Random1 as full_random
import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_Storage.Field_Focus_Random2 as field_random
import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_Storage.Field_Focus_Lowest_lvl3 as field_lowest_lvl
import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_Storage.Main_Building6 as main_building_focus
import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_Storage.Level_by_Level10 as level_by_level
import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_Storage.Level_by_Level_mod11 as level_by_level_mod

def provide_ai(randint, owning_player):
    if randint >= 101:
        #currently we only have one AI, so we'll just use this simple measure
        AI_chosen = full_random.Full_Random_1(owning_player)
    elif randint >= 201:
        AI_chosen = field_random.Field_Focus_2(owning_player)
    elif randint >= 301:
        AI_chosen = field_lowest_lvl.Field_Focus_lowest_level_3(owning_player)
    elif randint >= 401:
        AI_chosen = main_building_focus.Main_Building_Focus_6(owning_player)
    elif randint >= 501:
        AI_chosen = level_by_level.level_by_level_10(owning_player)
    elif randint <= 100:
        AI_chosen = level_by_level_mod.level_by_level_mod_11(owning_player)
    return AI_chosen
