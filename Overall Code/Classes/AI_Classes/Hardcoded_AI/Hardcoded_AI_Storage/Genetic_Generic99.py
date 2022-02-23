

#this stores the generic genetic algorithm

import Classes.AI_Classes.Hardcoded_AI.Hardcoded_AI_baseclass as baseclass
import random
import numpy as np

#the info packet delivered to this algorithm contains the following datapoints:
#main building level, warehouse level, granary level
#average field level by resource type
#current stored resources
#turn

#for each item on this data packet, we will store 4 variables, referred to as ax, bx, cx, dx
#example - input value = 5. a1 = 2.4, a2 = 1.02, a3 = 0.85, dx = 0.5
#output = (2.4*(5^1.02))^0.85 + 0.5
#but these shall simply be stored as [2.4, 1.02, 0.85, 0.5.....]

#given there are 12 input variables, this means we have 48 values per gene
#we shall generate 7 genes, such that each possible output (main building, warehouse, granary, 4 fields)
#can be given their own output
#this means our chromosome will contain 336 values. genes are arbitrary, and will be derived in calculation



class Genetic_Generic_1(baseclass.Underlying_Hardcoded):
    def __init__(self, owning_player, chromosome):
        super().__init__(owning_player)
        self.name = "Genetic-Generic99"
        self.chromosome = chromosome
        #temporary one to allow for easy shuffling of genes to the self.genes
        self.temporary_chromosome = chromosome
        self.genes = {"main_building": 0, "warehouse": 0, "granary": 0, "Wood": 0, "Clay": 0,
                      "Iron": 0, "Crop": 0}

        for key in self.genes:
            holder_set = self.temporary_chromosome[:48]
            self.temporary_chromosome = self.temporary_chromosome[48:]
            final_output = np.array_split(holder_set, 12)

            self.genes[key] = final_output

        #this should now be have a nice cleanly sorted set of outputs to make life easier

###this is the old evaluate utility function, left in in case reversion required
    #however, it will not work until the info packet is reverted to its old functionality

    # def evaluate_utility(self, building, info_packet):
    #
    #
    #     #find the buildings:
    #     if len(building) == 3:
    #         if building[0] == 0:
    #             key = "main_building"
    #         elif building[0] == 1:
    #             key = "warehouse"
    #         elif building[0] == 2:
    #             key = "granary"
    #         else:
    #             raise ValueError("I'm not sure what this building I encountered is??")
    #     else:
    #         key = building[0][:4]
    #
    #     active_gene = self.genes[key]
    #
    #     predicted_utility = 0
    #     for iterator in range(len(info_packet)):
    #         #list required because it's a numpy array which doesn't iterate properly otherwise
    #         gene_subset = list(active_gene[iterator])
    #         partial_val = ((gene_subset[0] * (info_packet[iterator]**gene_subset[1]))**gene_subset[2]) + gene_subset[3]
    #         predicted_utility += partial_val
    #
    #     return predicted_utility

    def evaluate_utility(self, building, info_packet):

        #modification to get the new correct info packet
        info_packet2 = info_packet[0]

        # find the buildings:
        if len(building) == 3:
            if building[0] == 0:
                key = "main_building"
            elif building[0] == 1:
                key = "warehouse"
            elif building[0] == 2:
                key = "granary"
            else:
                raise ValueError("I'm not sure what this building I encountered is??")
        else:
            key = building[0][:4]

        active_gene = self.genes[key]

        predicted_utility = 0
        for iterator in range(len(info_packet2)):
            # list required because it's a numpy array which doesn't iterate properly otherwise
            gene_subset = list(active_gene[iterator])
            partial_val = ((gene_subset[0] * (info_packet2[iterator] ** gene_subset[1])) ** gene_subset[2]) + \
                          gene_subset[3]
            predicted_utility += partial_val

        return predicted_utility

#this is a copy of the old select building function
#retained in case needed, but superseded by the below
    # def select_building(self, all_possible, info_packet):
    #
    #
    #     current_best = 0
    #     current_choice = 0
    #     #setting this as negative 42 because buildings start at level 0 and i need to compare
    #     current_level = -42
    #     for building in all_possible:
    #         utility_val = self.evaluate_utility(building, info_packet)
    #         if utility_val >= current_best:
    #             if current_level != -42:
    #                 if building[-1] < current_level:
    #                     current_best = utility_val
    #                     current_choice = building
    #                     current_level = building[-1]
    #             else:
    #                 current_best = utility_val
    #                 current_choice = building
    #                 current_level = building[-1]
    #
    #     #control for cases where it defaults to a value of 0
    #     if current_choice == 0:
    #         chosen_action = random.choice(all_possible)
    #     else:
    #         chosen_action = current_choice
    #
    #     return chosen_action

    def select_building(self, all_possible, info_packet):

        all_buildings = info_packet[2]
        current_yields = info_packet[1]
        current_stored = info_packet[0][7:11]

        current_best = 0
        current_choice = 0
        # setting this as negative 42 because buildings start at level 0 and i need to compare
        current_level = -42
        for building in all_buildings:
            utility_val = self.evaluate_utility(building[0], info_packet)
            if current_choice == 0:
                current_best = utility_val
                current_choice = building
                current_level = building[0][-1]
            elif utility_val >= current_best:
                if len(building[0]) == 3:
                    keycheck = building[0][1]
                else:
                    keycheck = building[0][0][:4]
                if current_choice == 0:
                    current_keycheck = "Fish"
                elif len(current_choice[0]) == 3:
                    current_keycheck = current_choice[0][1]
                else:
                    current_keycheck = current_choice[0][0][:4]
                if keycheck != current_keycheck:
                    if building[0][-1] < current_level:
                        current_best = utility_val
                        current_choice = building
                        current_level = building[0][-1]

        #if our chosen action is possible, then that's fine, we can just use that
        #however, otherwise, we'll need to work out how long it will take for it to be possible

        #control for if somehow nothing was found
        control_triggered = False
        if current_choice == 0:
            chosen_action = random.choice(all_possible)
            control_triggered = True

        #check for if its a currently possible buiding
        if not control_triggered:
            if current_choice[0] in all_possible:
                currently_possible = True
            else:
                currently_possible = False

            #if its currently possible
            if currently_possible:
                chosen_action = current_choice[0]
            #if its not
            else:
                time_list = []
                for i in range(len(current_yields)):
                    current_res = current_stored[i]
                    required_res = current_choice[1][i]
                    current_yield = current_yields[i]
                    if current_res > required_res:
                        time2 = 0
                    else:
                        diff = required_res - current_res
                        time = diff/current_yield
                        time2 = int(time) + 1
                    time_list.append(time2)
                max_time = max(time_list)

                chosen_action = ["None", max_time, max_time, max_time]

                #control for if all items are 0
                #this happens because you want to upgrade something, but don't have the crop to do so
                #it isn't possible, because it would put you in negative crop

                ##addendum - this clearly isn't possible
                #so if you get a zero for some reason, just randomly pick something
                if max_time == 0:
                    chosen_action_temp = 0
                    for building in all_possible:
                        if len(building) == 2:
                            key = building[0][0][:4]
                            if key == 'Crop':
                                chosen_action_temp = building
                    if chosen_action_temp == 0:
                        chosen_action = random.choice(all_possible)


        return chosen_action
