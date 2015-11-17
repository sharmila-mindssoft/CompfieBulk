from types import *
import datetime
import time

__all__ = [
    "CMObject", 
    "Form", 
    "Menu",
    "assertType",
    "listToString",
    "getCurrentTimeStamp",
    "getMenu",
    "JsonParser",
    "convertToString"
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

def getMenu(formList) :
    masters = []
    transactions = []
    reports = []
    settings = []
    for form in formList:
        structured_form = form.toStructure()
        if form.category == "Masters":
            masters.append(structured_form)
        elif form.category == "Transactions":
            transactions.append(structured_form)
        elif form.category == "Reports":
            reports.append(structured_form)    
        elif form.category == "Settings":
            settings.append(structured_form)

    return Menu(masters, transactions,reports, settings).toStructure()

class JsonParser():
	def __init__(self, jsonData):
		self.jsonData = jsonData

	def getString(self, key):
		return convertToString(self.jsonData.get(key))

	def getInt(self, key):
		int_value = self.jsonData.get(key)
		return int(int_value)

	def getData(self, key):
		return self.jsonData.get(key)

class CMObject(object) :
    def toJSON(self) :
        data = self.toStructure()
        return json.dumps(data)
    @classmethod
    def fromJSON(klass, jsonData) :
        data = json.loads(jsonData)
        return klass.fromStructure(data)

class Form(CMObject) :
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

class Menu(CMObject):
    def __init__(self, masterForms, transactionForms, report_forms, setting_forms):
        self.masterForms = masterForms
        self.transactionForms = transactionForms
        self.report_forms = report_forms
        self.setting_forms = setting_forms

    def toStructure(self):
        return {
            "masters": self.masterForms,
            "transactions": self.transactionForms,
            "reports": self.report_forms,
            "settings": self.setting_forms
        }