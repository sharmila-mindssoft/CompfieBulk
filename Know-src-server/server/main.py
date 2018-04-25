import os
import json
import threading
import traceback
import jinja2
import base64
import random
import string
import logging
import mysql.connector
import controller
import logger
from flask import Flask, request, send_from_directory, Response, render_template
from flask_wtf.csrf import CsrfProtect
from functools import wraps
from lxml import etree
from server.database import general as gen
from protocol import (
    admin, consoleadmin,
    generalprotocol, knowledgemaster, knowledgereport, knowledgetransaction,
    login, technomasters, technoreports, technotransactions,
    clientcoordinationmaster, mobile, domaintransactionprotocol
)

from server.dbase import Database
from distribution.protocol import (
    Request as DistributionRequest,
    CompanyServerDetails,
    ServerDetails
)
from replication.protocol import (
    GetChanges, GetDomainChanges, GetChangesSuccess,
    InvalidReceivedCount, GetDelReplicatedSuccess,
    GetClientChanges, GetClientChangesSuccess
)
from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME,
    IS_DEVELOPMENT, SESSION_CUTOFF, VERSION,
)

from bulkupload.bulkconstants import (
    BULK_UPLOAD_DB_HOST, BULK_UPLOAD_DB_PORT, BULK_UPLOAD_DB_USERNAME,
    BULK_UPLOAD_DB_PASSWORD, BULK_UPLOAD_DATABASE_NAME, REJECTED_DOWNLOAD_PATH

)

from server.templatepath import (
    TEMPLATE_PATHS
)
from server.exceptionmessage import fetch_error
from bulkupload.bulkuploadmain import BulkAPI

from server.userinfo import UserInfo
from server.common import encrypt

ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")

app = Flask(__name__)
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

# base config

csrf = CsrfProtect()
app.secret_key = "MGRkZjg2NTBiNGM0YzAzNmM1NTNhZTZhYTFiZjg1ZThjb21wZmllY29tcGZpZQ=="  # "0ddf8650b4c4c036c553ae6aa1bf85e8compfiecompfie"
app.config["WTF_CSRF_TIME_LIMIT"] = 100000

csrf.init_app(app)

if IS_DEVELOPMENT:
    app.config["debug"] = True
else:
    app.config["debug"] = False

__all__ = [
    "api_request",
    "API"
]
#
# api_request
#
def api_request(request_data_type, need_session_id=False):
    def wrapper(f):
        @wraps(f)
        def wrapped(self):
            return self.handle_api_request(f, request_data_type, need_session_id)
        return wrapped
    return wrapper

def before_first_request():
    cnx_pool = mysql.connector.connect(
        user=KNOWLEDGE_DB_USERNAME,
        password=KNOWLEDGE_DB_PASSWORD,
        host=KNOWLEDGE_DB_HOST,
        database=KNOWLEDGE_DATABASE_NAME,
        port=KNOWLEDGE_DB_PORT,
        autocommit=False,
    )
    return cnx_pool

def bulk_db_connect():
        cnx = mysql.connector.connect(
            user=BULK_UPLOAD_DB_USERNAME,
            password=BULK_UPLOAD_DB_PASSWORD,
            host=BULK_UPLOAD_DB_HOST,
            database=BULK_UPLOAD_DATABASE_NAME,
            port=BULK_UPLOAD_DB_PORT,
            autocommit=False,
        )
        return cnx

