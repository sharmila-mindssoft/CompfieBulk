import datetime
import MySQLdb as mysql

__all__ = [
	"KnowledgeDatabase", "ClientDatabase"
]


class Database(object) :
	def __init__(
		self, 
		mysqlHost, mysqlUser, 
		mysqlPassword, mysqlDatabase
	):
		self._mysqlHost = mysqlHost
		self._mysqlUser = mysqlUser
		self._mysqlPassword = mysqlPassword
		self._mysqlDatabase = mysqlDatabase
		self._connection = None
		self._cursor = None 

	def cursor(self):
		return self._cursor
 
	def connect(self):
		assert self._connection is None
		connection = mysql.connect(
			self._mysqlHost, self._mysqlUser, 
			self._mysqlPassword, self._mysqlDatabase
		)
		connection.autocommit(False)
		self._connection = connection

	def close(self):
		assert self._connection is not None
		self._connection.close()
		self._connection = None

	def begin(self):
		self.connect()
		assert self._connection is not None
		assert self._cursor is None
		self._cursor = self._connection.cursor()
		print self._cursor
		return self._cursor

	def commit(self):
		assert self._connection is not None
		assert self._cursor is not None
		self._cursor.close()
		self._connection.commit()
		self._cursor = None
		self.close()

	def rollback(self):
		assert self._connection is not None
		assert self._cursor is not None
		self._cursor.close()
		self._connection.rollback()
		self._cursor = None
		self.close()

	def select_all(self, query) :
		cursor = self.cursor()
		assert cursor is not None
		cursor.execute(query)
		return cursor.fetchall()

	def select_one(self, query) :
		cursor = self.cursor()
		assert cursor is not None
		cursor.execute(query)
		return cursor.fetchone()

	def execute(self, query) :
		cursor = self.cursor()
		assert cursor is not None
		cursor.execute(query)

class KnowledgeDatabase(Database):
	def __init__(
		self, 
		mysqlHost, mysqlUser, 
		mysqlPassword, mysqlDatabase
	):
		super(KnowledgeDatabase, self).__init__(
			mysqlHost, mysqlUser, mysqlPassword, mysqlDatabase
		)

	# def get_user(self, userid):
	#   query = "select * from users"
	#   return self.select_all(query)

	# def insert_user(self, username, user_id):
	#   query = "INSERT INTO USERS(username, user_id) VALUES (%s, %s)" % (
	#       username, user_id
	#   )
	#   self.execute(query)

	# def update_user(self, username, user_id):
	#   query = "UPDATE USERS SET username= %s WHERE user_id = %s" % (
	#       username, user_id
	#   )
	#   self.execute(query)

	def validate_session_token(self, session_token) :
		query = "SELECT user_id FROM tbl_user_sessions \
			WHERE session_token = '%s'" % (session_token)
		print query
		row = self.select_one(query)
		print row
		if row[0] is not None :
			return row[0]
		return None

	def get_domains_for_user(self, userId) :
		query = "SELECT distinct t1.domain_id, t1.domain_name, t1.is_active FROM tbl_domains t1"
		if userId > 0 :
			query = query + " INNER JOIN tbl_user_domains t2 ON t1.domain_id = t2.domain_id WHERE t2.user_id = %s" % (userId)
		rows = self.select_all(query)
		return rows


# class ClientDatabase(Database):
#   def __init__(
#       self, 
#       mysqlHost, mysqlUser, 
#       mysqlPassword, mysqlDatabase
#   ):
#       super(ClientDatabase, self).__init__(
#           mysqlHost, mysqlUser, mysqlPassword, mysqlDatabase
#       )

#   def get_data(self, table, columns, condition):
#       # query = "SELECT "+columns+" FROM "+table+" WHERE "+condition 
#       query = "SELECT %s FROM %s WHERE %s "  % (table, columns, condition)
#       return self.execute_and_return(query)

#   def get_data_from_multiple_tables(self, columns, tables, aliases, joinType, joinConditions, whereCondition):

#       query = "SELECT %s FROM " % columns

#       for index,table in enumerate(tables):
#           if index == 0:
#               query += "%s  %s  %s" % (table, aliases[index], joinType)
#           elif index <= len(tables) -2:
#               query += " %s %s on (%s) %s " % (table, aliases[index], joinConditions[index-1], joinType)
#           else:
#               query += " %s %s on (%s)" % (table, aliases[index],joinConditions[index-1])

#       query += " where %s" % whereCondition
#       print query
#       return self.execute_and_return(query)


#   def verify_login(self, username, password):
#       tblAdminCondition = "password='%s' and user_name='%s'" % (password, username)
#       adminDetails = self.get_data("tbl_admin", "*", tblAdminCondition)
#       if (len(adminDetails) == 0) :
#           query = "SELECT t1.user_id, t1.user_group_id, t1.email_id, \
#               t1.employee_name, t1.employee_code, t1.contact_no, t1.address, t1.designation \
#               t2.user_group_name, t2.form_ids \
#               FROM tbl_users t1 INNER JOIN tbl_user_groups t2\
#               ON t1.user_group_id = t2.user_group_id \
#               WHERE t1.password='%s' and t1.email_id='%s'" % (password, username)
#           return self.execute_and_return(query)
#       else :
#           return True

#   def validate_session_token(self, cursor, session_token) :
#       query = "SELECT user_id FROM tbl_user_sessions \
#           WHERE session_token = '%s'" % (session_token)
#       cursor.execute(query)
#       row = cursor.fetchone()
#       if row[0] is not None :
#           return row[0]
#       return None

