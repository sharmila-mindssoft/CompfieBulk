import os
from protocol import (
    core, general, clienttransactions, dashboard,
    clientreport, clientadminsettings
)
from database import Database
import json
import datetime
from datetime import timedelta
from types import *

from types import *

__all__ = [
    "ClientDatabase"
]
ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")
KNOWLEDGE_FORMAT_PATH = os.path.join(ROOT_PATH, "knowledgeformat")
FORMAT_DOWNLOAD_URL = "/client/compliance_format/"

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
        self.tblClientSettings = "tbl_client_settings"
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

    def verify_login(self, username, password):
        tblAdminCondition = "password='%s' and username='%s'" % (
            password, username
        )
        admin_details = self.get_data(
            "tbl_admin", "*", tblAdminCondition
        )
        print admin_details
        if (len(admin_details) == 0) :
            data_columns = [
                "user_id", "user_group_id", "email_id",
                "employee_name", "employee_code", "contact_no",
                "user_group_name", "form_ids"
            ]
            query = "SELECT t1.user_id, t1.user_group_id, t1.email_id, \
                t1.employee_name, t1.employee_code, t1.contact_no, \
                t2.user_group_name, t2.form_ids \
                FROM tbl_users t1 INNER JOIN tbl_user_groups t2\
                ON t1.user_group_id = t2.user_group_id \
                WHERE t1.password='%s' and t1.email_id='%s'" % (
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
        if is_admin != 0:
            whereCondition = " is_admin = 1 order by tf.form_order"
        else:
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

    def verify_username(self, username, client_id):
        columns = "count(*), user_id"
        condition = "email_id='%s'" % (username)
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

    def verify_password(self, password, user_id, client_id):
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
            return user_id
        else:
            return None

    def validate_session_token(self, client_id, session_token) :
        query = "SELECT user_id FROM tbl_user_sessions \
            WHERE session_token = '%s'" % (session_token)
        row = self.select_one(query)
        user_id = row[0]
        return user_id

    def get_forms(self, client_id):
        columns = "tf.form_id, tf.form_type_id, tft.form_type, "
        columns += "tf.form_name, tf.form_url, tf.form_order, tf.parent_menu"
        tables = [self.tblForms, self.tblFormType]
        aliases = ["tf",  "tft"]
        joinConditions = ["tf.form_type_id = tft.form_type_id"]
        whereCondition = " 1 order by tf.form_order"
        joinType = "left join"
        rows = self.get_data_from_multiple_tables(
            columns, tables, aliases, joinType,
            joinConditions, whereCondition
        )
        return rows

    def return_forms(self, client_id):
        columns = "form_id, form_name"
        forms = self.get_data(
            self.tblForms, columns, "1"
        )
        results = []
        for form in forms:
            results.append(general.AuditTrailForm(form[0], form[1]))
        return results

    def get_countries_for_user(self, user_id, client_id) :
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

    def get_domains_for_user(self, user_id, client_id) :
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

    def get_business_groups_for_user(self, business_group_ids, client_id):
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

    def get_legal_entities_for_user(self, legal_entity_ids, client_id):
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
            results.append(core.ClientLegalEntity(
                legal_entity["legal_entity_id"],
                legal_entity["legal_entity_name"],
                legal_entity["business_group_id"]
            ))
        return results

    def get_divisions_for_user(self, division_ids, client_id):
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

    def get_units_for_user(self, unit_ids, client_id):
        columns = "unit_id, unit_code, unit_name, address, division_id,"
        columns += " legal_entity_id, business_group_id, is_active"
        condition = "1"
        if unit_ids is not None:
            condition = "unit_id in (%s)" % unit_ids
        rows = self.get_data(
            self.tblUnits, columns, condition
        )
        columns = [
            "unit_id", "unit_code", "unit_name", "unit_address", "division_id",
            "legal_entity_id", "business_group_id", "is_active"
        ]
        result = self.convert_to_dict(rows, columns)
        return self.return_units(result)

    def get_units_for_user_grouped_by_industry(self, unit_ids, client_id):
        condition = "1"
        if unit_ids is not None:
            condition = "unit_id in (%s)" % unit_ids
        industry_column = "industry_name"
        industry_condition = condition + " group by industry_name"
        industry_rows = self.get_data(
            self.tblUnits, industry_column, industry_condition
        )

        columns = "unit_id, unit_code, unit_name, address, division_id,"+\
        " legal_entity_id, business_group_id, is_active"
        industry_wise_units =[]
        for industry in industry_rows:
            industry_name = industry[0]
            units = []
            condition += " and industry_name = '%s'" % industry_name
            rows = self.get_data(
                self.tblUnits, columns, condition
            )
            for unit in rows:
                units.append(core.ClientUnit(
                    unit[0], unit[4], unit[5],unit[6], unit[1],
                    unit[2], unit[3], bool(unit[7])
                ))
            industry_wise_units.append(clienttransactions.IndustryWiseUnits(industry_name, units))
        return industry_wise_units

    def return_units(self, units):
        results = []
        for unit in units :
            results.append(core.ClientUnit(
                unit["unit_id"], unit["division_id"], unit["legal_entity_id"],
                unit["business_group_id"], unit["unit_code"],
                unit["unit_name"], unit["unit_address"], bool(unit["is_active"])
            ))
        return results

    def save_activity(self, user_id, form_id, action, client_id):
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
            self.tblUserGroups, columns, "1"
        )
        return rows

    def get_user_privileges(self, client_id):
        columns = "user_group_id, user_group_name, is_active"
        rows = self.get_data(
            self.tblUserGroups, columns, "1"
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
        " is_admin, is_service_provider, service_provider_id, is_active"
        condition = "1"
        rows =  self.get_data(
            self.tblUsers,columns, condition
        )
        columns = ["user_id", "email_id", "user_group_id", "employee_name",
        "employee_code", "contact_no", "seating_unit_id", "user_level",
        "is_admin", "is_service_provider", "service_provider_id", "is_active"]
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
                user["service_provider_id"], bool(user["is_active"])))
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
        values = [ user_id, user.user_group_id, user.email_id, self.generate_password(), user.employee_name,
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

        action = None
        if is_admin == 0:
            action = "User \"%s - %s\" was demoted from admin status" % (employee_code, employee_name)
        else:
            action = "User \"%s - %s\" was promoted to admin status" % (employee_code, employee_name)
        self.save_activity(session_user, 4, action, client_id)

        return result

    def get_user_company_details(self, user_id, client_id):
        columns = "group_concat(unit_id)"
        condition = " user_id = '%d'"% user_id
        rows = self.get_data(
            self.tblUserUnits, columns, condition
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

    def get_user_countries(self, user_id, client_id):
        columns = "group_concat(country_id)"
        condition = " user_id = '%d'" % user_id
        rows = self.get_data(
            self.tblUserCountries, columns, condition
        )
        return rows[0][0]

    def get_user_domains(self, user_id, client_id):
        columns = "group_concat(domain_id)"
        condition = " user_id = '%d'" % user_id
        rows = self.get_data(
            self.tblUserDomains, columns, condition
        )
        return rows[0][0]

    def get_user_unit_ids(self, user_id, client_id):
        columns = "group_concat(unit_id)"
        condition = " user_id = '%d'"% user_id
        rows = self.get_data(
            self.tblUserUnits, columns, condition
        )
        return rows[0][0]

    def get_client_users(self, client_id):
        columns = "user_id, employee_name, employee_code, is_active"
        condition = "1"
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
            self.tblServiceProviders, columns, "1"
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

    def get_service_providers(self, client_id):
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
        forms = self.return_forms(client_id)
        return general.GetAuditTrailSuccess(audit_trail_details, users, forms)

#
# Statutory settings
#

    def get_statutory_settings(self, session_user, client_id):
        query = "SELECT distinct t1.client_statutory_id, \
            t1.geography, t1.country_id, t1.domain_id, t1.unit_id, \
            t2.unit_name, \
            t3.business_group_name, t4.legal_entity_name,\
            t5.division_name, t2.address, t2.postal_code, t2.unit_code, \
            t6.country_name, t7.domain_name \
            FROM tbl_client_statutories t1 \
            INNER JOIN tbl_units t2 \
            ON t1.unit_id = t2.unit_id \
            INNER JOIN tbl_business_groups t3 \
            ON t2.business_group_id = t3.business_group_id \
            INNER JOIN tbl_legal_entities t4 \
            ON t2.legal_entity_id = t4.legal_entity_id \
            INNER JOIN tbl_divisions t5 \
            ON t2.division_id = t5.division_id \
            INNER JOIN tbl_countries t6 \
            ON t1.country_id = t6.country_id \
            INNER JOIN tbl_domains t7 \
            ON t1.domain_id = t7.domain_id "
        rows = self.select_all(query)
        columns = [
            "client_statutory_id", "geography",
            "country_id", "domain_id", "unit_id", "unit_name",
            "business_group_name", "legal_entity_name",
            "division_name", "address", "postal_code", "unit_code",
            "country_name", 'domain_name'
        ]
        result = self.convert_to_dict(rows, columns)
        return self.return_statutory_settings(result, client_id)

    def return_compliance_for_statutory_settings(
        self, domain_id, client_statutory_id,
        client_id
    ):
        query = "SELECT t1.client_statutory_id, t1.compliance_id, \
            t1.statutory_applicable, t1.statutory_opted,\
            t1.not_applicable_remarks, \
            t1.compliance_applicable, t1.compliance_opted, \
            t1.compliance_remarks, \
            t2.compliance_task, t2.document_name, t2.statutory_mapping,\
            t2.statutory_provision, t2.compliance_description \
            FROM tbl_client_compliances t1 \
            INNER JOIN tbl_compliances t2 \
            ON t1.compliance_id = t2.compliance_id \
            INNER JOIN tbl_client_statutories t3 \
            ON t1.client_statutory_id = t3.client_statutory_id \
            WHERE t3.domain_id = %s AND \
            t1.client_statutory_id = %s" % (
                domain_id, client_statutory_id
            )
        rows = self.select_all(query)
        columns = [
            "client_statutory_id", "compliance_id",
            "statutory_applicable", "statutory_opted",
            "not_applicable_remarks", "compliance_applicable",
            "compliance_opted", "compliance_remarks",
            "compliance_task", "document_name", "statutory_mapping",
            "statutory_provision", "compliance_description"
        ]
        results = self.convert_to_dict(rows, columns)
        statutory_wise_compliances = {}
        for r in results :
            statutory_opted = r["statutory_opted"]
            if type(statutory_opted) is int :
                statutory_opted = bool(statutory_opted)
            else :
                statutory_opted = bool(r["statutory_applicable"])

            compliance_opted = r["compliance_opted"]
            if type(compliance_opted) is int :
                compliance_opted = bool(compliance_opted)
            else :
                compliance_opted = bool(r["compliance_applicable"])

            compliance_remarks = r["compliance_remarks"]
            if compliance_remarks == "" :
                compliance_remarks = None

            mappings = r["statutory_mapping"].split('>>')
            statutory_name = mappings[0].strip()
            provision = "%s - %s" % (
                ','.join(mappings[1:]),
                r["statutory_provision"]
            )
            name = "%s - %s" % (
                r["document_name"], r["compliance_task"]
            )
            compliance = clienttransactions.ComplianceApplicability(
                r["compliance_id"],
                name,
                r["compliance_description"],
                provision,
                bool(r["compliance_applicable"]),
                bool(compliance_opted),
                compliance_remarks
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
            client_statutory_id = d["client_statutory_id"]
            statutories = self.return_compliance_for_statutory_settings(
                domain_id, client_statutory_id, client_id
            )

            unit_statutories = unit_wise_statutories.get(unit_id)
            if unit_statutories is None :
                statutory_dict = {}
                statutory_dict[domain_id] = statutories.values()
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
                domain_statutories = statutory_dict.get(domain_id)
                if domain_statutories is None :
                    domain_statutories = statutories.values()
                else :
                    domain_statutories.extend(statutories.values())
                statutory_dict[domain_id] = domain_statutories

                # set values
                unit_statutories.domain_names = domain_list
                unit_statutories.statutories = statutory_dict
            unit_wise_statutories[unit_id] = unit_statutories

        return clienttransactions.GetStatutorySettingsSuccess(
            unit_wise_statutories.values()
        )

    def update_statutory_settings(self, data, session_user, client_id):
        unit_id = data.unit_id
        statutories = data.statutories
        updated_on = self.get_date_time()
        for s in statutories :
            client_statutory_id = s.client_statutory_id
            statutory_opted_status = int(s.applicable_status)
            not_applicable_remarks = s.not_applicable_remarks
            if not_applicable_remarks is None :
                not_applicable_remarks = ""
            compliances = s.compliances
            for c in compliances :
                compliance_id = c.compliance_id
                opted_status = int(c.compliance_opted_status)
                remarks = c.compliance_remarks

                query = "UPDATE tbl_client_compliances t1 \
                    INNER JOIN tbl_client_statutories t2 \
                    ON t1.client_statutory_id = t2.client_statutory_id \
                    SET \
                    t1.statutory_opted=%s, \
                    t1.not_applicable_remarks='%s', \
                    t1.compliance_opted=%s, \
                    t1.compliance_remarks='%s',\
                    t1.updated_by=%s, \
                    t1.updated_on='%s' \
                    WHERE t2.unit_id = %s \
                    AND t1.client_statutory_id = %s \
                    AND t1.compliance_id = %s" % (
                        statutory_opted_status, not_applicable_remarks,
                        opted_status, remarks, session_user, updated_on,
                        unit_id, client_statutory_id, compliance_id
                    )
                self.execute(query)

        return clienttransactions.UpdateStatutorySettingsSuccess()

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

    def get_level_1_statutories_for_user(self, session_user, client_id):
        domain_rows = self.get_data(self.tblUserDomains, "group_concat(domain_id)",
            "user_id='%d'"%session_user, client_id)

        domain_ids = domain_rows[0][0]

        client_statutory_rows = self.get_data(
            self.tblClientStatutories,
            "group_concat(client_statutory_id)",
            "domain_id in (%s)" % domain_ids,
            )
        client_statutory_ids = client_statutory_rows[0][0]

        client_compliance_rows = self.get_data(
            self.tblClientCompliances,
            "group_concat(compliance_id)",
            "client_statutory_id in (%s)" % client_statutory_ids,
            )
        client_compliance_ids = client_compliance_rows[0][0]

        mapping_rows = self.get_data(
            self.tblCompliances,
            "statutory_mapping",
            "compliance_id in (%s)" % (client_compliance_ids),
            client_id
        )

        level_1_statutory = []
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

    def get_statutory_wise_compliances(
        unit_id, domain_id, level_1_statutory_id,
        frequecy_id
    ):
        client_statutory_columns = "group_concat(client_statutory_id)"
        client_statutory_condition = " unit_id = '%d' and \
            domain_id = '%d' " % (
            unit_id, domain_id
        )
        client_statutory_rows = self.get_data(
            self.tblClientStatutories,
            client_statutory_columns,
            client_statutory_condition
        )
        client_statutory_ids = None
        if len(client_statutory_rows) > 0:
            client_statutory_ids = client_statutory_rows[0][0]
        else:
            return

        client_compliances_columns = "group_concat(compliance_id)"
        client_compliances_condition = " client_statutory_id in \
            (%s)" % client_statutory_ids

        client_compliances_rows = self.get_data(
                self.tblClientCompliances,
                client_compliances_columns,
                client_compliances_condition
            )
        client_compliance_ids = None
        if len(client_compliance_rows) > 0:
            client_compliance_ids = client_compliance_rows[0][0]
        else:
            return
        compliance_columns = "compliance_id, compliance_task, document_name, statutory_dates"
        compliance_condition = " compliance_id in (%s) " % client_compliance_ids
        compliance_rows = self.get_data(
            self.tblCompliances, compliance_columns,
            compliance_condition
        )
        for compliance in compliance_rows:
            pass

    def get_compliance_approval_list(self, session_user, client_id):
        assignee_columns = "completed_by, employee_code, employee_name"
        join_type = "left join"
        tables = [self.tblComplianceHistory, self.tblUsers]
        aliases = ["tch", "tu"]
        join_condition = ["tch.completed_by = tu.user_id"]
        assignee_condition = "completion_date is not Null and completed_on is not Null and "+\
        "approve_status is Null and (approved_by = '%d' or concurred_by = '%d')" % (session_user, session_user)
        assignee_rows = self.get_data_from_multiple_tables(
            assignee_columns, tables,
            aliases, join_type,  join_condition,
            assignee_condition
        )
        approved_compliances = []
        for assignee in assignee_rows:
            query_columns = "compliance_history_id, tch.compliance_id, start_date,"+\
            " due_date, documents, completion_date, completed_on, next_due_date, "+\
            "concurred_by, remarks, datediff(due_date, completion_date ),compliance_task,"+\
            " compliance_description, tc.frequency_id, frequency, document_name, concurrence_status"
            join_type = "left join"
            query_tables = [
                    self.tblComplianceHistory,
                    self.tblCompliances,
                    self.tblComplianceFrequency
            ]
            aliases = ["tch", "tc", "tcf"]
            join_condition = [
                    "tch.compliance_id = tc.compliance_id",
                    "tc.frequency_id = tcf.frequency_id"
            ]
            where_condition = "%s and completed_by = '%d'"% (
                assignee_condition, assignee[0]
            )
            rows = self.get_data_from_multiple_tables(
                query_columns, query_tables, aliases,
                join_type, join_condition,
                where_condition
            )
            compliances = []
            for row in rows:
                compliance_history_id = row[0]
                compliance_id = row[1]
                start_date = self.datetime_to_string(row[2])
                due_date = self.datetime_to_string(row[3])
                documents = row[4].split(",")
                completion_date = self.datetime_to_string(row[5])
                completed_on = self.datetime_to_string(row[6])
                next_due_date = self.datetime_to_string(row[7])
                concurred_by = self.get_user_name_by_id(int(row[8]), client_id)
                remarks = row[9]
                delayed_by = None if row[10] < 0 else row[10]
                compliance_name = "%s - %s"%(row[15], row[11])
                compliance_description = row[12]
                frequency_id = int(row[13])
                frequency = core.COMPLIANCE_FREQUENCY(row[14])
                description = row[12]
                concurrence_status = row[16]

                domain_name_column = "domain_name"
                condition = " domain_id = (select domain_id from tbl_client_statutories "+\
                " where client_statutory_id = (select client_statutory_id from "+\
                " tbl_client_compliances where compliance_id ='%d'))" % compliance_id
                domain_name_row =  self.get_data(
                    self.tblDomains, domain_name_column,
                    condition
                )
                domain_name = domain_name_row[0][0]

                action = None
                if int(row[8]) == session_user:
                    action = "Concur"
                else:
                    if concurrence_status is not None:
                        if concurrence_status != 0:
                            action = "Approve"
                        else:
                            continue
                    else:
                        continue

                compliances.append(clienttransactions.APPROVALCOMPLIANCE(
                    compliance_history_id, compliance_name, description, domain_name,
                    start_date, due_date, delayed_by, frequency, documents,
                    completion_date, completed_on, next_due_date, concurred_by,
                    remarks, action))
            assignee_id = assignee[0]
            assignee_name = "{} - {}".format(assignee[1], assignee[2])
            if len(compliances) > 0:
                approved_compliances.append(clienttransactions.APPORVALCOMPLIANCELIST(
                    assignee_id, assignee_name, compliances))
            else:
                continue
        return approved_compliances


    def get_compliance_approval_status_list(self, session_user, client_id):
        columns = "compliance_status_id, compliance_status"
        condition = "1"
        rows = self.get_data(
            self.tblComplianceStatus, columns, condition
        )
        columns = columns.split(",")
        return self.return_compliance_approval_status_list(columns, rows)

    def return_compliance_approval_status_list(self, columns, compliance_status_list):
        result_compliance_status = []
        for compliance_status in compliance_status_list:
            result_compliance_status.append(core.ComplianceApprovalStatus(
                compliance_status[0], core.COMPLIANCE_APPROVAL_STATUS(compliance_status[1])))
        return result_compliance_status

    def get_user_name_by_id(self, user_id, client_id):
        employee_name = None
        if user_id != None:
            columns = "employee_code, employee_name"
            condition = "user_id ='{}'".format(user_id)
            rows = self.get_data(
                self.tblUsers, columns, condition
            )
            if len(rows) > 0:
                employee_name = "{} - {}".format(rows[0][0], rows[0][1])
        return employee_name

    # def calculate_next_due_date(self, completion_date, due_date, compliance_id):
    #     compliance_columns = "statutory_date, repeat_type_id, duration_type_id,"+\
    #     " repeats_every, duration"
    #     condition = "compliance_id = '%d'" % compliance_id
    #     compliance_rows = self.get_data(self.tblCompliances, compliance_columns,
    #         condition)
    #     if len(compliance_rows) > 0:
    #         statutory_date = compliance_rows[0][0]
    #         repeat_type_id = compliance_rows[0][1]
    #         duration_type_id = compliance_rows[0][2]
    #         repeats_every = compliance_rows[0][3]
    #         duration = compliance_rows[0][4]
    #         if statutory_date == None:
    #             if repeat_type_id = 1:

    #             elif repeat_type_id = 2:
    #             elif repeat_type_id = 3:

#
# Assign Compliance
#

    def get_units_for_assign_compliance(self, session_user, client_id):
        if session_user == 0 :
            session_user = '%'
        query = "SELECT distinct t1.unit_id, t1.unit_code, t1.unit_name, \
            t1.division_id, t1.legal_entity_id, t1.business_group_id, \
            t1.address \
            FROM tbl_units t1 \
            INNER JOIN tbl_user_units t2 \
            ON t1.unit_id = t2.unit_id \
            AND t2.user_id like '%s' " % (
                session_user
            )
        rows = self.select_all(query)
        columns = [
            "unit_id", "unit_code", "unit_name",
            "division_id", "legal_entity_id",
            "business_group_id", "address"
        ]
        result = self.convert_to_dict(rows, columns)
        unit_list = []
        for r in result :
            name = "%s - %s" % (r["unit_code"], r["unit_name"])
            unit_list.append(
                clienttransactions.ASSIGN_COMPLIANCE_UNITS(
                    r["unit_id"], name,
                    r["address"],
                    r["division_id"],
                    r["legal_entity_id"],
                    r["business_group_id"]
                )
            )
        return unit_list

    def get_users_for_seating_units(self, session_user, client_id):
        where_condition = " WHERE t1.seating_unit_id In \
            (SELECT t.unit_id FROM tbl_user_units t \
            WHERE t.user_id = %s)" % (
                session_user
            )
        query = "SELECT t1.user_id, t1.employee_name, t1.employee_code, \
            t1.seating_unit_id, t1.user_level, \
            group_concat(distinct t2.domain_id) domain_ids, \
            group_concat(distinct t3.unit_id) unit_ids, \
            t4.address \
            FROM tbl_users t1 \
            INNER JOIN tbl_user_domains t2\
            ON t1.user_id = t2.user_id \
            INNER JOIN tbl_user_units t3\
            ON t1.user_id = t3.user_id \
            INNER JOIN tbl_units t4 \
            ON t1.seating_unit_id = t4.unit_id "

        if session_user > 0 :
            query = query + where_condition
        rows = self.select_all(query)
        columns = [
            "user_id", "employee_name", "employee_code",
            "seating_unit_id", "user_level",
            "domain_ids", "unit_ids", "address"
        ]
        result = self.convert_to_dict(rows, columns)
        seating_unit_users = {}
        for r in result :
            name = "%s - %s" % (r["employee_code"], r["employee_name"])
            unit_id = int(r["seating_unit_id"])
            domain_ids = [
                int(x) for x in r["domain_ids"].split(',')
            ]
            unit_ids = [
                int(y) for y in r["unit_ids"].split(',')
            ]
            user = clienttransactions.ASSIGN_COMPLIANCE_USER(
                r["user_id"],
                name,
                r["user_level"],
                unit_id,
                unit_ids,
                domain_ids,
                r["address"]
            )
            user_list = seating_unit_users.get(unit_id)
            if user_list is None :
                user_list = []
            user_list.append(user)
            seating_unit_users[unit_id] = user_list

        return seating_unit_users

    def get_assign_compliance_statutories_for_units(
        self, unit_ids, session_user, client_id
    ):
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
            t4.frequency\
            FROM tbl_client_compliances t2 \
            INNER JOIN tbl_client_statutories t1 \
            ON t2.client_statutory_id = t1.client_statutory_id \
            INNER JOIN tbl_compliances t3 \
            ON t2.compliance_id = t3.compliance_id \
            INNER JOIN tbl_compliance_frequency t4 \
            ON t3.frequency_id = t4.frequency_id \
            INNER JOIN tbl_user_domains t5 \
            ON t1.domain_id = t5.domain_id \
            INNER JOIN \
            (SELECT distinct U.compliance_id, group_concat(distinct U.unit_id) units FROM  \
            (SELECT A.unit_id, A.client_statutory_id, B.compliance_id FROM tbl_client_statutories A \
            INNER JOIN tbl_client_compliances B \
            ON A.client_statutory_id = B.client_statutory_id) U \
            group by U.compliance_id )UC \
            ON t2.compliance_id = UC.compliance_id \
            WHERE \
            t2.compliance_id NOT IN (SELECT C.compliance_id \
            FROM tbl_assigned_compliances C WHERE \
            C.unit_id IN %s ) \
            AND t1.unit_id IN %s \
            AND t2.statutory_opted = 1 \
            AND t2.compliance_opted = 1 \
            AND t3.is_active = 1 \
            AND t5.user_id LIKE '%s'; " % (
                str(tuple(unit_ids)),
                str(tuple(unit_ids)),
                session_user
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
            "statutory_dates", "frequency"
        ]
        result = self.convert_to_dict(rows, columns)
        return self.return_assign_compliance_data(result)

    def return_assign_compliance_data(self, result):
        now = datetime.datetime.now()
        current_month = now.month
        domain_wise_compliance = {}
        for r in result:
            domain_id = int(r["domain_id"])
            unit_ids = [
                int(x) for x in r["units"].split(',')
            ]
            compliance_list = domain_wise_compliance.get(domain_id)
            if compliance_list is None :
                compliance_list = []
            name = "%s - %s" % (r["document_name"], r["compliance_task"])
            statutory_dates = r["statutory_dates"]
            statutory_dates = json.loads(statutory_dates)
            date_list = []
            due_date = None
            for date in statutory_dates :
                s_date = core.StatutoryDate(
                    date["statutory_date"],
                    date["statutory_month"],
                    date["trigger_before_days"]
                )
                date_list.append(s_date)

            add_month = 0
            for date in statutory_dates:
                month = date["statutory_month"]
                s_day = date["statutory_date"]
                if current_month < month :
                    add_month = month - current_month
                    n_date = (datetime.date.today() + datetime.timedelta(add_month*365/12)).isoformat()
                    n_date = datetime.datetime.strptime(n_date, "%Y-%m-%d")
                    new_date = n_date.replace(day = s_day)
                    due_date = new_date.strftime("%d-%b-%Y")
                    break;

            compliance = clienttransactions.UNIT_WISE_STATUTORIES(
                r["compliance_id"],
                name,
                r["compliance_description"],
                core.COMPLIANCE_FREQUENCY(r["frequency"]),
                date_list,
                due_date,
                unit_ids
            )
            compliance_list.append(compliance)
            domain_wise_compliance[domain_id] = compliance_list
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
        for c in compliances:
            compliance_id = int(c.compliance_id)
            statutory_dates = c.statutory_dates
            if statutory_dates is not None :
                date_list = []
                for dates in statutory_dates :
                    date_list.append(dates.to_structure())
                date_list = json.dumps(date_list)
                due_date = datetime.datetime.strptime(c.due_date, "%d-%b-%Y")
                validity_date = c.validity_date
                if validity_date is not None :
                    validity_date = datetime.datetime.strptime(validity_date, "%d-%b-%Y")
                else :
                    validity_date = ""
            else :
                date_list = []
                due_date = ""
                validity_date = ""
            unit_ids = c.unit_ids
            for unit_id in unit_ids:
                query = "INSERT INTO tbl_assigned_compliances \
                    (country_id, unit_id, compliance_id, \
                    statutory_dates, assignee, \
                    concurrence_person, approval_person, \
                    due_date, validity_date, created_by, \
                    created_on) VALUES \
                    (%s, %s, %s, '%s', %s, '%s', %s, '%s', '%s', %s, '%s')" % (
                        country_id, unit_id, compliance_id,
                        date_list, assignee, concurrence,
                        approval, due_date, validity_date,
                        int(session_user), created_on
                    )
                self.execute(query)
            self.update_user_units(assignee, unit_ids, client_id)

        return clienttransactions.SaveAssignedComplianceSuccess()

    def update_user_units(self, user_id, unit_ids, client_id):
        user_units = self.get_user_unit_ids(user_id, client_id)
        user_units = [ int(x) for x in user_units.split(',')]
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

#
#   Chart Api
#
    def get_compliance_status(self, group_by_name, status_type_qry, filter_type_ids, client_id, request, chart_type=None) :
        country_ids = request.country_ids
        domain_ids = request.domain_ids
        if chart_type is None :
            from_date = request.from_date
            to_date = request.to_date
        else :
            from_date = None
            to_date = None

        date_qry = ""
        if from_date is not None and to_date is not None :
            date_qry = "AND T1.due_date >= '%s' AND T1.due_date <= '%s' " % (from_date, to_date)
        query = "SELECT \
            %s, \
            T3.country_id, \
            T3.domain_id, \
            SUBSTRING_INDEX(T1.due_date, '-', 1) as year, \
            SUBSTRING_INDEX(SUBSTRING_INDEX(T1.due_date , '-', -2 ),'-',1) as month,  \
            count(SUBSTRING_INDEX(SUBSTRING_INDEX(T1.due_date , '-', -2 ),'-',1)) as compliances \
            FROM tbl_compliance_history T1 \
            INNER JOIN tbl_client_compliances T2 \
            ON T1.compliance_id = T2.compliance_id \
            INNER JOIN tbl_client_statutories T3 \
            ON T2.client_statutory_id = T3.client_statutory_id \
            AND T1.unit_id = T3.unit_id \
            INNER JOIN tbl_units T4 \
            ON T1.unit_id = T4.unit_id \
            INNER JOIN tbl_divisions T5 \
            ON T4.division_id = T5.division_id \
            INNER JOIN tbl_legal_entities T6 \
            ON T4.legal_entity_id = T6.legal_entity_id \
            INNER JOIN tbl_business_groups T7 \
            ON T4.business_group_id = T7.business_group_id \
            INNER JOIN tbl_countries T8 \
            ON T3.country_id = T8.country_id \
            WHERE T3.country_id IN %s \
            AND T3.domain_id IN %s  \
            %s \
            %s \
            %s \
            GROUP BY month, year, T3.domain_id, %s\
            ORDER BY month desc, year desc, %s" % (
                group_by_name,
                str(tuple(country_ids)),
                str(tuple(domain_ids)),
                status_type_qry,
                filter_type_ids,
                date_qry,
                group_by_name,
                group_by_name
            )
        rows = self.select_all(query)
        columns = ["filter_type", "country_id", "domain_id", "year", "month", "compliances"]
        return self.convert_to_dict(rows, columns)

    def calculate_years(self, month_from, month_to):
        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year
        if month_from == 1 and month_to == 12 :
            single_years = []
            single_years.append(current_year)
            for i in range(1, 7):
                single_years.append(current_year - i)
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

    def get_status_wise_compliances_count(self, request, client_id):
        country_ids = request.country_ids
        domain_ids = request.domain_ids
        from_date =request.from_date
        to_date = request.to_date
        filter_type = request.filter_type
        filter_ids = request.filter_ids
        _bgroup_ids = '%'
        _lentity_ids = '%'
        _division_ids = '%'
        _unit_ids = '%'

        inprogress_qry = " AND T1.due_date > CURDATE() \
                AND T1.approve_status is NULL"

        complied_qry = " AND T1.due_date >= T1.completion_date \
                AND T1.approve_status = 1"

        delayed_qry = " AND T1.due_date < T1.completion_date \
                AND T1.approve_status = 1"

        not_complied_qry = " AND T1.due_date < CURDATE() \
                AND T1.approve_status is NULL "

        date_qry = ""

        if filter_ids == None :
            filter_ids = country_ids

        if len(filter_ids) == 1:
            filters = "(%s)" % filter_ids[0]
        else :
            filters = str(tuple(filter_ids))

        if filter_type ==  "Group" :
            group_by_name = "T4.country_id"
            # filter_type_ids = country_ids
            filter_type_ids = ""

        elif filter_type == "BusinessGroup" :
            group_by_name = "T4.business_group_id"
            filter_type_ids = "AND T4.business_group_id in %s" % (filters)

        elif filter_type == "LegalEntity" :
            group_by_name = "T4.legal_entity_id"
            filter_type_ids = "AND T4.legal_entity_id in %s" % (filters)

        elif filter_type == "Division" :
            group_by_name = "T4.division_id"
            filter_type_ids = "AND T4.division_id in %s" % (filters)

        elif filter_type == "Unit":
            group_by_name = "T4.unit_id"
            filter_type_ids = "AND T4.unit_id in %s" % (filters)

        elif filter_type == "Consolidated":
            group_by_name = "T4.country_id"
            filter_type_ids = ""

        inprogress = self.get_compliance_status(
                group_by_name, inprogress_qry, filter_type_ids, client_id,
                request
            )

        complied = self.get_compliance_status(
                group_by_name, complied_qry, filter_type_ids, client_id,
                request
            )
        delayed = self.get_compliance_status(
                group_by_name, delayed_qry, filter_type_ids, client_id,
                request
            )
        not_complied = self.get_compliance_status(
                group_by_name, not_complied_qry, filter_type_ids, client_id,
                request
            )

        if from_date is not None and to_date is not None :
            return self.frame_compliance_status_count(inprogress, complied, delayed, not_complied, filter_ids, domain_ids, client_id)
        else :
            return self.frame_compliance_status_yearwise_count(inprogress, complied, delayed, not_complied, filter_ids, domain_ids, client_id)

    def get_client_domain_configuration(self, client_id, country_id = None, domain_id = None) :
        where_qry = ""
        if country_id is not None and domain_id is not None :
            where_qry = " WHERE country_id = %s AND domain_id = %s" % (country_id, domain_id)

        query = "SELECT country_id, domain_id, \
            period_from, period_to \
            FROM  tbl_client_configurations %s" % (where_qry)

        rows = self.select_all(query)
        columns = ["country_id", "domain_id", "period_from", "period_to"]
        data = self.convert_to_dict(rows, columns)
        years_range = []
        for d in data :
            info = {}
            info["country_id"] = int(d["country_id"])
            info["domain_id"] = int(d["domain_id"])
            info["years"] = self.calculate_years(int(d["period_from"]), int(d["period_to"]))
            info["period_from"] = int(d["period_from"])
            info["period_to"] = int(d["period_to"])
            years_range.append(info)
        return years_range

    def calculate_year_wise_count(self, calculated_data, years_info, compliances, status, filter_ids, domain_ids):
        def month_range(period_from, period_to):
            if period_from == 1 and period_to == 12:
                return [int (x) for x in range(period_from, period_to + 1)]
            else :
                lst = [int (x) for x in range(period_from, 12+1)]
                lst.extend([int(y) for y in range(1, period_to+1)])
                return lst
        for f in filter_ids:
            filter_type = int(f)
            for y in years_info :

                country_id = y["country_id"]

                domain_id = y["domain_id"]

                if domain_id not in domain_ids :
                    continue

                country = calculated_data.get(filter_type)
                if country is None :
                    country = {}

                years_range = y["years"]

                year_wise = country.get(domain_id)
                if year_wise is None :
                    year_wise = {}
                month_list = month_range(y["period_from"], y["period_to"])
                period_from = int(y["period_from"])
                period_to = int(y["period_to"])
                for index, i in enumerate(years_range) :

                    compliance_sum = year_wise.get(str(i))

                    if compliance_sum is None :
                        compliance_sum = [0, 0, 0, 0]
                        compliance_count = 0
                    else :
                        if status == "inprogress":
                            compliance_count = compliance_sum[0]
                        elif status == "complied" :
                            compliance_count = compliance_sum[1]
                        elif status == "delayed" :
                            compliance_count = compliance_sum[2]
                        elif status == "not_complied":
                            compliance_count = compliance_sum[3]


                    if type(i) is list :
                        for c in compliances :
                            if int(c["year"]) not in (i) :
                                continue
                            if (filter_type == int(c["filter_type"]) and
                                country_id == c["country_id"] and domain_id == int(c["domain_id"])):
                                month = int(c["month"])
                                if int(c["year"]) == i[0] and month in [int(x) for x in range(period_from, 12+1)] :
                                    compliance_count += int(c["compliances"])

                                elif int(c["year"]) == i[1] and month in [int(y) for y in range(1, period_to+1)] :
                                    compliance_count += int(c["compliances"])

                    elif type(i) is int :
                        for c in compliances :

                            if int(c["year"]) != i :
                                continue
                            if (filter_type == int(c["filter_type"]) and
                                country_id == c["country_id"] and domain_id == int(c["domain_id"])):
                                month = int(c["month"])

                                if int(c["year"]) == i and month in [int (x) for x in range(period_from, period_to + 1)]:
                                    compliance_count += int(c["compliances"])

                    if status == "inprogress":
                        compliance_sum[0] = compliance_count
                    elif status == "complied" :
                        compliance_sum[1] = compliance_count
                    elif status == "delayed" :
                        compliance_sum[2] = compliance_count
                    elif status == "not_complied":
                        compliance_sum[3] = compliance_count

                    year_wise[str(i)] = compliance_sum


                country[domain_id] = year_wise
                calculated_data[filter_type] = country

        return calculated_data

    def frame_compliance_status_count(self, inprogress, complied, delayed, not_complied, filter_ids, domain_ids, client_id):
        calculated_data = {}

        def compliance_count(compliances, status):
            for i in compliances :
                filter_type = int(i["filter_type"])
                domain_id = int(i["domain_id"])
                domain_wise = calculated_data.get(filter_type)

                # domain_wise = country.get(domain_id)
                if domain_wise is None :
                    domain_wise = {}

                compliance_sum = domain_wise.get(domain_id)
                if compliance_sum is None :
                    compliance_sum = [0, 0, 0, 0]
                    compliance_count = 0
                else :
                    compliance_count = compliance_sum[status]

                compliance_count += int(i["compliances"])
                compliance_sum[status] = compliance_count
                domain_wise[domain_id] = compliance_sum
                calculated_data[filter_type] = domain_wise
            return calculated_data

        calculated_data = compliance_count(inprogress, 0)
        calculated_data = compliance_count(complied, 1)
        calculated_data = compliance_count(delayed, 2)
        calculated_data = compliance_count(not_complied, 3)

        current_year = datetime.datetime.now().year
        filter_type_wise = {}
        for key, value in calculated_data.iteritems() :
            domain_wise = {}
            compliance_list = []
            for k, v in value.iteritems() :
                dict = {}
                year = current_year
                inprogress = v[0]
                complied = v[1]
                delayed = v[2]
                not_complied = v[3]
                if len(compliance_list) == 0 :
                    compliance_count = core.NumberOfCompliances(
                        str(year), complied,
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
            chart = dashboard.ChartDataMap(k, v)
            final_result_list.append(chart)
        return final_result_list

    def frame_compliance_status_yearwise_count(self, inprogress, complied, delayed, not_complied, filter_type_ids, domain_ids, client_id):
        year_info = self.get_client_domain_configuration(client_id)
        calculated_data = {}
        calculated_data = self.calculate_year_wise_count(calculated_data, year_info, inprogress, "inprogress", filter_type_ids, domain_ids)
        calculated_data = self.calculate_year_wise_count(calculated_data, year_info, complied, "complied", filter_type_ids, domain_ids)
        calculated_data = self.calculate_year_wise_count(calculated_data, year_info, delayed, "delayed", filter_type_ids, domain_ids)
        calculated_data = self.calculate_year_wise_count(calculated_data, year_info, not_complied, "not_complied", filter_type_ids, domain_ids)

        # Sum compliance for filter_type wise
        filter_type_wise_list = []
        filter_type_wise = {}
        current_year = datetime.datetime.now().year

        for filter_type, value in calculated_data.iteritems():
            domain_wise = {}
            for key, val in value.iteritems():
                compliance_list = []
                for k , v in val.iteritems():
                    dict = {}
                    year =  k
                    inprogress = v[0]
                    complied = v[1]
                    delayed = v[2]
                    not_complied = v[3]
                    compliance_count = core.NumberOfCompliances(
                        str(year), complied,
                        delayed, inprogress, not_complied
                    )
                    compliance_list.append(compliance_count)
                domain_wise[key] = compliance_list
            filter_type_wise[filter_type] = domain_wise
        final_result_list = []
        for k, v in filter_type_wise.items():
            chart = dashboard.ChartDataMap(k, v)
            final_result_list.append(chart)
        return final_result_list

    def get_compliance_status_chart(self, request, session_user, client_id):
        result = self.get_status_wise_compliances_count(request, client_id)
        return dashboard.GetComplianceStatusChartSuccess(result)

    def compliance_details_query(self, domain_ids, date_qry, status_qry, filter_type_qry, client_id) :
        query = "SELECT \
            T1.compliance_history_id, T1.unit_id,\
            T1.compliance_id, T1.start_date, \
            T1.due_date, T1.completion_date, \
            T1.completed_by,\
            T4.compliance_task, T4.document_name, \
            T4.compliance_description, T4.statutory_mapping, \
            unit_name, division_name, legal_entity_name,\
            business_group_name, country_name, employee_name,\
            T5.unit_code, T5.address, T5.geography, T5.postal_code,\
            T5.industry_name, T3.country_id, \
            T3.domain_id, \
            SUBSTRING_INDEX(T1.due_date, '-', 1) as year, \
            SUBSTRING_INDEX(SUBSTRING_INDEX(T1.due_date , '-', -2 ),'-',1) as month  \
            FROM tbl_compliance_history T1 \
            INNER JOIN tbl_client_compliances T2 \
            ON T1.compliance_id = T2.compliance_id \
            INNER JOIN tbl_client_statutories T3 \
            ON T2.client_statutory_id = T3.client_statutory_id \
            AND T1.unit_id = T3.unit_id \
            INNER JOIN tbl_compliances T4\
            ON T1.compliance_id = T4.compliance_id \
            INNER JOIN tbl_units T5 \
            ON T1.unit_id = T5.unit_id \
            INNER JOIN tbl_divisions T6 \
            ON T5.division_id = T6.division_id \
            INNER JOIN tbl_legal_entities T7 \
            ON T5.legal_entity_id = T7.legal_entity_id \
            INNER JOIN tbl_business_groups T8 \
            ON T5.business_group_id = T8.business_group_id \
            INNER JOIN tbl_countries T9 \
            ON T3.country_id = T9.country_id \
            INNER JOIN tbl_users T10 \
            ON T1.completed_by = T10.user_id \
            WHERE \
            T3.domain_id IN %s  \
            %s \
            %s \
            %s \
            ORDER BY T1.due_date desc" % (
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
        to_date= request.to_date
        year = request.year
        filter_type = request.filter_type
        filter_id = request.filter_id
        compliance_status = request.compliance_status

        status_qry = ""
        if compliance_status == "Inprogress" :
            status_qry = " AND T1.due_date > CURDATE() \
                    AND T1.approve_status is NULL"

        elif compliance_status == "Complied" :
            status_qry = " AND T1.due_date >= T1.completion_date \
                AND T1.approve_status = 1"

        elif compliance_status == "DelayedCompliance" :
            status_qry = " AND T1.due_date < T1.completion_date \
                AND T1.approve_status = 1"

        elif compliance_status == "NotComplied" :
            status_qry = " AND T1.due_date < CURDATE() \
                AND T1.approve_status is NULL "

        if filter_type ==  "Group" :
            filter_type_qry = "AND T3.country_id = %s" % (filter_id)

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

        result = self.compliance_details_query(domain_ids, date_qry, status_qry, filter_type_qry, client_id)
        year_info = self.get_client_domain_configuration(client_id)
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
                    if (saved_year == years_list[0] and
                        saved_month not in [x for x in range(month_from, 12+1)]
                    ) :
                        continue
                    elif (saved_year == years_list[1] and
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
                ageing = abs((due_date - current_date).days)
            elif compliance_status == "Complied" :
                ageing = 0
            elif compliance_status == "NotComplied" :
                ageing = abs((current_date - due_date).days)
            elif compliance_status == "DelayedCompliance" :
                ageing = abs((completion_date - due_date).days)

            status = core.COMPLIANCE_STATUS(compliance_status)
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
                    r["division_name"], r["unit_name"], address,
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

#
# Escalation chart
#
    def get_escalation_chart(self, request, session_user, client_id):
        country_ids = request.country_ids
        domain_ids = request.domain_ids
        filter_type = request.filter_type
        filter_id = request.filter_id
        if filter_id is None :
            filter_ids = country_ids
        elif type(filter_id) is int :
            filter_ids = [filter_id]

        delayed_qry = " AND T1.due_date < T1.completion_date \
                AND T1.approve_status = 1"

        not_complied_qry = " AND T1.due_date < CURDATE() \
                AND T1.approve_status is NULL "

        if filter_type ==  "Group" :
            group_by_name = "T4.country_id"
            filter_type_ids = ""
            filter_ids = country_ids

        elif filter_type == "BusinessGroup" :
            group_by_name = "T4.business_group_id"
            filter_type_ids = "AND T4.business_group_id = %s" % (filter_id)

        elif filter_type == "LegalEntity" :
            group_by_name = "T4.legal_entity_id"
            filter_type_ids = "AND T4.legal_entity_id = %s" % (filter_id)

        elif filter_type == "Division" :
            group_by_name = "T4.division_id"
            filter_type_ids = "AND T4.division_id = %s" % (filter_id)

        elif filter_type == "Unit":
            group_by_name = "T4.unit_id"
            filter_type_ids = "AND T4.unit_id = %s" % (filter_id)

        chart_type = "Escalation"
        delayed = self.get_compliance_status(
                group_by_name, delayed_qry, filter_type_ids, client_id,
                request, chart_type
            )
        not_complied = self.get_compliance_status(
                group_by_name, not_complied_qry, filter_type_ids, client_id,
                request, chart_type
            )


        year_info = self.get_client_domain_configuration(client_id)
        calculated_data = {}
        calculated_data = self.calculate_year_wise_count(calculated_data, year_info, delayed, "delayed", filter_ids, domain_ids)
        calculated_data = self.calculate_year_wise_count(calculated_data, year_info, not_complied, "not_complied", filter_ids, domain_ids)

        # Sum compliance for filter_type wise
        filter_type_wise_list = []
        filter_type_wise = {}
        current_year = datetime.datetime.now().year

        for filter_type, value in calculated_data.iteritems():
            domain_wise = {}
            for key, val in value.iteritems():
                compliance_list = []
                for k , v in val.iteritems():
                    dict = {}
                    year =  k
                    inprogress = 0
                    complied = 0
                    delayed = v[2]
                    not_complied = v[3]
                    compliance_count = core.NumberOfCompliances(
                        str(year), complied,
                        delayed, inprogress, not_complied
                    )
                    compliance_list.append(compliance_count)
                domain_wise[key] = compliance_list
            filter_type_wise[filter_type] = domain_wise
        final_result_list = []
        for k, v in filter_type_wise.items():
            chart = dashboard.ChartDataMap(k, v)
            final_result_list.append(chart)

        return dashboard.GetEscalationsChartSuccess(final_result_list)

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

        if filter_type ==  "Group" :
            filter_type_qry = "AND T3.country_id IN %s" % (str(tuple(filter_ids)))

        elif filter_type == "BusinessGroup" :
            filter_type_qry = "AND T5.business_group_id IN %s" % (str(tuple(filter_ids)))

        elif filter_type == "LegalEntity" :
            filter_type_qry = "AND T5.legal_entity_id IN %s" % (str(tuple(filter_ids)))

        elif filter_type == "Division" :
            filter_type_qry = "AND T5.division_id IN %s" % (str(tuple(filter_ids)))

        elif filter_type == "Unit":
            filter_type_qry = "AND T5.unit_id IN %s" % (str(tuple(filter_ids)))

        date_qry = ""

        year_info = self.get_client_domain_configuration(client_id)

        delayed_details = self.compliance_details_query(
            domain_ids, date_qry, delayed_status_qry,
            filter_type_qry, client_id
        )

        delayed_details_list = self.return_compliance_details_drill_down(
            year_info, "DelayedCompliance", year,
            delayed_details, client_id
        )

        not_complied_details = self.compliance_details_query(
            domain_ids, date_qry, not_complied_status_qry,
            filter_type_qry, client_id
        )

        not_complied_details_list = self.return_compliance_details_drill_down(
            year_info, "NotComplied", year,
            not_complied_details, client_id
        )

        return [delayed_details_list.values(), not_complied_details_list.values()]

#
# Not Complied chart
#

    def get_not_complied_chart(self, request, session_user, client_id):
        country_ids = request.country_ids
        domain_ids = request.domain_ids
        filter_type = request.filter_type
        filter_id = request.filter_id
        if filter_id is None :
            filter_ids = country_ids
        elif type(filter_id) is int :
            filter_ids = [filter_id]

        if filter_type ==  "Group" :
            group_by_name = "T4.country_id"
            filter_type_ids = ""
            filter_ids = country_ids

        elif filter_type == "BusinessGroup" :
            group_by_name = "T4.business_group_id"
            filter_type_ids = "AND T4.business_group_id = %s" % (filter_id)

        elif filter_type == "LegalEntity" :
            group_by_name = "T4.legal_entity_id"
            filter_type_ids = "AND T4.legal_entity_id = %s" % (filter_id)

        elif filter_type == "Division" :
            group_by_name = "T4.division_id"
            filter_type_ids = "AND T4.division_id = %s" % (filter_id)

        elif filter_type == "Unit":
            group_by_name = "T4.unit_id"
            filter_type_ids = "AND T4.unit_id = %s" % (filter_id)

        chart_type = "Not Complied"
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
        filter_type = request.filter_type
        filter_ids = request.filter_ids
        not_complied_type = request.not_complied_type
        year = request.year

        not_complied_status_qry = " AND T1.due_date < CURDATE() \
            AND T1.approve_status is NULL  OR T1.approve_status != 1"

        if len(filter_ids) == 1:
            filter_ids.append(0)

        if filter_type ==  "Group" :
            filter_type_qry = "AND T3.country_id IN %s" % (str(tuple(filter_ids)))

        elif filter_type == "BusinessGroup" :
            filter_type_qry = "AND T5.business_group_id IN %s" % (str(tuple(filter_ids)))

        elif filter_type == "LegalEntity" :
            filter_type_qry = "AND T5.legal_entity_id IN %s" % (str(tuple(filter_ids)))

        elif filter_type == "Division" :
            filter_type_qry = "AND T5.division_id IN %s" % (str(tuple(filter_ids)))

        elif filter_type == "Unit":
            filter_type_qry = "AND T5.unit_id IN %s" % (str(tuple(filter_ids)))

        date_qry = ""

        year_info = self.get_client_domain_configuration(client_id)

        not_complied_details = self.compliance_details_query(
            domain_ids, date_qry, not_complied_status_qry,
            filter_type_qry, client_id
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

        not_complied_details_list = self.return_compliance_details_drill_down(
            year_info, "NotComplied", year,
            not_complied_details_filtered, client_id
        )

        return not_complied_details_list


    # unitwise compliance report
    def get_unitwise_compliance_report(self, country_id, domain_id, business_group_id, legal_entity_id, division_id, unit_id, user_id, client_id, session_user) :
        if unit_id is None :
            unit_ids = self.get_user_unit_ids(session_user, client_id)
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
                compliance_rows = self.select_all(query, client_id)

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
        client_id, session_user
    ) :

        if unit_id is None :
            unit_ids = self.get_user_unit_ids(session_user, client_id)
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
                compliance_rows = self.select_all(query, client_id)

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
        domain_ids = request.domain_ids
        filter_type = request.filter_type
        filter_id = request.filter_id

        if filter_type == "Group" :
            # filter_type_qry = "AND T3.country_id
            # IN %s" % (str(tuple(filter_ids)))
            filter_type_qry = ""

        elif filter_type == "BusinessGroup" :
            filter_type_qry = "AND T3.business_group_id = %s" % (filter_id)

        elif filter_type == "LegalEntity" :
            filter_type_qry = "AND T3.legal_entity_id = %s" % (filter_id)

        elif filter_type == "Division" :
            filter_type_qry = "AND T3.division_id = %s" % (filter_id)

        elif filter_type == "Unit":
            filter_type_qry = "AND T3.unit_id = %s" % (filter_id)

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
        query = "SELECT T1.compliance_id, T2.unit_id,\
            T4.frequency_id, T4.repeat_type_id, T4.duration_type_id,\
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
            INNER JOIN tbl_compliance_frequency T5\
            ON T4.frequency_id = T5.frequency_id \
            INNER JOIN tbl_divisions T6 \
            ON T3.division_id = T6.division_id \
            INNER JOIN tbl_legal_entities T7 \
            ON T3.legal_entity_id = T7.legal_entity_id \
            INNER JOIN tbl_business_groups T8 \
            ON T3.business_group_id = T8.business_group_id \
            INNER JOIN tbl_countries T9 \
            ON T3.country_id = T9.country_id \
            WHERE T2.country_id IN %s \
            AND T2.domain_id IN %s \
            %s %s"

        country_ids = request.country_ids
        domain_ids = request.domain_ids
        filter_type = request.filter_type
        filter_id = request.filter_id
        applicability = request.applicability_status

        if filter_type == "Group" :
            # filter_type_qry = "AND T3.country_id
            # IN %s" % (str(tuple(filter_ids)))
            filter_type_qry = ""

        elif filter_type == "BusinessGroup" :
            filter_type_qry = "AND T3.business_group_id = %s" % (filter_id)

        elif filter_type == "LegalEntity" :
            filter_type_qry = "AND T3.legal_entity_id = %s" % (filter_id)

        elif filter_type == "Division" :
            filter_type_qry = "AND T3.division_id = %s" % (filter_id)

        elif filter_type == "Unit":
            filter_type_qry = "AND T3.unit_id = %s" % (filter_id)

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
            "compliance_id", "unit_id",
            "frequency_id", "repeat_type_id", "duration_type_id",
            "statutory_mapping", "statutory_provision", "compliance_task",
            "compliance_description", "document_name", "format_file",
            "format_file_size", "penal_consequences", "statutory_dates",
            "repeats_every", "duration", "is_active"
        ]
        result = self.convert_to_dict(rows, columns)

        level_1_wise_compliance = {}

        for r in result :
            unit_id = r["unit_id"]
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

            format_file = d["format_file"]
            format_file_size = d["format_file_size"]
            file_list = []
            download_file_list = []
            if format_file :
                file_info = core.FileList(
                    format_file_size, format_file, None
                )
                file_list.append(file_info)
                file_name = format_file.split('-')[0]
                file_download = "%s/%s" % (
                    FORMAT_DOWNLOAD_URL, file_name
                )
                download_file_list.append(
                        file_download
                    )
            else :
                file_list = None
                download_file_list = None

            compliance = core.Compliance(
                int(r["compliance_id"]), r["statutory_provision"],
                r["compliance_task"], r["compliance_description"],
                r["document_name"], file_list, r["penal_consequences"],
                int(r["frequency_id"]), date_list, r["repeat_type_id"],
                r["repeats_every"], r["duration_type_id"],
                r["duration"], bool(r["is_active"]), download_file_list
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
                compliance_list = compliance_dict[unit_id]
                compliance_list.append(compliance)

                compliance_dict[unit_id] = compliance_list
                level_1_wise_data.compliances = compliance_dict

            level_1_wise_compliance[level_1] = level_1_wise_data

        return level_1_wise_compliance.values()

#
#   Compliance Approval
#
    def approveCompliance(self, compliance_history_id, remarks, next_due_date, client_id):
        columns = ["approve_status", "approved_on", "remarks"]
        condition = "compliance_history_id = '%d'" % compliance_history_id
        values = [1, self.get_date_time(), remarks]
        self.update(self.tblComplianceHistory, columns, values, condition, client_id)

        columns = "unit_id, compliance_id"
        rows = self.get_data(
            self.tblComplianceHistory, columns, condition
        )

        columns = ["due_date"]
        condition = " unit_id = '%d' and compliance_id = '%d'" %(
            rows[0][0], rows[0][1])
        values = [self.string_to_datetime(next_due_date)]
        self.update(self.tblAssignedCompliances, columns, values, condition, client_id)

    def rejectComplianceApproval(self, compliance_history_id, remarks,  next_due_date, client_id):
        columns = ["approve_status", "remarks", "completion_date", "completed_on"]
        condition = "compliance_history_id = '%d'" % compliance_history_id
        values = [0, remarks, None, None]
        self.update(self.tblComplianceHistory, columns, values, condition, client_id)

    def concurCompliance(self, compliance_history_id, remarks, next_due_date, client_id):
        columns = ["concurrence_status", "concurred_on", "remarks" ]
        condition = "compliance_history_id = '%d'" % compliance_history_id
        values = [1, self.get_date_time(), remarks]
        self.update(self.tblComplianceHistory, columns, values, condition, client_id)

    def rejectComplianceConcurrence(self, compliance_history_id, remarks,  next_due_date, client_id):
        columns = ["concurrence_status", "remarks", "completion_date", "completed_on"]
        condition = "compliance_history_id = '%d'" % compliance_history_id
        values = [0,  remarks, None, None]
        self.update(self.tblComplianceHistory, columns, values, condition, client_id)


    def get_client_level_1_statutoy(self, user_id, client_id) :
        query = "SELECT (case when (LEFT(statutory_mapping,INSTR(statutory_mapping,'>>')-1) = '') \
                THEN \
                statutory_mapping \
                ELSE \
                LEFT (statutory_mapping,INSTR(statutory_mapping,'>>')-1) \
                END ) as statutory \
                FROM tbl_compliances GROUP BY statutory"
        rows = self.select_all(query, client_id)
        columns = ["statutory"]
        result = self.convert_to_dict(rows, columns)
        return self.return_client_level_1_statutories(result)

    def return_client_level_1_statutories(self, data) :
        results = []
        for d in data :
            results.append(core.ClientLevelOneStatutory(
                d["statutory"]
            ))
        return results

    def get_client_compliances(self, user_id, client_id) :
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
        condition = " service_provider_id = '%d' and is_service_provider = 1"% service_provider_id
        rows = self.get_data(self.tblUsers, columns, condition, client_id)
        return rows[0][0]

    def get_service_provider_user_unit_ids(self, user_ids, client_id):
        columns = "group_concat(unit_id)"
        condition = " user_id in (%s)"% user_ids
        rows = self.get_data(self.tblUserUnits, columns, condition, client_id)
        return rows[0][0]

    def get_serviceproviderwise_compliance_report(self, country_id, domain_id, statutory_id, unit_id, service_provider_id, client_id, session_user) :

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
                unit_name = "%s - %s "% (unit[1], unit[2])
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
                    if(validity_date != None):
                        validity_date = self.datetime_to_string(compliance[3])

                    compliances_list.append(clientreport.ComplianceUnit(compliance_name, unit_address,
                        compliance_frequency, description, statutory_date,
                        due_date, validity_date))
                unit_wise_compliances[unit_name] = compliances_list
            service_provider_wise_compliances_list.append(clientreport.ServiceProviderCompliance(
                service_provider_name, address, contract_from, contract_to, contact_person, contact_no,
                unit_wise_compliances))
        return service_provider_wise_compliances_list

    def get_compliance_details_report(self, country_id, domain_id, statutory_id, unit_id, compliance_id, assignee_id, from_date, to_date, compliance_status, client_id,session_user) :

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

            start_date = self.string_to_datetime('01-'+self.string_months[period_from]+'-'+ str(year_from))
            end_date = self.string_to_datetime('31-'+self.string_months[period_to]+'-'+ str(year_to))

        else :
            start_date = self.string_to_datetime(from_date)
            end_date = self.string_to_datetime(to_date)


        unit_columns = "unit_id, unit_code, unit_name, address"
        detail_condition = "country_id = '%d' and unit_id in (%s) "% (country_id, unit_ids)
        unit_rows = self.get_data(self.tblUnits, unit_columns, detail_condition)

        unit_wise_compliances = []
        for unit in unit_rows:
            unit_id = unit[0]
            unit_name = "%s - %s "% (unit[1], unit[2])
            unit_address = unit[3]

            query = "SELECT c.compliance_task, c.compliance_description, ch.validity_date, ch.due_date, \
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

                documents = compliance[5]
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
    def get_client_statutory_ids_and_unit_ids_for_trend_chart(self, country_id,
        domain_id, client_id, filter_id = None, filter_type = None):
        columns = "group_concat(client_statutory_id), group_concat(unit_id)"
        condition = "country_id= '%d' and domain_id = '%d'" % (country_id, domain_id)
        condition += " and unit_id in (select unit_id from  tbl_units where "
        if filter_type != None:
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
        client_statutoy_ids = result[0][0]
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
        columns = "group_concat(compliance_history_id)"
        condition = "compliance_id in " +\
                    "(select group_concat(compliance_id) from "+\
                    "tbl_client_compliances where client_statutory_id "+\
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
            year_wise_count = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
            for domain_wise_timeline in domain_wise_timelines:
                domain_id = domain_wise_timeline[0]
                start_end_dates = domain_wise_timeline[1]
                for index, dates in enumerate(start_end_dates):
                    columns = "count(*) as total, sum(case when approve_status = 1 then 1 "+\
                        "else 0 end) as complied"
                    condition = "due_date between '{}' and '{}'".format(
                        dates["start_date"], dates["end_date"]
                    )
                    compliance_history_ids = self.get_compliance_history_ids_for_trend_chart(
                        country_id, domain_id, client_id)
                    condition += " and compliance_history_id in (%s)"% (compliance_history_ids[0])
                    rows = self.get_data(
                            self.tblComplianceHistory,
                            columns, condition
                        )
                    if len(rows) > 0:
                        row = rows[0]
                        total_compliances = row[0]
                        complied_compliances = row[1] if row[1] != None else 0
                        year_wise_count[index][0] += total_compliances if total_compliances != None else 0
                        year_wise_count[index][1] += complied_compliances if complied_compliances != None else 0
            compliance_chart_data = []
            for index, count_of_year in enumerate(year_wise_count):
                compliance_chart_data.append(
                    dashboard.CompliedMap(year = years[index],
                    total_compliances = int(count_of_year[0]),
                    complied_compliances_count = int(count_of_year[1])))
            chart_data.append(dashboard.TrendData(filter_id = country_id,
                complied_compliance= compliance_chart_data))
        return years,chart_data

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

        unit_ids = rows[0][0] if rows[0][0] != None else []
        drill_down_data = []
        for unit_id in unit_ids:
            # Getting Unit details
            unit_detail_columns = "tu.country_id, domain_ids, business_group_id, legal_entity_id,"+\
            " division_id, unit_code, unit_name, address, group_concat(tcs.client_statutory_id)"
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
                drill_down_data.append(
                    dashboard.TrendDrillDownData(
                            business_group_id,
                            legal_entity_id, division_id,
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
                        columns = "count(*) as total, sum(case when approve_status is null then 1 "+\
                            "else 0 end) as complied"
                        condition = "due_date between '{}' and '{}'".format(
                            dates["start_date"], dates["end_date"]
                        )
                        compliance_history_ids = self.get_compliance_history_ids_for_trend_chart(
                            country_id, domain_id, client_id, filter_id, filter_type)
                        condition += " and compliance_history_id in (%s)" % compliance_history_ids[0]
                        condition += " and unit_id in (%s)" % compliance_history_ids[2]
                        rows = self.get_data(
                            self.tblComplianceHistory, columns,
                            condition
                        )
                        if len(rows) > 0:
                            row = rows[0]
                            total_compliances =int(row[0])
                            complied_compliances = int(row[1]) if row[1] != None else 0
                            year_wise_count[0][0] += total_compliances if total_compliances != None else 0
                            year_wise_count[0][1] += complied_compliances if complied_compliances != None else 0
            compliance_chart_data = []
            for index, count_of_year in enumerate(year_wise_count):
                compliance_chart_data.append(
                    dashboard.CompliedMap(year = years[index],
                    total_compliances = int(count_of_year[0]),
                    complied_compliances_count = int(count_of_year[1])))
            chart_data.append(dashboard.TrendData(filter_id = filter_id,
                complied_compliance= compliance_chart_data))
        return years,chart_data

    def get_last_7_years(self):
        seven_years_list = []
        end_year = datetime.datetime.now().year - 1
        start_year = end_year - 5
        iter_value = start_year
        while iter_value <= end_year:
            seven_years_list.append(iter_value)
            iter_value += 1
        return seven_years_list

    def get_country_domain_timelines(self,country_ids, domain_ids, years, client_id):
        country_wise_timelines = []
        for country_id in country_ids:
            domain_wise_timeline = []
            for domain_id in domain_ids:
                columns = "period_from, period_to"
                condition = "country_id = '{}' and domain_id = '{}'".format(
                    country_id, domain_id)
                rows= self.get_data(
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
                            self.string_months[period_from],start_year
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
        columns = "two_levels_of_approval, assignee_reminder, "+\
        "escalation_reminder_in_advance, escalation_reminder,"+\
        "contract_from, contract_to, no_of_user_licence, "+\
        "total_disk_space, total_disk_space_used"
        condition = "1"
        rows = self.get_data(
            self.tblClientSettings, columns, condition
        )
        if len(rows) > 0:
            row = rows[0]
            return row
        else:
            return None

    def get_licence_holder_details(self, client_id):
        columns = "tcu.user_id, tcu.email_id, tcu.employee_name, tcu.employee_code,"+\
        " tcu.contact_no, tcu.is_admin, tu.unit_code, tu.unit_name, tu.address,"+\
        " tcu.is_active"
        tables = [self.tblUsers, self.tblUnits]
        aliases = ["tcu", "tu"]
        join_type = "left join"
        join_conditions = ["tcu.seating_unit_id = tu.unit_id"]
        where_condition = "1"
        return self.get_data_from_multiple_tables(
            columns, tables, aliases,
            join_type, join_conditions,
            where_condition
        )

    def get_profile(self, contract_from, contract_to, no_of_user_licence,
        total_disk_space, total_disk_space_used, client_id):
        contract_from = self.datetime_to_string(contract_from)
        contract_to = self.datetime_to_string(contract_to)
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
                unit_name = "-"
            else:
                unit_name =  "%s - %s" % (row[6], row[7])
            user_id = row[0]
            email_id= row[1]
            contact_no = row[4]
            is_admin= row[5]
            address= row[8]
            is_active = row[9]
            licence_holders.append(
                clientadminsettings.LICENCE_HOLDER(
                user_id, employee_name, email_id, contact_no,
                unit_name, address
            ))
        remaining_licence = (no_of_user_licence) - len(licence_holder_rows)
        profile_detail = clientadminsettings.PROFILE_DETAIL(contract_from,
            contract_to, no_of_user_licence, remaining_licence,licence_holders,
            total_disk_space/1000000000, total_disk_space_used/1000000000, )
        return profile_detail

    def updateSettings(self, is_two_levels_of_approval, assignee_reminder_days,
        escalation_reminder_In_advance_days, escalation_reminder_days, client_id):
        columns = ["two_levels_of_approval", "assignee_reminder",
        "escalation_reminder_in_advance", "escalation_reminder"]
        is_two_levels_of_approval = 1 if is_two_levels_of_approval == True else 0
        values = [is_two_levels_of_approval, assignee_reminder_days,
        escalation_reminder_In_advance_days, escalation_reminder_days]
        condition = "1"
        self.update(self.tblClientSettings, columns, values, condition, client_id)

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
        print "notification_rows:{}".format(notification_rows)
        notifications = []
        for notification in notification_rows:
            print "notification:{}".format(notification)
            notification_id = notification[0]
            read_status = bool(notification[1])
            # Getting notification details
            columns = "notification_id, notification_text, updated_on, extra_details, "+\
            "nl.statutory_provision, unit_code, unit_name, address, assignee, "+\
            "concurrence_person, approval_person, nl.compliance_id, "+\
            " compliance_task, document_name, compliance_description"
            tables = [self.tblNotificationsLog, self.tblUnits, self.tblCompliances]
            aliases = ["nl", "u", "c"]
            join_conditions = [
                "nl.unit_id = u.unit_id",
                "nl.compliance_id = c.compliance_id"
            ]
            join_type = " left join"
            where_condition = "notification_id = '%d'" % notification_id
            where_condition += " and notification_type_id = '%d'"% notification_type_id
            notification_detail_row = self.get_data_from_multiple_tables(
                columns, tables, aliases, join_type,
                join_conditions, where_condition
            )
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
            unit_name = "%s - %s" % (notification_detail[5],
                notification_detail[6])
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
            compliance_name = "%s - %s"%(notification_detail[13], notification_detail[12])
            compliance_description = notification_detail[14]

            notifications.append(
                dashboard.Notification(
                    notification_id, read_status, notification_text, extra_details,
                    updated_on, level_1_statutory, unit_name, unit_address, assignee,
                    concurrence_person, approval_person, compliance_name,
                    compliance_description, due_date, delayed_days
                )
            )
        return notifications


    def get_user_contact_details_by_id(self, user_id, client_id):
        columns = "employee_code, employee_name, contact_no, email_id"
        condition = "user_id = '%d'" % user_id
        rows = self.get_data(self.tblUsers, columns, condition)
        employee_name_with_contact_details = "%s - %s, (%s, %s)"%(
            rows[0][0],
            rows[0][1],
            rows[0][2],
            rows[0][3]
        )
        return employee_name_with_contact_details

    def update_notification_status(self, notification_id, has_read, session_user, client_id):
        columns = ["read_status"]
        values = [1 if has_read == True else 0]
        condition = "notification_id = '%d' and user_id='%d'"% (
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

        upcoming = "SELECT distinct T1.unit_id, \
            T1.compliance_id, T1.statutory_dates, T1.assignee, \
            T1.due_date, T1.validity_date, \
            T2.compliance_task, T2.document_name,\
            T2.compliance_description, T2.statutory_mapping,\
             T8.unit_name, T8.unit_code, T8.address, T8.postal_code,\
            frequency, NULL\
            FROM tbl_assigned_compliances T1 \
            INNER JOIN tbl_compliances T2 \
            ON T1.compliance_id = T2.compliance_id \
            INNER JOIN tbl_compliance_frequency T3 \
            ON T2.frequency_id = T3.frequency_id \
            INNER JOIN tbl_client_statutories T4 \
            ON T1.unit_id = T4.unit_id \
            AND T1.country_id = T4.country_id \
            INNER JOIN tbl_user_countries T5 \
            ON T1.country_id = T5.country_id \
            INNER JOIN tbl_user_domains T6 \
            ON T4.domain_id = T6.domain_id  \
            AND T5.user_id = T6.user_id \
            INNER JOIN tbl_users T7 \
            ON T6.user_id = T7.user_id \
            INNER JOIN tbl_units T8 \
            ON T1.unit_id = T8.unit_id \
            WHERE T1.due_date > CURDATE() \
            AND T1.is_active = 1 \
            AND T1.compliance_id NOT IN ( \
                SELECT DISTINCT distinct TA.compliance_id \
                FROM tbl_assigned_compliances TA \
                INNER JOIN tbl_compliance_history TC \
                ON TA.compliance_id = TC.compliance_id \
                AND TA.unit_id = TC.unit_id \
                WHERE TA.due_date > CURDATE() \
                AND TA.is_active = 1 \
                AND (TA.due_date = TC.due_date \
                OR TA.due_date = TC.next_due_date ) \
                AND TC.approve_status = 1 \
            ) \
            AND T1.compliance_id NOT IN ( \
                SELECT DISTINCT distinct TA.compliance_id \
                FROM tbl_assigned_compliances TA \
                INNER JOIN tbl_compliance_history TC \
                ON TA.compliance_id = TC.compliance_id \
                AND TA.unit_id = TC.unit_id \
                WHERE \
                TA.is_active = 1 \
                AND TC.approve_status is NULL \
                OR TC.approve_status != 1\
            ) \
            AND T7.user_id like '%s'" % (user_id)

        columns = [
            "unit_id", "compliance_id", "statutory_dates",
            "assignee", "due_date", "validity_date",
            "compliance_task", "document_name",
            "compliance_description", "statutory_mapping",
            "unit_name", "unit_code", "address", "postal_code",
            "frequency", "compliance_history_id"
        ]
        rows = self.select_all(upcoming)
        result = self.convert_to_dict(rows, columns)

        ongoing = "SELECT distinct T1.unit_id, \
            T1.compliance_id, T1.statutory_dates, T1.assignee, \
            TC.due_date, TC.validity_date, \
            T2.compliance_task, T2.document_name,\
            T2.compliance_description, T2.statutory_mapping,\
            T8.unit_name, T8.unit_code, T8.address, T8.postal_code,\
            frequency, TC.compliance_history_id \
            FROM tbl_compliance_history TC \
            INNER JOIN tbl_assigned_compliances T1 \
            ON TC.compliance_id = T1.compliance_id \
            AND TC.unit_id = T1.unit_id \
            INNER JOIN tbl_compliances T2 \
            ON T1.compliance_id = T2.compliance_id \
            INNER JOIN tbl_compliance_frequency T3 \
            ON T2.frequency_id = T3.frequency_id \
            INNER JOIN tbl_client_statutories T4 \
            ON T1.unit_id = T4.unit_id \
            AND T1.country_id = T4.country_id \
            INNER JOIN tbl_user_countries T5 \
            ON T1.country_id = T5.country_id \
            INNER JOIN tbl_user_domains T6 \
            ON T4.domain_id = T6.domain_id  \
            AND T5.user_id = T6.user_id \
            INNER JOIN tbl_users T7 \
            ON T6.user_id = T7.user_id \
            INNER JOIN tbl_units T8 \
            ON T1.unit_id = T8.unit_id \
            WHERE T1.is_active = 1 \
            AND TC.approve_status is NULL \
            OR TC.approve_status != 1\
            AND T7.user_id like '%s'" % (user_id)

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
            due_date = due_date.strftime("%d-%b-%Y")
            validity_date = d["validity_date"]
            if validity_date is not None :
                validity_date = validity_date.strftime("%d-%b-%Y")
            compliance_history_id = d["compliance_history_id"]
            if compliance_history_id is not None :
                compliance_history_id = int(compliance_history_id)
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
            compliance = clienttransactions.STATUTORYWISECOMPLIANCE(
                compliance_history_id, d["compliance_id"],
                compliance_name,
                d["compliance_description"], frequency,
                date_list, due_date, validity_date
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
                    if count is None :
                        count = 1
                    else :
                        count += len(compliance_list)
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
        for c in compliances :
            unit_id = c.unit_id
            compliance_id = c.compliance_id
            due_date = c.due_date
            history_id = c.compliance_history_id

            query = " INSERT INTO tbl_reassigned_compliances_history \
                (unit_id, compliance_id, asssignee, \
                reassigned_from, reassigned_date, remarks, \
                created_by, created_on) \
                VALUES (%s, %s, %s, %s, '%s', '%s', %s, '%s') " % (
                    unit_id, compliance_id, assignee,
                    reassigned_from, reassigned_date, reassigned_reason,
                    created_by, created_on
                )
            self.execute(query)

            update_assign = "UPDATE tbl_assigned_compliances SET assignee=%s, \
                is_reassigned=1, concurrence_person=%s, approval_person=%s \
                WHERE unit_id = %s AND compliance_id = %s " % (
                    assignee, concurrence, approval,
                    unit_id, compliance_id
                )
            self.execute(update_assign)

            if history_id is not None :
                if validity_date is None:
                    validity_date = ""
                update_history = "UPDATE tbl_compliance_history SET due_date='%s', \
                    validity_date = '%s', WHERE compliance_history_id=%s " % (
                        due_date, validity_date, history_id
                    )
                self.execute(update_history)

        return clienttransactions.ReassignComplianceSuccess()

#
#   Manage Compliances / Compliances List / Upload Compliances
#
    def calculate_ageing(self, due_date):
        current_time_stamp = self.get_date_time()
        due_date = datetime.datetime(due_date.year, due_date.month, due_date.day)
        ageing = abs(current_time_stamp - due_date).days
        compliance_status = " %d days left" % ageing
        if ageing > 0:
            compliance_status = "Overdue by %d days" % ageing
        return compliance_status

    def get_current_compliances_list(self, session_user, client_id):
        columns = "compliance_history_id, start_date, due_date, " +\
            "validity_date, next_due_date, document_name, compliance_task, " + \
            "compliance_description, format_file, unit_code, unit_name," + \
            "address, domain_name, frequency"
        tables = [
            self.tblComplianceHistory, self.tblCompliances, self.tblUnits,
            self.tblClientCompliances, self.tblClientStatutories, self.tblDomains,
            self.tblComplianceFrequency
        ]
        aliases = ["ch", "c" , "u", "cc", "cs", "d", "cf"]
        join_conditions = [
            "ch.compliance_id = c.compliance_id",
            "ch.unit_id = u.unit_id", "c.compliance_id = cc.compliance_id",
            "cc.client_statutory_id = cs.client_statutory_id", "cs.domain_id = d.domain_id",
            "c.frequency_id = cf.frequency_id"
        ]
        join_type = "right join"
        where_condition = "ch.completed_by='%d'" % (
            session_user)
        where_condition += " and (ch.completed_on is Null or " + \
            "ch.concurrence_status=0 or ch.approve_status=0)"
        current_compliances_row = self.get_data_from_multiple_tables(
            columns,
            tables, aliases, join_type, join_conditions, where_condition, client_id
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
            ageing = self.calculate_ageing(compliance[2])
            compliance_status = core.COMPLIANCE_STATUS("Inprogress")
            if ageing > 0:
                compliance_status = core.COMPLIANCE_STATUS("NotComplied")
            current_compliances_list.append(core.ActiveCompliance(
                compliance_history_id=compliance[0],
                compliance_name=compliance_name,
                compliance_frequency=core.COMPLIANCE_FREQUENCY(compliance[13]),
                domain_name=compliance[12],
                start_date=self.datetime_to_string(compliance[1]),
                due_date=self.datetime_to_string(compliance[2]),
                compliance_status=compliance_status,
                validity_date=None if compliance[3] == None else self.datetime_to_string(compliance[3]),
                next_due_date=self.datetime_to_string(compliance[4]),
                ageing=ageing,
                format_file_name=compliance[8].split(","),
                unit_name=unit_name, address=compliance[11],
                compliance_description=compliance[12])
            )
        return current_compliances_list

    def get_upcoming_compliances_list(self, session_user, client_id):
        columns = "due_date, document_name, compliance_task," + \
            " compliance_description, format_file, unit_code, unit_name," + \
            "  address, domain_name, ac.statutory_dates, repeats_every"
        tables = [
            self.tblAssignedCompliances, self.tblUnits,  self.tblCompliances,
            self.tblClientCompliances, self.tblClientStatutories, self.tblDomains
        ]
        aliases = ["ac", "u", "c", "cc", "cs", "d"]
        join_conditions = [
            "ac.unit_id = u.unit_id",
            "ac.compliance_id = c.compliance_id",
            "ac.compliance_id = cc.compliance_id",
            "cc.client_statutory_id = cs.client_statutory_id",
            "cs.domain_id = d.domain_id"
        ]
        join_type = "right join"
        where_condition = " assignee = '%d'" % session_user
        where_condition += " and due_Date > DATE_SUB(now(), INTERVAL 6 MONTH) "
        upcoming_compliances_rows = self.get_data_from_multiple_tables(
            columns,
            tables, aliases, join_type, join_conditions,
            where_condition, client_id
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
                compliance[9],  compliance[10]
            )

            upcoming_compliances_list.append(
                core.UpcomingCompliance(
                    compliance_name=compliance_name,
                    domain_name=compliance[8],
                    start_date=self.datetime_to_string(start_date),
                    due_date=self.datetime_to_string(compliance[0]),
                    format_file_name=compliance[4].split(","),
                    unit_name=unit_name,
                    address=compliance[7],
                    compliance_description=compliance[3]
                ))
        return upcoming_compliances_list

    def calculate_next_start_date(self, due_date, statutory_dates, repeats_every):
        statutory_dates = json.loads(statutory_dates)
        next_start_date = None
        if len(statutory_dates) > 1:
            month_of_due_date = due_date.month()
            for statutory_date in statutory_dates:
                if month_of_due_date == statutory_date["statutory_month"]:
                    next_start_date = due_date - timedelta(
                        days=statutory_date["trigger_before_days"])
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
        if from_date == None:
            from_date = '';
        else:
            from_date = self.string_to_datetime(from_date)
        if to_date == None:
            to_date = '';
        else:
            to_date = self.string_to_datetime(to_date)
        condition = "1"
        if business_group_id != None:
            condition += " AND business_group_id = '%d'" % business_group_id
        if legal_entity_id != None:
            condition += " AND legal_entity_id = '%d'" % legal_entity_id
        if division_id != None:
            condition += " AND division_id = '%d'" % division_id
        if unit_id != None:
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
            if level_1_statutory_name != None:
                conditionlevel1 = " AND statutory_provision like '%s'" %  str(level_1_statutory_name+"%")
                query = query + conditionlevel1        
            print query                
            result_rows = self.select_all(query)
            columns = ["business_group_name", "legal_entity_name", "division_name", "unit_code", "unit_name", "address",
                    "statutory_provision", "notification_text", "updated_on"]
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
                        statutory_provision = notification["statutory_provision"], 
                        unit_name = unit_name, 
                        notification_text = notification["notification_text"],
                        date_and_time = self.datetime_to_string(notification["updated_on"])
                    ))
                notifications.append(clientreport.STATUTORY_WISE_NOTIFICATIONS(
                    business_group_name, legal_entity_name, division_name, level_1_statutory_wise_notifications
                        ))
                print notifications
        return notifications

    # risk report
    def get_risk_report(self, country_id, domain_id, business_group_id, legal_entity_id, division_id, unit_id, statutory_id, statutory_status, client_id, session_user) :

        if unit_id is None :
            unit_ids = self.get_user_unit_ids(session_user, client_id)
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
            and u.division_id like '%s' GROUP BY u.business_group_id, u.legal_entity_id, u.division_id" % (
                str(business_group_id),
                str(legal_entity_id),
                str(division_id)
            )
        rows = self.select_all(q, client_id)

        level_1_statutory = []
        for row in rows:

            query = "SELECT (case when (LEFT(statutory_mapping,INSTR(statutory_mapping,'>>')-1) = '') \
                THEN \
                statutory_mapping \
                ELSE \
                LEFT (statutory_mapping,INSTR(statutory_mapping,'>>')-1) \
                END ) as statutory \
                FROM tbl_compliances GROUP BY statutory"
            statutory_rows = self.select_all(query, client_id)

            level_1_statutory_wise_units = {}

            for srow in statutory_rows:

                statutory_name = srow[0]
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
                unit_condition = detail_condition + " and country_id = '%d' and unit_id in (%s)" % (country_id, unit_ids)
                unit_rows = self.get_data(self.tblUnits, unit_columns, unit_condition)
                unit_wise_compliances = []
                for unit in unit_rows:
                    unit_id = unit[0]
                    unit_name = "%s - %s " % (unit[1], unit[2])
                    unit_address = unit[3]

                    query = "SELECT c.statutory_mapping, c.compliance_task, c.compliance_description, c.penal_consequences, \
                            cf.frequency, c.repeats_every from tbl_client_statutories cs, tbl_client_compliances cc, tbl_compliances c, \
                            tbl_assigned_compliances ac, tbl_compliance_frequency cf, tbl_compliance_history ch where \
                            ch.compliance_id = ac.compliance_id and ch.unit_id = ac.unit_id and ch.next_due_date = ac.due_date and \
                            cs.country_id = %s and cs.domain_id = %s and cs.unit_id like '%s' \
                            and cs.client_statutory_id = cc.client_statutory_id and c.compliance_id = cc.compliance_id \
                            and c.compliance_id = ac.compliance_id and ac.unit_id = cs.unit_id and cf.frequency_id = c.frequency_id \
                            and c.statutory_mapping like '%s' " % (
                            country_id, domain_id,
                            unit_id, str(statutory_name+"%")
                        )
                    compliance_rows = self.select_all(query, client_id)

                    compliances_list = []
                    for compliance in compliance_rows:
                        statutory_mapping = compliance[0]
                        compliance_name = compliance[1]
                        description = compliance[2]
                        penal_consequences = compliance[3]
                        compliance_frequency = "core.COMPLIANCE_FREQUENCY(compliance[4])"
                        repeats = "compliance[5]"

                        compliances_list.append(
                            clientreport.Level1Compliance(
                                statutory_mapping, compliance_name,
                                description, penal_consequences, compliance_frequency,
                                repeats
                            )
                        )

                    unit_wise_compliances.append(
                        clientreport.Level1Statutory(
                            unit_name, unit_address, compliances_list
                        )
                    )
                level_1_statutory_wise_units[statutory_name] = unit_wise_compliances

            level_1_statutory.append(clientreport.RiskData(
                business_group_name, legal_entity_name, division_name,
                level_1_statutory_wise_units))
        return level_1_statutory

    def update_compliances(
        self, compliance_history_id, documents, completion_date,
        validity_date, next_due_date, remarks, client_id, session_user
    ):
        current_time_stamp = self.get_date_time()
        history_columns = [
            "completion_date", "documents", "validity_date",
            "next_due_date", "remarks", "completed_on"
        ]
        history_values = [
            self.string_to_datetime(completion_date),
            ",".join(documents),
            self.string_to_datetime(validity_date),
            self.string_to_datetime(next_due_date),
            remarks,
            current_time_stamp
        ]
        history_condition = "compliance_history_id = '%d' \
            and completed_by ='%d'" % (
                compliance_history_id, session_user
            )
        return self.update(
            self.tblComplianceHistory,
            history_columns, history_values,
            history_condition
        )

    # Reassigned History Report
    def get_reassigned_history_report(self, country_id, domain_id, level_1_statutory_id, 
        unit_id, compliance_id, user_id, from_date, to_date, client_id, session_user ) :
        
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

            start_date = self.string_to_datetime('01-'+self.string_months[period_from]+'-'+ str(year_from))
            end_date = self.string_to_datetime('31-'+self.string_months[period_to]+'-'+ str(year_to))

        else :
            start_date = self.string_to_datetime(from_date)
            end_date = self.string_to_datetime(to_date)



        query = "SELECT (case when (LEFT(statutory_mapping,INSTR(statutory_mapping,'>>')-1) = '') \
            THEN \
            statutory_mapping \
            ELSE \
            LEFT (statutory_mapping,INSTR(statutory_mapping,'>>')-1) \
            END ) as statutory \
            FROM tbl_compliances GROUP BY statutory"


        statutory_rows = self.select_all(query, client_id)

        level_1_statutory_wise_units = []

        for srow in statutory_rows:
            statutoru_name = srow[0]
            unit_columns = "unit_id, unit_code, unit_name, address"
            detail_condition = "country_id = '%d' and unit_id in (%s) "% (country_id, unit_ids)
            unit_rows = self.get_data(self.tblUnits, unit_columns, detail_condition)

            unit_wise_compliances = []
            for unit in unit_rows:
                unit_id = unit[0]
                unit_name = "%s - %s "% (unit[1], unit[2])
                unit_address = unit[3]

                query = "SELECT rc.compliance_id, c.compliance_task, ch.due_date \
                        from tbl_compliances c,tbl_compliance_history ch, tbl_reassigned_compliances_history rc, \
                        tbl_units ut where \
                        ch.unit_id = %s \
                        AND ut.country_id = %s and ut.domain_ids like '%s' \
                        AND c.compliance_id = ch.compliance_id \
                        AND ch.completed_by like '%s'  AND c.statutory_mapping like '%s'  AND c.compliance_id like '%s' and rc.reassigned_date BETWEEN '%s' AND '%s' GROUP BY rc.compliance_id" % (
                        unit_id, country_id, domain_id,
                        user_id, str(level_1_statutory_id+"%"), compliance_id, start_date, end_date
                    )
                print query
                compliance_rows = self.select_all(query, client_id)

                compliances_list = []
                for compliance in compliance_rows:

                    compliance_id = compliance[0]
                    compliance_name = compliance[1]
                    due_date = self.datetime_to_string(compliance[2])

                    query = "SELECT (SELECT concat(u.employee_code, '-' ,u.employee_name ) FROM tbl_users u WHERE u.user_id = rh.assignee) AS assigneename, \
                            (SELECT concat(u.employee_code, '-' ,u.employee_name ) FROM tbl_users u WHERE u.user_id = rh.reassigned_from) AS reassignfrom, \
                            rh.reassigned_date, rh.remarks \
                            from tbl_reassigned_compliances_history rh where \
                            rh.unit_id = %s \
                            AND rh.complianceid = %s AND rh.reassigned_date BETWEEN %s AND %s \
                            ORDER BY rh.reassigned_date DESC" % (
                            unit_id, compliance_id,
                            start_date, end_date
                    )
                    history_rows = self.select_all(query, client_id)
                    history_list = []
                    for h_row in history_rows:
                        assignee = h_row[0]
                        reassignedfrom = h_row[1]
                        reassigned_date = h_row[2]
                        remarks = h_row[3]

                        history_list.append()
                        ReassignHistory
                        compliance = clientreport.ReassignHistory(
                        assignee, reassignedfrom, reassigned_date, remarks
                        )
                        history_list.append(compliance)


                    compliance = clientreport.ReassignUnitCompliance(
                        unit_name, compliances_list
                    )
                    unit_wise_compliances.append(compliance)


            unitwise = clientreport.StatutoryReassignCompliance(statutoru_name, unit_wise_compliances)
            level_1_statutory_wise_units.append(unitwise)
        return level_1_statutory_wise_units
