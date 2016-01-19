from basics.types import VectorType, RecordType, VariantType, MapType, Field, OptionalType
from common import (CLIENT_SAVED_STATUTORY_ID, CLIENT_ASSIGNED_STATUTORY_ID, CLIENT_NAME,
	GEOGRAPHY_ID, INDUSTRY_ID, COUNTRY_ID, COUNTRY_NAME, DOMAIN_ID, DOMAIN_NAME, BUSINESS_GROUP_NAME,
	BUSINESS_GROUP_ID, LEGAL_ENTITY_ID, LEGAL_ENTITY_NAME, DIVISION_ID, DIVISION_NAME, GROUP_ID,
	UNIT_ID, UNIT_NAME, GEOGRAPHY_NAME, SESSION_TOKEN, STATUTORY_ID)
from core import (AssignedStatutory, Country, Domain, Industry, GeographyLevel, Geography,
	GroupCompany, BusinessGroup, LegalEntity, Division, Domain, 
	ASSIGN_STATUTORY_SUBMISSION_TYPE, ASSIGN_STATUTORY_SUBMISSION_STATUS)

__all__=  [
	"Request", "Response", "RequestFormat", "ASSIGNED_STATUTORIES", "UNIT"
]

AssignedStatutoryList = VectorType(AssignedStatutory)
CountryList = VectorType(Country)
DomainList = VectorType(Domain)
IndustryList = VectorType(Industry)
GeographyLevelList = VectorType(GeographyLevel)
GeographyList = VectorType(Geography)
GroupCompanyList = VectorType(GroupCompany)
BusinessGroupList = VectorType(BusinessGroup)
LegalEntityList = VectorType(LegalEntity)
DivisionList = VectorType(Division)
DomainIdList = VectorType(Domain)

#	
#	Request
#

### Assign Statutory

GetAssignedStatutoriesList = RecordType("GetAssignedStatutoriesList", [
])

GetAssignedStatutoriesById = RecordType("GetAssignedStatutoriesById", [
	Field("client_statutory_id", CLIENT_SAVED_STATUTORY_ID)
])

GetAssignedStatutoryWizardOneData = RecordType("GetAssignedStatutoryWizardOneData", [
	Field("country_id", COUNTRY_ID)
])

GetStatutoryWizardTwoData = RecordType("GetStatutoryWizardTwoData", [
	Field("country_id", COUNTRY_ID),
	Field("geography_id", GEOGRAPHY_ID),
	Field("industry_id", INDUSTRY_ID),
	Field("domain_id", DOMAIN_ID),
	Field("unit_id", OptionalType(UNIT_ID))
])

# SaveAssignedCompliance = RecordType("SaveAssignedCompliance", [
# 	Field("compliance_id", COMPLIANCE_ID),
#     Field("compliance_applicable_status", STATUS), 
# ])

AssignedStatutoryCompliance = RecordType ("AssignedStatutoryCompliance", [
	Field("level_1_statutory_id", STATUTORY_ID),
	Field("compliances", MapType(COMPLIANCE_ID, STATUS)),
	Field("applicable_status", STATUS),
    Field("not_applicable_remarks", OptionalType(DESCRIPTION))
])

SaveAssignedStatutory = RecordType("SaveAssignedStatutory", [
	Field("country_id", COUNTRY_ID),
	Field("geography_id", GEOGRAPHY_ID),
	Field("industry_id", INDUSTRY_ID),
	Field("unit_ids", VectorType(UNIT_ID)),
	Field("domain_id", DOMAIN_ID),
	Field("submission_type", ASSIGN_STATUTORY_SUBMISSION_TYPE),
	Field("client_saved_statutory_id", OptionalType(CLIENT_SAVED_STATUTORY_ID)),
	# Field("client_assigned_statutory_id", CLIENT_ASSIGNED_STATUTORY_ID),
	Field("assigned_statutories", VectorType(AssignedStatutoryCompliance))
])

Request = VariantType("Request", [
	GetAssignedStatutoriesList, GetAssignedStatutoriesById, 
	GetAssignedStatutoryWizardOneData, GetStatutoryWizardTwoData,
	SaveAssignedStatutory
])

