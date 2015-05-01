from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.fields import TextField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp
from google.appengine.api import users


class GuestBookForm(Form):
    description = TextField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')