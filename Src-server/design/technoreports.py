from basics.types import VectorType, RecordType, VariantType, MapType, Field, OptionalType
from common import (COUNTRY_ID, GROUP_ID, BUSINESS_GROUP_ID, LEGAL_ENTITY_ID,
	DIVISION_ID, UNIT_ID, DOMAIN_ID, LEVEL_1_STATUTORY_ID, STATUTORY_PROVISION,
	NOTIFICATION_TEXT, TIMESTAMP, SESSION_TOKEN, UNIT_NAME, ADDRESS)
from core import (Country, Domain, GroupCompany, BusinessGroup, LegalEntity, Division, Statutory,
	Unit, UnitDetails, AssignedStatutory,
	APPLICABILITY_STATUS)

__all__=  [
	"Request", "Response", "RequestFormat", "COUNTRY_WISE_NOTIFICATIONS", "UNIT_WISE_ASSIGNED_STATUTORIES"
]

DomainIdList = VectorType(DOMAIN_ID)
CountryList = VectorType(Country)
DomainList = VectorType(Domain)
ClientList = VectorType(GroupCompany)
BusinessGroupList = VectorType(BusinessGroup)
LegalEntityList = VectorType(LegalEntity)
DivisionList = VectorType(Division)
UnitList = VectorType(Unit)
UnitDetailsList = VectorType(UnitDetails)
AssignedStatutoryList = VectorType(AssignedStatutory)

#
# Request
#

### Client Details Report

GetClientDetailsReportFilters = RecordType("GetClientDetailsReportFilters", [
])

GetClientDetailsReportData = RecordType("GetClientDetailsReportData", [
	Field("country_id", COUNTRY_ID),
	Field("group_id", GROUP_ID),
	Field("business_group_id", OptionalType(BUSINESS_GROUP_ID)),
	Field("legal_entity_id", OptionalType(LEGAL_ENTITY_ID)),
	Field("division_id", OptionalType(DIVISION_ID)),
	Field("unit_id", OptionalType(UNIT_ID)),
	Field("domain_ids", OptionalType(DomainIdList))

])

### Statutory Notifications Report

GetStatutoryNotifications = RecordType("GetStatutoryNotifications", [
])

### Assigned Statutory Report

GetAssignedStatutoryReportFilters = RecordType("GetAssignedStatutoryReportFilters", [
])

GetAssignedStatutoryReport = RecordType("GetAssignedStatutoryReport", [
	Field("country_id", COUNTRY_ID),
	Field("domain_id" , DOMAIN_ID),
	Field("group_id", OptionalType(GROUP_ID)),
	Field("business_group_id", OptionalType(BUSINESS_GROUP_ID)),
	Field("legal_entity_id", OptionalType(LEGAL_ENTITY_ID)),
	Field("division_id", OptionalType(DIVISION_ID)),
	Field("unit_id", OptionalType(UNIT_ID)),
	Field("level_1_statutory_id", OptionalType(LEVEL_1_STATUTORY_ID)),
	Field("applicability_status", APPLICABILITY_STATUS)
])

Request = VariantType("Request", [
	GetClientDetailsReportFilters, GetClientDetailsReportData,
	GetStatutoryNotifications, GetAssignedStatutoryReportFilters,
	GetAssignedStatutoryReport	
])

RequestFormat = RecordType("RequestFormat", [
	Field("session_token", SESSION_TOKEN),
	Field("request", Request)
])


#
# Response
#

### Client Details

GetClientDetailsReportFiltersSuccess = RecordType("GetClientDetailsReportFiltersSuccess", [
	Field("countries", CountryList),
	Field("domains", DomainList),
	Field("group_companies", ClientList),
	Field("business_groups" , OptionalType(BusinessGroupList)),
	Field("legal_entities", LegalEntityList),
	Field("divisions", OptionalType(DivisionList)),
	Field("units", UnitList)
])

GetClientDetailsReportDataSuccess = RecordType("GetClientDetailsReportDataSuccess", [
	Field("units", UnitDetailsList)
])

### Statutory Notifications

NOTIFICATIONS = RecordType("NOTIFICATIONS", [
	Field("statutory_provision", STATUTORY_PROVISION),
	Field("notification_text", NOTIFICATION_TEXT),
	Field("date_and_time", TIMESTAMP)
])

COUNTRY_WISE_NOTIFICATIONS = RecordType("COUNTRY_WISE_NOTIFICATIONS", [
	Field("country_id", CountryList),
	Field("domain_id", DomainList),
	Field("notifications", VectorType(NOTIFICATION_TEXT))
])

GetStatutoryNotificationsSuccess = RecordType("GetStatutoryNotificationsSuccess", [
	Field("countries", CountryList),
	Field("domains", DomainList),
	Field("level_1_statutories", MapType(COUNTRY_ID, Statutory)),
	Field("country_wise_notifications", VectorType(COUNTRY_WISE_NOTIFICATIONS))
])

### Assigned Statutory Report

GetAssignedStatutoryReportFiltersSuccess = RecordType("GetAssignedStatutoryReportFiltersSuccess", [
	Field("countries", CountryList),
	Field("domains", DomainList),
	Field("groups", ClientList),
	Field("business_groups", BusinessGroupList),
	Field("legal_entities", LegalEntityList),
	Field("divisions", DivisionList),
	Field("units", UnitList),
	Field("level_1_statutories", MapType(COUNTRY_ID, Statutory)),
])

UNIT_WISE_ASSIGNED_STATUTORIES = RecordType("UNIT_WISE_ASSIGNED_STATUTORIES", [
	Field("unit_id", UNIT_ID),
	Field("unit_name", UNIT_NAME),
	Field("group_name", UNIT_NAME),
	Field("business_group_name", UNIT_NAME),
	Field("legal_entity_name", UNIT_NAME),
	Field("division_name", UNIT_NAME)
	Field("address", ADDRESS),
	Field("assigned_statutories", AssignedStatutoryList),
])

GetAssignedStatutoryReportSuccess = RecordType("GetAssignedStatutoryReportSuccess", [
	Field("unit_wise_assigned_statutories", VectorType(UNIT_WISE_ASSIGNED_STATUTORIES))
])


Response = VariantType("Response", [
	GetClientDetailsReportFiltersSuccess, GetClientDetailsReportDataSuccess,
	GetStatutoryNotificationsSuccess, GetAssignedStatutoryReportFiltersSuccess,
	GetAssignedStatutoryReportSuccess
])