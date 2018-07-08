from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    tag = StringField('Player Tag', validators=[DataRequired()])
    password = StringField('Admin Key', validators=[DataRequired()])

    submit = SubmitField('Initiate')