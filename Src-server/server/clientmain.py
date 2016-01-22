import os
import json
import traceback
import mimetypes
import tornado.web
from tornado.web import StaticFileHandler
from user_agents import parse
import jinja2
from basics.webserver import WebServer
from basics.ioloop import IOLoop
from protocol import (
    clientadminsettings, clientmasters, clientreport,
    clienttransactions, clientuser, core, dashboard,
    login
)
from server.clientdatabase import ClientDatabase
from server.database import KnowledgeDatabase

import clientcontroller as controller 
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

        # self._db.begin()
        try:
            response_data = unbound_method(self, request_data, self._db)
            # self._db.commit() 
            respond(response_data)
        except Exception, e:
            print(traceback.format_exc())
            print e
            # self._db.rollback()


    @api_request(login.Request)
    def handle_login(self, request, db):
        return controller.process_login_request(request, db)

    @api_request(clientmasters.RequestFormat)
    def handle_client_masters(self, request, db):
        return controller.process_client_master_requests(request, db)

    @api_request(clienttransactions.RequestFormat)
    def handle_client_transaction(self, request, db):
        return controller.process_client_transaction_requests(request, db)

    @api_request(clientreport.RequestFormat)
    def handle_client_reports(self, request, db):
        return controller.process_client_report_requests(request, db)

    @api_request(dashboard.RequestFormat)
    def handle_client_dashboard(self, request, db):
        return controller.process_client_dashboard_requests(request, db)

template_loader = jinja2.FileSystemLoader(
    os.path.join(ROOT_PATH, "Src-client")
)
template_env = jinja2.Environment(loader=template_loader)

class TemplateHandler(tornado.web.RequestHandler) :
    def initialize(self, path_desktop, path_mobile, parameters) :
        self.__path_desktop = path_desktop
        self.__path_mobile = path_mobile
        self.__parameters = parameters

    def get(self, url = None) :
        if url != None:
            db = KnowledgeDatabase( "198.143.141.73", "root", "Root!@#123",  "mirror_knowledge")
            con = db.begin()
            if not db.validate_short_name(url):
                print "Invalid URL"
                return
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
    (r"/login/([a-zA-Z-0-9]+)", "files/desktop/login/login.html", "files/mobile/login/login.html", {}),
    (r"/forgot_password/([a-zA-Z-0-9]+)", "files/desktop/ForgotPassword/ForgotPassword.html", "", {}),
    (r"/reset_password/([a-zA-Z-0-9]+)", "files/desktop/ForgotPassword/resetpassword.html", "", {}),
    ("/change-password", "files/desktop/change-password/changepassword.html", None, {}),
    ("/test", "test_apis.html", "", {}),
    ("/home", "files/desktop/home/home.html", None, {}),
     #client admin
    ("/service-provider", "files/desktop/client/service-provider/serviceprovider.html", None, {}),   
    ("/client-user-privilege", "files/desktop/client/client-user-privilege/clientuserprivilege.html", None, {}),  
    ("/client-user-master", "files/desktop/client/client-user-master/clientusermaster.html", None, {}),  
    ("/unit-closure", "files/desktop/client/unit-closure/unitclosure.html", None, {}), 
    #reports
    ("/compliance", "files/desktop/client/audit-trail/audittrail.html", None, {}),
    ("/audit-trail", "files/desktop/client/audit-trail/audittrail.html", None, {}),       

]


def handle_root(request, response):
    # response.send("Are you lost?")
    template = template_env.get_template("/")
    output = template.render(**self.__parameters)
    self.write(output)

def run_server(port):
    io_loop = IOLoop()

    def delay_initialize():
        db = ClientDatabase()
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
            ("/api/client_masters", api.handle_client_masters),
            ("/api/client_transaction", api.handle_client_transaction),
            ("/api/client_reports", api.handle_client_reports),
            ("/api/client_dashboard", api.handle_client_dashboard)
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


