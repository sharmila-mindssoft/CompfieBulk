from basics.types import VectorType, RecordType, VariantType, MapType, Field
from common import (CLIENT_NAME, URL, DATE, NO_OF_USER_LICENCE, CLIENT_ID, USER_ID, CLIENT_NAME,
	TOTAL_DISK_SPACE, STATUS, EMAIL_ID, IS_ACTIVE, LEGAL_ENTITY_ID, DIVISION_ID, UNIT_ID, GROUP_ID,
	PASSWORD, EMPLOYEE_NAME, CONTACT_NUMBER, UNIT_NAME, ADDRESS, REMAINING_USER_LICENCE, USED_DISK_SPACE)
from core import (Domain, Country, User, GroupCompany, BusinessGroup, Division,
	UnitDetails, GroupCompanyDetail, ClientConfiguration, LegalEntity, CountryWiseUnits)




__all__=  [
	"Request", "Response", "LICENCE_HOLDER_DETAILS", "PROFILE_DETAIL",
	"PROFILES"
]

DomainList = VectorType(Domain)
CountryList = VectorType(Country)
UserIdList =  VectorType(USER_ID)
ClientConfigurationList = VectorType(ClientConfiguration)
UserList = VectorType(User)
ClientDetailsList = VectorType(GroupCompanyDetail)
ClientList = VectorType(GroupCompany)
BusinessGroupList= VectorType(BusinessGroup)
LegalEntityList = VectorType(LegalEntity)
DivisionList = VectorType(Division)
UnitDetailsList = VectorType(UnitDetails)

#	
#	Request
#

### Client Group 

GetClientGroups = RecordType("GetClientGroups", [
])

SaveClientGroup = RecordType("SaveClientGroup", [
	Field("group_name",CLIENT_NAME),
	Field("country_ids", CountryList),
	Field("domain_ids", DomainList),
	Field("logo", URL),
	Field("contract_from",DATE),
	Field("contract_to",DATE),
	Field("incharge_persons", UserIdList),
	Field("no_of_user_licence", NO_OF_USER_LICENCE),
	Field("file_space", TOTAL_DISK_SPACE),
	Field("is_sms_subscribed", STATUS),
	Field("email_id", EMAIL_ID),
	Field("DATE_configurations",ClientConfigurationList)
])

UpdateClientGroup = RecordType("UpdateClientGroup", [
	Field("client_id", CLIENT_ID),
	Field("group_name",CLIENT_NAME),
	Field("country_ids", CountryList),
	Field("domain_ids", DomainList),
	Field("logo", URL),
	Field("contract_from",DATE),
	Field("contract_to",DATE),
	Field("incharge_persons", UserIdList),
	Field("no_of_user_licence", NO_OF_USER_LICENCE),
	Field("file_space", TOTAL_DISK_SPACE),
	Field("is_sms_subscribed", STATUS),
	Field("email_id", EMAIL_ID),
	Field("DATE_configurations",ClientConfigurationList)
])

ChangeClientGroupStatus = RecordType("ChangeClientGroupStatus", [
	Field("client_id", CLIENT_ID),
	Field("is_active",IS_ACTIVE)
])

### Clients

GetClients = RecordType("GetClients", [
])

SaveClient = RecordType("SaveClient", [
	Field("client_id", CLIENT_ID),
	Field("business_group", BusinessGroup),
	Field("legal_entity", LegalEntity),
	Field("division", Division),
	Field("country_wise_units", CountryWiseUnits)
])	

UpdateClient = RecordType("UpdateClient", [
	Field("client_id", CLIENT_ID),
	Field("business_group", BusinessGroup),
	Field("legal_entity", LegalEntity),
	Field("division", Division),
	Field("country_wise_units", CountryWiseUnits)
])

ChangeClientStatus = RecordType("ChangeClientStatus", [
	Field("client_id", CLIENT_ID),
	Field("legal_entity_id", LEGAL_ENTITY_ID),
	Field("division_id", DIVISION_ID),
	Field("is_active", IS_ACTIVE)
])

ReactivateUnit = RecordType("ReactivateUnit", [
	Field("unit_id", UNIT_ID),
	Field("passsword", PASSWORD)
])

GetClientProfile = RecordType("GetClientProfile", [
])


