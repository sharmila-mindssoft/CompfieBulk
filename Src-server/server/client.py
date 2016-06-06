import time
from tornado.httpclient import HTTPRequest
import json
import traceback
from replication.protocol import (
    Response, GetChanges, GetDomainChanges,
    InvalidReceivedCount,
    GetClientChanges
)

import logger


#
# __all__
#

__all__ = [
    "ReplicationManager", "ClientReplicationManager",
    "ReplicationBase", "DomainReplicationManager",
    "ReplicationManagerWithBase"
]


class ClientReplicationManager(object) :
    def __init__(
        self, io_loop, knowledge_server_address,
        http_client, timeout_seconds, replication_added_callback
    ) :
        self._io_loop = io_loop
        self._knowledge_server_address = knowledge_server_address
        self._http_client = http_client
        self._timeout_seconds = timeout_seconds
        self._first_time = True
        self._replication_added_callback = replication_added_callback
        self._clients = {}
        ip, port = self._knowledge_server_address
        self._poll_url = "http://%s:%s/knowledge/client-list" % (ip, port)
        # print
        # print self._poll_url
        body = json.dumps(
            GetClientChanges().to_structure()
        )
        # print body
        request = HTTPRequest(
            self._poll_url, method="POST", body=body,
            headers={"Content-Type": "application/json"},
            request_timeout=10
        )
        self._request_body = request
        self._io_loop.add_callback(self._poll)

    def _poll(self) :
        # print "client list call"
        # self._http_client.fetch(self._request_body, self._poll_response)

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
        # print response.error
        # print response.body
        err = "knowledge server poll for client-list "
        if not response.error :
            r = None
            try :
                r = Response.parse_structure(
                    json.loads(response.body)
                )
            except Exception, e :
                print err, e
                self._poll()
                return
            assert r is not None
            self._clients = {}
            for client in r.clients :
                self._clients[client.client_id] = client
            self._replication_added_callback(self._clients)

        else :
            pass

        self._poll()


#
# ReplicationManager
#

class ReplicationManager(object) :
    def __init__(
        self, io_loop, knowledge_server_address, http_client,
        db, client_id
    ) :
        self._io_loop = io_loop
        self._knowledge_server_address = knowledge_server_address
        self._http_client = http_client
        self._db = db
        self._client_id = client_id
        self._received_count = None
        self._temp_count = 0
        self._stop = False
        self._auto_id_columns = {}
        self._load_auto_id_columns()
        self._columns_count = {}
        self._load_columns_count()
        self._get_received_count()
        ip, port = self._knowledge_server_address
        self._poll_url = "http://%s:%s/knowledge/replication" % (ip, port)
        self._poll_old_data_url = "http://%s:%s/knowledge/delreplicated" % (ip, port)
        # print "_received_count ================ " , self._received_count
        self._countries = []
        self._domains = []
        self._get_client_countries()
        self._get_client_domains()

    def _load_auto_id_columns(self):
        self._auto_id_columns = {
            "tbl_client_groups": "client_id",
            "tbl_business_groups": "business_group_id",
            "tbl_legal_entities": "legal_entity_id",
            "tbl_divisions": "division_id",
            "tbl_units": "unit_id",
            "tbl_client_configurations": "client_config_id",
            "tbl_compliances": "compliance_id",
            "tbl_client_statutories": "client_statutory_id",
            "tbl_client_compliances": "client_compliance_id",
            "tbl_statutory_notifications_log": "statutory_notification_id",
            "tbl_statutory_notifications_units": "statutory_notification_unit_id",
            "tbl_countries": "country_id",
            "tbl_domains": "domain_id"
        }

    def _load_columns_count(self):
        self._columns_count = {
            "tbl_client_groups": 11,
            "tbl_business_groups": 2,
            "tbl_legal_entities": 3,
            "tbl_divisions": 4,
            "tbl_units": 13,
            "tbl_client_configurations": 5,
            "tbl_compliances": 17,
            "tbl_client_statutories": 5,
            "tbl_client_compliances": 10,
            "tbl_statutory_notifications_log": 8,
            "tbl_statutory_notifications_units": 6,
            "tbl_countries": 2,
            "tbl_domains": 2
        }

    def _get_client_countries(self):
        country_list = None
        self._db.begin()
        try:
            country_list = self._db.get_countries()
            for c in country_list :
                self._countries.append(int(c.country_id))
            self._db.commit()
        except Exception, e :
            print e,
            self._countries = None
            self._db.rollback()
        assert self._countries is not None

    def _get_client_domains(self):
        domain_list = None
        self._db.begin()
        try:
            domain_list = self._db.get_domains()
            for d in domain_list :
                self._domains.append(int(d.domain_id))
            self._db.commit()
        except Exception, e :
            print e,
            self._domains = None
            self._db.rollback()
        assert self._domains is not None

    def _get_received_count(self):
        # assert self._received_count is None
        self._db.begin()
        try:
            self._received_count = self._db.get_trail_id()
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
            # print time.time()
            if self._stop:
                return
            body = json.dumps(
                GetChanges(
                    self._client_id,
                    self._received_count
                ).to_structure()
            )
            request = HTTPRequest(
                self._poll_url, method="POST", body=body,
                headers={"Content-Type": "application/json"},
                request_timeout=10
            )
            self._http_client.fetch(request, self._poll_response)
        self._io_loop.add_timeout(
            time.time() + 2, on_timeout
        )

    def _poll_response(self, response) :
        if self._stop:
            return
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
            if type(r) is InvalidReceivedCount:
                # print "InvalidReceivedCount sent %s"
                self._poll()
                return
            assert r is not None
            self._parse_data(r.changes)
            print len(r.changes)
            if len(r.changes) > 0 :
                self._poll()
        else :
            pass
            # print err, response.error

    def _execute_insert_statement(self, changes, error_ok=False):
        assert (len(changes)) > 0
        # print changes
        tbl_name = changes[0].tbl_name
        auto_id = self._auto_id_columns.get(tbl_name)
        print tbl_name
        column_count = self._columns_count.get(tbl_name)
        print column_count
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

        query = "INSERT INTO %s (%s, %s) VALUES(%s, %s);" % (
            tbl_name,
            auto_id,
            ",".join(i_column),
            changes[0].tbl_auto_id,
            val
        )
        try :
            print domain_id, self._domains
            print tbl_name
            print query
            if tbl_name != "tbl_compliances" :
                self._db.execute(query)
            elif tbl_name == "tbl_compliances" and domain_id in self._domains :
                self._db.execute(query)

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
                print query
                # logger.logClient("client.py", "update", query)
        self._temp_count = change.audit_trail_id

    def _parse_data(self, changes):
        # self._get_received_count()

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
            # print "audit_trail_id updated ", self._temp_count
            self._db.update_traild_id(self._temp_count)
            self._received_count = self._temp_count
            self._db.commit()
            # self._temp_count = 0
        except Exception, e:
            print(traceback.format_exc())
            print e
            logger.logClient("error", "client.py-parse-data", e)
            logger.logClient("error", "client.py", traceback.format_exc())

            self._temp_count = self._received_count
            self._db.rollback()
        assert self._received_count <= self._temp_count
        self._received_count = self._temp_count

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
        print "poll started for ", self._client_id
        self._io_loop.add_callback(self._poll)
        self._io_loop.add_callback(self._poll_for_del)

