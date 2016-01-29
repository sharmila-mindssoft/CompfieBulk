from basics.types import VectorType, RecordType, VariantType, MapType, Field
from common import (Text, Text20, Text50, Text100, Text500, Int8,
	COUNTRY_ID, DOMAIN_ID, DATE, FILTER_ID, FILTER_NAME, USER_ID, ADDRESS, LEVEL_1_STATUTORY_NAME,
	BUSINESS_GROUP_ID, LEGAL_ENTITY_ID, DIVISION_ID, UNIT_ID, SESSION_TOKEN)
from core import (
	FILTER_TYPE, COMPLIANCE_STATUS,
	APPLICABILITY_STATUS,
	ChartFilters,
	Country, Domain,
	BusinessGroup, LegalEntity,
	Division, Unit,
	Compliance
)

__all__ = [
	"Request", "Response", "RequestFormat", "ApplicableDrillDown", "DataMap", "ChartDataMap",
	"EscalationData", "CompliedMap", "TrendData", "RessignedCompliance",
	"DelayedCompliance", "DomainWise", "AssigneeWiseDetails", "AssigneeChartData",
	"Level1Compliance", "UnitCompliance", "DrillDownData",
]

#
# Request
#

GetChartFilters = RecordType("GetChartFilters", [])

GetComplianceStatusChart = RecordType("GetComplianceStatusChart", [
	Field("country_ids", VectorType(COUNTRY_ID)),
	Field("domain_ids", VectorType(DOMAIN_ID)),
	Field("from_date", Text),
	Field("to_date", Text),
	Field("filter_type", Text),
	Field("filter_ids",VectorType(Int8))
])

GetComplianceStatusDrillDownData = RecordType("GetComplianceStatusDrillDownData", [
	Field("domain_ids", VectorType(DOMAIN_ID)),
	Field("from_date", Text),
	Field("to_date", Text),
	Field("year", Text),
	Field("filter_type", FILTER_TYPE),
	Field("filter_id", Int8),
	Field("compliance_status", COMPLIANCE_STATUS)
])


GetEscalationsChart = RecordType("GetEscalationsChart", [
	Field("country_ids", VectorType(COUNTRY_ID)),
    Field("domain_ids", VectorType(DOMAIN_ID)),
    Field("filter_type", FILTER_TYPE),
    Field("filter_ids",  VectorType(Int8))
])

