# import instagram_scraper
#
# from instalooter.looters import ProfileLooter
#
# looter = ProfileLooter("rashesh.kothari")
# looter.download('~/Pictures', media_count=50)

from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import re
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import os
import requests
import pandas as pd, numpy as np

hashtag='pizza'
browser = webdriver.Chrome('/usr/local/bin/chromedriver')
browser.get('https://www.instagram.com/explore/tags/'+hashtag)
Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# #Extract links from user profile page
# links=[]
# source = browser.page_source
# data=bs(source, 'html.parser')
# body = data.find('body')
# script = body.find('script', text=lambda t: t.startswith('window._sharedData'))
# page_json = script.text.split(' = ', 1)[1].rstrip(';')
# data = json.loads(page_json)
# for link in data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']:
#     links.append('https://www.instagram.com'+'/p/'+link['node']['shortcode']+'/')

#Extract links from hashtag page
links=[]
source = browser.page_source
data=bs(source, 'html.parser')
body = data.find('body')
script = body.find('script', text=lambda t: t.startswith('window._sharedData'))
page_json = script.text.split(' = ', 1)[1].rstrip(';')
data = json.loads(page_json)
for link in data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']:
    links.append('https://www.instagram.com'+'/p/'+link['node']['shortcode']+'/')

# print(links)
#⁨Semester Two⁩ ▸ ⁨Welbilt⁩ ▸ ⁨dataset⁩
# Users⁩ ▸ ⁨rasheshkothari⁩ ▸ ⁨Desktop⁩ ▸ ⁨Study⁩ ▸ ⁨Semester Two⁩ ▸ ⁨Welbilt⁩ ▸
result = pd.DataFrame(links)

result.index = range(len(result.index))
result['display_url'] = result
print(result['display_url'])

result["sc"]= result["display_url"].astype(str)

result["sc"]= result["sc"].str.slice(start=30, stop=35, step=1)


directory="/Users/rasheshkothari/Desktop/Study/Semester Two/Welbilt/dataset/train/"
for i in range(len(result)):
    r = requests.get(result['display_url'][i])
    with open(directory+result['sc'][i]+".jpg", 'wb') as f:
                    f.write(r.content)