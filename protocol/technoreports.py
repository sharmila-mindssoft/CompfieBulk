from common import *
from core import *

__all__=  [
	"Request", "Response" ,"COUNTRY_WISE_NOTIFICATIONS", "UNIT_WISE_ASSIGNED_STATUTORIES"
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
	Field("business_group_id", BUSINESS_GROUP_ID),
	Field("legal_entity_id", LEGAL_ENTITY_ID),
	Field("division_id", DIVISION_ID),
	Field("unit_id", UNIT_ID),
	Field("domain_ids", DomainIdList)

])

### Statutory Notifications Report

GetStatutoryNotifications = RecordType("GetStatutoryNotifications", [
])

### Assigned Statutory Report

GetAssignedStatutoryReportFilters = RecordType("GetAssignedStatutoryReportFilters", [
])

GetAssignedStatutoryReport = RecordType("GetAssignedStatutoryReport", [
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

### Client Details

GetClientDetailsReportFiltersSuccess = RecordType("GetClientDetailsReportFiltersSuccess", [
	Field("countries", CountryList),
	Field("domains", DomainList),
	Field("group_companies", ClientList),
	Field("business_groups" , BusinessGroupList),
	Field("legal_entities", LegalEntityList),
	Field("divisions", DivisionList),
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
	Field("legal_entities", LegalEntityList),
	Field("divisions", DivisionList),
	Field("units", UnitList),
	Field("level_1_statutories", MapType(COUNTRY_ID, Statutory)),
])

UNIT_WISE_ASSIGNED_STATUTORIES = RecordType("UNIT_WISE_ASSIGNED_STATUTORIES", [
	Field("unit_id", CountryList),
	Field("address", DomainList),
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