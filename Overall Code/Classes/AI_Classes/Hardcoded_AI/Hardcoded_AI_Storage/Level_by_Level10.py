

#this stores the level by level random AI

import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_baseclass as baseclass
import random

class level_by_level_10(baseclass.Underlying_Hardcoded):
    def __init__(self, owning_player):
        super().__init__(owning_player)

    def select_building(self, all_possible):

        #now add in a modifier for field_subset
        lowest_level = 500
        #lowest level set to 500, will be overwritten each time
        for item in all_possible:
            #use negative one index to find level despite variant length
            level = item[-1]
            if level < lowest_level:
                lowest_level = level
        #now find all items that meet the criteria of lowest level
        output_subset = []
        for item in all_possible:
            level = item[1]
            if level == lowest_level:
                output_subset.append(item)

        chosen_action = random.choice(output_subset)

        return chosen_action