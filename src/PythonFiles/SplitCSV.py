import csv, os, glob, decimal
import pandas as pd
#import pymysql.cursor
import pymysql

# mysql -u root -p
#########################
# Dealing with csv's
#########################

months = [month for month in next(os.walk('.'))[1]]
for month in months:

    #########################
    # MySQLdb connection
    #########################

    mydb = pymysql.connect(host='192.168.99.100',
        user='root',
        passwd='1234Qwer',
        db=month)
    cursor = mydb.cursor()

    path = '/Users/broeking/Desktop/DKContests/' + month + '/'
    days = [day for day in next(os.walk(path))[1]]
    for day in days:
        curr_path = path + day
        if not os.path.exists(curr_path+'/split/'):
            os.makedirs(curr_path+'/split/')
        for root, dirs, files in os.walk(curr_path):
            if not dirs:
                print "Skipping split in" + root
            else:
                for file in files:
                    if file.endswith(".xlsx"):

                        ########################
                        # Break apart the csv file
                        ########################

                        print "month= " +root+ " file= " + file
                        df = pd.read_excel(root + "/" + file, encoding='utf-8')
                        team = df[['Rank', 'EntryName', 'Points', 'Lineup']]
                        ownership = df[['Player', "%Drafted", "FPTS"]]

                        team = team.dropna(axis=0, how='any')
                        ownership = ownership.dropna(axis=0, how='any')

                        contest = str(file)[:-5]
                        contest = contest.replace("#", "")
                        contest = contest.replace(" ", "")
                        contest = contest.replace("FANTASYBASEBALLWORLDCHAMPIONSHIP", "FBWC")
                        contest = contest.replace("-", "")
                        contest = contest.replace("&", "")
                        contest = contest.replace("(", "")
                        contest = contest.replace(")", "")
                        contest = contest.replace("[", "")
                        contest = contest.replace("]", "")
                        contest = contest.replace("!", "")
                        contest = contest.replace("'", "")
                        contest = contest.replace("$", "")
                        contest = contest.replace("TO1ST", "")
                        contest = contest.replace(".", "")
                        contest = contest.replace(",", "")
                        contest = contest.replace("%", "")

                        directory = str(root)
                        team.to_csv(directory+ '/split/'+contest+ '_team.csv', encoding='utf-8', index=False)
                        ownership.to_csv(directory+ '/split/' +contest+ '_ownership.csv', encoding='utf-8', index=False)

                        ########################
                        # Creating the tables
                        ########################
                        stripped_day = day.replace(".", "")

                        titleL = "lineups_"+stripped_day+"_"+contest
                        command  = ''.join(["create table IF NOT EXISTS ", titleL, "(e_id INTEGER(200) AUTO_INCREMENT PRIMARY KEY, Finish DECIMAL(50,3), \
                            EntryName VARCHAR(750), Points DECIMAL(65, 4), Lineup VARCHAR(750));"])
                        cursor.execute(command)

                        titleO = "ownership_"+stripped_day+"_"+contest
                        command = ''.join(["create table IF NOT EXISTS ", titleO, " (o_id INTEGER(200) AUTO_INCREMENT PRIMARY KEY, Player VARCHAR(50), \
                            Drafted DECIMAL(65, 4), FTPS DECIMAL(65, 4));"]);
                        cursor.execute(command)
                        mydb.commit()

                        ########################
                        # CSV to SQL Server
                        ########################
                        full = ''.join([directory, '/split/', contest, '_team.csv'])
                        queryL = ''.join(["LOAD DATA INFILE '", full, "' INTO TABLE ", titleL,
                            """ FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '""",
                            """\n""".encode('string_escape'), """' IGNORE 1 ROWS (Finish, EntryName, Points, Lineup)"""])
                        cursor.execute(queryL)
                        mydb.commit()

                        full = ''.join([directory, '/split/', contest, '_ownership.csv'])
                        queryO = ''.join(["LOAD DATA INFILE '", full, "' INTO TABLE ", titleO,
                            """ FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '""",
                            """\n""".encode('string_escape'), """' IGNORE 1 ROWS (Player, Drafted, FTPS)"""])
                        cursor.execute(queryO)
                        mydb.commit()

                        # cursor.execute("""LOAD DATA INFILE '/Users/broeking/Desktop/DKContests/April/4.11/split/102KGoldGlove_team.csv'
                        #     INTO TABLE lineups_411_102KGoldGlove
                        #     FIELDS TERMINATED BY ','
                        #     ENCLOSED BY '"'
                        #     LINES TERMINATED BY '\n'
                        #     IGNORE 1 ROWS
                        #     (Finish, EntryName, Points, Lineup)""")

                    elif file.endswith(".csv"):

                        ########################
                        # Break apart the csv file
                        ########################

                        print "month= " +root+ " file= " + file
                        df = pd.read_csv(root + "/" + file, encoding='utf-8')
                        team = df[['Rank', 'EntryName', 'Points', 'Lineup']]
                        ownership = df[['Player', "%Drafted", "FPTS"]]

                        ownership['%Drafted'] = ownership['%Drafted'].map(lambda x: str(x)[:-1])

                        team = team.dropna()
                        print team.head(5)
                        ownership = ownership.dropna()

                        contest = str(file)[:-5]
                        contest = contest.replace("#", "")
                        contest = contest.replace(" ", "")
                        contest = contest.replace("FANTASYBASEBALLWORLDCHAMPIONSHIP", "FBWC")
                        contest = contest.replace("-", "")
                        contest = contest.replace("&", "")
                        contest = contest.replace("(", "")
                        contest = contest.replace(")", "")
                        contest = contest.replace("[", "")
                        contest = contest.replace("]", "")
                        contest = contest.replace("!", "")
                        contest = contest.replace("'", "")
                        contest = contest.replace("$", "")
                        contest = contest.replace("TO1ST", "")
                        contest = contest.replace(".", "")
                        contest = contest.replace(",", "")
                        contest = contest.replace("%", "")


                        directory = str(root)
                        team.to_csv(directory+ '/split/'+contest+ '_team.csv', encoding='utf-8', index=False)
                        ownership.to_csv(directory+ '/split/' +contest+ '_ownership.csv', encoding='utf-8', index=False)

                        ########################
                        # Creating the tables
                        ########################

                        stripped_day = day.replace(".", "")

                        titleL = "lineups_"+stripped_day+"_"+contest
                        command  = ''.join(["create table IF NOT EXISTS ", titleL, "(e_id INTEGER(200) AUTO_INCREMENT PRIMARY KEY, Finish DECIMAL(50,3), \
                            EntryName VARCHAR(750), Points DECIMAL(65, 4), Lineup VARCHAR(750));"])
                        cursor.execute(command)

                        titleO = "ownership_"+stripped_day+"_"+contest
                        command = ''.join(["create table IF NOT EXISTS ", titleO, " (o_id INTEGER(200) AUTO_INCREMENT PRIMARY KEY, Player VARCHAR(50), \
                            Drafted DECIMAL(65, 4), FTPS DECIMAL(65, 4));"]);
                        cursor.execute(command)
                        mydb.commit()

                        ########################
                        # CSV to SQL Server
                        ########################

                        full = ''.join([directory, '/split/', contest, '_team.csv'])
                        queryL = ''.join(["LOAD DATA INFILE '", full, "' INTO TABLE ", titleL,
                            """ FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '""",
                            """\n""".encode('string_escape'), """' IGNORE 1 ROWS (Finish, EntryName, Points, Lineup)"""])
                        cursor.execute(queryL)
                        mydb.commit()

                        full = ''.join([directory, '/split/', contest, '_ownership.csv'])
                        queryO = ''.join(["LOAD DATA INFILE '", full, "' INTO TABLE ", titleO,
                            """ FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '""",
                            """\n""".encode('string_escape'), """' IGNORE 1 ROWS (Player, Drafted, FTPS)"""])
                        cursor.execute(queryO)
                        mydb.commit()
