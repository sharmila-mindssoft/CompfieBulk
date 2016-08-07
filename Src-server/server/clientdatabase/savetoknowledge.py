from server.dbase import Database
from server.exceptionmessage import client_process_error
from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
)

__all__ = [
    "UpdateFileSpace",
    "SaveUsers", "UpdateUsers", "UpdateUserStatus",
    "UnitClose"
]
class KnowledgedbConnect(object):
    def __init__(self):
        self._k_db = None

    def get_knowledge_connect(self):
        self._k_db = Database(
            KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT,
            KNOWLEDGE_DB_USERNAME, KNOWLEDGE_DB_PASSWORD,
            KNOWLEDGE_DATABASE_NAME
        )
        self._k_db.connect()

class UpdateFileSpace(KnowledgedbConnect):
    def __init__(self, space_used, client_id):
        super(UpdateFileSpace, self).__init__()
        self._space_used = space_used
        self._client_id = client_id
        self.procee_update_space()

    def _update_space(self):
        q = "Update tbl_client_groups set total_disk_space_used = %s \
            where client_id = %s "
        res = self._k_db.execute(q, [self._space_used, self._client_id])
        if res is False :
            raise client_process_error("E021")

    def procee_update_space(self):
        try:
            self.get_knowledge_connect()
            self._k_db.begin()
            self._update_space()
            self._k_db.commit()
            self._k_db.close()
            return True
        except Exception, e:
            print e
            self._k_db.rollback()
            raise client_process_error("E021")

class SaveUsers(KnowledgedbConnect):
    def __init__(self, user_info, user_id, client_id):
        super(SaveUsers, self).__init__()
        self._user_id = user_id
        self._user_info = user_info
        self._client_id = client_id
        self.process_save_user()

    def _save_user(self):
        if self._user_info.seating_unit_id is None :
            s_unit_id = 0
        else :
            s_unit_id = self._user_info.seating_unit_id

        q = "INSERT INTO tbl_client_users (client_id, user_id, \
            email_id, employee_name, employee_code, contact_no, created_on, \
            is_admin, is_active, seating_unit_id) VALUES (%s, %s, %s, %s, %s, %s, now(), 0, 1, %s) "
        values = [
            self._client_id, self._user_id, self._user_info.email_id,
            self._user_info.employee_name,
            self._user_info.employee_code, self._user_info.contact_no,
            s_unit_id
        ]
        self._k_db.execute(q, values)

    def process_save_user(self):
        try:
            self.get_knowledge_connect()
            self._k_db.begin()
            self._save_user()
            self._k_db.commit()
            self._k_db.close()
            return True
        except Exception, e:
            print e
            self._k_db.rollback()
            raise client_process_error("E022")

class UpdateUsers(KnowledgedbConnect):
    def __init__(self, user_info, user_id, client_id):
        super(SaveUsers, self).__init__()
        self._user_id = user_id
        self._user_info = user_info
        self._client_id = client_id
        self.process_update_user()

    def _update_user(self):
        if self._user_info.seating_unit_id is None :
            s_unit_id = 0
        else :
            s_unit_id = self._user_info.seating_unit_id

        q = "UPDATE tbl_client_users set employee_name = %s, \
            employee_code = %s, contact_no = %s, seating_unit_id = %s \
            Where client_id = %s and user_id = %s "
        values = [
            self._user_info.employee_name,
            self._user_info.employee_code, self._user_info.contact_no,
            s_unit_id,
            self._client_id, self._user_id,
        ]
        self._k_db.execute(q, values)

    def process_update_user(self):
        try:
            self.get_knowledge_connect()
            self._k_db.begin()
            self._update_user()
            self._k_db.commit()
            self._k_db.close()
            return True
        except Exception, e:
            print e
            self._k_db.rollback()
            raise client_process_error("E023")

class UpdateUserStatus(KnowledgedbConnect):
    def __init__(self, is_active, user_id, client_id, status_type="status"):
        super(SaveUsers, self).__init__()
        self._user_id = user_id
        self._is_active = is_active
        self._client_id = client_id
        self._status_type = status_type
        self.process_update_user_status()

    def _update_user_status(self):
        q = "UPDATE tbl_client_users set is_active = %s \
            Where client_id = %s and user_id = %s "
        values = [
            bool(self._is_active),
            self._client_id, self._user_id,
        ]
        self._k_db.execute(q, values)

    def _update_admin_status(self):
        q = "Update tbl_client_users set is_admin = %s \
            WHERE client_id = %s and user_id = %s "
        values = [
            self._is_active, self._client_id,
            self._user_id
        ]

        self._k_db.execute(q, values)

    def process_update_user_status(self):
        try:
            self.get_knowledge_connect()
            self._k_db.begin()
            if self._status_type == "status":
                self._update_user_status()
            elif self._status_type == "admin":
                self._update_admin_status()
            self._k_db.commit()
            self._k_db.close()
            return True
        except Exception, e:
            print e
            self._k_db.rollback()
            raise client_process_error("E024")

class UnitClose(KnowledgedbConnect):
    def __init__(self, unit_id):
        super(UnitClose, self).__init__()
        self._unit_id = unit_id
        self.process_close_unit()

    def _close_unit(self):
        q = "UPDATE tbl_units set is_active = 0 \
            Where unit_id = %s"
        values = [self._unit_id]
        self._k_db.execute(q, values)

    def process_close_unit(self):
        try:
            self.get_knowledge_connect()
            self._k_db.begin()
            self._close_unit()
            self._k_db.commit()
            self._k_db.close()
            return True
        except Exception, e:
            print e
            self._k_db.rollback()
            raise client_process_error("E025")
