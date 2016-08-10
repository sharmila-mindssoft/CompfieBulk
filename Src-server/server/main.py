import os
import time
import json
import traceback
import mimetypes
import tornado.web
from tornado.web import StaticFileHandler
from user_agents import parse
import jinja2
from lxml import etree
from basics.webserver import WebServer
from basics.ioloop import IOLoop
from protocol import (
    admin, clientadminsettings,
    general, knowledgemaster, knowledgereport, knowledgetransaction,
    login, technomasters, technoreports, technotransactions
)
# from server.database import KnowledgeDatabase
import controller
from server.dbase import Database
from server.database import general as gen
from distribution.protocol import (
    Request as DistributionRequest,
    CompanyServerDetails
)
from replication.protocol import (
    GetChanges, GetDomainChanges, GetChangesSuccess,
    InvalidReceivedCount, GetDelReplicatedSuccess,
    GetClientChanges, GetClientChangesSuccess
)
from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME,
    VERSION, IS_DEVELOPMENT
)

from server.templatepath import (
    TEMPLATE_PATHS
)

import logger

ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")

if IS_DEVELOPMENT :
    FILE_VERSION = time.time()
else :
    FILE_VERSION = VERSION

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

def api_request(request_data_type):
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
        self._ip_addess = None

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
            return request_data
        except Exception, e:
            print "_parse_request"
            print e
            logger.logKnowledgeApi(e, "_parse_request")
            logger.logKnowledgeApi(traceback.format_exc(), "")

            logger.logKnowledge("error", "main.py-parse-request", e)
            print(traceback.format_exc())
            logger.logKnowledge("error", "main.py", traceback.format_exc())
            response.set_status(400)
            response.send(str(e))
            # return None

    def handle_api_request(
        self, unbound_method, request, response,
        request_data_type
    ):
        response.set_default_header("Access-Control-Allow-Origin", "*")
        ip_address = str(request.remote_ip())
        self._ip_addess = ip_address
        if request_data_type == "knowledgeformat" :
            request_data = request
        else :
            request_data = self._parse_request(
                request_data_type, request, response
            )

        if request_data is None:
            return

        def respond(response_data):
            self._send_response(
                response_data, response
            )

        try:
            self._db.begin()
            response_data = unbound_method(self, request_data, self._db)
            if response_data is None or type(response_data) is bool :
                print response_data
                self._db.rollback()
            if type(response_data) != technomasters.ClientCreationFailed:
                self._db.commit()
            else:
                self._db.rollback()
            print "-------------"
            print response_data
            respond(response_data)
        except Exception, e:
            print "handle_api_request"
            print e
            print(traceback.format_exc())
            print ip_address
            logger.logKnowledgeApi(e, "handle_api_request")
            logger.logKnowledgeApi(traceback.format_exc(), "")
            logger.logKnowledgeApi(ip_address, "")

            logger.logKnowledge("error", "main.py-handle-api-", e)
            logger.logKnowledge("error", "main.py", traceback.format_exc())
            if str(e).find("expected a") is False :
                print "------- rollbacked"
                self._db.rollback()
            response.set_status(400)
            response.send(str(e))

    @api_request(
        DistributionRequest
    )
    def handle_server_list(self, request, db):
        return CompanyServerDetails(
            gen.get_servers(db)
        )

    @api_request(GetClientChanges)
    def handle_client_list(self, request, db) :
        return GetClientChangesSuccess(
            gen.get_client_replication_list(db)
        )

    @api_request(GetChanges)
    def handle_replication(self, request, db):
        actual_count = gen.get_trail_id(db)
        # print "actual_count ", actual_count

        client_id = request.client_id
        received_count = request.received_count
        # print  "received_count", received_count
        if received_count > actual_count:
            return InvalidReceivedCount()
        # print "replication client_id = %s, received_count = %s" % (client_id, received_count)
        res = GetChangesSuccess(
            gen.get_trail_log(db, client_id, received_count)
        )
        return res

    @api_request(GetDomainChanges)
    def handle_domain_replication(self, request, db):
        actual_count = gen.get_trail_id(db)
        client_id = request.client_id
        domain_id = request.domain_id
        received_count = request.received_count
        actual_replica_count = request.actual_count

        if received_count > actual_count :
            return InvalidReceivedCount()

        res = GetChangesSuccess(
            gen.get_trail_log_for_domain(
                db, client_id, domain_id, received_count,
                actual_replica_count
            )
        )
        return res

    @api_request(GetChanges)
    def handle_delreplicated(self, request, db):
        actual_count = gen.get_trail_id(db)

        client_id = request.client_id
        received_count = request.received_count
        s = "%s, %s, %s " % (client_id, received_count, actual_count)
        logger.logKnowledge("info", "trail", s)
        if actual_count >= received_count :
            gen.remove_trail_log(client_id, received_count)
        return GetDelReplicatedSuccess()

    @api_request(login.Request)
    def handle_login(self, request, db):
        print self._ip_addess
        return controller.process_login_request(request, db, self._ip_addess)
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

    @api_request("knowledgeformat")
    def handle_format_file(self, request, db):
        def validate_session_from_body(content):
            content_list = content.split("\r\n\r\n")
            session = content_list[-1].split("\r\n")[0]
            user_id = db.validate_session_token(str(session))
            if user_id is None :
                return False
            else :
                return True

        if (validate_session_from_body(request.body())) :
            info = request.files()
            response_data = controller.process_uploaded_file(info, "knowledge")
            return response_data
        else :
            return login.InvalidSessionToken()

