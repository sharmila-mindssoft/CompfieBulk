from protocol import (clientmasters, core)
from server.controller.corecontroller import process_user_menus

__all__ = [
	"process_client_master_requests"
]

def process_client_master_requests(request, db) :
	client_info = request.session_token.split("-")
	request = request.request
	client_id = int(client_info[0])
	session_token = client_info[1]
	session_user = db.validate_session_token(client_id, session_token)
	if session_user is None:
		return login.InvalidSessionToken()

	if type(request) is clientmasters.GetServiceProviders:
		return get_service_providers(db, request, session_user, client_id)

	if type(request) is clientmasters.SaveServiceProvider:
		return save_service_provider(db, request, session_user, client_id)

	if type(request) is clientmasters.UpdateServiceProvider:
		return update_service_provider(db, request, session_user, client_id)

	if type(request) is clientmasters.ChangeServiceProviderStatus:
		return change_service_provider_status(db, request, session_user, client_id)

	if type(request) is clientmasters.GetUserPrivileges:
		return get_user_privileges(db, request, session_user, client_id)

	if type(request) is clientmasters.SaveUserPrivileges:
		return save_user_privileges(db, request, session_user, client_id)

	if type(request) is clientmasters.UpdateUserPrivileges:
		return update_user_privileges(db, request, session_user, client_id)

	if type(request) is clientmasters.ChangeUserPrivilegeStatus:
		return change_user__privilege_status(db, request, session_user, client_id)

	if type(request) is clientmasters.GetClientUsers:
		return get_client_users(db, request, session_user, client_id)

	if type(request) is clientmasters.SaveClientUser:
		return save_client_user(db, request, session_user, client_id)

	if type(request) is clientmasters.UpdateClientUser:
		return update_client_user(db, request, session_user, client_id)

	if type(request) is clientmasters.UpdateClientUserStatus:
		return change_client_user_status(db, request, session_user, client_id)

	if type(request) is clientmasters.GetUnits:
		return get_units(db, request, session_user, client_id)

	if type(request) is clientmasters.CloseUnit:
		return close_unit(db, request, session_user, client_id)


def get_service_providers(db, request, session_user, client_id):
	service_provider_list = getDetailedList()
	response_data = {}
	response_data["service_providers"] = service_provider_list

	response = commonResponseStructure("GetServiceProvidersSuccess", response_data)
	return response

def save_service_provider(db, request, session_user, client_id):
	service_provider_id = db.generate_new_service_provider_id(client_id)
	if db.is_duplicate_service_provider(service_provider_id, 
		request.service_provider_name, client_id) :
		return clientmasters.ServiceProviderNameAlreadyExists()
	elif db.is_duplicate_service_provider_contact_no(service_provider_id,
		request.contact_no, client_id) :
		return clientmasters.ContactNumberAlreadyExists()
	elif db.save_service_provider(service_provider_id, request, session_user, client_id) :
		return clientmasters.SaveServiceProviderSuccess()

def update_service_provider(db, request, session_user, client_id):
	if db.is_invalid_id(db.tblServiceProviders, 
		"service_provider_id", request.service_provider_id, client_id):
		return clientmasters.InvalidServiceProviderId()
	elif is_duplicate_service_provider(request.service_provider_id, 
		request.service_provider_name, client_id) :
		return clientmasters.ServiceProviderNameAlreadyExists()
	elif db.is_duplicate_service_provider_contact_no(request.service_provider_id,
		request.contact_no, client_id) :
		return clientmasters.ContactNumberAlreadyExists()
	elif db.update_service_provider(request, session_user, client_id) :
		return clientmasters.UpdateServiceProviderSuccess()

def change_service_provider_status(db, request, session_user, client_id):
	if db.is_invalid_id(db.tblServiceProviders, 
		"service_provider_id", request.service_provider_id, client_id):
	    return clientmasters.InvalidServiceProviderId()
	elif db.update_service_provider_status(rquest.service_provider_id, 
		request.is_active, session_user, client_id):
	    return clientmasters.ChangeServiceProviderStatusSuccess()

def get_user_privileges(db, request, session_user, client_id):
	forms = getUserGroupsFormData()
	userGroupList = getDetailedList(session_user)

	response_data = {}
	response_data["forms"] = forms
	response_data["user_groups"] = userGroupList

	response = commonResponseStructure("GetUserGroupsSuccess", response_data)
	return response

def save_user_privileges(db, request, session_user, client_id):
	user_group_id = db.generate_new_user_privilege_id()
	if db.is_duplicate_user_privilege(user_group_id, 
		request.user_privilege_name, client_id) :
	    return clientmasters.GroupNameAlreadyExists()
	elif db.save_user_privilege(request, session_user, client_id) :
	    return clientmasters.SaveUserGroupSuccess()

