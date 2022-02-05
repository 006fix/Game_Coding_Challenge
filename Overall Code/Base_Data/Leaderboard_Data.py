
#the base data for the leaderboard will go here

import pandas as pd

#simple holder value for the leaderboard dataframe
leaderboard_base = ['name','pop','cp','attack','defence','raid', 'resources', 'agg_over_80%capacity', 'single_num_res',
                    'single_num_over80']

def new_leaderboard():
    global leaderboard
    leaderboard = []


def produce_leaderboard(leaderboard):
    leaderboard_df = pd.DataFrame(leaderboard)
    leaderboard_df.columns = leaderboard_base
    leaderboard_df['pop_rank'] = leaderboard_df['pop'].rank(ascending=False)
    leaderboard_df['cp_rank'] = leaderboard_df['cp'].rank(ascending=False)
