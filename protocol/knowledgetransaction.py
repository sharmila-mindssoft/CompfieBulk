from protocol.common import *

__all__ = [
	"Request", "Response"
]

#
# Request
#

GetStatutoryMappings = RecordType("GetStatutoryMappings", [])

SaveStatutoryMapping = RecordType("SaveStatutoryMapping", [
	Field("country_id", COUNTRY_ID),
	Field("domain_id", DOMAIN_ID),
	Field("industry_ids", VectorType(INDUSTRY_ID)),
	Field("statutory_nature_id", STATUTORY_NATURE_ID),
	Field("statutory_ids", VectorType(STATUTORY_ID)),
	Field("compliances", VectorType(Compliance)),
	Field("geography_ids", VectorType(GEOGRAPHY_ID))
])

UpdateStatutoryMapping = RecordType("UpdateStatutoryMapping", [
	Field("statutory_mapping_id", STATUTORY_MAPPING_ID),
	Field("industry_ids", VectorType(INDUSTRY_ID)),
	Field("statutory_nature_id", STATUTORY_NATURE_ID),
	Field("statutory_ids", VectorType(STATUTORY_ID)),
	Field("compliances", VectorType(Compliance)),
	Field("geography_ids", VectorType(GEOGRAPHY_ID))
])

ChangeStatutoryMappingStatus = RecordType("ChangeStatutoryMappingStatus", [
	Field("statutory_mapping_id", STATUTORY_MAPPING_ID),
	Field("is_active", IS_ACTIVE)
	
])

ApproveStatutoryMapping = RecordType("ApproveStatutoryMapping", [
	Field("statutory_mapping_id", STATUTORY_MAPPING_ID),
	Field("approval_status", APPROVAL_STATUS),
	Field("rejected_reason", REJECTED_REASON),
	Field("notification_text", NOTIFICATION_TEXT)
])

Request = VariantType("Request", [
	GetStatutoryMappings,
	SaveStatutoryMapping, UpdateStatutoryMapping,
	ChangeStatutoryMappingStatus, ApproveStatutoryMapping
])

#
# Response
#

DomainLevelMap = MapType(DOMAIN_ID, VectorType(Level))
DomainStatutoryMap = MapType(DOMAIN_ID, VectorType(Statutory))
StatutoryMapping = RecordType("StatutoryMapping", [
	Field("country_id", COUNTRY_ID),
    Field("country_name", COUNTRY_NAME),
    Field("domain_id", DOMAIN_ID),
    Field("domain_name", DOMAIN_NAME),
    Field("industry_ids", [INDUSTRY_ID,]),
    Field("industry_names", INDUSTRY_NAMES),
    Field("statutory_nature_id", STATUTORY_NATURE_ID),
    Field("statutory_nature_name", STATUTORY_NATURE_NAME),
    Field("statutory_ids", VectorType(STATUTORY_ID)),
    Field("statutory_mappings", VectorType(STATUTORY_MAPPING)),
    Field("compliances", VectorType(Compliance)),
    Field("compliance_names", VectorType(COMPLIANCE_NAMES)),
    Field("geographies", VectorType(GEOGRAPHY_ID)),
    Field("approval_status", APPROVAL_STATUS),
])

GetStatutoryMappingsSuccess = RecordType("GetStatutoryMappingsSuccess", [
   	Field("countries", VectorType(Country)),
	Field("domains", VectorType(Domain)),
	Field("industries", VectorType(Industry)),
	Field("statutory_natures", VectorType(StatutoryNature)),
	Field("statutory_levels", MapType(COUNTRY_ID, DomainLevelMap)),
	Field("statutories", MapType(COUNTRY_ID, DomainStatutoryMap))
	Field("geography_levels" MapType(COUNTRY_ID, VectorType(Level))),
	Field("geographies", MapType(COUNTRY_ID, VectorType(Geography))),
	Field("statutory_mappings", MapType(STATUTORY_MAPPING_ID, StatutoryMapping))
])

SaveStatutoryMappingSuccess = RecordType("SaveStatutoryMappingSuccess", [
])

UpdateStatutoryMappingSuccess = RecordType("UpdateStatutoryMappingSuccess", [
])

InvalidStatutoryMappingId = RecordType("InvalidStatutoryMappingId", [])

ChangeStatutoryMappingStatusSuccess = RecordType("ChangeStatutoryMappingStatusSuccess", [])

ApproveStatutoryMappingSuccess = RecordType("ApproveStatutoryMappingSuccess", [])

Response = VariantType("Response", [
	GetStatutoryMappingsSuccess,
	SaveStatutoryMappingSuccess, 
	UpdateStatutoryMappingSuccess,
	InvalidStatutoryMappingId,
	ChangeStatutoryMappingStatusSuccess,
	ApproveStatutoryMappingSuccess,
])
