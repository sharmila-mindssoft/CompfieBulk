import MySQLdb

HOST = "localhost"
USER = "root"
PASSWORD = "123456"

class Database(object) :

	### Knowledge Tables ###
	tblActivityLog = "tbl_activity_log"
	tblUsers = "tbl_users"
	tblForms = "tbl_forms"
	tblCoutries = "tbl_countries"
	tblDomains = "tbl_domains"
	tblUserDetails = "tbl_user_details"
	tblUserGroups = "tbl_user_groups"

	### Client Tables ###
	tblServiceProviders = "tbl_service_providers"
	tblClientUserGroups = "tbl_client_user_groups"
	tblBusinessGroup = "tbl_business_groups"
	tblLegalEntity = "tbl_legal_entities"
	tblDivision = "tbl_divisions"
	tblUnit = "tbl_units"
	tblClientUserDetails = "tbl_client_user_details"

	def __init__(self, database) :
		self._database = database

	def execute(self, query) :
		db = None
		cursor = None
		isComplete = True
		try:
			db = MySQLdb.connect(HOST, USER, PASSWORD, self._database)
			cursor = db.cursor()
			cursor.execute(query)
			db.commit()
		except Exception, e:
			isComplete = False
			raise
		finally:
			if db is not None:
				db.close()
			if cursor is not None:
				cursor.close()
		return isComplete

	def execute_and_return(self, query) :
		db = None
		cursor = None
		try:
			db = MySQLdb.connect(HOST, USER, PASSWORD, self._database)
			cursor = db.cursor()
			cursor.execute(query)
			result = cursor.fetchall()
			db.commit()
			return result
		except Exception, e:
			raise
		finally:
			if db is not None:
				db.close()
			if cursor is not None:
				cursor.close()

	def is_already_exists(self, table, condition) :
		query = "SELECT count(*) FROM %s WHERE %s" %(table, condition)
		print query
		rows = self.execute_and_return(query)
		if rows[0][0] > 0:
			return True
		else :
			return False

	def get_data(self, table, columns, condition):
		columns = ",".join(columns)
		query = "SELECT %s FROM %s WHERE %s" %  (columns, 
			table, condition) 
		print query
		return self.execute_and_return(query)

	def insert(self, table, columns, value_list) :
		query = "INSERT INTO %s (%s)  VALUES " % (table, columns)
		for index, value in enumerate(value_list):
			if index < len(value_list)-1:
				query += " %s," % str(value)
			else:
				query += str(value)
		print query
		return self.execute(query) 

	def update(self, table, columns, values, condition) :
		query = "UPDATE "+table+" set "
		for index,column in enumerate(columns):
			if index < len(columns)-1:
				query += column+" = '"+str(values[index])+"', "
			else:
				query += column+" = '"+str(values[index])+"' "
		query += " WHERE "+condition
		print query
		return self.execute(query)

	def generate_new_id(self, table, column):
		query = "SELECT max(%s) FROM %s" % (column, table)
		rows = self.execute_and_return(query)
		for row in rows :
			newId = row[0] + 1 if row[0] != None else 1
		return int(newId)

	def on_duplicate_key_update(self, table, columns, value_list, 
    	update_column_list):
		columns = ",".join(columns)
		query = "INSERT INTO %s (%s) VALUES " % (table, columns)

		for index, value in enumerate(value_list):
			if index < len(value_list)-1:
				query += "%s," % str(value)
			else:
				query += "%s" % str(value)

		query += " ON DUPLICATE KEY UPDATE "

		for index, update_column in enumerate(update_column_list):
			if index < len(update_column_list)-1:
				query += "%s = VALUES(%s)," % (update_column, update_column)
			else:
				query += "%s = VALUES(%s)" % (update_column, update_column)
		print query
		return self.execute(query)

	def get_data_from_multiple_tables(self, columns, tables, conditions, join_type):
		columns = ",".join(columns)
		query = "SELECT %s FROM " % columns
		for index,table in enumerate(tables):
			if index == 0:
				query += "%s alias%d  %s" % (table, index, join_type)
			elif index <= len(tables) -2:
				query += " %s alias%d on (alias%d.%s = alias%d.%s) %s " % (table, 
                    index, index-1, conditions[index-1][0], index, 
                    conditions[index-1][1], join_type)
			else:
				query += " %s alias%d on (alias%d.%s = alias%d.%s)" % (table, index,
                    index-1, conditions[index-1][0], index, conditions[index-1][1])
		return self.execute_and_return(query)	



