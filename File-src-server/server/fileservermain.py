import traceback
import json
from flask import Flask, Response, request
from functools import wraps
import fileprotocol
from filecontroller import *

app = Flask(__name__)

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


class API(object):
    def __init__(self):
        pass

    def _send_response(self, response_data, status_code):
        if type(response_data) is not str and type(response_data) is not Response:
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
        self, request_data_type
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
            # print company_id
            request_data = request_data_type.parse_structure(
                actual_data
            )

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
                return respond(response_data)
            else :
                return response_data
        except Exception, e:
            print(traceback.format_exc())
            return self._send_response(str(e), 400)

    @api_request(fileprotocol.RequestFormat)
    def handle_file_upload(self, request):
        print "file_upload"
        return process_file_based_request(request)

def handle_isalive():
    return Response("File server is alive", status=200, mimetype="application/json")

def run_server(address):
    ip, port = address

    def delay_initialize():
        api = API()
        api_urls_and_handlers = [
            ("/api/files", api.handle_file_upload),
            ("/api/isalive", handle_isalive)
        ]

        for url, handler in api_urls_and_handlers :
            app.add_url_rule(url, view_func=handler, methods=['POST'])

    print "Listening at %s:%s" % (ip, port)

    delay_initialize()
    settings = {
        "threaded": True
    }
    app.run(host="0.0.0.0", port=port, **settings)
