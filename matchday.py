from dataclasses import dataclass, field
from typing import List
import datetime
import re


@dataclass
class Matchday:
    date: datetime = field(init=False)
    player_names: List = field(init=False)
    runs_scored: int = field(init=False)
    # wickets_taken: int
    # bowling_runs_conceded: int
    # bowling_wickets_taken: int
    # opposition: str

    @staticmethod
    def get_player_names(rows: List):
        names = []
        for name in rows:
            if re.match("^[A-Z]\w*\s\w+", name):
                if name == "Not Out" or "Run Out" in name or "Caught" in name:
                    pass
                else:
                    names.append(name)
            else:
                continue

        names_final = []
        for name in names:
            if name not in names_final:
                names_final.append(name)

        if len(names_final) != 22:
            raise ValueError("There are not 22 players in the match")
        else:
            return names_final

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
    def get_config(cls, rows, date):
        config = cls()
        config.player_names = config.get_player_names(rows)
        config.date = config.get_runs_scored(rows)
        config.runs_scored = config.get_runs_scored(rows)
        return config

