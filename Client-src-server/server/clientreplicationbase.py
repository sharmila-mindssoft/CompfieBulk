import time
import threading
import base64
import random
import string
import datetime
# from tornado.httpclient import HTTPRequest
import requests
import json
import traceback
from replication.protocol import (
    Response, GetChanges, GetDomainChanges,
    InvalidReceivedCount,
    GetClientChanges
)
from server.clientdatabase.general import (
    get_countries, get_domains, get_trail_id,
    update_traild_id, reset_domain_trail_id
)
import logger

'''
    Replication has been splitted into two process as
      master replication which will replicate all master data to group db.
      compliance replication which will replicate all client-specific compliance data to le db.

'''


#
# __all__
#

__all__ = [
    "ClientReplicationManager",
    "ReplicationBase", "DomainReplicationManager",
    "ReplicationManagerWithBase"
]


class ClientReplicationManager(object) :
    def __init__(
        self, knowledge_server_address,
        timeout_seconds, replication_added_callback
    ) :
        self._knowledge_server_address = knowledge_server_address
        # self._http_client = http_client
        self._timeout_seconds = timeout_seconds
        self._first_time = True
        self._replication_added_callback = replication_added_callback
        self._clients = {}
        ip, port = self._knowledge_server_address
        self._poll_url = "http://%s:%s/knowledge/client-list" % (ip, port)
        print '*' * 100
        print self._poll_url
        self._request_body = json.dumps(
            GetClientChanges().to_structure(), indent=2
        )

    def _start(self):
        self._poll()

    def _poll(self) :

        def on_timeout():
            print "Poll rotated-----------------------------"
            print datetime.datetime.now()
            req_data = self._request_body
            # print req_data
            key = ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(5))
            req_data = base64.b64encode(req_data)

            req_data = key+req_data

            response = requests.post(self._poll_url, data=req_data)

            data = response.text[6:]
            # print data
            data = str(data).decode('base64')
            self._poll_response(data, response.status_code)
            t = threading.Timer(self._timeout_seconds, on_timeout)
            t.daemon = True
            t.start()

            # self._http_client.fetch(self._request_body, self._poll_response)

        if self._first_time:
            self._first_time = False
            on_timeout()

    def _poll_response(self, response, status_code) :
        # print response.error
        # print response.body
        err = "knowledge server poll for client-list "
        if status_code == 200 :
            r = None
            try :
                print json.loads(response)
                r = Response.parse_structure(
                    json.loads(response)
                )
            except Exception, e :
                # print err, e
                self._poll()
                return

            assert r is not None
            self._clients = []
            for client in r.clients :
                # self._clients[client.client_id] = client
                self._clients.append(client)
            self._replication_added_callback(self._clients)

        else :
            pass
            # print err, response

        self._poll()


#
# DomainReplicationManager
#

