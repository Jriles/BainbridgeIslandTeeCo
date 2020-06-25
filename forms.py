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