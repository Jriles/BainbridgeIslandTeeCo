from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, StringField, IntegerField, FileField, BooleanField, SubmitField, SelectField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.fields.html5 import EmailField, DecimalRangeField
from wtforms import validators


class EmailForm(FlaskForm):
    email = EmailField('Your Email', validators=[DataRequired()])