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
    admin_code = StringField('Admin Code', validators=[DataRequired()])
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

class EditProduct(FlaskForm):
    product_name = StringField('Name', validators=[validators.Optional()])
    product_price = IntegerField('Price',  validators=[validators.Optional()])
    primary_product_image = FileField('File', validators=[validators.Optional()])
    show_sizes = BooleanField('Show Product Sizes?', validators=[validators.Optional()])
    product_in_stock = BooleanField('In Stock?', validators=[validators.Optional()])
    description = TextAreaField('Product Description', validators=[validators.Optional()])
    product_id = HiddenField()
    order_number = HiddenField()

class AddDesign(FlaskForm):
    design_name = StringField('Design Name', validators=[DataRequired()])
    design_image = FileField('Design Image', validators=[DataRequired()])
    design_icon = FileField('Design Icon', validators=[DataRequired()])

class EditDesign(FlaskForm):
    edit_design_name = StringField('Design Name', validators=[validators.Optional()])
    edit_design_image = FileField('Design Image', validators=[validators.Optional()])
    edit_design_icon = FileField('Design Icon', validators=[validators.Optional()])
    design_id = HiddenField()

class CreateProduct(FlaskForm):
    product_name = StringField('Product Name', validators=[validators.Optional()])
    product_price = IntegerField('Product Price',  validators=[validators.Optional()])
    primary_product_image = FileField('File', validators=[validators.Optional()])
    show_sizes = BooleanField('Show Sizes?', validators=[validators.Optional()])
    product_in_stock = BooleanField('In Stock?', validators=[validators.Optional()])
    description = TextAreaField('Product Description', validators=[validators.Optional()])

class InternalOrderNote(FlaskForm):
    note = TextAreaField('A note for yourself about this order', validators=[validators.DataRequired()])
    orderID = HiddenField()

class OrderStatusForm(FlaskForm):
    status_choices = [('0', 'Waiting to ship'), ('1', 'Shipping'), ('2', 'Delivered to customer')]
    status = SelectField(validators=[DataRequired()], choices=status_choices)
    orderID = HiddenField()

class ReOrderProducts(FlaskForm):
    new_order_array = StringField('Ordering', validators=[validators.Optional()])

class ChangePrimaryColor(FlaskForm):
    new_color = HiddenField()

class ChangeLandingImage(FlaskForm):
    new_landing_image = FileField('New Landing Image')

class ChangeSiteFavicon(FlaskForm):
    new_favicon = FileField('New Favicon')

class ChangeSiteTitle(FlaskForm):
    new_site_title = StringField('New Website Title', validators=[validators.DataRequired()])

class ChangeLandingText(FlaskForm):
    new_landing_text = StringField('New Landing Text', validators=[validators.Optional()])
    new_call_to_action = StringField('New Call To Action', validators=[validators.Optional()])
    new_email_text = StringField('New Email Text', validators=[validators.Optional()])
    new_email_call_to_action = StringField('New Email Call To Action', validators=[validators.Optional()])

class ForgotForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit New Password')

class EditAccountDetails(FlaskForm):
    name = StringField('Change Name', validators=[validators.Optional()])
    email = EmailField('Change Email', validators=[validators.Optional()])
    password = PasswordField('Change Password', validators=[validators.Optional()])
    confirm = PasswordField(
        'Repeat New Password', validators=[validators.Optional(), EqualTo('password')])

#legal
class ChangeTermsConditions(FlaskForm):
    new_terms = TextAreaField('New Terms and Conditions', validators=[validators.DataRequired()])

class ChangePrivacyPolicy(FlaskForm):
    new_policy = TextAreaField('New Privacy Policy', validators=[validators.DataRequired()])

class ChangeUserAgreement(FlaskForm):
    new_agreement = TextAreaField('New User Agreement', validators=[validators.DataRequired()])