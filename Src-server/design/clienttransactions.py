from basics.types import (RecordType, VectorType, Field, VariantType, MapType)
from common import (UNIT_ID, DOMAIN_ID, USER_ID, DATE, COMPLIANCE_HISTORY_ID, DESCRIPTION, LEVEL_1_STATUTORY_ID,
	COMPLIANCE_ID, DOCUMENT_NAME, UNIT_NAME, ADDRESS, COUNTRY_NAME, DOMAIN_NAME, BUSINESS_GROUP_NAME,
	LEGAL_ENTITY_NAME, DIVISION_NAME, COMPLIANCE_TASK_NAME, DIVISION_ID, LEGAL_ENTITY_ID, BUSINESS_GROUP_ID,
	GROUP_ID, LEVEL_1_STATUTORY_NAME, EMPLOYEE_NAME, USER_LEVEL, NO_OF_COMPLIANCES, AGEING, FORMAT_FILE_NAME,
	INDUSTRY_NAME, SESSION_TOKEN )
from core import (
	COMPLIANCE_APPROVAL_STATUS, COMPLIANCE_FREQUENCY,
	AssignedStatutory, Country, 
	StatutoryDate, BusinessGroup, LegalEntity,
	Division, Domain, Unit, Statutory
)
__all__=  [
	"Request", "Response", "RequestFormat", "ASSINGED_COMPLIANCE", "REASSIGNED_COMPLIANCE",
	"PAST_RECORD_COMPLIANCE", "UNIT_WISE_STATUTORIES", 
	"UNIT_WISE_COMPLIANCE","ASSIGNCOMPLIANCEUSERS","STATUTORYWISECOMPLIANCE",
	"USERWISESTATUTORIES","USERWISEUNITS","USERWISECOMPLIANCE","APPROVALCOMPLIANCE",
	"APPORVALCOMPLIANCELIST", "STATUTORY_WISE_COMPLIANCES",
	"UnitStatutoryCompliances"
]

AssignedStatutoryList = VectorType(AssignedStatutory)
UnitIdList = VectorType(UNIT_ID)
CountryList = VectorType(Country)
StatutoryDateList = VectorType(StatutoryDate)
BusinessGroupList = VectorType(BusinessGroup)
LegalEntityList = VectorType(LegalEntity)
DivisionList = VectorType(Division)
UnitList = VectorType(Unit)
DomainList = VectorType(Domain)
StatutoryList = VectorType(Statutory)

#	
#	Request
#

### Statutory Settings

GetStatutorySettings = RecordType("GetStatutorySettings", [
])

UpdateStatutorySettings = RecordType("UpdateStatutorySettings", [
	Field("unit_id", UNIT_ID),
	Field("statutories", MapType(DOMAIN_ID, AssignedStatutoryList))
])

### Assign Compliance

GetAssignCompliancesFormData = RecordType("GetAssignCompliancesFormData", [
])

GetComplianceForUnits = RecordType("GetComplianceForUnits", [
	Field("unit_ids", VectorType(UNIT_ID))
])

ASSINGED_COMPLIANCE =  RecordType("ASSINGED_COMPLIANCE", [
	Field("compliance_id" ,USER_ID),
	Field("statutory_dates", StatutoryDateList),
	Field("due_date", DATE),
	Field("validity_date", DATE),
	Field("unit_ids", UnitIdList)
])


SaveAssignedCompliance = RecordType("SaveAssignedCompliance", [
	Field("assignee" ,USER_ID),
	Field("concurrence_person", USER_ID),
	Field("approval_person", USER_ID),
	Field("compliances", VectorType(ASSINGED_COMPLIANCE))
])

### Reassign Compliance

GetUserwiseCompliances = RecordType("GetUserwiseCompliances", [
])

REASSIGNED_COMPLIANCE = RecordType("REASSIGNED_COMPLIANCE", [
	Field("compliance_history_id",COMPLIANCE_HISTORY_ID),
	Field("due_date", DATE)
])

ReassignCompliance = RecordType("ReassignCompliance", [
	Field("reassigned_from", USER_ID),
	Field("assignee", USER_ID),
	Field("concurrence_person", USER_ID),
	Field("approval_person", USER_ID),
	Field("compliances", VectorType(REASSIGNED_COMPLIANCE)),
	Field("reassigned_reason", DESCRIPTION)
])

### Approve Compliance

GetComplianceApprovalList = RecordType("GetComplianceApprovalList", [
])

ApproveCompliance = RecordType("ApproveCompliance", [
	Field("compliance_history_id", COMPLIANCE_HISTORY_ID),
	Field("approval_status", COMPLIANCE_APPROVAL_STATUS),
	Field("remarks", DESCRIPTION)
])

### Past Records

GetPastRecordsFormData = RecordType("GetPastRecordsFormData", [
])

