
import Base_Data.map_data as map_data
import Classes.Location_Square_Classes as loc_sq
import Classes.Habitable as habitable
import Classes.Oasis as oasis

map_dict = {}

def map_creation():
    for x in range(map_data.map_xmin, map_data.map_xmax +1):
        for y in range(map_data.map_ymin, map_data.map_ymax +1):
            locval = [x ,y]
            dict_key = str(locval)
            map_data.map_dict[dict_key] = loc_sq.Square(locval)

def modify_base_map():
    for key in map_data.map_dict:
        value = map_data.map_dict[key]
        if value.type_square == 'wilderness':
            #value.interactable = False
            #above is now redunant
            pass
        if value.type_square == 'habitable':
            new_obj = habitable.Habitable(key)
            map_data.map_dict[key] = new_obj
        if value.type_square == 'oasis':
            new_obj = oasis.Oasis(key)
            map_data.map_dict[key] = new_obj