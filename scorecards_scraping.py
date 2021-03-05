# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 14:58:00 2021

@author: andrew
"""


#import packages for web scraping (beautiful soup), pandas
import requests
import pandas as pd
from bs4 import BeautifulSoup

#parse html to soup to be interpreted

URL = 'https://www.cricketstats.org.uk/wdcu/2019/'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find_all('td',{'class':'fixtures_result'})
dates = soup.find_all('td',{'class':'fixtures_date'})


#save html to file
html_file = open('year_results.txt','w')
html_file.write(str(results))
html_file.close()
#print(dates)

# get match and scorecard address for each match with a result
base_url = 'https://www.cricketstats.org.uk/wdcu/2019/'
df = pd.DataFrame()
tb_columns = ['home', 'away', 'scorecard_link', 'reduced_overs']
parsed_data = []
for result in results:
    fixture = result.find('b')
    scorecard = result.find('a')
    # if there was no result or match cancelled, skip the records
    if None in (fixture, scorecard):
        continue
    match = fixture.text.strip()
    #split match details, 1st team is home, 2nd team is away
    teams = match.split(" v ")
    home = teams[0]
    away = teams[1]
    overs = away.split("(")
    away = overs[0]
    if len(overs) == 2:
        over = int((overs[1].split(" ",1))[0])
    else:
        over = None
    index = scorecard.get('href')[30:72]
    link = base_url + index
    parsed_data.append([home, away, link, over])
    
df=pd.DataFrame(parsed_data, columns = tb_columns)

df.to_csv('teams.csv')


