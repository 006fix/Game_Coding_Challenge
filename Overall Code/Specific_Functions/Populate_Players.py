
import Classes.Player as player
import Base_Data.Players_Data as player_data
import Classes.AI_Classes.Rudimentary_AI as ai


def populate_players():
    for i in range(len(player_data.player_list)):
        key = player_data.player_list[i]
        holdval = ai.Rudimentary_AI(player_data.player_list[i], player_data.loc_list[i], player_data.race_list[i])
        player_data.player_dict[key] = holdval

#where is this used?
def update_player_dict():
    for key in player_data.holder_dict:
        holder = player_data.holder_dict[key]
        holder2 = [holder]
        player_data.player_dict[key].villages = holder2
        player_data.player_dict[key].location = 'None'
