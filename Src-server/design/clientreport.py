from basics.types import RecordType, VariantType, Field, MapType, VectorType, OptionalType
from core import (USER_TYPE,
	COMPLIANCE_STATUS, APPLICABILITY_STATUS, 
	COMPLIANCE_ACTIVITY_STATUS, COMPLIANCE_FREQUENCY,
	Country, Domain, Compliance, Statutory, Unit,
	BusinessGroup, LegalEntity, Division, ServiceProvider,
	StatutoryDates
)
from common import ( Text20, COUNTRY_ID, DOMAIN_ID, STATUTORY_ID, UNIT_ID, COMPLIANCE_ID, USER_ID,
	BUSINESS_GROUP_ID, LEGAL_ENTITY_ID, DIVISION_ID, UNIT_ID, STATUTORY_ID, Int8, SERVICE_PROVIDER_ID,
	COMPLIANCE_ID, Text20, LEVEL_1_STATUTORY_ID, Text100, EMPLOYEE_CODE, Text50, Text500, ADDRESS, 
	LEVEL_1_STATUTORY_NAME, CONTACT_NUMBER, UNIT_NAME, FORM_ID, FORM_NAME, SESSION_TOKEN)


__all__ = [
	"Request", "Response", "RequestFormat", "ComplianceName", "User", "ComplianceDetails", "Level1Statutory", 
	"ServiceProviderCompliance", "Activities", "ActivityCompliance", "ActivityLog", 
	"ApplicabilityCompliance", "AssigneeCompliance", "ComplianceForUnit", "ComplianceList",
	"ComplianceUnit", "DomainWiseCompliance", "FormName", "LoginTrace", "ReassignCompliance",
	"ReassignHistory", "StatutoryReassignCompliance", "UnitCompliance", "UnitWiseCompliance",
	"UnitName", "UserName", "UserWiseCompliance"
]

#
# Request
#

GetComplianceDetailsReportFilters = RecordType("GetComplianceDetailsReportFilters", [])

GetComplianceDetailsReport = RecordType("GetComplianceDetailsReport", [
	Field("country_id", COUNTRY_ID),
	Field("domain_id", DOMAIN_ID),
	Field("statutory_id", OptionalType(STATUTORY_ID)),
	Field("unit_id", OptionalType(UNIT_ID)),
	Field("compliance_id", OptionalType(COMPLIANCE_ID)),
	Field("assignee_id", OptionalType(USER_ID)),
	Field("from_date", OptionalType(Text20)),
	Field("to_date", OptionalType(Text20)),
	Field("compliance_status", COMPLIANCE_STATUS)
])

GetRiskReportFilters = RecordType("GetRiskReportFilters", [])

GetRiskReport = RecordType("GetRiskReport", [
	Field("country_id", COUNTRY_ID),
	Field("domain_id", DOMAIN_ID),
	Field("business_group_id", OptionalType(BUSINESS_GROUP_ID)),
	Field("legal_entity_id", OptionalType(LEGAL_ENTITY_ID)),
	Field("division_id", OptionalType(DIVISION_ID)),
	Field("unit_id", OptionalType(UNIT_ID)),
	Field("statutory_id",  OptionalType(STATUTORY_ID)),
	Field("statutory_status", Int8)
])

GetServiceProviderReportFilters = RecordType("GetServiceProviderReportFilters", [])

GetServiceProviderWiseCompliance = RecordType("GetServiceProviderWiseCompliance", [
	Field("country_id", COUNTRY_ID),
	Field("domain_id", DOMAIN_ID),
	Field("statutory_id", STATUTORY_ID),
	Field("unit_id",  OptionalType(UNIT_ID)),
	Field("service_provider_id", OptionalType(SERVICE_PROVIDER_ID))
])

GetClientReportFilters = RecordType("GetClientReportFilters", [])

GetAssigneewisecomplianceReport = RecordType(
	"GetAssigneewisecomplianceReport", 
	[
		Field("country_id", COUNTRY_ID),
		Field("domain_id", DOMAIN_ID),
		Field("business_group_id", OptionalType(BUSINESS_GROUP_ID)),
		Field("legal_entity_id", OptionalType(LEGAL_ENTITY_ID)),
		Field("division_id"  , OptionalType(DIVISION_ID)),
		Field("unit_id", OptionalType(UNIT_ID)),
		Field("user_id", OptionalType(USER_ID)),
	]
)

