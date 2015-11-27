import json

import tornado.ioloop
import tornado.web

from models import *
from aparajitha.server.common import *
from aparajitha.server.knowledge.models import DomainList, CountryList
from aparajitha.server.databasehandler import DatabaseHandler

__all__ = [
    "UserGroupController",
    "UserController",
    "ChangePassword"
]

class UserGroupController() :
    def getUserGroupsFormData(self) :
    	knowledgeForms = Form.getForms("knowledge")
    	technoForms = Form.getForms("techno")

        result = {}
        result["knowledge"] = Menu.getMenu(knowledgeForms)
        result["techno"] = Menu.getMenu(technoForms)

        return result

    def getUserGroups(self) :
    	forms = self.getUserGroupsFormData()
    	userGroupList = UserGroup.getDetailedList()

        response_data = {}
        response_data["forms"] = forms
        response_data["user_groups"] = userGroupList

        response = commonResponseStructure("GetUserGroupsSuccess", response_data)
        return response

    def saveUserGroup(self, requestData, sessionUser) :
        userGroupName = JSONHelper.getString(requestData, "user_group_name")
        formType = JSONHelper.getString(requestData, "form_type")
        formIds =  JSONHelper.getList(requestData, "form_ids")
        userGroup = UserGroup(None, userGroupName, formType, formIds, None)
        if userGroup.isDuplicate() :
            return commonResponseStructure("GroupNameAlreadyExists",{})
        elif userGroup.save(sessionUser) :
            return commonResponseStructure("SaveUserGroupSuccess",{})
        else:
            return commonResponseStructure("Error",{})

    def updateUserGroup(self, requestData, sessionUser) :
        userGroupId = JSONHelper.getInt(requestData,"user_group_id")
        userGroupName = JSONHelper.getString(requestData,"user_group_name")
        formType = JSONHelper.getString(requestData,"form_type")
        formIds =  JSONHelper.getList(requestData,"form_ids")
        userGroup = UserGroup(userGroupId, userGroupName, formType, formIds, None)
        if userGroup.isIdInvalid() :
            return commonResponseStructure("InvalidGroupId",{})
        elif userGroup.isDuplicate() :
            return commonResponseStructure("GroupNameAlreadyExists",{})
        elif userGroup.update(sessionUser) :
            return commonResponseStructure("UpdateUserGroupSuccess",{})
        else:
            return commonResponseStructure("Error",{})

    def changeUserGroupStatus(self, requestData, sessionUser) :
        userGroupId = JSONHelper.getInt(requestData, "user_group_id")
        isActive = JSONHelper.getInt(requestData, "is_active")
        userGroup = UserGroup(userGroupId, None, None, None, isActive)
        if userGroup.isIdInvalid() :
            return commonResponseStructure("InvalidGroupId",{})
        elif userGroup.updateStatus(sessionUser):
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
        user = User(userId, None, None, None, None, 
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


class ChangePassword() :
    userTblName = "tbl_users"

    def changePassword(self, requestData, sessionUser) :
        self.sessionUser = sessionUser
        self.currentPassword = JSONHelper.getString(requestData, "current_password")
        self.newPassword = JSONHelper.getString(requestData, "new_password")

        if self.validateCurrentPassword() :
            if self.updatePassword() :
                return commonResponseStructure("ChangePasswordSuccess",{})
        else :
            return commonResponseStructure("InvalidCurrentPassword",{})

    def validateCurrentPassword(self):
        column = "password"
        condition = " user_id='"+str(self.sessionUser)+"'"
        rows = DatabaseHandler.instance().getData(self.userTblName, column, condition)
        password = rows[0][0]
        if password == encrypt(self.currentPassword):
            return True
        else:
            return False

    def updatePassword(self):
        columns = ["password"]
        values = [encrypt(self.newPassword)]
        condition = " user_id='"+str(self.sessionUser)+"'"
        if DatabaseHandler.instance().update(self.userTblName, columns, values, condition):
            return True
        else:
            return False
