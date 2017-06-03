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
        self._request_body = json.dumps(
            GetClientChanges().to_structure(), indent=2
        )
        self.stop = False

    def _start(self):
        self._poll()

    def _stop(self):
        self.stop = True

    def _poll(self) :

        def on_timeout():
            # print "Poll rotated-----------------------------"
            # print datetime.datetime.now()
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

            if self.stop is False :
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
                r = Response.parse_structure(
                    json.loads(response)
                )
            except Exception, e :
                print err, e
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
        db, is_group, client_id, country_id, group_id
    ) :
        # self._io_loop = io_loop
        self._knowledge_server_address = knowledge_server_address
        # self._http_client = http_client
        self._db = db
        self._client_id = client_id
        self._is_group = is_group
        self._group_id = group_id
        self._country_id = country_id
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
            "tbl_client_configuration": "cn_config_id",
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
            "tbl_client_configuration": 6,
            "tbl_business_groups": 2,
            "tbl_legal_entities": 14,
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

    def check_compliance_available_for_statutory_notification(self, compliance_id):
        q = "select count(0) as cnt from tbl_compliances where compliance_id = %s  and country_id = %s"
        rows = self._db.select_one(q, [compliance_id, self._country_id])
        if rows.get("cnt") is None :
            return False
        elif rows.get("cnt") == 0 :
            return False
        else :
            return True

    def _execute_insert_mapped_industry(self, changes):

        tbl_name = changes[0].tbl_name

        # print tbl_name

        values = []
        columns = ["statutory_mapping_id", "organisation_id"]
        for x in changes:
            if x.value is None:
                # values.append('')
                pass
            else:
                if tbl_name == "tbl_mapped_industries" :
                    values.append((changes[0].tbl_auto_id, str(x.value)))

        q = "delete from tbl_mapped_industries where statutory_mapping_id = %s"
        self._db.execute(q, [changes[0].tbl_auto_id])

        query = "INSERT INTO %s (%s) VALUES " % (tbl_name, ",".join(columns))

        for index, value in enumerate(values):
            if index < len(values)-1:
                query += "%s," % str(value)
            else:
                query += "%s" % str(value)

        # print query
        self._db.execute(query)

    def _execute_insert_statement(self, changes, error_ok=False):
        assert (len(changes)) > 0

        tbl_name = changes[0].tbl_name
        auto_id = self._auto_id_columns.get(tbl_name)
        print tbl_name
        column_count = self._columns_count.get(tbl_name)
        column_count -= 1
        print column_count
        if tbl_name == "tbl_mapped_industries" :
            pass
            # self._execute_insert_mapped_industry(changes)
        else :
            print error_ok

            assert auto_id is not None
            if error_ok:
                if column_count != len(changes):
                    if tbl_name == "tbl_countries":
                        for r in changes :
                            self._execute_insert_statement([r])
                        return
                    else :
                        return

            else:
                if column_count != len(changes):
                    return
            # columns = [x.column_name for x in changes]
            i_column = []
            values = []
            domain_id = None
            compliance_id = None
            r_country_id = None
            r_le_id = None
            r_client_d = None
            for x in changes:
                if x.value is None:
                    # values.append('')
                    pass
                else:
                    i_column.append(x.column_name)
                    values.append(str(x.value))
                    if tbl_name == "tbl_compliances" and x.column_name == "domain_id" :
                        domain_id = int(x.value)
                    if tbl_name == "tbl_compliances" and x.column_name == "country_id" :
                        r_country_id = int(x.value)
                    if tbl_name == "tbl_statutory_notifications" and x.column_name == "compliance_id":
                        compliance_id = int(x.value)
                    if tbl_name == "tbl_units" and x.column_name == "legal_entity_id" :
                        r_le_id = int(x.value)
                    if tbl_name == "tbl_client_configuration" and x.column_name == "country_id" :
                        r_country_id = int(x.value)
                    if tbl_name == "tbl_client_configuration" and x.column_name == "client_id" :
                        r_client_d = int(x.value)
                    if tbl_name == "tbl_validity_date_settings" and x.column_name == "country_id" :
                        r_country_id = int(x.value)

                val = str(values)[1:-1]

            query = "INSERT INTO %s (%s, %s) VALUES(%s, %s)" % (
                    tbl_name,
                    auto_id,
                    ",".join(i_column),
                    changes[0].tbl_auto_id,
                    val
                )

            if tbl_name == "tbl_client_groups" :
                query += " ON DUPLICATE KEY UPDATE email_id = values(email_id), total_view_licence = values(total_view_licence) ;"

            elif tbl_name == "tbl_legal_entities" :
                query += " ON DUPLICATE KEY UPDATE legal_entity_name = values(legal_entity_name), " + \
                    " contract_from = values(contract_from), contract_to = values(contract_to), " + \
                    " logo = values(logo), logo_size = values(logo_size), file_space_limit = values(file_space_limit), " + \
                    " total_licence = values(total_licence), " + \
                    " used_licence = used_licence+1, " + \
                    " is_closed = values(is_closed), closed_on = values(closed_on), " + \
                    " closed_by = values(closed_by), closed_remarks = values(closed_remarks)"

            elif tbl_name == "tbl_units":
                query += " ON DUPLICATE KEY UPDATE unit_name = values(unit_name), " + \
                    " unit_code = values(unit_code), geography_name = values(geography_name), " + \
                    " address = values(address), postal_code = values(postal_code) "

            elif tbl_name == "tbl_compliances" :
                query += " ON DUPLICATE KEY UPDATE statutory_provision = values(statutory_provision), " + \
                    " compliance_task = values(compliance_task), document_name = values(document_name), " + \
                    " compliance_description = values(compliance_description), penal_consequences = values(penal_consequences), " + \
                    " reference_link = values(reference_link), frequency_id = values(frequency_id),  " + \
                    " statutory_dates = values(statutory_dates), repeats_type_id = values(repeats_type_id), " + \
                    " duration_type_id = values(duration_type_id), repeats_every = values(repeats_every), " + \
                    " duration = values(duration), is_active = values(is_active), " + \
                    " format_file = values(format_file), format_file_size = values(format_file_size), " + \
                    " statutory_nature = values(statutory_nature), statutory_mapping = values(statutory_mapping)"
            elif tbl_name == "tbl_legal_entity_domains":
                query += "ON DUPLICATE KEY UPDATE count = values(count)"
            else :
                query += ""

            try :
                print domain_id, self._domains
                if self._is_group :
                    print "Replication for client ", self._client_id, self
                else :
                    print "Replication for legal entity ", self._client_id,  self
                print tbl_name
                print query

                if tbl_name == "tbl_client_groups" :
                    if self._is_group is False and self._group_id == changes[0].tbl_auto_id :
                        self._db.execute(query)

                    elif self._is_group :
                        self._db.execute(query)

                elif tbl_name == "tbl_compliances" :
                    # print r_country_id, domain_id
                    # print self._country_id, self._domains
                    if r_country_id == self._country_id and domain_id in self._domains :
                        self._db.execute(query)

                elif tbl_name == "tbl_statutory_notifications" :
                    if self.check_compliance_available_for_statutory_notification(compliance_id) is True :
                        self._db.execute(query)

                elif tbl_name == "tbl_legal_entities" :
                    self._db.execute("delete from tbl_legal_entity_domains where legal_entity_id = %s", [changes[0].tbl_auto_id])
                    self._db.execute("delete from tbl_client_configuration")
                    if self._is_group is False and self._client_id == changes[0].tbl_auto_id :
                        self._db.execute(query)
                    elif self._is_group is True :
                        self._db.execute(query)

                elif tbl_name == "tbl_units" :
                    self._db.execute("delete from tbl_units_organizations where unit_id = %s", [changes[0].tbl_auto_id])

                    if self._is_group :
                        self._db.execute(query)
                    elif self._is_group is False and self._client_id == r_le_id :
                        self._db.execute(query)

                elif tbl_name == "tbl_client_configuration" :
                    # print self._group_id, self._country_id
                    # print r_client_d, r_country_id
                    # print self._is_group

                    if self._is_group and self._client_id == r_client_d :
                        self._db.execute(query)
                    elif self._is_group is False and self._group_id == r_client_d and self._country_id == r_country_id :
                        self._db.execute(query)

                elif tbl_name == "tbl_countries" :
                    if self._is_group is False and self._country_id == changes[0].tbl_auto_id :
                        self._db.execute(query)
                    else :
                        self._db.execute(query)

                elif tbl_name == "tbl_validity_date_settings" :
                    # print self._country_id, r_country_id

                    if self._country_id == r_country_id :
                        self._db.execute(query)

                else :
                    self._db.execute(query)

            except Exception, e:
                pass
                print e
                logger.logclient("error", "client replication base", e)
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
                logger.logclient("error", "client replication base", e)

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
                print change.to_structure()
                # Update
                if change.action == "1":
                    if is_insert:
                        print "inerst 1 ------------- "
                        self._execute_insert_statement(changes_list)
                    is_insert = False
                    changes_list = []
                    print "update 1 ---------------"
                    self._execute_update_statement(change)
                else:
                    if is_insert is False:
                        is_insert = True
                        auto_id = change.tbl_auto_id
                        tbl_name = change.tbl_name

                    if auto_id != change.tbl_auto_id or tbl_name != change.tbl_name:
                        print "insert 2 ---------------"
                        self._execute_insert_statement(changes_list)
                        changes_list = []
                    auto_id = change.tbl_auto_id
                    tbl_name = change.tbl_name
                    changes_list.append(change)
            if is_insert:
                print "insert 3 -------------------------"
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
            logger.logclient("error", "client replication base", e)
            logger.logclient("error", "client replication base", str(traceback.format_exc()))

            self._temp_count = self._received_count
            self._db.rollback()
        assert self._received_count <= self._temp_count
        self._received_count = self._temp_count