#
# DomainReplicationManager
#

class ReplicationBase(object):
    def __init__(
        self, io_loop, knowledge_server_address, http_client,
        db
    ) :
        self._io_loop = io_loop
        self._knowledge_server_address = knowledge_server_address
        self._http_client = http_client
        self._db = db
        self._received_count = None
        self._temp_count = 0
        self._stop = False
        self._auto_id_columns = {}
        self._load_auto_id_columns()
        self._columns_count = {}
        self._load_columns_count()
        self._countries = []
        self._domains = []
        self._get_client_countries()
        self._get_client_domains()
        self._type = None

    def _load_auto_id_columns(self):
        self._auto_id_columns = {
            "tbl_client_groups": "client_id",
            "tbl_business_groups": "business_group_id",
            "tbl_legal_entities": "legal_entity_id",
            "tbl_divisions": "division_id",
            "tbl_units": "unit_id",
            "tbl_client_configurations": "client_config_id",
            "tbl_compliances": "compliance_id",
            "tbl_client_statutories": "client_statutory_id",
            "tbl_client_compliances": "client_compliance_id",
            "tbl_statutory_notifications_log": "statutory_notification_id",
            "tbl_statutory_notifications_units": "statutory_notification_unit_id",
            "tbl_countries": "country_id",
            "tbl_domains": "domain_id"
        }

    def _load_columns_count(self):
        self._columns_count = {
            "tbl_client_groups": 11,
            "tbl_business_groups": 2,
            "tbl_legal_entities": 3,
            "tbl_divisions": 4,
            "tbl_units": 13,
            "tbl_client_configurations": 5,
            "tbl_compliances": 17,
            "tbl_client_statutories": 5,
            "tbl_client_compliances": 10,
            "tbl_statutory_notifications_log": 8,
            "tbl_statutory_notifications_units": 6,
            "tbl_countries": 2,
            "tbl_domains": 2
        }

    def _get_client_countries(self):
        country_list = None
        self._db.begin()
        try:
            country_list = self._db.get_countries()
            for c in country_list :
                self._countries.append(int(c.country_id))
            self._db.commit()
        except Exception, e :
            print e,
            self._countries = None
            self._db.rollback()
        assert self._countries is not None

    def _get_client_domains(self):
        domain_list = None
        self._db.begin()
        try:
            domain_list = self._db.get_domains()
            for d in domain_list :
                self._domains.append(int(d.domain_id))
            self._db.commit()
        except Exception, e :
            print e,
            self._domains = None
            self._db.rollback()
        assert self._domains is not None

    def _execute_insert_statement(self, changes, error_ok=False):
        assert (len(changes)) > 0
        # print changes
        tbl_name = changes[0].tbl_name
        auto_id = self._auto_id_columns.get(tbl_name)
        print tbl_name
        column_count = self._columns_count.get(tbl_name)
        print column_count
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

        query = "INSERT INTO %s (%s, %s) VALUES(%s, %s);" % (
            tbl_name,
            auto_id,
            ",".join(i_column),
            changes[0].tbl_auto_id,
            val
        )
        try :
            print domain_id, self._domains
            print tbl_name
            print query
            if tbl_name != "tbl_compliances" :
                self._db.execute(query)
            elif tbl_name == "tbl_compliances" and domain_id in self._domains :
                self._db.execute(query)

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
                print query
                # logger.logClient("client.py", "update", query)
        self._temp_count = change.audit_trail_id
        print self._temp_count

    def _parse_data(self, changes):
        # self._get_received_count()
        print self._temp_count
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
            # print "audit_trail_id updated ", self._temp_count
            self._db.update_traild_id(self._temp_count, self._type)
            self._received_count = self._temp_count
            self._db.commit()
            # self._temp_count = 0
        except Exception, e:
            print(traceback.format_exc())
            print e
            logger.logClient("error", "client.py-parse-data", e)
            logger.logClient("error", "client.py", traceback.format_exc())

            self._temp_count = self._received_count
            self._db.rollback()
        assert self._received_count <= self._temp_count
        self._received_count = self._temp_count

