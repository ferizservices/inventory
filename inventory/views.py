####################################################
####################################################
# ROUTE DEFINITIONS  
####################################################
####################################################

from flask import render_template,request,session,url_for,redirect,flash
from models import app,Utilisateur,Application,Script,Contract
from werkzeug.utils import secure_filename
import os
import csv

APP_ROOT= os.path.dirname(os.path.abspath(__file__))

def calcRecord(Rs):
    """ JUST RETURN THE NUMBER OF RECORSET OF ONE RECORDSET PASSED AS PARAMETER """
    myRs=Rs.query.all()
    recup=0
    for x in myRs:
        recup=recup +1
    return recup

@app.route("/")
def main():
    """ Default route of the application (Login) """
    return render_template('login.html')

@app.route("/showupload")
def showupload():
    """ In order to display the upload html page """ 
    try:
        if "username" in session:
            return render_template('uploadparam.html')
        else:
            return render_template('login.html')   
    except:
        return redirect(url_for('appError'))


@app.route("/menu")
def menu():
    """ In order to manage the menu of the application """ 
    try:
        if "username" in session:
            myUsername=session["username"]
            myRecordUser=calcRecord(Utilisateur)
            myRecordApplication=calcRecord(Application)
            myRecordScript=calcRecord(Script)
            myRecordContract=calcRecord(Contract)
            return render_template('index.html',myUsername=myUsername,myRecordUser=myRecordUser,myRecordApplication=myRecordApplication,myRecordScript=myRecordScript,myRecordContract=myRecordContract)
        else:
            return render_template('login.html')   
    except:
        return redirect(url_for('appError'))
 

@app.route("/logout")
def logout():
    """ In order to manage the logout of the application """ 
    try:
        # Release the session's variables
        session.pop("username",None)
        session.pop("sysytemname",None)
        session.pop("email",None)
        session.pop("scriptname",None)
        session.pop("contractref",None)
        return render_template('login.html')
    except:
        return redirect(url_for('appError'))


# bad url
@app.errorhandler(404) 
def not_found(error): 
    """ In order to manage the 404 error """ 
    flash('The page requested is not available in this App  !!! ','error')
    return render_template('error.html'), 404

# bad url
@app.route("/apperror")
def appError():
    """ In order to manage the unexpected error """ 
    flash('Something happened in the system !!! ','error')
    return render_template('general_error.html'), 404


####################################################
# UPLOAD MANAGEMENT
####################################################  
@app.route("/upload",methods=["POST"])
def upload():
    """ Retrieving the file from the request object """ 
    
    # creation of the folder on disk and upload the file selected
    target=os.path.join(APP_ROOT,"upload")
    
    if not os.path.isdir(target):
        os.mkdir(target)

#try :

    file=request.files["InputFile"]
    filename=file.filename
    destination="/".join((target,filename))
    file.save(destination)

    myTable=request.form["inputTable"]
    recImported=0
    
    # Management of the Scripts
    if myTable=="Script" :
        myFile=open(destination)
        reader=csv.reader(myFile)
        for row in reader:
            myScript=Script()
            myScript.scriptname=row[0]
            myScript.scriptcategory=row[1]
            myScript.scriptdescription=row[2]
            myScript.scripttechnology=row[3]
            myScript.businessowner=row[4]
            myScript.executionfrequency=row[5]
            myScript.technicalfirstfocalpoint=row[6]
            myScript.save()
            recImported+=1
        flash('Congratulations, {} Script(s) records have been imported recently !!! '.format(recImported), 'message')
        myFile.close()

    # Management of the Applications
    if myTable=="Application" :
        myFile=open(destination)
        reader=csv.reader(myFile)
        for row in reader:
            myApplication=Application()
            myApplication.systemname=row[0]
            myApplication.systembusinessneed=row[1]
            myApplication.systemdescription=row[2]
            myApplication.systemtechnology=row[3]
            myApplication.systemprovider=row[4]
            myApplication.systemowner=row[5]
            myApplication.systemstatus=row[6]
            myApplication.systemurl=row[7]
            myApplication.systemcategory=row[8]
            myApplication.save()
            recImported+=1
        flash('Congratulations, {} Application(s) records have been imported recently !!! '.format(recImported), 'message')
        myFile.close()
        
    # Management of the Contracts
    if myTable=="Contract" :
        myFile=open(destination)
        reader=csv.reader(myFile)
        for row in reader:
            myContract=Contract()
            myContract.contractref=row[0]
            myContract.systemname=row[1]
            myContract.contractrenewtype=row[2]
            myContract.contractcost=row[3]
            myContract.contractstartingdate=row[4]
            myContract.contractendingdate=row[5]
            myContract.contractcomment=row[6]
            myContract.contractyear=row[7]
            myContract.contractdhlowner=row[8]
            myContract.contractinvoice=row[9]
            myContract.contractvendor=row[10]
            myContract.save()
            recImported+=1
        flash('Congratulations, {} Contract(s) records have been imported recently !!! '.format(recImported), 'message')
        myFile.close()

