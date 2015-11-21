import json

import tornado.ioloop
import tornado.web
from models import *
from controllers import *
from aparajitha.server.common import JSONHelper
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
                if request[0] == "SaveClient" :
                    response = SaveClient(request[1], userId)
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
