from aparajitha.server.database import Database 
from aparajitha.server.clientmodels import *
from aparajitha.misc.dates import *

def to_dict(keys, values_list):
	values_list2 = []
	for values in values_list :
		values_list2.append(dict(zip(keys, values)))
	return values_list2

class ClientDatabase(object) :
	def __init__(self, db) :
		self._db = Database(db)

	def test(self) :
		query = "SHOW TABLES;"
		print self._db.execute_and_return(query)
		return True

#
# 	Common
#
	def generate_new_id(self, form):
		tbl_name = None
		column = None
		if form == "ServiceProvider":
			tbl_name = self._db.tblServiceProviders
			column = "service_provider_id"
		elif form == "UserPrivilege":
			tbl_name = self._db.tblClientUserGroups
			column = "user_group_id"
		else:
			print "Error : Cannot generate new id for form %s" % form

		return self._db.generate_new_id(tbl_name, column)

	def is_duplicate(self, form, field, value, idValue):
		tbl_name = None
		condition = None
		if form == "ServiceProvider":
			tbl_name = self._db.tblServiceProviders
			if field == "name":
				condition = "service_provider_name ='%s' AND service_provider_id != '%d'" %(
           value, idValue)
			elif field == "contact_no":
				condition = "contact_no ='%s' AND service_provider_id != '%d'" % (
					value, idValue)
		elif form == "UserPrivilege":		
			tbl_name = self._db.tblClientUserGroups
			if field == "name":
				condition = "user_group_name ='%s' AND user_group_id != '%d'" %(value, idValue)
		elif form == "User":		
			tbl_name = self._db.tblClientUserDetails
			if field == "employee_code":
				condition = "employee_code ='%s' AND user_id != '%d'" %(value, idValue)
			elif field == "contact_no":
				condition = "contact_no ='%s' AND user_id != '%d'" %(value, idValue)
		else:
			print "Error : Duplicate Validation for form %s not exists" % form
			return False

		if tbl_name == None and condition == None:
			print "Error : Duplicate Validation for field %s in form %s not exists" %(
					field, form)
			return False
		else:
			return self._db.is_already_exists(tbl_name, condition)

	def is_id_invalid(self, form, idValue):
		tbl_name = None
		condition = None
		if form == "ServiceProvider":
			tbl_name = self._db.tblServiceProviders
			condition = "service_provider_id = '%d'" % idValue
		elif form == "UserPrivilege":
			tbl_name = self._db.tblClientUserGroups
			condition = "user_group_id = '%d'" % idValue
		elif form == "User":
			tbl_name = self._db.tblClientUserDetails
			condition = "user_id = '%d'" % idValue
		else:
			print "Error: Id Validation not exists for form %s" % form

		return not self._db.is_already_exists(tbl_name, condition)
#
# Service Provider
#
	def get_service_providers(self):
		columns = ["service_provider_id", "service_provider_name", "address", "contract_from",
                "contract_to", "contact_person", "contact_no", "is_active"]
		condition = "1"
		rows = self._db.get_data(self._db.tblServiceProviders, columns, condition)
		return rows

	def save_service_provider(self, service_provider, session_user):
		timestamp = None
		timestamp = current_timestamp()
		columns = ["service_provider_id", "service_provider_name", "address",
		        	"contract_from", "contract_to", "contact_person",
		        	"contact_no","created_on","created_by", "updated_on", "updated_by"]
		values_list = [(service_provider.service_provider_id,service_provider.service_provider_name,
			service_provider.address, service_provider.contract_from, service_provider.contract_to,
			service_provider.contact_person, service_provider.contact_no, timestamp,
			session_user, timestamp, session_user)]
		update_columns_list = ["service_provider_name", "address", "contract_from",
		 					"contract_to", "contact_person", "contact_no", 
		 					"updated_on", "updated_by"]
		return self._db.on_duplicate_key_update(self._db.tblServiceProviders, columns, 
			values_list, update_columns_list)

	def change_service_provider_status(self, service_provider_id, is_active,
		session_user):
		timestamp = current_timestamp()
		columns = ["is_active", "updated_on" , "updated_by"]
		values = [is_active, timestamp, session_user]
		condition = "service_provider_id='%d'" % service_provider_id
		return self._db.update(self._db.tblServiceProviders, 
        	columns, values, condition)

