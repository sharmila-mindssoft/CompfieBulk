from aparajitha.server.database import Database
from aparajitha.misc.dates import *
from aparajitha.misc.client_mappings import *
from aparajitha.misc.formmappings import formIdMappings
import uuid
import datetime
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
		self.allStatutories = {}
		self.allGeographies = {}
		self.get_all_geographies()
		self.get_all_statutories()

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

	def getNewId(self, field , tableName) :
		query = "SELECT max(%s) from %s " % (field, tableName)
		result = self._db.execute_and_return(query)
		if len(result) == 0 :
			return 1
		return int(row[0][0]) + 1

	def getDateTime(self) :
		return datetime.datetime.now()

	def add_activity_log(self, user_id, form_id, action, notification_text=None, notification_link=None) :
		created_on = self.getDateTime()
		activityId = self.getNewId("activity_log_id", "tbl_activity_log")
		query = "INSERT INTO tbl_activity_log(activity_log_id, user_id, form_id, \
            action, ticker_text, ticker_link, created_on) \
            VALUES (%s, %s, %s, '%s', '%s', '%s', '%s')" % (
                activityId, userId, formId, action, str(notificationText), str(notificationLink), created_on
            )
		self._db.execute(query)

	def check_duplicate_domain(self, domain_name, domain_id) :
		query = "SELECT count(*) FROM tbl_domains \
            WHERE LOWER(domain_name) = LOWER('%s') " % domain_name
		if domain_id is not None :
			query = query + " AND domain_id != %s" % domain_id
		result = self._db.execute_and_return(query)
		if result[0][0] > 0 :
			return True
		return False
    
	def get_domains(self) :
		query = "SELECT domain_id, domain_name, is_active FROM tbl_domains "
		return self._db.execute_and_return(query)

	def add_domain(self, domain_name, created_by) :
		created_on = self.getDateTime()
		domain_id = self.getNewId("domain_id", "tbl_domains")
		is_active = 1

		query = "INSERT INTO tbl_domains(domain_id, domain_name, is_active, \
            created_by, created_on) VALUES (%s, '%s', %s, %s, '%s') " % (
            domain_id, domain_name, is_active, created_by, created_on
        )

		self._db.execute(query)
		action = "Add Domain - \"%s\"" % domainName
		self.add_activity_log(created_by, 4, action)
		return True

	def get_domain_by_domain_id(self, domain_id) :
		q = "SELECT domain_name FROM tbl_domains WHERE domain_id=%s" % domain_id
		rows = self._db.execute_and_return(q)
		return rows[0][0]

	def update_domain(self, domain_id, domain_name, updated_by) :
		old_data = self.get_domain_by_domain_id(domain_id)
		if old_data is not None :
			query = "UPDATE tbl_domains SET domain_name = '%s', \
            updated_by = %s WHERE domain_id = %s" % (
                domain_name, updated_by, domain_id
            )
			self._db.execute(query)
			action = "Edit Domain - \"%s\"" % domain_name
			self.add_activity_log(updated_by, 4, action)
			return True
		else :
			return False

	def update_domain_status(self, domain_id, is_active, updated_by) :
		old_data = self.get_domain_by_domain_id(domain_id)
		if old_data is not None :
			query = "UPDATE tbl_domains SET is_active = %s, \
            updated_by = %s WHERE domain_id = %s" % (
                is_active, updated_by, domain_id
            )
			self._db.execute(query)
			if is_active == 0 :
				status = "deactivated"
			else:
				status = "activated"
			action = "Domain %s status  - %s" % (old_data, status)
			self.add_activity_log(updated_by, 4, action)
			return True
		else :
			return False

	def update_domain_status(self, domain_id, is_active, updated_by) :
		old_data = self.get_domain_by_domain_id(domain_id)
		if old_data is not None :
			query = "UPDATE tbl_domains SET is_active = %s, \
            updated_by = %s WHERE domain_id = %s" % (
                is_active, updated_by, domain_id
            )
			self._db.execute(query)
			if is_active == 0 :
				status = "deactivated"
			else:
				status = "activated"
			action = "Domain %s status  - %s" % (old_data, status)
			self.add_activity_log(updated_by, 4, action)
			return True
		else :
			return False

	def get_countries(self) :
		query = "SELECT country_id, country_name, is_active FROM tbl_countries "
		return self._db.execute_and_return(query)

	def check_duplicate_country(self, country_name, country_id) :
	    query = "SELECT count(*) FROM tbl_countries \
	        WHERE LOWER(country_name) = LOWER('%s') " % country_name
	    if country_id is not None :
	        query = query + " AND country_id != %s" % country_id
	    result = self._db.execute_and_return(query)

	    if result[0][0] > 0 :
	        return True

	    return False

	def add_country(self, country_name, created_by) :
	    created_on = self.getDateTime()
	    country_id = self.getNewId("country_id", "tbl_countries")
	    is_active = 1

	    query = "INSERT INTO tbl_countries(country_id, country_name, \
	        is_active, created_by, created_on) VALUES (%s, '%s', %s, %s, '%s') " % (
	        country_id, country_name, is_active, created_by, created_on
	    )
	    self._db.execute(query)
	    action = "Add Country - \"%s\"" % country_name
	    self.add_activity_log(created_by, 4, action)
	    return True

	def get_country_by_country_id(self, country_id) :
	    q = "SELECT country_name FROM tbl_countries WHERE country_id=%s" % country_id
	    rows = self._db.execute_and_return(q)
	    return rows[0][0]

	def update_country(self, country_id, country_name, updated_by) :
	    old_data = self.get_country_by_country_id(country_id)
	    if old_data is not None :
	        query = "UPDATE tbl_countries SET country_name = '%s', \
	            updated_by = %s WHERE country_id = %s" % (
	                country_name, updated_by, country_id
	            )
	        self._db.execute(query)
	        action = "Edit Country - \"%s\"" % country_name
	        self.add_activity_log(updated_by, 3, action)
	        return True
	    else :
	        return False

	def update_country_status(self, country_id, is_active, updated_by) :
	    old_data = self.get_country_by_country_id(country_id)
	    if old_data is not None :
	        query = "UPDATE tbl_countries SET is_active = %s, \
	        updated_by = %s WHERE country_id = %s" % (
	            is_active, updated_by, country_id
	        )
	        if is_active == 0:
	            status = "deactivated"
	        else:
	            status = "activated"
	        self._db.execute(query)
	        action = "Country %s status  - %s" % (old_data, status)
	        self.add_activity_log(updated_by, 3, action)
	        return True
	    else :
	        return False

	def get_industries(self) :
	    query = "SELECT industry_id, industry_name, is_active FROM tbl_industries "
	    return self._db.execute_and_return(query)

	def check_duplicate_industry(self, industry_name, industry_id) :
	    query = "SELECT count(*) FROM tbl_industries \
	        WHERE LOWER(industry_name) = LOWER('%s') " % industr_name

	    if industry_id is not None :
	        query = query + " AND industry_id != %s" % industry_id
	    rows = self._db.execute_and_return(query)
	    if rows[0][0] > 0 :
	        return True

	    return False

	def add_industry(self, industry_name, created_by) :
	    created_on = self.getDateTime()
	    industry_id = self.getNewId("industry_id", "tbl_industries")
	    is_active = 1

	    query = "INSERT INTO tbl_industries(industry_id, industry_name, is_active, \
	        created_by, created_on) VALUES (%s, '%s', %s, %s, '%s') " % (
	        industry_id, industry_name, is_active, created_by, created_on
	    )

	    self._db.execute(query)
	    action = "Add Industry - \"%s\"" % industry_name
	    self.add_activity_log(created_by, 5, action)
	    return True

	def get_industry_by_industry_id(self, industry_id) :
	    if type(industry_id) == IntType :
	        qry = "SELECT industry_name FROM tbl_industries WHERE industry_id=%s" % industry_id
	    else :
	        if type(industry_id) == ListType :
	            ids = industry_id
	        else :
	            ids = [int(x) for x in industry_id[:-1].split(',')]
	        if (len(ids) == 1) :
	            qrywhere = "WHERE industry_id = %s" % ids[0]
	        else :
	            qrywhere = "WHERE industry_id in %s" % str(tuple(ids))

	        qry = " SELECT (GROUP_CONCAT(industry_name SEPARATOR ', ')) as industry_name \
	            FROM tbl_industries %s" % qrywhere

	    rows = self._db.execute_and_return(qry)
	    return str(rows[0][0])

	def update_industry(self, industry_id, industry_name, updated_by) :
	    old_data = self.get_industry_by_industry_id(industry_id)
	    if old_data is not None :
	        query = "UPDATE tbl_industries SET industry_name = '%s', \
	        updated_by = %s WHERE industry_id = %s" % (
	            industry_name, updated_by, industry_id
	        )
	        self._db.execute(query)
	        action = "Edit Industry - \"%s\"" % industry_name
	        self.add_activity_log(updated_by, 5, action)
	        return True
	    else :
	        return False

	def update_industry_status(self, industry_id, is_active, updated_by) :
	    old_data = self.get_industry_by_industry_id(industry_id)
	    if old_data is not None :
	        query = "UPDATE tbl_industries SET is_active = %s, updated_by = %s \
	        WHERE industry_id = %s" % (
	            is_active, updated_by, industry_id
	        )
	        if is_active == 0:
	            status = "deactivated"
	        else:
	            status = "activated"
	        self._db.execute(query)
	        action = "Industry %s status  - %s" % (old_data, status)
	        self.add_activity_log(updated_by, 5, action)
	        return True
	    else :
	        return False

	def get_statutory_natures(self) :
	    query = "SELECT statutory_nature_id, statutory_nature_name, is_active \
	        FROM tbl_statutory_natures "
	    return self._db.execute_and_return(query)

	def check_duplicate_statutory_nature(self, statutory_nature_name, statutory_nature_id) :
	    query = "SELECT count(*) FROM tbl_statutory_natures \
	        WHERE LOWER(statutory_nature_name) = LOWER('%s') " % statutory_nature_name

	    if statutory_nature_id is not None :
	        query = query + " AND statutory_nature_id != %s" % statutory_nature_id
	    result = self._db.execute_and_return(query)

	    if result[0][0] > 0 :
	        return True

	    return False

	def save_statutory_nature(self, statutory_nature_name, created_by) :
	    created_on = self.getDateTime()
	    statutory_nature_id = self.getNewId("statutory_nature_id", "tbl_statutory_natures")
	    is_active = 1

	    query = "INSERT INTO tbl_statutory_natures(statutory_nature_id, statutory_nature_name, \
	        is_active, created_by, created_on)  VALUES (%s, '%s', %s, %s, '%s') " % (
	            statutory_nature_id, statutory_nature_name, is_active, created_by, created_on
	        )

	    self._db.execute(query)
	    action = "Add Stautory Nature - \"%s\"" % statutory_nature_name
	    self.add_activity_log(created_by, 8, action)
	    return True

	def get_statutory_nature_by_id(self, statutory_nature_id) :
	    q = "SELECT statutory_nature_name FROM tbl_statutory_natures \
	        WHERE statutory_nature_id=%s" % statutory_nature_id
	    rows = self._db.execute_and_return(q)
	    return rows[0][0]

	def update_statutory_nature(self, statutory_nature_id, statutory_nature_name, updated_by) :
	    old_data = self.get_statutory_nature_by_id(statutory_nature_id)
	    if old_data is not None :
	        query = "UPDATE tbl_statutory_natures SET statutory_nature_name = \'%s\', \
	        updated_by = %s WHERE statutory_nature_id = %s" % (
	            statutory_nature_name, updated_by, statutory_nature_id
	        )
	        self._db.execute(query)
	        action = "Edit Stautory Nature - \"%s\"" % statutory_nature_name
	        self.add_activity_log(updated_by, 8, action)
	        return True
	    else :
	        return False

	def update_statutory_nature_status(self, statutory_nature_id, is_active, updated_by) :
	    old_data = self.get_statutory_nature_by_id(statutory_nature_id)
	    if old_data is not None :
	        query = "UPDATE tbl_statutory_natures SET is_active = %s, \
	            updated_by = %s WHERE statutory_nature_id = %s" % (
	                is_active, updated_by, statutory_nature_id
	            )
	        if is_active == 0:
	            status = "deactivated"
	        else:
	            status = "activated"
	        self._db.execute(query)
	        action = "Statutory Nature %s status  - %s" % (old_data, status)
	        self.add_activity_log(updated_by, 8, action)
	        return True
	    else :
	        return False

	def get_statutory_levels(self) :
	    query = "SELECT level_id, level_position, level_name, country_id, domain_id \
	        FROM tbl_statutory_levels ORDER BY level_position"
	    return self._db.execute_and_return(query)

	def get_statutory_levels_by_id(self, country_id, domain_id) :
	    query = "SELECT level_id, level_position, level_name \
	        FROM tbl_statutory_levels WHERE country_id = %s and domain_id = %s ORDER BY level_position" % (
	            country_id, domain_id
	        )
	    return self._db.execute_and_return(query)

	def save_statutory_level(self, country_id, domain_id, level_id, level_name, level_position, user_id) :
	    if level_id is None :
	        level_id = self.getNewId("level_id", "tbl_statutory_levels")
	        created_on = self.getDateTime()

	        query = "INSERT INTO tbl_statutory_levels (level_id, level_position, \
	            level_name, country_id, domain_id, created_by, created_on) VALUES (%s, %s, '%s', %s, %s, %s, '%s')" % (
	                level_id, level_position, level_name, country_id, domain_id, user_id, created_on
	            )
	        self._db.execute(query)
	        action = "Add Stautory Levels"
	        self.add_activity_log(user_id, 9, action)
	        return True
	    else :
	        query = "UPDATE tbl_statutory_levels SET level_position=%s, level_name='%s', \
	        updated_by=%s WHERE level_id=%s" % (
	            level_position, level_name, user_id, level_id
	        )
	        self._db.execute(query)
	        action = "Edit Stautory Levels"
	        self.add_activity_log(user_id, 9, action)
	        return True

	def get_geography_levels(self) :
	    query = "SELECT level_id, level_position, level_name, country_id \
	        FROM tbl_geography_levels ORDER BY level_position"
	    return self._db.execute_and_return(query)

	def get_geography_levels_by_country(self, country_id) :
	    query = "SELECT level_id, level_position, level_name \
	        FROM tbl_geography_levels WHERE country_id = %s ORDER BY level_position" % countryId
	    return self._db.execute_and_return(query)

	def save_geography_level(self, country_id, level_id, level_name, level_position, user_id) :
	    if level_id is None :
	        level_id = self.getNewId("level_id", "tbl_geography_levels")
	        created_on = self.getDateTime()

	        query = "INSERT INTO tbl_geography_levels (level_id, level_position, \
	            level_name, country_id, created_by, created_on) VALUES (%s, %s, '%s', %s, %s, '%s')" % (
	                level_id, level_position, level_name, country_id, user_id, created_on
	            )
	        self._db.execute(query)
	        action = "Add Geography Levels"
	        self.add_activity_log(user_id,6, action)
	        return True
	    else :
	        query = "UPDATE tbl_geography_levels SET level_position=%s, level_name='%s', \
	        updated_by=%s WHERE level_id=%s" % (
	            level_position, level_name, user_id, level_id
	        )
	        self._db.execute(query)
	        action = "Edit Geography Levels"
	        self.add_activity_log(user_id, 6, action)
	        return True

	def get_all_geographies(self):
	    rows = self.get_geographies()
	    _tempDict = {}
	    for row in rows :
	        _tempDict[int(row[0])] = row[1]

	    for row in rows :
	        parentIds = [int(x) for x in row[3][:-1].split(',')]
	        names = []
	        names.append(row[6])
	        for id in parentIds :
	            if id > 0 :
	                names.append(_tempDict.get(id))
	            names.append(row[1])
	        mappings = '>>'.join(str(x) for x in names)
	        self.allGeographies[int(row[0])] = [row[1], mappings, row[3]]

	def get_geographies(self) :
	    query = "SELECT t1.geography_id, t1.geography_name, t1.level_id, \
	        t1.parent_ids, t1.is_active, t2.country_id, t3.country_name FROM tbl_geographies t1 \
	        INNER JOIN tbl_geography_levels t2 on t1.level_id = t2.level_id \
	        INNER JOIN tbl_countries t3 on t2.country_id = t3.country_id"
	    return self._db.execute_and_return(query)

	def get_duplicate_geographies(self, parent_ids, geography_id) :
	    query = "SELECT geography_id, geography_name, level_id, is_active \
	        FROM tbl_geographies WHERE parent_ids='%s' " % (parent_ids)
	    if geography_id is not None :
	        query = query + " AND geography_id != %s" % geography_id
	    return self._db.execute(query)

	def save_geographies(self, name, level_id, parent_ids, user_id) :
	    geography_id = self.getNewId("geography_id", "tbl_geographies")
	    created_on = self.getDateTime()

	    query = "INSERT INTO tbl_geographies (geography_id, geography_name, level_id, \
	        parent_ids, created_by, created_on) VALUES (%s, '%s', %s, '%s', %s, '%s')" % (
	            geography_id, name, level_id, parent_ids, user_id, created_on
	        )
	    self._db.execute(query)
	    self.get_all_geographies()
	    action = "Add Geography - %s" % name
	    self.add_activity_log(user_d, 7, action)
	    return True

	def update_geography_master(self, geography_id, name, parent_ids, updated_by) :
	    oldData = self.allGeographies.get(geography_id)
	    old_parent_ids = oldData[2]
	    query = "UPDATE tbl_geographies set geography_name='%s', parent_ids='%s',\
	        updated_by=%s WHERE geography_id=%s " % (
	            name, parent_ids, updated_by, geography_id
	        )
	    self._db.execute(query)
	    action = "Edit Geography - %s" % name
	    self._db.execute(updated_by, 7, action)
	    if old_parent_ids != parent_ids :
	        oldPId = str(old_parent_ids) + str(geography_id)
	        newPId = str(parent_ids) + str(geography_id)
	        qry = "SELECT geography_id, geography_name, parent_ids from tbl_geographies \
	            WHERE parent_ids like '%s'" % str("%" + str(oldPId) + ",%")
	        rows = self._db.execute_and_return(qry)
	        for row in rows :
	            newParentId = str(row[2]).replace(oldPId, newPId)
	            q = "UPDATE tbl_geographies set parent_ids='%s', updated_by=%s where geography_id=%s" % (
	                newParentId, updated_by, row[0]
	            )
	            self._db.execute(q)
	        action = "Edit Geography Mappings Parent"
	        self.add_activity_log(updated_by, 7, action)
	    self.get_all_geographies()
	    return True

	def change_geography_status(self,geography_id, is_active, updated_by) :
	    query = "UPDATE tbl_geographies set is_active=%s, updated_by=%s WHERE geography_id=%s" % (
	        is_active, updated_by, geography_id
	    )
	    self._db.execute(query)
	    if is_active == 0:
	        status = "deactivated"
	    else:
	        status = "activated"
	    name = self.allGeographies.get(geography_id)[0]
	    action = "Geography %s status  - %s" % (name, status)
	    self.add_activity_log(updated_by, 7, action)
	    return True

	### Statutory ###
	def get_all_statutories(self):
	    rows = self.get_statutories()
	    _tempDict = {}
	    for row in rows :
	        _tempDict[int(row[0])] = row[1]

	    for row in rows :
	        parentIds = [int(x) for x in row[3][:-1].split(',')]
	        names = []
	        for id in parentIds :
	            if id > 0 :
	                names.append(_tempDict.get(id))
	            names.append(row[1])
	        mappings = '>>'.join(str(x) for x in names)
	        self.allStatutories[int(row[0])] = [row[1], mappings, row[3]]
	            
	def get_statutories(self) :
	    query = "SELECT t1.statutory_id, t1.statutory_name, t1.level_id, t1.parent_ids, \
	        t2.country_id, t3.country_name, t2.domain_id, t4.domain_name \
	        FROM tbl_statutories t1 \
	        INNER JOIN tbl_statutory_levels t2 on t1.level_id = t2.level_id \
	        INNER JOIN tbl_countries t3 on t2.country_id = t3.country_id \
	        INNER JOIN tbl_domains t4 on t2.domain_id = t4.domain_id"
	    return self._db.execute_and_return(query)

	def get_country_wise_level1_statutories(self) :
	    query = "SELECT t1.statutory_id, t1.statutory_name, t1.level_id, t1.parent_ids, \
	        t2.country_id, t3.country_name, t2.domain_id, t4.domain_name \
	        FROM tbl_statutories t1 \
	        INNER JOIN tbl_statutory_levels t2 on t1.level_id = t2.level_id \
	        INNER JOIN tbl_countries t3 on t2.country_id = t3.country_id \
	        INNER JOIN tbl_domains t4 on t2.domain_id = t4.domain_id \
	        WHERE t2.level_position=1"
	    return self._db.execute_and_return(query)

	def get_statutory_with_mappings(self) :
	    query = "SELECT t1.statutory_id, t1.statutory_name, t1.parent_ids FROM tbl_statutories t1"
	    _rows = self._db.execute_and_return(query)
	    statutoryNames = {}
	    statutoryMapping = {}

	    for row in _rows :
	        statutoryNames[int(row[0])] = row[1]

	    for geo in _rows :
	        parentIds = [int(x) for x in geo[2][:-1].split(',')]
	        names = []
	        for id in parentIds :
	            if id > 0 :
	                names.append(statutoryNames.get(id))
	            names.append(geo[1])

	        statutoryMapping [int(geo[0])] = '>>'.join(str(x) for x in names)

	    return statutoryMapping

	def get_statutories_by_ids(self, statutory_ids) :
	    if type(statutory_ids) == IntType :
	        qry = " WHERE t1.statutory_id = %s" %  statutory_ids
	    else :
	        ids = (int(x) for x in statutory_ids.split(','))
	        qry = " WHERE t1.statutory_id in (%s)" % str(ids)

	    query = "SELECT t1.statutory_id, t1.statutory_name, t1.level_id, t1.parent_ids, \
	        t2.country_id, t3.country_name, t2.domain_id, t4.domain_name \
	        FROM tbl_statutories t1 \
	        INNER JOIN tbl_statutory_levels t2 on t1.level_id = t2.level_id \
	        INNER JOIN tbl_countries t3 on t2.country_id = t3.country_id \
	        INNER JOIN tbl_domains t4 on t2.domain_id = t4.domain_id %s" % qry
	    return self._db.execute_and_return(query)

	def get_duplicate_statutories(self, parent_ids, statutory_id) :
	    query = "SELECT statutory_id, statutory_name, level_id \
	        FROM tbl_statutories WHERE parent_ids='%s' " % (parent_ids)
	    if statutory_id is not None :
	        query = query + " AND statutory_id != %s" % statutory_id
	    return self._db.execute_and_return(query)

	def save_statutories(self, name, level_id, parent_ids, user_id) :
	    statutory_id = self.getNewId("statutory_id", "tbl_statutories")
	    created_on = self.getDateTime()

	    query = "INSERT INTO tbl_statutories (statutory_id, statutory_name, level_id, \
	        parent_ids, created_by, created_on) VALUES (%s, '%s', %s, '%s', %s, '%s')" % (
	            statutory_id, name, level_id, parent_ids, user_id, created_on
	        )
	    if (self._db.execute(query)) :
	        self.get_all_statutories()
	        action = "Add Statutory - %s" % name
	        self.add_activity_log(user_id, 17, action)
	        return True

	def update_statutories(self, statutory_id, name, parent_ids, updated_by) :
	    oldData = self.allStatutories.get(statutory_id)
	    old_parent_ids = oldData[2]
	    query = "UPDATE tbl_statutories set statutory_name='%s', parent_ids='%s',\
	        updated_by=%s WHERE statutory_id=%s " % (
	            name, parent_ids, updated_by, statutory_id
	        )
	    self._db.execute(query)
	    action = "Edit Statutory - %s" % name
	    self.add_activity_log(updated_by, 17, action)
	    if old_parent_ids != parent_ids :
	        oldPId = str(old_parent_ids) + str(statutory_id)
	        newPId = str(parent_ids) + str(statutory_id)
	        qry = "SELECT statutory_id, statutory_name, parent_ids from tbl_statutories \
	            WHERE parent_ids like '%s'" % str("%" + str(oldPId) + ",%")
	        rows = self._db.execute_and_return(qry)
	        for row in rows :
	            newParentId = str(row[2]).replace(oldPId, newPId)
	            q = "UPDATE tbl_statutories set parent_ids='%s', updated_by=%s where statutory_id=%s" % (
	                newParentId, updated_by, row[0]
	            )
	            self._db.execute(q)
	        action = "Edit Statutory Mappings Parent"
	        self.add_activity_log(updated_by, 17, action)
	    self.get_all_statutories()
	    return True


	def update_statutory_mapping_id(self, statutory_ids, mapping_id, updated_by) :
	    # remove mapping id
	    mapId = str("%" + str(mapping_id) + ",%")
	    q = "SELECT statutory_id, statutory_mapping_ids from tbl_statutories \
	        WHERE statutory_mapping_ids like '%s'" % mapId
	    rows = self._db.execute_and_return(q)
	    oldStatuIds = {}
	    for row in rows :
	        oldStatuIds[int(row[0])] = row[1][:-1]
	    difference = list(set(oldStatuIds.keys()) - set(statutory_ids))

	    for x in difference :
	        oldMapId =  [int(j) for j in oldStatuIds.get(x).split(',')]
	        oldMapId = oldMapId.remove(mapping_id)

	        newMapId = ""
	        if oldMapId is not None : 
	            newMapId = ','.join(str(k) for k in oldMapId) + ","

	        qry1 = "UPDATE tbl_statutories set statutory_mapping_ids = '%s', updated_by = %s \
	            WHERE statutory_id = %s" % (newMapId, updated_by, x)
	        if (self._db.execute(qry1)) :
	            print "Mapping Id %s removed from statutory table, Id=%s" % (mapping_id, x)


	    # statutoryIds = statutoryIds[:-1]
	    # ids = [int(x) for x in statutoryIds.split(',')]
	    ids = tuple(statutory_ids)
	    if (len(ids) == 1) :
	        qryWhere = " WHERE statutory_id = %s" % ids[0]
	    else :
	        qryWhere = " WHERE statutory_id in %s" % str(ids)

	    qry = "SELECT statutory_id, statutory_mapping_ids from tbl_statutories %s" % qryWhere
	    isUpdated = False
	    rows = self._db.execute_and_return(qry)
	    for row in rows:
	        statutory_id = int(row[0])

	        if row[1] is None : 
	            mapId = ""
	        else :
	            mapId = row[1]
	        _statutoryMappingId = str(mapping_id) + ","
	        if (len(mapId) > 0):
	            mappingIds = [int(x) for x in row[1][:-1].split(',')]
	            if (mapping_id not in mappingIds) :
	                mappingIds.append(mappingId)
	            _statutoryMappingId = ','.join(str(x) for x in mappingIds) + ","
	        query = "UPDATE tbl_statutories set statutory_mapping_ids = '%s', updated_by = %s \
	            WHERE statutory_id = %s" % (
	            _statutoryMappingId, updated_by, statutory_id
	        )
	        isUpdated = self._db.execute(query)
	    return isUpdated


	### Compliance ###
	def get_compliances_by_ids(self, compliance_ids) :
	    if type(compliance_ids) == IntType :
	        qry = " WHERE t1.compliance_id = %s" %  compliance_ids
	    else :
	        # ids = (int(x) for x in complianceIds.split(','))
	        if (len(compliance_ids) == 1):
	            qry = " WHERE t1.compliance_id in (%s)" % compliance_ids[0]
	        else :
	            qry = " WHERE t1.compliance_id in %s" % str(tuple(compliance_ids))

	    query = "SELECT t1.compliance_id, t1.statutory_provision, t1.compliance_task, \
	        t1.compliance_description, t1.document_name, t1.format_file, t1.penal_consequences, \
	        t1.compliance_frequency, t1.statutory_dates, t1.repeats_every, t1.repeats_type, \
	        t1.duration, t1.duration_type, t1.is_active \
	        FROM tbl_compliances t1 %s" % qry
	    return self._db.execute_and_return(query)

	def save_compliance(self, mapping_id, datas, created_by) :
	    complianceIds = []
	    for data in datas :
	        compliance_id = self.getNewId("compliance_id", "tbl_compliances")
	        created_on = self.getDateTime()

	        statutory_provision = data.get("statutory_provision")
	        compliance_task = data.get("compliance_task")
	        compliance_description = data.get("description")
	        document_name = data.get("document")
	        format_file = data.get("format_file_name")
	        penal_consequences = data.get("penal_consequences")
	        compliance_frequency = data.get("compliance_frequency")
	        statutory_dates =  json.dumps(data.get("statutory_dates"))
	        repeats_every = data.get("repeats_every")
	        repeats_type = data.get("repeats_type")
	        duration = data.get("duration")
	        duration_type = data.get("duration_type")
	        is_active = data.get("is_active")

	        if compliance_frequency == "OneTime" :
	            query = "INSERT INTO tbl_compliances (compliance_id, statutory_provision, \
	                compliance_task, compliance_description, document_name, format_file, \
	                penal_consequences, compliance_frequency, statutory_dates, statutory_mapping_id, \
	                is_active, created_by, created_on) VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
	                '%s', %s, %s, %s, '%s')" % (compliance_id, statutory_provision, compliance_task, 
	                compliance_description, document_name, format_file, penal_consequences, compliance_frequency,
	                statutory_dates, mapping_id, is_active, created_by, created_on)

	        elif compliance_frequency == "OnOccurrence" :
	            query = "INSERT INTO tbl_compliances (compliance_id, statutory_provision, \
	                compliance_task, compliance_description, document_name, format_file, \
	                penal_consequences, compliance_frequency, statutory_dates, duration, \
	                duration_type, statutory_mapping_id, \
	                is_active, created_by, created_on) VALUES (%s,'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, \
	                '%s', %s, %s, %s, '%s')" % (compliance_id, statutory_provision, compliance_task, 
	                compliance_description, document_name, format_file, penal_consequences, compliance_frequency,
	                statutory_dates, int(duration), duration_type, mapping_id, is_active, created_by, created_on)

	        else :
	            query = "INSERT INTO tbl_compliances (compliance_id, statutory_provision, \
	                compliance_task, compliance_description, document_name, format_file, \
	                penal_consequences, compliance_frequency, statutory_dates, repeats_every, \
	                repeats_type, statutory_mapping_id, \
	                is_active, created_by, created_on) VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
	                %s, '%s', %s, %s, %s, '%s')"  % (compliance_id, statutory_provision, compliance_task, 
	                compliance_description, document_name, format_file, penal_consequences, compliance_frequency,
	                statutory_dates, int(repeats_every), repeats_type, mapping_id, is_active, created_by, created_on)

	        if (self._db.execute(query)) :
	            complianceIds.append(compliance_id)

	    return complianceIds

	def update_compliance(self, mapping_id, datas, updated_by) :
	    complianceIds = []
	    for data in datas :
	        compliance_id = data.get("compliance_id")
	        statutory_provision = data.get("statutory_provision")
	        compliance_task = data.get("compliance_task")
	        compliance_description = data.get("description")
	        document_name = data.get("document")
	        format_file = data.get("format_file_name")
	        penal_consequences = data.get("penal_consequences")
	        compliance_frequency = data.get("compliance_frequency")
	        statutory_dates =  json.dumps(data.get("statutory_dates"))
	        repeats_every = data.get("repeats_every")
	        repeats_type = data.get("repeats_type")
	        duration = data.get("duration")
	        duration_type = data.get("duration_type")
	        is_active = data.get("is_active")

	        if compliance_frequency == "OneTime" :
	            query = "UPDATE tbl_compliances set statutory_provision = '%s', \
	                compliance_task = '%s', compliance_description = '%s', document_name = '%s' , format_file = '%s', \
	                penal_consequences = '%s', compliance_frequency = '%s', statutory_dates = '%s', statutory_mapping_id = %s, \
	                is_active = %s, updated_by = %s WHERE compliance_id = %s "  % (
	                    statutory_provision, compliance_task, 
	                    compliance_description, document_name, format_file, penal_consequences, compliance_frequency,
	                    statutory_dates, mapping_id, is_active, updated_by, compliance_id
	                )

	        elif compliance_frequency == "OnOccurrence" :
	            query = "UPDATE tbl_compliances set statutory_provision='%s', \
	                compliance_task='%s', compliance_description='%s', document_name='%s', format_file='%s', \
	                penal_consequences='%s', compliance_frequency='%s', statutory_dates='%s', duration=%s, \
	                duration_type='%s', statutory_mapping_id = %s, \
	                is_active = %s, updated_by = %s WHERE compliance_id = %s "% (
	                    statutory_provision, compliance_task, 
	                    compliance_description, document_name, format_file, penal_consequences, compliance_frequency,
	                    statutory_dates, int(duration), duration_type, mapping_id, is_active, updated_by, compliance_id
	                )

	        else :
	            query = "UPDATE tbl_compliances set statutory_provision ='%s', \
	                compliance_task ='%s', compliance_description='%s', document_name='%s', format_file='%s', \
	                penal_consequences='%s', compliance_frequency='%s', statutory_dates='%s', repeats_every=%s, \
	                repeats_type='%s', statutory_mapping_id=%s, \
	                is_active=%s, updated_by=%s WHERE compliance_id = %s "  % (
	                    statutory_provision, compliance_task, 
	                    compliance_description, document_name, format_file, penal_consequences, compliance_frequency,
	                    statutory_dates, int(repeats_every), repeats_type, mapping_id, is_active, updated_by, compliance_id
	                )

	        if (self._db.execute(query)) :
	            complianceIds.append(compliance_id)

	    return complianceIds

	def change_compliance_status(self, mapping_id, is_active, updated_by) :
	    query = "UPDATE tbl_compliances set is_active=%s, \
	        updated_by=%s WHERE statutory_mapping_id=%s" % (
	            is_active, updated_by, mapping_id
	        )
	    return self._db.execute(query)

	### Stautory Mapping ###
	def get_stautory_mappings(self) :
	    query = "SELECT t1.statutory_mapping_id, t1.country_id, t2.country_name, t1.domain_id,  \
	        t3.domain_name, t1.industry_ids, t1.statutory_nature_id, t4.statutory_nature_name, \
	        t1.statutory_ids, t1.compliance_ids, t1.geography_ids, t1.approval_status, t1.is_active  \
	        FROM tbl_statutory_mappings t1 \
	        INNER JOIN tbl_countries t2 on t1.country_id = t2.country_id \
	        INNER JOIN tbl_domains t3 on t1.domain_id = t3.domain_id \
	        INNER JOIN tbl_statutory_natures t4 on t1.statutory_nature_id = t4.statutory_nature_id "
	    return self._db.execute_and_return(query)

	def get_statutory_mappings_by_id (self, mapping_id) :
	    query = "SELECT t1.country_id, t2.country_name, t1.domain_id,  \
	        t3.domain_name, t1.industry_ids, t1.statutory_nature_id, t4.statutory_nature_name, \
	        t1.statutory_ids, t1.compliance_ids, t1.geography_ids, t1.approval_status  \
	        FROM tbl_statutory_mappings t1 \
	        INNER JOIN tbl_countries t2 on t1.country_id = t2.country_id \
	        INNER JOIN tbl_domains t3 on t1.domain_id = t3.domain_id \
	        INNER JOIN tbl_statutory_natures t4 on t1.statutory_nature_id = t4.statutory_nature_id \
	        WHERE t1.statutory_mapping_id=%s" % mapping_id
	    rows = self._db.execute_and_return(query)
	    return rows[0]


	def save_statutory_mapping(self, data, created_by) :
	    country_id =data.get("country_id")
	    domain_id =data.get("domain_id")
	    industry_ids = ','.join(str(x) for x in data.get("industry_ids")) + ","
	    nature_id =data.get("statutory_nature_id")
	    statutory_ids = ','.join(str(x) for x in data.get("statutory_ids")) + ","
	    compliances = data.get("compliances")
	    geography_ids = ','.join(str(x) for x in data.get("geography_ids")) + ","
	    
	    statutory_mapping_id = self.getNewId("statutory_mapping_id", "tbl_statutory_mappings")
	    created_on = self.getDateTime()
	    is_active = 1

	    query = "INSERT INTO tbl_statutory_mappings (statutory_mapping_id, country_id, \
	        domain_id, industry_ids, statutory_nature_id, statutory_ids, geography_ids,\
	        is_active, created_by, created_on) \
	        VALUES (%s, %s, %s, '%s', %s, '%s', '%s', %s, %s, '%s' )" % (
	            statutory_mapping_id, country_id, domain_id, industry_ids, nature_id, statutory_ids,
	            geography_ids, is_active, created_by, created_on
	        )
	    if (self._db.execute(query)) :
	        self.update_statutory_mapping_id(data.get("statutory_ids"), statutory_mapping_id, created_by)
	        ids = self.save_compliance(statutory_mapping_id, compliances, created_by)
	        compliance_ids = ','.join(str(x) for x in ids) + ","
	        qry = "UPDATE tbl_statutory_mappings set compliance_ids='%s' \
	            where statutory_mapping_id = %s" % (compliance_ids, statutory_mapping_id)
	        self._db.execute(qry)
	        action = "Add Statutory Mappings"
	        self.add_activity_log(created_by, 17, action)
	        return True
	    else :
	        return False


	def update_statutory_mapping(self, data, updated_by) :
	    statutory_mapping_id = data.get("statutory_mapping_id")
	    country_id =data.get("country_id")
	    domain_id =data.get("domain_id")
	    industry_ids = ','.join(str(x) for x in data.get("industry_ids")) + ","
	    nature_id =data.get("statutory_nature_id")
	    statutory_ids = ','.join(str(x) for x in data.get("statutory_ids")) + ","
	    compliances = data.get("compliances")
	    geography_ids = ','.join(str(x) for x in data.get("geography_ids")) + ","

	    self.save_statutory_backup(statutory_mapping_id, updated_by)
	    query = "UPDATE tbl_statutory_mappings set country_id=%s, domain_id=%s, industry_ids='%s', \
	        statutory_nature_id=%s, statutory_ids='%s', geography_ids='%s', updated_by=%s \
	        WHERE statutory_mapping_id=%s" % (
	            country_id, domain_id, industry_ids, nature_id, statutory_ids, geography_ids,
	            updated_by, statutory_mapping_id
	        )
	    if (self._db.execute(query)) :
	        self.update_statutory_mapping_id(data.get("statutory_ids"), statutory_mapping_id, updated_by)
	        ids = self.update_compliance(statutory_mapping_id, compliances, updated_by)
	        compliance_ids = ','.join(str(x) for x in ids) + ","
	        qry = "UPDATE tbl_statutory_mappings set compliance_ids='%s' \
	            where statutory_mapping_id = %s" % (compliance_ids, statutory_mapping_id)
	        self._db.execute(qry)
	        action = "Edit Statutory Mappings"
	        self.add_activity_log(user_id, 17, action)
	        return True
	    else :
	        return False

	def change_statutory_mapping_status(self, data, updated_by):
	    statutory_mapping_id = data.get("statutory_mapping_id")
	    is_active = data.get("is_active")

	    query = "UPDATE tbl_statutory_mappings set is_active=%s, updated_by=%s \
	        WHERE statutory_mapping_id=%s" % (
	        is_active, updated_by, statutory_mapping_id
	    )
	    if (self._db.execute(query)) :
	        self.change_compliance_status(statutory_mapping_id, is_active, updated_by)
	        if is_active == 0:
	            status = "deactivated"
	        else:
	            status = "activated"
	        action = "Statutory Mapping status changed"
	        self.add_activity_log(updated_by, 17, action)
	        return True

	def change_approval_status(self, data, updated_by) :
	    statutory_mapping_id = data.get("statutory_mapping_id")
	    approval_status = data.get("approval_status")
	    rejected_reason = data.get("rejected_ reason")
	    notification_text = data.get("notification_text")

	    if approval_status == "Reject" :
	        query = "UPDATE tbl_statutory_mappings set approval_status='%s', rejected_reason='%s', \
	            updated_by=%s WHERE statutory_mapping_id = %s" % (
	                approval_status, rejected_reason, updated_by, statutory_mapping_id
	            )
	    elif approval_status == "Approve" :
	        query = "UPDATE tbl_statutory_mappings set approval_status='%s', \
	            updated_by=%s WHERE statutory_mapping_id = %s" % (
	                approval_status, updated_by, statutory_mapping_id
	            )
	    else :
	        query = "UPDATE tbl_statutory_mappings set approval_status='%s', \
	            updated_by=%s WHERE statutory_mapping_id = %s" % (
	                approval_status, updated_by, statutory_mapping_id
	            )
	        # if (self.dataInsertUpdate(query)) :

	    self._db.execute(query)
	    action = "Statutory Mapping approval status changed"
	    self.add_activity_log(updated_by, 17, action)
	    return True

	def save_statutory_backup(self, statutory_mapping_id, created_by):
	    oldRecord = self.get_statutory_nature_by_id(statutory_mapping_id)
	    backup_id = self.getNewId("statutory_backup_id", "tbl_statutories_backup")
	    created_on = self.getDateTime()
	    industry_name = self.get_industry_by_industry_id(oldRecord[4])

	    statutory_provision = []
	    for sid in oldRecord[7][:-1].split(',') :
	        data = self.allStatutories.get(int(sid))
	        statutory_provision.append(data[1])
	    mappings = ','.join(str(x) for x in statutory_provision)
	    geoMap = []
	    for gid in oldRecord[8][:-1].split(',') :
	        data = self.allGeographies.get(int(gid))
	        geoMap.append(data[1])
	    geoMappings = ','.join(str(x) for x in geoMap)
	    query = "INSERT INTO tbl_statutories_backup(statutory_backup_id, country_name, domain_name, industry_name, \
	        statutory_nature, statutory_provision, applicable_location, updated_by, updated_on) \
	        VALUES(%s, '%s', '%s', '%s', '%s', '%s', '%s', %s, '%s') " % (
	            backup_id, oldRecord[1], oldRecord[3], industry_name, oldRecord[6], mappings, geoMappings,
	            created_by, created_on
	        )
	    if (self._db.execute(query)) :
	        qry = " INSERT INTO tbl_compliances_backup(statutory_backup_id, statutory_provision, \
	            compliance_task, compliance_description, document_name, format_file, \
	            penal_consequences, compliance_frequency, statutory_dates, repeats_every, \
	            repeats_type, duration, duration_type)  \
	            SELECT %s,t1.statutory_provision, t1.compliance_task, t1.compliance_description, \
	            t1.document_name, t1.format_file, t1.penal_consequences, t1.compliance_frequency, \
	            t1.statutory_dates, t1.repeats_every, t1.repeats_type, t1.duration, t1.duration_type \
	            FROM tbl_compliances t1 WHERE statutory_mapping_id=%s" % (backup_id, statutory_mapping_id)
	        self._db.execute(qry)


	def get_statutory_mapping_report(self, country_id, domain_id, industry_id, statutory_nature_id, geography_id) :
	    query = "SELECT t1.statutory_mapping_id, t1.country_id, t1.domain_id,  \
	        t1.industry_ids, t1.statutory_nature_id, t1.statutory_ids, t1.compliance_ids, \
	        t1.geography_ids, t1.approval_status, t1.is_active  \
	        FROM tbl_statutory_mappings t1 \
	        WHERE t1.country_id = %s and t1.domain_id = %s and t1.industry_ids like '%s' and \
	        t1.statutory_nature_id like '%s' and t1.geography_ids like '%s'" % (
	            country_id, domain_id, str("%" + str(industry_id) + ",%"), str(statutory_nature_id),
	            str("%" + str(geography_id) + ",%")
	        )
	    return self._db.execute(query)

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
		elif form == "UserGroupMaster":
			tbl_name = self._db.tblUserGroups
			column = "user_group_id"
		elif form == "UserMaster":
			tbl_name = self._db.tblUsers
			column = "user_id"
		else:
			print "Error : Cannot generate new id for form %s" % form

		return self._db.generate_new_id(tbl_name, column)

	def is_duplicate(self, form, field, value, id_value):
		tbl_name = None
		condition = None
		if form == "User":
			tbl_name = self._db.tblUsers
			if field == "email":
				condition = "username ='%s' AND user_id != '%d'" %(
           value, id_value)
		elif form == "UserGroupMaster":
			tbl_name = self._db.tblUserGroups
			if field == "name":
				condition = "user_group_name = '%s' AND user_group_id != '%d'" %(
					value, id_value)
		elif form == "UserMaster":
			tbl_name = self._db.tblUserDetails
			if field == "email":
				condition = "email_id = '%s' AND user_id != '%d'" %(
					value, id_value)
			elif field == "contact_no":
				condition = "contact_no = '%s' AND user_id != '%d'" %(
					value, id_value)
			elif field == "employee_code":
				condition = "employee_code = '%s' AND user_id != '%d'" %(
					value, id_value)
		return self._db.is_already_exists(tbl_name, condition)

	def is_id_invalid(self, form, id_value):
		tbl_name = None
		condition = None
		if form == "User":
			tbl_name = self._db.tblUsers
			condition = "user_id = '%d'" % id_value
		elif form == "UserGroupMaster":
			tbl_name = self._db.tblUserGroups
			condition = "user_group_id = '%d'" % id_value
		elif form == "UserMaster":
			tbl_name = self._db.tblUsers
			condition = "user_id = '%d'" % id_value
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
		columns = ["country_id", "country_name", "is_active"]
		condition = "1"
		rows = self._db.get_data(self._db.tblCoutries,columns, 
			condition)
		return rows		

