import hashlib
import sqlite3
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
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

from sqlalchemy.orm import relationship
from werkzeug.utils import secure_filename
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from ups import UPSConnection
import datetime
from random import randint
import os
import paypalstuff
import forms
from flask_user import roles_required, UserManager, UserMixin, login_required
from flask_sqlalchemy import SQLAlchemy
from flask import g, abort
from email import encoders
import hmac
from flask.logging import default_handler
from logging.config import dictConfig
import jwt
from time import time
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
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'ico'}
app.config['SECRET_KEY'] = str(os.environ['SECRET_KEY'])
app.config['SESSION_TYPE'] = 'redis'
app.config['UPLOAD_FOLDER'] = os.path.abspath('static/img')
app.config["USER_UNAUTHENTICATED_ENDPOINT"] = 'login'
app.config["USER_UNAUTHORIZED_ENDPOINT"] = 'login'
app.config['USER_APP_NAME'] = 'Alex apparel website'
app.config['USER_ENABLE_EMAIL'] = True
app.config['USER_ENABLE_USERNAME'] = False
app.config['USER_REQUIRE_RETYPE_PASSWORD'] = False
app.config['USER_EMAIL_SENDER_EMAIL'] = "Meow"
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'

pathToDB = os.path.abspath("database/database.db")

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

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection

@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        app.logger.info("called foreign key enforcement event")
        cursor.close()

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

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'User_Roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String(), db.ForeignKey('Users.email', ondelete='CASCADE', onupdate='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('Roles.id'))

class Role(db.Model):
    __tablename__ = 'Roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

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

class Email(db.Model):
    __tablename__ = 'CustomerEmail'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(50), unique=True)


class UserOrders(db.Model):
    __tablename__ = "User_Orders"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String())
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

#sizes are crossed with designs
class DesignSize(db.Model):
    __tablename__ = "design_sizes"
    id = db.Column(db.Integer(), primary_key=True)
    size_name = db.Column(db.String())
    design_id = db.Column(db.Integer(), db.ForeignKey('Product_Designs.id', ondelete='CASCADE', onupdate='CASCADE'))
    order_number = db.Column(db.Integer(), autoincrement=True)
    inventory = db.Column(db.Integer())

class ProductDesign(db.Model):
    __tablename__ = "Product_Designs"
    id = db.Column(db.Integer(), primary_key=True)
    product_id = db.Column(db.Integer(), db.ForeignKey('Display_Products.id', ondelete='CASCADE', onupdate='CASCADE'))
    design_name = db.Column(db.String())
    design_image = db.Column(db.String())
    design_icon = db.Column(db.String())
    design_sizes = db.relationship("DesignSize")


class DisplayProduct(db.Model):
    __tablename__ = "Display_Products"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Integer())
    description = db.Column(db.String())
    primary_product_image = db.Column(db.String())
    product_order_num = db.Column(db.Integer(), autoincrement=True)
    product_designs = db.relationship("ProductDesign")

class MaintenanceMode(db.Model):
    __tablename__ = "Maintenance"
    id = db.Column(db.Integer(), primary_key=True)
    status = db.Column(db.String())

class SitePrimaryColor(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    color = db.Column(db.String())

class LandingImage(db.Model):
    __tablename__ = "LandingImages"
    id = db.Column(db.Integer(), primary_key=True)
    file_path = db.Column(db.String())

class LandingText(db.Model):
    __tablename__ = "LandingTexts"
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String())

class TabTitle(db.Model):
    __tablename__ = "TabTitles"
    id = db.Column(db.Integer(), primary_key=True)
    title_text = db.Column(db.String())

class TabIcon(db.Model):
    __tablename__ = "Favicons"
    id = db.Column(db.Integer(), primary_key=True)
    icon = db.Column(db.String())

class CallToAction(db.Model):
    __tablename__ = "CTA"
    id = db.Column(db.Integer(), primary_key=True)
    call_text = db.Column(db.String())

class EmailText(db.Model):
    __tablename__ = "EmailText"
    id = db.Column(db.Integer(), primary_key=True)
    email_text = db.Column(db.String())

class EmailCallToAction(db.Model):
    __tablename__ = "EmailCTA"
    id = db.Column(db.Integer(), primary_key=True)
    email_cta = db.Column(db.String())

#legal stuff
class TermsAndConditions(db.Model):
    __tablename__ = "Terms"
    id = db.Column(db.Integer(), primary_key=True)
    terms = db.Column(db.String())

class PrivacyPolicy(db.Model):
    __tablename__ = "privacy_policy"
    id = db.Column(db.Integer(), primary_key=True)
    privacy_policy = db.Column(db.String())

class UserAgreement(db.Model):
    __tablename__ = "user_agreement"
    id = db.Column(db.Integer(), primary_key=True)
    user_agreement = db.Column(db.String())

class ShippingPolicy(db.Model):
    __tablename__ = "shipping_policy"
    id = db.Column(db.Integer(), primary_key=True)
    shipping_policy = db.Column(db.String())

