
import Classes.Location_Square_Classes as loc_sq
import Classes.Fields as fields
import random

class Habitable(loc_sq.Square):
    # make sure the default classes go at the end
    def __init__(self, location):
        super().__init__(location)
        self.interactable=True
        self.type_square = 'habitable'

        # default buildings,overwritten if inhabited
        self.buildings = {'main building': 1}
        # add more later

        randval = random.randint(0, 100)
        if randval < 10:
            self.type_hab = [1, 1, 1, 15]
        elif randval < 25:
            self.type_hab = [3, 3, 3, 9]
        elif randval < 35:
            self.type_hab = [4, 3, 4, 7]
        elif randval < 45:
            self.type_hab = [4, 4, 3, 7]
        elif randval < 55:
            self.type_hab = [3, 4, 4, 7]
        else:
            self.type_hab = [4, 4, 4, 6]

        # now we expand this out a bit, to create the fields
        # fields occur in list, wood,clay,iron,crop
        # we're using lists above so we can iterate through them to create
        # without doing this seperately dependent on the type above
        field_list = ['Wood', 'Clay', 'Iron', 'Crop']
        self.field_list_dict = {}
        for i in range(len(self.type_hab)):
            for j in range(1, self.type_hab[i] + 1):
                key = field_list[i] + str(j)
                holdval = fields.Field(field_list[i])
                self.field_list_dict[key] = holdval

        self.next_action = False

    def next_update(self):
        if self.next_action == False:
            wait_duration = True
        else:
            wait_duration = self.next_action
        return wait_duration