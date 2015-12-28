import json
from basics.webserver import WebServer
from basics.ioloop import IOLoop
from protocol import (
    admin, clientadminsettings, clientmasters, clientreport,
    clienttransactions, clientuser, core, dashboard,
    general, knowledgemaster, knowledgereport, knowledgetransaction,
    login, technomasters, technoreports, technotransactions
)


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
        io_loop,
        controller
    ):
        self._io_loop = io_loop
        self._controller = controller

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
                data["data"]
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
        if type(request) is login.ForgotPassword:
            print "username=", request.username
        return login.ResetPasswordSuccess()

    @api_request(admin.Request)
    def handle_admin(self, request):
        pass

    @api_request(clientadminsettings.Request)
    def handle_client_admin_settings(self, request):
        pass

    @api_request(general.RequestFormat)
    def handle_save_domain(self, request):
        # return self._controller.process_save_domain(
        #     request
        # )

        # return Notification(
        #     1, "test", "", True,

        # )
        pass


#
# run_server
#

def handle_root(request, response):
    response.send("Are you lost?")

def run_server(port):
    io_loop = IOLoop()

    def delay_initialize():
        web_server = WebServer(io_loop)

        web_server.url("/", GET=handle_root)

        controller = Controller()

        api = API(io_loop, controller)
        api_urls_and_handlers = [
            ("/api/login", api.handle_login),
            ("/api/admin", api.handle_admin),
            (
                "/api/handle_client_admin_settings",
                api.handle_client_admin_settings
            ),
        ]
        for url, handler in api_urls_and_handlers:
            web_server.url(url, POST=handler, OPTIONS=cors_handler)

        print "Local port: %s" % port
        web_server.start(port, backlog=1000)

    io_loop.add_callback(delay_initialize)
    io_loop.run()


