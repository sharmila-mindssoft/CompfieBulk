from core import *
from common import *
from types import VectorType

__all__=  [
	"Request", "Response"
]

FormIdList = VectorType(FORM_ID)
CountryIdList = VectorType(COUNTRY_ID)
DomainIdList = VectorType(DOMAIN_ID)
UnitIdList = VectorType(UNIT_ID)

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

UpdateClientUser = RecordType("UpdateClientUser", [
	Field("user_id", USER_ID),
	Field("is_active", IS_ACTIVE)
])

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
	UpdateClientUser, GetUnits, CloseUnit
])

#
#	Response
#



