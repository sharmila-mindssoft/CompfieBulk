from protocol import (core, general, clienttransactions, dashboard)
from database import Database
import json
import datetime

from types import *

__all__ = [
    "ClientDatabase"
]

class ClientDatabase(Database):
    def __init__(self):
        # super(ClientDatabase, self).__init__(
        #     "localhost", "root", "123456", "mirror_knowledge")
        super(ClientDatabase, self).__init__(
            "198.143.141.73", "root", "Root!@#123", "mirror_knowledge"
        )
        self.begin()
        self._client_db_connections = {}
        self._client_db_cursors = {}
        rows = self.get_client_db_info()
        self._client_db_connections[0] = self._connection
        self._client_db_cursors[0] = self._cursor
        for row in rows:
            print row
            print

            host = row[0]
            client_id = row[1]
            username = row[2]
            password = row[3]
            database = row[4]
            super(ClientDatabase, self).__init__(
                host, username, password, database
            )
            print "_connection success"
            self.begin()
            self._client_db_connections[int(client_id)] = self._connection
            self._client_db_cursors[int(client_id)] = self._cursor
        print self._client_db_cursors
        self.initialize_table_names()

    def execute(self, query, client_id = None) :
        cursor = None
        if client_id != None:
            cursor = self._client_db_cursors[client_id]
        else:
            cursor = self.cursor()
        assert cursor is not None
        result = cursor.execute(query)
        if client_id != None:
            self._client_db_connections[client_id].commit()
        return result

    def select_one(self, query, client_id = None) :
        cursor = None
        if client_id != None:
            cursor = self._client_db_cursors[client_id]
        else:
            cursor = self.cursor()
        assert cursor is not None
        cursor.execute(query)
        result = cursor.fetchone()
        return result

    def select_all(self, query, client_id = None) :
        cursor = None
        if client_id != None:
            cursor = self._client_db_cursors[client_id]
        else:
            cursor = self.cursor()
        assert cursor is not None
        cursor.execute(query)
        return cursor.fetchall()

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

    def verify_login(self, username, password, client_id):
        tblAdminCondition = "password='%s' and username='%s'" % (
            password, username
        )
        admin_details = self.get_data("tbl_admin", "*", tblAdminCondition, client_id)
        print admin_details

        if (len(admin_details) == 0) :
            data_columns = ["user_id", "user_group_id", "email_id", 
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
            data_list = self.select_one(query, client_id)
            if data_list is None :
                return False
            else :
                result = self.convert_to_dict(data_list, data_columns)
                result["client_id"] = client_id
                return result
        else :
            return True

    def get_user_forms(self, form_ids, client_id, is_admin):
        columns = "tf.form_id, tf.form_type_id, tft.form_type, tf.form_name, "+\
        "tf.form_url, tf.form_order, tf.parent_menu"
        tables = [self.tblForms, self.tblFormType]
        aliases = ["tf",  "tft"]
        joinConditions = ["tf.form_type_id = tft.form_type_id"]
        if is_admin != 0:
            whereCondition = " is_admin = 1 order by tf.form_order"
        else:
            whereCondition = " form_id in (%s) order by tf.form_order" % form_ids
        joinType = "left join"

        rows = self.get_data_from_multiple_tables(columns, tables, aliases, joinType, 
            joinConditions, whereCondition, client_id)
        row_columns = [
            "form_id", "form_type_id", "form_type", "form_name", "form_url", 
            "form_order", "parent_menu"
        ]
        result = self.convert_to_dict(rows, row_columns)
        return result

    def get_client_id_from_short_name(self, short_name):
        columns = "client_id"
        condition = "url_short_name = '%s'"% short_name
        rows = self.get_data("tbl_client_groups", columns, condition, 0)
        return rows[0][0]

    def verify_username(self, username, client_id):
        columns = "count(*), user_id"
        condition = "email_id='%s'" % (username)
        rows = self.get_data(self.tblUsers, columns, condition, client_id)
        count = rows[0][0]
        if count == 1:
            return rows[0][1]
        else:
            condition = "username='%s'" % username
            columns = "count(*)"
            rows = self.get_data(self.tblAdmin, columns, condition, client_id)
            count = rows[0][0]
            if count == 1:
                return 0
            else:
                return None

    def verify_password(self, password, user_id, client_id):
        columns = "count(*)"
        encrypted_password = self.encrypt(password)
        condition = "1"
        rows= None
        if user_id == 0:
            condition = "password='%s'" % (encrypted_password)  
            rows = self.get_data(self.tblAdmin, columns, condition, client_id)
        else:  
            condition = "password='%s' and user_id='%d'" % (encrypted_password, user_id)
            rows = self.get_data(self.tblUsers, columns, condition, client_id)
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
            result = self.update(self.tblUsers, columns, values, condition, client_id)
        else:
            result = self.update(self.tblAdmin, columns, values, condition, client_id)
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
        rows = self.get_data(self.tblEmailVerification, column, condition, client_id)
        count = rows[0][0]
        user_id = rows[0][1]
        if count == 1:
            return user_id
        else:
            return None

    def validate_session_token(self, client_id, session_token) :
        query = "SELECT user_id FROM tbl_user_sessions \
            WHERE session_token = '%s'" % (session_token)
        row = self.select_one(query, client_id)
        user_id = row[0]
        return user_id

    def get_forms(self, client_id):
        columns = "tf.form_id, tf.form_type_id, tft.form_type, "+\
        "tf.form_name, tf.form_url, tf.form_order, tf.parent_menu"
        tables = [self.tblForms, self.tblFormType]
        aliases = ["tf",  "tft"]
        joinConditions = ["tf.form_type_id = tft.form_type_id"]
        whereCondition = " 1 order by tf.form_order"
        joinType = "left join"
        rows = self.get_data_from_multiple_tables(columns, tables, aliases, joinType, 
            joinConditions, whereCondition, client_id)
        return rows

    def return_forms(self, client_id):
        columns = "form_id, form_name"
        forms = self.get_data(self.tblForms, columns, "1", client_id)
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
        rows = self.select_all(query, client_id)
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
        rows = self.select_all(query, client_id)
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
        if business_group_ids != None:
            condition = "business_group_id in (%s)" % business_group_ids
        print condition
        rows = self.get_data(self.tblBusinessGroups, columns, condition, client_id) 
        print rows
        columns = ["business_group_id", "business_group_name"]
        result = self.convert_to_dict(rows, columns)
        return self.return_business_groups(result)

    def return_business_groups(self, business_groups):
        results = []
        for business_group in business_groups :
            results.append(core.ClientBusinessGroup(
                business_group["business_group_id"], business_group["business_group_name"]
            ))
        return results 

    def get_legal_entities_for_user(self, legal_entity_ids, client_id):
        columns = "legal_entity_id, legal_entity_name, business_group_id"
        condition = "1"
        if legal_entity_ids != None:
            condition = "legal_entity_id in (%s)" % legal_entity_ids
        rows = self.get_data(self.tblLegalEntities, columns, condition, client_id) 
        columns = ["legal_entity_id", "legal_entity_name", "business_group_id"]
        result = self.convert_to_dict(rows, columns)
        return self.return_legal_entities(result)

    def return_legal_entities(self, legal_entities):
        results = []
        for legal_entity in legal_entities :
            results.append(core.ClientLegalEntity(
                legal_entity["legal_entity_id"], legal_entity["legal_entity_name"],
                legal_entity["business_group_id"]
            ))
        return results

    def get_divisions_for_user(self, division_ids, client_id):
        columns = "division_id, division_name, legal_entity_id, business_group_id"
        condition = "1"
        if division_ids != None:
            condition = "division_id in (%s)" % division_ids
        rows = self.get_data(self.tblDivisions, columns, condition) 
        columns = ["division_id", "division_name", "legal_entity_id", 
        "business_group_id"]
        result = self.convert_to_dict(rows, columns)
        return self.return_divisions(result)

    def return_divisions(self, divisions):
        results = []
        for division in divisions :
            division_obj = core.ClientDivision(division["division_id"], division["division_name"],
                division["legal_entity_id"],division["business_group_id"])
            results.append(division_obj)
        return results

    def get_units_for_user(self, unit_ids, client_id):
        columns = "unit_id, unit_code, unit_name, address, division_id,"+\
        " legal_entity_id, business_group_id, is_active"
        condition = "1"
        if unit_ids != None:
            condition = "unit_id in (%s)" % unit_ids
        rows = self.get_data(self.tblUnits, columns, condition, client_id) 
        columns = ["unit_id", "unit_code", "unit_name", "unit_address", "division_id", 
        "legal_entity_id", "business_group_id", "is_active"]
        result = self.convert_to_dict(rows, columns)
        return self.return_units(result)

    def get_units_for_user_grouped_by_industry(self, unit_ids, client_id):
        condition = "1"
        if unit_ids != None:
            condition = "unit_id in (%s)" % unit_ids
        industry_column = "industry_name"
        industry_condition = condition + " group by industry_name"
        industry_rows = self.get_data(self.tblUnits, industry_column, industry_condition)

        columns = "unit_id, unit_code, unit_name, address, division_id,"+\
        " legal_entity_id, business_group_id, is_active"
        industry_wise_units =[]
        for industry in industry_rows:
            industry_name = industry[0]
            units = []
            condition += " and industry_name = '%s'" % industry_name
            rows = self.get_data(self.tblUnits, columns, condition, client_id)
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
        self.execute(query, client_id)
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
        return self.is_already_exists(self.tblUserGroups, condition, client_id)

    def get_user_privilege_details_list(self, client_id):
        columns = "user_group_id, user_group_name, form_ids, is_active"
        rows = self.get_data(self.tblUserGroups, columns, "1", client_id)
        return rows

    def get_user_privileges(self, client_id):
        columns = "user_group_id, user_group_name, is_active"
        rows = self.get_data(self.tblUserGroups, columns, "1", client_id)     
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
        result = self.insert(self.tblUserGroups, columns, values_list, client_id) 

        action = "Created User Group \"%s\"" % user_privilege.user_group_name
        self.save_activity(session_user, 3, action, client_id)

        return result

    def update_user_privilege(self, user_privilege, session_user, client_id):
        columns = ["user_group_name","form_ids", "updated_on", "updated_by"]
        values =  [ user_privilege.user_group_name, ",".join(str(x) for x in user_privilege.form_ids),
                    self.get_date_time(),session_user]
        condition = "user_group_id='%d'" % user_privilege.user_group_id
        result = self.update(self.tblUserGroups, columns, values, condition, client_id) 

        action = "Updated User Group \"%s\"" % user_privilege.user_group_name
        self.save_activity(session_user, 3, action, client_id)      

        return result

    def update_user_privilege_status(self, user_group_id, is_active, session_user, client_id):
        is_active = 0 if is_active != True else 1
        columns = ["is_active", "updated_by", "updated_on"]
        values = [is_active, session_user, self.get_date_time()]
        condition = "user_group_id='%d'" % user_group_id
        result = self.update(self.tblUserGroups, columns, values, condition, client_id)

        action_column = "user_group_name"
        rows = self.get_data(self.tblUserGroups, action_column, condition, client_id)
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
        rows =  self.get_data(self.tblUsers,columns, condition, client_id)
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
        rows = self.get_data(self.tblUsers, columns, condition, client_id)
        columns = ["user_id", "employee_name", "employee_code", "is_active"]
        result = self.convert_to_dict(rows, columns)
        return self.return_users(result)

    def get_users_by_id(self, user_ids, client_id):
        columns = "user_id, employee_name, employee_code, is_active"
        condition = " user_id in (%s)" % user_ids
        rows = self.get_data(self.tblUsers, columns, condition, client_id)
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
        rows = self.get_data(self.tblUsers, action_column, condition, client_id)
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
        rows = self.get_data(self.tblUsers, action_column, condition, client_id)
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
        rows = self.get_data(self.tblUserUnits, columns, condition, client_id)
        unit_ids = rows[0][0]

        columns = "group_concat(division_id), group_concat(legal_entity_id), "+\
        "group_concat(business_group_id)"
        unit_condition = "1"
        if unit_ids != None:
            unit_condition = "unit_id in (%s)" % unit_ids
        rows = self.get_data(self.tblUnits , columns, unit_condition, client_id)

        division_ids = rows[0][0]
        legal_entity_ids = rows[0][1]
        business_group_ids = rows[0][2]
        return unit_ids, division_ids, legal_entity_ids, business_group_ids
        
    def get_user_countries(self, user_id, client_id):
        columns = "group_concat(country_id)"
        condition = " user_id = '%d'"% user_id
        rows = self.get_data( self.tblUserCountries,columns, condition, client_id)
        return rows[0][0]

    def get_user_domains(self, user_id, client_id):
        columns = "group_concat(domain_id)"
        condition = " user_id = '%d'"% user_id
        rows = self.get_data(self.tblUserDomains, columns, condition, client_id)
        return rows[0][0]

    def get_user_unit_ids(self, user_id, client_id):
        columns = "group_concat(unit_id)"
        condition = " user_id = '%d'"% user_id
        rows = self.get_data(self.tblUserUnits, columns, condition, client_id)
        return rows[0][0]

    def deactivate_unit(self, unit_id, client_id, session_user):
        columns = ["is_active"]
        values = [1]
        condition = "unit_id ='%d'" % unit_id
        result = self.update(self.tblUnits, columns, values, condition, client_id) 

        action_column = "unit_code, unit_name"
        rows = self.get_data(self.tblUnits, action_column, condition, client_id)
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
        rows = self.get_data(self.tblServiceProviders, columns, "1", client_id)
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
        rows = self.get_data(self.tblServiceProviders, columns, "1", client_id)
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
        rows = self.get_data(self.tblServiceProviders, action_column, condition, client_id)
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
            rows = self.get_data(self.tblUsers, column, condition, client_id)
            user_group_id = rows[0][0]

            column = "form_category_id"
            condition = "user_group_id = '%d'" % user_group_id
            rows = self.get_data(self.tblUserGroups, column, condition, client_id)
            form_category_id = rows[0][0]

            column = "group_concat(user_group_id)"
            condition = "form_category_id = '%d'" % form_category_id
            rows = self.get_data(self.tblUserGroups, column, condition, client_id)
            user_group_ids = rows[0][0]

            column = "group_concat(user_id)"
            condition = "user_group_id in (%s)" % user_group_ids
            rows = self.get_data(self.tblUsers, column, condition, client_id)
            user_ids = rows[0][0]
            condition = "user_id in (%s)"% user_ids
        else:
            condition = "1"
        columns = "user_id, form_id, action, created_on"
        rows = self.get_data(self.tblActivityLog, columns, condition, client_id)
        audit_trail_details = []
        for row in rows:
            user_id = row[0]
            form_id = row[1]
            action = row[2]
            date = self.datetime_to_string(row[3])
            audit_trail_details.append(general.AuditTrail(user_id, form_id, action, date))
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
        rows = self.select_all(query, client_id)
        columns = ["client_statutory_id", "geography",
            "country_id", "domain_id", "unit_id", "unit_name", 
            "business_group_name", "legal_entity_name",
            "division_name", "address", "postal_code", "unit_code",
            "country_name", 'domain_name'
        ]
        result = self.convert_to_dict(rows, columns)
        return self.return_statutory_settings(result, client_id)

    def return_compliance_for_statutory_settings(self, domain_id, client_statutory_id, client_id):
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
        rows = self.select_all(query, client_id)
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
            provision = "%s - %s" % (','.join(mappings[1:]), r["statutory_provision"])
            name ="%s - %s" % (r["document_name"], r["compliance_task"])
            compliance = clienttransactions.ComplianceApplicability(
                r["compliance_id"],
                name,
                r["compliance_description"],
                provision,
                bool(r["compliance_applicable"]),
                bool(compliance_opted),
                compliance_remarks
            )

            level_1_statutories = statutory_wise_compliances.get(statutory_name)
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
            address = "%s, %s, %s" % (d["address"], d["geography"], d["postal_code"])
            domain_id = d["domain_id"]
            client_statutory_id = d["client_statutory_id"]
            statutories = self.return_compliance_for_statutory_settings(domain_id, client_statutory_id, client_id)

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
                    domain_statutories.append(statutories.values())
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
                self.execute(query, client_id)

        return clienttransactions.UpdateStatutorySettingsSuccess()

    def get_level_1_statutory(self, client_id):
        columns = "client_statutory_id, statutory_provision"
        condition = "compliance_applicable is Null AND compliance_opted is null"
        rows = self.get_data(self.tblClientCompliances, columns, condition, client_id)
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

    def get_compliance_frequency(self, client_id):
        columns = "frequency_id, frequency"
        rows = self.get_data(self.tblComplianceFrequency, columns, "1", client_id)
        compliance_frequency = []
        for row in rows:
            compliance_frequency.append(core.ComplianceFrequency(row[0],
             core.COMPLIANCE_FREQUENCY(row[1])))
        return compliance_frequency

    def get_statutory_wise_compliances(unit_id, domain_id, level_1_statutory_id, 
        frequecy_id):
        client_statutory_columns = "group_concat(client_statutory_id)"
        client_statutory_condition = " unit_id = '%d' and domain_id = '%d' "%(unit_id, domain_id)  
        client_statutory_rows = self.get_data(self.tblClientStatutories, client_statutory_columns,
            client_statutory_condition)
        client_statutory_ids = None
        if len(client_statutory_rows) > 0: 
            client_statutory_ids = client_statutory_rows[0][0]
        else:
            print "Assign Compliances to the Unit first"
            return

        client_compliances_columns = "group_concat(compliance_id)"
        client_compliances_condition = " client_statutory_id in (%s)" % client_statutory_ids
        client_compliances_rows = self.get_data(self.tblClientCompliances, client_compliances_columns,
            client_compliances_condition)
        client_compliance_ids = None
        if len(client_compliance_rows) > 0:
            client_compliance_ids = client_compliance_rows[0][0]
        else:
            print "Assign Compliances to the Unit first"
            return

        compliance_columns = "compliance_id, compliance_task, document_name, statutory_dates"
        compliance_condition = " compliance_id in (%s) " % client_compliance_ids
        compliance_rows = self.get_data(self.tblCompliances, compliance_columns, compliance_condition)
        for compliance in compliance_rows:
            pass

    def get_compliance_approval_list(self, session_user, client_id):
        assignee_columns = "completed_by, employee_code, employee_name"
        join_type = "left join"
        tables = [self.tblComplianceHistory, self.tblUsers]
        aliases = ["tch", "tu"]
        join_condition = ["tch.completed_by = tu.user_id"]
        assignee_condition = "completion_date is not Null and approved_on is Null and "+\
        "(approved_by = '%d' or concurred_by = '%d')" % (session_user, session_user)
        assignee_rows = self.get_data_from_multiple_tables(assignee_columns, tables, 
            aliases, join_type,  join_condition, assignee_condition, client_id)
        
        approved_compliances = []
        for assignee in assignee_rows:
            query_columns = "compliance_history_id, tch.compliance_id, start_date,"+\
            " due_date, documents, completion_date, completed_on, next_due_date, "+\
            "concurred_by, remarks, datediff(due_date, completion_date ),compliance_task,"+\
            " compliance_description, tc.frequency_id, frequency, document_name"
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
                query_columns, query_tables, aliases, join_type, join_condition,
                where_condition, client_id
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

                domain_name_column = "domain_name"
                condition = " domain_id = (select domain_id from tbl_client_statutories "+\
                " where client_statutory_id = (select client_statutory_id from "+\
                " tbl_client_compliances where compliance_id ='%d'))" % compliance_id 
                domain_name_row =  self.get_data(self.tblDomains, domain_name_column, 
                    condition)
                domain_name = domain_name_row[0][0]

                action = None
                if concurred_by == session_user:
                    action = "Concur"
                else:
                    action = "Approve"

                compliances.append(clienttransactions.APPROVALCOMPLIANCE(
                    compliance_history_id, compliance_name, description, domain_name, 
                    start_date, due_date, delayed_by, frequency, documents, 
                    completion_date, completed_on, next_due_date, concurred_by, 
                    remarks, action))
            assignee_id = assignee[0]
            assignee_name = "{} - {}".format(assignee[1], assignee[2])
            approved_compliances.append(clienttransactions.APPORVALCOMPLIANCELIST(
                assignee_id, assignee_name, compliances))
        return approved_compliances

    def get_user_name_by_id(self, user_id, client_id):
        employee_name = None
        if user_id != None:
            columns = "employee_code, employee_name"
            condition = "user_id ='{}'".format(user_id)
            rows = self.get_data(self.tblUsers, columns, condition, client_id)
            if len(rows) > 0:
                employee_name = "{} - {}".format(rows[0][0], rows[0][1])
            else:
                print "inside inner else"
        else:
            print "inside outer else"
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
        rows = self.select_all(query, client_id)
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
            group_concat(distinct t3.unit_id) unit_ids \
            FROM tbl_users t1 \
            INNER JOIN tbl_user_domains t2\
            ON t1.user_id = t2.user_id \
            INNER JOIN tbl_user_units t3\
            ON t1.user_id = t3.user_id "

        if session_user > 0 :
            query = query + where_condition
        rows = self.select_all(query, client_id)
        columns = [
            "user_id", "employee_name", "employee_code",
            "seating_unit_id", "user_level",
            "domain_ids", "unit_ids"
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
                domain_ids
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

        rows = self.select_all(query, client_id)
        columns = ["compliance_id", "domain_id", "units",
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
                self.execute(query, client_id)
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

    def get_compliance_approval_status_list(self, session_user, client_id):
        columns = "compliance_status_id, compliance_status"
        condition = "1"
        rows = self.get_data(self.tblComplianceStatus, columns, condition)
        columns = columns.split(",")
        return self.return_compliance_approval_status_list(columns, rows)

    def return_compliance_approval_status_list(self, columns, compliance_status_list):
        result_compliance_status = []
        for compliance_status in compliance_status_list:
            result_compliance_status.append(core.ComplianceApprovalStatus(
                compliance_status[0], core.COMPLIANCE_APPROVAL_STATUS(compliance_status[1])))
        return result_compliance_status

#
#   Chart Api
#
    def get_compliance_status(self, group_by_name, status_type_qry, filter_type_ids, client_id, request) :
        country_ids = request.country_ids
        domain_ids = request.domain_ids
        from_date = request.from_date
        to_date = request.to_date
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
        print
        print query
        print
        rows = self.select_all(query, client_id)
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
            return  single_years
        else :
            double_years = []
            if current_month in [ int(m) for m in range(month_from, 12+1)] :
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
                AND T1.completion_date != NULL \
                AND T1.approve_status = 1"

        delayed_qry = " AND T1.due_date < T1.completion_date \
                AND T1.completion_date != NULL\
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
            filter_type_ids = filter_ids

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
        if from_date is None and to_date is None :
            return self.frame_compliance_status_count(inprogress, complied, delayed, not_complied, filter_ids, client_id)
        else :
            return self.frame_compliance_status_count(inprogress, complied, delayed, not_complied, filter_ids, client_id)

    def get_client_domain_configuration(self, client_id) :
        query = "SELECT country_id, domain_id, \
            period_from, period_to \
            FROM  tbl_client_configurations "
        rows = self.select_all(query, client_id)
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

    def calculate_year_wise_count(self, calculated_data, years_info, compliances, status, filter_ids):
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
                    
                    compliance_sum = year_wise.get(str(index))
                    
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

                    year_wise[str(index)] = compliance_sum


                country[domain_id] = year_wise
                calculated_data[filter_type] = country

        return calculated_data

    def frame_compliance_status_count(self, inprogress, complied, delayed, not_complied, filter_type_ids, client_id):
        year_info = self.get_client_domain_configuration(client_id)
        calculated_data = {}
        calculated_data = self.calculate_year_wise_count(calculated_data, year_info, inprogress, "inprogress", filter_type_ids)
        calculated_data = self.calculate_year_wise_count(calculated_data, year_info, complied, "complied", filter_type_ids)
        calculated_data = self.calculate_year_wise_count(calculated_data, year_info, delayed, "delayed", filter_type_ids)
        calculated_data = self.calculate_year_wise_count(calculated_data, year_info, not_complied, "not_complied", filter_type_ids)

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
                    year =  current_year - int(k)
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
        print "inprogress"
        inprogress = self.get_status_wise_compliances(request, client_id, 1)
        print "complied"
        complied = self.get_status_wise_compliances(request, client_id, 2)
        print "delayed"
        delayed = self.get_status_wise_compliances(request, client_id, 3)
        print "not_complied"
        not_complied = self.get_status_wise_compliances(request, client_id, 4)
        result = self.get_status_wise_compliances_count(request, client_id)
        return dashboard.GetComplianceStatusChartSuccess(result)        
