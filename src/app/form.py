from wtforms import Form, StringField, SelectField
import sqlite3

 
class MonthSearchForm(Form):
    conn = sqlite3.connect("/Users/broeking/Desktop/T.R.E.A./src/Database/trea.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM lineups WHERE month="April" AND date="4.22" AND contest="MLB 100K THUNDERDOME SINGLE ENTRY"')

    choices = [('Artist', 'Artist'),
               ('Album', 'Album'),
               ('Publisher', 'Publisher')]
    select = SelectField('Search for music:', choices=choices)
    search = StringField('')

    class DateSearchForm(Form):
    conn = sqlite3.connect("/Users/broeking/Desktop/T.R.E.A./src/Database/trea.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM lineups WHERE month="April" AND date="4.22" AND contest="MLB 100K THUNDERDOME SINGLE ENTRY"')

    choices = [('Artist', 'Artist'),
               ('Album', 'Album'),
               ('Publisher', 'Publisher')]
    select = SelectField('Search for music:', choices=choices)
    search = StringField('')

    class ContestSearchForm(Form):
    conn = sqlite3.connect("/Users/broeking/Desktop/T.R.E.A./src/Database/trea.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM lineups WHERE month="April" AND date="4.22" AND contest="MLB 100K THUNDERDOME SINGLE ENTRY"')

    choices = [('Artist', 'Artist'),
               ('Album', 'Album'),
               ('Publisher', 'Publisher')]
    select = SelectField('Search for music:', choices=choices)
    search = StringField('')
