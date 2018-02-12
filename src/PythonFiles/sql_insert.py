import csv, os, glob, decimal
import pandas as pd
import sqlite3

conn = sqlite3.connect("/Users/broeking/Desktop/T.R.E.A./src/Database/trea.db")
cur = conn.cursor()

# Was walking '.'
months = [month for month in next(os.walk('/Users/broeking/Desktop/T.R.E.A./Lineups'))[1]]
for month in months:
    path = '/Users/broeking/Desktop/T.R.E.A./Lineups/' + month + '/'
    days = [day for day in next(os.walk(path))[1]]
    for day in days:
        curr_path = path + day
        for root, dirs, files in os.walk(curr_path):
            for file in files:
                df = pd.read_csv(root + "/" + file, encoding='utf-8')
                df['Month'] = month
                df['Date'] = day
                df['Contest'] = file[:-10]
            
                df = df.rename(index=str, columns={  
                "Rank" : "rank",
                "EntryName" : "entryname",
                "Points" : "points",
                "Lineup" : "Lineup",
                "SP1" : "sp1",
                "SP2" : "sp2",
                "C" : "c",
                "1B" : "oneb",
                "2B" : "twob",
                "3B" : "threeb",
                "SS" : "ss",
                "OF1" : "of1",
                "OF2" : "of2",
                "OF3" : "of3",
                "Month" : "month",
                "Date" : "date",
                "Context" : "contest" })

                df.to_sql("lineups", conn, if_exists='append')
            
                # print(month)
                # print(curr_path)
                # print("Day " + day)
                # print("File" + file)
conn.commit()