GetStatutoriesByUnit = RecordType("GetStatutoriesByUnit", [
	Field("unit_id", UNIT_ID),
	Field("domain_id", DOMAIN_ID),
	Field("level_1_statutory_id", LEVEL_1_STATUTORY_ID),
	Field("compliance_frequency", COMPLIANCE_FREQUENCY)
])

PAST_RECORD_COMPLIANCE =  RecordType("PAST_RECORD_COMPLIANCE", [
	Field("compliance_id", COMPLIANCE_ID),
	Field("due_date" , DATE),
	Field("completion_date", DATE),
	Field("validity_date", DATE),
	Field("documents", VectorType(DOCUMENT_NAME))
])

SavePastRecords = RecordType("SavePastRecords", [
	Field("compliances", VectorType(PAST_RECORD_COMPLIANCE))
])

Request = VariantType("Request", [
	GetStatutorySettings,
	UpdateStatutorySettings,
	GetAssignCompliancesFormData,
	GetComplianceForUnits,
	SaveAssignedCompliance,
	GetUserwiseCompliances,
	ReassignCompliance,
	GetComplianceApprovalList,
	ApproveCompliance,
	GetPastRecordsFormData,
	GetStatutoriesByUnit,
	SavePastRecords
])

RequestFormat = RecordType("RequestFormat", [
	Field("session_token", SESSION_TOKEN),
	Field("request", Request)
])


#
#	Response
#

### Statutory Settings

UnitStatutoryCompliances = RecordType("UnitStatutoryCompliances", [
	Field("unit_id", UNIT_ID),
	Field("unit_name", UNIT_NAME),
	Field("address", ADDRESS),
	Field("country_name", COUNTRY_NAME),
	Field("domain_names", VectorType(DOMAIN_NAME))
	Field("business_group_name", BUSINESS_GROUP_NAME),
	Field("legal_entity_name", LEGAL_ENTITY_NAME),
	Field("division_name", DIVISION_NAME),
	Field("statutories", MapType(DOMAIN_ID, AssignedStatutoryList))
])

GetStatutorySettingsSuccess = RecordType("GetStatutorySettingsSuccess", [
	Field("statutories", VectorType(UnitStatutoryCompliances))
])

UpdateStatutorySettingsSuccess = RecordType("UpdateStatutorySettingsSuccess", [
])

InvalidPassword = RecordType("InvalidPassword", [
])

### Assign Compliance


# UNIT_WISE_STATUTORIES_LIST = VectorType(UNIT_WISE_STATUTORIES)

# UNIT_WISE_COMPLIANCE = RecordType("UNIT_WISE_COMPLIANCE", [
# 	Field("unit_id", UNIT_ID),
# 	Field("unit_name", UNIT_NAME),
# 	Field("address", ADDRESS),
# 	Field("division_id", DIVISION_ID),
# 	Field("legal_entity_id", LEGAL_ENTITY_ID),
# 	Field("business_group_id", BUSINESS_GROUP_ID),
# 	Field("group_id", GROUP_ID),
# 	Field("statutories", MapType(LEVEL_1_STATUTORY_NAME, UNIT_WISE_STATUTORIES_LIST))
])

ASSIGNCOMPLIANCEUSERS =  RecordType("ASSIGNCOMPLIANCEUSERS", [
	Field("user_id", USER_ID),
	Field("user_name", EMPLOYEE_NAME),
	Field("user_level", USER_LEVEL),
	Field("seating_unit_id", UNIT_ID),
	Field("unit_ids", UnitIdList),
	Field("domain_ids", VectorType(DOMAIN_ID))
])

GetAssignCompliancesFormDataSuccess = RecordType("GetAssignCompliancesFormDataSuccess", [
	Field("countries", CountryList),
	Field("business_groups", BusinessGroupList),
	Field("legal_entities", LegalEntityList),
	Field("divisions", DivisionList),
	Field("units", UnitList),
	Field("users", MapType(UNIT_ID, VectorType(ASSIGNCOMPLIANCEUSERS)))
])

UNIT_WISE_STATUTORIES = RecordType("UNIT_WISE_STATUTORIES", [
	Field("compliance_id", COMPLIANCE_ID),
	Field("compliance_name", COMPLIANCE_TASK_NAME),
	Field("description", DESCRIPTION),
	Field("frequency", COMPLIANCE_FREQUENCY),
	Field("statutory_date", StatutoryDateList),
	Field("due_date", DATE),
	Field("applicable_units", VectorType(UNIT_ID))
])

GetComplianceForUnitsSuccess = RecordType("GetComplianceForUnitsSuccess", [
	Field("statutories", MapType(DOMAIN_ID, VectorType(UNIT_WISE_STATUTORIES)))
])

AssigneeNotBelongToUnit = RecordType("AssigneeNotBelongToUnit", [
])

ConcurrenceNotBelongToUnit = RecordType("ConcurrenceNotBelongToUnit", [
])

ApprovalPersonNotBelongToUnit = RecordType("ApprovalPersonNotBelongToUnit", [
])

SaveAssignedComplianceSuccess = RecordType("SaveAssignedComplianceSuccess", [
])

