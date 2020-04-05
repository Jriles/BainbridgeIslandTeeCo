from flask import Flask
from flask import render_template, session
from flask import url_for
#from flask_pymongo import PyMongo
from pymongo import*
from pymongo.errors import ConnectionFailure
from pymongo import MongoClient
from flask import request
from flask import Flask,redirect, flash
#from usps import USPSApi
from flask_user import login_required, UserManager, UserMixin
#from geopy.geocoders import Nominatim
import hashlib
import json
#import socketio
#import redis
#from flask_socketio import SocketIO
import socket
import io
import re
import smtplib
from smtplib import SMTPException
from smtpd import SMTPServer

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from ups import UPSConnection
import datetime
from random import randint
import os
sender = 'klikattatfootwear@gmail.com'
receivers = ['klikattatfootwear@gmail.com']

app = Flask(__name__)
client = MongoClient("mongodb+srv://jriley98:843134Jr@cluster0-sv54u.mongodb.net/test?retryWrites=true&w=majority")
db = client["products"]
invisocks = db["invisible_socks"]
users = db["users"]
products = db["products"]
firstproduct = products.find_one()["Name"], products.find_one()["Price"], products.find_one()["Category"], products.find_one()["imgurl"]
discounts = db["discounts"]
homeurl = "http://www.klikattatfootwear.com/"
#geolocator = Nominatim(user_agent="my-application")

app.config['SESSION_TYPE'] = 'redis'
#app.secret_key = 'mysecret'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'XYZ')
#socketio = SocketIO(app)
with open("cityLocations.txt", "r", encoding="utf-8") as f:
    cityLocationsList = list(f)

#h = hashlib.md5("843134Jr!".encode())
#hashvalue = h.hexdigest()
#newValues = {"$set": {"Password": hashvalue}}
#users.update({"Username": "Jriley9000"}, newValues)
#email server
smtpObj = smtplib.SMTP(host="smtp.gmail.com", port=587)
smtpObj.starttls()
print(smtpObj.login(sender, "mlstJ1998!"))
print("logged in")


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)
#print(cityLocationsList)
#import algorithms
#from algorithms.search import linear_search
#takes in city name and returns coordinates

def cityLocationSearch(cityName):
    citiesOfName = []
    cityName = cityName.lower()
    arrayOfStrings = cityName.split(" ")
    arrayOfStrings[0] = arrayOfStrings[0].capitalize()
    if arrayOfStrings.__len__() > 1:
        arrayOfStrings[1] = arrayOfStrings[1].capitalize()
        cityName = arrayOfStrings[0] + " " + arrayOfStrings[1]
    elif arrayOfStrings.__len__() < 2:
        cityName = arrayOfStrings[0]
    for c in cityLocationsList:
        if(c.__contains__("'" + cityName + "'")):
            citiesOfName.append(c)

    #if we have more than one city of the same name
    #pick the one with the greatest pop
    biggest = ""
    if(citiesOfName.__len__() > 1):
        for city in citiesOfName:
            numbers = re.findall(r"[+-]?\d+(?:\.\d+)?", str(city))
            if biggest == "":
                biggest = city
            else:
                curBiggestNumbers = re.findall(r"[+-]?\d+(?:\.\d+)?", str(biggest))
                curBiggestPop = curBiggestNumbers[2]
                if int(curBiggestPop) < int(numbers[2]):
                    biggest = city
        return biggest
    return citiesOfName[0]


def checksessionforuser():
    print(("username" in session))
    if ("username" in session) is False:
        print("thinks there is no one signed in yet")
        return "";
    else:
        print("thinks there is something in here for username")
        print(session["username"])
        return session["username"]

def checksessionforpoints():
    if ("username" in session) is True and session["username"] != "":
        points = users.find_one({"Username": session["username"]})
        points = points["Points"]
        return float(points)
    else:
        return 0.0
#we want to convert our discount code collection in our db to an array for safe passage
def discountDBtoArray():
    array = []
    for document in discounts.find():
        array.append(str(document["name"]))
    return array

