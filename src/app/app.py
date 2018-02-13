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


if __name__ == "__main__":
    app.run(debug=True)
