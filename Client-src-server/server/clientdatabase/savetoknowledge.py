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
        print (
            KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
            KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
        )
        conn = mysql.connect(
            host=KNOWLEDGE_DB_HOST, port=KNOWLEDGE_DB_PORT,
            user=KNOWLEDGE_DB_USERNAME, passwd=KNOWLEDGE_DB_PASSWORD,
            db=KNOWLEDGE_DATABASE_NAME
        )
        self._k_db = Database(conn)

    def get_knowledge_close(self):
        if self._k_db is not None :
            self._k_db.close()


class UpdateFileSpace(KnowledgedbConnect):
    def __init__(self, space_used, legal_entity_id):
        super(UpdateFileSpace, self).__init__()
        self._space_used = space_used
        self._legal_entity_id = legal_entity_id
        self.procee_update_space()

    def _update_space(self):
        # q = "Update tbl_client_groups set total_disk_space_used = %s " + \
        #     " where client_id = %s "
        q = "Update tbl_legal_entities set used_file_space = %s " + \
            " where legal_entity_id = %s "
        res = self._k_db.execute(q, [self._space_used, self._legal_entity_id])
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
            self._k_db.close()
            raise client_process_error("E021")


class SaveUsers(KnowledgedbConnect):
    def __init__(self, user_info, user_id, client_id):
        super(SaveUsers, self).__init__()
        self._user_id = user_id
        self._user_info = user_info
        self._client_id = client_id
        self.process_save_user()

    def _save_user(self):
        q = "select count(0) from tbl_client_users where " + \
                " client_id = %s and user_category_id = 1"
        row = self._k_db.select_one(q, [self._user_info["client_id"]])
        print "mangesh", row
        if row[0] > 0:
            return False
        else:
            q = "INSERT INTO tbl_client_users(user_id, user_category_id, client_id, " + \
                "seating_unit_id, service_provider_id, user_level, email_id, " + \
                "employee_name, employee_code, contact_no, mobile_no, address, " + \
                "is_service_provider, is_active, status_changed_on, is_disable, disabled_on, " + \
                " legal_entity_ids ) " + \
                "values(%s, %s, %s, %s, %s, %s, %s, %s, %s , %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = [
                self._user_id, self._user_info["user_category_id"],
                self._user_info["client_id"], self._user_info["seating_unit_id"],
                self._user_info["service_provider_id"], self._user_info["user_level"],
                self._user_info["email_id"], self._user_info["employee_name"],
                self._user_info["employee_code"], self._user_info["contact_no"],
                self._user_info["mobile_no"], self._user_info["address"],
                self._user_info["is_service_provider"], self._user_info["is_active"],
                self._user_info["status_changed_on"], self._user_info["is_disable"],
                self._user_info["disabled_on"], self._user_info["le_ids"]
            ]
            self._k_db.execute(q, values)

    def process_save_user(self):
        try:
            self.get_knowledge_connect()
            self._k_db._cursor = self._k_db._connection.cursor()
            self._save_user()
            self._k_db._cursor.close()
            self._k_db._connection.commit()
            self._k_db._connection.close()
        except Exception, e:
            print e
            self._k_db._cursor.close()
            self._k_db._connection.rollback()
            self._k_db._connection.close()
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
            " email_id = %s, is_service_provider = %s, user_level = %s,  " + \
            " legal_entity_ids = %s " + \
            " Where client_id = %s and user_id = %s "
        values = [
            self._user_info.employee_name,
            self._user_info.employee_code, self._user_info.contact_no,
            self._user_info.mobile_no, s_unit_id,
            self._user_info.email_id,
            int(self._user_info.is_service_provider),
            self._user_info.user_level,
            ",".join([str(x) for x in self._user_info.user_entity_ids]),
            self._client_id, self._user_info.user_id
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
            self._k_db._connection.close()
        except Exception, e:
            print e
            self._k_db._cursor.close()
            self._k_db._connection.rollback()
            self._k_db._connection.close()
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
            self._k_db.close()
            raise client_process_error("E024")


class UnitClose(KnowledgedbConnect):
    def __init__(self, unit_id, is_closed, closed_on, closed_by, remarks, msg_text):
        super(UnitClose, self).__init__()
        self._unit_id = unit_id
        self._is_closed = is_closed
        self._closed_on = closed_on
        self._closed_by = closed_by
        self._remarks = remarks
        self._msg_text = msg_text
        self.process_close_unit()

    def _close_unit(self):
        q = "UPDATE tbl_units set is_closed = %s, closed_on = %s, closed_by = %s, closed_remarks = %s " + \
            " Where unit_id = %s"
        values = [
            self._is_closed, self._closed_on, self._closed_by, self._remarks, self._unit_id
        ]
        self._k_db.execute(q, values)

        q = "INSERT into tbl_messages set user_category_id = 5, message_heading = %s, " + \
            "message_text = %s, created_by = (select created_by from tbl_units where unit_id = %s), created_on = %s "
        values = [
            "Unit Closure", self._msg_text, self._unit_id, self._closed_on
        ]
        self._k_db.execute(q, values)

        q = "INSERT into tbl_message_users set message_id = (select LAST_INSERT_ID()), " + \
            "user_id = (select user_id from tbl_user_clients where client_id = (select client_id from tbl_units " + \
            "where unit_id = %s));"
        values = [
            self._unit_id
        ]
        self._k_db.execute(q, values)

        q = "INSERT into tbl_messages set user_category_id = 1, message_heading = %s, " + \
            "message_text = %s, created_by = (select created_by from tbl_units where unit_id = %s), created_on = %s "
        values = [
            "Unit Closure", self._msg_text, self._unit_id, self._closed_on
        ]
        self._k_db.execute(q, values)

        q = "INSERT into tbl_message_users set message_id = (select LAST_INSERT_ID()), " + \
            "user_id = (select user_id from tbl_user_login_details where user_category_id = 1 limit 1);"

        self._k_db.execute(q, None)

    def process_close_unit(self):
        try:
            self.get_knowledge_connect()
            self._k_db._cursor = self._k_db._connection.cursor()
            self._close_unit()
            self._k_db._cursor.close()
            self._k_db._connection.commit()
            self._k_db._connection.close()
            return True
        except Exception, e:
            print e
            self._k_db._cursor.close()
            self._k_db._connection.rollback()
            self._k_db._connection.close()
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
            self._k_db._connection.close()
        except Exception, e:
            print e
            self._k_db._cursor.close()
            self._k_db._connection.rollback()
            self._k_db._connection.close()
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
            self._k_db.close()
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
            self._k_db._connection.close()
        except Exception, e:
            print e
            self._k_db._cursor.close()
            self._k_db._connection.rollback()
            self._k_db._connection.close()
            raise client_process_error("E090")

class SaveClientActivity(KnowledgedbConnect):
    def __init__(self, values):
        self._query = " INSERT INTO tbl_client_activity_log " + \
            " (client_id, legal_entity_id, unit_id, user_category_id, " + \
            " user_id, form_id, action, created_on) " + \
            " VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
        self._values = values
        self.process_save_activity()

    def process_save_activity(self):
        try :
            self.get_knowledge_connect()
            self._k_db._cursor = self._k_db._connection.cursor()

            self._k_db.execute(self._query, self._values)

            self._k_db._cursor.close()
            self._k_db._connection.commit()
            self._k_db._connection.close()
        except Exception, e:
            print e
            print (
                KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
                KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
            )
            self._k_db._cursor.close()
            self._k_db._connection.rollback()
            self._k_db._connection.close()
            raise client_process_error("E091")