GetUnitwisecomplianceReport = RecordType(
	"GetUnitwisecomplianceReport", [
		Field("country_id", COUNTRY_ID),
		Field("domain_id", DOMAIN_ID),
		Field("business_group_id",OptionalType(BUSINESS_GROUP_ID)),
		Field("legal_entity_id", OptionalType(LEGAL_ENTITY_ID)),
		Field("division_id"  , OptionalType(DIVISION_ID)),
		Field("unit_id", OptionalType(UNIT_ID)),
		Field("user_id", OptionalType(USER_ID)),
	]
)

GetReassignComplianceTaskReportFilters = RecordType("GetReassignComplianceTaskReportFilters", [])

GetReassignComplianceTaskDetails = RecordType(
	"GetReassignComplianceTaskDetails", [
		Field("country_id", COUNTRY_ID),
		Field("domain_id", DOMAIN_ID),
		Field("unit_id", OptionalType(UNIT_ID)),
		Field("statutory_id", OptionalType(STATUTORY_ID)),
		Field("compliance_id", OptionalType(COMPLIANCE_ID)),
		Field("user_id", OptionalType(USER_ID)),
		Field("from_date", OptionalType(Text20)),
		Field("to_date", OptionalType(Text20)),
	]
)

GetTaskApplicabilityStatusFilters = RecordType("GetTaskApplicabilityStatusFilters", [])

GetComplianceTaskApplicabilityStatusReport = RecordType(
	"GetComplianceTaskApplicabilityStatusReport", [
		Field("country_id", COUNTRY_ID),
		Field("domain_id", DOMAIN_ID),
		Field("business_group_id", OptionalType(BUSINESS_GROUP_ID)),
		Field("legal_entity_id", OptionalType(LEGAL_ENTITY_ID)),
		Field("division_id", OptionalType(DIVISION_ID)),
		Field("unit_id", OptionalType(UNIT_ID)),
		Field("statutory_id", OptionalType(STATUTORY_ID)),
		Field("applicable_status", OptionalType(APPLICABILITY_STATUS))
	]
)

GetComplianceActivityReportFilters = RecordType("GetComplianceActivityReportFilters", [])

GetComplianceActivityReport = RecordType(
	"GetComplianceActivityReport", [
		Field("user_type", USER_TYPE),
		Field("user_id", OptionalType(USER_ID)),
		Field("domain_id", OptionalType(DOMAIN_ID)),
		Field("statutory_id", OptionalType(STATUTORY_ID)),
		Field("unit_id", OptionalType(UNIT_ID)),
		Field("compliance_id", OptionalType(COMPLIANCE_ID)),
		Field("from_date", OptionalType(Text20)),
		Field("to_date", OptionalType(Text20))
	]
)

GetReassignedHistoryReportFilters = RecordType("GetReassignedHistoryReportFilters", [])

GetReassignedHistoryReport = RecordType(
	"GetReassignedHistoryReport", [
		Field("country_id", COUNTRY_ID),
		Field("domain_id", DOMAIN_ID),
		Field("unit_id", OptionalType(UNIT_ID)),
		Field("level_1_statutory_id", OptionalType(LEVEL_1_STATUTORY_ID)),
		Field("compliance_id", OptionalType(COMPLIANCE_ID)),
		Field("user_id", OptionalType(USER_ID))
	]
)

GetStatutoryNotificationsListFilters = RecordType("GetStatutoryNotificationsListFilters", [])

GetStatutoryNotificationsListReport = RecordType("GetStatutoryNotificationsListReport", [
	Field('country_id', COUNTRY_ID),
	Field('domain_id', DOMAIN_ID),
	Field('business_group_id', BUSINESS_GROUP_ID),
	Field('legal_entity_id', LEGAL_ENTITY_ID),
	Field('division_id', DIVISION_ID),
	Field('unit_id', UNIT_ID),
	Field('level_1_statutory_id', LEVEL_1_STATUTORY_ID),
	Field('from_date', Text20),
	Field('to_date', Text20)
])