#
# API
#
class API(BulkAPI):
    def __init__(
        self, con_pool
    ):
        super(BulkAPI, self).__init__()
        self._con_pool = con_pool
        # self._db_con = dbcon
        self._ip_addess = "127.0.0.1"
        self._remove_old_session()

    def _remove_old_session(self):

        def on_session_timeout():
            print "session timeout"
            _db_con_clr = before_first_request()
            _db_clr = Database(_db_con_clr)
            _db_clr.begin()
            try:
                _db_clr.clear_session(SESSION_CUTOFF)
                _db_clr.commit()
                _db_con_clr.close()

                t = threading.Timer(500, on_session_timeout)
                t.daemon = True
                t.start()

            except Exception, e:
                logger.logKnowledge("error", "remove_old_session", str(e))
                logger.logKnowledge("error", "remove_old_session", str(traceback.format_exc()))
                _db_clr.rollback()

            finally :
                _db_clr.close()
                _db_con_clr.close()

        on_session_timeout()

    def _send_response(
        self, response_data, status_code
    ):
        if type(response_data) is not str :
            data = response_data.to_structure()
            s = json.dumps(data, indent=1)
        else:
            s = response_data
        # print s
        logger.logKnowledge("api", "response", s)
        key = ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(5))
        s = base64.b64encode(s)
        s = json.dumps(key+s)

        resp = Response(s, status=status_code, mimetype="application/json")
        return resp

    def _parse_request(
        self, request_data_type
    ):
        request_data = None
        try:

            if not request.data:
                raise ValueError("Request data is Null")

            data = request.data[5:]
            data = data.decode('base64')
            data = json.loads(data)
            # print data
            logger.logKnowledge("api", "request", data)
            request_data = request_data_type.parse_structure(
                data
            )
            return request_data
        except Exception, e:
            logger.logKnowledge("error", "parse_request", str(e))
            logger.logKnowledge("error", "parse_request", str(traceback.format_exc()))
            raise ValueError("Request Process Failed")

    def respond(self, response_data):
        try :
            return self._send_response(
                response_data, 200
            )
        except Exception, e :
            logger.logKnowledge("error", "respond", str(e))
            logger.logKnowledge("error", "respond", str(traceback.format_exc()))
            raise Exception("Request Process Failed")

    def validate_user_rights(self, request_data, _session_db, caller_name):
        valid_session_data = None
        session_user = None
        if hasattr(request_data, "session_token") :
                session_user = gen.validate_user_rights(_session_db, request_data.session_token, caller_name)
                if session_user is False :
                    valid_session_data = login.InvalidSessionToken()
                    logger.logKnowledge(
                        "info", "invalid_user_session", "user:%s, caller_name:%s, request:%s" % (session_user, caller_name, request.url)
                    )
        print valid_session_data, session_user

        if valid_session_data is None and session_user is not False :
            if hasattr(request_data, "request") :
                if hasattr(request_data.request, "password") and type(request_data.request) != consoleadmin.SaveDBServer:
                    print "password validation"
                    enc_pwd = encrypt(request_data.request.password)
                    if gen.verify_password(_session_db, session_user, enc_pwd) == 0 :
                        valid_session_data = login.InvalidPassword()
                        logger.logKnowledge(
                            "info", "invalid_user_password", "user:%s, caller_name:%s, request:%s" % (session_user, caller_name, request.url)
                        )
        return valid_session_data, session_user

    def handle_api_request(
        self, unbound_method, request_data_type, need_session_id
    ):
        is_bulk_upload = False
        # self._ip_addess = request.remote_addr
        self._ip_addess = request.headers.get("X-Real-Ip")
        caller_name = request.headers.get("Caller-Name")

        api_type = request.url

        try:
            if request_data_type == "knowledgeformat":
                request_data = request
            else:
                request_data = self._parse_request(
                    request_data_type
                )

            if request_data is None:
                raise ValueError("Request data is Null")

            elif type(request_data) is str:
                raise ValueError(request_data)
            if "/api/bu" in api_type :
                is_bulk_upload = True
                _db_con = bulk_db_connect()
            else :
                _db_con = before_first_request()

            _db = Database(_db_con)
            _db.begin()

            valid_session_data = None
            session_user = None
            _session_db = None
            _session_db_con = None

            print is_bulk_upload
            if is_bulk_upload is True:
                _session_db_con = before_first_request()
                _session_db = Database(_session_db_con)
                _session_db.begin()
                valid_session_data, session_user = self.validate_user_rights(request_data, _session_db, caller_name)
                if valid_session_data is None :
                    session_user = UserInfo(_session_db, session_user)
                _session_db.commit()

            else :
                valid_session_data, session_user = self.validate_user_rights(request_data, _db, caller_name)

            if valid_session_data is None :
                if need_session_id is True :
                    response_data = unbound_method(self, request_data, _db, session_user)
                else :
                    response_data = unbound_method(self, request_data, _db)
            else :
                response_data = valid_session_data

            if response_data is None or type(response_data) is bool:
                _db.rollback()
                raise fetch_error()

            elif type(response_data) != technomasters.ClientCreationFailed:
                _db.commit()
            else:
                _db.rollback()

            _db.close()
            _db_con.close()
            return self.respond(response_data)

        except Exception, e:
            logger.logKnowledge("error", "handle_api_request", str(e))
            logger.logKnowledge("error", "handle_api_request", str(traceback.format_exc()))

            if str(e).find("expected a") is False:
                _db.rollback()
                _db.close()
                _db_con.close()

            return self._send_response(str(e), 400)

    @csrf.exempt
    @api_request(DistributionRequest)
    def handle_server_list(self, request, db):
        return CompanyServerDetails(gen.get_servers(db))

    @csrf.exempt
    @api_request(DistributionRequest)
    def handle_group_server_list(self, request, db):
        return ServerDetails(
            gen.get_group_servers(db),
            gen.get_ip_details(db)
        )

    @csrf.exempt
    @api_request(GetClientChanges)
    def handle_client_list(self, request, db):
        return GetClientChangesSuccess(
            gen.get_client_replication_list(db)
        )

    @csrf.exempt
    @api_request(GetChanges)
    def handle_replication(self, request, db):

        client_id = request.client_id
        received_count = request.received_count
        is_group = request.is_group
        res = GetChangesSuccess(
            gen.get_trail_log(db, client_id, received_count, is_group)
        )
        return res

    @csrf.exempt
    @api_request(GetDomainChanges)
    def handle_domain_replication(self, request, db):
        actual_count = gen.get_trail_id(db)
        client_id = request.client_id
        domain_id = request.domain_id
        received_count = request.received_count
        actual_replica_count = request.actual_count

        if received_count > actual_count:
            gen.update_replication_count(db, client_id)
            return InvalidReceivedCount()

        res = GetChangesSuccess(
            gen.get_trail_log_for_domain(
                db, client_id, domain_id, received_count,
                actual_replica_count
            )
        )
        return res

    @csrf.exempt
    @api_request(GetChanges)
    def handle_delreplicated(self, request, db):
        actual_count = gen.get_trail_id(db)

        client_id = request.client_id
        received_count = request.received_count
        if actual_count >= received_count:
            gen.remove_trail_log(client_id, received_count)
        return GetDelReplicatedSuccess()

    @csrf.exempt
    @api_request(login.Request)
    def handle_login(self, request, db):
        return controller.process_login_request(request, db, self._ip_addess)

    @csrf.exempt
    @api_request(login.Request)
    def handle_mobile_login_request(self, request, db):
        return controller.process_mobile_login_request(request, db, self._ip_addess)

    @csrf.exempt
    @api_request(mobile.RequestFormat, need_session_id=True)
    def handle_mobile_request(self, request, db, session_user):
        return controller.process_mobile_request(request, db, self._ip_addess, session_user)

    @api_request(admin.RequestFormat, need_session_id=True)
    def handle_admin(self, request, db, session_user):
        return controller.process_admin_request(request, db, session_user)

    @api_request(consoleadmin.RequestFormat, need_session_id=True)
    def handle_console_admin(self, request, db, session_user):
        return controller.process_console_admin_request(request, db, session_user)

    @api_request(technomasters.RequestFormat, need_session_id=True)
    def handle_techno(self, request, db, session_user):
        return controller.process_techno_request(request, db, session_user)

    @api_request(generalprotocol.RequestFormat, need_session_id=True)
    def handle_general(self, request, db, session_user):
        return controller.process_general_request(request, db, session_user)

    @api_request(knowledgemaster.RequestFormat, need_session_id=True)
    def handle_knowledge_master(self, request, db, session_user):
        return controller.process_knowledge_master_request(request, db, session_user)

    @api_request(knowledgetransaction.RequestFormat, need_session_id=True)
    def handle_knowledge_transaction(self, request, db, session_user):
        return controller.process_knowledge_transaction_request(request, db, session_user)

    @api_request(knowledgereport.RequestFormat, need_session_id=True)
    def handle_knowledge_report(self, request, db, session_user):
        return controller.process_knowledge_report_request(request, db, session_user)

    @api_request(technotransactions.RequestFormat, need_session_id=True)
    def handle_techno_transaction(self, request, db, session_user):
        return controller.process_techno_transaction_request(request, db, session_user)

    @api_request(technoreports.RequestFormat, need_session_id=True)
    def handle_techno_report(self, request, db, session_user):
        return controller.process_techno_report_request(request, db, session_user)

    @api_request(clientcoordinationmaster.RequestFormat, need_session_id=True)
    def handle_client_coordination_master(self, request, db, session_user):
        return controller.process_client_coordination_master_request(
            request, db, session_user
        )

    @csrf.exempt
    @api_request(domaintransactionprotocol.RequestFormat, need_session_id=True)
    def handle_domain_transaction(self, request, db, session_user):
        return controller.process_domain_transaction_request(request, db, session_user)

    @api_request("knowledgeformat")
    def handle_format_file(self, request, db):
        info = request.files
        response_data = controller.process_uploaded_file(info, "knowledge")
        return response_data