#except:
#    flash('Sorry, check the inputs of the importation process !!! ', 'error')
#    return redirect(url_for('menu'))

    return redirect(url_for('menu'))
 
       

####################################################
# USER MANAGEMENT
####################################################  

@app.route("/listeuser")
def listeUser():
    """ List of User """
    try:
        if "username" in session:
            if "username" in session:
                myUser=Utilisateur.query.all()
                total=0
                for rec in myUser:
                    total=total+1
                myRecord=total
                return render_template('listeuser.html',myUser=myUser,myRecord=myRecord)
            else:
                return render_template('login.html')   
        else:
            flash('Unknown user !!! ','error')
            return render_template('login.html')
    except:
        return redirect(url_for('appError'))


@app.route("/createuser", methods=['GET', 'POST'])
def createUser():
    """ User creation """
    try:
        if "username" in session:
            if request.method == 'POST':
                myUser=Utilisateur(
                    firstname=request.form["inputFirstName"],
                    lastname=request.form["inputLastName"],
                    username=request.form["inputUserName"],
                    password=request.form["inputPassword"],
                    email=request.form["inputEmail"])
                myUser.save()
                flash('User saved !!! ', 'message')
                return redirect(url_for('listeUser'))
            if request.method == 'GET':
                return render_template('newuser.html')
        else:
            flash('Unknown user !!! ','error')
            return render_template('login.html')
    except:
        return redirect(url_for('appError'))


@app.route("/updateuser", methods=['POST'])
def updateUser():
    """ User update """
    try:
        if "username" in session:
            myUser=Utilisateur.query.filter(Utilisateur.email==session["email"]).first()
            myUser.firstname=request.form["inputFirstName"]
            myUser.lastname=request.form["inputLastName"]
            myUser.username=request.form["inputUserName"]
            myUser.password=request.form["inputPassword"]
            myUser.email=request.form["inputEmail"]
            myUser.save()
            flash('User updated !!! ', 'message')
            return redirect(url_for('listeUser'))
        else:
            flash('Unknown user !!! ','error')
            return render_template('login.html')
    except:
        return redirect(url_for('appError'))


@app.route("/displayuser/<email>", methods=['GET'])
def displayUser(email):
    """ Display one User record """
    try:    
        if "username" in session:
            if request.method == 'GET':
                session["email"]=email
                myUser=Utilisateur.query.filter(Utilisateur.email==email).first()
                return render_template('updateuser.html',myUser=myUser)
        else:
            flash('Unknown user !!! ','error')
            return render_template('login.html')
    except:
        return redirect(url_for('appError'))