GetActivityLogFilters = RecordType("GetActivityLogFilters", [])

GetActivityLogReport = RecordType("GetActivityLogReport", [
	Field("from_date", Text20),
	Field("to_date", Text20),
	Field("form_name", OptionalType(Text20)),
	Field("action", OptionalType(Text100))
])

GetLoginTrace = RecordType("GetLoginTrace", [])

Request = VariantType("Request", [
	GetComplianceDetailsReportFilters,
	GetComplianceDetailsReport,
	GetRiskReportFilters,
	GetRiskReport,
	GetServiceProviderReportFilters,
	GetServiceProviderWiseCompliance,
	GetClientReportFilters,
	GetAssigneewisecomplianceReport,
	GetUnitwisecomplianceReport,
	GetReassignComplianceTaskReportFilters,
	GetReassignComplianceTaskDetails,
	GetTaskApplicabilityStatusFilters,
	GetComplianceTaskApplicabilityStatusReport,
	GetComplianceActivityReportFilters,
	GetComplianceActivityReport,
	GetReassignedHistoryReportFilters,
	GetReassignedHistoryReport,
	GetStatutoryNotificationsListFilters,
	GetStatutoryNotificationsListReport,
	GetActivityLogFilters,
	GetActivityLogReport,
	GetLoginTrace,
])

RequestFormat = RecordType("RequestFormat", [
	Field("session_token", SESSION_TOKEN),
	Field("request", Request)
])


#
# Response
#

User = RecordType("User", [
	Field("employee_id", USER_ID),
	Field("employee_code", EMPLOYEE_CODE),
	Field("employee_name", Text50)
]) 

ComplianceName = RecordType("ComplianceName", [
	Field("compliance_id", COMPLIANCE_ID),
	Field("compliance_name", Text100)

])

DomainStatutoryMap = MapType(DOMAIN_ID, VectorType(Statutory))

GetComplianceDetailsReportFiltersSuccess =  RecordType("GetComplianceDetailsReportFiltersSuccess", [
	Field("countries", VectorType(Country)),
	Field("domains", VectorType(Domain)),
	Field("level_1_statutories", MapType(COUNTRY_ID, DomainStatutoryMap)),
	Field("units", VectorType(Unit)),
	Field("Compliances", VectorType(ComplianceName)),
	Field("users", VectorType(User))

])

# Compliance Details

ComplianceDetails = RecordType("ComplianceDetails", [
	Field("compliance_name", Text100),
	Field("assignee", Text100),
	Field("due_date", Text20),
	Field("completion_date", Text20),
	Field("validity_date", Text20),
	Field("documents", VectorType(Text50)),
	Field("remarks", Text500)
])

GetComplianceDetailsReportSuccess =  RecordType("GetComplianceDetailsReportSuccess", [
	Field("unit_id", UNIT_ID),
	Field("unit_name", Text100),
	Field("address", ADDRESS),
	Field("Compliances", VectorType(ComplianceDetails))
])

GetRiskReportFiltersSuccess =  RecordType("GetRiskReportFiltersSuccess", [
	Field("countries", VectorType(Country)),
	Field("domains", VectorType(Domain)),
	Field("business_groups", VectorType(BusinessGroup)),
	Field("legal_entities", VectorType(LegalEntity)),
	Field("divisions", VectorType(Division)),
	Field("units", VectorType(Unit)),
	Field("level1_statutories", MapType(COUNTRY_ID, DomainStatutoryMap))
])

# Risk Report

Level1Statutory = RecordType("Level1Statutory", [
	Field("unit_name", Text100),
	Field("address", ADDRESS),
	Field("compliances", VectorType(Compliance))
])

GetRiskReportSuccess =  RecordType("GetRiskReportSuccess", [
	Field("delayed_compliance", MapType(LEVEL_1_STATUTORY_NAME, VectorType(Level1Statutory))),
	Field("not_complied", MapType(LEVEL_1_STATUTORY_NAME, VectorType(Level1Statutory))),
	Field("not_opted", MapType(LEVEL_1_STATUTORY_NAME, VectorType(Level1Statutory)))
])

