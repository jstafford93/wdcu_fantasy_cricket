from dataclasses import dataclass, field
from typing import List
import datetime
import re
from pcc_names import PCC_Player_Names
import logging

@dataclass
class Matchday:
    date: datetime = field(init=False)
    player_names: List = field(init=False)
    batting_metrics: tuple = field(init=False)
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
            print("There are not 11 players in the match")
        return names_final

    def get_wickets_taken(self, rows: List):
        bowlers_wickets = []
        for name in self.player_names:
            indices = [i for i, x in enumerate(rows) if x == name]
            logging.info("Grabbing data for ", name)
            for index in indices:
                last_index = index + 5
                entry = rows[index:last_index]
                entry_check = rows[index+1:last_index-2]
                if any(re.match("(^\d+\.\d+)", entry) for entry in entry_check):
                    bowler = entry[0]
                    overs = float(entry[1])
                    maidens = int(entry[2])
                    runs = int(entry[3])
                    wickets = int(entry[4])
                    combo = (bowler, overs, maidens, runs, wickets)
                    bowlers_wickets.append(combo)
                else:
                    pass
        return bowlers_wickets

    def get_runs_scored(self, rows: List):
        batsman_scores = []
        for name in self.player_names:
            indices = [i for i, x in enumerate(rows) if x == name]
            for index in indices:
                last_index = index + 4
                entry = rows[index:last_index]
                entry_check = rows[index+1:last_index-1]
                # initially, capture the batsman data for innings which were ended by a run out
                if len(entry_check) == 0:
                    pass
                elif re.match("Run Out", entry_check[0]):
                    batsman = entry[0]
                    if entry[3] == '0':
                        score = 0
                    elif re.match("\d\d", entry[3]) or re.match("\d", entry[3]):
                        score = int(entry[3])
                    else:
                        score = int(entry[2])
                    combo = (batsman, score)
                    batsman_scores.append(combo)
                # confirm no digits in the middle of the entry; rule out bowling data
                elif any(re.match("\d+", entry) for entry in entry_check):
                    pass
                elif re.match("DNB", entry[1]):
                    batsman = entry[0]
                    score = 0
                    combo = (batsman, score)
                    batsman_scores.append(combo)
                # if the last entry contains a non-digit character then it needs to be passed
                elif re.match("\D+", entry[-1]):
                    pass
                else:
                    batsman = entry[0]
                    if "DNB" in entry:
                        entry[-1] = 0
                        score = int(entry[-1])
                    else:
                        score = int(entry[-1])
                    combo = (batsman, score)
                    batsman_scores.append(combo)
        return batsman_scores



    @classmethod
    def get_config(cls, rows: List, date: datetime, oppostion: str):
        config = cls()
        logging.warning(f'Gathering data for game against {oppostion}')
        config.player_names = config.get_player_names(rows)
        config.date = date
        config.batting_metrics = config.get_runs_scored(rows)
        config.bowling_metrics = config.get_wickets_taken(rows)
        config.opposition = oppostion
        return config