### Reassign Compliance

STATUTORYWISECOMPLIANCE = RecordType("STATUTORYWISECOMPLIANCE", [
	Field("compliance_history_id",COMPLIANCE_HISTORY_ID),
	Field("compliance_id", COMPLIANCE_ID),
	Field("compliance_name", COMPLIANCE_TASK_NAME),
	Field("description", DESCRIPTION),
	Field("compliance_frequency", COMPLIANCE_FREQUENCY),
	Field("statutory_date", StatutoryDateList),
	Field("due_date", DATE)
])

USERWISESTATUTORIES = RecordType("USERWISESTATUTORIES", [
	Field("level_1_statutory_name", LEVEL_1_STATUTORY_NAME),
	Field("compliances", VectorType(STATUTORYWISECOMPLIANCE))
])

USERWISEUNITS = RecordType("USERWISEUNITS", [
	Field("unit_id", UNIT_ID),
	Field("unit_name", UNIT_NAME) ,
	Field("address", ADDRESS),
	Field("statutories", VectorType(USERWISESTATUTORIES))
])

USERWISECOMPLIANCE = RecordType("USERWISECOMPLIANCE", [
	Field("user_id", USER_ID),
	Field("user_name", EMPLOYEE_NAME),
	Field("seating_unit", UNIT_NAME),
	Field("address", ADDRESS),
	Field("no_of_compliances", NO_OF_COMPLIANCES),
	Field("units", VectorType(USERWISEUNITS))
])

GetUserwiseCompliancesSuccess = RecordType("GetUserwiseCompliancesSuccess", [
	Field("user_wise_compliances", VectorType(USERWISECOMPLIANCE)),
	Field("users", VectorType(ASSIGNCOMPLIANCEUSERS))
])

ReassignComplianceSuccess = RecordType("ReassignComplianceSuccess", [
])

### Compliance Approval

APPROVALCOMPLIANCE =  RecordType("APPROVALCOMPLIANCE", [
	Field("compliance_history_id", COMPLIANCE_HISTORY_ID),
	Field("compliance_name", COMPLIANCE_TASK_NAME),
	Field("description", DESCRIPTION),
	Field("domain_name", DOCUMENT_NAME),
	Field("start_date", DATE),
	Field("due_date", DATE),
	Field("delayed_by", AGEING),
	Field("compliance_frequency", COMPLIANCE_FREQUENCY),
	Field("documents", VectorType(FORMAT_FILE_NAME)),
	Field("upload_date", DATE),
	Field("completion_date", DATE),
	Field("next_due_date", DATE),
	Field("concurrenced_by", EMPLOYEE_NAME),
	Field("remarks", DESCRIPTION)
])

APPORVALCOMPLIANCELIST =  RecordType("APPORVALCOMPLIANCELIST", [
	Field("assignee_id", USER_ID),
	Field("assignee_name", EMPLOYEE_NAME),
	Field("compliances", VectorType(APPROVALCOMPLIANCE))
])

GetComplianceApprovalListSuccess = RecordType("GetComplianceApprovalListSuccess", [
	Field("approval_list", VectorType(APPORVALCOMPLIANCELIST)),
])

ApproveComplianceSuccess = RecordType("ApproveComplianceSuccess", [
])

GetPastRecordsFormDataSuccess = RecordType("GetPastRecordsFormDataSuccess", [
	Field("countries", CountryList),
	Field("business_groups", BusinessGroupList),
	Field("legal_entites", LegalEntityList),
	Field("divisions", DivisionList),
	Field("units", MapType(INDUSTRY_NAME, UnitList)),
	Field("domains", DomainList),
	Field("level_1_statutories", StatutoryList)
])

STATUTORY_WISE_COMPLIANCES = RecordType("STATUTORY_WISE_COMPLIANCES", [
	Field("level_1_statutory_name", LEVEL_1_STATUTORY_NAME),
	Field("compliences", VectorType(UNIT_WISE_STATUTORIES))
])

GetStatutoriesByUnitSuccess = RecordType("GetStatutoriesByUnitSuccess", [
	Field("statutory_wise_compliances", VectorType(STATUTORY_WISE_COMPLIANCES))
])

SavePastRecordsSuccess = RecordType("SavePastRecordsSuccess", [])

Response = VariantType("Response", [
	GetStatutorySettingsSuccess,
	UpdateStatutorySettingsSuccess,
	InvalidPassword,
	GetAssignCompliancesFormDataSuccess,
	GetComplianceForUnitsSuccess,
	SaveAssignedComplianceSuccess,
	AssigneeNotBelongToUnit,
	ConcurrenceNotBelongToUnit,
	ApprovalPersonNotBelongToUnit,
	GetUserwiseCompliancesSuccess,
	ReassignComplianceSuccess,
	GetComplianceApprovalListSuccess,
	ApproveComplianceSuccess,
	GetPastRecordsFormDataSuccess,
	GetStatutoriesByUnitSuccess,
	SavePastRecordsSuccess
])