class ReplicationManagerWithBase(ReplicationBase):
    def __init__(
        self, knowledge_server_address,
        db, client_id, is_group, country_id, group_id
    ) :
        super(ReplicationManagerWithBase, self).__init__(
            knowledge_server_address,
            db, is_group, client_id, country_id, group_id
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
            print "Error--------"
            print e
            self._received_count = None
            self._db.rollback()
        assert self._received_count is not None

    def _poll(self) :
        assert self._stop is False
        assert self._received_count is not None
        # print "ReplicationManager poll for client_id = %s, _received_count = %s " % (self._client_id, self._received_count)

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

        if self._stop is False :
            t = threading.Timer(5, on_timeout)
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
                print err, e
                self._poll()
                return
            if type(r) is InvalidReceivedCount:
                # print "InvalidReceivedCount sent"
                self._poll()
                return
            assert r is not None
            print r.changes
            self._parse_data(r.changes)
            print len(r.to_structure())
            # print len(r.changes)
            if len(r.changes) > 0 :
                # print len(r.changes)
                self._poll()
            else :
                print "0--------------11111--------------"
                self._stop = True
                return

        else :
            pass
            print err, response.error

    def stop(self):
        print "replication stoped"
        self._stop = True
        self._db.close()

    def start(self):
        self._stop = False
        self._poll()


class DomainReplicationManager(ReplicationBase):
    def __init__(
        self, knowledge_server_address,
        db, client_id, is_group, country_id, group_id,
        domain_id
    ) :
        super(DomainReplicationManager, self).__init__(
            knowledge_server_address,
            db, is_group, client_id, country_id, group_id
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
            self._db.commit()
        except Exception, e:
            print e
            self._actual_replica_count = None
            self._db.rollback()
        assert self._actual_replica_count is not None

    def _get_domain_received_count(self):
        self._db.begin()
        try:
            self._received_count = get_trail_id(self._db, self._type)
            self._db.commit()
        except Exception, e:
            print e
            self._received_count = None
            self._db.rollback()

    def _reset_domain_trail_id(self):
        self._db.begin()
        try :
            reset_domain_trail_id(self._db)
            self._db.commit()
        except Exception, e :
            print e
            self._db.rollback()

    def _poll(self):
        assert self._stop is False
        assert self._received_count is not None

        def on_timeout():
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
            key = ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(5))
            req_data = base64.b64encode(body)
            req_data = key+req_data

            response = requests.post(self._poll_url, data=req_data)

            data = response.text[6:]
            data = str(data).decode('base64')
            # print data
            self._poll_response(data, response.status_code)

        if self._stop is False :
            t = threading.Timer(5, on_timeout)
            t.daemon = True
            t.start()

    def _poll_response(self, response, status_code) :
        if self._stop :
            return
        err = "knowledge server poll error for compliances:"
        if status_code == 200 :
            r = None
            try :
                r = Response.parse_structure(
                    json.loads(response)
                )
            except Exception, e :
                print err, e
                self._poll()
                return

            if type(r) is InvalidReceivedCount :
                self._poll()
                return

            assert r is not None
            self._parse_data(r.changes)
            if len(r.changes) > 0 :
                self._poll()
            else :
                print "0--------------00--------------"
                self._reset_domain_trail_id()
                self._stop = True
                return
        else :
            pass

    def stop(self):
        self._stop = True
        self._db.close()

    def start(self):
        self._stop = False
        self._poll()
