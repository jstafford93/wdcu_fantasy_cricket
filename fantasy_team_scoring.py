import pandas as pd
from fantasy_constants import pricing
import numpy as np


def gather_teams(summary_df):
    # open file in read mode
    raw_data = pd.read_csv('pcc_fantasy_teams.csv')
    # iterate through the dataframe, index being the row index, row being the Series data for that records
    for index, row in raw_data.iterrows():
        entrant = row['Entrant']
        # generate a list for each entrant's team selection
        team = [row['Selection1'], row['Selection2'], row['Selection3'], row['Selection4'], row['Selection5']]
        player_costs = [pricing.get(player) for player in team]
        team_cost = 0
        for cost in player_costs:
            team_cost += cost
        if team_cost > 5000000:
            raise ValueError(f"{entrant} has submitted a team that cost {team_cost}, which is about £5m budget.")
        if row['Captain'] not in team:
            raise ValueError(f"{entrant} has selected a captain that is not within his selection of 5.")
    leaderboard_df = build_leaderboard(summary_df, raw_data)
    return leaderboard_df


def build_leaderboard(summary_df, raw_data):
    entrants = [row["Entrant"] for index, row in raw_data.iterrows()]
    teamnames = [row["Team Name"] for index, row in raw_data.iterrows()]
    s1scores = []
    s2scores = []
    s3scores = []
    s4scores = []
    s5scores = []
    captainscores = []

    for index, row in raw_data.iterrows():
        selection1_score = summary_df['Name'] == row['Selection1']
        if True not in selection1_score.unique():
            s1score = 0
            s1scores.append(s1score)
        else:
            sect1df = summary_df[selection1_score]
            s1score = sect1df['Total'].iloc[0]
            s1scores.append(s1score)
        selection2_score = summary_df['Name'] == row['Selection2']
        if True not in selection2_score.unique():
            s2score = 0
            s2scores.append(s2score)
        else:
            sect2df = summary_df[selection2_score]
            s2score = sect2df['Total'].iloc[0]
            s2scores.append(s2score)
        selection3_score = summary_df['Name'] == row['Selection3']
        if True not in selection3_score.unique():
            s3score = 0
            s3scores.append(s3score)
        else:
            sect3df = summary_df[selection3_score]
            s3score = sect3df['Total'].iloc[0]
            s3scores.append(s3score)
        selection4_score = summary_df['Name'] == row['Selection4']
        if True not in selection4_score.unique():
            s4score = 0
            s4scores.append(s4score)
        else:
            sect4df = summary_df[selection4_score]
            s4score = sect4df['Total'].iloc[0]
            s4scores.append(s4score)
        selection5_score = summary_df['Name'] == row['Selection5']
        if True not in selection5_score.unique():
            s5score = 0
            s5scores.append(s5score)
        else:
            sect5df = summary_df[selection5_score]
            s5score = sect5df['Total'].iloc[0]
            s5scores.append(s5score)
        captain_score = summary_df['Name'] == row['Captain']
        if True not in captain_score.unique():
            captain_score = 0
            captainscores.append(captain_score)
        else:
            captain_score_df = summary_df[captain_score]
            captain_score = captain_score_df['Total'].iloc[0]
            captainscores.append(captain_score)
    leaderboard_data = list(zip(entrants, teamnames, s1scores, s2scores, s3scores, s4scores, s5scores,
                                captainscores))
    print(leaderboard_data)
    leaderboard_df = pd.DataFrame(data=leaderboard_data,
                                  columns=["Team Name", "Entrant", "Selection1Score", "Selection2Score",
                                           "Selection3Score", "Selection4Score", "Selection5Score", "CaptainScore"])
    leaderboard_df["Total"] = leaderboard_df["Selection1Score"] + leaderboard_df["Selection2Score"] + \
                              leaderboard_df["Selection3Score"] + leaderboard_df["Selection4Score"] + \
                              leaderboard_df["Selection5Score"] + leaderboard_df["CaptainScore"]
    leaderboard_df = leaderboard_df.sort_values(by=['Total'], ascending=False).reset_index(drop=True)
    leaderboard_df.index = np.arange(1, len(leaderboard_df) + 1)
    return leaderboard_df
