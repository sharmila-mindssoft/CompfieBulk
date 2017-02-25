import os
import json
import time
import traceback
# import mysql.connector.pooling
import mysql.connector
from flask import Flask, request, Response

from functools import wraps

from clientprotocol import (
    clientadminsettings, clientmasters, clientreport,
    clienttransactions, dashboard,
    clientlogin, general, clientuser, clientmobile,
    widgetprotocol
)
from server.dbase import Database
import clientcontroller as controller
import mobilecontroller as mobilecontroller
from server.client import CompanyManager
from server.clientreplicationbase import (
    ClientReplicationManager, ReplicationManagerWithBase,
    # DomainReplicationManager
)
from server.constants import SESSION_CUTOFF
import logger

ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")
app = Flask(__name__)


#
# api_request
#

def api_request(
    request_data_type, need_client_id=False, is_group=False, need_category=False, save_le=True
):
    def wrapper(f):
        @wraps(f)
        def wrapped(self):
            return self.handle_api_request(
                f, request_data_type, need_client_id, is_group, need_category, save_le
            )
        return wrapped
    return wrapper


def global_api_request(
    request_data_type, is_group=True, need_category=False
):
    def wrapper(f):
        @wraps(f)
        def wrapped(self):
            return self.handle_global_api_request(
                f, request_data_type, is_group, need_category
            )
        return wrapped
    return wrapper