#
# User Groups
#
	def get_user_group_details(self):
		columns = ["user_group_id", "user_group_name","category",
                    "form_ids", "is_active"]
		condition = "1"
		rows = self._db.get_data(self._db.tblClientUserGroups, columns, condition)
		return rows

	def get_user_groups(self):
		columns = ["user_group_id", "user_group_name", "is_active"]
		condition = "1"
		rows = self._db.get_data(self._db.tblClientUserGroups, columns, condition)
		return rows

	def save_user_privilege(self, user_privilege, session_user):
		timestamp = current_timestamp()
		columns = ["user_group_id", "user_group_name","category", "form_ids",
		"is_active", "created_on", "created_by", "updated_on", "updated_by"]
		form_ids = ",".join(str(x) for x in user_privilege.form_ids)
		values_list =  [(user_privilege.user_group_id, user_privilege.user_group_name, user_privilege.form_type,
		 form_ids, user_privilege.is_active, timestamp,session_user,timestamp, session_user)]
		update_columns_list = ["user_group_name","category", "form_ids", "updated_on", "updated_by"]
		return self._db.on_duplicate_key_update(self._db.tblClientUserGroups, columns, values_list, update_columns_list)

	def change_user_privilege_status(self, user_group_id, is_active, session_user):
		timestamp = current_timestamp()
		columns = ["is_active", "updated_on" , "updated_by"]
		values = [is_active, timestamp, session_user]
		condition = "user_group_id='%d'" % user_group_id
		return self._db.update(self._db.tblClientUserGroups, columns, values, condition)

#
#	Users
#
	def get_user(self, user_id) :
		columns = ["user_id", "email_id", "is_active", "user_group_id",
			"employee_name", "employee_code", "contact_no", 
			"domain_ids", "country_ids", "is_admin"]
		condition = "user_id = %d" % user_id
		rows = self._db.get_data(self._db.tblClientUserDetails, columns, condition)
		result = to_dict(columns, rows)
		return result[0]

	def get_client_user_details_list(self):
		columns = ["user_id", "email_id", "user_group_id", "employee_name", "employee_code",
		"contact_no", "seating_unit_id", "user_level", "country_ids",
		"domain_ids", "unit_ids", "is_admin", "is_service_provider", "is_active"]
		condition = "1"
		rows = self._db.get_data(self._db.tblClientUserDetails, columns, condition)
		return rows

	def get_client_user_list(self):
		columns = ["user_id", "employee_name", "employee_code", "is_active"]
		condition = "1"
		rows = self._db.get_data(self._db.tblClientUserDetails, columns, condition)
		return rows

	def save_user_detail(self, user, session_user):
		timestamp = current_timestamp()
		columns = ["user_id", "email_id", "user_group_id", "employee_name", "employee_code",
                   "contact_no", "seating_unit_id", "user_level", "country_ids",
                    "domain_ids", "unit_ids", "is_admin", "is_service_provider", 
                    "created_by", "created_on", "updated_by","updated_on"]
		values_list = [ (user.user_id, user.email_id, user.user_group_id, user.employee_name,
                       	user.employee_code, user.contact_no, user.seating_unit_id, 
                        user.user_level, ",".join(str(x) for x in user.country_ids), 
                        ",".join(str(x) for x in user.domain_ids), 
                        ",".join(str(x) for x in user.unit_ids), user.is_admin,
                        user.is_service_provider, session_user,timestamp,
                        session_user, timestamp)]
		update_columns_list = [ "user_group_id", "employee_name", "employee_code",
                            "contact_no", "seating_unit_id", "user_level", "country_ids",
                            "domain_ids", "unit_ids", "is_admin", "is_service_provider",
                            "updated_on", "updated_by"]
		return self._db.on_duplicate_key_update(self._db.tblClientUserDetails, columns, 
        	values_list, update_columns_list)

	def update_user_detail(self, user,session_user):
		timestamp = current_timestamp()
		columns = ["user_group_id", "employee_name", "employee_code",
		"contact_no", "seating_unit_id", "user_level", "country_ids",
		"domain_ids", "unit_ids", "is_admin", "is_service_provider",
		"updated_by", "updated_on"]
		values_list = [ user.user_group_id, user.employee_name, user.employee_code,
						user.contact_no, user.seating_unit_id, user.user_level,
						",".join(str(x) for x in user.country_ids), 
                        ",".join(str(x) for x in user.domain_ids), 
                        ",".join(str(x) for x in user.unit_ids), user.is_admin,
                        user.is_service_provider, session_user, timestamp]
		condition = "user_id='%d'" % user.user_id
		return self._db.update(self._db.tblClientUserDetails, columns, values_list,
			condition)

	def change_user_detail_status(self, user_id, is_active, session_user):
		columns = ["is_active", "updated_on" , "updated_by"]
		values = [is_active, current_timestamp(), session_user]
		condition = "user_id='%d'" % user_id
		return self._db.update(self._db.tblClientUserDetails, columns, values,
			condition) 

	def change_admin_status(self, user_id, is_admin, session_user):
		columns = ["is_admin", "updated_on" , "updated_by"]
		values = [is_admin, current_timestamp(), session_user]
		condition = "user_id='%d'" % user_id
		return self._db.update(self._db.tblClientUserDetails, columns, values,
			condition)
