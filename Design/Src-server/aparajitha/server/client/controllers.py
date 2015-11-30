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
    "ChangePassword",
    "ForgotPassword"
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

class ForgotPassword() :
    userTblName = "tbl_users"
    emailVerificationTblName = "tbl_email_verification"

    def processRequest(self, requestData, url):
        self.url = url
        self.username = JSONHelper.getString(requestData, "username")
        if self.validateUsername():
            if self.sendResetLink():
                return commonResponseStructure("ForgotPasswordSuccess",{})
            else:
                print "sendResetLink Failed"
        else:
            return commonResponseStructure("InvalidUsername",{})

    def validateUsername(self):
        column = "count(*), user_id"
        condition = " username='"+self.username+"'"
        rows = DatabaseHandler.instance().getData(self.userTblName, column, condition)
        count = rows[0][0]
        if count == 1:
            self.userId = rows[0][1]
            return True
        else :
            return False

    def sendResetLink(self):
        resetToken = uuid.uuid4()
        print "http://localhost:8080"+self.url+"/ForgotPassword?reset_token=%d" % resetToken
        columns = "user_id, verification_code"
        valuesList = [self.userId, int(resetToken)]
        values = listToString(valuesList)
        if DatabaseHandler.instance().insert(self.emailVerificationTblName, columns, values):
            if self.sendEmail():
                return True
            else:
                print "Send email failed"
        else:
            print "Saving reset token failed"


    def sendEmail(self):
        return True

    def validateResetToken(self, requestData, url):
        self.resetToken = JSONHelper.getString(requestData, "reset_token")
        if self.validate():
            return commonResponseStructure("ResetTokenValidationSuccess", {})
        else:
            return commonResponseStructure("InvalidResetToken", {})

    def validate(self):
        column = "count(*), user_id"
        condition = " verification_code='"+self.resetToken+"'"
        rows = DatabaseHandler.instance().getData(self.emailVerificationTblName, column, condition)
        count = rows[0][0]
        self.userId = rows[0][1]
        if count == 1:
            return True
        else:
            return False

    def getUserId(self):
        column = "user_id"
        condition = " verification_code='"+self.resetToken+"'"
        rows = DatabaseHandler.instance().getData(self.emailVerificationTblName, column, condition)
        return rows[0][0]

    def updatePassword(self):
        columns = ["password"]
        values = [encrypt(self.newPassword)]
        condition = " user_id='%d'" % self.getUserId()
        if DatabaseHandler.instance().update(self.userTblName, columns, values, condition):
            return True
        else:
            return False

    def deleteUsedToken(self):
        condition = " verification_code='"+self.resetToken+"'"
        if DatabaseHandler.instance().delete(self.emailVerificationTblName, condition):
            return True
        else:
            return False

    def resetPassword(self, requestData):
        self.resetToken = JSONHelper.getString(requestData, "reset_token")
        if self.validate():
            self.newPassword = JSONHelper.getString(requestData, "new_password")
            if self.updatePassword():
                if self.deleteUsedToken():
                    return commonResponseStructure("ResetPasswordSuccess", {})
                else:
                    print "Failed to delete used token"
            else:
                print "Failed to update password"
        else:
            return commonResponseStructure("InvalidResetToken", {})
        