class ReplicationBase(object):
    def __init__(
        self, knowledge_server_address,
        db, is_group, client_id
    ) :
        # self._io_loop = io_loop
        self._knowledge_server_address = knowledge_server_address
        # self._http_client = http_client
        self._db = db
        self._client_id = client_id
        self._is_group = is_group
        self._received_count = None
        self._temp_count = 0
        self._stop = False
        self._auto_id_columns = {}
        self._load_auto_id_columns()
        self._columns_count = {}
        self._load_columns_count()
        self._countries = []
        self._domains = []
        # self._get_client_countries()
        self._get_client_domains()
        self._type = None

    def _load_auto_id_columns(self):
        self._auto_id_columns = {
            "tbl_client_groups": "client_id",
            "tbl_business_groups": "business_group_id",
            "tbl_legal_entities": "legal_entity_id",
            "tbl_legal_entity_domains": "le_domain_id",
            "tbl_divisions": "division_id",
            "tbl_categories": "category_id",
            "tbl_units": "unit_id",
            "tbl_units_organizations": "unit_org_id",
            "tbl_client_configuration": "client_id",
            "tbl_compliances": "compliance_id",
            "tbl_client_statutories": "client_statutory_id",
            "tbl_client_compliances": "client_compliance_id",
            "tbl_statutory_notifications": "notification_id",
            # "tbl_statutory_notifications_units": "statutory_notification_unit_id",
            "tbl_countries": "country_id",
            "tbl_domains": "domain_id",
            "tbl_validity_date_settings": "validity_date_id",
            "tbl_mapped_industries": "statutory_mapping_id"
        }

    def _load_columns_count(self):
        self._columns_count = {
            "tbl_client_groups": 5,
            "tbl_client_configuration": 5,
            "tbl_business_groups": 2,
            "tbl_legal_entities": 10,
            "tbl_legal_entity_domains": 6,
            "tbl_divisions": 4,
            "tbl_categories": 5,
            "tbl_units": 12,
            "tbl_units_organizations": 4,
            "tbl_compliances": 22,
            "tbl_client_statutories": 3,
            "tbl_client_compliances": 10,
            "tbl_statutory_notifications": 5,
            # "tbl_statutory_notifications_units": 6,
            "tbl_countries": 2,
            "tbl_domains": 2,
            "tbl_validity_date_settings": 4,
            "tbl_mapped_industries": 2
        }

    # def _get_client_countries(self):
    #     country_list = None
    #     self._db.begin()
    #     try:
    #         country_list = get_countries(self._db)
    #         for c in country_list :
    #             self._countries.append(int(c.country_id))
    #         self._db.commit()
    #     except Exception, e :
    #         print e,
    #         self._countries = None
    #         self._db.rollback()
    #     assert self._countries is not None

    def _get_client_domains(self):
        # print "---------------------------"
        self._db.begin()
        try:
            self._domains = get_domains(self._db)
            self._domains

            # for d in domain_list :
            #     self._domains.append(int(d.get("domain_id")))
            #     print self._domains
            #     print "=-=-=-"
            self._db.commit()
        except Exception, e:
            print e
            self._domains = None
            self._db.rollback()
        # assert self._domains is not None

    def _execute_insert_statement(self, changes, error_ok=False):
        assert (len(changes)) > 0
        # print changes
        tbl_name = changes[0].tbl_name
        auto_id = self._auto_id_columns.get(tbl_name)
        # print tbl_name
        column_count = self._columns_count.get(tbl_name)
        # print column_count
        column_count -= 1
        assert auto_id is not None
        if error_ok:
            if column_count != len(changes):
                return
        else:
            if column_count != len(changes):
                return
        # columns = [x.column_name for x in changes]
        i_column = []
        values = []
        domain_id = None
        for x in changes:
            if x.value is None:
                # values.append('')
                pass
            else:
                i_column.append(x.column_name)
                values.append(str(x.value))
                if tbl_name == "tbl_compliances" and x.column_name == "domain_id" :
                    domain_id = int(x.value)
            val = str(values)[1:-1]

        query = "INSERT INTO %s (%s, %s) VALUES(%s, %s)" % (
                tbl_name,
                auto_id,
                ",".join(i_column),
                changes[0].tbl_auto_id,
                val
            )

        if tbl_name == "tbl_compliances" :
            query += " ON DUPLICATE KEY UPDATE compliance_id = values(compliance_id) ;"
        elif tbl_name == "tbl_client_groups" :
            query += " ON DUPLICATE KEY UPDATE client_id = values(client_id) ;"
        elif tbl_name == "tbl_legal_entities" :
            query += " ON DUPLICATE KEY UPDATE legal_entity_id = values(legal_entity_id) ;"
        elif tbl_name == "tbl_units":
            query += " ON DUPLICATE KEY UPDATE unit_id = values(unit_id) ;"
        else :
            query += ""

        try :
            # print domain_id, self._domains
            if self._is_group :
                print "Replication for client ", self._client_id
            else :
                print "Replication for legal entity ", self._client_id
            print tbl_name
            print query
            if tbl_name != "tbl_compliances" :
                self._db.execute(query)
            elif tbl_name == "tbl_compliances" and domain_id in self._domains :
                self._db.execute(query)

            if tbl_name == "tbl_legal_entities" :
                self._db.execute("delete from tbl_legal_entity_domains where legal_entity_id = %s", [auto_id])
            elif tbl_name == "tbl_units" :
                self._db.execute("delete from tbl_units_organizations where unit_id = %s", [auto_id])

            # elif tbl_name == "tbl_client_groups" :
            #     self._db.execute("delete from tbl_client_configuration")

        except Exception, e:
            pass
            print e
            logger.logClient("client.py", "insert", e)
        self._temp_count = changes[-1].audit_trail_id

    def _execute_update_statement(self, change):
        auto_id = self._auto_id_columns.get(change.tbl_name)
        assert auto_id is not None
        val = change.value
        if val is not None :
            # val = "'" + change.value.replace("'", "\\'") + "'"
            query = "UPDATE %s SET %s = '%s' WHERE %s = %s;" % (
                change.tbl_name,
                change.column_name,
                val,
                auto_id,
                change.tbl_auto_id
            )
            try :
                self._db.execute(query)
            except Exception, e :
                print e,
                logger.logClient("client.py", "update", e)
                # print query
                # logger.logClient("client.py", "update", query)
        self._temp_count = change.audit_trail_id
        # print self._temp_count

    def _parse_data(self, changes):
        self._get_received_count()
        # print self._temp_count
        if self._temp_count > self._received_count :
            return

        self._db.begin()

        self._temp_count = self._received_count
        try:
            changes_list = []
            tbl_name = ""
            auto_id = 0
            is_insert = False
            for change in changes:
                # Update
                if change.action == "1":
                    if is_insert:
                        # print "inerst 1 ------------- "
                        self._execute_insert_statement(changes_list)
                    is_insert = False
                    changes_list = []
                    # print "update 1 ---------------"
                    self._execute_update_statement(change)
                else:
                    if is_insert is False:
                        is_insert = True
                        auto_id = change.tbl_auto_id
                        tbl_name = change.tbl_name
                    if auto_id != change.tbl_auto_id or tbl_name != change.tbl_name:
                        # print "insert 2 ---------------"
                        self._execute_insert_statement(changes_list)
                        changes_list = []
                    auto_id = change.tbl_auto_id
                    tbl_name = change.tbl_name
                    changes_list.append(change)
            if is_insert:
                # print "insert 3 -------------------------"
                self._execute_insert_statement(changes_list, error_ok=True)
                changes_list = []
            # print "audit_trail_id updated ", self._temp_count, self._type
            update_traild_id(self._db, self._temp_count, self._type)
            self._received_count = self._temp_count
            self._db.commit()
            # self._temp_count = 0
        except Exception, e:
            # print(traceback.format_exc())
            print e
            logger.logClient("error", "client.py-parse-data", e)
            logger.logClient("error", "client.py", traceback.format_exc())

            self._temp_count = self._received_count
            self._db.rollback()
        assert self._received_count <= self._temp_count
        self._received_count = self._temp_count