#delete the user
@app.route("/delete/<email>", methods=['GET'])
def deleteUser(email):
    """ User deletion """
    try:      
        if "username" in session:
            if request.method == 'GET':
                myUserToDelete=Utilisateur.query.filter(Utilisateur.email==email).first()
                myUserToDelete.remove()
                flash('User deleted !!! ', 'message')
                return redirect(url_for('listeUser'))
        else:
            flash('Unknown user !!! ','error')
            return render_template('login.html')
    except:
        return redirect(url_for('appError'))

# check of the user exists
@app.route("/checkuser", methods=['POST'])
def checkUser():
    """ User check Identification """
#try: 
    # Tip for admin
    if (request.form["inputEmail"]=="admin@un.org" and request.form["inputPassword"]=="admin"):
        session["username"]="admin"
        return redirect(url_for('menu'))

    # Normal way
    myResult=Utilisateur.query.filter(Utilisateur.email==request.form["inputEmail"],Utilisateur.password==request.form["inputPassword"]).first()
    if myResult:
        session["username"]=myResult.username
        return redirect(url_for('menu'))
    else:
        flash('Unknown user !!! ','error')
        return render_template('login.html')
#except:
#    return redirect(url_for('appError'))

####################################################
# APPLICATION MANAGEMENT
####################################################  

@app.route("/listeapplication")
def listeApplication():
    """ Display the list of Application """
    if "username" in session:
        myApp=Application.query.all()
        total=0
        for rec in myApp:
            total=total+1
        myRecord=total
        return render_template('listeapplication.html',myApp=myApp,myRecord=myRecord)
    else:
        flash('Unknown user !!! ','error')
        return render_template('login.html')   


@app.route("/createapplication", methods=['GET', 'POST'])
def createApplication():
    """ User creation """
    try:   
        if "username" in session:
            if request.method == 'POST':
                myApp=Application(
                    systemname=request.form["inputSystemName"],
                    systembusinessneed=request.form["inputSystemBusinessNeed"],
                    systemdescription=request.form["inputSystemDescription"],
                    systemtechnology=request.form["inputSystemTechnology"],
                    systemprovider=request.form["inputSystemProvider"],
                    systemowner=request.form["inputSystemOwner"],
                    systemstatus=request.form["inputSystemStatus"],
                    systemurl=request.form["inputSystemUrl"],
                    systemcategory=request.form["inputSystemCat"]
                    )
                myApp.save()
                flash('Application saved !!! ', 'message')
                return redirect(url_for('listeApplication'))
            if request.method == 'GET':
                return render_template('createapplication.html')
        else:
            flash('Unknown user !!! ','error')
            return render_template('login.html')    
    except:
        return redirect(url_for('appError'))

@app.route("/updateapplication", methods=['POST'])
def updateApplication():
    """ Application update """
    try:    
        if "username" in session:
            myApp=Application.query.filter(Application.systemname==session["systemname"]).first()
            myApp.systemname=request.form["inputSystemName"]
            myApp.systembusinessneed=request.form["inputSystemBusinessNeed"]
            myApp.systemdescription=request.form["inputSystemDescription"]
            myApp.systemtechnology=request.form["inputSystemTechnology"]
            myApp.systemprovider=request.form["inputSystemProvider"]
            myApp.systemowner=request.form["inputSystemOwner"]
            myApp.systemstatus=request.form["inputSystemStatus"]
            myApp.systemurl=request.form["inputSystemUrl"]
            myApp.systemcategory=request.form["inputSystemCat"]
            myApp.save()
            flash('Application updated !!! ', 'message')
            return redirect(url_for('listeApplication'))
        else:
            flash('Unknown user !!! ','error')
            return render_template('login.html')
    except:
        return redirect(url_for('appError'))

@app.route("/displayapp/<systemname>", methods=['GET'])
def displayApp(systemname):
    """ Display one Application record """
    try:    
        if "username" in session:
            if request.method == 'GET':
                session["systemname"]=systemname
                myApp=Application.query.filter(Application.systemname==systemname).first()
                return render_template('updateapplication.html',myApp=myApp)
        else:
            flash('Unknown user !!! ','error')
            return render_template('login.html')
    except:
        return redirect(url_for('appError'))


