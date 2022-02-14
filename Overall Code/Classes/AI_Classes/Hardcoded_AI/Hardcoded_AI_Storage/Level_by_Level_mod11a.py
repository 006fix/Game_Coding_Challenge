


#this stores the level by level random AI

import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_baseclass as baseclass
import random

class level_by_level_mod_11a(baseclass.Underlying_Hardcoded):
    def __init__(self, owning_player):
        super().__init__(owning_player)
        self.name = "Level by Level mod: 11a"

    def select_building(self, all_possible, info_packet):

        #now add in a modifier for field_subset
        lowest_level = 500
        #lowest level set to 500, will be overwritten each time
        for item in all_possible:
            #use negative one index to find level despite variant length
            if len(item) == 3:
                level = item[-1]
            elif len(item) == 2:
                if item[-1] <= 5:
                    level = item[-1] / 2
                else:
                    level = item[-1]
            else:
                raise ValueError("I've encountered a input variable that i'm not familiar with")
            if level < lowest_level:
                lowest_level = level
        #now find all items that meet the criteria of lowest level
        output_subset = []
        for item in all_possible:
            if len(item) == 3:
                level = item[-1]
            elif len(item) == 2:
                if item[-1] <= 5:
                    level = item[-1] / 2
                else:
                    level = item[-1]
            else:
                raise ValueError("I've encountered a input variable that i'm not familiar with")
            if level == lowest_level:
                output_subset.append(item)

        chosen_action = random.choice(output_subset)

        return chosen_action