

#this stores the main building focus random AI

import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_baseclass as baseclass
import random

class Main_Building_Focus_6(baseclass.Underlying_Hardcoded):
    def __init__(self, owning_player):
        super().__init__(owning_player)
        self.name = "Main Building: 6"

    def select_building(self, all_possible):

        final_output = []
        for item in all_possible:
            if len(item) == 3:
                if item[0] == 0:
                    final_output.append(item)


        if len(final_output) > 0:
            choose_from_list = final_output
        else:
            choose_from_list = all_possible
        chosen_action = random.choice(choose_from_list)

        return chosen_action