class ReplicationManagerWithBase(ReplicationBase):
    def __init__(
        self, knowledge_server_address,
        db, client_id, is_group
    ) :
        super(ReplicationManagerWithBase, self).__init__(
            knowledge_server_address,
            db, is_group, client_id
        )
        self._get_received_count()
        self._client_id = client_id
        self._is_group = is_group
        if self._is_group :
            print "Group db replication ", self._client_id
        else :
            print "LE db repliction ", self._client_id
        ip, port = self._knowledge_server_address
        self._poll_url = "http://%s:%s/knowledge/replication" % (ip, port)
        self._poll_old_data_url = "http://%s:%s/knowledge/delreplicated" % (ip, port)

    def _get_received_count(self):
        # assert self._received_count is None
        self._db.begin()
        try:
            self._received_count = get_trail_id(self._db)
            self._db.commit()
        except Exception, e:
            print e
            self._received_count = None
            self._db.rollback()
        assert self._received_count is not None

    def _poll(self) :
        assert self._stop is False
        assert self._received_count is not None
        print "ReplicationManager poll for client_id = %s, _received_count = %s " % (self._client_id, self._received_count)

        def on_timeout():
            # print "-1-1-1"
            # print time.time()
            if self._stop:
                return

            body = json.dumps(
                GetChanges(
                    self._client_id,
                    self._received_count,
                    self._is_group
                ).to_structure(), indent=2
            )
            key = ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(5))
            req_data = base64.b64encode(body)
            req_data = key+req_data

            response = requests.post(self._poll_url, data=req_data)

            data = response.text[6:]
            data = str(data).decode('base64')
            # print data
            self._poll_response(data, response.status_code)

        t = threading.Timer(10, on_timeout)
        t.daemon = True
        t.start()

    def _poll_response(self, response, status_code) :
        if self._stop:
            return
        err = "knowledge server poll error:"
        if status_code == 200 :
            r = None
            try:
                r = Response.parse_structure(
                    json.loads(response)
                )

            except Exception, e:
                # print err, e
                self._poll()
                return
            if type(r) is InvalidReceivedCount:
                # print "InvalidReceivedCount sent"
                self._poll()
                return
            assert r is not None
            self._parse_data(r.changes)
            # print len(r.changes)
            if len(r.changes) > 0 :
                # print len(r.changes)
                self._poll()
            else :
                return

        else :
            pass
            # print err, response.error
    #
    # poll for delete
    #

    def _poll_for_del(self):
        # print "poll for dell"
        assert self._stop is False
        assert self._received_count is not None

        def on_timeout():
            if self._stop :
                return
            body = json.dumps(
                GetChanges(
                    self._client_id,
                    self._received_count
                ).to_structure()
            )
            request = HTTPRequest(
                self._poll_old_data_url, method="POST",
                body=body,
                headers={"Content-Type": "application/json"},
                request_timeout=10
            )
            self._http_client.fetch(request, self._poll_del_response)
        self._io_loop.add_timeout(time.time() + 43200, on_timeout)

    def _poll_del_response(self, response) :
        if self._stop :
            return
        self._poll_for_del()

    def stop(self):
        self._stop = True

    def start(self):
        self._stop = False
        # print "poll started for ----------- ", self._client_id
        self._poll()
        # self._io_loop.add_callback(self._poll_for_del)