def discountAmountDBToArray():
    array = []
    for document in discounts.find():
        array.append(str(document["amount"]))
    return array

@app.route('/payment-success', methods=['GET', 'POST'])
def paymentsuccess():
    idExists = True
    orderID = ""
    while idExists:
        orderID = random_with_N_digits(8)
        if db["Orders"].find({"OrderID": orderID}).count() > 0:
            idExists = True
        else:
            idExists = False
    names = []
    prices = []
    x = datetime.datetime.now()
    x = str(x)[0:10]
    x = x.replace("-", "/")
    shippingState = "Yet to ship"
    trackingID = ""
    newPoints = float(request.form["Points"])
    for field in request.form:
        if str(field).__contains__("Name"):
            names.append(request.form[field])
        elif str(field).__contains__("Price"):
            prices.append(request.form[field])

    treeStatus = "No"
    if str(request.form.get('tree-checkbox')) == "on":
        treeStatus = "Yes"

    order = {
        "_id": orderID,
        "Email": request.form["Email"],
        "OrderDate": x,
        "ProductNames": names,
        "ProductPrices": prices,
        "State": shippingState,
        "TrackingID": trackingID,
        "OrderID": orderID,
        "PayPalTransactionID": request.form["PayPalTransactionID"],
        "PlantTree": treeStatus
    }
    #save order to main/independent orders collection
    db["Orders"].insert_one(order)

    #want to confirmation to email given by paypal for everyone, including not users.
    #we also want to send an email to the business to let them know there is a new order
    try:
        #send an email to the business
        body = MIMEText("A store user just ordered something! Paypal ID: " + request.form["PayPalTransactionID"])
        msg = MIMEMultipart()
        msg["From"] = 'klikattatfootwear@gmail.com'
        msg["To"] = 'jriley9000@gmail.com'
        msg["Subject"] = "New Order!"
        msg.attach(body)
        smtpObj.sendmail(sender, msg["To"], msg.as_string())
        #send an email to the customer
        body = MIMEText("Thank you for your order!")
        msg = MIMEMultipart()
        msg["From"] = 'klikattatfootwear@gmail.com'
        msg["To"] = request.form["Email"]
        msg["Subject"] = "Thank you!"
        msg.attach(body)
        smtpObj.sendmail(sender, msg["To"], msg.as_string())
    except SMTPException:
        print("there was a problem sending the confirmation email")
    if checksessionforuser() != "":
        #if the user is signed in
        #get this user's orders and update it to add a new one
        users.find_one_and_update({"Username": session["username"]}, {'$addToSet': {'Orders': order}})
        currentPoints = users.find_one({"Username": session["username"]})
        currentPoints = currentPoints["Points"]
        currentPoints = float(currentPoints) + newPoints
        users.find_one_and_update({"Username": session["username"]}, {'$set': {'Points': currentPoints}})


    #clear cart values
    #add purchase to database
    #show in my account section
    return render_template("/aroma/index.html", value=checksessionforuser(), firstproduct=firstproduct)

@app.route('/login-enter', methods=['GET', 'POST'])
def login():
    urlstring = homeurl
    email = str(request.form['email'])
    password = str(request.form['password'])
    h = hashlib.md5(password.encode())
    passhash = h.hexdigest()
    potentialusers = users.find({'$and': [{"Email": email}, {"PasswordHash": passhash}]})
    check = potentialusers.count()
    print(check)
    if(check > 0):
        print("success!")
        urlstring = urlstring + "login-success"
        session["username"] = potentialusers[0]["Username"]
        session["points-value"] = potentialusers[0]["Points"]
        print(session["username"])
        return redirect(urlstring)
    else:
        print("failure!")
        urlstring = urlstring + "login-failure"
        return redirect(urlstring)

