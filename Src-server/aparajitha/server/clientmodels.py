from aparajitha.misc.dates import *

__all__ = [
    "Form",
    "Menu",
    "ServiceProvider",
    "UserPrivilege",
    "User",
    "BusinessGroup",
    "LegalEntity",
    "Division",
    "Unit"
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
            "user_group_name": self.userGroupName,
            "is_active": self.isActive
        }

    @classmethod
    def getDetailedList(self, clientId, db) :
        userGroupList = []
        rows = db.getUserGroupDetails()
        for row in rows:
            userGroup = UserPrivilege(clientId, int(row[0]), row[1], row[2], 
                [int(x) for x in row[3].split(",")], row[4])
            userGroupList.append(userGroup.toDetailedStructure())
        return userGroupList

    @classmethod
    def getList(self, clientId, db):
        userGroupList = []
        rows = db.getUserGroups()
        for row in rows:
            userGroup = UserPrivilege(clientId, int(row[0]), row[1], None, None, int(row[2]))
            userGroupList.append(userGroup.toStructure())
        return userGroupList

class User(object):
    def __init__(self, clientId ,userId, emailId, userGroupId, employeeName, employeeCode, 
        contactNo, seatingUnitId, userLevel, countryIds, domainIds, unitIds, 
        isAdmin, isServiceProvider, serviceProviderId, isActive ) :
        self.clientId = clientId if clientId != None else 0
        self.userId =  userId if userId != None else self.generateNewUserId()
        self.emailId =  emailId
        self.userGroupId =  userGroupId
        self.employeeName =  employeeName
        self.employeeCode =  employeeCode
        self.contactNo =  contactNo
        self.seatingUnitId =  seatingUnitId
        self.userLevel =  userLevel
        self.countryIds =  countryIds
        self.domainIds =  domainIds
        self.unitIds =  unitIds
        self.isAdmin =  isActive if isActive != None else 0
        self.isActive =  isActive if isActive != None else 1
        self.isServiceProvider =  isServiceProvider
        self.serviceProviderId =  serviceProviderId

    @classmethod
    def initializeWithRequest(self, request, userId, clientId):
        emailId = ""
        try:
            emailId = str(request["email_id"])
        except:
            print "Updating User"
        userGroupId = int(request["user_group_id"])
        employeeName = str(request["employee_name"])
        employeeCode = str(request["employee_code"])
        contactNo = str(request["contact_no"])
        seatingUnitId =  int(request["seating_unit_id"])
        userLevel =  int(request["user_level"])
        countryIds = request["country_ids"]
        domainIds = request["domain_ids"]
        unitIds = request["unit_ids"]
        isServiceProvider = int(request["is_service_provider"])
        serviceProviderId = request["service_provider_id"]
        user = User(clientId ,userId, emailId, userGroupId, employeeName, 
            employeeCode, contactNo, seatingUnitId, userLevel, countryIds, 
            domainIds, unitIds, None, isServiceProvider, 
            serviceProviderId, None)
        return user

    def toDetailedStructure(self) :
        employeeName = "%s - %s" % (self.employeeCode,self.employeeName)
        return {
            "user_id": self.userId,
            "email_id": self.emailId,
            "user_group_id": self.userGroupId,
            "employee_name": employeeName,
            "contact_no": self.contactNo,
            "seating_unit_id": self.seatingUnitId, 
            "user_level": self.userLevel,
            "country_ids": self.countryIds,
            "domain_ids": self.domainIds,
            "unit_ids": self.unitIds,
            "is_admin": self.isAdmin,
            "is_active": self.isActive,
            "is_service_provider": self.isServiceProvider,
            "service_provider_id": self.serviceProviderId
        }

    def toStructure(self):
        employeeName = None
        if self.employeeCode == None:
            employeeName = self.employeeName
        else:
            employeeName = "%s-%s" % (self.employeeCode, self.employeeName)
        return {
            "user_id": self.userId,
            "employee_name": employeeName,
            "user_level": self.userLevel
        }

    @classmethod
    def getDetailedList(self, clientId, db):
        userList = []
        rows = db.getClientUserDetailsList()
        for row in rows:
            userId = int(row[0])
            emailId = row[1]
            userGroupId = int(row[2]) if row[2] != None else None
            employeeName = row[3]
            employeeCode = row[4]
            contactNo =  row[5]
            seatingUnitId = int(row[6]) if row[6] != None else None
            userLevel = int(row[7]) if row[7] != None else None
            countryIds = [int(x) for x in row[8].split(",")]
            domainIds = [int(x) for x in row[9].split(",")]
            unitIds = [int(x) for x in row[10].split(",")] if row[10] != None else None
            isAdmin = int(row[11])
            isServiceProvider = int(row[12])
            isActive = int(row[13])
            user = User(clientId,userId, emailId, userGroupId, employeeName, employeeCode,
                         contactNo, seatingUnitId, userLevel, countryIds, domainIds, unitIds, 
                         isAdmin, isServiceProvider,None, isActive) 
            userList.append(user.toDetailedStructure())
        return userList

    @classmethod
    def getList(self, clientId, db):
        userList = []
        rows = db.getClientUserList()
        for row in rows:
            userId = int(row[0])
            employeeName = row[1]
            employeeCode = row[2]
            isActive = int(row[3])
            user = User(clientId, userId, None, employeeName, employeeCode,
                 None, None, None, None, None, None, None, isActive)
            userList.append(user.toStructure())
        return userList


