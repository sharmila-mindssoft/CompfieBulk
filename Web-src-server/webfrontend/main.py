import os
import json
import traceback
import mimetypes
import jinja2
import time
from tornado.httpclient import AsyncHTTPClient
from tornado.web import (
    StaticFileHandler, RequestHandler
)
from user_agents import parse
from lxml import etree
from basics.webserver import WebServer
from basics.ioloop import IOLoop
from webfrontend.handlerequest import HandleRequest
from webfrontend.client import CompanyManager
from server.constants import IS_DEVELOPMENT, VERSION
from server.templatepath import (
    CLIENT_TEMPLATE_PATHS
)
# from server import logger


if IS_DEVELOPMENT:
    FILE_VERSION = time.time()
else:
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
# run_server
#
def expectation_error(expected, received):
    msg = "expected %s, but received: %s"
    return msg % (expected, repr(received))


def send_bad_request(response, custom_text=None):
    response.set_status(400)
    # logger.logWebfront(400)
    if custom_text is None:
        # logger.logWebfront("invalid json format")
        response.send("invalid json format")
    else:
        # logger.logWebfront(response)
        # logger.logWebfront(custom_text)
        response.send(custom_text)


def send_invalid_json_format(response):
    send_bad_request(response, "invalid json format")


class Controller(object):
    def __init__(
        self, io_loop, http_client, company_manager
    ):
        self._io_loop = io_loop
        self._http_client = http_client
        self._company_manager = company_manager

    def handle_post(self, request, response):
        data = None
        actual_data = None
        print request.remote_ip()
        print request.header('Remote_addr')
        print request.header('X-Real_ip')
        try:
            data = json.loads(request.body())
            print data
            if type(data) is not list:
                send_bad_request(
                    response,
                    expectation_error("a list", type(data))
                )
                return
            if len(data) != 2:
                send_invalid_json_format(response)
                return
            token = data[0]
            # logger.logWebfront(str(token))
            actual_data = data[1]
            if type(token) is unicode:
                token = token.encode("utf8")
            elif type(token) is str:
                pass
            else:
                send_bad_request(
                    response,
                    expectation_error("a string", type(token))
                )
                return
        except Exception:
            # logger.logWebfront(request.body())
            print traceback.format_exc()
            # logger.logWebfront(traceback.format_exc())
            send_invalid_json_format(response)
            return

        handle_request = HandleRequest(
            token, actual_data,
            request.uri(), response, self._http_client,
            request.remote_ip(), self._company_manager
        )
        # logger.logWebfront("forward_request")
        handle_request.forward_request()
        request.set_close_callback(
            handle_request.connection_closed
        )

ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")

template_loader = jinja2.FileSystemLoader(
    os.path.join(ROOT_PATH, "Client-src-client")
)
template_env = jinja2.Environment(loader=template_loader)


#
# TemplateHandler
#

class TemplateHandler(RequestHandler):
    def initialize(
        self, path_desktop, path_mobile, parameters,
        company_manager
    ):
        self.__path_desktop = path_desktop
        self.__path_mobile = path_mobile
        self.__parameters = parameters
        self._company_manager = company_manager

    def update_static_urls(self, content):
        parser = etree.HTMLParser()
        tree = etree.fromstring(content, parser)
        for node in tree.xpath('//*[@src]'):
            url = node.get('src')
            if node.tag == "script" or node.tag == "img":
                url += "?v=%s" % (FILE_VERSION)
            node.set('src', url)

        for node in tree.xpath('//*[@href]'):
            url = node.get('href')
            if not url.startswith("#"):
                if node.tag == "link":
                    url += "?v=%s" % (FILE_VERSION)
            else:
                if node.tag == "link":
                    url += "?v=%s" % (FILE_VERSION)
            node.set('href', url)
        data = etree.tostring(tree, method="html")
        return data

    def get(self, url=None, token=None):
        if url is not None:
            print 'GOT URL %s' % (url,)
            company = self._company_manager.locate_company(
                url
            )
            if company is None:
                path = "files/client/common/html/notfound.html"
                temp = template_env.get_template(path)
                self.set_status(404)
                self.write(temp.render())
                return
        path = self.__path_desktop
        if self.__path_mobile is not None:
            useragent = self.request.headers.get("User-Agent")
            if useragent is None:
                useragent = ""
            user_agent = parse(useragent)
            if user_agent.is_mobile:
                path = self.__path_mobile
        mime_type, encoding = mimetypes.guess_type(
            path
        )
        self.set_header("Content-Type", mime_type)
        template = template_env.get_template(path)
        output = template.render(**self.__parameters)
        output = self.update_static_urls(output)
        self.write(output)

    def options(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "GET, POST")
        self.set_status(204)
        self.write("")


