from bs4 import BeautifulSoup
import re
import requests
import datetime
from matchday import Matchday
from wdcu_dataframe import WDCU_dataframe
import pandas as pd
import fantasy_team_scoring

# ADD IN VALIDATION THAT CAPTAIN IS WITHIN THE SELECTION OF 5

def fetch_urls(base_url: str):
    first_xi_id = '1/'
    second_xi_id = '6/'
    pwick_id = '08'
    stnins_id = '08'
    opposition_ids_ones = ['0' + str(i) for i in range(1, 10) if i != 8] + ['10']
    opposition_ids_twos = ['0' + str(i) for i in range(1, 10) if i != 8] + ['10']

    scorecards = []
    for i in opposition_ids_ones:
        first_xi_home_scorecard = base_url + first_xi_id + pwick_id + i
        first_xi_away_scorecard = base_url + first_xi_id + i + pwick_id
        scorecards.extend([first_xi_home_scorecard, first_xi_away_scorecard])
    for i in opposition_ids_twos:
        second_xi_home_scorecard = base_url + second_xi_id + stnins_id + i
        second_xi_away_scorecard = base_url + second_xi_id + i + stnins_id
        scorecards.extend([second_xi_home_scorecard, second_xi_away_scorecard])
    return scorecards


def run():
    base_url = 'https://www.cricketstats.org.uk/wdcu/2019/index.php?table=0&stats=0&scorecard='
    urls = fetch_urls(base_url)
    # urls = ['https://www.cricketstats.org.uk/wdcu/2017/index.php?table=0&stats=0&scorecard=1/0207']
    df_list = []
    for url in urls:
        page = requests.get(url)
        # will parse through the provided URL and return a soup object with the HTML contents
        soup = BeautifulSoup(page.content, "html.parser")

        row1_tags = soup.select(".row1")
        row2_tags = soup.select(".row2")

        rows1_final = [pt.get_text() for pt in row1_tags]
        rows2_final = [pt.get_text() for pt in row2_tags]

        base = soup.find_all(class_="base_text")
        base_text = base[0].get_text()
        if "cancelled" in base_text:
            pass
        else:
            head = soup.find('h1').get_text()
            match_details = head.split("v")
            result = None
            if "Prestwick (25)" in base_text or "St.Ninians (25)" in base_text or "St. Ninians (25)" in base_text:
                result = "WIN"
            else:
                result = "LOSS"
            oppo = None
            for string in match_details:
                if "Prestwick" in string.strip() or "St.Ninians" in string.strip() or "St. Ninians" in string.strip():
                    pass
                else:
                    oppo = string.strip()

            date = datetime.datetime.strptime(re.search("\d\d/\d\d/\d\d\d\d",base_text).group(), "%d/%m/%Y")

            final_rows = rows1_final + rows2_final

            matchday_data = Matchday.get_config(final_rows, date, oppo)
            my_dataframe = WDCU_dataframe(matchday_data)
            final_tuples = my_dataframe.bat_bowl_join()
            temp_df = my_dataframe.create_dataframe(final_tuples)
            enriched_df = WDCU_dataframe.enrich_dataframe(temp_df, oppo, date, result)
            df_list.append(enriched_df)
    summary_df = return_dfs(df_list)


def return_dfs(df_list):
    final_df = pd.concat(df_list, ignore_index=True)
    fantasy_df = WDCU_dataframe.fantasise_final_df(final_df)
    fantasy_leaderboard = fantasy_team_scoring.gather_teams(fantasy_df)
    # removing individual selection scores for cleaner TeamStandings excel output
    fantasy_leaderboard_v2 = fantasy_leaderboard.drop(["Selection1Score", "Selection2Score", "Selection3Score", "Selection4Score",
                              "Selection5Score", "CaptainScore"],axis=1)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('PCC_2019.xlsx', engine='xlsxwriter')

    # Write each dataframe to a different worksheet.
    fantasy_leaderboard_v2.to_excel(writer, sheet_name="TeamStandings")
    fantasy_df.to_excel(writer, sheet_name='PlayerStandings')
    final_df.to_excel(writer, sheet_name='MatchDetails')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()


if __name__ == "__main__":
    run()

