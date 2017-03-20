import threading
from server.dbase import Database
from server.common import get_date_time, get_current_date, addHours
from server.clientdatabase.exportdata import UnitClosureExport
from server.constants import REGISTRATION_EXPIRY

__all__ = [
    "LegalEntityReplicationManager",
    "LEntityReplicationUSer",
    "LEntityReplicationServiceProvider",
    "LEntityUnitClosure",
    "LEntitySettingsData"
]

class LegalEntityReplicationManager(object):
    def __init__(
        self, group_db_info, time_out_seconds, callback
    ):
        self._group_db_info = group_db_info
        self._time_out_seconds = time_out_seconds
        self._callback = callback
        self._first_time = True

    def _start(self):
        self._poll()

    def _initiate_connction(self):
        con = Database.make_connection(self._group_db_info)
        _db = Database(con)
        return _db

    def _poll(self):
        def on_timeout():
            rows = []
            _db = self._initiate_connction()
            q = "select legal_entity_id, user_data, settings_data, provider_data " + \
                " from tbl_le_replication_status where user_data = 1 or settings_data = 1 " + \
                " or provider_data = 1 "
            try :
                _db.begin()
                rows = _db.select_all(q)
            except Exception, e :
                print e
                _db.rollback()

            finally :
                _db.close()
                self._poll_response(rows)

            t = threading.Timer(self._time_out_seconds, on_timeout)
            t.daemon = True
            t.start()

        if self._first_time :
            self._first_time = False
            on_timeout()

    def _poll_response(self, response):
        self._callback(self._group_db_info, response)