@app.route('/signup-enter', methods=['GET', 'POST'])
def signup(x=None, y=None):
    if request.method == 'POST':
        # do something to send email
        urlstring = homeurl
        formcontents = request.form
        #check to make sure nobody is using this email already
        emailvalue = str(formcontents['email'])
        emailCheck = users.find({"Email": emailvalue}).count()
        print(emailCheck)
        if emailCheck == 0:
            # do something
            password = formcontents['password']
            h = hashlib.md5(password.encode())
            hashvalue = h.hexdigest()
            user = {
                "Email": formcontents['email'],
                "Username": formcontents['username'],
                "PasswordHash": hashvalue,
                "Points": 0,
                "Orders": []
            }
            users.insert_one(user)
            try:
                body = MIMEText("Thanks for making an account, we hope it helps you save!")
                msg = MIMEMultipart()
                msg['From'] = 'klikattatfootwear@gmail.com'
                msg['To'] = formcontents['email']
                msg['Subject'] = 'Congrats on your new account!'
                msg.attach(body)
                smtpObj.sendmail(sender, formcontents['email'], msg.as_string())
                body = MIMEText("A store user just created an account")
                msg = MIMEMultipart()
                msg["From"] = 'klikattatfootwear@gmail.com'
                msg["To"] = 'jriley9000@gmail.com'
                msg["Subject"] = "New User!"
                msg.attach(body)
                smtpObj.sendmail(sender, msg["To"], msg.as_string())
                print("Successfully sent email")
            except SMTPException:
                print("Error: unable to send email")
            #login on successful signup with new account
            global currentUserName
            #print(currentUser["Username"])
            session["username"] = user["Username"]
            session["points-value"] = user["Points"]
            urlstring = urlstring + "signup-success"
            return redirect(urlstring)
        else:
            print("found this email in database")
            urlstring = urlstring + "signup-failure"
            return redirect(urlstring)

@app.route("/signup-success")
def signupsuccess():
    return redirect(homeurl + "myaccount")

@app.route("/login-success")
def loginsuccess():
    return redirect(homeurl + "myaccount")

@app.route("/")
def home():
    #socketio.emit("message", "data")
    return render_template('/aroma/index.html', value=checksessionforuser(), firstproduct=firstproduct)

@app.route("/<product>")
def product_view(product):
    return render_template('/aroma/index.html', value=checksessionforuser(), firstproduct=firstproduct, scroll_product=product)

@app.route("/login-failure")
def loginfailure():
    return render_template("/aroma/login.html", value=checksessionforuser())

@app.route("/signup-failure")
def failedtosignup():
    return render_template("/aroma/register.html", value=checksessionforuser())

@app.route("/ourstory")
def blog():
    return render_template('/aroma/blog.html', value=checksessionforuser())

@app.route("/shop/category1")
def shopcategory1():
    return render_template('/aroma/category.html', value=checksessionforuser())

@app.route("/mycart")
def thecart():
    return render_template('/aroma/cart.html', pointsValue=checksessionforpoints(),value=checksessionforuser(), discountDB=discountDBtoArray(), amountArray=discountAmountDBToArray())

@app.route("/websitesearch")
def search():
    return render_template('/aroma/search.html', value=checksessionforuser())

@app.route("/contact-us")
def contact():
    return render_template('aroma/contact.html', value=checksessionforuser())

@app.route("/login")
def loginpage():
    return render_template('aroma/login.html', value=checksessionforuser())

@app.route("/signup")
def signuppage():
    return render_template('aroma/register.html', value=checksessionforuser())

@app.route("/track-your-order")
def shipping():
    return render_template('aroma/tracking-order.html', value=checksessionforuser())

@app.route("/sample-product-page")
def sampleproduct():
    reviews = db["products"].find_one({"PageURL": request.base_url})["Reviews"]
    comments = db["products"].find_one({"PageURL": request.base_url})["Comments"]
    print(reviews)
    print(comments)
    return render_template('aroma/single-product.html', value=checksessionforuser(), comments=comments, reviews=reviews)

@app.route("/todays-promotion")
def todayspromotion():
    return render_template('aroma/todayspromotion.html', value=checksessionforuser())

