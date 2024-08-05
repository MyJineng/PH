from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime
import json
from pymongo import MongoClient
import time

MAGENTA = '\033[35m'
YELLOW = '\033[33m'
WHITE = '\033[0m'

# Create Datetime String for Record Keeping
CDT = datetime.now().strftime("%Y-%m-%d")
sCDT = str(CDT)

# Lists to append to later
natl = []
durationl = []
aliasesl = []
agel = []
dateOfBirthl = []
zodiacl = []
careerStatusl = []
careerStartl = []
pobl = []
nationalityl = []

ethnicityl = []
boobsl = []
bustl = []
cupl = []
bral = []
hipl = []
waistl = []
buttl = []
heightl = []
weightl = []
hair_colorl = []
eye_colorl = []
piercingsl = []
piercingLocationsl = []
tattoosl = []
tattooLocationsl = []
shoe_sizel = []

# Create Base Url
page_select = input('Do you want to specify a start page? Type: yes/no')
if page_select == 'yes':
    start_page = int(input('Enter Start Page Number: '))
else:
    start_page = 1
pages = int(input('Enter number of pages to be scraped: '))

for x in range(start_page, (pages + 1)):
    url = f'https://www.freeones.com/performers?s=followerCount&o=desc&l=96&v=grid&m%5BmeasurementSystem%5D=metric&m%5Bfilter_mode%5D%5BperformerType%5D=and&m%5Bfilter_mode%5D%5Bprofessions%5D=and&m%5Bfilter_mode%5D%5Bglobal%5D=and&f%5BperformerType%5D=babe&f%5Bprofessions%5D=porn_stars&p={x}'
    site = requests.get(url)
    soup = BeautifulSoup(site.text, 'html.parser')
    names = [i.text for i in soup.findAll('p', {"data-test": "subject-name"})]
    snames = []
    # Reformat Names to be used in url format
    count = 0
    for s in names:
        # count = count + 1
        s = s.strip()
        s = s.lower()
        s = s.replace(" ", "-")
        snames.append(s)
        # if count == 1:
        #     break
    print(snames)

    def get_var_name(var):
        for name, value in globals().items():
            if value is var:
                return name

    def finder(target_list):
        span = soup.find('span', {"data-test": f"link_span_{get_var_name(target_list)[:-1]}"})
        if span:
            attr_values = [i.text.strip() for i in span]
            target_list.append(attr_values[0])
        else:
            target_list.append('N/A')

    start_time = time.time()
    for index, x in enumerate(snames):
        url = f'https://www.freeones.com/{x}/bio'
        site = requests.get(url)
        soup = BeautifulSoup(site.text, 'html.parser')
        nat_div = soup.find_all('div', class_='hidden md:flex flex-col items-center global-header')
        if nat_div:
            try:
                nat_a = nat_div[1].find('a', attrs={'aria-label': True})
                nat = nat_a["aria-label"].strip()
            except:
                print(YELLOW + x + WHITE)
                nat = 'N/A'
        else:
            nat = 'N/A'
        natl.append(nat)
        duration_p = soup.find('p', {"class": "font-weight-base mb-0"})
        if duration_p:
            duration = [i.text.strip() for i in duration_p]
        else:
            duration = 'N/A'
        durationl.append(duration[0])
        aliases_span_span = soup.find('span', text='Aliases:')
        if aliases_span_span:
            aliases_span = aliases_span_span.find_next_sibling('span', class_='font-size-xs')
            if aliases_span:
                aliases = [alias.text.strip() for alias in
                           aliases_span.find_all('span', class_='text-underline-always')]
                aliases_count = len(aliases)
            else:
                aliases = []
                aliases_count = 0
            aliasesl.append(aliases_count)
        pob_span_span = soup.find('span', text='Place of birth:')
        if pob_span_span:
            pob_span = pob_span_span.find_next_sibling('span', class_='font-size-xs')
            if pob_span:
                pob = [i.text.strip() for i in pob_span.find_all('span', class_='text-underline-always')]
            else:
                pob = 'N/A'
            pobl.append(pob)

        finder(dateOfBirthl), finder(agel), finder(zodiacl), finder(careerStatusl), finder(careerStartl)
        finder(nationalityl), finder(ethnicityl), finder(boobsl), finder(cupl), finder(bral), finder(waistl), finder(
            hipl)
        finder(buttl), finder(heightl), finder(weightl), finder(hair_colorl), finder(eye_colorl), finder(piercingsl)
        finder(piercingLocationsl), finder(tattoosl), finder(tattooLocationsl), finder(shoe_sizel)

        percent_done = (index + 1) / len(snames) * 100
        if percent_done == 25:
            print('25% Done')
        elif percent_done == 50:
            print('50% Done')
        elif percent_done == 75:
            print('75% Done')

# Sets up DataFrame
sdf = pd.DataFrame({'Name': pd.Series(snames), 'Nat': pd.Series(natl),
                    'Duration': pd.Series(durationl), 'Alias Count': pd.Series(aliasesl),
                    'DoB': pd.Series(dateOfBirthl), 'Age': pd.Series(agel), 'Sign': pd.Series(zodiacl),
                    'Active': pd.Series(careerStatusl), 'Career Start': pd.Series(careerStartl),
                    'Place of Birth': pd.Series(pobl), 'Nationality': pd.Series(nationalityl),
                    'Ethnicity': pd.Series(ethnicityl), 'Boobs': pd.Series(boobsl), 'Bust': pd.Series(bustl),
                    'Cup': pd.Series(cupl),
                    'Bra': pd.Series(bral), 'Waist': pd.Series(waistl), 'Hip': pd.Series(hipl),
                    'Butt': pd.Series(buttl), 'Height': pd.Series(heightl), 'Weight': pd.Series(weightl),
                    'Hair Color': pd.Series(hair_colorl), 'Eye Color': pd.Series(eye_colorl),
                    'Piercings': pd.Series(piercingsl), 'Piercings Locations': pd.Series(piercingLocationsl),
                    'Tattoos': pd.Series(tattoosl), 'Tattoos Locations': pd.Series(tattooLocationsl),
                    'Shoe Size': pd.Series(shoe_sizel)})

# Choose Storage Type
select = input('Save records as a csv or json file? Type: csv/json')

if select == 'csv':
    sdf.to_csv((f'PF{sCDT}.csv'), encoding='utf-8', index=False)
elif select == 'json':
    # Conversion to json to be stored in Mongo
    data = sdf.to_dict(orient='records')
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    # Check to see if name in database, otherwise inserts new data
    mongo = MongoClient(port=27017)
    db = mongo["freeones_db"]
    collection = db["pornstars"]
    for document in data:
        existing_document = collection.find_one({"Name": document["Name"]})
        if existing_document is None:
            collection.insert_one(document)
            print(f'Done inserting data for {MAGENTA + document["Name"] + WHITE}')
        else:
            choice = input("Do you want to update documents (Y/N)?: ")
            if choice == 'Y':
                print('')
            else:
                print(f"Document with name {YELLOW + document['Name'] + WHITE} already exists, skipping insertion.")
    mongo.close()

print(f'Processing Time: {((time.time() - start_time).__round__(2))} Seconds')
