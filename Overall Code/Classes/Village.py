
import Classes.Location_Square_Classes as loc_sq
import Base_Data.Building_Data as building_data
import Base_Data.Fields_Data as fields_data
import Generic_Functions_Basic.All_Generic as generic_funcs
import random

class Village(loc_sq.Square):
    def __init__(self, location, type_hab, field_list_dict, owner, type_square='village'):
        super().__init__(location)
        self.location = location
        self.interactable = True
        self.type_hab = type_hab
        self.fields = field_list_dict
        self.type_square = type_square
        self.owner = owner
        self.buildings = {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '',
                          9: '', 10: '', 11: '', 12: '', 13: '', 14: '', 15: '', 16: '',
                          17: '', 18: '', 19: '', 20: '', 21: '', 22: ''}
        #structure of the below - reference key for buildings_dict lookup, level, upgradeable bool.
        self.buildings[0] = ['main_building', 1, True]
        self.buildings[1] = ['warehouse1', 0, True]
        self.buildings[2] = ['granary1', 0, True]
        #SORT THESE OUT LATER
        #self.buildings[22] = ['wall', 0, True]
        #self.buildings[21] = ['rally_point', 0, True]

        self.storage_cap = [800, 800, 800, 800]

        #just going to briefly randomise this so players act at different times
        base_value = random.randint(5, 200)
        self.stored = [base_value, base_value, base_value, base_value]
        #uncomment this later to restore functionality
        #self.stored = [5, 5, 5, 5]

        #this is the storage for anything you're currently building, in sequential order
        #for now we'll only allow one upgrade
        self.currently_upgrading = []

        #this is going to be used to store unbuilt buildings, once possible
        #for now, it's simply an empty holder
        self.unbuilt = []


        ##HOLDER VALUES FOR POPULATION AND CP
        self.pop = 0
        self.cp = 0

        #HOLDER VALUES FOR MAIN BUILDING UPGRADE TIME
        #this will need to be modified based on main building level
        self.upgrade_time_modifier = 1



    def modify_building_time(self):
        main_building_key = self.buildings[0][0]
        main_building_level = self.buildings[0][1]
        building_time = building_data.building_dict[main_building_key][main_building_level][4]
        self.upgrade_time_modifier = building_time

    def calculate_storage(self):
        warehouse_storage = 0
        granary_storage = 0
        for key in self.buildings:
            holder = self.buildings[key]
            #check if its empty
            if len(holder) > 0:
                if 'warehouse' in holder[0]:
                    level = holder[1]
                    storage = building_data.building_dict['warehouse'][level][4]
                    warehouse_storage += storage
                if 'granary' in holder[0]:
                    level = holder[1]
                    storage = building_data.building_dict['granary'][level][4]
                    granary_storage += storage
        self.storage_cap = [warehouse_storage, warehouse_storage, warehouse_storage, granary_storage]

    def calculate_pop(self):
        total_pop = 0
        #calculate pop from buildings
        for key in self.buildings:
            holder = self.buildings[key]
            #check if its empty
            if len(holder) > 0:
                building = holder[0]
                #controls for buildings that can duplicate
                if 'warehouse' in building:
                    building = 'warehouse'
                if 'granary' in building:
                    building = 'granary'
                level = holder[1]
                pop = building_data.building_dict[building][level][2]
                total_pop += pop
        for key in self.fields:
            pop = self.fields[key].pop
            total_pop += pop
        self.pop = total_pop

    def calculate_cp(self, game_counter, self_last_active):
        total_cp = 0
        #calculate pop from buildings
        for key in self.buildings:
            holder = self.buildings[key]
            #check if its empty
            if len(holder) > 0:
                building = holder[0]
                #controls for buildings that can duplicate
                if 'warehouse' in building:
                    building = 'warehouse'
                if 'granary' in building:
                    building = 'granary'
                level = holder[1]
                cp = building_data.building_dict[building][level][1]
                total_cp += cp
        for key in self.fields:
            pop = self.fields[key].cp
            total_cp += cp
        local_duration_slept = game_counter - self_last_active
        #86400 = seconds in a day
        cp_per_sec = total_cp / 86400
        cp_gained = cp_per_sec * local_duration_slept
        current_cp = self.cp
        self.cp = current_cp + cp_gained



    def yield_calc(self):
        wood_yield = 0
        clay_yield = 0
        iron_yield = 0
        crop_yield = 0
        crop_usage = 0
        for key3 in self.fields:
            if 'Wood' in key3:
                wood_yield += self.fields[key3].field_yield / 3600
                crop_usage += self.fields[key3].pop / 3600
            if 'Clay' in key3:
                clay_yield += self.fields[key3].field_yield / 3600
                crop_usage += self.fields[key3].pop / 3600
            if 'Iron' in key3:
                iron_yield += self.fields[key3].field_yield / 3600
                crop_usage += self.fields[key3].pop / 3600
            if 'Crop' in key3:
                crop_yield += self.fields[key3].field_yield / 3600
                crop_usage += self.fields[key3].pop / 3600
        #now reduce crop yield by crop usage
        #######WARNING WARNING WARNING WARNING WARNING
        #THIS DOES NOT CALCULATE CROP USAGE BY OTHER BUILDINGS
        #DO THAT SOON
        #
        #
        #
        #
        #

        crop_yield -= crop_usage
        # now we've got the full yields out, so multiply by time passed
        yields = [wood_yield, clay_yield, iron_yield, crop_yield]
        return yields


    def possible_buildings(self):
        possible_buildings = [[], []]
        for key in self.buildings:
            # this bottom one is simply for now, since i've put those holders in
            # remove this whole step later
            holdval = self.buildings[key]
            #THIS IS ALSO JUST TO STOP IT BREAKING FROM THE NULL VALUES
            #but maybe keep long term?
            if len(holdval) > 1:
                holdval_level = holdval[1]
                #if upgradeable
                if holdval[2] == True:
                    keyval = holdval[0]
                    #controls for buildings that can dupe
                    if 'warehouse' in keyval:
                        keyval = 'warehouse'
                    if 'granary' in keyval:
                        keyval = 'granary'
                    #HOW DO I KNOW THE BUILDINGS LEVEL?
                    upgrade_cost = building_data.building_dict[keyval][holdval_level][0]
                    #BOTH ARE REQUIRED, BECAUSE IF COND1-4 ARE TRUE, BUT COND5-8 AREN'T, IT'S A FUTURE POSSIBLE
                    #WORK IT OUT LATER
                    #print(f"My upgrade cost is {upgrade_cost}")
                    #print(f"My storage cap is {self.storage_cap}")
                    cond1 = upgrade_cost[0] < self.storage_cap[0]
                    cond2 = upgrade_cost[1] < self.storage_cap[1]
                    cond3 = upgrade_cost[2] < self.storage_cap[2]
                    cond4 = upgrade_cost[3] < self.storage_cap[3]
                    cond5 = upgrade_cost[0] <= self.stored[0]
                    cond6 = upgrade_cost[1] <= self.stored[1]
                    cond7 = upgrade_cost[2] <= self.stored[2]
                    cond8 = upgrade_cost[3] <= self.stored[3]
                    if cond1 and cond2 and cond3 and cond4 and cond5 and cond6 and cond7 and cond8:
                        #builings go in list 1
                        #passed as a two part list, to provide the key and the name
                        final_value = [key, holdval[0]]
                        possible_buildings[0].append(final_value)
        for key in self.fields:
            holdval = self.fields[key]
            holdval_level = holdval.level
            key2 = key[:4]
            upgrade_cost = fields_data.field_dict[key2][holdval_level][0]
            cond1 = upgrade_cost[0] < self.storage_cap[0]
            cond2 = upgrade_cost[1] < self.storage_cap[1]
            cond3 = upgrade_cost[2] < self.storage_cap[2]
            cond4 = upgrade_cost[3] < self.storage_cap[3]
            cond5 = upgrade_cost[0] <= self.stored[0]
            cond6 = upgrade_cost[1] <= self.stored[1]
            cond7 = upgrade_cost[2] <= self.stored[2]
            cond8 = upgrade_cost[3] <= self.stored[3]
            #new condition added here, since the upgradeability of the fields is stored seperately
            if len(upgrade_cost) > 1 and cond1 and cond2 and cond3 and cond4 and cond5 and cond6 and cond7 and cond8:
                #fields go in list two
                possible_buildings[1].append(key)
        return possible_buildings

    #using the seperate lists, allow for upgrading of a building.
    #if decided to upgrade a building, use this
    def upgrade_building(self, upgrade_target):
        building_dict_key = upgrade_target[0]
        relevant_target = self.buildings[building_dict_key]
        current_level = relevant_target[1]
        upgradeable_check = relevant_target[2]
        if upgradeable_check != True:
            print(f" You are upgrading {upgrade_target}")
            raise ValueError("You appear to have attempted to upgrade a building that cannot be upgraded :(")
        #from the above we have some basic data, but we need a subset of the name to actually link
        #to the building data field, due to duplicate buildings. This follows:
        building_data_key = upgrade_target[1]
        if 'warehouse' in building_data_key:
            building_data_key = 'warehouse'
        if 'granary' in building_data_key:
            building_data_key = 'granary'
        #now get upgrade costs
        upgrade_cost = building_data.building_dict[building_data_key][current_level][0]
        #THIS NEEDS MODIFICATION FOR THE MAIN BUILDING LEVEL
        upgrade_time = building_data.building_dict[building_data_key][current_level][3]
        true_upgrade_time = int(generic_funcs.sec_val(upgrade_time) * self.upgrade_time_modifier)
        #now update how many resources you have on hand
        hold_vals = self.stored
        for i in range(len(hold_vals)):
            hold_vals[i] -= upgrade_cost[i]
        self.stored = hold_vals
        self.currently_upgrading.append(upgrade_target)

        # variables to be returned
        # do i need any more?
        sleep_duration = true_upgrade_time
        return sleep_duration



    #if decided to upgrade a field, use this
    def upgrade_field(self, upgrade_target):

        field_data = self.fields[upgrade_target]
        field_dict_key = upgrade_target[:4]

        current_level = field_data.level
        upgradeable_check = field_data.upgradeable
        if upgradeable_check != True:
            print(f"you are upgrading {upgrade_target}")
            raise ValueError("You appear to have attempted to upgrade a field that cannot be upgraded :(")
        upgrade_cost = fields_data.field_dict[field_dict_key][current_level][0]
        # THIS NEEDS MODIFICATION TO ALLOW FOR MAIN BUILDING LEVEL
        upgrade_time = fields_data.field_dict[field_dict_key][current_level][3]
        true_upgrade_time = int(generic_funcs.sec_val(upgrade_time) * self.upgrade_time_modifier)
        # update what is currently stored as resources
        hold_vals = self.stored
        for i in range(len(hold_vals)):
            hold_vals[i] -= upgrade_cost[i]
        self.stored = hold_vals
        self.currently_upgrading.append(upgrade_target)


        # variables to be returned
        # do i need any more?
        sleep_duration = true_upgrade_time
        return sleep_duration

    def building_upgraded(self, upgrade_target):
        #THIS IS STILL JUST THE FIELD VERSION, REMEMBER TO CHANGE IT
        building_dict_key = upgrade_target[0]
        relevant_target = self.buildings[building_dict_key]
        current_level = relevant_target[1]
        upgradeable_check = relevant_target[2]
        if upgradeable_check != True:
            print(f" You are upgrading {upgrade_target}")
            raise ValueError("You appear to have attempted to upgrade a building that cannot be upgraded :(")
        #now get the key for the building data file
        building_data_key = upgrade_target[1]
        if 'warehouse' in building_data_key:
            building_data_key = 'warehouse'
        if 'granary' in building_data_key:
            building_data_key = 'granary'

        #used to check if the new building is upgradeable
        level_plusone = current_level + 1
        still_upgradeable = building_data.building_dict[building_data_key][level_plusone][0]
        if still_upgradeable[0] == False:
            upgrade_possible = False
        else:
            upgrade_possible = True
        # used to update the villages building list with the new level and upgradeability

        #NEW FUNCTION THAT UPDATES THE STATS OF THE FIELD ONCE ITS UPGRADED
        #update self is called in rudimentary ai will_i_act file, so no need for the below
        #field_data.update_stats()

        #NOW WE NEED TO RESET THE SELF.BUILDINGS KEY TO ACCOUNT FOR EVERYTHING
        self.buildings[building_dict_key][1] = level_plusone
        self.buildings[building_dict_key][2] = upgrade_possible


        #LATER, THIS WILL NEED TO BE CHANGED TO BE A SIMPLE REMOVAL OF THE 0TH INDEX
        self.currently_upgrading = []

        print(f"I have completed my upgrade of the building {upgrade_target}. It has upgraded from {current_level} to {level_plusone}")


    def field_upgraded(self, upgrade_target):

        field_data = self.fields[upgrade_target]
        field_dict_key = upgrade_target[:4]

        current_level = field_data.level
        #lets just make sure the original field was actually upgradeable
        upgradeable_check = field_data.upgradeable
        if upgradeable_check != True:
            raise ValueError("You appear to have attempted to upgrade a field that cannot be upgraded :(")

        #used to check if the new building is upgradeable
        #for fields in non capital, this will eventually need to cap at 10 in some way
        level_plusone = current_level + 1
        still_upgradeable = fields_data.field_dict[field_dict_key][level_plusone][0]
        if still_upgradeable[0] == False:
            upgrade_possible = False
        else:
            upgrade_possible = True
        # used to update the villages building list with the new level and upgradeability

        #NEW FUNCTION THAT UPDATES THE STATS OF THE FIELD ONCE ITS UPGRADED
        field_data.update_stats()


        fields_data.upgradeable = upgrade_possible

        #LATER, THIS WILL NEED TO BE CHANGED TO BE A SIMPLE REMOVAL OF THE 0TH INDEX
        self.currently_upgrading = []

        print(f"I have completed my upgrade of field {upgrade_target}. It has upgraded from {current_level} to {level_plusone}")