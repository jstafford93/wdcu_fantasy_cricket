from matchday import Matchday
import pandas as pd
from typing import List
import numpy as np
import uuid
from scoring_matrix import Matrix

class WDCU_dataframe:
    def __init__(self, matchday: Matchday):
        self.matchday = matchday

    @staticmethod
    def create_dataframe(combined_tuples: List):
        df = pd.DataFrame(combined_tuples, columns=["Name", "RunsScored", "OversBowled", "Maidens", "RunsConceded", "Wickets"])
        return df

    def bat_bowl_join(self):
        bowler_metrics = self.bowler_metrics()
        final_metrics = self.batter_bowler_metrics(bowler_metrics)
        return final_metrics

    def bowler_metrics(self):
        combo = []
        # gather the list of tuples containing the data for those who batted and bowled
        for entry in self.matchday.batting_metrics:
            for bowl in self.matchday.bowling_metrics:
                if entry[0] in bowl:
                    combo.append(entry+bowl[1:])
        # returns a list of those who batted and bowled
        return combo

    def batter_bowler_metrics(self, combo: List):
        bowl_batters = [entry[0] for entry in combo]
        # gather the list of tuples containing the data for those who only batted
        for entry in self.matchday.batting_metrics:
            if entry[0] not in bowl_batters:
                empty_bowling_stats = (0, 0, 0, 0)
                combo.append(entry + empty_bowling_stats)
        return combo

    @staticmethod
    def enrich_dataframe(dataframe, opposition, date, result):
        enriched_df = dataframe.assign(opposition=opposition, date=date, result=result)
        enriched_df["50Scored"] = np.where((enriched_df["RunsScored"] >= 50) & (enriched_df["RunsScored"] < 100), 1, 0)
        enriched_df["100Scored"] = np.where(enriched_df["RunsScored"] >= 100, 1, 0)
        enriched_df["3For"] = np.where((enriched_df["Wickets"] >= 3) & (enriched_df["Wickets"] < 5), 1, 0)
        enriched_df["5For"] = np.where(enriched_df["Wickets"] >= 5, 1, 0)
        enriched_df["Conceded45"] = np.where(enriched_df["RunsConceded"] >= 45, 1, 0)
        enriched_df["UUID"] = uuid.uuid4().hex
        return enriched_df

    @staticmethod
    def fantasise_final_df(final_df):
        fantasy_df = final_df
        fantasy_df['runsbonus'] = fantasy_df['RunsScored'] * Matrix['run_scored']
        fantasy_df['50bonus'] = fantasy_df['50Scored'] * Matrix['50_scored']
        fantasy_df['100bonus'] = fantasy_df['100Scored'] * Matrix['100_scored']
        fantasy_df['3forbonus'] = fantasy_df['3For'] * Matrix['3_for']
        fantasy_df['5forbonus'] = fantasy_df['5For'] * Matrix['5_for']
        fantasy_df['conceded45deduction'] = fantasy_df['Conceded45'] * Matrix['concede_over_45']
        fantasy_df['wicketbonus'] = fantasy_df['Wickets'] * Matrix['wicket']
        fantasy_df['maidenbonus'] = fantasy_df['Maidens'] * Matrix['maiden']
        fantasy_df['winbonus'] = np.where(fantasy_df["result"] == "WIN", 10, 0)
        new_df = fantasy_df.drop(['RunsScored', 'OversBowled', 'Maidens', 'RunsConceded', 'Wickets', 'result',
                                  '50Scored', '100Scored', '3For', '5For', 'Conceded45', 'UUID'], axis=1)
        ultimate_df = new_df.groupby(['Name']).agg(sum)
        ultimate_df['total'] = ultimate_df['runsbonus'] + ultimate_df['50bonus'] + ultimate_df['100bonus'] + ultimate_df['3forbonus'] + ultimate_df['5forbonus'] + ultimate_df['conceded45deduction'] + ultimate_df['wicketbonus'] + ultimate_df['maidenbonus'] + ultimate_df['winbonus']
        clean_df = ultimate_df.sort_values(by=['total'], ascending=False)
        return clean_df