class LEntityReplicationUSer(object):
    def __init__(self, group_info, le_info, le_id):
        self._group_info = group_info
        self._le_info = le_info
        self._le_id = le_id

    def _initiate_connection(self, connection_param):
        con = Database.make_connection(connection_param)
        _db = Database(con)
        return _db

    def reset_repliation_status(self, _db):
        q = "update tbl_le_replication_status set user_data=0 where legal_entity_id = %s"
        _db.execute(q, [self._le_id])

    def fetch_data_to_save(self):
        save_rows = []
        del_rows = []
        _db = self._initiate_connection(self._group_info)
        q = "select user_id, s_action " + \
            " from tbl_le_user_replication_status where legal_entity_id = %s"
        try :
            _db.begin()
            rows = _db.select_all(q, [self._le_id])
            for r in rows :
                if r["s_action"] == 1 :
                    save_rows.append(r["user_id"])
                else :
                    pass
                    del_rows.append(r["user_id"])
            if len(rows) == 0 :
                self.reset_repliation_status(_db)
            _db.commit()
        except Exception, e :
            print e
            _db.rollback()

        finally :
            _db.close()
            return save_rows, del_rows

    def delete_fetched_data(self, user_ids):
        suser_id = ",".join([str(x) for x in user_ids])
        _db = self._initiate_connection(self._group_info)
        q = " delete from tbl_le_user_replication_status where legal_entity_id = %s and " + \
            " find_in_set(user_id, %s)"
        try :
            _db.begin()
            _db.execute(q, [self._le_id, suser_id])

            _db.commit()
        except Exception, e :
            print e
            _db.rollback()

        finally :
            _db.close()

    def delete_user_data(self, _db, user_ids):
        suser_ids = ",".join([str(x) for x in user_ids])
        q = "delete from tbl_users where find_in_set(user_id, %s)"
        _db.execute(q, [suser_ids])
        q = "delete from tbl_user_legal_entities where find_in_set(user_id, %s)"
        _db.execute(q, [suser_ids])
        q1 = "delete from tbl_user_units where find_in_set(user_id, %s)"
        _db.execute(q1, [suser_ids])
        q2 = "delete from tbl_user_domains where find_in_set(user_id, %s)"
        _db.execute(q2, [suser_ids])

    def fetch_user_data(self, user_ids):
        suser_ids = ",".join([str(x) for x in user_ids])
        user_rows = []
        domain_rows = []
        unit_rows = []

        _db = self._initiate_connection(self._group_info)
        q_user = "select * " + \
            " from tbl_users where find_in_set(user_id, %s)"
        q_user_domains = "select * from tbl_user_domains where legal_entity_id = %s and find_in_set(user_id, %s)"
        q_user_units = "select * from tbl_user_units where legal_entity_id = %s and find_in_set(user_id, %s)"
        try :
            _db.begin()
            user_rows = _db.select_all(q_user, [suser_ids])
            domain_rows = _db.select_all(q_user_domains, [self._le_id, suser_ids])
            unit_rows = _db.select_all(q_user_units, [self._le_id, suser_ids])

        except Exception, e :
            print e
            _db.rollback()

        finally :
            _db.close()
            return user_rows, domain_rows, unit_rows

    def save_tbl_users(self, _db, user_info):
        d = user_info
        q = "insert into tbl_users(user_id, user_category_id, client_id, seating_unit_id, " + \
            " service_provider_id, user_level, user_group_id, email_id, employee_name, " + \
            " employee_code, contact_no, mobile_no, is_service_provider, is_active, is_disable, remarks) " + \
            " values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
        try :
            _db.execute(q, [
                d["user_id"], d["user_category_id"], d["client_id"], d["seating_unit_id"],
                d["service_provider_id"], d["user_level"], d["user_group_id"],
                d["email_id"], d["employee_name"], d["employee_code"],
                d["contact_no"], d["mobile_no"], d["is_service_provider"],
                d["is_active"], d["is_disable"], d["remarks"]
            ])
        except Exception, e :
            print e

    def save_tbl_user_legal_entities(self, _db, user_id):
        q = "insert into tbl_user_legal_entities(user_id, legal_entity_id) values (%s, %s)"
        try :
            _db.execute(q, [user_id, self._le_id])
        except Exception, e :
            print e

    def save_tbl_user_domains(self, _db, user_info):
        d = user_info

        q = "insert into tbl_user_domains(user_id, legal_entity_id, domain_id) " + \
            " values(%s, %s, %s)"
        try :
            _db.execute(q, [d["user_id"], d["legal_entity_id"], d["domain_id"]])
        except Exception, e :
            print e

    def save_tbl_user_units(self, _db, user_info):
        d = user_info
        q = "insert into tbl_user_units(user_id, legal_entity_id, unit_id) values " + \
            "(%s, %s, %s)"
        try :
            _db.execute(q, [d["user_id"], d["legal_entity_id"], d["unit_id"]])
        except Exception, e :
            print e

    def perform_save(self):
        save_rows, del_rows = self.fetch_data_to_save()
        user_rows, domain_rows, unit_rows = self.fetch_user_data(save_rows)
        u_ids = [x["user_id"] for x in user_rows]
        _db = self._initiate_connection(self._le_info)
        try:
            _db.begin()
            self.delete_user_data(_db, u_ids)
            for user in user_rows :
                self.save_tbl_users(_db, user)
                self.save_tbl_user_legal_entities(_db, user["user_id"])

            for domain in domain_rows :
                self.save_tbl_user_domains(_db, domain)

            for unit in unit_rows :
                self.save_tbl_user_units(_db, unit)

            _db.commit()
            self.delete_fetched_data(u_ids)
        except Exception, e:
            print e
            _db.rollback()
        finally:
            _db.close()

    def _start(self):
        self.perform_save()

