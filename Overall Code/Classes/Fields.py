import Generic_Functions_Basic.All_Generic as generic_funcs
import Base_Data.Fields_Data as f_data

class Field():
    # REMOVE MAIN BUILDING DEFAULT LATER
    # do i import main building?
    def __init__(self, type_field, upgradeable=True, level=0):
        # super high level stuff goes here
        self.type_field = type_field
        self.level = level
        # lower level stuff goes here:
        self.upgrade_cost = f_data.field_dict[self.type_field][self.level][0]
        self.field_yield = int(f_data.field_dict[self.type_field][self.level][4])
        self.cp = int(f_data.field_dict[self.type_field][self.level][1])
        self.pop = int(f_data.field_dict[self.type_field][self.level][2])
        self.upgrade_time = int(generic_funcs.sec_val(f_data.field_dict[self.type_field][self.level][3]))
        self.upgradeable = upgradeable

    def update_stats(self):
        holdval = self.level
        self.level = holdval + 1
        #now level is ugraded, the level can be used below
        self.cp = int(f_data.field_dict[self.type_field][self.level][1])
        self.pop = int(f_data.field_dict[self.type_field][self.level][2])
        self.upgrade_time = int(generic_funcs.sec_val(f_data.field_dict[self.type_field][self.level][3]))
        self.upgrade_cost = f_data.field_dict[self.type_field][self.level][0]
        self.field_yield = int(f_data.field_dict[self.type_field][self.level][4])