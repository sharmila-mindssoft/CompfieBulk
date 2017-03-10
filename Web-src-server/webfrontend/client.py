import base64
import time
import random
import string
from tornado.httpclient import HTTPRequest
import json
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
        self, io_loop, knowledge_server_address, http_client,
        timeout_seconds, server_added_callback
    ) :
        self._io_loop = io_loop
        self._knowledge_server_address = knowledge_server_address
        self._http_client = http_client
        self._timeout_seconds = timeout_seconds
        self._server_added_callback = server_added_callback
        self._servers = {}
        ip, port = self._knowledge_server_address
        self._first_time = True
        self._token = None
        self._poll_url = "http://%s:%s/knowledge/group-server-list" % (ip, port)
        body = json.dumps(
            GetCompanyServerDetails().to_structure(), indent=2
        )
        body = body.encode('base64')
        key = ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(5))
        body = key + body
        request = HTTPRequest(
            self._poll_url, method="POST", body=body,
            headers={
                "Content-Type": "application/json",
            },
            request_timeout=10
        )
        self._request_body = request
        self._io_loop.add_callback(self._poll)

    def _poll(self) :
        def on_timeout():
            req_data = self._request_body

            self._http_client.fetch(req_data, self._poll_response)
        if self._first_time:
            self._first_time = False
            on_timeout()
            return
        self._io_loop.add_timeout(
            time.time() + self._timeout_seconds, on_timeout
        )

    def _poll_response(self, response) :
        # print response.body
        err = "knowledge server poll error:"
        if not response.error :
            r = None
            try:
                data = response.body[6:]
                data = str(data).decode('base64')
                # print data
                r = Response.parse_structure(
                    json.loads(data)
                )
            except Exception, e:
                print err, e
                self._poll()
                return
            assert r is not None
            self._servers = {}
            for company in r.servers:
                if company.is_group is False:
                    continue
                self._servers[company.company_id] = company
            self._server_added_callback(self._servers)
        else :
            pass
            print err, response.error
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
            if company.is_group is False :
                continue

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