class BusinessEmail(db.Model):
    __tablename__ = "business_email"
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String())

def get_display_products_in_order():
    return DisplayProduct.query.order_by(DisplayProduct.product_order_num)

def get_designs_for_product(id):
    return ProductDesign.query.filter_by(product_id=id)

def get_sizes_for_design_in_order(id):
    return DesignSize.query.filter_by(design_id=id).order_by(DesignSize.order_number)

def get_product_inventory(id):
    total_inventory_count = 0
    designs = ProductDesign.query.filter_by(product_id=id).all()
    for design in designs:
        total_inventory_count += design.inventory

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
    status = MaintenanceMode()
    status.id = 0
    status.status = "Off"
    db.session.add(status)
    db.session.commit()
    default_color = SitePrimaryColor()
    default_color.id = 0
    default_color.color = "#20B22B"
    db.session.add(default_color)
    db.session.commit()
    landing_image = LandingImage()
    landing_image.id = 0
    landing_image.file_path = "/static/img/colorado.jpg"
    db.session.add(landing_image)
    db.session.commit()
    landing_text = LandingText()
    landing_text.id = 0
    landing_text.text = "Welcome to the store, feel free to check out our selection!"
    db.session.add(landing_text)
    db.session.commit()
    site_icon = TabIcon()
    site_icon.id = 0
    site_icon.icon = "/static/img/favicon.ico"
    db.session.add(site_icon)
    db.session.commit()
    site_title = TabTitle()
    site_title.id = 0
    site_title.title_text = "Bainbridge Island Tee Co"
    db.session.add(site_title)
    db.session.commit()
    terms = TermsAndConditions()
    terms.id = 0
    terms.terms = "Terms and conditions here."
    db.session.add(terms)
    db.session.commit()
    default_logo = Logo()
    default_logo.id = 0
    default_logo.file_path = "/static/img/cart.jpg"
    db.session.add(default_logo)
    db.session.commit()
    landing_cta = CallToAction()
    landing_cta.id = 0
    landing_cta.call_text = "Browse Our Selection"
    db.session.add(landing_cta)
    db.session.commit()
    landing_email_text = EmailText()
    landing_email_text.email_text = "Stay in the loop for great discounts"
    db.session.add(landing_email_text)
    db.session.commit()
    landing_email_cta = EmailCallToAction()
    landing_email_cta.id = 0
    landing_email_cta.email_cta = "Subscribe Now"
    db.session.add(landing_email_cta)
    db.session.commit()
    #need user agreement and privacy policy
    user_agreement = UserAgreement()
    user_agreement.id = 0
    user_agreement.user_agreement = "This user agreement is a contract between you and Bainbridge Island Tee Co, Inc. governing your use of bainbridgeislandteeco.com and associated services. You agree to comply with all of the terms and conditions in this user agreement. We may revise this user agreement and any of the policies listed above from time to time. The revised version will be effective at the time we post it, unless otherwise noted. If our changes reduce your rights or increase your responsibilities we will provide notice to you of at least 21 days. We reserve the right to amend this agreement at any time without notice, subject to applicable law. By continuing to use our services after any changes to this user agreement become effective, you agree to abide and be bound by those changes. If you do not agree with any changes to this user agreement, you may close your account.Intellectual Property<br>Any and all logos, product images and names are intellectual property of Bainbridge Island Tee Co. Use of any Bainbridge Island Tee Co branding materials, or other intellectual materials will result in legal retaliation and potential penalties."
    db.session.add(user_agreement)
    db.session.commit()
    privacy_policy = PrivacyPolicy()
    privacy_policy.id = 0
    privacy_policy.privacy_policy = "At Bainbridge Island Tee Co, we appreciate the trust you place in us when you choose to visit our stores or use our websites and mobile applications—and we take that responsibility seriously. This Bainbridge Island Tee Co Privacy Policy (the 'Policy') describes how we collect and use personal information about you when you visit our website, use our mobile application, or call us on the phone. By 'personal information', we mean information that directly identifies you, such as your name, address, or email address. In this Policy, 'we' and 'our' mean Bainbridge Island Tee Co, Inc., and 'you' means any person who visits our website, uses our mobile application, or calls us on the phone. Your information is never shared after your visit, the only third parties that your information could be made visible to are PayPal and Gmail, which are essential to the store.<br>Intellectual Property<br>Any and all logos, product images and names are intellectual property of Bainbridge Island Tee Co. Use of any Bainbridge Island Tee Co branding materials, or other intellectual materials will result in legal retaliation and potential penalties."
    db.session.add(privacy_policy)
    db.session.commit()
    shipping_policy = ShippingPolicy()
    shipping_policy.shipping_policy = "You can expect to receive your package within two weeks!"
    shipping_policy.id = 0
    db.session.add(shipping_policy)
    db.session.commit()
    #business email
    current_email = BusinessEmail()
    current_email.id = 0
    current_email.email = "bainbridgeislandteeco@gmail.com"
    db.session.add(current_email)
    db.session.commit()

