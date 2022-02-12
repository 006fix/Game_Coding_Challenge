
import copy
import pandas as pd

#the base data for the leaderboard will go here


#simple holder value for the leaderboard dataframe
leaderboard_base = ['name','AI_name', 'pop','cp','attack','defence','raid', 'resources', 'single_num_res',
                    'perc_stored']
#below is used as a null holder, which is then checked
#if null, charts base gets instantiated with player names
charts_base = []

def new_leaderboard():
    global leaderboard
    leaderboard = []


def produce_leaderboard(leaderboard, i):
    global leaderboard_df
    new_leaderboard()
    leaderboard_df = pd.DataFrame(leaderboard)
    leaderboard_df.columns = leaderboard_base
    leaderboard_df['pop_rank'] = leaderboard_df['pop'].rank(ascending=True)
    leaderboard_df['cp_rank'] = leaderboard_df['cp'].rank(ascending=True)
    leaderboard_df['res_rank'] = leaderboard_df['single_num_res'].rank(ascending=True)
    if len(charts_base) == 0:
        instantiate_chart_base(leaderboard_df)
        instantiate_charts(charts_base)
    produce_charts(leaderboard_df, i)

def instantiate_chart_base(leaderboard_df):
    global charts_base
    charts_base = leaderboard_df[['name', 'AI_name']]

def instantiate_charts(charts_base):

    global raw_pop_base
    global raw_cp_base
    global raw_res_base
    global rank_pop_base
    global rank_cp_base
    global rank_res_base

    raw_pop_base = charts_base
    raw_cp_base = charts_base
    raw_res_base = charts_base
    rank_pop_base = charts_base
    rank_cp_base = charts_base
    rank_res_base = charts_base

#associated global variable for the below function, which simply tracks leaderboard "turn counter", and then
#provides a suitable axis
def produce_charts(leaderboard_df, i):

    global raw_pop_base
    global raw_cp_base
    global raw_res_base
    global rank_pop_base
    global rank_cp_base
    global rank_res_base

    new_label = str(i)
    #now we modify the various charts.
    #lets just join in the details on player name
    raw_pop_base = pd.merge(raw_pop_base, leaderboard_df[['name', 'pop']], on='name', how='left')
    raw_cp_base = pd.merge(raw_cp_base, leaderboard_df[['name', 'cp']], on='name', how='left')
    raw_res_base = pd.merge(raw_res_base, leaderboard_df[['name', 'single_num_res']], on='name', how='left')
    rank_pop_base = pd.merge(rank_pop_base, leaderboard_df[['name', 'pop_rank']], on='name', how='left')
    rank_cp_base = pd.merge(rank_cp_base, leaderboard_df[['name', 'cp_rank']], on='name', how='left')
    rank_res_base = pd.merge(rank_res_base, leaderboard_df[['name', 'res_rank']], on='name', how='left')

    new_cols = list(raw_pop_base.columns)
    new_cols[-1] = new_label
    raw_pop_base.columns = new_cols
    raw_cp_base.columns = new_cols
    raw_res_base.columns = new_cols
    rank_pop_base.columns = new_cols
    rank_cp_base.columns = new_cols
    rank_res_base.columns = new_cols