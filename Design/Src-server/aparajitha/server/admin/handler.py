import json

import tornado.ioloop
import tornado.web

from databasehandler import DatabaseHandler
from models import UserGroup

__all__ = [
    "initializeAdminHandler"
]

def commonResultStructure(responseType) :
    response = [
        responseType,
        {}
    ]
    return json.dumps(response)

def convertToString(unicode_str):
    return unicode_str.encode('utf-8')

class UserGroupsHandler(tornado.web.RequestHandler) :
    def initialize(self, url, handler) :
        self.url = url
        self.handler = handler

    def getUserGroups(self) :
        userGroupList = []
        columns = "user_group_id, user_group_name,form_type, "+\
                    "form_ids, is_active "
        rows = DatabaseHandler.instance().getData(UserGroup.tblUserGroup, columns)

        for row in rows:
            userGroup = UserGroup(int(row[0]), row[1], row[2], row[3], row[4])
            userGroupList.append(userGroup.toStructure())
        print userGroupList
        return userGroupList

    def saveUserGroup(self, request_data) :
        userGroupName = convertToString(request_data.get("user_group_name"))
        formType = convertToString(request_data.get("form_type"))
        formIds =  request_data.get("form_ids")
        userGroup = UserGroup(None, userGroupName, formType, formIds, None)
        if userGroup.isDuplicate() :
            return commonResultStructure("GroupNameAlreadyExists")
        elif userGroup.save() :
            return commonResultStructure("SaveUserGroupSuccess")
        else:
            return commonResultStructure("Error")

    def updateUserGroup(self) :
        return commonResultStructure("InsideUpdateUsergroup")

    def changeUserGroupStatus(self) :
        return commonResultStructure("InsideChangeUsergroupStatus")

    @tornado.web.asynchronous
    def post(self) :
        print "Entering into UserGroupsHandler post method"
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
                data = self.updateUserGroup()
            elif request[0] == "ChangeUserGroupStatus" :
                data = self.changeUserGroupStatus()
            else :
                data = commonResultStructure("InvalidRequest")

        except Exception, e:
            print e
            self.send_error(400)
            return
        finally:            
            self.set_header("Content-Type", "application/json")
            self.write(data)
            self.finish()

def initializeAdminHandler() :
    admin_urls = [
        ("/UserGroups", UserGroupsHandler),
    ]
    return admin_urls