GetNotCompliedChart = RecordType("GetNotCompliedChart", [
	Field("country_ids", VectorType(COUNTRY_ID)),
    Field("domain_ids", VectorType(DOMAIN_ID)),
    Field("filter_type", FILTER_TYPE),
    Field("filter_ids", VectorType((Int8))
])

GetTrendChart = RecordType("GetTrendChart", [
	Field("country_id", COUNTRY_ID),
    Field("domain_id", DOMAIN_ID),
    Field("from_date", DATE),
    Field("to_date", DATE),
    Field("filter_type", FILTER_TYPE),
    Field("filter_id", Int8)
])

GetComplianceApplicabilityStatusChart = RecordType("GetComplianceApplicabilityStatusChart", [
	Field("country_id", COUNTRY_ID),
    Field("domain_id", DOMAIN_ID),
    Field("from_date", DATE),
    Field("to_date", DATE),
    Field("filter_type", FILTER_TYPE),
    Field("filter_id", Int8)
])

GetAssigneeWiseCompliancesChart = RecordType("GetAssigneeWiseCompliancesChart", [
	Field("country_id", COUNTRY_ID),
	Field("business_group_id", BUSINESS_GROUP_ID),
	Field("legal_entity_id", LEGAL_ENTITY_ID),
	Field("division_id", DIVISION_ID),
	Field("unit_id", UNIT_ID)
])

GetAssigneeWiseComplianceDrillDown = RecordType("GetAssigneeWiseComplianceDrillDown", [
	Field("assignee_id", USER_ID),
	Field("domain_id", DOMAIN_ID)
])


GetEscalationsDrillDownData = RecordType("GetEscalationsDrillDownData", [
	Field("domain_ids", VectorType(DOMAIN_ID)),
	Field("filter_type", FILTER_TYPE),
	Field("filter_ids", VectorType(FILTER_ID)),
	Field("year", Int8)
])

GetComplianceApplicabilityStatusDrillDown = RecordType("GetComplianceApplicabilityStatusDrillDown", [
	Field("filter_type", FILTER_TYPE),
	Field("filter_id", FILTER_ID),
	Field("applicability_status", APPLICABILITY_STATUS)
])

GetNotCompliedDrillDown = RecordType("GetNotCompliedDrillDown", [
	Field("filter_type", FILTER_TYPE),
	Field("filter_id", FILTER_ID)
])

GetTrendChartDrillDownData = RecordType("GetTrendChartDrillDownData", [
	Field("filter_type", FILTER_TYPE),
	Field("filter_id", FILTER_ID)
])


Request = VariantType("Request", [
	GetChartFilters,
	GetComplianceStatusChart,
	GetEscalationsChart,
	GetNotCompliedChart,
	GetTrendChart,
	GetComplianceApplicabilityStatusChart,
	GetAssigneeWiseCompliancesChart,
	GetAssigneeWiseComplianceDrillDown,
	GetComplianceStatusDrillDownData,
	GetEscalationsDrillDownData,
	GetComplianceApplicabilityStatusDrillDown,
	GetNotCompliedDrillDown,
	GetTrendChartDrillDownData,
])

RequestFormat = RecordType("RequestFormat", [
	Field("session_token", SESSION_TOKEN),
	Field("request", Request)
])


#
# Response
#

GetChartFiltersSuccess = RecordType("GetChartFiltersSuccess", [
	Field("countries", VectorType(Country)),
	Field("domains", VectorType(Domain)),
	Field("business_groups", VectorType(BusinessGroup)),
	Field("legal_entities", VectorType(LegalEntity)),
	Field("divisions", VectorType(Division)),
	Field("units", VectorType(Unit))
])

# Compliance Status
DataMap = RecordType("DataMap", [
	Field("filter_name", FILTER_NAME),
	Field("no_of_compliances", Int8)
])

ChartDataMap = RecordType("ChartDataMap", [
	Field("year", Text20),
	Field("data", VectorType(DataMap))
])

GetComplianceStatusChartSuccess = RecordType("GetComplianceStatusChartSuccess", [
	Field("chart_data", VectorType(ChartDataMap))
])

# Escalation Chart

EscalationData = RecordType("EscalationData", [
	Field("year", Text20),
	Field("delayed_compliance_count", Int8),
	Field("not_complied_count", Int8)
])

GetEscalationsChartSuccess = RecordType("GetEscalationsChartSuccess", [
	Field("chart_data", VectorType(EscalationData))
])

# Not Complied Chart
GetNotCompliedChartSuccess = RecordType("GetNotCompliedChartSuccess", [
	Field("T_0_to_30_days_count", Int8),
	Field("T_31_to_60_days_count", Int8),
	Field("T_61_to_90_days_count", Int8),
	Field("Above_90_days_count", Int8)
])

# Trend Chart

CompliedMap = RecordType("CompliedMap", [
	Field("total_compliances", Int8),
	Field("complied_compliances_count", Int8)
])

TrendData = RecordType("TrendData", [
	Field("filter_name", FILTER_NAME),
	Field("complied_compliance", VectorType(CompliedMap))
])

GetTrendChartSuccess = RecordType("GetTrendChartSuccess", [
	Field("years", VectorType(Int8)),
	Field("data", VectorType(TrendData))
])

# Compliance Applicability

GetComplianceApplicabilityStatusChartSuccess = RecordType("GetComplianceApplicabilityStatusChartSuccess", [
	Field("applicable_count", Int8),
	Field("not_applicable_count", Int8),
	Field("not_opted_count", Int8)
])

# Assignee Wise Compliance Chart

RessignedCompliance = RecordType("RessignedCompliance", [
	Field("compliance_name", Text50),
	Field("reassigned_from", Text50),
	Field("start_date", Text20),
	Field("due_date", Text20),
	Field("reassigned_date", Text20),
	Field("completed_date", Text20)
])

DelayedCompliance = RecordType("DelayedCompliance", [
	Field("assigned_count", Int8),
	Field("reassigned_count", Int8),
	Field("reassigned_compliances", VectorType(RessignedCompliance))
])

DomainWise = RecordType("DomainWise", [
	Field("domain_id", DOMAIN_ID),
	Field("domain_name", Text50),
	Field("total_compliances", Int8),
	Field("complied_count", Int8),
	Field("delayed_compliance", DelayedCompliance),
	Field("inprogress_compliance_count", Int8),
	Field("not_complied_count", Int8)
])

AssigneeWiseDetails = RecordType("AssigneeWiseDetails", [
	Field("user_id", USER_ID),
	Field("assignee_name", Text100),
	Field("domain_wise_details", VectorType(DomainWise))
])

AssigneeChartData = RecordType("AssigneeChartData", [
	Field("unit_name", Text50),
	Field("assignee_wise_details", VectorType(AssigneeWiseDetails))
])

GetAssigneeWiseCompliancesChartSuccess = RecordType("GetAssigneeWiseCompliancesChartSuccess", [
	Field("chart_data", VectorType(AssigneeChartData))
])

# Assignee Wise Compliance Drill Down

Level1Compliance = RecordType("Level1Compliance", [
	Field("compliance_name", Text100),
	Field("description", Text500),
	Field("assignee_name", Text100),
	Field("assigne_date", Text20),
	Field("due_date", Text20),
	Field("completion_date", Text20),
	Field("compliance_status", COMPLIANCE_STATUS),
	Field("ageing", Int8)
])

UnitCompliance = RecordType("UnitCompliance", [
	Field("unit_name", Text100),
	Field("address", ADDRESS),
	Field("compliances", MapType(LEVEL_1_STATUTORY_NAME, VectorType(Level1Compliance)))
])

GetAssigneeWiseComplianceDrillDownSuccess = RecordType("GetAssigneeWiseComplianceDrillDownSuccess", [
	Field("complied", VectorType(UnitCompliance)),
	Field("delayed", VectorType(UnitCompliance)),
	Field("inprogress", VectorType(UnitCompliance)),
	Field("not_complied", VectorType(UnitCompliance))
])

# Compliance Status Drill Down

DrillDownData = RecordType("DrillDownData", [
	Field("business_group", Text50),
	Field("legal_entity", Text50),
	Field("division", Text50),
	Field("unit_name", Text100),
	Field("address", ADDRESS),
	Field("compliances", MapType(LEVEL_1_STATUTORY_NAME, VectorType(Level1Compliance))),
	# Field("unit_wise_compliances", VectorType(UnitCompliance))
])

GetComplianceStatusDrillDownDataSuccess = RecordType("GetComplianceStatusDrillDownDataSuccess", [
	Field("drill_down_data", VectorType(DrillDownData))
])


# Escalation Drill Down

GetEscalationsDrillDownDataSuccess = RecordType("GetEscalationsDrillDownDataSuccess", [
	Field("delayed", VectorType(DrillDownData)),
	Field("not_complied", VectorType(DrillDownData))
])

# Applicability Status Drill Down

ApplicableDrillDown = RecordType("ApplicableDrillDown", [
	Field("level1_statutory_name", LEVEL_1_STATUTORY_NAME),
	Field("compliances", VectorType(Compliance)),
])

GetComplianceApplicabilityStatusDrillDownSuccess = RecordType(
	"GetComplianceApplicabilityStatusDrillDownSuccess",
	[
		Field("filter_name", FILTER_NAME),
		Field("drill_down_data", VectorType(ApplicableDrillDown))
	]
)

# Not complied drill down
GetNotCompliedDrillDownSuccess = RecordType(
	"GetNotCompliedDrillDownSuccess",
	[
		Field("filter_name", FILTER_NAME),
		Field("drill_down_data", VectorType(DrillDownData))
	]
)

GetTrendChartDrillDownDataSuccess = RecordType("GetTrendChartDrillDownDataSuccess", [
	Field("drill_down_data", VectorType(DrillDownData))
])



Response = VariantType("Response", [
	GetChartFiltersSuccess,
	GetComplianceStatusChartSuccess,
	GetEscalationsChartSuccess,
	GetNotCompliedChartSuccess,
	GetTrendChartSuccess,
	GetComplianceApplicabilityStatusChartSuccess,
	GetAssigneeWiseCompliancesChartSuccess,
	GetAssigneeWiseComplianceDrillDownSuccess,
	GetComplianceStatusDrillDownDataSuccess,
	GetEscalationsDrillDownDataSuccess,
	GetComplianceApplicabilityStatusDrillDownSuccess,
	GetNotCompliedDrillDownSuccess,
	GetTrendChartDrillDownDataSuccess
])
