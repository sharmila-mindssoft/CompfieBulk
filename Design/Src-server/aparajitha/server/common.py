from types import *
import datetime
import time
import string
import random
import os
import hashlib

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
    "commonResponseStructure"
]

clientDatabaseMappingFilePath = os.path.join(ROOT_PATH, 
    "Src-client/files/desktop/common/clientdatabase/clientdatabasemapping.txt")

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

def getCurrentTimeStamp() :
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def commonResponseStructure(responseType, data) :
	assertType(responseType, StringType)
	assertType(data, dict)
	response = [
		responseType,
		data
	]
	return response

def getClientDatabase(clientId):
    clientDatabaseMappingJson = json.load(open(clientDatabaseMappingFilePath))
    return clientDatabaseMappingJson[clientId] 

def generatePassword() : 
    characters = string.ascii_uppercase + string.digits
    password = ''.join(random.SystemRandom().choice(characters) for _ in range(7))
    m = hashlib.md5()
    m.update(password)
    return m.hexdigest()

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
        	condition = " form_type = 'knowledge' "
        elif type == "techno".lower():
        	condition = " form_type = 'techno' "
        else :
        	condition = " form_type = 'client' "

        rows = DatabaseHandler.instance().getData(Form.tblName, columns, condition)

        for row in rows:
            formObj = Form(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            forms.append(formObj)

        return forms
            
class Menu(object):
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
	        structuredForm = form.toStructure()
	        if form.category == "masters".lower():
	            masters.append(structuredForm)
	        elif form.category == "transactions".lower():
	            transactions.append(structuredForm)
	        elif form.category == "reports".lower():
	            reports.append(structuredform)    
	        elif form.category == "settings".lower():
	            settings.append(structuredForm)
	    menu = Menu(masters, transactions,reports, settings)
	    return menu.toStructure()