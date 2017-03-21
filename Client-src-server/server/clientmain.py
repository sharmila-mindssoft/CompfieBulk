import os
import json
import traceback
import threading
import datetime
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
from server.clientdatabase.savelegalentitydata import(
    LegalEntityReplicationManager, LEntityReplicationUSer,
    LEntityReplicationServiceProvider, LEntityUnitClosure,
    LEntitySettingsData
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
        self._replication_legal_entity = {}
        self._company_manager = CompanyManager(
            knowledge_server_address,
            5000,
            self.server_added
        )
        # print "Databases initialize"

        self._ip_address = None
        self._remove_old_session()
        self._notify_occurrence_task()

    def _remove_old_session(self):

        def _with_client_info():
            for c_id, c_db in self._group_databases.iteritems() :
                on_session_timeout(c_db)

            t = threading.Timer(500, _with_client_info)
            t.daemon = True
            t.start()

        def on_session_timeout(c_db):
            print "session called "
            print datetime.datetime.now()
            c_db_con = self.client_connection_pool(c_db)
            _db_clr = Database(c_db_con)
            try :
                _db_clr.begin()
                _db_clr.clear_session(SESSION_CUTOFF)
                _db_clr.commit()
                c_db_con.close()

            except Exception, e :
                print e
                _db_clr.rollback()
                c_db_con.close()

        _with_client_info()

    def _notify_occurrence_task(self):

        def _with_le_info():
            for c_id, c_db in self._le_databases.iteritems() :
                on_session_timeout(c_db)

            t = threading.Timer(500, _with_le_info)
            t.daemon = True
            t.start()

        def on_session_timeout(c_db):
            print "session called "
            print datetime.datetime.now()
            c_db_con = self.client_connection_pool(c_db)
            _db_clr = Database(c_db_con)
            try :
                _db_clr.begin()
                _db_clr.get_onoccurance_compliance_to_notify()
                _db_clr.commit()
                c_db_con.close()

            except Exception, e :
                print e
                _db_clr.rollback()
                c_db_con.close()

        _with_le_info()

    def close_connection(self, db):
        try:
            db.close()
        except Exception:
            pass

    def client_connection_pool(self, data):
        try:
            return mysql.connector.connect(
                autocommit=False,
                user=data.db_username,
                password=data.db_password,
                host=data.db_ip.ip_address,
                database=data.db_name,
                port=data.db_ip.port
            )
        except Exception:
            raise Exception("Client Connection Failed")

    def server_added(self, servers):
        self._group_databases = {}
        self._le_databases = {}
        self._replication_managers_for_group = {}
        self._replication_managers_for_le = {}
        self._replication_legal_entity = {}
        try:

            for company in servers:
                company.to_structure()
                company_id = company.company_id
                company_server_ip = company.company_server_ip
                ip, port = self._address
                # print company.to_structure()
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
                                # print " %s added in connection pool" % company_id
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
                                # print " %s added in le connection pool" % company_id
                            except Exception, e:
                                # when db connection failed continue to the next server
                                logger.logClientApi(ip, port)
                                logger.logClientApi(e, "LE database added")
                                logger.logClient("error", "exception", str(traceback.format_exc()))
                                logger.logClient("error", "clientmain.py-le_database-added", e)
                                logger.logClientApi("LE database not available to connect ", str(company_id) + "-" + str(company.to_structure()))
                                continue

            # print self._le_databases
            # print self._group_databases

            def client_added(clients):
                for client in clients:
                    _client_id = client.client_id
                    is_new_data = client.is_new_data
                    is_new_domain = client.is_new_domain

                    if client.is_group is True:

                        db_cons_info = self._group_databases.get(_client_id)
                        if db_cons_info is None :
                            continue

                        if is_new_data is True and is_new_domain is False :
                            # replication for group db only master data

                            db_cons = self.client_connection_pool(db_cons_info)
                            client_db = Database(db_cons)
                            client_db.set_owner_id(_client_id)
                            if client_db is not None :
                                rep_man = ReplicationManagerWithBase(
                                    self._knowledge_server_address,
                                    client_db,
                                    _client_id,
                                    client.is_group
                                )
                                if self._replication_managers_for_group.get(_client_id) is None :
                                    pass
                                else :
                                    self._replication_managers_for_group[_client_id].stop()
                                rep_man.start()
                                self._replication_managers_for_group[_client_id] = rep_man

                    else :
                        db_cons_info = self._le_databases.get(_client_id)
                        if db_cons_info is None :
                            continue

                        if is_new_data is True and is_new_domain is False :
                            # replication for group db only master data
                            db_cons = self.client_connection_pool(db_cons_info)
                            le_db = Database(db_cons)
                            le_db.set_owner_id(_client_id)
                            if le_db is not None :
                                rep_le_man = ReplicationManagerWithBase(
                                    self._knowledge_server_address,
                                    le_db,
                                    _client_id,
                                    client.is_group
                                )
                                if self._replication_managers_for_le.get(_client_id) is None :
                                    pass
                                else :
                                    self._replication_managers_for_le[_client_id].stop()

                                rep_le_man.start()
                                self._replication_managers_for_le[_client_id] = rep_le_man

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

            # Knowledge data replciation process for group admin legal entity db
            _client_manager = ClientReplicationManager(
                self._knowledge_server_address,
                60,
                client_added
            )
            # replication start
            _client_manager._start()

            # group data replication process corresponding legal entity database
            for k, gp in self._group_databases.items():
                gp_info = self._group_databases.get(k)
                gp_id = gp_info.company_id
                _le_entity = LegalEntityReplicationManager(gp_info, 10, self.legal_entity_replication_added)
                _le_entity._start()
                self._replication_legal_entity[gp_id] = _le_entity
        except Exception, e :
            logger.logClientApi(e, "Server added")
            logger.logClientApi(traceback.format_exc(), "")
            logger.logClient("error", "clientmain.py-server-added", e)
            logger.logClient("error", "clientmain.py-server-added", traceback.format_exc())
            return

    def legal_entity_replication_added(self, group_info, le_infos):
        for r in le_infos :
            le_id = r["legal_entity_id"]
            le_info = self._le_databases.get(le_id)
            if r["user_data"] == 1 :
                info = LEntityReplicationUSer(group_info, le_info, le_id)
                info._start()

            if r["provider_data"] == 1 :
                info = LEntityReplicationServiceProvider(group_info, le_info, le_id)
                info._start()

            if r["settings_data"] == 1 :
                info = LEntitySettingsData(group_info, le_info, le_id)
                info._start()

    def _send_response(
        self, response_data, status_code
    ):
        if type(response_data) is not str :
            data = response_data.to_structure()
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
        company_id = None
        try:
            data = request.get_json(force=True)
            if type(data) is not list:
                self._send_response(self.expectation_error("a list", type(data)), 400)

            if len(data) != 2:
                self._send_response("Invalid json format", 300)

            company_id = int(data[0])
            actual_data = data[1]
            request_data = request_data_type.parse_structure(
                actual_data
            )
            if is_group is False :
                company_id = request_data.request.legal_entity_id

        except Exception, e:
            print e
            logger.logClientApi(e, "_parse_request")
            logger.logClientApi(traceback.format_exc(), "")
            print(traceback.format_exc())
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

        try :
            _group_db_cons = self.client_connection_pool(_group_db_info)
            _group_db = Database(_group_db_cons)
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

        is_valid = False
        try :
            _group_db_cons = self.client_connection_pool(_group_db_info)
            _group_db = Database(_group_db_cons)
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
                    return respond(clientlogin.InvalidPassword())

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

        try:
            _db_con = self.client_connection_pool(db_cons_info)
            _db = Database(_db_con)
            _db.set_owner_id(company_id)
            if _db_con is None:
                self._send_response("Company not found", 404)

            _db.begin()
            if need_client_id :
                response_data = unbound_method(
                    self, request_data, _db, company_id, ip_address
                )
            elif is_group is True and need_category is True :
                response_data = unbound_method(
                    self, request_data, _db, session_user, client_id, session_category
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
                    print performed_les
                    p_response.chart_data = controller.merge_compliance_status(p_response.chart_data)

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

                elif type(request_data.request) is dashboard.GetStatutoryNotifications :
                    p_response.statutory.extend(data.statutory)

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

                elif type(request_data.request) is widgetprotocol.GetUserScoreCard :
                    p_response = controller.merge_user_scorecard(p_response, data)

                elif type(request_data.request) is widgetprotocol.GetDomainScoreCard :
                    if type(data) is widgetprotocol.ChartSuccess :
                        p_response = controller.merge_domain_scorecard(p_response, data)

                elif type(request_data.request) is widgetprotocol.GetCalendarView :
                    p_response = controller.merge_calendar_view(p_response, data)

                elif type(request_data.request) is widgetprotocol.GetRiskChart :
                    print "----------------------------------------------"
                    p_response = controller.merge_risk_chart_widget(p_response, data)

                else :
                    print "Else --------------"
                    pass
            return p_response

        try :
            # print "try"
            request_data, company_id = self._parse_request(request_data_type, is_group)
            session = request_data.session_token
            session_user, client_id, session_category = self._validate_user_session(session)

            if session_user is False :
                return respond(clientlogin.InvalidSessionToken())

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

                    try:
                        _db_con = self.client_connection_pool(db_cons_info)
                        _db = Database(_db_con)
                        _db.set_owner_id(le)
                        if _db_con is None:
                            performed_les.append(le)
                            continue
                            # return self._send_response("Company not found", 404)

                        _db.begin()

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

    @api_request(clientmasters.RequestFormat, is_group=True, need_category=True)
    def handle_client_masters(self, request, db, session_user, client_id, session_category):
        res = controller.process_client_master_requests(request, db, session_user, client_id, session_category)
        if type(res) is clientmasters.SaveUnitClosureSuccess :
            data = request.request
            le_id = data.legal_entity_id
            le_db_info = self._le_databases.get(le_id)
            gp_info = self._group_databases.get(client_id)
            LEntityUnitClosure(gp_info, le_db_info, le_id, data, session_user)._start()
        return res

    @api_request(clienttransactions.RequestFormat, is_group=True, need_category=True)
    def handle_client_master_filters(self, request, db, session_user, client_id, session_category):
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
        return controller.process_client_user_request(request, db, session_user)

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
        ]
        for url, handler in api_urls_and_handlers:
            app.add_url_rule(url, view_func=handler, methods=['POST'])

        print "Listening at: %s:%s" % (ip, port)

    delay_initialize()
    settings = {
        "threaded": True,
        "debug": True
    }
    app.run(host="0.0.0.0", port=port, **settings)
