import json

import tornado.ioloop
import tornado.web
import uuid

from models import *
from aparajitha.server.common import *
from aparajitha.server.admin.models import User as AdminUser
from aparajitha.server.techno.models import GroupCompany, BusinessGroup,LegalEntity,Division,Unit
from aparajitha.server.knowledge.models import DomainList, CountryList
from aparajitha.server.databasehandler import DatabaseHandler
from aparajitha.server.clientdatabasehandler import ClientDatabaseHandler

__all__ = [
    "UserPrivilegeController",
    "UserController",
    "ServiceProviderController",
    "UnitClosure"
]

class UserPrivilegeController() :
    db = None
    clientId = None
    userGroupId = None
    userGroupName = None
    formType = None
    formIds = None
    isActive = 1

    def __init__(self) :
        db = ClientDatabaseHandler.instance()

    def getUserGroupsFormData(self) :
    	ClientForms = Form.getForms("client")
        forms = Menu.getMenu(ClientForms)
        return forms

    def getUserPrivileges(self, sessionUser) :
    	forms = self.getUserGroupsFormData()
    	userGroupList = UserPrivilege.getDetailedList(sessionUser)

        response_data = {}
        response_data["forms"] = forms
        response_data["user_groups"] = userGroupList

        response = commonResponseStructure("GetUserGroupsSuccess", response_data)
        return response

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

    def generateNewUserGroupId(self) :
        return self.db.generateNewId(self.db.tblUserGroups, "user_group_id")

    def isDuplicate(self):
        condition = "user_group_name ='%s' AND user_group_id = '%d'" % (
            self.userGroupName, self.userGroupId)
        return self.db.isAlreadyExists(self.db.tblUserGroups, condition)

    def isIdInvalid(self):
        condition = "user_group_id = '%d'" % self.userGroupId
        return not self.db.isAlreadyExists(self.tblUserGroups, condition)

    def saveUserPrivilege(self, requestData, sessionUser) :
        self.userGroupName = JSONHelper.getString(requestData, "user_group_name")
        self.formType = JSONHelper.getString(requestData, "form_type")
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
        self.formType = JSONHelper.getString(requestData,"form_type")
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

class UserController() :
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
        db = ClientDatabaseHandler.instance()
        
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
        return self.db.generateNewId(self.tblUsers, "user_id")

    def isDuplicateEmail(self):
        condition = "username ='%s' AND user_id != '%d'" % (self.emailId, self.userId)
        return self.db.isAlreadyExists(self.tblUsers, condition)

    def isDuplicateEmployeeCode(self):
        condition = "employee_code ='%s' AND user_id != '%d'" % (self.employeeCode, self.userId)
        return self.db.isAlreadyExists(self.tblUsers, condition)

    def isDuplicateContactNo(self):
        condition = "contact_no ='%s' AND user_id != '%d'" % (self.contactNo, self.userId)
        return self.db.isAlreadyExists(self.tblUsers, condition)

    def isIdInvalid(self):
        condition = "user_id = '%d'" % self.userId
        return not self.db.isAlreadyExists(self.tblUsers, condition)

    def saveUser(self, requestData, sessionUser) :
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
        elif self.db.saveUser(sessionUser) :
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
        elif self.db.updateUser(sessionUser) :
            return commonResponseStructure("UpdateUserSuccess",{})
        else:
            return commonResponseStructure("Error",{})

    def changeUserStatus(self, requestData, sessionUser):
    	self.userId = JSONHelper.getInt(requestData, "user_id")
        self.isActive = JSONHelper.getInt(requestData, "is_active")
        if self.isIdInvalid() :
            return commonResponseStructure("InvalidUserId",{})
        elif self.db.updateUserStatus(sessionUser):
            return commonResponseStructure("ChangeClientUserStatusSuccess",{})

    def changeAdminStatus(self, requestData, sessionUser):
        self.userId = JSONHelper.getInt(requestData, "user_id")
        self.isAdmin = JSONHelper.getInt(requestData, "is_admin")
        if self.isIdInvalid() :
            return commonResponseStructure("InvalidUserId",{})
        elif self.db.updateAdminStatus(sessionUser):
            return commonResponseStructure("UpdateAdminStatusSuccess",{})

    def getUsers(self, sessionUser) :
        clientId = str(getClientId(sessionUser))

        countryList = CountryList.getCountryList()
        domainList = DomainList.getDomainList()
        businessGroupList = BusinessGroup.getList(clientId)
        legalEntityList = LegalEntity.getList(clientId)
        divisionList = Division.getList(clientId)
        unitList = Unit.getList(clientId)
        userGroupList = UserPrivilege.getList(clientId)
        userList = User.getDetailedList(clientId)
        groupDetails = GroupCompany.getDetailedClientList()
        serviceProvidersList = ServiceProvider.getSimpleList(sessionUser)


        countryIds =groupDetails[0]["country_ids"]
        domainIds =groupDetails[0]["domain_ids"]

        newCountryList = []
        newDomainList = []
        for country in countryList:
            if str(country["country_id"]) in countryIds:
                newCountryList.append(country) 

        for domain in domainList:
            if str(domain["domain_id"]) in domainIds:
                newDomainList.append(domain)

        response_data = {}
        response_data["domains"] = newDomainList
        response_data["countries"] = newCountryList
        response_data["business_groups"] = businessGroupList
        response_data["legal_entities"] = legalEntityList
        response_data["divisions"] = divisionList
        response_data["units"] = unitList
        response_data["user_groups"] = userGroupList
        response_data["users"] = userList
        response_data["service_providers"] = serviceProvidersList

        response = commonResponseStructure("GetClientUsersSuccess", response_data)
        return response

