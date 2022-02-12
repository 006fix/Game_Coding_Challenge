
#this stores the field focus random AI

import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_baseclass as baseclass
import random

class Field_Focus_2(baseclass.Underlying_Hardcoded):
    def __init__(self, owning_player):
        super().__init__(owning_player)
        self.name = "Field_Focus_random: 2"

    def select_building(self, all_possible):

        field_subset = []
        for item in all_possible:
            if len(item) == 2:
                field_subset.append(item)

        if len(field_subset) > 0:
            choose_from_list = field_subset
        else:
            choose_from_list = all_possible
        chosen_action = random.choice(choose_from_list)

        return chosen_action
