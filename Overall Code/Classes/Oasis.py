
import Classes.Location_Square_Classes as loc_sq
import random

class Oasis(loc_sq.Square):
    def __init__(self, location):
        super().__init__(location)
        self.type_square = 'oasis'
        self.interactable = True
        self.resources = []
        # type one addition
        randval = random.randint(0, 100)
        if randval < 25:
            self.resources.append('wood')
        elif randval < 50:
            self.resources.append('clay')
        elif randval < 75:
            self.resources.append('iron')
        elif randval <= 100:
            self.resources.append('crop')
        randval = random.randint(0 ,100)
        if randval > 80:
            self.resources.append('crop')
        # now define the storage
        self.storage = []
        if 'wood' in self.resources:
            self.storage.append([3600, 3600])
        else:
            self.storage.append([1800, 1800])
        if 'clay' in self.resources:
            self.storage.append([3600, 3600])
        else:
            self.storage.append([1800, 1800])
        if 'iron' in self.resources:
            self.storage.append([3600, 3600])
        else:
            self.storage.append([1800, 1800])
        if 'crop' in self.resources:
            self.storage.append([3600, 3600])
        else:
            self.storage.append([1800, 1800])

        self.zoo = [30, 20, 10]
        self.next_action = False
    def next_update(self):
        if self.next_action == False:
            wait_duration = True
        else:
            wait_duration = self.next_action
        return wait_duration

