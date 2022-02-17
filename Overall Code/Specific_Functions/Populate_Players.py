
import Classes.Player as player
import Base_Data.Players_Data as player_data
import Classes.AI_Classes.Rudimentary_AI as ai


def populate_players(num_players, chromosomes):
    player_list, loc_list, race_list = player_data.create_players(num_players)
    for i in range(num_players):
        key = player_list[i]
        #control for if len(chromosome = 0
        if chromosomes == 0:
            chromosome = 0
        else:
            chromosome = chromosomes[i]
        holdval = ai.Rudimentary_AI(player_list[i], loc_list[i], race_list[i], chromosome)
        player_data.player_dict[key] = holdval

#copy of the old populate players function
# def populate_players(num_players):
#     player_list, loc_list, race_list = player_data.create_players(num_players)
#     for i in range(num_players):
#         key = player_list[i]
#         holdval = ai.Rudimentary_AI(player_list[i], loc_list[i], race_list[i])
#         player_data.player_dict[key] = holdval

#where is this used?
def update_player_dict():
    for key in player_data.holder_dict:
        holder = player_data.holder_dict[key]
        holder2 = [holder]
        player_data.player_dict[key].villages = holder2
        player_data.player_dict[key].location = 'None'