app.cli.add_command(create_tables)

user_manager = UserManager(app, db, User)

def get_current_business_email():
    main_email_object = BusinessEmail.query.first()
    return main_email_object.email

@app.route('/turn-on-maintenance-mode')
def turn_on_mode():
    maintenance_status = MaintenanceMode.query.first()
    maintenance_status.status = "On"
    db.session.add(maintenance_status)
    db.session.commit()
    flash('turned on maintenance mode')
    return redirect('/admin')

@app.route('/turn-off-maintenance-mode')
def turn_off_mode():
    maintenance_status = MaintenanceMode.query.first()
    maintenance_status.status = "Off"
    db.session.add(maintenance_status)
    db.session.commit()
    flash('turned off maintenance mode')
    return redirect('/admin')

@app.before_request
def check_for_maintenance():
    maintenance_status = MaintenanceMode.query.first()
    if current_user.is_authenticated is False and maintenance_status.status == "On" and request.path != url_for('maintenance') and request.path != url_for('login') and "js" not in request.path and "css" not in request.path and "myhook" not in request.path:
        return redirect(url_for('maintenance'))
        # Or alternatively, dont redirect
        # return 'Sorry, off for maintenance!', 503

@app.route('/maintenance')
def maintenance():
    return 'Sorry, off for maintenance!', 503


@app.context_processor
def inject_logo():
    descending = Logo.query.order_by(Logo.id.desc())
    last_item = descending.first()
    path = ""
    if last_item is not None:
        path = last_item.file_path
    primary_color = SitePrimaryColor.query.first()
    primary_color = primary_color.color
    landing_image = LandingImage.query.first()
    if landing_image is None:
        landing_image = 'None'
    else:
        landing_image = landing_image.file_path
    landing_text = LandingText.query.first()
    landing_text = landing_text.text
    site_title = TabTitle.query.first()
    site_title = site_title.title_text
    site_icon = TabIcon.query.first()
    site_icon = "/static/img/" + str(site_icon.icon)
    call_to_action = CallToAction.query.first()
    call_to_action = call_to_action.call_text
    email_text = EmailText.query.first()
    email_text = email_text.email_text
    email_cta = EmailCallToAction.query.first()
    email_cta = email_cta.email_cta
    business_email = BusinessEmail.query.first()
    business_email = business_email.email
    return dict(this_file_path=path,
                nav_products=get_display_products_in_order(),
                primary_color=primary_color,
                landing_image=landing_image,
                landing_text=landing_text,
                site_title=site_title,
                site_icon=site_icon,
                call_to_action=call_to_action,
                email_text=email_text,
                email_cta=email_cta,
                business_email=business_email
                )


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
#the next three views all need some of the same things
@app.route('/payment-success', methods=['GET', 'POST'])
def paymentsuccess():
    email_form = forms.EmailForm()
    if email_form.validate_on_submit():
        app.logger.info(email_form.email.data)
        this_email = Email()
        this_email.email = email_form.email.data
        db.session.add(this_email)
        db.session.commit()
    email = request.form['Email']
    #add this email to our customer email pool
    if Email.query.filter_by(email=email) is None:
        this_email = Email()
        this_email.email = email
        db.session.add(this_email)
        db.session.commit()
    paypalID = request.form['PayPalTransactionID']
    orderDeets = paypalstuff.GetOrder.get_order(paypalstuff.GetOrder, paypalID)
    address = orderDeets.result.purchase_units[0].shipping.address
    app.logger.info(orderDeets)
    address = address.address_line_1 + ", " + address.admin_area_2 + ", " + address.admin_area_1 + ", " + address.postal_code + ", " + address.country_code
    cart = json.loads(request.form["CartJSON"])
    new_order = UserOrders()
    new_order.user_id = email
    new_order.paypal_order_id = paypalID
    new_order.address = address
    new_order.status = 0
    #app.logger.info("customer note: " + request.form.=)
    try:
        new_order.customer_note = request.form["CustomerNote"]
    except KeyError:
        new_order.customer_note = ""
    new_order.order_date = date.today()
    db.session.add(new_order)
    db.session.commit()
    descending = UserOrders.query.order_by(UserOrders.id.desc())
    most_recent_order = descending.first()
    app.logger.info("got through saving the order to the db")
    order_total = 0

    #login to email
    smtpObj = smtplib.SMTP(host="smtp.gmail.com", port=587)
    smtpObj.starttls()
    smtpObj.login(get_current_business_email(), str(os.environ["SMTP_PASS"]))
    for item in cart:
        new_item = OrderItem()
        new_item.order_id = most_recent_order.id
        new_item.product_name = item["ProductName"]
        new_item.product_size = item["Size"]
        new_item.price = item["Price"]
        new_item.quantity = int(item["Quantity"])
        order_total += (float(new_item.price[1:]) * new_item.quantity)
        new_item.product_img_src = item["IMGSRC"]
        new_item.design = item["Design"]
        app.logger.info(new_item.__str__())
        db.session.add(new_item)
        db.session.commit()

        if item["SizeID"] is not '':
            #now we want to go through and decrement the correct size
            this_design_size = DesignSize.query.filter_by(id=item["SizeID"]).first()
            this_design_size.inventory = this_design_size.inventory - 1
            new_inventory = this_design_size.inventory
            db.session.add(this_design_size)
            db.session.commit()

            if new_inventory <= 1:
                try:
                    #lets send an email to the admins saying how low the inventory is for this size
                    html_body = render_template('email/inventory-low.html', product_name=item["ProductName"], design_name=item["Design"], size_name=item["Size"], current_inventory=new_inventory)
                    html = MIMEText(html_body, 'html')
                    msg = MIMEMultipart()
                    msg["From"] = get_current_business_email()
                    msg["To"] = get_current_business_email()
                    msg["Subject"] = "Inventory Low!"
                    msg.attach(html)
                    smtpObj.sendmail(msg["From"], msg["To"], msg.as_string())
                except SMTPException:
                    app.logger.info("there was a problem sending the inventory email")
    app.logger.info("got though saving all the order items to the database")
    # want to confirmation to email given by paypal for everyone, including not users.
    # we also want to send an email to the business to let them know there is a new order
    try:
        # send an email to the business
        html_body = render_template('email/new_order_email.html', cart=cart, paypalID=paypalID, email=email,
                                    address=address)
        html = MIMEText(html_body, 'html')
        msg = MIMEMultipart()
        msg["From"] = get_current_business_email()
        msg["To"] = get_current_business_email()
        msg["Subject"] = "New Order!"
        msg.attach(html)
        smtpObj.sendmail(msg["From"], msg["To"], msg.as_string())
        # send an email to the customer
        logo = Logo.query.first()
        logo = logo.file_path
        primary_color = SitePrimaryColor.query.first()
        primary_color = primary_color.color
        html_body = render_template('email/thank_you.html', cart=cart, paypalID=paypalID, address=address, logo=logo, primary_color=primary_color, customer_name=request.form["Customer_Name"], order_total="{:.2f}".format(order_total))
        html = MIMEText(html_body, 'html')
        msg = MIMEMultipart()
        msg["From"] = get_current_business_email()
        msg["To"] = request.form["Email"]
        msg["Subject"] = "Thank you for your order!"
        msg.attach(html)
        local_dir = os.path.dirname(os.path.realpath('__file__'))
        app.logger.info("local dir: " + local_dir)
        logo = logo[1:]
        app.logger.info("logo dir: " + logo)
        full_path = os.path.join(local_dir, str(logo))
        app.logger.info(full_path)
        image_stream = open(full_path, mode='rb')
        msgImage = MIMEImage(image_stream.read())
        image_stream.close()
        msgImage.add_header('Content-ID', '<logo>')
        msg.attach(msgImage)
        smtpObj.sendmail(msg["From"], msg["To"], msg.as_string())
        smtpObj.quit()
    except SMTPException:
        app.logger.info("there was a problem sending the confirmation email")
    display_products = get_display_products_in_order()
    designs = ProductDesign.query.all()
    #we also need sizes too
    sizes = DesignSize.query.all()
    return render_template("/aroma/index.html", email_form=email_form, display_products=display_products,
                           designs=designs, sizes=sizes)


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
    display_products = get_display_products_in_order()
    designs = ProductDesign.query.all()
    #we also need sizes too
    sizes = DesignSize.query.all()
    return render_template('/aroma/index.html', email_form=email_form, display_products=display_products,
                           designs=designs, sizes=sizes)

