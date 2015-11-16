import json

import tornado.ioloop
import tornado.web
from models import *
from databasehandler import DatabaseHandler


__all__ = [
    "initializeKnowledgeHandler"
]

class APIRequestHandler(tornado.web.RequestHandler) :
    def initialize(self, url, handler) :
        self.url = url
        self.handler = handler

    @tornado.web.asynchronous
    def post(self, callerName) :
        try:
            data = json.loads(self.request.body)
            sessionToken = JSONHelper.getString(data, "session_token")
            request = JSONHelper.getList(data, "request")
            response = None
            userId = DatabaseHandler.instance().validateSessionToken(sessionToken)
            if userId is None :
                response = "InvalidSessionToken"
            else :
                if request[0] == "GetDomains" :
                    response = DomainList(request)
                elif request[0] == "SaveDomain" :
                    response = SaveDomain(request, userId)
                elif request[0] == "UpdateDomain" :
                    response = UpdateDomain(request, userId)
                elif request[0] == "ChangeDomainStatus" :
                    response = ChangeDomainStatus(request, userId)
                elif request[0] == "GetCountries" :
                    response = CountryList(request)
                elif request[0] == "SaveCountry" :
                    response = SaveCountry(request, userId)
                elif request[0] == "UpdateCountry" :
                    response = UpdateCountry(request, userId)
                elif request[0] == "ChangeCountryStatus" :
                    response = ChangeCountryStatus(request, userId)
                elif request[0] == "GetIndustries" :
                    response = IndustryList(request)
                elif request[0] == "SaveIndustry" :
                    response = SaveIndustry(request, userId)
                elif request[0] == "UpdateIndustry" :
                    response = UpdateIndustry(request, userId)
                elif request[0] == "ChangeIndustryStatus" :
                    response = ChangeIndustryStatus(request, userId)
                elif request[0] == "GetStatutoryNatures" :
                    response = StatutoryNatureList(request)
                elif request[0] == "SaveStatutoryNature" :
                    response = SaveStatutoryNature(request, userId)
                elif request[0] == "UpdateStatutoryNature" :
                    response = UpdateStatutoryNature(request, userId)
                elif request[0] == "ChangeStatutoryNatureStatus" :
                    response = ChangeStatutoryNatureStatus(request, userId)
                else :
                    response = "InvalidRequest"

        except Exception, e:
            print callerName, e
            self.send_error(400)
            return

        finally:
            self.set_header("Access-Control-Allow-Origin", "*")
            self.set_header("Access-Control-Allow-Headers", "Content-Type")
            self.set_header("Access-Control-Allow-Methods", "POST")
            self.write(json.dumps(str(response)))
            self.finish()

def initializeKnowledgeHandler() :
    knowledge_urls = [
        (r"/([a-zA-Z]+)", APIRequestHandler)
    ]
    return knowledge_urls
