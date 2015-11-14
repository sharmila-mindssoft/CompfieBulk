import os
from aparajitha.server.clientdatabase import ClientDatabase

#
# db_request
#

def db_request(f) :
	def wrapper(self, request_handler) :
		self._handle_db_request(f, request_handler)
	return wrapper


#
# ClientController
#

class ClientController(object):
	def __init__(self):
		self._db = ClientDatabase("mirror_knowledge")

	def _handle_db_request(self, unbound_method, request_handler) :
		request_handler.set_header("Access-Control-Allow-Origin", "*")
		unbound_method(self, self._db, request_handler)

	@db_request
	def handle_api_test(self, db, request_handler) :
		db.test()
		request_handler.write("client test api success")