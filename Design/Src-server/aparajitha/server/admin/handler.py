import json

import tornado.ioloop
import tornado.web
from controllers import *
from aparajitha.server.common import JSONHelper
from aparajitha.server.databasehandler import DatabaseHandler

__all__ = [
    "initializeAdminHandler"
]

class AdminAPIRequestHandler(tornado.web.RequestHandler) :
    def initialize(self, url, handler) :
        self.url = url
        self.handler = handler

    @tornado.web.asynchronous
    def post(self) :
        try:
            data = json.loads(self.request.body)
            request = data
            # sessionToken = JSONHelper.getString(data, "session_token")
            # request = JSONHelper.getList(data, "request")
            response = None
            userId = 1#DatabaseHandler.instance().validateSessionToken(sessionToken)
            if userId is None :
                response = PossibleError("InvalidSessionToken")
            else :
                userGroup = UserGroup()
                user = User()
                changePassword = ChangePassword()
                forgotPassword = ForgotPassword()
                if request[0] == "GetUserGroups" :
                    response = userGroup.getUserGroups()
                elif request[0] == "login" :
                    responseData = {}
                    responseData["helos"] = "hi"
                    response = responseData
                elif request[0] == "SaveUserGroup" :
                    response = userGroup.saveUserGroup(request[1], userId)
                elif request[0] == "UpdateUserGroup" :
                    response = userGroup.updateUserGroup(request[1], userId)
                elif request[0] == "ChangeUserGroupStatus" :
                    response = userGroup.changeUserGroupStatus(request[1], userId)
                elif request[0] == "GetUsers" :
                    response = user.getUsers()
                elif request[0] == "SaveUser" :
                    response = user.saveUser(request[1], userId)
                elif request[0] == "UpdateUser" :
                    response = user.updateUser(request[1], userId)
                elif request[0] == "ChangeUserStatus" :
                    response = user.changeUserStatus(request[1], userId)
                elif request[0] == "ChangePassword" :
                    response = changePassword.changePassword(request[1], userId)
                elif request[0] == "ForgotPassword" :
                    response = forgotPassword.processRequest(request[1], self.request.uri)
                elif request[0] == "ResetTokenValidation" :
                    response = forgotPassword.validateResetToken(request[1], self.request.uri)
                elif request[0] == "ResetPassword" :
                    response = forgotPassword.resetPassword(request[1])
                else :
                    response = commonResponseStructure("InvalidRequest",{})

        except Exception, e:
            print e
            self.send_error(400)
            return

        finally:
            self.set_header("Access-Control-Allow-Origin", "*")
            self.set_header("Access-Control-Allow-Headers", "Content-Type")
            self.set_header("Access-Control-Allow-Methods", "POST")
            self.write(json.dumps(response))
            self.finish()


def initializeAdminHandler() :
    admin_urls = [
        ("/AdminAPI", AdminAPIRequestHandler),
        ("/AdminAPI/ForgotPassword", AdminAPIRequestHandler)
    ]
    return admin_urls