#@app.route("/myaccount")
#def myaccount():
#    #get orders associated with this account
#    #only want ones with state "shipping"
#    #socketio.emit('message', {"data": "Passed data using socket"}, broadcast=True)
#    #currentLocations is a 2D array of orders and their associated travel history locations in longitude and latitude
#    username = checksessionforuser()
#    shippingOrders = users.find_one({"Username": username})
#    print(shippingOrders)
#    shippingOrders = shippingOrders["Orders"]
#    currentLocations = [None] * len(shippingOrders)
#    currentEvents = []
#    usps = USPSApi('000KLIKA1245')
#    ups = UPSConnection('AD6BC655AC6D6AB1',
#                        'jriley9000',
#                        '843134Jr!',
#                        debug=True)
##    count = 0
#    for document in shippingOrders:
#        print(document["State"])
#        if(str(document["State"]) == "Yet to ship"):
#            print("appended this event")
#            currentEvents.append("Shipping ASAP")
#            currentLocations[count] = ["47.258728, -122.465973"]
#        else:
#            print("this TrackingID: " + document["TrackingID"])
#            newLocations = []
#            if len(document["TrackingID"]) == 18:
#                print("thinks this is a ups tracking number")
#                thisTrackingID = document["TrackingID"]
#                print(thisTrackingID)
#                tracking = ups.tracking_info(thisTrackingID)
#                activitiesList = tracking.shipment_activities
#                currentEvent = activitiesList[0].get('Status').get('StatusType').get('Description')
#                for activity in activitiesList:
#                    location = activity["ActivityLocation"]
#                    address = location["Address"]
#                    city = address.get('City')
#                    if city is not None:
#                        cityStringArray = city.split()
#                        if cityStringArray.__len__() > 1:
#                            cityStringArray[0] = cityStringArray[0].lower()
#                            cityStringArray[0] = cityStringArray[0].capitalize()
#                            cityStringArray[1] = cityStringArray[1].lower()
#                            cityStringArray[1] = cityStringArray[1].capitalize()
#                            city = cityStringArray[0] + " " + cityStringArray[1]
#                        elif cityStringArray.__len__() == 1:
#                            city = cityStringArray[0]
#                            city = city.lower()
#                            city = city.capitalize()
#                        print("city name after processing: " + city)
#                        location = cityLocationSearch(city)
#                        location = re.findall(r"[+-]?\d+(?:\.\d+)?", str(location))
#                        longitude = location[0]
#                        latitude = location[1]
#                        newLocations.append(str(longitude) + ", " + str(latitude))
#                print(currentEvent)
#                currentEvents.append(str(currentEvent))
#                currentLocations[count] = newLocations
#                continue
#            else:
#                track = usps.track(document["TrackingID"])
#                eventChain = track.result.get("TrackResponse").get("TrackInfo").get("TrackDetail")
#                for event in eventChain:
#                    eventStringArray = str(event["EventCity"]).split()
#                    #check and make sure there is something for the first element, sometimes there isn't
#                    if(eventStringArray[0] != 'None'):
#                        if(eventStringArray.__len__() > 1):
#                            thisCity = eventStringArray[0] + " " + eventStringArray[1]
#                        elif(eventStringArray.__len__() == 1):
#                            thisCity = eventStringArray[0]
                        #location = geolocator.geocode(thisCity, timeout=None)
                        #make sure there isn't a state's initials thrown in with the city name (there often is).
#                        if (thisCity.split(" ").__len__() > 1):
#                            if (thisCity.split(" ")[1].__len__() == 2):
#                                thisCity = thisCity.split(" ")[0]
#                        location = cityLocationSearch(thisCity)
#                        location = re.findall(r"[+-]?\d+(?:\.\d+)?", str(location))
#                        longitude = location[0]
#                        latitude = location[1]
#                        newLocations.append(str(longitude) + ", " + str(latitude))
#                currentEvents.append(track.result.get("TrackResponse").get("TrackInfo").get("TrackSummary").get("Event"))
#                currentLocations[count] = newLocations
#        count += 1
#    print(currentEvents)
#    return render_template("aroma/myaccount.html", pointsValue=checksessionforpoints(),value=checksessionforuser(), shippingOrders=shippingOrders, currentLocations=currentLocations, currentEvents=currentEvents)

