from bs4 import BeautifulSoup
from dataclasses import dataclass
import pandas as pd
import re
import requests
from typing import List
import datetime

url = "https://www.cricketstats.org.uk/wdcu/2019/index.php?table=0&stats=0&scorecard=1/0107&css=undefined"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

row1_tags = soup.select(".row1")
row2_tags = soup.select(".row2")

rows1_final = [pt.get_text() for pt in row1_tags]
rows2_final = [pt.get_text() for pt in row2_tags]

base = soup.find_all(class_="base_text")
base_text = base[0].get_text()
date = datetime.datetime.strptime(re.search("\d\d/\d\d/\d\d\d\d",base_text).group(), "%d/%m/%Y")

final_rows = rows1_final + rows2_final


@dataclass
class matchday:
    player_name: str
    runs_scored: int
    wickets_taken: int
    bowling_runs_conceded: int
    bowling_wickets_taken: int
    opposition: str

def get_player_names(rows: List, date: datetime):
    names = []
    for name in rows:
        if re.match("^[A-Z]\w*\s\w+", name):
            if name == "Not Out" or name == "Run Out" or "Caught" in name:
                pass
            else:
                names.append(name)
        else:
            continue

    names_final = []
    for name in names:
        if name not in names_final:
            names_final.append(name)