GetServiceProviderReportFiltersSuccess =  RecordType("GetServiceProviderReportFiltersSuccess", [
	Field("countries", VectorType(Country)),
	Field("domains", VectorType(Domain)),
	Field("level_1_statutories", MapType(COUNTRY_ID, DomainStatutoryMap)),
	Field("units", VectorType(Unit)),
	Field("service_providers", VectorType(ServiceProvider))
])

# Service Provider Compliance

ComplianceForUnit = RecordType("ComplianceForUnit", [
	Field("compliance_name", Text100),
	Field("description", Text500),
	Field("statutory_dates", VectorType(StatutoryDates)),
	Field("due_date", Text20),
	Field("validity_date", Text20)
])

UnitWiseCompliance = RecordType("UnitWiseCompliance", [
	Field("unit_name", Text100),
	Field("address", ADDRESS),
	Field("compliances", VectorType(ComplianceForUnit))
])

ServiceProviderCompliance = RecordType("ServiceProviderCompliance", [
	Field("service_provider_name", Text50),
	Field("address", ADDRESS),
	Field("contract_from", Text20),
	Field("contract_to", Text20),
	Field("contact_person", Text50),
	Field("contact_no", CONTACT_NUMBER),
	Field("unit_wise_compliance", VectorType(ComplianceUnit))
])

GetServiceProviderWiseComplianceSuccess =  RecordType(
	"GetServiceProviderWiseComplianceSuccess", 
	[
		Field("compliance_list", VectorType(ServiceProviderCompliance))
	]
)

GetClientReportFiltersSuccess =  RecordType("GetClientReportFiltersSuccess", [
	Field("countries", VectorType(Country)),
	Field("domains", VectorType(Domain)),
	Field("business_groups", VectorType(BusinessGroup)),
	Field("legal_entities", VectorType(LegalEntity)),
	Field("divisions", VectorType(Division)),
	Field("units", VectorType(Unit)),
	Field("users", VectorType(User))
])

# Assignee compliance report

ComplianceUnit= RecordType("ComplianceUnit", [
	Field("compliance_name", Text100),
	Field("unit_address", Text500),
	Field("compliance_frequency", COMPLIANCE_FREQUENCY),
	Field("description", Text500),
	Field("statutory_dates", VectorType(StatutoryDates)),
	Field("due_date", Text20),
	Field("validity_date", Text20)
])

UserWiseCompliance = RecordType("UserWiseCompliance", [
	Field("assignee", Text100),
	Field("concurrence_person", Text100),
	Field("approval_person", Text100),
	Field("compliances", VectorType(ComplianceUnit))
])

AssigneeCompliance = RecordType("AssigneeCompliance", [
	Field("business_group_name", Text100),
	Field("legal_entity_name", Text100),
	Field("division_name", Text100),
	Field("user_wise_compliance", VectorType(UserWiseCompliance))
])

GetAssigneewisecomplianceReportSuccess =  RecordType("GetAssigneewisecomplianceReportSuccess", [
	Field("compliance_list", VectorType(AssigneeCompliance))
])

UnitCompliance = RecordType("UnitCompliance", [
	Field("business_group_name", Text50),
	Field("legal_entity_name", Text50),
	Field("division_name", Text50),
	Field("unit_wise_compliances", MapType(UNIT_NAME, VectorType(ComplianceUnit)))
])

GetUnitwisecomplianceReportSuccess =  RecordType("GetUnitwisecomplianceReportSuccess", [
	Field("compliance_list", VectorType(UnitCompliance))
])

UnitName = RecordType("UnitName", [
	Field("unit_name", Text100),
	Field("address", ADDRESS)
])

UserName= RecordType("UserName", [
	Field("user_id", USER_ID),
	Field("user_name", Text100)
])

GetReassignComplianceTaskReportFiltersSuccess =  RecordType("GetReassignComplianceTaskReportFiltersSuccess", [
	Field("countries", VectorType(Country)),
	Field("doamins", VectorType(Domain)),
	Field("level_1_statutories", MapType(COUNTRY_ID, DomainStatutoryMap)),
	Field("units", VectorType(UnitName)),
	Field("compliances", VectorType(ComplianceName)),
	Field("users", VectorType(UserName))
])

