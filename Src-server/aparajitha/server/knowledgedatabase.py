from aparajitha.server.database import Database
from aparajitha.misc.dates import *
from aparajitha.misc.client_mappings import *
from aparajitha.misc.formmappings import formIdMappings
import uuid
import hashlib
import string
import random


DATABASE = "mirror_knowledge"

def to_dict(keys, values_list):
	values_list2 = []
	for values in values_list :
		values_list2.append(dict(zip(keys, values)))
	return values_list2

def get(fields) :
	return ", ".join(fields)

def generate_password() : 
    characters = string.ascii_uppercase + string.digits
    password = ''.join(random.SystemRandom().choice(characters) for _ in range(7))
    print password
    print encrypt(password)
    return encrypt(password)

def encrypt(value):
	m = hashlib.md5()
	m.update(value)
	return m.hexdigest()

def client_database(client_id) :
	database_name = None
	if client_id in client_db_mappings :
		database_name = client_db_mappings[client_id]
	if database_name is None :
		# temporary purpose
		database_name = "mirror_client"
		# return None
	return Database(database_name)

class KnowledgeDatabase(object) :
	def __init__(self) :
		self._db = Database(DATABASE)

	def new_uuid(self) :
		s = str(uuid.uuid4())
		return s.replace("-", "")

	def test(self) :
		query = "SHOW TABLES;"
		return self._db.execute_and_return(query)

	def add_session(self, user_id) :
		session_id = self.new_uuid()
		query = "insert into tbl_user_sessions values ('%s', '%s', '%d');"
		query = query % (session_id, user_id, current_timestamp())
		self._db.execute(query)
		return session_id

	def remove_session(self, session_id) :
		query = "delete from tbl_user_sessions where session_id = '%s';"
		query = query % (session_id,)
		self._db.execute(query)

	def get_session_user_id(self, session_id) :
		query = "select user_id from tbl_user_sessions where session_id = '%s';"
		query = query % (session_id,)
		result = self._db.execute_and_return(query)
		if len(result) == 0 :
			return None
		return int(result[0][0])

	def get_user(self, user_id) :
		select_fields = [
			"user_id", "email_id", "client_id", "is_active", "user_group_id",
			"category", "employee_name", "employee_code", "contact_no", "address",
			"designation", "domain_ids", "country_ids", "client_ids", "is_admin"
		]
		query = "select %s from tbl_user_details where user_id = %s;"
		query = query % (get(select_fields), user_id,)
		result = self._db.execute_and_return(query)
		if len(result) == 0 :
			return None
		result = to_dict(select_fields, result)
		for row in result :
			row["user_id"] = int(row["user_id"])
			row["user_group_id"] = int(row["user_group_id"])
		return result[0]

	def get_user_id(self, email) :
		select_fields = ["user_id"]
		query = "select %s from tbl_users where username = '%s';"
		query = query % (get(select_fields), email,)
		result = self._db.execute_and_return(query)
		if len(result) == 0 :
			return None
		return int(result[0][0])

	def get_client_id(self, user_id):
		select_fields = ["client_id"]
		query = "select %s from tbl_users where user_id = '%s';"
		query = query % (get(select_fields), user_id,)
		result = self._db.execute_and_return(query)
		if len(result) == 0 :
			return None
		return int(result[0][0])		

	def match_password(self, user_id, password) :
		select_fields = ["client_id"]
		encrypted_password = encrypt(password)
		query = ("select %s from tbl_users where user_id = %s and " +
			"password = '%s' and is_active = 1;")
		query = query % (get(select_fields), user_id, encrypted_password)
		result = self._db.execute_and_return(query)
		if len(result) == 0 :
			return None
		return to_dict(select_fields, result)

	def get_user_details(self, user_id, client_id) :
		select_fields = [
			"tbl1.category", "user_group_name", "form_ids",
			"employee_name", "employee_code",
			"contact_no", "address", "designation", "is_admin"
		]
		client_select_fields = [
			"user_group_name", "form_ids",
			"employee_name", "employee_code",
			"contact_no", "is_admin"
		]
		query = ("select %s from %s tbl1 " +
			"inner join %s tbl2 " +
			"on tbl1.user_group_id = tbl2.user_group_id " +
			"where user_id = %s;")

		result = None
		if client_id is None :
			query = query % (get(select_fields), 
			self._db.tblUserDetails,self._db.tblUserGroups,user_id,)
			result = self._db.execute_and_return(query)
			result = to_dict(select_fields, result)
		else :
			client_db = client_database(client_id)
			if client_db is None :
				return None
			query = query % (get(client_select_fields), 
			self._db.tblClientUserDetails, self._db.tblClientUserGroups,user_id,)
			result = client_db.execute_and_return(query)
			result = to_dict(client_select_fields, result)
		if len(result) == 0 :
			return None
		result = result[0]
		form_ids = result["form_ids"].split(",")
		form_ids2 = []
		for form_id in form_ids :
			form_ids2.append(int(form_id))

		select_fields = [
			"form_id", "form_name", "form_url",
			"form_type", "form_order", "parent_menu"
		]
		query = "select %s from tbl_forms where form_id in %s "
		if result["is_admin"] == 0 :
			query = query + " and admin_form = 0"
		query = query % (get(select_fields), tuple(form_ids2))
		forms = self._db.execute_and_return(query)
		if len(forms) == 0 :
			return None
		forms = to_dict(select_fields, forms)

		menu = {
			"masters": [],
			"transactions": [],
			"reports": [],
			"settings": []
		}
		for form in forms :
			form_type = form["form_type"] + "s"
			form["form_id"] = int(form["form_id"])
			form["form_order"] = int(form["form_order"])
			menu[form_type].append(form)
		result2 = {
			"user_group_name": result["user_group_name"],
			"employee_name": result["employee_name"],
			"employee_code": result["employee_code"],
			"contact_no": result["contact_no"],
			"menu": menu
		}
		if client_id == None :
			result2["address"] = result["address"]
			result2["designation"] = result["designation"]
			result2["category"] = result["tbl.category"]
		else:
			result2["address"] = ""
			result2["designation"] = ""
			result2["category"] = ""
		return result2