class DomainReplicationManager(ReplicationBase):
    def __init__(
        self, io_loop, knowledge_server_address,
        http_client, db, client_id, domain_id
    ) :
        super(DomainReplicationManager, self).__init__(
            io_loop, knowledge_server_address,
            http_client, db
        )
        self._client_id = client_id
        self._domain_id = domain_id
        self._type = "domain_trail_id"
        self._actual_replica_count = None
        self._received_count = None
        self._get_received_count()
        self._get_domain_received_count()
        ip, port = self._knowledge_server_address
        self._poll_url = "http://%s:%s/knowledge/domain-replication" % (ip, port)

    def _get_received_count(self):
        self._db.begin()
        try:
            self._actual_replica_count = get_trail_id(self._db)
            # print "_actual_replica_count"
            # print self._actual_replica_count
            self._db.commit()
        except Exception, e:
            # print e
            self._actual_replica_count = None
            self._db.rollback()
        assert self._actual_replica_count is not None

    def _get_domain_received_count(self):
        self._db.begin()
        try:
            self._received_count = get_trail_id(self._db, self._type)
            # print "_received_count"
            # print self._received_count
            self._db.commit()
        except Exception, e:
            # print e
            self._received_count = None
            self._db.rollback()

    def _reset_domain_trail_id(self):
        self._db.begin()
        try :
            reset_domain_trail_id(self._db)
            self._db.commit()
        except Exception, e :
            # print e
            self._db.rollback()

    def _poll(self):
        assert self._stop is False
        assert self._received_count is not None
        # print "poll validate"
        # if self._received_count > self._actual_replica_count :
        #     return
        # print "Domain replication poll for client_id = %s, domain_id = %s, _received_count=%s " % (self._client_id, self._domain_id, self._received_count)

        def on_timeout():
            # print time.time()
            # print self._received_count
            if self._stop :
                return

            body = json.dumps(
                GetDomainChanges(
                    self._client_id,
                    self._domain_id,
                    self._received_count,
                    self._actual_replica_count
                ).to_structure()
            )
            request = HTTPRequest(
                self._poll_url, method="POST", body=body,
                headers={"Content-Type": "appliation/json"},
                request_timeout=10
            )
            self._http_client.fetch(request, self._poll_response)
        self._io_loop.add_timeout(
            time.time() + 3, on_timeout
        )

    def _poll_response(self, response) :
        if self._stop :
            return
        # print "poll response receive, actual"
        # print self._received_count, self._actual_replica_count

        # if self._received_count > self._actual_replica_count :
        #     return
        # print "Domain replication poll for client_id = %s, domain_id = %s, _received_count=%s " % (self._client_id, self._domain_id, self._received_count)

        err = "knowledge server poll error for compliances:"
        if not response.error :
            r = None
            try :
                r = Response.parse_structure(
                    json.loads(response.body)
                )
                # print r.to_structure()

            except Exception, e :
                # print err, e
                self._poll()
                return

            if type(r) is InvalidReceivedCount :
                self._poll()
                return

            assert r is not None
            self._parse_data(r.changes)
            # print len(r.changes)
            if len(r.changes) > 0 :
                self._poll()
            else :
                self._reset_domain_trail_id()
                return
        else :
            pass

    def stop(self):
        self._stop = True

    def start(self):
        self._stop = False
        # print "poll started for ", self._client_id
        self._io_loop.add_callback(self._poll)
