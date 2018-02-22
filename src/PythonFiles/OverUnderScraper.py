from bs4 import BeautifulSoup
import requests
import itertools
import pandas as pd

from datetime import timedelta, date

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2016, 4, 2)
end_date = date(2016, 10, 2)
for single_date in daterange(start_date, end_date):

    date = single_date.strftime("%Y%m%d")
    url = "http://www.donbest.com/mlb/odds/totals/" + date + ".html"
    r  = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')

    odds = soup.find("div", {"class": "odds_gamesHolder"})
    left_games = soup.find_all("td", {"class":"alignLeft"})
    right_games = soup.find_all("td", {"class":"alignRight oddsOpener"})
    game_count = -1

    teams = ['Away_Team','Home_Team']
    starter = ['Away_Starter','Home_Starter']
    center_cols = ['Start_Time', 'Away_Final_Score', 'Home_Final_Score']

    df = pd.DataFrame(columns=['Away_Team','Home_Team','Away_Starter','Home_Starter', 'Total'])

    ##  Game Time / Score ##
    # We have a duplicate in cyclic groups of three
    skip_every_third = 1
    pos = 0
    row = 0

    ##########
    #  LEFT  #
    ##########
    for left in left_games:
      
        game_count = game_count + 1
        div = left.find_all("div")
        span = left.find_all("span")
        skip = True

        pos = 0
        for playername in div:
            if skip:
                skip = False
            else:
                df.at[row, starter[pos]] = playername.text
                pos = pos + 1

        pos = 0
        for teamname in span:
            df.at[row, teams[pos]] = teamname.text
            pos = pos + 1
        row = row + 1
    
    row = 0
    ###########
    #  RIGHT  #
    ###########

    for right in right_games:

        print(right.prettify())

        middle_one = right.find("div", {"class":"oddsAlignMiddleOne"})
        middle_two = right.find("div", {"class":"oddsAlignMiddleTwo"})

        if middle_one is not None:
            df.at[row, 'Total'] = middle_one.text
        elif middle_two is not None:
            df.at[row, 'Total'] = middle_two.text
        else:
            print("help")
            df.at[row, 'Total'] = "0"   
        row = row + 1

    df.to_csv('/Users/broeking/Desktop/T.R.E.A./MLBTotals/2016/' + date + '.csv', encoding='utf-8', index=False)