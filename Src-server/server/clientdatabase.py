from protocol import core
from database import Database

__all__ = [
	"ClientDatabase"
]

class ClientDatabase(Database):

    def __init__(self):
		super(ClientDatabase, self).__init__(
		    "localhost", "root", "123456", "mirror_knowledge")
		self.begin()
		self._client_db_connections = {}
		rows = self.get_client_db_info()
		for row in rows:
			host = row[0]
			client_id = row[1]
			username = row[2]
			password = row[3]
			database = row[4]
			self._client_db_connections[client_id] = super(
				ClientDatabase, self).__init__(
			    host, username, password, database
			)
		print self._client_db_connections