class API(object):
    def __init__(
        self,
        address,
        knowledge_server_address,
    ):
        self._address = address
        self._knowledge_server_address = knowledge_server_address
        self._group_databases = {}
        self._le_databases = {}
        self._replication_managers_for_group = {}
        self._replication_managers_for_le = {}
        self._company_manager = CompanyManager(
            knowledge_server_address,
            5000,
            self.server_added
        )
        # print "Databases initialize"

        self._ip_address = None
        # self._remove_old_session()

    def _remove_old_session(self):

        def on_return():
            self._remove_old_session()

        def _with_client_info():
            for c_id, c_db in self._databases.iteritems() :
                on_session_timeout(c_db)
            on_return()

        def on_session_timeout(c_db):
            c_db.begin()
            try :
                c_db.clear_session(SESSION_CUTOFF)
                c_db.commit()
            except Exception, e :
                print e
                c_db.rollback()

        self._io_loop.add_timeout(
            time.time() + 1080, _with_client_info
        )

    def close_connection(self, db):
        try:
            db.close()
        except Exception:
            pass

    def client_connection_pool(self, data):
        # return mysql.connector.pooling.MySQLConnectionPool(
        #     pool_name=str(le_id) + poolname,
        #     pool_size=10,
        #     pool_reset_session=True,
        #     autocommit=False,
        #     user=data.db_username,
        #     password=data.db_password,
        #     host=data.db_ip.ip_address,
        #     database=data.db_name,
        #     port=data.db_ip.port
        # )
        return mysql.connector.connect(
            autocommit=False,
            user=data.db_username,
            password=data.db_password,
            host=data.db_ip.ip_address,
            database=data.db_name,
            port=data.db_ip.port
        )

    def server_added(self, servers):
        self._group_databases = {}
        self._le_databases = {}
        self._replication_managers_for_group = {}
        self._replication_managers_for_le = {}
        try:

            for company in servers:
                company.to_structure()
                company_id = company.company_id
                company_server_ip = company.company_server_ip
                ip, port = self._address
                # print self._address
                if company_server_ip.ip_address == ip and company_server_ip.port == port :
                    if company.is_group is True:
                        if self._group_databases.get(company_id) is not None :
                            continue
                        else :
                            # group db connections
                            try:
                                # db_cons = self.client_connection_pool(company, company_id, "con_pool_group")
                                self._group_databases[company_id] = company
                                print " %s added in connection pool" % company_id
                            except Exception, e:
                                # when db connection failed continue to the next server
                                logger.logClientApi(ip, port)
                                logger.logClientApi(e, "Group Server added")
                                logger.logClient("error", "exception", str(traceback.format_exc()))
                                logger.logClient("error", "clientmain.py-server-added", e)
                                logger.logClientApi("GROUP database not available to connect ", str(company_id) + "-" + str(company.to_structure()))
                                continue
                    else :
                        if self._le_databases.get(company_id) is not None :
                            continue
                        else :
                            try:
                                # db_cons = self.client_connection_pool(company, company_id, "con_pool_le")
                                self._le_databases[company_id] = company
                                print " %s added in le connection pool" % company_id
                            except Exception, e:
                                # when db connection failed continue to the next server
                                logger.logClientApi(ip, port)
                                logger.logClientApi(e, "LE database added")
                                logger.logClient("error", "exception", str(traceback.format_exc()))
                                logger.logClient("error", "clientmain.py-le_database-added", e)
                                logger.logClientApi("LE database not available to connect ", str(company_id) + "-" + str(company.to_structure()))
                                continue

            print self._le_databases
            print self._group_databases

            def client_added(clients):
                print clients
                for client in clients:
                    _client_id = client.client_id
                    # print _client_id
                    is_new_data = client.is_new_data
                    is_new_domain = client.is_new_domain
                    # _domain_id = client.domain_id
                    print client.to_structure()
                    print " \n "
                    if client.is_group is True:
                        # print "client added"
                        db_cons_info = self._group_databases.get(_client_id)
                        print db_cons_info
                        if db_cons_info is None :
                            continue
                        # db_cons = db_cons_info.get_connection()
                        db_cons = self.client_connection_pool(db_cons_info)

                        client_db = Database(db_cons)
                        if client_db is not None :
                            print _client_id
                            if is_new_data is True and is_new_domain is False :
                                # replication for group db only master data
                                rep_man = ReplicationManagerWithBase(
                                    self._knowledge_server_address,
                                    client_db,
                                    _client_id,
                                    client.is_group
                                )

                                if self._replication_managers_for_group.get(_client_id) is None :
                                    rep_man.start()
                                    self._replication_managers_for_group[_client_id] = rep_man
                    else :
                        db_cons_info = self._le_databases.get(_client_id)
                        print db_cons_info
                        if db_cons_info is None :
                            continue
                        # db_cons = db_cons_info.get_connection()
                        db_cons = self.client_connection_pool(db_cons_info)
                        le_db = Database(db_cons)
                        if le_db is not None :
                            if is_new_data is True and is_new_domain is False :
                                # replication for group db only master data
                                rep_man = ReplicationManagerWithBase(
                                    self._knowledge_server_address,
                                    le_db,
                                    _client_id,
                                    client.is_group
                                )

                                if self._replication_managers_for_le.get(_client_id) is None :
                                    rep_man.start()
                                    self._replication_managers_for_le[_client_id] = rep_man

                            # if is_new_domain is True and _domain_id is not None :
                            #     d_rep_man = {}
                            #     domain_lst = _domain_id.strip().split(",")
                            #     for d in domain_lst :
                            #         domain_id = int(d)
                            #         domain_rep_man = DomainReplicationManager(
                            #             self._io_loop,
                            #             self._knowledge_server_address,
                            #             self._http_client,
                            #             client_db,
                            #             _client_id,
                            #             domain_id
                            #         )
                            #         domain_rep_man.start()
                            #         d_rep_man[_client_id] = domain_rep_man

            _client_manager = ClientReplicationManager(
                self._knowledge_server_address,
                500,
                client_added
            )
            # replication start
            _client_manager._start()

        except Exception, e :
            logger.logClientApi(e, "Server added")
            logger.logClientApi(traceback.format_exc(), "")
            logger.logClient("error", "clientmain.py-server-added", e)
            logger.logClient("error", "clientmain.py-server-added", traceback.format_exc())
            return

    def _send_response(
        self, response_data, status_code
    ):
        if type(response_data) is not str :
            data = response_data.to_structure()
            #print data
            s = json.dumps(data, indent=2)
        else:
            s = response_data
        resp = Response(s, status=status_code, mimetype="application/json")
        return resp

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
        self, request_data_type, is_group
    ):
        request_data = None
        # _db = None
        company_id = None
        try:
            data = request.get_json(force=True)
            if type(data) is not list:
                self._send_response(self.expectation_error("a list", type(data)), 400)

            if len(data) != 2:
                self._send_response("Invalid json format", 300)

            company_id = int(data[0])
            actual_data = data[1]
            # print actual_data
            # print company_id
            request_data = request_data_type.parse_structure(
                actual_data
            )
            if is_group is False :
                company_id = request_data.request.legal_entity_id

        except Exception, e:
            print e
            logger.logClientApi(e, "_parse_request")
            logger.logClientApi(traceback.format_exc(), "")

            logger.logClient("error", "clientmain.py-parse-request", e)
            logger.logClient("error", "clientmain.py", traceback.format_exc())

            return str(e)
        return request_data, company_id

    def _validate_user_session(self, session):
        session_token = session.split('-')
        client_id = int(session_token[0])
        _group_db_info = self._group_databases.get(client_id)
        if _group_db_info is None :
            raise Exception("Client Not Found")
        _group_db_cons = self.client_connection_pool(_group_db_info)
        _group_db = Database(_group_db_cons)
        try :
            _group_db.begin()
            session_user, session_category = _group_db.validate_session_token(session)
            _group_db.commit()
            _group_db_cons.close()
            if session_user is None :
                return False, False, None
            else :
                return session_user, client_id, session_category
        except Exception, e :
            print e
            _group_db.rollback()
            _group_db_cons.close()
            raise Exception(e)

    def _validate_user_password(self, session, user_id, usr_pwd):
        session_token = session.split('-')
        client_id = int(session_token[0])
        _group_db_info = self._group_databases.get(client_id)
        if _group_db_info is None :
            raise Exception("Client Not Found")
        _group_db_cons = self.client_connection_pool(_group_db_info)
        _group_db = Database(_group_db_cons)
        is_valid = False
        try :
            _group_db.begin()
            is_valid = _group_db.verify_password(user_id, usr_pwd)
            _group_db.commit()
            _group_db_cons.close()
        except Exception, e :
            print e
            _group_db.rollback()
            _group_db_cons.close()
            raise Exception(e)
        return is_valid

    def handle_api_request(
        self, unbound_method,
        request_data_type, need_client_id, is_group, need_category, save_le
    ):
        def respond(response_data):
            return self._send_response(
                response_data, 200
            )

        ip_address = request.remote_addr
        self._ip_address = ip_address
        # response.set_default_header("Access-Control-Allow-Origin", "*")
        # validate api format
        request_data, company_id = self._parse_request(
            request_data_type, is_group
        )
        if request_data is None:
            return

        # validate session token
        if need_client_id is False :
            session = request_data.session_token
            session_user, client_id, session_category = self._validate_user_session(session)
            if session_user is False :
                return respond(clientlogin.InvalidSessionToken())

            if hasattr(request_data.request, "password") :
                if (self._validate_user_password(session, session_user, request_data.request.password)) is False :
                    return respond(clientlogin.InvalidCurrentPassword())

        # request process in controller
        if is_group :
            print "Group DB"
            db_cons_info = self._group_databases.get(company_id)
        else :
            print "LE Db"
            db_cons_info = self._le_databases.get(company_id)

        if db_cons_info is None:
            print 'connection pool is none'
            self._send_response("Company not found", 404)

        # _db_con = db_cons.get_connection()
        _db_con = self.client_connection_pool(db_cons_info)
        print db_cons_info
        _db = Database(_db_con)
        print _db
        if _db_con is None:
            self._send_response("Company not found", 404)

        _db.begin()
        try:
            if need_client_id :
                response_data = unbound_method(
                    self, request_data, _db, company_id, ip_address
                )
            elif need_category :
                response_data = unbound_method(
                    self, request_data, _db, session_user, session_category
                )
            elif save_le :
                response_data = unbound_method(
                    self, request_data, _db, session_user, client_id, self._le_databases
                )
            else :
                response_data = unbound_method(
                    self, request_data, _db, session_user, client_id, company_id
                )
            _db.commit()
            _db_con.close()
            return respond(response_data)
        except Exception, e:
            logger.logClientApi(e, "handle_api_request")
            logger.logClientApi(traceback.format_exc(), "")
            print(traceback.format_exc())
            logger.logClient("error", "clientmain.py-handle-api", e)
            logger.logClient("error", "clientmain.py", traceback.format_exc())
            if str(e).find("expected a") is False :
                _db.rollback()
                _db_con.close()

            return self._send_response(str(e), 400)
            # response.set_status(400)
            # response.send(str(e))

    def handle_global_api_request(self, unbound_method, request_data_type, is_group, need_category):
        le_ids = []

        def respond(response_data):
            return self._send_response(response_data, 200)

        performed_les = []
        # global performed_response
        performed_response = None

        def merge_data(p_response, data, request_data):
            if p_response is None :
                p_response = data
            else :
                # merge chart from the processed LE database
                if type(request_data.request) is dashboard.GetComplianceStatusChart :
                    p_response.chart_data.extend(data.chart_data)

                elif type(request_data.request) is dashboard.GetEscalationsChart :
                    p_response.chart_data.extend(data.chart_data)

                elif type(request_data.request) is dashboard.GetNotCompliedChart :

                    p_response.T_0_to_30_days_count += data.T_0_to_30_days_count
                    p_response.T_31_to_60_days_count += data.T_31_to_60_days_count
                    p_response.T_61_to_90_days_count += data.T_61_to_90_days_count
                    p_response.Above_90_days_count += data.Above_90_days_count

                elif type(request_data.request) is dashboard.GetTrendChart :
                    p_response.data.extend(data.data)

                elif type(request_data.request) is dashboard.GetComplianceApplicabilityStatusChart :
                    p_response.unassign_count += data.unassign_count
                    p_response.not_opted_count += data.not_opted_count
                    p_response.rejected_count += data.rejected_count
                    p_response.not_complied_count += data.not_complied_count

                # merge drilldown from the processed LE database
                elif type(request_data.request) is dashboard.GetComplianceStatusDrillDownData :
                    p_response.drill_down_data.extend(data.drill_down_data)

                elif type(request_data.request) is dashboard.GetEscalationsDrillDownData :
                    p_response.delayed.extend(data.delayed)
                    p_response.not_complied.extend(data.not_complied)

                elif type(request_data.request) is dashboard.GetNotCompliedDrillDown :
                    p_response.drill_down_data.extend(data.drill_down_data)

                elif type(request_data.request) is dashboard.GetTrendChartDrillDownData :
                    p_response.drill_down_data.extend(data.drill_down_data)

                elif type(request_data.request) is dashboard.GetComplianceApplicabilityStatusDrillDown :
                    p_response.drill_down_data.extend(data.drill_down_data)

                elif type(request_data.request) is widgetprotocol.GetComplianceChart :
                    p_response = controller.merge_compliance_chart_widget(p_response, data)

                elif type(request_data.request) is widgetprotocol.GetEscalationChart :
                    p_response = controller.merge_escalation_chart_widget(p_response, data)
                else :
                    pass
            return p_response

        try :
            # print "try"
            request_data, company_id = self._parse_request(request_data_type, is_group)
            session = request_data.session_token
            session_user, client_id, session_category = self._validate_user_session(session)
            if hasattr(request_data.request, "legal_entity_ids") :
                le_ids = request_data.request.legal_entity_ids
                performed_les = []
                performed_response = None

                for le in le_ids :
                    db_cons_info = self._le_databases.get(le)

                    if db_cons_info is None:
                        performed_les.append(le)
                        print 'connection pool is none'
                        continue
                        # return self._send_response("Company not found", 404)

                    # _db_con = db_cons.get_connection()
                    _db_con = self.client_connection_pool(db_cons_info)
                    _db = Database(_db_con)
                    if _db_con is None:
                        performed_les.append(le)
                        continue
                        # return self._send_response("Company not found", 404)

                    _db.begin()
                    try:
                        response_data = unbound_method(
                            self, request_data, _db, session_user, session_category
                        )

                        _db.commit()
                        _db_con.close()
                        performed_les.append(le)
                        performed_response = merge_data(performed_response, response_data, request_data)

                    except Exception, e:
                        print " --------------"
                        logger.logClientApi(e, "handle_api_request")
                        logger.logClientApi(traceback.format_exc(), "")
                        print(traceback.format_exc())
                        logger.logClient("error", "clientmain.py-handle-api", e)
                        logger.logClient("error", "clientmain.py", traceback.format_exc())
                        if str(e).find("expected a") is False :
                            _db.rollback()
                            _db_con.close()
                        performed_response = str(e)
                        # return self._send_response(str(e), 400)

                if len(le_ids) == len(performed_les) :
                    return respond(performed_response)

            else :
                print "le-ids not found"
                return self._send_response("le-ids not found", 400)

        except Exception, e :
            print(traceback.format_exc())
            return self._send_response(str(e), 400)

    @api_request(clientlogin.Request, need_client_id=True, is_group=True)
    def handle_login(self, request, db, client_id, user_ip):
        # print self._ip_address

        logger.logLogin("info", user_ip, "login-user", "Login process end")
        return controller.process_login_request(request, db, client_id, user_ip)

    @api_request(clientmasters.RequestFormat, is_group=True, save_le=True)
    def handle_client_masters(self, request, db, session_user, client_id, le_ids):
        return controller.process_client_master_requests(request, db, session_user, client_id, le_ids)

    @api_request(clienttransactions.RequestFormat, is_group=True, need_category=True)
    def handle_client_master_filters(self, request, db, session_user, session_category):
        return controller.process_client_master_filters_request(request, db, session_user, session_category)

    @api_request(clienttransactions.RequestFormat, need_category=True)
    def handle_client_transaction(self, request, db, session_user, session_category):
        return controller.process_client_transaction_requests(request, db, session_user, session_category)

    @api_request(clientreport.RequestFormat, is_group=False, need_category=True)
    def handle_client_reports(self, request, db, session_user, session_category):
        return controller.process_client_report_requests(request, db, session_user, session_category)

    @global_api_request(dashboard.RequestFormat, is_group=True, need_category=True)
    def handle_client_dashboard(self, request, db, session_user, session_category):
        return controller.process_client_dashboard_requests(request, db, session_user, session_category)

    @api_request(clientadminsettings.RequestFormat)
    def handle_client_admin_settings(self, request, db, session_user, client_id, le_id):
        return controller.process_client_admin_settings_requests(request, db)

    @api_request(general.RequestFormat)
    def handle_general(self, request, db, session_user, client_id, le_id):
        return controller.process_general_request(request, db)

    @api_request(clientuser.RequestFormat)
    def handle_client_user(self, request, db, session_user, client_id, le_id):
        return controller.process_client_user_request(request, db)

    @api_request(clientmobile.RequestFormat)
    def handle_mobile_request(self, request, db, session_user, client_id, le_id):
        return mobilecontroller.process_client_mobile_request(request, db)

    @global_api_request(widgetprotocol.RequestFormat, is_group=True, need_category=True)
    def handle_widget_request(self, request, db, session_user, session_category):
        return controller.process_client_widget_requests(request, db, session_user, session_category)


