
import Specific_Functions.Map_Creation as map_creation
import Specific_Functions.Populate_Players as populate_players
import Game_State_Progression.Game_State_Progression as move_time


#below just so i can easily see it
import Base_Data.map_data as map_data

#trial


#create the base map
map_creation.map_creation()
#modify the base map to include oasis, wilderness, habitable
map_creation.modify_base_map()

#import a list of trial players
populate_players.populate_players()
#update the player dict with their new village locations
populate_players.update_player_dict()

#now lets try running time
for i in range(100):
    move_time.simulate_time()

print(move_time.game_counter)

#test comment to confirm update to github


####FOR NOW, THIS IS NEVER GOING TO WORK FOR MULTIPLE PLAYERS
#BECAUSE IT HAS NO WAY OF SUBTRACTING THE TIME PASSED FROM THE OTHER PLAYERS
#I THINK?

