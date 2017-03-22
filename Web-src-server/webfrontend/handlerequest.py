import json
import string
import random
import base64
from tornado.httpclient import HTTPRequest

# from server import logger


#
# HandleRequest
#

class HandleRequest(object):
    def __init__(
        self,
        security_token, body, relative_url, response,
        http_client, remote_ip, company_manager
    ):
        self._security_token = security_token
        self._body = body
        self._relative_url = relative_url
        self._http_response = response
        self._http_client = http_client
        self._remote_ip = remote_ip
        self._company_manager = company_manager
        self._url_template = "http://%s:%s%s"
        self._connection_closed = False
        self._company_id = 0
        self._url = None
        print "In Handle request"
        print relative_url

    def _api_request(self, url, body, callback):
        def client_callback(response):
            code = response.code
            body = response.body
            headers = response.headers
            if code == 200:
                callback(None, body, headers)
            else:
                callback(code, body, headers)

        body = json.dumps([self._company_id, body])

        request = HTTPRequest(
            url,
            method="POST",
            body=body,
            headers={
                "Content-Type": "application/json",
                "X-Real-Ip": self._remote_ip
            },
            request_timeout=100
        )
        self._http_client.fetch(request, client_callback)

    def _respond(self, response_data, headers):
        assert self._connection_closed is False
        # print headers
        # print self._url
        print type(response_data)
        print "begin response"
        if len(headers) == 6 :
            for k, v in headers.items() :
                self._http_response.set_default_header(k, v)
        else :
            self._http_response.set_default_header(
                "Content-Type", "application/json"
            )
            response_data = json.dumps(json.loads(response_data), indent=2)
            print response_data
            key = ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(5))
            response_data = base64.b64encode(response_data)
            response_data = json.dumps(key+response_data)
            self._http_response.set_default_header(
                "Content-Length", len(response_data)
            )

        self._http_response.set_default_header(
            "Access-Control-Allow-Origin", "*"
        )

        self._http_response.send(response_data)
        self._connection_closed = True
        print "response end"

    def _respond_error(self, code, response_data):
        self._http_response.set_status(code)
        self._http_response.send(response_data)

    def _respond_not_found(self):
        self._http_response.set_status(404)
        self._http_response.send("client not found")

    def _respond_connection_timeout(self):
        self._http_response.set_status(500)
        self._http_response.send("Request timeout")

    def _forward_request_callback(self, code, response_data, headers):
        if self._connection_closed:
            return
        if code is None:
            self._respond(response_data, headers)
        elif code == 599 :
            self._respond_connection_timeout()
        else:
            print "error", code
            self._respond_error(code, response_data)

    def forward_request(self):
        company = self._company_manager.locate_company_server(
            self._security_token
        )

        if company is None:
            self._respond_not_found()
            return
        self._company_id = company.company_id
        file_server_ip = None
        ip = None
        port = None
        if self._relative_url == "/api/files" :
            legal_entity_id = self._body["request"][1]["le_id"]
        else :
            legal_entity_id = None

        if legal_entity_id is not None :
            for f in company.file_server_info :
                if f.legal_entity_id == legal_entity_id :
                    file_server_ip = f.file_server_ip
                    break

            if file_server_ip is None :
                self._respond_not_found()
                return
            else :
                ip = file_server_ip.ip_address
                port = file_server_ip.port
        else :
            company_server_ip = company.company_server_ip
            ip = company_server_ip.ip_address
            port = company_server_ip.port

        assert ip is not None
        assert port is not None
        url = self._url_template % (ip, port, self._relative_url)
        self._url = url
        print "before request call"
        print self._url
        print "$" * 100
        self._api_request(
            url, self._body, self._forward_request_callback
        )

    def connection_closed(self):
        self._connection_closed = True