#
#	Common
#

	def generate_new_id(self, form):
		tbl_name = None
		column = None
		if form == "ActivityLog":
			tbl_name = self._db.tblActivityLog
			column = "activity_log_id"
		elif form == "User":
			tbl_name = self._db.tblUsers
			column = "user_id"
		else:
			print "Error : Cannot generate new id for form %s" % form

		return self._db.generate_new_id(tbl_name, column)

	def is_duplicate(self, form, field, value, idValue):
		tbl_name = None
		condition = None
		if form == "User":
			tbl_name = self._db.tblUsers
			if field == "email":
				condition = "username ='%s' AND user_id != '%d'" %(
           value, idValue)
		
		return self._db.is_already_exists(tbl_name, condition)

	def isIdInvalid(self, form, idValue):
		tbl_name = None
		condition = None
		if form == "User":
			tbl_name = self._db.tblUsers
			condition = "user_id = '%d'" % idValue
		else:
			print "Error: Id Validation not exists for form %s" % form

		return not self._db.is_already_exists(tbl_name, condition)

	def verify_password(self, password, session_user, client_id):
		encrypted_password = encrypt(password)
		columns = ["count(*)"]
		condition = "password='%s' and user_id='%d'" % (encrypted_password, session_user)
		if client_id != None:
			condition += " and client_id='%d'" % client_id
		rows = self._db.get_data(self._db.tblUsers, columns, condition)
		if(int(rows[0][0]) <= 0):
			return False
		else:
			return True

#
#	Forms
#
	def get_section_wise_forms(self, type):
		columns = ["form_id", "form_name", "form_url", "form_order", "form_type",
		"category", "admin_form", "parent_menu"]
		if type == "knowledge".lower():
			condition = " category = 'knowledge' "
		elif type == "techno".lower():
			condition = " category = 'techno' "
		else :
			condition = " category = 'client' "
		rows = self._db.get_data(self._db.tblForms, columns, condition)
		return rows

#
#	Country
#
	def get_countries(self):
		columns = "country_id, country_name, is_active"
		condition = "1"
		rows = self._db.get_data(self._db.tblCoutries,columns, 
			condition)
		return rows		

#
#	Domain
#
	def getDomains(self):
		columns = "domain_id, domain_name, is_active"
		condition = "1"
		rows = self._db.get_data(self._db.tblDomains,columns, 
			condition)
		return rows	

#
#	Unit
#
	def deactivate_unit(self, unit_id, client_id, session_user):
		columns = ["is_active", "updated_by", "updated_on"]
		values = [0, session_user, current_timestamp()]
		condition = "unit_id = {unit_id} and client_id={client_id}".format(
            unit_id = unit_id, client_id = client_id)
		return self._db.update(self._db.tblUnit, columns, 
        	values, condition)

#
#	User
#
	def save_user(self, user, session_user):
		timestamp = current_timestamp()
		columns = "user_id, username, password, client_id,created_on,created_by,"+\
                        " updated_on, updated_by"
		values = [(user.user_id, user.email_id, generate_password(), 
        		user.client_id, timestamp,session_user,
                timestamp,session_user)]
		return self._db.insert(self._db.tblUsers, columns, values)

	def change_user_status(self, user_id, is_active, session_user):
		columns = ["is_active", "updated_on" , "updated_by"]
		values = [is_active, current_timestamp(), session_user]
		condition = "user_id='%d'" % user_id
		return self._db.update(self._db.tblUsers, columns, values,
			condition)
#
#	Activity Log
#

	def save_activity(self, form, obj, action_type, session_user):
		activity_log_id = self.generate_new_id("ActivityLog")
		form_id = formIdMappings[form]
		action = None
		ticker_text = None
		ticker_link = None
		created_on = current_timestamp()

		if form == "ServiceProvider":
			if action_type == "save":
				action = "Service Provider %s has been created" % obj
			elif action_type == "update":
				action = "Service Provider %s has been updated" % obj
			elif action_type == "status_change":
				action = "Status of service Provider %s has been updated" % str(obj)
		elif form == "UserPrivilege":
			if action_type == "save":
				action = "User Privilege %s has been created" % obj
			elif action_type == "update":
				action = "User Privilege %s has been updated" % obj
			elif action_type == "status_change":
				action = "Status of User Privilege %s has been updated" % str(obj)			
		elif form == "User":
			if action_type == "save":
				action = "User %s has been created" % obj
			elif action_type == "update":
				action = "User %s has been updated" % obj
			elif action_type == "status_change":
				action = "Status of User %s has been updated" % str(obj)
			elif action_type == "admin_status_change":
				action = "Admin Status of User Privilege %s has been updated" % str(obj)
		else:
			print "Error : Activity Log not available for form %s" % form
		
		if ticker_text != None and ticker_link != None:
			columns = "activity_log_id, user_id, form_id, action, ticker_text,"+\
						"ticker_link, created_on"
			values_list = [(activity_log_id, session_user, form_id, action, ticker_text,
					ticker_link, created_on)]
		else:
			columns = "activity_log_id, user_id, form_id, action, created_on"
			values_list = [(activity_log_id, session_user, form_id, action, created_on)]

		return self._db.insert(self._db.tblActivityLog, columns, values_list)
