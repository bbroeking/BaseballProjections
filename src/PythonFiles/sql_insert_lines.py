import csv, os, glob, decimal
import pandas as pd
import sqlite3

conn = sqlite3.connect("/Users/broeking/Desktop/T.R.E.A./src/Database/trea.db")
cur = conn.cursor()

# Was walking '.'
years = [year for year in next(os.walk('/Users/broeking/Desktop/T.R.E.A./MLBLines'))[1]]
for year in years:
    path = '/Users/broeking/Desktop/T.R.E.A./MLBLines/' + year + '/'
    for root, dirs, files in os.walk(path):
        for file in files:
            df = pd.read_csv(root + "/" + file, encoding='utf-8')
            df['date'] = file[4:6].lstrip('0') + "." + file[6:8]
            df['year'] = file[0:4]

            # print("Month " + file[4:6].lstrip('0') + "." + file[6:8])
            # print("Date " + file[0:4])
            
            df.to_sql("lines", conn, if_exists='append', index = False)             
conn.commit()