template_loader = jinja2.FileSystemLoader(
    os.path.join(ROOT_PATH, "Src-client")
)
template_env = jinja2.Environment(loader=template_loader)

class TemplateHandler(tornado.web.RequestHandler) :
    def initialize(self, path_desktop, path_mobile, parameters) :
        self.__path_desktop = path_desktop
        self.__path_mobile = path_mobile
        self.__parameters = parameters

    def set_path(self, url):
        if url.startswith("/"):
            new_url = "/knowledge" + url
        else :
            new_url = "/knowledge/" + url
        return new_url

    def update_static_urls(self, content):
        parser = etree.HTMLParser()
        tree = etree.fromstring(content, parser)
        for node in tree.xpath('//*[@src]'):
            url = node.get('src')
            new_url = self.set_path(url)
            if node.tag == "script" :
                new_url += "?v=%s" % (FILE_VERSION)
            if node.tag == "img" :
                new_url += "?v=%s" % (FILE_VERSION)
            node.set('src', new_url)
        for node in tree.xpath('//*[@href]'):
            url = node.get('href')
            if not url.startswith("#"):
                new_url = self.set_path(url)
                if node.tag == "link" :
                    new_url += "?v=%s" % (FILE_VERSION)
            else :
                new_url = url
                if node.tag == "link" :
                    new_url += "?v=%s" % (FILE_VERSION)
            node.set('href', new_url)
        data = etree.tostring(tree, method="html")
        return data

    def get(self, url=None) :
        if url is not None:
            print "url:{}".format(url)
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
        output = self.update_static_urls(output)
        token = self.xsrf_token
        print token
        self.set_cookie("_xsrf", token)
        # print self.get_secure_cookie('_xsrf')
        # if not self.get_cookie("_xsrf"):
        #     self.set_cookie("test", token)
        # print self.get_secure_cookie('_xsrf')
        # self.write(d)
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

