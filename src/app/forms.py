from wtforms import Form, TextField, validators
from flask_wtf import FlaskForm

class MonthForm(FlaskForm):
    month = TextField('Month:', validators=[validators.required()])

class DateForm(FlaskForm):
    date = TextField('Date:', validators=[validators.required()])

class ContestForm(FlaskForm):
    contest = TextField('Contest:', validators=[validators.required()])