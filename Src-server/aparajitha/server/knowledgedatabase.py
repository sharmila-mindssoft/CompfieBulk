from aparajitha.server.database import Database
from aparajitha.misc.dates import *
from aparajitha.misc.client_mappings import *
import uuid

DATABASE = "mirror_knowledge"

def to_dict(keys, values_list):
	values_list2 = []
	for values in values_list :
		values_list2.append(dict(zip(keys, values)))
	return values_list2

def get(fields) :
	return ", ".join(fields)

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
		return self._db.execute_and_return(query)

	def add_session(self, user_id) :
		session_id = self.new_uuid()
		query = "insert into tbl_user_sessions values ('%s', '%s', '%d');"
		query = query % (session_id, user_id, current_timestamp())
		self._db.execute(query)
		return session_id

	def get_session_user_id(self, session_id) :
		pass

	def get_user(self, user_id) :
		pass

	def get_user_id(self, email) :
		select_fields = ["user_id"]
		query = "select %s from tbl_users where username = '%s';"
		query = query % (get(select_fields), email,)
		result = self._db.execute_and_return(query)
		if result is None :
			return None
		return int(result[0][0])

	def match_password(self, user_id, password) :
		select_fields = ["client_id"]
		query = ("select %s from tbl_users where user_id = %s and " +
			"password = '%s' and is_active = 1;")
		query = query % (get(select_fields), user_id, password)
		result = self._db.execute_and_return(query)
		if result is None :
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
			result = self._db.execute_and_return(query)
		else :
			client_db = client_database(client_id)
			if client_db is None :
				return None
			result = self.client_db.execute_and_return(query)
		if result is None :
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
		query = "select %s from tbl_forms where form_id in %s;"
		if result["is_admin"] == 0 :
			query = query + " and admin_form = 0"
		query = query % (get(select_fields), tuple(form_ids2))
		forms = self._db.execute_and_return(query)
		if forms is None :
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
