
import Specific_Functions.Village_Creation as vil_creation
import random


class Player:
    def __init__(self, name, quadrant, race,
                 population=0, attack_points=0, defence_points=0, raid_points=0, culture_points=0, villages = []):
        self.name = name
        self.quadrant = quadrant
        self.race = race
        self.culture_points = culture_points
        self.population = population
        self.attack_points = attack_points
        self.defence_points = defence_points
        self.raid_points = raid_points
        self.villages = villages
        self.location = 'None'
        self.Last_Active = 0
        self.Sleep = False


        #the below should probably turn into a function at some point

        if self.quadrant[0] == '+':
            loop1 = True
            if self.quadrant[1] == '+':
                loop2 = True
                output = vil_creation.Can_i_make_a_village(loop1, loop2, self.name)
            else:
                loop2 = False
                output = vil_creation.Can_i_make_a_village(loop1, loop2, self.name)
        else:
            loop1 = False
            if self.quadrant[1] == '+':
                loop2 = True
                output = vil_creation.Can_i_make_a_village(loop1, loop2, self.name)
            else:
                loop2 = False
                output = vil_creation.Can_i_make_a_village(loop1, loop2, self.name)
        self.location = output

        self.next_action = False
        #now add a trial so that we can see if we can vary this, and there will be variance in how long they wait

        self.next_action = 5000

    def next_update(self):
        #whats this first step meant to do exactly?
        if self.next_action == False:
            wait_duration = True
        else:
            wait_duration = self.next_action
        return wait_duration