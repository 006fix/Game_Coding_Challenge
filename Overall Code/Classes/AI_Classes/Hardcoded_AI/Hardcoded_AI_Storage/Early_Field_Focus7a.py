



#this stores the early field focus random AI

#HOWEVER, this will require a control for if the only options available are main building, warehouse, granary

import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_baseclass as baseclass
import random


class Early_Field_Focus_7a(baseclass.Underlying_Hardcoded):
    def __init__(self, owning_player):
        super().__init__(owning_player)
        self.name = "Early_Field_Focus: 7a"

    def select_building(self, all_possible):

        #control for if there's only warehouse and main building upgrades
        priority_warehouse = []
        if len(all_possible) == 3:
            all_buildings = True
            for item in all_possible:
                if len(item) == 2:
                    all_buildings = False
            if all_buildings:
                for item in all_possible:
                    if (item[0] == 1) or (item[0] == 2):
                        priority_warehouse.append(item)


        #this first loop is used to select all fields <= 5
        priority_fields = []
        for item in all_possible:
            if len(item) == 2:
                level = item[-1]
                if level <= 5:
                    priority_fields.append(item)

        #this second loop is used to select main building, it first loop is empty and main building <= 10
        priority_main_building = []
        if len(priority_fields) == 0:
            for item in all_possible:
                if len(item) == 3:
                    if item[0] == 0:
                        if item[-1] <= 10:
                            priority_main_building.append(item)

        if len(priority_warehouse) > 0:
            choose_from_this = priority_warehouse
        elif len(priority_fields) > 0:
            choose_from_this = priority_fields
        elif len(priority_main_building) > 0:
            choose_from_this = priority_main_building
        else:
            choose_from_this = all_possible

        chosen_action = random.choice(choose_from_this)

        return chosen_action