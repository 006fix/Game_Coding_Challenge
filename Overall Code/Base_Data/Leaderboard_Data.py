
#the base data for the leaderboard will go here

import pandas as pd

#simple holder value for the leaderboard dataframe
leaderboard_base = ['name','pop','cp','attack','defence','raid', 'resources', 'single_num_res',
                    'perc_stored']

def new_leaderboard():
    global leaderboard
    leaderboard = []


def produce_leaderboard(leaderboard):
    global leaderboard_df
    leaderboard_df = pd.DataFrame(leaderboard)
    leaderboard_df.columns = leaderboard_base
    leaderboard_df['pop_rank'] = leaderboard_df['pop'].rank(ascending=False)
    leaderboard_df['cp_rank'] = leaderboard_df['cp'].rank(ascending=False)
    leaderboard_df['res_rank'] = leaderboard_df['single_num_res'].rank(ascending=False)
