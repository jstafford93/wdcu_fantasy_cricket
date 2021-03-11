from bs4 import BeautifulSoup
import re
import requests
import datetime
from matchday import Matchday
from wdcu_dataframe import WDCU_dataframe

def run():
    url = "https://www.cricketstats.org.uk/wdcu/2019/index.php?table=0&stats=0&scorecard=1/0804&css=undefined"
    page = requests.get(url)
    # will parse through the provided URL and return a soup object with the HTML contents
    soup = BeautifulSoup(page.content, "html.parser")

    row1_tags = soup.select(".row1")
    row2_tags = soup.select(".row2")

    rows1_final = [pt.get_text() for pt in row1_tags]
    rows2_final = [pt.get_text() for pt in row2_tags]

    base = soup.find_all(class_="base_text")
    base_text = base[0].get_text()

    head = soup.find('h1').get_text()
    match_details = head.split("v")

    oppo = None
    for string in match_details:
        if string.strip() == "Prestwick":
            pass
        else:
            oppo = string.strip()

    date = datetime.datetime.strptime(re.search("\d\d/\d\d/\d\d\d\d",base_text).group(), "%d/%m/%Y")

    final_rows = rows1_final + rows2_final

    matchday_data = Matchday.get_config(final_rows, date, oppo)
    print(matchday_data.player_names)

if __name__ == "__main__":
    run()
