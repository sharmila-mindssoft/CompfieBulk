import os
import threading
from protocol import (
    core, general, clienttransactions, dashboard,
    clientreport, clientadminsettings, clientuser
)
from database import Database
import json
import datetime
from datetime import timedelta
from dateutil import relativedelta
from types import *

from types import *
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

    def update_traild_id(self, audit_trail_id):
        query = "UPDATE tbl_audit_log SET audit_trail_id=%s;" % (audit_trail_id)
        self.execute(query)

    def get_trail_id(self):
        query = "select IFNULL(MAX(audit_trail_id), 0) as audit_trail_id from tbl_audit_log;"
        row = self.select_one(query)
        trail_id = row[0]
        return trail_id

    def is_in_contract(self):
        columns = "count(*)"
        condition = "now() BETWEEN contract_from and contract_to "
        rows = self.get_data(
            self.tblClientGroups, columns, condition
        )
        if rows[0][0] <= 0:
            return False
        else:
            return True

    def is_contract_not_started(self):
        columns = "count(*)"
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
                "user_group_name", "form_ids", "is_admin"
            ]
            query = "SELECT t1.user_id, t1.user_group_id, t1.email_id, \
                t1.employee_name, t1.employee_code, t1.contact_no, \
                t2.user_group_name, t2.form_ids, t1.is_admin \
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
                # result["client_id"] = client_id
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
        if user_id != 0:
            condition = " user_id='%d'" % user_id
            result = self.update(
                self.tblUsers, columns, values, condition, client_id
            )
        else:
            result = self.update(
                self.tblAdmin, columns, values, condition, client_id
            )
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
            if rows[0][0] > 0:
                return user_id
            else:
                return None
        else:
            return None

    def validate_session_token(self, client_id, session_token) :
        query = "SELECT user_id FROM tbl_user_sessions \
            WHERE session_token = '%s'" % (session_token)
        row = self.select_one(query)
        user_id = None
        if row :
            user_id = row[0]
        return user_id

    def get_forms(self, client_id):
        columns = "tf.form_id, tf.form_type_id, tft.form_type, "
        columns += "tf.form_name, tf.form_url, tf.form_order, tf.parent_menu"
        tables = [self.tblForms, self.tblFormType]
        aliases = ["tf",  "tft"]
        joinConditions = ["tf.form_type_id = tft.form_type_id"]
        whereCondition = " is_admin = 0 and tf.form_type_id not in (5) \
        order by tf.form_order"
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

    def get_countries_for_user(self, user_id, client_id=None) :
        query = "SELECT distinct t1.country_id, t1.country_name, \
            t1.is_active FROM tbl_countries t1 "
        if user_id > 0 :
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

    def get_domains_for_user(self, user_id, client_id=None) :
        query = "SELECT distinct t1.domain_id, t1.domain_name, \
            t1.is_active FROM tbl_domains t1 "
        if user_id > 0 :
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
            condition = "business_group_id in (%s)" % business_group_ids
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
            condition = "legal_entity_id in (%s)" % legal_entity_ids
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
            condition = "division_id in (%s)" % division_ids
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
        columns += " legal_entity_id, business_group_id, is_active"
        condition = "1"
        if unit_ids is not None:
            condition = "unit_id in (%s) and is_closed = 0 and is_active = 1" % unit_ids
        rows = self.get_data(
            self.tblUnits, columns, condition
        )
        columns = [
            "unit_id", "unit_code", "unit_name", "unit_address", "division_id","domain_ids", "country_id",
            "legal_entity_id", "business_group_id", "is_active"
        ]

        result = self.convert_to_dict(rows, columns)
        return self.return_units(result)

    def get_units_closure_for_user(self, unit_ids):
        columns = "unit_id, unit_code, unit_name, address, division_id, domain_ids, country_id,"
        columns += " legal_entity_id, business_group_id, is_closed"
        condition = "1"
        if unit_ids is not None:
            condition = "unit_id in (%s) and is_active = 1" % unit_ids
        rows = self.get_data(
            self.tblUnits, columns, condition
        )
        columns = [
            "unit_id", "unit_code", "unit_name", "unit_address", "division_id","domain_ids", "country_id",
            "legal_entity_id", "business_group_id", "is_active"
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
            condition += " and industry_name = '%s' and is_active = 1" % industry_name
            rows = self.get_data(
                self.tblUnits, columns, condition
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
                [int(x) for x in unit["domain_ids"].split(",")], unit["country_id"]
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
        return self.get_new_id("user_group_id",self.tblUserGroups, client_id)

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
        condition = "email_id ='%s' AND user_id != '%d'" %(
            email_id, user_id)
        return self.is_already_exists(self.tblUsers, condition, client_id)

    def is_duplicate_employee_code(self, user_id, employee_code, client_id):
        condition = "employee_code ='%s' AND user_id != '%d'" %(
            employee_code, user_id)
        return self.is_already_exists(self.tblUsers, condition, client_id)

    def is_duplicate_user_contact_no(self, user_id, contact_no, client_id):
        condition = "contact_no ='%s' AND user_id != '%d'" %(
            contact_no, user_id)
        return self.is_already_exists(self.tblUsers, condition, client_id)

    def get_user_details(self, client_id):
        columns = "user_id, email_id, user_group_id, employee_name,"+\
        "employee_code, contact_no, seating_unit_id, user_level, "+\
        " is_admin, is_service_provider, service_provider_id, is_active,\
        is_primary_admin "
        condition = "1 ORDER BY employee_name"
        rows =  self.get_data(
            self.tblUsers,columns, condition
        )
        columns = ["user_id", "email_id", "user_group_id", "employee_name",
        "employee_code", "contact_no", "seating_unit_id", "user_level",
        "is_admin", "is_service_provider", "service_provider_id", "is_active",
        "is_primary_admin"]
        result = self.convert_to_dict(rows, columns)
        return self.return_user_details(result, client_id)

    def return_user_details(self, users, client_id):
        results = []
        for user in users :
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
            employee_name = "%s - %s"% (user["employee_code"],user["employee_name"])
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
            print "Error while sending email : {}".format(e)

    def save_user(self, user_id, user, session_user, client_id):
        result1 = None
        result2 = None
        result3 = None
        current_time_stamp = self.get_date_time()
        user.is_service_provider = 0 if user.is_service_provider== False else 1
        columns = ["user_id", "user_group_id", "email_id", "password", "employee_name",
                    "employee_code", "contact_no", "user_level",
                "is_admin", "is_service_provider","created_by", "created_on",
                "updated_by", "updated_on"]
        encrypted_password, password = self.generate_and_return_password()
        values = [ user_id, user.user_group_id, user.email_id,
                encrypted_password, user.employee_name,
                user.employee_code, user.contact_no, user.user_level,
                0, user.is_service_provider, session_user,current_time_stamp,
                session_user, current_time_stamp]
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
        employee_code, contact_no, created_on, is_admin, is_active, seating_unit_id"
        q = "INSERT INTO tbl_client_users ({}) values ('{}', '{}', '{}', '{}', \
        '{}', '{}', now(), 0, 1, '{}')".format(
            columns, client_id, user_id, user.email_id, user.employee_name,
            user.employee_code, user.contact_no, user.seating_unit_id
        )
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
        values = [ user.user_group_id, user.employee_name, user.employee_code,
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
        q = "UPDATE tbl_client_users set \
        employee_name = '{}', employee_code = '{}', \
        contact_no = '{}', seating_unit_id = '{}' where client_id ='{}' \
        and user_id = '{}'".format(
             user.employee_name, user.employee_code, user.contact_no,
             user.seating_unit_id, client_id, user.user_id
        )
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
        is_admin = 1 if is_admin != False else 0
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
        columns = "group_concat(unit_id)"
        condition = " 1 "
        rows = None
        if user_id > 0:
            condition = "  user_id = '%d'" % user_id
            rows = self.get_data(
                self.tblUserUnits, columns, condition
            )
        else:
            rows = self.get_data(
                self.tblUnits, columns, condition
            )
        unit_ids = rows[0][0]

        columns = "group_concat(division_id), group_concat(legal_entity_id), "+\
        "group_concat(business_group_id)"
        unit_condition = "1"
        if unit_ids != None:
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
        columns = "group_concat(domain_id)"
        table = self.tblDomains
        result = None
        condition = 1
        if user_id > 0:
            table  = self.tblUserDomains
            condition = " user_id = '%d'" % user_id
        rows = self.get_data(
            table, columns, condition
        )
        if rows:
            result = rows[0][0]
        return result

    def get_user_unit_ids(self, user_id, client_id=None):
        columns = "group_concat(unit_id)"
        table = self.tblUnits
        result = None
        condition = 1
        if user_id > 0:
            table = self.tblUserUnits
            condition = " user_id = '%d'"% user_id
        rows = self.get_data(
            table, columns, condition
        )
        if rows :
            result = rows[0][0]
        return result

    def get_user_business_group_ids(self, user_id):
        columns = "group_concat(distinct business_group_id)"
        table = self.tblUnits
        result = None
        condition = 1
        if user_id > 0 :
            table = self.tblUserUnits
            condition = " user_id = %s " % user_id
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
        if user_id > 0 :
            table = self.tblUserUnits
            condition = " user_id = %s " % user_id
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
        if user_id > 0 :
            table = self.tblUserUnits
            condition = " user_id = %s " % user_id
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

    def deactivate_unit(self, unit_id, client_id, session_user):
        columns = ["is_active"]
        values = [1]
        condition = "unit_id ='%d'" % unit_id
        result = self.update(
            self.tblUnits, columns, values, condition, client_id
        )

        action_column = "unit_code, unit_name"
        rows = self.get_data(
            self.tblUnits, action_column, condition
        )
        action = "Closed Unit \"%s - %s\"" % (rows[0][0], rows[0][1])
        self.save_activity(session_user, 5, action, client_id)

        return result

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

    def is_duplicate_service_provider_contact_no(self, service_provider_id,
            contact_no, client_id):
        condition = "contact_no ='%s' AND service_provider_id != '%d'" % (contact_no,
            service_provider_id)
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
        rows = self.get_data(
            self.tblServiceProviders, columns, "1"
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

    def get_audit_trails(self, user_id, client_id):
        user_ids = ""
        form_ids = None
        if user_id != 0:
            column = "user_group_id"
            condition = "user_id = '%d'" % user_id
            rows = self.get_data(
                self.tblUsers, column, condition
            )
            user_group_id = rows[0][0]

            column = "form_category_id"
            condition = "user_group_id = '%d'" % user_group_id
            rows = self.get_data(
                self.tblUserGroups, column, condition
            )
            form_category_id = rows[0][0]

            column = "group_concat(form_id)"
            condition = "form_category_id = '%d' AND form_type_id != 4" % (
                form_category_id
            )
            rows = self.get_data(
                self.tblForms, column, condition
            )
            form_ids = rows[0][0]

            column = "group_concat(user_group_id)"
            condition = "form_category_id = '%d'" % form_category_id
            rows = self.get_data(
                self.tblUserGroups, column, condition
            )
            user_group_ids = rows[0][0]

            column = "group_concat(user_id)"
            condition = "user_group_id in (%s)" % user_group_ids
            rows = self.get_data(
                self.tblUsers, column, condition
            )
            user_ids = rows[0][0]
            condition = "user_id in (%s)" % user_ids
        else:
            condition = "1"
            form_column = "group_concat(form_id)"
            form_condition = "form_type_id != 4"
            rows = self.get_data(
                self.tblForms, form_column, form_condition
            )
            form_ids = rows[0][0]
        columns = "user_id, form_id, action, created_on"
        rows = self.get_data(
            self.tblActivityLog, columns, condition
        )
        audit_trail_details = []
        for row in rows:
            user_id = row[0]
            form_id = row[1]
            action = row[2]
            date = self.datetime_to_string(row[3])
            audit_trail_details.append(
                general.AuditTrail(user_id, form_id, action, date)
            )
        users = None
        if user_id != 0:
            users = self.get_users_by_id(user_ids, client_id)
        else:
            users = self.get_users(client_id)
        forms = self.return_forms(client_id, form_ids)
        return general.GetAuditTrailSuccess(audit_trail_details, users, forms)

#
# Statutory settings
#

    def get_statutory_settings(self, session_user, client_id):
        if session_user == 0 :
            user_id = '%'
        else :
            user_id = int(session_user)
        query = "SELECT distinct t1.geography, \
            t1.country_id, t1.domain_id, t1.unit_id,t2.unit_name, \
            (select business_group_name from tbl_business_groups \
                where business_group_id = t2.business_group_id)business_group_name, \
            (select legal_entity_name from tbl_legal_entities \
                where legal_entity_id = t2.legal_entity_id)legal_entity_name,\
            (select division_name from tbl_divisions \
                where division_id = t2.division_id)division_name, \
            t2.address, t2.postal_code, t2.unit_code, \
            (select country_name from tbl_countries where country_id = t1.country_id )country_name, \
            (select domain_name from tbl_domains where domain_id = t1.domain_id)domain_name \
            FROM tbl_client_statutories t1 \
            INNER JOIN tbl_units t2 \
            ON t1.unit_id = t2.unit_id \
            WHERE t1.unit_id in (select unit_id from tbl_user_units where user_id LIKE '%s') \
            AND t1.domain_id in (select domain_id from tbl_user_domains where user_id LIKE '%s')" % (
                user_id, user_id
            )

        rows = self.select_all(query)
        columns = [
            "geography",
            "country_id", "domain_id", "unit_id", "unit_name",
            "business_group_name", "legal_entity_name",
            "division_name", "address", "postal_code", "unit_code",
            "country_name", 'domain_name'
        ]
        result = self.convert_to_dict(rows, columns)
        return self.return_statutory_settings(result, client_id)

    def return_compliance_for_statutory_settings(
        self, domain_id, unit_id
    ):
        query = "SELECT t1.client_statutory_id, t1.compliance_id, \
            t1.statutory_applicable, t1.statutory_opted,\
            t1.not_applicable_remarks, \
            t1.compliance_applicable, t1.compliance_opted, \
            t1.compliance_remarks, \
            t2.compliance_task, t2.document_name, t2.statutory_mapping,\
            t2.statutory_provision, t2.compliance_description, \
            t3.is_new\
            FROM tbl_client_compliances t1 \
            INNER JOIN tbl_compliances t2 \
            ON t1.compliance_id = t2.compliance_id \
            INNER JOIN tbl_client_statutories t3 \
            ON t1.client_statutory_id = t3.client_statutory_id \
            WHERE t3.domain_id = %s AND \
            t3.unit_id = %s" % (
                domain_id, unit_id
            )
        rows = self.select_all(query)
        columns = [
            "client_statutory_id", "compliance_id",
            "statutory_applicable", "statutory_opted",
            "not_applicable_remarks", "compliance_applicable",
            "compliance_opted", "compliance_remarks",
            "compliance_task", "document_name", "statutory_mapping",
            "statutory_provision", "compliance_description",
            "is_new"
        ]
        results = self.convert_to_dict(rows, columns)
        statutory_wise_compliances = {}
        print statutory_wise_compliances
        for r in results :
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
                r["client_statutory_id"],
                r["compliance_id"],
                name,
                r["compliance_description"],
                provision,
                bool(r["compliance_applicable"]),
                bool(compliance_opted),
                compliance_remarks,
                not bool(r["is_new"])
            )

            level_1_statutories = statutory_wise_compliances.get(
                statutory_name
            )
            if level_1_statutories is None :
                level_1_statutories = clienttransactions.AssignedStatutory(
                    r["client_statutory_id"],
                    statutory_name,
                    [compliance],
                    bool(r["statutory_applicable"]),
                    statutory_opted,
                    r["not_applicable_remarks"]
                )
            else :
                compliance_list = level_1_statutories.compliances
                compliance_list.append(compliance)
                level_1_statutories.compliances = compliance_list

            statutory_wise_compliances[statutory_name] = level_1_statutories
        print statutory_wise_compliances
        return statutory_wise_compliances

    def return_statutory_settings(self, data, client_id):
        unit_wise_statutories = {}
        for d in data :
            domain_name = d["domain_name"]
            unit_id = d["unit_id"]
            unit_name = "%s - %s" % (d["unit_code"], d["unit_name"])
            address = "%s, %s, %s" % (
                d["address"],
                d["geography"],
                d["postal_code"]
            )
            domain_id = d["domain_id"]
            # client_statutory_id = d["client_statutory_id"]
            statutories = self.return_compliance_for_statutory_settings(
                domain_id, unit_id
            )
            statutory_val = []
            for key in sorted(statutories):
                statutory_val.append(
                    statutories[key]
                )

            unit_statutories = unit_wise_statutories.get(unit_id)
            if unit_statutories is None :
                statutory_dict = {}
                statutory_dict[domain_name] = statutory_val
                unit_statutories = clienttransactions.UnitStatutoryCompliances(
                    unit_id,
                    unit_name,
                    address,
                    d["country_name"],
                    [domain_name],
                    d["business_group_name"],
                    d["legal_entity_name"],
                    d["division_name"],
                    statutory_dict
                )
            else :
                domain_list = unit_statutories.domain_names
                domain_list.append(domain_name)
                domain_list = list(set(domain_list))
                statutory_dict = unit_statutories.statutories
                domain_statutories = statutory_dict.get(domain_name)
                if domain_statutories is None :
                    domain_statutories = statutories.values()
                else :
                    domain_statutories.extend(statutories.values())
                statutory_dict[domain_name] = domain_statutories

                # set values
                unit_statutories.domain_names = domain_list
                unit_statutories.statutories = statutory_dict
            unit_wise_statutories[unit_id] = unit_statutories

        return clienttransactions.GetStatutorySettingsSuccess(
            unit_wise_statutories.values()
        )

    def update_statutory_settings(self, data, session_user, client_id):
        unit_id = data.unit_id
        unit_name = data.unit_name
        statutories = data.statutories
        updated_on = self.get_date_time()
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

            query = "UPDATE tbl_client_compliances t1 \
                INNER JOIN tbl_client_statutories t2 \
                ON t1.client_statutory_id = t2.client_statutory_id \
                SET \
                t1.statutory_opted=%s, \
                t1.not_applicable_remarks='%s', \
                t1.compliance_opted=%s, \
                t1.compliance_remarks='%s',\
                t1.updated_by=%s, \
                t1.updated_on='%s', t2.is_new = 1 \
                WHERE t2.unit_id = %s \
                AND t1.client_statutory_id = %s \
                AND t1.compliance_id = %s" % (
                    statutory_opted_status, not_applicable_remarks,
                    opted_status, remarks, session_user, updated_on,
                    unit_id, client_statutory_id, compliance_id
                )
            self.execute(query)

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
            print e
            db_con.rollback()

    def get_level_1_statutory(self, client_id):
        columns = "client_statutory_id, statutory_provision"
        condition = "compliance_applicable is Null AND compliance_opted is null"
        rows = self.get_data(
            self.tblClientCompliances, columns, condition
        )
        columns = ["level_1_statutory_id" , "level_1_statutory_name"]
        result = self.convert_to_dict(rows, columns)
        return self.return_level_1_statutories(result)

    def return_level_1_statutories(self, statutories):
        results = []
        for statutory in statutories :
            statutory_obj = core.Level1Statutory(
                statutory["level_1_statutory_id"],
                statutory["level_1_statutory_name"])
            results.append(statutory_obj)
        return results

    def get_level_1_statutories_for_user_with_domain(self, session_user, client_id, domain_id=None):
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
            mapping_rows = self.get_data(
                self.tblCompliances,
                "statutory_mapping",
                "domain_id in (%s)" % (domain_id)
            )
            level_1_statutory[domain_id] = []
            for mapping in mapping_rows:
                statutories = mapping[0].split(">>")
                if statutories[0].strip() not in level_1_statutory[domain_id]:
                    level_1_statutory[domain_id].append(statutories[0].strip())
        return level_1_statutory

    def get_level_1_statutories_for_user(self, session_user, client_id, domain_id=None):
        domain_ids = domain_id
        if domain_ids is None :
            columns = "group_concat(domain_id)"
            domain_rows = None
            if session_user != 0:
                domain_rows = self.get_data(self.tblUserDomains, columns,
                "user_id='%d'" % session_user)
            else:
                domain_rows = self.get_data(self.tblDomains, columns,
                "1")
            domain_ids = domain_rows[0][0]
        client_statutory_rows = self.get_data(
            self.tblClientStatutories,
            "group_concat(client_statutory_id)",
            "domain_id in (%s)" % domain_ids
            )
        client_statutory_ids = client_statutory_rows[0][0]
        mapping_rows = []
        if client_statutory_ids is not None:
            client_compliance_rows = self.get_data(
                self.tblClientCompliances,
                "group_concat(compliance_id)",
                "client_statutory_id in (%s)" % client_statutory_ids,
                )
            client_compliance_ids = client_compliance_rows[0][0]
            if client_compliance_ids is not None:
                mapping_rows = self.get_data(
                    self.tblCompliances,
                    "statutory_mapping",
                    "compliance_id in (%s)" % (client_compliance_ids)
                )
        level_1_statutory = []
        if len(mapping_rows) > 0:
            for mapping in mapping_rows:
                statutories = mapping[0].split(">>")
                if statutories[0].strip() not in level_1_statutory:
                    level_1_statutory.append(statutories[0].strip())
        return level_1_statutory

    def get_compliance_frequency(self, client_id):
        columns = "frequency_id, frequency"
        rows = self.get_data(
            self.tblComplianceFrequency, columns, "1"
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

    def get_frequecy_id_by_name(self, frequency_name):
        columns = "frequency_id"
        condition = "frequency = '%s'" % frequency_name
        rows = self.get_data(self.tblComplianceFrequency, columns, condition)
        result = None
        if rows:
            result = rows[0][0]
        return result

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
        user_ids = ",".join(str(x) for x in users)
        return user_ids


    def get_users_by_unit_and_domain(
            self, unit_id, domain_id
        ):
        user_ids = self.get_user_ids_by_unit_and_domain(
            unit_id, domain_id
        )
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
        country_id
    ):
        condition = "1"
        if frequency_name:
            frequency_id = self.get_frequecy_id_by_name(frequency_name)
            if frequency_id is not None:
                condition = "c.frequency_id = %d" % int(frequency_id)

        compliance_ids_query = "SELECT group_concat(distinct compliance_id) \
            FROM tbl_client_compliances \
            WHERE client_statutory_id IN (SELECT client_statutory_id \
            FROM tbl_client_statutories WHERE unit_id = %d AND domain_id = %d) \
            AND compliance_opted = 1 AND statutory_opted = 1" % (
                unit_id, domain_id
            )
        compliance_id_rows = self.select_all(compliance_ids_query)
        statutory_wise_compliances = []
        level_1_statutory_wise_compliances = {}
        if level_1_statutory_name is not None:
            condition = "statutory_mapping like '%s%s'" % (
                level_1_statutory_name, "%"
            )
        if frequency_name is not None:
            condition = "frequency like '%s%s%s'" % (
                "%", frequency_name, "%"
            )
        if compliance_id_rows :
            compliance_ids = compliance_id_rows[0][0]
            query = "SELECT ac.compliance_id, ac.statutory_dates, ac.due_date, assignee, employee_code, \
                employee_name, statutory_mapping, document_name, compliance_task, \
                compliance_description, c.repeats_type_id, repeat_type, repeats_every, frequency, \
                c.frequency_id FROM %s ac LEFT JOIN %s u ON (ac.assignee = u.user_id) \
                LEFT JOIN %s c ON (ac.compliance_id = c.compliance_id) \
                LEFT JOIN %s f ON (c.frequency_id = f.frequency_id) \
                LEFT JOIN %s rt ON (c.repeats_type_id = rt.repeat_type_id) \
                WHERE ac.compliance_id IN (%s) AND ac.is_active = %d \
                AND unit_id = %d AND %s" % (
                    self.tblAssignedCompliances, self.tblUsers, self.tblCompliances,
                    self.tblComplianceFrequency, self.tblComplianceRepeatType, compliance_ids,
                    1, unit_id, condition
                )
            client_compliance_rows = self.select_all(query)
            if client_compliance_rows:
                columns = [
                    "compliance_id", "statutory_dates", "due_date", "assignee", "employee_code",
                    "employee_name", "statutory_mapping", "document_name", "compliance_task",
                    "compliance_description", "repeats_type_id",  "repeat_type", "repeat_every",
                    "frequency", "frequency_id"
                ]
                client_compliance_rows = self.convert_to_dict(client_compliance_rows, columns)
                for compliance in client_compliance_rows:
                    statutories = compliance["statutory_mapping"].split(">>")
                    if level_1_statutory_name is not None:
                        if statutories[0].strip() != level_1_statutory_name.strip():
                            continue
                    if statutories[0].strip() not in level_1_statutory_wise_compliances:
                        level_1_statutory_wise_compliances[statutories[0].strip()] = []

                    compliance_name = "%s - %s" % (
                        compliance["document_name"], compliance["compliance_task"]
                    )
                    assingee_name = "%s - %s" % (
                        compliance["employee_code"], compliance["employee_name"]
                    )
                    due_dates = []
                    statutory_dates_list = []
                    if ((compliance["frequency_id"] == 2) or (compliance["frequency_id"] == 3)):
                        if compliance["repeats_type_id"] == 1:# Days
                            due_dates, statutory_dates = self.calculate_due_date(
                                repeat_by = 1,
                                repeat_every = compliance["repeat_every"],
                                due_date = compliance["due_date"],
                                domain_id=domain_id,
                                country_id=country_id
                            )
                        elif compliance["repeats_type_id"] == 2:# Months
                            due_dates, statutory_dates_list = self.calculate_due_date(
                                statutory_dates = compliance["statutory_dates"],
                                repeat_by = 2,
                                repeat_every = compliance["repeat_every"],
                                due_date = compliance["due_date"],
                                domain_id=domain_id,
                                country_id=country_id
                            )
                        elif compliance["repeats_type_id"] == 3:# years
                            due_dates, statutory_dates = self.calculate_due_date(
                                repeat_by = 3,
                                repeat_every = compliance["repeat_every"],
                                due_date = compliance["due_date"],
                                domain_id=domain_id,
                                country_id=country_id
                            )
                    elif (compliance["frequency_id"] == 1):
                        pass
                    for due_date in due_dates:
                        if not self.is_already_completed_compliance(
                            due_date, compliance["compliance_id"], unit_id
                        ):
                            level_1_statutory_wise_compliances[statutories[0].strip()].append(
                                clienttransactions.UNIT_WISE_STATUTORIES_FOR_PAST_RECORDS(
                                    compliance["compliance_id"], compliance_name,
                                    compliance["compliance_description"],
                                    core.COMPLIANCE_FREQUENCY(compliance["frequency"]),
                                    statutory_dates_list, self.datetime_to_string(due_date),
                                    assingee_name, compliance["assignee"]
                                )
                            )
                        else:
                            pass
                for level_1_statutory_name, compliances in level_1_statutory_wise_compliances.iteritems():
                    if len(compliances) > 0:
                        statutory_wise_compliances.append(
                            clienttransactions.STATUTORY_WISE_COMPLIANCES(
                                level_1_statutory_name, compliances
                            )
                        )
        return statutory_wise_compliances


    def is_already_completed_compliance(
            self, due_date, compliance_id, unit_id
        ):
        columns = "count(*)"
        condition = "unit_id = '{}' and due_date = '{}' and compliance_id = '{}'".format(
            unit_id, due_date, compliance_id
        )
        rows = self.get_data(self.tblComplianceHistory, columns, condition)
        if rows[0][0] > 0:
            return True
        else:
            return False

    def calculate_from_and_to_date_for_domain(self, country_id, domain_id):
        columns = "period_from, period_to"
        condition = "country_id = '%d' and domain_id = '%d'" % (
            country_id, domain_id
        )
        rows = self.get_data(self.tblClientConfigurations, columns, condition)
        period_from = rows[0][0]
        period_to = rows[0][0]
        to_date = self.get_date_time()
        current_year = to_date.year
        previous_year = current_year-1
        from_date = datetime.datetime(previous_year, period_from, 1)
        r = relativedelta.relativedelta(to_date, from_date)
        no_of_years = r.years
        no_of_months = r.months
        if no_of_years is not 0 or no_of_months >= 12:
            from_date = datetime.datetime(current_year, period_from, 1)
        return from_date, to_date

    def calculate_due_date(
        self, country_id, domain_id, statutory_dates = None, repeat_by = None,
        repeat_every = None, due_date = None
    ):
        def is_future_date(test_date):
            result = False
            current_date = datetime.datetime.today()
            if ((current_date - test_date).days < 0):
                result = True
            return result
        from_date, to_date = self.calculate_from_and_to_date_for_domain(country_id, domain_id)
        due_dates = []
        statutory_dates_list = []
        # For Monthly Recurring compliances
        if statutory_dates and len(json.loads(statutory_dates)) > 1:
            for statutory_date in json.loads(statutory_dates):
                date = statutory_date["statutory_date"]
                month = statutory_date["statutory_month"]
                current_date = datetime.datetime.today()
                due_date_guess = datetime.datetime(current_date.year, month, date)
                real_due_date = None
                if is_future_date(due_date_guess):
                    real_due_date = datetime.datetime(current_date.year - 1, month, date)
                else:
                    real_due_date = due_date_guess
                if from_date <= real_due_date <= to_date:
                    due_dates.append(
                        real_due_date
                    )
                    statutory_dates_list.append(
                        core.StatutoryDate(
                            date, month, statutory_date["trigger_before_days"]
                        )
                    )
                else:
                    continue
        elif repeat_by:
            # For Compliances Recurring in days
            if repeat_by == 1:
                previous_year_due_date = datetime.datetime(
                    due_date.year - 1, due_date.month, due_date.day
                )
                if from_date <= previous_year_due_date <= to_date:
                    due_dates.append(previous_year_due_date)
                iter_due_date = previous_year_due_date
                while not is_future_date(iter_due_date):
                    iter_due_date = iter_due_date + datetime.timedelta(days = repeat_every)
                    if from_date <= iter_due_date <= to_date:
                        due_dates.append(iter_due_date)
            elif repeat_by == 2:
                previous_year_due_date = datetime.datetime(
                    due_date.year - 1, due_date.month, due_date.day
                )
                if from_date <= previous_year_due_date <= to_date:
                    due_dates.append(previous_year_due_date)
                iter_due_date = previous_year_due_date
                while not is_future_date(iter_due_date):
                    iter_due_date = iter_due_date + relativedelta.relativedelta(months = repeat_every)
                    if from_date <= iter_due_date <= to_date:
                        due_dates.append(iter_due_date)
            elif repeat_by == 3:
                previous_due_date = datetime.datetime(
                    due_date.year - repeat_every, due_date.month, due_date.day
                )
                r = relativedelta.relativedelta(
                    previous_due_date, due_date
                )
                if r.months < 12:
                    due_dates.append(previous_due_date)
        return due_dates, statutory_dates_list

    def convert_base64_to_file(self, file_name, file_content, client_id):
        client_directory = "%s/%d" % (CLIENT_DOCS_BASE_PATH, client_id)
        file_path = "%s/%s" % (client_directory, file_name)
        if not os.path.exists(client_directory):
            os.makedirs(client_directory)
        self.remove_uploaded_file(file_path)
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

    def save_past_record(
            self, unit_id, compliance_id, due_date, completion_date, documents,
            validity_date, completed_by, client_id
        ):
        is_uploading_file = False
        # Checking whether compliance already completed
        if self.is_already_completed_compliance(
                due_date, compliance_id, unit_id
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
        completion_date = self.string_to_datetime(completion_date)
        next_due_date = None
        if validity_date:
            next_due_date = self.string_to_datetime(validity_date)

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
            approved_by = rows [0][0]
            if is_two_level:
                concurred_by = rows[0][1]
        columns = [
            "compliance_history_id", "unit_id", "compliance_id", "due_date", "completion_date",
            "validity_date", "next_due_date", "completed_by", "completed_on",
            "approve_status", "approved_by", "approved_on"
        ]
        values = [
            compliance_history_id, unit_id, compliance_id, self.string_to_datetime(due_date),
            completion_date, self.string_to_datetime(validity_date),
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

    def get_compliance_approval_list(
            self, session_user, client_id
        ):
        assignee_columns = "completed_by, employee_code, employee_name"
        join_type = "inner join"
        tables = [self.tblComplianceHistory, self.tblUsers]
        aliases = ["tch", "tu"]
        join_condition = ["tch.completed_by = tu.user_id"]
        assignee_condition = "(completion_date is not Null and completion_date != 0 \
        ) and (completed_on is not Null and completed_on != 0 ) and "+\
        "(approve_status is Null or approve_status = 0) and (approved_by = '%d' or concurred_by = '%d')\
        group by completed_by" % (session_user, session_user)
        assignee_rows = self.get_data_from_multiple_tables(
            assignee_columns, tables,
            aliases, join_type,  join_condition,
            assignee_condition
        )
        approval_compliances = []
        for assignee in assignee_rows:
            query_columns = "compliance_history_id, tch.compliance_id, start_date,"+\
            " tch.due_date, documents, completion_date, completed_on, next_due_date, "+\
            "concurred_by, remarks, datediff(tch.due_date, completion_date ),compliance_task,"+\
            " compliance_description, tc.frequency_id, frequency, document_name, concurrence_status, \
            tac.statutory_dates, tch.validity_date"
            join_type = "inner join"
            query_tables = [
                    self.tblComplianceHistory,
                    self.tblCompliances,
                    self.tblComplianceFrequency,
                    self.tblAssignedCompliances
            ]
            aliases = ["tch", "tc", "tcf", "tac"]
            join_condition = [
                    "tch.compliance_id = tc.compliance_id",
                    "tc.frequency_id = tcf.frequency_id",
                    "tac.compliance_id = tc.compliance_id"
            ]
            where_condition = "(completion_date is not Null and \
            completion_date != 0 ) and (completed_on is not Null \
            and completed_on != 0) and \
            (approve_status is Null or approve_status = 0) and completed_by = '%d'"% (
                assignee[0]
            )
            rows = self.get_data_from_multiple_tables(
                query_columns, query_tables, aliases,
                join_type, join_condition,
                where_condition
            )
            compliances = []
            for row in rows:
                download_urls = []
                file_name = []
                if row[4] is not None and len(row[4]) > 0:
                    for document in row[4].split(","):
                        if documents is not None and document.strip(',') != '':
                            dl_url = "%s/%s" % (CLIENT_DOCS_DOWNLOAD_URL, document)
                            download_urls.append(dl_url)
                            file_name_part = document.split("-")[0]
                            file_extn_parts = document.split(".")
                            file_extn_part = None
                            if len(file_extn_parts) > 1:
                                file_extn_part = file_extn_parts[len(file_extn_parts)-1]
                            if file_extn_part is not None:
                                name  = "%s.%s" % (
                                    file_name_part, file_extn_part
                                )
                                file_name.append(name)
                            else:
                               file_name.append(file_name_part)
                concurred_by_id = None if row[8] is None else int(row[8])
                compliance_history_id = row[0]
                compliance_id = row[1]
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
                compliance_name = "%s - %s"%(row[15], row[11])
                compliance_description = row[12]
                frequency_id = int(row[13])
                frequency = core.COMPLIANCE_FREQUENCY(row[14])
                description = row[12]
                concurrence_status = bool(row[16])
                statutory_dates = [] if row[17] is None else json.loads(row[17])
                validity_date = None if row[18] is None else self.datetime_to_string(row[18])
                date_list = []
                for date in statutory_dates :
                    s_date = core.StatutoryDate(
                        date["statutory_date"],
                        date["statutory_month"],
                        date["trigger_before_days"]
                    )
                    date_list.append(s_date)

                domain_name_column = "domain_name"
                condition = " domain_id = (select domain_id from tbl_client_statutories "+\
                " where client_statutory_id = (select client_statutory_id from "+\
                " tbl_client_compliances where compliance_id ='%d' limit 1))" % compliance_id
                domain_name_row =  self.get_data(
                    self.tblDomains, domain_name_column,
                    condition
                )
                domain_name = domain_name_row[0][0]

                action = None
                if self.is_two_levels_of_approval():
                    if concurred_by_id == session_user:
                        if concurrence_status is True:
                            continue
                        else:
                            action = "Concur"
                    elif concurrence_status is True:
                        action = "Approve"
                    else:
                        continue
                elif concurred_by_id != session_user:
                    action = "Approve"
                else:
                    continue
                compliances.append(clienttransactions.APPROVALCOMPLIANCE(
                        compliance_history_id, compliance_name, description, domain_name,
                        start_date, due_date, delayed_by, frequency, documents,
                        file_names, completion_date, completed_on, next_due_date,
                        concurred_by, remarks, action, date_list, validity_date
                    )
                )
            assignee_id = assignee[0]
            assignee_name = "{} - {}".format(assignee[1], assignee[2])
            if len(compliances) > 0:
                approval_compliances.append(clienttransactions.APPORVALCOMPLIANCELIST(
                    assignee_id, assignee_name, compliances))
            else:
                continue
        return approval_compliances

    def get_user_name_by_id(self, user_id, client_id = None):
        employee_name = None
        if user_id != None and user_id != 0:
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

    def get_unit_name_by_id(self, unit_id):
        columns = "concat(unit_code, '-', unit_name)"
        condition = "unit_id ='{}'".format(unit_id)
        rows = self.get_data(
            self.tblUnits, columns, condition
        )
        return rows[0][0]

#
# Assign Compliance
#

    def get_units_for_assign_compliance(self, session_user, client_id=None):
        if session_user > 0 :
            qry = ' WHERE t1.unit_id in (select distinct unit_id from tbl_user_units where user_id = %s) ' % (int(session_user))
        else :
            qry = ""

        query = "SELECT distinct t1.unit_id, t1.unit_code, t1.unit_name, \
            t1.division_id, t1.legal_entity_id, t1.business_group_id, \
            t1.address, t1.country_id, domain_ids\
            FROM tbl_units t1 "
        query += qry
        rows = self.select_all(query)
        columns = [
            "unit_id", "unit_code", "unit_name",
            "division_id", "legal_entity_id",
            "business_group_id", "address", "country_id", "domain_ids"
        ]
        result = self.convert_to_dict(rows, columns)
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
        # where_condition = " WHERE t1.seating_unit_id In \
        #     (SELECT t.unit_id FROM tbl_user_units t \
        #     WHERE t.user_id = %s)" % (
        #         session_user
        #     )
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
            ON t1.user_id = t2.user_id "

        if session_user > 0 :
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
            unit_id = None
            if r["seating_unit_id"]:
                unit_id = int(r["seating_unit_id"])
            domain_ids = [
                int(x) for x in r["domain_ids"].split(',')
            ]
            unit_ids = [
                int(y) for y in r["unit_ids"].split(',')
            ]
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

    def get_assign_compliance_statutories_for_units(
        self, unit_ids, session_user, client_id
    ):
        if len(unit_ids) == 1 :
            unit_ids.append(0)
        if session_user == 0 :
            session_user = '%'
        query = "SELECT distinct t2.compliance_id,\
            t1.domain_id,\
            UC.units,\
            t2.statutory_applicable, \
            t2.statutory_opted,\
            t2.not_applicable_remarks,\
            t2.compliance_applicable,\
            t2.compliance_opted,\
            t2.compliance_remarks,\
            t3.compliance_task,\
            t3.document_name,\
            t3.compliance_description,\
            t3.statutory_mapping,\
            t3.statutory_provision,\
            t3.statutory_dates,\
            (select frequency from tbl_compliance_frequency where frequency_id = t3.frequency_id)frequency, t3.frequency_id, \
            (select duration_type from tbl_compliance_duration_type where duration_type_id = t3.duration_type_id) duration_type, t3.duration,\
            (select repeat_type from tbl_compliance_repeat_type where repeat_type_id = t3.repeats_type_id) repeat_type, t3.repeats_every\
            FROM tbl_client_compliances t2 \
            INNER JOIN tbl_client_statutories t1 \
            ON t2.client_statutory_id = t1.client_statutory_id \
            INNER JOIN tbl_compliances t3 \
            ON t2.compliance_id = t3.compliance_id \
            INNER JOIN \
            (SELECT distinct U.compliance_id, group_concat(distinct U.unit_id) units FROM  \
            (SELECT A.unit_id, A.client_statutory_id, B.compliance_id FROM tbl_client_statutories A \
            INNER JOIN tbl_client_compliances B \
            ON A.client_statutory_id = B.client_statutory_id \
            AND B.compliance_opted = 1 \
            AND A.unit_id IN %s) U \
            group by U.compliance_id )UC \
            ON t2.compliance_id = UC.compliance_id \
            WHERE \
            t2.compliance_id NOT IN (SELECT C.compliance_id \
            FROM tbl_assigned_compliances C WHERE \
            C.unit_id IN %s ) \
            AND t1.unit_id IN %s \
            AND t2.statutory_opted = 1 \
            AND t2.compliance_opted = 1 \
            AND t3.is_active = 1 " % (
                str(tuple(unit_ids)),
                str(tuple(unit_ids)),
                str(tuple(unit_ids)),
            )

        rows = self.select_all(query)
        columns = [
            "compliance_id", "domain_id", "units",
            "statutory_applicable", "statutory_opted",
            "not_applicable_remarks",
            "compliance_applicable", "compliance_opted",
            "compliance_remarks", "compliance_task",
            "document_name", "compliance_description",
            "statutory_mapping", "statutory_provision",
            "statutory_dates", "frequency", "frequency_id", "duration_type", "duration",
            "repeat_type", "repeats_every"
        ]
        result = self.convert_to_dict(rows, columns)
        return self.return_assign_compliance_data(result)

    def return_assign_compliance_data(self, result):
        now = datetime.datetime.now()

        current_year = now.year
        domain_wise_compliance = {}
        for r in result:
            domain_id = int(r["domain_id"])
            maipping = r["statutory_mapping"].split(">>")
            level_1 = maipping[0].strip()
            unit_ids = [
                int(x) for x in r["units"].split(',')
            ]
            level_1_wise = domain_wise_compliance.get(domain_id)
            if level_1_wise is None :
                level_1_wise = {}

            compliance_list = level_1_wise.get(level_1)
            if compliance_list is None :
                compliance_list = []
            if r["document_name"] not in ("", "None", None):
                name = "%s - %s" % (r["document_name"], r["compliance_task"])
            else :
                name = r["compliance_task"]
            statutory_dates = r["statutory_dates"]
            statutory_dates = json.loads(statutory_dates)
            date_list = []
            due_date = None
            due_date_list = []

            for date in statutory_dates:
                s_date = core.StatutoryDate(
                    date["statutory_date"],
                    date["statutory_month"],
                    date["trigger_before_days"]
                )
                date_list.append(s_date)

                s_month = date["statutory_month"]
                s_day = date["statutory_date"]
                current_date = n_date = datetime.date.today()

                if s_date.statutory_month is not None :
                    n_date = n_date.replace(month=s_month)

                if s_date.statutory_date is not None :
                    n_date = n_date.replace(day=s_day)

                if current_date > n_date:
                    n_date = n_date.replace(year=current_year+1)

                due_date = n_date.strftime("%d-%b-%Y")
                due_date_list.append(due_date)

            if r["frequency_id"] in (2, 3) :
                summary = "Repeats every %s - %s" % (r["repeats_every"], r["repeat_type"])
            elif r["frequency_id"] == 4 :
                summary = "To complete within %s - %s" % (r["duration"], r["duration_type"])
            else :
                summary = None

            compliance = clienttransactions.UNIT_WISE_STATUTORIES(
                r["compliance_id"],
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
            domain_wise_compliance[domain_id] = level_1_wise
        return domain_wise_compliance

    def save_assigned_compliance(self, request, session_user, client_id):
        created_on = self.get_date_time()
        country_id = int(request.country_id)
        assignee = int(request.assignee)
        concurrence = request.concurrence_person
        if concurrence is None :
            concurrence = ""
        approval = int(request.approval_person)
        compliances = request.compliances
        compliance_names = []
        for c in compliances:
            compliance_id = int(c.compliance_id)
            compliance_names.append(c.compliance_name)
            statutory_dates = c.statutory_dates
            if statutory_dates is not None :
                date_list = []
                for dates in statutory_dates :
                    date_list.append(dates.to_structure())
                date_list = json.dumps(date_list)
                # due_date = datetime.datetime.strptime(c.due_date, "%d-%b-%Y")
                # validity_date = c.validity_date
            else :
                date_list = []

            unit_ids = c.unit_ids
            if c.trigger_before is not None :
                trigger_before = int(c.trigger_before)
            else :
                trigger_before = ""
            if c.due_date is not None :
                due_date = datetime.datetime.strptime(c.due_date, "%d-%b-%Y")
            else :
                due_date = ""
            validity_date = c.validity_date
            if validity_date is not None :
                validity_date = datetime.datetime.strptime(validity_date, "%d-%b-%Y")
                if due_date > validity_date :
                    due_date = validity_date
                elif (validity_date - datetime.timedelta(days=60)) < due_date :
                    due_date = validity_date
            else :
                validity_date = ""

            for unit_id in unit_ids:
                query = "INSERT INTO tbl_assigned_compliances \
                    (country_id, unit_id, compliance_id, \
                    statutory_dates, assignee, \
                    concurrence_person, approval_person, \
                    trigger_before_days, due_date, validity_date, created_by, \
                    created_on) VALUES \
                    (%s, %s, %s, '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                        country_id, unit_id, compliance_id,
                        date_list, assignee, concurrence,
                        approval, trigger_before, due_date, validity_date,
                        int(session_user), created_on
                    )
                self.execute(query)
            # self.update_user_units(assignee, unit_ids, client_id)
        compliance_names = json.dumps(compliance_names)
        if request.concurrence_person_name is None :
            action = "Compliances %s assigned to assignee - %s and approval-person - %s " % (
                str(compliance_names), request.assignee_name,
                request.approval_person_name
            )
        else :
            action = "Compliances %s assigned to assignee - %s concurrence-person - %s approval-person - %s " % (
                str(compliance_names), request.assignee_name, request.concurrence_person_name,
                request.approval_person_name
            )
        action = json.dumps(action)
        self.save_activity(session_user, 7, action)
        return clienttransactions.SaveAssignedComplianceSuccess()

    def update_user_units(self, user_id, unit_ids, client_id):
        user_units = self.get_user_unit_ids(user_id, client_id)
        user_units = [int(x) for x in user_units.split(',')]
        new_units = []
        for u_id in unit_ids :
            if u_id not in user_units :
                new_units.append(u_id)

        if len(new_units) > 0 :
            unit_values_list = []
            unit_columns = ["user_id", "unit_id"]
            for unit_id in new_units:
                unit_value_tuple = (int(user_id), int(unit_id))
                unit_values_list.append(unit_value_tuple)
            result4 = self.bulk_insert(self.tblUserUnits, unit_columns, unit_values_list, client_id)
            action = "New units %s added for user %s while assign compliance " % (new_units, user_id)
            self.save_activity(user_id, 7, action)

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
        t1.period_from, t1.period_to from tbl_client_configurations t1"
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
        # countries = self.get_user_countries(user_id)
        # country_ids = countries.split(',')
        country_ids = request.country_ids

        if len(country_ids) == 1 :
            country_ids.append(0)
        # domains = self.get_user_domains(user_id)
        # domain_ids = domains.split(',')
        domain_ids = request.domain_ids

        if len(domain_ids) == 1 :
            domain_ids.append(0)
        filter_type = request.filter_type

        # domain_ids = request.domain_ids
        year_range_qry = ""
        filter_ids = country_ids
        if chart_type is None :
            from_date = request.from_date
            to_date = request.to_date
            chart_year = request.chart_year
            year_condition = self.get_client_domain_configuration(chart_year)[1]

            for i, y in enumerate(year_condition):
                if i == 0 :
                    year_range_qry = y
                else :
                    year_range_qry += "OR %s" % (y)
            year_range_qry = "AND (%s)" % year_range_qry

        else :
            from_date = None
            to_date = None

        if filter_type == "Group" :
            group_by_name = "T3.country_id"
            filter_type_ids = ""

        elif filter_type == "BusinessGroup" :
            filters = self.get_user_business_group_ids(user_id)
            filter_ids = filters.split(',')
            if len(filter_ids) == 1 :
                filter_ids.append(0)
            group_by_name = "T3.business_group_id"
            filter_type_ids = "AND T3.business_group_id in %s" % str(tuple(filter_ids))

        elif filter_type == "LegalEntity" :
            filters = self.get_user_legal_entity_ids(user_id)
            filter_ids = filters.split(',')
            if len(filter_ids) == 1 :
                filter_ids.append(0)
            group_by_name = "T3.legal_entity_id"
            filter_type_ids = "AND T3.legal_entity_id in %s" % str(tuple(filter_ids))

        elif filter_type == "Division" :
            filters = self.get_user_division_ids(user_id)
            filter_ids = filters.split(',')
            if len(filter_ids) == 1 :
                filter_ids.append(0)
            group_by_name = "T3.division_id"
            filter_type_ids = "AND T3.division_id in %s" % str(tuple(filter_ids))

        elif filter_type == "Unit":
            filters = self.get_user_unit_ids(user_id)
            filter_ids = filters.split(',')
            if len(filter_ids) == 1 :
                filter_ids.append(0)
            group_by_name = "T3.unit_id"
            filter_type_ids = "AND T3.unit_id in %s" % str(tuple(filter_ids))

        elif filter_type == "Consolidated":
            group_by_name = "T3.country_id"
            filter_type_ids = ""

        if user_id == 0 :
            user_id = '%'

        date_qry = ""
        if from_date is not None and to_date is not None :
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
            WHERE T1.completed_by LIKE '%s'\
            %s \
            %s \
            %s \
            AND T3.country_id IN %s \
            AND T2.domain_id IN %s  \
            %s \
            GROUP BY month, year, T2.domain_id, %s\
            ORDER BY month desc, year desc, %s" % (
                group_by_name,
                user_id,
                year_range_qry,
                status_type_qry,
                date_qry,
                str(tuple(country_ids)),
                str(tuple(domain_ids)),
                filter_type_ids,
                group_by_name,
                group_by_name
            )

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
            elif current_month in [int(m) for m in range(1, month_to+1)] :
                first_year = current_year - 1
                second_year = current_year

            for i in range(1, 8):
                if i == 1 :
                    years = [first_year, second_year]
                else :
                    first_year = current_year - i
                    second_year = first_year + 1
                    years = [first_year, second_year]

                double_years.append(years)
            return double_years

    def get_status_wise_compliances_count(self, request, session_user):
        user_id = int(session_user)
        from_date = request.from_date
        to_date = request.to_date
        chart_year = request.chart_year

        filter_ids = []

        inprogress_qry = " AND T1.due_date >= CURDATE() \
                AND IFNULL(T1.approve_status,0) <> 1"

        complied_qry = " AND T1.due_date >= T1.completion_date \
                AND IFNULL(T1.approve_status,0) = 1"

        delayed_qry = " AND T1.due_date < T1.completion_date \
                AND IFNULL(T1.approve_status,0) = 1"

        not_complied_qry = " AND T1.due_date < CURDATE() \
                AND IFNULL(T1.approve_status,0) <> 1"

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
        # if country_id is not None and domain_id is not None :
        #     where_qry = " WHERE country_id = %s AND domain_id = %s" % (country_id, domain_id)

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

                    if status == "inprogress":
                        compliance_count_info["inprogress_count"] += compliance_count
                    elif status == "complied" :
                        compliance_count_info["complied_count"] += compliance_count
                    elif status == "delayed" :
                        compliance_count_info["delayed_count"] += compliance_count
                    elif status == "not_complied":
                        compliance_count_info["not_complied_count"] += compliance_count

                    compliance_count_info["domain_id"] = domain_id
                    compliance_count_info["country_id"] = country_id
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
        return dashboard.GetComplianceStatusChartSuccess(result)

    def compliance_details_query(self, domain_ids, date_qry, status_qry, filter_type_qry, user_id) :
        if len(domain_ids) == 1 :
            domain_ids.append(0)
        if user_id == 0 :
            user_id = '%'
        query = "SELECT \
            T1.compliance_history_id, T1.unit_id,\
            T1.compliance_id, T1.start_date, \
            T1.due_date, T1.completion_date, \
            T1.completed_by,\
            T4.compliance_task, T4.document_name, \
            T4.compliance_description, T4.statutory_mapping, \
            unit_name, \
            (select division_name from tbl_divisions where division_id = T5.division_id)division_name, \
            (select legal_entity_name from tbl_legal_entities where legal_entity_id = T5.legal_entity_id)legal_entity_name,  \
            (select business_group_name from tbl_business_groups where business_group_id = T5.business_group_id )business_group_name, \
            (select country_name from tbl_countries where country_id = T5.country_id)country_name, \
            employee_name,\
            T5.unit_code, T5.address, T5.geography, T5.postal_code,\
            T5.industry_name, T5.country_id, \
            T4.domain_id, \
            YEAR(T1.due_date) as year, \
            MONTH(T1.due_date) as month \
            FROM tbl_compliance_history T1  \
            INNER JOIN tbl_compliances T4  ON T1.compliance_id = T4.compliance_id  \
            INNER JOIN tbl_units T5 ON T1.unit_id = T5.unit_id \
            INNER JOIN tbl_users T10 ON T1.completed_by = T10.user_id \
            WHERE T1.completed_by LIKE '%s' AND \
            T4.domain_id IN %s  \
            %s \
            %s \
            %s \
            ORDER BY T1.due_date desc" % (
                user_id,
                str(tuple(domain_ids)),
                date_qry,
                status_qry,
                filter_type_qry,
            )
        rows = self.select_all(query)
        columns = [
            "compliance_history_id", "unit_id",
            "compliance_id", "start_date", "due_date",
            "completion_date", "assignee", "compliance_task",
            "document_name", "compliance_description",
            "statutory_mapping", "unit_name", "division_name",
            "legal_entity_name", "business_group_name",
            "country_name", "employee_name",
            "unit_code", "address", "geography",
            "postal_code", "industry_name",
            "country_id", "domain_id",
            "year", "month"
        ]
        result = self.convert_to_dict(rows, columns)
        return result

    def get_compliances_details_for_status_chart(self, request, session_user, client_id):
        domain_ids = request.domain_ids
        from_date = request.from_date
        to_date = request.to_date
        year = request.year
        filter_type = request.filter_type
        filter_id = request.filter_id
        compliance_status = request.compliance_status

        status_qry = ""
        if compliance_status == "Inprogress" :
            status_qry = " AND T1.due_date >= CURDATE() \
                    AND IFNULL(T1.approve_status, 0) != 1"

        elif compliance_status == "Complied" :
            status_qry = " AND T1.due_date >= T1.completion_date \
                AND T1.approve_status = 1"

        elif compliance_status == "Delayed Compliance" :
            status_qry = " AND T1.due_date < T1.completion_date \
                AND T1.approve_status = 1"

        elif compliance_status == "Not Complied" :
            status_qry = " AND T1.due_date < CURDATE() \
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
            date_qry = " AND T1.due_date >= '%s' AND T1.due_date <= '%s' " % (from_date, to_date)

        result = self.compliance_details_query(domain_ids, date_qry, status_qry, filter_type_qry, session_user)
        year_info = self.get_client_domain_configuration(int(year))[0]
        return self.return_compliance_details_drill_down(year_info, compliance_status, request.year, result, client_id)

    def return_compliance_details_drill_down(self, year_info, compliance_status, request_year, result, client_id) :
        current_date = datetime.date.today()

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
                ageing = abs((due_date - current_date).days) + 1
            elif compliance_status == "Complied" :
                ageing = 0
            elif compliance_status == "Not Complied" :
                ageing = abs((current_date - due_date).days) + 1
            elif compliance_status == "Delayed Compliance" :
                ageing = abs((completion_date - due_date).days) + 1

            status = core.COMPLIANCE_STATUS(compliance_status)
            if r["document_name"] not in ("", "None", None):
                name = "%s-%s" % (r["document_name"], r["compliance_task"])
            else :
                name = r["compliance_task"]
            compliance = dashboard.Level1Compliance(
                name, r["compliance_description"], r["employee_name"],
                str(r["start_date"]), str(due_date),
                str(completion_date), status,
                ageing
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

        not_complied_qry = " AND T1.due_date < CURDATE() \
                AND T1.approve_status is NULL "


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

        for filter_type, value in calculated_data.iteritems():
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

        # final_result_list = []
        # print
        # print escalation_years
        # for k, v in filter_type_wise.items():
        #     data_list = []
        #     for i, j in v.items():
        #         data_list.extend(j)
        #     chart = dashboard.ChartDataMap(k, data_list)
        #     final_result_list.append(chart)

        return dashboard.GetEscalationsChartSuccess(
            years, chart_data
        )

    def get_escalation_drill_down_data(self, request, session_user, client_id):
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
            filter_type_qry, session_user
        )

        delayed_details_list = self.return_compliance_details_drill_down(
            year_info, "Delayed Compliance", year,
            delayed_details, client_id
        )

        not_complied_details = self.compliance_details_query(
            domain_ids, date_qry, not_complied_status_qry,
            filter_type_qry, session_user
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
        filter_ids = request.filter_ids
        if len(filter_ids) == 1 :
            filter_ids.append(0)

        filter_type_ids = ""

        if filter_type == "Group" :
            group_by_name = "T4.country_id"

        elif filter_type == "BusinessGroup" :
            group_by_name = "T4.business_group_id"
            filter_type_ids = "AND T4.business_group_id IN %s" % str(tuple(filter_ids))

        elif filter_type == "LegalEntity" :
            group_by_name = "T4.legal_entity_id"
            filter_type_ids = "AND T4.legal_entity_id IN %s" % str(tuple(filter_ids))

        elif filter_type == "Division" :
            group_by_name = "T4.division_id"
            filter_type_ids = "AND T4.division_id IN %s" % str(tuple(filter_ids))

        elif filter_type == "Unit":
            group_by_name = "T4.unit_id"
            filter_type_ids = "AND T4.unit_id IN %s" % str(tuple(filter_ids))

        query = "SELECT T1.compliance_history_id, T1.unit_id, \
            T1.compliance_id, T1.start_date, T1.due_date \
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
            "start_date", "due_date"
        ]
        not_complied = self.convert_to_dict(rows, columns)
        current_date = datetime.date.today()
        below_30 = 0
        below_60 = 0
        below_90 = 0
        above_90 = 0
        for i in not_complied :
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

    def get_not_complied_drill_down(self, request, session_user, client_id):
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
            filter_type_qry, session_user
        )
        current_date = datetime.date.today()
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

        current_date = datetime.date.today()

        unit_wise_data = {}
        for r in not_complied_details_filtered :

            unit_id = int(r["unit_id"])
            statutories = r["statutory_mapping"].split('>>')
            level_1 = statutories[0].strip()
            ageing = 0
            due_date = r["due_date"]
            completion_date = r["completion_date"]

            ageing = abs((current_date - due_date).days) + 1

            status = core.COMPLIANCE_STATUS("Not Complied")
            name = "%s-%s" % (r["document_name"], r["compliance_task"])
            compliance = dashboard.Level1Compliance(
                name, r["compliance_description"], r["employee_name"],
                str(r["start_date"]), str(due_date),
                str(completion_date), status,
                ageing
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
                compliance_list = level_compliance[level_1]
                if compliance_list is None :
                    compliance_list = []
                compliance_list.append(compliance)

                level_compliance[level_1] = compliance_list
                drill_down_data.compliances = level_compliance

            unit_wise_data[unit_id] = drill_down_data

        return unit_wise_data


    # unitwise compliance report
    def get_unitwise_compliance_report(
        self, country_id, domain_id, business_group_id,
        legal_entity_id, division_id, unit_id, user_id, session_user
    ) :
        if unit_id is None :
            unit_ids = self.get_user_unit_ids(session_user)
        else:
            unit_ids = unit_id

        q = "SELECT u.business_group_id, u.legal_entity_id, u.division_id,  \
            bg.business_group_name, le.legal_entity_name, d.division_name \
            FROM tbl_units u \
            INNER JOIN tbl_business_groups bg \
            ON u.business_group_id = bg.business_group_id \
            INNER JOIN tbl_legal_entities le \
            ON u.legal_entity_id = le.legal_entity_id \
            INNER JOIN tbl_divisions d \
            ON u.division_id = d.division_id \
            WHERE u.business_group_id like '%s' \
            and u.legal_entity_id like '%s' \
            and u.division_id like '%s' \
            GROUP BY u.business_group_id, u.legal_entity_id, u.division_id" % (
                str(business_group_id),
                str(legal_entity_id),
                str(division_id)
            )
        rows = self.select_all(q)

        unit_wise_compliances_list = []
        for row in rows:
            business_group_name = row[3]
            legal_entity_name = row[4]
            division_name = row[5]
            unit_columns = "unit_id, unit_code, unit_name, address"
            detail_condition = "legal_entity_id = '%d' " % row[1]
            if row[0] == None:
                detail_condition += " And business_group_id is NULL"
            else:
                detail_condition += " And business_group_id = '%d'" % row[0]
            if row[2] == None:
                detail_condition += " And division_id is NULL"
            else:
                detail_condition += " And division_id = '%d'" % row[2]
            unit_condition = detail_condition + " and country_id = '%d' and unit_id in (%s)" % (
                country_id, unit_ids
            )
            unit_rows = self.get_data(
                self.tblUnits, unit_columns, unit_condition
            )
            unit_wise_compliances = {}
            for unit in unit_rows:
                unit_id = unit[0]
                unit_name = "%s - %s " % (unit[1], unit[2])
                unit_address = unit[3]

                query = "select c.compliance_task, c.compliance_description, ac.statutory_dates, ch.validity_date, ch.due_date, \
                        ac.assignee, cf.frequency from tbl_client_statutories cs, tbl_client_compliances cc, tbl_compliances c, \
                        tbl_assigned_compliances ac, tbl_compliance_frequency cf, tbl_compliance_history ch where \
                        ch.compliance_id = ac.compliance_id and ch.unit_id = ac.unit_id and ch.next_due_date = ac.due_date and \
                        cs.country_id = %s and cs.domain_id = %s and cs.unit_id like '%s' \
                        and cs.client_statutory_id = cc.client_statutory_id and c.compliance_id = cc.compliance_id \
                        and c.compliance_id = ac.compliance_id and ac.unit_id = cs.unit_id and cf.frequency_id = c.frequency_id and ac.assignee like '%s' " % (
                        country_id, domain_id,
                        unit_id, user_id
                    )
                compliance_rows = self.select_all(query)

                compliances_list = []
                for compliance in compliance_rows:
                    statutory_dates = compliance[2]
                    statutory_dates = json.loads(statutory_dates)
                    date_list = []
                    for date in statutory_dates :
                        s_date = core.StatutoryDate(
                            date["statutory_date"],
                            date["statutory_month"],
                            date["trigger_before_days"]
                        )
                        date_list.append(s_date)

                    compliance_name = compliance[0]
                    description = compliance[1]
                    statutory_date = date_list
                    compliance_frequency = core.COMPLIANCE_FREQUENCY(
                        compliance[6]
                    )
                    due_date = self.datetime_to_string(compliance[4])

                    validity_date = None
                    if(validity_date is not None):
                        validity_date = self.datetime_to_string(compliance[3])

                    compliances_list.append(
                        clientreport.ComplianceUnit(
                            compliance_name, unit_address,
                            compliance_frequency, description, statutory_date,
                            due_date, validity_date
                            )
                        )
                unit_wise_compliances[unit_name] = compliances_list
            unit_wise_compliances_list.append(clientreport.UnitCompliance(
                business_group_name, legal_entity_name, division_name,
                unit_wise_compliances))
        return unit_wise_compliances_list

    # assigneewise compliance report
    def get_assigneewise_compliance_report(
        self, country_id, domain_id, business_group_id,
        legal_entity_id, division_id, unit_id, user_id,
        session_user
    ) :

        if unit_id is None :
            unit_ids = self.get_user_unit_ids(session_user)
        else:
            unit_ids = unit_id

        q = "SELECT u.business_group_id, u.legal_entity_id, u.division_id,  \
            bg.business_group_name, le.legal_entity_name, d.division_name \
            FROM tbl_units u \
            INNER JOIN tbl_business_groups bg \
            ON u.business_group_id = bg.business_group_id \
            INNER JOIN tbl_legal_entities le \
            ON u.legal_entity_id = le.legal_entity_id \
            INNER JOIN tbl_divisions d \
            ON u.division_id = d.division_id \
            WHERE u.business_group_id like '%s' \
            and u.legal_entity_id like '%s' \
            and u.division_id like '%s' \
            GROUP BY u.business_group_id, u.legal_entity_id, u.division_id" % (
                str(business_group_id),
                str(legal_entity_id),
                str(division_id)
            )
        rows = self.select_all(q)

        assignee_wise_compliances_list = []
        for row in rows:
            business_group_name = row[3]
            legal_entity_name = row[4]
            division_name = row[5]
            q = "SELECT ac.assignee, \
            (SELECT concat( u.employee_code, '-' ,u.employee_name ) FROM tbl_users u WHERE u.user_id = ac.assignee) AS assigneename, \
            (SELECT concat( u.employee_code, '-', u.employee_name )FROM tbl_users u WHERE u.user_id = ac.concurrence_person) AS concurrencename,\
            (SELECT concat( u.employee_code, '-', u.employee_name )FROM tbl_users u WHERE u.user_id = ac.approval_person) AS approvalname \
            FROM tbl_client_statutories cs, tbl_client_compliances cc, tbl_assigned_compliances ac, tbl_units ut \
            WHERE cs.country_id = %s  and ut.unit_id = (SELECT u.seating_unit_id from tbl_users u WHERE u.user_id = ac.assignee) \
            AND ut.business_group_id = %s and ut.legal_entity_id = %s and ut.division_id = %s \
            AND cs.domain_id = %s \
            AND cs.client_statutory_id = cc.client_statutory_id  AND ac.assignee like '%s'\
            GROUP BY ac.assignee, ac.concurrence_person, ac.approval_person \
            ORDER BY ac.assignee" % (
                        country_id, row[0], row[1], row[2], domain_id, user_id
                    )

            assigneerows = self.select_all(q)

            assignee_wise_compliances = []
            for assignee in assigneerows:
                assignee_id = assignee[0]
                assingee_name = assignee[1]
                concurrence_person = assignee[2]
                approval_person = assignee[3]
                query = "SELECT c.compliance_task, c.compliance_description, ac.statutory_dates, ch.validity_date, ch.due_date, \
                        ac.assignee, cf.frequency FROM tbl_client_statutories cs, tbl_client_compliances cc, tbl_compliances c, \
                        tbl_assigned_compliances ac, tbl_compliance_frequency cf, tbl_compliance_history ch where \
                        ch.compliance_id = ac.compliance_id and ch.unit_id = ac.unit_id and ch.next_due_date = ac.due_date and \
                        cs.country_id = %s and cs.domain_id = %s and cs.unit_id in (%s) \
                        and cs.client_statutory_id = cc.client_statutory_id and c.compliance_id = cc.compliance_id \
                        and c.compliance_id = ac.compliance_id and ac.unit_id = cs.unit_id and cf.frequency_id = c.frequency_id and ac.assignee = '%s' " % (
                        country_id, domain_id,
                        unit_ids, assignee_id
                    )
                compliance_rows = self.select_all(query)

                compliances_list = []
                for compliance in compliance_rows:
                    statutory_dates = compliance[2]
                    statutory_dates = json.loads(statutory_dates)
                    date_list = []
                    for date in statutory_dates :
                        s_date = core.StatutoryDate(
                            date["statutory_date"],
                            date["statutory_month"],
                            date["trigger_before_days"]
                        )
                        date_list.append(s_date)

                    compliance_name = compliance[0]
                    description = compliance[1]
                    statutory_date = date_list
                    compliance_frequency = core.COMPLIANCE_FREQUENCY(
                        compliance[6]
                    )
                    due_date = self.datetime_to_string(compliance[4])

                    validity_date = None
                    if(validity_date is not None):
                        validity_date = self.datetime_to_string(compliance[3])

                    compliances_list.append(
                        clientreport.ComplianceUnit(
                            compliance_name, "unit_name",
                            compliance_frequency, description,
                            statutory_date,
                            due_date, validity_date)
                        )

                assignee_wise_compliances.append(
                    clientreport.UserWiseCompliance(
                        assingee_name, concurrence_person,
                        approval_person,
                        compliances_list
                        )
                    )

            assignee_wise_compliances_list.append(
                clientreport.AssigneeCompliance(
                    business_group_name, legal_entity_name,
                    division_name,
                    assignee_wise_compliances
                    )
                )
        return assignee_wise_compliances_list

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
        self, request, session_user, client_id
    ):
        query = "SELECT T1.compliance_id, T2.unit_id, T4.frequency_id, \
            (select frequency from tbl_compliance_frequency where frequency_id = T4.frequency_id) frequency,\
            (select repeat_type from tbl_compliance_repeat_type where repeat_type_id = T4.repeats_type_id) repeats_type, \
            (select duration_type from tbl_compliance_duration_type where duration_type_id = T4.duration_type_id)duration_type,\
            T4.statutory_mapping, T4.statutory_provision,\
            T4.compliance_task, T4.compliance_description,  \
            T4.document_name, T4.format_file, T4.format_file_size, T4.penal_consequences, \
            T4.statutory_dates, T4.repeats_every, T4.duration, T4.is_active \
            FROM tbl_client_compliances T1 \
            INNER JOIN tbl_client_statutories T2 \
            ON T1.client_statutory_id = T2.client_statutory_id \
            INNER JOIN tbl_units T3 \
            ON T2.unit_id = T3.unit_id \
            INNER JOIN tbl_compliances T4\
            ON T1.compliance_id = T4.compliance_id\
            WHERE T2.country_id IN %s \
            AND T2.domain_id IN %s \
            %s %s"

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
            applicable_type_qry
        )
        rows = self.select_all(query1)
        columns = [
            "compliance_id", "unit_id", "frequency_id",
            "frequency", "repeats_type", "duration_type",
            "statutory_mapping", "statutory_provision", "compliance_task",
            "compliance_description", "document_name", "format_file",
            "format_file_size", "penal_consequences", "statutory_dates",
            "repeats_every", "duration", "is_active"
        ]
        result = self.convert_to_dict(rows, columns)

        level_1_wise_compliance = {}

        for r in result :
            unit_id = int(r["unit_id"])
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
                    s["trigger_before_days"]
                )
                date_list.append(s_date)

            format_file = r["format_file"]
            format_file_size = r["format_file_size"]
            file_list = []
            download_file_list = []
            if format_file is not None and format_file_size is not None :
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
            else :
                file_list = None
                download_file_list = None

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
                compliance_dict[unit_id] = compliance_list
                level_1_wise_data = dashboard.ApplicableDrillDown(
                    level_1, compliance_dict
                )
            else :
                compliance_dict = level_1_wise_data.compliances
                compliance_list = compliance_dict.get(unit_id)
                if compliance_list is None :
                    compliance_list = []
                compliance_list.append(compliance)

                compliance_dict[unit_id] = compliance_list
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
        columns = ["approve_status", "approved_on", "remarks"]
        condition = "compliance_history_id = '%d'" % compliance_history_id
        values = [1, self.get_date_time(), remarks]
        self.update(self.tblComplianceHistory, columns, values, condition, client_id)
        get_columns = "unit_id, compliance_id"
        rows = self.get_data(
            self.tblComplianceHistory, get_columns, condition
        )
        columns = []
        if next_due_date is not None:
            columns.append("due_date")
            condition = " unit_id = '%d' and compliance_id = '%d'" % (
                rows[0][0], rows[0][1])
            values = [self.string_to_datetime(next_due_date)]
        if validity_date is not None:
            columns.append("validity_date")
            values.append(self.string_to_datetime(validity_date))
        if len(columns) > 0 and len(values) > 0 and len(columns) == len(values):
            self.update(self.tblAssignedCompliances, columns, values, condition, client_id)

        get_columns = "unit_id, compliance_id, due_date, completion_date"
        condition = "compliance_history_id = '%d'" % compliance_history_id
        rows = self.get_data(
            self.tblComplianceHistory, get_columns, condition
        )
        unit_id = rows[0][0]
        compliance_id = rows[0][1]
        due_date = rows[0][2]
        completion_date = rows[0][3]
        status = "Complied"
        due_date_parts = str(due_date).split("-")
        due_date = datetime.date(
            int(due_date_parts[0]), int(due_date_parts[1]), int(due_date_parts[2])
        )
        if due_date < completion_date:
            status = "Delayed Compliance"
        self.save_compliance_activity(
            unit_id, compliance_id, "Approved", status,
            remarks
        )
        # notify_compliance_approved = threading.Thread(
        #     target=self.notify_compliance_approved, args=[
        #         self, compliance_history_id, "Approved"
        #     ]
        # )
        # notify_compliance_approved.start()
        email.notify_task_approved(
                self, compliance_history_id, "Approved"
        )
        return True

    def notify_compliance_approved(self, db, compliance_history_id, approval_status):
        try:
            email.notify_task_approved(
                db, compliance_history_id, approval_status
            )
        except Exception, e:
            print "Error while sending email : {}".format(e)

    def reject_compliance_approval(self, compliance_history_id, remarks,
        next_due_date, client_id):
        columns = "unit_id, compliance_id, due_date, completion_date"
        condition = "compliance_history_id = '%d'" % compliance_history_id
        rows = self.get_data(
            self.tblComplianceHistory, columns, condition
        )
        unit_id = rows[0][0]
        compliance_id = rows[0][1]
        due_date = rows[0][2]
        completion_date = rows[0][3]
        status = "Inprogress"
        due_date_parts = str(due_date).split("-")
        due_date = datetime.date(
            int(due_date_parts[0]), int(due_date_parts[1]), int(due_date_parts[2])
        )
        if due_date < completion_date:
            status = "Not Complied"
        self.save_compliance_activity(
            unit_id, compliance_id, "Rejected", status,
            remarks
        )

        columns = ["approve_status", "remarks", "completion_date", "completed_on", "concurred_on"]
        condition = "compliance_history_id = '%d'" % compliance_history_id
        values = [0, remarks, None, None, None]
        self.update(self.tblComplianceHistory, columns, values, condition, client_id)

        # notify_compliance_rejected = threading.Thread(
        #     target=self.notify_compliance_rejected, args=[
        #         self, compliance_history_id, remarks, "Reject Approval"
        #     ]
        # )
        # notify_compliance_rejected.start()
        email.notify_task_rejected(
                self, compliance_history_id, remarks, "Reject Approval"
        )
        return True

    def notify_compliance_rejected(self, db, compliance_history_id, remarks, reject_status):
        try:
            email.notify_task_rejected(
                self, compliance_history_id, remarks, reject_status
            )
        except Exception, e:
            print "Error while sending email : {}".format(e)

    def concur_compliance(self, compliance_history_id, remarks,
        next_due_date, validity_date, client_id):
        columns = ["concurrence_status", "concurred_on", "remarks"]
        condition = "compliance_history_id = '%d'" % compliance_history_id
        values = [1, self.get_date_time(), remarks]
        if validity_date is not None:
            columns.append("validity_date")
            values.append(self.string_to_datetime(validity_date))
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
        status = "Inprogress"
        due_date_parts = str(due_date).split("-")
        due_date = datetime.date(
            int(due_date_parts[0]), int(due_date_parts[1]), int(due_date_parts[2])
        )
        if due_date < completion_date:
            status = "Not Complied"
        self.save_compliance_activity(
            unit_id, compliance_id, "Concurred", status,
            remarks
        )
        # notify_compliance_approved = threading.Thread(
        #     target=self.notify_compliance_approved, args=[
        #         self, compliance_history_id, "Concurred"
        #     ]
        # )
        # notify_compliance_approved.start()
        email.notify_task_approved(
                self, compliance_history_id, "Concurred"
        )
        return True

    def reject_compliance_concurrence(self, compliance_history_id, remarks,
        next_due_date, client_id):
        columns = "unit_id, compliance_id, due_date, completion_date"
        condition = "compliance_history_id = '%d'" % compliance_history_id
        rows = self.get_data(
            self.tblComplianceHistory, columns, condition
        )
        unit_id = rows[0][0]
        compliance_id = rows[0][1]
        due_date = rows[0][2]
        completion_date = rows[0][3]
        status = "Inprogress"
        due_date_parts = str(due_date).split("-")
        due_date = datetime.date(
            int(due_date_parts[0]), int(due_date_parts[1]), int(due_date_parts[2])
        )
        if due_date < completion_date:
            status = "Not Complied"
        self.save_compliance_activity(
            unit_id, compliance_id, "Rejected", status,
            remarks
        )
        columns = ["concurrence_status", "remarks", "completion_date", "completed_on"]
        condition = "compliance_history_id = '%d'" % compliance_history_id
        values = [0,  remarks, None, None]
        self.update(self.tblComplianceHistory, columns, values, condition, client_id)

        # notify_compliance_rejected = threading.Thread(
        #     target=self.notify_compliance_rejected, args=[
        #         self, compliance_history_id, remarks, "Reject Concurrence"
        #     ]
        # )
        # notify_compliance_rejected.start()
        email.notify_task_rejected(
            self, compliance_history_id, remarks, "Reject Concurrence"
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
        query = "SELECT compliance_id, concat(document_name, '-' ,compliance_task) AS compliance_name  \
                FROM tbl_compliances"
        rows = self.select_all(query, client_id)
        columns = ["compliance_id", "compliance_name"]
        result = self.convert_to_dict(rows, columns)
        return self.return_client_compliances(result)

    def return_client_compliances(self, data) :
        results = []
        for d in data :
            results.append(core.ComplianceFilter(
                d["compliance_id"], d["compliance_name"]
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

    def get_serviceproviderwise_compliance_report(
        self, country_id, domain_id, statutory_id, unit_id,
        service_provider_id, client_id, session_user
    ) :

        query = "SELECT service_provider_id, service_provider_name, address, contract_from, contract_to, contact_person, contact_no  \
                FROM tbl_service_providers \
                WHERE service_provider_id like '%s' and is_active = 1" % (service_provider_id)
        rows = self.select_all(query, client_id)

        service_provider_wise_compliances_list = []
        for row in rows:

            service_provider_name = row[1]
            address = row[2]
            contract_from = self.datetime_to_string(row[3])
            contract_to = self.datetime_to_string(row[4])
            contact_person = row[5]
            contact_no = row[6]

            user_ids = self.get_service_provider_user_ids(row[0], client_id)
            if unit_id is None :
                unit_ids = self.get_service_provider_user_unit_ids(user_ids, client_id)
            else:
                unit_ids = unit_id

            q = "SELECT unit_id, unit_code, unit_name, address  \
                FROM tbl_units \
                WHERE country_id = '%d' and unit_id in (%s)" % (country_id, unit_ids)

            unit_rows = self.select_all(q, client_id)

            unit_wise_compliances = {}
            for unit in unit_rows:
                unit_id = unit[0]
                unit_name = "%s - %s " % (unit[1], unit[2])
                unit_address = unit[3]

                query = "SELECT c.compliance_task, c.compliance_description, ac.statutory_dates, ch.validity_date, ch.due_date, \
                        ac.assignee, cf.frequency FROM tbl_client_statutories cs, tbl_client_compliances cc, tbl_compliances c, \
                        tbl_assigned_compliances ac, tbl_compliance_frequency cf, tbl_compliance_history ch where \
                        ch.compliance_id = ac.compliance_id and ch.unit_id = ac.unit_id and ch.next_due_date = ac.due_date and \
                        cs.country_id = %s and cs.domain_id = %s and cs.unit_id like '%s' \
                        and cs.client_statutory_id = cc.client_statutory_id and c.compliance_id = cc.compliance_id \
                        and c.compliance_id = ac.compliance_id and ac.unit_id = cs.unit_id and cf.frequency_id = c.frequency_id and ac.assignee in (%s) and \
                        c.statutory_mapping like '%s' " % (
                        country_id, domain_id,
                        unit_id, user_ids, str(statutory_id+"%")
                    )
                compliance_rows = self.select_all(query)

                compliances_list = []
                for compliance in compliance_rows:
                    statutory_dates = compliance[2]
                    statutory_dates = json.loads(statutory_dates)
                    date_list = []
                    for date in statutory_dates :
                        s_date = core.StatutoryDate(
                            date["statutory_date"],
                            date["statutory_month"],
                            date["trigger_before_days"]
                        )
                        date_list.append(s_date)

                    compliance_name = compliance[0]
                    description = compliance[1]
                    statutory_date = date_list
                    compliance_frequency = core.COMPLIANCE_FREQUENCY(compliance[6])
                    due_date = self.datetime_to_string(compliance[4])

                    validity_date = None
                    if(validity_date is not None):
                        validity_date = self.datetime_to_string(compliance[3])

                    compliances_list.append(clientreport.ComplianceUnit(
                        compliance_name, unit_address,
                        compliance_frequency, description, statutory_date,
                        due_date, validity_date
                    ))
                unit_wise_compliances[unit_name] = compliances_list
            service_provider_wise_compliances_list.append(clientreport.ServiceProviderCompliance(
                service_provider_name, address, contract_from, contract_to, contact_person, contact_no,
                unit_wise_compliances))
        return service_provider_wise_compliances_list

    def get_compliance_details_report(self, country_id, domain_id, statutory_id, unit_id, compliance_id, assignee_id, from_date, to_date, compliance_status, client_id, session_user) :

        if unit_id is None :
            unit_ids = self.get_user_unit_ids(session_user, client_id)
        else :
            unit_ids = unit_id

        if from_date is None :
            query = "SELECT period_from, period_to FROM tbl_client_configurations where country_id = %s AND domain_id = %s " % (country_id, domain_id)
            daterow = self.select_all(query, client_id)

            period_from = daterow[0][0]
            period_to = daterow[0][1]

            current_year = datetime.date.today().year

            if period_from == 1 :
                year_from = current_year
                year_to = current_year
            else :
                current_month = datetime.date.today().month
                if current_month < period_from :
                    year_from = datetime.date.today().year - 1
                    year_to = datetime.date.today().year
                else :
                    year_from = datetime.date.today().year
                    year_to = datetime.date.today().year + 1

            start_date = self.string_to_datetime('01-' + self.string_months[period_from] + '-' + str(year_from))
            day = "30-"
            if period_to == 2:
                day = "29-"
            elif period_to in [1, 3, 5, 7, 8, 10, 12]:
                day = "31-"
            end_date = self.string_to_datetime(
                day + self.string_months[period_to] + '-' + str(year_to))

        else :
            start_date = self.string_to_datetime(from_date)
            end_date = self.string_to_datetime(to_date)

        unit_columns = "unit_id, unit_code, unit_name, address"
        detail_condition = "country_id = '%d' and unit_id in (%s) " % (country_id, unit_ids)
        unit_rows = self.get_data(self.tblUnits, unit_columns, detail_condition)

        unit_wise_compliances = []
        for unit in unit_rows:
            unit_id = unit[0]
            unit_name = "%s - %s " % (unit[1], unit[2])
            unit_address = unit[3]

            query = "SELECT concat(c.document_name,'-',c.compliance_task), c.compliance_description, ch.validity_date, ch.due_date, \
                    (SELECT concat( u.employee_code, '-' ,u.employee_name ) FROM tbl_users u WHERE u.user_id = ch.completed_by) AS assigneename, \
                    ch.documents, ch.completion_date \
                    from tbl_compliances c,tbl_compliance_history ch, \
                    tbl_units ut where \
                    ch.unit_id = %s \
                    AND ut.country_id = %s and ut.domain_ids like '%s' \
                    AND c.compliance_id = ch.compliance_id \
                    AND ch.completed_by like '%s'  AND c.statutory_mapping like '%s'  AND c.compliance_id like '%s' and ch.due_date BETWEEN '%s' AND '%s'" % (
                    unit_id, country_id, domain_id,
                    assignee_id, str(statutory_id+"%"), compliance_id, start_date, end_date
                )
            compliance_rows = self.select_all(query, client_id)

            compliances_list = []
            for compliance in compliance_rows:

                compliance_name = compliance[0]
                assignee = compliance[4]
                due_date = self.datetime_to_string(compliance[3])

                validity_date = None
                if(compliance[2] != None):
                    validity_date = self.datetime_to_string(compliance[2])

                documents = None if compliance[5] == "" else compliance[5]
                remarks = "remarks"
                completion_date = None
                if(compliance[6] != None):
                    completion_date = self.datetime_to_string(compliance[6])

                compliance = clientreport.ComplianceDetails(
                    compliance_name, assignee,
                    due_date, completion_date, validity_date, documents, remarks
                )
                compliances_list.append(compliance)

            unitwise = clientreport.ComplianceDetailsUnitWise(unit_id, unit_name, unit_address, compliances_list)
            unit_wise_compliances.append(unitwise)
        return unit_wise_compliances

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
        result = self.get_client_statutory_ids_and_unit_ids_for_trend_chart(
            country_id, domain_id, client_id, filter_id, filter_type)
        client_statutory_ids = result[0]
        unit_ids = result[1]
        compliance_history_ids = None
        if client_statutory_ids is not None and unit_ids is not None:
            columns = "group_concat(compliance_history_id)"
            condition = "compliance_id in " +\
                        "(select group_concat(compliance_id) from " + \
                        "tbl_client_compliances where client_statutory_id " + \
                        "in (%s) and unit_id in (%s))" % (client_statutory_ids, unit_ids)
            result = self.get_data(
                self.tblComplianceHistory, columns, condition
            )
            compliance_history_ids = result[0][0]
        return compliance_history_ids, client_statutory_ids, unit_ids

    def get_trend_chart(self, country_ids, domain_ids, client_id):
        years = self.get_last_7_years()
        country_domain_timelines = self.get_country_domain_timelines(
            country_ids, domain_ids, years, client_id)
        chart_data = []
        for country_wise_timeline in country_domain_timelines:
            country_id = country_wise_timeline[0]
            domain_wise_timelines = country_wise_timeline[1]
            year_wise_count = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
            for domain_wise_timeline in domain_wise_timelines:
                domain_id = domain_wise_timeline[0]
                start_end_dates = domain_wise_timeline[1]
                for index, dates in enumerate(start_end_dates):
                    columns = "count(*) as total, sum(case when approve_status = 1 then 1 " + \
                        "else 0 end) as complied"
                    condition = "due_date between '{}' and '{}'".format(
                        dates["start_date"], dates["end_date"]
                    )
                    compliance_history_ids = self.get_compliance_history_ids_for_trend_chart(
                        country_id, domain_id, client_id)
                    if compliance_history_ids[0] is not None :
                        condition += " and compliance_history_id in (%s)" % (compliance_history_ids[0])
                    rows = self.get_data(
                            self.tblComplianceHistory,
                            columns, condition
                        )
                    if len(rows) > 0:
                        row = rows[0]
                        total_compliances = row[0]
                        complied_compliances = row[1] if row[1] != None else 0
                        year_wise_count[index][0] += total_compliances if total_compliances is not None else 0
                        year_wise_count[index][1] += complied_compliances if complied_compliances is not None else 0
            compliance_chart_data = []
            for index, count_of_year in enumerate(year_wise_count):
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
        return years, chart_data

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

        unit_ids = [int(x) for x in rows[0][0].split(",")] if rows[0][0] != None else []
        drill_down_data = []
        for unit_id in unit_ids:
            # Getting Unit details
            unit_detail_columns = "tu.country_id, domain_ids, business_group_id, \
            legal_entity_id, division_id, unit_code, unit_name, address, \
            group_concat(tcs.client_statutory_id)"
            unit_detail_condition = "tu.unit_id = '{}'".format(unit_id)
            tables = "%s tu, %s tcs" % (
                self.tblUnits, self.tblClientStatutories
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

            # Getting compliances relevent to unit, country, domain
            compliance_columns = "group_concat(compliance_id)"
            compliance_condition = "compliance_opted = 1"
            if unit_detail[8] != None:
                compliance_condition += " and client_statutory_id in (%s)" % unit_detail[8]
            compliance_rows = self.get_data(
                self.tblClientCompliances, compliance_columns,
                compliance_condition
            )
            compliance_ids = compliance_rows[0][0]

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
                # domain_id = domain_wise_timeline[0]
                start_end_dates = domain_wise_timeline[1][0]
                start_date = start_end_dates["start_date"]
                end_date = start_end_dates["end_date"]
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
                    statutories = history_row[7].split(" >> ")
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
                    business_group_name = rows[0][0]
                if division_id is not None:
                    rows = self.get_data(
                        self.tblDivisions, "division_name", "division_id='%d'" % (division_id)
                    )
                    division_name = rows[0][0]
                rows = self.get_data(
                    self.tblLegalEntities, "legal_entity_name", "legal_entity_id='%d'" % (legal_entity_id)
                )
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
                                year_wise_count[0][0] += total_compliances if total_compliances is not None else 0
                                year_wise_count[0][1] += complied_compliances if complied_compliances is not None else 0
            compliance_chart_data = []
            for index, count_of_year in enumerate(year_wise_count):
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
        return years, chart_data

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
        self, country_ids, domain_ids, years, client_id
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
                    period_to = rows[0][0]
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
        is_admin_is_a_user= False

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
        if not is_admin_is_a_user:
            licence_holders.append(
                clientadminsettings.LICENCE_HOLDER(
                    0, "Administrator", admin_email, None,
                    None, None
                ))
        remaining_licence = (no_of_user_licence) - len(licence_holder_rows)
        profile_detail = clientadminsettings.PROFILE_DETAIL(
            contract_from,
            contract_to,
            no_of_user_licence,
            remaining_licence,
            licence_holders,
            total_disk_space/1000000000,
            total_disk_space_used/1000000000
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

#
#   Notifications
#
    def get_notifications(self, notification_type, session_user, client_id):
        notification_type_id = None
        if notification_type == "Notification":
            notification_type_id = 1
        elif notification_type == "Reminder":
            notification_type_id = 2
        elif notification_type == "Escalation":
            notification_type_id = 3

        notification_rows = self.get_data(
            self.tblNotificationUserLog,
            "notification_id, read_status",
            "user_id = '%d'" % session_user
        )
        notifications = []
        for notification in notification_rows:
            notification_id = notification[0]
            read_status = bool(notification[1])
            # Getting notification details
            columns = "notification_id, notification_text, created_on, extra_details, " + \
                "statutory_provision, unit_code, unit_name, address, assignee, " + \
                "concurrence_person, approval_person, nl.compliance_id, " + \
                " compliance_task, document_name, compliance_description, penal_consequences"
            tables = [self.tblNotificationsLog, self.tblUnits, self.tblCompliances]
            aliases = ["nl", "u", "c"]
            join_conditions = [
                "nl.unit_id = u.unit_id",
                "nl.compliance_id = c.compliance_id"
            ]
            join_type = " left join"
            where_condition = "notification_id = '%d'" % notification_id
            where_condition += " and notification_type_id = '%d' order by created_on DESC limit 30" % notification_type_id
            notification_detail_row = self.get_data_from_multiple_tables(
                columns, tables, aliases, join_type,
                join_conditions, where_condition
            )
            notification_detail = []
            if notification_detail_row:
                notification_detail = notification_detail_row[0]
                extra_details = notification_detail[3].split("-")
                compliance_history_id = int(extra_details[0])

                due_date_rows = self.get_data(
                    self.tblComplianceHistory,
                    "due_date",
                    "compliance_history_id = '%d'" % compliance_history_id
                )
                due_date_as_date = due_date_rows[0][0]
                due_date_as_datetime = datetime.datetime(
                    due_date_as_date.year,
                    due_date_as_date.month,
                    due_date_as_date.day
                )
                due_date = self.datetime_to_string(due_date_as_datetime)

                diff = self.get_date_time() - due_date_as_datetime
                delayed_days = "%d days" % diff.days
                statutory_provision = notification_detail[4].split(">>")
                level_1_statutory = statutory_provision[0]

                notification_id = notification_detail[0]
                notification_text = notification_detail[1]
                extra_details = notification_detail[3]
                updated_on = self.datetime_to_string(notification_detail[2])
                unit_name = "%s - %s" % (
                    notification_detail[5],
                    notification_detail[6]
                )
                unit_address = notification_detail[7]
                assignee = self.get_user_contact_details_by_id(
                    notification_detail[8], client_id
                )
                concurrence_person = self.get_user_contact_details_by_id(
                    notification_detail[9], client_id
                )
                approval_person = self.get_user_contact_details_by_id(
                    notification_detail[10], client_id
                )
                compliance_name = "%s - %s" % (
                    notification_detail[13], notification_detail[12]
                )
                compliance_description = notification_detail[14]
                penal_consequences = notification_detail[15]
                notifications.append(
                    dashboard.Notification(
                        notification_id, read_status, notification_text, extra_details,
                        updated_on, level_1_statutory, unit_name, unit_address, assignee,
                        concurrence_person, approval_person, compliance_name,
                        compliance_description, due_date, delayed_days, penal_consequences
                    )
                )
        return notifications

    def get_user_contact_details_by_id(self, user_id, client_id):
        columns = "employee_code, employee_name, contact_no, email_id"
        condition = "user_id = '%d'" % user_id
        rows = self.get_data(self.tblUsers, columns, condition)
        employee_name_with_contact_details = "%s - %s, (%s, %s)" % (
            rows[0][0],
            rows[0][1],
            rows[0][2],
            rows[0][3]
        )
        return employee_name_with_contact_details

    def update_notification_status(self, notification_id, has_read, session_user, client_id):
        columns = ["read_status"]
        values = [1 if has_read == True else 0]
        condition = "notification_id = '%d' and user_id='%d'" % (
            notification_id, session_user)
        self.update(self.tblNotificationUserLog , columns, values, condition, client_id)

#
# ReAssign Compliance
#

    def get_user_wise_compliance(self, session_user, client_id):
        # upcoming compliance
        result = []
        user_id = session_user
        if session_user == 0 :
            user_id = '%'

        upcoming = "SELECT distinct t1.compliance_id, t1.unit_id, t1.statutory_dates, t1.assignee, \
            t1.due_date, t1.validity_date, t2.compliance_task, t2.document_name, t2.compliance_description, \
            t2.statutory_mapping, t3.unit_name, t3.unit_code, t3.address, t3.postal_code, \
            (select frequency from tbl_compliance_frequency where frequency_id = t2.frequency_id) frequency, t2.frequency_id,\
            (select duration_type from tbl_compliance_duration_type where duration_type_id = t2.duration_type_id) duration_type, t2.duration, \
            (select repeat_type from tbl_compliance_repeat_type where repeat_type_id = t2.repeats_type_id) repeat_type, t2.repeats_every,\
            NULL \
            FROM tbl_assigned_compliances t1 \
            INNER JOIN tbl_compliances t2 on t1.compliance_id = t2.compliance_id AND t1.is_active = 1 \
            INNER JOIN tbl_units t3 on t1.unit_id = t3.unit_id \
            AND t1.compliance_id NOT IN ( \
                SELECT DISTINCT distinct TA.compliance_id \
                FROM tbl_assigned_compliances TA \
                INNER JOIN tbl_compliance_history TC \
                ON TA.compliance_id = TC.compliance_id \
                AND TA.unit_id = TC.unit_id \
                WHERE \
                TA.is_active = 1 \
                AND IFNULL(TC.approve_status, 0) != 1 \
            ) \
            AND t1.unit_id in (select distinct unit_id from tbl_user_units where user_id like '%s') " % (user_id)

        columns = [
            "compliance_id", "unit_id", "statutory_dates",
            "assignee", "due_date", "validity_date",
            "compliance_task", "document_name",
            "compliance_description", "statutory_mapping",
            "unit_name", "unit_code", "address", "postal_code",
            "frequency", "frequency_id", "duration_type", "duration",
            "repeat_type", "repeats_every",
            "compliance_history_id"
        ]
        rows = self.select_all(upcoming)
        result = self.convert_to_dict(rows, columns)

        ongoing = "SELECT distinct t1.compliance_id, t1.unit_id, t1.statutory_dates, t1.assignee, \
            tc.due_date, tc.validity_date, t2.compliance_task, t2.document_name, t2.compliance_description, \
            t2.statutory_mapping, t3.unit_name, t3.unit_code, t3.address, t3.postal_code, \
            (select frequency from tbl_compliance_frequency where frequency_id = t2.frequency_id) frequency, t2.frequency_id,\
            (select duration_type from tbl_compliance_duration_type where duration_type_id = t2.duration_type_id) duration_type, t2.duration, \
            (select repeat_type from tbl_compliance_repeat_type where repeat_type_id = t2.repeats_type_id) repeat_type, t2.repeats_every,\
            tc.compliance_history_id \
            FROM tbl_compliance_history tc\
            INNER JOIN tbl_assigned_compliances t1 on tc.compliance_id = t1.compliance_id \
            INNER JOIN tbl_compliances t2 on t1.compliance_id = t2.compliance_id \
            INNER JOIN tbl_units t3 on t1.unit_id = t3.unit_id \
            WHERE IFNULL(tc.approve_status, 0) != 1 \
            AND t1.unit_id in (select distinct unit_id from tbl_user_units where user_id like '%s') " % (user_id)

        rows = self.select_all(ongoing)
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
            compliance_history_id = d["compliance_history_id"]
            if compliance_history_id is not None :
                compliance_history_id = int(compliance_history_id)
            else :
                compliance_history_id = None
            statutory_dates = json.loads(d["statutory_dates"])
            date_list = []
            for date in statutory_dates :
                s_date = core.StatutoryDate(
                    date["statutory_date"],
                    date["statutory_month"],
                    date["trigger_before_days"]
                )
                date_list.append(s_date)
            compliance_name = "%s - %s" % (
                d["document_name"], d["compliance_task"]
            )
            if d["frequency_id"] in (2, 3) :
                summary = "Repeats ever %s - %s" % (d["repeats_every"], d["repeat_type"])
            elif d["frequency_id"] == 4 :
                summary = "To complete within %s - %s" % (d["duration"], d["duration_type"])
            else :
                summary = None

            compliance = clienttransactions.STATUTORYWISECOMPLIANCE(
                compliance_history_id, d["compliance_id"],
                compliance_name,
                d["compliance_description"], frequency,
                date_list, due_date, validity_date,
                summary
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
        compliance_ids = []
        for c in compliances :
            unit_id = c.unit_id
            compliance_id = c.compliance_id
            compliance_ids.append(compliance_id)
            due_date = c.due_date
            if due_date is not None :
                due_date = datetime.datetime.strptime(due_date, "%d-%b-%Y")
                print due_date

            history_id = c.compliance_history_id

            query = " INSERT INTO tbl_reassigned_compliances_history \
                (unit_id, compliance_id, assignee, \
                reassigned_from, reassigned_date, remarks, \
                created_by, created_on) \
                VALUES (%s, %s, %s, %s, '%s', '%s', %s, '%s') " % (
                    unit_id, compliance_id, assignee,
                    reassigned_from, reassigned_date, reassigned_reason,
                    created_by, created_on
                )
            self.execute(query)

            update_qry = "UPDATE tbl_assigned_compliances SET assignee=%s, is_reassigned=1, approval_person=%s "
            if concurrence is not None :
                update_qry += " ,concurrence_person = %s " % (concurrence)
            where_qry = " WHERE unit_id = %s AND compliance_id = %s "

            qry = update_qry + where_qry

            update_assign = qry % (
                assignee, approval, unit_id, compliance_id
            )

            # update_assign = "UPDATE tbl_assigned_compliances SET assignee=%s, \
            #     is_reassigned=1, concurrence_person=%s, approval_person=%s \
            #     WHERE unit_id = %s AND compliance_id = %s " % (
            #         assignee, concurrence, approval,
            #         unit_id, compliance_id
            #     )
            self.execute(update_assign)

            if history_id is not None :
                update_history = "UPDATE tbl_compliance_history SET due_date='%s', \
                    completed_by = '%s', approved_by = %s"
                if concurrence is not None :
                    update_qry += " ,concurred_by = %s " % (concurrence)
                where_qry = " WHERE compliance_history_id = %s "

                qry = update_history + where_qry

                update_history = qry % (
                    due_date, assignee, approval, history_id
                )
                self.execute(update_history)

        action = "Compliances reassigned %s to assignee %s" % (str(compliance_ids), assignee)
        self.save_activity(session_user, 8, action)
        return clienttransactions.ReassignComplianceSuccess()

#
#   Manage Compliances / Compliances List / Upload Compliances
#
    def calculate_ageing(self, due_date):
        current_time_stamp = self.get_date_time()
        due_date = datetime.datetime(due_date.year, due_date.month, due_date.day)
        ageing = (current_time_stamp - due_date).days
        compliance_status = " %d days left" % abs(ageing)
        if ageing > 0:
            compliance_status = "Overdue by %d days" % abs(ageing)
            return ageing, compliance_status
        return 0, compliance_status


    def get_current_compliances_list(self, session_user, client_id):
        columns = "compliance_history_id, start_date, due_date, " +\
            "validity_date, next_due_date, document_name, compliance_task, " + \
            "compliance_description, format_file, unit_code, unit_name," + \
            "address, (select domain_name from %s d \
            where d.domain_id = c.domain_id) as domain_name, frequency, remarks,\
            ch.compliance_id" % (
                self.tblDomains
            )
        tables = [
            self.tblComplianceHistory, self.tblCompliances, self.tblUnits,
            self.tblComplianceFrequency
        ]
        aliases = ["ch", "c" , "u", "cf"]
        join_conditions = [
            "ch.compliance_id = c.compliance_id",
            "ch.unit_id = u.unit_id", "c.frequency_id = cf.frequency_id"
        ]
        join_type = "inner join"
        where_condition = "ch.completed_by='%d'" % (
            session_user)
        where_condition += " and ((ch.completed_on is null or ch.completed_on = 0) \
        and (ch.approve_status is null or ch.approve_status = 0))"

        current_compliances_row = self.get_data_from_multiple_tables(
            columns,
            tables, aliases, join_type, join_conditions, where_condition
        )
        current_compliances_list = []
        for compliance in current_compliances_row:
            document_name = compliance[5]
            compliance_task = compliance[6]
            compliance_name = "%s - %s" % (
                document_name, compliance_task
            )

            unit_code = compliance[9]
            unit_name = compliance[10]
            unit_name = "%s - %s" % (
                unit_code, unit_name
            )
            no_of_days, ageing = self.calculate_ageing(compliance[2])
            compliance_status = core.COMPLIANCE_STATUS("Inprogress")
            if no_of_days > 0:
                compliance_status = core.COMPLIANCE_STATUS("Not Complied")
            format_files = None
            if compliance[8] is not None and compliance[8].strip() != '':
                format_files = [ "%s/%s" % (
                        FORMAT_DOWNLOAD_URL, x
                    ) for x in compliance[8].split(",")]
            current_compliances_list.append(
                core.ActiveCompliance(
                    compliance_history_id=compliance[0],
                    compliance_name=compliance_name,
                    compliance_frequency=core.COMPLIANCE_FREQUENCY(compliance[13]),
                    domain_name=compliance[12],
                    start_date=self.datetime_to_string(compliance[1]),
                    due_date=self.datetime_to_string(compliance[2]),
                    compliance_status=compliance_status,
                    validity_date=None if compliance[3] == None else self.datetime_to_string(compliance[3]),
                    next_due_date=None if compliance[4] == None else self.datetime_to_string(compliance[4]),
                    ageing=ageing,
                    format_file_name=format_files,
                    unit_name=unit_name, address=compliance[11],
                    compliance_description=compliance[7],
                    remarks=compliance[14],
                    compliance_id=compliance[15]
                )
            )
        return current_compliances_list

    def get_upcoming_compliances_list(self, session_user, client_id):
        columns = "due_date, document_name, compliance_task," + \
            " compliance_description, format_file, unit_code, unit_name," + \
            "  address, ac.statutory_dates, repeats_every, (select domain_name \
            from %s d where d.domain_id = c.domain_id) as domain_name" % (
            self.tblDomains
        )
        tables = [
            self.tblAssignedCompliances, self.tblUnits,  self.tblCompliances
        ]
        aliases = ["ac", "u", "c"]
        join_conditions = [
            "ac.unit_id = u.unit_id",
            "ac.compliance_id = c.compliance_id"
        ]
        join_type = "inner join"
        where_condition = " assignee = '%d'" % session_user
        where_condition += " and due_Date > DATE_SUB(now(), INTERVAL 6 MONTH) and ac.is_active = 1"
        upcoming_compliances_rows = self.get_data_from_multiple_tables(
            columns,
            tables, aliases, join_type, join_conditions,
            where_condition
        )
        upcoming_compliances_list = []
        for compliance in upcoming_compliances_rows:
            document_name = compliance[1]
            compliance_task = compliance[2]
            compliance_name = "%s - %s" % (document_name, compliance_task)

            unit_code = compliance[5]
            unit_name = compliance[6]
            unit_name = "%s - %s" % (unit_code, unit_name)

            start_date = self.calculate_next_start_date(
                compliance[0],
                compliance[8],  compliance[9]
            )
            format_files = None
            if compliance[4] is not None and compliance[4].strip() != '':
                format_files = [ "%s/%s" % (
                        FORMAT_DOWNLOAD_URL, x
                    ) for x in compliance[4].split(",")]
            upcoming_compliances_list.append(
                core.UpcomingCompliance(
                    compliance_name = compliance_name,
                    domain_name = compliance[10],
                    start_date = self.datetime_to_string(start_date),
                    due_date = self.datetime_to_string(compliance[0]),
                    format_file_name = format_files,
                    unit_name = unit_name,
                    address = compliance[7],
                    compliance_description = compliance[3]
                ))
        return upcoming_compliances_list

    def calculate_next_start_date(self, due_date, statutory_dates, repeats_every):
        statutory_dates = json.loads(statutory_dates)
        next_start_date = None
        if len(statutory_dates) > 1:
            month_of_due_date = due_date.month
            for statutory_date in statutory_dates:
                if month_of_due_date >= statutory_date["statutory_month"]:
                    next_start_date = due_date - timedelta(
                        days = statutory_date["trigger_before_days"])
                    break
                else:
                    continue
        else:
            trigger_before = int(statutory_dates[0]["trigger_before_days"])
            next_start_date = due_date - timedelta(days=trigger_before)
        return next_start_date

    def get_statutory_notifications_list_report(self, request_data, client_id):
        country_name = request_data.country_name
        domain_name = request_data.domain_name
        business_group_id = request_data.business_group_id
        legal_entity_id = request_data.legal_entity_id
        division_id = request_data.division_id
        unit_id = request_data.unit_id
        level_1_statutory_name = request_data.level_1_statutory_name
        from_date = request_data.from_date
        to_date = request_data.to_date
        if from_date is None:
            from_date = ''
        else:
            from_date = self.string_to_datetime(from_date)
        if to_date is None:
            to_date = ''
        else:
            to_date = self.string_to_datetime(to_date)
        condition = "1"
        if business_group_id is not None:
            condition += " AND business_group_id = '%d'" % business_group_id
        if legal_entity_id is not None:
            condition += " AND legal_entity_id = '%d'" % legal_entity_id
        if division_id is not None:
            condition += " AND division_id = '%d'" % division_id
        if unit_id is not None:
            condition += " AND unit_id = '%d'" % unit_id

        # Gettings distinct sets of bg_id, le_id, div_id, unit_id
        columns = "business_group_id, legal_entity_id, division_id, unit_id"
        where_condition = "1 AND %s" % condition
        where_condition += " group by business_group_id, legal_entity_id, division_id, unit_id"
        rows = self.get_data(self.tblStatutoryNotificationsUnits, columns, where_condition)
        columns = ["business_group_id", "legal_entity_id", "division_id", "unit_id"]
        rows = self.convert_to_dict(rows, columns)
        notifications = []
        conditiondate = None
        for row in rows:
            business_group_id = row["business_group_id"]
            legal_entity_id = row["legal_entity_id"]
            division_id = row["division_id"]
            unit_id = row["unit_id"]
            query = "SELECT bg.business_group_name, le.legal_entity_name, d.division_name, u.unit_code, u.unit_name, u.address,\
                snl.statutory_provision, snl.notification_text, snl.updated_on \
                from \
                tbl_statutory_notifications_log snl \
                INNER JOIN \
                tbl_statutory_notifications_units snu  ON \
                snl.statutory_notification_id = snu.statutory_notification_id \
                INNER JOIN \
                tbl_business_groups bg ON \
                snu.business_group_id = bg.business_group_id \
                INNER JOIN \
                tbl_legal_entities le ON \
                snu.legal_entity_id = le.legal_entity_id \
                INNER JOIN \
                tbl_divisions d ON \
                snu.division_id = d.division_id \
                INNER JOIN \
                tbl_units u ON \
                snu.unit_id = u.unit_id \
                where \
                snl.country_name = '%s' \
                and \
                snl.domain_name = '%s' \
                and \
                bg.business_group_id = '%d' \
                and \
                le.legal_entity_id = '%d' \
                and \
                d.division_id = '%d' \
                and \
                u.unit_id = '%d' " % (
                    country_name, domain_name, business_group_id, legal_entity_id, division_id, unit_id
                )
            if from_date != '' and to_date != '':
                conditiondate = " AND  snl.updated_on between '%s' and '%s' " % (from_date, to_date)
                query = query + conditiondate
            if level_1_statutory_name is not None:
                conditionlevel1 = "AND statutory_provision like '%s'" % str(level_1_statutory_name + "%")
                query = query + conditionlevel1
            result_rows = self.select_all(query)
            columns = [
                "business_group_name", "legal_entity_name", "division_name", "unit_code", "unit_name", "address",
                "statutory_provision", "notification_text", "updated_on"
            ]
            statutory_notifications = self.convert_to_dict(result_rows, columns)
            level_1_statutory_wise_notifications = {}
            if len(result_rows) > 0:
                business_group_name = result_rows[0][0]
                legal_entity_name = result_rows[0][1]
                division_name = result_rows[0][2]
                for notification in statutory_notifications:
                    unit_name = "%s - %s" % (notification["unit_code"], notification["unit_name"])
                    statutories = notification["statutory_provision"].split(">>")
                    level_1_statutory_name = statutories[0]
                    if level_1_statutory_name not in level_1_statutory_wise_notifications:
                        level_1_statutory_wise_notifications[level_1_statutory_name] = []
                    level_1_statutory_wise_notifications[level_1_statutory_name].append(
                        clientreport.LEVEL_1_STATUTORY_NOTIFICATIONS(
                            statutory_provision=notification["statutory_provision"],
                            unit_name=unit_name,
                            notification_text=notification["notification_text"],
                            date_and_time=self.datetime_to_string(notification["updated_on"])
                        ))
                notifications.append(clientreport.STATUTORY_WISE_NOTIFICATIONS(
                    business_group_name, legal_entity_name, division_name, level_1_statutory_wise_notifications
                        ))
        return notifications

#
#   Risk Report
#
    def get_unasssigned_compliances(
            self, country_id, domain_id, business_group_id,
            legal_entity_id, division_id, unit_id, level_1_statutory_name, statutory_status,
            client_id, session_user
    ):
        columns = "group_concat(unit_id), business_group_id, (select business_group_name from \
            %s b where b.business_group_id = u.business_group_id) as business_group_name, \
            legal_entity_id, (select legal_entity_name from  %s l where l.legal_entity_id = \
            u.legal_entity_id) as legal_entity_name, division_id, (select division_name from \
            %s d where d.division_id = u.division_id) as division_name" % (
                self.tblBusinessGroups, self.tblLegalEntities, self.tblDivisions
            )
        condition = "1 "
        if business_group_id is not None:
            condition += " and u.business_group_id = '%d'" % business_group_id
        if legal_entity_id is not None:
            condition += " and u.legal_entity_id = '%d'" % legal_entity_id
        if division_id is not None:
            condition += " and u.division_id = '%d'" % division_id
        if unit_id is not None:
            condition += " and u.unit_id = '%d'" % unit_id
        condition += " group by business_group_id, legal_entity_id, division_id"
        rows = self.get_data(self.tblUnits+" u", columns, condition)

        level_1_statutories_list = [level_1_statutory_name]
        if level_1_statutory_name is None:
            level_1_statutories_list = self.get_level_1_statutories_for_user(
                session_user, client_id, domain_id
            )
        risk_report_Data = []
        for row in rows:
            unit_ids_list = [int(x) for x in row[0].split(",")]
            business_group_name = row[2]
            legal_entity_name = row[4]
            division_name = row[6]
            level_1_statutory_wise_units = {}
            for level_1_statutory in level_1_statutories_list:
                unit_wise_compliances = []
                for unit_id in unit_ids_list:
                    assigned_compliance_columns = "group_concat(compliance_id)"
                    assigned_compliance_condition = "compliance_id not in (select group_concat(\
                        compliance_id) from %s where unit_id = '%d')  and client_statutory_id in \
                        (select group_concat(client_statutory_id) from %s where unit_id ='%d' )" % (
                        self.tblAssignedCompliances, unit_id, self.tblClientStatutories, unit_id
                    )
                    assigned_compliance_rows = self.get_data(
                        self.tblClientCompliances, assigned_compliance_columns, assigned_compliance_condition
                    )
                    compliances_list = []
                    if assigned_compliance_rows:
                        compliance_ids = assigned_compliance_rows[0][0]
                        if compliance_ids is not None:
                            compliance_columns = "document_name, compliance_task, compliance_description, \
                            penal_consequences, (select frequency from %s f where c.frequency_id = \
                            f.frequency_id) as frequency, c.frequency_id, repeats_type_id, repeats_every, \
                            duration_type_id, duration, statutory_dates, statutory_mapping, \
                            statutory_provision" % (
                                self.tblComplianceFrequency
                            )
                            compliance_condition = "statutory_mapping like '%s%s' and compliance_id \
                            in (%s)" % (level_1_statutory, "%" , compliance_ids)
                            compliance_rows = self.get_data(
                                self.tblCompliances+" c", compliance_columns, compliance_condition
                            )
                            compliance_columns = [
                                "document_name", "compliance_task", "compliance_description",
                                "penal", "frequency", "frequency_id", "repeats_type_id", "repeats_every",
                                "duration_type_id", "duration", "statutory_dates", "statutory_mapping",
                                "statutory_provision"
                            ]
                            compliance_rows = self.convert_to_dict(
                                compliance_rows, compliance_columns
                            )
                            for compliance in compliance_rows:
                                compliance_name = "%s - %s" % (
                                    compliance["document_name"], compliance["compliance_task"]
                                )
                                statutory_mapping = "%s >> %s" % (
                                    compliance["statutory_mapping"], compliance["statutory_provision"]
                                )
                                repeats = None
                                trigger = "Trigger :"
                                if compliance["frequency_id"] != 1 and compliance["frequency_id"] != 4: # checking not onetime and onoccrence
                                    if compliance["repeats_type_id"] == 1: # Days
                                        repeats = "Every %s Day/s" % (compliance["repeats_every"])
                                    elif compliance["repeats_type_id"] == 2: # Month
                                        repeats = "Every %s Month/s" % (compliance["repeats_every"])
                                    elif compliance["repeats_type_id"] == 3: # Year
                                        repeats = "Every %s Year/s" % (compliance["repeats_every"])
                                    if compliance["statutory_dates"] is not None:
                                        statutory_dates = json.loads(compliance["statutory_dates"])
                                        for index, statutory_date in enumerate(statutory_dates):
                                            if index  == 0:
                                                repeats += "%s %s, " % (
                                                    statutory_date["statutory_date"], statutory_date["statutory_month"]
                                                )
                                                trigger += "%s Days" % statutory_date["trigger_before_days"]
                                            else:
                                                trigger += " and %s Days" % statutory_date["trigger_before_days"]
                                    repeats += trigger
                                elif compliance["frequency_id"] == 1:
                                    statutory_dates = json.loads(compliance["statutory_dates"])
                                    statutory_date = statutory_dates[0]
                                    repeats = "%s %s" % (
                                        statutory_date["statutory_date"], statutory_date["statutory_month"]
                                    )
                                    trigger += "%s Days" % statutory_date["trigger_before_days"]
                                    repeats += trigger
                                elif compliance["frequency_id"] == 4:
                                    if compliance["duration_type_id"] == 1: # Days
                                        repeats = "Complete within %s Day/s" % (compliance["duration"])
                                    elif compliance["duration_type_id"] == 2: # Hours
                                        repeats = "Complete within %s Hour/s" % (compliance["duration"])
                                compliances_list.append(
                                    clientreport.Level1Compliance(
                                        statutory_mapping, compliance_name,
                                        compliance["compliance_description"], compliance["penal"],
                                        compliance["frequency"], repeats
                                    )
                                )
                if len(compliances_list) > 0:
                        unit_columns = "unit_code, unit_name, address"
                        unit_condition = "unit_id = '%d'" % unit_id
                        unit_rows = self.get_data(
                            self.tblUnits, unit_columns, unit_condition
                        )
                        unit_name = "%s - %s" % (
                            unit_rows[0][0], unit_rows[0][1]
                        )
                        address = unit_rows[0][2]
                        unit_wise_compliances.append(
                            clientreport.Level1Statutory(
                                unit_name, address, compliances_list
                            )
                        )
                        level_1_statutory_wise_units[level_1_statutory] = unit_wise_compliances
            if len(level_1_statutory_wise_units) > 0:
                risk_report_Data.append(
                    clientreport.RiskData(
                        business_group_name, legal_entity_name, division_name,
                        level_1_statutory_wise_units
                    )
                )
        return risk_report_Data



    def get_not_opted_compliances(
            self, country_id, domain_id, business_group_id,
            legal_entity_id, division_id, unit_id, level_1_statutory_name, statutory_status,
            client_id, session_user
    ):
        columns = "group_concat(unit_id), business_group_id, (select business_group_name from \
            %s b where b.business_group_id = u.business_group_id) as business_group_name, \
            legal_entity_id, (select legal_entity_name from  %s l where l.legal_entity_id = \
            u.legal_entity_id) as legal_entity_name, division_id, (select division_name from \
            %s d where d.division_id = u.division_id) as division_name" % (
                self.tblBusinessGroups, self.tblLegalEntities, self.tblDivisions
            )
        condition = "1 "
        if business_group_id is not None:
            condition += " and u.business_group_id = '%d'" % business_group_id
        if legal_entity_id is not None:
            condition += " and u.legal_entity_id = '%d'" % legal_entity_id
        if division_id is not None:
            condition += " and u.division_id = '%d'" % division_id
        if unit_id is not None:
            condition += " and u.unit_id = '%d'" % unit_id
        condition += " group by business_group_id, legal_entity_id, division_id"
        rows = self.get_data(self.tblUnits+" u", columns, condition)

        level_1_statutories_list = [level_1_statutory_name]
        if level_1_statutory_name is None:
            level_1_statutories_list = self.get_level_1_statutories_for_user(
                session_user, client_id, domain_id
            )
        risk_report_Data = []
        for row in rows:
            unit_ids_list = [int(x) for x in row[0].split(",")]
            business_group_name = row[2]
            legal_entity_name = row[4]
            division_name = row[6]
            level_1_statutory_wise_units = {}
            for level_1_statutory in level_1_statutories_list:
                unit_wise_compliances = []
                for unit_id in unit_ids_list:
                    assigned_compliance_columns = "group_concat(compliance_id)"
                    assigned_compliance_condition = "client_statutory_id in ( select group_concat( \
                    client_statutory_id) from %s where unit_id = '%d') and (compliance_opted = 0 or \
                     compliance_opted is null)" % (
                        self.tblClientStatutories, unit_id
                    )
                    assigned_compliance_rows = self.get_data(
                        self.tblClientCompliances, assigned_compliance_columns, assigned_compliance_condition
                    )
                    compliances_list = []
                    if assigned_compliance_rows:
                        compliance_ids = assigned_compliance_rows[0][0]
                        if compliance_ids is not None:
                            compliance_columns = "document_name, compliance_task, compliance_description, \
                            penal_consequences, (select frequency from %s f where c.frequency_id = \
                            f.frequency_id) as frequency, c.frequency_id, repeats_type_id, repeats_every, \
                            duration_type_id, duration, statutory_dates, statutory_mapping, \
                            statutory_provision" % (
                                self.tblComplianceFrequency
                            )
                            compliance_condition = "statutory_mapping like '%s%s' and compliance_id \
                            in (%s)" % (level_1_statutory, "%" , compliance_ids)
                            compliance_rows = self.get_data(
                                self.tblCompliances+" c", compliance_columns, compliance_condition
                            )
                            compliance_columns = [
                                "document_name", "compliance_task", "compliance_description",
                                "penal", "frequency", "frequency_id", "repeats_type_id", "repeats_every",
                                "duration_type_id", "duration", "statutory_dates", "statutory_mapping",
                                "statutory_provision"
                            ]
                            compliance_rows = self.convert_to_dict(
                                compliance_rows, compliance_columns
                            )
                            for compliance in compliance_rows:
                                compliance_name = "%s - %s" % (
                                    compliance["document_name"], compliance["compliance_task"]
                                )
                                statutory_mapping = "%s >> %s" % (
                                    compliance["statutory_mapping"], compliance["statutory_provision"]
                                )
                                repeats = None
                                trigger = "Trigger :"
                                if compliance["frequency_id"] != 1 and compliance["frequency_id"] != 4: # checking not onetime and onoccrence
                                    if compliance["repeats_type_id"] == 1: # Days
                                        repeats = "Every %s Day/s" % (compliance["repeats_every"])
                                    elif compliance["repeats_type_id"] == 2: # Month
                                        repeats = "Every %s Month/s" % (compliance["repeats_every"])
                                    elif compliance["repeats_type_id"] == 3: # Year
                                        repeats = "Every %s Year/s" % (compliance["repeats_every"])
                                    if compliance["statutory_dates"] is not None:
                                        statutory_dates = json.loads(compliance["statutory_dates"])
                                        for index, statutory_date in enumerate(statutory_dates):
                                            if index  == 0:
                                                repeats += "%s %s, " % (
                                                    statutory_date["statutory_date"], statutory_date["statutory_month"]
                                                )
                                                trigger += "%s Days" % statutory_date["trigger_before_days"]
                                            else:
                                                trigger += " and %s Days" % statutory_date["trigger_before_days"]
                                    repeats += trigger
                                elif compliance["frequency_id"] == 1:
                                    statutory_dates = json.loads(compliance["statutory_dates"])
                                    statutory_date = statutory_dates[0]
                                    repeats = "%s %s" % (
                                        statutory_date["statutory_date"], statutory_date["statutory_month"]
                                    )
                                    trigger += "%s Days" % statutory_date["trigger_before_days"]
                                    repeats += trigger
                                elif compliance["frequency_id"] == 4:
                                    if compliance["duration_type_id"] == 1: # Days
                                        repeats = "Complete within %s Day/s" % (compliance["duration"])
                                    elif compliance["duration_type_id"] == 2: # Hours
                                        repeats = "Complete %s Hour/s" % (compliance["duration"])
                                compliances_list.append(
                                    clientreport.Level1Compliance(
                                        statutory_mapping, compliance_name,
                                        compliance["compliance_description"], compliance["penal"],
                                        compliance["frequency"], repeats
                                    )
                                )
                if len(compliances_list) > 0:
                        unit_columns = "unit_code, unit_name, address"
                        unit_condition = "unit_id = '%d'" % unit_id
                        unit_rows = self.get_data(
                            self.tblUnits, unit_columns, unit_condition
                        )
                        unit_name = "%s - %s" % (
                            unit_rows[0][0], unit_rows[0][1]
                        )
                        address = unit_rows[0][2]
                        unit_wise_compliances.append(
                            clientreport.Level1Statutory(
                                unit_name, address, compliances_list
                            )
                        )
                        level_1_statutory_wise_units[level_1_statutory] = unit_wise_compliances
            if len(level_1_statutory_wise_units) > 0:
                risk_report_Data.append(
                    clientreport.RiskData(
                        business_group_name, legal_entity_name, division_name,
                        level_1_statutory_wise_units
                    )
                )
        return risk_report_Data


    def get_risk_report(
        self, country_id, domain_id, business_group_id, legal_entity_id, division_id, unit_id,
        level_1_statutory_name, statutory_status, client_id, session_user
    ) :
        columns = "group_concat(unit_id), business_group_id, (select business_group_name from \
            %s b where b.business_group_id = u.business_group_id) as business_group_name, \
            legal_entity_id, (select legal_entity_name from  %s l where l.legal_entity_id = \
            u.legal_entity_id) as legal_entity_name, division_id, (select division_name from \
            %s d where d.division_id = u.division_id) as division_name" % (
                self.tblBusinessGroups, self.tblLegalEntities, self.tblDivisions
            )
        condition = "1 "
        if business_group_id is not None:
            condition += " and u.business_group_id = '%d'" % business_group_id
        if legal_entity_id is not None:
            condition += " and u.legal_entity_id = '%d'" % legal_entity_id
        if division_id is not None:
            condition += " and u.division_id = '%d'" % division_id
        if unit_id is not None:
            condition += " and u.unit_id = '%d'" % unit_id
        condition += " group by business_group_id, legal_entity_id, division_id"
        rows = self.get_data(self.tblUnits+" u", columns, condition)

        level_1_statutories_list = [level_1_statutory_name]
        if level_1_statutory_name is None:
            level_1_statutories_list = self.get_level_1_statutories_for_user(
                session_user, client_id, domain_id
            )
        risk_report_Data = []
        for row in rows:
            unit_ids_list = [int(x) for x in row[0].split(",")]
            business_group_name = row[2]
            legal_entity_name = row[4]
            division_name = row[6]
            level_1_statutory_wise_units = {}
            for level_1_statutory in level_1_statutories_list:
                unit_wise_compliances = []
                for unit_id in unit_ids_list:
                    compliance_history_columns = "compliance_id, (select statutory_mapping from \
                     %s c where ch.compliance_id = c.compliance_id and statutory_mapping like '%s%s') \
                    as statu" % (self.tblCompliances, level_1_statutory, "%")
                    compliance_history_condition = "unit_id = '%d'" % (
                        unit_id
                    )
                    if statutory_status == 1:
                        compliance_history_condition += " and completed_on > due_date and \
                        approve_status = 1"
                    elif statutory_status == 2:
                        compliance_history_condition += " and (approve_status = 0 or \
                        approve_status is null) and due_date < now()"
                    compliance_history_rows = self.get_data(
                        self.tblComplianceHistory+" ch", compliance_history_columns, compliance_history_condition
                    )
                    compliances_list = []
                    if len(compliance_history_rows) > 0:
                        compliance_ids = compliance_history_rows[0][0]
                        statutory_mapping = compliance_history_rows[0][1]
                        if compliance_ids is not None and statutory_mapping is not None:
                            compliance_columns = "document_name, compliance_task, compliance_description, \
                            penal_consequences, (select frequency from %s f where c.frequency_id = \
                            f.frequency_id) as frequency, c.frequency_id, repeats_type_id, repeats_every, \
                            duration_type_id, duration, statutory_dates, statutory_mapping, \
                            statutory_provision" % (
                                self.tblComplianceFrequency
                            )
                            compliance_condition = "statutory_mapping like '%s%s' and compliance_id \
                            in (%s)" % (level_1_statutory, "%" , compliance_ids)
                            compliance_rows = self.get_data(
                                self.tblCompliances+" c", compliance_columns, compliance_condition
                            )
                            compliance_columns = [
                                "document_name", "compliance_task", "compliance_description",
                                "penal", "frequency", "frequency_id", "repeats_type_id", "repeats_every",
                                "duration_type_id", "duration", "statutory_dates", "statutory_mapping",
                                "statutory_provision"
                            ]
                            compliance_rows = self.convert_to_dict(
                                compliance_rows, compliance_columns
                            )
                            for compliance in compliance_rows:
                                compliance_name = "%s - %s" % (
                                    compliance["document_name"], compliance["compliance_task"]
                                )
                                statutory_mapping = "%s >> %s" % (
                                    compliance["statutory_mapping"], compliance["statutory_provision"]
                                )
                                repeats = None
                                trigger = "Trigger :"
                                if compliance["frequency_id"] != 1 and compliance["frequency_id"] != 4: # checking not onetime and onoccrence
                                    if compliance["repeats_type_id"] == 1: # Days
                                        repeats = "Every %s Day/s" % (compliance["repeats_every"])
                                    elif compliance["repeats_type_id"] == 2: # Month
                                        repeats = "Every %s Month/s" % (compliance["repeats_every"])
                                    elif compliance["repeats_type_id"] == 3: # Year
                                        repeats = "Every %s Year/s" % (compliance["repeats_every"])
                                    if compliance["statutory_dates"] is not None:
                                        statutory_dates = json.loads(compliance["statutory_dates"])
                                        for index, statutory_date in enumerate(statutory_dates):
                                            if index  == 0:
                                                repeats += "%s %s, " % (
                                                    statutory_date["statutory_date"], statutory_date["statutory_month"]
                                                )
                                                trigger += "%s Days" % statutory_date["trigger_before_days"]
                                            else:
                                                trigger += " and %s Days" % statutory_date["trigger_before_days"]
                                    repeats += trigger
                                elif compliance["frequency_id"] == 1:
                                    statutory_dates = json.loads(compliance["statutory_dates"])
                                    statutory_date = statutory_dates[0]
                                    repeats = "%s %s" % (
                                        statutory_date["statutory_date"], statutory_date["statutory_month"]
                                    )
                                    trigger += "%s Days" % statutory_date["trigger_before_days"]
                                    repeats += trigger
                                elif compliance["frequency_id"] == 4:
                                    if compliance["duration_type_id"] == 1: # Days
                                        repeats = "Complete within %s Day/s" % (compliance["duration"])
                                    elif compliance["duration_type_id"] == 2: # Hours
                                        repeats = "Complete %s Hour/s" % (compliance["duration"])
                                compliances_list.append(
                                    clientreport.Level1Compliance(
                                        statutory_mapping, compliance_name,
                                        compliance["compliance_description"], compliance["penal"],
                                        compliance["frequency"], repeats
                                    )
                                )
                    if len(compliances_list) > 0:
                        unit_columns = "unit_code, unit_name, address"
                        unit_condition = "unit_id = '%d'" % unit_id
                        unit_rows = self.get_data(
                            self.tblUnits, unit_columns, unit_condition
                        )
                        unit_name = "%s - %s" % (
                            unit_rows[0][0], unit_rows[0][1]
                        )
                        address = unit_rows[0][2]
                        unit_wise_compliances.append(
                            clientreport.Level1Statutory(
                                unit_name, address, compliances_list
                            )
                        )
                        level_1_statutory_wise_units[level_1_statutory] = unit_wise_compliances
            if len(level_1_statutory_wise_units) > 0:
                risk_report_Data.append(
                    clientreport.RiskData(
                        business_group_name, legal_entity_name, division_name,
                        level_1_statutory_wise_units
                    )
                )
        return risk_report_Data

    def update_compliances(
        self, compliance_history_id, documents, completion_date,
        validity_date, next_due_date, remarks, client_id, session_user
    ):
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

        current_time_stamp = self.get_date_time()
        history_columns = [
            "completion_date", "documents", "validity_date",
            "next_due_date", "remarks", "completed_on"
        ]
        if validity_date is not None:
            validity_date = self.string_to_datetime(validity_date)
        if next_due_date is not None:
            next_due_date = self.string_to_datetime(next_due_date)
        history_values = [
            self.string_to_datetime(completion_date),
            ",".join(document_names),
            validity_date,
            next_due_date,
            remarks,
            current_time_stamp
        ]
        history_condition = "compliance_history_id = '%d' \
            and completed_by ='%d'" % (
                compliance_history_id, session_user
            )
        email.notify_task_completed(
            self, compliance_history_id
        )
        columns = "unit_id, compliance_id"
        condition = "compliance_history_id = '%d'" % compliance_history_id
        rows = self.get_data(
            self.tblComplianceHistory, columns, condition
        )
        unit_id = rows[0][0]
        compliance_id = rows[0][1]
        self.save_compliance_activity(
            unit_id, compliance_id, "Submited", "Inprogress",
            remarks
        )
        return self.update(
            self.tblComplianceHistory,
            history_columns, history_values,
            history_condition
        )

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

    # Reassigned History Report
    def get_reassigned_history_report(
        self, country_id, domain_id, level_1_statutory_name,
        unit_id, compliance_id, user_id, from_date, to_date, client_id, session_user
    ) :
        level_1_statutories_list = self.get_level_1_statutories_for_user(
            session_user, client_id, domain_id
        )
        if level_1_statutory_name is not None:
            level_1_statutories_list = [level_1_statutory_name]

        unit_ids = self.get_user_unit_ids(session_user, client_id)
        unit_ids_list = [int(x) for x in unit_ids.split(",")]
        if unit_id is not None:
            unit_ids_list = [unit_id]

        level_1_statutory_wise_compliance = []
        for level_1_statutory in level_1_statutories_list:
            unit_wise_compliances = []
            for unit_id in unit_ids_list:
                columns = "compliance_id, document_name, compliance_task, compliance_description, "\
                "statutory_mapping"
                condition = "select compliance_id from %s where \
                    unit_id = '%d' group by compliance_id" % (
                        self.tblReassignedCompliancesHistory, unit_id
                    )
                if compliance_id is not None:
                    condition = compliance_id
                whereCondition = " compliance_id in (%s) and statutory_mapping like '%s%s'" % (
                        condition, level_1_statutory, "%"
                )

                compliance_rows = self.get_data(
                    self.tblCompliances, columns, whereCondition
                )

                compliance_wise_history = []
                if len(compliance_rows) > 0:
                    compliance_columns = [
                        "compliance_id", "document_name", "compliance_task", "compliance_description",
                        "tc.statutory_mapping"
                    ]
                    compliance_rows = self.convert_to_dict(
                        compliance_rows, compliance_columns
                    )

                    for compliance in compliance_rows:
                        compliance_name = "%s - %s" % (
                            compliance["document_name"], compliance["compliance_task"]
                        )
                        reassign_columns = "assignee, reassigned_from, reassigned_date, remarks"
                        condition = "1"
                        if user_id is not None:
                            condition = "reassigned_from = '%d' or assignee = '%d'" % (
                                user_id, user_id
                            )
                        if from_date is not None and to_date is not None:
                            condition += " and reassigned_date between '{}' and '{}'".format(
                                from_date, to_date
                            )
                        elif from_date is None and to_date is None:
                            current_year = self.get_date_time().year
                            result = self.get_country_domain_timelines(
                                [country_id], [domain_id], [current_year], client_id
                            )
                            calculated_from_date = result[0][1][0][1][0]["start_date"]
                            calculated_to_date = result[0][1][0][1][0]["end_date"]
                            condition += " and reassigned_date between '{}' and '{}'".format(
                                calculated_from_date, calculated_to_date
                            )
                        else:
                            if from_date is not None:
                                condition += " and reassigned_date > '{}'".format(from_date)
                            elif to_date is not None:
                                condition += " and reassigned_date < '{}'".format(to_date)

                        reassign_condition = "compliance_id = '%d' and unit_id = '%d' \
                        and %s" % (
                            compliance["compliance_id"], unit_id, condition
                        )
                        reassign_rows = self.get_data(
                            self.tblReassignedCompliancesHistory, reassign_columns, reassign_condition
                        )
                        history_list = []
                        if reassign_rows:
                            for history in reassign_rows:
                                reassigned_from = self.get_user_name_by_id(history[1], client_id)
                                reassigned_to = self.get_user_name_by_id(history[0], client_id)
                                history_list.append(
                                    clientreport.ReassignHistory(
                                        reassigned_to, reassigned_from,
                                        self.datetime_to_string(history[2]),
                                        history[3]
                                    )
                                )
                        current_due_date_column = "due_date"
                        current_due_date_condition = " next_due_date = (select due_date from %s where \
                            compliance_id = '%d' and unit_id = '%d')" % (
                            self.tblAssignedCompliances, compliance["compliance_id"], unit_id
                        )
                        current_due_date_rows = self.get_data(
                            self.tblComplianceHistory, current_due_date_column, current_due_date_condition
                        )
                        current_due_date = self.datetime_to_string(current_due_date_rows[0][0])
                        if len(history_list) > 0:
                            compliance_wise_history.append(
                                clientreport.ReassignCompliance(
                                    compliance_name, current_due_date, history_list
                                )
                            )
                if len(compliance_wise_history) > 0:
                    unit_column = "unit_code, unit_name, address"
                    condition = "unit_id = '%d'" % unit_id
                    unit_rows = self.get_data(
                        self.tblUnits, unit_column, condition
                    )
                    unit_name = "%s - %s" % (
                        unit_rows[0][0], unit_rows[0][1]
                    )
                    unit_wise_compliances.append(
                        clientreport.ReassignUnitCompliance(
                            unit_name, unit_rows[0][2], compliance_wise_history
                        )
                    )
            if len(unit_wise_compliances) > 0:
                level_1_statutory_wise_compliance.append(
                    clientreport.StatutoryReassignCompliance(
                        level_1_statutory, unit_wise_compliances
                    )
                )
        return level_1_statutory_wise_compliance

    #login trace
    def get_login_trace(self, client_id, session_user ):
        query = "SELECT al.created_on, f.form_name, al.action \
                FROM tbl_activity_log al \
                INNER JOIN \
                tbl_users u ON \
                al.user_id  = u.user_id \
                INNER JOIN \
                tbl_forms f ON \
                al.form_id = f.form_id \
                WHERE \
                al.form_id in (26, 27)"

        rows = self.select_all(query)
        columns = ["created_on", "form_name", "action"]
        result = self.convert_to_dict(rows, columns)
        return self.return_logintrace(result)

    def return_logintrace(self, data) :
        results = []
        for d in data :
            created_on = self.datetime_to_string_time(d["created_on"])
            results.append(clientreport.LoginTrace(
                 created_on, d["form_name"], d["action"]
            ))
        return results

#
#   Compliance Activity Report
#
    def get_compliance_activity_report(
        self, country_id, domain_id, user_type, user_id, unit_id, compliance_id,
        level_1_statutory_name, from_date, to_date, session_user, client_id
    ):
        unit_ids = unit_id
        unit_ids_list = []
        # user_unit_columns = "group_concat(unit_id)"
        # user_unit_condition = "user_id = '%d'" % session_user
        # rows = self.get_data(self.tblUserUnits, user_unit_columns, user_unit_condition)
        # if rows:
        unit_ids = self.get_user_unit_ids(session_user)
        session_unit_ids = [int(x) for x in unit_ids.split(",")]
        if user_id is not None:
            user_unit_condition = "user_id = '%d'" % user_id
            user_unit_columns = "group_concat(unit_id)"
            rows = self.get_data(self.tblUserUnits, user_unit_columns, user_unit_condition)
            if rows:
                user_unit_ids = rows[0][0]
            user_unit_ids = [int(x) for x in user_unit_ids.split(",")]
            unit_ids_list = list(set(user_unit_ids).intersection(session_unit_ids))
        else:
            unit_ids_list = session_unit_ids
        level_1_statutories_list = []
        if level_1_statutory_name is not None:
            level_1_statutories_list = [level_1_statutory_name]
        else:
            level_1_statutories_list = self.get_level_1_statutories_for_user(
                session_user, client_id, domain_id
            )
        unit_wise_compliances = []
        for unit_id in unit_ids_list:
            unit_columns = "unit_name, unit_code, address"
            unit_condition = "unit_id = '%d'" % unit_id
            unit_rows = self.get_data(
                self.tblUnits, unit_columns, unit_condition
            )
            unit_name = "%s-%s" % (unit_rows[0][1], unit_rows[0][0])
            address = unit_rows[0][2]
            compliance_ids_list = []
            if compliance_id is not None:
                compliance_ids_list = [compliance_id]
            else:
                client_statutory_columns = "group_concat(client_statutory_id)"
                client_statutory_conditions = "country_id = '%d' and domain_id = '%d' and unit_id='%d'" % (
                    country_id, domain_id, unit_id
                )
                client_statutory_rows = self.get_data(
                    self.tblClientStatutories, client_statutory_columns, client_statutory_conditions
                )
                if client_statutory_rows:
                    client_statutory_ids = client_statutory_rows[0][0]
                    client_compliance_columns = "group_concat(compliance_id)"
                    client_compliance_conditions = "client_statutory_id in (%s)" % client_statutory_ids
                    client_compliance_rows = self.get_data(
                        self.tblClientCompliances, client_compliance_columns, client_compliance_conditions
                    )
                    if client_compliance_rows:
                        compliance_ids = client_compliance_rows[0][0]
                        compliance_ids_list = compliance_ids.split(",")
            level_1_statutory_wise_activities = {}
            for level_1_statutory in level_1_statutories_list:
                compliance_wise_activities = {}
                for compliance_id in compliance_ids_list:
                    compliance_columns = "statutory_mapping, document_name, compliance_task, compliance_description"
                    compliance_condition = "statutory_mapping like '%s%s' and compliance_id = '%d'" % (
                        level_1_statutory, "%", int(compliance_id))
                    compliance_rows = self.get_data(
                        self.tblCompliances, compliance_columns, compliance_condition
                    )
                    if compliance_rows:
                        compliance_name = "%s - %s" % (compliance_rows[0][1], compliance_rows[0][2])

                        compliance_activity_columns = "activity_date, activity_status, compliance_status," \
                        "remarks"
                        compliance_activity_condition = "compliance_id = '%d' and unit_id = '%d'" % (
                            int(compliance_id), int(unit_id)
                        )
                        if from_date is not None and to_date is not None:
                            from_date_in_datetime = self.string_to_datetime(from_date)
                            to_date_in_datetime = self.string_to_datetime(to_date)
                            compliance_activity_condition += " and activity_date between '{}' and '{}'".format(
                                from_date_in_datetime, to_date_in_datetime
                            )
                        else:
                            if from_date is not None:
                                from_date_in_datetime = self.string_to_datetime(from_date)
                                compliance_activity_condition += " and activity_date > '{}' ".format(
                                    from_date_in_datetime
                                )
                            if to_date is not None:
                                to_date_in_datetime = self.string_to_datetime(to_date)
                                compliance_activity_condition += " and activity_date < '{}' ".format(
                                    to_date_in_datetime
                                )
                        compliance_activity_rows = self.get_data(
                            self.tblComplianceActivityLog, compliance_activity_columns, compliance_activity_condition
                        )
                        if compliance_activity_rows:
                            columns = ["activity_date", "activity_status", "compliance_status", "remarks"]
                            compliance_activity_rows = self.convert_to_dict(compliance_activity_rows, columns)
                            activity_data = []
                            for compliance_activity in compliance_activity_rows:
                                activity_data.append(
                                    clientreport.ActivityData(
                                        activity_date=self.datetime_to_string(compliance_activity["activity_date"]),
                                        activity_status=core.COMPLIANCE_ACTIVITY_STATUS(compliance_activity["activity_status"]),
                                        compliance_status=core.COMPLIANCE_STATUS(compliance_activity["compliance_status"]),
                                        remarks=compliance_activity["remarks"]
                                    )
                                )
                            if compliance_name not in compliance_wise_activities:
                                compliance_wise_activities[compliance_name] = []
                            activity_data.reverse()
                            compliance_wise_activities[compliance_name] += activity_data

                if compliance_wise_activities:
                    if level_1_statutory not in level_1_statutory_wise_activities:
                        level_1_statutory_wise_activities[level_1_statutory] = {}
                    level_1_statutory_wise_activities[level_1_statutory] = compliance_wise_activities
            if len(level_1_statutory_wise_activities) > 0:
                unit_wise_compliances.append(
                    clientreport.Activities(
                        unit_name=unit_name,
                        address=address,
                        statutory_wise_compliances=level_1_statutory_wise_activities
                    )
                )
        return unit_wise_compliances

#
#   Assigee wise compliance chart
#
    def get_assigneewise_compliances_list(
        self, country_id, business_group_id, legal_entity_id, division_id, unit_id,
        session_user, client_id, assignee_id
    ):
        unit_ids = None
        if unit_id is not None:
            unit_ids = unit_id
        else:
            user_unit_ids = self.get_user_unit_ids(session_user, client_id)
            if session_user > 0:
                seating_unit_column = "seating_unit_id"
                seating_unit_condition = "user_id = '%d'" % session_user
                seating_unit_rows = self.get_data(
                    self.tblUsers, seating_unit_column, seating_unit_condition
                )
                unit_ids = "%s,%s" % (user_unit_ids, seating_unit_rows[0][0])
            unit_ids = user_unit_ids

        unit_columns = "unit_id, unit_code, unit_name, address"
        unit_condition = " unit_id in (%s) AND country_id = %d" % (
            unit_ids, country_id
        )

        if business_group_id is not None:
            unit_condition += " AND business_group_id = '%d' " % (business_group_id)
        if legal_entity_id is not None:
            unit_condition += " AND legal_entity_id = '%d' " % (legal_entity_id)
        if division_id is not None:
            unit_condition += " AND division_id = '%d' " % (division_id)

        unit_list = self.get_data(
            self.tblUnits, unit_columns, unit_condition
        )
        chart_data = []
        for unit in unit_list:
            unit_id = unit[0]
            unit_name = "%s - %s" % (
                unit[1], unit[2]
            )
            address = unit[3]
            user_ids = None
            if assignee_id is not None:
                user_ids = str(assignee_id)
            else:
                user_ids = self.get_unit_user_ids(unit_id)

            assignee_wise_compliances_count = []
            for user_id in user_ids.split(","):
                assigned_compliance_ids, reassigned_compliance_ids = self.get_user_assigned_reassigned_ids(
                    user_id
                )
                all_compliance_ids = None
                if assigned_compliance_ids is not None:
                    all_compliance_ids = "%s" % (
                        assigned_compliance_ids
                    )
                if reassigned_compliance_ids is not None:
                    if all_compliance_ids is not None:
                        all_compliance_ids = "%s, %s" % (
                            all_compliance_ids, reassigned_compliance_ids
                        )
                    all_compliance_ids = "%s" % (
                        reassigned_compliance_ids
                    )
                if all_compliance_ids is not None:
                    client_statutory_id_columns = "group_concat(client_statutory_id)"
                    client_statutory_id_condition = "compliance_id in (%s)" % all_compliance_ids
                    client_statutory_id_rows = self.get_data(
                        self.tblClientCompliances,
                        client_statutory_id_columns,
                        client_statutory_id_condition
                    )

                    domain_columns = "group_concat(client_statutory_id), domain_id, \
                    (select domain_name from %s d where d.domain_id = cs.domain_id)" % self.tblDomains
                    domain_condition = "unit_id = '%d'" % unit_id
                    domain_condition += " and client_statutory_id in (%s)" % (
                        client_statutory_id_rows[0][0]
                    )
                    domain_rows = self.get_data(
                        self.tblClientStatutories+" cs", domain_columns, domain_condition
                    )
                    domain_wise_compliance_count = []
                    for domain in domain_rows:
                        unit_users_column = "user_id, "
                        domain_id = domain[1]
                        domain_name = domain[2]
                        client_statutory_ids = domain[0]
                        complied = inprogress = not_complied = delayed_compliance = total = 0
                        if client_statutory_ids is not None:
                            client_compliance_columns = "group_concat(compliance_id)"
                            client_compliance_condition = "client_statutory_id in (%s)" % client_statutory_ids
                            client_compliance_rows = self.get_data(
                                self.tblClientCompliances, client_compliance_columns, client_compliance_condition
                            )
                            current_year = self.get_date_time().year
                            result = self.get_country_domain_timelines(
                                [country_id], [domain_id], [current_year], client_id
                            )
                            from_date = result[0][1][0][1][0]["start_date"]
                            to_date = result[0][1][0][1][0]["end_date"]
                            compliance_ids = client_compliance_rows[0][0]
                            columns = "sum(case when (approve_status = 1 and (due_date < completion_date or \
                            due_date = completion_date)) then 1 else 0 end) as complied, \
                            sum(case when ((approve_status = 0 or approve_status is null) and \
                            due_date > now()) then 1 else 0 end) as Inprogress, \
                            sum(case when ((approve_status = 0 or approve_status is null) and \
                            due_date < now()) then 1 else 0 end) as NotComplied, \
                            sum(case when (approve_status = 1 and completion_date > due_date) then 1 else 0 end)\
                            as DelayedCompliance"
                            condition = "compliance_id in (%s) and due_date \
                            between '%s' and '%s'" % (
                                compliance_ids, from_date, to_date
                            )
                            rows = self.get_data(
                                self.tblComplianceHistory, columns, condition
                            )
                            complied = int(rows[0][0])
                            inprogress = int(rows[0][1])
                            not_complied = int(rows[0][2])
                            delayed_compliance = int(rows[0][3])
                            total = complied + inprogress + not_complied + delayed_compliance
                        reassigned_compliances = []
                        delayed_reassigned_count = 0
                        if reassigned_compliance_ids is not None:
                            delayed_reassigned_columns = "compliance_id, start_date, due_date, completed_on, \
                            (select concat(document_name,'-',compliance_task) from %s c where \
                            ch.compliance_id = c.compliance_id)" % self.tblCompliances
                            delayed_reassigned_condition = " compliance_id in ({}) and completed_by = '{}'".format(
                                reassigned_compliance_ids, user_id
                            )
                            delayed_reassigned_condition += " and completed_on > due_date and approve_status = 1"
                            delayed_rows = self.get_data(
                                self.tblComplianceHistory+" ch", delayed_reassigned_columns,
                                delayed_reassigned_condition
                            )
                            delayed_reassigned_count = len(delayed_rows)
                            for delayed in delayed_rows:
                                start_date = delayed[1]
                                due_date = delayed[2]
                                completed_on = delayed[3]
                                compliance_name = delayed[4]
                                rh_columns = "reassigned_date, reassigned_from, (select concat(\
                                employee_code, '-', employee_name) from %s u where u.user_id = rh.reassigned_from\
                                )" % self.tblUsers
                                rh_condition = "compliance_id = '%d' and assignee = '%d'" % (
                                    delayed[0], user_id
                                )
                                rh_rows = self.get_data(
                                    self.tblReassignedCompliancesHistory+" rh", rh_columns, rh_condition
                                )
                                reassigned_compliances.append(
                                    dashboard.RessignedCompliance(
                                        compliance_name=compliance_name,
                                        reassigned_from=rh_rows[0][1],
                                        start_date=start_date,
                                        due_date=due_date,
                                        reassigned_date=rh_rows[0][0],
                                        completed_date=completed_on
                                    )
                                )
                        delayed_compliances_obj = dashboard.DelayedCompliance(
                            assigned_count=delayed_compliance - delayed_reassigned_count,
                            reassigned_count=delayed_reassigned_count,
                            reassigned_compliances=None if len(reassigned_compliances) == 0 else  reassigned_compliances
                        )
                        domain_wise_compliance_count.append(
                            dashboard.DomainWise(
                                domain_id=domain_id,
                                domain_name=domain_name,
                                total_compliances=total,
                                complied_count=complied,
                                delayed_compliance=delayed_compliances_obj,
                                inprogress_compliance_count=inprogress,
                                not_complied_count=not_complied
                            )
                        )
                    year_wise_compliance_count = self.get_year_wise_assignee_compliances(
                        country_id, domain_id, client_id, compliance_ids
                    )
                    assignee_wise_compliances_count.append(
                        dashboard.AssigneeWiseDetails(
                            user_id=int(user_id),
                            assignee_name=self.get_user_name_by_id(user_id),
                            domain_wise_details=domain_wise_compliance_count,
                            year_wise_details= year_wise_compliance_count
                        )
                    )
            chart_data.append(
                dashboard.AssigneeChartData(
                    unit_name=unit_name,
                    address=address,
                    assignee_wise_details=assignee_wise_compliances_count
                )
            )
        return chart_data

    def get_year_wise_assignee_compliances(
        self, country_id, domain_id, client_id, compliance_ids
    ):
        current_year = self.get_date_time().year
        start_year = current_year - 5
        iter_year = start_year
        year_wise_compliance_count = []
        while iter_year <= current_year:
            result = self.get_country_domain_timelines(
                [country_id], [domain_id], [iter_year], client_id
            )
            from_date = result[0][1][0][1][0]["start_date"]
            to_date = result[0][1][0][1][0]["end_date"]
            columns = "sum(case when (approve_status = 1 and (due_date < completion_date or \
            due_date = completion_date)) then 1 else 0 end) as complied, \
            sum(case when ((approve_status = 0 or approve_status is null) and \
            due_date > now()) then 1 else 0 end) as Inprogress, \
            sum(case when ((approve_status = 0 or approve_status is null) and \
            due_date < now()) then 1 else 0 end) as NotComplied, \
            sum(case when (approve_status = 1 and completion_date > due_date) then 1 else 0 end)\
            as DelayedCompliance"
            condition = "compliance_id in (%s) and due_date \
            between '%s' and '%s'" % (
                compliance_ids, from_date, to_date
            )
            rows = self.get_data(
                self.tblComplianceHistory, columns, condition
            )
            complied = 0 if rows[0][0] is None else int(rows[0][0])
            inprogress = 0 if rows[0][1] is None else int(rows[0][1])
            not_complied = 0 if rows[0][2] is None else int(rows[0][2])
            delayed_compliance = 0 if rows[0][3] is None else  int(rows[0][3])
            total = complied + inprogress + not_complied + delayed_compliance
            year_wise_compliance_count.append(
                dashboard.YearWise(
                    year=str(iter_year),
                    total_compliances=total,
                    complied_count=complied,
                    delayed_compliance=delayed_compliance,
                    inprogress_compliance_count=inprogress,
                    not_complied_count=not_complied
                )
            )
            iter_year += 1
        return year_wise_compliance_count

    def get_assigneewise_compliances_drilldown_data(
        self, assignee_id, domain_id, client_id, year
    ):
        level_1_statutories_list = self.get_level_1_statutories_for_user(
            assignee_id, client_id, domain_id
        )

        assigned, reassigned = self.get_user_assigned_reassigned_ids(assignee_id)
        compliance_ids = "%s, %s" % (assigned, reassigned)

        unit_ids = self.get_user_unit_ids(assignee_id)
        complied_unit_wise_compliances = []
        delayed_unit_wise_compliances = []
        inprogress_unit_wise_compliances = []
        not_complied_unit_wise_compliances = []
        for unit_id in [int(x) for x in unit_ids.split(",")]:
            country_id_columns = "country_id"
            country_id_condition = "unit_id = '%d'" % unit_id
            rows = self.get_data(self.tblUnits, country_id_columns, country_id_condition)
            country_id = rows[0][0]
            current_year = year
            if year is None:
                current_year = self.get_date_time().year
            result = self.get_country_domain_timelines(
                [country_id], [domain_id], [current_year], client_id
            )
            from_date = result[0][1][0][1][0]["start_date"]
            to_date = result[0][1][0][1][0]["end_date"]
            complied_compliances = {}
            delayed_compliances = {}
            inprogress_compliances = {}
            not_complied_compliances = {}
            for level_1_statutory in level_1_statutories_list:
                complied_level_1_statutory_wise_compliances = []
                delayed_level_1_statutory_wise_compliances = []
                inprogress_level_1_statutory_wise_compliances = []
                not_complied_level_1_statutory_wise_compliances = []

                columns = "ch.compliance_id, start_date, due_date, completed_on, \
                concat(document_name, '-', compliance_task), compliance_description, statutory_mapping "
                tables = [self.tblComplianceHistory, self.tblCompliances]
                aliases = ["ch", "c"]
                join_type = "inner join"
                join_condition = ["ch.compliance_id = c.compliance_id"]
                where_condition = "completed_by = '{}' and unit_id = {} and \
                due_date  between '{}' and '{}' and statutory_mapping like '{}{}'".format(
                    assignee_id, unit_id, from_date, to_date, level_1_statutory, "%"
                )

                complied_condition = "%s and approve_status = 1 and completed_on <= due_date" % where_condition
                delayed_condition = "%s and approve_status = 1 and completed_on > due_date" % where_condition
                inprogress_condition = "%s and (approve_status = 0 or approve_status is null) and \
                due_date > now()" % where_condition
                not_complied_condition = "%s and (approve_status = 0 or approve_status is null) and \
                due_date < now()" % where_condition

                complied_rows = self.get_data_from_multiple_tables(
                    columns, tables, aliases, join_type,join_condition, complied_condition
                )
                delayed_rows = self.get_data_from_multiple_tables(
                    columns, tables, aliases, join_type,join_condition, delayed_condition
                )
                inprogress_rows = self.get_data_from_multiple_tables(
                    columns, tables, aliases, join_type,join_condition, inprogress_condition
                )
                not_complied_rows = self.get_data_from_multiple_tables(
                    columns, tables, aliases, join_type,join_condition, not_complied_condition
                )

                for compliance in complied_rows:
                    complied_level_1_statutory_wise_compliances.append(
                        dashboard.AssigneeWiseLevel1Compliance(
                            compliance_name=compliance[4], description=compliance[5],
                            assignee_name=self.get_user_name_by_id(assignee_id),
                            assigned_date=self.datetime_to_string(compliance[1]),
                            due_date=self.datetime_to_string(compliance[2]),
                            completion_date=None if compliance[3] is None else self.datetime_to_string(compliance[3])
                        )
                    )
                if len(complied_level_1_statutory_wise_compliances) > 0:
                    complied_compliances[level_1_statutory] = complied_level_1_statutory_wise_compliances

                for compliance in delayed_rows:
                    delayed_level_1_statutory_wise_compliances.append(
                        dashboard.AssigneeWiseLevel1Compliance(
                            compliance_name=compliance[4], description=compliance[5],
                            assignee_name=self.get_user_name_by_id(assignee_id),
                            assigned_date=self.datetime_to_string(compliance[1]),
                            due_date=self.datetime_to_string(compliance[2]),
                            completion_date=None if compliance[3] is None else self.datetime_to_string(compliance[3])
                        )
                    )
                if len(delayed_level_1_statutory_wise_compliances) > 0:
                    delayed_compliances[level_1_statutory] = delayed_level_1_statutory_wise_compliances

                for compliance in inprogress_rows:
                    inprogress_level_1_statutory_wise_compliances.append(
                        dashboard.AssigneeWiseLevel1Compliance(
                            compliance_name=compliance[4], description=compliance[5],
                            assignee_name=self.get_user_name_by_id(assignee_id),
                            assigned_date=self.datetime_to_string(compliance[1]),
                            due_date=self.datetime_to_string(compliance[2]),
                            completion_date=None if compliance[3] is None else self.datetime_to_string(compliance[3])
                        )
                    )
                if len(inprogress_level_1_statutory_wise_compliances) > 0:
                    inprogress_compliances[level_1_statutory] = inprogress_level_1_statutory_wise_compliances

                for compliance in not_complied_rows:
                    not_complied_level_1_statutory_wise_compliances.append(
                        dashboard.AssigneeWiseLevel1Compliance(
                            compliance_name=compliance[4], description=compliance[5],
                            assignee_name=self.get_user_name_by_id(assignee_id),
                            assigned_date=self.datetime_to_string(compliance[1]),
                            due_date=self.datetime_to_string(compliance[2]),
                            completion_date=None if compliance[3] is None else self.datetime_to_string(compliance[3])
                        )
                    )
                if len(not_complied_level_1_statutory_wise_compliances) > 0:
                    not_complied_compliances[level_1_statutory] = not_complied_level_1_statutory_wise_compliances

            unit_columns = "unit_id, concat(unit_code, '-', unit_name), address"
            unit_condition = " unit_id = %d" % unit_id
            unit_details = self.get_data(
                self.tblUnits, unit_columns, unit_condition
            )

            if len(complied_compliances) > 0:
                complied_unit_wise_compliances.append(
                    dashboard.UnitCompliance(
                        unit_name=unit_details[0][1],
                        address=unit_details[0][2],
                        compliances=complied_compliances
                    )
                )
            if len(delayed_compliances) > 0:
                delayed_unit_wise_compliances.append(
                    dashboard.UnitCompliance(
                        unit_name=unit_details[0][1],
                        address=unit_details[0][2],
                        compliances=delayed_compliances
                    )
                )
            if len(inprogress_compliances) > 0:
                inprogress_unit_wise_compliances.append(
                    dashboard.UnitCompliance(
                        unit_name=unit_details[0][1],
                        address=unit_details[0][2],
                        compliances=inprogress_compliances
                    )
                )
            if len(not_complied_compliances) > 0:
                not_complied_unit_wise_compliances.append(
                    dashboard.UnitCompliance(
                        unit_name=unit_details[0][1],
                        address=unit_details[0][2],
                        compliances=not_complied_compliances
                    )
                )
        return (
            complied_unit_wise_compliances, delayed_unit_wise_compliances,
            inprogress_unit_wise_compliances, not_complied_unit_wise_compliances
        )


    def get_unit_user_ids(self, unit_id, client_id=None):
        columns = "group_concat(user_id)"
        table = self.tblUnits
        result = None
        condition = " unit_id = '%d'"% unit_id
        rows = self.get_data(
            self.tblUserUnits, columns, condition
        )
        if rows :
            result = rows[0][0]
        return result

    def get_client_details_report(self, country_id,  business_group_id,
            legal_entity_id, division_id, unit_id, domain_ids):

        condition = "country_id = '%d' "%(country_id)
        if business_group_id is not None:
            condition += " AND business_group_id = '%d'" % business_group_id
        if legal_entity_id is not None:
            condition += " AND legal_entity_id = '%d'" % legal_entity_id
        if division_id is not None:
            condition += " AND division_id = '%d'" % division_id
        if unit_id is not None:
            condition += " AND unit_id = '%d'" % unit_id
        if domain_ids is not None:
            for domain_id in domain_ids:
                condition += " AND  ( domain_ids LIKE  '%,"+str(domain_id)+",%' "+\
                            "or domain_ids LIKE  '%,"+str(domain_id)+"' "+\
                            "or domain_ids LIKE  '"+str(domain_id)+",%'"+\
                            " or domain_ids LIKE '"+str(domain_id)+"') "

        group_by_columns = "business_group_id, legal_entity_id, division_id"
        group_by_condition = condition+" group by business_group_id, legal_entity_id, division_id"
        group_by_rows = self.get_data(self.tblUnits, group_by_columns, group_by_condition)
        GroupedUnits = []
        for row in group_by_rows:
            columns = "unit_id, unit_code, unit_name, geography, "\
            "address, domain_ids, postal_code"

            where_condition = "legal_entity_id = '%d' "% row[1]
            if row[0] == None:
                where_condition += " And business_group_id is NULL"
            else:
                where_condition += " And business_group_id = '%d'" % row[0]
            if row[2] == None:
                where_condition += " And division_id is NULL"
            else:
                where_condition += " And division_id = '%d'" % row[2]
            if unit_id is not None:
                where_condition += " AND unit_id = '%d'" % unit_id
            result_rows = self.get_data(self.tblUnits, columns,  where_condition)
            units = []
            for result_row in result_rows:
                units.append(clientreport.UnitDetails(result_row[0], result_row[3], result_row[1],
                    result_row[2], result_row[4], result_row[6],
                    [int(x) for x in result_row[5].split(",")]))
            GroupedUnits.append(clientreport.GroupedUnits(row[2], row[1], row[0], units))
        return GroupedUnits


    def get_user_assigned_reassigned_ids(self, user_id):
        columns = "group_concat(compliance_id)"
        condition = " assignee = '{}' ".format(
            user_id
        )
        assigned_condition = "%s %s" % (
            condition, "and (is_reassigned = 0 or is_reassigned is null)"
        )
        reassigned_condition = "%s %s" % (
            condition, "and (is_reassigned = 1)"
        )
        assigned_rows = self.get_data(
            self.tblAssignedCompliances, columns, assigned_condition
        )
        reassigned_rows = self.get_data(
            self.tblAssignedCompliances, columns, reassigned_condition
        )
        assigned_compliance_ids = None
        reassigned_compliance_ids = None
        if assigned_rows :
            assigned_compliance_ids = assigned_rows[0][0]
        if reassigned_rows:
            reassigned_compliance_ids = reassigned_rows[0][0]
        return assigned_compliance_ids, reassigned_compliance_ids


#
#   Email
#

#   Service Provider Contract Exiration

    def get_admin_username(self):
        # Getting primary admin username password
        column = "username"
        rows = self.get_data(
            self.tblAdmin, column, "1"
        )
        admin_username = rows[0][0]

        # Getting Secondary admin username password
        column = "email_id"
        condition = "isadmin = 1"
        rows = self.get_data(
            self.tblUsers, column, condition
        )
        for row in rows:
            admin_username += ", %s" % row[0]

        return admin_username

    def get_service_provider_name_by_id(self, service_provider_id):
        column = "service_provider_name"
        condition = "service_provider_id = '%d'" % service_provider_id
        rows = self.get_data(
            self.tblServiceProviders, column, condition
        )
        return rows[0][0]


# Task Rejected notification

    def get_user_email_name(self, user_ids):
        column = "email_id, employee_name"
        condition = "user_id in (%s)" % user_ids
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
        return email_ids, employee_name


    def get_compliance_history_details(self, compliance_history_id):
        columns = "completed_by, ifnull(concurred_by, 0), approved_by, ( \
            select concat(document_name, ' - ', compliance_task) from %s c \
            where c.compliance_id = ch.compliance_id ), due_date" % (self.tblCompliances)
        condition = "compliance_history_id = '%d'" % compliance_history_id
        rows = self.get_data(self.tblComplianceHistory+" ch", columns, condition )
        if rows:
            return rows[0]

    def get_client_details_report(
        self, country_id,  business_group_id,
        legal_entity_id, division_id, unit_id, domain_ids
    ):

        condition = "country_id = '%d' " % (country_id)
        if business_group_id is not None:
            condition += " AND business_group_id = '%d'" % business_group_id
        if legal_entity_id is not None:
            condition += " AND legal_entity_id = '%d'" % legal_entity_id
        if division_id is not None:
            condition += " AND division_id = '%d'" % division_id
        if unit_id is not None:
            condition += " AND unit_id = '%d'" % unit_id
        if domain_ids is not None:
            for domain_id in domain_ids:
                condition += " AND  ( domain_ids LIKE  '%," + str(domain_id) + ",%' " +\
                            "or domain_ids LIKE  '%," + str(domain_id) + "' " +\
                            "or domain_ids LIKE  '" + str(domain_id) + ",%'" +\
                            " or domain_ids LIKE '" + str(domain_id) + "') "

        group_by_columns = "business_group_id, legal_entity_id, division_id"
        group_by_condition = condition+" group by business_group_id, legal_entity_id, division_id"
        group_by_rows = self.get_data(self.tblUnits, group_by_columns, group_by_condition)
        GroupedUnits = []
        for row in group_by_rows:
            columns = "unit_id, unit_code, unit_name, geography, "\
                "address, domain_ids, postal_code"

            where_condition = "legal_entity_id = '%d' " % row[1]
            if row[0] == None:
                where_condition += " And business_group_id is NULL"
            else:
                where_condition += " And business_group_id = '%d'" % row[0]
            if row[2] == None:
                where_condition += " And division_id is NULL"
            else:
                where_condition += " And division_id = '%d'" % row[2]
            if unit_id is not None:
                where_condition += " AND unit_id = '%d'" % unit_id

            result_rows = self.get_data(self.tblUnits, columns,  where_condition)
            units = []
            for result_row in result_rows:
                units.append(clientreport.UnitDetails(
                    result_row[0], result_row[3], result_row[1],
                    result_row[2], result_row[4], result_row[6],
                    [int(x) for x in result_row[5].split(",")]
                ))
            GroupedUnits.append(clientreport.GroupedUnits(row[2], row[1], row[0], units))
        return GroupedUnits

    def get_compliance_task_applicability(self, request, session_user):
        business_group = request.business_group_id
        legal_entity = request.legal_entity_id
        division_id = request.division_id
        unit = request.unit_id
        where_qry = ""
        if business_group is not None :
            where_qry = " AND T4.business_group_id = %s" % (business_group)

        if legal_entity is not None :
            where_qry += " AND T4.legal_entity_id = %s" % (legal_entity)

        if division_id is not None :
            where_qry += " AND T4.division_id = %s" % (division_id)

        if unit is not None :
            where_qry += " AND T3.unit_id = %s" % (unit)

        query = "SELECT T2.statutory_provision, T2.statutory_mapping, \
            T2.compliance_task, T2.document_name, T2.format_file, \
            T2.penal_consequences, T2.compliance_description, \
            T2.statutory_dates, T3.unit_id, (select frequency \
                from tbl_compliance_frequency where \
                frequency_id = T2.frequency_id) as frequency,\
            (select business_group_name from tbl_business_groups where business_group_id = T4.business_group_id)business_group, \
            (select legal_entity_name from tbl_legal_entities where legal_entity_id = T4.legal_entity_id)legal_entity, \
            (select division_name from tbl_divisions where division_id = T4.division_id )division_name,\
            (select group_concat(unit_code, '-', unit_name) from tbl_units \
                where unit_id = T3.unit_id) as unit_name, \
            (select group_concat(address, '-', postal_code) from tbl_units \
                where unit_id = T3.unit_id) as unit_address, \
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
            " % (
                request.country_id,
                request.domain_id,
                where_qry
            )
        rows = self.select_all(query)
        columns = [
            "statutory_provision", "statutory_mapping", "compliance_task",
            "document_name", "format_file", "penal_consequences",
            "compliance_description", "statutory_dates", "unit_id", "frequency",
            "business_group", "legal_entity", "division_name",
            "unit_name", "unit_address", "statutory_applicable",
            "statutory_opted", "compliance_opted",
            "repeat_type", "duration_type", "repeats_every",
            "duration"
        ]
        result = self.convert_to_dict(rows, columns)

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

        applicable_wise = {}
        for r in result :
            unit_id = r["unit_id"]
            mapping = r["statutory_mapping"].split(">>")
            level_1_statutory = mapping[0]
            level_1_statutory = level_1_statutory.strip()

            if r["statutory_applicable"] == 1 :
                applicability_status = "applicable"
            else :
                applicability_status = "not applicable"

            if r["compliance_opted"] == 0:
                applicability_status = "not opted"

            act_wise = applicable_wise.get(applicability_status)
            if act_wise is None :
                act_wise = {}

            unit_wise = act_wise.get(level_1_statutory)

            document_name = r["document_name"]
            if document_name :
                compliance_name = "%s - %s" % (document_name, r["compliance_task"])
            else :
                compliance_name = r["compliance_task"]

            if unit_wise is None :
                unit_wise = {}

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

            compliance_det = unit_wise.get(unit_id)
            if compliance_det is None :
                compliance_det = clientreport.ApplicabilityCompliance(
                    unit_id, r["unit_name"], r["unit_address"],
                    [compliance]
                )
            else :
                compliance_list = compliance_det.compliances
                compliance_list.append(compliance)
                compliance_det.compliances = compliance_list

            unit_wise[unit_id] = compliance_det
            act_wise[level_1_statutory] = unit_wise

            applicable_wise[applicability_status] = act_wise

        applicable_list = {}
        not_applicable_list = {}
        not_opted_list = {}
        for status, value in applicable_wise.iteritems():
            for act, act_data in value.iteritems():
                unit_list = []
                for unit, u_data in act_data.iteritems():
                    unit_list.append(u_data)
                if status == "applicable" :
                    applicable_list[act] = unit_list
                elif status == "not applicable" :
                    not_applicable_list[act] = unit_list
                else :
                    not_opted_list[act] = unit_list

        return clientreport.GetComplianceTaskApplicabilityStatusReportSuccess(
            applicable_list, not_applicable_list, not_opted_list
        )

    def get_on_occurrence_compliances_for_user(self, session_user):
        user_domain_ids = self.get_user_domains(session_user)
        user_unit_ids = self.get_user_unit_ids(session_user)
        unit_wise_compliances = {}
        if user_domain_ids is not None and user_unit_ids is not None:
            for unit in [int(x) for x in user_unit_ids.split(",")]:
                columns = "ac.compliance_id, c.statutory_provision, concat(document_name,'-',\
                compliance_task), compliance_description, duration_type, duration"
                tables = [
                    self.tblAssignedCompliances, self.tblCompliances,
                    self.tblComplianceDurationType
                ]
                aliases = [
                    "ac", "c", "cd"
                ]
                join_type = "inner join"
                join_condition = [
                    "ac.compliance_id = c. compliance_id",
                    "c.duration_type_id = cd.duration_type_id"
                ]
                where_condition = "ac.unit_id = (%d) and c.domain_id in (%s) and \
                c.frequency_id = 4" % (
                    unit, user_domain_ids
                )
                rows = self.get_data_from_multiple_tables(
                    columns, tables, aliases, join_type,
                    join_condition, where_condition
                )
                columns = [
                    "compliance_id", "statutory_provision", "compliance_name",
                    "description", "duration_type", "duration"
                ]
                result = self.convert_to_dict(rows, columns)
                compliances = []
                for row in result:
                    duration = "%s %s" % (row["duration"], row["duration_type"])
                    compliances.append(
                        clientuser.ComplianceOnOccurrence(
                            row["compliance_id"], row["statutory_provision"],
                            row["compliance_name"], row["description"],
                            duration, unit
                        )
                    )
                if len(compliances) > 0:
                    unit_name = self.get_unit_name_by_id(unit)
                    unit_wise_compliances[unit_name] = compliances
        return unit_wise_compliances

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
        start_date = self.string_to_datetime(start_date)
        duration = duration.split(" ")
        duration_value = duration[0]
        duration_type = duration[1]
        due_date = None
        if duration_type == "Day(s)":
            due_date = start_date + datetime.timedelta(days = int(duration_value))
        elif duration_type == "Hour(s)":
            due_date = start_date + datetime.timedelta(hours = int(duration_value))
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

        history_id = self.insert(
            self.tblComplianceHistory, columns, values
        )
        try:
            email.notify_task(
                self, history_id, "Start"
            )
            return True
        except Exception, e:
            print "Error sending email :{}".format(e)


    def get_form_ids_for_admin(self):
        columns = "group_concat(form_id)"
        condition = "is_admin = 1 OR form_type_id in (4,5) OR form_id in (9,11,10,12)"
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
        values = [1, 0]
        result = self.update(
            self.tblAssignedCompliances, columns, values, condition
        )

        columns = "client_statutory_id"
        rows = self.get_data(self.tblClientStatutories, columns, condition)
        if rows:
            client_statutory_id = rows[0][0]

            condition = "client_statutory_id='{}' and unit_id='{}'".format(
                client_statutory_id, unit_id
            )
            self.delete(self.tblClientStatutories, condition)

            condition = "client_statutory_id='{}' ".format(
                client_statutory_id
            )
            self.delete(self.tblClientCompliances, condition)

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
        column = "notification_id"

        notification_condition = "notification_type_id = 1 ORDER BY created_on \
        DESC limit 30"
        reminder_condition = "notification_type_id = 2 ORDER BY created_on \
        DESC limit 30"
        escalation_condition = "notification_type_id = 3 ORDER BY created_on \
        DESC limit 30"

        notification_rows = self.get_data(
            self.tblNotificationsLog, column, notification_condition
        )
        reminder_rows = self.get_data(
            self.tblNotificationsLog, column, reminder_condition
        )
        escalation_rows = self.get_data(
            self.tblNotificationsLog, column, escalation_condition
        )

        notification_ids = None if len(notification_rows) <= 0 else notification_rows[0][0]
        reminder_ids = None if len(reminder_rows) <= 0 else reminder_rows[0][0]
        escalation_ids = None if len(escalation_rows) <= 0 else escalation_rows[0][0]

        column = "count(*)"
        notification_condition = None if notification_ids is None else "notification_ids in (%s) AND read_status=0 AND user_id = '%d'" % (
            notification_ids, session_user
        )
        reminder_condition = None if reminder_ids is None else "notification_ids in (%s) AND read_status=0 AND user_id = '%d'" % (
            reminder_ids, session_user
        )
        escalation_condition = None if escalation_ids is None else "notification_ids in (%s) AND read_status=0 AND user_id = '%d'" % (
            escalation_ids, session_user
        )

        notification_count = 0
        reminder_count = 0
        escalation_count = 0
        if notification_condition is not None:
            notification_count_rows = self.get_data(
                self.tblNotificationUserLog, column, notification_condition
            )
            if notification_count_rows :
                notification_count = notification_count_rows[0]

        if reminder_condition is not None:
            reminder_count_rows = self.get_data(
                self.tblNotificationUserLog, column, reminder_condition
            )
            if reminder_count_rows :
                reminder_count = reminder_count_rows[0]

        if escalation_condition is not None:
            escalation_count_rows = self.get_data(
                self.tblNotificationUserLog, column, escalation_condition
            )
            if escalation_count_rows :
                escalation_count = escalation_count_rows[0]

        ## Getting statutory notifications
        statutory_column = "count(*)"
        statutory_condition = "user_id = '%d' and read_status = 0 ORDER BY \
        statutory_notification_id DESC limit 30" % session_user
        statutory_notification_rows = self.get_data(
            self.tblStatutoryNotificationStatus, statutory_column, statutory_condition
        )
        statutory_notification_count = statutory_notification_rows[0][0]
        notification_count += statutory_notification_count

        return notification_count, reminder_count, escalation_count

    def is_primary_admin(self, user_id):
        column = "count(*)"
        condition = "user_id = '%d' and is_primary_admin = 1" % user_id
        rows = self.get_data(self.tblUsers, column, condition)
        if rows[0][0] > 0:
            return True
        else:
            return False

    def is_service_proivder_user(self, user_id):
        column = "count(*)"
        condition = "user_id = '%d' and is_service_provider = 1" % user_id
        rows = self.get_data(self.tblUsers, column, condition)
        if rows[0][0] > 0:
            return True
        else:
            return False
