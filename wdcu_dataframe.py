from matchday import Matchday
import pandas as pd
from typing import List
import numpy as np
import uuid

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
        enriched_df["UUID"] = uuid.uuid4().hex
        return enriched_df


