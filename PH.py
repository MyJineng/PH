from bs4 import BeautifulSoup
import pandas as pd
import requests, os
from datetime import datetime
import matplotlib.pyplot as plt

# Datetime string for chart name and csv
CDT = datetime.now().strftime("%Y-%m-%d")
sCDT = str(CDT)
# Create url bases for category lookup
all = "https://www.pornhub.com/pornstars?gender=female&performerType=pornstar"
start = 'https://www.pornhub.com/pornstars?gender=female&ethnicity='
end = '&performerType=pornstar'
# Input required to finish url if eth != all
eth = input('Select a category - all, asian, black, latin or white: ')
if eth == 'all':
    url = all
else:
    url = f'{start}{eth}{end}'
# Parse url
site = requests.get(url)
soup = BeautifulSoup(site.text, 'html.parser')

# Create lists from items found in each class
views = [i.text for i in soup.findAll('span', {"class": "viewsNumber performerCount"})]
names = [i.text for i in soup.findAll('span', {"class": "pornStarName performerCardName"})]
ranks = [i.text for i in soup.findAll('span', {"class": "rank_number"})] #PH Rank is based on all performers ie. "amateur" models
videos = [i.text for i in soup.findAll('span', {"class": "videosNumber performerCount"})]
# Strip ugly html from lists
sviews = [s.strip() for s in views]
snames = [s.strip() for s in names]
sranks = [s.strip() for s in ranks]
svideos = [s.strip() for s in videos]
# Create pandas DataFrame
sdf = pd.DataFrame({'Name': pd.Series(snames), 'Views': pd.Series(sviews),
                    'Videos': pd.Series(svideos), 'PH Rank': pd.Series(sranks)})
# Change dftype to integer to do maths... lol
sdf['PH Rank'] = sdf['PH Rank'].astype(str).astype(int)
# Get rid of extra string
sdf['Videos'] = sdf['Videos'].str.replace(' Videos', '')
sdf['Videos'] = sdf['Videos'].astype(str).astype(int)
# Change string to numbers based on ending
sdf['Views'] = sdf['Views'].str.replace('K Views', '000')
sdf['Views'] = sdf['Views'].str.replace('M Views', '000000')
sdf['Views'] = sdf['Views'].str.replace('B Views', '000000000')
# Use for loop to fix discrepancy between 2B vs 2.1B
for x in range(1, 10):
    sdf['Views'] = sdf['Views'].str.replace(f'.{x}0', f'{x}')
sdf['Views'] = sdf['Views'].astype(str).astype(int)
sdf['View/Video Ratio'] = (round(sdf["Views"] / sdf['Videos']))
# print(round(sdf.describe()))
print(sdf)
sdf = sdf[['Videos', 'Name']]

# print(sdf)
# print(sdf.dtypes)

# Special case for bar graph title
if str(eth) == 'all':
    eth = 'Pornhub'
# Time to see who's most popular via a Bar Graph
plot = sdf['Videos'].plot(kind="bar", figsize=(30, 5))
plot.set_xticklabels(sdf["Name"], rotation=45)
plt.title(f"Top {eth} Models by Video Count: {sCDT}")
plt.xlabel("Models")
plt.ylabel("Video Count")
plt.tight_layout()
plt.show()

# Create csv to store our important data and assign the date
sdf.to_csv((f'PH{sCDT}.csv'), encoding='utf-8', index=False)


