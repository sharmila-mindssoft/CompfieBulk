from basics.types import VectorType, RecordType, VariantType, MapType, Field

from common import (GROUP_ID,
	Int8, Text20, Text50, Text500, Text100, Bool,
	USER_ID, COMPLIANCE_HISTORY_ID, DOMAIN_ID, DOMAIN_NAME, INDUSTRY_ID,
	INDUSTRY_NAME, COUNTRY_ID, COUNTRY_NAME, SESSION_TOKEN, INDUSTRY_NAME,
	BUSINESS_GROUP_ID, BUSINESS_GROUP_NAME, LEGAL_ENTITY_ID,
	LEGAL_ENTITY_NAME, DIVISION_ID, DIVISION_NAME,
	UNIT_ID, UNIT_NAME, COMPLIANCE_ID, SESSION_TOKEN)

from core import Compliance, COMPLIANCE_FREQUENCY

__all__=  [
	"Request", "Response", "RequestFormat", "ApproveComplianceList",
	"SaveCompliance", "ComplianceApplicability",
	"ComplianceHistory", "ReassignHistory", "EscalationData",
	"PastYearEscalation", "TrendData", "TrendChartData"
]

# 
# Request
#

GetVersions = RecordType("GetVersions", [
	Field("group_id", GROUP_ID),
	Field("unit_details_version", Int8),
	Field("user_details_version", Int8),
	Field("compliance_applicability_version", Int8),
	Field("compliance_history_version", Int8),
	Field("reassign_history_version",  Int8)
])

GetUsers = RecordType("GetUsers", [
	Field("user_id", USER_ID),
	Field("version", Int8)
])

GetUnitDetails = RecordType("GetUnitDetails", [
	Field("user_id", USER_ID),
	Field("version", Int8)
])

GetComplianceApplicabilityStatus = RecordType("GetComplianceApplicabilityStatus", [
	Field("user_id", USER_ID),
	Field("version", Int8)	
])

GetComplianceHistory = RecordType("GetComplianceHistory", [
	Field("user_id", USER_ID),
	Field("version", Int8)	
])

GetReassignedComplianceHistory = RecordType("GetReassignedComplianceHistory", [
	Field("user_id", USER_ID),
	Field("version", Int8)	
])

GetPastFourYearEscalations = RecordType("GetPastFourYearEscalations", [
	Field("user_id", USER_ID)
])


CheckDiskSpace = RecordType("CheckDiskSpace", [])

SaveCompliance = RecordType("SaveCompliance", [
	Field("compliance_history_id", COMPLIANCE_HISTORY_ID),
	Field("user_id", USER_ID),
	Field("documents", VectorType(Text50)), 
	Field("completion_date", Text20),
	Field("validity_date", Text20),
	Field("next_due_date", Text20),
	Field("remarks", Text500)
])

SaveComplianceDetails = RecordType("SaveComplianceDetails", [
	Field("save_compliance", SaveCompliance)
])

ApproveComplianceList = RecordType("ApproveComplianceList", [
	Field("compliance_history_id" , COMPLIANCE_HISTORY_ID),
	Field("approval_status" , Bool),
	Field("concurrence_status" , Bool),
	Field("approved_on" , Text20),
	Field("concurred_on" , Text20),
	Field("remarks" , Text500)
])

ApproveCompliance = RecordType("ApproveCompliance", [
	Field("approve_compliance", ApproveComplianceList)
])

GetTrendChartData = RecordType("GetTrendChartData", [
	Field("user_id", USER_ID)
])

Request = VariantType("Request", [
	GetVersions,
	GetUsers,
	GetUnitDetails,
	GetComplianceApplicabilityStatus,
	GetComplianceHistory,
	GetReassignedComplianceHistory,
	GetPastFourYearEscalations,
	CheckDiskSpace,
	SaveComplianceDetails,
	ApproveCompliance,
	GetTrendChartData
])

RequestFormat = RecordType("RequestFormat", [
	Field("session_token", SESSION_TOKEN),
	Field("request", Request)
])

#
# Response
#

GetVersionsSuccess = RecordType("GetVersionsSuccess", [
	Field("unit_details_version", Int8),
	Field("user_details_version", Int8),
	Field("compliance_applicability_version", Int8),
	Field("compliance_history_version", Int8),
	Field("reassign_history_version", Int8)
])

GetUsersSuccess = RecordType("GetUsersSuccess", [
	Field("user_id", USER_ID),
	Field("user_name", Text100)
])

