from bs4 import BeautifulSoup
import requests
import itertools
import pandas as pd

url = "http://www.donbest.com/mlb/odds/totals/20150407.html"
r  = requests.get(url)
data = r.text
soup = BeautifulSoup(data, 'html.parser')

odds = soup.find("div", {"class": "odds_gamesHolder"})
left_games = soup.find_all("td", {"class":"alignLeft"})

right_games = soup.find_all("td", {"class":"alignRight oddsOpener"})
game_count = -1

df = pd.DataFrame(columns=['Away_Team','Home_Team','Away_Starter','Home_Starter', 'Total'])


##  Game Time / Score ##
#counter = 1
# Skipping the first line in the right
first = True
# Skipping the added one at the front
oddOne = True
# This one needs to be broken into total and line
break_apart = True
# We have a duplicate in cyclic groups of three
skip_every_third = 1

pos = 0
row = 0

for left, right in zip(left_games, right_games):
    #  LEFT  #
    game_count = game_count + 1
    div = left.find_all("div")
    span = left.find_all("span")
    skip = True

    pos = 0
    for playername in div:
        if skip:
            skip = False
        else:
            # df.at[row, starter[pos]] = playername.text
            print("playername")
            print(playername.text)
            pos = pos + 1
    pos = 0
    for teamname in span:
        # df.at[row, teams[pos]] = teamname.text
        print("teamname")
        print(teamname.text)
        pos = pos + 1

    #  RIGHT  #

    middle_one = right.find("div", {"class":"oddsAlignMiddleOne"})
    middle_two = right.find("div", {"class":"oddsAlignMiddleTwo"})

    if middle_one is not None:
        print(middle_one.prettify())
    elif middle_two is not None:
        print(middle_two.prettify())
    else:
        print("Empty")        
    row = row + 1



# This functionality doesn't currently matter
# We don't need this spectific information about the lines
# Simply the opener will suffice

# else:
#     if not oddOne:
#         # df.at[row, sportsbooks[pos]] = line.text
#         if skip_every_third % 3 != 0:
#             # row needs to be broken into two parts
#             if break_apart:
#                 if len(line.text) == 7:
#                     print(line.text[0:3])
#                     print(line.text[3:7])
#                 else:
#                     print(line.text[0:4])
#                     print(line.text[4:8])
#                 break_apart = False
#             else:
#                 break_apart = True                
#         else:
#             every_other = True
#     else:
#         oddOne = False
#     skip_every_third = skip_every_third + 1                
# pos = pos + 1


# More un-used code, might need later, deals with the problem of 3 digit vs 4 digit totals
    # lines = right.find_all("div")
    # for line in lines:
    #     # if first:
    #     #     first = False
    #         # df.at[row, 'Away_Opening'] = (line.text)[:-4]
    #         # df.at[row, 'Home_Opening'] = (line.text)[4:]
    #     if len(line.text) == 11:
    #         print((line.text)[0:4])
    #         print((line.text)[4:7])
    #         print((line.text)[7:12])

    #     if len(line.text) == 12:
    #         print((line.text)[0:5])
    #         print((line.text)[5:8])
    #         print((line.text)[8:13])

# We already have this data in our money-line database
# We might be able to edit this later
# center_games = soup.find_all("td", {"class":"alignCenter"})
# for center in center_games:
#         #  CENTER  #
#     scores = center.find_all("div")
#     # if skip_every_third % 3 != 0:
#     for score in scores:
#         print(row)
#         print(score.text)
#         # df.at[row, center_cols[pos]] = score.text
#         pos = pos + 1
#     row = row + 1
#     # skip_every_third = skip_every_third + 1