import json

import tornado.ioloop
import tornado.web
from models import *
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
            sessionToken = JSONHelper.getString(data, "session_token")
            request = JSONHelper.getList(data, "request")
            response = None
            userId = DatabaseHandler.instance().validateSessionToken(sessionToken)
            if userId is None :
                response = PossibleError("InvalidSessionToken")
            else :
                userGroupController = UserGroupController()
                userController = UserController()
                changePassword = ChangePassword()
                forgotPassword = ForgotPassword()
                if request[0] == "GetUserGroups" :
                    response = userGroupController.getUserGroups()
                elif request[0] == "SaveUserGroup" :
                    response = userGroupController.saveUserGroup(request[1], userId)
                elif request[0] == "UpdateUserGroup" :
                    response = userGroupController.updateUserGroup(request[1], userId)
                elif request[0] == "ChangeUserGroupStatus" :
                    response = userGroupController.changeUserGroupStatus(request[1], userId)
                elif request[0] == "GetUsers" :
                    response = userController.getUsers()
                elif request[0] == "SaveUser" :
                    response = userController.saveUser(request[1], userId)
                elif request[0] == "UpdateUser" :
                    response = userController.updateUser(request[1], userId)
                elif request[0] == "ChangeUserStatus" :
                    response = userController.changeUserStatus(request[1], userId)
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
