import json

import tornado.ioloop
import tornado.web
import uuid

from aparajitha.server.common import *
from aparajitha.server.knowledge.models import DomainList, CountryList
from aparajitha.server.databasehandler import DatabaseHandler

__all__ = [
    "UserGroup",
    "User",
    "ChangePassword",
    "ForgotPassword"
]

class UserGroup() :
    db = None
    userGroupId =  None
    userGroupName = None
    formCategoryId = None
    formIds = None
    isActive = 1

    def __init__(self) :
        self.db = DatabaseHandler.instance()

    def toDetailedStructure(self) :
        return {
            "user_group_id": self.userGroupId,
            "user_group_name": self.userGroupName,
            "form_category_id": self.formCategoryId,
            "form_ids": self.formIds,
            "is_active": self.isActive
        }

    def toStructure(self) :
        return {
            "user_group_id": self.userGroupId,
            "user_group_name": self.userGroupName,
            "is_active": self.isActive
        }

    def getForms(self) :
        form = Form()
    	resultRows = form.getForms()

        knowledgeForms = []
        technoForms = []

        for row in resultRows:
            if int(row[1]) == 2:
                form = Form(formId = row[0], formName = row[5], formUrl = row[6], formOrder = row[7], 
                    formType = row[4], Category = row[2], parentMenu = row[8])
                knowledgeForms.append(form)
            elif int(row[1]) == 3: 
                form = Form(formId = row[0], formName = row[5], formUrl = row[6], formOrder = row[7], 
                    formType = row[4], Category = row[2], parentMenu = row[8])
                technoForms.append(form)

        result = {}
        knowledgeMenu = Menu()
        technoMenu = Menu()
        result[2] = knowledgeMenu.generateMenu(knowledgeForms)
        result[3] = technoMenu.generateMenu(technoForms)

        return result

    def getUserGroupDetailedList(self):
        userGroupList = []
        rows = self.db.getUserGroupDetailedList()
        for row in rows:
            self.userGroupId = int(row[0])
            self.userGroupName = row[1]
            self.formCategoryId = row[2]
            self.formIds = [int(x) for x in row[3].split(",")]
            self.isActive = row[4]
            userGroupList.append(self.toDetailedStructure())
        return userGroupList

    def getUserGroupList(self):
        userGroupList = []
        rows = self.db.getUserGroupList()
        for row in rows:
            self.userGroupId = int(row[0])
            self.userGroupName = row[1]
            self.isActive = row[2]
            userGroupList.append(self.toStructure())
        return userGroupList

    def getUserGroups(self) :
    	forms = self.getForms()
    	userGroupList = self.getUserGroupDetailedList()
        formCategory =  FormCategory()
        formCategories = formCategory.getFormCategories()
        response_data = {}
        response_data["forms"] = forms
        response_data["user_groups"] = userGroupList
        response_data["form_categories"] = formCategories
        response = commonResponseStructure("GetUserGroupsSuccess", response_data)
        return response

    def isIdInvalid(self):
        condition = "user_group_id = '%d'" % self.userGroupId
        return not self.db.isAlreadyExists(self.db.tblUserGroups, condition)

    def generateNewUserGroupId(self) :
        return self.db.generateNewId(self.db.tblUserGroups, "user_group_id")

    def isDuplicate(self):
        condition = "user_group_name ='"+self.userGroupName+\
                "' AND user_group_id != '"+str(self.userGroupId)+"'"
        return self.db.isAlreadyExists(self.db.tblUserGroups, condition)

    def saveUserGroup(self, requestData, sessionUser) :
        self.userGroupName = JSONHelper.getString(requestData, "user_group_name")
        self.formCategoryId = JSONHelper.getInt(requestData, "form_category_id")
        self.formIds =  JSONHelper.getList(requestData, "form_ids")
        self.userGroupId = self.generateNewUserGroupId()
        if self.isDuplicate() :
            return commonResponseStructure("GroupNameAlreadyExists",{})
        elif self.db.saveUserGroup(self) :
            return commonResponseStructure("SaveUserGroupSuccess",{})
        else:
            return commonResponseStructure("Error",{})

    def updateUserGroup(self, requestData, sessionUser) :
        self.userGroupId = JSONHelper.getInt(requestData,"user_group_id")
        self.userGroupName = JSONHelper.getString(requestData,"user_group_name")
        self.formCategoryId = JSONHelper.getInt(requestData,"form_category_id")
        self.formIds =  JSONHelper.getList(requestData,"form_ids")
        if self.isIdInvalid() :
            return commonResponseStructure("InvalidGroupId",{})
        elif self.isDuplicate() :
            return commonResponseStructure("GroupNameAlreadyExists",{})
        elif self.db.updateUserGroup(self) :
            return commonResponseStructure("UpdateUserGroupSuccess",{})
        else:
            return commonResponseStructure("Error",{})

    def changeUserGroupStatus(self, requestData, sessionUser) :
        self.userGroupId = JSONHelper.getInt(requestData, "user_group_id")
        self.isActive = JSONHelper.getInt(requestData, "is_active")
        if self.isIdInvalid() :
            return commonResponseStructure("InvalidGroupId",{})
        elif self.db.updateUserGroupStatus(self.userGroupId, self.isActive):
            return commonResponseStructure("ChangeUserGroupStatusSuccess",{})


