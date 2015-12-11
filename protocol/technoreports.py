__all__=  [
	"Request", "Response"
]

DomainIdList = VectorType(DOMAIN_ID)
CountryList = VectorType(Country)
DomainList = VectorType(Domain)
ClientList = VectorType(GroupCompany)
BusinessGroupList = VectorType(BusinessGroup)
LegalEntity = VectorType(BusinessGroup)

#
# Request
#

### Client Details Report

GetClientDetailsReportFilters = Recordtype("GetClientDetailsReportFilters", [
])

GetClientDetailsReportData = Recordtype("GetClientDetailsReportData", [
	Field("country_id", COUNTRY_ID),
	Field("group_id", GROUP_ID),
	Field("business_group_id", BUSINESS_GROUP_ID),
	Field("legal_entity_id", LEGAL_ENTITY_ID),
	Field("division_id", DIVISION_ID),
	Field("unit_id", UNIT_ID),
	Field("domain_ids", DomainIdList)

])

### Statutory Notifications Report

GetStatutoryNotifications = Recordtype("GetStatutoryNotifications", [
])

### Assigned Statutory Report

GetAssignedStatutoryReportFilters = Recordtype("GetAssignedStatutoryReportFilters", [
])

GetAssignedStatutoryReport = Recordtype("GetAssignedStatutoryReport", [
	Field("country_id", COUNTRY_ID),
	Field("domain_ids" , DomainIdList),
	Field("group_id", GROUP_ID),
	Field("business_group_id", BUSINESS_GROUP_ID),
	Field("legal_entity_id", LEGAL_ENTITY_ID),
	Field("division_id", DIVISION_ID),
	Field("unit_id", UNIT_ID),
	Field("level_1_statutory_id", LEVEL_1_STATUTORY_ID),
	Field("applicability_status", APPLICABILITY_STATUS)
])

Request = VariantType("Request", [
	GetClientDetailsReportFilters, GetClientDetailsReportData,
	GetStatutoryNotifications, GetAssignedStatutoryReportFilters,
	GetAssignedStatutoryReport	
])

#
# Response
#

GetClientDetailsReportFiltersSuccess = Recordtype("GetClientDetailsReportFiltersSuccess", [
	Field("countries", CountryList),
	Field("domains", DomainList),
	Field("group_companies": ClientList),
	Field("business_groups" , BusinessGroupList),
	Field("legal_entities", LegalEntityList),
	Field("divisions", DivisionList),
	Field("units", UnitList)
])