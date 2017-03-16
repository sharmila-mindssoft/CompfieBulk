import MySQLdb as mysql
from server.dbase import Database
from server.exceptionmessage import client_process_error
from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
)

__all__ = [
    "KnowledgedbConnect",
    "UpdateFileSpace",
    "SaveUsers", "UpdateUsers", "UpdateUserStatus",
    "UnitClose", "SaveOptedStatus", "IsClientActive",
    "SaveGroupAdminName"
]


class KnowledgedbConnect(object):
    def __init__(self):
        self._k_db = None

    def get_knowledge_connect(self):
        conn = mysql.connect(
            host=KNOWLEDGE_DB_HOST, port=KNOWLEDGE_DB_PORT,
            user=KNOWLEDGE_DB_USERNAME, passwd=KNOWLEDGE_DB_PASSWORD,
            db=KNOWLEDGE_DATABASE_NAME
        )
        self._k_db = Database(conn)


class UpdateFileSpace(KnowledgedbConnect):
    def __init__(self, space_used, client_id):
        super(UpdateFileSpace, self).__init__()
        self._space_used = space_used
        self._client_id = client_id
        self.procee_update_space()

    def _update_space(self):
        q = "Update tbl_client_groups set total_disk_space_used = %s " + \
            " where client_id = %s "
        res = self._k_db.execute(q, [self._space_used, self._client_id])
        if res is False:
            raise client_process_error("E021")

    def procee_update_space(self):
        try:
            self.get_knowledge_connect()
            # self._k_db.begin()
            self._k_db._cursor = self._k_db._connection.cursor()
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

        q = "INSERT INTO tbl_client_users(user_id, user_category_id, client_id, " + \
            "seating_unit_id, service_provider_id, user_level, email_id, " + \
            "employee_name, employee_code, contact_no, mobile_no, address, " + \
            "is_service_provider, is_active, status_changed_on, is_disable, disabled_on) " + \
            "values(%s, %s, %s, %s, %s, %s, %s, %s, %s , %s, %s, %s, %s, %s, %s, %s, %s)"
        values = [
            self._user_id, self._user_info["user_category_id"],
            self._user_info["client_id"], self._user_info["seating_unit_id"],
            self._user_info["service_provider_id"], self._user_info["user_level"],
            self._user_info["email_id"], self._user_info["employee_name"],
            self._user_info["employee_code"], self._user_info["contact_no"],
            self._user_info["mobile_no"], self._user_info["address"],
            self._user_info["is_service_provider"], self._user_info["is_active"],
            self._user_info["status_changed_on"], self._user_info["is_disable"],
            self._user_info["disabled_on"]
        ]
        self._k_db.execute(q, values)

    def process_save_user(self):
        try:
            self.get_knowledge_connect()
            self._k_db._cursor = self._k_db._connection.cursor()
            self._save_user()
            self._k_db._cursor.close()
            self._k_db._connection.commit()
        except Exception, e:
            print e
            self._k_db._cursor.close()
            self._k_db._connection.rollback()
            raise client_process_error("E022")


class UpdateUsers(KnowledgedbConnect):
    def __init__(self, user_info, client_id):
        super(UpdateUsers, self).__init__()
        self._user_info = user_info
        self._client_id = client_id
        self.process_update_user()

    def _update_user(self):
        if self._user_info.seating_unit_id is None:
            s_unit_id = 0
        else:
            s_unit_id = self._user_info.seating_unit_id

        # if int(self._user_info.is_service_provider) == 1 :
        #     spid = self._user_info.service_provider_id
        # else :
        #     spid = 0

        q = "UPDATE tbl_client_users set employee_name = %s, " + \
            " employee_code = %s, contact_no = %s, mobile_no = %s, seating_unit_id = %s, " + \
            " email_id = %s, is_service_provider = %s, user_level = %s  " + \
            " Where client_id = %s and user_id = %s "
        values = [
            self._user_info.employee_name,
            self._user_info.employee_code, self._user_info.contact_no,
            self._user_info.mobile_no, s_unit_id,
            self._user_info.email_id,
            int(self._user_info.is_service_provider),
            self._user_info.user_level, self._client_id, self._user_info.user_id
        ]
        self._k_db.execute(q, values)

    def process_update_user(self):
        try:
            self.get_knowledge_connect()
            # self._k_db.begin()
            self._k_db._cursor = self._k_db._connection.cursor()
            self._update_user()
            self._k_db._cursor.close()
            self._k_db._connection.commit()
        except Exception, e:
            print e
            self._k_db._cursor.close()
            self._k_db._connection.rollback()
            raise client_process_error("E023")


