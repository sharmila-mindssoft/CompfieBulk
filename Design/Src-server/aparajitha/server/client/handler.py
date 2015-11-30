import json

import tornado.ioloop
import tornado.web
from models import *
from controllers import *
from aparajitha.server.common import *
from aparajitha.server.databasehandler import DatabaseHandler

__all__ = [
    "initializeClientAdminHandler"
]

class ClientAdminAPIRequestHandler(tornado.web.RequestHandler) :
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
                userPrivilegeController = UserPrivilegeController()
                if request[0] == "GetUserPrivileges" :
                    response = userPrivilegeController.getUserPrivileges(userId)
                elif request[0] == "SaveUserPrivilege" :
                    response = userPrivilegeController.saveUserPrivilege(request[1], userId)
                elif request[0] == "UpdateUserPrivilege" :
                    response = userPrivilegeController.updateUserPrivilege(request[1], userId)
                elif request[0] == "ChangeUserPrivilegeStatus" :
                    response = userPrivilegeController.changeUserPrivilegeStatus(
                        request[1], userId)
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


def initializeClientAdminHandler() :
    admin_urls = [
        ("/ClientAdminAPI", ClientAdminAPIRequestHandler),
    ]
    return admin_urls