template_loader = jinja2.FileSystemLoader(
    os.path.join(ROOT_PATH, "Know-src-client")
)
app.jinja_loader = template_loader

TEMP_PATH = os.path.join(ROOT_PATH, "Know-src-client", "files")
KNOW_PATH = os.path.join(TEMP_PATH, "knowledge")
COMMON_PATH = os.path.join(KNOW_PATH, "common")
JS_PATH = os.path.join(COMMON_PATH, "js")
CSS_PATH = os.path.join(COMMON_PATH, "css")
IMG_PATH = os.path.join(COMMON_PATH, "images")
FONT_PATH = os.path.join(COMMON_PATH, "fonts")
SCRIPT_PATH = os.path.join(TEMP_PATH, "knowledge")
LOGO_PATH = os.path.join(ROOT_PATH, "Know-src-server", "server", "clientlogo")
DOC_PATH = os.path.join(ROOT_PATH, "Know-src-server", "server", "knowledgeformat")

CSV_PATH = os.path.join(ROOT_PATH, "exported_reports")

BULK_CSV_FORMAT_PATH = os.path.join(ROOT_PATH, "bulkuploadcsvformat")
BULK_CSV_UPLOAD_PATH = os.path.join(ROOT_PATH, "bulkuploadcsv")
BULK_CSV_INVALID_PATH = os.path.join(ROOT_PATH, "bulkuploadinvalid")
BULK_CSV_UPLOAD_PATH_CSV = os.path.join(ROOT_PATH, "bulkuploadcsv/csv")

