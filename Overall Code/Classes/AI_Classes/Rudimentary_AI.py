
import Classes.Player as player
import Classes.Village as village
import Base_Data.map_data as map_data
import random


class Rudimentary_AI(player.Player):
    def __init__(self, name, quadrant, race,
                 population=0, attack_points=0, defence_points=0, raid_points=0, culture_points=0,
                 villages=[], AI_type = 'generic'):
        super().__init__(name, quadrant, race,
                    population=0, attack_points=0, defence_points=0, raid_points=0, culture_points=0, villages=[])

    #THIS IS THE GENERIC "REFRESH YOURSELF TO THE PRESENT TIME" FUNCTION
    def update_self(self):
        pass

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
    def will_i_act(self, game_counter, global_last_active):

        #this is set to null, but if the player takes a new action it will be used to reset time
        reset_time = False

        #main function starts
        if self.Sleep == False:
            duration_slept = game_counter - global_last_active
            local_duration_slept = game_counter - self.Last_Active
            if duration_slept == self.next_action:
                print(f"Player {self.name} is ready to take an action")
                print(f" the last active time for the player is {self.Last_Active}")
                #now reset the last active value to the current time
                self.Last_Active = game_counter
                #at a later date, it may be necessary to return multiple wait times
                #so for now, we'll replicate that structure and return a list of times
                wait_time_list = []
                for village in self.villages:
                    #ITERATE THROUGH VILLAGES, THEN FOR EACH ACTIVE ONE:
                    active_village = map_data.map_dict[village]
                    #how many resources have I gained, update totals
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
                    #COMPLETION OF UPDATING RESOURCES

                    #CHECK TO SEE IF YOU HAD A BUILDING YOU WERE UPGRADING
                    if len(active_village.currently_upgrading) > 0:
                        upgraded_building = active_village.currently_upgrading[0]
                        print(f"I, player {self.name} have just finished upgrading {upgraded_building}")
                        active_village.field_upgraded(upgraded_building)
                        # now we need to reset this back to an empty list
                        # this lets our timer restart
                        self.reset_next_action([])

                    #NOW WE NEED TO USE SOME MORE CODE - LATER THIS SHOULD BE SPLIT OUT INTO A SEPERATE FUNCTION
                    #BUT LETS MAKE SURE IT ALL WORKS NOW

                    possible_actions = active_village.possible_buildings()
                    print(f"I, player {self.name}, have several possible actions - the buildings I can currently upgrade are as follows:")
                    print(possible_actions)

                    #find possible fields to upgrade
                    possible_fields = possible_actions[1]

                    #select a field
                    if len(possible_fields) > 0:
                        chosen_action = random.choice(possible_fields)
                        print(f"I, player {self.name} have chosen to upgrade {chosen_action}")

                    #initiate the upgrade
                    #BUT ONLY IF THERE'S NOTHING CURRENTLY UPGRADING
                    if len(active_village.currently_upgrading) == 0:
                        if len(possible_fields) > 0:
                            reset_time = True
                            wait_time = active_village.upgrade_field(chosen_action)
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

        return true_wait_time





