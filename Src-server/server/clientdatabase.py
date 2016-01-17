from protocol import (core, general, clienttransactions)
from database import Database

__all__ = [
    "ClientDatabase"
]

class ClientDatabase(Database):
    def __init__(self):
        super(ClientDatabase, self).__init__(
            "localhost", "root", "123456", "mirror_knowledge")
        self.begin()
        self._client_db_connections = {}
        self._client_db_cursors = {}
        rows = self.get_client_db_info()
        self._client_db_connections[0] = self._connection
        self._client_db_cursors[0] = self._cursor
        for row in rows:
            host = row[0]
            client_id = row[1]
            username = row[2]
            password = row[3]
            database = row[4]
            super(
                ClientDatabase, self).__init__(
                host, username, password, database
            )
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
        print rows
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
        columns = ["user_id", "user_group_id", "email_id", "password", "employee_name", 
                "employee_code", "contact_no", "seating_unit_id", "user_level", 
                "is_admin", "is_service_provider","created_by", "created_on", 
                "updated_by", "updated_on"]
        values = [ user_id, user.user_group_id, user.email_id, self.generate_password(), user.employee_name,
                user.employee_code, user.contact_no, user.seating_unit_id, user.user_level, 
                0, user.is_service_provider, session_user,current_time_stamp,
                session_user, current_time_stamp]
        if user.is_service_provider == 1:
            columns.append("service_provider_id")
            values.append(user.service_provider_id)

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
            t1.applicable, t1.not_applicable_remarks, \
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
            "client_statutory_id", "compliance_id", "applicable",
            "not_applicable_remarks", "compliance_applicable",
            "compliance_opted", "compliance_remarks",
            "compliance_task", "document_name", "statutory_mapping",
            "statutory_provision", "compliance_description"
        ]
        results = self.convert_to_dict(rows, columns)
        statutory_wise_compliances = {}
        for r in results :
            compliance_opted = r["compliance_opted"]
            if compliance_opted is None :
                compliance_opted = bool(r["compliance_applicable"])
            if compliance_opted == "" :
                compliance_opted = True
            compliance_remarks = r["compliance_remarks"]
            if compliance_remarks == "" :
                compliance_remarks = None
            mappings = r["statutory_mapping"].split('>>')
            statutory_name = mappings[0]
            provision = "%s - %s" % (','.join(mappings[1:]), r["statutory_provision"])
            name ="%s - %s" % (r["document_name"], r["compliance_task"])
            compliance = clienttransactions.ComplianceApplicability(
                r["compliance_id"],
                name,
                r["compliance_description"],
                provision,
                bool(r["compliance_applicable"]),
                compliance_opted,
                compliance_remarks
            )

            level_1_statutories = statutory_wise_compliances.get(statutory_name)
            if level_1_statutories is None :
                level_1_statutories = clienttransactions.AssignedStatutory(
                    r["client_statutory_id"],
                    statutory_name,
                    [compliance],
                    bool(r["applicable"]),
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
            applicable_status = int(s.applicable_status)
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
                    t1.applicable=%s, \
                    t1.not_applicable_remarks='%s', \
                    t1.compliance_opted=%s, \
                    t1.compliance_remarks='%s',\
                    t1.updated_by=%s, \
                    t1.updated_on='%s' \
                    WHERE t2.unit_id = %s \
                    AND t1.client_statutory_id = %s \
                    AND t1.compliance_id = %s" % (
                        applicable_status, not_applicable_remarks,
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