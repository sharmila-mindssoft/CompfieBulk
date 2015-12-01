import json

import tornado.ioloop
import tornado.web
import uuid

from models import *
from aparajitha.server.common import *
from aparajitha.server.admin.models import User as AdminUser
from aparajitha.server.techno.models import BusinessGroup,LegalEntity,Division,Unit
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
    def getUserGroupsFormData(self) :
    	ClientForms = Form.getForms("client")
        forms = Menu.getMenu(ClientForms)
        return forms

    def getUserPrivileges(self, sessionUser) :
    	forms = self.getUserGroupsFormData()
        print "got forms"
    	userGroupList = UserPrivilege.getDetailedList(sessionUser)
        print "got userGroupList"

        response_data = {}
        response_data["forms"] = forms
        response_data["user_groups"] = userGroupList

        response = commonResponseStructure("GetUserGroupsSuccess", response_data)
        return response

    def saveUserPrivilege(self, requestData, sessionUser) :
        userGroupName = JSONHelper.getString(requestData, "user_group_name")
        formType = JSONHelper.getString(requestData, "form_type")
        formIds =  JSONHelper.getList(requestData, "form_ids")
        userPrivilege = UserPrivilege(getClientId(sessionUser), None, userGroupName, 
            formType, formIds, None)
        if userPrivilege.isDuplicate() :
            return commonResponseStructure("GroupNameAlreadyExists",{})
        elif userPrivilege.save(sessionUser) :
            return commonResponseStructure("SaveUserGroupSuccess",{})
        else:
            return commonResponseStructure("Error",{})

    def updateUserPrivilege(self, requestData, sessionUser) :
        userGroupId = JSONHelper.getInt(requestData,"user_group_id")
        userGroupName = JSONHelper.getString(requestData,"user_group_name")
        formType = JSONHelper.getString(requestData,"form_type")
        formIds =  JSONHelper.getList(requestData,"form_ids")
        userPrivilege = UserPrivilege(getClientId(sessionUser), userGroupId, userGroupName, formType, formIds, None)
        if userPrivilege.isIdInvalid() :
            return commonResponseStructure("InvalidGroupId",{})
        elif userPrivilege.isDuplicate() :
            return commonResponseStructure("GroupNameAlreadyExists",{})
        elif userPrivilege.update(sessionUser) :
            return commonResponseStructure("UpdateUserGroupSuccess",{})
        else:
            return commonResponseStructure("Error",{})

    def changeUserPrivilegeStatus(self, requestData, sessionUser) :
        userGroupId = JSONHelper.getInt(requestData, "user_group_id")
        isActive = JSONHelper.getInt(requestData, "is_active")
        userPrivilege = UserPrivilege(getClientId(sessionUser), userGroupId, None, None, None, isActive)
        if userPrivilege.isIdInvalid() :
            return commonResponseStructure("InvalidGroupId",{})
        elif userPrivilege.updateStatus(sessionUser):
            return commonResponseStructure("ChangeUserGroupStatusSuccess",{})

class UserController() :
    def saveUser(self, requestData, sessionUser) :
        emailId = JSONHelper.getString(requestData, "email_id")
        userGroupId = JSONHelper.getInt(requestData,"user_group_id")
        employeeName = JSONHelper.getString(requestData,"employee_name")
        employeeCode = JSONHelper.getString(requestData,"employee_code")
        contactNo = JSONHelper.getString(requestData,"contact_no")
        seatingUnitId =  JSONHelper.getInt(requestData,"seating_unit_id")
        userLevel =  JSONHelper.getInt(requestData,"user_level")
        countryIds = JSONHelper.getList(requestData,"country_ids")
        domainIds = JSONHelper.getList(requestData,"domain_ids")
        unitIds = JSONHelper.getList(requestData,"unit_ids")
        isAdmin = JSONHelper.getInt(requestData,"is_admin")
        isServiceProvider = JSONHelper.getInt(requestData,"is_service_provider")
        try:
            serviceProviderId = JSONHelper.getInt(requestData,"service_provider_id")
        except:
            serviceProviderId = None

        user = User(getClientId(sessionUser), None, emailId, userGroupId, employeeName, 
                    employeeCode, contactNo, seatingUnitId, userLevel, countryIds,
                    domainIds, unitIds, isAdmin, isServiceProvider, serviceProviderId)
        if user.isDuplicateEmail() :
            return commonResponseStructure("EmailIDAlreadyExists",{})
        elif user.isDuplicateEmployeeCode() :
            return commonResponseStructure("EmployeeCodeAlreadyExists",{})
        elif user.isDuplicateContactNo() :
            return commonResponseStructure("ContactNumberAlreadyExists",{})
        elif user.save(sessionUser) :
            return commonResponseStructure("SaveClientUserSuccess",{})
        else:
            return commonResponseStructure("Error",{})

    def updateUser(self, requestData, sessionUser) :
        userId = JSONHelper.getInt(requestData, "user_id")
        userGroupId = JSONHelper.getInt(requestData,"user_group_id")
        employeeName = JSONHelper.getString(requestData,"employee_name")
        employeeCode = JSONHelper.getString(requestData,"employee_code")
        contactNo = JSONHelper.getString(requestData,"contact_no")
        seatingUnitId =  JSONHelper.getInt(requestData,"seating_unit_id")
        userLevel =  JSONHelper.getInt(requestData,"user_level")
        countryIds = JSONHelper.getList(requestData,"country_ids")
        domainIds = JSONHelper.getList(requestData,"domain_ids")
        unitIds = JSONHelper.getList(requestData,"unit_ids")
        isAdmin = JSONHelper.getInt(requestData,"is_admin")
        isServiceProvider = JSONHelper.getInt(requestData,"is_service_provider")
        try:
            serviceProviderId = JSONHelper.getInt(requestData,"service_provider_id")
        except:
            serviceProviderId = None

        user = User(getClientId(sessionUser), userId, None,userGroupId, employeeName, 
                    employeeCode, contactNo, seatingUnitId, userLevel, countryIds,
                    domainIds, unitIds, isAdmin, isServiceProvider, serviceProviderId)
        if user.isIdInvalid() :
            return commonResponseStructure("InvalidUserId",{})
        elif user.isDuplicateEmployeeCode() :
            return commonResponseStructure("EmployeeCodeAlreadyExists",{})
        elif user.isDuplicateContactNo() :
            return commonResponseStructure("ContactNumberAlreadyExists",{})
        elif user.update(sessionUser) :
            return commonResponseStructure("UpdateUserSuccess",{})
        else:
            return commonResponseStructure("Error",{})

    def changeUserStatus(self, requestData, sessionUser):
    	userId = JSONHelper.getInt(requestData, "user_id")
        isActive = JSONHelper.getInt(requestData, "is_active")
        user = AdminUser(userId, None, None, None, None, None,
                    None, None, None, None, None,isActive)
        if user.isIdInvalid() :
            return commonResponseStructure("InvalidUserId",{})
        elif user.updateStatus(sessionUser):
            return commonResponseStructure("ChangeClientUserStatusSuccess",{})

    def changeAdminStatus(self, requestData, sessionUser):
        print "inside change Admin status in controller"
        userId = JSONHelper.getInt(requestData, "user_id")
        isAdmin = JSONHelper.getInt(requestData, "is_admin")
        user = User( getClientId(sessionUser), userId, None, None, None, None, None, None, None, 
                    None, None, None, isAdmin, None, None )
        if user.isIdInvalid() :
            return commonResponseStructure("InvalidUserId",{})
        elif user.updateAdminStatus(sessionUser):
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

        response_data = {}
        response_data["domains"] = domainList
        response_data["countries"] = countryList
        response_data["business_groups"] = businessGroupList
        response_data["legal_entities"] = legalEntityList
        response_data["divisions"] = divisionList
        response_data["units"] = unitList
        response_data["user_groups"] = userGroupList
        response_data["users"] = userList

        response = commonResponseStructure("GetClientUsersSuccess", response_data)
        return response