ReassignHistory = RecordType("ReassignHistory", [
	Field("reassigned_from", Text100),
	Field("reassigned_to", Text100),
	Field("reassigned_date", Text20),
	Field("reassign_reason", Text500)
])

ReassignCompliance = RecordType("ReassignCompliance", [
	Field("unit_name", Text100),
	Field("compliance_name", Text100),
	Field("due_date", Text20),
	Field("assignee", Text100),
	Field("reassign_history", VectorType(ReassignHistory))
])

GetReassignComplianceTaskDetailsSuccess =  RecordType("GetReassignComplianceTaskDetailsSuccess", [
	Field("compliance_list", VectorType(ReassignCompliance))
])

GetTaskApplicabilityStatusFiltersSuccess =  RecordType("GetTaskApplicabilityStatusFiltersSuccess", [
	Field("countries", VectorType(Country)),
	Field("domains", VectorType(Domain)),
	Field("business_groups", VectorType(BusinessGroup)),
	Field("legal_entities", VectorType(LegalEntity)),
	Field("divisions", VectorType(Division)),
	Field("units", VectorType(UnitName)),
	Field("level_1_statutories", MapType(COUNTRY_ID, DomainStatutoryMap))
])

ComplianceList = RecordType("ComplianceList", [
	Field("statutory_provision", Text100),
	Field("compliance_name", Text100),
	Field("description", Text500),
	Field("penal_consequences"  , Text500),
	Field("compliance_frequency", COMPLIANCE_FREQUENCY),
	Field("repeats"  , Text500)
])

ApplicabilityCompliance = RecordType("ApplicabilityCompliance", [
	Field("unit_name", Text100),
	Field("address", ADDRESS),
	Field("compliances", VectorType(ComplianceList))
])

GetComplianceTaskApplicabilityStatusReportSuccess =  RecordType("GetComplianceTaskApplicabilityStatusReportSuccess", [
	Field("applicable", MapType(LEVEL_1_STATUTORY_NAME, VectorType(ApplicabilityCompliance))),
	Field("not_applicable", MapType(LEVEL_1_STATUTORY_NAME, VectorType(ApplicabilityCompliance))),
	Field("not_opted", MapType(LEVEL_1_STATUTORY_NAME, VectorType(ApplicabilityCompliance)))
])

GetComplianceActivityReportFiltersSuccess =  RecordType("GetComplianceActivityReportFiltersSuccess", [
	Field("users", VectorType(UserName)),
	Field("domains", VectorType(Domain)),
	Field("level_1_statutories", MapType(COUNTRY_ID, DomainStatutoryMap)),
	Field("units", VectorType(UnitName)),
	Field("compliances", VectorType(ComplianceName))
])

ActivityCompliance = RecordType("ActivityCompliance", [
	Field("compliance_name", Text100),
	Field("activity_date", Text20),
	Field("activity_status", COMPLIANCE_ACTIVITY_STATUS),
	Field("compliance_status", COMPLIANCE_STATUS),
	Field("remarks", Text500)
])

DomainWiseCompliance = RecordType("DomainWiseCompliance", [
	Field("domain_name", Text50),
	Field("statutory_wise_compliances", MapType(LEVEL_1_STATUTORY_NAME, VectorType(ActivityCompliance)))
])

Activities = RecordType("Activities", [
	Field("unit_name", Text100),
	Field("address", ADDRESS),
	Field("domain_wise_compliances", VectorType(DomainWiseCompliance))
])

GetComplianceActivityReportSuccess =  RecordType("GetComplianceActivityReportSuccess", [
	Field("activities", VectorType(Activities))
])

GetReassignedHistoryReportFiltersSuccess =  RecordType("GetReassignedHistoryReportFiltersSuccess", [
	Field("countries", VectorType(Country)),
	Field("domains", VectorType(Domain)),
	Field("units", VectorType(UnitName)),
	Field("level_1_statutories", MapType(COUNTRY_ID, VectorType(DomainStatutoryMap))),
	Field("compliances", VectorType(Compliance)),
	Field("users", VectorType(UserName))
])

# Reassigned History

StatutoryReassignCompliance = RecordType("StatutoryReassignCompliance", [
	Field("level_1_statutory_id", LEVEL_1_STATUTORY_ID),
	Field("level_1_statutory_name", LEVEL_1_STATUTORY_NAME),
	Field("compliance", VectorType(ReassignCompliance))
])