class LEntityReplicationServiceProvider(object):
    def __init__(self, group_info, le_info, le_id):
        self._group_info = group_info
        self._le_info = le_info
        self._le_id = le_id

    def _initiate_connection(self, connection_param):
        con = Database.make_connection(connection_param)
        _db = Database(con)
        return _db

    def reset_repliation_status(self, _db):
        q = "update tbl_le_replication_status set provider_data=0 where legal_entity_id = %s"
        _db.execute(q, [self._le_id])

    def fetch_data_to_save(self):
        save_rows = []
        _db = self._initiate_connection(self._group_info)
        q = "select provider_id, s_action " + \
            " from tbl_le_provider_replication_status where legal_entity_id = %s"
        try :
            _db.begin()
            rows = _db.select_all(q, [self._le_id])
            for r in rows :
                save_rows.append(r["provider_id"])
            if len(rows) == 0 :
                self.reset_repliation_status(_db)
            _db.commit()
        except Exception, e :
            print e
            _db.rollback()

        finally :
            _db.close()
            return save_rows

    def delete_fetched_data(self, provider_ids):
        sprovider_id = ",".join([str(x) for x in provider_ids])
        _db = self._initiate_connection(self._group_info)
        q = " delete from tbl_le_provider_replication_status where legal_entity_id = %s and " + \
            " find_in_set(provider_id, %s)"
        try :
            _db.begin()
            _db.execute(q, [self._le_id, sprovider_id])

            _db.commit()
        except Exception, e :
            print e
            _db.rollback()

        finally :
            _db.close()

    def delete_sprovider_data(self, _db, provider_id):
        sprovider_id = ",".join([str(x) for x in provider_id])
        q = "delete from tbl_service_providers where find_in_set(service_provider_id, %s)"
        _db.execute(q, [sprovider_id])

    def fetch_sprovider_data(self, provider_id):
        sprovider_id = ",".join([str(x) for x in provider_id])
        provider_rows = []

        _db = self._initiate_connection(self._group_info)
        q_user = "select * " + \
            " from tbl_service_providers where find_in_set(service_provider_id, %s)"

        try :
            _db.begin()
            provider_rows = _db.select_all(q_user, [sprovider_id])

        except Exception, e :
            print e
            _db.rollback()

        finally :
            _db.close()
            return provider_rows

    def save_tbl_service_provider(self, _db, data):
        d = data
        q = "insert into tbl_service_providers(service_provider_id, service_provider_name, " + \
            " short_name, contract_from, contract_to, contact_person, contact_no, email_id, mobile_no, " + \
            " address, is_active, status_changed_by, status_changed_on, is_blocked, blocked_by, " + \
            " blocked_on, remarks, created_by, created_on, updated_by, updated_on) " + \
            " values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try :
            _db.execute(q, [
                d["service_provider_id"], d["service_provider_name"], d["short_name"],
                d["contract_from"], d["contract_to"], d["contact_person"], d["contact_no"],
                d["email_id"], d["mobile_no"], d["address"], d["is_active"],
                d["status_changed_by"], d["status_changed_on"], d["is_blocked"],
                d["blocked_by"], d["blocked_on"], d["remarks"], d["created_by"],
                d["created_on"], d["updated_by"], d["updated_on"]
            ])
        except Exception, e :
            print e

    def perform_save(self):
        save_rows = self.fetch_data_to_save()
        provider_rows = self.fetch_sprovider_data(save_rows)
        s_ids = [x["service_provider_id"] for x in provider_rows]
        _db = self._initiate_connection(self._le_info)
        try:
            _db.begin()
            self.delete_sprovider_data(_db, s_ids)
            for user in provider_rows :
                self.save_tbl_service_provider(_db, user)

            _db.commit()
            self.delete_fetched_data(s_ids)
        except Exception, e:
            print e
            _db.rollback()
        finally:
            _db.close()

    def _start(self):
        self.perform_save()

class LEntityUnitClosure(object):
    def __init__(self, group_info, le_info, le_id, data, user_id):
        self._group_info = group_info
        self._le_info = le_info
        self._le_id = le_id
        self._data = data
        self._user_id = user_id
        self._closed_on = None
        self._unit_id = None

    def _initiate_connection(self, connection_param):
        con = Database.make_connection(connection_param)
        _db = Database(con)
        return _db

    def save_in_group_db(self, export_obj, export_link):
        current_time_stamp = get_current_date()
        expiry_date = addHours(int(REGISTRATION_EXPIRY), current_time_stamp)

        _db = self._initiate_connection(self._group_info)
        try:
            _db.begin()
            export_obj.save_download_session(_db, expiry_date, export_link)
            _db.commit()

        except Exception, e:
            print e
            _db.rollback()
        finally:
            _db.close()

    def save_unit_closure_data(self, db, user_id, unit_id, remarks, action_mode):
        current_time_stamp = get_date_time()
        self._closed_on = current_time_stamp
        self._unit_id = unit_id
        print action_mode
        columns = ["is_closed", "closed_on", "closed_by", "closed_remarks"]
        values = []
        if action_mode == "close":
            print "save"
            values = [1, current_time_stamp, user_id, remarks]
            condition_val = "unit_id= %s"
            values.append(unit_id)
            result = db.update("tbl_units", columns, values, condition_val)
            uce = UnitClosureExport(db, self._unit_id, self._closed_on)
            export_link = uce.perform_export()
            if export_link is not None :
                self.save_in_group_db(uce, export_link)

        elif action_mode == "reactive":
            values = [0, current_time_stamp, user_id, remarks]
            condition_val = "unit_id= %s"
            values.append(unit_id)
            result = db.update("tbl_units", columns, values, condition_val)
        print "result"
        print result

    def save_tbl_units(self, _db):
        try :
            self.save_unit_closure_data(
                _db, self._user_id, self._data.unit_id,  self._data.closed_remarks,
                self._data.grp_mode
            )
        except Exception, e :
            print e

    def perform_closure(self):

        _db = self._initiate_connection(self._le_info)
        try:
            _db.begin()
            self.save_tbl_units(_db)
            _db.commit()

        except Exception, e:
            print e
            _db.rollback()
        finally:
            _db.close()

    def _start(self):
        self.perform_closure()

