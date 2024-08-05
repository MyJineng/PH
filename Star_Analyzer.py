import pandas as pd
import json
from pymongo import MongoClient
import time
import numpy as np

pd.set_option('display.max_columns', None)
import matplotlib as plt

# Connecting to DataBase and Reformating to JSON
mongo = MongoClient(port=27017)
db = mongo["freeones_db"]
collection = db["pornstars"]
data = (collection.find())

dat = []

start_time = time.time()

for document in data:
    document['_id'] = str(document['_id'])
    dat.append(document)

json_data = json.dumps(dat)

print(f'Processing Time: {((time.time() - start_time).__round__(2))} Seconds')

df = pd.read_json(json_data, orient='records')
print(df.columns)
df = df.drop(columns='_id')

# Split the 'text' column on whitespace
df['Duration'] = df['Duration'].str.split(' ', expand=True)[0]
df['Duration'] = df['Duration'].replace('N', np.nan).dropna()
df['Duration'] = pd.to_numeric(df['Duration'], errors='coerce')

# print(df['Nat'].value_counts())
print(df['Active'].value_counts())
retired_df = df[df['Active'] == 'Active']
print(retired_df['Duration'].mean().round(2))

