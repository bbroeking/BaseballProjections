from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def mainmenu():
    conn = sqlite3.connect("/Users/broeking/Desktop/T.R.E.A./src/Database/trea.db")
    print("connected")
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

@app.route('/search')
def search():
    return render_template("hello.html")

if __name__ == "__main__":
    app.run(debug=True)