#
#	Domain
#
	def get_domains(self):
		columns = ["domain_id", "domain_name", "is_active"]
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
#	User Group
#
	def get_user_group_details_list(self):
		columns = ["user_group_id", "user_group_name","form_type", 
                    "form_ids", "is_active"]
		condition = "1"
		rows = self._db.get_data(self._db.tblUserGroups, columns, condition)
		return rows

	def get_user_group_list(self):
		columns = ["user_group_id", "user_group_name", "is_active"]
		condition = "1"
		rows = self._db.get_data(self._db.tblUserGroups, columns, condition)
		return rows

	def save_user_group(self, user_group, session_user):
		columns = ["user_group_id", "user_group_name","form_type", "form_ids", "is_active",
                  "created_on", "created_by", "updated_on", "updated_by"]
		form_ids = ",".join(str(x) for x in user_group.form_ids)
		values_list =  [(user_group.user_group_id, user_group.user_group_name, user_group.form_type,
        				form_ids, user_group.is_active, current_timestamp(), 
        				session_user,current_timestamp(), session_user)]
		update_columns_list = ["user_group_name","form_type", "form_ids", 
        						"updated_on", "updated_by"]
		return self._db.on_duplicate_key_update(self._db.tblUserGroups, 
			columns, values_list, update_columns_list)

	def change_user_group_status(self, user_group_id, is_active, session_user):
		timestamp = current_timestamp()
		columns = ["is_active", "updated_on" , "updated_by"]
		values = [is_active, timestamp, session_user]
		condition = "user_group_id='%d'" % user_group_id
		return self._db.update(self._db.tblUserGroups, columns, values, condition)
