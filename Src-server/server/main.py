import os
import json
import mimetypes
import tornado.web
from tornado.web import StaticFileHandler
from user_agents import parse
import jinja2
from basics.webserver import WebServer
from basics.ioloop import IOLoop
from protocol import (
    admin, clientadminsettings, clientmasters, clientreport,
    clienttransactions, clientuser, core, dashboard,
    general, knowledgemaster, knowledgereport, knowledgetransaction,
    login, technomasters, technoreports, technotransactions
)
from server.database import KnowledgeDatabase

import controller 
import MySQLdb as mysql

ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")

#
# cors_handler
#

def cors_handler(request, response):
    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Headers", "Content-Type")
    response.set_header("Access-Control-Allow-Methods", "POST")
    response.set_status(204)
    response.send("")


#
# api_request
#

def api_request(
    request_data_type
):
    def wrapper(f):
        def wrapped(self, request, response):
            self.handle_api_request(
                f, request, response,
                request_data_type
            )
        return wrapped
    return wrapper


#
# API
#

class API(object):
    def __init__(
        self, io_loop, db
    ):
        self._io_loop = io_loop
        self._db = db
    
    def _send_response(
        self, response_data, response
    ):
        assert response is not None
        data = response_data.to_structure()
        s = json.dumps(data, indent=2)
        print s
        response.send(s)

    def _parse_request(
        self, request_data_type, request, response
    ):
        request_data = None
        try:
            data = json.loads(request.body())
            request_data = request_data_type.parse_structure(
                data
            )
        except Exception, e:
            print e
            response.set_status(400)
            response.send(str(e))
            return None
        return request_data

    def handle_api_request(
        self, unbound_method, request, response,
        request_data_type
    ):
        response.set_default_header("Access-Control-Allow-Origin", "*")
        ip_address = unicode(request.remote_ip())
        request_data = self._parse_request(
            request_data_type, request, response
        )
        if request_data is None:
            return

        def respond(response_data):
            self._send_response(
                response_data, response
            )

        self._db.begin()
        try:
            response_data = unbound_method(self, request_data, self._db)
            self._db.commit()
            respond(response_data)
        except Exception, e:
            print e
            self._db.rollback()
        

    @api_request(login.Request)
    def handle_login(self, request, db):
        return controller.process_login_request(request, db)
        # return login.ResetPasswordSuccess()

    @api_request(admin.RequestFormat)
    def handle_admin(self, request, db):
        return controller.process_admin_request(request, db)

    @api_request(technomasters.RequestFormat)
    def handle_techno(self, request, db):
        print "inside handle techno requests"
        return controller.process_techno_request(request, db)

    @api_request(clientadminsettings.Request)
    def handle_client_admin_settings(self, request, db):
        pass
                         
    @api_request(general.RequestFormat)
    def handle_general(self, request, db):
        return controller.process_general_request(request, db)

    @api_request(knowledgemaster. RequestFormat)
    def handle_knowledge_master(self, request, db) :
        return controller.process_knowledge_master_request(request, db)


template_loader = jinja2.FileSystemLoader(
    os.path.join(ROOT_PATH, "Src-client")
)
template_env = jinja2.Environment(loader=template_loader)

class TemplateHandler(tornado.web.RequestHandler) :
    def initialize(self, path_desktop, path_mobile,     parameters) :
        # parameters = {"user":self.get_cookie("user"), "data":OrderedDict(sorted(countriesdb.countries.items(), key=lambda t: t[1])),}
        self.__path_desktop = path_desktop
        self.__path_mobile = path_mobile
        self.__parameters = parameters

    def get(self) :
        path = self.__path_desktop
        if self.__path_mobile is not None :
            useragent = self.request.headers.get("User-Agent")
            if useragent is None:
                useragent = ""
            user_agent = parse(useragent)
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

#
# run_server
#