class BusinessGroup(object):
    def __init__(self, businessGroupId, businessGroupName, clientId):
        self.clientId = clientId
        self.businessGroupId = businessGroupId if businessGroupId != None else self.generateNewBusinessGroupId()
        self.businessGroupName = businessGroupName

    def toStructure(self) :
        return {
            "business_group_id": self.businessGroupId,
            "business_group_name": self.businessGroupName,
            "client_id": self.clientId
        }

    @classmethod
    def getList(self, clientId, db):
        businessGroupList = []
        rows = db.getBusinessGroups()
        for row in rows:
            businessGroupId = int(row[0])
            businessGroupName = row[1]
            businessGroup = BusinessGroup(businessGroupId, businessGroupName, clientId)
            businessGroupList.append(businessGroup.toStructure())

        return businessGroupList

class LegalEntity(object):

    def __init__(self, legalEntityId, legalEntityName, businessGroupId, clientId):
        self.clientId = clientId
        self.legalEntityId = legalEntityId if legalEntityId != None else self.generateNewLegalEntityId()
        self.legalEntityName = legalEntityName
        self.businessGroupId = businessGroupId

    def toStructure(self) :
        return {
            "legal_entity_id": self.legalEntityId,
            "legal_entity_name": self.legalEntityName,
            "business_group_id": self.businessGroupId,
            "client_id": self.clientId
        }

    @classmethod
    def getList(self, clientId, db):
        legalEntitiesList = []
        rows = db.getLegalEntities()
        for row in rows:
            legalEntityId = int(row[0])
            legalEntityName = row[1]
            businessGroupId = int(row[2])
            legalEntity = LegalEntity(legalEntityId, legalEntityName, businessGroupId, clientId)
            legalEntitiesList.append(legalEntity.toStructure())
        return legalEntitiesList

class Division(object):
    divisionTblName = "tbl_divisions"

    def __init__(self, divisionId, divisionName,legalEntityId, businessGroupId, clientId):
        self.clientId = clientId
        self.divisionId = divisionId if divisionId != None else self.generateNewDivisionId()
        self.divisionName = divisionName
        self.legalEntityId = legalEntityId
        self.businessGroupId = businessGroupId

    def toStructure(self) :
        return {
            "division_id": self.divisionId,
            "division_name": self.divisionName,
            "legal_entity_id": self.legalEntityId,
            "business_group_id": self.businessGroupId,
            "client_id": self.clientId
        }

    @classmethod
    def getList(self, clientId, db):
        divisionsList = []
        rows = db.getDivisions()     
        for row in rows:
            divisionId = int(row[0])
            divisionName = row[1]
            legalEntityId = int(row[2])
            businessGroupId = int(row[2])
            division = Division(divisionId, divisionName, legalEntityId, 
                        businessGroupId, clientId)
            divisionsList.append(division.toStructure())

        return divisionsList

class Unit(object):
    unitTblName = "tbl_units"
    divisionTblName = "tbl_divisions"
    legalEntityTblName = "tbl_legal_entities"
    businessGroupTblName = "tbl_business_groups"

    def __init__(self, unitId, divisionId, legalEntityId, businessGroupId, clientId, 
                countryId, geographyId, unitCode, unitName, industryId, address, 
                postalCode, domainIds, isActive, industryName, geography):
        self.clientId = clientId
        self.unitId = int(unitId) if unitId != None else self.generateNewUnitId()
        self.divisionId = divisionId
        self.legalEntityId = legalEntityId
        self.businessGroupId = businessGroupId
        self.countryId = countryId
        self.geographyId = geographyId
        self.unitCode = unitCode
        self.unitName = unitName
        self.industryId = industryId
        self.address = address
        self.postalCode = postalCode
        self.domainIds = domainIds
        self.isActive = isActive if isActive != None else 1
        self.industryName = industryName
        self.geography = geography

    def toDetailedStructure(self) :
        return {
            "unit_id": self.unitId,
            "division_id": self.divisionId,
            "legal_entity_id": self.legalEntityId,
            "business_group_id": self.businessGroupId,
            "client_id"  : self.clientId,
            "country_id": self.countryId,
            "geography_id": self.geographyId,
            "unit_code": self.unitCode,
            "unit_name": self.unitName,
            "industry_id": self.industryId,
            "unit_address": self.address,
            "postal_code": self.postalCode,
            "domain_ids": self.domainIds,
            "is_active": self.isActive
        }

    def toStructure(self):
        unitName = "%s - %s" % (self.unitCode, self.unitName)
        return{
            "unit_id": self.unitId,
            "division_id": self.divisionId,
            "legal_entity_id": self.legalEntityId,
            "business_group_id": self.businessGroupId,
            "client_id": self.clientId,
            "country_id": self.countryId,
            "domain_ids": self.domainIds,
            "unit_name": unitName,
            "unit_address": self.address
        }

    @classmethod
    def getList(self, clientId , db):
        unitList = []
        rows = db.getUnits()
        for row in rows:
            unitId = row[0]
            divisionId = int(row[1])
            legalEntityId = int(row[2])
            businessGroupId = int(row[3])
            unitCode = row[4]
            unitName = row[5]
            countryId = int(row[6])
            address = row[7]
            domainIds = [int(x) for x in row[8].split(",")]
            unit = Unit(unitId, divisionId, legalEntityId, businessGroupId, 
                        clientId, countryId, None, unitCode, unitName,
                        None, address, None, domainIds, None, None, None)
            unitList.append(unit.toStructure())
        return unitList