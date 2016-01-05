from basics.types import VectorType, RecordType, Field, VariantType
from common import (COMPLIANCE_HISTORY_ID, Text20, Text500, COMPLIANCE_ID, UNIT_ID, Int8, Text100, SESSION_TOKEN)
from core import (
	ActiveCompliance,
	UpcomingCompliance
)

__all__ = [
	"Request", "Response", "RequestFormat", "ComplianceDetail", "ComplianceOnOccurrence"
]

#
# Request
#

GetComplianceDetail = RecordType("GetComplianceDetail", [])

CheckDiskSpace = RecordType("CheckDiskSpace", [])

UpdateComplianceDetail = RecordType("UpdateComplianceDetail", [
	Field("compliance_history_id", COMPLIANCE_HISTORY_ID),
	Field("documents", VectorType(Text20)),
	Field("completion_date", Text20),
	Field("validity_date", Text20),
	Field("next_due_date", Text20),
	Field("remarks", Text500)
])

GetOnOccurrenceCompliances = RecordType("GetOnOccurrenceCompliances", [])

StartOnOccurrenceCompliance = RecordType("StartOnOccurrenceCompliance", [
	Field("compliance_id", COMPLIANCE_ID),
	Field("start_date", Text20)
])

Request = VariantType("Request", [
	GetComplianceDetail, CheckDiskSpace,
	UpdateComplianceDetail,
	GetOnOccurrenceCompliances,
	StartOnOccurrenceCompliance
])

RequestFormat = RecordType("RequestFormat", [
	Field("session_token", SESSION_TOKEN),
	Field("request", Request)
])


#
# Response
#

ComplianceDetail = RecordType("ComplianceDetail", [
	Field("unit_id", UNIT_ID),
	Field("current_compliances", VectorType(ActiveCompliance)),
	Field("upcoming_compliances", VectorType(UpcomingCompliance))
])

GetComplianceDetailSuccess = RecordType("GetComplianceDetailSuccess", [
	Field("compliance_detail", VectorType(ComplianceDetail))
])

CheckDiskSpaceSuccess = RecordType("CheckDiskSpaceSuccess", [
	Field("total_disk_space", Int8),
	Field("available_disk_space", Int8)
])

UpdateComplianceDetailSuccess = RecordType("UpdateComplianceDetailSuccess", [])

NotEnoughDiskSpaceAvailable = RecordType("NotEnoughDiskSpaceAvailable", [])

ComplianceOnOccurrence = RecordType("ComplianceOnOccurrence", [
	Field("compliance_id",  COMPLIANCE_ID),
	Field("statutory_provision", Text500),
	Field("compliance_name", Text100),
	Field("description", Text500),
	Field("complete_within_days", Int8)
])

GetOnOccurrenceCompliancesSuccess = RecordType("GetOnOccurrenceCompliancesSuccess", [
	Field("compliances", VectorType(ComplianceOnOccurrence))
])

StartOnOccurrenceComplianceSuccess = RecordType("StartOnOccurrenceComplianceSuccess", [])

Response = VariantType("Response", [
	GetComplianceDetailSuccess,
	CheckDiskSpaceSuccess,
	UpdateComplianceDetailSuccess,
	NotEnoughDiskSpaceAvailable,
	GetOnOccurrenceCompliancesSuccess,
	StartOnOccurrenceComplianceSuccess
])