#
#	User
#
	def save_user(self, user, session_user):
		timestamp = current_timestamp()
		columns = "user_id, username, password, created_on,"+\
					"created_by,updated_on, updated_by"
		values = [(user.user_id, user.email_id, generate_password(), 
        		timestamp,session_user, timestamp,session_user)]
		return self._db.insert(self._db.tblUsers, columns, values)

	def get_form_type(self, user_group_id) :
		column = ["form_type"]
		condition = "user_group_id='%d'" % user_group_id
		rows = self._db.get_data(self._db.tblUserGroups, 
                    column, condition)
		return rows[0][0]

	def save_user_details(self, user, session_user):
		timestamp = current_timestamp()
		columns = ["user_id", "email_id", "user_group_id", "form_type", "employee_name", 
                  "employee_code", "contact_no", "address", "designation", "country_ids",
                  "domain_ids", "created_on", "created_by", "updated_on", "updated_by"]
		form_type = self.get_form_type(user.user_group_id)
		country_ids = ",".join(str(x) for x in user.country_ids)
		domain_ids = ",".join(str(x) for x in user.domain_ids)
		values_list =  [(user.user_id, user.email_id, user.user_group_id,
        				form_type, user.employee_name, user.employee_code, 
        				user.contact_no, user.address, user.designation, 
        				country_ids, domain_ids, timestamp, session_user,
        				timestamp, session_user)]
		update_columns_list = ["user_group_id", "form_type","employee_name", 
					"employee_code", "contact_no", "address", "designation", 
					"country_ids", "domain_ids","updated_on", "updated_by"]
		return self._db.on_duplicate_key_update(self._db.tblUserDetails, 
			columns, values_list, update_columns_list)

	def change_user_status(self, user_id, is_active, session_user):
		columns = ["is_active", "updated_on" , "updated_by"]
		values = [is_active, current_timestamp(), session_user]
		condition = "user_id='%d'" % user_id
		return self._db.update(self._db.tblUsers, columns, values,
			condition)

	def get_user_details_list(self):
		columns = ["user_id", "email_id", "user_group_id", "employee_name",
				"employee_code","contact_no", "address", "designation", 
				"country_ids","domain_ids","client_ids", "is_active"]
		condition = "1"                                
		rows = self._db.get_data(self._db.tblUserDetails, columns, condition)
		return rows

	def get_user_list(self):
		columns = "user_id, employee_name, employee_code, is_active"
		condition = "1"
		rows = self._db.get_data(self._db.tblUserDetails, columns, conditions)
		return rows
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
		elif ((form == "User") or (form == "UserMaster")):
			if action_type == "save":
				action = "User %s has been created" % obj
			elif action_type == "update":
				action = "User %s has been updated" % obj
			elif action_type == "status_change":
				action = "Status of User %s has been updated" % str(obj)
			elif action_type == "admin_status_change":
				action = "Admin Status of User Privilege %s has been updated" % str(obj)
		elif form == "UserGroupMaster":
			if action_type == "save":
				action = "User Group %s has been created" % obj
			elif action_type == "update":
				action = "User Group %s has been updated" % obj
			elif action_type == "status_change":
				action = "Status of User Group %s has been updated" % str(obj)
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
