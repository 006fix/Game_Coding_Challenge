
#this file exists to provide a function to instantiate the specific AI classes to the rudimentary AI
#this makes it easier to modify things as new AI's are added

import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_baseclass as base_hardcoded
import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_Storage.Full_Random1 as full_random

def provide_ai(randint, owning_player):
    if randint >= 0:
        #currently we only have one AI, so we'll just use this simple measure
        AI_chosen = full_random.Full_Random_1(owning_player)
    return AI_chosen
