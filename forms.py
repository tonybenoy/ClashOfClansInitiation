from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,RadioField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    tag = StringField('Player Tag', validators=[DataRequired()])
    submit = SubmitField('Read all')
    
class initform(FlaskForm):
    donwar = RadioField("Should you donate to war?",validators=[DataRequired()],choices=[("1","Yes"),("0","No")])
    mindon = StringField('Minimum Donations Required', validators=[DataRequired()])
    submits = SubmitField('Initiate')

class searchclan(FlaskForm):
    clantag =StringField("Clan Tag", validators=[DataRequired()])
    submits = SubmitField('Initiate')