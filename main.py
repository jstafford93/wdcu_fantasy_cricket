from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd
import requests

url = "https://www.cricketstats.org.uk/wdcu/2019/index.php?table=0&stats=0&scorecard=1/0110&css=undefined"
page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
soup = BeautifulSoup(page.content, "html.parser")
html = list(soup.children)[2]
body = list(html.children)[3]
p = list(body.children)[1]

p = soup.find_all("p")
print(p[0].get_text())