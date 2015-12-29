import os
import json
import jinja2
import mimetypes
import tornado.web
from tornado.web import StaticFileHandler
from user_agents import parse
from basics.webserver import WebServer
from basics.ioloop import IOLoop
from protocol import (
    admin, clientadminsettings, clientmasters, clientreport,
    clienttransactions, clientuser, core, dashboard,
    general, knowledgemaster, knowledgereport, knowledgetransaction,
    login, technomasters, technoreports, technotransactions
)

import controller 

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
        self,
        io_loop
    ):
        self._io_loop = io_loop

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

        response_data = unbound_method(self, request_data)
        respond(response_data)

    @api_request(login.Request)
    def handle_login(self, request):
        if type(request) is login.Login:
            print "username=", request.username
            return controller.process_login(request)
        # return login.ResetPasswordSuccess()

    @api_request(admin.Request)
    def handle_admin(self, request):
        pass

    @api_request(clientadminsettings.Request)
    def handle_client_admin_settings(self, request):
        pass

    @api_request(general.RequestFormat)
    def handle_general(self, request):
        session_token = request.session_token
        request_frame = request.request
        print session_token, request_frame
        user_id = controller.validate_session_token(session_token)
        if user_id is None:
            return login.InvalidSessionToken()

        if type(request_frame) is general.GetDomains :
            return controller.process_get_domains(user_id)
        if type(request_frame) is general.SaveDomain :
            return controller.process_save_domain(request_frame, user_id)
        if type(request_frame) is general.UpdateDomain :
            return controller.process_update_domain(request_frame, user_id)
        if type(request_frame) is general.ChangeDomainStatus :
            return controller.process_change_domain_status(request_frame, user_id)

        # return self._controller.process_save_domain(
        #     request
        # )

        # return Notification(
        #     1, "test", "", True,

        # )
        pass

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
]


def handle_root(request, response):
    response.send("Are you lost?")

def run_server(port):
    io_loop = IOLoop()

    def delay_initialize():
        web_server = WebServer(io_loop)

        web_server.url("/", GET=handle_root)

        # controller = Controller

        application_urls = []

        for url, path_desktop, path_mobile, parameters in TEMPLATE_PATHS :
            args = {
                "path_desktop": path_desktop,
                "path_mobile": path_mobile,
                "parameters": parameters
            }
            # entry = (url, TemplateHandler, args)
            # application_urls.append(entry)
            web_server.low_level_url(url, TemplateHandler, args)


        api = API(io_loop)
        api_urls_and_handlers = [
            ("/api/login", api.handle_login),
            ("/api/admin", api.handle_admin),
            (
                "/api/handle_client_admin_settings",
                api.handle_client_admin_settings
            ),
            ("/api/general", api.handle_general),
        ]
        for url, handler in api_urls_and_handlers:
            web_server.url(url, POST=handler, OPTIONS=cors_handler)

        static_path = os.path.join(ROOT_PATH, "Src-client")
        api_design_path = os.path.join(ROOT_PATH, "Doc", "API", "Web-API", "Version-1.0.4", "html")
        web_server.low_level_url(r"/api-design/(.*)", tornado.web.StaticFileHandler, dict(path=api_design_path))
        web_server.low_level_url(r"/(.*)", tornado.web.StaticFileHandler, dict(path=static_path))


        print "Local port: %s" % port
        web_server.start(port, backlog=1000)

    io_loop.add_callback(delay_initialize)
    io_loop.run()