GetUnitDetailsSuccess = RecordType("GetUnitDetailsSuccess", [
	Field("unit_id",  UNIT_ID),
	Field("unit_name",  Text20),
	Field("country_id",  COUNTRY_ID),
	Field("country_name",  COUNTRY_NAME),
	Field("domain_id",  DOMAIN_ID),
	Field("domain_name",  DOMAIN_NAME),
	Field("industry_id",  INDUSTRY_ID),
	Field("industry_name",  INDUSTRY_NAME),
	Field("group_id",  GROUP_ID),
	Field("business_group_id", BUSINESS_GROUP_ID),
	Field("business_group_name", BUSINESS_GROUP_NAME),
	Field("legal_entity_id",  LEGAL_ENTITY_ID),
	Field("legal_entity_name",  LEGAL_ENTITY_NAME),
	Field("division_id",  DIVISION_ID),
	Field("division_name",  DIVISION_NAME),
])

ComplianceApplicability = RecordType("ComplianceApplicability", [
	Field("country_id",  COUNTRY_ID),
	Field("domain_id",  DOMAIN_ID),
	Field("unit_id",  UNIT_ID),
	Field("compliance_id",  COMPLIANCE_ID),
	Field("compliance_name",  Text100),
	Field("compliance_frequency",  COMPLIANCE_FREQUENCY),
	Field("compliance_applicable",  Bool),
	Field("compliance_opted",  Bool)
])

GetComplianceApplicabilityStatusSuccess = RecordType("GetComplianceApplicabilityStatusSuccess", [
	Field("applicabilty_list", VectorType(ComplianceApplicability))
])

ComplianceHistory = RecordType("ComplianceHistory", [
	Field("compliance_history_id", COMPLIANCE_HISTORY_ID),
	Field("unit_id", UNIT_ID),
	Field("compliance_id", COMPLIANCE_ID),
	Field("start_date", Text20),
	Field("due_date", Text20),
	Field("completion_date", Text20),
	Field("documents", VectorType(Text20)),
	Field("validity_date", Text20),
	Field("next_due_date", Text20),
	Field("remarks", Text500),
	Field("completed_by", USER_ID),
	Field("completed_on", Text20),
	Field("concurrence_status", Bool),
	Field("concurred_by", USER_ID),
	Field("concurred_on", Text20),
	Field("approval_status", Bool),
	Field("approved_by", USER_ID),
	Field("approved_on", Text20)
])

GetComplianceHistorySuccess = RecordType("GetComplianceHistorySuccess", [
	Field("compliance_history", VectorType(ComplianceHistory) )
])

ReassignHistory = RecordType("ReassignHistory", [
	Field("unit_id" , UNIT_ID),
	Field("compliance_history_id" , COMPLIANCE_HISTORY_ID),
	Field("assignee" , USER_ID),
	Field("reassigned_from" , USER_ID),
	Field("reassigned_date" , Text20),
	Field("remarks" , Text500)
])

GetReassignedComplianceHistorySuccess = RecordType("GetReassignedComplianceHistorySuccess", [
	Field("Reassign_history", ReassignHistory)
])

CheckDiskSpaceSuccess = RecordType("CheckDiskSpaceSuccess", [
	Field("total_disk_space", Int8),
	Field("available_disk_space", Int8)
])

SaveComplianceDetailsSuccess = RecordType("SaveComplianceDetailsSuccess", [])

NotEnoughDiskSpaceAvailable = RecordType("NotEnoughDiskSpaceAvailable", [])

ApproveComplianceSuccess = RecordType("ApproveComplianceSuccess", [])

EscalationData = RecordType("EscalationData", [
	Field("year", Int8),
	Field("delayed_compliance_count", Int8),
	Field("not_complied_count", Int8)
])

PastYearEscalation = RecordType("PastYearEscalation", [
	Field("unit_id" , UNIT_ID),
	Field("unit_name" , UNIT_NAME),
	Field("data", VectorType(EscalationData))
])

GetPastFourYearEscalationsSuccess = RecordType("GetPastFourYearEscalationsSuccess", [
	Field("past_year_escalation", VectorType(PastYearEscalation))
])

TrendData = RecordType("TrendData", [
	Field("year", Int8),
	Field("total_compliances", Int8),
	Field("complied_compliances_count", Int8)	
])
TrendChartData = RecordType("TrendChartData", [
	Field("unit_id", UNIT_ID),
	Field("unit_name", UNIT_NAME),
	Field("data", VectorType(TrendData))
])

GetTrendChartDataSuccess = RecordType("GetTrendChartDataSuccess", [
	Field("trend_chart_data", VectorType(TrendChartData))
])

Response = VariantType("Response", [
	GetVersionsSuccess,
	GetUsersSuccess,
	GetUnitDetailsSuccess,
	GetComplianceApplicabilityStatusSuccess,
	GetComplianceHistorySuccess,
	GetReassignedComplianceHistorySuccess,
	CheckDiskSpaceSuccess,
	SaveComplianceDetailsSuccess,
	NotEnoughDiskSpaceAvailable,
	ApproveComplianceSuccess,
	GetPastFourYearEscalationsSuccess,
	GetTrendChartDataSuccess,
])