#delete the application
@app.route("/deleteapplication/<systemname>", methods=['GET'])
def deleteApplication(systemname):
    """ Application deletion """
    try:       
        if "username" in session:
            if request.method == 'GET':
                myApp=Application.query.filter(Application.systemname==systemname).first()
                myApp.remove()
                flash('Application deleted !!! ', 'message')
                return redirect(url_for('listeApplication'))
        else:
            flash('Unknown user !!! ','error')
            return render_template('login.html')
    except:
        return redirect(url_for('appError'))

####################################################
# SCRIPT MANAGEMENT
####################################################  

@app.route("/listescript")
def listeScript():
    """ Display the list of script """
    try:          
        if "username" in session:
            myScript=Script.query.all()
            total=0
            for rec in myScript:
                total=total+1
            myRecord=total
            return render_template('listescript.html',myScript=myScript,myRecord=myRecord)
        else:
            flash('Unknown user !!! ','error')
            return render_template('login.html')   
    except:
        return redirect(url_for('appError'))

@app.route("/createscript", methods=['GET', 'POST'])
def createScript():
    """ Script creation """
    try:          
        if "username" in session:
            if request.method == 'POST':
                myScript=Script(
                    scriptname=request.form["inputScriptName"],
                    scriptcategory=request.form["inputScriptCategory"],
                    scriptdescription=request.form["inputScriptDescription"],
                    scripttechnology=request.form["inputScriptTechnology"],
                    businessowner=request.form["inputBusinessOwner"],
                    executionfrequency=request.form["inputExecutionFrequency"],
                    technicalfirstfocalpoint=request.form["inputTechnicalFirstFocalPoint"])
                myScript.save()
                flash('Script saved !!! ', 'message')
                return redirect(url_for('listeScript'))
            if request.method == 'GET':
                return render_template('createscript.html')
        else:
            flash('Unknown user !!! ','error')
            return render_template('login.html')    
    except:
        return redirect(url_for('appError'))
    

@app.route("/updatescript", methods=['POST'])
def updateScript():
    """ Script update """
    try:          
        if "username" in session:
            myScript=Script.query.filter(Script.scriptname==session["scriptname"]).first()
            myScript.scriptname=request.form["inputScriptName"]
            myScript.scriptcategory=request.form["inputScriptCategory"]
            myScript.scriptdescription=request.form["inputScriptDescription"]
            myScript.scripttechnology=request.form["inputScriptTechnology"]
            myScript.businessowner=request.form["inputBusinessOwner"]
            myScript.executionfrequency=request.form["inputExecutionFrequency"]
            myScript.technicalfirstfocalpoint=request.form["inputTechnicalFirstFocalPoint"]
            myScript.save()
            flash('Script updated !!! ', 'message')
            return redirect(url_for('listeScript'))
        else:
            flash('Unknown user !!! ','error')
            return render_template('login.html')
    except:
        return redirect(url_for('appError'))
    
    
@app.route("/displayscript/<scriptname>", methods=['GET'])
def displayScript(scriptname):
    """ Display one script record """
    try:       
        if "username" in session:
            if request.method == 'GET':
                session["scriptname"]=scriptname
                myScript=Script.query.filter(Script.scriptname==scriptname).first()
                return render_template('updatescript.html',myScript=myScript)
        else:
            flash('Unknown user !!! ','error')
            return render_template('login.html')
    except:
        return redirect(url_for('appError'))

#delete the application
@app.route("/deletescript/<scriptname>", methods=['GET'])
def deleteScript(scriptname):
    """ Script deletion """
    try:     
        if "username" in session:
            if request.method == 'GET':
                myScript=Script.query.filter(Script.scriptname==scriptname).first()
                myScript.remove()
                flash('Script deleted !!! ', 'message')
                return redirect(url_for('listeScript'))
        else:
            flash('Unknown user !!! ','error')
            return render_template('login.html')
    except:
        return redirect(url_for('appError'))


