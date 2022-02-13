
import copy
import pandas as pd
import os
import matplotlib.pyplot as plt


#the base data for the leaderboard will go here


#simple holder value for the leaderboard dataframe
leaderboard_base = ['name','AI_name', 'pop','cp','attack','defence','raid', 'resources', 'single_num_res',
                    'perc_stored']
#below is used as a null holder, which is then checked
#if null, charts base gets instantiated with player names
charts_base = []

#variables used in the creation of the final output graphs
outpath1 = r"C:\Users\pyeac\Desktop\Travian_Game\Output_Charts"
#new variable to generate a subset if I want to store multiple tests
outpath2 = r"\test2"
#variable to store both aggregate and specific outputs
outpath3_list = [r"\Aggregate", r"\Specific"]
#we'll also generate more outpath variables later, to store the various varietities

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
    leaderboard_df['total_rank_pre'] = leaderboard_df['pop_rank'] + leaderboard_df['cp_rank'] + leaderboard_df['res_rank']
    leaderboard_df['total_rank'] = leaderboard_df['total_rank_pre'].rank(ascending=True)
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
    global total_rank_base

    raw_pop_base = charts_base
    raw_cp_base = charts_base
    raw_res_base = charts_base
    rank_pop_base = charts_base
    rank_cp_base = charts_base
    rank_res_base = charts_base
    total_rank_base = charts_base

#associated global variable for the below function, which simply tracks leaderboard "turn counter", and then
#provides a suitable axis
def produce_charts(leaderboard_df, i):

    global raw_pop_base
    global raw_cp_base
    global raw_res_base
    global rank_pop_base
    global rank_cp_base
    global rank_res_base
    global total_rank_base

    new_label = str(i)
    #now we modify the various charts.
    #lets just join in the details on player name
    raw_pop_base = pd.merge(raw_pop_base, leaderboard_df[['name', 'pop']], on='name', how='left')
    raw_cp_base = pd.merge(raw_cp_base, leaderboard_df[['name', 'cp']], on='name', how='left')
    raw_res_base = pd.merge(raw_res_base, leaderboard_df[['name', 'single_num_res']], on='name', how='left')
    rank_pop_base = pd.merge(rank_pop_base, leaderboard_df[['name', 'pop_rank']], on='name', how='left')
    rank_cp_base = pd.merge(rank_cp_base, leaderboard_df[['name', 'cp_rank']], on='name', how='left')
    rank_res_base = pd.merge(rank_res_base, leaderboard_df[['name', 'res_rank']], on='name', how='left')
    total_rank_base = pd.merge(total_rank_base, leaderboard_df[['name', 'total_rank']], on='name', how='left')

    new_cols = list(raw_pop_base.columns)
    new_cols[-1] = new_label
    raw_pop_base.columns = new_cols
    raw_cp_base.columns = new_cols
    raw_res_base.columns = new_cols
    rank_pop_base.columns = new_cols
    rank_cp_base.columns = new_cols
    rank_res_base.columns = new_cols
    total_rank_base.columns = new_cols


def produce_final_outputs():
    #check to see if the file paths required exist.
    outpath1_5 = outpath1 + outpath2
    if not os.path.exists(outpath1_5):
        os.makedirs(outpath1_5)
    for item in outpath3_list:
        outpath_temp = outpath1_5 + item
        if not os.path.exists(outpath_temp):
            os.makedirs(outpath_temp)

    #now that we've created the various directories, lets create our charts
    tables_list = [raw_pop_base, raw_cp_base, raw_res_base, rank_pop_base, rank_cp_base, rank_res_base, total_rank_base]
    tables_list_names = ["raw_pop_base", "raw_cp_base", "raw_res_base", "rank_pop_base",
                         "rank_cp_base", "rank_res_base", "total_rank_base"]
    table_y_axis_names = ["population", "culture points", "total resources per second",
                          "population rank", "culture points rank", "resources rank", "total rank"]
    #step 1 is to create the Aggregate_files
    outpath3_active = r"\Aggregate"

    for i in range(len(tables_list)):
        active_table = tables_list[i]
        table_name = tables_list_names[i]
        final_outpath = outpath1 + outpath2 + outpath3_active + r"\\" + table_name + ".png"

        summarised_table = active_table.groupby(['AI_name']).mean()
        summarised_table2 = summarised_table.T
        summarised_table2.reset_index(inplace=True)
        #print(summarised_table2)

        for col in summarised_table2.columns:
            if not col == 'index':
                plt.plot(summarised_table2['index'], summarised_table2[col], label = col)
        plt.xlabel("Game Turns")
        plt.ylabel(table_y_axis_names[i])
        plt.title(tables_list_names[i])
        plt.xticks([])
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=4)
        plt.savefig(final_outpath, bbox_inches='tight')
        plt.clf()

    #step 2 is to create the specific files
    outpath3_active = r"\Specific"
    #we also need to get all the unique AI types to subset them
    ignore_table = tables_list[0]
    unique_vals = ignore_table['AI_name'].unique()
    #now loop through tables as before

    for i in range(len(tables_list)):
        for j in range(len(unique_vals)):
            active_table = tables_list[i].loc[tables_list[i]['AI_name'] == unique_vals[j]]
            del active_table['AI_name']
            table_title = tables_list_names[i] + unique_vals[j]
            table_name = tables_list_names[i] + str(j)
            final_outpath = outpath1 + outpath2 + outpath3_active + r"\\" + table_name + ".png"
            transposed_table = active_table.T
            transposed_table.reset_index(inplace=True)
            headers = transposed_table.iloc[0]
            new_transposed_table = pd.DataFrame(transposed_table.values[1:], columns=headers)

            #print(transposed_table)
            for col in new_transposed_table.columns:
                if not col == 'name':
                    plt.plot(new_transposed_table['name'], new_transposed_table[col], label=str(col))
            plt.xlabel("Game Turns")
            plt.ylabel(table_y_axis_names[i])
            plt.title(table_title)
            plt.xticks([])
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=4)
            plt.savefig(final_outpath, bbox_inches='tight')
            plt.clf()
