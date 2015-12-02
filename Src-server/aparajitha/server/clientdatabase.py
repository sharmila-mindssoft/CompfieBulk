from aparajitha.server.database import Database

class ClientDatabase(object) :
	def __init__(self, db) :
		self._db = Database(db)

	def test(self) :
		query = "SHOW TABLES;"
		print self._db.execute_and_return(query)
		return True