STATIC_PATHS = [
    ("/knowledge/css/<path:filename>", CSS_PATH),
    ("/knowledge/js/<path:filename>", JS_PATH),
    ("/knowledge/images/<path:filename>", IMG_PATH),
    ("/knowledge/fonts/<path:filename>", FONT_PATH),
    ("/knowledge/script/<path:filename>", SCRIPT_PATH),
    ("/knowledge/clientlogo/<path:filename>", LOGO_PATH),
    ("/clientlogo/<path:filename>", LOGO_PATH),
    ("/knowledge/downloadcsv/<path:filename>", CSV_PATH),
    ("/knowledge/compliance_format/<path:filename>", DOC_PATH),
    ("/compliance_format/<path:filename>", DOC_PATH),
    ("/csv_format/<path:filename>", BULK_CSV_FORMAT_PATH),
    ("/uploaded_file/<path:filename>", BULK_CSV_UPLOAD_PATH),
    ("/uploaded_file/csv/<path:filename>", BULK_CSV_UPLOAD_PATH_CSV),
    ("/invalid_file/<path:filename>", BULK_CSV_INVALID_PATH),
    ("/knowledge/rejected/downloads/<path:filename>", REJECTED_DOWNLOAD_PATH),
]

def staticTemplate(pathname, filename):
    return send_from_directory(pathname, filename)


