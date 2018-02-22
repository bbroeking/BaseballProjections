from flask import Flask, render_template, request, session, redirect, url_for
from forms import MonthForm, DateForm, ContestForm

import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

################################################
##             Example Query                  ##
################################################

@app.route('/')
def mainmenu():
    conn = sqlite3.connect("/Users/broeking/Desktop/T.R.E.A./src/Database/trea.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM lineups WHERE month="April" AND date="4.22" AND contest="MLB 100K THUNDERDOME SINGLE ENTRY"')
    items = [dict(id=row[0],
                    Rank=row[1],
                    EntryName=row[2],
                    Points=row[3],
                    Lineup=row[4],
                    SP1=row[5],
                    SP2=row[6],
                    C=row[7],
                    First=row[8],
                    Second=row[9],
                    Third=row[10],
                    Short=row[11],
                    OF1=row[12],
                    OF2=row[13],
                    OF3=row[14],
                    blank=row[15],
                    month=row[16],
                    date=row[17],
                    contest=row[18]) for row in cursor.fetchall()]

    return render_template("table.html", items=items)

################################################
##        Structured User DB Search           ##
################################################

@app.route('/search', methods=['GET', 'POST'])
def search():
    # Data Collectors
    mf = MonthForm()
    df = DateForm()
    cf = ContestForm()
    emptyList = [" "]

    conn = sqlite3.connect("/Users/broeking/Desktop/T.R.E.A./src/Database/trea.db")
    cursor = conn.cursor()

    # Executes if we know contest
    if cf.validate_on_submit():
        cursor.execute('SELECT * FROM lineups where month = "' + session['month'] + '" AND date = "' + session['date'] + 
        '" AND contest = "' + cf.contest.data + '"')
        session['contest'] = cf.contest.data
        lineups = [dict(id=row[0],
                    Rank=row[1],
                    EntryName=row[2],
                    Points=row[3],
                    Lineup=row[4],
                    SP1=row[5],
                    SP2=row[6],
                    C=row[7],
                    First=row[8],
                    Second=row[9],
                    Third=row[10],
                    Short=row[11],
                    OF1=row[12],
                    OF2=row[13],
                    OF3=row[14],
                    blank=row[15],
                    month=row[16],
                    date=row[17],
                    contest=row[18]) for row in cursor.fetchall()]
        # return redirect(url_for('lineup', lineps=lineups))
        return render_template('search.html', months=emptyList, dates=emptyList, contests=emptyList,
                 mf=None, df=None, cf=None, lineups=lineups)

    # Executes if we know date
    if df.validate_on_submit():
        cursor.execute('SELECT DISTINCT contest FROM lineups where month = "' + session['month'] + '" AND date = ' + df.date.data)
        session['date'] = df.date.data
        contests  = [item[0] for item in cursor.fetchall()]
        return render_template('search.html', months=emptyList, dates=emptyList, contests=contests, mf=None, df=None, cf=cf)

    # Executes if we know the month
    if mf.validate_on_submit():
        cursor.execute('SELECT DISTINCT date FROM lineups where month = "' + mf.month.data + '"')
        session['month'] = mf.month.data
        dates  = [item[0] for item in cursor.fetchall()]
        return render_template('search.html', months=emptyList, dates=dates, contests=emptyList, mf=None, df=df, cf=None)

    # Initial return
    cursor.execute('SELECT DISTINCT month FROM lineups')
    months  = [item[0] for item in cursor.fetchall()]
    return render_template('search.html', months=months, dates=emptyList, contests=emptyList, mf=mf, df=None, cf=None)

################################################
##             Grabs User Query               ##
################################################

@app.route('/querydb', methods= ['POST', 'GET'])
def querydb():
    return render_template('querydb.html')

################################################
##              Lineups Display Page          ##
################################################

@app.route('/lineup', methods = ['POST', 'GET'])
def lineup():
    if request.method == 'POST':
        conn = sqlite3.connect("/Users/broeking/Desktop/T.R.E.A./src/Database/trea.db")
        cursor = conn.cursor()
        cursor.execute(request.form['text'])

        lineups = [dict(id=row[0],
        Rank=row[1],
        EntryName=row[2],
        Points=row[3],
        Lineup=row[4],
        SP1=row[5],
        SP2=row[6],
        C=row[7],
        First=row[8],
        Second=row[9],
        Third=row[10],
        Short=row[11],
        OF1=row[12],
        OF2=row[13],
        OF3=row[14],
        blank=row[15],
        month=row[16],
        date=row[17],
        contest=row[18]) for row in cursor.fetchall()]
        return render_template("lineup.html", lineups=lineups)

################################################
##            Vegas Display Page              ##
################################################

@app.route('/vegas', methods = ['POST', 'GET'])
def vegas():
    # Data Collectors
    mf = MonthForm()
    df = DateForm()
    cf = ContestForm()
    emptyList = [" "]

    conn = sqlite3.connect("/Users/broeking/Desktop/T.R.E.A./src/Database/trea.db")
    cursor = conn.cursor()

    # Executes if we know contest
    if cf.validate_on_submit():

        # Collect the Ownerships and Points for that day
        cursor.execute('SELECT * FROM ownerships where month = "' + session['month'] + '" AND date = "' + session['date'] + 
        '" AND contest = "' + cf.contest.data + '"')
        session['contest'] = cf.contest.data
        ownerships = [dict(id=row[0],
                    player=row[1],
                    drafted=row[2],
                    FPTS=row[3],
                    month=row[4],
                    date=row[5],
                    contest=row[6]) for row in cursor.fetchall()]

        # Collect the lines for that day
        cursor.execute('SELECT * FROM lines where date = "' + session['date'] + 
        '" AND year = "2017"')
        lines = [dict(id=row[0],
                    Away_Team = row[1],
                    Home_Team = row[2],
                    Away_Starter = row[3],
                    Home_Starter = row[4],
                    Start_Time = row[5],
                    Away_Final_Score = row[6], 	
                    Home_Final_Score = row[7],
                    Away_Opening = row[8],
                    Home_Opening = row[9],
                    Away_Westgate = row[10],
                    Home_Westgate = row[11],
                    Away_Mirage = row[12],
                    Home_Mirage = row[13],
                    Away_Station = row[14],
                    Home_Station = row[15],
                    Away_Pinnacle = row[16],
                    Home_Pinnacle = row[17],
                    Away_SIA = row[18],
                    Home_SIA = row[19],
                    Away_SBG = row[20],
                    Home_SBG = row[21],
                    Away_BetUS = row[22],
                    Home_BetUS = row[23],
                    Away_BetPhoenix = row[24],	
                    Home_BetPhoenix = row[25],
                    Away_EasyStreet = row[26],
                    Home_EasyStreet = row[27],
                    Away_Bovada = row[28],
                    Home_Bovada = row[29],
                    Away_Jazz = row[30],
                    Home_Jazz = row[31],
                    Away_Sportsbet = row[32],
                    Home_Sportsbet = row[33],
                    Away_Bookmaker = row[34],
                    Home_Bookmaker = row[35],
                    Away_DSI = row[36],
                    Home_DSI = row[37],
                    Away_AceSport = row[38],
                    Home_AceSport = row[39],
                    date = row[40],
                    year = row[41]) for row in cursor.fetchall()]

        # return redirect(url_for('lineup', lineps=lineups))
        return render_template('vegas.html', months=emptyList, dates=emptyList, contests=emptyList,
                 mf=None, df=None, cf=None, ownerships=ownerships, lines=lines)

    # Executes if we know date
    if df.validate_on_submit():
        cursor.execute('SELECT DISTINCT contest FROM ownerships where month = "' + session['month'] + '" AND date = ' + df.date.data)
        session['date'] = df.date.data
        contests  = [item[0] for item in cursor.fetchall()]
        return render_template('lines_search.html', months=emptyList, dates=emptyList, contests=contests, mf=None, df=None, cf=cf)

    # Executes if we know the month
    if mf.validate_on_submit():
        cursor.execute('SELECT DISTINCT date FROM ownerships where month = "' + mf.month.data + '"')
        session['month'] = mf.month.data
        dates  = [item[0] for item in cursor.fetchall()]
        return render_template('lines_search.html', months=emptyList, dates=dates, contests=emptyList, mf=None, df=df, cf=None)

    # Initial return
    cursor.execute('SELECT DISTINCT month FROM ownerships')
    months  = [item[0] for item in cursor.fetchall()]
    return render_template('lines_search.html', months=months, dates=emptyList, contests=emptyList, mf=mf, df=None, cf=None)

if __name__ == "__main__":
    app.run(debug=True)
