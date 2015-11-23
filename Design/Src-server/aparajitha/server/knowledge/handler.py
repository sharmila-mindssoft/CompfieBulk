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
                response = PossibleError("InvalidSessionToken")
            else :
                if request[0] == "GetDomains" :
                    response = DomainList()
                elif request[0] == "SaveDomain" :
                    response = SaveDomain(request, userId)
                elif request[0] == "UpdateDomain" :
                    response = UpdateDomain(request, userId)
                elif request[0] == "ChangeDomainStatus" :
                    response = ChangeDomainStatus(request, userId)
                elif request[0] == "GetCountries" :
                    response = CountryList()
                elif request[0] == "SaveCountry" :
                    response = SaveCountry(request, userId)
                elif request[0] == "UpdateCountry" :
                    response = UpdateCountry(request, userId)
                elif request[0] == "ChangeCountryStatus" :
                    response = ChangeCountryStatus(request, userId)
                elif request[0] == "GetIndustries" :
                    response = IndustryList()
                elif request[0] == "SaveIndustry" :
                    response = SaveIndustry(request, userId)
                elif request[0] == "UpdateIndustry" :
                    response = UpdateIndustry(request, userId)
                elif request[0] == "ChangeIndustryStatus" :
                    response = ChangeIndustryStatus(request, userId)
                elif request[0] == "GetStatutoryNatures" :
                    response = StatutoryNatureList()
                elif request[0] == "SaveStatutoryNature" :
                    response = SaveStatutoryNature(request, userId)
                elif request[0] == "UpdateStatutoryNature" :
                    response = UpdateStatutoryNature(request, userId)
                elif request[0] == "ChangeStatutoryNatureStatus" :
                    response = ChangeStatutoryNatureStatus(request, userId)
                elif request[0] == "GetStatutoryLevels" :
                    response = StatutoryLevelsList()
                elif request[0] == "SaveStatutoryLevel" :
                    response = SaveStatutoryLevel(request, userId)
                elif request[0] == "GetGeographyLevels" :
                    response = GeographyLevelList()
                elif request[0] == "SaveGeographyLevel" :
                    response = SaveGeographyLevel(request, userId)
                else :
                    response = PossibleError("InvalidRequest")

        except Exception, e:
            print callerName, e
            self.send_error(400)
            return

        finally:
            self.set_header("Access-Control-Allow-Origin", "*")
            self.set_header("Access-Control-Allow-Headers", "Content-Type")
            self.set_header("Access-Control-Allow-Methods", "POST")
            self.write(json.dumps(response.toStructure(), indent=4))
            self.finish()

def initializeKnowledgeHandler() :
    knowledge_urls = [
        (r"/([a-zA-Z]+)", APIRequestHandler)
    ]
    return knowledge_urls
