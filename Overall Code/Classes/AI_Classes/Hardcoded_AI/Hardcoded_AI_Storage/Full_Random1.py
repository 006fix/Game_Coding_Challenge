
#this stores the completely random AI

import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_baseclass as baseclass
import random

class Full_Random_1(baseclass.Underlying_Hardcoded):
    def __init__(self, owning_player):
        super().__init__(owning_player)
        self.name = "Full Random: 1"

    def select_building(self, all_possible):

        chosen_action = random.choice(all_possible)

        return chosen_action

