import os
from aparajitha.server.clientdatabase import ClientDatabase
from aparajitha.server.clientmodels import *
from aparajitha.model.common import validate_data
from aparajitha.model import protocol
import json
from aparajitha.misc.client_mappings import client_db_mappings
from aparajitha.server.knowledgedatabase import KnowledgeDatabase
from aparajitha.server.knowledgemodels import *


class APIHandler(object):
	def __init__(self):
		self._client_id = None
		self._db = None
		self._knowledge_db = KnowledgeDatabase()
		self._request_map = {
			"Test": self._test,
			"GetServiceProviders": self._get_service_providers,
			"SaveServiceProvider": self._save_service_provider,
			"UpdateServiceProvider": self._update_service_provider,
			"ChangeServiceProviderStatus": self._change_service_provider_status,
			"GetUserPrivileges": self._get_user_privileges,
			"SaveUserPrivilege": self._save_user_privilege,
			"UpdateUserPrivilege": self._update_user_privilege,
			"ChangeUserPrivilegeStatus": self._change_user_privilege_status,
			"GetClientUsers": self._get_client_users,
			"SaveClientUser": self._save_client_user,
			"UpdateClientUser": self._update_client_user,
			"ChangeClientUserStatus": self._change_client_user_status,
			"ChangeAdminStatus": self._change_admin_status,
			"GetUnitClosureList": self._get_unit_closure_list,
			"CloseUnit": self._close_unit
		}

	def _success_response(self, response, response_option, data) :
		response = getattr(protocol, response)
		return {"protocol": response, "data": [response_option, data]}

	def _failure_response(self, response, option) :
		response = getattr(protocol, response)
		return {"protocol": response, "data": [option, {}]}

	def _get_database(self, client_id) :
		database_name = None
		if client_id is None :
			return None
		database_name = client_db_mappings[client_id]
		self._db = ClientDatabase(database_name)
		return self._db

	def process(self, session_id, request) :
		request_option = request[0]
		request_data = request[1]
		handler = self._request_map[request_option]
		user_id = self._knowledge_db.get_session_user_id(session_id)
		if user_id is None :
			return self._failure_response(
				request_option + "Response", "InvalidSession"
			)
		self._client_id = self._knowledge_db.get_client_id(user_id)
		db = self._get_database(self._client_id)
		user = db.get_user(user_id)
		if db is None :
			return self._failure_response(
				request_option + "Response", "InvalidSession"
			)
		return handler(db, user, request_data)

	def _test(self, db, user, request):
		return self._success_response(
			"TestResponse", "TestSuccess", {}
		)

#
#	Service Provider
#	
	def _get_service_providers(self, db, user, request):
		service_provider_list = ServiceProvider.get_list(db)
		response_data = {}
		response_data["service_providers"] = service_provider_list
		return self._success_response(
			"GetServiceProvidersResponse", 
			"GetServiceProvidersSuccess", 
			response_data
		)

	def _save_service_provider(self, db, user, request):
		form = "ServiceProvider"
		session_user = int(user["user_id"])

		response = "SaveServiceProviderResponse"
		response_data = None

		service_provider_id = db.generate_new_id(form)
		service_provider = ServiceProvider.initialize_with_request(request, 
			service_provider_id, self._client_id)

		if db.is_duplicate(form, "name", service_provider.service_provider_name,
			service_provider.service_provider_id):
			response_data = self._failure_response(
				response,"ServiceProviderNameAlreadyExists")
		elif db.is_duplicate(form, "contact_no", service_provider.contact_no,
			service_provider.service_provider_id):
			response_data = self._failure_response(
				response,"ContactNumberAlreadyExists")
		elif db.save_service_provider(service_provider, session_user):
			action_type = "save"
			self._knowledge_db.save_activity(form, service_provider.service_provider_name, 
				action_type, session_user)
			response_data =  self._success_response(
				response,"SaveServiceProviderSuccess",{})		
		return response_data

	def _update_service_provider(self, db, user, request):
		form = "ServiceProvider"
		session_user = int(user["user_id"])

		response = "UpdateServiceProviderResponse"
		response_data = None

		service_provider_id = request["service_provider_id"]
		service_provider = ServiceProvider.initialize_with_request(request, 
			service_provider_id, self._client_id)
		
		if db.is_id_invalid(form, service_provider_id):
			response_data = self._failure_response(
				response, "InvalidService_provider_id")
		elif db.is_duplicate(form, "name", service_provider.service_provider_name,
			service_provider.service_provider_id):
			response_data = self._failure_response(
				response, "ServiceProviderNameAlreadyExists")
		elif db.is_duplicate(form, "contact_no", service_provider.contact_no,
			service_provider.service_provider_id):
			response_data = self._failure_response(
				response, "ContactNumberAlreadyExists")
		elif db.save_service_provider(service_provider, session_user):
			action_type = "update"
			self._knowledge_db.save_activity(form, service_provider.service_provider_name, 
				action_type, session_user)
			response_data =  self._success_response(
				response, "UpdateServiceProviderSuccess",{})		
		return response_data

	def _change_service_provider_status(self, db, user, request):
		form = "ServiceProvider"
		session_user = int(user["user_id"])

		response = "ChangeServiceProviderStatusResponse"
		response_data = None

		service_provider_id = request["service_provider_id"]
		is_active = request["is_active"]

		if db.is_id_invalid(form, service_provider_id):
			response_data = self._failure_response(
				response, "InvalidServiceProviderId")
		elif db.change_service_provider_status(service_provider_id, is_active,
				session_user):
			action_type = "status_change"
			self._knowledge_db.save_activity(form, service_provider_id, 
				action_type, session_user)
			response_data = self._success_response(
				response, "ChangeServiceProviderStatusSuccess",{})
		return response_data

