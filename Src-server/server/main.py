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
            print(traceback.format_exc())
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
        # return login.ResetPasswordSuccess()

    @api_request(admin.RequestFormat)
    def handle_admin(self, request, db):
        return controller.process_admin_request(request, db)

    @api_request(technomasters.RequestFormat)
    def handle_techno(self, request, db):
        return controller.process_techno_request(request, db)

    @api_request(clientadminsettings.Request)
    def handle_client_admin_settings(self, request, db):
        pass
                         
    @api_request(general.RequestFormat)
    def handle_general(self, request, db):
        return controller.process_general_request(request, db)

    @api_request(knowledgemaster.RequestFormat)
    def handle_knowledge_master(self, request, db) :
        return controller.process_knowledge_master_request(request, db)

    @api_request(knowledgetransaction.RequestFormat)
    def handle_knowledge_transaction(self, request, db) :
        return controller.process_knowledge_transaction_request(request, db)

    @api_request(knowledgereport.RequestFormat)
    def handle_knowledge_report(self, request, db) :
        return controller.process_knowledge_report_request(request, db)

    @api_request(technotransactions.RequestFormat)
    def handle_techno_transaction(self, request, db):
        return controller.process_techno_transaction_request(request, db)

    @api_request(technoreports.RequestFormat)
    def handle_techno_report(self, request, db):
        return controller.process_techno_report_request(request, db)

template_loader = jinja2.FileSystemLoader(
    os.path.join(ROOT_PATH, "Src-client")
)
template_env = jinja2.Environment(loader=template_loader)

class TemplateHandler(tornado.web.RequestHandler) :
    def initialize(self, path_desktop, path_mobile,     parameters) :
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
    #common
    ("/profile", "files/desktop/profile/profile.html", None, {}),
    ("/change-password", "files/desktop/change-password/changepassword.html", None, {}),
    #IT Admin Master
    ("/domain-master", "files/desktop/domain-master/domainmaster.html", None, {}),
    ("/country-master", "files/desktop/country-master/countrymaster.html", None, {}),
    ("/user-group-master", "files/desktop/user-group-master/usergroupmaster.html", None, {}),
    ("/user-master", "files/desktop/user-master/usermaster.html", None, {}),    
    #knowledge manager transaction
    ("/approve-statutory-mapping", "files/desktop/approve-statutory-mapping/approvestatutorymapping.html", None, {}),
    #knowledge user master
    ("/geography-master", "files/desktop/geography-master/geographymaster.html", None, {}),
    ("/geography-level-master", "files/desktop/geography-level-master/geographylevelmaster.html", None, {}),
    ("/industry-master", "files/desktop/industry-master/industrymaster.html", None, {}),   
    ("/statutory-nature-master", "files/desktop/statutory-nature-master/statutorynaturemaster.html", None, {}),
    ("/statutory-level-master", "files/desktop/statutory-level-master/statutorylevelmaster.html", None, {}),
    #knowledge user Transaction
    ("/statutory-mapping", "files/desktop/statutory-mapping/statutorymapping.html", None, {}),    
    #knowledge Reports
    ("/statutory-mapping-report", "files/desktop/statutory-mapping-report/statutorymappingreport.html", None, {}),
    ("/country-report", "files/desktop/knowledge-master-report/country-master-report/countrymasterreport.html", None, {}),
    ("/domain-report", "files/desktop/knowledge-master-report/domain-master-report/domainmasterreport.html", None, {}),
    ("/geography-report", "files/desktop/knowledge-master-report/geography-master-report/geographymasterreport.html", None, {}),
    ("/industry-report", "files/desktop/knowledge-master-report/industry-master-report/industrymasterreport.html", None, {}),
    ("/statutory-nature-report", "files/desktop/knowledge-master-report/statutory-nature-master-report/statutorynaturemasterreport.html", None, {}),
    #Techno Manager master
    ("/client-master", "files/desktop/client-master/clientmaster.html", None, {}),
    #Techno user master
    ("/client-unit", "files/desktop/client-unit/clientunit.html", None, {}),
    ("/unit-closure", "files/desktop/unit-closure/unitclosure.html", None, {}), 
    ("/client-profile", "files/desktop/client-profile/clientprofile.html", None, {}),
    #Techno User Transaction
    ("/assign-statutory", "files/desktop/assign-statutory/assignstatutory.html", None, {}),
    #Techno reports
    ("/client-details-report", "files/desktop/client-details-report/clientdetailsreport.html", None, {}),
    ("/assigned-statutory-report", "files/desktop/assigned-statutory-report/assignedstatutoryreport.html", None, {}),
    ("/compliance-task-list", "files/desktop/compliance-task-list/compliancetasklist.html", None, {}),
    #audit trial
    ("/audit-trail", "files/desktop/audit-trail/audittrail.html", None, {}),
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
            "198.143.141.73", "root", "Root!@#123", "mirror_knowledge"
        )
        # db = KnowledgeDatabase(
        #     "localhost", "root", "123456", "mirror_knowledge"
        # )
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
            ("/api/knowledge_transaction", api.handle_knowledge_transaction),
            ("/api/knowledge_report", api.handle_knowledge_report),
            ("/api/techno_transaction", api.handle_techno_transaction),
            ("/api/techno_report", api.handle_techno_report)
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


