import os
from aparajitha.server.knowledgedatabase import KnowledgeDatabase
from aparajitha.model.common import validate_data
from aparajitha.model import protocol
from aparajitha.server.knowledgemodels import *
from aparajitha.server.clientmodels import *
import json

class APIHandler(object):
	def __init__(self):
		self._request_map = {
			"Login": self._login,
			"Logout": self._logout,
			"GetUserGroups": self._get_user_groups,
			"SaveUserGroup": self._save_user_group,
			"UpdateUserGroup": self._update_user_group,
			"ChangeUserGroupStatus": self._change_user_group_status,
			"GetUsers": self._get_users,
			"SaveUser": self._save_user,
			"UpdateUser": self._update_user,
			"ChangeUserStatus": self._change_admin_user_status,									
		}

	def _success_response(self, response, response_option, data) :
		response = getattr(protocol, response)
		return {"protocol": response, "data": [response_option, data]}

	def _failure_response(self, response, option) :
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
			return self._failure_response(
				request_option + "Response", "InvalidSession"
			)
		if request_option == u"Logout" :
			return handler(db, session_id, request_data)
		user = db.get_user(user_id)
		print user
		return handler(db, user, request_data)


	#
	# Login, Logout
	#

	def _login(self, db, request) :
		email, password = request["username"], request["password"]
		email = email.lower()
		user_id = db.get_user_id(email)
		if user_id is None :
			return self._failure_response("LoginResponse", "LoginFailed")
		user = db.match_password(user_id, password)
		if user is None :
			return self._failure_response("LoginResponse", "LoginFailed")
		user = user[0]
		user_details = db.get_user_details(user_id, user["client_id"])
		if user_details is None :
			return self._failure_response("LoginResponse", "LoginFailed")
		session_id = db.add_session(user_id)
		response_data = {
			"session_token": session_id,
			"user": {
				"user_id": user_id,
				"client_id": int(user["client_id"]),
				"email_id": str(email),
				"category": user_details["category"],
				"user_group_name": user_details["user_group_name"],
				"employee_name": user_details["employee_name"],
				"employee_code": user_details["employee_code"],
				"contact_no": user_details["contact_no"],
				"address": user_details["address"],
				"designation": user_details["designation"]
			},
			"menu": user_details["menu"]
		}
		return self._success_response(
			"LoginResponse", "LoginSuccess", response_data
		)

	def _logout(self, db, session_id, request) :
		db.remove_session(session_id)
		return self._success_response(
			"LogoutResponse", "LogoutSuccess", {}
		)

	def _get_user_groups(self, db, user, request):
		knowledge_forms = Form.get_forms("knowledge", db)
		techno_forms = Form.get_forms("techno", db)
		forms = {}
		forms["knowledge"] = Menu.get_menu(knowledge_forms)
		forms["techno"] = Menu.get_menu(techno_forms)
		user_group_list = UserGroup.get_detailed_list(db)
		response_data = {}
		response_data["forms"] = forms
		response_data["user_groups"] = user_group_list
		print response_data
		return self._success_response(
			"GetUserGroupsResponse", 
			"GetUserGroupsSuccess", 
			response_data
		)

	def _save_user_group(self, db, user, request):
		form = "UserGroupMaster"
		session_user = int(user["user_id"])
		response = "SaveUserGroupResponse"
		response_data = None
		user_group_id = db.generate_new_id(form)
		user_group = UserGroup.initialize_with_request( request, user_group_id)
		if db.is_duplicate(form, "name", user_group.user_group_name,user_group_id):
			response_data = self._failure_response(response, "GroupNameAlreadyExists")
		elif db.save_user_group(user_group, session_user):
			action_type = "save"
			db.save_activity(form, user_group.user_group_name, 
				action_type, session_user)
			response_data =  self._success_response(
				response, 
				"SaveUserGroupSuccess", 
				{}
			)
		return response_data
        

	def _update_user_group(self, db, user, request):
		form = "UserGroupMaster"
		session_user = int(user["user_id"])
		response = "UpdateUserGroupResponse"
		response_data = None
		user_group_id = request["user_group_id"]
		user_group = UserGroup.initialize_with_request(request, user_group_id)
		if db.is_id_invalid(form, user_group_id):
			response_data = self._failure_response(response, "InvalidUserGroupId")
		elif db.is_duplicate(form, "name", user_group.user_group_name,
			user_group.user_group_id):
			response_data = self._failure_response(response,"GroupNameAlreadyExists")
		elif db.save_user_group(user_group, session_user):
			action_type = "update"
			db.save_activity(form, user_group.user_group_name, 
				action_type, session_user)
			response_data =  self._success_response(response, "UpdateUserGroupSuccess",{})
		return response_data

	def _change_user_group_status(self, db, user, request):
		form = "UserGroupMaster"
		session_user = int(user["user_id"])
		response = "ChangeUserGroupStatusResponse"
		response_data = None
		user_group_id = request["user_group_id"]
		is_active = request["is_active"]
		if db.is_id_invalid(form, user_group_id):
			response_data = self._failure_response(
				response, "InvalidUserGroupId")
		elif db.change_user_group_status(user_group_id, is_active,
				session_user):
			action_type = "status_change"
			db.save_activity(form, user_group_id, 
				action_type, session_user)
			response_data = self._success_response(
				response, "ChangeUserGroupStatusSuccess",{})
		return response_data

	def _get_users(self, db, user, request):
		domain_list = Domain.get_list(db)
		country_list = Country.get_list(db)
		user_group_list = UserGroup.get_list(db)
		user_list = AdminUser.get_detailed_list(db)
		response_data = {}
		response_data["domains"] = domain_list
		response_data["countries"] = country_list
		response_data["user_groups"] = user_group_list
		response_data["users"] = user_list
		print response_data
		return self._success_response(
				"GetUsersResponse", 
				"GetUsersSuccess",
				response_data)
        
	def _save_user(self, db, user, request):
		form = "UserMaster"
		session_user = int(user["user_id"])
		response = "SaveUserResponse"
		response_data = None
		user_id = db.generate_new_id(form)
		user = AdminUser.initialize_with_request( request, user_id)
		if db.is_duplicate(form, "email", user.email_id,user_id):
			response_data = self._failure_response(
				response, "EmailIdAlreadyExists")
		elif db.is_duplicate(form, "employee_code", user.employee_code,user_id):
			response_data = self._failure_response(
				response, "EmployeeCodeAlreadyExists")
		elif db.is_duplicate(form, "contact_no", user.contact_no,user_id):
			response_data = self._failure_response(
				response, "ContactNumberAlreadyExists")
		elif (db.save_user(user, session_user) and db.save_user_details(
					user, session_user)):
			action_type = "save"
			db.save_activity(form, user.employee_code+"-"+user.employee_name, 
				action_type, session_user)
			response_data = self._success_response(response, "SaveUserSuccess",
				{})
		return response_data

	def _update_user(self, db, user, request):
		form = "UserMaster"
		session_user = int(user["user_id"])
		response = "UpdateUserResponse"
		response_data = None
		user_id = request["user_id"]
		user = AdminUser.initialize_with_request( request, user_id)
		if db.is_id_invalid(form, user_id):
			response_data = self._failure_response(
				response, "InvalidUserId")
		elif db.is_duplicate(form, "email", user.email_id,user_id):
			response_data = self._failure_response(
				response, "EmailIdAlreadyExists")
		elif db.is_duplicate(form, "employee_code", user.employee_code,user_id):
			response_data = self._failure_response(
				response, "EmployeeCodeAlreadyExists")
		elif db.is_duplicate(form, "contact_no", user.contact_no,user_id):
			response_data = self._failure_response(
				response, "ContactNumberAlreadyExists")
		elif db.save_user_details(user, session_user):
			action_type = "update"
			db.save_activity(form, user.employee_code+"-"+user.employee_name, 
				action_type, session_user)
			response_data = self._success_response(response, "UpdateUserSuccess",
				{})
		return response_data

	def _change_admin_user_status(self, db, user, request):
		form = "UserMaster"
		session_user = int(user["user_id"])
		response = "ChangeUserStatusResponse"
		response_data = None
		user_id = request["user_id"]
		is_active = request["is_active"]
		if db.is_id_invalid(form, user_id):
			response_data = self._failure_response(
				response, "InvalidUserId")
		elif db.change_user_status(user_id, is_active,
				session_user):
			action_type = "status_change"
			db.save_activity(form, user_id, 
				action_type, session_user)
			response_data = self._success_response(
				response, "ChangeUserStatusSuccess",{})
		return response_data


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
