import MySQLdb

HOST = "localhost"
USER = "root"
PASSWORD = "mysql-dl"

class Database(object) :
	def __init__(self, database) :
		self._database = database

	def execute(self, query) :
		db = None
		cursor = None
		try:
			db = MySQLdb.connect(HOST, USER, PASSWORD, self._database)
			cursor = db.cursor()
			cursor.execute(query)
			db.commit()
		except Exception, e:
			raise
		finally:
			if db is not None:
				db.close()
			if cursor is not None:
				cursor.close()

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