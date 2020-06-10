import hashlib
import sqlite3
from email.mime.base import MIMEBase
from subprocess import TimeoutExpired, check_output

from flask import Flask, jsonify
from flask import render_template, session
from flask import url_for
# from flask_pymongo import PyMongo
from flask.cli import with_appcontext
from flask_login import logout_user, login_user, current_user
from pymongo import *
from pymongo.errors import ConnectionFailure
from pymongo import MongoClient
from flask import request
from flask import Flask, redirect, flash
from flask_mongoengine import MongoEngine
from datetime import date
import json
from pathlib import Path
import socket
import io
import re
import smtplib
from smtplib import SMTPException
from smtpd import SMTPServer

from werkzeug.utils import secure_filename
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from ups import UPSConnection
import datetime
from random import randint
import os
import paypalstuff

sender = 'bainbridgeislandteeco@gmail.com'
import forms
from flask_user import roles_required, UserManager, UserMixin, login_required
from flask_sqlalchemy import SQLAlchemy
from flask import g, abort
from email import encoders
import hmac
from flask.logging import default_handler
from logging.config import dictConfig
import logging

#configure logging for production
dictConfig({
    'version': 1,
    'formatters': {
        'f': {'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
    },
    'handlers': {
        'ch': {'class': 'logging.StreamHandler',
               'formatter': 'f',
               'level': 'DEBUG'},
        'fh': {'class': 'logging.FileHandler',
               'formatter': 'f',
               'filename': 'app.log',
               'level': 'DEBUG'}
    },
    'root': {
        'handlers': ['ch', 'fh'],
        'level': 'DEBUG',
    }
})

app = Flask(__name__)
import logging
from logging.handlers import RotatingFileHandler
app.logger.removeHandler(default_handler)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4'}

app.config['SESSION_TYPE'] = 'redis'
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['UPLOAD_FOLDER'] = os.path.abspath('static/img')
app.config["USER_UNAUTHENTICATED_ENDPOINT"] = 'login'
app.config["USER_UNAUTHORIZED_ENDPOINT"] = 'login'
app.config['USER_APP_NAME'] = 'Alex apparel website'
app.config['USER_ENABLE_EMAIL'] = True
app.config['USER_ENABLE_USERNAME'] = False
app.config['USER_REQUIRE_RETYPE_PASSWORD'] = False
app.config['USER_EMAIL_SENDER_EMAIL'] = sender
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'

pathToDB = os.path.abspath("database/database.db")
admin_code = 12345
# email server
smtpObj = smtplib.SMTP(host="smtp.gmail.com", port=587)
smtpObj.starttls()
print(smtpObj.login(sender, "rkadniupkausbhog"))
print("logged in")

db = SQLAlchemy(app)


# IMPORTANT: Make sure to specify this route (https://<this server>/myhook) on
# GitHub's webhook configuration page as "Payload URL".
@app.route("/myhook", methods=['POST'])
def github_webhook_endpoint():
    app.logger.info("called webhook route")
    # Extract signature header
    signature = request.headers.get("X-Hub-Signature")
    if not signature or not signature.startswith("sha1="):
        abort(400, "X-Hub-Signature required")

    # Create local hash of payload
    digest = hmac.new(str(os.environ['REPOSITORY_KEY']).encode(),
                      request.data, hashlib.sha1).hexdigest()

    # Verify signature
    if not hmac.compare_digest(signature, "sha1=" + digest):
        abort(400, "Invalid signature")

    # The signature was fine, let's parse the data
    request_data = request.get_json()

    # now we want to run our .sh file in our home page
    import subprocess
    os.environ['PATH'] = '/home/ubuntu/BainbridgeIslandTeeCo/BainbridgeIslandTeeCoenv/bin:/home/ubuntu/bin:/home/ubuntu/.local/bin:/usr/bin/git:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin'
    os.environ['GIT_SSH_COMMAND'] = "ssh -o IdentitiesOnly=yes -i /home/ubuntu/.ssh/id_rsa"
    app.logger.info("path: " + str(os.environ['PATH']))

    process =subprocess.Popen('git pull origin master', cwd="/home/ubuntu/BainbridgeIslandTeeCo", universal_newlines=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    app.logger.info(process.stdout.read())
    #now we need to restart the server
    restart_process = subprocess.Popen('sudo systemctl restart BainbridgeIslandTeeCo', cwd="/home/ubuntu/BainbridgeIslandTeeCo",
                               universal_newlines=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    app.logger.info(restart_process.stdout.read())
    app.logger.info("finished running the command")
    return "Okay, thank you, if you still care."


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(pathToDB)
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    # User Authentication fields
    email = db.Column(db.String(255), primary_key=True)
    email_confirmed_at = datetime.datetime.now()
    password = db.Column(db.String(255))
    roles = db.relationship('Role', secondary='User_Roles')
    active = True
    name = db.Column(db.String(255))
    id = db.Column(db.String(255))


class Role(db.Model):
    __tablename__ = 'Roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'User_Roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String(), db.ForeignKey('Users.email', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('Roles.id', ondelete='CASCADE'))


class Email(db.Model):
    __tablename__ = 'CustomerEmail'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(50), unique=True)


class UserOrders(db.Model):
    __tablename__ = "User_Orders"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String(), db.ForeignKey('Users.email', ondelete='CASCADE'))
    paypal_order_id = db.Column(db.String())
    address = db.Column(db.String())
    internal_note = db.Column(db.String())
    customer_note = db.Column(db.String())
    order_date = db.Column(db.String())
    status = db.Column(db.Integer())


class OrderItem(db.Model):
    __tablename__ = "Order_Item"
    id = db.Column(db.Integer(), primary_key=True)
    order_id = db.Column(db.Integer(), db.ForeignKey('User_Orders.id', ondelete='CASCADE'))
    product_name = db.Column(db.String())
    product_size = db.Column(db.String())
    price = db.Column(db.String())
    quantity = db.Column(db.Integer())
    product_img_src = db.Column(db.String())
    design = db.Column(db.String())


class Logo(db.Model):
    __tablename__ = "LogoImages"
    id = db.Column(db.Integer(), primary_key=True)
    file_path = db.Column(db.String())


class Discount(db.Model):
    __tablename__ = "Discounts"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    amount = db.Column(db.Integer())
    type = db.Column(db.String())


class DisplayProduct(db.Model):
    __tablename__ = "Display_Products"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Integer())
    in_stock = db.Column(db.Integer())
    description = db.Column(db.String())
    primary_product_image = db.Column(db.String())


