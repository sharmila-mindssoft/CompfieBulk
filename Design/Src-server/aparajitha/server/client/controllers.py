import json

import tornado.ioloop
import tornado.web
import uuid

from aparajitha.server.common import *
from aparajitha.server.techno.controllers import GroupCompany, BusinessGroup,LegalEntity,Division,Unit
from aparajitha.server.knowledge.models import DomainList, CountryList
from aparajitha.server.databasehandler import DatabaseHandler
from aparajitha.server.clientdatabasehandler import ClientDatabaseHandler

__all__ = [
    "UserPrivilege",
    "User",
    "ServiceProvider",
    "UnitClosure"
]

class UserPrivilege() :
    db = None
    clientId = None
    userGroupId = None
    userGroupName = None
    formType = None
    formIds = None
    isActive = 1

    def __init__(self) :
        self.db = ClientDatabaseHandler.instance()
        print "inside init:db:{}".format(self.db)

    def getUserGroupsFormData(self) :
        form = Form()
        resultRows = form.getForms()
        clientForms = []
        for row in resultRows:
            form = Form(formId = row[0], formName = row[5], formUrl = row[6], formOrder = row[7], 
                    formType = row[4], Category = row[2], parentMenu = row[8])
            clientForms.append(form)
        menu = Menu()
        menuStructure = menu.generateMenu(clientForms)
        return menuStructure

    def getUserPrivileges(self, sessionUser) :
    	forms = self.getUserGroupsFormData()
    	userGroupList = self.getDetailedList(sessionUser)

        response_data = {}
        response_data["forms"] = forms
        response_data["user_groups"] = userGroupList

        response = commonResponseStructure("GetUserGroupsSuccess", response_data)
        return response

    def toDetailedStructure(self) :
        return {
            "user_group_id": self.userGroupId,
            "user_group_name": self.userGroupName,
            "form_ids": self.formIds,
            "is_active": self.isActive
        }

    def toStructure(self):
        return {
            "user_group_id": self.userGroupId,
            "user_group_name": self.userGroupName,
            "is_active": self.isActive
        }

    def getDetailedList(self, sessionUser) :
        userGroupList = []
        rows = self.db.getUserPrivilegeDetailsList()
        for row in rows:
            self.userGroupId = int(row[0])
            self.userGroupName = row[1]
            self.formIds = [int(x) for x in row[2].split(",")]
            self.isActive = row[3]
            userGroupList.append(self.toDetailedStructure())
        return userGroupList

    def getList(self, clientId):
        userGroupList = []
        rows = self.db.getUserPrivileges()
        for row in rows:
            self.userGroupId = int(row[0])
            self.userGroupName = row[1]
            self.isActive = row[2]
            userGroupList.append(self.toStructure())
        return userGroupList 

    def generateNewUserGroupId(self) :
        return self.db.generateNewId(self.db.tblUserGroups, "user_group_id")

    def isDuplicate(self):
        condition = "user_group_name ='%s' AND user_group_id = '%d'" % (
            self.userGroupName, self.userGroupId)
        return self.db.isAlreadyExists(self.db.tblUserGroups, condition)

    def isIdInvalid(self):
        condition = "user_group_id = '%d'" % self.userGroupId
        return not self.db.isAlreadyExists(self.db.tblUserGroups, condition)

    def saveUserPrivilege(self, requestData, sessionUser) :
        self.userGroupId = self.generateNewUserGroupId()
        self.userGroupName = JSONHelper.getString(requestData, "user_group_name")
        self.formIds =  JSONHelper.getList(requestData, "form_ids")
        if self.isDuplicate() :
            return commonResponseStructure("GroupNameAlreadyExists",{})
        elif self.db.saveUserPrivilege(self, sessionUser) :
            return commonResponseStructure("SaveUserGroupSuccess",{})
        else:
            return commonResponseStructure("Error",{})

    def updateUserPrivilege(self, requestData, sessionUser) :
        self.userGroupId = JSONHelper.getInt(requestData,"user_group_id")
        self.userGroupName = JSONHelper.getString(requestData,"user_group_name")
        self.formIds =  JSONHelper.getList(requestData,"form_ids")
        if self.isIdInvalid() :
            return commonResponseStructure("InvalidGroupId",{})
        elif self.isDuplicate() :
            return commonResponseStructure("GroupNameAlreadyExists",{})
        elif self.db.updateUserPrivilege(self, sessionUser) :
            return commonResponseStructure("UpdateUserGroupSuccess",{})
        else:
            return commonResponseStructure("Error",{})

    def changeUserPrivilegeStatus(self, requestData, sessionUser) :
        self.userGroupId = JSONHelper.getInt(requestData, "user_group_id")
        self.isActive = JSONHelper.getInt(requestData, "is_active")
        if self.isIdInvalid() :
            return commonResponseStructure("InvalidGroupId",{})
        elif self.db.updateUserPrivilegeStatus(self.userGroupId, self.isActive, sessionUser):
            return commonResponseStructure("ChangeUserGroupStatusSuccess",{})