def renderTemplate(pathname, code=None):
    def set_path(url):
        if url.startswith("/"):
            new_url = "/knowledge" + url
        else :
            new_url = "/knowledge/" + url
        return new_url

    def update_static_urls(content):
        v = VERSION
        data = "<!DOCTYPE html>"
        parser = etree.HTMLParser()
        tree = etree.fromstring(content, parser)

        for node in tree.xpath('//*[@src]'):
            url = node.get('src')
            new_url = set_path(url)
            new_url += "?v=%s" % (v)
            node.set('src', new_url)
        for node in tree.xpath('//*[@href]'):
            if node.tag != "link":
                continue

            url = node.get('href')
            if not url.startswith("#"):
                new_url = set_path(url)
                new_url += "?v=%s" % (v)
            else:
                new_url = url

            node.set('href', new_url)
        data += etree.tostring(tree, method="html")
        return data

    output = render_template(pathname)
    output = update_static_urls(output)
    return output

#
# run_server
#
def run_server(port):

    def delay_initialize():
        mysqlConPool = before_first_request()
        api = API(mysqlConPool)
        print "%" * 50

        api_urls_and_handlers = [
            ("/knowledge/server-list", api.handle_server_list),
            ("/knowledge/group-server-list", api.handle_group_server_list),
            ("/knowledge/client-list", api.handle_client_list),
            ("/knowledge/replication", api.handle_replication),
            ("/knowledge/domain-replication", api.handle_domain_replication),
            ("/knowledge/delreplicated", api.handle_delreplicated),
            ("/knowledge/api/login", api.handle_login),
            ("/knowledge/api/admin", api.handle_admin),
            ("/knowledge/api/console_admin", api.handle_console_admin),
            ("/knowledge/api/techno", api.handle_techno),
            ("/knowledge/api/general", api.handle_general),
            ("/knowledge/api/knowledge_master", api.handle_knowledge_master),
            ("/knowledge/api/knowledge_transaction", api.handle_knowledge_transaction),
            ("/knowledge/api/knowledge_report", api.handle_knowledge_report),
            ("/knowledge/api/techno_transaction", api.handle_techno_transaction),
            ("/knowledge/api/techno_report", api.handle_techno_report),
            ("/knowledge/api/domain_transaction", api.handle_domain_transaction),
            ("/knowledge/api/files", api.handle_format_file),
            ("/knowledge/api/client_coordination_master", api.handle_client_coordination_master),
            ("/knowledge/api/mobile/login", api.handle_mobile_login_request),
            ("/knowledge/api/mobile", api.handle_mobile_request),

        ]

        # api urls for bulk-upload
        api_urls_and_handlers.extend(api.bulk_upload_api_urls())

        for idx, path in enumerate(TEMPLATE_PATHS):
            app.add_url_rule(
                path[0], view_func=renderTemplate, methods=['GET'],
                defaults={'pathname': path[1]}
            )

        for path in STATIC_PATHS:
            app.add_url_rule(
                path[0], view_func=staticTemplate, methods=['GET'],
                defaults={'pathname': path[1]}
            )

        for u in api_urls_and_handlers:
            app.add_url_rule(u[0], view_func=u[1], methods=['POST'])

        print "Listening port: %s" % port

    delay_initialize()
    settings = {
        "threaded": True
    }
    app.run(host="0.0.0.0", port=port, **settings)