def run_server(port):
    io_loop = IOLoop()

    def delay_initialize():
        db = Database(
            KNOWLEDGE_DB_HOST,
            KNOWLEDGE_DB_PORT,
            KNOWLEDGE_DB_USERNAME, KNOWLEDGE_DB_PASSWORD,
            KNOWLEDGE_DATABASE_NAME
        )
        db.connect()

        web_server = WebServer(io_loop)

        # web_server.url("/", GET=handle_root)

        for url, path_desktop, path_mobile, parameters in TEMPLATE_PATHS :
            args = {
                "path_desktop": path_desktop,
                "path_mobile": path_mobile,
                "parameters": parameters
            }
            web_server.low_level_url(url, TemplateHandler, args)

        api = API(io_loop, db)

        api_urls_and_handlers = [
            ("/knowledge/server-list", api.handle_server_list),
            ("/knowledge/client-list", api.handle_client_list),
            ("/knowledge/replication", api.handle_replication),
            ("/knowledge/domain-replication", api.handle_domain_replication),
            ("/knowledge/delreplicated", api.handle_delreplicated),
            ("/knowledge/api/login", api.handle_login),
            ("/knowledge/api/admin", api.handle_admin),
            ("/knowledge/api/techno", api.handle_techno),
            (
                "/knowledge/api/handle_client_admin_settings",
                api.handle_client_admin_settings
            ),
            ("/knowledge/api/general", api.handle_general),
            ("/knowledge/api/knowledge_master", api.handle_knowledge_master),
            (
                "/knowledge/api/knowledge_transaction",
                api.handle_knowledge_transaction
            ),
            ("/knowledge/api/knowledge_report", api.handle_knowledge_report),
            (
                "/knowledge/api/techno_transaction",
                api.handle_techno_transaction
            ),
            ("/knowledge/api/techno_report", api.handle_techno_report),
            ("/knowledge/api/files", api.handle_format_file)
        ]
        for url, handler in api_urls_and_handlers:
            web_server.url(url, POST=handler, OPTIONS=cors_handler)

        server_path = os.path.join(ROOT_PATH, "Src-server")
        server_path = os.path.join(server_path, "server")
        format_path = os.path.join(server_path, "knowledgeformat")
        logo_path = os.path.join(server_path, "clientlogo")

        web_server.low_level_url(
            r"/knowledge/compliance_format/(.*)",
            StaticFileHandler,
            dict(path=format_path)
        )

        web_server.low_level_url(
            r"/knowledge/clientlogo/(.*)",
            StaticFileHandler,
            dict(path=logo_path)
        )

        static_path = os.path.join(ROOT_PATH, "Src-client")
        files_path = os.path.join(static_path, "files")
        desktop_path = os.path.join(files_path, "desktop")
        common_path = os.path.join(desktop_path, "common")
        images_path = os.path.join(common_path, "images")
        css_path = os.path.join(common_path, "css")
        js_path = os.path.join(common_path, "js")
        script_path = os.path.join(desktop_path, "knowledge")
        login_path = os.path.join(desktop_path, "login")

        web_server.low_level_url(
            r"/images/(.*)",
            StaticFileHandler, dict(path=images_path)
        )
        web_server.low_level_url(
            r"/knowledge/images/(.*)",
            StaticFileHandler, dict(path=images_path)
        )
        web_server.low_level_url(
            r"/knowledge/css/(.*)",
            StaticFileHandler, dict(path=css_path)
        )
        web_server.low_level_url(
            r"/knowledge/js/(.*)",
            StaticFileHandler, dict(path=js_path)
        )
        web_server.low_level_url(
            r"/knowledge/common/(.*)",
            StaticFileHandler,
            dict(path=common_path)
        )
        web_server.low_level_url(
            r"/knowledge/script/(.*)",
            StaticFileHandler,
            dict(path=script_path)
        )
        web_server.low_level_url(
            r"/knowledge/login/(.*)",
            StaticFileHandler,
            dict(path=login_path)
        )

        api_design_path = os.path.join(
            ROOT_PATH, "Doc", "API", "Web-API", "Version-1.0.4", "html"
        )
        web_server.low_level_url(
            r"/knowledge/api-design/(.*)", StaticFileHandler,
            dict(path=api_design_path)
        )
        web_server.low_level_url(
            r"/knowledge/(.*)", StaticFileHandler,
            dict(path=static_path)
        )
        web_server.low_level_url(
            r"/(.*)", StaticFileHandler,
            dict(path=static_path)
        )
        print "Listening port: %s" % port
        web_server.start(port, backlog=1000)

    io_loop.add_callback(delay_initialize)
    io_loop.run()
