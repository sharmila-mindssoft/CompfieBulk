import os
from aparajitha.server.clientdatabase import ClientDatabase
from aparajitha.server.clientmodels import *
from aparajitha.model.common import validate_data
from aparajitha.model import protocol
import json
from aparajitha.misc.client_mappings import client_db_mappings
from aparajitha.server.knowledgedatabase import KnowledgeDatabase


class APIHandler(object):
	def __init__(self):
		self._client_id = None
		self._db = None
		self._knowledge_db = KnowledgeDatabase()
		self._request_map = {
			"Test": self._test,
			"GetServiceProviders": self._getServiceProviders,
			"SaveServiceProvider": self._saveServiceProvider,
			"UpdateServiceProvider": self._updateServiceProvider,
			"ChangeServiceProviderStatus": self._changeServiceProviderStatus,
			"GetUserPrivileges": self._getUserPrivileges,
			"SaveUserPrivilege": self._saveUserPrivilege,
			"UpdateUserPrivilege": self._updateUserPrivilege,
			"ChangeUserPrivilegeStatus": self._changeUserPrivilegeStatus,
			"GetClientUsers": self._getClientUsers,
			"SaveClientUser": self._saveClientUser,
			"UpdateClientUser": self._updateClientUser,
			"ChangeClientUserStatus": self._changeClientUserStatus,
			"ChangeAdminStatus": self._changeAdminStatus
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
		user = self._knowledge_db.get_user(user_id)
		db = self._get_database(user["client_id"])
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
	def _getServiceProviders(self, db, user, request):
		serviceProviderList = ServiceProvider.getList(db)
		responseData = {}
		responseData["service_providers"] = serviceProviderList
		return self._success_response(
			"GetServiceProvidersResponse", 
			"GetServiceProvidersSuccess", 
			responseData
		)

	def _saveServiceProvider(self, db, user, request):
		form = "ServiceProvider"
		sessionUser = user["user_id"]

		response = "SaveServiceProviderResponse"
		responseData = None

		serviceProviderId = db.generateNewId(form)
		serviceProvider = ServiceProvider.initializeWithRequest(request, 
			serviceProviderId, self._client_id)

		if db.isDuplicate(form, "name", serviceProvider.serviceProviderName,
			serviceProvider.serviceProviderId):
			responseData = self._failure_response(
				response,"ServiceProviderNameAlreadyExists")
		elif db.isDuplicate(form, "contactNo", serviceProvider.contactNo,serviceProvider.serviceProviderId):
			responseData = self._failure_response(
				response,"ContactNumberAlreadyExists")
		elif db.saveServiceProvider(serviceProvider, sessionUser):
			actionType = "save"
			self._knowledge_db.saveActivity(form, serviceProvider.serviceProviderName, 
				actionType, sessionUser)
			responseData =  self._success_response(
				response,"SaveServiceProviderSuccess",{})		
		return responseData

	def _updateServiceProvider(self, db, user, request):
		form = "ServiceProvider"
		sessionUser = user["user_id"]

		response = "UpdateServiceProviderResponse"
		responseData = None

		serviceProviderId = request["service_provider_id"]
		serviceProvider = ServiceProvider.initializeWithRequest(request, 
			serviceProviderId, self._client_id)
		
		if db.isIdInvalid(form, serviceProviderId):
			responseData = self._failure_response(
				response, "InvalidServiceProviderId")
		elif db.isDuplicate(form, "name", serviceProvider.serviceProviderName,
			serviceProvider.serviceProviderId):
			responseData = self._failure_response(
				response, "ServiceProviderNameAlreadyExists")
		elif db.isDuplicate(form, "contactNo", serviceProvider.contactNo,serviceProvider.serviceProviderId):
			responseData = self._failure_response(
				response, "ContactNumberAlreadyExists")
		elif db.saveServiceProvider(serviceProvider, sessionUser):
			actionType = "update"
			self._knowledge_db.saveActivity(form, serviceProvider.serviceProviderName, 
				actionType, sessionUser)
			responseData =  self._success_response(
				response, "UpdateServiceProviderSuccess",{})		
		return responseData

	def _changeServiceProviderStatus(self, db, user, request):
		form = "ServiceProvider"
		sessionUser = user["user_id"]

		response = "ChangeServiceProviderStatusResponse"
		responseData = None

		serviceProviderId = request["service_provider_id"]
		isActive = request["is_active"]

		if db.isIdInvalid(form, serviceProviderId):
			responseData = self._failure_response(
				response, "InvalidServiceProviderId")
		elif db.changeServiceProviderStatus(serviceProviderId, isActive,
				sessionUser):
			actionType = "statusChange"
			self._knowledge_db.saveActivity(form, serviceProviderId, 
				actionType, sessionUser)
			responseData = self._success_response(
				response, "ChangeServiceProviderStatusSuccess",{})
		return responseData

#
#	User Privilege
#	
	def _getUserPrivileges(self, db, user, request):
		sessionUser = user["user_id"]

		clientForms = Form.getForms("client", self._knowledge_db)
		forms = Menu.getMenu(clientForms)
		userGroupList = UserPrivilege.getDetailedList(sessionUser, db)
		
		responseData = {}
		responseData["forms"] = forms
		responseData["user_groups"] = userGroupList
		response = self._success_response("GetUserPrivilegesResponse", 
			"GetUserPrivilegesSuccess",responseData)
		return response

	def _saveUserPrivilege(self, db, user, request):
		form = "UserPrivilege"
		sessionUser = user["user_id"]
		response = "SaveUserPrivilegeResponse"
		responseData = None
		userPrivilegeId = db.generateNewId(form)
		userPrivilege = UserPrivilege.initializeWithRequest(request, userPrivilegeId, self._client_id)
		if db.isDuplicate(form, "name", userPrivilege.userGroupName,userPrivilegeId):
			responseData = self._failure_response(response,"GroupNameAlreadyExists")
		elif db.saveUserPrivilege(userPrivilege, sessionUser):
			actionType = "save"
			self._knowledge_db.saveActivity(form, userPrivilege.userGroupName, 
				actionType, sessionUser)
			responseData =  self._success_response(response, "SaveUserPrivilegeSuccess",{})
		return responseData

	def _updateUserPrivilege(self, db, user, request):
		form = "UserPrivilege"
		sessionUser = user["user_id"]
		response = "UpdateUserPrivilegeResponse"
		responseData = None
		userPrivilegeId = request["user_group_id"]
		userPrivilege = UserPrivilege.initializeWithRequest(request, 
			userPrivilegeId, self._client_id)
		if db.isIdInvalid(form, userPrivilegeId):
			responseData = self._failure_response(response, "InvalidUserGroupId")
		elif db.isDuplicate(form, "name", userPrivilege.userGroupName,
			userPrivilege.userGroupId):
			responseData = self._failure_response(response,"GroupNameAlreadyExists")
		elif db.saveUserPrivilege(userPrivilege, sessionUser):
			actionType = "update"
			self._knowledge_db.saveActivity(form, userPrivilege.userGroupName, 
				actionType, sessionUser)
			responseData =  self._success_response(response, "UpdateUserPrivilegeSuccess",{})
		return responseData

	def _changeUserPrivilegeStatus(self, db, user, request):
		form = "UserPrivilege"
		sessionUser = user["user_id"]

		response = "ChangeUserPrivilegeStatusResponse"
		responseData = None

		userGroupId = request["user_group_id"]
		isActive = request["is_active"]

		if db.isIdInvalid(form, userGroupId):
			responseData = self._failure_response(
				response, "InvalidUserGroupId")
		elif db.changeUserPrivilegeStatus(userGroupId, isActive,
				sessionUser):
			actionType = "statusChange"
			self._knowledge_db.saveActivity(form, userGroupId, 
				actionType, sessionUser)
			responseData = self._success_response(
				response, "ChangeUserPrivilegeStatusSuccess",{})
		return responseData


#
#	User
#

	def _getClientUsers(self, db, user, request):

        countryList = CountryList.getCountryList()
    	domainList = DomainList.getDomainList()
        businessGroupList = BusinessGroup.getList(self._client_id, db)
        legalEntityList = LegalEntity.getList(self._client_id, db)
        divisionList = Division.getList(self._client_id, db)
        unitList = Unit.getList(self._client_id, db)
    	userGroupList = UserPrivilege.getList(self._client_id, db)
    	userList = User.getDetailedList(self._client_id, db)

        responseData = {}
        responseData["domains"] = domainList
        responseData["countries"] = countryList
        responseData["business_groups"] = businessGroupList
        responseData["legal_entities"] = legalEntityList
        responseData["divisions"] = divisionList
        responseData["units"] = unitList
        responseData["user_groups"] = userGroupList
        responseData["users"] = userList

       	return self._success_response("GetClientUsersResponse", 
			"GetClientUsersSuccess",responseData

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