def handle_isalive():
    return Response("Application is alive", status=200, mimetype="application/json")

#
# run_server
#
def run_server(address, knowledge_server_address):
    ip, port = address

    def delay_initialize():

        api = API(
            address,
            knowledge_server_address,
        )

        api_urls_and_handlers = [
            ("/api/isalive", handle_isalive),
            ("/api/login", api.handle_login),
            ("/api/client_masters", api.handle_client_masters),
            ("/api/client_master_filters", api.handle_client_master_filters),
            ("/api/client_transaction", api.handle_client_transaction),
            ("/api/client_reports", api.handle_client_reports),
            ("/api/client_dashboard", api.handle_client_dashboard),
            ("/api/client_admin_settings", api.handle_client_admin_settings),
            ("/api/general", api.handle_general),
            ("/api/client_user", api.handle_client_user),
            ("/api/mobile", api.handle_mobile_request),
            ("/api/widgets", api.handle_widget_request),
            # (r"/api/files/([a-zA-Z-0-9]+)", api.handle_client_format_file)
        ]
        for url, handler in api_urls_and_handlers:
            app.add_url_rule(url, view_func=handler, methods=['POST'])

        print "Listening at: %s:%s" % (ip, port)

    delay_initialize()
    settings = {
        "threaded": True
    }
    app.run(host="0.0.0.0", port=port, **settings)
