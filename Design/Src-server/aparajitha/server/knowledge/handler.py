import json

import tornado.ioloop
import tornado.web
from models import *
from databasehandler import *


__all__ = [
    "initializeKnowledgeHandler"
]

class GetDomainHandler(tornado.web.RequestHandler) :
    def initialize(self, url, handler) :
        self.url = url
        self.handler = handler

    @tornado.web.asynchronous
    def post(self) :
        try:
            data = json.loads(self.request.body)
            sessionToken = JSONHelper.getString(data, "session_token")
            request = JSONHelper.getList(data, "request")
            response = DomainList(sessionToken, request)
        except Exception, e:
            print e
            self.send_error(400)
            return

        finally:            
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(str(response)))
            self.finish()

class SaveDomainHandler(tornado.web.RequestHandler) :
    def initialize(self, url, handler) :
        self.url = url
        self.handler = handler
    
    @tornado.web.asynchronous
    def post(self) :
        try:
            data = json.loads(self.request.body)
            sessionToken = JSONHelper.getString(data, "session_token")
            request = JSONHelper.getList(data, "request")
            response = SaveDomain(sessionToken, request)
        except Exception, e:
            print e
            self.send_error(400)
            return
        finally :
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(str(response)))
            self.finish()
        
class UpdateDomainHandler(tornado.web.RequestHandler) :
    def initialize(self, url, handler) :
        self.url = url
        self.handler = handler

    @tornado.web.asynchronous
    def post(self) :
        try:
            data = json.loads(self.request.body)
            sessionToken = JSONHelper.getString(data, "session_token")
            request = JSONHelper.getList(data, "request")
            response = UpdateDomain(sessionToken, request)

        except Exception, e:
            print e
            self.send_error(400)
            return
        finally:
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(str(response)))
            self.finish()

class ChangeDomainStatusHandler(tornado.web.RequestHandler) :
    def initialize(self, url, handler) :
        self.url = url
        self.handler = handler

    @tornado.web.asynchronous
    def post(self) :
        try:
            data = json.loads(self.request.body)
            sessionToken = JSONHelper.getString(data, "session_token")
            request = JSONHelper.getList(data, "request")
            response = ChangeDomainStatus(sessionToken, request)

        except Exception, e:
            print e
            self.send_error(400)
            return
        finally:
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(str(response)))
            self.finish()

def initializeKnowledgeHandler() :
    knowledge_urls = [
        ("/GetDomains", GetDomainHandler),
        ("/SaveDomain", SaveDomainHandler),
        ("/UpdateDomain", UpdateDomainHandler),
        ("/ChangeDomainStatus", ChangeDomainStatusHandler)

    ]
    return knowledge_urls
