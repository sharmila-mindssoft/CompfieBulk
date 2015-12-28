import datetime
import MySQLdb as mysql

__all__ = [
	"DatabaseHandler"
]

class DatabaseHandler(object) :

	def __init__(self):
		self.mysqlHost = "localhost"
		self.mysqlUser = "root"
		self.mysqlPassword = "123456"
		self.mysqlDatabase = "mirror_knowledge"

	def dbConnect(self) :
		return mysql.connect(
			self.mysqlHost, self.mysqlUser, 
			self.mysqlPassword, self.mysqlDatabase
		)

	def execute(self, query):
		con = None
		cursor = None
		isComplete = True
		try:
			con = self.dbConnect()
			cursor = con.cursor()
			cursor.execute(query)
			con.commit()

		except mysql.Error, e:
			print ("Error:%s - %s" % (query, e))
			isComplete = False

		finally:
			if cursor is not None :
				cursor.close()
			if con is not None :
				con.close()

		return isComplete

	def execute_and_return(self, query) :
		con = None
		cursor = None
		result = None
		try:
			con = self.dbConnect()
			cursor = con.cursor()
			cursor.execute(query)
			result = cursor.fetchall()

		except mysql.Error, e:
			print ("Error:%s - %s" % (query, e))

		finally:
			if cursor is not None :
				cursor.close()
			if con is not None :
				con.close()

		return result

	def get_data(self, table, columns, condition):
		# query = "SELECT "+columns+" FROM "+table+" WHERE "+condition 
		query = "SELECT %s FROM %s WHERE %s "  % (table, columns, condition)
		return self.execute_and_return(query)

	def get_data_from_multiple_tables(self, columns, tables, aliases, joinType, joinConditions, whereCondition):

		query = "SELECT %s FROM " % columns

		for index,table in enumerate(tables):
			if index == 0:
				query += "%s  %s  %s" % (table, aliases[index], joinType)
			elif index <= len(tables) -2:
				query += " %s %s on (%s) %s " % (table, aliases[index], joinConditions[index-1], joinType)
			else:
				query += " %s %s on (%s)" % (table, aliases[index],joinConditions[index-1])

		query += " where %s" % whereCondition
		print query
		return self.execute_and_return(query)


	def verify_login(self, username, password):
		tblAdminCondition = "password='%s' and user_name='%s'" % (password, username)
		adminDetails = self.get_data("tbl_admin", "*", tblAdminCondition)
		if (len(adminDetails) == 0) :
			query = "SELECT t1.user_id, t1.user_group_id, t1.email_id, \
				t1.employee_name, t1.employee_code, t1.contact_no, t1.address, t1.designation \
				t2.user_group_name, t2.form_ids \
				FROM tbl_users t1 INNER JOIN tbl_user_groups t2\
				ON t1.user_group_id = t2.user_group_id \
				WHERE t1.password='%s' and t1.email_id='%s'" % (password, username)
			return self.execute_and_return(query)
		else :
			return True

	def getNewId(self, field , tableName) :
		newId = 1
		query = "SELECT max(%s) from %s " % (field, tableName)

		rows = self.execute_and_return(query)
		for row in rows :
			if row[0] is not None :
				newId = int(row[0]) + 1
		return newId

	def saveCountry(self, countryName, createdBy) :
		createdOn = self.getDateTime()
		countryId = self.getNewId("country_id", "tbl_countries")
		isActive = 1

		query = "INSERT INTO tbl_countries(country_id, country_name, \
			is_active, created_by, created_on) VALUES (%s, '%s', %s, %s, '%s') " % (
			countryId, countryName, isActive, createdBy, createdOn
		)
		self.execute(query)
		# action = "Add Country - \"%s\"" % countryName
		# self.saveActivity(createdBy, 4, action)
		return True

	def add_session(self, user_id) :
		session_id = self.new_uuid()
		query = "insert into tbl_user_sessions values ('%s', '%s', '%d');"
		query = query % (session_id, user_id, current_timestamp())
		self._db.execute(query)
		return session_id

	def getUserForms(self, formIds):
		forms = []

		columns = "tf.form_id, tf.form_category_id, tfc.form_category, tf.form_type_id, tft.form_type,"+\
		"tf.form_name, tf.form_url, tf.form_order, tf.parent_menu"
		tables = [self.tblForms, self.tblFormCategory, self.tblFormType]
		aliases = ["tf", "tfc", "tft"]
		joinConditions = ["tf.form_category_id = tfc.form_category_id", "tf.form_type_id = tft.form_type_id"]
		whereCondition = " tf.form_id in ('%s') order by tf.form_order" % (formIds)
		joinType = "left join"

		rows = self.get_data_from_multiple_tables(columns, tables, aliases, joinType, 
			joinConditions, whereCondition)
		return rows 

