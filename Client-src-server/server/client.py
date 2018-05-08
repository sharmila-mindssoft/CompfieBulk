import time
import threading
import base64
import random
import string
# from tornado.httpclient import HTTPRequest
import json
import requests
from distribution.protocol import (
    Response, GetCompanyServerDetails
)


#
# __all__
#

__all__ = [
    "CompanyManager"
]


#
# CompanyManager
#


class CompanyManager(object) :
    def __init__(
        self, knowledge_server_address,
        timeout_seconds, server_added_callback
    ) :
        # self._io_loop = io_loop
        self._knowledge_server_address = knowledge_server_address
        # self._http_client = http_client
        self._timeout_seconds = timeout_seconds
        self._server_added_callback = server_added_callback
        self._servers = {}
        ip, port = self._knowledge_server_address
        self._first_time = True
        self._token = None
        # self.get_token(ip, port)
        self._poll_url = "http://%s:%s/knowledge/server-list" % (ip, port)
        print self._poll_url
        # print self._poll_url
        self._request_body = json.dumps(
            GetCompanyServerDetails().to_structure(), indent=2
        )
        # print self._request_body
        self._poll()

    def _poll(self) :
        def on_timeout():
            req_data = self._request_body
            key = ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(5))
            req_data = base64.b64encode(req_data)
            req_data = key+req_data
            # req_data = json.dumps(key+req_data)
            response = requests.post(self._poll_url, data=req_data)

            data = response.text[6:]
            data = str(data).decode('base64')
            # data = json.loads(data)
            # data = json.dumps(key+data)
            self._poll_response(data, response.status_code)

            # self._http_client.fetch(self._request_body, self._poll_response)
            t = threading.Timer(self._timeout_seconds, on_timeout)
            t.daemon = True
            t.start()
        if self._first_time :
            self._first_time = False
            on_timeout()

    def _poll_response(self, response, status_code) :
        # print response.body
        err = "knowledge server poll error:"
        if status_code == 200:
            r = None
            try:
                r = Response.parse_structure(
                    json.loads(response)
                )
            except Exception, e:
                print err, e
                self._poll()
                return
            assert r is not None
            self._servers = []
            for company in r.companies:
                self._servers.append(company)
            self._server_added_callback(self._servers)
        else :
            pass
            print err, response
        self._poll()

    def _get_company_id(self, security_token):
        token = security_token.split("-")
        company_id = 0
        if len(token) == 2:
            try:
                company_id = int(token[0].strip())
            except Exception :
                company_id = 0
        else:
            company_id = self._get_company_id_from_url(
                security_token
            )
        return company_id

    def _get_company_id_from_url(self, url):
        for company_id, company in self._servers.iteritems():
            if company.short_url == url:
                return company_id
        return 0

    def locate_company(self, token):
        company_id = self._get_company_id(token)
        company = self._servers.get(company_id)
        # print company
        if company is None:
            return None
        return company

    def locate_company_server(self, token):
        return self.locate_company(token)

    def locate_company_db_server(self, token):
        return self.locate_company(token)

    def servers(self):
        return self._servers