class User():
    db = None
    clientId = None
    userId =  None
    emailId =  None
    userGroupId =  None
    employeeName =  None
    employeeCode =  None
    contactNo =  None
    seatingUnitId =  None
    userLevel =  None
    countryIds =  None
    domainIds =  None
    unitIds =  None
    isAdmin =  None
    isServiceProvider =  None
    serviceProviderId =  None

    def __init__(self) :
        self.db = ClientDatabaseHandler.instance()
        
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

    def generateNewUserId(self) :
        return self.db.generateNewId(self.db.tblUsers, "user_id")

    def isDuplicateEmail(self):
        condition = "email_id ='%s' AND user_id != '%d'" % (self.emailId, self.userId)
        return self.db.isAlreadyExists(self.db.tblUsers, condition)

    def isDuplicateEmployeeCode(self):
        condition = "employee_code ='%s' AND user_id != '%d'" % (self.employeeCode, self.userId)
        return self.db.isAlreadyExists(self.db.tblUsers, condition)

    def isDuplicateContactNo(self):
        condition = "contact_no ='%s' AND user_id != '%d'" % (self.contactNo, self.userId)
        return self.db.isAlreadyExists(self.db.tblUsers, condition)

    def isIdInvalid(self):
        condition = "user_id = '%d'" % self.userId
        return not self.db.isAlreadyExists(self.db.tblUsers, condition)

    def saveUser(self, requestData, sessionUser) :
        self.userId = self.generateNewUserId()
        self.emailId = JSONHelper.getString(requestData, "email_id")
        self.userGroupId = JSONHelper.getInt(requestData,"user_group_id")
        self.employeeName = JSONHelper.getString(requestData,"employee_name")
        self.employeeCode = JSONHelper.getString(requestData,"employee_code")
        self.contactNo = JSONHelper.getString(requestData,"contact_no")
        self.seatingUnitId =  JSONHelper.getInt(requestData,"seating_unit_id")
        self.userLevel =  JSONHelper.getInt(requestData,"user_level")
        self.countryIds = JSONHelper.getList(requestData,"country_ids")
        self.domainIds = JSONHelper.getList(requestData,"domain_ids")
        self.unitIds = JSONHelper.getList(requestData,"unit_ids")
        self.isAdmin = JSONHelper.getInt(requestData,"is_admin")
        self.isServiceProvider = JSONHelper.getInt(requestData,"is_service_provider")
        try:
            self.serviceProviderId = JSONHelper.getInt(requestData,"service_provider_id")
        except:
            self.serviceProviderId = None
        if self.isDuplicateEmail() :
            return commonResponseStructure("EmailIDAlreadyExists",{})
        elif self.isDuplicateEmployeeCode() :
            return commonResponseStructure("EmployeeCodeAlreadyExists",{})
        elif self.isDuplicateContactNo() :
            return commonResponseStructure("ContactNumberAlreadyExists",{})
        elif self.db.saveUser(self, sessionUser) :
            return commonResponseStructure("SaveClientUserSuccess",{})
        else:
            return commonResponseStructure("Error",{})

    def updateUser(self, requestData, sessionUser) :
        self.userId = JSONHelper.getInt(requestData, "user_id")
        self.userGroupId = JSONHelper.getInt(requestData,"user_group_id")
        self.employeeName = JSONHelper.getString(requestData,"employee_name")
        self.employeeCode = JSONHelper.getString(requestData,"employee_code")
        self.contactNo = JSONHelper.getString(requestData,"contact_no")
        self.seatingUnitId =  JSONHelper.getInt(requestData,"seating_unit_id")
        self.userLevel =  JSONHelper.getInt(requestData,"user_level")
        self.countryIds = JSONHelper.getList(requestData,"country_ids")
        self.domainIds = JSONHelper.getList(requestData,"domain_ids")
        self.unitIds = JSONHelper.getList(requestData,"unit_ids")
        self.isAdmin = JSONHelper.getInt(requestData,"is_admin")
        self.isServiceProvider = JSONHelper.getInt(requestData,"is_service_provider")
        try:
            self.serviceProviderId = JSONHelper.getInt(requestData,"service_provider_id")
        except:
            self.serviceProviderId = None

        if self.isIdInvalid() :
            return commonResponseStructure("InvalidUserId",{})
        elif self.isDuplicateEmployeeCode() :
            return commonResponseStructure("EmployeeCodeAlreadyExists",{})
        elif self.isDuplicateContactNo() :
            return commonResponseStructure("ContactNumberAlreadyExists",{})
        elif self.db.updateUser(self, sessionUser) :
            return commonResponseStructure("UpdateUserSuccess",{})
        else:
            return commonResponseStructure("Error",{})

    def changeUserStatus(self, requestData, sessionUser):
    	self.userId = JSONHelper.getInt(requestData, "user_id")
        self.isActive = JSONHelper.getInt(requestData, "is_active")
        if self.isIdInvalid() :
            return commonResponseStructure("InvalidUserId",{})
        elif self.db.updateUserStatus(self.userId, self.isActive,sessionUser):
            return commonResponseStructure("ChangeClientUserStatusSuccess",{})

    def changeAdminStatus(self, requestData, sessionUser):
        self.userId = JSONHelper.getInt(requestData, "user_id")
        self.isAdmin = JSONHelper.getInt(requestData, "is_admin")
        if self.isIdInvalid() :
            return commonResponseStructure("InvalidUserId",{})
        elif self.db.updateAdminStatus(self.userId, self.isAdmin, sessionUser):
            return commonResponseStructure("UpdateAdminStatusSuccess",{})

    def getDetailedList(self, clientId):
        userList = []
        rows = self.db.getUserDetails()
        for row in rows:
            self.userId = row[0]
            self.emailId = row[1]
            self.userGroupId = row[2]
            self.employeeName = row[3]
            self.employeeCode = row[4]
            self.contactNo = row[5]
            self.seatingUnitId = row[6]
            self.userLevel = row[7]
            self.isAdmin = row[8]
            self.isServiceProvider = row[9]
            self.serviceProviderId = row[10]
            self.isActive = row[11]
            countryIds = self.db.getUserCountries(self.userId)
            domainIds = self.db.getUserDomains(self.userId)
            unitIds = self.db.getUserUnitIds(self.userId)   
            self.countryIds = [int(x) for x in countryIds.split(",")]
            self.domainIds = [int(x) for x in domainIds.split(",")]
            self.unitIds = [int(x) for x in unitIds.split(",")]
            userList.append(self.toDetailedStructure())
        return userList

    def getUsers(self, sessionUser) :
        countryList= CountryList().getUserCountry(sessionUser)
        domainList = DomainList().getUserDomains(sessionUser)
        DetailsTuple = self.db.getUserCompanyDetails(sessionUser)
        unitIds = DetailsTuple[0]
        divisionIds = DetailsTuple[1]
        legalEntityIds = DetailsTuple[2]
        businessGroupIds = DetailsTuple[3]

        clientId = 1
        divisionList = None
        businessGroupList = None
        if businessGroupIds != None:
            businessGroupList = BusinessGroup(clientId, self.db).getBusinessGroupById(businessGroupIds)
        legalEntityList = LegalEntity(clientId, self.db).getLegalEntitiesById(legalEntityIds)
        if divisionIds != None:
            divisionList = Division(clientId, self.db).getDivisionsById(divisionIds)
        unitList = Unit(clientId, self.db).getUnitsById(unitIds)
        userGroupList = UserPrivilege().getList(clientId)
        userList = User().getDetailedList(clientId)
        serviceProvidersList = ServiceProvider().getList()

        response_data = {}
        response_data["domains"] = domainList
        response_data["countries"] = countryList
        response_data["business_groups"] = businessGroupList
        response_data["legal_entities"] = legalEntityList
        response_data["divisions"] = divisionList
        response_data["units"] = unitList
        response_data["user_groups"] = userGroupList
        response_data["users"] = userList
        response_data["service_providers"] = serviceProvidersList

        response = commonResponseStructure("GetClientUsersSuccess", response_data)
        return response

