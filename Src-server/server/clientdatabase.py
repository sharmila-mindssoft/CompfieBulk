import os
import threading
import json
import logger
import datetime
from dateutil import relativedelta
from types import *

from protocol import (
    core, general, clienttransactions, dashboard,
    clientreport, clientadminsettings, clientuser,
    mobile
)
from database import Database
from Currentcompliancetask import ComplianceTask
from server.emailcontroller import EmailHandler
from server.constants import KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME, KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME


__all__ = [
    "ClientDatabase"
]
ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")
CLIENT_DOCS_BASE_PATH = os.path.join(ROOT_PATH, "clientdocuments")
CLIENT_DOCS_DOWNLOAD_URL = "/client/client_documents"
FORMAT_DOWNLOAD_URL = "/client/compliance_format"
email = EmailHandler()

class ClientDatabase(Database):
    def __init__(
        self, host, port,
        username, password, database_name
    ):
        super(ClientDatabase, self).__init__(
            host, port, username, password, database_name
        )
        self._compliance_task = ComplianceTask(host, port, username, password, database_name)
        self._compliance_task.connect()
        self.initialize_table_names()

    def execute(self, query) :
        assert self._cursor is not None
        result = self._cursor.execute(query)
        return result

    def select_one(self, query, client_id=None) :
        assert self._cursor is not None
        self._cursor.execute(query)
        result = self._cursor.fetchone()
        return result

    def select_all(self, query, client_id=None) :
        assert self._cursor is not None
        self._cursor.execute(query)
        return self._cursor.fetchall()

    def initialize_table_names(self):
        self.tblActivityLog = "tbl_activity_log"
        self.tblAdmin = "tbl_admin"
        self.tblApprovalStatus = "tbl_approval_status"
        self.tblAssignedCompliances = "tbl_assigned_compliances"
        self.tblBusinessGroups = "tbl_business_groups"
        self.tblClientCompliances = "tbl_client_compliances"
        self.tblClientConfigurations = "tbl_client_configurations"
        self.tblClientGroups = "tbl_client_groups"
        self.tblClientStatutories = "tbl_client_statutories"
        self.tblComplianceActivityLog = "tbl_compliance_activity_log"
        self.tblComplianceDurationType = "tbl_compliance_duration_type"
        self.tblComplianceFrequency = "tbl_compliance_frequency"
        self.tblComplianceHistory = "tbl_compliance_history"
        self.tblComplianceRepeatType = "tbl_compliance_repeat_type"
        self.tblComplianceStatus = "tbl_compliance_status"
        self.tblCompliances = "tbl_compliances"
        self.tblCountries = "tbl_countries"
        self.tblDivisions = "tbl_divisions"
        self.tblDomains = "tbl_domains"
        self.tblEmailVerification = "tbl_email_verification"
        self.tblFormType = "tbl_form_type"
        self.tblForms = "tbl_forms"
        self.tblLegalEntities = "tbl_legal_entities"
        self.tblMobileRegistration = "tbl_mobile_registration"
        self.tblNotificationTypes = "tbl_notification_types"
        self.tblNotificationUserLog = "tbl_notification_user_log"
        self.tblNotificationsLog = "tbl_notifications_log"
        self.tblReassignedCompliancesHistory = "tbl_reassigned_compliances_history"
        self.tblServiceProviders = "tbl_service_providers"
        self.tblSessionTypes = "tbl_session_types"
        self.tblStatutoryNotificationStatus = "tbl_statutory_notification_status"
        self.tblStatutoryNotificationsLog = "tbl_statutory_notifications_log"
        self.tblStatutoryNotificationsUnits = "tbl_statutory_notifications_units"
        self.tblUnits = "tbl_units"
        self.tblUserCountries = "tbl_user_countries"
        self.tblUserDomains = "tbl_user_domains"
        self.tblUserGroups = "tbl_user_groups"
        self.tblUserLoginHistory = "tbl_user_login_history"
        self.tblUserSessions = "tbl_user_sessions"
        self.tblUserUnits = "tbl_user_units"
        self.tblUsers = "tbl_users"

    #
    # Replication
    #

    def update_traild_id(self, audit_trail_id, get_type=None):
        if get_type is None :
            query = "UPDATE tbl_audit_log SET audit_trail_id=%s;" % (audit_trail_id)
        else :
            query = "UPDATE tbl_audit_log SET domain_trail_id=%s;" % (audit_trail_id)
        self.execute(query)

    def reset_domain_trail_id(self):
        q = "update tbl_audit_log set domain_trail_id=0"
        self.execute(q)

    def get_trail_id(self, type=None):
        if type is None :
            query = "select IFNULL(MAX(audit_trail_id), 0) as audit_trail_id from tbl_audit_log;"
            # row = self.select_one(query)
            # trail_id = row[0]
            # return trail_id
        else :
            query = "select IFNULL(MAX(domain_trail_id), 0) as audit_trail_id from tbl_audit_log;"
        row = self.select_one(query)
        trail_id = row[0]
        return trail_id

    def is_configured(self):
        columns = "count(1)"
        condition = "1"
        rows = self.get_data(
            self.tblClientGroups, columns, condition
        )
        if rows[0][0] <= 0:
            return False
        else:
            return True

    def is_in_contract(self):
        columns = "count(1)"
        condition = "now() between contract_from and DATE_ADD(contract_to, INTERVAL 1 DAY)"
        rows = self.get_data(
            self.tblClientGroups, columns, condition
        )
        if rows[0][0] <= 0:
            return False
        else:
            return True

    def is_contract_not_started(self):
        columns = "count(1)"
        condition = "now() < contract_from"
        rows = self.get_data(
            self.tblClientGroups, columns, condition
        )
        if rows[0][0] <= 0:
            return False
        else:
            return True

    def verify_login(self, username, password):
        tblAdminCondition = "password='%s' and username='%s'" % (
            password, username
        )
        admin_details = self.get_data(
            "tbl_admin", "*", tblAdminCondition
        )
        if (len(admin_details) == 0) :
            data_columns = [
                "user_id", "user_group_id", "email_id",
                "employee_name", "employee_code", "contact_no",
                "user_group_name", "form_ids", "is_admin",
                "service_provider_id"
            ]
            query = "SELECT t1.user_id, t1.user_group_id, t1.email_id, \
                t1.employee_name, t1.employee_code, t1.contact_no, \
                t2.user_group_name, t2.form_ids, t1.is_admin, \
                t1.service_provider_id \
                FROM tbl_users t1 INNER JOIN tbl_user_groups t2\
                ON t1.user_group_id = t2.user_group_id \
                WHERE t1.password='%s' and t1.email_id='%s' and t1.is_active=1" % (
                    password, username
                )
            data_list = self.select_one(query)
            if data_list is None :
                return False
            else :
                result = self.convert_to_dict(data_list, data_columns)
                if self.is_service_proivder_user(result["user_id"]):
                    if (
                        self.is_service_provider_in_contract(
                            result["service_provider_id"]
                        )
                    ):
                        # result["client_id"] = client_id
                        return result
                    else:
                        return "ContractExpired"
                else:
                    return result
        else :
            return True

    def get_user_forms(self, form_ids, client_id, is_admin):
        columns = "tf.form_id, tf.form_type_id, tft.form_type, tf.form_name, "
        columns += "tf.form_url, tf.form_order, tf.parent_menu "

        tables = [self.tblForms, self.tblFormType]
        aliases = ["tf",  "tft"]
        joinConditions = ["tf.form_type_id = tft.form_type_id"]
        whereCondition = " form_id in (%s) order by tf.form_order" % (
            form_ids
        )
        joinType = "left join"

        rows = self.get_data_from_multiple_tables(
            columns, tables, aliases, joinType,
            joinConditions, whereCondition
        )
        row_columns = [
            "form_id", "form_type_id", "form_type", "form_name", "form_url",
            "form_order", "parent_menu"
        ]
        result = self.convert_to_dict(rows, row_columns)
        return result

    def get_client_id_from_short_name(self, short_name):
        columns = "client_id"
        condition = "url_short_name = '%s'" % short_name
        rows = self.get_data(
            "tbl_client_groups", columns, condition
        )
        return rows[0][0]

    def get_short_name_from_client_id(self, client_id):
        columns = "url_short_name"
        rows = self.get_data(
            self.tblClientGroups, columns, "1"
        )
        return rows[0][0]

    def verify_username(self, username):
        columns = "count(*), user_id"
        condition = "email_id='%s' and is_active = 1" % (username)
        rows = self.get_data(
            self.tblUsers, columns, condition
        )
        count = rows[0][0]
        if count == 1:
            return rows[0][1]
        else:
            condition = "username='%s'" % username
            columns = "count(*)"
            rows = self.get_data(
                self.tblAdmin, columns, condition
            )
            count = rows[0][0]
            if count == 1:
                return 0
            else:
                return None

    def verify_password(self, password, user_id, client_id=None):
        columns = "count(*)"
        encrypted_password = self.encrypt(password)
        condition = "1"
        rows = None
        if user_id == 0:
            condition = "password='%s'" % (encrypted_password)
            rows = self.get_data(
                self.tblAdmin, columns, condition
            )
        else:
            condition = "password='%s' and user_id='%d'" % (
                encrypted_password, user_id
            )
            rows = self.get_data(
                self.tblUsers, columns, condition
            )
        if(int(rows[0][0]) <= 0):
            return False
        else:
            return True

    def update_password(self, password, user_id, client_id):
        columns = ["password"]
        values = [self.encrypt(password)]
        condition = "1"
        result = False
        condition = " user_id='%d'" % user_id
        result = self.update(
            self.tblUsers, columns, values, condition, client_id
        )
        if self.is_primary_admin(user_id) or user_id == 0:
            result = self.update(
                self.tblAdmin, columns, values, "1", client_id
            )
        if user_id != 0:
            columns = "employee_code, employee_name"
            condition = "user_id = '%d'" % user_id
            rows = self.get_data(self.tblUsers, columns, condition)
            employee_name = rows[0][1]
            if rows[0][0] is not None:
                employee_name = "%s - %s" % (rows[0][0], rows[0][1])
        else:
            employee_name = "Administrator"

        action = "\"%s\" has updated his/her password" % ( employee_name)
        self.save_activity(user_id, 0, action)

        if result:
            return True
        else:
            return False

    def delete_used_token(self, reset_token, client_id):
        condition = " verification_code='%s'" % reset_token
        if self.delete(self.tblEmailVerification, condition, client_id):
            return True
        else:
            return False

    def validate_reset_token(self, reset_token, client_id):
        column = "count(*), user_id"
        condition = " verification_code='%s'" % reset_token
        rows = self.get_data(
            self.tblEmailVerification, column, condition
        )
        count = rows[0][0]
        user_id = rows[0][1]
        if count == 1:
            column = "count(*)"
            condition = "user_id = '%d' and is_active = 1" % user_id
            rows = self.get_data(self.tblUsers, column, condition)
            if rows[0][0] > 0 or user_id == 0:
                return user_id
            else:
                return None
        else:
            return None

    def update_session_time(self, session_token):
        updated_on = self.get_date_time()
        q = "update tbl_user_sessions set \
        last_accessed_time='%s' where session_token = '%s' " % (
            str(updated_on), str(session_token)
        )
        self.execute(q)

    def remove_session(self, session_token):
        q = "delete from tbl_user_sessions where session_token = '%s'" % (session_token)
        self.execute(q)

    def chack_client_contract():
        return True

    def validate_session_token(self, client_id, session_token) :
        query = "SELECT t1.user_id, IFNULL(t2.is_service_provider, 0), IFNULL(t2.service_provider_id, 0) \
        FROM tbl_user_sessions t1 \
        INNER JOIN tbl_users t2 ON t1.user_id = t2.user_id AND t2.is_active = 1 \
            WHERE t1.session_token = '%s'" % (session_token)
        row = self.select_one(query)
        user_id = None
        if row :
            user_id = int(row[0])
            is_service_provider = int(row[1])
            service_id = int(row[2])
            if is_service_provider == 1 :
                res = self.is_service_provider_in_contract(service_id)
                if res :
                    self.update_session_time(session_token)
                    return user_id
            else :
                res = self.is_in_contract()
                if res :
                    self.update_session_time(session_token)
                    return user_id

        return None

    def get_forms(self, client_id):
        columns = "tf.form_id, tf.form_type_id, tft.form_type, "
        columns += "tf.form_name, tf.form_url, tf.form_order, tf.parent_menu"
        tables = [self.tblForms, self.tblFormType]
        aliases = ["tf",  "tft"]
        joinConditions = ["tf.form_type_id = tft.form_type_id"]
        whereCondition = " is_admin = 0 and tf.form_type_id not in (5) \
        order by tf.form_order, tf.form_name ASC"
        joinType = "left join"
        rows = self.get_data_from_multiple_tables(
            columns, tables, aliases, joinType,
            joinConditions, whereCondition
        )
        return rows

    def return_forms(self, client_id, form_ids=None):
        columns = "form_id, form_name"
        condition = "form_id != 24"
        if form_ids is not None:
            condition += " AND form_id in (%s)" % form_ids
        forms = self.get_data(
            self.tblForms, columns, condition
        )
        results = []
        for form in forms:
            results.append(general.AuditTrailForm(form[0], form[1]))
        return results

    def get_admin_id(self):
        columns = "admin_id"
        condition = "1"
        rows = self.get_data(self.tblAdmin, columns, condition)
        return rows[0][0]

    def get_countries(self):
        query = "SELECT distinct t1.country_id, t1.country_name, \
            t1.is_active FROM tbl_countries t1 "
        rows = self.select_all(query)
        columns = ["country_id", "country_name", "is_active"]
        result = self.convert_to_dict(rows, columns)
        return self.return_countries(result)

    def get_countries_for_user(self, user_id, client_id=None) :
        admin_id = self.get_admin_id()
        query = "SELECT distinct t1.country_id, t1.country_name, \
            t1.is_active FROM tbl_countries t1 "
        if user_id > 0 and user_id != admin_id:
            query = query + " INNER JOIN tbl_user_countries t2 \
                ON t1.country_id = t2.country_id WHERE t2.user_id = %s" % (
                    user_id
                )
        rows = self.select_all(query)
        columns = ["country_id", "country_name", "is_active"]
        result = self.convert_to_dict(rows, columns)
        return self.return_countries(result)

    def return_countries(self, data) :
        results = []

        for d in data :
            results.append(core.Country(
                d["country_id"], d["country_name"], bool(d["is_active"])
            ))
        return results

    def get_domains(self):
        query = "SELECT distinct t1.domain_id, t1.domain_name, \
            t1.is_active FROM tbl_domains t1 "
        rows = self.select_all(query)
        columns = ["domain_id", "domain_name", "is_active"]
        result = self.convert_to_dict(rows, columns)
        return self.return_domains(result)

    def get_domains_for_user(self, user_id, client_id=None) :
        admin_id = self.get_admin_id()
        query = "SELECT distinct t1.domain_id, t1.domain_name, \
            t1.is_active FROM tbl_domains t1 "
        if user_id > 0 and user_id != admin_id:
            query = query + " INNER JOIN tbl_user_domains t2 ON \
                t1.domain_id = t2.domain_id WHERE t2.user_id = %s" % (user_id)
        rows = self.select_all(query)
        columns = ["domain_id", "domain_name", "is_active"]
        result = self.convert_to_dict(rows, columns)
        return self.return_domains(result)

    def return_domains(self, data):
        results = []
        for d in data :
            results.append(core.Domain(
                d["domain_id"], d["domain_name"], bool(d["is_active"])
            ))
        return results

    def get_business_groups_for_user(self, business_group_ids):
        columns = "business_group_id, business_group_name"
        condition = "1"
        if business_group_ids is not None:
            condition = "business_group_id in (%s) ORDER BY business_group_name" % business_group_ids
        rows = self.get_data(
            self.tblBusinessGroups, columns, condition
        )
        columns = ["business_group_id", "business_group_name"]
        result = self.convert_to_dict(rows, columns)
        return self.return_business_groups(result)

    def return_business_groups(self, business_groups):
        results = []
        for business_group in business_groups :
            results.append(core.ClientBusinessGroup(
                business_group["business_group_id"],
                business_group["business_group_name"]
            ))
        return results

    def get_legal_entities_for_user(self, legal_entity_ids):
        columns = "legal_entity_id, legal_entity_name, business_group_id"
        condition = "1"
        if legal_entity_ids is not None:
            condition = "legal_entity_id in (%s) ORDER BY legal_entity_name" % legal_entity_ids
        rows = self.get_data(
            self.tblLegalEntities, columns, condition
        )
        columns = ["legal_entity_id", "legal_entity_name", "business_group_id"]
        result = self.convert_to_dict(rows, columns)
        return self.return_legal_entities(result)

    def return_legal_entities(self, legal_entities):
        results = []
        for legal_entity in legal_entities :
            b_group_id = None
            if legal_entity["business_group_id"] > 0:
                b_group_id = int(legal_entity["business_group_id"])
            results.append(core.ClientLegalEntity(
                legal_entity["legal_entity_id"],
                legal_entity["legal_entity_name"],
                b_group_id
            ))
        return results

    def get_divisions_for_user(self, division_ids):
        columns = "division_id, division_name, legal_entity_id, business_group_id"
        condition = "1"
        if division_ids is not None:
            condition = "division_id in (%s) ORDER BY division_name" % division_ids
        rows = self.get_data(
            self.tblDivisions, columns, condition
        )
        columns = [
            "division_id", "division_name", "legal_entity_id",
            "business_group_id"
        ]
        result = self.convert_to_dict(rows, columns)
        return self.return_divisions(result)

    def return_divisions(self, divisions):
        results = []
        for division in divisions :
            division_obj = core.ClientDivision(
                division["division_id"], division["division_name"],
                division["legal_entity_id"], division["business_group_id"]
            )
            results.append(division_obj)
        return results

    def get_units_for_user(self, unit_ids, client_id=None):
        columns = "unit_id, unit_code, unit_name, address, division_id, domain_ids, country_id,"
        columns += " legal_entity_id, business_group_id, is_active, is_closed"
        condition = "is_closed = 0"
        if unit_ids is not None:
            condition = "unit_id in (%s) ORDER BY unit_name" % unit_ids
        rows = self.get_data(
            self.tblUnits, columns, condition
        )
        columns = [
            "unit_id", "unit_code", "unit_name", "unit_address", "division_id","domain_ids", "country_id",
            "legal_entity_id", "business_group_id", "is_active", "is_closed"
        ]
        result = self.convert_to_dict(rows, columns)
        return self.return_units(result)

    def get_units_closure_for_user(self, unit_ids):
        columns = "unit_id, unit_code, unit_name, address, division_id, domain_ids, country_id,"
        columns += " legal_entity_id, business_group_id, is_active, is_closed"
        condition = "1"
        if unit_ids is not None:
            condition = "unit_id in (%s)  ORDER BY unit_id ASC" % unit_ids
        rows = self.get_data(
            self.tblUnits, columns, condition
        )
        columns = [
            "unit_id", "unit_code", "unit_name", "unit_address", "division_id","domain_ids", "country_id",
            "legal_entity_id", "business_group_id", "is_active", "is_closed"
        ]

        result = self.convert_to_dict(rows, columns)
        return self.return_units(result)

    def get_units_for_user_grouped_by_industry(self, unit_ids):
        condition = "1"
        if unit_ids is not None:
            condition = "unit_id in (%s)" % unit_ids
        industry_column = "industry_name"
        industry_condition = condition + " group by industry_name"
        industry_rows = self.get_data(
            self.tblUnits, industry_column, industry_condition
        )

        columns = "unit_id, concat(unit_code,'-',unit_name), address, division_id,"+\
        " legal_entity_id, business_group_id, country_id, domain_ids"
        industry_wise_units =[]
        for industry in industry_rows:
            industry_name = industry[0]
            units = []
            ad_condition = " and industry_name = '%s' and is_active = 1" % industry_name
            rows = self.get_data(
                self.tblUnits, columns, condition+ad_condition
            )
            for unit in rows:
                domain_ids_list = [int(x) for x in unit[7].split(",")]
                division_id = None
                b_group_id = None
                if unit[3] > 0 :
                    division_id = unit[3]
                if unit[5] > 0 :
                    b_group_id = unit[5]
                units.append(
                    clienttransactions.PastRecordUnits(
                        unit[0], unit[1], unit[2], division_id, unit[4],
                        b_group_id, unit[6], domain_ids_list
                    )
                )
            industry_wise_units.append(clienttransactions.IndustryWiseUnits(industry_name, units))
        return industry_wise_units

    def return_units(self, units):
        results = []
        for unit in units :
            division_id = None
            b_group_id = None
            if unit["division_id"] > 0 :
                division_id = unit["division_id"]
            if unit["business_group_id"] > 0 :
                b_group_id = unit["business_group_id"]
            results.append(core.ClientUnit(
                unit["unit_id"], division_id, unit["legal_entity_id"],
                b_group_id, unit["unit_code"],
                unit["unit_name"], unit["unit_address"], bool(unit["is_active"]),
                [int(x) for x in unit["domain_ids"].split(",")], unit["country_id"],
                bool(unit["is_closed"])
            ))
        return results

    def save_activity(self, user_id, form_id, action, client_id=None):
        created_on = self.get_date_time()
        activityId = self.get_new_id("activity_log_id", "tbl_activity_log", client_id)
        query = "INSERT INTO tbl_activity_log \
            (activity_log_id, user_id, form_id, action, created_on) \
            VALUES (%s, %s, %s, '%s', '%s')" % (
                activityId, user_id, form_id, action, created_on
            )
        self.execute(query)
        return True

#
# User Privilege
#

    def generate_new_user_privilege_id(self, client_id) :
        return self.get_new_id("user_group_id", self.tblUserGroups, client_id)

    def is_duplicate_user_privilege(self, user_group_id, user_privilege_name,
        client_id):
        condition = "user_group_name ='%s' AND user_group_id != '%d'" %(
            user_privilege_name, user_group_id)
        return self.is_already_exists(self.tblUserGroups, condition)

    def get_user_privilege_details_list(self, client_id):
        columns = "user_group_id, user_group_name, form_ids, is_active"
        rows = self.get_data(
            self.tblUserGroups, columns, "1 ORDER BY user_group_name"
        )
        return rows

    def get_user_privileges(self, client_id):
        columns = "user_group_id, user_group_name, is_active"
        rows = self.get_data(
            self.tblUserGroups, columns, "1 ORDER BY user_group_name"
        )

        columns = ["user_group_id", "user_group_name", "is_active"]
        result = self.convert_to_dict(rows, columns)
        return self.return_user_privileges(result)

    def return_user_privileges(self, user_privileges):
        results = []
        for user_privilege in user_privileges :
            results.append(core.UserGroup(
                user_privilege["user_group_id"], user_privilege["user_group_name"],
                bool(user_privilege["is_active"])
            ))
        return results

    def save_user_privilege(self, user_group_id, user_privilege, session_user, client_id):
        columns = ["user_group_id", "user_group_name","form_ids", "is_active",
                  "created_on", "created_by", "updated_on", "updated_by"]
        values_list =  [user_group_id, user_privilege.user_group_name,
                        ",".join(str(x) for x in user_privilege.form_ids), 1,
                        self.get_date_time(), session_user,self.get_date_time(),
                        session_user]
        result = self.insert(self.tblUserGroups, columns, values_list)

        action = "Created User Group \"%s\"" % user_privilege.user_group_name
        self.save_activity(session_user, 3, action, client_id)

        return result

    def update_user_privilege(self, user_privilege, session_user, client_id):
        columns = ["user_group_name","form_ids", "updated_on", "updated_by"]
        values =  [ user_privilege.user_group_name, ",".join(str(x) for x in user_privilege.form_ids),
                    self.get_date_time(),session_user]
        condition = "user_group_id='%d'" % user_privilege.user_group_id
        result = self.update(self.tblUserGroups, columns, values, condition)

        action = "Updated User Group \"%s\"" % user_privilege.user_group_name
        self.save_activity(session_user, 3, action)

        return result

    def update_user_privilege_status(self, user_group_id, is_active, session_user, client_id):
        is_active = 0 if is_active != True else 1
        columns = ["is_active", "updated_by", "updated_on"]
        values = [is_active, session_user, self.get_date_time()]
        condition = "user_group_id='%d'" % user_group_id
        result = self.update(self.tblUserGroups, columns, values, condition)

        action_column = "user_group_name"
        rows = self.get_data(
            self.tblUserGroups, action_column, condition
        )
        user_group_name = rows[0][0]
        action = None
        if is_active == 0:
            action = "Deactivated user group \"%s\"" % user_group_name
        else:
            action = "Activated user group \"%s\"" % user_group_name
        self.save_activity(session_user, 3, action, client_id)
        return result

#
#   User
#

    def generate_new_user_id(self, client_id):
        return self.get_new_id("user_id",self.tblUsers, client_id)

    def is_duplicate_user_email(self, user_id, email_id, client_id):
        flag1 = False
        flag2 = False
        columns = "count(*)"
        condition = "username = '%s'" % email_id
        rows = self.get_data(self.tblAdmin, columns, condition)
        if rows[0][0] > 0 :
            flag1 = True
        else:
            flag1 = False
        condition = "email_id ='%s' AND user_id != '%d'" %(
            email_id, user_id)
        flag2 = self.is_already_exists(self.tblUsers, condition, client_id)
        return (flag1 or flag2)

    def is_duplicate_employee_code(self, user_id, employee_code, client_id):
        condition = "employee_code ='%s' AND user_id != '%d'" %(
            employee_code, user_id)
        return self.is_already_exists(self.tblUsers, condition, client_id)

    def get_user_details(self, client_id, session_user):
        unit_ids = None
        if not self.is_primary_admin(session_user):
            unit_ids = self.get_user_unit_ids(session_user)
        columns = "user_id, email_id, user_group_id, employee_name,"+\
        "employee_code, contact_no, seating_unit_id, user_level, "+\
        " is_admin, is_service_provider, service_provider_id, is_active,\
        is_primary_admin"
        condition = "1 ORDER BY employee_name"
        rows =  self.get_data(
            self.tblUsers+ " tu",columns, condition
        )
        columns = ["user_id", "email_id", "user_group_id", "employee_name",
        "employee_code", "contact_no", "seating_unit_id", "user_level",
        "is_admin", "is_service_provider", "service_provider_id", "is_active",
        "is_primary_admin"]
        result = self.convert_to_dict(rows, columns)
        return self.return_user_details(result, client_id, unit_ids)

    def return_user_details(
        self, users, client_id, unit_ids=None
    ):
        unit_ids_list = []
        if unit_ids not in [None, "", "None"]:
            try :
                unit_ids_list = [int(x) for x in unit_ids.split(",")]
            except e :
                unit_ids_list = []
        results = []
        for user in users :
            query = "select unit_id from %s tuu where \
            user_id = '%d'" % (self.tblUserUnits, user["user_id"])
            rows = self.select_all(query)
            user_unit_ids = []
            for row in rows:
                user_unit_ids.append(row[0])
            if len(unit_ids_list) > 0:
                if len(user_unit_ids) > 0:
                    if set(user_unit_ids) & set(unit_ids_list):
                        pass
                    else:
                        continue
            countries = self.get_user_countries(user["user_id"], client_id)
            domains = self.get_user_domains(user["user_id"], client_id)
            units = self.get_user_unit_ids(user["user_id"], client_id)
            results.append(core.ClientUser(user["user_id"], user["email_id"],
                user["user_group_id"], user["employee_name"],
                user["employee_code"], user["contact_no"],
                user["seating_unit_id"], user["user_level"],
                [int(x) for x in countries.split(",")] if countries != None else [],
                [int(x) for x in domains.split(",")] if domains != None else [],
                [int(x) for x in units.split(",")] if units != None else [],
                bool(user["is_admin"]), bool(user["is_service_provider"]),
                user["service_provider_id"], bool(user["is_active"]),
                bool(user["is_primary_admin"])
            ))
        return results

    def get_users(self, client_id):
        columns = "user_id, employee_name, employee_code, is_active"
        condition = "1"
        rows = self.get_data(
            self.tblUsers, columns, condition
        )
        columns = ["user_id", "employee_name", "employee_code", "is_active"]
        result = self.convert_to_dict(rows, columns)
        return self.return_users(result)

    def get_users_by_id(self, user_ids, client_id):
        columns = "user_id, employee_name, employee_code, is_active"
        condition = " user_id in (%s)" % user_ids
        rows = self.get_data(
            self.tblUsers, columns, condition
        )
        columns = ["user_id", "employee_name", "employee_code", "is_active"]
        result = self.convert_to_dict(rows, columns)
        return self.return_users(result)

    def return_users(self, users):
        results = []
        for user in users :
            if user["employee_code"] is not None:
                employee_name = "%s - %s" % (user["employee_code"],user["employee_name"])
            else:
                employee_name = "Administrator"
            results.append(core.User(
                user["user_id"], employee_name, bool(user["is_active"])
            ))
        return results

    def notify_user(
        self, short_name, email_id, password, employee_name, employee_code
    ):
        try:
            email.send_user_credentials(
                short_name, email_id, password, employee_name, employee_code
            )
        except Exception, e:
            logger.logClient("error", "clientdatabase.py-notify-user", e)
            print "Error while sending email : {}".format(e)

    def save_user(self, user_id, user, session_user, client_id):
        result1 = None
        result2 = None
        result3 = None
        current_time_stamp = self.get_date_time()
        user.is_service_provider = 0 if user.is_service_provider is False else 1
        columns = [
            "user_id", "user_group_id", "email_id", "password", "employee_name",
            "employee_code", "contact_no", "user_level",
            "is_admin", "is_service_provider", "created_by", "created_on",
            "updated_by", "updated_on"
        ]
        encrypted_password, password = self.generate_and_return_password()
        values = [
            user_id, user.user_group_id, user.email_id,
            encrypted_password, user.employee_name,
            user.employee_code.replace(" ", ""), user.contact_no, user.user_level,
            0, user.is_service_provider, session_user, current_time_stamp,
            session_user, current_time_stamp
        ]
        if user.is_service_provider == 1:
            columns.append("service_provider_id")
            values.append(user.service_provider_id)
        else:
            columns.append("seating_unit_id")
            values.append(user.seating_unit_id)

        result1 = self.insert(self.tblUsers, columns, values, client_id)

        db_con = Database(
            KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
            KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
        )
        db_con.connect()
        db_con.begin()
        columns = "client_id, user_id, email_id, employee_name, \
        employee_code, contact_no, created_on, is_admin, is_active"
        if user.seating_unit_id is not None:
            columns += ", seating_unit_id"
        q = "INSERT INTO tbl_client_users ({}) values ('{}', '{}', '{}', '{}', \
        '{}', '{}', now(), 0, 1".format(
            columns, client_id, user_id, user.email_id, user.employee_name,
            user.employee_code, user.contact_no
        )

        if user.seating_unit_id is not None:
            q += ",'{}')".format(user.seating_unit_id)
        else:
            q += ")"
        db_con.execute(q)
        db_con.commit()
        db_con.close()

        country_columns = ["user_id", "country_id"]
        country_values_list = []
        for country_id in user.country_ids:
            country_value_tuple = (user_id, int(country_id))
            country_values_list.append(country_value_tuple)
        result2 = self.bulk_insert(self.tblUserCountries, country_columns, country_values_list, client_id)

        domain_columns = ["user_id", "domain_id"]
        domain_values_list = []
        for domain_id in user.domain_ids:
            domain_value_tuple = (user_id, int(domain_id))
            domain_values_list.append(domain_value_tuple)
        result3 = self.bulk_insert(self.tblUserDomains, domain_columns, domain_values_list, client_id)

        unit_columns = ["user_id", "unit_id"]
        unit_values_list = []
        for unit_id in user.unit_ids:
            unit_value_tuple = (user_id, int(unit_id))
            unit_values_list.append(unit_value_tuple)
        result4 = self.bulk_insert(self.tblUserUnits, unit_columns, unit_values_list, client_id)

        action = "Created user \"%s - %s\"" % (user.employee_code, user.employee_name)
        self.save_activity(session_user, 4, action, client_id)
        short_name = self.get_short_name_from_client_id(
            client_id
        )
        notify_user_thread = threading.Thread(
            target=self.notify_user, args=[
                short_name, user.email_id, password, user.employee_name, user.employee_code
            ]
        )
        notify_user_thread.start()
        return (result1 and result2 and result3 and result4)

    def update_user(self, user, session_user, client_id):
        result1 = None
        result2 = None
        result3 = None
        result4 = None

        current_time_stamp = self.get_date_time()
        user.is_service_provider = 0 if user.is_service_provider == False else 1
        columns = [ "user_group_id", "employee_name", "employee_code",
                "contact_no", "seating_unit_id", "user_level",
                "is_service_provider", "updated_on", "updated_by"]
        values = [ user.user_group_id, user.employee_name, user.employee_code.replace(" ", ""),
                user.contact_no, user.seating_unit_id, user.user_level,
                user.is_service_provider, current_time_stamp, session_user ]
        condition = "user_id='%d'" % user.user_id

        if user.is_service_provider == 1:
            columns.append("service_provider_id")
            values.append(user.service_provider_id)
        else:
            columns.append("seating_unit_id")
            values.append(user.seating_unit_id)

        result1 = self.update(self.tblUsers, columns, values, condition, client_id)
        self.delete(self.tblUserCountries, condition, client_id)
        self.delete(self.tblUserDomains, condition, client_id)
        self.delete(self.tblUserUnits, condition, client_id)

        country_columns = ["user_id", "country_id"]
        country_values_list = []
        for country_id in user.country_ids:
            country_value_tuple = (user.user_id, int(country_id))
            country_values_list.append(country_value_tuple)
        result2 = self.bulk_insert(self.tblUserCountries, country_columns, country_values_list, client_id)

        domain_columns = ["user_id", "domain_id"]
        domain_values_list = []
        for domain_id in user.domain_ids:
            domain_value_tuple = (user.user_id, int(domain_id))
            domain_values_list.append(domain_value_tuple)
        result3 = self.bulk_insert(self.tblUserDomains, domain_columns, domain_values_list, client_id)

        db_con = Database(
            KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
            KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
        )
        db_con.connect()
        db_con.begin()
        condition = "where client_id ='{}' and user_id = '{}'".format(client_id, user.user_id)
        q = "UPDATE tbl_client_users set \
        employee_name = '{}', employee_code = '{}', \
        contact_no = '{}' ".format(
             user.employee_name, user.employee_code, user.contact_no,
             user.seating_unit_id
        )
        if user.seating_unit_id is not None:
            q += ", seating_unit_id = '{}' {}".format(user.seating_unit_id, condition)
        else:
            q += condition
        db_con.execute(q)
        db_con.commit()
        db_con.close()

        unit_columns = ["user_id", "unit_id"]
        unit_values_list = []
        for unit_id in user.unit_ids:
            unit_value_tuple = (user.user_id, int(unit_id))
            unit_values_list.append(unit_value_tuple)
        result4 = self.bulk_insert(self.tblUserUnits, unit_columns, unit_values_list, client_id)

        action = "Updated user \"%s - %s\"" % (user.employee_code, user.employee_name)
        self.save_activity(session_user, 4, action, client_id)

        return (result1 and result2 and result3 and result4)

    def update_user_status(self, user_id, is_active, session_user, client_id):
        columns = ["is_active", "updated_on", "updated_by"]
        is_active = 1 if is_active != False else 0
        values = [is_active, self.get_date_time(), session_user]
        condition = "user_id = '%d'"% user_id

        db_con = Database(
            KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
            KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
        )
        db_con.connect()
        db_con.begin()
        q = "UPDATE tbl_client_users set is_active = '{}' where \
        user_id = '{}'".format(
            is_active, user_id
        )
        db_con.execute(q)
        db_con.commit()
        db_con.close()

        action_column = "employee_code, employee_name"
        rows = self.get_data(
            self.tblUsers, action_column, condition
        )
        employee_code = rows [0][0]
        employee_name = rows[0][1]
        if is_active == 1:
            action = "Activated user \"%s - %s\"" % (employee_code, employee_name)
        else:
            action = "Dectivated user \"%s - %s\"" % (employee_code, employee_name)
        self.save_activity(session_user, 4, action, client_id)

        return self.update(self.tblUsers, columns, values, condition, client_id)

    def update_admin_status(self, user_id, is_admin, session_user, client_id):
        columns = ["is_admin", "updated_on" , "updated_by"]
        is_admin = 1 if is_admin is not False else 0
        values = [is_admin, self.get_date_time(), session_user]
        condition = "user_id='%d'" % user_id
        result = self.update(self.tblUsers, columns, values, condition, client_id)

        action_column = "employee_code, employee_name"
        rows = self.get_data(
            self.tblUsers, action_column, condition
        )
        employee_code = rows[0][0]
        employee_name = rows[0][1]

        db_con = Database(
            KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
            KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
        )
        db_con.connect()
        db_con.begin()
        q = "UPDATE tbl_client_users set is_admin = '{}' where \
        user_id = '{}'".format(
            is_admin, user_id
        )
        db_con.execute(q)
        db_con.commit()
        db_con.close()

        action = None
        if is_admin == 0:
            action = "User \"%s - %s\" was demoted from admin status" % (employee_code, employee_name)
        else:
            action = "User \"%s - %s\" was promoted to admin status" % (employee_code, employee_name)
        self.save_activity(session_user, 4, action, client_id)

        return result

    def get_user_company_details(self, user_id, client_id=None):
        admin_id = self.get_admin_id()
        columns = "unit_id"
        condition = " 1 "
        rows = None
        if user_id > 0 and user_id != admin_id:
            condition = "  user_id = '%d'" % user_id
            rows = self.get_data(
                self.tblUserUnits, columns, condition
            )
        else:
            rows = self.get_data(
                self.tblUnits, columns, condition
            )
        unit_ids = None
        division_ids = None
        legal_entity_ids = None
        business_group_ids = None
        if len(rows) > 0:
            result = []
            for row in rows:
                result.append(row[0])
            unit_ids = ",".join(str(x) for x in result)

        if unit_ids not in [None, "None", ""]:
            columns = "group_concat(distinct division_id), group_concat(distinct legal_entity_id), \
            group_concat(distinct business_group_id)"
            unit_condition = "1"
            if unit_ids is not None :
                unit_condition = "unit_id in (%s)" % unit_ids
            rows = self.get_data(
                self.tblUnits , columns, unit_condition
            )
            division_ids = rows[0][0]
            legal_entity_ids = rows[0][1]
            business_group_ids = rows[0][2]

        return unit_ids, division_ids, legal_entity_ids, business_group_ids

    def get_user_countries(self, user_id, client_id=None):
        columns = "group_concat(country_id)"
        table = self.tblCountries
        result = None
        condition = 1
        if user_id > 0:
            table = self.tblUserCountries
            condition = " user_id = '%d'" % user_id
        rows = self.get_data(
            table, columns, condition
        )
        if rows :
            result = rows[0][0]
        return result

    def get_user_domains(self, user_id, client_id=None):
        columns = "domain_id"
        table = self.tblDomains
        result = None
        condition = 1
        if user_id > 0:
            table  = self.tblUserDomains
            condition = " user_id = '%d'" % user_id
        rows = self.get_data(
            table, columns, condition
        )
        result = ""
        if rows:
            for index, row in enumerate(rows):
                if index == 0:
                    result += str(row[0])
                else:
                    result += ", %s" % str(row[0])
        return result

    def get_user_unit_ids(self, user_id, client_id=None):
        columns = "unit_id"
        table = self.tblUnits
        result = None
        condition = 1
        if user_id > 0:
            table = self.tblUserUnits
            condition = " user_id = '%d'" % user_id
        rows = self.get_data(
            table, columns, condition
        )
        if rows :
            result = ""
            for index, row in enumerate(rows):
                if index == 0:
                    result += str(row[0])
                else:
                    result += ",%s" % str(row[0])
        return result

    def get_user_business_group_ids(self, user_id):
        columns = "group_concat(distinct business_group_id)"
        table = self.tblUnits
        result = None
        condition = 1
        # if user_id > 0 :
        #     table = self.tblUserUnits
        #     condition = " user_id = %s " % user_id
        rows = self.get_data(
            table, columns, condition
        )
        if rows :
            result = rows[0][0]
        return result

    def get_user_legal_entity_ids(self, user_id):
        columns = "group_concat(distinct legal_entity_id)"
        table = self.tblUnits
        result = None
        condition = 1
        # if user_id > 0 :
        #     table = self.tblUserUnits
        #     condition = " user_id = %s " % user_id
        rows = self.get_data(
            table, columns, condition
        )
        if rows :
            result = rows[0][0]
        return result

    def get_user_division_ids(self, user_id):
        columns = "group_concat(distinct division_id)"
        table = self.tblUnits
        result = None
        condition = 1
        # if user_id > 0 :
        #     table = self.tblUserUnits
        #     condition = " user_id = %s " % user_id
        rows = self.get_data(
            table, columns, condition
        )
        if rows :
            result = rows[0][0]
        return result

    def get_client_users(self, client_id=None, unit_ids=None):
        columns = "user_id, employee_name, employee_code, is_active"
        condition = "1"
        if unit_ids is not None:
            condition += " and seating_unit_id in (%s)" % unit_ids
        rows = self.get_data(
            self.tblUsers, columns, condition
        )
        columns = ["user_id", "employee_name", "employee_code", "is_active"]
        result = self.convert_to_dict(rows, columns)
        return self.return_client_users(result)

    def return_client_users(self, users):
        results = []
        for user in users :
            results.append(clientreport.User(
                user["user_id"], user["employee_code"], user["employee_name"]
            ))
        return results

#
#   Service Provider
#

    def generate_new_service_provider_id(self, client_id) :
        return self.get_new_id("service_provider_id",self.tblServiceProviders,  client_id)

    def is_duplicate_service_provider(self, service_provider_id,
        service_provider_name, client_id):
        condition = "service_provider_name ='%s' AND service_provider_id != '%d'" %(
            service_provider_name, service_provider_id)
        return self.is_already_exists(self.tblServiceProviders, condition, client_id)

    def get_service_provider_details_list(self, client_id):
        columns = "service_provider_id, service_provider_name, address, contract_from,"+\
                "contract_to, contact_person, contact_no, is_active"
        rows = self.get_data(
            self.tblServiceProviders, columns, "1 ORDER BY service_provider_name"
        )
        columns = ["service_provider_id", "service_provider_name", "address", "contract_from",
        "contract_to", "contact_person", "contact_no", "is_active"]
        result = self.convert_to_dict(rows, columns)
        return self.return_service_provider_details(result)

    def return_service_provider_details(self, service_providers):
        results = []
        for service_provider in service_providers :
            service_provider_obj = core.ServiceProviderDetails(
                service_provider["service_provider_id"],
                service_provider["service_provider_name"],
                service_provider["address"],
                self.datetime_to_string(service_provider["contract_from"]),
                self.datetime_to_string(service_provider["contract_to"]),
                service_provider["contact_person"],
                service_provider["contact_no"],
                bool(service_provider["is_active"]))
            results.append(service_provider_obj)
        return results

    def get_service_providers(self, client_id=None):
        columns = "service_provider_id, service_provider_name, is_active"
        condition = "1"
        rows = self.get_data(
            self.tblServiceProviders, columns, condition
        )
        columns = ["service_provider_id", "service_provider_name", "is_active"]
        result = self.convert_to_dict(rows, columns)
        return self.return_service_providers(result)

    def return_service_providers(self, service_providers):
        results = []
        for service_provider in service_providers :
            service_provider_obj = core.ServiceProvider(
                service_provider["service_provider_id"],
                service_provider["service_provider_name"],
                bool(service_provider["is_active"]))
            results.append(service_provider_obj)
        return results

    def save_service_provider(self, service_provider_id, service_provider, session_user, client_id):
        current_time_stamp = self.get_date_time()
        contract_from = self.string_to_datetime(service_provider.contract_from)
        contract_to = self.string_to_datetime(service_provider.contract_to)
        columns = ["service_provider_id", "service_provider_name", "address", "contract_from",
                "contract_to", "contact_person", "contact_no", "created_on", "created_by",
                "updated_on", "updated_by"]
        values = [service_provider_id, service_provider.service_provider_name,
                    service_provider.address, contract_from, contract_to,
                    service_provider.contact_person, service_provider.contact_no,
                    current_time_stamp, session_user, current_time_stamp, session_user]
        result = self.insert(self.tblServiceProviders,columns, values, client_id)

        action = "Created Service Provider \"%s\"" % service_provider.service_provider_name
        self.save_activity(session_user, 2, action, client_id)

        return result

    def update_service_provider(self, service_provider, session_user, client_id):
        column = "count(*)"
        condition = "now() between contract_from and contract_to \
        and service_provider_id = '%d'" % service_provider.service_provider_id
        rows = self.get_data(self.tblServiceProviders, column, condition)
        if int(rows[0][0]) > 0:
            contract_status_before_update = True
        else:
            contract_status_before_update = False

        current_time_stamp = self.get_date_time()
        contract_from = self.string_to_datetime(service_provider.contract_from)
        contract_to = self.string_to_datetime(service_provider.contract_to)
        columns_list = [ "service_provider_name", "address", "contract_from", "contract_to",
                    "contact_person", "contact_no", "updated_on", "updated_by"]
        values_list = [service_provider.service_provider_name, service_provider.address,
                contract_from, contract_to, service_provider.contact_person,
                service_provider.contact_no, current_time_stamp, session_user]
        condition = "service_provider_id='%d'" % service_provider.service_provider_id
        result = self.update(self.tblServiceProviders, columns_list, values_list, condition, client_id)

        column = "count(*)"
        condition = "now() between contract_from and contract_to \
        and service_provider_id = '%d'" % service_provider.service_provider_id
        rows = self.get_data(self.tblServiceProviders, column, condition)


        if int(rows[0][0]) > 0:
            contract_status_after_update = True
        else:
            contract_status_after_update = False

        if contract_status_before_update is False and contract_status_after_update is True:
            self.update_service_provider_status(
                service_provider.service_provider_id,  1, session_user, client_id
            )
        elif contract_status_before_update is True and contract_status_after_update is False:
            self.update_service_provider_status(
                service_provider.service_provider_id,  0, session_user, client_id
            )

        action = "Updated Service Provider \"%s\"" % service_provider.service_provider_name
        self.save_activity(session_user, 2, action, client_id)

        return result

    def update_service_provider_status(self, service_provider_id,  is_active, session_user, client_id):
        is_active= 1 if is_active != False else 0
        columns = ["is_active", "updated_on" , "updated_by"]
        values = [is_active, self.get_date_time(), session_user]
        condition = "service_provider_id='%d'" % service_provider_id
        result = self.update(self.tblServiceProviders, columns, values, condition, client_id)

        action_column = "service_provider_name"
        rows = self.get_data(
            self.tblServiceProviders, action_column,
            condition
        )
        service_provider_name = rows[0][0]
        action = None
        if is_active == 1:
            action = "Activated Service Provider \"%s\"" % service_provider_name
        else:
            action = "Deactivated Service Provider \"%s\"" % service_provider_name
        self.save_activity(session_user, 2, action, client_id)

        return result

#
#   Audit Trail
#
    def get_audit_trails(
        self, session_user, client_id, from_count, to_count,
        from_date, to_date, user_id, form_id
    ):
        form_ids = None
        form_column = "group_concat(form_id)"
        form_condition = "form_type_id != 4"
        rows = self.get_data(
            self.tblForms, form_column, form_condition
        )
        form_ids = rows[0][0]
        forms = self.return_forms(client_id, form_ids)

        if not self.is_primary_admin(session_user) and not self.is_admin(session_user):
            unit_ids = self.get_user_unit_ids(session_user)
            query = "SELECT DISTINCT user_id FROM %s where unit_id in (%s)" % (
                self.tblUserUnits, unit_ids
            )
            rows = self.select_all(query)
            user_ids = ""
            for index, row in enumerate(rows):
                if index == 0:
                    user_ids += str(row[0])
                else:
                    user_ids += "%s%s" % (
                        ",", str(row[0])
                    )
            users = self.get_users_by_id(user_ids, client_id)
        else:
            users = self.get_users(client_id)

        from_date = self.string_to_datetime(from_date).date()
        to_date = self.string_to_datetime(to_date).date()
        where_qry = "1"
        if from_date is not None and to_date is not None:
            where_qry += " AND  date(created_on) between '%s' AND '%s' " % (
                from_date, to_date

            )

        if user_id is not None:
            where_qry += " AND user_id = '%s'" % (user_id)
        if form_id is not None:
            where_qry += " AND form_id = '%s'" % (form_id)

        columns = "user_id, form_id, action, created_on"
        where_qry += ''' AND action not like "%sLog In by%s"
        ORDER BY activity_log_id DESC limit %s, %s ''' % (
            "%", "%", from_count, to_count
        )
        rows = self.get_data(
            self.tblActivityLog, columns, where_qry
        )
        audit_trail_details = []
        for row in rows:
            user_id = row[0]
            form_id = row[1]
            action = row[2]
            date = self.datetime_to_string_time(row[3])
            audit_trail_details.append(
                general.AuditTrail(user_id, form_id, action, date)
            )
        return general.GetAuditTrailSuccess(audit_trail_details, users, forms)

#
# Statutory settings
#

    def get_statutory_settings(self, session_user, client_id):
        admin_id = self.get_admin_id()
        if session_user == 0 or session_user == admin_id:
            where_qry = ''
        else :
            user_id = int(session_user)
            where_qry = " WHERE t2.is_closed=0 AND t1.unit_id in (select unit_id from tbl_user_units where user_id LIKE '%s') \
            AND t1.domain_id in (select domain_id from tbl_user_domains where user_id LIKE '%s')" % (
                user_id, user_id
            )
        query = "SELECT distinct  \
            t1.country_id, t1.domain_id, t1.unit_id,t2.unit_name, \
            (select business_group_name from tbl_business_groups \
                where business_group_id = t2.business_group_id)business_group_name, \
            (select legal_entity_name from tbl_legal_entities \
                where legal_entity_id = t2.legal_entity_id)legal_entity_name,\
            (select division_name from tbl_divisions \
                where division_id = t2.division_id)division_name, \
            t2.address, t2.postal_code, t2.unit_code, \
            (select country_name from tbl_countries where country_id = t1.country_id )country_name, \
            (select domain_name from tbl_domains where domain_id = t1.domain_id)domain_name, \
            t2.is_closed,  \
            (select is_new from tbl_client_statutories where unit_id = t1.unit_id order by is_new limit 1)\
            FROM tbl_client_statutories t1 \
            INNER JOIN tbl_units t2 \
            ON t1.unit_id = t2.unit_id %s \
            ORDER BY t1.unit_id " % (where_qry)
        rows = self.select_all(query)

        columns = [
            "country_id", "domain_id", "unit_id", "unit_name",
            "business_group_name", "legal_entity_name",
            "division_name", "address", "postal_code", "unit_code",
            "country_name", 'domain_name', 'is_closed', 'is_new'
        ]
        result = self.convert_to_dict(rows, columns)
        return self.return_statutory_settings(result, client_id)

    def return_compliance_for_statutory_settings(
        self, unit_id,  from_count, to_count
    ):
        query = "SELECT t1.client_compliance_id, t1.client_statutory_id, t1.compliance_id, \
            t1.statutory_applicable, t1.statutory_opted,\
            t1.not_applicable_remarks, \
            t1.compliance_applicable, t1.compliance_opted, \
            t1.compliance_remarks, \
            t2.compliance_task, t2.document_name, t2.statutory_mapping,\
            t2.statutory_provision, t2.compliance_description, \
            (select is_new from tbl_client_statutories where client_statutory_id = t1.client_statutory_id), \
            (select domain_name from tbl_domains where domain_id = t2.domain_id), \
            (select count(tc1.client_compliance_id) from tbl_client_compliances tc1 \
            inner join tbl_client_statutories ts2 \
            ON ts2.client_statutory_id = tc1.client_statutory_id \
            AND ts2.unit_id = %s \
            ) total\
            FROM tbl_client_compliances t1 \
            INNER JOIN tbl_compliances t2 \
            ON t2.compliance_id = t1.compliance_id \
            WHERE \
            t1.client_statutory_id in (select distinct client_statutory_id from \
            tbl_client_statutories where unit_id = %s)\
            ORDER BY t2.domain_id, t2.statutory_mapping \
            limit %s, %s\
            " % (
                unit_id,
                unit_id,
                from_count,
                to_count
            )
        rows = self.select_all(query)
        columns = [
            "client_compliance_id", "client_statutory_id", "compliance_id",
            "statutory_applicable", "statutory_opted",
            "not_applicable_remarks", "compliance_applicable",
            "compliance_opted", "compliance_remarks",
            "compliance_task", "document_name", "statutory_mapping",
            "statutory_provision", "compliance_description",
            "is_new", "domain", "total"
        ]
        results = self.convert_to_dict(rows, columns)
        statutory_wise_compliances = []
        total = 0
        for r in results :
            total = r["total"]
            statutory_opted = r["statutory_opted"]
            if statutory_opted is None :
                statutory_opted = bool(r["statutory_applicable"])
            else :
                statutory_opted = bool(statutory_opted)

            compliance_opted = r["compliance_opted"]
            if type(compliance_opted) is int :
                compliance_opted = bool(compliance_opted)
            else :
                compliance_opted = bool(r["compliance_applicable"])

            compliance_remarks = r["compliance_remarks"]
            if compliance_remarks == "" :
                compliance_remarks = None
            if r["document_name"] == "" :
                r["document_name"] = None

            mappings = r["statutory_mapping"].split('>>')
            statutory_name = mappings[0].strip()
            statutory_name = statutory_name.strip()
            if len(mappings) > 1 :
                provision = "%s - %s" % (
                    ','.join(mappings[1:]),
                    r["statutory_provision"]
                )
            else :
                provision = r["statutory_provision"]

            if r["document_name"] not in [None, "None"] :
                name = "%s - %s" % (
                    r["document_name"], r["compliance_task"]
                )

            else :
                name = r["compliance_task"]

            compliance = clienttransactions.ComplianceApplicability(
                statutory_name,
                bool(r["statutory_applicable"]),
                statutory_opted,
                r["not_applicable_remarks"],
                r["client_statutory_id"],
                r["client_compliance_id"],
                r["compliance_id"],
                name,
                r["compliance_description"],
                provision,
                bool(r["compliance_applicable"]),
                bool(compliance_opted),
                compliance_remarks,
                not bool(r["is_new"]),
                r["domain"]
            )

            statutory_wise_compliances.append(compliance)
        return statutory_wise_compliances, total

    def return_statutory_settings(self, data, client_id):
        unit_wise_statutories = {}
        for d in data :
            domain_name = d["domain_name"]
            unit_id = d["unit_id"]
            unit_name = "%s - %s" % (d["unit_code"], d["unit_name"])
            address = "%s, %s" % (
                d["address"],
                d["postal_code"]
            )

            unit_statutories = unit_wise_statutories.get(unit_id)
            if unit_statutories is None :
                # statutory_dict = {}
                # statutory_dict[domain_name] = statutory_val
                unit_statutories = clienttransactions.UnitStatutoryCompliances(
                    unit_id,
                    unit_name,
                    address,
                    d["country_name"],
                    [domain_name],
                    d["business_group_name"],
                    d["legal_entity_name"],
                    d["division_name"],
                    bool(d["is_closed"]),
                    not bool(d["is_new"])
                )
            else :
                domain_list = unit_statutories.domain_names
                domain_list.append(domain_name)
                domain_list = list(set(domain_list))
                unit_statutories.domain_names = domain_list
                # unit_statutories.statutories = statutory_dict
            unit_wise_statutories[unit_id] = unit_statutories
        lst = []
        for k in sorted(unit_wise_statutories):
            lst.append(unit_wise_statutories.get(k))

        return clienttransactions.GetStatutorySettingsSuccess(
            lst
        )

    def execute_bulk_insert(self, value_list) :
        table = "tbl_client_compliances"
        column = [
            "client_compliance_id", "client_statutory_id",
            "compliance_id",
            "statutory_opted", "not_applicable_remarks",
            "compliance_opted", "compliance_remarks",
            "updated_by", "updated_on"
        ]
        update_column = [
            "client_statutory_id", "compliance_id",
            "statutory_opted", "not_applicable_remarks",
            "compliance_opted", "compliance_remarks",
            "updated_by", "updated_on"
        ]

        self.on_duplicate_key_update(table, ",".join(column), value_list, update_column)

    def update_new_statutory_settings(self, unit_id):
        q = "Update tbl_client_statutories set is_new=1 where unit_id = %s" % (
             unit_id,
        )
        self.execute(q)

    def update_statutory_settings(self, data, session_user, client_id):
        unit_id = data.unit_id
        unit_name = data.unit_name
        statutories = data.statutories
        updated_on = self.get_date_time()
        value_list = []
        for s in statutories :
            client_compliance_id = s.client_compliance_id
            client_statutory_id = s.client_statutory_id
            statutory_opted_status = int(s.applicable_status)
            not_applicable_remarks = s.not_applicable_remarks
            if not_applicable_remarks is None :
                not_applicable_remarks = ""
            compliance_id = s.compliance_id
            opted_status = int(s.compliance_opted_status)
            remarks = s.compliance_remarks
            if remarks is None :
                remarks = ""
            value = (
                client_compliance_id, client_statutory_id, compliance_id,
                statutory_opted_status, not_applicable_remarks,
                opted_status, remarks,
                int(session_user), str(updated_on)
            )
            value_list.append(value)

        self.execute_bulk_insert(value_list)
        self.update_new_statutory_settings(unit_id)
        action = "Statutory settings updated for unit - %s " % (unit_name)
        self.save_activity(session_user, 6, action)
        self.update_opted_status_in_knowledge(data)

        return clienttransactions.UpdateStatutorySettingsSuccess()

    def update_opted_status_in_knowledge(self, data):
        try :
            db_con = Database(
                KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
                KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
            )
            db_con.connect()
            db_con.begin()
            statutories = data.statutories
            for s in statutories :
                client_statutory_id = s.client_statutory_id
                statutory_opted_status = int(s.applicable_status)
                not_applicable_remarks = s.not_applicable_remarks
                if not_applicable_remarks is None :
                    not_applicable_remarks = ""
                compliance_id = s.compliance_id
                opted_status = int(s.compliance_opted_status)
                remarks = s.compliance_remarks
                if remarks is None :
                    remarks = ""
                q = "UPDATE tbl_client_compliances SET \
                    statutory_opted = %s, \
                    not_applicable_remarks = '%s', \
                    compliance_opted = %s, \
                    compliance_remarks = '%s' \
                    WHERE client_statutory_id = %s AND \
                    compliance_id = %s" % (
                        statutory_opted_status,
                        not_applicable_remarks,
                        opted_status,
                        remarks,
                        client_statutory_id,
                        compliance_id
                    )
                db_con.execute(q)
            db_con.commit()
            db_con.close()
        except Exception, e :
            logger.logClient("error", "clientdatabase.py-update_opted_status_in_knowledge", e)
            print e
            db_con.rollback()

    def is_admin(self, user_id):
        if user_id == 0:
            return True
        else:
            columns = "count(*)"
            condition = "(is_admin = 1 or is_primary_admin = 1) and user_id = '%d'" % user_id
            rows = self.get_data(self.tblUsers, columns, condition)
            if rows[0][0] > 0:
                return True
            else:
                return False

    def get_level_1_statutories_for_user_with_domain(self, session_user, client_id, domain_id=None):
        columns = "group_concat(distinct compliance_id)"
        condition = "1"
        if not self.is_admin(session_user):
            condition = "assignee = '%d'" % session_user
        rows = self.get_data(self.tblAssignedCompliances, columns, condition)
        compliance_ids = None
        if rows:
            compliance_ids = rows[0][0]


        domain_ids = domain_id
        if domain_ids is None :
            columns = "group_concat(domain_id)"
            domain_rows = None
            if session_user != 0:
                domain_rows = self.get_data(
                    self.tblUserDomains, columns,
                    "user_id='%d'" % session_user
                )
            else:
                domain_rows = self.get_data(
                    self.tblDomains, columns,
                    "1"
                )
            domain_ids = domain_rows[0][0]
        level_1_statutory = {}
        for domain_id in domain_ids.split(","):
            condition = "domain_id in (%s)" % (domain_id)
            if compliance_ids is not None:
                condition += "AND compliance_id in (%s)" % (compliance_ids)
            mapping_rows = self.get_data(
                self.tblCompliances,
                "statutory_mapping",
                condition
            )
            level_1_statutory[domain_id] = []
            for mapping in mapping_rows:
                statutories = mapping[0].split(">>")
                if statutories[0].strip() not in level_1_statutory[domain_id]:
                    level_1_statutory[domain_id].append(statutories[0].strip())
        return level_1_statutory

    def get_compliance_frequency(self, client_id, condition="1"):
        columns = "frequency_id, frequency"
        rows = self.get_data(
            self.tblComplianceFrequency, columns, condition
        )
        compliance_frequency = []
        for row in rows:
            compliance_frequency.append(
                core.ComplianceFrequency(
                    row[0],
                    core.COMPLIANCE_FREQUENCY(row[1])
                    )
                )
        return compliance_frequency

    def get_user_ids_by_unit_and_domain(
            self, unit_id, domain_id
        ):
        unit_user_rows = self.get_data(
            self.tblUserUnits, "user_id" , "unit_id = '%d'" % unit_id
        )
        unit_users = []
        for unit_user in unit_user_rows:
            unit_users.append(unit_user[0])

        domain_user_rows = self.get_data(
            self.tblUserDomains, "user_id" , "domain_id = '%d'" % domain_id
        )
        domain_users = []
        for domain_user in domain_user_rows:
            domain_users.append(domain_user[0])

        users = list(set(unit_users).intersection(domain_users))
        user_ids = None
        if len(users) > 0:
            user_ids = ",".join(str(x) for x in users)
        else:
            user_ids = None
        return user_ids


    def get_users_by_unit_and_domain(
            self, unit_id, domain_id
        ):
        user_ids = self.get_user_ids_by_unit_and_domain(
            unit_id, domain_id
        )
        result = []
        if user_ids is not None:
            columns = "user_id, employee_name, employee_code, is_active"
            condition = " is_active = 1 and user_id in (%s)" % user_ids
            rows = self.get_data(
                self.tblUsers, columns, condition
            )
            columns = ["user_id", "employee_name", "employee_code", "is_active"]
            result = self.convert_to_dict(rows, columns)
        return self.return_users(result)

    def get_statutory_wise_compliances(
        self, unit_id, domain_id, level_1_statutory_name, frequency_name,
        country_id, session_user, start_count, to_count
    ):
        condition = "1 "
        if frequency_name is not None:
            condition += "AND c.frequency_id = (SELECT frequency_id FROM %s WHERE \
            frequency = '%s')" % (
                self.tblComplianceFrequency, frequency_name
            )
        else:
            condition += "AND c.frequency_id in (2,3)"
        if level_1_statutory_name is not None:
            condition += " AND statutory_mapping like '%s%s'" % (
                level_1_statutory_name, "%"
            )

        query = "SELECT ac.compliance_id, ac.statutory_dates, ac.due_date,\
            assignee, employee_code, employee_name, statutory_mapping,\
            document_name, compliance_task, compliance_description,\
            c.repeats_type_id, repeat_type, repeats_every, frequency,\
            c.frequency_id FROM %s ac \
            INNER JOIN %s u ON (ac.assignee = u.user_id) \
            INNER JOIN %s c ON (ac.compliance_id = c.compliance_id) \
            INNER JOIN %s f ON (c.frequency_id = f.frequency_id) \
            INNER JOIN %s rt ON (c.repeats_type_id = rt.repeat_type_id) \
            WHERE ac.is_active = 1 \
            AND c.domain_id = '%d' AND ac.unit_id = %d \
            AND %s " % (
                self.tblAssignedCompliances, self.tblUsers,
                self.tblCompliances, self.tblComplianceFrequency,
                self.tblComplianceRepeatType,
                domain_id, unit_id, condition
            )
        rows = self.select_all(query)
        columns = [
            "compliance_id", "statutory_dates", "due_date", "assignee",
            "employee_code", "employee_name", "statutory_mapping",
            "document_name", "compliance_task", "compliance_description",
            "repeats_type_id",  "repeat_type", "repeat_every", "frequency",
            "frequency_id"
        ]
        client_compliance_rows = self.convert_to_dict(rows, columns)
        level_1_statutory_wise_compliances = {}
        total_count = 0
        compliance_count = 0
        for compliance in client_compliance_rows:
            statutories = compliance["statutory_mapping"].split(">>")
            if level_1_statutory_name is None:

                level_1 = statutories[0]
            else:
                level_1 = level_1_statutory_name
            if level_1 not in level_1_statutory_wise_compliances:
                level_1_statutory_wise_compliances[level_1] = []
            compliance_name = compliance["compliance_task"]
            if compliance["document_name"] not in (None, "None", ""):
                compliance_name = "%s - %s" % (
                    compliance["document_name"], compliance_name
                )
            employee_code = compliance["employee_code"]
            if employee_code is None:
                employee_code = "Administrator"
            assingee_name = "%s - %s" % (
                employee_code, compliance["employee_name"]
            )
            due_dates = []
            # statutory_dates_list = []
            summary = ""
            if compliance["repeats_type_id"] == 1:  # Days
                due_dates, summary = self.calculate_due_date(
                    repeat_by=1,
                    repeat_every=compliance["repeat_every"],
                    due_date=compliance["due_date"],
                    domain_id=domain_id,
                    country_id=country_id
                )
            elif compliance["repeats_type_id"] == 2:  # Months
                due_dates, summary = self.calculate_due_date(
                    statutory_dates=compliance["statutory_dates"],
                    repeat_by=2,
                    repeat_every=compliance["repeat_every"],
                    due_date=compliance["due_date"],
                    domain_id=domain_id,
                    country_id=country_id
                )
            elif compliance["repeats_type_id"] == 3:  # years
                due_dates, summary = self.calculate_due_date(
                    repeat_by=3,
                    statutory_dates=compliance["statutory_dates"],
                    repeat_every=compliance["repeat_every"],
                    due_date=compliance["due_date"],
                    domain_id=domain_id,
                    country_id=country_id
                )
            final_due_dates = self.filter_out_due_dates(
                unit_id, compliance["compliance_id"], due_dates
            )
            total_count += len(final_due_dates)
            for due_date in final_due_dates:
                if int(start_count) <= compliance_count and compliance_count < (int(start_count)+to_count):
                    due_date_parts = due_date.replace("'","").split("-")
                    year = due_date_parts[0]
                    month = due_date_parts[1]
                    day = due_date_parts[2]
                    due_date = datetime.date(int(year), int(month), int(day))
                    level_1_statutory_wise_compliances[
                        statutories[0].strip()
                    ].append(
                        clienttransactions.UNIT_WISE_STATUTORIES_FOR_PAST_RECORDS(
                            compliance["compliance_id"], compliance_name,
                            compliance["compliance_description"],
                            core.COMPLIANCE_FREQUENCY(compliance["frequency"]),
                            summary, self.datetime_to_string(due_date),
                            assingee_name, compliance["assignee"]
                        )
                    )
                    compliance_count += 1
                elif compliance_count > (int(start_count)+to_count):
                    break
                else:
                    compliance_count += 1
                    continue

        statutory_wise_compliances = []
        for level_1_statutory_name, compliances in level_1_statutory_wise_compliances.iteritems():
            if len(compliances) > 0:
                statutory_wise_compliances.append(
                    clienttransactions.STATUTORY_WISE_COMPLIANCES(
                        level_1_statutory_name, compliances
                    )
                )
        return statutory_wise_compliances, total_count

    def filter_out_due_dates(self, unit_id, compliance_id, due_dates_list):
        # Checking same due date already exists
        if due_dates_list is not None and len(due_dates_list) > 0:
            formated_date_list = []
            for x in due_dates_list:
                x = str(x)
                x.replace(" ", "")
                formated_date_list.append('%s%s%s' % ("'", x, "'"))
            due_dates = ",".join(str(x) for x in formated_date_list)
            query = '''
                SELECT is_ok FROM
                (SELECT (CASE WHEN (unit_id = '{}' AND DATE(due_date) IN ({}) AND \
                compliance_id = '{}') THEN DATE(due_date) ELSE 'NotExists' END ) as
                is_ok FROM {} ) a WHERE is_ok != "NotExists"'''.format(
                unit_id, due_dates, compliance_id, self.tblComplianceHistory
            )
            rows = self.select_all(query)
            if len(rows) > 0:
                for row in rows:
                    formated_date_list.remove("%s%s%s" % ("'", row[0], "'"))
            result_due_date = []
            for current_due_date_index, due_date in enumerate(formated_date_list):
                next_due_date = None
                if len(due_dates_list)-1 < current_due_date_index+1:
                    continue
                else:
                    next_due_date = due_dates_list[current_due_date_index+1]
                    columns = "count(*)"
                    condition = "unit_id = '{}' AND due_date < {} AND compliance_id = '{}' AND \
                    approve_status = 1 and validity_date > {} and validity_date > '{}'".format(
                        unit_id, due_date, compliance_id, due_date, next_due_date
                    )
                    rows = self.get_data(self.tblComplianceHistory, columns, condition)
                    if rows[0][0] > 0:
                        continue
                    else:
                        result_due_date.append(due_date)
            return result_due_date
        else:
            return []

    def is_already_completed_compliance(
        self, due_date, compliance_id, unit_id, due_dates_list=None
    ):
        # Checking same due date already exists
        columns = "count(*)"
        condition = "unit_id = '{}' and due_date = '{}' and compliance_id = '{}'".format(
            unit_id, due_date, compliance_id
        )
        rows = self.get_data(self.tblComplianceHistory, columns, condition)
        is_compliance_with_same_due_date_exists = True if rows[0][0] > 0 else False
        if is_compliance_with_same_due_date_exists:
            return is_compliance_with_same_due_date_exists
        else:
            # Checking validity of previous compliance exceeds the current compliance
            if due_dates_list is not None:
                next_due_date = None
                current_due_date_index = due_dates_list.index(due_date)
                if len(due_dates_list)-1 < current_due_date_index+1:
                    return False
                else:
                    next_due_date = due_dates_list[current_due_date_index+1]
                    columns = "count(*)"
                    condition = "unit_id = '{}' AND due_date < '{}' AND compliance_id = '{}' AND \
                    approve_status = 1 and validity_date > '{}' and validity_date > '{}'".format(
                        unit_id, due_date, compliance_id, due_date, next_due_date
                    )
                    rows = self.get_data(self.tblComplianceHistory, columns, condition)
                    if rows[0][0] > 0:
                        return True
                    else:
                        return False

    def calculate_from_and_to_date_for_domain(self, country_id, domain_id):
        columns = "contract_from, contract_to"
        rows = self.get_data(self.tblClientGroups, columns, "1")
        contract_from = rows[0][0]
        contract_to = rows[0][1]

        columns = "period_from, period_to"
        condition = "country_id = '%d' and domain_id = '%d'" % (
            country_id, domain_id
        )
        rows = self.get_data(self.tblClientConfigurations, columns, condition)
        period_from = rows[0][0]
        period_to = rows[0][1]

        to_date = contract_from
        current_year = to_date.year
        previous_year = current_year-1
        from_date = datetime.date(previous_year, period_from, 1)
        r = relativedelta.relativedelta(to_date, from_date)
        no_of_years = r.years
        no_of_months = r.months
        if no_of_years is not 0 or no_of_months >= 12:
            from_date = datetime.date(current_year, period_from, 1)
        return from_date, to_date

    def calculate_due_date(
        self, country_id, domain_id, statutory_dates=None, repeat_by=None,
        repeat_every=None, due_date=None
    ):
        def is_future_date(test_date):
            result = False
            current_date = datetime.date.today()
            if type(test_date) == datetime.datetime:
                test_date = test_date.date()
            if ((current_date - test_date).days < 0):
                result = True
            return result
        from_date, to_date = self.calculate_from_and_to_date_for_domain(country_id, domain_id)
        due_dates = []
        summary = ""
        # For Monthly Recurring compliances
        if statutory_dates and len(json.loads(statutory_dates)) > 1:
            summary += "Every {} month(s) (".format(repeat_every)
            for statutory_date in json.loads(statutory_dates):
                date = statutory_date["statutory_date"]
                month = statutory_date["statutory_month"]
                summary += "{} {} ".format(self.string_months[month], date)
                current_date = datetime.datetime.today().date()
                due_date_guess = datetime.date(current_date.year, month, date)
                real_due_date = None
                if is_future_date(due_date_guess):
                    real_due_date = datetime.date(current_date.year - 1, month, date)
                else:
                    real_due_date = due_date_guess
                if from_date <= real_due_date <= to_date:
                    due_dates.append(
                        real_due_date
                    )
                else:
                    continue
            summary += ")"
        elif repeat_by:
            date_details = ""
            if statutory_dates not in  ["None", None, ""]:
                statutory_date_json = json.loads(statutory_dates)
                if len(statutory_date_json) > 0:
                    date_details += "({})".format(statutory_date_json[0]["statutory_date"])
            # For Compliances Recurring in days
            if repeat_by == 1: # Days
                summary = "Every {} day(s)".format(repeat_every)
                previous_year_due_date = datetime.date(
                    due_date.year - 1, due_date.month, due_date.day
                )
                if from_date <= previous_year_due_date <= to_date:
                    due_dates.append(previous_year_due_date)
                iter_due_date = previous_year_due_date
                while not is_future_date(iter_due_date):
                    iter_due_date = iter_due_date + datetime.timedelta(days=repeat_every)
                    if from_date <= iter_due_date <= to_date:
                        due_dates.append(iter_due_date)
            elif repeat_by == 2: # Months
                summary = "Every {} month(s) {}".format(repeat_every, date_details)
                iter_due_date = due_date
                while iter_due_date > from_date:
                    iter_due_date = iter_due_date + relativedelta.relativedelta(months=-repeat_every)
                    if from_date <= iter_due_date <= to_date:
                        due_dates.append(iter_due_date)
            elif repeat_by == 3: # Years
                summary = "Every {} year(s) {}".format(repeat_every, date_details)
                year = from_date.year
                while year <= to_date.year:
                    due_date = datetime.date(
                        year, due_date.month, due_date.day
                    )
                    if from_date <= due_date  <= to_date:
                        due_dates.append (due_date)
                    year += 1
        if len(due_dates) > 2:
            if due_dates[0] > due_dates[1]:
                due_dates.reverse()
        return due_dates, summary

    def convert_base64_to_file(self, file_name, file_content, client_id):
        client_directory = "%s/%d" % (CLIENT_DOCS_BASE_PATH, client_id)
        file_path = "%s/%s" % (client_directory, file_name)
        if not os.path.exists(client_directory):
            os.makedirs(client_directory)
        self.remove_uploaded_file(file_path)
        if file_content is not None :
            new_file = open(file_path, "wb")
            new_file.write(file_content.decode('base64'))
            new_file.close()

    def remove_uploaded_file(self, file_path):
        if os.path.exists(file_path) :
            os.remove(file_path)

    def is_space_available(self, upload_size):
        columns = "total_disk_space - total_disk_space_used"
        rows = self.get_data(self.tblClientGroups, columns, "1")
        remaining_space = rows[0][0]
        if upload_size < remaining_space:
            return True
        else:
            return False

    def update_used_space(self, file_size):
        columns = "total_disk_space_used"
        condition = "1"
        self.increment( self.tblClientGroups, columns, condition, value = file_size)

        total_used_space = 0

        rows = self.get_data(self.tblClientGroups, "total_disk_space_used, client_id", "1")
        client_id = rows[0][1]
        if rows[0][0] is not None:
            total_used_space = int(rows[0][0])

        db_con = Database(
            KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
            KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
        )
        db_con.connect()
        db_con.begin()
        q = "UPDATE tbl_client_groups set total_disk_space_used = '%d' where client_id = '%d'" % (
            total_used_space, client_id
        )
        db_con.execute(q)
        db_con.commit()
        db_con.close()

    def validate_before_save(
        self, unit_id, compliance_id, due_date, completion_date, documents,
        validity_date, completed_by, client_id
    ):
        # Checking whether compliance already completed
        if self.is_already_completed_compliance(
            self.string_to_datetime(due_date), compliance_id, unit_id
        ):
            return False
        else:
            return True

    def save_past_record(
            self, unit_id, compliance_id, due_date, completion_date, documents,
            validity_date, completed_by, client_id
        ):
        is_uploading_file = False

        # Checking whether compliance already completed
        if self.is_already_completed_compliance(
            self.string_to_datetime(due_date), compliance_id, unit_id
        ):
            return False

        # Hanling upload
        document_names = []
        file_size = 0
        if len(documents) > 0:
            for doc in documents:
                file_size += doc.file_size

            if self.is_space_available(file_size):
                is_uploading_file = True
                for doc in documents:
                    file_name_parts = doc.file_name.split('.')
                    name = None
                    exten = None
                    for index, file_name_part in enumerate(file_name_parts):
                        if index == len(file_name_parts) - 1:
                            exten = file_name_part
                        else:
                            if name is None:
                                name = file_name_part
                            else:
                                name += file_name_part
                    auto_code = self.new_uuid()
                    file_name = "%s-%s.%s" % (name, auto_code, exten)
                    document_names.append(file_name)
                    self.convert_base64_to_file(file_name, doc.file_content, client_id)
                self.update_used_space(file_size)
            else:
                return clienttransactions.NotEnoughSpaceAvailable()

        # Checking Settings for two levels of approval
        is_two_level = self.is_two_levels_of_approval()
        compliance_history_id = self.get_new_id("compliance_history_id", self.tblComplianceHistory)
        completion_date = self.string_to_datetime(completion_date).date()
        next_due_date = None
        if validity_date:
            next_due_date = self.string_to_datetime(validity_date).date()

        # Getting Approval and Concurrence Persons
        concur_approve_columns = "approval_person"
        if is_two_level:
            concur_approve_columns += ", concurrence_person"
        condition = "compliance_id = '%d' and unit_id = '%d'" % (
            compliance_id, unit_id
        )
        rows = self.get_data(
            self.tblAssignedCompliances, concur_approve_columns, condition
        )
        concurred_by = 0
        approved_by = 0
        if rows:
            approved_by = rows[0][0]
            if is_two_level:
                concurred_by = rows[0][1]
        if validity_date is not None:
            validity_date = self.string_to_datetime(validity_date).date()
        columns = [
            "compliance_history_id", "unit_id", "compliance_id", "due_date", "completion_date",
            "validity_date", "next_due_date", "completed_by", "completed_on",
            "approve_status", "approved_by", "approved_on"
        ]
        values = [
            compliance_history_id, unit_id, compliance_id, self.string_to_datetime(due_date).date(),
            completion_date, validity_date,
            next_due_date, completed_by, completion_date, 1, approved_by, completion_date
        ]
        if is_two_level:
            columns.append("concurrence_status")
            columns.append("concurred_by")
            columns.append("concurred_on")
            values.append(1)
            values.append(concurred_by)
            values.append(completion_date)

        if is_uploading_file:
            columns.append("documents")
            columns.append("document_size")
            values.append(",".join(document_names))
            values.append(file_size)

        self.insert(
            self.tblComplianceHistory, columns, values
        )
        return True

    def is_two_levels_of_approval(self):
        columns = "two_levels_of_approval"
        rows = self.get_data(self.tblClientGroups, columns, "1")
        return rows[0][0]

#
#   Compliance Approval
#

    def get_compliance_approval_count(self, session_user):
        columns = "count(*)"
        condition = "1"
        concur_count = 0
        if (self.is_two_levels_of_approval()):
            condition = " concurrence_status is not NULL AND \
            concurrence_status != 0 AND concurrence_status != '' AND \
            concurred_by is not NULL"
            concur_condition = "concurred_by = '%d' AND (approve_status is NULL OR \
                approve_status = 0 OR approve_status = '') AND (\
                completed_on is not NULL AND completed_on !=0) AND \
                (concurrence_status = 0 OR concurrence_status is NULL OR \
                concurrence_status = '')" % (
                    session_user
                )
            concur_count = self.get_data(
                self.tblComplianceHistory, columns, concur_condition
            )[0][0]
        approve_condition = "approved_by = '%d' AND (approve_status is NULL OR \
        approve_status = 0 or approve_status = '') AND ( \
        completed_on is not NULL and completed_on !=0) AND ( %s \
        )" % (
            session_user, condition
        )

        approve_count = self.get_data(
            self.tblComplianceHistory, columns, approve_condition
        )[0][0]
        return concur_count + approve_count

    def get_compliance_approval_list(
        self, start_count, to_count, session_user, client_id
    ):
        approval_user_ids = str(session_user)
        if self.is_primary_admin(session_user):
            approval_user_ids += ",0"

        if self.is_two_levels_of_approval():
            concurrence_condition = "IF ( (concurred_by = '%s' AND concurrence_status = 1), 0, 1)" % (session_user)
        else:
            concurrence_condition = "1"
        query = "SELECT * FROM \
        (SELECT compliance_history_id, tch.compliance_id, start_date,\
        tch.due_date as due_date, documents, completion_date, completed_on, next_due_date, \
        concurred_by, remarks, datediff(tch.due_date, completion_date ), \
        compliance_task, compliance_description, tc.frequency_id, \
        (SELECT frequency FROM %s tcf WHERE tcf.frequency_id = tc.frequency_id ), \
        document_name, concurrence_status, (select statutory_dates from \
        tbl_assigned_compliances tac where tac.compliance_id = tch.compliance_id \
        limit 1), tch.validity_date, approved_by, \
        (SELECT concat(unit_code, '-', tu.unit_name) FROM %s tu \
        where tch.unit_id = tu.unit_id), \
        completed_by, \
        (SELECT concat(IFNULL(employee_code, ''),'-',employee_name) FROM %s tu\
        WHERE tu.user_id = tch.completed_by), \
        (SELECT domain_name from %s td WHERE td.domain_id = tc.domain_id )\
        FROM %s tch \
        INNER JOIN %s tc ON (tch.compliance_id = tc.compliance_id) \
        WHERE IFNULL(completion_date, 0) != 0  \
        AND IFNULL(completed_on, 0) != 0  \
        AND IFNULL(approve_status, 0) = 0 \
        AND (approved_by IN (%s) OR concurred_by = '%s') \
        AND %s\
        LIMIT %s, %s) a \
        ORDER BY completed_by, due_date ASC" % (
            self.tblComplianceFrequency, self.tblUnits, self.tblUsers, self.tblDomains,
            self.tblComplianceHistory, self.tblCompliances, approval_user_ids,
            session_user, concurrence_condition, start_count, to_count
        )
        rows = self.select_all(query)
        is_two_levels = self.is_two_levels_of_approval()
        assignee_wise_compliances = {}
        assignee_id_name_map = {}
        count = 0
        for row in rows:
            download_urls = []
            file_name = []
            if row[4] is not None and len(row[4]) > 0:
                for document in row[4].split(","):
                    if document is not None and document.strip(',') != '':
                        dl_url = "%s/%s/%s" % (CLIENT_DOCS_DOWNLOAD_URL, str(client_id), document)
                        download_urls.append(dl_url)
                        file_name_part = document.split("-")[0]
                        file_extn_parts = document.split(".")
                        file_extn_part = None
                        if len(file_extn_parts) > 1:
                            file_extn_part = file_extn_parts[len(file_extn_parts)-1]
                        if file_extn_part is not None:
                            name = "%s.%s" % (
                                file_name_part, file_extn_part
                            )
                            file_name.append(name)
                        else:
                            file_name.append(file_name_part)
            concurred_by_id = None if row[8] is None else int(row[8])
            compliance_history_id = row[0]
            start_date = self.datetime_to_string(row[2])
            due_date = self.datetime_to_string(row[3])
            documents = download_urls if len(download_urls) > 0 else None
            file_names = file_name if len(file_name) > 0 else None
            completion_date = None if row[5] is None else self.datetime_to_string(row[5])
            completed_on = None if row[6] is None else self.datetime_to_string(row[6])
            next_due_date = None if row[7] is None else self.datetime_to_string(row[7])
            concurred_by = None if concurred_by_id is None else self.get_user_name_by_id(concurred_by_id, client_id)
            remarks = row[9]
            delayed_by = None if row[10] < 0 else row[10]
            compliance_name = row[11]
            if row[15] not in (None, "None", "") :
                compliance_name = "%s - %s" % (row[15], row[11])
            frequency = core.COMPLIANCE_FREQUENCY(row[14])
            description = row[12]
            concurrence_status = None if row[16] in [None, "None", ""] else bool(int(row[16]))
            statutory_dates = [] if row[17] is [None, "None", ""] else json.loads(row[17])
            validity_date = None if row[18] is [None, "None", ""] else self.datetime_to_string(row[18])
            unit_name = row[20]
            date_list = []
            for date in statutory_dates :
                s_date = core.StatutoryDate(
                    date["statutory_date"],
                    date["statutory_month"],
                    date["trigger_before_days"],
                    date.get("repeat_by")
                )
                date_list.append(s_date)

            domain_name = row[23]
            action = None
            if is_two_levels:
                if concurred_by_id == session_user:
                    action = "Concur"
                elif concurrence_status is True and session_user in [int(x) for x in approval_user_ids.split(",")]:
                    action = "Approve"
                elif concurred_by_id is None and session_user in [int(x) for x in approval_user_ids.split(",")]:
                    action = "Approve"
                else:
                    continue
            elif concurred_by_id != session_user and session_user in [int(x) for x in approval_user_ids.split(",")]:
                action = "Approve"
            else:
                continue
            assignee = row[22]

            if assignee not in assignee_id_name_map:
                assignee_id_name_map[assignee] = row[21]
            if assignee not in assignee_wise_compliances:
                assignee_wise_compliances[assignee] = []
            count += 1
            assignee_wise_compliances[assignee].append(
                clienttransactions.APPROVALCOMPLIANCE(
                    compliance_history_id, compliance_name, description, domain_name,
                    start_date, due_date, delayed_by, frequency, documents,
                    file_names, completed_on, completion_date, next_due_date,
                    concurred_by, remarks, action, date_list, validity_date, unit_name
                )
            )
        approval_compliances = []
        for assignee in assignee_wise_compliances:
            if len(assignee_wise_compliances[assignee]) > 0:
                approval_compliances.append(
                    clienttransactions.APPORVALCOMPLIANCELIST(
                        assignee_id_name_map[assignee], assignee,
                        assignee_wise_compliances[assignee]
                    )
                )
            else:
                continue
        return approval_compliances, count

    def get_user_name_by_id(self, user_id, client_id=None):
        employee_name = None
        if user_id is not None and user_id != 0:
            columns = "employee_code, employee_name"
            condition = "user_id ='{}'".format(user_id)
            rows = self.get_data(
                self.tblUsers, columns, condition
            )
            if len(rows) > 0:
                employee_name = "{} - {}".format(rows[0][0], rows[0][1])
        else:
            employee_name = "Administrator"
        return employee_name

#
# Assign Compliance
#

    def get_units_for_dashboard_filters(self, session_user, is_closed=True):
        return self.get_units_for_assign_compliance(session_user, is_closed)

    def get_units_for_assign_compliance(self, session_user, is_closed=None):
        if is_closed is None :
            is_close = 0
        else:
            is_close = '%'
        if session_user > 0 and session_user != self.get_admin_id() :
            qry = ' AND t1.unit_id in (select distinct unit_id from tbl_user_units where user_id = %s) ' % (int(session_user))
        else :
            qry = ""
        query = "SELECT distinct t1.unit_id, t1.unit_code, t1.unit_name, \
            t1.division_id, t1.legal_entity_id, t1.business_group_id, \
            t1.address, t1.country_id, domain_ids\
            FROM tbl_units t1 WHERE t1.is_closed like '%s'" % is_close
        query += qry

        rows = self.select_all(query)
        columns = [
            "unit_id", "unit_code", "unit_name",
            "division_id", "legal_entity_id",
            "business_group_id", "address", "country_id", "domain_ids"
        ]
        result = self.convert_to_dict(rows, columns)
        return self.return_units_for_assign_compliance(result)

    def get_units_to_assig(self, session_user) :
        if session_user > 0 and session_user != self.get_admin_id() :
            qry = ' AND t1.unit_id in (select distinct unit_id from tbl_user_units where user_id = %s) ' % (int(session_user))
        else :
            qry = ""
        query = "SELECT distinct t1.unit_id, t1.unit_code, t1.unit_name, \
            t1.division_id, t1.legal_entity_id, t1.business_group_id, \
            t1.address, t1.country_id, domain_ids\
            FROM tbl_units t1 WHERE t1.is_closed = 0 \
            AND (select count(distinct t1.compliance_id) from tbl_client_compliances t1 \
                inner join tbl_client_statutories t2  \
                on t1.client_statutory_id = t2.client_statutory_id \
                left join tbl_assigned_compliances t3 \
                on t3.unit_id = t2.unit_id and t3.compliance_id = t1.compliance_id \
                inner join tbl_compliances t4 on t4.compliance_id = t1.compliance_id and t4.is_active = 1 \
                where t3.compliance_id is null and t1.compliance_opted = 1 \
                and t2.unit_id = t1.unit_id) > 0 "

        query += qry

        rows = self.select_all(query)
        columns = [
            "unit_id", "unit_code", "unit_name",
            "division_id", "legal_entity_id",
            "business_group_id", "address", "country_id", "domain_ids"
        ]
        result = self.convert_to_dict(rows, columns)
        return self.return_units_for_assign_compliance(result)

    def return_units_for_assign_compliance(self, result):
        unit_list = []
        for r in result :
            name = "%s - %s" % (r["unit_code"], r["unit_name"])
            division_id = None
            b_group_id = None
            if r["division_id"] > 0 :
                division_id = r["division_id"]
            if r["business_group_id"] > 0 :
                b_group_id = r["business_group_id"]

            domain_ids = [int(x) for x in r["domain_ids"].split(',')]
            unit_list.append(
                clienttransactions.ASSIGN_COMPLIANCE_UNITS(
                    r["unit_id"], name,
                    r["address"],
                    division_id,
                    r["legal_entity_id"],
                    b_group_id,
                    r["country_id"],
                    domain_ids
                )
            )
        return unit_list

    def get_users_for_seating_units(self, session_user, client_id):
        where_condition = "WHERE t1.is_primary_admin = 0 AND t1.is_active = 1 AND t2.unit_id \
            IN \
            (select distinct unit_id from tbl_user_units where user_id = %s)" % (session_user)
        query = "SELECT distinct t1.user_id, t1.service_provider_id, t1.employee_name, \
            t1.employee_code, \
            t1.seating_unit_id, t1.user_level, \
            (select group_concat(distinct domain_id) from tbl_user_domains where user_id = t1.user_id) domain_ids, \
            (select group_concat(distinct unit_id) from tbl_user_units where user_id = t1.user_id ) unit_ids,\
            t1.is_service_provider, \
            (select service_provider_name from  tbl_service_providers where service_provider_id = t1.service_provider_id) service_provider, \
            (select form_ids from tbl_user_groups where user_group_id = t1.user_group_id)fomr_ids\
            FROM tbl_users t1 \
            INNER JOIN tbl_user_units t2 \
            ON t1.user_id = t2.user_id "

        if session_user > 0 and session_user != self.get_admin_id() :
            query = query + where_condition
        else :
            query = query + " AND t1.is_active = 1 "
        rows = self.select_all(query)
        columns = [
            "user_id", "service_provider_id", "employee_name", "employee_code",
            "seating_unit_id", "user_level",
            "domain_ids", "unit_ids",
            "is_service_provider", "service_provider",
            "form_ids"
        ]
        result = self.convert_to_dict(rows, columns)
        user_list = []
        for r in result :
            q = "select distinct unit_id from tbl_user_units where user_id = %s" % (int(r["user_id"]))
            r_rows = self.select_all(q)
            r_unit_ids = self.convert_to_dict(r_rows, ["unit_id"])
            unit_ids = []
            for u in r_unit_ids :
                unit_ids.append(u["unit_id"])
            if int(r["is_service_provider"]) == 0 :
                name = "%s - %s" % (r["employee_code"], r["employee_name"])
            else :
                name = "%s - %s" % (r["service_provider"], r["employee_name"])
            unit_id = None
            if r["seating_unit_id"]:
                unit_id = int(r["seating_unit_id"])
            domain_ids = [
                int(x) for x in r["domain_ids"].split(',')
            ]
            # unit_ids = [
            #     int(y) for y in r["unit_ids"].split(',')
            # ]
            form_ids = [int(x) for x in r["form_ids"].split(',')]
            is_assignee = False
            is_approver = False
            is_concurrence = False

            if 11 in form_ids or 12 in form_ids :
                is_assignee = True
            if 9 in form_ids :
                is_concurrence = True
                is_approver = True

            user = clienttransactions.ASSIGN_COMPLIANCE_USER(
                r["user_id"],
                r["service_provider_id"],
                name,
                r["user_level"],
                unit_id,
                unit_ids,
                domain_ids,
                is_assignee,
                is_approver,
                is_concurrence
            )
            # user_list = seating_unit_users.get(unit_id)
            # if user_list is None :
            #     user_list = []
            # user_list.append(user)
            # seating_unit_users[unit_id] = user_list
            user_list.append(user)

        return user_list

    def total_compliance_for_units(self, unit_ids, domain_id):
        q = "select \
                count(distinct t01.compliance_id) \
            From \
                tbl_client_compliances t01 \
                    inner join \
                tbl_client_statutories t02 ON t01.client_statutory_id = t02.client_statutory_id \
                    inner join \
                tbl_compliances t04 ON t01.compliance_id = t04.compliance_id \
                    left join \
                tbl_assigned_compliances t03 ON t02.unit_id = t03.unit_id \
                    and t01.compliance_id = t03.compliance_id \
            where \
            t02.unit_id in %s \
            and t02.domain_id = %s \
            and t02.is_new = 1 \
            and t01.compliance_opted = 1 \
            and t04.is_active = 1 \
            and t03.compliance_id IS NULL " % (
            str(tuple(unit_ids)),
            domain_id
        )
        row = self.select_one(q)
        if row :
            return row[0]
        else :
            return 0

    def get_assign_compliance_statutories_for_units(
        self, unit_ids, domain_id, session_user, from_count, to_count
    ):
        if len(unit_ids) == 1 :
            unit_ids.append(0)
        if session_user == 0 or session_user == self.get_admin_id() :
            session_user = '%'

        qry_applicable = "SELECT distinct A.compliance_id, B.unit_id units \
            FROM \
                tbl_client_compliances A \
                INNER JOIN tbl_client_statutories B ON A.client_statutory_id = B.client_statutory_id \
                INNER JOIN tbl_compliances C ON A.compliance_id = C.compliance_id \
                LEFT JOIN tbl_assigned_compliances AC ON B.unit_id = AC.unit_id AND A.compliance_id = AC.compliance_id \
            WHERE \
                B.unit_id in %s \
                AND B.domain_id = %s \
                AND A.compliance_opted = 1 \
                AND C.is_active = 1 \
                AND B.is_new = 1 \
                AND AC.compliance_id is null \
            ORDER BY SUBSTRING_INDEX(SUBSTRING_INDEX(C.statutory_mapping, '>>', 1), \
                    '>>', \
                    - 1) , A.compliance_id \
            " % (
                str(tuple(unit_ids)),
                domain_id
            )
        query = " SELECT distinct \
            t2.compliance_id, \
            t1.domain_id, \
            t3.compliance_task, \
            t3.document_name, \
            t3.compliance_description, \
            t3.statutory_mapping, \
            t3.statutory_provision, \
            t3.statutory_dates, \
            (select frequency from tbl_compliance_frequency where frequency_id = t3.frequency_id) frequency, \
            t3.frequency_id, \
            (select duration_type from tbl_compliance_duration_type where duration_type_id = t3.duration_type_id) duration_type, \
            t3.duration, \
            (select repeat_type from tbl_compliance_repeat_type where repeat_type_id = t3.repeats_type_id) repeat_type, \
            t3.repeats_every, \
            t3.repeats_type_id\
        FROM \
            tbl_client_compliances t2  \
                INNER JOIN \
            tbl_client_statutories t1 ON t2.client_statutory_id = t1.client_statutory_id \
                INNER JOIN \
            tbl_compliances t3 ON t2.compliance_id = t3.compliance_id \
          LEFT JOIN tbl_assigned_compliances AC ON t2.compliance_id = AC.compliance_id and t1.unit_id = AC.unit_id \
        WHERE t1.unit_id IN %s \
          AND t1.domain_id = %s \
                AND t1.is_new = 1 \
                AND t2.compliance_opted = 1 \
                AND t3.is_active = 1 \
                AND AC.compliance_id IS NULL \
        ORDER BY SUBSTRING_INDEX(SUBSTRING_INDEX(t3.statutory_mapping, '>>', 1), \
                '>>', - 1) , t2.compliance_id \
        limit %s, %s " % (
            str(tuple(unit_ids)),
            domain_id,
            from_count,
            to_count
        )
        self.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ;")
        total = self.total_compliance_for_units(unit_ids, domain_id)
        c_rows = self.select_all(qry_applicable)
        rows = self.select_all(query)
        self.execute("SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ ;")

        temp = self.convert_to_dict(c_rows, ["compliance_id", "units"])
        applicable_units = {}
        for r in temp :
            c_id = int(r["compliance_id"])
            if applicable_units.get(c_id) is None :
                applicable_units[c_id] = [int(r["units"])]
            else :
                applicable_units[c_id].append(int(r["units"]))

        columns = [
            "compliance_id", "domain_id",
            "compliance_task",
            "document_name", "compliance_description",
            "statutory_mapping", "statutory_provision",
            "statutory_dates", "frequency", "frequency_id", "duration_type", "duration",
            "repeat_type", "repeats_every", "repeats_type_id"
        ]
        result = self.convert_to_dict(rows, columns)
        return self.return_assign_compliance_data(result, applicable_units, total)

    def set_new_due_date(self, statutory_dates, repeats_type_id, compliance_id):
        due_date = None
        due_date_list = []
        date_list = []
        now = datetime.datetime.now()
        current_year = now.year
        current_month = now.month
        for date in statutory_dates:
                s_date = core.StatutoryDate(
                    date["statutory_date"],
                    date["statutory_month"],
                    date["trigger_before_days"],
                    date.get("repeat_by")
                )
                date_list.append(s_date)

                s_month = date["statutory_month"]
                s_day = date["statutory_date"]
                current_date = n_date = datetime.date.today()

                if s_date.statutory_date is not None :
                    try :
                        n_date = n_date.replace(day=int(s_day))
                    except ValueError :
                        if n_date.month == 12 :
                            days = 31
                        else :
                            days = (n_date.replace(month=n_date.month+1, day=1) - datetime.timedelta(days=1)).day
                        n_date = n_date.replace(day=days)

                if s_date.statutory_month is not None :
                    if s_date.statutory_date is not None :
                        n_date = n_date.replace(day=s_day, month=int(s_month))
                    else :
                        try :
                            n_date = n_date.replace(month=int(s_month))
                        except ValueError :
                            if n_date.month == 12 :
                                days = 31
                            else :
                                days = (n_date.replace(day=1, month=s_month+1) - datetime.timedelta(days=1)).day
                            n_date = n_date.replace(day=days, month=int(s_month))
                if current_date > n_date:
                    if repeats_type_id == 2 and len(statutory_dates) == 1 :
                        try :
                            n_date = n_date.replace(month=current_month+1)
                        except ValueError :
                            if n_date.month == 12 :
                                days = 31
                            else :
                                days = (n_date.replace(day=1, month=current_month+1, year=current_year+1) - datetime.timedelta(days=1)).day
                            try :
                                n_date = n_date.replace(day=days, month=current_month+1)
                            except ValueError :
                                logger.logClient("error", "set_new_due_date", n_date)
                                logger.logClient("error", "set_new_due_date", days)
                                logger.logClient("error", "set_new_due_date", current_month+1)

                    else :
                        try :
                            n_date = n_date.replace(year=current_year+1)
                        except ValueError :
                            if n_date.month == 12 :
                                days = 31
                            else :
                                days = (n_date.replace(day=1, month=n_date.month+1, year=current_year+1) - datetime.timedelta(days=1)).day

                            n_date = n_date.replace(day=days, year=current_year+1)
                if s_day is None and s_month is None :
                    due_date = ""
                else :
                    due_date = n_date.strftime("%d-%b-%Y")
                due_date_list.append(due_date)
        return due_date, due_date_list, date_list

    def return_assign_compliance_data(self, result, applicable_units, total):
        level_1_wise = {}
        level_1_name = []
        for r in result:
            c_id = int(r["compliance_id"])
            maipping = r["statutory_mapping"].split(">>")
            level_1 = maipping[0].strip()
            c_units = applicable_units.get(c_id)
            if c_units is None :
                continue
            print c_units
            unit_ids = c_units
            # unit_ids = [
            #     int(x) for x in c_units.split(',')
            # ]
            compliance_list = level_1_wise.get(level_1)
            if compliance_list is None :
                compliance_list = []
            if r["document_name"] not in ("", "None", None):
                name = "%s - %s" % (r["document_name"], r["compliance_task"])
            else :
                name = r["compliance_task"]
            statutory_dates = r["statutory_dates"]
            statutory_dates = json.loads(statutory_dates)

            if r["frequency_id"] in (2, 3) :
                summary = "Repeats every %s - %s" % (r["repeats_every"], r["repeat_type"])
            elif r["frequency_id"] == 4 :
                summary = "To complete within %s - %s" % (r["duration"], r["duration_type"])
            else :
                summary = None

            due_date, due_date_list, date_list = self.set_new_due_date(statutory_dates, r["repeats_type_id"], c_id)

            compliance = clienttransactions.UNIT_WISE_STATUTORIES(
                c_id,
                name,
                r["compliance_description"],
                core.COMPLIANCE_FREQUENCY(r["frequency"]),
                date_list,
                due_date_list,
                unit_ids,
                summary
            )
            compliance_list.append(compliance)
            level_1_wise[level_1] = compliance_list
        level_1_name = sorted(level_1_wise.keys())
        return level_1_name, level_1_wise, total

    def get_email_id_for_users(self, user_id):
        if user_id == 0 :
            q = "SELECT 'Administrator', username from tbl_admin where admin_id = %s" % (
                user_id
            )
            pass
        else :
            q = "SELECT employee_name, email_id from tbl_users where user_id = %s" % (
                user_id
            )
        row = self.select_one(q)
        if row :
            return row[0], row[1]
        else :
            return None

    def validate_compliance_due_date(self, request):
        c_ids = []
        for c in request.compliances :
            c_ids.append(c.compliance_id)
            q = "SELECT compliance_id, compliance_task, statutory_dates, repeats_type_id from tbl_compliances \
                where compliance_id = %s" % int(c.compliance_id)
            row = self.select_one(q)
            if row :
                comp_id = row[0]
                task = row[1]
                s_dates = json.loads(row[2])
                repeats_type_id = row[3]
                due_date, due_date_list, date_list = self.set_new_due_date(s_dates, repeats_type_id, comp_id)

                if c.due_date not in [None, ""] and due_date not in [None, ""]:
                    t_due_date = datetime.datetime.strptime(c.due_date, "%d-%b-%Y")
                    n_due_date = datetime.datetime.strptime(due_date, "%d-%b-%Y")
                    if (n_due_date < t_due_date) :
                        # Due date should be lessthen statutory date
                        return False, task
        return True, None

    # start current date compliances after assign-compliances
    def start_new_task(self, current_date, country_id):
        # print "bg task start begin"
        try :
            self._compliance_task.begin()
            self._compliance_task.start(current_date, country_id)
            self._compliance_task.commit()
            # print "bg task start end"
        except Exception, e:
            print e
            logger.logClientApi("task-start", e)
            self._compliance_task.rollback()
            # print "bg task start rollback"

    def save_assigned_compliance(self, request, session_user, client_id):
        new_unit_settings = request.new_units
        current_date = self.get_date_time()
        created_on = str(current_date)
        country_id = int(request.country_id)
        assignee = int(request.assignee)
        concurrence = request.concurrence_person
        approval = int(request.approval_person)
        compliances = request.compliances

        compliance_names = []
        columns = [
            "country_id", "unit_id", "compliance_id",
            "statutory_dates", "assignee",
            "approval_person", "trigger_before_days",
            "due_date", "validity_date", "created_by",
            "created_on"
        ]
        value_list = []
        update_column = [
            "statutory_dates", "assignee",
            "approval_person", "trigger_before_days",
            "due_date", "validity_date", "created_by",
            "created_on"
        ]

        if concurrence is not None :
            columns.append("concurrence_person")
            update_column.append("concurrence_person")

        for c in compliances :
            compliance_id = int(c.compliance_id)
            statutory_dates = c.statutory_dates
            if statutory_dates is not None :
                date_list = []
                for dates in statutory_dates :
                    date_list.append(dates.to_structure())
                date_list = json.dumps(date_list)
            else :
                date_list = []

            unit_ids = c.unit_ids
            if c.trigger_before is not None :
                trigger_before = int(c.trigger_before)
            else :
                trigger_before = "0"
            if c.due_date is not None :
                due_date = datetime.datetime.strptime(c.due_date, "%d-%b-%Y")
                a_due_date = due_date
            else :
                due_date = "0000-00-00"
                a_due_date = "Nil"

            compliance_names.append("Complaince Name:" + c.compliance_name + "- Due Date:" + str(a_due_date))
            validity_date = c.validity_date
            if validity_date is not None :
                validity_date = datetime.datetime.strptime(validity_date, "%d-%b-%Y")
                if due_date > validity_date :
                    due_date = validity_date
                elif (validity_date - datetime.timedelta(days=90)) > due_date :
                    due_date = validity_date
            else :
                validity_date = "0000-00-00"

            for unit_id in unit_ids :
                value = [
                    country_id, unit_id, compliance_id,
                    str(date_list), assignee,
                    approval, trigger_before, str(due_date),
                    str(validity_date), int(session_user), created_on
                ]
                if concurrence is not None :
                    value.append(concurrence)
                value_list.append(tuple(value))

        # self.bulk_insert("tbl_assigned_compliances", columns, value_list)
        self.on_duplicate_key_update("tbl_assigned_compliances", ",".join(columns), value_list, update_column)
        if new_unit_settings is not None :
            self.update_user_settings(new_unit_settings)

        compliance_names = " <br> ".join(compliance_names)
        if request.concurrence_person_name is None :
            action = " Following compliances has assigned to assignee - %s and approval-person - %s <br> %s" % (
                request.assignee_name,
                request.approval_person_name,
                compliance_names
            )
        else :
            action = " Following compliances has assigned to assignee - %s concurrence-person - %s approval-person - %s <br> %s" % (
                request.assignee_name,
                request.concurrence_person_name,
                request.approval_person_name,
                compliance_names
            )
        activity_text = action.replace("<br>", " ")
        self.save_activity(session_user, 7, json.dumps(activity_text))
        receiver = self.get_email_id_for_users(assignee)[1]
        notify_assign_compliance = threading.Thread(
            target=email.notify_assign_compliance,
            args=[
                receiver, request.assignee_name, action
            ]
        )
        notify_assign_compliance.start()

        # bg_task_start = threading.Thread(
        #     target=self.start_new_task,
        #     args=[
        #         current_date.date(), country_id
        #     ]
        # )
        # # print "bg_task_start begin"
        # bg_task_start.start()
        # self.start_new_task(current_date.date(), country_id)

        return clienttransactions.SaveAssignedComplianceSuccess()

    def update_user_settings(self, new_units):
        for n in new_units :
            user_id = n.user_id
            unit_ids = n.unit_ids
            domain_ids = n.domain_id
            country_ids = n.country_id

            user_units = self.get_user_unit_ids(user_id)
            user_units = [int(x) for x in user_units.split(',')]
            new_unit = []
            if unit_ids is not None :
                for u_id in unit_ids :
                    if u_id not in user_units :
                        new_unit.append(u_id)

            if len(new_unit) > 0 :
                unit_values_list = []
                unit_columns = ["user_id", "unit_id"]
                for unit_id in new_unit:
                    unit_value_tuple = (int(user_id), int(unit_id))
                    unit_values_list.append(unit_value_tuple)
                self.bulk_insert(self.tblUserUnits, unit_columns, unit_values_list)
                # action = "New units %s added for user %s while assign compliance " % (new_units, user_id)
                # self.save_activity(user_id, 7, action)

            user_domain_ids = self.get_user_domains(user_id)
            user_domain_ids = [int(x) for x in user_domain_ids.split(',')]
            new_domains = []
            if domain_ids is not None :
                for d_id in domain_ids :
                    if d_id not in user_domain_ids :
                        new_domains.append(d_id)

            if len(new_domains) > 0 :
                domain_values_list = []
                domain_columns = ["user_id", "domain_id"]
                for domain_id in new_domains :
                    domain_value_tuple = (int(user_id), int(domain_id))
                    domain_values_list.append(domain_value_tuple)
                self.bulk_insert(self.tblUserDomains, domain_columns, domain_values_list)

                # if domain_id not in user_domain_ids :
                #     domain_columns = ["user_id", "domain_id"]
                #     values = (user_id, domain_id)
                #     value_list = [values]
                #     self.bulk_insert(self.tblUserDomains, domain_columns, value_list, client_id)
                #     # action = "New domains %s added for user %s while assign compliance " % (domain_id, user_id)
                #     # self.save_activity(user_id, 7, action)

            user_countries = self.get_user_countries(user_id)
            user_countries = [int(x) for x in user_countries.split(',')]
            new_countries = []
            if country_ids is not None :
                for c_id in country_ids :
                    if c_id not in user_countries :
                        new_countries.append(c_id)

            if len(new_countries) > 0 :
                country_values_list = []
                country_columns = ["user_id", "country_id"]
                for country_id in new_countries :
                    country_value_tuple = (int(user_id), int(country_id))
                    country_values_list.append(country_value_tuple)
                self.bulk_insert(self.tblUserCountries, country_columns, country_values_list)
                # if country_id not in user_countries :
                #     country_columns = ["user_id", "country_id"]
                #     values = (user_id, country_id)
                #     value_list = [values]
                #     self.bulk_insert(self.tblUserCountries, country_columns, value_list, client_id)

#
#   Chart Api
#
    def get_group_name(self):
        query = "SELECT group_name from %s " % self.tblClientGroups
        row = self.select_one(query)
        if row :
            return row[0]
        return "group_name"

    def get_country_wise_domain_month_range(self):
        q = "SELECT t1.country_id, \
        (select country_name from tbl_countries where country_id = t1.country_id) country_name, \
        t1.domain_id,\
        (select domain_name from tbl_domains where domain_id = t1.domain_id)domain_name,\
        t1.period_from, t1.period_to from tbl_client_configurations t1 INNER JOIN \
        tbl_countries TC ON TC.country_id = t1.country_id  \
        INNER JOIN tbl_domains TD ON TD.domain_id = t1.domain_id"
        rows = self.select_all(q)
        columns = [
            "country_id", "country_name",
            "domain_id", "domain_name",
            "period_from", "period_to"
        ]
        result = self.convert_to_dict(rows, columns)

        country_wise = {}
        domain_info = []
        for r in result:
            country_name = r["country_name"].strip()
            domain_name = r["domain_name"]
            info = dashboard.DomainWiseYearConfiguration(
                country_name,
                domain_name,
                self.string_full_months.get(int(r["period_from"])),
                self.string_full_months.get(int(r["period_to"]))
            )
            domain_info = country_wise.get(country_name)
            if domain_info is None :
                domain_info = []

            domain_info.append(info)
            country_wise[country_name] = domain_info
        return country_wise

    def get_compliance_status(
        self, status_type_qry,
        request, user_id, chart_type=None
    ):
        country_ids = request.country_ids

        if len(country_ids) == 1 :
            country_ids.append(0)
        domain_ids = request.domain_ids

        if len(domain_ids) == 1 :
            domain_ids.append(0)
        filter_type = request.filter_type

        # domain_ids = request.domain_ids
        filter_ids = request.filter_ids
        year_range_qry = ""

        if chart_type is None :
            from_date = request.from_date
            if from_date == "" :
                from_date = None
            to_date = request.to_date
            if to_date == "" :
                to_date = None
            chart_year = request.chart_year
            year_condition = self.get_client_domain_configuration(chart_year)[1]

            for i, y in enumerate(year_condition):
                if i == 0 :
                    year_range_qry = y
                else :
                    year_range_qry += "OR %s" % (y)
            if len(year_condition) > 0 :
                year_range_qry = "AND (%s)" % year_range_qry
            else :
                year_range_qry = ""

        else :
            from_date = None
            to_date = None

        if filter_type == "Group" :
            group_by_name = "T3.country_id"
            filter_type_ids = ""
            filter_ids = country_ids

        elif filter_type == "BusinessGroup" :
            filters = self.get_user_business_group_ids(user_id)
            # filter_ids = filters.split(',')
            if len(filter_ids) == 1 :
                filter_ids.append(0)
            group_by_name = "T3.business_group_id"
            filter_type_ids = "AND T3.business_group_id in %s" % str(tuple(filter_ids))

        elif filter_type == "LegalEntity" :
            filters = self.get_user_legal_entity_ids(user_id)
            # filter_ids = filters.split(',')
            if len(filter_ids) == 1 :
                filter_ids.append(0)
            group_by_name = "T3.legal_entity_id"
            filter_type_ids = "AND T3.legal_entity_id in %s" % str(tuple(filter_ids))

        elif filter_type == "Division" :
            filters = self.get_user_division_ids(user_id)
            # filter_ids = filters.split(',')
            if len(filter_ids) == 1 :
                filter_ids.append(0)
            group_by_name = "T3.division_id"
            filter_type_ids = "AND T3.division_id in %s" % str(tuple(filter_ids))

        elif filter_type == "Unit":
            filters = self.get_user_unit_ids(user_id)
            # filter_ids = filters.split(',')
            if len(filter_ids) == 1 :
                filter_ids.append(0)
            group_by_name = "T3.unit_id"
            filter_type_ids = "AND T3.unit_id in %s" % str(tuple(filter_ids))

        elif filter_type == "Consolidated":
            group_by_name = "T3.country_id"
            filter_type_ids = ""
            filter_ids = country_ids

        if user_id == 0 :
            user_qry = '1'
        else :
            user_qry = "(T1.completed_by LIKE '%s' OR T1.concurred_by LIKE '%s' \
            OR T1.approved_by LIKE '%s')" % (user_id, user_id, user_id)

        date_qry = ""
        if from_date is not None and to_date is not None :
            from_date = self.string_to_datetime(from_date)
            to_date = self.string_to_datetime(to_date)
            date_qry = "AND T1.due_date >= '%s' AND T1.due_date <= '%s' " % (from_date, to_date)
        query = "SELECT \
            %s, \
            T3.country_id, \
            T2.domain_id, \
            YEAR(T1.due_date) as year, \
            MONTH(T1.due_date) as month,  \
            count(1) as compliances \
            FROM tbl_compliance_history T1  \
            INNER JOIN tbl_compliances T2 ON T1.compliance_id = T2.compliance_id  \
            INNER JOIN tbl_units T3  \
            ON T1.unit_id = T3.unit_id  \
            WHERE %s \
            %s \
            %s \
            %s \
            AND T3.country_id IN %s \
            AND T2.domain_id IN %s  \
            %s \
            GROUP BY month, year, T2.domain_id, %s\
            ORDER BY month desc, year desc, %s" % (
                group_by_name,
                user_qry,
                year_range_qry,
                status_type_qry,
                date_qry,
                str(tuple(country_ids)),
                str(tuple(domain_ids)),
                filter_type_ids,
                group_by_name,
                group_by_name
            )
        # # print query
        rows = self.select_all(query)
        columns = ["filter_type", "country_id", "domain_id", "year", "month", "compliances"]
        return filter_ids, self.convert_to_dict(rows, columns)

    def calculate_years(self, month_from, month_to):
        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year
        if month_from == 1 and month_to == 12 :
            single_years = []
            single_years.append([current_year])
            for i in range(1, 7):
                single_years.append([current_year - i])
            return single_years
        else :
            double_years = []
            if current_month in [int(m) for m in range(month_from, 12+1)] :
                first_year = current_year
                second_year = current_year + 1
                years = [first_year, second_year]
                # print first_year, second_year, years
            elif current_month in [int(m) for m in range(1, month_to+1)] :
                first_year = current_year - 1
                second_year = current_year
                # print first_year, second_year

            for i in range(1, 8):
                if i == 1 :
                    years = [first_year, second_year]
                    # print years
                else :
                    first_year = current_year - i
                    second_year = first_year + 1
                    years = [first_year, second_year]
                    # print years

                double_years.append(years)
            # print double_years
            return double_years

    def get_status_wise_compliances_count(self, request, session_user):
        user_id = int(session_user)
        from_date = request.from_date
        to_date = request.to_date
        chart_year = request.chart_year

        filter_ids = []

        inprogress_qry = " AND ((IFNULL(T2.duration_type_id, 0) = 2 AND T1.due_date >= now()) or (IFNULL(T2.duration_type_id, 0) != 2 and T1.due_date >= CURDATE())) \
                AND IFNULL(T1.approve_status,0) != 1"

        complied_qry = " AND T1.due_date >= T1.completion_date \
                AND IFNULL(T1.approve_status,0) = 1"

        delayed_qry = " AND T1.due_date < T1.completion_date \
                AND IFNULL(T1.approve_status,0) = 1"

        not_complied_qry = " AND ((IFNULL(T2.duration_type_id, 0) = 2 AND T1.due_date < now()) or (IFNULL(T2.duration_type_id, 0) != 2 and T1.due_date < CURDATE())) \
                AND IFNULL(T1.approve_status,0) != 1"

        filter_ids, inprogress = self.get_compliance_status(
                inprogress_qry, request, user_id
            )
        filter_ids, complied = self.get_compliance_status(
                complied_qry, request, user_id
            )
        filter_ids, delayed = self.get_compliance_status(
                delayed_qry, request, user_id
            )
        filter_ids, not_complied = self.get_compliance_status(
                not_complied_qry, request, user_id
            )
        if from_date is not None and to_date is not None :
            return self.frame_compliance_status_count(
                inprogress, complied, delayed,
                not_complied
            )
        else :
            return self.frame_compliance_status_yearwise_count(
                inprogress, complied, delayed, not_complied,
                filter_ids, chart_year
            )

    def get_client_domain_configuration(
        self, current_year=None
    ):
        where_qry = ""

        query = "SELECT country_id, domain_id, \
            period_from, period_to \
            FROM  tbl_client_configurations %s" % (where_qry)

        rows = self.select_all(query)
        columns = ["country_id", "domain_id", "period_from", "period_to"]
        data = self.convert_to_dict(rows, columns)
        years_range = []
        year_condition = []
        cond = "(T3.country_id = %s AND T2.domain_id = %s AND YEAR(T1.due_date) IN %s)"
        for d in data :
            info = {}
            country_id = int(d["country_id"])
            domain_id = int(d["domain_id"])
            info["country_id"] = country_id
            info["domain_id"] = domain_id
            year_list = self.calculate_years(int(d["period_from"]), int(d["period_to"]))
            years_list = []
            if current_year is None :
                years_list = year_list
            else :
                for y in year_list :
                    if current_year == y[0]:
                        years_list.append(y)
                        if len(y) == 1 :
                            y.append(0)
                        year_condition.append(
                            cond % (country_id, domain_id, str(tuple(y)))
                        )
            if len(years_list) == 0 :
                info["years"] = []
            else :
                info["years"] = years_list
            info["period_from"] = int(d["period_from"])
            info["period_to"] = int(d["period_to"])
            years_range.append(info)
        return (years_range, year_condition)

    def calculate_year_wise_count(
        self,
        calculated_data, years_info, compliances,
        status, filter_ids
    ):
        for f in filter_ids:
            if f == 0:
                continue
            filter_type = int(f)
            for y in years_info :

                country_id = y["country_id"]

                domain_id = y["domain_id"]

                country = calculated_data.get(filter_type)
                if country is None :
                    country = {}

                years_range = y["years"]

                year_wise = country.get(domain_id)

                if year_wise is None :
                    year_wise = {}

                period_from = int(y["period_from"])
                period_to = int(y["period_to"])
                for index, i in enumerate(years_range) :
                    compliance_count_info = year_wise.get(i[0])
                    if compliance_count_info is None :
                        compliance_count_info = {
                            "inprogress_count": 0,
                            "complied_count": 0,
                            "delayed_count": 0,
                            "not_complied_count": 0,
                            "country_id": country_id,
                            "domain_id": domain_id
                        }
                    compliance_count = 0
                    for c in compliances :
                        if int(c["year"]) not in (i) :
                            continue
                        if (
                            filter_type == int(c["filter_type"]) and
                            country_id == int(c["country_id"]) and
                            domain_id == int(c["domain_id"])
                        ):
                            month = int(c["month"])

                            if len(i) == 2 :
                                if (
                                    c["year"] == i[0] and
                                    month in [
                                        int(x) for x in range(period_from, 12+1)
                                    ]
                                ):
                                    compliance_count += int(c["compliances"])

                                elif (
                                    c["year"] == i[1] and
                                    month in [
                                        int(y) for y in range(1, period_to+1)
                                    ]
                                ):
                                    compliance_count += int(c["compliances"])

                            else :
                                if (
                                    int(c["year"]) == i[0] and
                                    month in [
                                        int(x) for x in range(period_from, period_to + 1)
                                    ]
                                ):
                                    compliance_count += int(c["compliances"])

                            compliance_count_info["domain_id"] = c["domain_id"]
                            compliance_count_info["country_id"] = c["country_id"]

                    if status == "inprogress":
                        compliance_count_info["inprogress_count"] += compliance_count
                    elif status == "complied" :
                        compliance_count_info["complied_count"] += compliance_count
                    elif status == "delayed" :
                        compliance_count_info["delayed_count"] += compliance_count
                    elif status == "not_complied":
                        compliance_count_info["not_complied_count"] += compliance_count

                    year_wise[i[0]] = compliance_count_info

                country[domain_id] = year_wise
                calculated_data[filter_type] = country

        return calculated_data

    def frame_compliance_status_count(
        self,
        inprogress, complied, delayed,
        not_complied
    ):
        calculated_data = {}

        def compliance_count(compliances, status):
            for i in compliances :
                filter_type = int(i["filter_type"])
                domain_id = int(i["domain_id"])
                domain_wise = calculated_data.get(filter_type)

                # domain_wise = country.get(domain_id)
                if domain_wise is None :
                    domain_wise = {}

                compliance_count_info = domain_wise.get(domain_id)
                if compliance_count_info is None :
                    compliance_count_info = {
                        "inprogress_count": 0,
                        "complied_count": 0,
                        "delayed_count": 0,
                        "not_complied_count": 0,
                    }

                compliance_count_info[status] += int(i["compliances"])
                compliance_count_info["domain_id"] = i["domain_id"]
                compliance_count_info["country_id"] = i["country_id"]
                domain_wise[domain_id] = compliance_count_info
                calculated_data[filter_type] = domain_wise
            return calculated_data

        calculated_data = compliance_count(inprogress, "inprogress_count")
        calculated_data = compliance_count(complied, "complied_count")
        calculated_data = compliance_count(delayed, "delayed_count")
        calculated_data = compliance_count(not_complied, "not_complied_count")

        current_year = datetime.datetime.now().year
        filter_type_wise = {}
        for key, value in calculated_data.iteritems() :
            domain_wise = {}
            compliance_list = []

            for k, v in value.iteritems() :
                year = current_year
                inprogress = v["inprogress_count"]
                complied = v["complied_count"]
                delayed = v["delayed_count"]
                not_complied = v["not_complied_count"]
                country_id = v["country_id"]
                domain_id = v["domain_id"]
                if len(compliance_list) == 0 :
                    compliance_count = core.NumberOfCompliances(
                        domain_id, country_id, str(year), complied,
                        delayed, inprogress, not_complied
                    )
                    compliance_list.append(compliance_count)
                else :
                    compliance_count = compliance_list[0]
                    compliance_count.inprogress_compliance_count += v[0]
                    compliance_count.complied_count += v[1]
                    compliance_count.delayed_compliance_count += v[2]
                    compliance_count.not_complied_count += v[3]

                domain_wise[k] = compliance_list
                compliance_list = []
            filter_type_wise[key] = domain_wise

        final_result_list = []
        for k, v in filter_type_wise.items():
            data_list = []
            for i, j in v.items():
                data_list.extend(j)
            chart = dashboard.ChartDataMap(k, data_list)
            final_result_list.append(chart)
        return final_result_list

    def frame_compliance_status_yearwise_count(
        self,
        inprogress, complied, delayed,
        not_complied, filter_type_ids, current_year
    ):
        year_info = self.get_client_domain_configuration(current_year)[0]
        calculated_data = {}
        calculated_data = self.calculate_year_wise_count(
            calculated_data, year_info, inprogress, "inprogress",
            filter_type_ids
        )
        calculated_data = self.calculate_year_wise_count(
            calculated_data, year_info, complied, "complied",
            filter_type_ids
        )
        calculated_data = self.calculate_year_wise_count(
            calculated_data, year_info, delayed, "delayed",
            filter_type_ids
        )
        calculated_data = self.calculate_year_wise_count(
            calculated_data, year_info, not_complied, "not_complied",
            filter_type_ids
        )

        # Sum compliance for filter_type wise
        filter_type_wise = {}

        for filter_type, value in calculated_data.iteritems():
            domain_wise = {}
            for key, val in value.iteritems():
                compliance_list = []
                for k , v in val.iteritems():
                    year = k
                    inprogress = v["inprogress_count"]
                    complied = v["complied_count"]
                    delayed = v["delayed_count"]
                    not_complied = v["not_complied_count"]
                    country_id = v["country_id"]
                    domain_id = v["domain_id"]
                    compliance_count = core.NumberOfCompliances(
                        domain_id, country_id, str(year), complied,
                        delayed, inprogress, not_complied
                    )
                    compliance_list.append(compliance_count)
                domain_wise[key] = compliance_list
            filter_type_wise[filter_type] = domain_wise

        final_result_list = []
        for k, v in filter_type_wise.items():
            data_list = []
            for i, j in v.items():
                data_list.extend(j)
            chart = dashboard.ChartDataMap(k, data_list)
            final_result_list.append(chart)
        return final_result_list

    def get_client_compliance_count(self):
        q = "select count(*) from tbl_compliances"
        row = self.select_one(q)
        return row[0]

    def get_compliance_status_chart(self, request, session_user, client_id):
        result = self.get_status_wise_compliances_count(request, session_user)
        final = []
        filter_types = []
        for r in result :
            data = r.data
            for d in data :
                if (
                    d.inprogress_compliance_count == 0 and
                    d.not_complied_count == 0 and
                    d.delayed_compliance_count == 0 and
                    d.complied_count == 0
                ):
                    pass
                else :
                    if r.filter_type_id not in filter_types :
                        filter_types.append(r.filter_type_id)
                        final.append(r)

        return dashboard.GetComplianceStatusChartSuccess(final)

    def compliance_details_query(
        self, domain_ids, date_qry, status_qry, filter_type_qry, user_id,
        from_count, to_count
    ) :
        if len(domain_ids) == 1 :
            domain_ids.append(0)
        if user_id == 0 :
            user_qry = '1'
        else :
            user_qry = "(T1.completed_by LIKE '%s' OR T1.concurred_by LIKE '%s' \
            OR T1.approved_by LIKE '%s')" % (user_id, user_id, user_id)

        query = "SELECT \
            T1.compliance_history_id, T1.unit_id,\
            T1.compliance_id, T1.start_date, \
            T1.due_date, T1.completion_date, \
            T1.completed_by,\
            T4.compliance_task, T4.document_name, \
            T4.compliance_description, T4.statutory_mapping, \
            T4.frequency_id, T4.duration_type_id, \
            unit_name, \
            (select division_name from tbl_divisions where division_id = T5.division_id)division_name, \
            (select legal_entity_name from tbl_legal_entities where legal_entity_id = T5.legal_entity_id)legal_entity_name,  \
            (select business_group_name from tbl_business_groups where business_group_id = T5.business_group_id )business_group_name, \
            (select country_name from tbl_countries where country_id = T5.country_id)country_name, \
            (select employee_name from tbl_users where user_id = T1.completed_by) employee_name,\
            T5.unit_code, T5.address, T5.geography, T5.postal_code,\
            T5.industry_name, T5.country_id, \
            T4.domain_id, \
            YEAR(T1.due_date) as year, \
            MONTH(T1.due_date) as month \
            FROM tbl_compliance_history T1  \
            INNER JOIN tbl_compliances T4  ON T1.compliance_id = T4.compliance_id  \
            INNER JOIN tbl_units T5 ON T1.unit_id = T5.unit_id \
            WHERE %s AND \
            T4.domain_id IN %s  \
            %s \
            %s \
            %s \
            ORDER BY  T1.unit_id,  \
            SUBSTRING_INDEX(SUBSTRING_INDEX(T4.statutory_mapping, '>>', 1), '>>', -1), \
            T1.due_date \
            limit %s, %s " % (
                user_qry,
                str(tuple(domain_ids)),
                date_qry,
                status_qry,
                filter_type_qry,
                from_count , to_count
            )
        rows = self.select_all(query)
        columns = [
            "compliance_history_id", "unit_id",
            "compliance_id", "start_date", "due_date",
            "completion_date", "assignee", "compliance_task",
            "document_name", "compliance_description",
            "statutory_mapping", "frequency_id", "duration_type_id",
            "unit_name", "division_name",
            "legal_entity_name", "business_group_name",
            "country_name", "employee_name",
            "unit_code", "address", "geography",
            "postal_code", "industry_name",
            "country_id", "domain_id",
            "year", "month"
        ]
        result = self.convert_to_dict(rows, columns)
        return result

    def get_compliances_details_for_status_chart(self, request, session_user, client_id, from_count, to_count):
        domain_ids = request.domain_ids
        from_date = request.from_date
        to_date = request.to_date
        year = request.year
        filter_type = request.filter_type
        filter_id = request.filter_id
        compliance_status = request.compliance_status

        status_qry = ""
        if compliance_status == "Inprogress" :
            status_qry = " AND ((IFNULL(T4.duration_type_id,0) = 2 AND T1.due_date >= now()) or (IFNULL(T4.duration_type_id, 0) != 2 AND T1.due_date >= CURDATE())) \
                    AND IFNULL(T1.approve_status, 0) != 1"

        elif compliance_status == "Complied" :
            status_qry = " AND T1.due_date >= T1.completion_date \
                AND T1.approve_status = 1"

        elif compliance_status == "Delayed Compliance" :
            status_qry = " AND T1.due_date < T1.completion_date \
                AND T1.approve_status = 1"

        elif compliance_status == "Not Complied" :
            status_qry = " AND ((IFNULL(T4.duration_type_id,0) =2 AND T1.due_date < now()) or (IFNULL(T4.duration_type_id,0) != 2 AND T1.due_date < CURDATE())) \
                AND IFNULL(T1.approve_status, 0) != 1 "

        if filter_type == "Group" :
            filter_type_qry = "AND T5.country_id = %s" % (filter_id)

        elif filter_type == "BusinessGroup" :
            filter_type_qry = "AND T5.business_group_id = %s" % (filter_id)

        elif filter_type == "LegalEntity" :
            filter_type_qry = "AND T5.legal_entity_id = %s" % (filter_id)

        elif filter_type == "Division" :
            filter_type_qry = "AND T5.division_id = %s" % (filter_id)

        elif filter_type == "Unit":
            filter_type_qry = "AND T5.unit_id = %s" % (filter_id)

        date_qry = ""
        if from_date is not None and to_date is not None :
            from_date = self.string_to_datetime(from_date)
            to_date = self.string_to_datetime(to_date)
            date_qry = " AND T1.due_date >= '%s' AND T1.due_date <= '%s' " % (from_date, to_date)

        result = self.compliance_details_query(
            domain_ids, date_qry, status_qry, filter_type_qry,
            session_user, from_count, to_count
        )
        year_info = self.get_client_domain_configuration(int(year))[0]
        return self.return_compliance_details_drill_down(year_info, compliance_status, request.year, result, client_id)

    def calculate_ageing_in_hours(self, ageing) :
        day = ageing.days
        hour = 0
        if day > 0 :
            hour += day * 24
        hour += (ageing.seconds / 3600)
        minutes = (ageing.seconds / 60 % 60)
        summary = "%s:%s Hour(s)" % (hour, minutes)
        return summary

    def return_compliance_details_drill_down(self, year_info, compliance_status, request_year, result, client_id) :
        current_date = datetime.datetime.today()
        unit_wise_data = {}
        for r in result :
            country_id = int(r["country_id"])
            domain_id = int(r["domain_id"])
            saved_year = int(r["year"])
            saved_month = int(r["month"])

            years_list = []
            month_from = 0
            month_to = 0
            for y in year_info :
                if country_id == int(y["country_id"]) and domain_id == int(y["domain_id"]) :
                    years = y["years"]
                    month_from = int(y["period_from"])
                    month_to = int(y["period_to"])
                    for i in years :
                        year = 0
                        if type(i) is int and i == int(request_year):
                            years_list = [i]
                        elif type(i) is list :
                            if i[0] == int(request_year) :
                                years_list = i
                    break

            if saved_year not in years_list :
                continue
            else :
                if len(years_list) == 2:
                    if (
                        saved_year == years_list[0] and
                        saved_month not in [x for x in range(month_from, 12+1)]
                    ):
                        continue
                    elif (
                        saved_year == years_list[1] and
                        saved_month not in [x for x in range(1, month_to+1)]
                    ) :
                        continue

            unit_id = int(r["unit_id"])
            statutories = r["statutory_mapping"].split('>>')
            level_1 = statutories[0].strip()
            ageing = 0
            due_date = r["due_date"]
            completion_date = r["completion_date"]

            if compliance_status == "Inprogress" :
                if r["frequency_id"] != 4 :
                    ageing = abs((due_date.date() - current_date.date()).days) + 1
                else :
                    diff = (due_date - current_date)
                    if r["duration_type_id"] == 2 :
                        ageing = self.calculate_ageing_in_hours(diff)
                    else :
                        ageing = diff.days
            elif compliance_status == "Complied" :
                ageing = 0
            elif compliance_status == "Not Complied" :
                if r["frequency_id"] != 4 :
                    ageing = abs((current_date.date() - due_date.date()).days) + 1
                else :
                    diff = (current_date - due_date)
                    if r["duration_type_id"] == 2 :
                        ageing = self.calculate_ageing_in_hours(diff)
                    else :
                        ageing = diff.days
            elif compliance_status == "Delayed Compliance" :
                ageing = abs((completion_date - due_date).days) + 1
                if r["frequency_id"] != 4 :
                    ageing = abs((completion_date - due_date).days) + 1
                else :
                    diff = (completion_date - due_date)
                    if r["duration_type_id"] == 2 :
                        ageing = self.calculate_ageing_in_hours(diff)
                    else :
                        ageing = diff.days

            if type(ageing) is int :
                ageing = " %s Day(s)" % ageing

            status = core.COMPLIANCE_STATUS(compliance_status)
            if r["document_name"] not in ("", "None", None):
                name = "%s-%s" % (r["document_name"], r["compliance_task"])
            else :
                name = r["compliance_task"]
            if r["employee_name"] is None :
                employee_name = "Administrator"
            else :
                employee_name = r["employee_name"]
            compliance = dashboard.Level1Compliance(
                name, r["compliance_description"], employee_name,
                str(r["start_date"]), str(due_date),
                str(completion_date), status,
                str(ageing)
            )

            drill_down_data = unit_wise_data.get(unit_id)
            if drill_down_data is None :
                level_compliance = {}
                level_compliance[level_1] = [compliance]
                unit_name = "%s-%s" % (r["unit_code"], r["unit_name"])
                geography = r["geography"].split(">>")
                geography.reverse()
                geography = ','.join(geography)
                address = "%s, %s, %s" % (r["address"], geography, r["postal_code"])
                drill_down_data = dashboard.DrillDownData(
                    r["business_group_name"], r["legal_entity_name"],
                    r["division_name"], unit_name, address,
                    r["industry_name"],
                    level_compliance
                )

            else :
                level_compliance = drill_down_data.compliances
                compliance_list = level_compliance.get(level_1)
                if compliance_list is None :
                    compliance_list = []
                compliance_list.append(compliance)

                level_compliance[level_1] = compliance_list
                drill_down_data.compliances = level_compliance

            unit_wise_data[unit_id] = drill_down_data

        return unit_wise_data

#
# Escalation chart
#
    def get_escalation_chart(self, request, session_user, client_id):
        user_id = int(session_user)

        filter_type = request.filter_type

        delayed_qry = " AND T1.due_date < T1.completion_date \
                AND T1.approve_status = 1"

        not_complied_qry = " AND ((IFNULL(T2.duration_type_id, 0) =2 AND T1.due_date < now()) or (IFNULL(T2.duration_type_id, 0) != 2 and T1.due_date < CURDATE())) \
                AND IFNULL(T1.approve_status,0) <> 1"

        chart_type = "Escalation"
        filter_ids, delayed = self.get_compliance_status(
                delayed_qry, request, user_id, chart_type
            )
        filter_ids, not_complied = self.get_compliance_status(
                not_complied_qry, request, user_id, chart_type
            )

        year_info = self.get_client_domain_configuration()[0]
        calculated_data = {}
        calculated_data = self.calculate_year_wise_count(
            calculated_data, year_info, delayed,
            "delayed", filter_ids
        )
        calculated_data = self.calculate_year_wise_count(
            calculated_data, year_info, not_complied,
            "not_complied", filter_ids
        )

        # Sum compliance for filter_type wise
        escalation_years = {}

        filter_ids = request.filter_ids

        for filter_type, value in calculated_data.iteritems():
            if filter_type not in filter_ids :
                continue
            for key, val in value.iteritems():
                for k , v in val.iteritems():
                    year = k
                    delayed = v["delayed_count"]
                    not_complied = v["not_complied_count"]

                    count_det = escalation_years.get(year)
                    if count_det is None :
                        count_det = dashboard.EscalationData(
                            year,
                            delayed,
                            not_complied
                        )
                        # count_det["year"] = year
                        # count_det["delayed_count"] = delayed
                        # count_det["not_complied_count"] = not_complied

                    else :
                        count_det.delayed_compliance_count += int(delayed)
                        count_det.not_complied_count += int(not_complied)

                    escalation_years[year] = count_det

        years = escalation_years.keys()
        years.sort()
        chart_data = []
        for y in years:
            chart_data.append(
                escalation_years.get(y)
            )
        return dashboard.GetEscalationsChartSuccess(
            years, chart_data
        )

    def get_escalation_drill_down_data(
        self, request, session_user, client_id, from_count, to_count
    ):
        domain_ids = request.domain_ids
        filter_type = request.filter_type
        filter_ids = request.filter_ids
        year = request.year

        delayed_status_qry = " AND T1.due_date < T1.completion_date \
            AND T1.approve_status = 1"

        not_complied_status_qry = " AND T1.due_date < CURDATE() \
            AND T1.approve_status is NULL "

        if len(filter_ids) == 1:
            filter_ids.append(0)

        if filter_type == "Group" :
            filter_type_qry = "AND T5.country_id IN %s" % (str(tuple(filter_ids)))

        elif filter_type == "BusinessGroup" :
            filter_type_qry = "AND T5.business_group_id IN %s" % (str(tuple(filter_ids)))

        elif filter_type == "LegalEntity" :
            filter_type_qry = "AND T5.legal_entity_id IN %s" % (str(tuple(filter_ids)))

        elif filter_type == "Division" :
            filter_type_qry = "AND T5.division_id IN %s" % (str(tuple(filter_ids)))

        elif filter_type == "Unit":
            filter_type_qry = "AND T5.unit_id IN %s" % (str(tuple(filter_ids)))

        date_qry = ""

        year_info = self.get_client_domain_configuration()[0]

        delayed_details = self.compliance_details_query(
            domain_ids, date_qry, delayed_status_qry,
            filter_type_qry, session_user,
            from_count, to_count
        )

        delayed_details_list = self.return_compliance_details_drill_down(
            year_info, "Delayed Compliance", year,
            delayed_details, client_id
        )

        not_complied_details = self.compliance_details_query(
            domain_ids, date_qry, not_complied_status_qry,
            filter_type_qry, session_user,
            from_count, to_count
        )

        not_complied_details_list = self.return_compliance_details_drill_down(
            year_info, "Not Complied", year,
            not_complied_details, client_id
        )

        return [delayed_details_list.values(), not_complied_details_list.values()]

#
# Not Complied chart
#

    def get_not_complied_chart(self, request, session_user, client_id):
        country_ids = request.country_ids
        if len(country_ids) == 1:
            country_ids.append(0)
        domain_ids = request.domain_ids
        if len(domain_ids) == 1:
            domain_ids.append(0)
        filter_type = request.filter_type
        _filter_ids = request.filter_ids
        if len(_filter_ids) == 1 :
            _filter_ids.append(0)

        filter_type_ids = ""

        if filter_type == "Group" :
            pass

        elif filter_type == "BusinessGroup" :
            filter_type_ids = "AND T4.business_group_id IN %s" % str(tuple(_filter_ids))

        elif filter_type == "LegalEntity" :
            filter_type_ids = "AND T4.legal_entity_id IN %s" % str(tuple(_filter_ids))

        elif filter_type == "Division" :
            filter_type_ids = "AND T4.division_id IN %s" % str(tuple(_filter_ids))

        elif filter_type == "Unit":
            filter_type_ids = "AND T4.unit_id IN %s" % str(tuple(_filter_ids))

        query = "SELECT T1.compliance_history_id, T1.unit_id, \
            T1.compliance_id, T1.start_date, T1.due_date, \
            T4.business_group_id, T4.legal_entity_id, T4.division_id \
            FROM tbl_compliance_history T1 \
            INNER JOIN tbl_client_compliances T2 \
            ON T1.compliance_id = T2.compliance_id \
            INNER JOIN tbl_client_statutories T3 \
            ON T2.client_statutory_id = T3.client_statutory_id \
            AND T1.unit_id = T3.unit_id \
            INNER JOIN tbl_units T4 \
            ON T1.unit_id = T4.unit_id \
            WHERE T3.country_id IN %s \
            AND T3.domain_id IN %s \
            AND T1.due_date < CURDATE() \
            AND T1.approve_status is NULL \
            OR T1.approve_status != 1 \
            %s \
            ORDER BY T1.due_date " % (
                str(tuple(country_ids)),
                str(tuple(domain_ids)),
                filter_type_ids
            )
        rows = self.select_all(query)
        columns = [
            "compliance_history_id", "unit_id", "compliance_id",
            "start_date", "due_date", "business_group_id",
            "legal_entity_id", "division_id"
        ]
        not_complied = self.convert_to_dict(rows, columns)
        current_date = datetime.datetime.today()
        below_30 = 0
        below_60 = 0
        below_90 = 0
        above_90 = 0

        for i in not_complied :
            if filter_type == "BusinessGroup" :
                if i["business_group_id"] == 0 :
                    continue
                if i["business_group_id"] not in request.filter_ids :
                    continue
            elif filter_type == "LegalEntity" :
                if i["legal_entity_id"] == 0 :
                    continue
                if i["legal_entity_id"] not in request.filter_ids :
                    continue
            elif filter_type == "Division" :
                if i["division_id"] == 0 :
                    continue
                if i["division_id"] not in request.filter_ids :
                    continue
            elif filter_type == "Unit" :
                if i["unit_id"] == 0 :
                    continue
                if i["unit_id"] not in request.filter_ids :
                    continue

            due_date = i["due_date"]
            if due_date is None :
                continue
            ageing = abs((current_date - due_date).days)
            if ageing <= 30 :
                below_30 += 1
            elif ageing > 30 and ageing <= 60 :
                below_60 += 1
            elif ageing > 60 and ageing <= 90 :
                below_90 += 1
            else :
                above_90 += 1

        return dashboard.GetNotCompliedChartSuccess(
            below_30, below_60,
            below_90, above_90
        )

    def get_not_complied_drill_down(self, request, session_user, client_id, from_count, to_count):
        domain_ids = request.domain_ids
        if len(domain_ids) == 1:
            domain_ids.append(0)
        filter_type = request.filter_type
        filter_ids = request.filter_ids
        if len(filter_ids) == 1 :
            filter_ids.append(0)
        not_complied_type = request.not_complied_type

        not_complied_status_qry = " AND T1.due_date < CURDATE() \
            AND T1.approve_status is NULL  OR T1.approve_status != 1"

        filter_type_qry = ""
        if filter_type == "Group" :
            filter_type_qry = "AND T5.country_id IN %s" % (str(tuple(filter_ids)))

        elif filter_type == "BusinessGroup" :
            filter_type_qry = "AND T5.business_group_id IN %s" % (str(tuple(filter_ids)))

        elif filter_type == "LegalEntity" :
            filter_type_qry = "AND T5.legal_entity_id IN %s" % (str(tuple(filter_ids)))

        elif filter_type == "Division" :
            filter_type_qry = "AND T5.division_id IN %s" % (str(tuple(filter_ids)))

        elif filter_type == "Unit":
            filter_type_qry = "AND T5.unit_id IN %s" % (str(tuple(filter_ids)))

        date_qry = ""

        not_complied_details = self.compliance_details_query(
            domain_ids, date_qry, not_complied_status_qry,
            filter_type_qry, session_user,
            from_count, to_count
        )
        current_date = datetime.datetime.today()
        not_complied_details_filtered = []

        for c in not_complied_details :
            due_date = c["due_date"]
            ageing = abs((current_date - due_date).days)

            if not_complied_type == "Below 30":
                if ageing <= 30 :
                    not_complied_details_filtered.append(c)
            elif not_complied_type == "Below 60":
                if ageing > 30 and ageing <= 60 :
                    not_complied_details_filtered.append(c)
            elif not_complied_type == "Below 90":
                if ageing > 60 and ageing <= 90 :
                    not_complied_details_filtered.append(c)
            else :
                if ageing > 90 :
                    not_complied_details_filtered.append(c)
        unit_wise_data = {}
        for r in not_complied_details_filtered :

            unit_id = int(r["unit_id"])
            statutories = r["statutory_mapping"].split('>>')
            level_1 = statutories[0].strip()
            ageing = 0
            due_date = r["due_date"]
            completion_date = r["completion_date"]

            if r["frequency_id"] != 4 :
                    ageing = abs((current_date - due_date).days) + 1
            else :
                diff = (current_date - due_date)
                if r["duration_type_id"] == 2 :
                    ageing = self.calculate_ageing_in_hours(diff)
                else :
                    ageing = diff.days

            if type(ageing) is int :
                ageing = " %s Day(s)" % ageing

            status = core.COMPLIANCE_STATUS("Not Complied")
            name = "%s-%s" % (r["document_name"], r["compliance_task"])
            compliance = dashboard.Level1Compliance(
                name, r["compliance_description"], r["employee_name"],
                str(r["start_date"]), str(due_date),
                str(completion_date), status,
                str(ageing)
            )

            drill_down_data = unit_wise_data.get(unit_id)
            if drill_down_data is None :
                level_compliance = {}
                level_compliance[level_1] = [compliance]
                unit_name = "%s-%s" % (r["unit_code"], r["unit_name"])
                geography = r["geography"].split(">>")
                geography.reverse()
                geography = ','.join(geography)
                address = "%s, %s, %s" % (r["address"], geography, r["postal_code"])
                drill_down_data = dashboard.DrillDownData(
                    r["business_group_name"], r["legal_entity_name"],
                    r["division_name"], unit_name, address,
                    r["industry_name"],
                    level_compliance
                )

            else :
                level_compliance = drill_down_data.compliances
                compliance_list = level_compliance.get(level_1)
                if compliance_list is None :
                    compliance_list = []
                compliance_list.append(compliance)

                level_compliance[level_1] = compliance_list
                drill_down_data.compliances = level_compliance

            unit_wise_data[unit_id] = drill_down_data

        return unit_wise_data

    # assigneewise compliance report
    def report_assigneewise_compliance(
        self, country_id, domain_id, business_group_id,
        legal_entity_id, division_id, unit_id, assignee,
        session_user, from_count, to_count
    ):
        columns = [
            "country_id", "unit_id", "compliance_id", "statutory_dates",
            "trigger_before_days", "due_date", "validity_date",
            "compliance_task", "document_name", "description", "frequency_id",
            "assignee_name", "concurrence_name", "approval_name",
            "assignee", "concurrance", "approval",
            "business_group", "legal_entity", "division",
            "unit_code", "unit_name", "frequency",
            "duration_type", "repeat_type", "duration",
            "repeat_every"
        ]
        qry_where = ""
        admin_id = self.get_admin_id()
        if business_group_id is not None :
            qry_where += " AND u.business_group_id = %s " % (business_group_id)
        if legal_entity_id is not None :
            qry_where += " AND u.legal_entity_id = %s " % (legal_entity_id)
        if division_id is not None :
            qry_where += " AND u.division_id = %s " % (division_id)
        if unit_id is not None :
            qry_where += " AND u.unit_id = %s" % (unit_id)
        if assignee is not None :
            qry_where += " AND ac.assignee = %s" % (assignee)
        if session_user > 0 and session_user != admin_id :
            qry_where += " AND u.unit_id in \
                (select us.unit_id from tbl_user_units us where \
                    us.user_id = %s\
                )" % int(session_user)

        q_count = " SELECT  \
            count(ac.compliance_id) \
        FROM tbl_assigned_compliances ac \
            INNER JOIN tbl_units u on ac.unit_id = u.unit_id \
            INNER JOIN tbl_compliances c on ac.compliance_id = c.compliance_id \
            WHERE c.is_active = 1 \
            and ac.country_id = %s and c.domain_id = %s \
            %s \
        " % (
            country_id, domain_id,
            qry_where
        )
        row = self.select_one(q_count)
        if row :
            count = row[0]
        else :
            count = 0


        q = " SELECT  \
            ac.country_id, ac.unit_id, ac.compliance_id, ac.statutory_dates ,\
            ac. trigger_before_days, ac.due_date, ac.validity_date, \
            c.compliance_task, c.document_name, c.compliance_description, c.frequency_id, \
            IFNULL((select concat(a.employee_code, ' - ', a.employee_name) from tbl_users a \
                where a.user_id = ac.assignee \
            ), 'Administrator') assignee_name, \
            (select concat(a.employee_code, ' - ', a.employee_name) from tbl_users a  \
                where a.user_id = ac.concurrence_person \
            ) concurrence_name, \
            IFNULL((select concat(a.employee_code, ' - ', a.employee_name) from tbl_users a  \
                where a.user_id = ac.approval_person \
            ), 'Administrator') approval_name,  \
            ac.assignee, ac.concurrence_person, ac.approval_person, \
            (select b.business_group_name from tbl_business_groups b \
                where b.business_group_id = u.business_group_id \
            )business_group_name, \
            (select l.legal_entity_name from tbl_legal_entities l \
                where l.legal_entity_id = u.legal_entity_id \
            )legal_entity_name, \
            (select d.division_name from tbl_divisions d \
                where d.division_id = u.division_id \
            )business_group_name, \
            u.unit_code, u.unit_name, \
            (select f.frequency from tbl_compliance_frequency f where f.frequency_id = c.frequency_id) frequency, \
            (select duration_type from tbl_compliance_duration_type where duration_type_id = c.duration_type_id) AS duration_type, \
            (select repeat_type from tbl_compliance_repeat_type where repeat_type_id = c.repeats_type_id) AS repeat_type, \
            c.duration, c.repeats_every \
        FROM tbl_assigned_compliances ac \
            INNER JOIN tbl_units u on ac.unit_id = u.unit_id \
            INNER JOIN tbl_compliances c on ac.compliance_id = c.compliance_id \
            WHERE c.is_active = 1 \
            and ac.country_id = %s and c.domain_id = %s \
            %s \
        ORDER BY u.legal_entity_id, ac.assignee, u.unit_id \
        limit %s, %s" % (
            country_id, domain_id,
            qry_where, from_count, to_count
        )

        rows = self.select_all(q)
        data = self.convert_to_dict(rows, columns)
        return data, count

    def return_assignee_report_data(self, data):
        legal_wise = {}
        for d in data :
            statutory_dates = json.loads(d["statutory_dates"])
            date_list = []
            for date in statutory_dates :
                s_date = core.StatutoryDate(
                    date["statutory_date"],
                    date["statutory_month"],
                    date["trigger_before_days"],
                    date.get("repeat_by")
                )
                date_list.append(s_date)

            compliance_frequency = core.COMPLIANCE_FREQUENCY(
                d["frequency"]
            )

            due_date = None
            if(d["due_date"] is not None):
                due_date = self.datetime_to_string(d["due_date"])

            validity_date = None
            if(d["validity_date"] is not None):
                validity_date = self.datetime_to_string(d["validity_date"])

            if d["frequency_id"] in (2, 3) :
                summary = "Repeats every %s - %s" % (d["repeat_every"], d["repeat_type"])
            elif d["frequency_id"] == 4 :
                summary = "To complete within %s - %s" % (d["duration"], d["duration_type"])
            else :
                summary = None

            if d["document_name"] in ["None", None, ""] :
                name = d["compliance_task"]
            else :
                name = d["document_name"] + " - " + d["compliance_task"]
            compliance = clientreport.ComplianceUnit(
                name, d["unit_code"] + " - " + d["unit_name"],
                compliance_frequency, d["description"],
                date_list, due_date, validity_date,
                summary
            )
            user_wise_compliance = clientreport.UserWiseCompliance(
                d["assignee_name"], d["concurrence_name"],
                d["approval_name"], [compliance]
            )
            group_by_legal = legal_wise.get(d["legal_entity"])
            if group_by_legal is None :
                AC = clientreport.AssigneeCompliance(
                    d["business_group"], d["legal_entity"],
                    d["division"], [user_wise_compliance]
                )
                AC.to_structure()
                legal_wise[d["legal_entity"]] = AC
            else :
                user_wise_list = group_by_legal.user_wise_compliance
                if user_wise_list is None :
                    user_wise_list = []
                    user_wise_list.append(user_wise_compliance)
                else :
                    is_added = False
                    for u in user_wise_list :
                        if (
                            d["assignee_name"] == u.assignee and
                            d["concurrence_name"] == u.concurrence_person and
                            d["approval_name"] == u.approval_person
                        ):
                            lst = u.compliances
                            if lst is None :
                                lst = []
                            lst.append(compliance)
                            u.complaince = lst
                            is_added = True
                    if is_added is False:
                        user_wise_list.append(user_wise_compliance)

                group_by_legal.user_wise_compliance = user_wise_list
                legal_wise[d["legal_entity"]] = group_by_legal
        return legal_wise.values()

    def report_unitwise_compliance(
        self, country_id, domain_id, business_group_id,
        legal_entity_id, division_id, unit_id, assignee,
        session_user, from_count, to_count
    ):
        data, total = self.report_assigneewise_compliance(
            country_id, domain_id, business_group_id,
            legal_entity_id, division_id, unit_id, assignee,
            session_user, from_count, to_count
        )
        return data, total

    def return_unitwise_report(self, data):
        legal_wise = {}
        for d in data :
            statutory_dates = json.loads(d["statutory_dates"])
            date_list = []
            for date in statutory_dates :
                s_date = core.StatutoryDate(
                    date["statutory_date"],
                    date["statutory_month"],
                    date["trigger_before_days"],
                    date.get("repeat_by")
                )
                date_list.append(s_date)

            compliance_frequency = core.COMPLIANCE_FREQUENCY(
                d["frequency"]
            )

            due_date = None
            if(d["due_date"] is not None):
                due_date = self.datetime_to_string(d["due_date"])

            validity_date = None
            if(d["validity_date"] is not None):
                validity_date = self.datetime_to_string(d["validity_date"])

            if d["frequency_id"] in (2, 3) :
                summary = "Repeats every %s - %s" % (d["repeat_every"], d["repeat_type"])
            elif d["frequency_id"] == 4 :
                summary = "To complete within %s - %s" % (d["duration"], d["duration_type"])
            else :
                summary = None

            if d["document_name"] in ["None", None, ""] :
                name = d["compliance_task"]
            else :
                name = d["document_name"] + " - " + d["compliance_task"]
            uname = d["unit_code"] + " - " + d["unit_name"]
            compliance = clientreport.ComplianceUnit(
                name, uname,
                compliance_frequency, d["description"],
                date_list, due_date, validity_date,
                summary
            )

            group_by_legal = legal_wise.get(d["legal_entity"])
            if group_by_legal is None :
                unit_wise = {}
                unit_wise[uname] = [compliance]
                AC = clientreport.UnitCompliance(
                    d["business_group"], d["legal_entity"],
                    d["division"], unit_wise
                )
                AC.to_structure()
                legal_wise[d["legal_entity"]] = AC
            else :
                unit_wise_list = group_by_legal.unit_wise_compliances
                if unit_wise_list is None :
                    unit_wise_list = {}
                    unit_wise_list[uname] = [compliance]
                else :
                    lst = unit_wise_list.get(uname)
                    if lst is None :
                        lst = []
                    lst.append(compliance)
                    unit_wise_list[uname] = lst

                group_by_legal.unit_wise_compliances = unit_wise_list
                legal_wise[d["legal_entity"]] = group_by_legal
        return legal_wise.values()

#
# Compliance Applicability Chart
#

    def get_compliance_applicability_chart(
        self, request, session_user, client_id
    ):
        query = "SELECT T1.compliance_id, \
            T1.statutory_applicable, T1.statutory_opted, \
            T1.not_applicable_remarks, \
            T1.compliance_applicable, T1.compliance_opted, \
            T1.compliance_remarks \
            FROM tbl_client_compliances T1 \
            INNER JOIN tbl_client_statutories T2 \
            ON T1.client_statutory_id = T2.client_statutory_id \
            INNER JOIN tbl_units T3 \
            ON T2.unit_id = T3.unit_id \
            WHERE T2.country_id IN %s \
            AND T2.domain_id IN %s \
            %s "

        country_ids = request.country_ids
        if len(country_ids) == 1 :
            country_ids.append(0)
        domain_ids = request.domain_ids
        if len(domain_ids) == 1:
            domain_ids.append(0)
        filter_type = request.filter_type
        filter_id = request.filter_ids
        if len(filter_id) == 1:
            filter_id.append(0)
        filter_type_qry = ""
        if filter_type == "Group" :
            # filter_type_qry = "AND T3.country_id
            # IN %s" % (str(tuple(filter_ids)))
            pass

        elif filter_type == "BusinessGroup" :
            filter_type_qry = "AND T3.business_group_id IN %s" % str(tuple(filter_id))

        elif filter_type == "LegalEntity" :
            filter_type_qry = "AND T3.legal_entity_id IN %s" % str(tuple(filter_id))

        elif filter_type == "Division" :
            filter_type_qry = "AND T3.division_id IN %s" % str(tuple(filter_id))

        elif filter_type == "Unit":
            filter_type_qry = "AND T3.unit_id IN %s" % str(tuple(filter_id))

        query1 = query % (
            str(tuple(country_ids)),
            str(tuple(domain_ids)),
            filter_type_qry
        )
        rows = self.select_all(query1)

        columns = [
            "compliance_id", "statutory_applicable",
            "statutory_opted", "not_applicable_remarks",
            "compliance_applicable", "compliance_opted",
            "compliance_remarks"
        ]
        result = self.convert_to_dict(rows, columns)

        applicable_count = 0
        not_applicable_count = 0
        not_opted_count = 0

        for r in result :
            if r["compliance_opted"] == 1 :
                applicable_count += 1
            elif r["compliance_opted"] == 0 :
                if r["compliance_applicable"] == 0 :
                    not_applicable_count += 1
                else :
                    not_opted_count += 1

        return dashboard.GetComplianceApplicabilityStatusChartSuccess(
            applicable_count, not_applicable_count, not_opted_count
        )

    def get_compliance_applicability_drill_down(
        self, request, session_user, client_id, from_count, to_count
    ):
        query = "SELECT T1.compliance_id, T2.unit_id, T4.frequency_id, \
            (select frequency from tbl_compliance_frequency where frequency_id = T4.frequency_id) frequency,\
            (select repeat_type from tbl_compliance_repeat_type where repeat_type_id = T4.repeats_type_id) repeats_type, \
            (select duration_type from tbl_compliance_duration_type where duration_type_id = T4.duration_type_id)duration_type,\
            T4.statutory_mapping, T4.statutory_provision,\
            T4.compliance_task, T4.compliance_description,  \
            T4.document_name, T4.format_file, T4.format_file_size, T4.penal_consequences, \
            T4.statutory_dates, T4.repeats_every, T4.duration, T4.is_active, \
            (select group_concat(unit_code, ' - ', unit_name) from tbl_units where unit_id =  T3.unit_id)\
            FROM tbl_client_compliances T1 \
            INNER JOIN tbl_client_statutories T2 \
            ON T2.client_statutory_id = T1.client_statutory_id \
            INNER JOIN tbl_units T3 \
            ON T3.unit_id = T2.unit_id \
            INNER JOIN tbl_compliances T4\
            ON T4.compliance_id = T1.compliance_id\
            WHERE T2.country_id IN %s \
            AND T2.domain_id IN %s \
            %s %s \
            limit %s, %s "

        country_ids = request.country_ids
        if len(country_ids) == 1:
            country_ids.append(0)
        domain_ids = request.domain_ids
        if len(domain_ids) == 1:
            domain_ids.append(0)
        filter_type = request.filter_type
        filter_id = request.filter_ids
        if len(filter_id) == 1 :
            filter_id.append(0)
        applicability = request.applicability_status

        if filter_type == "Group" :
            # filter_type_qry = "AND T3.country_id
            # IN %s" % (str(tuple(filter_ids)))
            filter_type_qry = ""

        elif filter_type == "BusinessGroup" :
            filter_type_qry = "AND T3.business_group_id IN %s" % str(tuple(filter_id))

        elif filter_type == "LegalEntity" :
            filter_type_qry = "AND T3.legal_entity_id IN %s" % str(tuple(filter_id))

        elif filter_type == "Division" :
            filter_type_qry = "AND T3.division_id IN %s" % str(tuple(filter_id))

        elif filter_type == "Unit":
            filter_type_qry = "AND T3.unit_id IN %s" % str(tuple(filter_id))

        applicable_type_qry = ""

        if applicability == "Applicable" :
            applicable_type_qry = "AND T1.compliance_opted = 1"
        elif applicability == "NotApplicable" :
            applicable_type_qry = "AND T1.compliance_opted = 0 \
                AND T1.compliance_applicable = 0"
        elif applicability == "NotOpted" :
            applicable_type_qry = "AND T1.compliance_opted = 0"

        query1 = query % (
            str(tuple(country_ids)),
            str(tuple(domain_ids)),
            filter_type_qry,
            applicable_type_qry,
            from_count, to_count
        )
        rows = self.select_all(query1)
        columns = [
            "compliance_id", "unit_id", "frequency_id",
            "frequency", "repeats_type", "duration_type",
            "statutory_mapping", "statutory_provision", "compliance_task",
            "compliance_description", "document_name", "format_file",
            "format_file_size", "penal_consequences", "statutory_dates",
            "repeats_every", "duration", "is_active", "unit_name"
        ]
        result = self.convert_to_dict(rows, columns)

        level_1_wise_compliance = {}

        for r in result :
            unit_name = r["unit_name"]
            mappings = r["statutory_mapping"].split(">>")
            if len(mappings) >= 1 :
                level_1 = mappings[0]
            else :
                level_1 = mappings

            level_1 = level_1.strip()

            statutory_dates = json.loads(r["statutory_dates"])
            date_list = []
            for s in statutory_dates :
                s_date = core.StatutoryDate(
                    s["statutory_date"], s["statutory_month"],
                    s["trigger_before_days"],
                    s.get("repeat_by")
                )
                date_list.append(s_date)

            format_file = r["format_file"]
            format_file_size = r["format_file_size"]
            file_list = None
            download_file_list = None
            if format_file is not None and format_file_size is not None :
                if len(format_file) != 0 :
                    file_list = []
                    download_file_list = []
                    file_info = core.FileList(
                        int(format_file_size), format_file, None
                    )
                    file_list.append(file_info)
                    # file_name = format_file.split('-')[0]
                    file_download = "%s/%s" % (
                        FORMAT_DOWNLOAD_URL, format_file
                    )
                    download_file_list.append(
                            file_download
                        )

            if int(r["frequency_id"]) == 1 :
                summary = None
            elif int(r["frequency_id"]) in (2, 3) :
                summary = "Repeats every %s %s " % (r["repeats_every"], r["repeats_type"])
            else :
                summary = "To complete with in %s %s " % (r["duration"], r["duration_type"])

            compliance = dashboard.Compliance(
                int(r["compliance_id"]), r["statutory_provision"],
                r["compliance_task"], r["compliance_description"],
                r["document_name"], file_list, r["penal_consequences"],
                r["frequency"], date_list, bool(r["is_active"]),
                download_file_list, summary
            )
            level_1_wise_data = level_1_wise_compliance.get(level_1)
            if level_1_wise_data is None :
                compliance_dict = {}
                compliance_list = [compliance]
                compliance_dict[unit_name] = compliance_list
                level_1_wise_data = dashboard.ApplicableDrillDown(
                    level_1, compliance_dict
                )
            else :
                compliance_dict = level_1_wise_data.compliances
                compliance_list = compliance_dict.get(unit_name)
                if compliance_list is None :
                    compliance_list = []
                compliance_list.append(compliance)

                compliance_dict[unit_name] = compliance_list
                level_1_wise_data.compliances = compliance_dict

            level_1_wise_compliance[level_1] = level_1_wise_data

        return level_1_wise_compliance.values()

#
#   Compliance Approval
#
    def approve_compliance(
        self, compliance_history_id, remarks, next_due_date,
        validity_date, client_id
    ):
        # Updating approval in compliance history
        columns = ["approve_status", "approved_on"]
        condition = "compliance_history_id = '%d'" % compliance_history_id
        values = [1, self.get_date_time()]
        if remarks is not None:
            columns.append("remarks")
            values.append(remarks)
        if next_due_date is not None:
            columns.append("next_due_date")
            values.append(self.string_to_datetime(next_due_date))
        self.update(self.tblComplianceHistory, columns, values, condition, client_id)

        # Getting compliance details from compliance history
        query = '''
            SELECT tch.unit_id, tch.compliance_id,
            (SELECT frequency_id FROM %s tc WHERE tch.compliance_id = tc.compliance_id ),
            due_date, completion_date
            FROM %s tch
            WHERE compliance_history_id = '%d'
        ''' % (
            self.tblCompliances, self.tblComplianceHistory, compliance_history_id
        )
        rows = self.select_all(query)
        columns = ["unit_id", "compliance_id", "frequency_id", "due_date", "completion_date"]
        rows = self.convert_to_dict(rows, columns)

        unit_id = rows[0]["unit_id"]
        compliance_id = rows[0]["compliance_id"]
        due_date = rows[0]["due_date"]
        completion_date = rows[0]["completion_date"]
        frequency_id = rows[0]["frequency_id"]

        # Updating next due date validity dates in assign compliance table
        as_columns = []
        as_values = []
        as_condition = " unit_id = '%d' and compliance_id = '%d'" % (
                unit_id, compliance_id
        )
        if next_due_date is not None:
            as_columns.append("due_date")
            as_values.append(self.string_to_datetime(next_due_date))
        if validity_date is not None:
            as_columns.append("validity_date")
            as_values.append(self.string_to_datetime(validity_date))
        if frequency_id in (1, "1"):
            as_columns.append("is_active")
            as_values.append(0)
        if len(as_columns) > 0 and len(as_values) > 0 and len(as_columns) == len(as_values):
            self.update(
                self.tblAssignedCompliances, as_columns, as_values, as_condition,
                client_id
            )
        status = "Complied"
        if due_date < completion_date:
            status = "Delayed Compliance"

        # Saving in compliance activity
        ageing, remarks = self.calculate_ageing(
            due_date, frequency_type=frequency_id, completion_date=completion_date, duration_type=None
        )
        self.save_compliance_activity(
            unit_id, compliance_id, "Approved", status,
            remarks
        )


        self.notify_compliance_approved(compliance_history_id, "Approved")
        return True

    def notify_compliance_approved(
        self, compliance_history_id, approval_status
    ):
        assignee_id, concurrence_id, approver_id, compliance_name, document_name, due_date = self.get_compliance_history_details(
            compliance_history_id
        )
        if document_name is not None and document_name != '' and document_name != 'None':
            compliance_name = "%s - %s" % (document_name, compliance_name)
        assignee_email, assignee_name = self.get_user_email_name(str(assignee_id))
        approver_email, approver_name = self.get_user_email_name(str(approver_id))
        concurrence_email, concurrence_name = (None, None)
        if concurrence_id not in [None, "None", 0, "", "null", "Null"] and self.is_two_levels_of_approval():
            concurrence_email, concurrence_name = self.get_user_email_name(str(concurrence_id))
            if approval_status == "Approved":
                notification_text = "Compliance %s, completed by %s and concurred by you \
                has approved by %s" % (
                    compliance_name, assignee_name, approver_name
                )
                self.save_compliance_notification(
                    compliance_history_id, notification_text, "Compliance Approved",
                    "ApprovedToConcur"
                )
            else:
                notification_text = "Compliance %s,has completed by %s and concurred by %s \
                Review and approve" % (
                    compliance_name, assignee_name, concurrence_name
                )
                self.save_compliance_notification(
                    compliance_history_id, notification_text, "Compliance Concurred",
                    "Approve"
                )

        who_approved = approver_name if approval_status == "Approved" else concurrence_name
        category = "Compliance Approved" if approval_status == "Approved" else "Compliance Concurred"
        notification_text = "Compliance %s has %s by %s" % (
            compliance_name, approval_status, who_approved
        )
        self.save_compliance_notification(
            compliance_history_id, notification_text, category,
            "ApprovedToAssignee"
        )

        try:
            notify_compliance_approved = threading.Thread(
                target=email.notify_task_approved, args=[
                    approval_status, assignee_name, assignee_email,
                    concurrence_name, concurrence_email, approver_name,
                    approver_email, compliance_name, self.is_two_levels_of_approval()
                ]
            )
            notify_compliance_approved.start()
            return True
        except Exception, e:
            logger.logClient("error", "clientdatabase.py-notifycomplianceapproved", e)
            print "Error while sending email : {}".format(e)

    def reject_compliance_approval(self, compliance_history_id, remarks,
        next_due_date, client_id):
        columns = "unit_id, ch.compliance_id, due_date, completion_date, completed_by,\
        concurred_by, approved_by, \
        (SELECT concat(IFNULL(document_name,''),'-',compliance_task) FROM tbl_compliances tc\
        WHERE tc.compliance_id = ch.compliance_id)"
        condition = "compliance_history_id = '%d'" % compliance_history_id
        rows = self.get_data(
            self.tblComplianceHistory+ " ch", columns, condition
        )
        columns = ["unit_id", "compliance_id", "due_date", "completion_date",
        "assignee_id", "concurrence_id", "approval_id", "compliance_name"]
        rows = self.convert_to_dict(rows, columns)
        unit_id = rows[0]["unit_id"]
        compliance_id = rows[0]["compliance_id"]
        due_date = rows[0]["due_date"]
        completion_date = rows[0]["completion_date"]
        status = "Inprogress"

        if due_date is not None:
            if due_date < completion_date:
                status = "Not Complied"

        ageing, ageing_remarks = self.calculate_ageing(
            due_date, frequency_type=None, completion_date=completion_date, duration_type=None
        )
        self.save_compliance_activity(
            unit_id, compliance_id, "Rejected", status,
            ageing_remarks
        )

        columns = ["approve_status", "remarks", "completion_date", "completed_on",
        "concurred_on", "concurrence_status"]
        condition = "compliance_history_id = '%d'" % compliance_history_id
        values = [0, remarks, None, None, None, None]
        self.update(self.tblComplianceHistory, columns, values, condition, client_id)
        self.notify_compliance_rejected(
            compliance_history_id, remarks, "RejectApproval", rows[0]["assignee_id"],
            rows[0]["concurrence_id"], rows[0]["approval_id"], rows[0]["compliance_name"],
            due_date
        )
        return True

    def notify_compliance_rejected(
        self,  compliance_history_id, remarks, reject_status, assignee_id,
        concurrence_id,  approver_id, compliance_name, due_date
    ):
        assignee_email, assignee_name = self.get_user_email_name(str(assignee_id))
        approver_email, approver_name = self.get_user_email_name(str(approver_id))
        concurrence_email, concurrence_name = (None, None)
        if concurrence_id not in [None, "None", "", "null", "Null", 0] and self.is_two_levels_of_approval():
            concurrence_email, concurrence_name = self.get_user_email_name(str(concurrence_id))
            if reject_status == "RejectApproval":
                notification_text = "Compliance %s, completed by %s and concurred by you \
                has rejected by %s" % (
                    compliance_name, assignee_name, approver_name
                )
                self.save_compliance_notification(
                    compliance_history_id, notification_text, "Compliance Approved",
                    "ApproveRejectedToConcur"
                )

        who_rejected = approver_name if reject_status == "RejectApproval" else concurrence_name
        category = "Compliance Approval Rejected" if reject_status == "RejectApproval" else "Compliance Concurrence Rejected"
        notification_text = "Compliance %s has rejected by %s. the reason is %s" % (
            compliance_name, who_rejected, remarks
        )
        action = "ApproveRejectedToAssignee" if reject_status == "RejectApproval" else "ConcurRejected"
        self.save_compliance_notification(
            compliance_history_id, notification_text, category,
            action
        )
        try:
            notify_compliance_rejected_thread = threading.Thread(
                target=email.notify_task_rejected, args=[
                    compliance_history_id, remarks, reject_status,
                    assignee_name, assignee_email, concurrence_email,
                    concurrence_name, compliance_name
                ]
            )
            notify_compliance_rejected_thread.start()
            return True
        except Exception, e:
            logger.logClient("error", "clientdatabase.py-notify-compliance", e)
            print "Error while sending email : {}".format(e)

    def concur_compliance(
        self, compliance_history_id, remarks,
        next_due_date, validity_date, client_id
    ):
        columns = ["concurrence_status", "concurred_on"]
        condition = "compliance_history_id = '%d'" % compliance_history_id
        values = [1, self.get_date_time()]
        if validity_date is not None:
            columns.append("validity_date")
            values.append(self.string_to_datetime(validity_date))
        if next_due_date is not None:
            columns.append("next_due_date")
            values.append(self.string_to_datetime(next_due_date))
        if remarks is not None:
            columns.append("remarks")
            values.append(remarks)
        self.update(self.tblComplianceHistory, columns, values, condition, client_id)

        columns = "unit_id, compliance_id, due_date, completion_date"
        condition = "compliance_history_id = '%d'" % compliance_history_id
        rows = self.get_data(
            self.tblComplianceHistory, columns, condition
        )
        unit_id = rows[0][0]
        compliance_id = rows[0][1]
        due_date = rows[0][2]
        completion_date = rows[0][3]

        columns = []
        values = []
        if validity_date is not None:
            columns.append("validity_date")
            values.append(self.string_to_datetime(validity_date))
        if next_due_date is not None:
            columns.append("due_date")
            values.append(self.string_to_datetime(next_due_date))
        if len(columns) > 0:
            condition = "compliance_id = '%d' AND unit_id = '%d'" % (compliance_id, unit_id)
            self.update(self.tblAssignedCompliances, columns, values, condition, client_id)

        status = "Inprogress"
        # due_date = datetime.datetime(
        #     int(due_date_parts[0]), int(due_date_parts[1]), int(due_date_parts[2])
        # )
        if due_date < completion_date:
            status = "Not Complied"
        ageing, remarks = self.calculate_ageing(
            due_date, frequency_type=None, completion_date=completion_date, duration_type=None
        )
        self.save_compliance_activity(
            unit_id, compliance_id, "Concurred", status,
            remarks
        )
        self.notify_compliance_approved(compliance_history_id, "Concurred")
        return True

    def reject_compliance_concurrence(self, compliance_history_id, remarks,
        next_due_date, client_id):
        columns = "unit_id, ch.compliance_id, due_date, completion_date, completed_by,\
        concurred_by, approved_by, \
        (SELECT concat(IFNULL(document_name,''),'-',compliance_task) FROM tbl_compliances tc\
        WHERE tc.compliance_id = ch.compliance_id)"
        condition = "compliance_history_id = '%d'" % compliance_history_id
        # columns = "unit_id, compliance_id, due_date, completion_date"
        # condition = "compliance_history_id = '%d'" % compliance_history_id
        rows = self.get_data(
            self.tblComplianceHistory+ " ch", columns, condition
        )
        columns = ["unit_id", "compliance_id", "due_date", "completion_date",
        "assignee_id", "concurrence_id", "approval_id", "compliance_name"]
        rows = self.convert_to_dict(rows, columns)
        unit_id = rows[0]["unit_id"]
        compliance_id = rows[0]["compliance_id"]
        due_date = rows[0]["due_date"]
        completion_date = rows[0]["completion_date"]
        status = "Inprogress"
        if due_date < completion_date:
            status = "Not Complied"
        ageing, ageing_remarks = self.calculate_ageing(
            due_date, frequency_type=None, completion_date=completion_date, duration_type=None
        )
        self.save_compliance_activity(
            unit_id, compliance_id, "Rejected", status,
            ageing_remarks
        )
        columns = ["concurrence_status", "remarks", "completion_date", "completed_on"]
        condition = "compliance_history_id = '%d'" % compliance_history_id
        values = [0,  remarks, None, None]
        self.update(self.tblComplianceHistory, columns, values, condition, client_id)
        self.notify_compliance_rejected(
            compliance_history_id, remarks, "RejectConcurrence", rows[0]["assignee_id"],
            rows[0]["concurrence_id"], rows[0]["approval_id"], rows[0]["compliance_name"],
            due_date
        )
        return True

    def get_client_level_1_statutoy(self, user_id, client_id=None) :
        query = "SELECT (case when (LEFT(statutory_mapping,INSTR(statutory_mapping,'>>')-1) = '') \
                THEN \
                statutory_mapping \
                ELSE \
                LEFT (statutory_mapping,INSTR(statutory_mapping,'>>')-1) \
                END ) as statutory \
                FROM tbl_compliances GROUP BY statutory"
        rows = self.select_all(query)
        columns = ["statutory"]
        result = self.convert_to_dict(rows, columns)
        return self.return_client_level_1_statutories(result)

    def return_client_level_1_statutories(self, data) :
        results = []
        for d in data :
            results.append(
                d["statutory"]
            )
        return results

    def get_client_compliances(self, user_id, client_id=None) :
        query = "SELECT compliance_id, document_name ,compliance_task \
                FROM tbl_compliances"
        rows = self.select_all(query, client_id)
        columns = ["compliance_id", "document_name", "compliance_name"]
        result = self.convert_to_dict(rows, columns)
        return self.return_client_compliances(result)

    def return_client_compliances(self, data) :
        results = []
        for d in data :
            compliance_name = d["compliance_name"]
            if d["document_name"] not in ["None", None, ""]:
                compliance_name = "%s - %s" % (d["document_name"], compliance_name)
            results.append(core.ComplianceFilter(
                d["compliance_id"], compliance_name
            ))
        return results

    def get_service_provider_user_ids(self, service_provider_id, client_id):
        columns = "group_concat(user_id)"
        condition = " service_provider_id = '%d' and is_service_provider = 1" % service_provider_id
        rows = self.get_data(self.tblUsers, columns, condition)
        return rows[0][0]

    def get_service_provider_user_unit_ids(self, user_ids, client_id):
        columns = "group_concat(unit_id)"
        condition = " user_id in (%s)" % user_ids
        rows = self.get_data(self.tblUserUnits, columns, condition)
        return rows[0][0]

    # serviceproviderwise compliance report
    def report_serviceproviderwise_compliance(
        self, country_id, domain_id, statutory_id, unit_id,
        service_provider_id, session_user, from_count, to_count
    ):
        columns = [
            "country_id", "unit_id", "compliance_id", "statutory_dates",
            "trigger_before_days", "due_date", "validity_date",
            "compliance_task", "document_name", "description", "frequency_id",
            "assignee", "service_provider_id",
            "service_provider_name", "address", "contract_from",
            "contract_to", "contact_person", "contact_no",
            "unit_code", "unit_name", "frequency",
            "duration_type", "repeat_type", "duration",
            "repeat_every"
        ]
        qry_where = ""
        admin_id = self.get_admin_id()

        if unit_id is not None :
            qry_where += " AND u.unit_id = %s" % (unit_id)
        if service_provider_id is not None :
            qry_where += " AND s.service_provider_id = %s" % (service_provider_id)
        if session_user > 0 and session_user != admin_id :
            qry_where += " AND u.unit_id in \
                (select us.unit_id from tbl_user_units us where \
                    us.user_id = %s\
                )" % int(session_user)

        q_count = " SELECT  \
            count(ac.compliance_id) \
        FROM tbl_assigned_compliances ac \
            INNER JOIN tbl_units u on ac.unit_id = u.unit_id \
            INNER JOIN tbl_compliances c on ac.compliance_id = c.compliance_id \
            INNER JOIN tbl_users ur on ur.user_id = ac.assignee and ur.is_service_provider = 1 \
            INNER JOIN tbl_service_providers s on s.service_provider_id = ur.service_provider_id \
            WHERE c.is_active = 1 \
            and ac.country_id = %s and c.domain_id = %s  \
            AND SUBSTRING_INDEX(SUBSTRING_INDEX(c.statutory_mapping, '>>', 1),'>>',- 1) = '%s'\
            %s \
        " % (
            country_id, domain_id, statutory_id,
            qry_where
        )

        row = self.select_one(q_count)
        if row :
            count = row[0]
        else :
            count = 0


        q = " SELECT  \
            ac.country_id, ac.unit_id, ac.compliance_id, ac.statutory_dates ,\
            ac.trigger_before_days, ac.due_date, ac.validity_date, \
            c.compliance_task, c.document_name, c.compliance_description, c.frequency_id, \
            ac.assignee, \
            s.service_provider_id, s.service_provider_name, s.address, s.contract_from, s.contract_to, s.contact_person, s.contact_no,  \
            u.unit_code, u.unit_name, \
            (select f.frequency from tbl_compliance_frequency f where f.frequency_id = c.frequency_id) frequency, \
            (select duration_type from tbl_compliance_duration_type where duration_type_id = c.duration_type_id) AS duration_type, \
            (select repeat_type from tbl_compliance_repeat_type where repeat_type_id = c.repeats_type_id) AS repeat_type, \
            c.duration, c.repeats_every \
        FROM tbl_assigned_compliances ac \
            INNER JOIN tbl_units u on ac.unit_id = u.unit_id \
            INNER JOIN tbl_compliances c on ac.compliance_id = c.compliance_id \
            INNER JOIN tbl_users ur on ur.user_id = ac.assignee and ur.is_service_provider = 1 \
            INNER JOIN tbl_service_providers s on s.service_provider_id = ur.service_provider_id \
            WHERE c.is_active = 1 \
            and ac.country_id = %s and c.domain_id = %s \
            AND SUBSTRING_INDEX(SUBSTRING_INDEX(c.statutory_mapping, '>>', 1),'>>',- 1) = '%s'\
            %s \
        ORDER BY ac.assignee, u.unit_id \
        limit %s, %s" % (
            country_id, domain_id, statutory_id,
            qry_where, from_count, to_count
        )

        rows = self.select_all(q)
        data = self.convert_to_dict(rows, columns)
        return data, count

    def return_serviceprovider_report_data(self, data):
        serviceprovider_wise = {}
        for d in data :
            statutory_dates = json.loads(d["statutory_dates"])
            date_list = []
            for date in statutory_dates :
                s_date = core.StatutoryDate(
                    date["statutory_date"],
                    date["statutory_month"],
                    date["trigger_before_days"],
                    date.get("repeat_by")
                )
                date_list.append(s_date)

            compliance_frequency = core.COMPLIANCE_FREQUENCY(
                d["frequency"]
            )

            due_date = None
            if(d["due_date"] is not None):
                due_date = self.datetime_to_string(d["due_date"])

            validity_date = None
            if(d["validity_date"] is not None):
                validity_date = self.datetime_to_string(d["validity_date"])

            if d["frequency_id"] in (2, 3) :
                summary = "Repeats every %s - %s" % (d["repeat_every"], d["repeat_type"])
            elif d["frequency_id"] == 4 :
                summary = "To complete within %s - %s" % (d["duration"], d["duration_type"])
            else :
                summary = None

            if d["document_name"] in ["None", None, ""] :
                name = d["compliance_task"]
            else :
                name = d["document_name"] + " - " + d["compliance_task"]
            uname = d["unit_code"] + " - " + d["unit_name"]
            compliance = clientreport.ComplianceUnit(
                name, uname,
                compliance_frequency, d["description"],
                date_list, due_date, validity_date,
                summary
            )

            group_by_serviceprovider = serviceprovider_wise.get(d["service_provider_name"])
            if group_by_serviceprovider is None :
                unit_wise = {}
                unit_wise[uname] = [compliance]
                AC = clientreport.ServiceProviderCompliance(
                    d["service_provider_name"], d["address"],
                    self.datetime_to_string(d["contract_from"]),self.datetime_to_string(d["contract_to"]),
                    d["contact_person"], d["contact_no"], unit_wise
                )
                AC.to_structure()
                serviceprovider_wise[d["service_provider_name"]] = AC
            else :
                unit_wise_list = group_by_serviceprovider.unit_wise_compliance
                if unit_wise_list is None :
                    unit_wise_list = {}
                    unit_wise_list[uname] = [compliance]
                else :
                    lst = unit_wise_list.get(uname)
                    if lst is None :
                        lst = []
                    lst.append(compliance)
                    unit_wise_list[uname] = lst

                group_by_serviceprovider.unit_wise_compliances = unit_wise_list
                serviceprovider_wise[d["service_provider_name"]] = group_by_serviceprovider
        return serviceprovider_wise.values()

    def get_compliance_details(
        self, country_id, domain_id, statutory_id,
        qry_where, from_count, to_count    ):
        columns = [
            "compliance_history_id", "document_name",
            "compliance_description", "validity_date",
            "due_date", "completed_by", "status", "assigneename", "documents",
            "completion_date", "compliance_task", "frequency_id", "fname",
            "unit_id", "unit_code", "unit_name", "address"
        ]
        qry = "SELECT \
            distinct ch.compliance_history_id, \
            c.document_name, \
            c.compliance_description, \
            ch.validity_date, \
            ch.due_date, \
            ch.completed_by, \
            ifnull(ch.approve_status, 0) status,\
            (SELECT  \
                    concat(u.employee_code, '-', u.employee_name) \
                FROM \
                    tbl_users u \
                WHERE \
                    u.user_id = ch.completed_by) AS assigneename, \
            ch.documents, \
            ch.completion_date, \
            c.compliance_task, \
            c.frequency_id, \
            (select f.frequency from tbl_compliance_frequency f where f.frequency_id = c.frequency_id) fname, \
            ch.unit_id, ut.unit_code, ut.unit_name, ut.address\
        from \
            tbl_compliance_history ch  \
            inner join  \
            tbl_compliances c on ch.compliance_id = c.compliance_id  \
            inner join  \
            tbl_units ut on ch.unit_id = ut.unit_id \
        where ut.country_id = %s \
                AND c.domain_id = %s \
                AND c.statutory_mapping like '%s' \
                %s \
        order by ch.due_date desc limit %s, %s \
        " % (
            country_id, domain_id,
            str(statutory_id+"%"),
            qry_where, from_count, to_count
        )
        rows = self.select_all(qry)
        result = self.convert_to_dict(rows, columns)
        return result

    def get_compliance_details_total_count(
        self, country_id, domain_id, statutory_id, qry_where
    ):
        qry_count = "SELECT \
            count(distinct ch.compliance_history_id) \
        from \
            tbl_compliance_history ch  \
            inner join  \
            tbl_compliances c on ch.compliance_id = c.compliance_id  \
            inner join  \
            tbl_units ut on ch.unit_id = ut.unit_id \
        where ut.country_id = %s \
                AND c.domain_id = %s \
                AND c.statutory_mapping like '%s' \
                %s \
        order by ch.due_date desc \
         " % (
            country_id, domain_id,
            str(statutory_id+"%"),
            qry_where
        )

        row = self.select_one(qry_count)
        if row :
            total = int(row[0])
        else :
            total = 0
        return total

    def get_where_query_for_compliance_details_report(
        self, country_id, domain_id, statutory_id,
        unit_id, compliance_id, assignee,
        from_date, to_date, compliance_status,
        session_user
    ):
        qry_where = ""
        admin_id = self.get_admin_id()
        if unit_id is not None :
            qry_where += " AND ch.unit_id = %s" % (unit_id)
        if compliance_id is not None :
            qry_where += " AND ch.compliance_id = %s " % (compliance_id)
        if assignee is not None :
            qry_where += " AND ch.completed_by = %s" % (assignee)
        if session_user > 0 and session_user != admin_id :
            qry_where += " AND ch.unit_id in \
                (select us.unit_id from tbl_user_units us where \
                    us.user_id = %s\
                )" % int(session_user)
            qry_where += " and c.domain_id IN \
                (SELECT ud.domain_id FROM tbl_user_domains ud \
                where ud.user_id = %s)" % int(session_user)

        if(compliance_status == 'Complied'):
            c_status = " AND ch.due_date >= ch.completion_date \
                AND IFNULL(ch.approve_status,0) = 1"
        elif(compliance_status == 'Delayed Compliance'):
            c_status = " AND ch.due_date < ch.completion_date \
                AND IFNULL(ch.approve_status,0) = 1"
        elif(compliance_status == 'Inprogress'):
            c_status = " AND ((c.duration_type_id =2 AND ch.due_date >= now()) or (c.duration_type_id != 2 and ch.due_date >= CURDATE())) \
                AND IFNULL(ch.approve_status,0) <> 1"
        elif(compliance_status == 'Not Complied'):
            c_status = " AND ((c.duration_type_id =2 AND ch.due_date < now()) or (c.duration_type_id != 2 and ch.due_date < CURDATE())) \
                AND IFNULL(ch.approve_status,0) <> 1"
        else:
            c_status = ''

        qry_where += c_status

        if from_date is not None and to_date is not None :
            start_date = self.string_to_datetime(from_date)
            end_date = self.string_to_datetime(to_date)
            qry_where += " AND ch.due_date between '%s' and '%s'" % (start_date, end_date)

        else :
            qry_where += " AND MONTH(ch.due_date) >= (SELECT t.period_from FROM tbl_client_configurations t \
                where t.country_id = ut.country_id and t.domain_id = c.domain_id ) \
                AND MONTH(ch.due_date) <= (SELECT t.period_to FROM tbl_client_configurations t \
                where t.country_id = ut.country_id and t.domain_id = c.domain_id )"
        return qry_where

    def report_compliance_details(
        self, client_id, country_id, domain_id, statutory_id,
        unit_id, compliance_id, assignee,
        from_date, to_date, compliance_status,
        session_user, from_count, to_count
    ) :

        qry_where = self.get_where_query_for_compliance_details_report(
            country_id, domain_id, statutory_id,
            unit_id, compliance_id, assignee,
            from_date, to_date, compliance_status,
            session_user
        )

        total = self.get_compliance_details_total_count(
            country_id, domain_id, statutory_id, qry_where
        )

        result = self.get_compliance_details(
            country_id, domain_id, statutory_id,
            qry_where, from_count, to_count
        )

        return self.return_cmopliance_details_report(client_id, compliance_status, result, total)

    def return_cmopliance_details_report(self, client_id, compliance_status, result, total):
        unitWise = {}
        for r in result :
            uname = r["unit_code"] + ' - ' + r["unit_name"]
            if r["document_name"] == "None" :
                compliance_name = r["compliance_task"]
            else :
                compliance_name = r["document_name"] + ' - ' + r["compliance_task"]

            if r["assigneename"] is None :
                assignee = 'Administrator'
            else :
                assignee = r["assigneename"]

            due_date = None
            if(r["due_date"] != None):
                due_date = self.datetime_to_string(r["due_date"])

            validity_date = None
            if(r["validity_date"] != None):
                validity_date = self.datetime_to_string(r["validity_date"])

            documents = [x for x in r["documents"].split(",")] if r["documents"] != None else None
            doc_urls = []
            if documents is not None :
                for d in documents :
                    if d != "" :
                        t = "%s/%s/%s" % (CLIENT_DOCS_DOWNLOAD_URL, str(client_id), str(d))
                        doc_urls.append(t)

            completion_date = None
            if(r["completion_date"] != None):
                completion_date = self.datetime_to_string(r["completion_date"])

            remarks = self.calculate_ageing(r["due_date"], r["fname"], r["completion_date"])[1]

            compliance = clientreport.ComplianceDetails(
                compliance_name, assignee, due_date,
                completion_date, validity_date,
                doc_urls, remarks
            )
            unit_compliance = unitWise.get(uname)
            if unit_compliance is None :
                unit_compliance = clientreport.ComplianceDetailsUnitWise(
                    r["unit_id"], uname, r["address"],
                    [compliance]
                )
            else :
                compliance_lst = unit_compliance.Compliances
                if compliance_lst is None :
                    compliance_lst = []
                compliance_lst.append(compliance)
                unit_compliance.Compliances = compliance_lst
            unitWise[uname] = unit_compliance

        final_lst = []
        for k in sorted(unitWise):
            final_lst.append(unitWise.get(k))

        return final_lst, total

#
#   Trend Chart
#
    def get_client_statutory_ids_and_unit_ids_for_trend_chart(
        self, country_id,
        domain_id, client_id, filter_id=None, filter_type=None
    ):
        columns = "group_concat(client_statutory_id), group_concat(unit_id)"
        condition = "country_id= '%d' and domain_id = '%d'" % (country_id, domain_id)
        condition += " and unit_id in (select unit_id from  tbl_units where "
        if filter_type is not None:
            if filter_type == "BusinessGroup":
                condition += " business_group_id ='%d' and country_id ='%d')" % (
                    filter_id, country_id
                )
            elif filter_type == "LegalEntity":
                condition += " legal_entity_id ='%d' and country_id ='%d')" % (
                    filter_id, country_id
                )
            elif filter_type == "Division":
                condition += " division_id ='%d' and country_id ='%d')" % (
                    filter_id, country_id
                )
            elif filter_type == "Unit":
                condition += " unit_id ='%d' and country_id ='%d')" % (
                    filter_id, country_id
                )
        else:
            condition += " country_id = '%d' )" % (country_id)

        result = self.get_data(
            self.tblClientStatutories, columns, condition
        )
        client_statutory_ids = result[0][0]
        unit_ids = result[0][1]
        return client_statutory_ids, unit_ids

    def get_compliance_history_ids_for_trend_chart(
        self,
        country_id, domain_id, client_id,
        filter_id=None, filter_type=None
    ):
        # Units related to the selected country and domain
        unit_columns = "unit_id"
        unit_condition = "country_id = '%d' " % country_id
        unit_condition += " AND  ( domain_ids LIKE  '%,"+str(domain_id)+",%' "+\
                "or domain_ids LIKE  '%,"+str(domain_id)+"' "+\
                "or domain_ids LIKE  '"+str(domain_id)+",%'"+\
                " or domain_ids LIKE '"+str(domain_id)+"') "

        if filter_type is not None:
            if filter_type == "BusinessGroup":
                unit_condition += " AND business_group_id ='%d' " % (
                    filter_id, country_id
                )
            elif filter_type == "LegalEntity":
                unit_condition += " AND legal_entity_id ='%d' " % (
                    filter_id, country_id
                )
            elif filter_type == "Division":
                unit_condition += " AND division_id ='%d'" % (
                    filter_id, country_id
                )
            elif filter_type == "Unit":
                unit_condition += " AND unit_id ='%d' " % (
                    filter_id
                )
        unit_result_rows = self.get_data(self.tblUnits, unit_columns, unit_condition)
        unit_rows = ()
        for row in unit_result_rows:
            unit_rows += row
        unit_ids = None
        if len(unit_rows) > 0:
            unit_ids = ",".join(str(int(x)) for x in unit_rows)

        # Compliances related to the domain
        compliance_columns = "compliance_id"
        compliance_condition = "domain_id = '{}'".format(domain_id)
        compliance_result_rows = self.get_data(
            self.tblCompliances, compliance_columns, compliance_condition
        )
        compliance_rows = ()
        for row in compliance_result_rows:
            compliance_rows += row
        compliance_ids = None
        if len(compliance_rows) > 0:
            compliance_ids = ",".join(str(int(x)) for x in compliance_rows)

        result = self.get_client_statutory_ids_and_unit_ids_for_trend_chart(
            country_id, domain_id, client_id, filter_id, filter_type
        )
        client_statutory_ids = result[0]

        # Getting compliance history ids for selected country, domain
        compliance_history_ids = None
        if compliance_ids is not None and unit_ids is not None:
            columns = "compliance_history_id"
            condition = "compliance_id in (%s) and unit_id in (%s)" % (
                compliance_ids, unit_ids
            )
            rows = self.get_data(
                self.tblComplianceHistory, columns, condition
            )
            result = ()
            for row in rows:
                result += row
            compliance_history_ids = ",".join(str(x) for x in result)
        return compliance_history_ids, client_statutory_ids, unit_ids

    def get_trend_chart(self, country_ids, domain_ids, client_id):
        years = self.get_last_7_years()
        country_domain_timelines = self.get_country_domain_timelines(
            country_ids, domain_ids, years, client_id)
        chart_data = []
        count_flag = 0
        for country_wise_timeline in country_domain_timelines:
            country_id = country_wise_timeline[0]
            domain_wise_timelines = country_wise_timeline[1]
            year_wise_count = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
            for domain_wise_timeline in domain_wise_timelines:
                domain_id = domain_wise_timeline[0]
                start_end_dates = domain_wise_timeline[1]
                compliance_history_ids, client_statutory_ids, unit_ids = self.get_compliance_history_ids_for_trend_chart(
                    country_id, domain_id, client_id
                )
                if compliance_history_ids not in [None, "None", ""]:
                    for index, dates in enumerate(start_end_dates):
                        columns = "count(*) as total, sum(case when approve_status = 1 then 1 " + \
                            "else 0 end) as complied"
                        condition = "due_date between '{}' and '{}'".format(
                            dates["start_date"], dates["end_date"]
                        )
                        condition += " and compliance_history_id in ({})".format(compliance_history_ids)
                        rows = self.get_data(
                            self.tblComplianceHistory,
                            columns, condition
                        )
                        if len(rows) > 0:
                            row = rows[0]
                            total_compliances = row[0]
                            complied_compliances = row[1] if row[1] != None else 0
                            year_wise_count[index][0] += int(total_compliances) if total_compliances is not None else 0
                            year_wise_count[index][1] += int(complied_compliances) if complied_compliances is not None else 0
            compliance_chart_data = []
            for index, count_of_year in enumerate(year_wise_count):
                count_flag += int(count_of_year[0])
                compliance_chart_data.append(
                    dashboard.CompliedMap(
                        year=years[index],
                        total_compliances=int(count_of_year[0]),
                        complied_compliances_count=int(count_of_year[1])
                    ))
            chart_data.append(dashboard.TrendData(
                filter_id=country_id,
                complied_compliance=compliance_chart_data
            ))
        return years, chart_data, count_flag

    def get_trend_chart_drill_down(
        self, country_ids, domain_ids, filter_ids,
        filter_type, year, client_id
    ):
        # Getting Unit ids
        rows = None
        country_ids = ",".join(str(x) for x in country_ids)
        domain_ids = ",".join(str(x) for x in domain_ids)

        if filter_type == "Group":
            columns = "group_concat(DISTINCT unit_id)"
            condition = "country_id in (%s) and domain_id in (%s)" % (
                country_ids, domain_ids)
            rows = self.get_data(
                self.tblClientStatutories,
                columns, condition
            )
        else:
            columns = "group_concat(DISTINCT tcs.unit_id)"
            tables = [self.tblClientStatutories, self.tblUnits]
            aliases = ["tcs", "tu"]
            join_type = "left join "
            join_conditions = ["tcs.unit_id = tu.unit_id"]
            where_condition = "tu.country_id in (%s) and domain_id in (%s)" % (
                country_ids, domain_ids)
            if filter_type == "BusinessGroup":
                where_condition += " and business_group_id in(%s)" % filter_ids
            elif filter_type == "LegalEntity":
                where_condition += " and legal_entity_id in (%s)" % filter_ids
            elif filter_type == "Division":
                where_condition += " and  division_id in (%s) " % filter_ids
            elif filter_type == "Unit":
                where_condition += " and  tcs.unit_id in (%s) " % filter_ids
            rows = self.get_data_from_multiple_tables(
                columns, tables, aliases,
                join_type, join_conditions,
                where_condition
            )

        if rows:
            unit_ids = [int(x) for x in rows[0][0].split(",")] if rows[0][0] != None else []
        drill_down_data = []
        for unit_id in unit_ids:
            # Getting Unit details
            unit_detail_columns = "tu.country_id, domain_ids, business_group_id, \
            legal_entity_id, division_id, unit_code, unit_name, address"
            unit_detail_condition = "tu.unit_id = '{}'".format(unit_id)
            tables = "%s tu" % (
                self.tblUnits
            )
            unit_rows = self.get_data(
                tables, unit_detail_columns,
                unit_detail_condition,
            )
            unit_detail = unit_rows[0]
            business_group_id = unit_detail[2]
            legal_entity_id = unit_detail[3]
            division_id = unit_detail[4]
            unit_name = "%s-%s" % (
                unit_detail[5], unit_detail[6]
            )
            address = unit_detail[7]

            # Getting complied compliances for the given year
            years = [year]
            country_ids = [unit_detail[0]]
            domain_ids = unit_detail[1].split(",")
            timelines = self.get_country_domain_timelines(
                    country_ids, domain_ids,
                    years, client_id
                )
            domain_wise_timelines = timelines[0][1] if len(timelines) > 0 else []
            for domain_wise_timeline in domain_wise_timelines:
                domain_id = domain_wise_timeline[0]
                start_end_dates = domain_wise_timeline[1][0]
                start_date = start_end_dates["start_date"]
                end_date = start_end_dates["end_date"]

                # Getting compliances relevent to unit, country, domain
                compliance_columns = "group_concat(distinct compliance_id)"
                compliance_condition = "compliance_opted = 1"
                compliance_condition += " and client_statutory_id in (\
                select client_statutory_id from %s where unit_id = '%d' and domain_id = '%d')" % (
                    self.tblClientStatutories, int(unit_id), int(domain_id)
                )
                compliance_rows = self.get_data(
                    self.tblClientCompliances, compliance_columns,
                    compliance_condition
                )
                compliance_ids = compliance_rows[0][0]
                if compliance_ids is not None:
                    history_columns = "tch.compliance_id, tu.employee_code, "
                    history_columns += "tu.employee_name, tc.compliance_task,"
                    history_columns += " tc.compliance_description, "
                    history_columns += " tc.document_name,"
                    history_columns += "tc.compliance_description, "
                    history_columns += "tc.statutory_mapping"
                    history_condition = "due_date between '{}' and '{}'".format(
                        start_date, end_date
                    )
                    history_condition += " and tch.compliance_id in (%s)" % (
                        compliance_ids
                    )
                    history_condition += " and tch.unit_id = '%d'" % (
                        unit_id
                    )
                    tables = [
                        self.tblComplianceHistory,
                        self.tblUsers, self.tblCompliances
                    ]
                    aliases = ["tch", "tu", "tc"]
                    join_type = "left join"
                    join_condition = [
                        "tch.completed_by = tu.user_id",
                        "tch.compliance_id = tc.compliance_id"
                    ]
                    history_rows = self.get_data_from_multiple_tables(
                        history_columns, tables, aliases,
                        join_type, join_condition,
                        history_condition,
                    )
                    level_1_statutory_wise_compliances = {}
                    for history_row in history_rows:
                        assignee_name = "%s-%s" % (history_row[1], history_row[2])
                        compliance_name = "%s-%s" % (
                            history_row[5], history_row[3]
                        )
                        description = history_row[4]
                        statutories = history_row[7].split(">>")
                        level_1_statutory = statutories[0]
                        if level_1_statutory not in level_1_statutory_wise_compliances:
                            level_1_statutory_wise_compliances[level_1_statutory] = []
                        level_1_statutory_wise_compliances[
                            level_1_statutory
                        ].append(dashboard.TrendCompliance(
                            compliance_name, description, assignee_name
                            )
                        )
            if len(level_1_statutory_wise_compliances) > 0:
                business_group_name = None
                legal_entity_name = None
                division_name = None
                if business_group_id is not None:
                    rows = self.get_data(
                        self.tblBusinessGroups, "business_group_name", "business_group_id='%d'" % (business_group_id)
                    )
                    if rows:
                        business_group_name = rows[0][0]
                if division_id is not None:
                    rows = self.get_data(
                        self.tblDivisions, "division_name", "division_id='%d'" % (division_id)
                    )
                    if rows:
                        division_name = rows[0][0]
                rows = self.get_data(
                    self.tblLegalEntities, "legal_entity_name", "legal_entity_id='%d'" % (legal_entity_id)
                )
                if rows:
                    legal_entity_name = rows[0][0]

                drill_down_data.append(
                    dashboard.TrendDrillDownData(
                            business_group_name,
                            legal_entity_name, division_name,
                            unit_name, address,
                            level_1_statutory_wise_compliances
                        )
                    )
        return drill_down_data

    def get_filtered_trend_data(
        self,
        country_ids, domain_ids, filter_type,
        filter_ids, client_id
    ):
        years = self.get_last_7_years()
        country_domain_timelines = self.get_country_domain_timelines(
            country_ids, domain_ids, years, client_id)
        chart_data = []
        count_flag = 0
        for filter_id in filter_ids:
            year_wise_count = [
                [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]
            ]
            for country_wise_timeline in country_domain_timelines:
                country_id = country_wise_timeline[0]
                domain_wise_timelines = country_wise_timeline[1]
                for domain_wise_timeline in domain_wise_timelines:
                    domain_id = domain_wise_timeline[0]
                    start_end_dates = domain_wise_timeline[1]
                    for index, dates in enumerate(start_end_dates):
                        columns = "count(*) as total, sum(case when approve_status is null then 1 " + \
                            "else 0 end) as complied"
                        condition = "due_date between '{}' and '{}'".format(
                            dates["start_date"], dates["end_date"]
                        )
                        compliance_history_ids = self.get_compliance_history_ids_for_trend_chart(
                            country_id, domain_id, client_id, filter_id, filter_type)
                        if compliance_history_ids[0] is not None and compliance_history_ids[2] is not None:
                            condition += " and compliance_history_id in (%s)" % compliance_history_ids[0]
                            condition += " and unit_id in (%s)" % compliance_history_ids[2]
                            rows = self.get_data(
                                self.tblComplianceHistory, columns,
                                condition
                            )
                            if len(rows) > 0:
                                row = rows[0]
                                total_compliances = int(row[0])
                                complied_compliances = int(row[1]) if row[1] != None else 0
                                year_wise_count[index][0] += total_compliances if total_compliances is not None else 0
                                year_wise_count[index][1] += complied_compliances if complied_compliances is not None else 0
            compliance_chart_data = []
            for index, count_of_year in enumerate(year_wise_count):
                count_flag += int(count_of_year[0])
                compliance_chart_data.append(
                    dashboard.CompliedMap(
                        year=years[index],
                        total_compliances=int(count_of_year[0]),
                        complied_compliances_count=int(count_of_year[1])
                    ))
            chart_data.append(dashboard.TrendData(
                filter_id=filter_id,
                complied_compliance=compliance_chart_data
            ))
        return years, chart_data, count_flag

    def get_last_7_years(self):
        seven_years_list = []
        end_year = datetime.datetime.now().year - 1
        start_year = end_year - 5
        iter_value = start_year
        while iter_value <= end_year:
            seven_years_list.append(iter_value)
            iter_value += 1
        return seven_years_list

    def get_country_domain_timelines(
        self, country_ids, domain_ids, years, client_id=None
    ):
        country_wise_timelines = []
        for country_id in country_ids:
            domain_wise_timeline = []
            for domain_id in domain_ids:
                columns = "period_from, period_to"
                condition = "country_id = '{}' and domain_id = '{}'".format(
                    country_id, domain_id)
                rows = self.get_data(
                    self.tblClientConfigurations, columns,
                    condition
                )
                if len(rows) > 0:
                    period_from = rows[0][0]
                    period_to = rows[0][1]
                    start_end_dates = []
                    for year in years:
                        start_year = year
                        end_year = year+1
                        start_date_string = None
                        end_date_string = None
                        start_date_string = "1-{}-{}".format(
                            self.string_months[period_from],
                            start_year
                        )
                        start_date = self.string_to_datetime(start_date_string)
                        end_date_string = "{}-{}-{}".format(
                            self.end_day_of_month[period_to],
                            self.string_months[period_to],
                            end_year
                        )
                        end_date = self.string_to_datetime(end_date_string)
                        r = relativedelta.relativedelta(end_date, start_date)
                        if r.years > 0:
                            end_date = end_date - relativedelta.relativedelta(years=1)
                        start_end_dates.append(
                            {
                                "year" : year,
                                "start_date" : start_date,
                                "end_date" : end_date
                            }
                        )
                    domain_wise_timeline.append(
                        [domain_id, start_end_dates]
                    )
            country_wise_timelines.append([country_id, domain_wise_timeline])
        return country_wise_timelines

#
#   Client Admin Settings
#

    def get_settings(self, client_id):
        columns = "two_levels_of_approval, assignee_reminder, " + \
            "escalation_reminder_in_advance, escalation_reminder," + \
            "contract_from, contract_to, no_of_user_licence, " + \
            "total_disk_space, total_disk_space_used"
        condition = "1"
        rows = self.get_data(
            self.tblClientGroups, columns, condition
        )
        if len(rows) > 0:
            row = rows[0]
            return row
        else:
            return None

    def get_licence_holder_details(self, client_id):
        columns = "tcu.user_id, tcu.email_id, tcu.employee_name, tcu.employee_code," + \
            " tcu.contact_no, tcu.is_admin, tu.unit_code, tu.unit_name, tu.address," + \
            " tcu.is_active, tsp.service_provider_name"
        tables = [self.tblUsers, self.tblUnits, self.tblServiceProviders]
        aliases = ["tcu", "tu", "tsp"]
        join_type = "left join"
        join_conditions = [
            "tcu.seating_unit_id = tu.unit_id",
            "tcu.service_provider_id=tsp.service_provider_id"
        ]
        where_condition = "1"
        return self.get_data_from_multiple_tables(
            columns, tables, aliases,
            join_type, join_conditions,
            where_condition
        )

    def get_profile(
        self, contract_from, contract_to, no_of_user_licence,
        total_disk_space, total_disk_space_used, client_id
    ):
        contract_from = self.datetime_to_string(contract_from)
        contract_to = self.datetime_to_string(contract_to)

        admin_columns = "username"
        admin_condition = "1"
        result = self.get_data(
            self.tblAdmin, admin_columns, admin_condition
        )
        admin_email = result[0][0]
        is_admin_is_a_user = False

        licence_holder_rows = self.get_licence_holder_details(client_id)
        licence_holders = []
        for row in licence_holder_rows:
            employee_name = None
            unit_name = None
            if(row[3] == None):
                employee_name = row[2]
            else:
                employee_name = "%s - %s" % (row[3], row[2])

            if row[7] == None:
                unit_name = row[10]
            else:
                unit_name = "%s - %s" % (row[6], row[7])
            user_id = row[0]
            email_id = row[1]
            if email_id == admin_email:
                is_admin_is_a_user = True
                employee_name = "Administrator: %s" % employee_name
            contact_no = row[4]
            is_admin = row[5]
            address = row[8]
            is_active = row[9]
            licence_holders.append(
                clientadminsettings.LICENCE_HOLDER(
                    user_id, employee_name, email_id, contact_no,
                    unit_name, address
                ))
        remaining_licence = (no_of_user_licence) - len(licence_holder_rows)
        if not is_admin_is_a_user:
            licence_holders.append(
                clientadminsettings.LICENCE_HOLDER(
                    0, "Administrator", admin_email, None,
                    None, None
                ))
            remaining_licence -= 1

        used_space = (total_disk_space_used/1000000000)
        used_space = str(used_space)
        tmp_s = used_space.split(".")
        if len(tmp_s) > 0 :
            val = tmp_s[0] + "." + tmp_s[1][:2]
            used_space = float(val)

        total_space = total_disk_space/1000000000

        profile_detail = clientadminsettings.PROFILE_DETAIL(
            contract_from,
            contract_to,
            no_of_user_licence,
            remaining_licence,
            licence_holders,
            total_space,
            used_space
        )
        return profile_detail

    def updateSettings(
        self, is_two_levels_of_approval, assignee_reminder_days,
        escalation_reminder_In_advance_days, escalation_reminder_days, client_id
    ):
        columns = [
            "two_levels_of_approval", "assignee_reminder",
            "escalation_reminder_in_advance", "escalation_reminder"
        ]
        is_two_levels_of_approval = 1 if is_two_levels_of_approval == True else 0
        values = [
            is_two_levels_of_approval, assignee_reminder_days,
            escalation_reminder_In_advance_days, escalation_reminder_days
        ]
        condition = "1"
        self.update(self.tblClientGroups, columns, values, condition, client_id)

        action = "Settings Updated"
        self.save_activity(0, 25, action)

#
#   Notifications
#

    def get_notifications(
        self, notification_type, start_count, to_count,
        session_user, client_id
    ):
        notification_type_id = None
        if notification_type == "Notification":
            notification_type_id = 1
        elif notification_type == "Reminder":
            notification_type_id = 2
        elif notification_type == "Escalation":
            notification_type_id = 3
        columns = '''nul.notification_id as notification_id, notification_text, created_on, \
            extra_details, statutory_provision, \
            assignee, concurrence_person, approval_person, \
            nl.compliance_id, compliance_task, document_name, \
            compliance_description, penal_consequences, read_status,\
            due_date, completion_date, approve_status'''
        subquery_columns = "(SELECT concat(IFNULL(employee_code, 'Administrator'), '-', employee_name,\
        ',','(' , IFNULL(contact_no, '-'), '-', email_id, ')') FROM %s WHERE user_id = assignee), IF(\
        concurrence_person IS NULL, '', (SELECT concat(IFNULL(employee_code, 'Administrator'), '-', \
        employee_name,',','(' ,  IFNULL(contact_no, '-'), '-', email_id, ')') FROM %s WHERE \
        user_id = concurrence_person)), (SELECT concat(IFNULL(employee_code, 'Administrator'), '-',\
        employee_name,',','(' ,  IFNULL(contact_no, '-'), '-', email_id, ')') FROM %s WHERE \
        user_id = approval_person),\
        (select concat(unit_code, '-', unit_name, ',', address) \
        FROM tbl_units tu WHERE tu.unit_id = nl.unit_id) " % (self.tblUsers, self.tblUsers, self.tblUsers)
        query = " \
                SELECT * FROM (\
                SELECT %s,%s \
                FROM %s nul \
                LEFT JOIN %s nl ON (nul.notification_id = nl.notification_id)\
                LEFT JOIN %s tc ON (tc.compliance_id = nl.compliance_id) \
                LEFT JOIN %s tch ON (tch.compliance_id = nl.compliance_id AND \
                tch.unit_id = nl.unit_id) \
                WHERE notification_type_id = '%s' \
                AND user_id = '%s' \
                AND read_status = 0\
                AND (compliance_history_id is null \
                OR  compliance_history_id = CAST(REPLACE(\
                SUBSTRING_INDEX(extra_details, '-', 1),\
                ' ','') AS UNSIGNED)) \
                LIMIT %s, %s ) as a \
                ORDER BY a.notification_id DESC" % (
                    columns, subquery_columns,
                    self.tblNotificationUserLog,
                    self.tblNotificationsLog,
                    self.tblCompliances,
                    self.tblComplianceHistory,
                    notification_type_id, session_user,
                    start_count, to_count
                )
        rows = self.select_all(query)
        columns_list = [
            "notification_id", "notification_text", "created_on",
            "extra_details", "statutory_provision",
            "assignee", "concurrence_person", "approval_person",
            "compliance_id", "compliance_task", "document_name",
            "compliance_description", "penal_consequences", "read_status",
            "due_date", "completion_date", "approve_status"
        ]
        columns_list += ["assignee_details", "concurrence_details", "approver_details", "unit_details"]
        notifications = self.convert_to_dict(rows, columns_list)
        notifications_list = []
        for notification in notifications:
            notification_id = notification["notification_id"]
            read_status = bool(int(notification["read_status"]))
            extra_details_with_history_id = notification["extra_details"].split("-")
            compliance_history_id = int(extra_details_with_history_id[0])
            extra_details = extra_details_with_history_id[1]
            if compliance_history_id not in [0, "0", None, "None", ""]:
                due_date_as_date = notification["due_date"]
                due_date = self.datetime_to_string_time(due_date_as_date)
                completion_date = notification["completion_date"]
                approve_status = notification["approve_status"]
                delayed_days = "-"
                if completion_date is None or approve_status == 0:
                    no_of_days, delayed_days = self.calculate_ageing(due_date_as_date)
                else:
                    r = relativedelta.relativedelta(due_date_as_date, completion_date)
                    delayed_days = "-"
                    if r.days < 0 and r.hours < 0 and r.minutes < 0:
                        delayed_days = "Overdue by %d days" % abs(r.days)
                if "Overdue" not in delayed_days:
                    delayed_days = "-"
                # diff = self.get_date_time() - due_date_as_datetime
                statutory_provision = notification["statutory_provision"].split(">>")
                level_1_statutory = statutory_provision[0]

                notification_text = notification["notification_text"]
                updated_on = self.datetime_to_string(notification["created_on"])
                unit_details = notification["unit_details"].split(",")
                unit_name = unit_details[0]
                unit_address = unit_details[1]
                assignee = notification["assignee_details"]
                concurrence_person = None if notification["concurrence_details"] in ['', None, "None"] else notification["concurrence_details"]
                approval_person = notification["approver_details"]
                compliance_name = notification["compliance_task"]
                if notification["document_name"] is not None and notification["document_name"].replace(" ", "") != "None":
                    compliance_name = "%s - %s" % (
                        notification["document_name"],
                        notification["compliance_task"]
                    )
                compliance_description = notification["compliance_description"]
                penal_consequences = notification["penal_consequences"]
                due_date = self.datetime_to_string_time(notification["due_date"])
            else:
                penal_consequences = None
                delayed_days = None
                due_date = None
                compliance_description = None
                approval_person = None
                compliance_name = None
                concurrence_person = None
                assignee = None
                unit_name = None
                unit_address = None
                level_1_statutory = None
                extra_details = notification["extra_details"].split("-")[1]
                read_status = bool(0)
                updated_on = self.datetime_to_string(self.get_date_time())
                notification_text = notification["notification_text"]
            notifications_list.append(
                dashboard.Notification(
                    notification_id, read_status, notification_text, extra_details,
                    updated_on, level_1_statutory, unit_name, unit_address, assignee,
                    concurrence_person, approval_person, compliance_name,
                    compliance_description, due_date, delayed_days,
                    penal_consequences
                )
            )
        return notifications_list

    def update_notification_status(self, notification_id, has_read, session_user, client_id):
        columns = ["read_status"]
        values = [1 if has_read is True else 0]
        condition = "notification_id = '%d' and user_id='%d'" % (
            notification_id, session_user)
        self.update(self.tblNotificationUserLog , columns, values, condition, client_id)

#
# ReAssign Compliance
#
    def get_assigneewise_complaince_count(self, session_user):
        admin_id = self.get_admin_id()
        user_qry = ""
        if session_user > 0 and session_user != admin_id :
            user_qry = " AND t01.unit_id in (select distinct unit_id from tbl_user_units where user_id like '%s')" % session_user
            user_qry += " AND t02.domain_id in (select distinct domain_id from tbl_user_domains where user_id like '%s')" % session_user

        q = "SELECT t01.assignee, count( t01.compliance_id ) AS cnt \
                FROM tbl_assigned_compliances t01 \
                INNER JOIN tbl_compliances t02 ON t01.compliance_id = t02.compliance_id \
                LEFT JOIN tbl_compliance_history t03 ON t01.assignee = t03.completed_by \
                AND t01.unit_id = t03.unit_id \
                AND t01.compliance_id = t03.compliance_id \
                AND IFNULL( t03.approve_status, 0 ) !=1 \
                INNER JOIN tbl_client_statutories t04 ON t01.unit_id = t04.unit_id \
                INNER JOIN tbl_client_compliances t05 ON t04.client_statutory_id = t05.client_statutory_id \
                AND t01.compliance_id = t05.compliance_id \
                AND IFNULL(t05.compliance_opted, 0) = 1\
                WHERE \
                %s \
                t02.is_active =1 and t01.is_active = 1 \
                GROUP BY t01.assignee " % (user_qry)

        self.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ;")
        rows = self.select_all(q)
        self.execute("SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ ;")
        result = self.convert_to_dict(rows, columns=["assignee", "count"])
        data = {}
        for r in result :
            data[int(r["assignee"])] = int(r["count"])
        return data

    def get_compliance_for_assignee(self, session_user, assignee, from_count, to_count):
        admin_id = self.get_admin_id()
        result = []
        user_qry = ""
        if session_user > 0 and session_user != admin_id :
            user_qry = " AND t1.unit_id in (select distinct unit_id from tbl_user_units where user_id like '%s')" % session_user
            user_qry = " AND t2.domain_id in (select distinct domain_id from tbl_user_domains where domain_id like '%s')" % session_user

        columns = [
            "compliance_id", "unit_id", "statutory_dates",
            "assignee", "due_date", "validity_date",
            "compliance_task", "document_name",
            "compliance_description", "statutory_mapping",
            "unit_name", "unit_code", "address", "postal_code",
            "frequency", "frequency_id", "duration_type", "duration", "duration_type_id",
            "repeat_type", "repeats_every",
            "compliance_history_id", "current_due_date", "domain_id", "trigger_before_days", "approve_status"
        ]
        q = " SELECT distinct t1.compliance_id, t1.unit_id, t1.statutory_dates, t1.assignee, \
            t1.due_date, t1.validity_date, t2.compliance_task, t2.document_name, \
            t2.compliance_description, t2.statutory_mapping, t3.unit_name, \
            t3.unit_code, t3.address, t3.postal_code, \
            (select frequency from tbl_compliance_frequency where frequency_id = t2.frequency_id) frequency, t2.frequency_id, \
            (select duration_type from tbl_compliance_duration_type where duration_type_id = t2.duration_type_id) duration_type, t2.duration, t2.duration_type_id, \
            (select repeat_type from tbl_compliance_repeat_type where repeat_type_id = t2.repeats_type_id) repeat_type, t2.repeats_every, \
            t4.compliance_history_id, \
            t4.due_date, t2.domain_id, t1.trigger_before_days, \
            IFNULL(t4.approve_status, 0) \
            FROM \
                tbl_assigned_compliances t1 \
                INNER JOIN \
            tbl_compliances t2 ON t1.compliance_id = t2.compliance_id \
                AND t1.is_active = 1 \
                INNER JOIN \
            tbl_units t3 ON t1.unit_id = t3.unit_id \
            LEFT JOIN tbl_compliance_history t4 on \
            t4.unit_id = t1.unit_id \
            and t4.compliance_id = t1.compliance_id and t4.completed_by = t1.assignee \
            INNER JOIN tbl_client_statutories t5 ON t1.unit_id = t5.unit_id \
                INNER JOIN tbl_client_compliances t6 ON t5.client_statutory_id = t6.client_statutory_id \
                AND t1.compliance_id = t6.compliance_id \
                AND IFNULL(t6.compliance_opted, 0) = 1 \
        WHERE \
            t1.assignee = %s %s \
            and t1.is_active = 1  \
        ORDER BY t3.unit_id , t2.statutory_mapping , t2.frequency_id \
        limit %s, %s " % (
            assignee, user_qry,
            from_count, to_count
        )
        self.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ;")
        rows = self.select_all(q)
        self.execute("SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ ;")
        result.extend(self.convert_to_dict(rows, columns))
        return self.return_compliance_to_reassign(result)

    def return_compliance_to_reassign(self, data):
        assignee_compliance_count = {}
        assignee_wise_compliances = {}
        for d in data :
            assignee = d["assignee"]
            unit_id = d["unit_id"]
            mappings = d["statutory_mapping"].split('>>')
            level_1 = mappings[0].strip()
            unit_name = "%s - %s " % (
                d["unit_code"], d["unit_name"]
            )
            address = "%s- %s " % (
                d["address"], d["postal_code"]
            )
            frequency = core.COMPLIANCE_FREQUENCY(d["frequency"])
            compliance_history_id = d["compliance_history_id"]
            if compliance_history_id is not None and d["approve_status"] == "0" :
                compliance_history_id = int(compliance_history_id)
                due_date = d["current_due_date"]
            else :
                compliance_history_id = None
                due_date = d["due_date"]
            if due_date is not None :
                due_date = due_date.strftime("%d-%b-%Y")
            else :
                due_date = ''
            validity_date = d["validity_date"]
            if validity_date is not None :
                validity_date = validity_date.strftime("%d-%b-%Y")
            else :
                validity_date = ''
            statutory_dates = json.loads(d["statutory_dates"])
            date_list = []
            for date in statutory_dates :
                s_date = core.StatutoryDate(
                    date["statutory_date"],
                    date["statutory_month"],
                    date["trigger_before_days"],
                    date.get("repeat_by")
                )
                date_list.append(s_date)
            if d["document_name"] not in (None, "None", "") :
                compliance_name = "%s - %s" % (
                    d["document_name"], d["compliance_task"]
                )
            else :
                compliance_name = d["compliance_task"]
            if d["frequency_id"] in (2, 3) :
                summary = "Repeats every %s - %s" % (d["repeats_every"], d["repeat_type"])
            elif d["frequency_id"] == 4 :
                summary = "To complete within %s - %s" % (d["duration"], d["duration_type"])
                if d["duration_type_id"] == 2 :
                    due_date = d["due_date"]
                    if due_date is not None :
                        due_date = due_date.strftime("%d-%b-%Y %H:%M")
                    else :
                        due_date = ''
            else :
                summary = None

            compliance = clienttransactions.STATUTORYWISECOMPLIANCE(
                compliance_history_id, d["compliance_id"],
                compliance_name,
                d["compliance_description"], frequency,
                date_list, due_date, validity_date,
                summary, int(d["domain_id"]), d["trigger_before_days"]
            )
            assignee_data = assignee_wise_compliances.get(assignee)
            if assignee_data is None :
                assignee_data = {}
                # unit_wise_compliances = {}
                statutories = {}
                statutories[level_1] = [compliance]
                unit_data = clienttransactions.USER_WISE_UNITS(
                    unit_id, unit_name, address, statutories
                )
                count = assignee_compliance_count.get(assignee)
                if count is None :
                    count = 1
                else :
                    count += 1
                assignee_compliance_count[assignee] = count
                assignee_data[unit_id] = unit_data
            else :
                unit_data = assignee_data.get(unit_id)
                if unit_data is None :
                    statutories = {}
                    statutories[level_1] = [compliance]
                    unit_data = clienttransactions.USER_WISE_UNITS(
                        unit_id, unit_name, address, statutories
                    )
                    count = assignee_compliance_count.get(assignee)
                    if count is None :
                        count = 1
                    else :
                        count += 1
                    assignee_compliance_count[assignee] = count
                else :
                    statutories = unit_data.statutories
                    compliance_list = statutories.get(level_1)
                    if compliance_list is None :
                        compliance_list = []
                    compliance_list.append(compliance)
                    statutories[level_1] = compliance_list

                    unit_data.statutories = statutories
                    count = assignee_compliance_count.get(assignee)
                    if count is None :
                        count = 1
                    else :
                        count += 1
                    assignee_compliance_count[assignee] = count
                assignee_data[unit_id] = unit_data

            assignee_wise_compliances[assignee] = assignee_data
        return (
                assignee_wise_compliances, assignee_compliance_count
            )

    def reassign_compliance(self, request, session_user):
        reassigned_from = request.reassigned_from
        assignee = request.assignee
        concurrence = request.concurrence_person
        approval = request.approval_person
        compliances = request.compliances
        reassigned_reason = request.reassigned_reason
        created_on = self.get_date_time()
        reassigned_date = created_on.strftime("%Y-%m-%d")
        created_by = int(session_user)
        new_unit_settings = request.new_units
        compliance_names = []
        compliance_ids = []
        reassing_columns = [
            "unit_id", "compliance_id", "assignee",
            "reassigned_from", "reassigned_date", "remarks",
            "created_by", "created_on"
        ]
        for c in compliances :
            unit_id = c.unit_id
            compliance_id = c.compliance_id
            compliance_ids.append(compliance_id)
            compliance_names.append(c.compliance_name)
            due_date = c.due_date
            if due_date is not None :
                due_date = datetime.datetime.strptime(due_date, "%d-%b-%Y").date()

            history_id = c.compliance_history_id
            values = [
                unit_id, compliance_id, assignee, reassigned_from,
                reassigned_date, reassigned_reason, created_by,
                created_on
            ]
            self.insert(self.tblReassignedCompliancesHistory, reassing_columns, values)

            update_qry = "UPDATE tbl_assigned_compliances SET assignee=%s, is_reassigned=1, approval_person=%s, due_date='%s' "
            if concurrence not in [None, "None", 0, "null", "Null"] :
                update_qry += " ,concurrence_person = %s " % (concurrence)
            where_qry = " WHERE unit_id = %s AND compliance_id = %s "

            qry = update_qry + where_qry

            update_assign = qry % (
                assignee, approval, due_date, unit_id, compliance_id
            )
            self.execute(update_assign)

            if history_id is not None :
                update_history = "UPDATE tbl_compliance_history SET  \
                    completed_by = '%s', approved_by = %s"
                if concurrence not in [None, "None", "null", "Null", 0] :
                    update_history += " ,concurred_by = %s " % (concurrence)
                where_qry = " WHERE IFNULL(approve_status, 0) != 1 and compliance_id = %s  and unit_id = %s "

                qry = update_history + where_qry

                update_history = qry % (
                    assignee, approval, compliance_id,
                    unit_id
                )
                self.execute(update_history)

        if new_unit_settings is not None :
            self.update_user_settings(new_unit_settings)

        compliance_names = " <br> ".join(compliance_names)
        if concurrence is None :
            action = " Following compliances has reassigned to assignee - %s and approval-person - %s <br> %s" % (
                request.assignee_name,
                approval,
                compliance_names
            )
        else :
            action = " Following compliances has reassigned to assignee - %s concurrence-person - %s approval-person - %s <br> %s" % (
                request.assignee_name,
                concurrence,
                approval,
                compliance_names
            )
        activity_text = action.replace("<br>", " ")
        self.save_activity(session_user, 8, json.dumps(activity_text))
        receiver = self.get_email_id_for_users(assignee)[1]
        notify_reassing_compliance = threading.Thread(
            target=email.notify_assign_compliance,
            args=[
                receiver, request.assignee_name, action
            ]
        )
        notify_reassing_compliance.start()
        return clienttransactions.ReassignComplianceSuccess()

#
#   Manage Compliances / Compliances List / Upload Compliances
#
    def calculate_ageing(self, due_date, frequency_type=None, completion_date=None, duration_type=None):
        current_time_stamp = self.get_date_time()
        compliance_status = "-"
        # due_date = self.localize(due_date)
        if frequency_type == "On Occurrence":
            r = relativedelta.relativedelta(due_date, current_time_stamp)
            if completion_date is not None:
                r = relativedelta.relativedelta(due_date, completion_date)
                if r.days < 0 and r.hours < 0 and r.minutes < 0:
                    compliance_status = "On Time"
                else:
                    if r.days == 0:
                        if duration_type in ["2", 2]:
                            compliance_status = "Delayed by %d.%d hour(s) " % (
                                abs(r.hours), abs(r.minutes)
                            )
                        else:
                            compliance_status = "Delayed by 1 day "
                    else:
                        if duration_type in ["2", 2]:
                            compliance_status = "Delayed by %d.%d hour(s)" % (
                               ( abs(r.days) * 4 + abs(r.hours)), abs(r.minutes)
                            )
                        else:
                            compliance_status = "Delayed by %d day(s)" % (
                                abs(r.days)
                            )
                    return r.days, compliance_status
            else:
                if r.days >= 0 and r.hours >= 0 and r.minutes >= 0:
                    if r.days == 0:
                        if duration_type in ["2", 2]:
                            compliance_status = " %d.%d hour(s) left" % (
                                abs(r.hours), abs(r.minutes)
                            )
                        else:
                            compliance_status = "1 Day left"
                    else:
                        if duration_type in ["2", 2]:
                            compliance_status = "%d.%d hour(s) left" % (
                               ( abs(r.days) * 24 + abs(r.hours)), abs(r.minutes)
                            )
                        else:
                            compliance_status = " %d day(s) left" % (
                                abs(r.days)
                            )
                else:
                    if r.days == 0:
                        if duration_type in ["2", 2]:
                            compliance_status = "Overdue by %d.%d hour(s) " % (
                                abs(r.hours), abs(r.minutes)
                            )
                        else:
                            compliance_status = "Overdue by 1 day "
                    else:
                        if duration_type in ["2", 2]:
                            compliance_status = "Overdue by %d.%d hours" % (
                               (abs(r.days) * 24 + abs(r.hours)), abs(r.minutes)
                            )
                        else:
                            compliance_status = "Overdue by %d day(s)" %(
                                abs(r.days)
                            )
                return r.days, compliance_status
        else:
            if completion_date is not None:
                compliance_status = "On Time"
                if due_date not in [None, "None", 0]:
                    if type(due_date) == datetime.datetime:
                        due_date = due_date.date()
                    if type(completion_date) == datetime.datetime:
                        completion_date = completion_date.date()
                    r = relativedelta.relativedelta(due_date, completion_date)
                    if r.days < 0:
                        compliance_status = "Delayed by %d day(s)" % abs(r.days)
                    return r.days, compliance_status
            else:
                if due_date not in [None, "None", 0]:
                    r = relativedelta.relativedelta(due_date.date(), current_time_stamp.date())
                    compliance_status = " %d days left" % abs(r.days+1)
                    if r.days < 0:
                        compliance_status = "Overdue by %d day(s)" % abs(r.days)
                        return r.days, compliance_status
        return 0, compliance_status

    def get_inprogress_count(self, session_user):
        other_compliance_condition = "completed_by='{}' AND \
        IFNULL(due_date, 0) >= current_date() \
        AND IFNULL(completed_on, 0) = 0".format(
            session_user
        )
        on_occurrence_condition = "completed_by='{}' AND \
        IFNULL(due_date, 0) >= now() \
        AND IFNULL(completed_on, 0) = 0".format(
            session_user
        )
        query = "SELECT count(*) FROM %s ch INNER JOIN \
        %s c ON (ch.compliance_id = c.compliance_id ) " % (
            self.tblComplianceHistory , self.tblCompliances
        )

        other_compliance_rows = self.select_all(
            "%s WHERE frequency_id != 4 AND %s" % (query, other_compliance_condition)
        )
        other_compliance_count = other_compliance_rows[0][0]

        query += " WHERE frequency_id = 4 AND %s" % (on_occurrence_condition)
        on_occurrence_rows = self.select_all(query)
        on_occurrence_count = on_occurrence_rows[0][0]

        return int(other_compliance_count) + int(on_occurrence_count)

    def get_overdue_count(self, session_user):
        query = "SELECT count(*) FROM %s ch INNER JOIN \
        %s c ON (ch.compliance_id = c.compliance_id) WHERE " % (
            self.tblComplianceHistory, self.tblCompliances
        )
        condition = "completed_by ='%d'" % (session_user)
        other_compliance_condition = " %s AND frequency_id != 4 AND \
        IFNULL(due_date, 0) < current_date() AND \
        IFNULL(completed_on, 0) = 0 " % (
            condition
        )

        on_occurrence_condition = " %s AND frequency_id = 4 AND \
        IFNULL(due_date, 0) < now() AND \
        IFNULL(completed_on, 0) = 0 " % (
            condition
        )
        other_compliance_count = self.select_all("%s %s" % (
            query, other_compliance_condition)
        )[0][0]
        on_occurrence_count = self.select_all("%s %s" % (
            query, on_occurrence_condition)
        )[0][0]
        return int(other_compliance_count) + int(on_occurrence_count)

    def get_current_compliances_list(self, current_start_count, to_count, session_user, client_id):
        columns = [
            "compliance_history_id", "start_date", "due_date", "validity_date",
            "next_due_date", "document_name", "compliance_task", "description",
            "format_file", "unit", "domain_name", "frequency", "remarks",
            "compliance_id", "duration_type_id"
        ]
        query = '''
            SELECT * FROM
            (SELECT
            compliance_history_id,
            start_date,
            ch.due_date as due_date,
            ch.validity_date,
            ch.next_due_date,
            document_name,
            compliance_task,
            compliance_description,
            format_file,
            (SELECT
                    concat(unit_code, '-', unit_name, ',', address)
                FROM
                    tbl_units tu
                WHERE
                    tu.unit_id = ch.unit_id) as unit,
            (SELECT
                    domain_name
                FROM
                    tbl_domains td
                WHERE
                    td.domain_id = c.domain_id) as domain_name,
            (SELECT
                    frequency
                FROM
                    tbl_compliance_frequency
                WHERE
                    frequency_id = c.frequency_id),
            ch.remarks,
            ch.compliance_id,
            duration_type_id
        FROM
            tbl_compliance_history ch
                INNER JOIN
            tbl_assigned_compliances ac ON (ac.unit_id = ch.unit_id
                AND ac.compliance_id = ch.compliance_id)
                INNER JOIN
            tbl_compliances c ON (ac.compliance_id = c.compliance_id)
        WHERE
            ch.completed_by = '%d'
                and ac.is_active = 1
                and IFNULL(ch.completed_on, 0) = 0
                and IFNULL(ch.due_date, 0) != 0
        LIMIT %s, %s ) a
        ORDER BY due_date ASC
        ''' % (
            session_user, current_start_count, to_count
        )
        rows = self.select_all(query)
        current_compliances_row = self.convert_to_dict(rows, columns)
        current_compliances_list = []
        for compliance in current_compliances_row:
            document_name = compliance["document_name"]
            compliance_task = compliance["compliance_task"]
            compliance_name = compliance_task
            if document_name not in (None, "None", "") :
                compliance_name = "%s - %s" % (
                    document_name, compliance_task
                )
            unit_details = compliance["unit"].split(",")
            unit_name = unit_details[0]
            address = unit_details[1]
            no_of_days, ageing = self.calculate_ageing(
                due_date=compliance["due_date"],
                frequency_type=compliance["frequency"],
                duration_type=compliance["duration_type_id"]
            )
            compliance_status = core.COMPLIANCE_STATUS("Inprogress")
            if "Overdue" in ageing:
                compliance_status = core.COMPLIANCE_STATUS("Not Complied")
            format_files = None
            if compliance["format_file"] is not None and compliance["format_file"].strip() != '':
                format_files = [ "%s/%s" % (
                        FORMAT_DOWNLOAD_URL, x
                    ) for x in compliance["format_file"].split(",")]
            remarks = compliance["remarks"]
            if remarks in ["None", None, ""]:
                remarks = None
            current_compliances_list.append(
                core.ActiveCompliance(
                    compliance_history_id=compliance["compliance_history_id"],
                    compliance_name=compliance_name,
                    compliance_frequency=core.COMPLIANCE_FREQUENCY(compliance["frequency"]),
                    domain_name=compliance["domain_name"],
                    start_date=self.datetime_to_string(compliance["start_date"]),
                    due_date=self.datetime_to_string(compliance["due_date"]),
                    compliance_status=compliance_status,
                    validity_date=None if compliance["validity_date"] == None else self.datetime_to_string(compliance["validity_date"]),
                    next_due_date=None if compliance["next_due_date"] == None else self.datetime_to_string(compliance["next_due_date"]),
                    ageing=ageing,
                    format_file_name=format_files,
                    unit_name=unit_name, address=address,
                    compliance_description=compliance["description"],
                    remarks=remarks,
                    compliance_id=compliance["compliance_id"]
                )
            )
        return current_compliances_list

    def get_upcoming_count(self, session_user):
        all_compliance_query = '''
            SELECT ac.compliance_id, ac.unit_id FROM tbl_assigned_compliances ac
            INNER JOIN tbl_compliances c ON (ac.compliance_id = c.compliance_id)
            WHERE
            assignee = '%d' AND frequency_id != 4
            AND ac.due_Date < DATE_ADD(now(), INTERVAL 6 MONTH)
            AND ac.is_active = 1;
        ''' % (
            session_user
        )
        all_compliace_rows = self.select_all(all_compliance_query)
        all_compliance_count = len(all_compliace_rows)
        onetime_query = '''
            SELECT ch.compliance_id, ch.unit_id FROM tbl_compliance_history ch
            INNER JOIN tbl_compliances c on (ch.compliance_id =  c.compliance_id)
            WHERE frequency_id = 1 and completed_by = '%d' ;
        ''' % (
            session_user
        )
        onetime_rows = self.select_all(onetime_query)

        combined_rows = []
        for combination in onetime_rows:
            if combination in all_compliace_rows:
                combined_rows.append(combination)
            else:
                continue

        count = len(combined_rows)
        return all_compliance_count - count

    def get_upcoming_compliances_list(self, upcoming_start_count, to_count, session_user, client_id):
        query = "SELECT * FROM (SELECT ac.due_date, document_name, compliance_task, \
                compliance_description, format_file, \
                (select concat(unit_code,'-' ,unit_name, ',',address) from %s tu  where\
                tu.unit_id = ac.unit_id), \
                (select domain_name \
                FROM %s d where d.domain_id = c.domain_id) as domain_name, \
                DATE_SUB(ac.due_date, INTERVAL ac.trigger_before_days DAY) \
                as start_date\
                FROM %s  ac \
                INNER JOIN %s c ON (ac.compliance_id = c.compliance_id) WHERE \
                assignee = '%d' AND frequency_id != 4 \
                AND ac.due_Date < DATE_ADD(now(), INTERVAL 6 MONTH) \
                AND ac.is_active = 1 AND IF ( (frequency_id = 1 AND ( \
                select count(*) from tbl_compliance_history ch \
                where ch.compliance_id = ac.compliance_id and \
                ch.unit_id = ac.unit_id ) >0), 0,1) \
                LIMIT %d, %d ) a ORDER BY start_date ASC"  % (
                    self.tblUnits, self.tblDomains, self.tblAssignedCompliances,
                    self.tblCompliances, session_user, int(upcoming_start_count),
                    to_count
                )
        upcoming_compliances_rows = self.select_all(query)

        columns = ["due_date", "document_name", "compliance_task",
        "description","format_file", "unit", "domain_name",  "start_date"]
        upcoming_compliances_result = self.convert_to_dict(
            upcoming_compliances_rows, columns
        )
        upcoming_compliances_list = []
        for compliance in upcoming_compliances_result:
            document_name = compliance["document_name"]
            compliance_task = compliance["compliance_task"]
            compliance_name = compliance_task
            if document_name not in (None, "None", "") :
                compliance_name = "%s - %s" % (document_name, compliance_task)

            unit_details = compliance["unit"].split(",")
            unit_name = unit_details[0]
            address = unit_details[1]

            start_date = compliance["start_date"]
            format_files = None
            if compliance["format_file"] is not None and compliance["format_file"].strip() != '':
                format_files = [ "%s/%s" % (
                        FORMAT_DOWNLOAD_URL, x
                    ) for x in compliance["format_file"].split(",")]
            upcoming_compliances_list.append(
                core.UpcomingCompliance(
                    compliance_name=compliance_name,
                    domain_name=compliance["domain_name"],
                    start_date=self.datetime_to_string(start_date),
                    due_date=self.datetime_to_string(compliance["due_date"]),
                    format_file_name=format_files,
                    unit_name=unit_name,
                    address=address,
                    compliance_description=compliance["description"]
                ))
        return upcoming_compliances_list

    # def calculate_next_start_date(self, due_date, statutory_dates, repeats_every):
    #     statutory_dates = json.loads(statutory_dates)
    #     next_start_date = None
    #     if len(statutory_dates) > 1:
    #         month_of_due_date = due_date.month
    #         for statutory_date in statutory_dates:
    #             if month_of_due_date >= statutory_date["statutory_month"]:
    #                 next_start_date = due_date - timedelta(
    #                     days = statutory_date["trigger_before_days"])
    #                 break
    #             else:
    #                 continue
    #     else:
    #         trigger_before = 0
    #         if len(statutory_dates) > 0:
    #             trigger_before = int(statutory_dates[0]["trigger_before_days"])
    #         next_start_date = due_date - timedelta(days=trigger_before)
    #     return next_start_date

    def report_statutory_notifications_list(self, request_data):
        country_name = request_data.country_name
        domain_name = request_data.domain_name
        business_group_id = request_data.business_group_id
        legal_entity_id = request_data.legal_entity_id
        division_id = request_data.division_id
        unit_id = request_data.unit_id
        level_1_statutory_name = request_data.level_1_statutory_name
        from_date = request_data.from_date
        to_date = request_data.to_date
        condition = ""
        if from_date is not None and to_date is not None :
            from_date = self.string_to_datetime(from_date).date()
            to_date = self.string_to_datetime(to_date).date()
            condition += " AND date(snl.updated_on) >= '%s' AND date(snl.updated_on) <= '%s'" % (from_date, to_date)
        if business_group_id is not None:
            condition += " AND u.business_group_id = '%s'" % business_group_id
        if legal_entity_id is not None:
            condition += " AND u.legal_entity_id = '%s'" % legal_entity_id
        if division_id is not None:
            condition += " AND u.division_id = '%s'" % division_id
        if unit_id is not None:
            condition += " AND u.unit_id = '%s'" % unit_id

        if level_1_statutory_name is not None :
            condition += " AND snl.statutory_provision like '%s'" % str((level_1_statutory_name + '%'))

        query = "SELECT \
            (select business_group_name from tbl_business_groups where business_group_id = u.business_group_id), \
            (select legal_entity_name from tbl_legal_entities where legal_entity_id = u.legal_entity_id), \
            (select division_name from tbl_divisions where division_id = u.division_id), \
            u.unit_code, \
            u.unit_name, \
            u.address, \
            snl.statutory_provision, \
            snl.notification_text, \
            snl.updated_on \
        from \
            tbl_statutory_notifications_log snl \
                INNER JOIN \
            tbl_statutory_notifications_units snu \
        ON snl.statutory_notification_id = snu.statutory_notification_id \
                INNER JOIN \
            tbl_units u ON snu.unit_id = u.unit_id \
            INNER JOIN tbl_countries tc ON \
            tc.country_id = snl.country_name \
            INNER JOIN tbl_domains td ON \
            td.domain_id = snl.domain_name \
        where \
            tc.country_name = '%s' \
            and td.domain_name = '%s' \
            %s \
            ORDER BY snl.updated_on" % (
                    country_name, domain_name,
                    condition
                )
        rows = self.select_all(query)
        columns = [
            "business_group", "legal_entity", "division", "unit_code", "unit_name",
            "address", "statutory_provision", "notification_text", "updated_on"
        ]
        data = self.convert_to_dict(rows, columns)
        legal_wise = {}
        for d in data :
            unit_name = "%s - %s" % (d["unit_code"], d["unit_name"])
            statutories = d["statutory_provision"].split(">>")
            level_1_statutory_name = statutories[0].strip()

            level_1_statutory_wise_notifications = {}
            notify = clientreport.LEVEL_1_STATUTORY_NOTIFICATIONS(
                d["statutory_provision"],
                unit_name,
                d["notification_text"],
                self.datetime_to_string(d["updated_on"])
            )
            level_1_statutory_wise_notifications[level_1_statutory_name] = [notify]
            legal_wise_data = legal_wise.get(d["legal_entity"])
            if legal_wise_data is None :
                legal_wise_data = clientreport.STATUTORY_WISE_NOTIFICATIONS(
                    d["business_group"], d["legal_entity"], d["division"],
                    level_1_statutory_wise_notifications
                )
            else :
                dict_level_1 = legal_wise_data.level_1_statutory_wise_notifications
                if dict_level_1 is None :
                    dict_level_1 = {}
                lst = dict_level_1.get(level_1_statutory_name)
                if lst is None :
                    lst = []
                else :
                    lst.append(notify)
                dict_level_1[level_1_statutory_name] = lst
                legal_wise_data.level_1_statutory_wise_notifications = dict_level_1
            legal_wise[d["legal_entity"]] = legal_wise_data

        notification_lst = []
        for k in sorted(legal_wise):
            notification_lst.append(legal_wise.get(k))
        return notification_lst

#
#   Risk Report
#
    def get_not_opted_compliances(
        self, domain_id, country_id, where_qry, from_count, to_count
    ):
        query = "SELECT c.compliance_id, c.compliance_task, c.document_name, \
            c.statutory_dates, c.compliance_description, c.penal_consequences, c.frequency_id, \
            (select frequency from tbl_compliance_frequency where frequency_id = c.frequency_id ), \
            c.repeats_type_id, c.repeats_every, c.duration_type_id, c.duration, \
            c.statutory_mapping, \
            SUBSTRING_INDEX(SUBSTRING_INDEX(c.statutory_mapping, '>>', 1), '>>', - 1) level_1, c.statutory_provision, \
            (select business_group_name from tbl_business_groups where business_group_id = u.business_group_id ), \
            (select legal_entity_name from tbl_legal_entities where legal_entity_id = u.legal_entity_id), \
            (select division_name from tbl_divisions where division_id = u.division_id), \
            u.unit_code, u.unit_name, u.address, u.postal_code, u.unit_id \
            FROM tbl_compliances c \
            INNER JOIN tbl_client_compliances cc \
            ON c.compliance_id = cc.compliance_id \
            INNER JOIN tbl_client_statutories cs  \
            ON cs.client_statutory_id = cc.client_statutory_id \
            INNER JOIN tbl_units u ON  \
            cs.unit_id = u.unit_id \
            WHERE  cc.compliance_opted = 0 \
            AND c.domain_id = %s \
            AND cs.country_id = %s \
            %s \
            order by SUBSTRING_INDEX(SUBSTRING_INDEX(c.statutory_mapping, '>>', 1), '>>', - 1), u.unit_id \
            limit %s, %s " % (
                domain_id, country_id,
                where_qry,
                from_count, to_count
            )
        columns = [
            "compliance_id", "compliance_task", "document_name",
            "statutory_dates", "compliance_description", "penal_consequences",
            "frequency_id", "frequency",
            "repeats_type_id", "repeats_every", "duration_type_id", "duration",
            "statutory_mapping", "level_1", "statutory_provision",
            "business_group", "legal_entity",
            "division", "unit_code", "unit_name",
            "address", "postal_code", "unit_id"
        ]
        rows = self.select_all(query)
        result = self.convert_to_dict(rows, columns)
        return result

    def get_not_opted_compliances_where_qry(
        self, business_group_id, legal_entity_id, division_id, unit_id,
        leval_1_statutory_name, session_user
    ) :
        where_qry = ""
        admin_id = self.get_admin_id()

        if session_user > 0 and session_user != admin_id :
            where_qry += " AND u.unit_id in \
                (select us.unit_id from tbl_user_units us where \
                    us.user_id = %s\
                )" % int(session_user)
            where_qry += " AND c.domain_id in \
                (select us.domain_id from tbl_user_domains us where \
                    us.user_id = %s\
                )" % int(session_user)

        if business_group_id is not None :
            where_qry += " AND u.business_group_id = %s " % (business_group_id)

        if legal_entity_id is not None :
            where_qry += " AND u.legal_entity_id = %s " % (legal_entity_id)

        if division_id is not None :
            where_qry += " AND u.division_id = %s " % (division_id)

        if unit_id is not None :
            where_qry += " AND u.unit_id = %s " % (unit_id)

        if leval_1_statutory_name is not None :
            where_qry += " AND c.statutory_mapping like '%s' " % (leval_1_statutory_name + '%')

        return where_qry

    def get_not_opted_compliances_count(
        self, country_id, domain_id, where_qry
    ) :
        q_count = "SELECT count(c.compliance_id) \
            FROM tbl_compliances c \
            INNER JOIN tbl_client_compliances cc \
            ON c.compliance_id = cc.compliance_id \
            INNER JOIN tbl_client_statutories cs  \
            ON cs.client_statutory_id = cc.client_statutory_id \
            INNER JOIN tbl_units u ON  \
            cs.unit_id = u.unit_id \
            WHERE  cc.compliance_opted = 0 \
            AND c.domain_id = %s \
            AND cs.country_id = %s \
            %s " % (
                domain_id, country_id,
                where_qry
            )
        c_row = self.select_one(q_count)
        if c_row :
            total = int(c_row[0])
        else :
            total = 0
        return total

    def get_not_opted_compliances_with_count(
        self, country_id, domain_id, business_group_id,
        legal_entity_id, division_id, unit_id, leval_1_statutory_name,
        session_user, from_count, to_count
    ) :
        where_qry = self.get_not_opted_compliances_where_qry(
            business_group_id, legal_entity_id, division_id, unit_id,
            leval_1_statutory_name,  session_user
        )
        total = self.get_not_opted_compliances_count(
            country_id, domain_id, where_qry
        )
        result = self.get_not_opted_compliances(
            domain_id, country_id, where_qry, from_count, to_count
        )
        return self.return_risk_report_data(result, total)

    def get_unassigned_compliances(
        self, domain_id, country_id, where_qry, from_count, to_count
    ):
        query = "SELECT c.compliance_id, c.compliance_task, c.document_name, \
            c.statutory_dates, c.compliance_description, c.penal_consequences, c.frequency_id, \
            (select frequency from tbl_compliance_frequency where frequency_id = c.frequency_id ), \
            c.repeats_type_id, c.repeats_every, c.duration_type_id, c.duration, \
            c.statutory_mapping,\
            SUBSTRING_INDEX(SUBSTRING_INDEX(c.statutory_mapping, '>>', 1), '>>', - 1) level_1, c.statutory_provision, \
            (select business_group_name from tbl_business_groups where business_group_id = u.business_group_id ), \
            (select legal_entity_name from tbl_legal_entities where legal_entity_id = u.legal_entity_id), \
            (select division_name from tbl_divisions where division_id = u.division_id), \
            u.unit_code, u.unit_name, u.address, u.postal_code, u.unit_id \
            FROM tbl_compliances c \
            INNER JOIN tbl_client_compliances cc \
            ON c.compliance_id = cc.compliance_id \
            INNEr JOIN tbl_client_statutories cs  \
            ON cs.client_statutory_id = cc.client_statutory_id \
            INNER JOIN tbl_units u ON  \
            cs.unit_id = u.unit_id \
            LEFT JOIN tbl_assigned_compliances ac \
            ON ac.compliance_id = cc.compliance_id and \
            ac.unit_id = cs.unit_id \
            WHERE  ac.compliance_id is Null \
            AND c.domain_id = %s \
            AND cs.country_id = %s \
            %s \
            order by SUBSTRING_INDEX(SUBSTRING_INDEX(c.statutory_mapping, '>>', 1), '>>', - 1), u.unit_id \
            limit %s, %s " % (
                domain_id, country_id,
                where_qry,
                from_count, to_count
            )
        columns = [
            "compliance_id", "compliance_task", "document_name",
            "statutory_dates", "compliance_description", "penal_consequences",
            "frequency_id", "frequency",
            "repeats_type_id", "repeats_every", "duration_type_id", "duration",
            "statutory_mapping", "level_1", "statutory_provision",
            "business_group", "legal_entity",
            "division", "unit_code", "unit_name",
            "address", "postal_code", "unit_id"
        ]
        rows = self.select_all(query)
        result = self.convert_to_dict(rows, columns)
        return result

    def get_unassigned_compliances_where_qry(
        self, business_group_id, legal_entity_id, division_id, unit_id,
        leval_1_statutory_name, session_user
    ) :
        where_qry = ""
        admin_id = self.get_admin_id()

        if session_user > 0 and session_user != admin_id :
            where_qry += " AND u.unit_id in \
                (select us.unit_id from tbl_user_units us where \
                    us.user_id = %s\
                )" % int(session_user)
            where_qry += " AND c.domain_id in \
                (select us.domain_id from tbl_user_domains us where \
                    us.user_id = %s\
                )" % int(session_user)

        if business_group_id is not None :
            where_qry += " AND u.business_group_id = %s " % (business_group_id)

        if legal_entity_id is not None :
            where_qry += " AND u.legal_entity_id = %s " % (legal_entity_id)

        if division_id is not None :
            where_qry += " AND u.division_id = %s " % (division_id)

        if unit_id is not None :
            where_qry += " AND u.unit_id = %s " % (unit_id)

        if leval_1_statutory_name is not None :
            where_qry += " AND c.statutory_mapping like '%s' " % (leval_1_statutory_name + '%')
        return where_qry

    def get_unassigned_compliances_count(
        self, country_id, domain_id, where_qry
    ) :
        q_count = "SELECT count(c.compliance_id) \
            FROM tbl_compliances c \
            INNER JOIN tbl_client_compliances cc \
            ON c.compliance_id = cc.compliance_id \
            INNER JOIN tbl_client_statutories cs  \
            ON cs.client_statutory_id = cc.client_statutory_id \
            INNER JOIN tbl_units u ON  \
            cs.unit_id = u.unit_id \
            Left JOIN tbl_assigned_compliances ac \
            ON ac.compliance_id = cc.compliance_id and \
            ac.unit_id = cs.unit_id \
            WHERE  ac.compliance_id is Null \
            AND c.domain_id = %s \
            AND cs.country_id = %s \
            %s " % (
                domain_id, country_id,
                where_qry
            )
        c_row = self.select_one(q_count)
        if c_row :
            total = int(c_row[0])
        else :
            total = 0
        return total

    def get_unassigned_compliances_with_count(
        self, country_id, domain_id, business_group_id,
        legal_entity_id, division_id, unit_id, leval_1_statutory_name,
        session_user, from_count, to_count
    ) :
        where_qry = self.get_unassigned_compliances_where_qry(
            business_group_id, legal_entity_id, division_id, unit_id,
            leval_1_statutory_name, session_user
        )
        total = self.get_unassigned_compliances_count(
            country_id, domain_id, where_qry
        )
        result = self.get_unassigned_compliances(
            domain_id, country_id, where_qry, from_count, to_count
        )
        return self.return_risk_report_data(result, total)

    def get_delayed_compliances(
        self, domain_id, country_id, where_qry, from_count, to_count
    ):
        query = "SELECT  c.compliance_id, c.compliance_task, c.document_name, \
            ac.statutory_dates, c.compliance_description, c.penal_consequences, c.frequency_id, \
            (select frequency from tbl_compliance_frequency where frequency_id = c.frequency_id ), \
            c.repeats_type_id, c.repeats_every, c.duration_type_id, c.duration, \
            c.statutory_mapping,\
            SUBSTRING_INDEX(SUBSTRING_INDEX(c.statutory_mapping, '>>', 1), '>>', - 1) level_1, c.statutory_provision, \
            (select business_group_name from tbl_business_groups where business_group_id = u.business_group_id ), \
            (select legal_entity_name from tbl_legal_entities where legal_entity_id = u.legal_entity_id), \
            (select division_name from tbl_divisions where division_id = u.division_id), \
            u.unit_code, u.unit_name, u.address, u.postal_code, u.unit_id \
            FROM tbl_compliance_history ch \
            INNER JOIN tbl_assigned_compliances ac \
            ON ch.compliance_id = ac.compliance_id \
            AND ch.unit_id = ac.unit_id \
            INNER JOIN tbl_compliances c \
            ON ch.compliance_id = c.compliance_id \
            INNER JOIN tbl_units u ON  \
            ch.unit_id = u.unit_id \
            WHERE c.domain_id = %s \
            AND ac.country_id = %s \
            AND ch.due_date < ch.completion_date \
            AND ch.approve_status = 1 \
            %s \
            order by SUBSTRING_INDEX(SUBSTRING_INDEX(c.statutory_mapping, '>>', 1), '>>', - 1), u.unit_id \
            limit %s, %s " % (
                domain_id, country_id,
                where_qry,
                from_count, to_count
            )
        columns = [
            "compliance_id", "compliance_task", "document_name",
            "statutory_dates", "compliance_description", "penal_consequences",
            "frequency_id", "frequency",
            "repeats_type_id", "repeats_every", "duration_type_id", "duration",
            "statutory_mapping", "level_1", "statutory_provision",
            "business_group", "legal_entity",
            "division", "unit_code", "unit_name",
            "address", "postal_code", "unit_id"
        ]
        rows = self.select_all(query)
        result = self.convert_to_dict(rows, columns)
        return result

    def get_delayed_compliances_where_qry(
        self, business_group_id, legal_entity_id, division_id, unit_id,
        leval_1_statutory_name, session_user
    ) :
        where_qry = ""
        admin_id = self.get_admin_id()
        if session_user > 0 and session_user != admin_id :
            where_qry += " AND u.unit_id in \
                (select us.unit_id from tbl_user_units us where \
                    us.user_id = %s\
                )" % int(session_user)
            where_qry += " AND c.domain_id in \
                (select us.domain_id from tbl_user_domains us where \
                    us.user_id = %s\
                )" % int(session_user)

        if business_group_id is not None :
            where_qry += " AND u.business_group_id = %s " % (business_group_id)

        if legal_entity_id is not None :
            where_qry += " AND u.legal_entity_id = %s " % (legal_entity_id)

        if division_id is not None :
            where_qry += " AND u.division_id = %s " % (division_id)

        if unit_id is not None :
            where_qry += " AND u.unit_id = %s " % (unit_id)

        if leval_1_statutory_name is not None :
            where_qry += " AND c.statutory_mapping like '%s' " % (leval_1_statutory_name + '%')
        return where_qry

    def get_delayed_compliances_count(
        self, country_id, domain_id, business_group_id,
        legal_entity_id, division_id, unit_id, leval_1_statutory_name,
        session_user
    ) :
        where_qry = self.get_delayed_compliances_where_qry(
            business_group_id, legal_entity_id, division_id, unit_id,
            leval_1_statutory_name, session_user
        )
        q_count = "SELECT count(distinct ch.compliance_history_id) \
            FROM tbl_compliance_history ch \
            INNER JOIN tbl_assigned_compliances ac \
            ON ch.compliance_id = ac.compliance_id \
            AND ch.unit_id = ac.unit_id \
            INNER JOIN tbl_compliances c \
            ON ch.compliance_id = c.compliance_id \
            INNER JOIN tbl_units u ON  \
            ch.unit_id = u.unit_id \
            WHERE c.domain_id = %s \
            AND ac.country_id = %s \
            AND ch.due_date < ch.completion_date \
            AND ch.approve_status = 1 \
            %s " % (
                domain_id, country_id,
                where_qry
            )
        c_row = self.select_one(q_count)
        if c_row :
            total = int(c_row[0])
        else :
            total = 0
        return total

    def get_delayed_compliances_with_count(
        self, country_id, domain_id, business_group_id,
        legal_entity_id, division_id, unit_id, leval_1_statutory_name,
        session_user, from_count, to_count
    ) :
        where_qry = self.get_delayed_compliances_where_qry(
            business_group_id, legal_entity_id, division_id, unit_id,
            leval_1_statutory_name, session_user
        )
        total = self.get_delayed_compliances_count(
            country_id, domain_id, business_group_id,
            legal_entity_id, division_id, unit_id, leval_1_statutory_name,
            session_user
        )
        result = self.get_delayed_compliances(
            domain_id, country_id, where_qry, from_count, to_count
        )
        return self.return_risk_report_data(result, total)

    def get_not_complied_compliances(
        self, domain_id, country_id, where_qry, from_count, to_count
    ):
        query = "SELECT distinct c.compliance_id, c.compliance_task, c.document_name, \
            ac.statutory_dates, c.compliance_description, c.penal_consequences, c.frequency_id, \
            (select frequency from tbl_compliance_frequency where frequency_id = c.frequency_id ), \
            c.repeats_type_id, c.repeats_every, c.duration_type_id, c.duration, \
            c.statutory_mapping,\
            SUBSTRING_INDEX(SUBSTRING_INDEX(c.statutory_mapping, '>>', 1), '>>', - 1) level_1, c.statutory_provision, \
            (select business_group_name from tbl_business_groups where business_group_id = u.business_group_id ), \
            (select legal_entity_name from tbl_legal_entities where legal_entity_id = u.legal_entity_id), \
            (select division_name from tbl_divisions where division_id = u.division_id), \
            u.unit_code, u.unit_name, u.address, u.postal_code, u.unit_id, \
            ch.compliance_history_id \
            FROM tbl_compliance_history ch \
            INNER JOIN tbl_assigned_compliances ac \
            ON ch.compliance_id = ac.compliance_id \
            AND ch.unit_id = ac.unit_id \
            INNER JOIN tbl_compliances c \
            ON ch.compliance_id = c.compliance_id \
            INNER JOIN tbl_units u ON  \
            ch.unit_id = u.unit_id \
            WHERE c.domain_id = %s \
            AND ac.country_id = %s \
            AND ((IFNULL(c.duration_type_id, 0) = 2 AND ch.due_date < now()) \
            or (IFNULL(c.duration_type_id, 0) != 2 AND ch.due_date < CURDATE()))  \
            AND IFNULL(ch.approve_status, 0) != 1 \
            %s \
            order by SUBSTRING_INDEX(SUBSTRING_INDEX(c.statutory_mapping, '>>', 1), '>>', - 1), u.unit_id \
            limit %s, %s " % (
                domain_id, country_id,
                where_qry,
                from_count, to_count
            )
        print query
        columns = [
            "compliance_id", "compliance_task", "document_name",
            "statutory_dates", "compliance_description", "penal_consequences",
            "frequency_id", "frequency",
            "repeats_type_id", "repeats_every", "duration_type_id", "duration",
            "statutory_mapping", "level_1", "statutory_provision",
            "business_group", "legal_entity",
            "division", "unit_code", "unit_name",
            "address", "postal_code", "unit_id",
            "compliance_history_id"
        ]
        rows = self.select_all(query)
        result = self.convert_to_dict(rows, columns)
        return result

    def get_not_complied_where_qry(
        self, business_group_id, legal_entity_id, division_id, unit_id,
        leval_1_statutory_name
    ):
        where_qry = ""
        if business_group_id is not None :
            where_qry = " AND u.business_group_id = %s " % (business_group_id)

        if legal_entity_id is not None :
            where_qry = " AND u.legal_entity_id = %s " % (legal_entity_id)

        if division_id is not None :
            where_qry = " AND u.division_id = %s " % (division_id)

        if unit_id is not None :
            where_qry = " AND u.unit_id = %s " % (unit_id)

        if leval_1_statutory_name is not None :
            where_qry = " AND c.statutory_mapping like '%s' " % (leval_1_statutory_name + '%')
        return where_qry

    def get_not_complied_compliances_count(
        self, country_id, domain_id, where_qry
    ):
        q_count = "SELECT count(c.compliance_id) \
            FROM tbl_compliance_history ch \
            INNER JOIN tbl_compliances c \
            ON ch.compliance_id = c.compliance_id \
            INNER JOIN tbl_units u ON  \
            ch.unit_id = u.unit_id \
            WHERE c.domain_id = %s \
            AND u.country_id = %s \
            AND ((IFNULL(c.duration_type_id, 0) = 2 AND ch.due_date < now()) \
            or (IFNULL(c.duration_type_id, 0) != 2 AND ch.due_date < CURDATE()))  \
            AND IFNULL(ch.approve_status, 0) != 1 \
            %s " % (
                domain_id, country_id,
                where_qry
            )
        print q_count
        c_row = self.select_one(q_count)
        if c_row :
            total = int(c_row[0])
        else :
            total = 0
        return total

    def get_not_complied_compliances_with_count(
        self, country_id, domain_id, business_group_id,
        legal_entity_id, division_id, unit_id, leval_1_statutory_name,
        session_user, from_count, to_count
    ):
        where_qry = self.get_not_complied_where_qry(
            business_group_id, legal_entity_id, division_id, unit_id,
            leval_1_statutory_name
        )
        total = self.get_not_complied_compliances_count(
            country_id, domain_id, where_qry
        )
        result = self.get_not_complied_compliances(
            domain_id, country_id, where_qry, from_count, to_count
        )
        return self.return_risk_report_data(result, total)

    def return_risk_report_data(self, data, total) :
        report_data_list = {}
        for d in data :
            unit_id = int(d["unit_id"])
            business_group_name = d["business_group"]
            legal_entity = d["legal_entity"]
            division_name = d["division"]
            level_1 = d["level_1"]
            compliance_name = d["compliance_task"]
            if d["document_name"] not in (None, "None", "") :
                compliance_name = "%s - %s" % (
                    d["document_name"], d["compliance_task"]
                )
            statutory_mapping = "%s >> %s" % (
                d["statutory_mapping"], d["statutory_provision"]
            )
            repeats = ""
            trigger = "Trigger :"
            if d["frequency_id"] != 1 and d["frequency_id"] != 4 :
                if d["repeats_type_id"] == 1 :
                    repeats = "Every %s Day/s " % (d["repeats_every"])
                elif d["repeats_type_id"] == 2 :
                    repeats = "Every %s Month/s " % (d["repeats_every"])
                elif d["repeats_type_id"] == 3 :
                    repeats = "Every %s Year/s " % (d["repeats_every"])
                if d["statutory_dates"] is not None:
                    statutory_dates = json.loads(d["statutory_dates"])
                    for index, statutory_date in enumerate(statutory_dates):
                        if index == 0:
                            if statutory_date["statutory_date"] is not None and statutory_date["statutory_month"] is not None:
                                repeats += "%s %s, " % (
                                    statutory_date["statutory_date"], statutory_date["statutory_month"]
                                )
                            if statutory_date["trigger_before_days"] is not None:
                                trigger += "%s Days" % statutory_date["trigger_before_days"]
                        else:
                            if statutory_date["trigger_before_days"] is not None:
                                trigger += " and %s Days" % statutory_date["trigger_before_days"]
                repeats += trigger
            elif d["frequency_id"] == 1:
                statutory_dates = json.loads(d["statutory_dates"])
                statutory_date = statutory_dates[0]
                if statutory_date["statutory_date"] is not None and statutory_date["statutory_month"] is not None:
                    repeats = "%s %s " % (
                        statutory_date["statutory_date"], self.string_months[statutory_date["statutory_month"]]
                    )
                if statutory_date["trigger_before_days"] is not None:
                    trigger += "%s Days " % statutory_date["trigger_before_days"]
                repeats += trigger
            elif d["frequency_id"] == 4:
                if d["duration_type_id"] == 1 :
                    if d["duration"] is not None:
                        repeats = "Complete within %s Day/s " % (d["duration"])
                elif d["duration_type_id"] == 2 :  # Hours
                    if d["duration"] is not None:
                        repeats = "Complete within %s Hour/s" % (d["duration"])
            compliance = clientreport.Level1Compliance(
                statutory_mapping, compliance_name,
                d["compliance_description"], d["penal_consequences"],
                d["frequency"], repeats
            )
            unit_name = "%s - %s" % (
                d["unit_code"], d["unit_name"]
            )
            address = d["address"] + " - " + str(d["postal_code"])
            unit_wise_comp = clientreport.Level1Statutory(
                unit_id, unit_name, address, [compliance]
            )
            level_1_statutory_wise_units = {}
            level_1_statutory_wise_units[level_1] = [unit_wise_comp]
            report_data = clientreport.RiskData(
                business_group_name, legal_entity, division_name,
                level_1_statutory_wise_units
            )
            legal_wise = report_data_list.get(legal_entity)
            if legal_wise is None :
                legal_wise = report_data
            else :
                level_1_units = legal_wise.level_1_statutory_wise_units.get(level_1)
                if level_1_units is None :
                    level_1_units = []
                    level_1_units.append(unit_wise_comp)
                else :
                    is_new_unit = True
                    for u in level_1_units :
                        if u.unit_id == unit_id :
                            is_new_unit = False
                            c_list = u.compliances
                            if c_list is None :
                                c_list = []
                            c_list.append(compliance)
                            u.compliances = c_list
                    if is_new_unit :
                        level_1_units.append(unit_wise_comp)
                legal_wise.level_1_statutory_wise_units[level_1] = level_1_units
            report_data_list[legal_entity] = legal_wise

        final_lst = []
        for k in sorted(report_data_list) :
            final_lst.append(report_data_list.get(k))
        return total, final_lst

    def update_compliances(
        self, compliance_history_id, documents, completion_date,
        validity_date, next_due_date, remarks, client_id, session_user
    ):
        if validity_date not in [None, "None", ""]:
            validity_date = self.string_to_datetime(validity_date)
        else:
            validity_date = None
        if next_due_date not in [None, "None", ""]:
            next_due_date = self.string_to_datetime(next_due_date)
        else:
            next_due_date = None

        if None not in [validity_date, next_due_date]:
            r = relativedelta.relativedelta(validity_date, next_due_date)
            if abs(r.months) > 3 or abs(r.years) > 0:
                return False

        # Hanling upload
        document_names = []
        file_size = 0
        if documents is not None:
            if len(documents) > 0:
                for doc in documents:
                    file_size += doc.file_size

                if self.is_space_available(file_size):
                    is_uploading_file = True
                    for doc in documents:
                        file_name_parts = doc.file_name.split('.')
                        name = None
                        exten = None
                        for index, file_name_part in enumerate(file_name_parts):
                            if index == len(file_name_parts) - 1:
                                exten = file_name_part
                            else:
                                if name is None:
                                    name = file_name_part
                                else:
                                    name += file_name_part
                        auto_code = self.new_uuid()
                        file_name = "%s-%s.%s" % (name, auto_code, exten)
                        document_names.append(file_name)
                        self.convert_base64_to_file(file_name, doc.file_content, client_id)
                    self.update_used_space(file_size)
                else:
                    return clienttransactions.NotEnoughSpaceAvailable()

        assignee_id, concurrence_id, approver_id, compliance_name, document_name, due_date = self.get_compliance_history_details(
            compliance_history_id
        )
        current_time_stamp = self.get_date_time()
        history_columns = [
            "completion_date", "documents", "remarks", "completed_on"
        ]
        if self.is_onOccurrence_with_hours(compliance_history_id):
            completion_date = self.string_to_datetime(completion_date)
        else:
            completion_date = self.string_to_datetime(completion_date).date()
        history_values = [
            completion_date,
            ",".join(document_names),
            remarks,
            current_time_stamp
        ]
        if validity_date not in ["", None, "None"]:
            history_columns.append("validity_date")
            history_values.append(validity_date)
        if next_due_date not in ["", None, "None"]:
            history_columns.append("next_due_date")
            history_values.append(next_due_date)
        history_condition = "compliance_history_id = '%d' \
            and completed_by ='%d'" % (
                compliance_history_id, session_user
            )

        columns = "unit_id, compliance_id"
        condition = "compliance_history_id = '%d'" % compliance_history_id
        rows = self.get_data(
            self.tblComplianceHistory, columns, condition
        )
        unit_id = rows[0][0]
        compliance_id = rows[0][1]
        ageing, remarks = self.calculate_ageing(
            due_date, frequency_type=None, completion_date=completion_date, duration_type=None
        )
        if assignee_id == approver_id:
            history_columns.append("approve_status")
            history_columns.append("approved_on")
            history_values.append(1)
            history_values.append(current_time_stamp)
            query = "SELECT frequency_id FROM %s tc WHERE tc.compliance_id = '%s' " % (
                self.tblCompliances, compliance_id
            )
            rows = self.select_all(query)
            columns = ["frequency_id"]
            rows = self.convert_to_dict(rows, columns)
            as_condition = " unit_id = '%d' and compliance_id = '%d'" % (
                unit_id, compliance_id
            )
            self.update(
                self.tblAssignedCompliances, ["is_active"], [0], as_condition,
                client_id
            )
            self.save_compliance_activity(
                unit_id, compliance_id, "Approved", "Complied",
                remarks
            )
        else:
            self.save_compliance_activity(
                unit_id, compliance_id, "Submitted", "Inprogress",
                remarks
            )

        self.update(
            self.tblComplianceHistory, history_columns, history_values,
            history_condition
        )

        if assignee_id != approver_id:
            if document_name is not None and document_name != '' and document_name != 'None':
                compliance_name = "%s - %s" % (document_name, compliance_name)

            assignee_email, assignee_name = self.get_user_email_name(str(assignee_id))
            approver_email, approver_name = self.get_user_email_name(str(approver_id))
            action = "approve"
            notification_text = "%s has completed the compliance %s. Review and approve" % (
                assignee_name, compliance_name
            )
            concurrence_email, concurrence_name = (None, None)
            if self.is_two_levels_of_approval() and concurrence_id not in [None, "None", 0, "", "null", "Null"]:
                concurrence_email, concurrence_name = self.get_user_email_name(str(concurrence_id))
                action = "Concur"
                notification_text = "%s has completed the compliance %s. Review and concur" % (
                    assignee_name, compliance_name
                )

            self.save_compliance_notification(
                compliance_history_id, notification_text, "Compliance Completed", action
            )

            notify_task_completed_thread = threading.Thread(
                target=email.notify_task_completed, args=[
                    assignee_email, assignee_name, concurrence_email,
                    concurrence_name, approver_email, approver_name, action,
                    self.is_two_levels_of_approval(), compliance_name
                ]
            )
            notify_task_completed_thread.start()
        return True

    def is_onOccurrence_with_hours(self, compliance_history_id):
        columns = "compliance_id"
        condition = "compliance_history_id = '%d'" % compliance_history_id
        rows = self.get_data(self.tblComplianceHistory, columns, condition)
        compliance_id = rows[0][0]

        comp_columns = "frequency_id, duration_type_id"
        comp_condition = "compliance_id = '%d'" % compliance_id
        comp_rows = self.get_data(self.tblCompliances, comp_columns, comp_condition)
        frequency_id = comp_rows[0][0]
        duration_type_id = comp_rows[0][1]
        if frequency_id == 4 and duration_type_id == 2:
            return True
        else:
            return False

    def save_compliance_notification(
        self, compliance_history_id, notification_text, category, action
    ):
        notification_id = self.get_new_id(
            "notification_id", self.tblNotificationsLog
        )
        current_time_stamp = self.get_date_time()

        # Get history details from compliance history id
        history_columns = "unit_id, compliance_id, completed_by, concurred_by, \
        approved_by"
        history_condition = "compliance_history_id = '%d'" % compliance_history_id
        history_rows = self.get_data(
            self.tblComplianceHistory, history_columns, history_condition
        )
        history_columns_list = [
            "unit_id", "compliance_id", "completed_by",
            "concurred_by", "approved_by"
        ]
        history = self.convert_to_dict(history_rows[0], history_columns_list)
        unit_id = history["unit_id"]
        compliance_id = history["compliance_id"]

        # Getting Unit details from unit_id
        unit_columns = "country_id, business_group_id, legal_entity_id, division_id"
        unit_condition = "unit_id = '%d'" % int(unit_id)
        unit_rows = self.get_data(self.tblUnits, unit_columns, unit_condition)
        unit_columns_list = [
            "country_id", "business_group_id", "legal_entity_id", "division_id"
        ]
        unit = self.convert_to_dict(unit_rows[0], unit_columns_list)

        # Getting compliance_details from compliance_id
        compliance_columns = "domain_id"
        compliance_condition = "compliance_id = '%d'" % compliance_id
        compliance_rows = self.get_data(
            self.tblCompliances, compliance_columns, compliance_condition
        )
        domain_id = compliance_rows[0][0]

        # Saving notification
        columns = [
            "notification_id", "country_id", "domain_id", "business_group_id",
            "legal_entity_id", "division_id", "unit_id", "compliance_id",
            "assignee", "concurrence_person", "approval_person", "notification_type_id",
            "notification_text", "extra_details", "created_on"
        ]
        extra_details = "%d-%s" % (compliance_history_id, category)
        values = [
            notification_id, unit["country_id"], domain_id, unit["business_group_id"],
            unit["legal_entity_id"], unit["division_id"], unit_id, compliance_id,
            history["completed_by"], history["concurred_by"], history["approved_by"],
            1, notification_text, extra_details, current_time_stamp
        ]
        self.insert(self.tblNotificationsLog, columns, values)

        # Saving in user log
        columns = [
            "notification_id", "read_status", "updated_on", "user_id"
        ]
        values = [
            notification_id, 0, current_time_stamp
        ]
        if action.lower() == "concur":
            values.append(int(history["concurred_by"]))
        elif action.lower() == "approve":
            values.append(int(history["approved_by"]))
        elif action.lower() == "concurred":
            values.append(int(history["completed_by"]))
        elif action.lower() == "approvedtoassignee":
            values.append(int(history["completed_by"]))
        elif action.lower() == "approvedtoconcur":
            values.append(int(history["concurred_by"]))
        elif action.lower() == "concurrejected":
            values.append(int(history["completed_by"]))
        elif action.lower() == "approverejectedtoassignee":
            values.append(int(history["completed_by"]))
        elif action.lower() == "approverejectedtoconcur":
            values.append(int(history["concurred_by"]))
        elif action.lower() == "started":
            values.append(int(history["completed_by"]))
        return self.insert(self.tblNotificationUserLog, columns, values)

    def save_compliance_activity(
        self, unit_id, compliance_id, activity_status, compliance_status,
        remarks
    ):
        compliance_activity_id = self.get_new_id(
            "compliance_activity_id", self.tblComplianceActivityLog,
        )
        date = self.get_date_time()
        columns = [
            "compliance_activity_id", "unit_id", "compliance_id",
            "activity_date", "activity_status", "compliance_status",
            "updated_on"
        ]
        values = [
            compliance_activity_id, unit_id, compliance_id, date, activity_status,
            compliance_status,  date
        ]
        if remarks:
            columns.append("remarks")
            values.append(remarks)
        self.insert(
            self.tblComplianceActivityLog, columns, values
        )

    def get_where_query_for_reassigned_history_report(
        self, country_id, domain_id, level_1_statutory_name,
        unit_id, compliance_id, user_id, from_date, to_date, session_user
    ):
        qry_where = ""
        admin_id = self.get_admin_id()
        if level_1_statutory_name is not None :
            qry_where += " AND t3.statutory_mapping like '%s'" % (str(level_1_statutory_name+'%'))
        if unit_id is not None :
            qry_where += " And t1.unit_id = %s" % (unit_id)

        if compliance_id is not None :
            qry_where += " AND t1.compliance_id = %s" % (compliance_id)
        if user_id is not None :
            qry_where += " AND t1.assignee = %s " % (user_id)

        if from_date is not None and to_date is not None :
            start_date = self.string_to_datetime(from_date).date()
            end_date = self.string_to_datetime(to_date).date()
            qry_where += " AND t1.reassigned_date between '%s' and '%s' " % (start_date, end_date)
        elif from_date is not None:
            start_date = self.string_to_datetime(from_date).date()
            qry_where += " AND t1.reassigned_date > DATE_SUB('%s', INTERVAL 1 DAY)" % (start_date)
        elif to_date is not None:
            end_date = self.string_to_datetime(from_date).date()
            qry_where += " AND t1.reassigned_date < DATE_SUB('%s', INTERVAL 1 DAY)" % (end_date)

        if session_user > 0 and session_user != admin_id :
            qry_where += " AND t1.unit_id in \
                (select us.unit_id from tbl_user_units us where \
                    us.user_id = %s\
                )" % int(session_user)
            qry_where += " and t3.domain_id IN \
                (SELECT ud.domain_id FROM tbl_user_domains ud \
                where ud.user_id = %s)" % int(session_user)
        return qry_where


    def get_reassigned_history_report_count(
        self, country_id, domain_id, qry_where
    ):
        qry_count = "SELECT sum(t.c_count) from \
        (SELECT \
            count(distinct t1.compliance_id) c_count \
        FROM \
            tbl_reassigned_compliances_history t1 \
                INNER JOIN \
            tbl_assigned_compliances t2 ON t1.compliance_id = t2.compliance_id \
                AND t1.unit_id = t2.unit_id \
                INNEr JOIN \
            tbl_compliances t3 ON t1.compliance_id = t3.compliance_id \
                INNER JOIN \
            tbl_units t4 ON t1.unit_id = t4.unit_id \
        WHERE \
            t4.country_id = %s AND t3.domain_id = %s \
            %s \
        group by t1.unit_id) t " % (
            country_id, domain_id,
            qry_where,
        )
        rcount = self.select_one(qry_count)
        if rcount[0] :
            count = int(rcount[0])
        else :
            count = 0
        return count

    def get_reassigned_history_report_data(
        self, country_id, domain_id, qry_where,
        from_count, to_count
    ):
        columns = [
            "compliance_id", "assignee", "reassigned_from", "reassigned_date",
            "remarks", "due_date", "compliance_task",
            "document_name", "unit_code", "unit_name", "address",
            "assigneename", "oldassignee", "unit_id", "statutory_mapping"
        ]
        qry = " SELECT distinct t1.compliance_id, t1.assignee, t1.reassigned_from, \
            t1.reassigned_date, t1.remarks, t2.due_date, t3.compliance_task, \
            t3.document_name, t4.unit_code, t4.unit_name, t4.address, \
            ifnull((select concat(a.employee_code, ' - ', a.employee_name) from tbl_users a where a.user_id = t1.assignee), 'Administrator') assigneename, \
            ifnull((select concat(a.employee_code, ' - ', a.employee_name) from tbl_users a where a.user_id = t1.reassigned_from) , 'Administrator') oldassignee, \
            t1.unit_id, t3.statutory_mapping \
            FROM tbl_reassigned_compliances_history t1 \
            INNER JOIN tbl_assigned_compliances t2 on t1.compliance_id = t2.compliance_id \
            AND t1.unit_id = t2.unit_id \
            INNEr JOIN tbl_compliances t3 on t1.compliance_id = t3.compliance_id \
            INNER JOIN tbl_units t4 on t1.unit_id = t4.unit_id \
            WHERE t4.country_id = %s \
            AND t3.domain_id = %s \
            %s \
            order by SUBSTRING_INDEX(SUBSTRING_INDEX(t3.statutory_mapping, '>>', 1), \
            '>>', - 1), t1.unit_id,  t1.reassigned_date desc \
            limit %s, %s" % (
                country_id, domain_id,
                qry_where,
                from_count, to_count

            )
        rows = self.select_all(qry)
        result = self.convert_to_dict(rows, columns)
        return result

    # Reassigned History Report
    def report_reassigned_history(
        self, country_id, domain_id, level_1_statutory_name,
        unit_id, compliance_id, user_id, from_date, to_date, session_user,
        from_count, to_count
    ):
        qry_where = self.get_where_query_for_reassigned_history_report(
            country_id, domain_id, level_1_statutory_name,
            unit_id, compliance_id, user_id, from_date, to_date, session_user
        )
        result = self.get_reassigned_history_report_data(
            country_id, domain_id, qry_where,
            from_count, to_count
        )
        count = self.get_reassigned_history_report_count(
            country_id, domain_id, qry_where
        )
        return self.return_reassinged_history_report(
            result, count
        )

    def return_reassinged_history_report(self, result, total):
        level_wise = {}
        for r in result :
            if r["document_name"] is not None :
                cname = " %s - %s" % (r["document_name"], r["compliance_task"])
            else :
                cname = r["compliance_task"]

            uname = r["unit_code"] + ' - ' + r["unit_name"]
            uid = r["unit_id"]

            mappings = r["statutory_mapping"].split('>>')
            statutory_name = mappings[0].strip()
            statutory_name = statutory_name.strip()

            reassign = clientreport.ReassignHistory(
                r["oldassignee"], r["assigneename"],
                self.datetime_to_string(r["reassigned_date"]),
                r["remarks"]
            )
            reassignCompliance = clientreport.ReassignCompliance(
                cname, self.datetime_to_string(r["due_date"]),
                [reassign]
            )
            unitcompliance = clientreport.ReassignUnitCompliance(
                uid,
                uname,
                r["address"], [reassignCompliance]
            )
            level_unit = level_wise.get(statutory_name)
            if level_unit is None :
                level_unit = clientreport.StatutoryReassignCompliance(
                    statutory_name, [unitcompliance]
                )
            else :
                unitcompliancelst = level_unit.compliance
                if unitcompliancelst is None :
                    unitcompliancelst = []
                u_new = True
                for c in unitcompliancelst :
                    if uid == c.unit_id :
                        u_new = False
                        reassing_compliance_lst = c.reassign_compliances
                        if reassing_compliance_lst is None :
                            reassing_compliance_lst = []
                        r_new = True
                        for r in reassing_compliance_lst :
                            if cname == r.compliance_name :
                                r_new = False
                                history_lst = r.reassign_history
                                if history_lst is None :
                                    history_lst = []
                                history_lst.append(reassign)
                                r.reassign_history = history_lst
                        if r_new is True :
                            reassing_compliance_lst.append(reassignCompliance)
                if u_new is True :
                    unitcompliancelst.append(unitcompliance)
                level_unit.compliance = unitcompliancelst
            level_wise[statutory_name] = level_unit
        final_list = []
        for k in sorted(level_wise) :
            final_list.append(level_wise.get(k))
        return final_list, total

    # login trace

    def get_login_trace(
        self, client_id, session_user, from_count, to_count, user_id,
        from_date, to_date
    ):
        from_date = self.string_to_datetime(from_date).date()
        to_date = self.string_to_datetime(to_date).date()
        condition = "1"
        if user_id is not None:
            condition = " al.user_id = '%d' " % user_id
        if from_date is not None and to_date is not None:
            condition += " AND  date(al.created_on) between '%s' AND '%s'" % (
                from_date, to_date
            )

        query = "SELECT al.created_on, al.action \
            FROM tbl_activity_log al \
            INNER JOIN \
            tbl_users u ON \
            al.user_id  = u.user_id \
            WHERE \
            al.form_id = 0 and al.action not like '%s%s%s'\
            AND %s\
            order by al.created_on desc \
            limit %s, %s" % (
                "%", "password", "%", condition,
                from_count, to_count
            )
        rows = self.select_all(query)
        columns = ["created_on", "action"]
        result = self.convert_to_dict(rows, columns)
        return self.return_logintrace(result)

    def return_logintrace(self, data) :
        results = []
        for d in data :
            created_on = self.datetime_to_string_time(d["created_on"])
            results.append(clientreport.LoginTrace(created_on, d["action"]))
        return results

#
#   Compliance Activity Report
#
    def get_compliance_activity_report(
        self, country_id, domain_id, user_type, user_id, unit_id, compliance_id,
        level_1_statutory_name, from_date, to_date, session_user, client_id
    ):
        conditions = []
        #user_type_condition
        if user_type == "Inhouse":
            conditions.append("us.service_provider_id is null or us.service_provider_id = 0")
        else:
            conditions.append("us.service_provider_id = 1")

        #session_user_condition
        if session_user != 0:
            conditions.append(
                '''
                u.unit_id in (
                    SELECT unit_id FROM tbl_user_units WHERE user_id = {}
                ) '''.format(session_user)
            )
        else:
           conditions.append(
                '''
                u.unit_id in (
                    SELECT unit_id FROM tbl_units
                ) '''.format(session_user)
            )

        # assignee_condition
        if user_id is not None:
            conditions.append("ac.assignee = {}".format(user_id))


        # unit_condition
        if unit_id is not None:
            conditions.append("cal.unit_id = {}".format(unit_id))

        # level_1_statutory_condition
        if level_1_statutory_name is not None:
            conditions.append(
                "c.statutory_mapping like '%{}%'".format(
                    level_1_statutory_name
                )
            )

        # compliance_name_condition
        if compliance_id is not None:
            conditions.append(
                "compliance_task = (SELECT compliance_task FROM tbl_compliances WHERE \
                    compliance_id = '%d')" % compliance_id
            )

        #timeline_condition
        # [[1, [[1, [{'start_date': datetime.datetime(2016, 5, 1, 5, 30), 'end_date': datetime.datetime(2016, 12, 31, 5, 30), 'year': 2016}]]]]]
        timeline = self.get_country_domain_timelines(
            [country_id], [domain_id], [self.get_date_time().year], client_id
        )
        year_start_date = timeline[0][1][0][1][0]["start_date"]
        year_end_date = timeline[0][1][0][1][0]["end_date"]
        if from_date is not None and to_date is not None:
            conditions.append(
                "cal.updated_on between '{}' and DATE_ADD('{}', INTERVAL 1 DAY)".format(
                   self.string_to_datetime(from_date).date(), self.string_to_datetime(to_date).date()
                )
            )
        elif from_date is not None and to_date is None:
            conditions.append(
                "cal.updated_on between '{}' and DATE_ADD('{}', INTERVAL 1 DAY)".format(
                   self.string_to_datetime(from_date).date(), year_end_date
                )
            )
        elif from_date is None and to_date is not None:
            conditions.append(
                "cal.updated_on between '{}' and DATE_ADD('{}', INTERVAL 1 DAY)".format(
                   year_start_date, self.string_to_datetime(to_date).date()
                )
            )
        else:
            conditions.append(
                "cal.updated_on between '{}' and DATE_ADD('{}', INTERVAL 1 DAY)".format(
                   year_start_date, year_end_date
                )
            )

        query = '''SELECT activity_date, activity_status, compliance_status, remarks, concat(unit_code, "-", unit_name),
                address, document_name, compliance_task, compliance_description, statutory_mapping, ac.assignee,
                employee_code, employee_name
                FROM tbl_compliance_activity_log cal
                INNER JOIN tbl_compliances c ON (c.compliance_id = cal.compliance_id)
                INNER JOIN tbl_units u ON (u.unit_id = cal.unit_id)
                INNER JOIN tbl_assigned_compliances ac ON ((cal.compliance_id = ac.compliance_id) and (cal.unit_id = ac.unit_id))
                INNER JOIN tbl_users us ON (us.user_id = ac.assignee)
                WHERE u.country_id = '{}'
                AND c.domain_id = '{}'
                AND {} ORDER BY cal.updated_on DESC'''.format(
                    country_id, domain_id, " AND ".join(conditions)
                )
        result = self.select_all(query)
        columns = [
            "activity_date", "activity_status", "compliance_status", "remarks",
            "unit_name", "address", "document_name", "compliance_name", "description",
            "statutory_mapping", "assignee_id", "employee_code", "employee_name"
        ]
        rows = self.convert_to_dict(result, columns)
        return rows


    def return_compliance_activity_report(
        self, country_id, domain_id, user_type, user_id,
        unit_id, compliance_id,
        level_1_statutory_name, from_date, to_date,
        session_user, client_id
    ):
        rows = self.get_compliance_activity_report(
            country_id, domain_id, user_type, user_id,
            unit_id, compliance_id,
            level_1_statutory_name, from_date, to_date,
            session_user, client_id
        )
        unit_wise_activities = {}
        unit_address_mapping = {}
        for row in rows:
            unit_name = row["unit_name"]
            if unit_name not in unit_address_mapping:
                unit_address_mapping[unit_name] = row["address"]
            if unit_name not in unit_wise_activities:
                unit_wise_activities[row["unit_name"]] = {}

            statutories = row["statutory_mapping"].split(">>")
            level_1_statutory = statutories[0]
            if level_1_statutory not in unit_wise_activities[unit_name]:
                unit_wise_activities[unit_name][level_1_statutory] = {}

            compliance_name = row["compliance_name"]
            if row["document_name"] not in [None, "None", ""]:
                compliance_name = "%s - %s" % (row["document_name"], compliance_name)

            if compliance_name not in unit_wise_activities[unit_name][level_1_statutory]:
                unit_wise_activities[unit_name][level_1_statutory][compliance_name] = []

            employee_name = row["employee_name"]
            if row["employee_code"] not in ["None", None, ""]:
                employee_name = "%s - %s" % (row["employee_code"], employee_name)
            if row["activity_status"] == "Submited":
                row["activity_status"] = "Submitted"
            unit_wise_activities[unit_name][level_1_statutory][compliance_name].append(
                clientreport.ActivityData(
                    activity_date=self.datetime_to_string(row["activity_date"]),
                    activity_status=core.COMPLIANCE_ACTIVITY_STATUS(row["activity_status"]),
                    compliance_status=core.COMPLIANCE_STATUS(row["compliance_status"]),
                    remarks=row["remarks"],
                    assignee_name=employee_name
                )
            )

        activities = []
        for unit in unit_wise_activities:
            activities.append(
                clientreport.Activities(
                    unit_name=unit,
                    address=unit_address_mapping[unit],
                    statutory_wise_compliances=unit_wise_activities[unit]
                )
            )
        return activities

#
#   Assigee wise compliance chart
#
    def get_assigneewise_compliances_list(
        self, country_id, business_group_id, legal_entity_id, division_id,
        unit_id, session_user, client_id, assignee_id
    ):
        condition = "tu.country_id = '%d'" % country_id
        if business_group_id is not None:
            condition += " AND tu.business_group_id = '%d'" % (business_group_id)
        if legal_entity_id is not None:
            condition += " AND tu.legal_entity_id = '%d'" % (legal_entity_id)
        if division_id is not None:
            condition += " AND tu.division_id = '%d'" % (division_id)
        if unit_id is not None:
            condition += " AND tu.unit_id = '%d'" % (unit_id)
        else:
            condition += " AND tu.unit_id in (%s)" % (
                self.get_user_unit_ids(session_user)
            )
        if assignee_id is not None:
            condition += " AND tch.completed_by = '%d'" % (assignee_id)
        domain_ids = self.get_user_domains(session_user)
        domain_ids_list = [int(x) for x in domain_ids.split(",")]
        current_date = self.get_date_time()
        result = {}
        for domain_id in domain_ids_list:
            timelines = self.get_country_domain_timelines(
                    [country_id], [domain_id], [current_date.year], client_id
            )
            from_date = timelines[0][1][0][1][0]["start_date"].date()
            to_date = timelines[0][1][0][1][0]["end_date"].date()

            query = '''
                SELECT concat(IFNULL(employee_code, 'Administrator'), '-', employee_name)
                as Assignee, tch.completed_by, tch.unit_id,
                concat(unit_code, '-', unit_name) as Unit, address, tc.domain_id,
                (SELECT domain_name FROM tbl_domains td WHERE tc.domain_id = td.domain_id) as Domain,
                sum(case when (approve_status = 1 and (tch.due_date > completion_date or
                    tch.due_date = completion_date)) then 1 else 0 end) as complied,
                sum(case when ((approve_status = 0 or approve_status is null) and
                    tch.due_date > now()) then 1 else 0 end) as Inprogress,
                sum(case when ((approve_status = 0 or approve_status is null) and
                    tch.due_date < now()) then 1 else 0 end) as NotComplied,
                sum(case when (approve_status = 1 and completion_date > tch.due_date and
                    (is_reassigned = 0 or is_reassigned is null) )
                    then 1 else 0 end) as DelayedCompliance ,
                sum(case when (approve_status = 1 and completion_date > tch.due_date and (is_reassigned = 1))
                    then 1 else 0 end) as DelayedReassignedCompliance
                FROM tbl_compliance_history tch
                INNER JOIN tbl_assigned_compliances tac ON (
                tch.compliance_id = tac.compliance_id AND tch.unit_id = tac.unit_id)
                INNER JOIN tbl_units tu ON (tac.unit_id = tu.unit_id)
                INNER JOIN tbl_users tus ON (tus.user_id = tac.assignee)
                INNER JOIN tbl_compliances tc ON (tac.compliance_id = tc.compliance_id)
                WHERE %s AND domain_id = '%d' AND tch.due_date BETWEEN '%s' AND '%s'
                group by completed_by, tch.unit_id;
            ''' % (
                condition, domain_id, from_date, to_date
            )
            rows = self.select_all(query)
            columns = [
                "assignee", "completed_by", "unit_id", "unit_name", "address", "domain_id",
                "domain_name", "complied", "inprogress", "not_complied", "delayed",
                "delayed_reassigned"
            ]
            assignee_wise_compliances = self.convert_to_dict(rows, columns)

            for compliance in assignee_wise_compliances:
                unit_name = compliance["unit_name"]
                assignee = compliance["assignee"]
                if unit_name not in result:
                    result[unit_name] = {
                        "unit_id": compliance["unit_id"],
                        "address" : compliance["address"],
                        "assignee_wise" : {}
                    }
                if assignee not in result[unit_name]["assignee_wise"]:
                    result[unit_name]["assignee_wise"][assignee] = {
                        "user_id": compliance["completed_by"],
                        "domain_wise" : []
                    }
                total_compliances = int(compliance["complied"]) + int(compliance["inprogress"])
                total_compliances += int(compliance["delayed"]) + int(compliance["delayed_reassigned"])
                total_compliances += int(compliance["not_complied"])
                result[unit_name]["assignee_wise"][assignee]["domain_wise"].append(
                    dashboard.DomainWise(
                        domain_id=domain_id,
                        domain_name=compliance["domain_name"],
                        total_compliances=total_compliances,
                        complied_count=int(compliance["complied"]),
                        assigned_count=int(compliance["delayed"]),
                        reassigned_count=int(compliance["delayed_reassigned"]),
                        inprogress_compliance_count=int(compliance["inprogress"]),
                        not_complied_count=int(compliance["not_complied"])
                    )
                )
        chart_data = []
        for unit_name in result:
            assignee_wise_compliances_count = []
            for assignee in result[unit_name]["assignee_wise"]:
                result[unit_name]["assignee_wise"][assignee]["domain_wise"]
                assignee_wise_compliances_count.append(
                    dashboard.AssigneeWiseDetails(
                        user_id=result[unit_name]["assignee_wise"][assignee]["user_id"],
                        assignee_name=assignee,
                        domain_wise_details=result[unit_name]["assignee_wise"][assignee]["domain_wise"]
                    )
                )
            if len(assignee_wise_compliances_count) > 0:
                chart_data.append(
                    dashboard.AssigneeChartData(
                        unit_name=unit_name,
                        unit_id=result[unit_name]["unit_id"],
                        address=result[unit_name]["address"],
                        assignee_wise_details=assignee_wise_compliances_count
                    )
                )
        return chart_data

    def get_assigneewise_yearwise_compliances(
        self, country_id, unit_id, user_id, client_id
    ):
        current_year = self.get_date_time().year
        domain_ids = [int(x) for x in self.get_user_domains(user_id).split(",")]
        start_year = current_year - 5
        iter_year = start_year
        year_wise_compliance_count = []
        while iter_year <= current_year:
            domain_ids = self.get_user_domains(user_id)
            domain_ids_list = [int(x) for x in domain_ids.split(",")]
            domainwise_complied = 0
            domainwise_inprogress = 0
            domainwise_notcomplied = 0
            domainwise_total = 0
            domainwise_delayed = 0
            for domain_id in domain_ids_list:
                result = self.get_country_domain_timelines(
                        [country_id], [domain_id], [iter_year], client_id
                )
                from_date = result[0][1][0][1][0]["start_date"].date()
                to_date = result[0][1][0][1][0]["end_date"].date()
                query = '''
                    SELECT tc.domain_id,
                    sum(case when (approve_status = 1 and (tch.due_date > completion_date or
                        tch.due_date = completion_date)) then 1 else 0 end) as complied,
                    sum(case when ((approve_status = 0 or approve_status is null) and
                        tch.due_date > now()) then 1 else 0 end) as Inprogress,
                    sum(case when ((approve_status = 0 or approve_status is null) and
                        tch.due_date < now()) then 1 else 0 end) as NotComplied,
                    sum(case when (approve_status = 1 and completion_date > tch.due_date and
                        (is_reassigned = 0 or is_reassigned is null) )
                        then 1 else 0 end) as DelayedCompliance ,
                    sum(case when (approve_status = 1 and completion_date > tch.due_date and (is_reassigned = 1))
                        then 1 else 0 end) as DelayedReassignedCompliance
                    FROM tbl_compliance_history tch
                    INNER JOIN tbl_assigned_compliances tac ON (
                    tch.compliance_id = tac.compliance_id AND tch.unit_id = tac.unit_id
                    AND tch.completed_by = '%s')
                    INNER JOIN tbl_units tu ON (tac.unit_id = tu.unit_id)
                    INNER JOIN tbl_users tus ON (tus.user_id = tac.assignee)
                    INNER JOIN tbl_compliances tc ON (tac.compliance_id = tc.compliance_id)
                    INNER JOIN tbl_domains td ON (td.domain_id = tc.domain_id)
                    WHERE tch.unit_id = '%d' AND tc.domain_id = '%d'
                    AND tch.due_date between '%s' AND '%s';
                ''' % (
                    user_id, unit_id, int(domain_id), from_date, to_date
                )
                rows = self.select_all(query)
                if rows:
                    convert_columns = ["domain_id", "complied", "inprogress", "not_complied",
                    "delayed", "delayed_reassigned"]
                    count_rows = self.convert_to_dict(rows, convert_columns)
                    for row in count_rows:
                        domainwise_complied += 0 if row["complied"] is None else int(row["complied"])
                        domainwise_inprogress += 0 if row["inprogress"] is None else int(row["inprogress"])
                        domainwise_notcomplied += 0 if row["not_complied"] is None else int(row["not_complied"])
                        domainwise_delayed += 0 if row["delayed"] is None else  int(row["delayed"])
                        domainwise_delayed += 0 if row["delayed_reassigned"] is None else  int(row["delayed_reassigned"])
                        domainwise_total += domainwise_complied + domainwise_inprogress
                        domainwise_total += domainwise_notcomplied + domainwise_delayed

            year_wise_compliance_count.append(
                dashboard.YearWise(
                    year=str(iter_year),
                    total_compliances=domainwise_total,
                    complied_count=domainwise_complied,
                    delayed_compliance=domainwise_delayed,
                    inprogress_compliance_count=domainwise_inprogress,
                    not_complied_count=domainwise_notcomplied
                )
            )
            iter_year += 1
        return year_wise_compliance_count

    def get_assigneewise_reassigned_compliances(
        self, country_id, unit_id, user_id, domain_id, client_id
    ):
        current_year = self.get_date_time().year
        result = self.get_country_domain_timelines(
                [country_id], [domain_id], [current_year], client_id
        )
        from_date = result[0][1][0][1][0]["start_date"].date()
        to_date = result[0][1][0][1][0]["end_date"].date()
        query = '''
            SELECT reassigned_date, concat(IFNULL(employee_code, 'Administrator'), '-',
            employee_name) as previous_assignee, document_name, compliance_task,
            tch.due_date, DATE_SUB(tch.due_date, INTERVAL trigger_before_days DAY) as start_date,
            completion_date
            FROM %s trch INNER JOIN
            tbl_compliance_history tch ON (trch.compliance_id = tch.compliance_id
            AND assignee='%d' AND trch.unit_id = tch.unit_id)
            INNER JOIN tbl_assigned_compliances tac ON (
            tch.compliance_id = tac.compliance_id AND tch.unit_id = tac.unit_id
            AND tch.completed_by = '%s')
            INNER JOIN tbl_units tu ON (tac.unit_id = tu.unit_id)
            INNER JOIN tbl_users tus ON (tus.user_id = tac.assignee)
            INNER JOIN tbl_compliances tc ON (tac.compliance_id = tc.compliance_id)
            INNER JOIN tbl_domains td ON (td.domain_id = tc.domain_id)
            WHERE tch.unit_id = '%d' AND tc.domain_id = '%d'
            AND approve_status = 1 AND completed_by = '%d'
            AND reassigned_date between tch.due_date and completion_date
            AND completion_date > tch.due_date AND is_reassigned = 1
            AND tch.due_date between '%s' AND '%s'
        ''' % (
            self.tblReassignedCompliancesHistory, user_id, user_id, unit_id,
            int(domain_id), user_id, from_date, to_date
        )
        rows = self.select_all(query)
        columns = ["reassigned_date", "reassigned_from", "document_name",
        "compliance_name", "due_date", "start_date", "completion_date"]
        results = self.convert_to_dict(rows, columns)
        reassigned_compliances = []
        for compliance in results:
            compliance_name = compliance["compliance_name"]
            if compliance["document_name"] is not None:
                compliance_name = "%s - %s" % (
                    compliance["document_name"], compliance_name
                )
            reassigned_compliances.append(
                dashboard.RessignedCompliance(
                    compliance_name=compliance_name,
                    reassigned_from=compliance["reassigned_from"],
                    start_date=self.datetime_to_string(compliance["start_date"]),
                    due_date=self.datetime_to_string(compliance["due_date"]),
                    reassigned_date=self.datetime_to_string(compliance["reassigned_date"]),
                    completed_date=self.datetime_to_string(compliance["completion_date"])
                )
            )
        return reassigned_compliances

    def get_assigneewise_compliances_drilldown_data_count(
        self, country_id, assignee_id, domain_id, client_id, year, unit_id,
        session_user
    ):
        domain_id_list = []
        if domain_id is None:
            domain_ids = self.get_user_domains(session_user)
            domain_id_list = [int(x) for x in domain_ids.split(",")]
        else:
            domain_id_list = [domain_id]

        if year is None:
            current_year = self.get_date_time().year
        else:
            current_year = year
        result = self.get_country_domain_timelines(
            [country_id], [domain_id], [current_year], client_id
        )
        from_date = datetime.datetime(current_year, 1, 1)
        to_date = datetime.datetime(current_year, 12, 31)
        domain_condition = ",".join(str(x) for x in domain_id_list)
        if len(domain_id_list) == 1:
            result = self.get_country_domain_timelines(
                [country_id], domain_id_list, [current_year], client_id
            )
            from_date = result[0][1][0][1][0]["start_date"]
            to_date = result[0][1][0][1][0]["end_date"]
            domain_condition = str(domain_id_list[0])
        query = '''SELECT count(*)
        FROM %s tch
        INNER JOIN %s tc ON (tch.compliance_id = tc.compliance_id)
        INNER JOIN %s tu ON (tch.completed_by = tu.user_id)
        WHERE completed_by = '%d' AND unit_id = '%d'
        AND due_date BETWEEN '%s' AND '%s '
        AND domain_id in (%s)
        ''' % (
            self.tblComplianceHistory, self.tblCompliances, self.tblUsers,
            assignee_id, unit_id, from_date, to_date, domain_condition
        )
        rows = self.select_all(query)
        return rows[0][0]

    def get_assigneewise_compliances_drilldown_data(
        self, country_id, assignee_id, domain_id, client_id, year, unit_id,
        start_count, to_count, session_user
    ):
        domain_id_list = []
        if domain_id is None:
            domain_ids = self.get_user_domains(session_user)
            domain_id_list = [int(x) for x in domain_ids.split(",")]
        else:
            domain_id_list = [domain_id]

        if year is None:
            current_year = self.get_date_time().year
        else:
            current_year = year
        from_date = datetime.datetime(current_year, 1, 1)
        to_date = datetime.datetime(current_year, 12, 31)
        domain_condition = ",".join(str(x) for x in domain_id_list)
        if len(domain_id_list) == 1:
            result = self.get_country_domain_timelines(
                [country_id], domain_id_list, [current_year], client_id
            )
            from_date = result[0][1][0][1][0]["start_date"]
            to_date = result[0][1][0][1][0]["end_date"]
            domain_condition = str(domain_id_list[0])
        columns = '''tch.compliance_id, start_date, due_date, completion_date,
                document_name, compliance_task, compliance_description,
                statutory_mapping, concat(IFNULL(employee_code, 'Administrator'),
                '-', employee_name)'''
        subquery_columns = '''
            IF(
                (approve_status = 1 and completion_date <= due_date),
                "Complied",
                (
                    IF(
                        (approve_status = 1 and completion_date > due_date),
                        "Delayed",
                        (
                            IF (
                                 ((approve_status = 0 or approve_status is null) and
                                due_date > now()),
                                "Inprogress",
                                "NotComplied"
                            )
                        )
                    )
                )
            ) as compliance_status
        '''
        query = '''SELECT %s, %s
        FROM %s tch
        INNER JOIN %s tc ON (tch.compliance_id = tc.compliance_id)
        INNER JOIN %s tu ON (tch.completed_by = tu.user_id)
        WHERE completed_by = '%d' AND unit_id = '%d'
        AND due_date BETWEEN '%s' AND '%s'
        AND domain_id in (%s)
        ORDER BY compliance_status
        LIMIT %d, %d
        ''' % (
            columns, subquery_columns, self.tblComplianceHistory,
            self.tblCompliances, self.tblUsers, assignee_id, unit_id,
            from_date, to_date, domain_condition, int(start_count), to_count
        )
        rows = self.select_all(query)
        columns_list = [
            "compliance_id", "start_date", "due_date", "completion_date",
            "document_name", "compliance_name", "compliance_description",
            "statutory_mapping", "assignee", "compliance_status"
        ]
        result = self.convert_to_dict(rows, columns_list)

        complied_compliances = {}
        inprogress_compliances = {}
        delayed_compliances = {}
        not_complied_compliances = {}

        for compliance in result:
            compliance_name = compliance["compliance_name"]
            compliance_status = compliance["compliance_status"]
            if compliance["document_name"] is not None:
                compliance_name = "%s - %s" % (
                    compliance["document_name"], compliance_name
                )
            level_1_statutory = compliance["statutory_mapping"].split(">>")[0]

            current_list = not_complied_compliances
            if compliance_status == "Complied":
                current_list = complied_compliances
            elif compliance_status == "Delayed":
                current_list = delayed_compliances
            elif compliance_status == "Inprogress":
                current_list = inprogress_compliances

            if level_1_statutory not in current_list:
                current_list[level_1_statutory] = []

            current_list[level_1_statutory].append(
                dashboard.AssigneeWiseLevel1Compliance(
                    compliance_name=compliance_name,
                    description=compliance["compliance_description"],
                    assignee_name=compliance["assignee"],
                    assigned_date=None if compliance["start_date"] is None else self.datetime_to_string(compliance["start_date"]),
                    due_date=self.datetime_to_string(compliance["due_date"]),
                    completion_date=None if compliance["completion_date"] is None else self.datetime_to_string(compliance["completion_date"])
                )
            )
        return (
            complied_compliances, delayed_compliances, inprogress_compliances,
            not_complied_compliances
        )

    def get_client_details_condition(
        self, country_id,  business_group_id, legal_entity_id, division_id,
        unit_id, domain_ids, session_user
    ):
        user_unit_ids = self.get_user_unit_ids(session_user)
        condition = "u.country_id = '%d' " % (country_id)
        if business_group_id is not None:
            condition += " AND u.business_group_id = '%d'" % business_group_id
        if legal_entity_id is not None:
            condition += " AND u.legal_entity_id = '%d'" % legal_entity_id
        if division_id is not None:
            condition += " AND u.division_id = '%d'" % division_id
        if unit_id is not None:
            condition += " AND unit_id = '%d'" % unit_id
        else:
            condition += " AND unit_id in (%s)" % user_unit_ids
        if domain_ids is not None:
            for domain_id in domain_ids:
                condition += " AND  ( domain_ids LIKE  '%,"+str(domain_id)+",%' "+\
                            "or domain_ids LIKE  '%,"+str(domain_id)+"' "+\
                            "or domain_ids LIKE  '"+str(domain_id)+",%'"+\
                            " or domain_ids LIKE '"+str(domain_id)+"') "
        return condition

    def get_client_details_count(
        self, country_id,  business_group_id, legal_entity_id, division_id,
        unit_id, domain_ids, session_user
    ):

        condition = self.get_client_details_condition(
            country_id,  business_group_id, legal_entity_id, division_id,
            unit_id, domain_ids, session_user
        )
        query = "SELECT count(*) \
                FROM %s u \
                WHERE %s " % (
                    self.tblUnits, condition
                )
        rows = self.select_all(query)
        count = 0
        if rows:
            count = rows[0][0]
        return count

    def get_client_details_report(
        self, country_id,  business_group_id, legal_entity_id, division_id,
        unit_id, domain_ids, session_user, start_count, to_count
    ):
        condition = self.get_client_details_condition(
            country_id,  business_group_id, legal_entity_id, division_id,
            unit_id, domain_ids, session_user
        )
        columns = "unit_id, unit_code, unit_name, geography, "\
                "address, domain_ids, postal_code, business_group_name,\
                legal_entity_name, division_name"
        query = "SELECT %s \
                FROM %s u \
                LEFT JOIN %s b ON (b.business_group_id = u.business_group_id)\
                INNER JOIN %s l ON (l.legal_entity_id = u.legal_entity_id) \
                LEFT JOIN %s d ON (d.division_id = u.division_id) \
                WHERE %s \
                ORDER BY u.business_group_id, u.legal_entity_id, u.division_id, \
                u.unit_id ASC LIMIT %d, %d" % (
                    columns, self.tblUnits, self.tblBusinessGroups,
                    self.tblLegalEntities, self.tblDivisions, condition,
                    int(start_count), to_count
                )
        rows = self.select_all(query)
        columns_list = columns.replace(" ", "").split(",")
        unit_rows = self.convert_to_dict(rows, columns_list)
        units = []
        grouped_units = {}
        for unit in unit_rows:
            business_group_name = unit["business_group_name"]
            legal_entity_name = unit["legal_entity_name"]
            division_name = unit["division_name"]
            if business_group_name in ["None", None, ""]:
                business_group_name = "null"
            if division_name in ["None", None, ""]:
                division_name = "null"
            if business_group_name not in grouped_units:
                grouped_units[business_group_name] = {}
            if legal_entity_name not in grouped_units[business_group_name]:
                grouped_units[business_group_name][legal_entity_name] = {}
            if division_name not in grouped_units[business_group_name][legal_entity_name]:
                grouped_units[business_group_name][legal_entity_name][division_name] = []

            grouped_units[business_group_name][legal_entity_name][division_name].append(
                clientreport.UnitDetails(
                    unit["unit_id"], unit["geography"], unit["unit_code"],
                    unit["unit_name"], unit["address"], unit["postal_code"],
                    [int(x) for x in unit["domain_ids"].split(",")]
                )
            )
        GroupedUnits = []
        for business_group in grouped_units:
            for legal_entity_name in grouped_units[business_group]:
                for division in grouped_units[business_group][legal_entity_name]:
                    if business_group == "null":
                        business_group_name = None
                    else:
                        business_group_name = business_group
                    if division == "null":
                        division_name = None
                    else:
                        division_name = division
                    GroupedUnits.append(
                        clientreport.GroupedUnits(
                            division_name, legal_entity_name, business_group_name,
                            grouped_units[business_group][legal_entity_name][division]
                        )
                    )
        return GroupedUnits
#
#   Email
#

# Task Rejected notification

    def get_user_email_name(self, user_ids):
        user_id_list = [int(x) for x in user_ids.split(",")]
        admin_email = None
        index = None
        if 0 in user_id_list:
            index = user_id_list.index(0)
            column = "username"
            admin_rows = self.get_data(self.tblAdmin, column, "1")
            user_id_list.remove(0)
            admin_email = admin_rows[0][0]
        column = "email_id, employee_name"
        condition = "user_id in (%s)" % ",".join(str(x) for x in user_ids)
        rows = self.get_data(
            self.tblUsers, column, condition
        )
        email_ids = ""
        employee_name = ""
        for index, row in enumerate(rows):
            if index == 0:
                if row[1] is not None:
                    employee_name += "%s" % row[1]
                email_ids += "%s" % row[0]
            else:
                if row[1] is not None:
                    employee_name += ", %s" % row[1]
                email_ids += ", %s" % row[0]
        if admin_email is not None:
            employee_name += "Administrator"
            email_ids += admin_email

        return email_ids, employee_name

    def get_compliance_history_details(self, compliance_history_id):
        columns = "completed_by, ifnull(concurred_by, 0), approved_by, ( \
            select compliance_task from %s c \
            where c.compliance_id = ch.compliance_id ), \
            (select document_name from %s c \
            where c.compliance_id = ch.compliance_id ), due_date" % (
                self.tblCompliances, self.tblCompliances)
        condition = "compliance_history_id = '%d'" % compliance_history_id
        rows = self.get_data(self.tblComplianceHistory + " ch", columns, condition)
        if rows:
            return rows[0]

    def get_on_occurrence_compliance_count(
        self, session_user, user_domain_ids, user_unit_ids
    ):
        query = "SELECT count(*) \
                FROM %s ac \
                INNER JOIN %s c ON (ac.compliance_id = c.compliance_id)\
                INNER JOIN %s u ON (ac.unit_id = u.unit_id) \
                WHERE u.is_closed = 0 \
                AND ac.unit_id in (%s)\
                AND c.domain_id in (%s) \
                AND c.frequency_id = 4 \
                AND ac.assignee = '%d' " % (
                    self.tblAssignedCompliances,
                    self.tblCompliances, self.tblUnits, user_unit_ids,
                    user_domain_ids, session_user
                )
        rows = self.select_all(query)
        return rows[0][0]

    def get_on_occurrence_compliances_for_user(
        self, session_user, user_domain_ids, user_unit_ids, start_count,
        to_count
    ):
        columns = "ac.compliance_id, c.statutory_provision,\
                compliance_task, compliance_description, \
                duration_type, duration, document_name, u.unit_id"
        concat_columns = "concat(unit_code, '-', unit_name)"
        query = "SELECT %s, %s \
                FROM %s ac \
                INNER JOIN %s c ON (ac.compliance_id = c.compliance_id)\
                INNER JOIN %s cd ON (c.duration_type_id = cd.duration_type_id) \
                INNER JOIN %s u ON (ac.unit_id = u.unit_id) \
                WHERE u.is_closed = 0 \
                AND ac.unit_id in (%s)\
                AND c.domain_id in (%s) \
                AND c.frequency_id = 4 \
                AND ac.assignee = '%d' \
                ORDER BY u.unit_id, document_name, compliance_task \
                LIMIT %d, %d" % (
                    columns, concat_columns, self.tblAssignedCompliances,
                    self.tblCompliances, self.tblComplianceDurationType,
                    self.tblUnits, user_unit_ids, user_domain_ids,
                    session_user, int(start_count), to_count
                )
        rows = self.select_all(query)
        columns_list = columns.replace(" ", "").split(",")
        columns_list += ["unit_name"]
        result = self.convert_to_dict(rows, columns_list)
        compliances = []
        unit_wise_compliances = {}
        for row in result:
            duration = "%s %s" % (row["duration"], row["duration_type"])
            compliance_name = row["compliance_task"]
            if row["document_name"] not in ["None", "", None]:
                compliance_name = "%s - %s" % (
                    row["document_name"], compliance_name
                )
            unit_name = row["unit_name"]
            if unit_name not in unit_wise_compliances:
                unit_wise_compliances[unit_name] = []
            unit_wise_compliances[unit_name].append(
                clientuser.ComplianceOnOccurrence(
                    row["ac.compliance_id"], row["c.statutory_provision"],
                    compliance_name, row["compliance_description"],
                    duration, row["u.unit_id"]
                )
            )
        return unit_wise_compliances

    def get_compliance_task_applicability(self, request, session_user):
        business_group = request.business_group_id
        legal_entity = request.legal_entity_id
        division_id = request.division_id
        unit = request.unit_id
        from_count = request.record_count
        to_count = 100
        statutory_name = request.statutory_name
        status = request.applicable_status

        def statutory_repeat_text(statutory_dates, repeat, repeat_type) :
            trigger_days = ""
            repeats_text = ""
            for index, dat in enumerate(statutory_dates) :
                if dat["statutory_month"] is not None :
                    day = dat["statutory_date"]
                    if day == 1 :
                        day = "1st"
                    elif day == 2 :
                        day = "2nd"
                    else :
                        day = "%sth" % (day)
                    month = self.string_months[dat["statutory_month"]]
                    days = dat["trigger_before_days"]
                    if index == 0 :
                        repeats_text += " %s %s" % (day, month)
                        trigger_days += " %s days" % (days)
                    else :
                        repeats_text += " %s %s" % (day, month)
                        trigger_days += " and %s days" % (days)

            if repeats_text == "" :
                repeats_text = "Every %s %s" % (repeat, repeat_type)
            else :
                repeats_text = "Every %s" % (repeats_text)

            if trigger_days is not "" :
                trigger_days = "triggers (%s)" % (trigger_days)
            result = "%s %s" % (repeats_text, trigger_days)
            return result

        def statutory_duration_text(duration, duration_type):
            result = "To complete within %s %s" % (duration, duration_type)
            return result

        where_qry = ""

        admin_id = self.get_admin_id()

        if status.lower() == "applicable" :
            where_qry += " AND T1.statutory_applicable = 1"
        elif status.lower() == "not applicable":
            where_qry += " AND T1.statutory_applicable = 0"
        else :
            where_qry += " AND T1.compliance_opted = 0"

        if business_group is not None :
            where_qry = " AND T4.business_group_id = %s" % (business_group)

        if legal_entity is not None :
            where_qry += " AND T4.legal_entity_id = %s" % (legal_entity)

        if division_id is not None :
            where_qry += " AND T4.division_id = %s" % (division_id)

        if unit is not None :
            where_qry += " AND T3.unit_id = %s" % (unit)

        if statutory_name is not None :
            where_qry += " AND T2.statutory_mapping like '%s'" % (statutory_name + '%')

        if session_user > 0 and session_user != admin_id :
            where_qry += " AND T4.unit_id in \
                (select us.unit_id from tbl_user_units us where \
                    us.user_id = %s\
                )" % int(session_user)

        act_wise = {}

        q_count = "SELECT count( T2.compliance_id) \
            FROM tbl_client_compliances T1 \
            INNER JOIN tbl_compliances T2 \
            ON T1.compliance_id = T2.compliance_id \
            INNER JOIN tbl_client_statutories T3 \
            ON T1.client_statutory_id = T3.client_statutory_id \
            INNER JOIN tbl_units T4 \
            ON T3.unit_id = T4.unit_id \
            WHERE T3.country_id = %s \
            AND T3.domain_id = %s \
            %s \
            " % (
                request.country_id,
                request.domain_id,
                where_qry
            )
        row = self.select_one(q_count)
        if row :
            total = int(row[0])
        else :
            total = 0

        query = "SELECT distinct T2.compliance_id, T2.statutory_provision, T2.statutory_mapping, \
            T2.compliance_task, T2.document_name, T2.format_file, \
            T2.penal_consequences, T2.compliance_description, \
            T2.statutory_dates, (select frequency \
                from tbl_compliance_frequency where \
                frequency_id = T2.frequency_id) as frequency,\
            (select business_group_name from tbl_business_groups where business_group_id = T4.business_group_id)business_group, \
            (select legal_entity_name from tbl_legal_entities where legal_entity_id = T4.legal_entity_id)legal_entity, \
            (select division_name from tbl_divisions where division_id = T4.division_id )division_name,\
            T4.unit_id, T4.unit_code, T4.unit_name, T4.address, T4.postal_code, \
            T1.statutory_applicable, T1.statutory_opted, T1.compliance_opted, \
            (select repeat_type from tbl_compliance_repeat_type where \
                repeat_type_id = T2.repeats_type_id) repeat_type, \
            (select duration_type from tbl_compliance_duration_type where \
                duration_type_id = T2.duration_type_id) duration_type , \
            T2.repeats_every, T2.duration \
            FROM tbl_client_compliances T1 \
            INNER JOIN tbl_compliances T2 \
            ON T1.compliance_id = T2.compliance_id \
            INNER JOIN tbl_client_statutories T3 \
            ON T1.client_statutory_id = T3.client_statutory_id \
            INNER JOIN tbl_units T4 \
            ON T3.unit_id = T4.unit_id \
            WHERE T3.country_id = %s \
            AND T3.domain_id = %s \
            %s \
            limit %s, %s" % (
                request.country_id,
                request.domain_id,
                where_qry,
                from_count, to_count
            )
        rows = self.select_all(query)
        columns = [
            "compliance_id", "statutory_provision", "statutory_mapping", "compliance_task",
            "document_name", "format_file", "penal_consequences",
            "compliance_description", "statutory_dates", "frequency",
            "business_group", "legal_entity", "division_name",
            "unit_id", "unit_code", "unit_name", "address", "postal_code", "statutory_applicable",
            "statutory_opted", "compliance_opted",
            "repeat_type", "duration_type", "repeats_every",
            "duration"
        ]
        result = self.convert_to_dict(rows, columns)
        legal_entity_wise = {}
        for r in result :
            business_group_name = r["business_group"]
            legal_entity_name = r["legal_entity"]
            division_name = r["division_name"]
            unit_id = r["unit_id"]
            name = "%s - %s" % (r["unit_code"], r["unit_name"])
            mapping = r["statutory_mapping"].split(">>")
            address = "%s - %s" % (r["address"], r["postal_code"])
            level_1_statutory = mapping[0]
            level_1_statutory = level_1_statutory.strip()

            document_name = r["document_name"]
            if document_name not in (None, "None", ""):
                compliance_name = "%s - %s" % (document_name, r["compliance_task"])
            else :
                compliance_name = r["compliance_task"]

            statutory_dates = json.loads(r["statutory_dates"])
            repeat_text = ""
            repeats_every = r["repeats_every"]
            repeat_type = r["repeat_type"]
            if repeats_every :
                repeat_text = statutory_repeat_text(statutory_dates, repeats_every, repeat_type)

            duration = r["duration"]
            duration_type = r["duration_type"]
            if duration:
                repeat_text = statutory_duration_text(duration, duration_type)

            compliance_name_list = [compliance_name]
            format_file = r["format_file"]
            if format_file :
                compliance_name_list.append("%s/%s" % (FORMAT_DOWNLOAD_URL, format_file))
            compliance = clientreport.ComplianceList(
                r["statutory_provision"] + r["statutory_mapping"],
                compliance_name_list,
                r["compliance_description"],
                r["penal_consequences"],
                core.COMPLIANCE_FREQUENCY(r["frequency"]),
                repeat_text
            )
            unit_data = clientreport.ApplicabilityCompliance(
                unit_id, name, address, [compliance]
            )

            legal_wise = legal_entity_wise.get(legal_entity_name)
            if legal_wise is None :
                act_wise = {}
                act_wise[level_1_statutory] = [unit_data]
                legal_wise = clientreport.GetComplianceTaskApplicabilityStatusReportData(
                    business_group_name, legal_entity_name, division_name,
                    act_wise
                )
                # legal_entity_wise[legal_entity_name] = legal_wise
            else :
                act_wise = legal_wise.actwise_units
                unit_wise = act_wise.get(level_1_statutory)

                if unit_wise is None :
                    unit_wise = []
                    unit_wise.append(unit_data)
                else :
                    is_new_unit = True
                    for u in unit_wise :
                        if u.unit_id == unit_id :
                            is_new_unit = False
                            c_list = u.compliances
                            if c_list is None :
                                c_list = []
                            c_list.append(compliance)
                            u.compliances = c_list

                    if is_new_unit :
                        unit_wise.append(unit_data)

                act_wise[level_1_statutory] = unit_wise
                legal_wise.actwise_units = act_wise
            legal_entity_wise[legal_entity_name] = legal_wise

        lst = []
        for k in sorted(legal_entity_wise):
            lst.append(legal_entity_wise.get(k))
        return clientreport.GetComplianceTaskApplicabilityStatusReportSuccess(
            total, lst
        )

    def start_on_occurrence_task(
        self, compliance_id, start_date, unit_id, duration, session_user, client_id
    ):
        columns = [
            "compliance_history_id", "unit_id", "compliance_id",
            "start_date", "due_date", "completed_by"
        ]
        compliance_history_id = self.get_new_id(
            "compliance_history_id", self.tblComplianceHistory, client_id
        )
        start_date = self.string_to_datetime_with_time(start_date)
        duration = duration.split(" ")
        duration_value = duration[0]
        duration_type = duration[1]
        due_date = None
        if duration_type == "Day(s)":
            due_date = start_date + datetime.timedelta(days=int(duration_value))
        elif duration_type == "Hour(s)":
            due_date = start_date + datetime.timedelta(hours=int(duration_value))
        values = [
            compliance_history_id, unit_id, compliance_id, start_date, due_date,
            session_user
        ]

        approval_columns = "approval_person, concurrence_person"
        approval_condition = " compliance_id = '%d' and unit_id = '%d' " % (
            compliance_id, unit_id
        )
        rows = self.get_data(
            self.tblAssignedCompliances, approval_columns, approval_condition
        )
        concurred_by = rows[0][1]
        approved_by = rows[0][0]
        if self.is_two_levels_of_approval():
            columns.append("concurred_by")
            values.append(concurred_by)
        columns.append("approved_by")
        values.append(approved_by)

        self.insert(
            self.tblComplianceHistory, columns, values
        )

        assignee_id, concurrence_id, approver_id, compliance_name, document_name, due_date = self.get_compliance_history_details(
            compliance_history_id
        )
        user_ids = "{},{},{}".format(assignee_id, concurrence_id, approver_id)
        assignee_email, assignee_name = self.get_user_email_name(str(assignee_id))
        approver_email, approver_name = self.get_user_email_name(str(approver_id))
        if concurrence_id not in [None, "None", 0, "", "null", "Null"] and self.is_two_levels_of_approval():
            concurrence_email, concurrence_name = self.get_user_email_name(str(concurrence_id))
        if document_name not in (None, "None", "") :
            compliance_name = "%s - %s" % (document_name, compliance_name)
        notification_text = "Compliance task %s has started" % compliance_name
        self.save_compliance_notification(
            compliance_history_id, notification_text, "Compliance Started",
            "Started"
        )
        try:
            notify_on_occur_thread = threading.Thread(
                target=email.notify_task, args=[
                    assignee_email, assignee_name,
                    concurrence_email, concurrence_name,
                    approver_email, approver_name, compliance_name,
                    due_date, "Start"
                ]
            )
            notify_on_occur_thread.start()
        except Exception, e:
            logger.logClient("error", "clientdatabase.py-start-on-occurance", e)
            print "Error sending email :{}".format(e)
        return True

    def get_form_ids_for_admin(self):
        columns = "group_concat(form_id)"
        condition = "is_admin = 1 OR form_type_id in (4,5) OR form_id in (1, 9,11,10,12)"
        rows = self.get_data(
            self.tblForms, columns, condition
        )
        return rows[0][0]

    def get_report_form_ids(self):
        columns = "group_concat(form_id)"
        condition = " form_type_id = 3"
        rows = self.get_data(
            self.tblForms, columns, condition
        )
        return rows[0][0]

    def get_client_settings(self):
        query = "SELECT two_levels_of_approval \
            FROM tbl_client_groups"
        row = self.select_one(query)
        if row:
            return bool(int(row[0]))

    def get_admin_info(self):
        query = "SELECT admin_id from tbl_admin"
        row = self.select_one(query)
        return int(row[0])

    def close_unit(self, unit_id, session_user):
        condition = "unit_id ='{}'".format(unit_id)
        columns = ["is_closed", "is_active"]
        values = [1, 0]
        result = self.update(
            self.tblUnits, columns, values, condition
        )

        columns = ["is_active"]
        values = [0]
        result = self.update(
            self.tblAssignedCompliances, columns, values, condition
        )

        db_con = Database(
            KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
            KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
        )
        db_con.connect()
        db_con.begin()
        q = "UPDATE tbl_units set is_active = 0 where unit_id = '%d'" % unit_id
        db_con.execute(q)
        db_con.commit()
        db_con.close()

        # columns = "client_statutory_id"
        # rows = self.get_data(self.tblClientStatutories, columns, condition)
        # if rows:
        #     client_statutory_id = rows[0][0]

        #     condition = "client_statutory_id='{}' and unit_id='{}'".format(
        #         client_statutory_id, unit_id
        #     )
        #     self.delete(self.tblClientStatutories, condition)

        #     condition = "client_statutory_id='{}' ".format(
        #         client_statutory_id
        #     )
        #     self.delete(self.tblClientCompliances, condition)

        action_column = "unit_code, unit_name"
        action_condition = "unit_id='{}'".format(unit_id)
        rows = self.get_data(
            self.tblUnits, action_column, action_condition
        )
        action = "Closed Unit \"%s - %s\"" % (rows[0][0], rows[0][1])
        self.save_activity(session_user, 5, action)

    def is_user_exists_under_user_group(self, user_group_id):
        columns = "count(*)"
        condition = "user_group_id = '%d'" % user_group_id
        rows = self.get_data(
            self.tblUsers, columns, condition
        )
        if rows[0][0] > 0:
            return True
        else:
            return False

    def is_user_exists_under_service_provider(self, service_provider_id):
        columns = "count(*)"
        condition = "service_provider_id = '%d'" % service_provider_id
        rows = self.get_data(
            self.tblUsers, columns, condition
        )
        if rows[0][0] > 0:
            return True
        else:
            return False

    def get_no_of_remaining_licence(self):
        columns = "count(*)"
        condition = "1"
        rows = self.get_data(self.tblUsers, columns, condition)
        no_of_licence_holders = rows[0][0]

        columns = "no_of_user_licence"
        rows = self.get_data(self.tblClientGroups, columns, condition)
        no_of_licence = rows[0][0]

        remaining_licence = int(no_of_licence) - int(no_of_licence_holders)
        return remaining_licence

    def is_already_notified(self):
        query = '''
            select count(*) from tbl_notifications_log
            where notification_text like '%sYour contract with Compfie for%s'
            AND created_on > DATE_SUB(now(), INTERVAL 30 DAY);
        ''' % ('%', '%')
        rows = self.select_all(query)
        if rows:
            count = rows[0][0]
            if count > 0:
                return True
            else:
                return False
        else:
            return False

    def notify_expiration(self):
        # download_link = exp(client_id, db).generate_report()
        group_name = self.get_group_name()

        notification_text = '''Your contract with Compfie for the group \"%s\" is about to expire. \
        Kindly renew your contract to avail the services continuously.'''  % group_name
        # Before contract expiration \
        # You can download documents of %s <a href="%s">here </a> ''' % (
        #     group_name, download_link
        # )
        extra_details = "0 - Reminder : Contract Expiration"
        notification_id = self.get_new_id("notification_id", self.tblNotificationsLog)
        created_on = datetime.datetime.now()
        columns = ["notification_id", "notification_type_id", "notification_text",
        "extra_details", "created_on"]
        values = [notification_id, 2, notification_text, extra_details, created_on]
        self.insert(self.tblNotificationsLog, columns, values)

        columns = ["notification_id", "user_id"]
        values = [notification_id, 0]
        self.insert(self.tblNotificationUserLog, columns, values)

        q = "SELECT username from tbl_admin"
        rows = self.select_all(q)
        admin_mail_id = rows[0][0]
        email.notify_contract_expiration(
            admin_mail_id, notification_text
        )

    def get_no_of_days_left_for_contract_expiration(self):
        column = "contract_to"
        condition = "1"
        rows = self.get_data(self.tblClientGroups, column, condition)
        contract_to_str = str(rows[0][0])
        contract_to_parts = [int(x) for x in contract_to_str.split("-")]
        contract_to = datetime.date(
            contract_to_parts[0], contract_to_parts[1], contract_to_parts[2]
        )
        delta = contract_to - self.get_date_time().date()
        if delta.days < 30:
            if not self.is_already_notified():
                self.notify_expiration()
        return delta.days

    def is_client_active(self, client_id):
        db_con = Database(
            KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
            KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
        )
        db_con.connect()
        db_con.begin()
        db_cur = db_con.cursor()
        q = "select count(*) from tbl_client_groups where \
        client_id = '%d' and is_active = 1" % client_id
        db_cur.execute(q)
        rows = db_cur.fetchall()
        db_con.commit()
        db_con.close()
        if rows[0][0] > 0:
            return True
        else:
            return False

    def get_dashboard_notification_counts(
        self, session_user
    ):
        query = '''
            SELECT
                tnl.notification_id
            FROM
                %s tnl
            INNER JOIN
                %s tnul
            ON tnl.notification_id = tnul.notification_id
            WHERE user_id = '%d' AND read_status = 0
        ''' % (
            self.tblNotificationsLog, self.tblNotificationUserLog, session_user
        )
        notification_condition = " AND notification_type_id = 1"
        escalation_condition = " AND notification_type_id = 3"
        reminder_condition = " AND notification_type_id = 2"

        notification_query = "%s %s" % (query, notification_condition)
        reminder_query = "%s %s" % (query, reminder_condition)
        escalation_query = "%s %s" % (query, escalation_condition)

        notification_rows = self.select_all(notification_query)
        reminder_rows = self.select_all(reminder_query)
        escalation_rows = self.select_all(escalation_query)

        notification_count = len(notification_rows)
        reminder_count = len(reminder_rows)
        escalation_count = len(escalation_rows)

        ## Getting statutory notifications
        statutory_column = "count(*)"
        statutory_condition = "user_id = '%d' and read_status = 0 ORDER BY \
        statutory_notification_id DESC" % session_user
        statutory_notification_rows = self.get_data(
            self.tblStatutoryNotificationStatus, statutory_column, statutory_condition
        )
        statutory_notification_count = statutory_notification_rows[0][0]
        notification_count += statutory_notification_count

        return notification_count, reminder_count, escalation_count

    def is_primary_admin(self, user_id):
        column = "count(1)"
        condition = "user_id = '%d' and is_primary_admin = 1" % user_id
        rows = self.get_data(self.tblUsers, column, condition)
        if rows[0][0] > 0 or user_id == 0:
            return True
        else:
            return False

    def is_service_proivder_user(self, user_id):
        column = "count(1)"
        condition = "user_id = '%d' and is_service_provider = 1" % user_id
        rows = self.get_data(self.tblUsers, column, condition)
        if rows[0][0] > 0:
            return True
        else:
            return False

    def is_service_provider_in_contract(self, service_provider_id):
        column = "count(1)"
        condition = "now() between contract_from and DATE_ADD(contract_to, INTERVAL 1 DAY)\
        and service_provider_id = '%d' and is_active = 1" % service_provider_id
        rows = self.get_data(self.tblServiceProviders, column, condition)
        if rows[0][0] > 0:
            return True
        else:
            return False

#
# mobile_api
#

    def get_client_group(self):
        q = "SELECT client_id, group_name from  tbl_client_groups"
        row = self.select_one(q)
        result = []
        if row :
            result = self.convert_to_dict(row, ["client_id", "group_name"])
        return result

    def get_client_configuration(self):
        q = "SELECT country_id, domain_id, period_from, period_to from tbl_client_configurations"
        rows = self.select_all(q)
        result = []
        if rows :
            result = self.convert_to_dict(rows, ["country_id", "domain_id", "period_from", "period_to"])
        c_list = []
        for r in result :
            info = core.ClientConfiguration(
                r["country_id"],
                r["domain_id"],
                r["period_from"],
                r["period_to"]
            )
            c_list.append(info)

        return c_list

    def get_version(self):
        q = "SELECT unit_details_version, user_details_version, \
            compliance_applicability_version, compliance_history_version, \
            reassign_history_version FROM tbl_mobile_sync_versions"
        rows = self.select_one(q)
        column = [
            "unit_details", "user_details",
            "compliance_applicability",
            "compliance_history",
            "reassign_history"
        ]
        result = self.convert_to_dict(rows, column)
        return result

    def get_users_for_mobile(self, session_user):
        where_condition = "WHERE t2.unit_id \
            IN \
            (select distinct unit_id from tbl_user_units where user_id = %s)" % (session_user)

        query = "SELECT distinct t1.user_id, t1.employee_name, \
            t1.employee_code, \
            t1.seating_unit_id, t1.user_level, \
            (select group_concat(distinct domain_id) from tbl_user_domains where user_id = t1.user_id) domain_ids, \
            (select group_concat(distinct unit_id) from tbl_user_units where user_id = t1.user_id ) unit_ids,\
            t1.is_service_provider, \
            (select service_provider_name from  tbl_service_providers where service_provider_id = t1.service_provider_id) service_provider, \
            (select form_ids from tbl_user_groups where user_group_id = t1.user_group_id)fomr_ids\
            FROM tbl_users t1 \
            INNER JOIN tbl_user_units t2 \
            ON t1.user_id = t2.user_id AND t1.is_active = 1 "

        if session_user > 0 and session_user != self.get_admin_id() :
            query = query + where_condition
        rows = self.select_all(query)
        columns = [
            "user_id", "employee_name", "employee_code",
            "seating_unit_id", "user_level",
            "domain_ids", "unit_ids",
            "is_service_provider", "service_provider",
            "form_ids"
        ]
        result = self.convert_to_dict(rows, columns)
        user_list = []
        for r in result :
            if int(r["is_service_provider"]) == 0 :
                name = "%s - %s" % (r["employee_code"], r["employee_name"])
            else :
                name = "%s - %s" % (r["service_provider"], r["employee_name"])

            user_id = r["user_id"]
            user_list.append(mobile.GetUsersList(user_id, name))

        return user_list

    def get_business_groups_for_mobile(self):
        q = "select business_group_id, business_group_name from tbl_business_groups order by business_group_name"
        rows = self.select_all(q)
        result = self.convert_to_dict(rows, ["business_group_id", "business_group_name"])
        business_group_list = []
        for r in result :
            business_group_list.append(
                core.ClientBusinessGroup(
                    r["business_group_id"],
                    r["business_group_name"]
                )
            )
        return business_group_list

    def get_legal_entities_for_mobile(self):
        columns = "legal_entity_id, legal_entity_name, business_group_id"
        condition = " 1 ORDER BY legal_entity_name"
        rows = self.get_data(
            self.tblLegalEntities, columns, condition
        )
        result = self.convert_to_dict(rows, ["legal_entity_id", "legal_entity_name", "business_group_id"])
        legal_entity_list = []
        for r in result :
            legal_entity_list.append(
                core.ClientLegalEntity(
                    r["legal_entity_id"],
                    r["legal_entity_name"],
                    r["business_group_id"]
                )
            )
        return legal_entity_list

    def get_divisions_for_mobile(self):
        columns = "division_id, division_name, legal_entity_id, business_group_id"
        condition = " 1 ORDER BY division_name"
        rows = self.get_data(
            self.tblDivisions, columns, condition
        )
        columns = [
            "division_id", "division_name", "legal_entity_id",
            "business_group_id"
        ]
        result = self.convert_to_dict(rows, columns)
        division_list = []
        for r in result:
            division_list.append(core.ClientDivision(
                r["division_id"],
                r["division_name"],
                r["legal_entity_id"],
                r["business_group_id"]
            ))
        return division_list

    def get_compliance_applicability_for_mobile(self, session_user):
        user_id = session_user
        if session_user == 0 or session_user == self.get_admin_id :
            user_id = '%'
        q = "SELECT t1.country_id, t1.domain_id, t1.unit_id, \
            t2.compliance_id, t2.compliance_applicable, t2.compliance_opted, \
            t3.compliance_task, t3.document_name, \
            (select frequency from tbl_compliance_frequency where \
            frequency_id = t3.frequency_id) frequency \
            FROM tbl_client_statutories t1 \
            INNER JOIN \
            tbl_client_compliances t2 on \
            t1.client_statutory_id = t2.client_statutory_id \
            INNER JOIN \
            tbl_compliances t3 ON t2.compliance_id = t3.compliance_id \
            WHERE t1.is_new = 1 AND t1.unit_id in (select unit_id from tbl_user_units where \
            user_id LIKE '%s')" % (user_id)

        rows = self.select_all(q)
        result = self.convert_to_dict(rows, [
            "country_id", "domain_id", "unit_id",
            "compliance_id", "compliance_applicable",
            "compliance_opted", "compliance_task",
            "document_name", "frequency"
        ])
        applicability = []
        for r in result :
            if r["document_name"] not in ("None", "", None):
                name = "%s - %s" % (r["document_name"], r["compliance_task"])
            else :
                name = r["compliance_task"]
            applicability.append(mobile.ComplianceApplicability(
                r["country_id"],
                r["domain_id"],
                r["unit_id"],
                r["compliance_id"],
                name,
                r["frequency"],
                bool(r["compliance_applicable"]),
                bool(r["compliance_opted"])
            ))
        return applicability

    def get_trend_chart_for_mobile(self, session_user):
        years = self.get_last_7_years()
        unit_ids = self.get_user_unit_ids(session_user)
        unit_wise_details = []
        for unit_id in [int(x) for x in unit_ids.split(",")]:
            unit_details_column = "country_id, domain_ids"
            unit_details_condition = "unit_id = '%d'" % unit_id
            rows = self.get_data(
                self.tblUnits, unit_details_column, unit_details_condition
            )
            country_id = rows[0][0]
            domain_ids = rows[0][1]
            country_ids_list = [country_id]
            domain_ids_list = [int(x) for x in domain_ids.split(",")]
            country_domain_timelines = self.get_country_domain_timelines(
                country_ids_list, domain_ids_list, years
            )
            chart_data = []
            for country_wise_timeline in country_domain_timelines:
                country_id = country_wise_timeline[0]
                domain_wise_timelines = country_wise_timeline[1]
                domain_wise_details = []
                for domain_wise_timeline in domain_wise_timelines:
                    year_wise_count = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
                    domain_id = domain_wise_timeline[0]
                    start_end_dates = domain_wise_timeline[1]

                    history_columns = "group_concat(compliance_history_id)"
                    history_condition = "compliance_id in ( SELECT compliance_id \
                    FROM %s WHERE domain_id = '%d') AND unit_id = '%d'" % (
                        self.tblCompliances, domain_id, unit_id
                    )
                    history_rows = self.get_data(
                        self.tblComplianceHistory, history_columns,
                        history_condition
                    )
                    compliance_history_ids = history_rows[0][0]

                    if compliance_history_ids not in [None, '', "None"]:
                        for index, dates in enumerate(start_end_dates):
                            columns = "count(*) as total, sum(case when approve_status = 1 then 1 " + \
                                "else 0 end) as complied"
                            condition = "due_date between '{}' and '{}'".format(
                                dates["start_date"], dates["end_date"]
                            )
                            condition += " and compliance_history_id in ({})".format(compliance_history_ids)
                            rows = self.get_data(
                                self.tblComplianceHistory,
                                columns, condition
                            )
                            if len(rows) > 0:
                                row = rows[0]
                                total_compliances = row[0]
                                complied_compliances = row[1] if row[1] != None else 0
                                year_wise_count[index][0] += int(total_compliances) if total_compliances is not None else 0
                                year_wise_count[index][1] += int(complied_compliances) if complied_compliances is not None else 0

                    for index, count_of_year in enumerate(year_wise_count):
                        domain_wise_details.append(
                            mobile.DomainWiseCount(
                                domain_id=domain_id,
                                year=years[index],
                                total_compliances=int(count_of_year[0]),
                                complied_compliances_count=int(count_of_year[1])
                            ))
            unit_wise_details.append(mobile.UnitWiseCount(
                unit_id=unit_id,
                domain_wise_count=domain_wise_details
            ))
        return unit_wise_details

    def get_compliance_history_for_mobile(self, user_id, request):
        compliance_history_id = request.compliance_history_id
        if user_id == 0 :
            user_qry = '1'
        else :
            user_qry = "(t1.completed_by LIKE '%s' OR t1.concurred_by LIKE '%s' \
            OR t1.approved_by LIKE '%s')" % (user_id, user_id, user_id)

        q = "SELECT t1.compliance_history_id, t1.unit_id, \
            t1.compliance_id, t1.start_date, t1.due_date, \
            t1.completion_date, t1.documents, IFNULL(t1.document_size, 0), \
            t1.validity_date, t1.next_due_date, t1.remarks, \
            t1.completed_by, t1.completed_on, IFNULL(t1.concurrence_status, 0), \
            t1.concurred_by, t1.concurred_on, IFNULL(t1.approve_status, 0), \
            t1.approved_by, t1.approved_on \
            FROM tbl_compliance_history t1 \
            WHERE t1.compliance_history_id > %s AND %s" % (
                compliance_history_id, user_qry
            )
        rows = self.select_all(q)
        column = [
            "compliance_history_id", "unit_id", "compliance_id",
            "start_date", "due_date", "completion_date",
            "documents", "document_size", "validity_date",
            "next_due_date", "remarks", "completed_by",
            "completed_on", "concurrence_status",
            "concurred_by", "concurred_on", "approve_status",
            "approved_by", "approved_on"
        ]
        result = self.convert_to_dict(rows, column)
        history_list = []
        for r in result :
            document_list = None
            if r["documents"] is not None :
                documents = r["documents"].strip().split(',')
                if len(documents) > 0 :
                    document_list = []
                    for d in documents :
                        document_list.append(
                            core.FileList(
                                r["document_size"],
                                d,
                                None
                            )
                        )

            history_list.append(mobile.ComplianceHistory(
                r["compliance_history_id"],
                r["unit_id"],
                r["compliance_id"],
                str(r["start_date"]),
                str(r["due_date"]),
                str(r["completion_date"]),
                document_list,
                str(r["validity_date"]),
                str(r["next_due_date"]),
                r["remarks"],
                r["completed_by"],
                str(r["completed_on"]),
                bool(r["concurrence_status"]),
                r["concurred_by"],
                str(r["concurred_on"]),
                bool(r["approve_status"]),
                r["approved_by"],
                str(r["approved_on"])
            ))

        return history_list

    def get_check_disk_space_for_mobile(self):
        q = "SELECT total_disk_space, IFNULL(total_disk_space_used, 0) FROM \
            tbl_client_groups"
        row = self.select_one(q)
        result = self.convert_to_dict(row, ["total_disk_space", "total_disk_space_used"])
        return result

    def have_compliances(self, user_id):
        column = "count(*)"
        condition = "assignee = '%d' and is_active = 1" % user_id
        rows = self.get_data(self.tblAssignedCompliances, column, condition)
        no_of_compliances = rows[0][0]
        if no_of_compliances > 0:
            return True
        else:
            return False

    def get_compliance_name_by_id(self, compliance_id):
        column = "document_name, compliance_task"
        condition = "compliance_id = '%d'" % compliance_id
        rows = self.get_data(self.tblCompliances, column, condition)
        compliance_name = ""
        if rows[0][0] is not None:
            compliance_name += rows[0][0]+" - "+rows[0][1]
        else:
            compliance_name = rows[0][1]
        return compliance_name

    def save_registration_key(self, session_user, request):
        columns = ["registration_key", "device_type_id", "user_id"]
        if request.session_type.lower() is "android" :
            device = 2
        elif request.session_type.lower() is "ios" :
            device = 3
        elif request.session_type.lower() is "blackberry" :
            device = 4

        value_list = [
            request.reg_key, device, session_user
        ]

        self.insert(self.tblMobileRegistration, columns, value_list)

    def is_seating_unit(self, unit_id):
        column = "count(*)"
        condition = "seating_unit_id ='%d'" % unit_id
        rows = self.get_data(self.tblUsers, column, condition)
        user_count = rows[0][0]
        if user_count > 0:
            return True
        else:
            return False

    def need_to_display_deletion_popup(self):
        current_date = self.get_date_time()
        column = "notification_id, created_on, notification_text"
        condition = "extra_details like '%s%s%s' AND \
        created_on > DATE_SUB(now(), INTERVAL 30 DAY )" % ("%", "Auto Deletion", "%")
        notification_rows = self.get_data(self.tblNotificationsLog, column, condition)
        if len(notification_rows) > 0:
            notification_id = notification_rows[0][0]
            created_on = notification_rows[0][1]
            r = relativedelta.relativedelta(current_date.date(), created_on)
            if ((abs(r.days) % 6) == 0 and r.years == 0 and r.months == 0 and r.days != 0):
                columns = "updated_on"
                condition = "notification_id = '%d' and date(updated_on) !=  CURDATE()" % notification_id
                rows = self.get_data(self.tblNotificationUserLog, columns, condition)
                if len(rows) > 0:
                    columns = ["updated_on"]
                    values = [current_date]
                    condition = "notification_id = '%d'" % notification_id
                    self.update(self.tblNotificationUserLog, columns, values, condition)
                    return True, notification_rows[0][2]
                else:
                    return False, ""
            else:
                return False, ""
        else :
            return False, ""

#
#   Update Profile
#

    def update_profile(self, contact_no, address, session_user):
        columns = ["contact_no", "address"]
        values = [contact_no, address]
        condition = "user_id= '%d'" % session_user
        self.update(self.tblUsers, columns, values, condition)
