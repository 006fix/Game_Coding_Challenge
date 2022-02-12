
#this file exists to provide a function to instantiate the specific AI classes to the rudimentary AI
#this makes it easier to modify things as new AI's are added

import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_baseclass as base_hardcoded
import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_Storage.Full_Random1 as full_random
import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_Storage.Field_Focus_Random2 as field_random

def provide_ai(randint, owning_player):
    if randint >= 50:
        #currently we only have one AI, so we'll just use this simple measure
        AI_chosen = full_random.Full_Random_1(owning_player)
    else:
        AI_chosen = field_random.Field_Focus_2(owning_player)
    return AI_chosen
