from basics.types import VectorType, VariantType, RecordType, Field
from core import (BusinessGroup, LegalEntity, Division, Unit, FORM_TYPE, ServiceProvider,
		Menu, UserGroup, ClientUser, )
from common import (FORM_ID, COUNTRY_ID, DOMAIN_ID, UNIT_ID, SERVICE_PROVIDER_NAME,  ADDRESS, DATE,
	CONTACT_PERSON, CONTACT_NUMBER, SERVICE_PROVIDER_ID, CLIENT_ID, USER_GROUP_NAME,USER_GROUP_ID, 
	IS_ACTIVE, EMAIL_ID, EMPLOYEE_NAME, EMPLOYEE_CODE, UNIT_NAME,
	USER_LEVEL, STATUS, USER_ID, PASSWORD, SESSION_TOKEN)

__all__=  [
	"Request", "Response", "RequestFormat"
]

FormIdList = VectorType(FORM_ID)
CountryIdList = VectorType(COUNTRY_ID)
DomainIdList = VectorType(DOMAIN_ID)
UnitIdList = VectorType(UNIT_ID)
BusinessGroupList = VectorType(BusinessGroup)
LegalEntityList = VectorType(LegalEntity)
DivisionList = VectorType(Division)
UnitList = VectorType(Unit)

#	
#	Request
#

### Service Providers

GetServiceProviders = RecordType("GetServiceProviders", [
])

SaveServiceProvider = RecordType("SaveServiceProvider", [
	Field("service_provider_name", SERVICE_PROVIDER_NAME), 
	Field("address", ADDRESS),
	Field("contract_from", DATE),
	Field("contract_to", DATE), 
	Field("contact_person", CONTACT_PERSON),
	Field("contact_no", CONTACT_NUMBER)
])

UpdateServiceProvider = RecordType("UpdateServiceProvider", [
	Field("service_provider_id", SERVICE_PROVIDER_ID),
	Field("service_provider_name", SERVICE_PROVIDER_NAME), 
	Field("address", ADDRESS),
	Field("contract_from", DATE),
	Field("contract_to", DATE), 
	Field("contact_person", CONTACT_PERSON),
	Field("contact_no", CONTACT_NUMBER)
])

ChangeServiceProviderStatus = RecordType("ChangeServiceProviderStatus", [
	Field("service_provider_id", SERVICE_PROVIDER_ID),
	Field("is_active", IS_ACTIVE)
])

### User Privilege

GetUserPrivileges = RecordType("GetUserPrivileges", [
])

SaveUserPrivileges = RecordType("SaveUserPrivileges", [
	Field("client_id", CLIENT_ID),
	Field("user_group_name", USER_GROUP_NAME),
	Field("form_type", FORM_TYPE),
	Field("form_ids", FormIdList)
])

UpdateUserPrivileges = RecordType("UpdateUserPrivileges", [
	Field("user_group_id", USER_GROUP_ID),
	Field("client_id", CLIENT_ID),
	Field("user_group_name", USER_GROUP_NAME),
	Field("form_type", FORM_TYPE),
	Field("form_ids", FormIdList)
])

ChangeUserPrivilegeStatus = RecordType("ChangeUserPrivilegeStatus", [
	Field("user_group_id", USER_GROUP_ID),
	Field("is_active", IS_ACTIVE)
])

### Users

GetClientUsers = RecordType("GetClientUsers", [
])

SaveClientUser = RecordType("SaveClientUser", [
	Field("email_id", EMAIL_ID),
	Field("user_group_id", USER_GROUP_ID), 
	Field("employee_name", EMPLOYEE_NAME),
	Field("employee_code", EMPLOYEE_CODE),
	Field("contact_no", CONTACT_NUMBER),
	Field("seating_unit_id", UNIT_ID),
	Field("seating_unit_name", UNIT_NAME),
	Field("user_level", USER_LEVEL),
	Field("country_ids", CountryIdList),
	Field("domain_ids", DomainIdList),
	Field("unit_ids", UnitIdList),
	Field("is_service_provider", STATUS),
	Field("service_provider_id", SERVICE_PROVIDER_ID)
])

UpdateClientUser = RecordType("UpdateClientUser", [
	Field("user_id", USER_ID),
	Field("user_group_id", USER_GROUP_ID), 
	Field("employee_name", EMPLOYEE_NAME),
	Field("employee_code", EMPLOYEE_CODE),
	Field("contact_no", CONTACT_NUMBER),
	Field("seating_unit_id", UNIT_ID),
	Field("seating_unit_name", UNIT_NAME),
	Field("user_level", USER_LEVEL),
	Field("country_ids", CountryIdList),
	Field("domain_ids", DomainIdList),
	Field("unit_ids", UnitIdList),
	Field("is_service_provider", STATUS),
	Field("service_provider_id", SERVICE_PROVIDER_ID)
])