#
#	User Privilege
#	
	def _get_user_privileges(self, db, user, request):
		session_user = int(user["user_id"])

		client_forms = Form.get_forms("client", self._knowledge_db)
		forms = Menu.get_menu(client_forms)
		user_group_list = UserPrivilege.get_detailed_list(self._client_id, db)
		
		response_data = {}
		response_data["forms"] = forms
		response_data["user_groups"] = user_group_list
		response = self._success_response("GetUserPrivilegesResponse", 
			"GetUserPrivilegesSuccess",response_data)
		return response

	def _save_user_privilege(self, db, user, request):
		form = "UserPrivilege"
		session_user = int(user["user_id"])
		response = "SaveUserPrivilegeResponse"
		response_data = None
		user_privilege_id = db.generate_new_id(form)
		user_privilege = UserPrivilege.initialize_with_request(request, user_privilege_id, 
			self._client_id)
		if db.is_duplicate(form, "name", user_privilege.user_group_name,user_privilege_id):
			response_data = self._failure_response(response,"GroupNameAlreadyExists")
		elif db.save_user_privilege(user_privilege, session_user):
			action_type = "save"
			self._knowledge_db.save_activity(form, user_privilege.user_group_name, 
				action_type, session_user)
			response_data =  self._success_response(response, "SaveUserPrivilegeSuccess",{})
		return response_data

	def _update_user_privilege(self, db, user, request):
		form = "UserPrivilege"
		session_user = int(user["user_id"])
		response = "UpdateUserPrivilegeResponse"
		response_data = None
		user_privilege_id = request["user_group_id"]
		user_privilege = UserPrivilege.initialize_with_request(request, 
			user_privilege_id, self._client_id)
		if db.is_id_invalid(form, user_privilege_id):
			response_data = self._failure_response(response, "InvalidUser_group_id")
		elif db.is_duplicate(form, "name", user_privilege.user_group_name,
			user_privilege.user_group_id):
			response_data = self._failure_response(response,"GroupNameAlreadyExists")
		elif db.save_user_privilege(user_privilege, session_user):
			action_type = "update"
			self._knowledge_db.save_activity(form, user_privilege.user_group_name, 
				action_type, session_user)
			response_data =  self._success_response(response, "UpdateUserPrivilegeSuccess",{})
		return response_data

	def _change_user_privilege_status(self, db, user, request):
		form = "UserPrivilege"
		session_user = int(user["user_id"])

		response = "ChangeUserPrivilegeStatusResponse"
		response_data = None

		user_group_id = request["user_group_id"]
		is_active = request["is_active"]

		if db.is_id_invalid(form, user_group_id):
			response_data = self._failure_response(
				response, "InvalidUserGroupId")
		elif db.change_user_privilege_status(user_group_id, is_active,
				session_user):
			action_type = "status_change"
			self._knowledge_db.save_activity(form, user_group_id, 
				action_type, session_user)
			response_data = self._success_response(
				response, "ChangeUserPrivilegeStatusSuccess",{})
		return response_data