class ServiceProviderController() :
    tblName = " tbl_service_providers"

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

    def saveServiceProvider(self, requestData, sessionUser) :
        serviceProviderName = JSONHelper.getString(requestData, "service_provider_name")
        address = JSONHelper.getString(requestData, "address")
        contractFrom =  JSONHelper.getString(requestData, "contract_from")
        contractTo =  JSONHelper.getString(requestData, "contract_to")
        contactPerson =  JSONHelper.getString(requestData, "contact_person")
        contactNo =  JSONHelper.getString(requestData, "contact_no")
        contractFrom = datetimeToTimestamp(stringToDatetime(contractFrom))
        contractTo = datetimeToTimestamp(stringToDatetime(contractTo))
        serviceProvider = ServiceProvider(getClientId(sessionUser), None, serviceProviderName, 
                                        address, contractFrom, contractTo, contactPerson, 
                                        contactNo, None)
        if serviceProvider.isDuplicate() :
            return commonResponseStructure("ServiceProviderNameAlreadyExists",{})
        elif serviceProvider.isDuplicateContactNo() :
            return commonResponseStructure("ContactNumberAlreadyExists",{})
        elif serviceProvider.save(sessionUser) :
            return commonResponseStructure("SaveServiceProviderSuccess",{})
        else:
            return commonResponseStructure("Error",{})

    def updateServiceProvider(self, requestData, sessionUser) :
        serviceProviderId = JSONHelper.getInt(requestData,"service_provider_id")
        serviceProviderName = JSONHelper.getString(requestData, "service_provider_name")
        address = JSONHelper.getString(requestData, "address")
        contractFrom =  JSONHelper.getString(requestData, "contract_from")
        contractTo =  JSONHelper.getString(requestData, "contract_to")
        contactPerson =  JSONHelper.getString(requestData, "contact_person")
        contactNo =  JSONHelper.getString(requestData, "contact_no")
        contractFrom = datetimeToTimestamp(stringToDatetime(contractFrom))
        contractTo = datetimeToTimestamp(stringToDatetime(contractTo))
        serviceProvider = ServiceProvider(getClientId(sessionUser), serviceProviderId, 
                                        serviceProviderName, address, contractFrom, 
                                        contractTo, contactPerson, contactNo, None)
        if serviceProvider.isIdInvalid() :
            return commonResponseStructure("InvalidServiceProviderId",{})
        elif serviceProvider.isDuplicate() :
            return commonResponseStructure("ServiceProviderNameAlreadyExists",{})
        elif serviceProvider.isDuplicateContactNo() :
            return commonResponseStructure("ContactNumberAlreadyExists",{})
        elif serviceProvider.update(sessionUser) :
            return commonResponseStructure("UpdateServiceProviderSuccess",{})
        else:
            return commonResponseStructure("Error",{})

    def changeServiceProviderStatus(self, requestData, sessionUser) :
        serviceProviderId = JSONHelper.getInt(requestData,"service_provider_id")
        isActive = JSONHelper.getInt(requestData, "is_active")
        serviceProvider = ServiceProvider(getClientId(sessionUser), serviceProviderId,
                                        None, None, None, None, None, None, isActive )
        if serviceProvider.isIdInvalid() :
            return commonResponseStructure("InvalidServiceProviderId",{})
        elif serviceProvider.updateStatus(sessionUser):
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




        