GetReassignedHistoryReportSuccess =  RecordType("GetReassignedHistoryReportSuccess", [
	Field("statutory_wise_compliances", VectorType(StatutoryReassignCompliance))
])


#Statutory Notification List

GetStatutoryNotificationsListFiltersSuccess = RecordType("GetStatutoryNotificationsListFiltersSuccess", [
	Field("countries", VectorType(Country)),
	Field("domains", VectorType(Domain)),
	Field("business_groups", VectorType(BusinessGroup)),
	Field("legal_entities", VectorType(LegalEntity)),
	Field("divisions", VectorType(Division)),
	Field("units", VectorType(Unit)),
	Field("level1_statutories", MapType(COUNTRY_ID, DomainStatutoryMap))
])

NOTIFICATIONS = RecordType("NOTIFICATIONS", [
	Field("statutory_provision", STATUTORY_PROVISION),
	Field("notification_text", NOTIFICATION_TEXT),
	Field("date_and_time", TIMESTAMP)
])

COUNTRY_WISE_NOTIFICATIONS = RecordType("COUNTRY_WISE_NOTIFICATIONS", [
	Field("country_id", CountryList),
	Field("domain_id", DomainList),
	Field("notifications", VectorType(NOTIFICATIONS))
])

GetStatutoryNotificationsListReportSuccess = RecordType("GetStatutoryNotificationsListReportSuccess", [
	Field("countries", VectorType(Country)),
	Field("domains", VectorType(Domain)),
	Field("business_groups", VectorType(BusinessGroup)),
	Field("legal_entities", VectorType(LegalEntity)),
	Field("divisions", VectorType(Division)),
	Field("units", VectorType(Unit)),	Field("level_1_statutories", MapType(COUNTRY_ID, Statutory)),
	Field("country_wise_notifications", VectorType(COUNTRY_WISE_NOTIFICATIONS))
])

#Activity Log

FormName = RecordType("FormName", [
	Field("form_id", FORM_ID),
	Field("form_name", FORM_NAME)
])

GetActivityLogFiltersSuccess =  RecordType("GetActivityLogFiltersSuccess", [
	Field("users", VectorType(UserName)),
	Field("forms", VectorType(FormName))
])

ActivityLog = RecordType("ActivityLog", [
	Field("user_name", Text100),
	Field("date_and_time", Text20),
	Field("form_name", Text50),
	Field("action", Text500)	
])

GetActivityLogReportSuccess =  RecordType("GetActivityLogReportSuccess", [
	Field("activity_log", VectorType(ActivityLog))
])

LoginTrace = RecordType("LoginTrace", [
	Field("date_and_time", Text20),
	Field("action", Text100)
])

GetLoginTraceSuccess =  RecordType("GetLoginTraceSuccess", [
	Field("users", VectorType(UserName)),
	Field("login_trace", VectorType(LoginTrace))
])

Response = VariantType("Response", [

	GetComplianceDetailsReportFiltersSuccess,
	GetComplianceDetailsReportSuccess,
	GetRiskReportFiltersSuccess,
	GetRiskReportSuccess,
	GetServiceProviderReportFiltersSuccess,
	GetServiceProviderWiseComplianceSuccess,
	GetClientReportFiltersSuccess,
	GetAssigneewisecomplianceReportSuccess,
	GetUnitwisecomplianceReportSuccess,
	GetReassignComplianceTaskReportFiltersSuccess,
	GetReassignComplianceTaskDetailsSuccess,
	GetTaskApplicabilityStatusFiltersSuccess,
	GetComplianceTaskApplicabilityStatusReportSuccess,
	GetComplianceActivityReportFiltersSuccess,
	GetComplianceActivityReportSuccess,
	GetReassignedHistoryReportFiltersSuccess,
	GetReassignedHistoryReportSuccess,
	GetStatutoryNotificationsListFiltersSuccess,
	GetStatutoryNotificationsListReportSuccess,
	GetActivityLogFiltersSuccess,
	GetActivityLogReportSuccess,
	GetLoginTraceSuccess
])