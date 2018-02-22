import csv, os, glob, decimal
import pandas as pd
import sqlite3

conn = sqlite3.connect("/Users/broeking/Desktop/T.R.E.A./src/Database/trea.db")
cur = conn.cursor()

# Was walking '.'
months = [month for month in next(os.walk('/Users/broeking/Desktop/T.R.E.A./Ownerships'))[1]]
for month in months:
    path = '/Users/broeking/Desktop/T.R.E.A./Ownerships/' + month + '/'
    days = [day for day in next(os.walk(path))[1]]
    for day in days:
        curr_path = path + day
        for root, dirs, files in os.walk(curr_path):
            for file in files:
                df = pd.read_csv(root + "/" + file, encoding='utf-8')
                df['Month'] = month
                df['Date'] = day
                df['Contest'] = file[:-15]

                df = df.rename(index=str, columns={  
                "Player" : "player",
                "%Drafted" : "drafted",
                "FTPS" : "FPTS",
                "Month" : "month",
                "Date" : "date",
                "Contest" : "contest" })

                df = df.dropna()

                # print(df.head(50))

                # print(month)
                # print(curr_path)
                # print("Day " + day)
                # print("File " + file)
                
                df.to_sql("ownerships", conn, if_exists='append')             
conn.commit()
