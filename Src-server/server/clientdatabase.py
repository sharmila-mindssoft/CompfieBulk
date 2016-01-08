from protocol import core
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
			    return self.convert_to_dict(data_list, data_columns)
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

	def verify_password(self, password, userId, client_id):
		columns = "count(*)"
		encrypted_password = self.encrypt(password)
		condition = "password='%s' and user_id='%d'" % (encrypted_password, userId)
		rows = self.get_data(self.tblUsers, columns, condition, client_id)
		if(int(rows[0][0]) <= 0):
		    return False
		else:
		    return True

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
		rows = self.get_data(self.tblBusinessGroups, columns, condition, client_id) 
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

	def return_units(self, units):
		results = []
		for unit in units :
		    results.append(core.ClientUnit(
		        unit["unit_id"], unit["division_id"], unit["legal_entity_id"],
		        unit["business_group_id"], unit["unit_code"],
		        unit["unit_name"], unit["unit_address"], bool(unit["is_active"])
		    ))
		return results

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
		return self.insert(self.tblUserGroups, columns, values_list, client_id)

	def update_user_privilege(self, user_privilege, session_user, client_id):
		columns = ["user_group_name","form_ids", "updated_on", "updated_by"]
		values =  [ user_privilege.user_group_name, ",".join(str(x) for x in user_privilege.form_ids),
		            self.get_date_time(),session_user]
		condition = "user_group_id='%d'" % user_privilege.user_group_id
		return self.update(self.tblUserGroups, columns, values, condition, client_id)

	def update_user_privilege_status(self, user_group_id, is_active, session_user, client_id):
		is_active = 0 if is_active != True else 1
		columns = ["is_active", "updated_by", "updated_on"]
		values = [is_active, session_user, self.get_date_time()]
		condition = "user_group_id='%d'" % user_group_id
		return self.update(self.tblUserGroups, columns, values, condition, client_id)

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

		return (result1 and result2 and result3 and result4)

	def update_user_status(self, user_id, is_active, session_user, client_id):
		columns = ["is_active", "updated_on", "updated_by"]
		is_active = 1 if is_active != False else 0
		values = [is_active, self.get_date_time(), session_user]
		condition = "user_id = '%d'"% user_id
		return self.update(self.tblUsers, columns, values, condition, client_id)

	def update_admin_status(self, user_id, is_admin, session_user, client_id):
		columns = ["is_admin", "updated_on" , "updated_by"]
		is_admin = 1 if is_admin != False else 0
		values = [is_admin, self.get_date_time(), session_user]
		condition = "user_id='%d'" % user_id
		return self.update(self.tblUsers, columns, values, condition, client_id)

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

	def deactivate_unit(self, unit_id, client_id):
		columns = ["is_active"]
		values = [1]
		condition = "unit_id ='%d'" % unit_id
		return self.update(self.tblUnits, columns, values, condition, client_id)

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
		return self.update(self.tblServiceProviders, columns_list, values_list, condition, client_id)

	def update_service_provider_status(self, service_provider_id,  is_active, session_user, client_id):
		columns = ["is_active", "updated_on" , "updated_by"]
		values = [is_active, self.get_date_time(), session_user]
		condition = "service_provider_id='%d'" % service_provider_id
		return self.update(self.tblServiceProviders, columns, values, condition, client_id)