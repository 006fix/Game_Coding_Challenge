
import Classes.Player as player
import Classes.Village as village
import Base_Data.map_data as map_data
import Base_Data.Building_Data as building_data
import random
import Base_Data.Leaderboard_Data as leaderboard


class Rudimentary_AI(player.Player):
    def __init__(self, name, quadrant, race,
                 population=0, attack_points=0, defence_points=0, raid_points=0, culture_points=0,
                 villages=[], AI_type = 'generic'):
        super().__init__(name, quadrant, race,
                    population=0, attack_points=0, defence_points=0, raid_points=0, culture_points=0, villages=[])

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
            self.next_action = 20000  #wait a little while then check again
        print(f"player {self.name} will awaken in {self.next_action} seconds")

    #THIS IS THE FUNCTION THAT CHECKS IF AN UPDATE IS REQUIRED
    #logic - if asleep, pass
    #
    def will_i_act(self, game_counter, global_last_active, calc_leaderboard):
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
                    if len(all_possible) > 0:
                        chosen_action = random.choice(all_possible)
                        print(f"I, player {self.name} have chosen to upgrade {chosen_action}")

                    #NOW WE'VE CHOSEN SOMETHING TO UPGRADE
                    ##BUT IS IT A BUILDING, OR A FIELD?
                    #we'll use "if in buildings then building else field" to handle this

                        if chosen_action in possible_buildings:
                            chosen_action_type = 'building'
                        elif chosen_action in possible_fields:
                            chosen_action_type = 'field'
                        else:
                            raise ValueError(f"I'm afraid I don't recognise what you're trying to upgrade!!!!")

                    #initiate the upgrade
                    #BUT ONLY IF THERE'S NOTHING CURRENTLY UPGRADING
                    if len(active_village.currently_upgrading) == 0:
                        if len(all_possible) > 0:
                            reset_time = True
                            #here we need to vary by chosen_action_type
                            if chosen_action_type == 'building':
                                #we return both parts of the 2 part key, so we can distinguish fields and buildings
                                wait_time = active_village.upgrade_building(chosen_action[:2])
                            elif chosen_action_type == 'field':
                                wait_time = active_village.upgrade_field(chosen_action[0])
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


        self_data = [self.name, self_pop, self_cp, self.attack_points, self.defence_points, self.raid_points,
                     self_resources, aggregate_income, perc_stored]
        leaderboard.leaderboard.append(self_data)

        return true_wait_time