Request = VariantType("Request", [
	GetClientGroups, SaveClientGroup, UpdateClientGroup,
	ChangeClientGroupStatus, GetClients, SaveClient,
	UpdateClient, ChangeClientStatus, ReactivateUnit,
	GetClientProfile
])


#	
#	Response
#

### Client Group

GetClientGroupsSuccess = RecordType("GetClientGroupsSuccess", [
	Field("countries", CountryList),
	Field("domains", DomainList),
	Field("users", UserList),
	Field("client_list", ClientDetailsList)
])

SaveClientGroupSuccess = RecordType("SaveClientGroupSuccess", [
])

GroupNameAlreadyExists = RecordType("GroupNameAlreadyExists", [
])

UpdateClientGroupSuccess = RecordType("UpdateClientGroupSuccess", [
])

ChangeClientGroupStatusSuccess = RecordType("ChangeClientGroupStatusSuccess", [
])

InvalidClientId = RecordType("InvalidClientId", [
])

### Client Unit 

GetClientsSuccess = RecordType("GetClientsSuccess", [
	Field("countries", CountryList),
	Field("domains", DomainList),
	Field("group_companies", ClientList),
	Field("business_groups", BusinessGroupList),
	Field("legal_entities", LegalEntityList),
	Field("divisions", DivisionList),
	Field("units", UnitDetailsList)
])

SaveClientSuccess = RecordType("SaveClientSuccess", [
])

BusinessGroupNameAlreadyExists = RecordType("BusinessGroupNameAlreadyExists", [
])

LegalEntityNameAlreadyExists = RecordType("LegalEntityNameAlreadyExists", [
])

DivisionNameAlreadyExists = RecordType("DivisionNameAlreadyExists", [
])

UnitNameAlreadyExists = RecordType("UnitNameAlreadyExists", [
])

UnitCodeAlreadyExists = RecordType("UnitCodeAlreadyExists", [
])

LogoSizeLimitExceeds = RecordType("LogoSizeLimitExceeds", [
])

UpdateClientSuccess = RecordType("UpdateClientSuccess", [
])

ChangeClientStatusSuccess = RecordType("ChangeClientStatusSuccess", [
])

ReactivateUnitSuccess = RecordType("ReactivateUnitSuccess", [
])

LICENCE_HOLDER_DETAILS = RecordType("LICENCE_HOLDER_DETAILS", [
	Field("user_id", USER_ID),
	Field("user_name", EMPLOYEE_NAME),
	Field("email_id", EMAIL_ID),
	Field("contact_no", CONTACT_NUMBER),
	Field("seating_unit_name", UNIT_NAME),
	Field("address", ADDRESS),
	Field("total_disk_space", TOTAL_DISK_SPACE),
	Field("used_disk_space", USED_DISK_SPACE)
])

PROFILE_DETAIL = RecordType("PROFILE_DETAIL", [
	Field("contract_from", DATE),
	Field("contract_to", DATE),
	Field("no_of_user_licence", NO_OF_USER_LICENCE),
	Field("remaining_licence", REMAINING_USER_LICENCE),
	Field("total_disk_space", REMAINING_USER_LICENCE),
	Field("used_disk_space", USED_DISK_SPACE),
	Field("licence_holders", VectorType(LICENCE_HOLDER_DETAILS))
])

PROFILES = RecordType("PROFILES", [
	Field("client_id", GROUP_ID),
	Field("profile_detail", PROFILE_DETAIL),
])

GetClientProfileSuccess = RecordType("GetClientProfileSuccess", [
	Field("group_companies", ClientList),
	Field("profiles", VectorType(PROFILES))
])

Response = VariantType("Response", [
	GetClientGroupsSuccess, SaveClientGroupSuccess,
	GroupNameAlreadyExists, UpdateClientGroupSuccess, 
	ChangeClientGroupStatusSuccess, InvalidClientId, 
	GetClientsSuccess, SaveClientSuccess, 
	BusinessGroupNameAlreadyExists, LegalEntityNameAlreadyExists,
	DivisionNameAlreadyExists, UnitNameAlreadyExists, 
	UnitCodeAlreadyExists, LogoSizeLimitExceeds,
	UpdateClientSuccess, ChangeClientStatusSuccess,
	ReactivateUnitSuccess, GetClientProfileSuccess
])