class ReplicationManagerWithBase(ReplicationBase):
    def __init__(
        self, io_loop, knowledge_server_address,
        http_client, db, client_id
    ) :
        super(ReplicationManagerWithBase, self).__init__(
            io_loop, knowledge_server_address,
            http_client, db
        )
        self._get_received_count()
        self._client_id = client_id
        ip, port = self._knowledge_server_address
        self._poll_url = "http://%s:%s/knowledge/replication" % (ip, port)
        self._poll_old_data_url = "http://%s:%s/knowledge/delreplicated" % (ip, port)

    def _get_received_count(self):
        # assert self._received_count is None
        self._db.begin()
        try:
            self._received_count = self._db.get_trail_id()
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
            print time.time()
            if self._stop:
                return

            body = json.dumps(
                GetChanges(
                    self._client_id,
                    self._received_count
                ).to_structure()
            )
            request = HTTPRequest(
                self._poll_url, method="POST", body=body,
                headers={"Content-Type": "application/json"},
                request_timeout=10
            )
            self._http_client.fetch(request, self._poll_response)
        self._io_loop.add_timeout(
            time.time() + 3, on_timeout
        )

    def _poll_response(self, response) :
        if self._stop:
            return
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
            if type(r) is InvalidReceivedCount:
                # print "InvalidReceivedCount sent %s"
                self._poll()
                return
            assert r is not None
            self._parse_data(r.changes)
            print len(r.changes)
            if len(r.changes) > 0 :
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
        print "poll started for ", self._client_id
        self._io_loop.add_callback(self._poll)
        self._io_loop.add_callback(self._poll_for_del)


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
            self._actual_replica_count = self._db.get_trail_id()
            print "_actual_replica_count"
            print self._actual_replica_count
            self._db.commit()
        except Exception, e:
            print e
            self._actual_replica_count = None
            self._db.rollback()
        assert self._actual_replica_count is not None

    def _get_domain_received_count(self):
        self._db.begin()
        try:
            self._received_count = self._db.get_trail_id(self._type)
            print "_received_count"
            print self._received_count
            self._db.commit()
        except Exception, e:
            print e
            self._received_count = None
            self._db.rollback()

    def _reset_domain_trail_id(self):
        self._db.begin()
        try :
            self._db.reset_domain_trail_id()
            self._db.commit()
        except Exception, e :
            print e
            self._db.rollback()

    def _poll(self):
        assert self._stop is False
        assert self._received_count is not None
        print "poll validate"
        # if self._received_count > self._actual_replica_count :
        #     return
        print "Domain replication poll for client_id = %s, domain_id = %s, _received_count=%s " % (self._client_id, self._domain_id, self._received_count)

        def on_timeout():
            print time.time()
            print self._received_count
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
        print "poll response receive, actual"
        print self._received_count, self._actual_replica_count

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
                print err, e
                self._poll()
                return

            if type(r) is InvalidReceivedCount :
                self._poll()
                return

            assert r is not None
            self._parse_data(r.changes)
            print len(r.changes)
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
        print "poll started for ", self._client_id
        self._io_loop.add_callback(self._poll)
