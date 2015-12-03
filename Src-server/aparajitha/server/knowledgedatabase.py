from aparajitha.server.database import Database
from aparajitha.misc.dates import *
from aparajitha.misc.client_mappings import *
from aparajitha.misc.formmappings import formIdMappings
import uuid
import hashlib

DATABASE = "mirror_knowledge"

def to_dict(keys, values_list):
	values_list2 = []
	for values in values_list :
		values_list2.append(dict(zip(keys, values)))
	return values_list2

def get(fields) :
	return ", ".join(fields)

def encrypt(value):
	m = hashlib.md5()
	m.update(value)
	return m.hexdigest()

class KnowledgeDatabase(object) :
	def __init__(self) :
		self._db = Database(DATABASE)

	def client_database(client_id) :
		database_name = None
		if client_id in client_db_mappings :
			database_name = client_db_mappings[client_id]
		if database_name is None :
			# temporary purpose
			database_name = "mirror_client"
			# return None
		return Database(database_name)

	def new_uuid(self) :
		s = str(uuid.uuid4())
		return s.replace("-", "")
		
	def test(self) :
		query = "SHOW TABLES;"
		return self._db.executeAndReturn(query)

	def add_session(self, user_id) :
		session_id = self.new_uuid()
		query = "insert into tbl_user_sessions values ('%s', '%s', '%d');"
		query = query % (session_id, user_id, currentTimestamp())
		self._db.execute(query)
		return session_id

	def remove_session(self, session_id) :
		query = "delete from tbl_user_sessions where session_id = '%s';"
		query = query % (session_id,)
		self._db.execute(query)

	def get_session_user_id(self, session_id) :
		query = "select user_id from tbl_user_sessions where session_id = '%s';"
		query = query % (session_id,)
		result = self._db.executeAndReturn(query)
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
		result = self._db.executeAndReturn(query)
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
		result = self._db.executeAndReturn(query)
		if len(result) == 0 :
			return None
		return int(result[0][0])

	def match_password(self, user_id, password) :
		select_fields = ["client_id"]
		encryptedPassword = encrypt(password)
		query = ("select %s from tbl_users where user_id = %s and " +
			"password = '%s' and is_active = 1;")
		query = query % (get(select_fields), user_id, encryptedPassword)
		result = self._db.executeAndReturn(query)
		if len(result) == 0 :
			return None
		return to_dict(select_fields, result)

	def get_user_details(self, user_id, client_id) :
		select_fields = [
			"user_group_name", "form_ids",
			"employee_name", "employee_code",
			"contact_no", "address", "designation", "is_admin"
		]
		query = ("select %s from tbl_user_details tbl1 " +
			"inner join tbl_user_groups tbl2 " +
			"on tbl1.user_group_id = tbl2.user_group_id " +
			"where user_id = %s;")
		query = query % (get(select_fields), user_id,)
		result = None
		if client_id is None :
			result = self._db.executeAndReturn(query)
		else :
			client_db = client_database(client_id)
			if client_db is None :
				return None
			result = self.client_db.executeAndReturn(query)
		if len(result) == 0 :
			return None
		result = to_dict(select_fields, result)
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
		forms = self._db.executeAndReturn(query)
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
			"address": result["address"],
			"designation": result["designation"],
			"menu": menu
		}
		return result2

#
#	Common
#

	def generateNewId(self, form):
		tblName = None
		column = None
		if form == "ActivityLog":
			tblName = self._db.tblActivityLog
			column = "activity_log_id"
		else:
			print "Error : Cannot generate new id for form %s" % form

		return self._db.generateNewId(tblName, column)

#
#	Activity Log
#

	def saveActivity(self, form, obj, actionType, sessionUser):
		activityLogId = self.generateNewId("ActivityLog")
		formId = formIdMappings[form]
		action = None
		tickerText = None
		tickerLink = None
		createdOn = currentTimestamp()

		if form == "ServiceProvider":
			if actionType == "save":
				action = "Service Provider %s has been created" % obj.serviceProviderName
			elif actionType == "update":
				action = "Service Provider %s has been updated" % obj.serviceProviderName
			elif actionType == "statusChange":
				action = "Status of service Provider %s has been updated" % str(obj)
		else:
			print "Error : Activity Log not available for form %s" % form
		
		if tickerText != None and tickerLink != None:
			columns = "activity_log_id, user_id, form_id, action, ticker_text,"+\
						"ticker_link, created_on"
			valuesList = [(activityLogId, sessionUser, formId, action, tickerText,
					tickerLink, createdOn)]
		else:
			columns = "activity_log_id, user_id, form_id, action, created_on"
			valuesList = [(activityLogId, sessionUser, formId, action, createdOn)]

		return self._db.insert(self._db.tblActivityLog, columns, valuesList)
