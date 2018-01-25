from bs4 import BeautifulSoup
import requests
import itertools
import pandas as pd

url = "http://www.donbest.com/mlb/odds/money-lines/20170805.html"
r  = requests.get(url)
data = r.text
soup = BeautifulSoup(data, 'html.parser')

odds = soup.find("div", {"class": "odds_gamesHolder"})
left_games = soup.find_all("td", {"class":"alignLeft"})
center_games = soup.find_all("td", {"class":"alignCenter"})
right_games = soup.find_all("td", {"class":"alignRight"})
game_count = -1

df = pd.DataFrame(columns=['Away_Team','Home_Team','Away_Starter','Home_Starter','Start_Time','Away_Final_Score','Home_Final_Score', 'Away_Opening', 'Home_Opening', 'Away_Westgate', 
    'Home_Westgate', 'Away_Mirage', 'Home_Mirage', 'Away_Station', 'Home_Station', 'Away_Pinnacle', 'Home_Pinnacle', 'Away_SIA', 'Home_SIA', 'Away_SBG', 'Home_SBG', 
        'Away_BetUS', 'Home_BetUS', 'Away_BetPhoenix', 'Home_BetPhoenix', 'Away_EasyStreet', 'Home_EasyStreet', 'Away_Bovada', 'Home_Bovada', 'Away_Jazz', 'Home_Jazz',
            'Away_Sportsbet', 'Home_Sportsbet', 'Away_Bookmaker', 'Home_Bookmaker', 'Away_DSI', 'Home_DSI', 'Away_AceSport', 'Home_AceSport'])


##  Game Time / Score ##
counter = 1
for center in center_games:
#    scores = center.find_all("div")
    print(center.prettify())

## Starter Names / Team Names / Game Lines ##
for left in left_games:

    game_count = game_count + 1
    div = left.find_all("div")
    span = left.find_all("span")
    skip = True

    for playername in div:
        if skip:
            skip = False
        else:
            print(playername.text)

    for teamname in span:
        print(teamname.text)

    first = True
    for x in range(0, 17):
        lines = right_games[x+(game_count*17)].find_all("div")
        for line in lines:
            if first:
                first = False
                print((line.text)[:-4])
                print((line.text)[4:])
            else:
                print(line.text)

