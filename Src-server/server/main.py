import os
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
from server.database import KnowledgeDatabase
import controller
from distribution.protocol import (
    Request as DistributionRequest,
    CompanyServerDetails
)
from replication.protocol import (
    GetChanges, GetChangesSuccess, InvalidReceivedCount
)
from server.constants import (
    TEMPLATE_PATHS,
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
)


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
            self._db.rollback()

    @api_request(
        DistributionRequest
    )
    def handle_server_list(self, request, db):
        return CompanyServerDetails(
            db.get_servers()
        )

    @api_request(
        GetChanges
    )
    def handle_replication(self, request, db):
        actual_count = db.get_trail_id()
        client_id = request.client_id
        received_count = request.received_count
        if received_count > actual_count:
            return InvalidReceivedCount()
        res = GetChangesSuccess(
            db.get_trail_log(client_id, received_count)
        )
        res.to_structure()
        return res

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
            node.set('src', new_url)
        for node in tree.xpath('//*[@href]'):
            url = node.get('href')
            if not url.startswith("#"):
                new_url = self.set_path(url)
            else :
                new_url = url
            node.set('href', new_url)
        data = etree.tostring(tree, method="html")
        return data

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
        output = self.update_static_urls(output)
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
        # db = KnowledgeDatabase(
        #     "localhost", 3306, "root", "123456",
        #     "mirror_knowledge"
        # )

        # db = KnowledgeDatabase(
        #     "198.143.141.73", 3306, "root", "Root!@#123",
        #     "mirror_knowledge"
        # )
        db = KnowledgeDatabase(
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
            ("/server-list", api.handle_server_list),
            ("/replication", api.handle_replication),
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
            ("/knowledge/api/techno_report", api.handle_techno_report)
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