####################################################
# CONTRACT MANAGEMENT
####################################################  

@app.route("/listecontract")
def listeContract():
    """ Display the list of contract """
    try:      
        if "username" in session:
            myContract=Contract.query.all()
            total=0
            for rec in myContract:
                total=total+1
            myRecord=total
            return render_template('listecontract.html',myContract=myContract,myRecord=myRecord)
        else:
            flash('Unknown user !!! ','error')
            return render_template('login.html')   
    except:
        return redirect(url_for('appError'))

@app.route("/createcontract", methods=['GET', 'POST'])
def createContract():
    """ Contract creation """
    try:      
        if "username" in session:
            if request.method == 'POST':
                myContract=Contract(
                    contractref=request.form["inputContractReference"],
                    systemname=request.form["inputSystemName"],
                    contractrenewtype=request.form["inputRenewType"],
                    contractcost=request.form["inputContractCost"],
                    contractstartingdate=request.form["inputContractStartingDate"],
                    contractendingdate=request.form["inputContractEndingDate"],
                    contractcomment=request.form["inputContractComment"],
                    contractyear=request.form["inputContractYear"],
                    contractdhlowner=request.form["inputDHLOwner"],
                    contractinvoice=request.form["inputInvoice"],
                    contractvendor=request.form["inputContractVendor"])
                myContract.save()
                flash('Contract saved !!! ', 'message')
                return redirect(url_for('listeContract'))
            if request.method == 'GET':
                return render_template('createcontract.html')
        else:
            flash('Unknown user !!! ','error')
            return render_template('login.html')
    except:
        return redirect(url_for('appError'))

@app.route("/updatecontract", methods=['POST'])
def updateContract():
    """ Contract update """
    try: 
        if "username" in session:
            myContract=Contract.query.filter(Contract.contractref==session["contractref"]).first()
            myContract.contractref=request.form["inputContractReference"]
            myContract.systemname=request.form["inputSystemName"]
            myContract.contractrenewtype=request.form["inputRenewType"]
            myContract.contractcost=request.form["inputContractCost"]
            myContract.contractstartingdate=request.form["inputContractStartingDate"]
            myContract.contractendingdate=request.form["inputContractEndingDate"]
            myContract.contractcomment=request.form["inputContractComment"]
            myContract.contractyear=request.form["inputContractYear"]
            myContract.contractdhlowner=request.form["inputDHLOwner"]
            myContract.contractinvoice=request.form["inputInvoice"]
            myContract.contractvendor=request.form["inputContractVendor"]
            myContract.save()
            flash('Contract updated !!! ', 'message')
            return redirect(url_for('listeContract'))
        else:
            flash('Unknown user !!! ','error')
            return render_template('login.html')
    except:
        return redirect(url_for('appError'))


@app.route("/displaycontract/<contractref>", methods=['GET'])
def displayContract(contractref):
    """ Display one contract record """
    try: 
        if "username" in session:
            if request.method == 'GET':
                session["contractref"]=contractref
                myContract=Contract.query.filter(Contract.contractref==contractref).first()
                return render_template('updatecontract.html',myContract=myContract)
        else:
            flash('Unknown user !!! ','error')
            return render_template('login.html')
    except:
        return redirect(url_for('appError'))


#delete the contract
@app.route("/deletecontract/<contractref>", methods=['GET'])
def deleteContract(contractref):
    """ Contract deletion """
    try: 
        if "username" in session:
            if request.method == 'GET':
                myContract=Contract.query.filter(Contract.contractref==contractref).first()
                myContract.remove()
                flash('Contract deleted !!! ', 'message')
                return redirect(url_for('listeContract'))
        else:
            flash('Unknown user !!! ','error')
            return render_template('login.html')
    except:
        return redirect(url_for('appError'))