class ProductDesign(db.Model):
    __tablename__ = "Product_Designs"
    id = db.Column(db.Integer(), primary_key=True)
    product_id = db.Column(db.Integer())
    design_name = db.Column(db.String())
    design_image = db.Column(db.String())
    design_icon = db.Column(db.String())


@app.cli.command("create_tables")
@with_appcontext
def create_tables():
    db.drop_all()
    db.create_all()
    admin_role = Role()
    admin_role.id = '1'
    admin_role.name = 'Admin'
    db.session.add(admin_role)
    db.session.commit()


app.cli.add_command(create_tables)

user_manager = UserManager(app, db, User)


@app.context_processor
def inject_logo():
    descending = Logo.query.order_by(Logo.id.desc())
    last_item = descending.first()
    path = ""
    if last_item is not None:
        path = last_item.file_path
    return dict(this_file_path=path)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


# print(cityLocationsList)
# import algorithms
# from algorithms.search import linear_search
# takes in city name and returns coordinates


# we want to convert our discount code collection in our db to an array for safe passage

@app.route('/payment-success', methods=['GET', 'POST'])
def paymentsuccess():
    email_form = forms.EmailForm()
    if email_form.validate_on_submit():
        print(email_form.email.data)
        this_email = Email()
        this_email.email = email_form.email.data
        db.session.add(this_email)
        db.session.commit()
    email = request.form['Email']
    paypalID = request.form['PayPalTransactionID']
    orderDeets = paypalstuff.GetOrder.get_order(paypalstuff.GetOrder, paypalID)
    address = orderDeets.result.purchase_units[0].shipping.address
    print(orderDeets)
    address = address.address_line_1 + ", " + address.admin_area_2 + ", " + address.admin_area_1 + ", " + address.postal_code + ", " + address.country_code
    cart = json.loads(request.form["CartJSON"])
    new_order = UserOrders()
    new_order.user_id = email
    new_order.paypal_order_id = paypalID
    new_order.address = address
    new_order.status = 0
    new_order.customer_note = request.form["CustomerNote"]
    new_order.order_date = date.today()
    db.session.add(new_order)
    db.session.commit()
    descending = UserOrders.query.order_by(UserOrders.id.desc())
    most_recent_order = descending.first()
    for item in cart:
        new_item = OrderItem()
        new_item.order_id = most_recent_order.id
        new_item.product_name = item["ProductName"]
        new_item.product_size = item["Size"]
        new_item.price = item["Price"]
        new_item.quantity = int(item["Quantity"])
        new_item.product_img_src = item["IMGSRC"]
        new_item.design = item["Design"]
        db.session.add(new_item)
        db.session.commit()

    # want to confirmation to email given by paypal for everyone, including not users.
    # we also want to send an email to the business to let them know there is a new order
    try:
        # send an email to the business
        html_body = render_template('email/new_order_email.html', cart=cart, paypalID=paypalID, email=email,
                                    address=address)
        html = MIMEText(html_body, 'html')
        msg = MIMEMultipart()
        msg["From"] = 'bainbrigeislandteeco@gmail.com'
        msg["To"] = 'bainbridgeislandteeco@gmail.com'
        msg["Subject"] = "New Order!"
        msg.attach(html)
        smtpObj.sendmail(msg["From"], msg["To"], msg.as_string())
        # send an email to the customer
        body = MIMEText("Thank you for your order!\n Your paypal transaction ID: " + paypalID)
        msg = MIMEMultipart()
        msg["From"] = 'bainbridgeislandteeco@gmail.com'
        msg["To"] = request.form["Email"]
        msg["Subject"] = "Thank you!"
        msg.attach(body)
        smtpObj.sendmail(msg["From"], msg["To"], msg.as_string())
    except SMTPException:
        print("there was a problem sending the confirmation email")
    return render_template("/aroma/index.html", email_form=email_form)


