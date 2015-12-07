import os
import mimetypes
import jinja2
import tornado.web
from tornado.web import StaticFileHandler
import tornado.ioloop
from aparajitha.server.constants import ROOT_PATH, HTTP_PORT
from aparajitha.server.knowledgecontroller import KnowledgeController
from aparajitha.server.clientcontroller import ClientController
from user_agents import parse
from aparajitha.server import countries as countriesdb
import json
from collections import OrderedDict


#
# TemplateHandler
#

template_loader = jinja2.FileSystemLoader(
    os.path.join(ROOT_PATH, "Src-client")
)
template_env = jinja2.Environment(loader=template_loader)

class TemplateHandler(tornado.web.RequestHandler) :
    def initialize(self, path_desktop, path_mobile, parameters) :
        parameters = {"user":self.get_cookie("user"), "data":OrderedDict(sorted(countriesdb.countries.items(), key=lambda t: t[1])),}
        self.__path_desktop = path_desktop
        self.__path_mobile = path_mobile
        self.__parameters = parameters

    def get(self) :
        path = self.__path_desktop
        if self.__path_mobile is not None :
            user_agent = parse(self.request.headers["User-Agent"])
            if user_agent.is_mobile :
                path = self.__path_mobile
        mime_type, encoding = mimetypes.guess_type(path)
        self.set_header("Content-Type", mime_type)
        template = template_env.get_template(path)
        output = template.render(**self.__parameters)
        self.write(output)

    def options(self) :
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "GET, POST")
        self.set_status(204)
        self.write("")

class APIHandler(tornado.web.RequestHandler) :
    def initialize(self, handler) :
        self._handler = handler

    def post(self) :
        self._handler(self)

    def options(self) :
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "GET, POST")
        self.set_status(204)
        self.write("")


#
# run_server
#

TEMPLATE_PATHS = [
    # ("/", "files/desktop/index/index.html",
    #     "files/mobile/index/index.html", {}),
    ("/", "files/desktop/login/login.html",
        "files/mobile/login/login.html", {}),
    ("/login", "files/desktop/login/login.html",
        "files/mobile/login/login.html", {}),
    ("/test", "test_apis.html",
        "", {}),
    ("/home", "files/desktop/home/home.html", None, {}),
]

def run_server() :
    knowledge_controller = KnowledgeController()
    client_controller = ClientController()

    application_urls = []

    api_urls_and_handlers = [
        ("/api/login", knowledge_controller.handle_api_knowledge),
        ("/api/logout", knowledge_controller.handle_api_knowledge),
        ("/api/get-domains", knowledge_controller.handle_api_knowledge),
        ("/api/save-domain", knowledge_controller.handle_api_knowledge),
        ("/api/update-domain", knowledge_controller.handle_api_knowledge),
        ("/api/change-domain-status", knowledge_controller.handle_api_knowledge),
        ("/api/get-countries", knowledge_controller.handle_api_knowledge),
        ("/api/save-country", knowledge_controller.handle_api_knowledge),
        ("/api/update-country", knowledge_controller.handle_api_knowledge),
        ("/api/change-country-status", knowledge_controller.handle_api_knowledge),
        ("/api/get-industries", knowledge_controller.handle_api_knowledge),
        ("/api/save-industry", knowledge_controller.handle_api_knowledge),
        ("/api/update-industry", knowledge_controller.handle_api_knowledge),
        ("/api/change-industry-status", knowledge_controller.handle_api_knowledge),
        ("/api/get-statutory-natures", knowledge_controller.handle_api_knowledge),
        ("/api/save-statutory-nature", knowledge_controller.handle_api_knowledge),
        ("/api/update-statutory-nature", knowledge_controller.handle_api_knowledge),
        ("/api/change-statutory-nature-status", knowledge_controller.handle_api_knowledge),
        ("/api/get-statutory-levels", knowledge_controller.handle_api_knowledge),
        ("/api/save-statutory-level", knowledge_controller.handle_api_knowledge),
        ("/api/get-geography-levels", knowledge_controller.handle_api_knowledge),
        ("/api/save-geography-level", knowledge_controller.handle_api_knowledge),
        ("/api/get-geographies", knowledge_controller.handle_api_knowledge),
        ("/api/save-geography", knowledge_controller.handle_api_knowledge),
        ("/api/update-geography", knowledge_controller.handle_api_knowledge),
        ("/api/change-geography-status", knowledge_controller.handle_api_knowledge),
        ("/api/geography-report", knowledge_controller.handle_api_knowledge),
        ("/api/get-statutory-mappings", knowledge_controller.handle_api_knowledge),
        ("/api/save-statutory-mapping", knowledge_controller.handle_api_knowledge),
        ("/api/update-statutory-mapping", knowledge_controller.handle_api_knowledge),
        ("/api/change-statutory-mapping-status", knowledge_controller.handle_api_knowledge),
        ("/api/approve-statutory-mapping", knowledge_controller.handle_api_knowledge),
        ("/api/test-client", client_controller.handle_api_client),
        ("/api/client", client_controller.handle_api_client),
    ]
    for url, handler in api_urls_and_handlers :
        entry = (url, APIHandler, dict(handler=handler))
        application_urls.append(entry)

    for url, path_desktop, path_mobile, parameters in TEMPLATE_PATHS :
        args = {
            "path_desktop": path_desktop,
            "path_mobile": path_mobile,
            "parameters": parameters
        }
        entry = (url, TemplateHandler, args)
        application_urls.append(entry)

    static_path = os.path.join(ROOT_PATH, "Src-client")

    api_design_path = os.path.join(
        ROOT_PATH, "Doc", "API", "Web-API", "Version-1.0.4", "html")

    lower_level_handlers = [
        (r"/api-design/(.*)", tornado.web.StaticFileHandler, dict(path=api_design_path)),
        (r"/(.*)", tornado.web.StaticFileHandler, dict(path=static_path)),
    ]
    application_urls.extend(lower_level_handlers)

    print "Listening on port %s" % (HTTP_PORT,)
    application = tornado.web.Application(
        application_urls,
        gzip=True
    )
    application.listen(HTTP_PORT)
    try :
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt :
        print ""
        print "Ctrl-C received. Exiting."
