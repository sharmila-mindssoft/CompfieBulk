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
                    response = DomainList().toStructure()
                elif request[0] == "SaveDomain" :
                    response = SaveDomain(request, userId).toStructure()
                elif request[0] == "UpdateDomain" :
                    response = UpdateDomain(request, userId).toStructure()
                elif request[0] == "ChangeDomainStatus" :
                    response = ChangeDomainStatus(request, userId).toStructure()
                elif request[0] == "GetCountries" :
                    response = CountryList().toStructure()
                elif request[0] == "SaveCountry" :
                    response = SaveCountry(request, userId).toStructure()
                elif request[0] == "UpdateCountry" :
                    response = UpdateCountry(request, userId).toStructure()
                elif request[0] == "ChangeCountryStatus" :
                    response = ChangeCountryStatus(request, userId).toStructure()
                elif request[0] == "GetIndustries" :
                    response = IndustryList().toStructure()
                elif request[0] == "SaveIndustry" :
                    response = SaveIndustry(request, userId).toStructure()
                elif request[0] == "UpdateIndustry" :
                    response = UpdateIndustry(request, userId).toStructure()
                elif request[0] == "ChangeIndustryStatus" :
                    response = ChangeIndustryStatus(request, userId).toStructure()
                elif request[0] == "GetStatutoryNatures" :
                    response = StatutoryNatureList().toStructure()
                elif request[0] == "SaveStatutoryNature" :
                    response = SaveStatutoryNature(request, userId).toStructure()
                elif request[0] == "UpdateStatutoryNature" :
                    response = UpdateStatutoryNature(request, userId).toStructure()
                elif request[0] == "ChangeStatutoryNatureStatus" :
                    response = ChangeStatutoryNatureStatus(request, userId).toStructure()
                elif request[0] == "GetStatutoryLevels" :
                    response = StatutoryLevelsList().toStructure()
                elif request[0] == "SaveStatutoryLevel" :
                    response = SaveStatutoryLevel(request, userId).toStructure()
                elif request[0] == "GetGeographyLevels" :
                    response = GeographyLevelList().toStructure()
                elif request[0] == "SaveGeographyLevel" :
                    response = SaveGeographyLevel(request, userId).toStructure()
                elif request[0] == "GetGeographies" :
                    response = GeographyAPI(request, userId).getGeographies()
                elif request[0] == "SaveGeography" :
                    response = GeographyAPI(request, userId).saveGeographies()
                elif request[0] == "UpdateGeography" :
                    response = GeographyAPI(request, userId).updateGeographies()
                elif request[0] == "ChangeGeographyStatus" :
                    response = GeographyAPI(request, userId).changeGeographyStatus()
                elif request[0] == "GeographyReport" :
                    response = GeographyAPI(request, userId).geographyReport()
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
            self.write(json.dumps(response, indent=4))
            self.finish()

def initializeKnowledgeHandler() :
    knowledge_urls = [
        (r"/([a-zA-Z]+)", APIRequestHandler)
    ]
    return knowledge_urls
