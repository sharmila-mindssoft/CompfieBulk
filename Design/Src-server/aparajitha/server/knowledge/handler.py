import json

import tornado.ioloop
import tornado.web

from databasehandler import *

__all__ = [
    "initializeKnowledgeHandler"
]

def commonResultStructure(responseType) :
    return [
        responseType,
        {}
    ]

class GetDomainHandler(tornado.web.RequestHandler) :
    def initialize(self, url, handler) :
        self.url = url
        self.handler = handler

    def toStructure(self, domainList) :
        response = [
            "success",
            { "domains" : str(domainList) }
        ]
        return json.dumps(response)

    @tornado.web.asynchronous
    def post(self) :
        try:
            data = json.loads(self.request.body)
            sessionToken = data.get("session_token")
            userId = 1
            request = data.get("request")
            if userId is None :
                data = commonResultStructure("InvalidSessionToken")
            elif request[0] != "GetDomains" :
                data = commonResultStructure("InvalidRequest")
            else :
                domainList = DatabaseHandler.instance().getDomains()
                data = self.toStructure(domainList)

        except Exception, e:
            print e
            self.send_error(400)
            return
        finally:            
            self.set_header("Content-Type", "application/json")
            self.write(data)
            self.finish()

class SaveDomainHandler(tornado.web.RequestHandler) :
    def initialize(self, url, handler) :
        self.url = url
        self.handler = handler
    
    @tornado.web.asynchronous
    def post(self) :
        try:
            data = json.loads(self.request.body)
            sessionToken = data.get("session_token")
            request = data.get("request")
            userId = 1
            if userId is None :
                data = commonResultStructure("InvalidSessionToken")
            elif request[0] != "SaveDomain" :
                data = commonResultStructure("InvalidRequest")
            else :
                requestData = request[1]
                #asserttype
                domainName = requestData.get("domain_name")
                isDuplicate = DatabaseHandler.instance().checkDuplicateDomain(domainName, None)
                if isDuplicate :
                    data = commonResultStructure("DomainNameAlreadyExists")
                else :
                    if DatabaseHandler.instance().saveDomain(domainName, userId) :
                        data = commonResultStructure("success")
                    else :
                        data = commonResultStructure("SaveFailed")
        except Exception, e:
            print e
            self.send_error(400)
            return
        finally :
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(data))
            self.finish()
        
class UpdateDomainHandler(tornado.web.RequestHandler) :
    def initialize(self, url, handler) :
        self.url = url
        self.handler = handler

    @tornado.web.asynchronous
    def post(self) :
        try:
            data = json.loads(self.request.body)
            sessionToken = data.get("session_token")
            request = data.get("request")
            userId = 1
            if userId is None :
                data = commonResultStructure("InvalidSessionToken")
            elif request[0] != "UpdateDomain" :
                data = commonResultStructure("InvalidRequest")
            else :
                requestData = request[1]
                #asserttype
                domainName = requestData.get("domain_name")
                domainId = requestData.get("domain_id")
                isDuplicate = DatabaseHandler.instance().checkDuplicateDomain(domainName, domainId)
                if isDuplicate :
                    data = commonResultStructure("DomainNameAlreadyExists")
                else :
                    if DatabaseHandler.instance().updateDomain(domainId, domainName, userId) :
                        data = commonResultStructure("success")
                    else :
                        data = commonResultStructure("InvalidDomainId")

        except Exception, e:
            print e
            self.send_error(400)
            return
        finally:
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(data))
            self.finish()

class ChangeDomainStatusHandler(tornado.web.RequestHandler) :
    def initialize(self, url, handler) :
        self.url = url
        self.handler = handler

    @tornado.web.asynchronous
    def post(self) :
        try:
            data = json.loads(self.request.body)
            sessionToken = data.get("session_token")
            request = data.get("request")
            userId = 1
            if userId is None :
                data = commonResultStructure("InvalidSessionToken")
            elif request[0] != "ChangeDomainStatus" :
                data = commonResultStructure("InvalidRequest")
            else :
                requestData = request[1]
                #asserttype
                domainId = requestData.get("domain_id")
                isActive = requestData.get("is_active")
                if DatabaseHandler.instance().updateDomainStatus(domainId, isActive, userId) :
                    data = commonResultStructure("success")
                else :
                    data = commonResultStructure("InvalidDomainId")
        except Exception, e:
            raise e
        finally:
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(data))
            self.finish()

def initializeKnowledgeHandler() :
    knowledge_urls = [
        ("/GetDomains", GetDomainHandler),
        ("/SaveDomain", SaveDomainHandler),
        ("/UpdateDomain", UpdateDomainHandler),
        ("/ChangeDomainStatus", ChangeDomainStatusHandler)

    ]
    return knowledge_urls