def server_added(servers):
    pass


def run_web_front_end(port, knowledge_server_address):
    io_loop = IOLoop()

    def delay_initialize():
        http_client = AsyncHTTPClient(
            io_loop.inner(),
            max_clients=1000
        )
        print "knowledge_server_address ", knowledge_server_address
        company_manager = CompanyManager(
            io_loop,
            knowledge_server_address,
            http_client,
            80,
            server_added
        )
        controller = Controller(
            io_loop, http_client, company_manager
        )
        web_server = WebServer(io_loop)

        for path in CLIENT_TEMPLATE_PATHS:
            url, path_desktop, path_mobile, parameters = path
            args = {
                "path_desktop": path_desktop,
                "path_mobile": path_mobile,
                "parameters": parameters,
                "company_manager": company_manager
            }
            web_server.low_level_url(url, TemplateHandler, args)

        web_server.url(
            "/api/(.*)",
            POST=controller.handle_post,
            OPTIONS=cors_handler
        )

        src_server_path = os.path.join(ROOT_PATH, "Web-src-server")
        server_path = os.path.join(src_server_path, "server")
        format_path = os.path.join(server_path, "knowledgeformat")
        reports_path = os.path.join(ROOT_PATH, "exported_reports")
        client_docs_path = os.path.join(server_path, "clientdocuments")
        expiry_download = os.path.join(src_server_path, "expired")
        seven_year_data_download = os.path.join(
            src_server_path, "seven_years_before_data"
        )

        web_server.low_level_url(
            r"/client/compliance_format/(.*)",
            StaticFileHandler,
            dict(path=format_path)
        )

        web_server.low_level_url(
            r"/download/csv/(.*)",
            StaticFileHandler,
            dict(path=reports_path)
        )
        web_server.low_level_url(
            r"/client/client_documents/(.*)",
            StaticFileHandler,
            dict(path=client_docs_path)
        )

        web_server.low_level_url(
            r"/download/bkup/(.*)",
            StaticFileHandler,
            dict(path=expiry_download)
        )

        web_server.low_level_url(
            r"/download_7_year_data/bkup/(.*)",
            StaticFileHandler,
            dict(path=seven_year_data_download)
        )

        static_path = os.path.join(ROOT_PATH, "Client-src-client")
        files_path = os.path.join(static_path, "files")
        client_path = os.path.join(files_path, "client")
        common_path = os.path.join(client_path, "common")
        images_path = os.path.join(common_path, "images")
        css_path = os.path.join(common_path, "css")
        js_path = os.path.join(common_path, "js")
        font_path = os.path.join(common_path, "fonts")
        script_path = client_path
        login_path = os.path.join(client_path, "login")

        web_server.low_level_url(
            r"/images/(.*)",
            StaticFileHandler,
            dict(path=images_path)
        )
        web_server.low_level_url(
            r"/css/(.*)",
            StaticFileHandler,
            dict(path=css_path)
        )
        web_server.low_level_url(
            r"/js/(.*)",
            StaticFileHandler,
            dict(path=js_path)
        )
        web_server.low_level_url(
            r"/fonts/(.*)",
            StaticFileHandler,
            dict(path=font_path)
        )
        web_server.low_level_url(
            r"/common/(.*)",
            StaticFileHandler,
            dict(path=common_path)
        )
        web_server.low_level_url(
            r"/script/(.*)",
            StaticFileHandler,
            dict(path=script_path)
        )
        web_server.low_level_url(
            r"/login/(.*)",
            StaticFileHandler,
            dict(path=login_path)
        )

        api_design_path = os.path.join(
            ROOT_PATH, "Doc", "API",
            "Web-API", "Version-1.0.4", "html"
        )
        web_server.low_level_url(
            r"/api-design/(.*)",
            StaticFileHandler,
            dict(path=api_design_path)
        )

        web_server.low_level_url(
            r"/(.*)", StaticFileHandler,
            dict(path=static_path)
        )

        print "Listening port: %s" % port
        web_server.start(port, backlog=1000)

    io_loop.add_callback(delay_initialize)
    io_loop.run()
