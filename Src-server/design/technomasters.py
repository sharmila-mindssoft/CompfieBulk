from basics.types import VectorType, RecordType, VariantType, MapType, Field, OptionalType, Int8
from common import (CLIENT_NAME, URL, DATE, NO_OF_USER_LICENCE, CLIENT_ID, USER_ID, CLIENT_NAME,
	TOTAL_DISK_SPACE, STATUS, EMAIL_ID, IS_ACTIVE, LEGAL_ENTITY_ID, DIVISION_ID, UNIT_ID, GROUP_ID,
	PASSWORD, EMPLOYEE_NAME, CONTACT_NUMBER, UNIT_NAME, ADDRESS, REMAINING_USER_LICENCE, USED_DISK_SPACE, 
	SESSION_TOKEN, COUNTRY_ID, DOMAIN_ID, SHORT_NAME, BUSINESS_GROUP_ID, BUSINESS_GROUP_NAME,
	LEGAL_ENTITY_NAME, DIVISION_NAME , LOCATION, INDUSTRY_NAME, GEOGRAPHY_ID, UNIT_CODE,
	INDUSTRY_ID)
from core import (Domain, Country, User, GroupCompany, BusinessGroup, Division,
	UnitDetails, GroupCompanyDetail, ClientConfiguration, LegalEntity, CountryWiseUnits,
	Unit, Industry, Geography, Level)


__all__=  [
	"Request", "Response", "RequestFormat", "LICENCE_HOLDER_DETAILS", "PROFILE_DETAIL",
	"PROFILES", "BUSINESS_GROUP", "LEGAL_ENTITY", "DIVISION", "UNIT", "COUNTRYWISEUNITS"
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
LevelList = VectorType(Level)

#	
#	Request
#

### Client Group 

GetClientGroups = RecordType("GetClientGroups", [
])

SaveClientGroup = RecordType("SaveClientGroup", [
	Field("group_name",CLIENT_NAME),
	Field("country_ids", VectorType(COUNTRY_ID)),
	Field("domain_ids", VectorType(DOMAIN_ID)),
	Field("logo", URL),
	Field("contract_from",DATE),
	Field("contract_to",DATE),
	Field("incharge_persons", UserIdList),
	Field("no_of_user_licence", NO_OF_USER_LICENCE),
	Field("file_space", TOTAL_DISK_SPACE),
	Field("is_sms_subscribed", STATUS),
	Field("email_id", EMAIL_ID),
	Field("date_configurations",ClientConfigurationList),
	Field("short_name", SHORT_NAME),
])

UpdateClientGroup = RecordType("UpdateClientGroup", [
	Field("client_id", CLIENT_ID),
	Field("group_name",CLIENT_NAME),
	Field("country_ids", VectorType(COUNTRY_ID)),
	Field("domain_ids", VectorType(DOMAIN_ID)),
	Field("logo", URL),
	Field("contract_from",DATE),
	Field("contract_to",DATE),
	Field("incharge_persons", UserIdList),
	Field("no_of_user_licence", NO_OF_USER_LICENCE),
	Field("file_space", TOTAL_DISK_SPACE),
	Field("is_sms_subscribed", STATUS),
	Field("date_configurations",ClientConfigurationList)
])

ChangeClientGroupStatus = RecordType("ChangeClientGroupStatus", [
	Field("client_id", CLIENT_ID),
	Field("is_active",IS_ACTIVE)
])

### Clients

GetClients = RecordType("GetClients", [
])

BUSINESS_GROUP = RecordType("BUSINESS_GROUP", [
	Field("business_group_id", OptionalType(BUSINESS_GROUP_ID)),
	Field("business_name",BUSINESS_GROUP_NAME)
])

LEGAL_ENTITY = RecordType("LEGAL_ENTITY", [
	Field("legal_entity_id", OptionalType(LEGAL_ENTITY_ID)),
	Field("legal_entity_name",LEGAL_ENTITY_NAME)
])

DIVISION = RecordType("DIVISION", [
	Field("division_id", OptionalType(DIVISION_ID)),
	Field("division_name",DIVISION_NAME)
])

UNIT = RecordType("UNIT", [
	Field("unit_id", OptionalType(UNIT_ID)),
    Field("geography_id", GEOGRAPHY_ID),
    Field("unit_code", UNIT_CODE),
    Field("unit_name", UNIT_NAME),
    Field("industry_id", INDUSTRY_ID),
    Field("industry_name", INDUSTRY_NAME),
    Field("unit_address", ADDRESS),
    Field("unit_location", LOCATION),
    Field("postal_code", Int8),
    Field("domain_ids", VectorType(DOMAIN_ID))
])

COUNTRYWISEUNITS = RecordType("CountryWiseUnits", [
	Field("country_id", COUNTRY_ID),
	Field("units", VectorType(UNIT)),
])

SaveClient = RecordType("SaveClient", [
	Field("client_id", CLIENT_ID),
	Field("business_group", OptionalType(BUSINESS_GROUP)),
	Field("legal_entity", LEGAL_ENTITY),
	Field("division", OptionalType(DIVISION)),
	Field("country_wise_units", CountryWiseUnits)
])	

UpdateClient = RecordType("UpdateClient", [
	Field("client_id", CLIENT_ID),
	Field("business_group", OptionalType(BusinessGroup)),
	Field("legal_entity", LegalEntity),
	Field("division", OptionalType(Division)),
	Field("country_wise_units", CountryWiseUnits)
])

ChangeClientStatus = RecordType("ChangeClientStatus", [
	Field("client_id", CLIENT_ID),
	Field("legal_entity_id", LEGAL_ENTITY_ID),
	Field("division_id", OptionalType(DIVISION_ID)),
	Field("is_active", IS_ACTIVE)
])

ReactivateUnit = RecordType("ReactivateUnit", [
	Field("client_id", CLIENT_ID),
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

RequestFormat = RecordType("RequestFormat", [
	Field("session_token", SESSION_TOKEN),
	Field("request", Request)
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
	Field("geography_levels", MapType(COUNTRY_ID, LevelList)),
	Field("geographies", MapType(COUNTRY_ID, VectorType(Geography))),
	Field("industries", VectorType(Industry))
	Field("domains", DomainList),
	Field("group_companies", ClientList),
	Field("business_groups", OptionalType(BusinessGroupList)),
	Field("legal_entities", LegalEntityList),
	Field("divisions", OptionalType(DivisionList)),
	Field("units", VectorType(Unit))
])

SaveClientSuccess = RecordType("SaveClientSuccess", [
])

EmailIDAlreadyExists = RecordType("EmailIDAlreadyExists", [
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

InvalidBusinessGroupId = RecordType("InvalidBusinessGroupId", [
])

InvalidLegalEntityId = RecordType("InvalidLegalEntityId", [
])

InvalidDivisionId = RecordType("InvalidDivisionId", [
])

InvalidUnitId = RecordType("InvalidUnitId", [
])

InvalidPassword = RecordType("InvalidPassword", [
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
	Field(GROUP_ID, PROFILE_DETAIL)
])

GetClientProfileSuccess = RecordType("GetClientProfileSuccess", [
	Field("group_companies", ClientList),
	Field("profiles", PROFILES)
])

UserIsNotResponsibleForAnyClient = RecordType("UserIsNotResponsibleForAnyClient", [
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
	ReactivateUnitSuccess, GetClientProfileSuccess,
	InvalidBusinessGroupId,InvalidLegalEntityId,InvalidDivisionId,
	InvalidUnitId, InvalidPassword, UserIsNotResponsibleForAnyClient]
)