@app.route("/logout-success")
def logout():
    print("thinks there is something in here for username")
    session["username"] = ""
    session["points-value"] = ""
    return redirect(homeurl)

@app.route("/cart-login", methods=['GET', 'POST'])
def cartlogin():
    print("here")
    print(request)
    print(login())
    return render_template('/aroma/cart.html', pointsValue=checksessionforpoints(),value=checksessionforuser(), discountDB=discountDBtoArray(), amountArray=discountAmountDBToArray())

@app.route("/terms-and-conditions")
def showtermspage():
    return render_template('/aroma/terms.html')

@app.route("/settingsReset", methods=['GET', 'POST'])
def postSettingsChange():
    #get user document using session
    #insert document
    if request.form['email'] != "":
        newValues2 = {"$set": {"Email": request.form['email']}}
        users.update({"Username": session["username"]}, newValues2)
    if request.form['username'] != "":
        newValues2 = {"$set": {"Username": request.form['username']}}
        users.update({"Username": session["username"]}, newValues2)
        session["username"] = request.form['username']
    if request.form['password'] != "":
        password = request.form['password']
        h = hashlib.md5(password.encode())
        hashvalue = h.hexdigest()
        print(hashvalue)
        newValues2 = {"$set": {"PasswordHash": hashvalue}}
        users.update({"Username": session["username"]}, newValues2)

    return redirect(homeurl + "myaccount")

@app.route("/contactus-form", methods=['GET', 'POST'])
def contactusFunct():
    print("called contact us form funct")
    name = request.form["name"]
    email = request.form["email"]
    subject = request.form["subject"]
    message = request.form["message"]
    if(session["username"] != ""):
        #this way we can record if they have an account
        message={
            "Name": name,
            "Email": email,
            "Subject": subject,
            "Message": message,
            "Has-Account": True
        }
    else:
        message = {
            "Name": name,
            "Email": email,
            "Subject": subject,
            "Message": message,
            "Has-Account": False
        }


    try:
        body = MIMEText("We'll address your concern as quickly as possible!")
        msg = MIMEMultipart()
        msg['From'] = 'klikattatfootwear@gmail.com'
        msg['To'] = email
        msg['Subject'] = 'Thanks for contacting us!'
        msg.attach(body)
        smtpObj.sendmail(sender, email, msg.as_string())
        print("successfully sent email")
    except SMTPException:
        print("failed to send email")

    try:
        body = MIMEText("A store user just sent a message")
        msg = MIMEMultipart()
        msg["From"] = 'klikattatfootwear@gmail.com'
        msg["To"] = 'jriley9000@gmail.com'
        msg["Subject"] = "New User Message!"
        msg.attach(body)
        smtpObj.sendmail(sender, msg["To"], msg.as_string())
        print("Successfully sent email")
    except SMTPException:
        print("Error: unable to send email")
    db["contactus-forms"].insert_one(message)
    return redirect(homeurl + "contact-us")

@app.route("/submit-comment", methods=["GET", "POST"])
def submitComment():
    message = request.form["textarea"]
    print(redirect_url())
    comment = {
        "Username": session["username"],
        "Message": message,
        "Date-Time": request.form["time-date"]
    }
    #need product from url
    db["products"].update({"PageURL": redirect_url()}, {'$push': {'Comments': comment}})
    return redirect(redirect_url())

@app.route("/submit-review", methods=["GET", "POST"])
def submitReview():
    print(request.form["user-rating"])
    review = {
        "Username": session["username"],
        "Message": request.form["textarea"],
        "Star-rating": int(request.form["user-rating"]),
        "Date-Time": request.form["time-date"]
    }
    print(review["Star-rating"])
    db["products"].update({"PageURL": redirect_url()}, {'$push': {'Reviews': review}})
    return redirect(redirect_url())

def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)

if __name__ == "__main__":
    #socketio.run(app)
    app.run(debug=True)
