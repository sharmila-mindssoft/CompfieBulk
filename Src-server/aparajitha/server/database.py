import MySQLdb

HOST = "localhost"
USER = "root"
PASSWORD = "123456"

class Database(object) :

	### Knowledge Tables ###
	tblActivityLog = "tbl_activity_log"
	tblUsers = "tbl_users"
	tblForms = "tbl_forms"

	### Client Tables ###
	tblServiceProviders = "tbl_service_providers"
	tblClientUserGroups = "tbl_client_user_groups"

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

	def isAlreadyExists(self, table, condition) :
		query = "SELECT count(*) FROM %s WHERE %s" %(table, condition)
		rows = self.executeAndReturn(query)
		if rows[0][0] > 0:
			return True
		else :
			return False

	def getData(self, table, columns, condition):
		query = "SELECT %s FROM %s WHERE %s" %  (columns, 
			table, condition) 
		return self.executeAndReturn(query)

	def insert(self, table, columns, valueList) :
		query = "INSERT INTO %s (%s)  VALUES" % (table, columns)
		for index, value in enumerate(valueList):
			if index < len(valueList)-1:
				query += " %s," % str(value)
			else:
				query += str(value)
		return self.execute(query) 

	def update(self, table, columns, values, condition) :
		query = "UPDATE "+table+" set "
		for index,column in enumerate(columns):
			if index < len(columns)-1:
				query += column+" = '"+str(values[index])+"', "
			else:
				query += column+" = '"+str(values[index])+"' "
		query += " WHERE "+condition
		return self.execute(query)

	def generateNewId(self, table, column):
		query = "SELECT max(%s) FROM %s" % (column, table)
		rows = self.executeAndReturn(query)
		for row in rows :
			newId = row[0] + 1 if row[0] != None else 1
		return int(newId)

	def onDuplicateKeyUpdate(self, table, columns, valueList, 
    	updateColumnsList):
		query = "INSERT INTO %s (%s) VALUES " % (table, columns)

		for index, value in enumerate(valueList):
			if index < len(valueList)-1:
				query += "%s," % str(value)
			else:
				query += "%s" % str(value)

		query += " ON DUPLICATE KEY UPDATE "

		for index, updateColumn in enumerate(updateColumnsList):
			if index < len(updateColumnsList)-1:
				query += "%s = VALUES(%s)," % (updateColumn, updateColumn)
			else:
				query += "%s = VALUES(%s)" % (updateColumn, updateColumn)
		print query
		return self.execute(query)



