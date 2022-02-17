
#base class used as generic structure for all hardcoded AI's

#test

class Underlying_Hardcoded():
    def __init__(self, owning_player):
        self.owning_player = owning_player

    def select_building(self):
        #this function just exists to be overwritten, but if it isn't overwritten, will throw an error
        raise ValueError("Why are you calling the generic version of the select building category???")

    # from here, I may need to insert additional features for the generic AI classes
    # but for now, I can't actually think of anything.



