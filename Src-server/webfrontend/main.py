import os
import json
from tornado.httpclient import AsyncHTTPClient
from tornado.web import (
    StaticFileHandler, RequestHandler
)
from user_agents import parse
import mimetypes
from basics.webserver import WebServer
from basics.ioloop import IOLoop
from webfrontend.handlerequest import HandleRequest
from webfrontend.client import CompanyManager
from server.constants import CLIENT_TEMPLATE_PATHS
import jinja2


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

def expectation_error(expected, received) :
    msg = "expected %s, but received: %s"
    return msg % (expected, repr(received))

def send_bad_request(response, custom_text=None):
    response.set_status(400)
    if custom_text is None:
        response.send("invalid json format")
    else:
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
        print "handle_post web frontend"
        print request.uri()
        data = None
        actual_data = None
        try:
            data = json.loads(request.body())
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
            actual_data = data[1]
            if type(token) is unicode :
                token = token.encode("utf8")
            elif type(token) is str :
                pass
            else :
                send_bad_request(
                    response,
                    expectation_error("a string", type(token))
                )
                return
        except Exception:
            print "Exception"
            send_invalid_json_format(response)
            return

        handle_request = HandleRequest(
            token, actual_data,
            request.uri(), response, self._http_client,
            request.remote_ip(), self._company_manager
        )
        handle_request.forward_request()
        request.set_close_callback(
            handle_request.connection_closed
        )

ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")

template_loader = jinja2.FileSystemLoader(
    os.path.join(ROOT_PATH, "Src-client")
)
template_env = jinja2.Environment(loader=template_loader)


#
# TemplateHandler
#

class TemplateHandler(RequestHandler):
    def initialize(
        self, path_desktop, path_mobile, parameters,
        company_manager
    ) :
        self.__path_desktop = path_desktop
        self.__path_mobile = path_mobile
        self.__parameters = parameters
        self._company_manager = company_manager

    def get(self, url=None) :
        if url is not None:
            print 'GOT URL%s1' % (url,)
            company = self._company_manager.locate_company(
                url
            )
            if company is None:
                self.set_status(404)
                self.write("client not found")
                return
        path = self.__path_desktop
        if self.__path_mobile is not None :
            useragent = self.request.headers.get("User-Agent")
            if useragent is None:
                useragent = ""
            user_agent = parse(useragent)
            if user_agent.is_mobile :
                path = self.__path_mobile
        mime_type, encoding = mimetypes.guess_type(
            path
        )
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
def server_added(servers):
    pass

def run_web_front_end(port, knowledge_server_address):
    io_loop = IOLoop()

    def delay_initialize():
        http_client = AsyncHTTPClient(
            io_loop.inner(),
            max_clients=1000
        )
        company_manager = CompanyManager(
            io_loop,
            knowledge_server_address,
            http_client,
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

        static_path = os.path.join(ROOT_PATH, "Src-client")
        files_path = os.path.join(static_path, "files")
        desktop_path = os.path.join(files_path, "desktop")
        common_path = os.path.join(desktop_path, "common")
        images_path = os.path.join(common_path, "images")

        web_server.low_level_url(
            r"/images/(.*)",
            StaticFileHandler,
            dict(path=images_path)
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

        print "Local port: %s" % port
        web_server.start(port, backlog=1000)

    io_loop.add_callback(delay_initialize)
    io_loop.run()