class ServiceProviderController() :
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

    def getUserGroupsFormData(self) :
        ClientForms = Form.getForms("client")
        forms = Menu.getMenu(ClientForms)
        return forms

    def getServiceProviders(self, sessionUser) :
        serviceProviderList = ServiceProvider.getList(sessionUser)

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
        self.contractFrom = datetimeToTimestamp(stringToDatetime(self.contractFrom))
        self.contractTo = datetimeToTimestamp(stringToDatetime(self.contractTo))
        if self.isIdInvalid() :
            return commonResponseStructure("InvalidServiceProviderId",{})
        elif self.isDuplicate() :
            return commonResponseStructure("ServiceProviderNameAlreadyExists",{})
        elif self.isDuplicateContactNo() :
            return commonResponseStructure("ContactNumberAlreadyExists",{})
        elif self.updateServiceProvider(self, sessionUser) :
            return commonResponseStructure("UpdateServiceProviderSuccess",{})
        else:
            return commonResponseStructure("Error",{})

    def changeServiceProviderStatus(self, requestData, sessionUser) :
        self.serviceProviderId = JSONHelper.getInt(requestData,"service_provider_id")
        self.isActive = JSONHelper.getInt(requestData, "is_active")
        if self.isIdInvalid() :
            return commonResponseStructure("InvalidServiceProviderId",{})
        elif self.db.updateServiceProviderStatus(sessionUser):
            return commonResponseStructure("ChangeServiceProviderStatusSuccess",{})

class UnitClosure():
    unitTblName = "tbl_units"

    def getList(self, sessionUser):
        self.clientId = getClientId(sessionUser)
        unitList = Unit.getUnitListForClosure(self.clientId)
        unitStructure = {}
        unitStructure["units"] = unitList
        return commonResponseStructure("GetUnitClosureListSuccess", unitStructure)

    def closeUnit(self, requestData, sessionUser):
        self.sessionUser = sessionUser
        self.unitId = JSONHelper.getInt(requestData, "unit_id")
        self.password = JSONHelper.getString(requestData, "password")
        self.clientId = getClientId(sessionUser)

        if self.verifyPassword():
            if self.deactivateUnitInClientDB():
                if self.deactivateUnitInKnowledgeDB():
                    return commonResponseStructure("CloseUnitSuccess", {})
                else:
                    print "Error : While deactivating Unit in Knowledge DB"    
                    return False
            else:
                print "Error : While deactivating Unit in client DB"
                return False
        else:
            return commonResponseStructure("InvalidPassword", {})

    def verifyPassword(self):
        encryptedPassword = encrypt(self.password)
        return DatabaseHandler.instance().verifyPassword(encryptedPassword, 
            self.sessionUser, self.clientId)

    def deactivateUnitInClientDB(self):
        columns = ["is_active"]
        values = [0]
        condition = "unit_id ='%d'" % self.unitId
        return ClientDatabaseHandler.instance(
            getClientDatabase(self.clientId)).update(
            self.unitTblName, columns, values, condition)

    def deactivateUnitInKnowledgeDB(self):    
        columns = ["is_active", "updated_by", "updated_on"]
        values = [0, self.sessionUser, getCurrentTimeStamp()]
        condition = "unit_id = {unitId} and client_id={clientId}".format(
            unitId = self.unitId, clientId = self.clientId)
        return DatabaseHandler.instance().update(
            self.unitTblName, columns, values, condition)




        


