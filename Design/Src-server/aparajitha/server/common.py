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
    "getClientId",
    "FormCategory"
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
        return [
            str(self.possibleError),
            {}
        ]

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

   
class FormCategory(object):
    def __init__(self, form_category_id = None, form_category = None):
        self.db = DatabaseHandler.instance()
        self.form_category_id = form_category_id
        self.form_category = form_category

    def toStructure(self):
        return {
            "form_category_id" : self.form_category_id,
            "form_category" : self.form_category
        }

    def getFormCategories(self): 
        formCategoryList = []
        columns = "form_category_id, form_category"
        condition = " form_category_id in (2,3)"
        rows = self.db.getData(columns, self.db.tblFormCategory, condition)
        for row in rows:
            formCategory = FormCategory(row[0], row[1])
            formCategoryList.append(formCategory.toStructure())
        return formCategoryList

class Form(object) :

    def __init__(self, formId = None, formName = None, formUrl = None, formOrder = None, formType = None, 
        Category = None, parentMenu = None) :
        self.db = DatabaseHandler.instance()
        self.formId = formId
        self.formName = formName
        self.formUrl = formUrl
        self.formOrder = formOrder
        self.formType = formType
        self.category = Category
        self.parentMenu = parentMenu

    def toStructure(self) :
        return {
            "form_id": self.formId,
            "form_name": self.formName,
            "form_url": self.formUrl,
            "parent_menu": self.parentMenu
        }

    def getForms(self):
        forms = []

        columns = "tf.form_id, tf.form_category_id, tfc.form_category, tf.form_type_id, tft.form_type,"+\
        "tf.form_name, tf.form_url, tf.form_order, tf.parent_menu"
        tables = [self.db.tblForms, self.db.tblFormCategory, self.db.tblFormType]
        aliases = ["tf", "tfc", "tft"]
        joinConditions = ["tf.form_catEgory_id = tfc.form_category_id", "tf.form_type_id = tft.form_type_id"]
        whereCondition = " tf.form_category_id in (3,2,4) order by tf.form_order"
        joinType = "left join"

        rows = self.db.getDataFromMultipleTables(columns, tables, aliases, joinType, 
            joinConditions, whereCondition)
        return rows

    def getUserForms(self, formIds):
        formList = []
        rows = self.db.getUserForms(formIds)
        for row in rows:
            form = Form(formId = row[0], formName = row[5], formUrl = row[6], formOrder = row[7], 
                    formType = row[4], Category = row[2], parentMenu = row[8])
            formList.append(form)
        menu = Menu()
        result = menu.generateMenu(formList)
        return result


            
class Menu(object):
    masterForms = []
    transactionForms = []
    reportForms = []
    settingForms = []

    def __init__(self):
        print "constructor"

    def toStructure(self):
        return {
            "masters": self.masterForms,
            "transactions": self.transactionForms,
            "reports": self.reportForms,
            "settings": self.settingForms
        }

    def clearLists(self):
        self.masterForms = []
        self.transactionForms = []
        self.reportForms = []
        self.settingForms = []

    def generateMenu(self, formList) :
        self.clearLists()
        for form in formList:
            structuredForm = form.toStructure()
            if form.formType == "Master":
                self.masterForms.append(structuredForm)
            elif form.formType == "Transaction":
                self.transactionForms.append(structuredForm)
            elif form.formType == "Report":
                self.reportForms.append(structuredForm)    
            elif form.formType == "Settings":
                self.settingForms.append(structuredForm)
        return self.toStructure()