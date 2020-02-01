from flask_wtf import FlaskForm
from wtforms import  StringField, TextAreaField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Optional, DataRequired, Length

class ViewForm(FlaskForm):
    key = StringField('Key', validators=[DataRequired(), Length(min=32, max=32)])
    password = PasswordField('Password')
    submit = SubmitField('View')
    
class ClipForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    clip = TextAreaField('Text', validators=[DataRequired()])
    duration = StringField('Duration', validators=[DataRequired()])
    access = BooleanField('Private')
    protected = BooleanField('Password Protect')
    password = PasswordField('Password')
    submit = SubmitField('Done')