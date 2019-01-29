####################################################
# IMPORTS  
####################################################

from flask import Flask
from flask_mongoalchemy import MongoAlchemy
from bson.objectid import ObjectId
from datetime import datetime
import feature

####################################################
# MONGO SETTING
####################################################

# FLASK SETTINGS
app= Flask(__name__)
if feature.checkParams:
    app.config['MONGOALCHEMY_CONNECTION_STRING'],app.config['MONGOALCHEMY_DATABASE']=feature.returnParameter()
else:
    print(" Issue with the database connectivity !!! ")
    exit
db = MongoAlchemy(app)

# generation secret key
app.secret_key=b'a=pGw%4L1tB{aK6'

####################################################
# USER CLASS  
####################################################

class Utilisateur(db.Document):
    """ Definition of the class for the management of the Users """
    firstname = db.StringField()
    lastname = db.StringField()
    username= db.StringField()
    password = db.StringField()
    email =db.StringField()

    
####################################################
# Application CLASS
###################################################

class Application(db.Document):
    """ Definition of the class for the management of the applications """
    systemname = db.StringField()
    systembusinessneed= db.StringField()
    systemdescription = db.StringField()
    systemtechnology = db.StringField()
    systemprovider =db.StringField()
    systemowner = db.StringField()
    systemstatus = db.StringField()
    systemurl = db.StringField()
    systemcategory = db.StringField()


####################################################
# Script CLASS
###################################################

class Script(db.Document):
    """ Definition of the class for the management of the Scripts """
    scriptname = db.StringField()
    scriptcategory = db.StringField()
    scriptdescription = db.StringField()
    scripttechnology = db.StringField()
    businessowner = db.StringField()
    executionfrequency = db.StringField()
    technicalfirstfocalpoint = db.StringField()

####################################################
# DHL Business Function CLASS
###################################################

class BusinessFunction(db.Document):
    """ Definition of the class for the business function """
    #businessname = db.StringField()
    #businessneed = db.StringField()
    #businessdescription = db.StringField()
    #businessechnology = db.StringField()
    #businessprovider = db.StringField()
    #businessowner = db.StringField()
    #businessstatus = db.StringField()
    #businessurl = db.StringField()

####################################################
# Internal Process CLASS
###################################################

class InternalProcess(db.Document):
    """ Definition of the class for the inetrnal process """
    #ipname = db.StringField()
    #ipdescription = db.StringField()
    #ipunit = db.StringField()
    #ipstatus = db.StringField()
    #ipdocumented = db.StringField()

####################################################
# Contract CLASS
###################################################

class Contract(db.Document):
    """ Definition of the class for the management of the Contracts """
    contractref = db.StringField()
    systemname = db.StringField()
    contractrenewtype = db.StringField()
    contractcost = db.StringField()
    contractstartingdate = db.StringField()
    contractendingdate = db.StringField()
    contractcomment = db.StringField()
    contractyear=db.StringField()
    contractdhlowner = db.StringField()
    contractinvoice = db.StringField()
    contractvendor = db.StringField()