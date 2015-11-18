from aparajitha.server.database import Database

DATABASE = "mirror_knowledge"

class KnowledgeDatabase(object) :
	def __init__(self) :
		self._db = Database(DATABASE)

	def test(self) :
		query = "SHOW TABLES;"
		print self._db.execute_and_return(query)
