import json

import tornado.ioloop
import tornado.web

from databasehandler import DatabaseHandler
from models import *
from aparajitha.server.common import *

__all__ = [
    "initializeAdminHandler"
]

def commonResultStructure(responseType) :
    response = [
        responseType,
        {}
    ]
    return json.dumps(response)

class UserGroupsHandler(tornado.web.RequestHandler) :
    def initialize(self, url, handler) :
        self.url = url
        self.handler = handler

    @tornado.web.asynchronous
    def post(self) :
        try:
            data = json.loads(self.request.body)
            sessionToken = data.get("session_token")
            userId = 1
            request = data.get("request")
            if userId is None :
                data = commonResultStructure("InvalidSessionToken")
            elif request[0] == "GetUserGroups" :
                data = self.getUserGroups()
            elif request[0] == "SaveUserGroup" :
                data = self.saveUserGroup(request[1])
            elif request[0] == "UpdateUserGroup" :
                data = self.updateUserGroup(request[1])
            elif request[0] == "ChangeUserGroupStatus" :
                data = self.changeUserGroupStatus(request[1])
            else :
                data = commonResultStructure("InvalidRequest")

        except Exception, e:
            print e
            self.send_error(400)
            return
        finally:       
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(str(data)))
            self.finish()

    def getUserGroupsFormData(self) :
        knowledgeForms = []
        technoForms = []

        columns = "form_id, form_name, form_url, form_order, form_type,"+\
                 "category, admin_form, parent_menu"
        rows = DatabaseHandler.instance().getData(Form.tblName, columns, " form_type = 'knowledge' "+\
            " or form_type='techno'")
        for row in rows:
            form = Form(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            if form.formType == "Knowledge":
                knowledgeForms.append(form)
            else:
                technoForms.append(form)

        result = {}
        result["knowledge"] = getMenu(knowledgeForms)
        result["techno"] = getMenu(technoForms)

        return result


    def getUserGroups(self) :
        userGroupList = []

        columns = "user_group_id, user_group_name,form_type, "+\
                    "form_ids, is_active"
        rows = DatabaseHandler.instance().getData(UserGroup.tblName, columns, "1")

        for row in rows:
            userGroup = UserGroup(int(row[0]), row[1], row[2], row[3].split(","), row[4])
            userGroupList.append(userGroup.toStructure())

        response_data = {}
        forms = self.getUserGroupsFormData()
        response_data["forms"] = forms
        response_data["user_groups"] = userGroupList

        response = []
        response.append("GetUserGroupsSuccess")
        response.append(response_data)

        return response

    def saveUserGroup(self, request_data) :
        json = JsonParser(request_data)
        userGroupName = json.getString("user_group_name")
        formType = json.getString("form_type")
        formIds =  json.getData("form_ids")
        userGroup = UserGroup(None, userGroupName, formType, formIds, None)
        if userGroup.isDuplicate() :
            return commonResultStructure("GroupNameAlreadyExists")
        elif userGroup.save() :
            return commonResultStructure("SaveUserGroupSuccess")
        else:
            return commonResultStructure("Error")

    def updateUserGroup(self, request_data) :
        json = JsonParser(request_data)
        userGroupId = json.getInt("user_group_id")
        userGroupName = json.getString("user_group_name")
        formType = json.getString("form_type")
        formIds =  json.getData("form_ids")
        userGroup = UserGroup(userGroupId, userGroupName, formType, formIds, None)
        if userGroup.isIdInvalid() :
            return commonResultStructure("InvalidGroupId")
        elif userGroup.isDuplicate() :
            return commonResultStructure("GroupNameAlreadyExists")
        elif userGroup.update() :
            return commonResultStructure("UpdateUserGroupSuccess")
        else:
            return commonResultStructure("Error")

    def changeUserGroupStatus(self, request_data) :
        json = JsonParser(request_data)
        userGroupId = json.getInt("user_group_id")
        isActive = json.getInt("is_active")
        userGroup = UserGroup(userGroupId, None, None, None, isActive)
        if userGroup.isIdInvalid() :
            return commonResultStructure("InvalidGroupId")
        elif userGroup.updateStatus():
            return commonResultStructure("ChangeUserGroupStatusSuccess")

class UserHandler(tornado.web.RequestHandler) :
    def initialize(self, url, handler) :
        self.url = url
        self.handler = handler

    @tornado.web.asynchronous
    def post(self) :
        try:
            data = json.loads(self.request.body)
            sessionToken = data.get("session_token")
            userId = 1
            request = data.get("request")
            if userId is None :
                data = commonResultStructure("InvalidSessionToken")
            elif request[0] == "GetUsers" :
                data = self.getUsers()
            elif request[0] == "SaveUser" :
                data = self.saveUser(request[1])
            elif request[0] == "UpdateUser" :
                data = self.updateUser(request[1])
            elif request[0] == "ChangeUserStatus" :
                data = self.changeUserStatus(request[1])
            else :
                data = commonResultStructure("InvalidRequest")

        except Exception, e:
            print e
            self.send_error(400)
            return
        finally:       
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(str(data)))
            self.finish()

    def saveUser(self, request_data) :
        json = JsonParser(request_data)
        emailId = json.getString("email_id")
        userGroupId = json.getInt("user_group_id")
        employeeName = json.getString("employee_name")
        employeeCode = json.getString("employee_code")
        contactNo = json.getString("contact_no")
        address =  json.getString("address")
        designation =  json.getString("designation")
        domainIds = json.getData("domain_ids")
        user = User(None, emailId, userGroupId, employeeName, employeeCode, 
                    contactNo, address, designation, domainIds, None)
        if user.isDuplicateEmail() :
            return commonResultStructure("EmailIDAlreadyExists")
        elif user.isDuplicateEmployeeCode() :
            return commonResultStructure("EmployeeCodeAlreadyExists")
        elif user.isDuplicateContactNo() :
            return commonResultStructure("ContactNumberAlreadyExists")
        elif user.save() :
            return commonResultStructure("SaveUserSuccess")
        else:
            return commonResultStructure("Error")

    def updateUser(self, request_data) :
        json = JsonParser(request_data)
        userId = json.getInt("user_id")
        emailId = json.getString("email_id")
        userGroupId = json.getInt("user_group_id")
        employeeName = json.getString("employee_name")
        employeeCode = json.getString("employee_code")
        contactNo = json.getString("contact_no")
        address =  json.getString("address")
        designation =  json.getString("designation")
        domainIds = json.getData("domain_ids")
        user = User(userId, emailId, userGroupId, employeeName, employeeCode, 
                    contactNo, address, designation, domainIds, None)
        if user.isIdInvalid() :
            return commonResultStructure("InvalidUserId")
        elif user.isDuplicateEmail() :
            return commonResultStructure("EmailIDAlreadyExists")
        elif user.isDuplicateEmployeeCode() :
            return commonResultStructure("EmployeeCodeAlreadyExists")
        elif user.isDuplicateContactNo() :
            return commonResultStructure("ContactNumberAlreadyExists")
        elif user.update() :
            return commonResultStructure("UpdateUserSuccess")
        else:
            return commonResultStructure("Error")

def initializeAdminHandler() :
    admin_urls = [
        ("/UserGroups", UserGroupsHandler),
        ("/AdminUsers", UserHandler),
    ]
    return admin_urls
