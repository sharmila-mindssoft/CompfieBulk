import os
from aparajitha.server.knowledgedatabase import KnowledgeDatabase

#
# db_request
#

def db_request(f) :
	def wrapper(self, request_handler) :
		self._handle_db_request(f, request_handler)
	return wrapper


#
# KnowledgeController
#

class KnowledgeController(object):
	def __init__(self):
		self._db = KnowledgeDatabase()

	def _handle_db_request(self, unbound_method, request_handler) :
		request_handler.set_header("Access-Control-Allow-Origin", "*")
		unbound_method(self, self._db, request_handler)

	@db_request
	def handle_api_knowledge(self, db, request_handler) :
		db.test()
		request_handler.write("knowledge test api success")