@app.route("/", methods=('GET', 'POST'))
def home():
    # socketio.emit("message", "data")
    email_form = forms.EmailForm()
    if email_form.validate_on_submit():
        app.logger.info(email_form.email.data)
        this_email = Email()
        this_email.email = email_form.email.data
        db.session.add(this_email)
        db.session.commit()
    display_products = query_db('SELECT * FROM Display_Products')
    designs = []
    for product in display_products:
        designs.append(query_db("SELECT * FROM Product_Designs where product_id='%s'" % product[0]))
    app.logger.info("products: " + str(len(display_products)))
    app.logger.info("designs: " + str(len(designs)))
    return render_template('/aroma/index.html', email_form=email_form, display_products=display_products,
                           designs=designs)


@app.route('/admin-register', methods=('GET', 'POST'))
def register():
    admin_register_form = forms.AdminRegisterForm()
    if admin_register_form.admin_code.data == admin_code and admin_register_form.validate():
        # check that this email doesnt already exist
        if User.query.filter_by(email=admin_register_form.email.data).count() == 0:
            # then there are no users who currently have this email
            # we want to insert this person into our users collection
            new_user = User()
            new_user.email = admin_register_form.email.data
            new_user.id = new_user.email
            password = admin_register_form.data["password"]
            h = hashlib.md5(password.encode())
            passhash = h.hexdigest()
            new_user.password = passhash
            new_user.name = admin_register_form.name.data
            new_user.confirmed_at = date.today()
            role = Role.query.filter_by(name="Admin").one()
            new_user.roles.append(role)
            db.session.add(new_user)
            db.session.commit()
            login_user(User.query.filter_by(email=admin_register_form.email.data).first())
            return redirect('/admin')
        else:
            return redirect('/admin-register')
    return render_template('/aroma/admin_register.html', admin_register_form=admin_register_form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    login_form = forms.LoginForm()
    if login_form.validate_on_submit():
        # check that this email doesnt already exist
        print("form email: " + login_form.email.data)
        print("form password: " + login_form.password.data)
        h = hashlib.md5(login_form.password.data.encode())
        password_hash_code = h.hexdigest()
        user_object = query_db(
            'SELECT * from Users WHERE email="%s" AND password="%s"' % (login_form.email.data, password_hash_code),
            one=True)
        if user_object is not None:
            # print(our_users.first().)
            user = User.query.filter_by(id=login_form.email.data).one()
            login_user(user)
            return redirect('/admin')
        else:
            flash("Unable to find user with those details, please try again")
            return redirect('/login')
    return render_template('/aroma/login.html', login_form=login_form)


@app.route("/admin", methods=('GET', 'POST'))
@roles_required(['Admin'])
def admin():
    # logo form
    logo_form = forms.LogoForm()
    new_discount_form = forms.NewDiscount()
    email_all_customers_form = forms.EmailCustomers()
    if logo_form.new_logo.data is not None and logo_form.validate():
        image = request.files["new_logo"]
        if 'new_logo' not in request.files:
            return redirect(request.url)
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            print(filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(img_path)
            logo = Logo()
            logo.file_path = "/static/img/" + filename
            db.session.add(logo)
            db.session.commit()
    if new_discount_form.name.data is not None and new_discount_form.validate():
        new_discount = Discount()
        new_discount.name = new_discount_form.name.data
        if new_discount_form.type.data == '0':
            new_discount.amount = float("." + str(new_discount_form.amount.data))
            new_discount.type = "percentage"
        else:
            new_discount.amount = int(new_discount_form.amount.data)
            new_discount.type = "cash"
        db.session.add(new_discount)
        db.session.commit()
        flash("Saved New Discount")
    if email_all_customers_form.subject.data is not None and email_all_customers_form.validate():
        image = request.files["attachment"]
        this_file_path = ""
        if 'attachment' not in request.files:
            return redirect(request.url)
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(img_path)
            this_file_path = img_path
        for customer in Email.query.all():
            body = email_all_customers_form.message.data
            msg = MIMEMultipart()
            msg["From"] = 'bainbridgeislandteeco@gmail.com'
            msg["To"] = customer.email
            msg["Subject"] = email_all_customers_form.subject.data
            msg.attach(MIMEText(body))
            part = MIMEBase('application', "octet-stream")

            if this_file_path is not '':
                part.set_payload(open(this_file_path, 'rb').read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                'attachment; filename="{}"'.format(Path(this_file_path).name))
                msg.attach(part)
            smtpObj.sendmail(msg["From"], msg["To"], msg.as_string())
    return render_template('/aroma/admin.html', logo_form=logo_form, new_discount_form=new_discount_form,
                           email_all_customers=email_all_customers_form)


@app.route("/new-design/<productID>", methods=('GET', 'POST'))
@roles_required(['Admin'])
def create_design(productID):
    new_design_form = forms.AddDesign()
    if new_design_form.design_name.data is not None and new_design_form.validate():
        image = request.files["design_image"]
        icon = request.files["design_icon"]
        if 'design_image' not in request.files or 'design_icon' not in request.files:
            return redirect(request.url)
        if (image and allowed_file(image.filename)) and (icon and allowed_file(icon.filename)):
            image_file_name = secure_filename(image.filename)
            icon_file_name = secure_filename(icon.filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file_name)
            image.save(img_path)
            icon_path = os.path.join(app.config['UPLOAD_FOLDER'], icon_file_name)
            icon.save(icon_path)
            new_design = ProductDesign()
            new_design.product_id = productID
            new_design.design_name = new_design_form.design_name.data
            new_design.design_image = "/static/img/" + image_file_name
            print(icon_file_name)
            new_design.design_icon = "/static/img/" + icon_file_name
            db.session.add(new_design)
            db.session.commit()
            flash("Successfully created a new design for product " + productID)
    return render_template('/aroma/create-design.html', new_design_form=new_design_form)


@app.route("/delete-design/<designID>", methods=('GET', 'POST'))
@roles_required(['Admin'])
def delete_design(designID):
    design_to_delete = ProductDesign.query.filter_by(id=designID).first()
    db.session.delete(design_to_delete)
    db.session.commit()
    return redirect('/manage-products')


@app.route("/manage-products", methods=('GET', 'POST'))
@roles_required(['Admin'])
def edit_products():
    edit_product_form = forms.EditProduct()
    edit_design_form = forms.EditDesign()
    if edit_product_form.product_name.data is not None and edit_product_form.validate():
        this_display_product = DisplayProduct.query.filter_by(id=edit_product_form.product_id.data).first()
        this_display_product.name = edit_product_form.product_name.data
        this_display_product.price = edit_product_form.product_price.data
        this_display_product.in_stock = edit_product_form.product_in_stock.data
        this_display_product.description = edit_design_form.description.data
        db.session.commit()
    if (
            edit_design_form.edit_design_name.data is not None or edit_design_form.edit_design_image.data is not None or edit_design_form.edit_design_icon.data is not None) and edit_design_form.validate():
        this_design = ProductDesign.query.filter_by(id=edit_design_form.design_id.data).first()
        if this_design is not None:
            this_design.design_name = edit_design_form.edit_design_name.data
            image = request.files["edit_design_image"]
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                print(filename)
                img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(img_path)
                this_design.design_image = "/static/img/" + filename
            icon = request.files["edit_design_icon"]
            if icon and allowed_file(icon.filename):
                icon_file_name = secure_filename(icon.filename)
                icon_path = os.path.join(app.config['UPLOAD_FOLDER'], icon_file_name)
                icon.save(icon_path)
                this_design.design_icon = "static/img/" + icon_file_name
            db.session.commit()
    # we need to query all of the existing products and render them with the forms
    display_products = query_db('SELECT * FROM Display_Products')
    designs = []
    for product in display_products:
        designs.append(query_db("SELECT * FROM Product_Designs where product_id='%s'" % product[0]))
    return render_template('/aroma/manage-products.html', edit_product_form=edit_product_form,
                           display_products=display_products, designs=designs, edit_design_form=edit_design_form)


@app.route("/new-product", methods=('GET', 'POST'))
@roles_required(['Admin'])
def new_product():
    new_product_form = forms.CreateProduct()
    if new_product_form.description.data is not None and new_product_form.validate():
        app.logger.info("validated product image")
        new_product = DisplayProduct()
        new_product.name = new_product_form.product_name.data
        new_product.price = float(new_product_form.product_price.data)
        new_product.in_stock = int(new_product_form.product_in_stock.data)
        new_product.description = new_product_form.description.data
        image = request.files["primary_product_image"]
        app.logger.info(image.filename)
        if image and allowed_file(image.filename):
            app.logger.info("decided that we can add the image")
            image_file_name = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file_name)
            image.save(image_path)
            new_product.primary_product_image = "static/img/" + image_file_name
            app.logger.info("finished with image")
        db.session.add(new_product)
        db.session.commit()
        flash("Successfully created new product: " + new_product.name)
    return render_template('/aroma/new-product.html', new_product_form=new_product_form)


@app.route("/<product>", methods=('GET', 'POST'))
def product_view(product):
    email_form = forms.EmailForm()
    if email_form.validate_on_submit():
        print(email_form.email.data)
        this_email = Email()
        this_email.email = email_form.email.data
        db.session.add(this_email)
        db.session.commit()
    display_products = query_db('SELECT * FROM Display_Products')
    designs = []
    for product in display_products:
        designs.append(query_db("SELECT * FROM Product_Designs where product_id='%s'" % product[0]))
    return render_template('/aroma/index.html', scroll_product=product, email_form=email_form, display_products=display_products,
                           designs=designs)


@app.route("/manage-orders", methods=('GET', 'POST'))
@roles_required(['Admin'])
def manage_orders():
    orders = query_db("SELECT * FROM User_Orders")
    order_items = []
    for order in orders:
        order_items.append(query_db("SELECT * FROM Order_Item WHERE order_id='%s'" % order[0]))

    internal_order_note = forms.InternalOrderNote()
    order_status_form = forms.OrderStatusForm()
    if internal_order_note.note.data is not None and internal_order_note.validate():
        this_order = UserOrders.query.filter_by(id=internal_order_note.orderID.data).first()
        this_order.internal_note = internal_order_note.note.data
        db.session.commit()
        return redirect("/manage-orders")
    if order_status_form.status.data is not None and order_status_form.validate():
        this_order = UserOrders.query.filter_by(id=order_status_form.orderID.data).first()
        print(order_status_form.status.data)
        this_order.status = int(order_status_form.status.data)
        db.session.commit()
        return redirect("/manage-orders")
    return render_template('/aroma/manage-orders.html', orders=orders, order_items=order_items,
                           internal_order_note=internal_order_note, order_status_form=order_status_form)


@app.route("/mycart")
def thecart():
    discounts_original_structure = query_db("SELECT * FROM Discounts")
    discount_2d = []
    for discount in discounts_original_structure:
        new_inner_array = []
        new_inner_array.append(discount[0])
        new_inner_array.append(discount[1])
        new_inner_array.append(discount[2])
        new_inner_array.append(discount[3])
        discount_2d.append(new_inner_array)
    return render_template('/aroma/cart.html', discounts=discount_2d)


@app.route("/terms-and-conditions")
def showtermspage():
    return render_template('/aroma/terms.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')


def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


if __name__ == "__main__":
    # socketio.run(app)
    app.run(host='0.0.0.0', port='5050', debug=True)
