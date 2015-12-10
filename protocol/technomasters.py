__all__=  [
	"Request", "Response"
]

DomainList = VectorType(Domain)
CountryList = VectorType(Country)
UserIdList =  VectorType(USER_ID)
ClientConfigurationList = VectorType(ClientConfiguration)
UserList = VectorType(User)
ClientDetailsList = VectorType(GroupCompanyDetail)
ClientList = VectorType(Groupcompany)
BusinessGroupList= VectorType(BusinessGroup)
LegalEntityList = VectorType(LegalEntity)
DivisionList = VectorType(DivisionList)
UnitDetailsList = VectorType(UnitDetails)

#	
#	Request
#

### Client Group 

GetClientGroups = Recordtype("GetClientGroups", [
])

SaveClientGroup = Recordtype("SaveClientGroup", [
	Field("group_name",CLIENT_NAME),
	Field("country_ids", CountryList),
	Field("domain_ids", DomainList),
	Field("logo", URL),
	Field("contract_from",Date),
	Field("contract_to",Date),
	Field("incharge_persons", UserIdList),
	Field("no_of_user_licence", NO_OF_USER_LICENCE),
	Field("file_space", TOTAL_DISK_SPACE),
	Field("is_sms_subscribed", STATUS),
	Field("email_id", EMAIL_ID),
	Field("date_configurations",ClientConfigurationList)
])

UpdateClientGroup = Recordtype("UpdateClientGroup", [
	Field("client_id", CLIENT_ID),
	Field("group_name",CLIENT_NAME),
	Field("country_ids", CountryList),
	Field("domain_ids", DomainList),
	Field("logo", URL),
	Field("contract_from",Date),
	Field("contract_to",Date),
	Field("incharge_persons", UserIdList),
	Field("no_of_user_licence", NO_OF_USER_LICENCE),
	Field("file_space", TOTAL_DISK_SPACE),
	Field("is_sms_subscribed", STATUS),
	Field("email_id", EMAIL_ID),
	Field("date_configurations",ClientConfigurationList)
])

ChangeClientGroupStatus = Recordtype("ChangeClientGroupStatus", [
	Field("client_id", CLIENT_ID),
	Field("is_active",IS_ACTIVE))
])

### Clients

GetClients = Recordtype("GetClients", [
])

SaveClient = Recordtype("SaveClient", [
	Field("client_id", CLIENT_ID),
	Field("business_group", BusinessGroup),
	Field("legal_entity", LegalEntity),
	Field("division", Division),
	Field("country_wise_units", CountryWiseUnits)
])	

UpdateClient = Recordtype("UpdateClient", [
	Field("client_id", CLIENT_ID),
	Field("business_group", BusinessGroup),
	Field("legal_entity", LegalEntity),
	Field("division", Division),
	Field("country_wise_units", CountryWiseUnits)
])

ChangeClientStatus = Recordtype("ChangeClientStatus", [
	Field("client_id", CLIENT_ID),
	Field("legal_entity_id", LEGAL_ENTITY_ID),
	Field("division_id", DIVISION_ID),
	Field("is_active", IS_ACTIVE)
])

ReactivateUnit = Recordtype("ReactivateUnit", [
	Field("unit_id", UNIT_ID),
	Field("passsword", PASSWORD)
])


Request = VariantType("Request", [
	GetClientGroups, SaveClientGroup, UpdateClientGroup,
	ChangeClientGroupStatus, GetClients, SaveClient,
	UpdateClient, ChangeClientStatus, ReactivateUnit
])


#	
#	Response
#

### Client Group

GetClientGroupsSuccess = Recordtype("GetClientGroupsSuccess", [
	Field("countries", CountryList),
	Field("domains", DomainList),
	Field("users", UserList),
	Field("client_list", ClientDetailsList)
])

SaveClientGroupSuccess = Recordtype("SaveClientGroupSuccess", [
])

GroupNameAlreadyExists = Recordtype("GroupNameAlreadyExists", [
])

UsernameAlreadyExists = Recordtype("UsernameAlreadyExists", [
])

UpdateClientGroupSuccess = Recordtype("UpdateClientGroupSuccess", [
])

ChangeClientGroupStatusSuccess = Recordtype("ChangeClientGroupStatusSuccess", [
])

InvalidClientId = Recordtype("InvalidClientId", [
])

### Client Unit 

GetClientsSuccess = Recordtype("GetClientsSuccess", [
	Field("countries", CountryList),
	Field("domains", DomainList),
	Field("group_companies", ClientList),
	Field("business_groups", BusinessGroupList),
	Field("legal_entities", LegalEntityList),
	Field("divisions", DivisionList),
	Field("units", UnitDetailsList)
])

SaveClientSuccess = Recordtype("SaveClientSuccess", [
])

BusinessGroupNameAlreadyExists = Recordtype("BusinessGroupNameAlreadyExists", [
])

LegalEntityNameAlreadyExists = Recordtype("LegalEntityNameAlreadyExists", [
])

DivisionNameAlreadyExists = Recordtype("DivisionNameAlreadyExists", [
])

UnitNameAlreadyExists = Recordtype("UnitNameAlreadyExists", [
])

UnitCodeAlreadyExists = Recordtype("UnitCodeAlreadyExists", [
])

LogoSizeLimitExceeds = Recordtype("LogoSizeLimitExceeds", [
])

UpdateClientSuccess = Recordtype("UpdateClientSuccess", [
])

ChangeClientStatusSuccess = Recordtype("ChangeClientStatusSuccess", [
])

ReactivateUnitSuccess = Recordtype("ReactivateUnitSuccess", [
])

InvalidPassword = Recordtype("InvalidPassword", [
])

InvalidUnitId = Recordtype("InvalidUnitId", [
])

Response = VariantType("Response", [
	GetClientGroupsSuccess, SaveClientGroupSuccess,
	GroupNameAlreadyExists, UsernameAlreadyExists,
	UpdateClientGroupSuccess, ChangeClientGroupStatusSuccess,
	InvalidClientId, GetClientsSuccess, SaveClientSuccess, 
	BusinessGroupNameAlreadyExists, LegalEntityNameAlreadyExists,
	DivisionNameAlreadyExists, UnitNameAlreadyExists, 
	UnitCodeAlreadyExists, LogoSizeLimitExceeds,
	UpdateClientSuccess, ChangeClientStatusSuccess,
	ReactivateUnitSuccess, InvalidPassword, InvalidUnitId
])