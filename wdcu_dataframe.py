from matchday import Matchday
import pandas as pd
from itertools import groupby
from operator import itemgetter


class WDCU_dataframe:
    def __init__(self, matchday: Matchday):
        self.matchday = matchday

    @staticmethod
    def create_dataframe(matchday_data: Matchday):
        names = matchday_data.player_names
        df = pd.DataFrame(names, columns=["PlayerName"])
        df['Opposition'] = matchday_data.opposition
        print(df)

    def inner_join(self):
        combo = self.matchday.runs_scored + self.matchday.bowling_metrics
        print(combo)


    # @staticmethod
    # def inner_join(runs_scored, bowler_metrics):
    #     combo = runs_scored + bowler_metrics
    #     combo.sort(key=itemgetter(0))  # sort by the first column
    #     for _, group in groupby(combo, itemgetter(0)):
    #         row_a, row_b = next(group), next(group, None)
    #         if row_b is not None:  # join
    #             yield row_a + row_b[1:]  # cut 1st column from 2nd row

