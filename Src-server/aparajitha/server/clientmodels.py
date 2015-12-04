from aparajitha.misc.dates import *

__all__ = [
    "Form",
    "Menu",
    "ServiceProvider",
    "UserPrivilege"
]

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
            "form_order": self.formOrder,
            "parent_menu": self.parentMenu
        }

    @classmethod
    def getForms(self, type, db):
        forms = []
        rows = db.getSectionWiseForms(type)
        for row in rows:
            formObj = Form(int(row[0]), row[1], row[2], int(row[3]), 
                row[4], row[5], row[6], row[7])
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

class ServiceProvider(object):
    def __init__(self, clientId, serviceProviderId, serviceProviderName, address, 
                contractFrom, contractTo, contactPerson, contactNo, isActive) :
        self.clientId = clientId
        self.serviceProviderId =  serviceProviderId
        self.serviceProviderName =  serviceProviderName
        self.address =  address
        self.contractFrom =  contractFrom
        self.contractTo =  contractTo
        self.contactPerson =  contactPerson
        self.contactNo =  contactNo
        self.isActive = isActive if isActive != None else 1

    @classmethod
    def initializeWithRequest(self, request, serviceProviderId, clientId):
    	serviceProviderName = str(request["service_provider_name"])
    	address = str(request["address"])
    	contractFrom =  str(request["contract_from"])
    	contractTo =  str(request["contract_to"])
    	contactPerson =  str(request["contact_person"])
    	contactNo =  str(request["contact_no"])
    	contractFrom = datetimeToTimestamp(stringToDatetime(contractFrom))
    	contractTo = datetimeToTimestamp(stringToDatetime(contractTo))
    	return ServiceProvider(clientId, serviceProviderId, serviceProviderName, address, 
                contractFrom, contractTo, contactPerson, contactNo, None)

    def toStructure(self):
        return {
	        "service_provider_id": self.serviceProviderId,
	        "service_provider_name": self.serviceProviderName, 
	        "address": self.address,
	        "contract_from": self.contractFrom,
	        "contract_to": self.contractTo, 
	        "contact_person": self.contactPerson,
	        "contact_no": self.contactNo,
	        "is_active": self.isActive
    	}

    @classmethod
    def getList(self, db):
        servcieProviderList = []
        rows = db.getServiceProviders()
        for row in rows:
            serviceProviderId = int(row[0])
            serviceProviderName = row[1]
            address = row[2]
            contractFrom = datetimeToString(timestampToDatetime(row[3]))
            contractTo = datetimeToString(timestampToDatetime(row[4]))
            contactPerson = row[5]
            contactNo = row[6]
            isActive = row[7]
            serviceProvider = ServiceProvider(None, serviceProviderId, serviceProviderName, address, 
                contractFrom, contractTo, contactPerson, contactNo, isActive)
            servcieProviderList.append(serviceProvider.toStructure())
        return servcieProviderList

class UserPrivilege() :

    def __init__(self, clientId, userGroupId, userGroupName, formType, formIds, isActive) :
        self.clientId = clientId
        self.userGroupId =  userGroupId 
        self.userGroupName = userGroupName
        self.formType = formType 
        self.formIds = formIds 
        self.isActive = isActive if isActive != None else 1

    @classmethod
    def initializeWithRequest(self, request, userGroupId, clientId):
        userGroupName = str(request["user_group_name"])
        formType = str(request["form_type"])
        formIds =  request["form_ids"]
        userPrivilege = UserPrivilege(clientId, userGroupId, userGroupName, 
            formType, formIds, None)
        return userPrivilege

    def toDetailedStructure(self) :
        return {
            "user_group_id": self.userGroupId,
            "user_group_name": self.userGroupName,
            "form_type": self.formType,
            "form_ids": self.formIds,
            "is_active": self.isActive
        }

    def toStructure(self):
        return {
            "user_group_id": self.userGroupId,
            "user_group_name": self.userGroupName
        }

    @classmethod
    def getDetailedList(self, sessionUser, db) :
        userGroupList = []
        rows = db.getUserGroupDetails()
        for row in rows:
            userGroup = UserPrivilege(None, int(row[0]), row[1], row[2], 
                [int(x) for x in row[3].split(",")], row[4])
            userGroupList.append(userGroup.toDetailedStructure())
        return userGroupList

    @classmethod
    def getList(self, clientId, db):
        userGroupList = []
        rows = db.getUserGroups()
        for row in rows:
            userGroup = UserPrivilege(clientId, int(row[0]), row[1], None, None, None)
            userGroupList.append(userGroup.toStructure())
        return userGroupList