class UpdateUserStatus(KnowledgedbConnect):
    def __init__(self, is_active, user_id, client_id, status_type="status"):
        super(UpdateUserStatus, self).__init__()
        self._user_id = user_id
        self._is_active = is_active
        self._client_id = client_id
        self._status_type = status_type
        self.process_update_user_status()

    def _update_user_status(self):
        q = "UPDATE tbl_client_users set is_active = %s " + \
            " Where client_id = %s and user_id = %s "
        values = [
            bool(self._is_active),
            self._client_id, self._user_id,
        ]
        self._k_db.execute(q, values)

    def _update_admin_status(self):
        q = "Update tbl_client_users set is_admin = %s " + \
            " WHERE client_id = %s and user_id = %s "
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
    def __init__(self, unit_id, is_closed, closed_on, closed_by, remarks):
        super(UnitClose, self).__init__()
        self._unit_id = unit_id
        self._is_closed = is_closed
        self._closed_on = closed_on
        self._closed_by = closed_by
        self._remarks = remarks
        self.process_close_unit()

    def _close_unit(self):
        q = "UPDATE tbl_units set is_closed = %s, closed_on = %s, closed_by = %s, closed_remarks = %s " + \
            " Where unit_id = %s"
        values = [
            self._is_closed, self._closed_on, self._closed_by, self._remarks, self._unit_id
        ]
        self._k_db.execute(q, values)

    def process_close_unit(self):
        try:
            self.get_knowledge_connect()
            self._k_db._cursor = self._k_db._connection.cursor()
            self._close_unit()
            self._k_db._cursor.close()
            self._k_db._connection.commit()
            return True
        except Exception, e:
            print e
            self._k_db._cursor.close()
            self._k_db._connection.rollback()
            raise client_process_error("E025")


class SaveOptedStatus(KnowledgedbConnect):
    def __init__(self, statu_data, updated_by, updated_on):
        super(SaveOptedStatus, self).__init__()
        self._statu_data = statu_data
        self._updated_by = updated_by
        self._updated_on = updated_on
        self.process_opted_status()

    def _update_opted_status(self):
        statutories = self._statu_data.statutories
        for s in statutories:
            client_compliance_id = s.client_compliance_id
            statutory_opted_status = int(s.applicable_status)
            not_applicable_remarks = s.not_applicable_remarks
            if not_applicable_remarks is None:
                not_applicable_remarks = ""
            compliance_id = s.compliance_id
            opted_status = int(s.compliance_opted_status)
            remarks = s.compliance_remarks
            if remarks is None:
                remarks = ""
            q = "UPDATE tbl_client_compliances SET " + \
                " statutory_opted_status = %s, " + \
                " remarks = %s, " + \
                " compliance_opted_status = %s, " + \
                " not_opted_remarks = %s, " + \
                " client_opted_by = %s, " + \
                " client_opted_on = %s " + \
                " WHERE client_compliance_id = %s AND " + \
                " compliance_id = %s"
            self._k_db.execute(q, [
                statutory_opted_status,
                not_applicable_remarks,
                opted_status,
                remarks,
                self._updated_by,
                self._updated_on,
                client_compliance_id,
                compliance_id
            ])

    def process_opted_status(self):
        try:
            self.get_knowledge_connect()
            # self._k_db.begin()
            self._k_db._cursor = self._k_db._connection.cursor()
            self._update_opted_status()
            self._k_db._cursor.close()
            self._k_db._connection.commit()
        except Exception, e:
            print e
            self._k_db._cursor.close()
            self._k_db._connection.rollback()
            raise client_process_error("E026")


class IsClientActive(KnowledgedbConnect):
    def __init__(self, client_id):
        super(IsClientActive, self).__init__()
        self._client_id = client_id

    def _is_client_active(self):
        try:
            self.get_knowledge_connect()
            self._k_db.begin()
            q = "select count(0) from tbl_client_groups where " + \
                " client_id = %s and is_active = 1"
            row = self._k_db.select_one(q, [self._client_id])
            if row[0] > 0:
                status = True
            else:
                status = False
            self._k_db.close()
            return status
        except Exception, e:
            print e
            self._k_db.rollback()
            raise client_process_error("E027")

class SaveGroupAdminName(KnowledgedbConnect):
    def __init__(self, username, client_id):
        self.username = username
        self.client_id = client_id
        self.process_save_username()

    def _update_groupadmin_uname(self):

        q = "UPDATE tbl_client_groups SET " + \
            " group_admin_username = %s " + \
            " WHERE client_id = %s "

        self._k_db.execute(q, [
            self.username, self.client_id
        ])

    def process_save_username(self):
        try :
            self.get_knowledge_connect()
            self._k_db._cursor = self._k_db._connection.cursor()
            self._update_groupadmin_uname()
            self._k_db._cursor.close()
            self._k_db._connection.commit()
        except Exception, e:
            print e
            self._k_db._cursor.close()
            self._k_db._connection.rollback()
            raise client_process_error("E026")