RequestFormat = RecordType("RequestFormat", [
	Field("session_token", SESSION_TOKEN),
	Field("request", Request)
])

#
#	Response
#

### Assign Statutory

ASSIGNED_STATUTORIES = RecordType("ASSIGNED_STATUTORIES", [
	Field("submission_status", ASSIGN_STATUTORY_SUBMISSION_STATUS),
	Field("client_statutory_id", CLIENT_ASSIGNED_STATUTORY_ID),
	Field("country_id", COUNTRY_ID),
	Field("country_name", COUNTRY_NAME),
	Field("client_id", CLIENT_ID),
	Field("group_name", CLIENT_NAME),
	Field("business_group_name", OptionalType(BUSINESS_GROUP_NAME )),
	Field("legal_entity_name", LEGAL_ENTITY_NAME),
	Field("division_name", OptionalType(DIVISION_NAME)),
	Field("unit_id", UNIT_ID),
	Field("unit_name", UNIT_NAME),
	Field("geography_id", GEOGRAPHY_ID),
	Field("geography_name", GEOGRAPHY_NAME),
	Field("domain_id", DOMAIN_ID),
	Field("domain_name", DOMAIN_NAME)
])

GetAssignedStatutoriesListSuccess = RecordType("GetAssignedStatutoriesListSuccess", [
	Field("assigned_statutories", VectorType(ASSIGNED_STATUTORIES))
])

GetAssignedStatutoriesByIdSuccess = RecordType("GetAssignedStatutoriesByIdSuccess", [
	Field("country_name",  COUNTRY_NAME),
	Field("group_name",  CLIENT_NAME),
	Field("business_group_name",  OptionalType(BUSINESS_GROUP_NAME)),
	Field("legal_entity_name",  LEGAL_ENTITY_NAME),
	Field("division_name",  OptionalType(DIVISION_NAME)),
	Field("unit_name", UNIT_NAME),
	Field("geography_name",  GEOGRAPHY_NAME),
	Field("domain_name", DOMAIN_NAME),
	Field("statutories", AssignedStatutoryList),
	Field("new_compliances", MapType(STATUTORY_ID, VectorType(ComplianceApplicability)))
])

UNIT = RecordType("UNIT", [
	Field("unit_id", UNIT_ID),
	Field("unit_name", UNIT_NAME),
	Field("division_id", OptionalType(DIVISION_ID)),
	Field("legal_entity_id", LEGAL_ENTITY_ID),
	Field("business_group_id", OptionalType(BUSINESS_GROUP_ID)),
	Field("client_id", GROUP_ID),
	Field("domain_ids", DomainIdList),
	Field("industry_id", INDUSTRY_ID),
	Field("geography_ids", VectorType(GEOGRAPHY_ID))
])

LevelList = VectorType(Level)

GetAssignedStatutoryWizardOneDataSuccess = RecordType("GetAssignedStatutoryWizardOneDataSuccess", [
	Field("domains", DomainList),
	Field("industries", IndustryList),
	Field("geography_levels", MapType(COUNTRY_ID, LevelList)),
	Field("geographies", MapType(COUNTRY_ID,GeographyList)),
	Field("group_companies", GroupCompanyList),
	Field("business_groups", BusinessGroupList),
	Field("legal_entities", LegalEntityList),
	Field("divisions", DivisionList),
	Field("units", VectorType(UNIT))
])

GetStatutoryWizardTwoDataSuccess = RecordType("GetStatutoryWizardTwoDataSuccess", [
	Field("statutories", AssignedStatutoryList)	
])

SaveAssignedStatutorySuccess = RecordType("SaveAssignedStatutorySuccess", [
])

Response = VariantType("Response", [
	GetAssignedStatutoriesListSuccess, GetAssignedStatutoriesByIdSuccess,
	GetAssignedStatutoryWizardOneDataSuccess, GetStatutoryWizardTwoDataSuccess,
	SaveAssignedStatutorySuccess
])