TEMPLATE_PATHS = [
    ("/login", "files/desktop/login/login.html", "files/mobile/login/login.html", {}),
    ("/test", "test_apis.html", "", {}),
    ("/home", "files/desktop/home/home.html", None, {}),
    ("/custom-controls", "files/desktop/custom-controls/custom-controls.html", None, {}),
    ("/domain/create", "files/desktop/domain-master/domainmaster.html", None, {}),
    ("/domain/list", "files/desktop/domain-master/domainmasterlist.html", None, {}),
    ("/country/list", "files/desktop/CountryMaster/CountryMasterList.html", None, {}),
    ("/country/create", "files/desktop/CountryMaster/CountryMaster.html", None, {}),
    ("/industry/create", "files/desktop/Industry_Master/IndustryMaster.html", None, {}),
    ("/industry/list", "files/desktop/Industry_Master/IndustryMasterList.html", None, {}),
    ("/applicability/create", "files/desktop/Applicability_master/ApplicabilityMaster.html", None, {}),
    ("/applicability/list", "files/desktop/Applicability_master/ApplicabilityMasterList.html", None, {}),
    ("/geographylevel/create", "files/desktop/GeographyLevel/GeographyLevelMaster.html", None, {}),
    ("/geographylevel/list", "files/desktop/GeographyLevel/GeographyLevelList.html", None, {}),
    ("/geographymapping", "files/desktop/GeographyMaster/GeographyMapping.html", None, {}),
    ("/geographymapping/list", "files/desktop/GeographyMaster/GeographyMappingList.html", None, {}),
    ("/statutorylevel/list", "files/desktop/StatutoryLevelMaster/StatutoryLevelMasterList.html", None, {}),
    ("/statutorylevel/create", "files/desktop/StatutoryLevelMaster/StatutoryLevelMaster.html", None, {}),
    ("/statutorymapping", "files/desktop/StatutoryMapping/StatutoryMapping.html", None, {}),
    ("/statutorymapping/list", "files/desktop/StatutoryMapping/StatutoryMappingList.html", None, {}),

]


def handle_root(request, response):
    # response.send("Are you lost?")
    template = template_env.get_template("/")
    output = template.render(**self.__parameters)
    self.write(output)

def run_server(port):
    io_loop = IOLoop()

    def delay_initialize():
        db = KnowledgeDatabase(
            "localhost", "root", "123456", "mirror_knowledge"
        )
        web_server = WebServer(io_loop)

        web_server.url("/", GET=handle_root)

        for url, path_desktop, path_mobile, parameters in TEMPLATE_PATHS :
            args = {
                "path_desktop": path_desktop,
                "path_mobile": path_mobile,
                "parameters": parameters
            }
            web_server.low_level_url(url, TemplateHandler, args)

        api = API(io_loop, db)

        api_urls_and_handlers = [
            ("/api/login", api.handle_login),
            ("/api/admin", api.handle_admin),
            ("/api/techno", api.handle_techno),
            (
                "/api/handle_client_admin_settings",
                api.handle_client_admin_settings
            ),
            ("/api/general", api.handle_general),
            ("/api/knowledge_master", api.handle_knowledge_master),
        ]
        for url, handler in api_urls_and_handlers:
            web_server.url(url, POST=handler, OPTIONS=cors_handler)

        static_path = os.path.join(ROOT_PATH, "Src-client")
        files_path = os.path.join(static_path, "files")
        desktop_path = os.path.join(files_path, "desktop")
        common_path = os.path.join(desktop_path, "common")
        images_path = os.path.join(common_path, "images")
        css_path = os.path.join(common_path, "css")
        js_path = os.path.join(common_path, "js")

        web_server.low_level_url(r"/images/(.*)", tornado.web.StaticFileHandler, dict(path=images_path))
        
        api_design_path = os.path.join(ROOT_PATH, "Doc", "API", "Web-API", "Version-1.0.4", "html")
        web_server.low_level_url(r"/api-design/(.*)", tornado.web.StaticFileHandler, dict(path=api_design_path))
        web_server.low_level_url(r"/(.*)", tornado.web.StaticFileHandler, dict(path=static_path))


        print "Local port: %s" % port
        web_server.start(port, backlog=1000)

    io_loop.add_callback(delay_initialize)
    io_loop.run()


