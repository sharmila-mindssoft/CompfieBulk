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
                serviceProvider = ServiceProviderController()
                userPrivilege = UserPrivilegeController()
                user = UserController()
                unitClosure = UnitClosure()
                if request[0] == "GetUserPrivileges" :
                    response = userPrivilege.getUserPrivileges(userId)
                elif request[0] == "SaveUserPrivilege" :
                    response = userPrivilege.saveUserPrivilege(request[1], userId)
                elif request[0] == "UpdateUserPrivilege" :
                    response = userPrivilege.updateUserPrivilege(request[1], userId)
                elif request[0] == "ChangeUserPrivilegeStatus" :
                    response = userPrivilege.changeUserPrivilegeStatus(
                        request[1], userId)
                elif request[0] == "GetServiceProviders" :
                    response = serviceProvider.getServiceProviders( userId)
                elif request[0] == "SaveServiceProvider" :
                    response = serviceProvider.saveServiceProvider(request[1], userId)
                elif request[0] == "UpdateServiceProvider" :
                    response = serviceProvider.updateServiceProvider(request[1], userId)
                elif request[0] == "ChangeServiceProviderStatus" :
                    response = serviceProvider.changeServiceProviderStatus(
                        request[1], userId)
                elif request[0] == "GetClientUsers" :
                    response = user.getUsers( userId)
                elif request[0] == "SaveClientUser" :
                    response = user.saveUser(request[1], userId)
                elif request[0] == "UpdateClientUser" :
                    response = user.updateUser(request[1], userId)
                elif request[0] == "ChangeClientUserStatus" :
                    response = user.changeUserStatus(
                        request[1], userId)
                elif request[0] == "ChangeAdminStatus" :
                    response = user.changeAdminStatus(
                        request[1], userId)
                elif request[0] == "GetUnitClosureList" :
                    response = unitClosure.getList(userId)
                elif request[0] == "CloseUnit" :
                    response = unitClosure.closeUnit(request[1], userId)
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
