from types import *
import datetime
import calendar
import time
import string
import random
import os
import hashlib
import json

from databasehandler import DatabaseHandler 
from aparajitha.server.constants import ROOT_PATH

__all__ = [
    "Form", 
    "Menu",
    "assertType",
    "listToString",
    "getCurrentTimeStamp",
    "JSONHelper",
    "convertToString",
    "generatePassword",
    "encrypt",
    "commonResponseStructure",
    "getClientDatabase",
    "datetimeToTimestamp",
    "timestampToDatetime",
    "stringToDatetime",
    "datetimeToString",
    "getClientId"
]

clientDatabaseMappingFilePath = os.path.join(ROOT_PATH, 
    "Src-client/files/desktop/common/clientdatabase/clientdatabasemapping.txt")

IntegerMonths = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}

StringMonths = {
     1 : "Jan",
     2 : "Feb",
     3 : "Mar",
     4 : "Apr",
     5 : "May",
     6 : "Jun",
     7 : "Jul",
     8 : "Aug",
     9 : "Sep",
     10 : "Oct",
     11 : "Nov",
     12 : "Dec",
}

def assertType (x, typeObject) :
    if type(x) is not typeObject :
        msg = "expected type %s, received invalid type  %s " % (typeObject, type(x))
        raise TypeError(msg)

def convertToString(unicode_str):
	return unicode_str.encode('utf-8')

def listToString(valueList):
    stringValue = ""
    for index,value in enumerate(valueList):
        if(index < len(valueList)-1):
            stringValue = stringValue+"'"+str(value)+"',"
        else:
            stringValue = stringValue+"'"+str(value)+"'"

    return stringValue

def commonResponseStructure(responseType, data) :
	assertType(responseType, StringType)
	assertType(data, dict)
	response = [
		responseType,
		data
	]
	return response

def getClientId(sessionUser):
    userTblName = "tbl_users"
    columns = "client_id"
    condition = "user_id='%d'" % sessionUser
    rows = DatabaseHandler.instance().getData(userTblName, columns, condition)
    return rows[0][0]

def getClientDatabase(clientId):
    databaseName = None
    clientDatabaseMappingJson = json.load(open(clientDatabaseMappingFilePath))
    try:
        databaseName = JSONHelper.getString(clientDatabaseMappingJson,  unicode(str(clientId), "utf-8"))
    except:
        print "Error: Database Not exists for the client %d" % clientId
    return databaseName

def generatePassword() : 
    characters = string.ascii_uppercase + string.digits
    password = ''.join(random.SystemRandom().choice(characters) for _ in range(7))
    print password
    print encrypt(password)
    return encrypt(password)

def encrypt(value):
    m = hashlib.md5()
    m.update(value)
    return m.hexdigest()

def stringToDatetime(string):
    date = string.split("-")
    datetimeVal = datetime.datetime(year=int(date[2]), 
        month=IntegerMonths[date[1]], day=int(date[0]))
    return datetimeVal

def datetimeToString(datetimeVal):
    return "%d-%s-%d" % (datetimeVal.day, StringMonths[datetimeVal.month], datetimeVal.year)

def datetimeToTimestamp(d) :
    return calendar.timegm(d.timetuple())

def timestampToDatetime(t) :
    return datetime.datetime.utcfromtimestamp(t)

def getCurrentTimeStamp() :
    return datetimeToTimestamp(datetime.datetime.utcnow())

class PossibleError(object) :
    def __init__(self, possibleError) :
        self.possibleError = possibleError
        self.verify()

    def verify(self) :
        assertType(self.possibleError, StringType)

    def toStructure(self) :
        return {
            str(self.possibleError),
            {}
        }

    def __repr__(self) :
        return str(self.toStructure())

class JSONHelper(object) :
    
    @staticmethod
    def string(x) :
        assertType(x, UnicodeType)
        return str(x)

    @staticmethod
    def getString(data, name) :
        return JSONHelper.string(data.get(name))

    @staticmethod
    def int(x):
        assertType(x, IntType)
        return x

    @staticmethod
    def getInt(data, name) :
        return JSONHelper.int(data.get(name))

    @staticmethod
    def float(x) :
        assertType(x, FloatType)
        return x

    @staticmethod
    def getFloat(data, name) :
        return JSONHelper.float(data.get(name))

    @staticmethod
    def list(x) :
        assertType(x, ListType)
        return x

    @staticmethod
    def getList(data, name) :
        return JSONHelper.list(data.get(name))

    @staticmethod
    def dict(x) :
        assertType(x, DictType)
        return x

    @staticmethod
    def getDict(data, name) :
        return JSONHelper.dict(data.get(name))

    @staticmethod
    def long(x):
        assertType(x, LongType)
        return x

    @staticmethod
    def getLong(data, name) :
        return JSONHelper.long(data.get(name))

   

class Form(object) :
    tblName = "tbl_forms"

    def __init__(self, formId, formName, formUrl, formOrder, formType, 
        Category, isAdminForm, parentMenu) :
        self.formId = formId
        self.formName = formName
        self.formUrl = formUrl
        self.formOrder = formOrder
        self.formType = formType
        self.category = Category
        self.isAdminForm = isAdminForm
        self.parentMenu = parentMenu

    def toStructure(self) :
        return {
            "form_id": self.formId,
            "form_name": self.formName,
            "form_url": self.formUrl,
            "form_type": self.formType,
            "parent_menu": self.parentMenu
        }

    @classmethod
    def getForms(self, type):
    	print "inside get forms"
    	forms = []

        columns = "form_id, form_name, form_url, form_order, form_type,"+\
                 "category, admin_form, parent_menu"

        if type == "knowledge".lower():
        	condition = " category = 'knowledge' "
        elif type == "techno".lower():
        	condition = " category = 'techno' "
        else :
        	condition = " category = 'client' "

        rows = DatabaseHandler.instance().getData(Form.tblName, columns, condition)

        for row in rows:
            formObj = Form(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            forms.append(formObj)

        return forms
            
class Menu(object):
    structuredForm = {}
    def __init__(self, masterForms, transactionForms, reportForms, settingForms):
        self.masterForms = masterForms
        self.transactionForms = transactionForms
        self.reportForms = reportForms
        self.settingForms = settingForms

    def toStructure(self):
        return {
            "masters": self.masterForms,
            "transactions": self.transactionForms,
            "reports": self.reportForms,
            "settings": self.settingForms
        }

    @classmethod
    def getMenu(self, formList) :
	    masters = []
	    transactions = []
	    reports = []
	    settings = []
	    for form in formList:
	        self.structuredForm = form.toStructure()
	        if form.formType == "master".lower():
	            masters.append(self.structuredForm)
	        elif form.formType == "transaction".lower():
	            transactions.append(self.structuredForm)
	        elif form.formType == "report".lower():
	            reports.append(self.structuredForm)    
	        elif form.formType == "setting".lower():
	            settings.append(self.structuredForm)
	    menu = Menu(masters, transactions,reports, settings)
	    return menu.toStructure()