@app.route("/<product>", methods=('GET', 'POST'))
def product_view(product):
    email_form = forms.EmailForm()
    if email_form.validate_on_submit():
        print(email_form.email.data)
        this_email = Email()
        this_email.email = email_form.email.data
        db.session.add(this_email)
        db.session.commit()
    display_products = get_display_products_in_order()
    designs = ProductDesign.query.all()
    sizes = DesignSize.query.all()
    product_order_index = DisplayProduct.query.filter_by(id=product).first()
    return render_template('/aroma/index.html', scroll_product=product_order_index.product_order_num, email_form=email_form, display_products=display_products,
                           designs=designs, sizes=sizes)


@app.route('/admin-register', methods=('GET', 'POST'))
def register():
    admin_register_form = forms.AdminRegisterForm()
    if admin_register_form.admin_code.data == str(os.environ['ADMIN_CODE']) and admin_register_form.validate():
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
            flash("There is already an account in our system with that email. Please try again.")
            return redirect('/admin-register')
    elif request.method == 'POST':
        flash("Unable to validate form.")
    return render_template('/aroma/admin_register.html', admin_register_form=admin_register_form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    login_form = forms.LoginForm()
    if login_form.validate_on_submit():
        # check that this email doesnt already exist
        app.logger.info("form email: " + login_form.email.data)
        app.logger.info("form password: " + login_form.password.data)
        h = hashlib.md5(login_form.password.data.encode())
        password_hash_code = h.hexdigest()
        user_object = User.query.filter_by(id=login_form.email.data).first()
        app.logger.info(user_object)
        if user_object is not None and user_object.password == password_hash_code:
            # print(our_users.first().)
            app.logger.info("thinks that we're in")
            login_user(user_object)
            return redirect('/admin')
        else:
            flash("Unable to find user with those details, please try again")
            return redirect('/login')
    return render_template('/aroma/login.html', login_form=login_form)


@app.route("/admin", methods=('GET', 'POST'))
@roles_required(['Admin'])
def admin():
    maintenance_status = MaintenanceMode.query.first()
    if maintenance_status.status == "On":
        is_maintenance_mode = True
    else:
        is_maintenance_mode = False
    return render_template('/aroma/admin.html', maintenance_mode=is_maintenance_mode)

@app.route("/delete-design/<designID>", methods=('GET', 'POST'))
@roles_required(['Admin'])
def delete_design(designID):
    design_to_delete = ProductDesign.query.filter_by(id=designID).first()
    db.session.delete(design_to_delete)
    db.session.commit()
    return redirect('/manage-products')

@app.route("/delete-product/<productID>", methods=('GET', 'POST'))
@roles_required(['Admin'])
def delete_product(productID):
    product_to_delete = DisplayProduct.query.filter_by(id=productID).first()
    db.session.delete(product_to_delete)
    db.session.commit()
    return redirect('/manage-products')


@app.route("/manage-products", methods=('GET', 'POST'))
@roles_required(['Admin'])
def edit_products():
    #edit product form
    edit_product_form = forms.EditProduct()
    #edit design form
    edit_design_form = forms.EditDesign()
    #edit size form
    edit_size_form = forms.EditSize()
    edit_product_order = forms.ReOrderProducts()
    edit_size_order = forms.ReOrderSizes()
    app.logger.info("about to try to validate product forms")
    if edit_product_form.validate_on_submit() and edit_product_form.edit_product.data:
        app.logger.info("id= " + str(edit_product_form.data["product_id"]))
        this_display_product = DisplayProduct.query.filter_by(id=edit_product_form.data["product_id"]).first()
        this_display_product.name = edit_product_form.data["product_name"]
        this_display_product.price = edit_product_form.data["product_price"]
        this_display_product.description = edit_product_form.data["description"]
        this_display_product.product_order_num = int(edit_product_form.data["order_number"])
        image = request.files["primary_product_image"]
        if image and allowed_file(image.filename):
            app.logger.info("validated image form")
            filename = secure_filename(image.filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(img_path)
            this_display_product.primary_product_image = "/static/img/" + filename
            app.logger.info("this product image: " + this_display_product.primary_product_image)
        db.session.commit()
    elif edit_design_form.validate_on_submit() and edit_design_form.edit_design.data:
        this_design = ProductDesign.query.filter_by(id=edit_design_form.design_id.data).first()
        app.logger.info("thinks that we are in the edit design form")
        if this_design is not None:
            this_design.design_name = edit_design_form.edit_design_name.data
            image = request.files["edit_design_image"]
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
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
    elif edit_size_form.validate_on_submit() and edit_size_form.edit_size.data:
        app.logger.info("validated size form")
        app.logger.info("size id: " + edit_size_form.size_id.data)
        this_size = DesignSize.query.filter_by(id=edit_size_form.size_id.data).first()
        if this_size is not None:
            app.logger.info("found this size")
            app.logger.info("previous name: " + this_size.size_name)
            app.logger.info("new name: " + edit_size_form.size_name.data)
            this_size.size_name = edit_size_form.size_name.data
            this_size.inventory = int(edit_size_form.inventory.data)
            db.session.commit()
        else:
            app.logger.info("unable to find the right size")
    elif edit_product_order.new_order_array.data is not None and edit_product_order.new_order_array.data is not '':
        app.logger.info("new order array data: " + edit_product_order.new_order_array.data)
        #we should be able to validate these but jquery is fun
        new_order_id_arr = edit_product_order.new_order_array.data.split(',')
        app.logger.info("REORDER PRODUCT ARRAY[1]: " + str(new_order_id_arr))
        for idx, this_id in enumerate(new_order_id_arr):
            #get this particular product using its id
            current_product = DisplayProduct.query.filter_by(id=int(this_id)).first()
            current_product.product_order_num = idx
            db.session.add(current_product)
            db.session.commit()
    elif edit_size_order.new_size_order_arr.data is not None and edit_size_order.new_size_order_arr.data is not '':
        new_order_id_arr = edit_size_order.new_size_order_arr.data.split(',')
        app.logger.info("REORDER SIZE ARRAY[1]: " + str(new_order_id_arr))
        for idx, this_id in enumerate(new_order_id_arr):
            # get this particular product using its id
            current_size = DesignSize.query.filter_by(id=int(this_id)).first()
            current_size.order_number = idx
            db.session.add(current_size)
            db.session.commit()
    # we need to query all of the existing products and render them with the forms
    display_products = get_display_products_in_order()
    designs = ProductDesign.query.all()
    #we also need sizes too
    sizes = DesignSize.query.all()
    return render_template('/aroma/manage-products.html', edit_product_form=edit_product_form,
                           display_products=display_products, designs=designs, edit_design_form=edit_design_form, edit_product_order=edit_product_order, edit_size_form=edit_size_form, sizes=sizes, edit_size_order=edit_size_order)


@app.route("/new-product", methods=('GET', 'POST'))
@roles_required(['Admin'])
def new_product():
    new_product_form = forms.CreateProduct()
    if new_product_form.description.data is not None and new_product_form.validate():
        app.logger.info("validated product image")
        new_product = DisplayProduct()
        new_product.name = new_product_form.product_name.data
        new_product.price = float(new_product_form.product_price.data)
        new_product.description = new_product_form.description.data
        rows = len(DisplayProduct.query.all())
        app.logger.info("rows: " + str(rows))
        new_product.product_order_num = rows + 1
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
        flash("Successfully created new product: " + str(new_product.product_order_num))
    return render_template('/aroma/new-product.html', new_product_form=new_product_form)



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
    return render_template('/aroma/cart.html', discounts=discount_2d, shipping_policy=ShippingPolicy.query.first().shipping_policy)


@app.route("/terms-and-conditions")
def showtermspage():
    terms_and_conds = TermsAndConditions.query.first()
    terms_and_conds = terms_and_conds.terms
    return render_template('/aroma/terms.html', terms=terms_and_conds)


@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')

@app.route("/change-logo", methods=('GET', 'POST'))
@roles_required(['Admin'])
def change_logo_view():
    logo_form = forms.LogoForm()
    if logo_form.new_logo.data is not None and logo_form.validate():
        image = request.files["new_logo"]
        if 'new_logo' not in request.files:
            return redirect(request.url)
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            print(filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(img_path)
            logo = Logo.query.first()
            logo.file_path = "/static/img/" + filename
            db.session.add(logo)
            db.session.commit()
        image = request.files["new_favicon"]
        if 'new_favicon' not in request.files:
            return redirect(request.url)
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(img_path)
            image = TabIcon.query.first()
            image.icon = filename
            db.session.add(image)
            db.session.commit()
            flash("Successfully uploaded new tab icon.")
    return render_template('/aroma/changelogo.html', logo_form=logo_form)

@app.route("/discount-form", methods=('GET', 'POST'))
@roles_required(['Admin'])
def make_discount():
    new_discount_form = forms.NewDiscount()
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
    return render_template('/aroma/makediscount.html', new_discount_form=new_discount_form)

@app.route('/email-customers', methods=('GET', 'POST'))
@roles_required(['Admin'])
def email_all_customers():
    email_all_customers_form = forms.EmailCustomers()
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
        smtpObj = smtplib.SMTP(host="smtp.gmail.com", port=587)
        smtpObj.starttls()
        smtpObj.login(get_current_business_email(), str(os.environ["SMTP_PASS"]))
        app.logger.info("logged in")
        for customer in Email.query.all():
            body = email_all_customers_form.message.data
            msg = MIMEMultipart()
            msg["From"] = get_current_business_email()
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
            app.logger.info("about to try to send email")
            app.logger.info(smtpObj.sendmail(msg["From"], msg["To"], msg.as_string()))
        smtpObj.quit()
    return render_template('/aroma/emailallcustomers.html', email_all_customers=email_all_customers_form)

@app.route("/change-color", methods=('GET', 'POST'))
@roles_required(['Admin'])
def change_color():
    color_form = forms.ChangePrimaryColor()
    if color_form.validate_on_submit():
        color = SitePrimaryColor.query.first()
        color.color = color_form.new_color.data
        db.session.add(color)
        db.session.commit()
        flash("Successfully changed primary color.")
    return render_template("/aroma/changecolor.html", color_form=color_form)

@app.route("/change-landing-image", methods=('GET', 'POST'))
@roles_required(['Admin'])
def change_landing_image():
    landing_form = forms.ChangeLandingImage()
    if landing_form.new_landing_image.data is not None and landing_form.validate():
        image = request.files["new_landing_image"]
        if 'new_landing_image' not in request.files:
            return redirect(request.url)
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(img_path)
            image = LandingImage.query.first()
            image.file_path = "/static/img/" + filename
            db.session.add(image)
            db.session.commit()
            flash("Successfully uploaded new landing image.")
    return render_template('/aroma/changelandingimage.html', landing_image_form=landing_form)

@app.route("/change-landing-text", methods=('GET', 'POST'))
@roles_required(['Admin'])
def change_landing_text():
    text_form = forms.ChangeLandingText()
    if text_form.validate_on_submit():
        if text_form.new_landing_text.data != '':
            text = LandingText.query.first()
            text.text = text_form.new_landing_text.data
            db.session.add(text)
            db.session.commit()
        if text_form.new_call_to_action.data != '':
            call_to_action = CallToAction.query.first()
            call_to_action.call_text = text_form.new_call_to_action.data
            db.session.add(call_to_action)
            db.session.commit()
        if text_form.new_email_text.data != '':
            email_text = EmailText.query.first()
            email_text.email_text = text_form.new_email_text.data
            db.session.add(email_text)
            db.session.commit()
        if text_form.new_email_call_to_action.data != '':
            email_cta = EmailCallToAction.query.first()
            email_cta.email_cta = text_form.new_email_call_to_action.data
            db.session.add(email_cta)
            db.session.commit()
        flash("Successfully changed landing text.")
    return render_template("/aroma/changelandingtext.html", text_form=text_form)

@app.route("/change-business-name", methods=('GET', 'POST'))
@roles_required(['Admin'])
def change_site_title():
    title_form = forms.ChangeSiteTitle()
    if title_form.validate_on_submit():
        title = TabTitle.query.first()
        title.title_text = title_form.new_site_title.data
        db.session.add(title)
        db.session.commit()
        flash("Successfully changed landing site title.")
    return render_template("/aroma/changesitetitle.html", title_form=title_form)


@app.route("/change-terms-and-conditions", methods=('GET', 'POST'))
@roles_required(['Admin'])
def change_terms():
    terms_form = forms.ChangeTermsConditions()
    if terms_form.validate_on_submit():
        terms = TermsAndConditions.query.first()
        terms.terms = terms_form.new_terms.data
        db.session.add(terms)
        db.session.commit()
        flash("Successfully changed landing terms and conditions.")
    return render_template("/aroma/changetermsandconditions.html", terms_form=terms_form)

@app.route("/change-landing-details", methods=('GET', 'POST'))
@roles_required(['Admin'])
def landing_details_area():
    return render_template("/aroma/landingsummary.html")


from flask import send_from_directory

@app.route('/favicon.ico')
def favicon():
    favicon_file_name = TabIcon.query.first()
    favicon_file_name = favicon_file_name.icon
    app.logger.info("favicon file name: " + str(favicon_file_name))
    return send_from_directory(os.path.join(app.root_path, 'static'), favicon_file_name)

def get_user_token(email):
    # we want to use our database to get an id for this user from their email, we then use this id to generate a token that is unique to that user.
    return jwt.encode({'reset_password': email, 'exp': time() + 600}, app.config['SECRET_KEY'],
                      algorithm='HS256').decode('utf-8')


def verify_reset_password_token(token):
    try:
        id = jwt.decode(token, app.config['SECRET_KEY'],
                        algorithms=['HS256'])['reset_password']
    except:
        return -1
    return id

@app.route('/forgot', methods=('GET', 'POST'))
def forgot():
    forgot_form = forms.ForgotForm()
    if forgot_form.validate_on_submit():
        email = str(forgot_form.email.data)
        user_object = User.query.filter_by(id=forgot_form.email.data).first()
        app.logger.info(user_object)
        if user_object is None:
            flash("Unable to find user with those details, please try again")
            # return render_template('forms/login.html', form=form)
            return redirect("/login")
        else:
            token = get_user_token(email)
            smtpObj = smtplib.SMTP(host="smtp.gmail.com", port=587)
            smtpObj.starttls()
            smtpObj.login(get_current_business_email(), str(os.environ["SMTP_PASS"]))
            html_body = render_template('email/reset_password.html', token=token)
            html = MIMEText(html_body, 'html')
            msg = MIMEMultipart()
            msg["From"] = get_current_business_email()
            msg["To"] = email
            msg["Subject"] = "Reset Password"
            msg.attach(html)
            smtpObj.sendmail(get_current_business_email(), msg["To"], msg.as_string())
            smtpObj.quit()
            flash("Successfully sent reset email to: " + str(email) + ".")
            # except :
    return render_template('/aroma/forgot.html', forgot_form=forgot_form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = verify_reset_password_token(token)
    if user == -1:
        return redirect("/")
    else:
        reset_form = forms.ResetPasswordForm()
        if reset_form.validate_on_submit():
            password = reset_form.password.data
            h = hashlib.md5(password.encode())
            hashvalue = h.hexdigest()
            user_object = User.query.filter_by(email=user).first()
            user_object.password = hashvalue
            db.session.add(user_object)
            db.session.commit()
            login_user(User.query.filter_by(email=user).first())
            return redirect("/admin")
    return render_template('/aroma/reset_password.html', reset_form=reset_form)

@app.route("/delete-order/<order_id>", methods=('GET', 'POST'))
@roles_required(['Admin'])
def delete_order(order_id):
    order_to_delete = UserOrders.query.filter_by(id=order_id).first()
    db.session.delete(order_to_delete)
    db.session.commit()
    flash("Deleted order successfully.")
    return redirect('/manage-orders')

@app.route("/admin-account-settings", methods=('GET', 'POST'))
@roles_required(['Admin'])
def edit_admin_account_details():
    edit_admin_settings = forms.EditAccountDetails()
    if edit_admin_settings.validate_on_submit():
        current_user_id = current_user.id
        if edit_admin_settings.name.data != '':
            current_user.name = edit_admin_settings.name.data
            flash("Successfully changed name to " + current_user.name + ".")
        if edit_admin_settings.email.data != '' and User.query.filter_by(id=edit_admin_settings.email.data).first() is None:
            current_user.id = edit_admin_settings.email.data
            current_user.email = edit_admin_settings.email.data
            current_user_id = edit_admin_settings.email.data
            flash("Successfully changed email to " + current_user.id + ".")
        if edit_admin_settings.confirm.data != '':
            h = hashlib.md5(edit_admin_settings.confirm.data.encode())
            hashvalue = h.hexdigest()
            current_user.password = hashvalue
            flash("Successfully changed password.")
        db.session.commit()
        logout()
        user = User.query.filter_by(id=current_user_id).first()
        login_user(user)
    return render_template("/aroma/admin-account-settings.html", form=edit_admin_settings)

@app.route("/delete-account")
@roles_required(['Admin'])
def delete_admin_account():
    current_user_id = current_user.id
    logout_user()
    previously_authed_user = User.query.filter_by(id=current_user_id).first()
    db.session.delete(previously_authed_user)
    db.session.commit()
    return redirect('/')

@app.route('/privacy-policy')
def privacy_policy_view():
    policy = PrivacyPolicy.query.first()
    policy = policy.privacy_policy
    return render_template("/aroma/privacy-policy.html", privacy_policy=policy)

@app.route('/user-agreement')
def user_agreement_view():
    agreement = UserAgreement.query.first()
    agreement = agreement.user_agreement
    return render_template("/aroma/user-agreement.html", user_agreement=agreement)

@app.route('/legal')
@roles_required(['Admin'])
def admin_legal_view():
    return render_template('/aroma/legal-summary.html')

@app.route("/change-privacy-policy", methods=('GET', 'POST'))
@roles_required(['Admin'])
def change_privacy_policy():
    form = forms.ChangePrivacyPolicy()
    if form.validate_on_submit():
        policy = PrivacyPolicy.query.first()
        policy.privacy_policy = form.new_policy.data
        db.session.add(policy)
        db.session.commit()
        flash("Successfully changed privacy policy.")
    return render_template("/aroma/change-privacy-policy.html", form=form)

@app.route("/change-user-agreement", methods=('GET', 'POST'))
@roles_required(['Admin'])
def change_user_agreement():
    form = forms.ChangeUserAgreement()
    if form.validate_on_submit():
        agreement = UserAgreement.query.first()
        agreement.user_agreement = form.new_agreement.data
        db.session.add(agreement)
        db.session.commit()
        flash("Successfully changed user agreement.")
    return render_template("/aroma/change-user-agreement.html", form=form)

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

@app.route("/new-size/<productID>/<designID>", methods=('GET', 'POST'))
@roles_required(['Admin'])
def create_size(productID, designID):
    new_size_form = forms.CreateSize()
    if new_size_form.size_name.data is not None and new_size_form.validate():
        new_size = DesignSize()
        app.logger.info("size name: " + new_size_form.size_name.data)
        new_size.size_name = new_size_form.size_name.data
        new_size.inventory = new_size_form.inventory.data
        new_size.design_id = designID
        db.session.add(new_size)
        db.session.commit()
        flash("Successfully created a new size for product " + productID)
    return render_template('/aroma/create-design-size.html', new_size_form=new_size_form)

@app.route("/delete-size/<sizeID>", methods=('GET', 'POST'))
@roles_required(['Admin'])
def delete_size(sizeID):
    size_to_delete = DesignSize.query.filter_by(id=sizeID).first()
    db.session.delete(size_to_delete)
    db.session.commit()
    return redirect('/manage-products')

@app.route("/change-shipping-policy", methods=('GET', 'POST'))
@roles_required(['Admin'])
def change_shipping_policy():
    form = forms.ChangeShippingPolicy()
    if form.validate_on_submit():
        agreement = ShippingPolicy.query.first()
        agreement.shipping_policy = form.new_policy.data
        db.session.add(agreement)
        db.session.commit()
        flash("Successfully changed shipping policy.")
    return render_template("/aroma/shipping-policy.html", form=form)

@app.route("/business-details")
@roles_required(['Admin'])
def admin_company_summary():
    return render_template('/aroma/company-details-section.html')

@app.route("/change-business-email", methods=('GET', 'POST'))
@roles_required(['Admin'])
def change_business_email():
    email_form = forms.ChangeBusinessEmail()
    if email_form.validate_on_submit():
        email = BusinessEmail.query.first()
        email.email = email_form.new_email.data
        db.session.add(email)
        db.session.commit()
        flash("Successfully changed business email.")
    return render_template("/aroma/change-business-email.html", email_form=email_form)

def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


if __name__ == "__main__":
    # socketio.run(app)
    app.run(host='0.0.0.0', port='5050', debug=True)