#
#	Country
#
	def get_countries(self):
		columns = ["country_id", "country_name", "is_active"]
		condition = " is_active = '1' "
		rows = self._db.get_data(self._db.tblCoutries,columns, 
			condition)
		return rows		

#
#	Domain
#
	def get_domains(self):
		columns = ["domain_id", "domain_name", "is_active"]
		condition = " is_active = '1' "
		rows = self._db.get_data(self._db.tblDomains,columns, 
			condition)
		return rows	

#
#	Business Group
#

	def get_business_groups(self):
		columns = ["business_group_id", "business_group_name"]
		condition = "1"
		rows = self._db.get_data(self._db.tblBusinessGroup,columns, 
			condition)
		return rows

#
#	Legal Entity
#
	def get_legal_entities(self):
		columns = ["legal_entity_id", "legal_entity_name", "business_group_id"]
		condition = "1"
		rows = self._db.get_data(self._db.tblLegalEntity,columns, condition)
		return rows
#
# 	Divisions
#

	def get_divisions(self):
		columns = ["division_id", "division_name", 
		"legal_entity_id", "business_group_id"]
		condition = "1"
		rows = self._db.get_data(self._db.tblDivision,columns, condition)
		return rows

#
#	Units
#
	def get_units(self):
		columns = ["unit_id", "division_id", "legal_entity_id",
                   "business_group_id", "unit_code", "unit_name",
                   "country_id", "address", "domain_ids"]
		condition = " is_active = '1' "                 
		rows = self._db.get_data(self._db.tblUnit, columns, condition)
		return rows

	def get_units_closure_list(self):
		columns = ["business_group_name","legal_entity_name","division_name","unit_id",
                   "unit_code", "unit_name", "address","is_active"]
		tables = [self._db.tblUnit, self._db.tblDivision, self._db.tblLegalEntity,
                self._db.tblBusinessGroup]
		condition_columns = [("division_id","division_id"), 
                            ("legal_entity_id","legal_entity_id"),
                            ("business_group_id","business_group_id")]
		rows = self._db.get_data_from_multiple_tables(columns, tables, 
        	condition_columns, "left join")
		return rows

	def deactivate_unit(self, unitId):
		columns = ["is_active"]
		values = [0]
		condition = "unit_id ='%d'" % unitId
		return self._db.update(self._db.tblUnit, columns, 
        	values, condition)

