
#this stores the field focus lowest level random AI

import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_baseclass as baseclass
import random

class Field_Focus_lowest_level_3(baseclass.Underlying_Hardcoded):
    def __init__(self, owning_player):
        super().__init__(owning_player)
        self.name = "Field_Focus_Lowest_Level: 3"

    def select_building(self, all_possible, info_packet):

        field_subset = []
        for item in all_possible:
            if len(item) == 2:
                field_subset.append(item)

        #now add in a modifier for field_subset
        lowest_level = 500
        #lowest level set to 500, will be overwritten each time
        for item in field_subset:
            level = item[1]
            if level < lowest_level:
                lowest_level = level
        #now find all items that meet the criteria of lowest level
        field_subset2 = []
        for item in field_subset:
            level = item[1]
            if level == lowest_level:
                field_subset2.append(item)

        if len(field_subset2) > 0:
            choose_from_list = field_subset2
        else:
            choose_from_list = all_possible
        chosen_action = random.choice(choose_from_list)

        return chosen_action