class ServiceProvider() :
    clientId = None
    serviceProviderId =  None
    serviceProviderName =  None
    address =  None
    contractFrom =  None
    contractTo =  None
    contactPerson =  None
    contactNo =  None
    isActive = 1
    db = None

    def __init__(self) :
        self.db = ClientDatabaseHandler.instance()

    def toDetailedStructure(self):
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

    def toStructure(self):
        return {
            "service_provider_id": self.serviceProviderId,
            "service_provider_name": self.serviceProviderName,
            "is_active": self.isActive
        }

    def getDetailedList(self):
        servcieProviderList = []
        rows = self.db.getServiceProviderDetailsList()
        for row in rows:
            self.serviceProviderId = int(row[0])
            self.serviceProviderName = row[1]
            self.address = row[2]
            self.contractFrom = datetimeToString(row[3])
            self.contractTo = datetimeToString(row[4])
            self.contactPerson = row[5]
            self.contactNo = row[6]
            self.isActive = row[7]
            servcieProviderList.append(self.toDetailedStructure())

        return servcieProviderList

    def getList(self):
        servcieProviderList = []
        rows = self.db.getServiceProviders()
        for row in rows:
            self.serviceProviderId = int(row[0])
            self.serviceProviderName = row[1]
            self.isActive = row[2]
            servcieProviderList.append(self.toStructure())
        return servcieProviderList

    def getServiceProviders(self) :
        serviceProviderList = self.getDetailedList()

        response_data = {}
        response_data["service_providers"] = serviceProviderList

        response = commonResponseStructure("GetServiceProvidersSuccess", response_data)
        return response

    def generateNewId(self) :
        return self.db.generateNewId(self.db.tblServiceProviders, "service_provider_id")

    def isDuplicate(self):
        print "Checking isDuplicate"
        condition = "service_provider_name ='%s' AND service_provider_id != '%d'" %(
            self.serviceProviderName, self.serviceProviderId)
        return self.db.isAlreadyExists(self.db.tblServiceProviders, condition)

    def isDuplicateContactNo(self):
        print "Checking isDuplicateContactNo"
        condition = "contact_no ='%s' AND service_provider_id != '%d'" % (self.contactNo, 
            self.serviceProviderId)
        return self.db.isAlreadyExists(self.db.tblServiceProviders, condition)

    def isIdInvalid(self):
        condition = "service_provider_id = '%d'" % self.serviceProviderId
        return not self.db.isAlreadyExists(self.db.tblServiceProviders, condition)

    def saveServiceProvider(self, requestData, sessionUser) :
        self.serviceProviderId = self.generateNewId()
        self.serviceProviderName = JSONHelper.getString(requestData, "service_provider_name")
        self.address = JSONHelper.getString(requestData, "address")
        self.contractFrom =  JSONHelper.getString(requestData, "contract_from")
        self.contractTo =  JSONHelper.getString(requestData, "contract_to")
        self.contactPerson =  JSONHelper.getString(requestData, "contact_person")
        self.contactNo =  JSONHelper.getString(requestData, "contact_no")
        self.contractFrom = stringToDatetime(self.contractFrom)
        self.contractTo = stringToDatetime(self.contractTo)
        if self.isDuplicate() :
            return commonResponseStructure("ServiceProviderNameAlreadyExists",{})
        elif self.isDuplicateContactNo() :
            return commonResponseStructure("ContactNumberAlreadyExists",{})
        elif self.db.saveServiceProvider(self, sessionUser) :
            return commonResponseStructure("SaveServiceProviderSuccess",{})
        else:
            return commonResponseStructure("Error",{})

    def updateServiceProvider(self, requestData, sessionUser) :
        self.serviceProviderId = JSONHelper.getInt(requestData,"service_provider_id")
        self.serviceProviderName = JSONHelper.getString(requestData, "service_provider_name")
        self.address = JSONHelper.getString(requestData, "address")
        self.contractFrom =  JSONHelper.getString(requestData, "contract_from")
        self.contractTo =  JSONHelper.getString(requestData, "contract_to")
        self.contactPerson =  JSONHelper.getString(requestData, "contact_person")
        self.contactNo =  JSONHelper.getString(requestData, "contact_no")
        self.contractFrom = stringToDatetime(self.contractFrom)
        self.contractTo = stringToDatetime(self.contractTo)
        if self.isIdInvalid() :
            return commonResponseStructure("InvalidServiceProviderId",{})
        elif self.isDuplicate() :
            return commonResponseStructure("ServiceProviderNameAlreadyExists",{})
        elif self.isDuplicateContactNo() :
            return commonResponseStructure("ContactNumberAlreadyExists",{})
        elif self.db.updateServiceProvider(self, sessionUser) :
            return commonResponseStructure("UpdateServiceProviderSuccess",{})
        else:
            return commonResponseStructure("Error",{})

    def changeServiceProviderStatus(self, requestData, sessionUser) :
        self.serviceProviderId = JSONHelper.getInt(requestData,"service_provider_id")
        self.isActive = JSONHelper.getInt(requestData, "is_active")
        if self.isIdInvalid() :
            return commonResponseStructure("InvalidServiceProviderId",{})
        elif self.db.updateServiceProviderStatus(self.serviceProviderId, self.isActive, sessionUser):
            return commonResponseStructure("ChangeServiceProviderStatusSuccess",{})

class UnitClosure():

    def __init__(self):
        self.db = ClientDatabaseHandler.instance()

    def getList(self, sessionUser):
        clientId = 1
        unitList = Unit(clientId, self.db).getUnitListForClosure(clientId)
        unitStructure = {}
        unitStructure["units"] = unitList
        return commonResponseStructure("GetUnitClosureListSuccess", unitStructure)

    def closeUnit(self, requestData, sessionUser):
        self.sessionUser = sessionUser
        self.unitId = JSONHelper.getInt(requestData, "unit_id")
        self.password = JSONHelper.getString(requestData, "password")
        self.clientId = 1

        if self.verifyPassword():
            if self.db.deactivateUnit(self.unitId):
                return commonResponseStructure("CloseUnitSuccess", {})
            else:
                print "Error : While deactivating Unit in client DB"
                return False
        else:
            return commonResponseStructure("InvalidPassword", {})

    def verifyPassword(self):
        encryptedPassword = encrypt(self.password)
        return self.db.verifyPassword(encryptedPassword, self.sessionUser)




        


