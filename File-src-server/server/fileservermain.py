import base64
import string
import random
import os
import traceback
import json
import requests
import urllib
from zipfile import ZipFile
from constants import CLIENT_DOCS_BASE_PATH
from flask import Flask, Response, request, send_from_directory
from functools import wraps
import fileprotocol
from filecontroller import *
from filehandler import *

app = Flask(__name__)

ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")
EXP_BASE_PATH = os.path.join(ROOT_PATH, "exported_reports")
TEMP_FILE_SERVER = "http://localhost:8083/temp/"


def api_request(
    request_data_type
):
    def wrapper(f):
        @wraps(f)
        def wrapped(self):
            return self.handle_api_request(
                f, request_data_type
            )
        return wrapped
    return wrapper


@app.route('/clientfile', methods=['POST'])
def move_client_files():
    print "CAME IN file SERVER "
    csv_id = request.args.get('csvid')

    legal_entity_id = request.args.get('le_id')
    country_id = request.args.get('c_id')
    domain_id = request.args.get('d_id')
    unit_id = request.args.get('u_id')
    start_date = request.args.get('start_date')
    client_id = request.args.get('client_id')
    if " " in start_date:
        start_date = string_to_datetime(start_date.split(" ")[0]).date()
    else:
        start_date = string_to_datetime(start_date).date()
    year = start_date.year
    month = "%s%s" % (string_months.get(start_date.month), str(year))

    file_path = "%s/%s/%s/%s/%s/%s/%s/%s" % (
        CLIENT_DOCS_BASE_PATH, client_id, country_id, legal_entity_id,
        unit_id, domain_id, year, month
    )
    if not os.path.exists(file_path):
        print "path created ", file_path
        os.makedirs(file_path)

    print "csv_id-> ", csv_id
    actual_zip_file = os.path.join(
        file_path, str(csv_id) + ".zip"
    )
    print "actual_zip_file > ", actual_zip_file
    caller_name = "%sdownloadclientfile?csvid=%s" % (TEMP_FILE_SERVER, csv_id)
    print "download file Cller nameeeeee in file server main ", caller_name
    a, b = urllib.urlretrieve(caller_name, actual_zip_file)
    print "A ", a
    print "b ", b
    # print os.path.getsize(actual_zip_file)
    zip_ref = ZipFile(actual_zip_file, 'r')
    print "zip_ref>>> ", zip_ref
    zip_ref.extractall(file_path)
    zip_ref.close()
    os.remove(actual_zip_file)
    temp_file_server_remove_call(csv_id)
    return "Success Response"


def temp_file_server_remove_call(csv_id):
    caller_name = "%sremoveclientfile?csvid=%s" % (TEMP_FILE_SERVER, csv_id)
    response = requests.post(caller_name)
    print response.text

class API(object):
    def __init__(self):
        pass

    def _send_response(self, response_data, status_code):
        # if type(response_data) is not str and type(response_data) is not Response:
        #     data = response_data.to_structure()
        #     #print data
        #     s = json.dumps(data, indent=2)
        # else:
        # key = ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(5))
        if status_code != 400 :
            data = json.dumps(response_data.to_structure(), indent=2)
        else :
            data = response_data
        print data
        # s = base64.b64encode(data)
        # s = json.dumps(key+s)

        resp = Response(data, status=status_code, mimetype="application/json")
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
        self, request_data_type
    ):
        request_data = None
        # _db = None
        company_id = None
        try:
            data = request.get_json(force=True)
            print "******************"
            print data
            print type(data)
            print len(data)
            if type(data) is not list:
                self._send_response(self.expectation_error("a list", type(data)), 400)

            if len(data) != 2:
                self._send_response("Invalid json format", 400)

            company_id = int(data[0])
            actual_data = data[1]
            print company_id
            # print actual_data
            request_data = request_data_type.parse_structure(
                actual_data
            )
            # print request_data

        except Exception, e:
            print e
            return str(e)
        return request_data, company_id

    def handle_api_request(self, unbound_method, request_data_type):

        def respond(response_data):
            return self._send_response(
                response_data, 200
            )

        ip_address = request.remote_addr
        self._ip_address = ip_address
        print request_data_type
        request_data, company_id = self._parse_request(
            request_data_type
        )
        if request_data is None:
            return

        try:
            response_data = unbound_method(
                self, request_data
            )

            if type(request_data.request) is not fileprotocol.DownloadFile :
                print "send response"
                return respond(response_data)
            else :
                print type(response_data)
                print response_data
                return response_data
        except Exception, e:
            print(traceback.format_exc())
            return self._send_response(str(e), 400)

    @api_request(fileprotocol.RequestFormat)
    def handle_file_upload(self, request):
        print "file_upload"
        return process_file_based_request(request)
        return

    @api_request(fileprotocol.RequestFormat)
    def handle_auto_deletion(self, request):
        print "file_upload"
        return process_auto_deletion_request(request)
        return

def handle_isalive():
    return Response("File server is alive", status=200, mimetype="application/json")

def staticTemplate(pathname, filename):
    return send_from_directory(pathname, filename)
def run_server(address):
    ip, port = address

    def delay_initialize():
        api = API()
        api_urls_and_handlers = [
            ("/api/files", api.handle_file_upload),
            ("/api/isfilealive", handle_isalive),
            ("/api/mobile/files", api.handle_file_upload),
            ("/api/formulatedownload", api.handle_file_upload),
            ("/api/formulatedeldownload", api.handle_auto_deletion),
        ]

        for url, handler in api_urls_and_handlers :
            app.add_url_rule(url, view_func=handler, methods=['POST'])

        STATIC_PATHS = [
            ("/download/export/<path:filename>", EXP_BASE_PATH),
            ("/download/<path:filename>", EXP_BASE_PATH),
            ("/closure/<path:filename>", EXP_BASE_PATH)
        ]
        for path in STATIC_PATHS :
            app.add_url_rule(
                path[0], view_func=staticTemplate, methods=['GET'],
                defaults={'pathname': path[1]}
            )

    print "Listening at %s:%s" % (ip, port)

    delay_initialize()
    settings = {
        "threaded": True
    }
    app.run(host="0.0.0.0", port=port, **settings)