#
#	User
#
	def _get_client_users(self, db, user, request):
			country_list = Country.get_list(db)
			domain_list = Domain.get_list(db)
			business_group_list = BusinessGroup.get_list(self._client_id, db)
			legal_entity_list = LegalEntity.get_list(self._client_id, db)
			division_list = Division.get_list(self._client_id, db)
			unit_list = Unit.get_list(self._client_id, db)
			user_group_list = UserPrivilege.get_list(self._client_id, db)
			user_list = User.get_detailed_list(self._client_id, db)

			response_data = {}
			response_data["domains"] = domain_list
			response_data["countries"] = country_list
			response_data["business_groups"] = business_group_list
			response_data["legal_entities"] = legal_entity_list
			response_data["divisions"] = division_list
			response_data["units"] = unit_list
			response_data["user_groups"] = user_group_list
			response_data["users"] = user_list
			return self._success_response("GetClientUsersResponse",
	        	"GetClientUsersSuccess",response_data)

	def _save_client_user(self, db, user, request):
		form = "User"
		session_user = int(user["user_id"])
		response = "SaveClientUserResponse"
		response_data = None
		user_id = self._knowledge_db.generate_new_id(form)
		user = User.initialize_with_request(request, user_id, self._client_id)
		if self._knowledge_db.is_duplicate(form, "email", user.email_id, user_id):
			response_data = self._failure_response(response,"EmailIdAlreadyExists")
		elif db.is_duplicate(form, "employee_code", user.employee_code, user_id):
			response_data = self._failure_response(response,"EmployeeCodeAlreadyExists")
		elif db.is_duplicate(form, "contact_no", user.contact_no, user_id):
			response_data = self._failure_response(response,"ContactNumberAlreadyExists")
		elif (self._knowledge_db.save_user(user, session_user) and db.save_user_detail(user, session_user)):
			action_type = "save"
			self._knowledge_db.save_activity(form, user.employee_code+"-"+user.employee_name, 
				action_type, session_user)
			response_data =  self._success_response(response, "SaveClientUserSuccess",{})
		return response_data
        
	def _update_client_user(self, db, user, request):
		form = "User"
		session_user = int(user["user_id"])
		response = "UpdateClientUserResponse"
		response_data = None
		user_id = request["user_id"]
		user = User.initialize_with_request(request, user_id, self._client_id)
		if self._db.is_id_invalid(form, user_id):
			response_data = self._failure_response(response,"InvalidUser_id")
		elif db.is_duplicate(form, "employee_code", user.employee_code, user_id):
			response_data = self._failure_response(response,"EmployeeCodeAlreadyExists")
		elif db.is_duplicate(form, "contact_no", user.contact_no, user_id):
			response_data = self._failure_response(response,"ContactNumberAlreadyExists")
		elif db.update_user_detail(user, session_user):
			action_type = "update"
			self._knowledge_db.save_activity(form, user.employee_code+"-"+user.employee_name, 
				action_type, session_user)
			response_data =  self._success_response(response, "UpdateClientUserSuccess",{})
		return response_data

	def _change_client_user_status(self, db, user, request):
		form = "User"
		session_user = int(user["user_id"])

		response = "ChangeClientUserStatusResponse"
		response_data = None

		user_id = request["user_id"]
		is_active = request["is_active"]

		if db.is_id_invalid(form, user_id):
			response_data = self._failure_response(
				response, "InvalidUserId")
		elif (self._knowledge_db.change_user_status (
			user_id, is_active, session_user) and db.change_user_detail_status(
			user_id, is_active, session_user)):
			action_type = "status_change"
			self._knowledge_db.save_activity(form, user_id, 
				action_type, session_user)
			response_data = self._success_response(
				response, "ChangeClientUserStatusSuccess",{})
		return response_data		

	def _change_admin_status(self, db, user, request):
		form = "User"
		session_user = int(user["user_id"])

		response = "ChangeAdminStatusResponse"
		response_data = None

		user_id = request["user_id"]
		is_admin = request["is_admin"]

		if db.is_id_invalid(form, user_id):
			response_data = self._failure_response(
				response, "InvalidUserId")
		elif db.change_admin_status(user_id, is_admin, session_user):
			action_type = "admin_status_change"
			self._knowledge_db.save_activity(form, user_id, 
				action_type, session_user)
			response_data = self._success_response(
				response, "ChangeAdminStatusSuccess",{})
		return response_data	

#
#	Close Unit
#

	def _get_unit_closure_list(self, db, user, request):
		unit_list = Unit.get_unit_list_for_closure(self._client_id, db)
		response_data = {}
		response_data["units"] = unit_list
		return self._success_response(
        	"GetUnitClosureListResponse", 
        	"GetUnitClosureListSuccess",
        	response_data)

	def _close_unit(self, db, user, request):
		session_user = int(user["user_id"])
		unit_id = request["unit_id"]
		password = request["password"]
		response_data = None
		response = "CloseUnitResponse"
		if not self._knowledge_db.verify_password(password, session_user, self._client_id):
			response_data =  self._failure_response(
						        	response, 
						        	"InvalidPassword")
		elif (db.deactivate_unit(unit_id) and self._knowledge_db.deactivate_unit(
			unit_id, self._client_id, session_user)):
				response_data =  self._success_response(
						        	response, 
						        	"CloseUnitSuccess",
						        	{})
		else:
			print "Error : While deactivating Unit in client DB"
			return False
		return response_data

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
		self._api_handler = APIHandler()

	def _handle_db_request(self, unbound_method, request_handler) :
		request_handler.set_header("Access-Control-Allow-Origin", "*")
		unbound_method(self, request_handler)

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
	def handle_api_client(self, request_handler) :
		request_frame = self._parse_request(request_handler, protocol.RequestFrame)
		if request_frame is None :
			request_handler.set_status(500)
			request_handler.write("")
			return
		session_id = request_frame["session_token"]
		request_obj = request_frame["request"]
		response_obj = self._api_handler.process(session_id, request_obj)
		self._send_response(request_handler, response_obj["protocol"], response_obj["data"])
