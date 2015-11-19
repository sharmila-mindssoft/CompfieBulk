from types import *
import datetime
import time
import string
import random
from databasehandler import DatabaseHandler 

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

def assertType (x, typeObject) :
    if type(x) is not typeObject :
        msg = "expected type %s, received invalid type  %s " % (typeObject, type(x))
        raise TypeError(msg)

def convertToString(unicode_str):
	return unicode_str.encode('utf-8')

def listToString(list_value):
    string_value = ""
    for index,value in enumerate(list_value):
        if(index < len(list_value)-1):
            string_value = string_value+"'"+str(value)+"',"
        else:
            string_value = string_value+"'"+str(value)+"'"

    return string_value

def getCurrentTimeStamp() :
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def generatePassword() : 
	characters = string.ascii_uppercase + string.digits
	password = ''.join(random.SystemRandom().choice(characters) for _ in range(7))
	return password

def commonResponseStructure(responseType, data) :
	assertType(responseType, StringType)
	assertType(data, dict)
	response = [
		responseType,
		data
	]
	return response

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

        if type == "Knowledge":
        	condition = " form_type = 'knowledge' "
        elif type == "Techno":
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
	        if form.category == "Masters":
	            masters.append(structuredForm)
	        elif form.category == "Transactions":
	            transactions.append(structuredForm)
	        elif form.category == "Reports":
	            reports.append(structuredform)    
	        elif form.category == "Settings":
	            settings.append(structuredForm)
	    menu = Menu(masters, transactions,reports, settings)
	    return menu.toStructure()