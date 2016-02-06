import json
import traceback
from tornado.httpclient import AsyncHTTPClient
from basics.webserver import WebServer
from basics.ioloop import IOLoop
from protocol import (
    clientadminsettings, clientmasters, clientreport,
    clienttransactions, dashboard,
    login, general
)
from server.clientdatabase import ClientDatabase

import clientcontroller as controller
from webfrontend.client import CompanyManager


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
    request_data_type, need_client_id=False
):
    def wrapper(f):
        def wrapped(self, request, response):
            self.handle_api_request(
                f, request, response,
                request_data_type, need_client_id
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
        address,
        knowledge_server_address,
        http_client
    ):
        self._io_loop = io_loop
        self._address = address
        self._company_manager = CompanyManager(
            io_loop,
            knowledge_server_address,
            http_client,
            self.server_added
        )
        self._databases = {}

    def close_connection(self, db):
        try:
            db.close()
        except Exception:
            pass

    def server_added(self, servers):
        # self._databases = {}
        try:
            for company_id, db in self._databases.iteritems():
                db.close()
                # self.close_connection(db)
            for company_id, company in servers.iteritems():
                company_server_ip = company.company_server_ip
                ip, port = self._address
                if company_server_ip.ip_address == ip and \
                        company_server_ip.port == port:
                    db = ClientDatabase(
                        company.db_ip.ip_address,
                        company.db_ip.port,
                        company.db_username,
                        company.db_password,
                        company.db_name
                    )
                    db.connect()
                    self._databases[company_id] = db
        except Exception:
            print db

    def _send_response(
        self, response_data, response
    ):
        assert response is not None
        data = response_data.to_structure()
        s = json.dumps(data, indent=2)
        response.send(s)

    def expectation_error(self, expected, received) :
        msg = "expected %s, but received: %s"
        return msg % (expected, repr(received))

    def send_bad_request(self, response, custom_text=None):
        response.set_status(400)
        if custom_text is None:
            response.send("invalid json format")
        else:
            response.send(custom_text)

    def _parse_request(
        self, request_data_type, request, response
    ):
        request_data = None
        db = None
        company_id = None
        try:
            data = json.loads(request.body())
            if type(data) is not list:
                self.send_bad_request(
                    response,
                    self.expectation_error(
                        "a list", type(data)
                    )
                )
                return None
            if len(data) != 2:
                self.send_invalid_json_format(
                    response
                )
                return None
            company_id = int(data[0])
            db = self._databases.get(company_id)
            if db is None:
                response.set_status(404)
                response.send("company not found")
                return None
            actual_data = data[1]
            request_data = request_data_type.parse_structure(
                actual_data
            )
        except Exception, e:
            print e
            response.set_status(400)
            response.send(str(e))
            return None
        return (db, request_data, company_id)

    def handle_api_request(
        self, unbound_method, request, response,
        request_data_type, need_client_id
    ):
        response.set_default_header("Access-Control-Allow-Origin", "*")

        request_data = self._parse_request(
            request_data_type, request, response
        )
        if request_data is None:
            return

        db, request_data, company_id = request_data

        def respond(response_data):
            self._send_response(
                response_data, response
            )

        db.begin()
        try:
            if need_client_id :
                response_data = unbound_method(
                    self, request_data, db, company_id
                )
            else :
                response_data = unbound_method(self, request_data, db)
            db.commit()
            respond(response_data)
        except Exception, e:
            print(traceback.format_exc())
            print e
            db.rollback()

    @api_request(login.Request, need_client_id=True)
    def handle_login(self, request, db, client_id):
        return controller.process_login_request(request, db, client_id)

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

    @api_request(clientadminsettings.RequestFormat)
    def handle_client_admin_settings(self, request, db):
        return controller.process_client_admin_settings_requests(request, db)

    @api_request(general.RequestFormat)
    def handle_general(self, request, db):
        return controller.process_general_request(request, db)

#
# run_server
#

def run_server(address, knowledge_server_address):
    ip, port = address
    io_loop = IOLoop()

    def delay_initialize():
        http_client = AsyncHTTPClient(
            io_loop.inner(),
            max_clients=1000
        )

        web_server = WebServer(io_loop)

        api = API(
            io_loop,
            address,
            knowledge_server_address,
            http_client
        )

        api_urls_and_handlers = [
            ("/api/login", api.handle_login),
            ("/api/client_masters", api.handle_client_masters),
            ("/api/client_transaction", api.handle_client_transaction),
            ("/api/client_reports", api.handle_client_reports),
            ("/api/client_dashboard", api.handle_client_dashboard),
            ("/api/client_admin_settings", api.handle_client_admin_settings),
            ("/api/general", api.handle_general),
        ]
        for url, handler in api_urls_and_handlers:
            web_server.url(url, POST=handler, OPTIONS=cors_handler)

        print "Listening at: %s:%s" % (ip, port)
        web_server.start(port, backlog=1000)

    io_loop.add_callback(delay_initialize)
    io_loop.run()
