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
        try:
            rows = db.getBusinessGroups()
            for row in rows:
                businessGroupId = row[0]
                businessGroupName = row[1]
                businessGroup = BusinessGroup(businessGroupId, businessGroupName, clientId)
                businessGroupList.append(businessGroup.toStructure())
            except:
                print "Error: While fetching Business Groups of client id %s" % clientId
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
    def getList(self, clientId):
        legalEntitiesList = []
        try:
            rows = db.getLegalEntities()
            for row in rows:
                legalEntityId = row[0]
                legalEntityName = row[1]
                businessGroupId = row[2]
                legalEntity = LegalEntity(legalEntityId, legalEntityName, businessGroupId, clientId)
                legalEntitiesList.append(legalEntity.toStructure())
        except:
            print "Error: While fetching Legal Entities of client id %s" % clientId
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
        try:
            rows = db.getDivisions()     
            for row in rows:
                divisionId = row[0]
                divisionName = row[1]
                legalEntityId = row[2]
                businessGroupId = row[2]
                division = Division(divisionId, divisionName, legalEntityId, 
                        businessGroupId, clientId)
                    divisionsList.append(division.toStructure())
            except:
                print "Error: While fetching Division of client id %s" % clientId
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
        self.unitId = unitId if unitId != None else self.generateNewUnitId()
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
        try:
            rows = db.getUnits()
            for row in rows:1
                unitId = row[0]
                divisionId = row[1]
                legalEntityId = row[2]
                businessGroupId = row[3]
                unitCode = row[4]
                unitName = row[5]
                countryId = row[6]
                address = row[7]
                domainIds = row[8]
                unit = Unit(unitId, divisionId, legalEntityId, businessGroupId, 
                            clientId, countryId, None, unitCode, unitName,
                            None, address, None, domainIds, None, None, None)
                unitList.append(unit.toStructure())
        except:
            print "Error: While fetching Unit of client id %s" % clientId

        return unitList