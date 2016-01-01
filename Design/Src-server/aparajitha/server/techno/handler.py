import json

import tornado.ioloop
import tornado.web
from controllers import *
from aparajitha.server.common import *
from aparajitha.server.databasehandler import DatabaseHandler 

__all__ = [
    "initializeTechnoHandler"
]

class TechnoAPIRequestHandler(tornado.web.RequestHandler) :
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
                clientGroup = ClientGroup()
                clientController = ClientController()
                clientProfile = ClientProfile()
                if request[0] == "SaveClientGroup" :
                    response = clientGroup.saveClientGroup(request[1], userId)
                elif request[0] == "GetClientGroups" :
                    response = clientGroup.getClientGroups()
                elif request[0] == "ChangeClientGroupStatus" :
                    response = clientGroup.changeClientGroupStatus(
                        request[1], userId)
                elif request[0] == "UpdateClientGroup" :
                    response = clientGroup.updateClientGroup(request[1], userId)
                elif request[0] == "GetClients" :
                    response = clientController.getClients(userId)
                elif request[0] == "SaveClient" :
                    response = clientController.saveClient(request[1], userId)
                elif request[0] == "UpdateClient" :
                    response = clientController.saveClient(request[1], userId, )
                elif request[0] == "ChangeClientStatus" :
                    response = clientController.changeClientStatus(request[1], userId)
                elif request[0] == "ReactivateUnit" :
                    response = clientController.reactivateUnit(request[1], userId)
                elif request[0] == "GetClientProfile" :
                    response = clientProfile.getClientProfile(userId)
                elif request[0] == "GetClientDetailsReportFilters" :
                    response = clientProfile.getClientDetailsReportFilters(userId)
                elif request[0] == "GetClientDetailsReport" :
                    response = clientProfile.getClientDetailsReport(request[1], userId)
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


def initializeTechnoHandler() :
    techno_urls = [
        ("/TechnoAPI", TechnoAPIRequestHandler)
    ]
    return techno_urls