#   def add_session(self, user_id) :
#       session_id = self.new_uuid()
#       query = "insert into tbl_user_sessions values ('%s', '%s', '%d');"
#       query = query % (session_id, user_id, current_timestamp())
#       self._db.execute(query)
#       return session_id

#   def get_new_id(self, field , tableName) :
#       newId = 1
#       query = "SELECT max(%s) from %s " % (field, tableName)

#       rows = self.execute_and_return(query)
#       for row in rows :
#           if row[0] is not None :
#               newId = int(row[0]) + 1
#       return newId

#   def get_date_time(self) :
#       return datetime.datetime.now()

#   def save_activity(self, userId, formId, action):
#       createdOn = self.get_date_time()
#       activityId = self.get_new_id("activity_log_id", "tbl_activity_log")
#       query = "INSERT INTO tbl_activity_log(activity_log_id, user_id, form_id, \
#           action, created_on) \
#           VALUES (%s, %s, %s, '%s', '%s')" % (
#               activityId, userId, formId, action, createdOn
#           )
#       self.execute(query)

#   #
#   # Domain
#   #

#   def get_domains_for_user(self, cursor, userId) :
#       query = "SELECT distinct t1.domain_id, t1.domain_name, t1.is_active FROM tbl_domains t1"
#       if userId > 0 :
#           query = query + " INNER JOIN tbl_user_domains t2 ON t1.domain_id = t2.domain_id WHERE t2.user_id = %s" % (userId)
#       cursor.execute(query)
#       rows = cursor.fetchall()
#       return rows

#   def check_duplicate_domain(self, domainName, domainId) :
#       isDuplicate = False
#       query = "SELECT count(*) FROM tbl_domains \
#           WHERE LOWER(domain_name) = LOWER('%s') " % domainName
#       if domainId is not None :
#           query = query + " AND domain_id != %s" % domainId
#       rows = self.execute_and_return(query)
#       row = rows[0]

#       if row[0] > 0 :
#           isDuplicate = True

#       return isDuplicate


#   def save_domain(self, domainName, createdBy) :
#       createdOn = self.get_date_time()
#       domainId = self.get_new_id("domain_id", "tbl_domains")
#       isActive = 1

#       query = "INSERT INTO tbl_domains(domain_id, domain_name, is_active, \
#           created_by, created_on) VALUES (%s, '%s', %s, %s, '%s') " % (
#           domainId, domainName, isActive, createdBy, createdOn
#       )

#       self.execute(query)
#       action = "Add Domain - \"%s\"" % domainName
#       self.save_activity(createdBy, 4, action)
#       return True

#   def get_domain_by_id(self, domainId) :
#       q = "SELECT domain_name FROM tbl_domains WHERE domain_id=%s" % domainId
#       row = self.execute_and_return_one(q)
#       print row
#       domainName = row[0]
#       return domainName


#   def update_domain(self, domainId, domainName, updatedBy) :
#       oldData = self.get_domain_by_id(domainId)
#       if oldData is None :
#           return False
#       else :
#           query = "UPDATE tbl_domains SET domain_name = '%s', \
#           updated_by = %s WHERE domain_id = %s" % (
#               domainName, updatedBy, domainId
#           )
#           self.execute(query)
#           action = "Edit Domain - \"%s\"" % domainName
#           self.save_activity(updatedBy, 4, action)
#           return True

#   def update_domain_status(self, domainId, isActive, updatedBy) :
#       oldData = self.get_domain_by_id(domainId)
#       if oldData is None :
#           return False
#       else :
#           query = "UPDATE tbl_domains SET is_active = %s, \
#           updated_by = %s WHERE domain_id = %s" % (
#               isActive, updatedBy, domainId
#           )
#           self.execute(query)
#           if isActive == 0 :
#               status = "deactivated"
#           else:
#               status = "activated"
#           action = "Domain %s status  - %s" % (oldData, status)
#           self.save_activity(updatedBy, 4, action)
#           return True


#   def save_country(self, countryName, createdBy) :
#       createdOn = self.get_date_time()
#       countryId = self.get_new_id("country_id", "tbl_countries")
#       isActive = 1

#       query = "INSERT INTO tbl_countries(country_id, country_name, \
#           is_active, created_by, created_on) VALUES (%s, '%s', %s, %s, '%s') " % (
#           countryId, countryName, isActive, createdBy, createdOn
#       )
#       self.execute(query)
#       action = "Add Country - \"%s\"" % countryName
#       self.save_activity(createdBy, 4, action)
#       return True

#   def get_user_forms(self, formIds):
#       forms = []

#       columns = "tf.form_id, tf.form_category_id, tfc.form_category, tf.form_type_id, tft.form_type,"+\
#       "tf.form_name, tf.form_url, tf.form_order, tf.parent_menu"
#       tables = [self.tblForms, self.tblFormCategory, self.tblFormType]
#       aliases = ["tf", "tfc", "tft"]
#       joinConditions = ["tf.form_category_id = tfc.form_category_id", "tf.form_type_id = tft.form_type_id"]
#       whereCondition = " tf.form_id in ('%s') order by tf.form_order" % (formIds)
#       joinType = "left join"

#       rows = self.get_data_from_multiple_tables(columns, tables, aliases, joinType, 
#           joinConditions, whereCondition)
#       return rows 
