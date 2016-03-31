import time
from tornado.httpclient import HTTPRequest
import json
import traceback
from replication.protocol import (
    Response, GetChanges, GetChangesSuccess, InvalidReceivedCount
)

import logger


#
# __all__
#

__all__ = [
    "ReplicationManager"
]


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
        self._poll_url = "http://%s:%s/replication" % (ip, port)
        # print "_received_count ================ " , self._received_count

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
            "tbl_statutory_notifications_units": "statutory_notification_unit_id"
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
            "tbl_statutory_notifications_units": 6
        }

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
        # print "ReplicationManager poll for client_id = %s, _received_count = %s " % (self._client_id, self._received_count)

        def on_timeout():
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
            time.time() + 1, on_timeout
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
        else :
            pass
            # print err, response.error
        self._poll()

    def _execute_insert_statement(self, changes, error_ok=False):
        assert (len(changes)) > 0
        # print changes
        tbl_name = changes[0].tbl_name
        auto_id = self._auto_id_columns.get(tbl_name)
        column_count = self._columns_count.get(tbl_name)
        column_count -= 1
        assert auto_id is not None
        if error_ok:
            if column_count != len(changes):
                return
        else:
            assert column_count == len(changes)
        columns = [x.column_name for x in changes]
        values = []
        for x in changes:
            if x.value is None:
                values.append('')
            else:
                values.append(str(x.value))
            val = str(values)[1:-1]

        query = "INSERT INTO %s (%s, %s) VALUES(%s, %s);" % (
            tbl_name,
            auto_id,
            ",".join(columns),
            changes[0].tbl_auto_id,
            val
        )
        try :
            pass
            self._db.execute(query)

        except Exception, e:
            pass
            print e
            self._temp_count = changes[-1].audit_trail_id

    def _execute_update_statement(self, change):
        auto_id = self._auto_id_columns.get(change.tbl_name)
        assert auto_id is not None
        if change.value is None:
            val = ""
        else:
            val = change.value
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
            print query

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

    def stop(self):
        self._stop = True

    def start(self):
        self._stop = False
        self._io_loop.add_callback(self._poll)
