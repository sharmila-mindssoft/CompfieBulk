import time
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
        self._poll_url = "http://%s:%s/server-list" % (ip, port)
        print self._poll_url
        body = json.dumps(
            GetCompanyServerDetails().to_structure()
        )
        request = HTTPRequest(
            self._poll_url, method="POST", body=body,
            headers={"Content-Type": "application/json"},
            request_timeout=10
        )
        self._request_body = request
        self._io_loop.add_callback(self._poll)
        self._first_time = True

    def _poll(self) :
        def on_timeout():
            self._http_client.fetch(self._request_body, self._poll_response)
        if self._first_time:
            self._first_time = False
            on_timeout()
            return
        self._io_loop.add_timeout(
            time.time() + self._timeout_seconds, on_timeout
        )

    def _poll_response(self, response) :
        err = "knowledge server poll error:"
        if not response.error :
            r = None
            try:
                r = Response.parse_structure(
                    json.loads(response.body)
                )
            except Exception, e:
                print err, e
                self._poll()
                return
            assert r is not None
            self._servers = {}
            for company in r.companies:
                self._servers[company.company_id] = company
            self._server_added_callback(self._servers)
        else :
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
            if company.short_url == url:
                return company_id
        return 0

    def locate_company(self, token):
        company_id = self._get_company_id(token)
        print "company_id inside locate_company:{}".format(company_id)
        company = self._servers.get(company_id)
        print "company inside locate_company:{}".format(company)
        if company is None:
            return None
        return company

    def locate_company_server(self, token):
        return self.locate_company(token)

    def locate_company_db_server(self, token):
        return self.locate_company(token)

    def servers(self):
        return self._servers