class User() :

    userId = None
    emailId = None
    userGroupId = None
    employeeName = None
    employeeCode = None
    contactNumber = None
    address = None
    designation = None
    countryIds = None
    domainIds = None
    isActive = 1

    def __init__(self):
        self.db = DatabaseHandler.instance()

    def toDetailedStructure(self) :
        return {
            "user_id": self.userId,
            "email_id": self.emailId,
            "user_group_id": self.userGroupId,
            "employee_name": self.employeeName,
            "employee_code": self.employeeCode,
            "contact_no": self.contactNo,
            "address": self.address, 
            "designation": self.designation,
            "country_ids": self.countryIds,
            "domain_ids": self.domainIds,
            "client_ids": self.clientIds,
            "is_active": self.isActive
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
            "is_active":self.isActive
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
        self.address =  JSONHelper.getString(requestData,"address")
        self.designation =  JSONHelper.getString(requestData,"designation")
        self.countryIds = JSONHelper.getList(requestData,"country_ids")
        self.domainIds = JSONHelper.getList(requestData,"domain_ids")
        if self.isDuplicateEmail() :
            return commonResponseStructure("EmailIDAlreadyExists",{})
        elif self.isDuplicateEmployeeCode() :
            return commonResponseStructure("EmployeeCodeAlreadyExists",{})
        elif self.isDuplicateContactNo() :
            return commonResponseStructure("ContactNumberAlreadyExists",{})
        elif self.db.saveUser(self) :
            return commonResponseStructure("SaveUserSuccess",{})
        else:
            return commonResponseStructure("Error",{})

    def updateUser(self, requestData, sessionUser) :
        self.userId = JSONHelper.getInt(requestData,"user_id")
        self.userGroupId = JSONHelper.getInt(requestData,"user_group_id")
        self.employeeName = JSONHelper.getString(requestData,"employee_name")
        self.employeeCode = JSONHelper.getString(requestData,"employee_code")
        self.contactNo = JSONHelper.getString(requestData,"contact_no")
        self.address =  JSONHelper.getString(requestData,"address")
        self.designation =  JSONHelper.getString(requestData,"designation")
        self.countryIds = JSONHelper.getList(requestData,"country_ids")
        self.domainIds = JSONHelper.getList(requestData,"domain_ids")
        if self.isIdInvalid() :
            return commonResponseStructure("InvalidUserId",{})
        elif self.isDuplicateEmployeeCode() :
            return commonResponseStructure("EmployeeCodeAlreadyExists",{})
        elif self.isDuplicateContactNo() :
            return commonResponseStructure("ContactNumberAlreadyExists",{})
        elif self.db.updateUser(self) :
            return commonResponseStructure("UpdateUserSuccess",{})
        else:
            return commonResponseStructure("Error",{})

    def changeUserStatus(self, requestData, sessionUser):
    	self.userId = JSONHelper.getInt(requestData, "user_id")
        self.isActive = JSONHelper.getInt(requestData, "is_active")
        if self.isIdInvalid() :
            return commonResponseStructure("InvalidUserId",{})
        elif self.db.updateUserStatus(self.userId, self.isActive):
            return commonResponseStructure("ChangeUserStatusSuccess",{})

    def getDetailedList(self):
        userList = []
        rows = self.db.getDetailedUserList()
        for row in rows:
            self.userId = row[0]
            self.emailId = row[1]
            self.userGroupId = row[2]
            self.employeeName = row[3]
            self.employeeCode = row[4]
            self.contactNo = row[5]
            self.address = row[6]
            self.designation = row[7]
            countryIds =  self.db.getUserCountries(self.userId)
            domainIds = self.db.getUserDomains(self.userId)
            clientIds = self.db.getUserClients(self.userId)
            self.countryIds = None if countryIds == None else [int(x) for x in countryIds.split(",")]
            self.domainIds = None if domainIds == None else [int(x) for x in domainIds.split(",")]
            self.clientIds = None if clientIds == None else [int(x) for x in clientIds.split(",")]
            self.isActive = row[8]
            userList.append(self.toDetailedStructure())
        return userList

    def getList(self):
        userList = []
        rows = self.db.getUserList()
        for row in rows:
            self.userId = int(row[0])
            self.employeeName = row[1]
            self.employeeCode = row[2]
            self.isActive = row[3]
            userList.append(self.toStructure())
        return userList


    def getUsers(self) :
    	domainList = DomainList.getDomainList()
        countryList = CountryList.getCountryList()
    	userGroupList = UserGroup().getUserGroupList()
    	userList = self.getDetailedList()

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
        


