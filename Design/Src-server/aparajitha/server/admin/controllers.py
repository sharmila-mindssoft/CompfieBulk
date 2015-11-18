import json

import tornado.ioloop
import tornado.web

from aparajitha.server.databasehandler import DatabaseHandler
from models import *
from aparajitha.server.common import *
from aparajitha.server.knowledge.models import DomainList

__all__ = [
    "UserGroupController",
    "UserController"
]

class UserGroupController() :
    def getUserGroupsFormData(self) :
    	print "inside get user groups form data"
    	knowledgeForms = Form.getForms("Knowledge")
    	technoForms = Form.getForms("Techno")

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
        domainIds = JSONHelper.getList(requestData,"domain_ids")
        user = User(None, emailId, userGroupId, employeeName, employeeCode, 
                    contactNo, address, designation, domainIds, None)
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
        domainIds = JSONHelper.getList(requestData,"domain_ids")
        user = User(userId, None, userGroupId, employeeName, employeeCode, 
                    contactNo, address, designation, domainIds, None)
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
                    None, None, None, None, isActive)
        if user.isIdInvalid() :
            return commonResponseStructure("InvalidUserId",{})
        elif user.updateStatus(sessionUser):
            return commonResponseStructure("ChangeUserStatusSuccess",{})

    def getUsers(self) :
    	domainList = DomainList.getDomainList()
    	print domainList
    	userGroupList = UserGroup.getList()
    	print userGroupList
    	userList = User.getList()

        response_data = {}
        response_data["domains"] = domainList
        response_data["user_groups"] = userGroupList
        response_data["users"] = userList

        response = commonResponseStructure("GetUsersSuccess", response_data)
        return response
