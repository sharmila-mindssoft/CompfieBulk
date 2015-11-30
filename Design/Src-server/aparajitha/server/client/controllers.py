import json

import tornado.ioloop
import tornado.web
import uuid

from models import *
from aparajitha.server.common import *
from aparajitha.server.knowledge.models import DomainList, CountryList
from aparajitha.server.databasehandler import DatabaseHandler

__all__ = [
    "UserPrivilegeController",
    "UserController",
    "ServiceProviderController"
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
        address =  JSONHelper.getString(requestData,"address")
        designation =  JSONHelper.getString(requestData,"designation")
        countryIds = JSONHelper.getList(requestData,"country_ids")
        domainIds = JSONHelper.getList(requestData,"domain_ids")
        user = User(None, emailId, userGroupId, employeeName, employeeCode, contactNo, 
                    address, designation, countryIds, domainIds, None,None)
        if user.isDuplicateEmail() :
            return commonResponseStructure("EmailIDAlreadyExists",{})
        elif user.isDuplicateEmployeeCode() :
            return commonResponseStructure("EmployeeCodeAlreadyExists",{})
        elif user.isDuplicateContactNo() :
            return commonResponseStructure("ContactNumberAlreadyExists",{})
        elif user.save(sessionUser) :
            return commonResponseStructure("SaveUserSuccess",{})
        else:
            return commonResponseStructure("Error",{})

    def updateUser(self, requestData, sessionUser) :
        userId = JSONHelper.getInt(requestData,"user_id")
        userGroupId = JSONHelper.getInt(requestData,"user_group_id")
        employeeName = JSONHelper.getString(requestData,"employee_name")
        employeeCode = JSONHelper.getString(requestData,"employee_code")
        contactNo = JSONHelper.getString(requestData,"contact_no")
        address =  JSONHelper.getString(requestData,"address")
        designation =  JSONHelper.getString(requestData,"designation")
        countryIds = JSONHelper.getList(requestData,"country_ids")
        domainIds = JSONHelper.getList(requestData,"domain_ids")
        user = User(userId, None, userGroupId, employeeName, employeeCode, contactNo,
                    address, designation, countryIds, domainIds, None, None)
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
        user = User(userId, None, None, None, None, None,
                    None, None, None, None, None,isActive)
        if user.isIdInvalid() :
            return commonResponseStructure("InvalidUserId",{})
        elif user.updateStatus(sessionUser):
            return commonResponseStructure("ChangeUserStatusSuccess",{})

    def getUsers(self) :
    	domainList = DomainList.getDomainList()
        countryList = CountryList.getCountryList()
    	userGroupList = UserGroup.getList()
    	userList = User.getDetailedList()

        response_data = {}
        response_data["domains"] = domainList
        response_data["countries"] = countryList
        response_data["user_groups"] = userGroupList
        response_data["users"] = userList

        response = commonResponseStructure("GetUsersSuccess", response_data)
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

        


