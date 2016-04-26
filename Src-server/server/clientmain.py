import os
import json
import traceback
from tornado.web import StaticFileHandler
from tornado.httpclient import AsyncHTTPClient
from basics.webserver import WebServer
from basics.ioloop import IOLoop
from protocol import (
    clientadminsettings, clientmasters, clientreport,
    clienttransactions, dashboard,
    login, general, clientuser, mobile
)
from server.clientdatabase import ClientDatabase

import clientcontroller as controller
import mobilecontroller as mobilecontroller
from webfrontend.client import CompanyManager
from server.client import ReplicationManager

import logger

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
        self._knowledge_server_address = knowledge_server_address
        self._http_client = http_client
        self._company_manager = CompanyManager(
            io_loop,
            knowledge_server_address,
            http_client,
            60,
            self.server_added
        )
        self._databases = {}
        self._replication_managers = {}
        self._ip_address = None

    def close_connection(self, db):
        try:
            db.close()
        except Exception:
            pass

    def server_added(self, servers):
        # print "server_added called"
        # self._databases = {}
        try:
            #
            for company_id, db in self._databases.iteritems():
                db.close()

            for company_id, rep_man in self._replication_managers.iteritems():
                rep_man.stop()

            self._databases = {}
            self._replication_managers = {}
            # print servers
            for company_id, company in servers.iteritems():
                company_server_ip = company.company_server_ip
                ip, port = self._address
                if company_server_ip.ip_address == ip and \
                        company_server_ip.port == port:
                    try:
                        db = ClientDatabase(
                            company.db_ip.ip_address,
                            company.db_ip.port,
                            company.db_username,
                            company.db_password,
                            company.db_name
                        )
                        db.connect()
                        if db._connection is not None :
                            self._databases[company_id] = db
                            rep_man = ReplicationManager(
                                self._io_loop,
                                self._knowledge_server_address,
                                self._http_client,
                                db,
                                company_id
                            )
                            # print "replication started ", company_id
                            rep_man.start()
                            self._replication_managers[company_id] = rep_man
                    except Exception, e:
                        print e
                        logger.logClient("error", "clientmain.py-server-added", e)
                        # print "Client database not available to connect ", company_id, company.to_structure()
                        continue

        except Exception, e :
            logger.logClient("error", "clientmain.py-server-added", e)
            logger.logClient("error", "clientmain.py-server-added", traceback.format_exc())

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
                response.send("Company not found")
                # data = login.ClientDatabaseNotExists().to_structure()
                # s = json.dumps(data, indent=2)
                # response.send(s)
                # response.send()
                # self._send_response(login.ClientDatabaseNotExists(), response)
                return None
            actual_data = data[1]
            request_data = request_data_type.parse_structure(
                actual_data
            )
        except Exception, e:
            # print e
            # print(traceback.format_exc())
            logger.logClient("error", "clientmain.py-parse-request", e)
            logger.logClient("error", "clientmain.py", traceback.format_exc())

            response.set_status(400)
            response.send(str(e))
            return None
        return (db, request_data, company_id)

    def handle_api_request(
        self, unbound_method, request, response,
        request_data_type, need_client_id
    ):
        ip_address = str(request.remote_ip())
        self._ip_address = ip_address
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
            # print(traceback.format_exc())
            # print e
            logger.logClient("error", "clientmain.py-handle-api", e)
            logger.logClient("error", "clientmain.py", traceback.format_exc())

            db.rollback()

    @api_request(login.Request, need_client_id=True)
    def handle_login(self, request, db, client_id):
        print self._ip_address
        return controller.process_login_request(request, db, client_id, self._ip_address)

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

    @api_request(clientuser.RequestFormat)
    def handle_client_user(self, request, db):
        return controller.process_client_user_request(request, db)

    @api_request(mobile.RequestFormat)
    def handle_mobile_request(self, request, db):
        return mobilecontroller.process_client_mobile_request(request, db)

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
        client_docs_path = os.path.join(ROOT_PATH, "clientdocuments")
        exported_reports_path = os.path.join(ROOT_PATH, "exported_reports")

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
            ("/api/client_user", api.handle_client_user),
            ("/api/mobile", api.handle_mobile_request)
        ]
        for url, handler in api_urls_and_handlers:
            web_server.url(url, POST=handler, OPTIONS=cors_handler)

        web_server.low_level_url(
            r"/client/client_documents/(.*)",
            StaticFileHandler,
            dict(path=client_docs_path)
        )

        web_server.low_level_url(
            r"/download/csv/(.*)", StaticFileHandler,
            dict(path=exported_reports_path)
        )
        print "Listening at: %s:%s" % (ip, port)
        web_server.start(port, backlog=1000)

    io_loop.add_callback(delay_initialize)
    io_loop.run()
