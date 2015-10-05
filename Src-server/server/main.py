import os
import mimetypes
import json
import jinja2
import tornado.web
import tornado.ioloop

from tornado.web import StaticFileHandler
from user_agents import parse
from collections import OrderedDict

from server import countries as countriesdb
from server.common import WebServer
from server.common import IOLoop
from server.constants import ROOT_PATH, HTTP_PORT
from server.database import Database
from server.knowledgeteam.handler import KnowledgeteamHandler

CLIENT_PATH = os.path.join(ROOT_PATH, "Src-client")

TEMPLATE_URLS = [
    ("/login", "web/login/Login.html", None, {}),
    ("/home", "web/home/Home.html", None, {}),
    ("/index", "web/login/index.html", None, {}),
    ("/service_provider", "web/home/ServiceProviderHome.html", None, {}),
    ("/business_team", "web/home/BusinessTeamHome.html", None, {}),
    ("/it", "web/home/ITHome.html", None, {}),
    ("/it/user/home", "web/home/ITUserHome.html", None, {}),
    ("/knowledge", "web/home/KnowledgeHome.html",
        None, {}),
    ("/knowledge/user/home", "web/home/KnowledgeUserHome.html",
            None, {}),
    ("/techno", "web/home/TechnoHome.html",
        None, {}),
    ("/techno/user/home", "web/home/TechnoUserHome.html",
            None, {}),
    ("/inhouse/home", "web/home/InhouseHome.html",
            None, {}),
    ("/home", "web/home/Home.html",
        None, {}),
    ("/index", "web/login/index.html", None, {})
]


template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(CLIENT_PATH)
)

def templateHandler(request, response) :
    parameters = {"user":request.get_cookie("user"), "data":OrderedDict(sorted(countriesdb.countries.items(), key=lambda t: t[1])),}
    output = template_env.render()
    response.send(output)


def loginHandler(request, response):
    username = request.parameter("username")
    password = request.parameter("password")
    
    js = ""
    if(username == "serviceproviderManager@domain.com" and password == '0123456789'):
        js = '../service_provider'
    elif(username == "serviceproviderUser@domain.com" and password == '0123456789'):
        js = '../service_provider'
    elif(username == "business@domain.com" and password == '0123456789'):
        js = '../business_team'
    elif(username == "itManager@domain.com" and password == '0123456789'):
        js = '../it'
    elif(username == "itUser@domain.com" and password == '0123456789'):
        js = '../it/user/home'
    elif(username == "knowledgeManager@domain.com" and password == '0123456789'):
        js = '../knowledge'
    elif(username == "knowledgeUser@domain.com" and password == '0123456789'):
        js = '../knowledge/user/home'
    elif(username == "technoManager@domain.com" and password == '0123456789'):
        js = '../techno'
    elif(username == "technoUser@domain.com" and password == '0123456789'):
        js = '../techno/user/home'
    elif(username == "client@domain.com" and password == '0123456789'):
        js = '../inhouse/home'
    elif(username == "clientadmin@domain.com" and password == '0123456789'):
        js = '../home'
    else:
        js = '../index'
    response.set_cookie("user", username)
    response.set_header('Content-Type', 'application/json')
    json_ = tornado.escape.json_encode(js)
    response.send(json_)

# class APIHandler(tornado.web.RequestHandler):
#     def initialize(self, url, handler) :
#         self.url = url
#         self.handler = handler

#     def get(self) :
#         countries = {"IND": "India", "SGP": "Singapore", "MYS": "Malaysia", "USA": "United States", "CAN": "Canada"}
#         template = template_env.get_template("files/desktop/Test/test.html")
#         output = template.render()
#         self.write(output)


#
# run_server
#

# REQUEST_PATHS = [
#     ("/post/login", LoginHandler),
#     ("/login/(.*)", LoginHandler),
#     ("/test2", APIHandler),
# ] 
 
def run_server() :
    io_loop = IOLoop()
    web_server = WebServer(io_loop)
    db = Database()
    knowledgeteam_handler = KnowledgeteamHandler(io_loop, db, template_env, countriesdb.countries_by_name)
    knowledgeteam_handler.configure(web_server)
    
    STATIC_PATH = os.path.join(CLIENT_PATH, "static")

    for url, path_desktop, path_mobile, parameters in TEMPLATE_URLS :
        args = {
            "path_desktop": path_desktop,
            "path_mobile": path_mobile,
            "parameters": parameters
        }
        web_server.url(url, GET=templateHandler, POST=templateHandler)

    web_server.url("/login/(.*)", GET=loginHandler, POST=loginHandler)
    web_server.low_level_url(
        "/Static/(.*)", StaticFileHandler, dict(path=STATIC_PATH)
    )

    print "Listening on port %s" % (HTTP_PORT)
    web_server.start(HTTP_PORT)

    io_loop.run()