class LEntitySettingsData(object):
    def __init__(self, group_info, le_info, le_id):
        self._group_info = group_info
        self._le_info = le_info
        self._le_id = le_id

    def _initiate_connection(self, connection_param):
        con = Database.make_connection(connection_param)
        _db = Database(con)
        return _db

    def reset_repliation_status(self, _db):
        q = "update tbl_le_replication_status set settings_data=0 where legal_entity_id = %s"
        _db.execute(q, [self._le_id])

    def fetch_data_to_save(self):
        _db = self._initiate_connection(self._group_info)
        q = "select client_id, legal_entity_id, two_levels_of_approval, assignee_reminder, " + \
            " escalation_reminder_in_advance, escalation_reminder, reassign_service_provider, " + \
            "created_by, created_on, updated_by, updated_on " + \
            " from tbl_reminder_settings where legal_entity_id = %s"
        try :
            _db.begin()
            rows = _db.select_all(q, [self._le_id])

            if len(rows) == 0 :
                self.reset_repliation_status(_db)
            _db.commit()
        except Exception, e :
            print e
            _db.rollback()

        finally :
            _db.close()
            return rows

    def delete_fetched_data(self):
        _db = self._initiate_connection(self._group_info)
        q = " delete from tbl_le_settings_replication_status where legal_entity_id = %s "
        try :
            _db.begin()
            _db.execute(q, [self._le_id])
            self.reset_repliation_status(_db)
            _db.commit()
        except Exception, e :
            print e
            _db.rollback()

        finally :
            _db.close()

    def save_settings(self, _db, settings_info):
        s = settings_info
        q = "insert into tbl_reminder_settings (client_id, legal_entity_id, two_levels_of_approval, assignee_reminder, " + \
            " escalation_reminder_in_advance, escalation_reminder, reassign_service_provider, " + \
            "created_by, created_on, updated_by, updated_on )" + \
            "values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) " + \
            "on duplicate key update two_levels_of_approval = values(two_levels_of_approval), " + \
            "assignee_reminder = values(assignee_reminder), escalation_reminder_in_advance = values(escalation_reminder_in_advance), " + \
            "escalation_reminder = values(escalation_reminder), reassign_service_provider = values(reassign_service_provider), " + \
            "created_by = values(created_by), created_on = values(created_on), updated_by = values(updated_by), " + \
            "updated_on = values(updated_on)"
        try :
            _db.execute(q, [
                s.get("client_id"), s.get("legal_entity_id"), s.get("two_levels_of_approval"),
                s.get("assignee_reminder"), s.get("escalation_reminder_in_advance"),
                s.get("escalation_reminder"), s.get("reassign_service_provider"),
                s.get("created_by"), s.get("created_on"), s.get("updated_by"),
                s.get("updated_on")
            ])
        except Exception, e :
            print e

    def perform_save(self):
        save_rows = self.fetch_data_to_save()
        _db = self._initiate_connection(self._le_info)
        try:
            _db.begin()
            if save_rows :
                self.save_settings(_db, save_rows[0])
            _db.commit()

        except Exception, e:
            print e
            _db.rollback()
        finally:
            _db.close()
        self.delete_fetched_data()

    def _start(self):
        self.perform_save()
