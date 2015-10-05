import MySQLdb as mysql

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "minds"
MYSQL_DATABASE = "aparajitha"

__all__ = [
	"Database"
]

class Database(object) :
	# def __init__(self) :

	def dbConnection(self) :
		return mysql.connect(
			MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
		)

	def commit(self, query) :
		try :
			db = self.dbConnection()
			cursor = db.cursor()
			cursor.execute(query)
			db.commit()
		except mysql.Error, e :
			print e
			print "error while processing commit "
		finally :
			if cursor is  not None :
				cursor.close()
			if db is not None :
				db.close()

	def fetchOne(self, query) :
		try :
			db = self.dbConnection()
			cursor = db.cursor()
			cursor.execute(query)
			result = cursor.fetchone()
			return result
		except mysql.Error, e :
			print "error in fetchOne"
		finally :
			if cursor is not None :
				cursor.close()
			if db is not None :
				db.close()

	def fetchAll(self, query) :
		try :
			db = self.dbConnection()
			cursor = db.cursor()
			cursor.execute(query)
			result = cursor.fetchall()
			return result
		except mysql.Error, e :
			print "error in fetchAll"
		finally :
			if cursor is not None :
				cursor.close()
			if db is not None :
				db.close()

