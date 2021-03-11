from dataclasses import dataclass, field
from typing import List
import datetime
import re
from pcc_names import PCC_Player_Names


@dataclass
class Matchday:
    date: datetime = field(init=False)
    player_names: List = field(init=False)
    runs_scored: tuple = field(init=False)
    bowling_metrics: tuple = field(init=False)
    opposition: str = field(init=False)

    @staticmethod
    def get_player_names(rows: List):
        names = []
        for name in rows:
            if re.match("^[A-Z]\w*\s\w+", name):
                if name == "Not Out" or "Run Out" in name or "Caught" in name:
                    pass
                elif name in PCC_Player_Names:
                    names.append(name)
            else:
                continue

        names_final = []
        for name in names:
            if name not in names_final:
                names_final.append(name)

        if len(names_final) != 11:
            raise ValueError("There are not 11 players in the match")
        else:
            return names_final

    def get_wickets_taken(self, rows: List):
        bowlers_wickets = []
        for name in self.player_names:
            indices = [i for i, x in enumerate(rows) if x == name]
            for index in indices:
                last_index = index + 5
                entry = rows[index:last_index]
                entry_check = rows[index+1:last_index-2]
                if any(re.match("(^\d+\.\d+)", entry) for entry in entry_check):
                    bowler = entry[0]
                    overs = entry[1]
                    runs = entry[3]
                    wickets = entry[4]
                    combo = (bowler, overs, runs, wickets)
                    bowlers_wickets.append(combo)
                else:
                    pass
        print(bowlers_wickets)
        return bowlers_wickets

    def get_runs_scored(self, rows: List):
        batsman_scores = []
        for name in self.player_names:
            indices = [i for i, x in enumerate(rows) if x == name]
            for index in indices:
                last_index = index + 4
                entry = rows[index:last_index]
                entry_check = rows[index+1:last_index-1]
                if any(re.match("\d+", entry) for entry in entry_check):
                    pass
                else:
                    batsman = entry[0]
                    if "DNB" in entry:
                        entry[-1] = 0
                        score = entry[-1]
                    else:
                        score = entry[-1]
                    combo = (batsman, score)
                    batsman_scores.append(combo)
        return batsman_scores

    @classmethod
    def get_config(cls, rows: List, date: datetime, oppostion: str):
        config = cls()
        config.player_names = config.get_player_names(rows)
        config.date = date
        config.runs_scored = config.get_runs_scored(rows)
        config.bowling_metrics = config.get_wickets_taken(rows)
        config.opposition = oppostion
        return config

