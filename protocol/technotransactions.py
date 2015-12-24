from common import *
from core import *

__all__=  [
	"Request", "Response"
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
	Field("submission_status", ASSIGN_STATUTORY_SUBMISSION_TYPE),
	Field("client_saved_statutory_id", CLIENT_SAVED_STATUTORY_ID),
	Field("client_assigned_statutory_id", CLIENT_ASSIGNED_STATUTORY_ID)
])

GetAssignedStatutoryWizardOneData = RecordType("GetAssignedStatutoryWizardOneData", [
])

GetStatutoryWizardTwoData = RecordType("GetStatutoryWizardTwoData", [
	Field("geography_id", GEOGRAPHY_ID),
	Field("industry_id", INDUSTRY_ID),
	Field("domain_id", DOMAIN_ID)
])

SaveAssignedStatutory = RecordType("SaveAssignedStatutory", [
	Field("submission_type", ASSIGN_STATUTORY_SUBMISSION_TYPE),
	Field("client_saved_statutory_id", CLIENT_SAVED_STATUTORY_ID),
	Field("client_assigned_statutory_id", CLIENT_ASSIGNED_STATUTORY_ID),
	Field("assigned_statutories", AssignedStatutoryList)
])

Request = VariantType("Request", [
	GetAssignedStatutoriesList, GetAssignedStatutoriesById, 
	GetAssignedStatutoryWizardOneData, GetStatutoryWizardTwoData,
	SaveAssignedStatutory
])


#
#	Response
#

### Assign Statutory

ASSIGNED_STATUTORIES = RecordType("ASSIGNED_STATUTORIES", [
	Field("submission_status", ASSIGN_STATUTORY_SUBMISSION_STATUS),
	Field("client_saved_statutory_id", CLIENT_SAVED_STATUTORY_ID),
	Field("client_assigned_statutory_id", CLIENT_ASSIGNED_STATUTORY_ID),
	Field("country_name", COUNTRY_NAME),
	Field("group_name", CLIENT_NAME),
	Field("business_group_name", BUSINESS_GROUP_NAME ),
	Field("legal_entity_name", LEGAL_ENTITY_NAME),
	Field("division_name", DIVISION_NAME),
	Field("unit_name", UNIT_NAME),
	Field("geography_name", GEOGRAPHY_NAME),
	Field("domain_name", DOMAIN_NAME)
])

GetAssignedStatutoriesListSuccess = RecordType("GetAssignedStatutoriesListSuccess", [
	Field("assigned_statutories", VectorType(ASSIGNED_STATUTORIES))
])

GetAssignedStatutoriesByIdSuccess = RecordType("GetAssignedStatutoriesByIdSuccess", [
	Field("country_name",  COUNTRY_NAME),
	Field("group_name",  CLIENT_NAME),
	Field("business_group_name",  BUSINESS_GROUP_NAME),
	Field("legal_entity_name",  LEGAL_ENTITY_NAME),
	Field("division_name",  DIVISION_NAME),
	Field("unit_name", UNIT_NAME),
	Field("geography_name",  GEOGRAPHY_NAME),
	Field("domain_name", DOMAIN_NAME),
	Field("statutories", AssignedStatutoryList)
])

UNIT = RecordType("ASSIGNED_STATUTORIES", [
	Field("unit_id", UNIT_ID),
	Field("unit_name", UNIT_NAME),
	Field("division_id", DIVISION_ID),
	Field("legal_entity_id", LEGAL_ENTITY_ID),
	Field("business_group_id", BUSINESS_GROUP_ID),
	Field("group_id", GROUP_ID),
	Field("domain_ids", DomainIdList),
	Field("industry_id", INDUSTRY_ID),
	Field("geography_id", GEOGRAPHY_ID)
])

GetAssignedStatutoryWizardOneDataSuccess = RecordType("GetAssignedStatutoryWizardOneDataSuccess", [
	Field("countries", CountryList),
	Field("domains", DomainList),
	Field("industries", IndustryList),
	Field("geography_levels", MapType(COUNTRY_ID, GeographyLevelList)),
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