import os
from aparajitha.server.knowledgedatabase import KnowledgeDatabase
from aparajitha.model.common import validate_data
from aparajitha.model import protocol
import json

class APIHandler(object):
	def __init__(self):
		self._request_map = {
			"Login": self._login,
			"Logout": self._logout,
		}

	def success_response(self, response, response_option, data) :
		response = getattr(protocol, response)
		return {"protocol": response, "data": [response_option, data]}

	def failure_response(self, response, option) :
		response = getattr(protocol, response)
		return {"protocol": response, "data": [option, {}]}

	def _is_protocol_without_session(self, option) :
		protocols = [
			"Login"
		]
		if option in protocols :
			return True
		return False

	def process(self, db, session_id, request) :
		request_option = request[0]
		request_data = request[1]
		handler = self._request_map[request_option]
		if self._is_protocol_without_session(request_option) :
			return handler(db, request_data)
		user_id = db.get_session_user_id(session_id)
		if user_id is None :
			return self.failure_response(
				request_option + "Response", "InvalidSession"
			)
		if request_option == u"Logout" :
			return handler(db, session_id, request_data)
		user = db.get_user(user_id)
		return handler(db, user, request_data)


	#
	# Login, Logout
	#

	def _login(self, db, request) :
		email, password = request["username"], request["password"]
		email = email.lower()
		user_id = db.get_user_id(email)
		if user_id is None :
			return self.failure_response("LoginResponse", "LoginFailed")
		user = db.match_password(user_id, password)
		user = user[0]
		if user is None :
			return self.failure_response("LoginResponse", "LoginFailed")
		user_details = db.get_user_details(user_id, user["client_id"])
		if user_details is None :
			return self.failure_response("LoginResponse", "LoginFailed")
		session_id = db.add_session(user_id)
		response_data = {
			"session_token": session_id,
			"user": {
				"user_id": user_id,
				"client_id": user["client_id"],
				"email_id": email,
				"user_group_name": user_details["user_group_name"],
				"employee_name": user_details["employee_name"],
				"employee_code": user_details["employee_code"],
				"contact_no": user_details["contact_no"],
				"address": user_details["address"],
				"designation": user_details["designation"]
			},
			"menu": user_details["menu"]
		}
		return self.success_response(
			"LoginResponse", "LoginSuccess", response_data
		)

	def _logout(self, db, session_id, request) :
		db.remove_session(session_id)
		return self.success_response(
			"LogoutResponse", "LogoutSuccess", {}
		)


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
		self._api_handler = APIHandler()

	def _handle_db_request(self, unbound_method, request_handler) :
		request_handler.set_header("Access-Control-Allow-Origin", "*")
		unbound_method(self, self._db, request_handler)

	def _send_error(self, request_handler, status, msg) :
		request_handler.set_status(status)
		request_handler.write(msg)

	def _parse_request(self, request_handler, protocol2) :
		try:
			data = json.loads(request_handler.request.body)
			data = data["data"]
			if validate_data(protocol2, data) :
				return data
			else :
				return None
		except Exception, e:
			print e
			raise

	def _send_response(self, request_handler, protocol, data) :
		if not validate_data(protocol, data) :
			self._send_error(request_handler, 500, "")
			return
		structure = {"data": data}
		response_data = json.dumps(structure)
		request_handler.set_header("Content-Type", "application/json")
		request_handler.write(response_data)

	@db_request
	def handle_api_knowledge(self, db, request_handler) :
		db.test()
		request_frame = self._parse_request(request_handler, protocol.RequestFrame)
		if request_frame is None :
			request_handler.set_status(500)
			request_handler.write("")
			return
		session_id = request_frame["session_token"]
		request_obj = request_frame["request"]
		response_obj = self._api_handler.process(db, session_id, request_obj)
		self._send_response(request_handler, response_obj["protocol"], response_obj["data"])