UpdateClientUserStatus = RecordType("UpdateClientUserStatus", [
	Field("user_id", USER_ID),
	Field("is_active", IS_ACTIVE)
])

### Close Unit

GetUnits = RecordType("GetUnits", [
])

CloseUnit = RecordType("CloseUnit", [
	Field("unit_id", UNIT_ID),
	Field("password", PASSWORD)
])

Request = VariantType("Request", [
	GetServiceProviders, SaveServiceProvider,
	UpdateServiceProvider, ChangeServiceProviderStatus,
	GetUserPrivileges, SaveUserPrivileges,
	UpdateUserPrivileges, ChangeUserPrivilegeStatus,
	GetClientUsers, SaveClientUser, UpdateClientUser,
	UpdateClientUserStatus, GetUnits, CloseUnit
])

RequestFormat = RecordType("RequestFormat", [
	Field("session_token", SESSION_TOKEN),
	Field("request", Request)
])


#
#	Response
#

### Service Providers

GetServiceProvidersSuccess = RecordType("GetServiceProvidersSuccess", [
	Field("service_providers", VectorType(ServiceProvider))
])

SaveServiceProviderSuccess = RecordType("SaveServiceProviderSuccess", [
])

ServiceProviderNameAlreadyExists = RecordType("ServiceProviderNameAlreadyExists", [
])

UpdateServiceProviderSuccess = RecordType("UpdateServiceProviderSuccess", [
])

InvalidServiceProviderId = RecordType("InvalidServiceProviderId", [
])

ChangeServiceProviderStatusSuccess = RecordType("ChangeServiceProviderStatusSuccess", [
])

### User Privileges

GetUserPrivilegesSuccess = RecordType("GetUserPrivilegesSuccess", [
	Field("forms", Menu),
	Field("user_groups", VectorType(UserGroup))
])

UserGroupNameAlreadyExists = RecordType("UserGroupNameAlreadyExists", [
])

InvalidUserGroupId = RecordType("InvalidUserGroupId", [
])

SaveUserPrivilegesSuccess = RecordType("SaveUserPrivilegesSuccess", [
])

UpdateUserPrivilegesSuccess = RecordType("UpdateUserPrivilegesSuccess", [
])

ChangeUserPrivilegeStatusSuccess = RecordType("ChangeUserPrivilegeStatusSuccess", [
])

### Users

GetClientUsersSuccess = RecordType("GetClientUsersSuccess", [
	Field("client_users", VectorType(ClientUser))
])

SaveClientUserSuccess = RecordType("SaveClientUserSuccess", [
])

EmployeeCodeAlreadyExists = RecordType("EmployeeCodeAlreadyExists", [
])

EmployeeCodeAlreadyExists = RecordType("EmployeeCodeAlreadyExists", [
])

ContactNumberAlreadyExists = RecordType("ContactNumberAlreadyExistss", [
])

UpdateClientUserSuccess = RecordType("UpdateClientUserSuccess", [
])

InvalidUserId = RecordType("InvalidUserId", [
])

ChangeClientUserStatusSuccess = RecordType("ChangeClientUserStatusSuccess", [
])

### Close Unit

GetUnitsSuccess = RecordType("GetUnitsSuccess", [
	Field("business_groups", BusinessGroupList),
	Field("legal_entities", LegalEntityList),
	Field("divisions", DivisionList),
	Field("units", UnitList)
])

CloseUnitSuccess = RecordType("CloseUnitSuccess", [
])

InvalidPassword = RecordType("InvalidPassword", [
])

Response = VariantType("Response", [
	GetServiceProvidersSuccess, SaveServiceProviderSuccess,
	ServiceProviderNameAlreadyExists,
	UpdateServiceProviderSuccess,  ChangeServiceProviderStatusSuccess,
	GetUserPrivilegesSuccess, UserGroupNameAlreadyExists, 
	InvalidUserGroupId, SaveUserPrivilegesSuccess, 
	UpdateUserPrivilegesSuccess, ChangeUserPrivilegeStatusSuccess,
	GetClientUsersSuccess, SaveClientUserSuccess, EmployeeCodeAlreadyExists,
	UpdateClientUserSuccess, InvalidUserId, ChangeClientUserStatusSuccess,
	GetUnitsSuccess, InvalidPassword, CloseUnitSuccess,ContactNumberAlreadyExists
])


