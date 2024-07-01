from bs4 import BeautifulSoup
import pandas as pd
import requests, os
from datetime import datetime
import matplotlib.pyplot as plt
import time

# Create Datetime String for Record Keeping
CDT = datetime.now().strftime("%Y-%m-%d")
sCDT = str(CDT)
# Create Base Url
all = "https://www.pornhub.com/pornstars?gender=female&performerType=pornstar"
start = 'https://www.pornhub.com/pornstars?gender=female&ethnicity='
end = '&performerType=pornstar'
# Input for the Url
eth = input('Select a category - all, asian, black, latin or white: ')
if eth == 'all':
    url = all
else:
    url = f'{start}{eth}{end}'
# Parse the Top Pornstars Url
site = requests.get(url)
soup = BeautifulSoup(site.text, 'html.parser')
# Create List of Top Pornstar Names
names = [i.text for i in soup.findAll('span', {"class": "pornStarName performerCardName"})]
snames = []
# Reformat Names to be used in url format
for s in names:
    s = s.strip()
    s = s.lower()
    s = s.replace(" ", "-")
    snames.append(s)
# Lists to append to later
weightl = []
heightl = []
# Loop through names to make urls to parse weight and height data
for x in snames:
    if x == 'rose-monroe-your-fav':
        x = 'rose-monroe'
    try:
        # Tries 1st format and appends data
        url = f'https://www.pornhub.com/pornstar/{x}'
        site = requests.get(url)
        soup = BeautifulSoup(site.text, 'html.parser')
        weight = [i.text for i in soup.find('span', {"itemprop": "weight"})]
        height = [i.text for i in soup.find('span', {"itemprop": "height"})]
        weightl.append(weight[0])
        heightl.append(height[0])
    except:
        try:
            # Tries 2nd format and appends data
            select = soup.find_all('div', class_='infoPiece')
            height = [i for i in select if i.find(text=lambda text: text.strip() == "Birthplace:")]
            height = height[0].find_next_sibling().text.strip()
            height = height.split()[1:]
            height = ' '.join(height)
            weight = [i for i in select if i.find(text=lambda text: text.strip() == "Height:")]
            weight = weight[0].find_next_sibling().text.strip()
            weight = weight.split()[1:]
            weight = ' '.join(weight)
            weightl.append(weight)
            heightl.append(height)
        except:
            # if either weight or height not found tries to look for only one of the elements
            try:
                weight = [i for i in select if i.find(text=lambda text: text.strip() == "Height:")]
                weight = weight[0].find_next_sibling().text.strip()
                weight = weight.split()[1:]
                weight = ' '.join(weight)
                if "lbs" in weight:
                    weightl.append(weight)
                    height = 'NaN'
                    heightl.append(height)
                # Backs up one element to grab element data since ethnicity data is usually after height
                else:
                    weight = [i for i in select if i.find(text=lambda text: text.strip() == "Ethnicity:")]
                    weight = weight[0].find_previous_sibling().text.strip()
                    weight = weight.split()[1:]
                    weight = ' '.join(weight)
                    weightl.append(weight)
                    height = 'NaN'
                    heightl.append(height)
            except:
                try:
                    height = [i for i in select if i.find(text=lambda text: text.strip() == "Birthplace:")]
                    height = height[0].find_next_sibling().text.strip()
                    height = height.split()[1:]
                    height = ' '.join(height)
                    if "ft" in height:
                        heightl.append(height)
                        weight = 'NaN'
                        weightl.append(weight)
                    else:
                        height = [i for i in select if i.find(text=lambda text: text.strip() == "Ethnicity:")]
                        height = height[0].find_previous_sibling().text.strip()
                        height = height.split()[1:]
                        height = ' '.join(height)
                        heightl.append(height)
                        weight = 'NaN'
                        weightl.append(weight)
                except:
                    weight = 'NaN'
                    weightl.append(weight)
                    height = 'NaN'
                    heightl.append(height)
                    print(f'{x} has no weight or height data!')
# Sets up DataFrame
sdf = pd.DataFrame({'Name': pd.Series(snames), 'Height': pd.Series(heightl),
                    'Weight': pd.Series(weightl)})

# Local option as to not get blocked...
# csv = pd.read_csv('c:\PycharmProjects\PH\PH2024-04-24.csv')
# sdf = pd.DataFrame(csv)

# Clean by getting rid of string data and reformat to float
sdf['Height'] = sdf['Height'].str.extract("\((.*) cm\)")
sdf['Weight'] = sdf['Weight'].str.extract("\((.*) kg\)")
sdf['Height'] = (sdf['Height'].astype(float) * 0.0328).__round__(2)
sdf['Weight'] = (sdf['Weight'].astype(float) * 2.2050).__round__(2)
avg_weight = sdf["Weight"].mean()
avg_height = sdf["Height"].mean()

# The Important Stats Lol!
print(f'Avg Pornstar Height: {avg_height.round(2)} ft, Avg Pornstar Weight: {avg_weight.round(2)} lbs')
print(sdf.describe().round(2))
print(sdf.head(10))

# Save as a csv
sdf.to_csv((f'PH{eth}{sCDT}.csv'), encoding='utf-8', index=False)

# Bar Plot for Fun!
plot = sdf['Height'].plot(kind="bar", figsize=(30, 5))
plot.set_xticklabels(sdf["Name"], rotation=45)
plt.title(f"Top {eth.capitalize()} Models by Video Count: {sCDT}")
plt.xlabel("Models")
plt.ylabel("Height (ft)")
plt.ylim(4.5, 6)
plt.tight_layout()
plt.show()