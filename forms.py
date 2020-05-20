from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, StringField, IntegerField, FileField, BooleanField, SubmitField, SelectField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.fields.html5 import EmailField, DecimalRangeField
from wtforms import validators


class EmailForm(FlaskForm):
    email = EmailField('Your Email', validators=[DataRequired()])

class LogoForm(FlaskForm):
    new_logo = FileField('Your New Logo')

class AdminRegisterForm(FlaskForm):
    admin_code = IntegerField('Admin Code', validators=[DataRequired()])
    email = EmailField('Your Email', validators=[DataRequired()])
    name = StringField('Your Name, This is Optional', validators=[validators.Optional()])
    password = PasswordField('Your Password', validators=[DataRequired()])

class LoginForm(FlaskForm):
    email = EmailField('Your Email', validators=[DataRequired()])
    password = PasswordField('Your Password', validators=[DataRequired()])

class NewDiscount(FlaskForm):
    name = StringField('Discount Name (what customers will use)', validators=[DataRequired()])
    amount = IntegerField('Discount Amount (always just a number)', validators=[DataRequired()])
    type_choices = [('0', 'Percentage'), ('1', 'Cash Amount')]
    type = SelectField(validators=[DataRequired()], choices=type_choices)

class EmailCustomers(FlaskForm):
    subject = StringField('Subject', validators=[validators.Optional()])
    message = TextAreaField('Message', validators=[DataRequired()])
    attachment = FileField('Attach a file')
