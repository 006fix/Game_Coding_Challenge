
import Classes.Player as player
import Classes.Village as village
import Base_Data.map_data as map_data
import Base_Data.Building_Data as building_data
import random
import Base_Data.Leaderboard_Data as leaderboard
import Classes.AI_Classes.Hardcoded_AI.AI_selection as AI_selection


class Rudimentary_AI(player.Player):
    def __init__(self, name, quadrant, race, chromosome,
                 population=0, attack_points=0, defence_points=0, raid_points=0, culture_points=0,
                 villages=[], AI_type = 'generic'):
        super().__init__(name, quadrant, race,
                    population=0, attack_points=0, defence_points=0, raid_points=0, culture_points=0, villages=[])
        ##insertion of the AI class chosen will go here, in the instantiation of the rudimentary ai class
        ai_seed_topval = AI_selection.numeric_ai_possibles
        ai_seed = random.randint(0, ai_seed_topval)


        ##genetic algorithm testing modification
        #self.AI = AI_selection.provide_ai(ai_seed, self.name)
        #further modification to run genetic algorithms
        #self.AI = AI_selection.provide_ai_gentest(ai_seed, self.name)
        self.AI = AI_selection.provide_ai_genloop(chromosome, self.name)

        #new functions to provide turn counts, and dictionary of all completed actions
        self.turn_count = 1
        self.building_history = {}


    #THIS IS THE GENERIC "REFRESH YOURSELF TO THE PRESENT TIME" FUNCTION
    #time is required to allow for cp calculations
    #do i need anything else beyond storage, pop, cp?
    #either way, this needs to be called every single time the player is directly called
    ####BUT, it can also be called without the player waking themselves up
    def update_self(self, game_counter):
        local_duration_slept = game_counter - self.Last_Active
        for village in self.villages:
            active_village = map_data.map_dict[village]
            # update building time
            active_village.modify_building_time()
            # update storage
            active_village.calculate_storage()
            # update pop
            active_village.calculate_pop()
            # update cp
            self_last_active = self.Last_Active
            active_village.calculate_cp(game_counter, self_last_active)
            #update yields
            resources_gained = active_village.yield_calc()
            for i in range(len(resources_gained)):
                resources_gained[i] *= local_duration_slept
            current_stockpile = active_village.stored
            current_max = active_village.storage_cap
            for i in range(len(resources_gained)):
                if (resources_gained[i] + current_stockpile[i]) > current_max[i]:
                    current_stockpile[i] = current_max[i]
                else:
                    current_stockpile[i] = resources_gained[i] + current_stockpile[i]
            active_village.stored = current_stockpile
            print(f"for player {self.name}, village {village}, current stockpile is {current_stockpile}")
            resources_per_hour = active_village.yield_calc()
            for i in range(len(resources_per_hour)):
                resources_per_hour[i] *= 3600
            print(f"for player {self.name}, village {village}, current resources generation per hour is {resources_per_hour}")

            # COMPLETION OF UPDATING RESOURCES
        #now we may need to have the ability to handle resets, but in such a way that
        #if needs be, we can "wake" without actually waking up
        self.Last_Active = game_counter




    #THIS IS THE "UPDATE YOUR WAITING TIME" FUNCTION, FOR CALLS OF THE ABOVE
    def waiting_duration(self, action_time):
        pass

    def reset_next_action(self, upgrade_time):
        if upgrade_time != []:
            self.next_action = upgrade_time
        else:
            self.next_action = 2500  #wait a little while then check again
        print(f"player {self.name} will awaken in {self.next_action} seconds")

    #this function will be used by the genetic algorithm, generating an up to date list of all information
    #about the village, and packeting it for later consumption
    def information_packet(self, i):
        #info packets generated :
        #main building level, warehouse level, granary level
        #average field level for each resource type
        #current resources stored for each resource type
        #turn counter (i)

        #we've only got one village for now so just using a 1 loop call
        for village in self.villages:
            active_village = map_data.map_dict[village]

        info_packet = []
        info_packet.append(active_village.buildings[0][1])
        info_packet.append(active_village.buildings[1][1])
        info_packet.append(active_village.buildings[2][1])
        #now fields
        wood_level = 0
        wood_count = 0
        clay_level = 0
        clay_count = 0
        iron_level = 0
        iron_count = 0
        crop_level = 0
        crop_count = 0

        for field in active_village.fields:
            if 'Wood' in field:
                wood_count += 1
                wood_level += active_village.fields[field].level
            if 'Clay' in field:
                clay_count += 1
                clay_level += active_village.fields[field].level
            if 'Iron' in field:
                iron_count += 1
                iron_level += active_village.fields[field].level
            if 'Crop' in field:
                crop_count += 1
                crop_level += active_village.fields[field].level
        wood_av = wood_level/wood_count
        clay_av = clay_level/clay_count
        iron_av = iron_level/iron_count
        crop_av = crop_level/crop_count
        info_packet.append(wood_av)
        info_packet.append(clay_av)
        info_packet.append(iron_av)
        info_packet.append(crop_av)

        stored = active_village.stored
        for res in stored:
            info_packet.append(res)

        info_packet.append(self.turn_count)

        #extra parts for the enhanced info packet
        yields = active_village.yield_calc()
        every_building = active_village.all_buildings()

        info_packet2 = [info_packet, yields, every_building]

        return info_packet2



    #THIS IS THE FUNCTION THAT CHECKS IF AN UPDATE IS REQUIRED
    #logic - if asleep, pass
    #
    def will_i_act(self, game_counter, global_last_active, calc_leaderboard, i):

        #this is set to null, but if the player takes a new action it will be used to reset time
        reset_time = False

        #main function starts
        if self.Sleep == False:
            duration_slept = game_counter - global_last_active
            #the below variable is literally never used - does it still need to exist?
            #is there any kind of use for it?
            local_duration_slept = game_counter - self.Last_Active
            if duration_slept == self.next_action:
                print(f"Player {self.name} is ready to take an action")
                print(f" the last active time for the player is {self.Last_Active}")
                #now reset the last active value to the current time

                #new modification
                #providing a value of true for self_triggered, since
                self.update_self(game_counter)
                #new modification ends
                #at a later date, it may be necessary to return multiple wait times
                #so for now, we'll replicate that structure and return a list of times
                wait_time_list = []
                for village in self.villages:
                    #ITERATE THROUGH VILLAGES, THEN FOR EACH ACTIVE ONE:
                    active_village = map_data.map_dict[village]
                    #updating of resources removed, since handled above

                    #CHECK TO SEE IF YOU HAD A BUILDING YOU WERE UPGRADING
                    if len(active_village.currently_upgrading) > 0:
                        upgraded_building = active_village.currently_upgrading[0]
                        print(f"I, player {self.name} have just finished upgrading {upgraded_building}")
                        #here we need to recognise what was upgraded, and properly account for what it actually was
                        #luckily, buildings return as a 2 part list
                        if isinstance(upgraded_building, list):
                            #if this is true, it's a building
                            active_village.building_upgraded(upgraded_building)
                        else:
                            #if this triggers, its a field
                            active_village.field_upgraded(upgraded_building)
                        # now we need to reset this back to an empty list
                        # this lets our timer restart
                        self.reset_next_action([])
                        #now update yourself again because the buildings have changed
                        #BUT, if its worked properly, the time duration should be zero, so no resources etc should be added
                        self.update_self(game_counter)

                    #NOW WE NEED TO USE SOME MORE CODE - LATER THIS SHOULD BE SPLIT OUT INTO A SEPERATE FUNCTION
                    #BUT LETS MAKE SURE IT ALL WORKS NOW

                    possible_actions = active_village.possible_buildings()
                    print(f"I, player {self.name}, have several possible actions - the buildings I can currently upgrade are as follows:")
                    print(possible_actions)

                    #find possible fields to upgrade
                    possible_buildings = possible_actions[0]
                    possible_fields = possible_actions[1]
                    all_possible = possible_buildings + possible_fields

                    #select a field
                    # new control for if wait value chosen
                    wait_value_chosen = False
                    if len(all_possible) > 0:
                        #print(all_possible)

                        info_packet = self.information_packet(i)
                        chosen_action = self.AI.select_building(all_possible, info_packet)

                        action_key = self.turn_count
                        if len(chosen_action) == 3:
                            action_content = chosen_action[1:]
                        elif len(chosen_action) == 2:
                            action_content = chosen_action
                        else:
                            wait_value_chosen = True
                            action_content = chosen_action[0]
                        self.building_history[action_key] = action_content
                        self.turn_count = action_key + 1

                    #NOW WE'VE CHOSEN SOMETHING TO UPGRADE
                    ##BUT IS IT A BUILDING, OR A FIELD?
                    #we'll use "if in buildings then building else field" to handle this

                        if chosen_action in possible_buildings:
                            chosen_action_type = 'building'
                        elif chosen_action in possible_fields:
                            chosen_action_type = 'field'
                        elif chosen_action[0] == "None":
                            chosen_action_type = 'wait'
                        else:
                            raise ValueError(f"I'm afraid I don't recognise what you're trying to upgrade!!!!")

                    #initiate the upgrade
                    #BUT ONLY IF THERE'S NOTHING CURRENTLY UPGRADING
                    if len(active_village.currently_upgrading) == 0:
                        #modification for if we're waiting for an action
                        if (len(all_possible) > 0) or wait_value_chosen:
                            reset_time = True
                            #here we need to vary by chosen_action_type
                            if chosen_action_type == 'building':
                                #we return both parts of the 2 part key, so we can distinguish fields and buildings
                                wait_time = active_village.upgrade_building(chosen_action[:2])
                            elif chosen_action_type == 'field':
                                wait_time = active_village.upgrade_field(chosen_action[0])
                            elif chosen_action_type == 'wait':
                                wait_time = chosen_action[-1]
                            else:
                                raise ValueError(f"I don't recognise what i'm upgrading here!")
                            wait_time_list.append(wait_time)
                        else:
                            print(f"I, player {self.name} am currently unable to take an action at this time")
                    else:
                        raise ValueError("I appear to have tried to ugrade something, but apparently I already am - why?")

                    #only do the below if youre reseting time from the above subfunction
                    #get the minimum wait time until the player is awoken
                if reset_time == True:
                    true_wait_time = min(wait_time_list)
                    #set the next time they wake up
                    self.reset_next_action(true_wait_time)
                else:
                    #I DONT REALLY KNOW WHY THIS MIGHT BE NECESSARY?
                #BUT I THINK BASICALLY SOMETIMES TIME DOESN'T GET RESET
                    print(f"I, player {self.name}, appear to have been unable to take an action, such that reset_time == True")
                    self.reset_next_action([])
                    true_wait_time = self.next_action


            #THIS ACCOUNTS FOR IF ITS NOT TIME FOR THEM TO WAKE UP YET
            else:
                self.next_action -= duration_slept
                true_wait_time = self.next_action

        #adding in a new function to utilise the calc_leaderboard variable
        #if false, ignore
        #if true, run an update self regardless of any actual game state
        #BUT, this will need to be checked to ensure it doesn't accidentally trigger other functions that affect time
        if calc_leaderboard == True:
            self.update_self(game_counter)
            #new code to update the leaderboard initially
            self_pop = 0
            self_cp = 0
            self_resources = [0, 0, 0, 0]
            perc_stored = [0, 0, 0, 0]
            aggregate_income = 0
            aggregate_over80 = 0
            #for now, just write out of the self.attack/defenece/raid - later these will need to be updates
            attack = self.attack_points
            defence = self.defence_points
            raid_points = self.raid_points
            for village in self.villages:
                active_village = map_data.map_dict[village]
                #get_pop
                vil_pop = active_village.pop
                # get_cp
                vil_cp = active_village.cp
                self_pop += vil_pop
                self_cp += vil_cp
                income = active_village.yield_calc()
                for res_type in range(len(income)):
                    self_resources[res_type] += income[res_type]
                storage_cap = active_village.storage_cap
                current_resources = active_village.stored
                #now get % storage utilised
                #LOCAL ONLY
                for checking_caps in range(len(current_resources)):
                    perc_usage = current_resources[checking_caps] / storage_cap[checking_caps]
                    perc_stored[checking_caps] = perc_usage
                for zz in range(len(current_resources)):
                    aggregate_income += income[zz]


            self_data = [self.name, self.AI.name, self_pop, self_cp, self.attack_points, self.defence_points, self.raid_points,
                         self_resources, aggregate_income, perc_stored]
            leaderboard.leaderboard.append(self_data)

        return true_wait_time