def update_user_privileges(db, request, session_user, client_id):
	if db.is_invalid_id(db.tblUserGroups, "user_group_id",
		request.user_group_id, client_id):
	    return clientmasters.InvalidGroupId()
	elif db.is_duplicate_user_privilege(user_group_id, 
		request.user_privilege_name, client_id) :
	    return clientmasters.GroupNameAlreadyExists()
	elif db.update_user_privilege(request, session_user, client_id) :
	    return clientmasters.UpdateUserGroupSuccess()

def change_user__privilege_status(db, request, session_user, client_id):
	if db.is_invalid_id(db.tblUserGroups, "user_group_id", 
		request.user_group_id, client_id):
	    return clientmasters.InvalidGroupId()
	elif db.update_user_privilege_status(user_group_id, is_active, 
		session_user, client_id):
	    return clientmasters.ChangeUserPrivilegeStatusSuccess()

def get_client_users(db, request, session_user, client_id):
	countryList= CountryList().getUserCountry(session_user)
	domainList = DomainList().getUserDomains(session_user)
	DetailsTuple = db.getUserCompanyDetails(session_user)
	unitIds = DetailsTuple[0]
	divisionIds = DetailsTuple[1]
	legalEntityIds = DetailsTuple[2]
	businessGroupIds = DetailsTuple[3]

	clientId = 1
	divisionList = None
	businessGroupList = None
	if businessGroupIds != None:
	    businessGroupList = BusinessGroup(clientId, db).getBusinessGroupById(businessGroupIds)
	legalEntityList = LegalEntity(clientId, db).getLegalEntitiesById(legalEntityIds)
	if divisionIds != None:
	    divisionList = Division(clientId, db).getDivisionsById(divisionIds)
	unitList = Unit(clientId, db).getUnitsById(unitIds)
	userGroupList = UserPrivilege().getList(clientId)
	userList = User().getDetailedList(clientId)
	serviceProvidersList = ServiceProvider().getList()

	response_data = {}
	response_data["domains"] = domainList
	response_data["countries"] = countryList
	response_data["business_groups"] = businessGroupList
	response_data["legal_entities"] = legalEntityList
	response_data["divisions"] = divisionList
	response_data["units"] = unitList
	response_data["user_groups"] = userGroupList
	response_data["users"] = userList
	response_data["service_providers"] = serviceProvidersList

	response = commonResponseStructure("GetClientUsersSuccess", response_data)
	return response

def save_client_user(db, request, session_user, client_id):
	user_id = db.generate_new_user_id(client_id)
	if db.is_duplicate_user_email(user_id, request.email_id, client_id) :
	    return clientmasters.EmailIdAlreadyExists()
	elif db.is_duplicate_employee_code(user_id, 
		request.employee_code, client_id):
	    return clientmasters.EmployeeCodeAlreadyExists()
	elif is_duplicate_user_contact_no(user_id, request.contact_no, client_id):
	    return clientmasters.ContactNumberAlreadyExists()
	elif db.save_user(request, session_user, client_id) :
	    return clientmasters.SaveClientUserSuccess()

def update_client_user(db, request, session_user, client_id):
	if db.is_invalid_id(db.tblUsers, "user_id", request.user_id, client_id) :
	    return clientmasters.InvalidUserId()
	elif db.is_duplicate_employee_code(user_id, 
		request.employee_code, client_id):
	    return clientmasters.EmployeeCodeAlreadyExists()
	elif is_duplicate_user_contact_no(user_id, 
		request.contact_no, client_id):
	    return clientmasters.ContactNumberAlreadyExists()
	elif db.update_user(request, session_user, client_id) :
	    return clientmasters.UpdateUserSuccess()

def change_client_user_status(db, request, session_user, client_id):
	if db.is_invalid_id(db.tblUsers, "user_id", request.user_id, client_id) :
	    return clientmasters.InvalidUserId()
	elif db.update_user_status(request.user_id, 
		request.is_active, session_user, client_id):
	    return clientmasters.ChangeClientUserStatusSuccess()

def get_units(db, request, session_user, client_id):
	clientId = 1
	unitList = Unit(clientId, db).getUnitListForClosure(clientId)
	unitStructure = {}
	unitStructure["units"] = unitList
	return commonResponseStructure("GetUnitClosureListSuccess", unitStructure)

def close_unit(db, request, session_user, client_id):
	session_user = session_user
	unitId = request.unit_id
	password = request.password
	clientId = 1

	if db.verify_password():
	    if db.deactivate_unit(request.unitId, client_id):
	        return clientmasters.CloseUnitSuccess()
	    else:
	        print "Error : While deactivating Unit in client DB"
	        return False
	else:
	    return clientmasters.InvalidPassword()

