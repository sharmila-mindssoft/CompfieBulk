from basics.types import VectorType, RecordType, VariantType, MapType, Field
from common import (GEOGRAPHY_LEVEL_ID, GEOGRAPHY_NAME, 
	GEOGRAPHY_ID, COUNTRY_ID, IS_ACTIVE, INDUSTRY_ID, INDUSTRY_NAME,
	STATUTORY_NATURE_NAME, STATUTORY_NATURE_ID, DOMAIN_ID,
	STATUTORY_LEVEL_ID, STATUTORY_ID, STATUTORY_NAME, SESSION_TOKEN)

from core import Level, Industry, StatutoryNature, Country, Domain, Geography, Statutory
__all__ = [
	"Request", "Response", "RequestFormat"
]

LevelList = VectorType(Level)
#
# Request
#

GetGeographyLevels = RecordType("GetGeographyLevels", [])

SaveGeographyLevel = RecordType("SaveGeographyLevel", [
	Field("country_id", COUNTRY_ID),
	Field("levels", LevelList)
])

GetGeographies = RecordType("GetGeographies", [])

SaveGeography  = RecordType("SaveGeography", [
	Field("geography_level_id", GEOGRAPHY_LEVEL_ID),
	Field("geography_name", GEOGRAPHY_NAME),
	Field("parent_ids", VectorType(GEOGRAPHY_ID))
])

UpdateGeography = RecordType("UpdateGeography", [
	Field("geography_id", GEOGRAPHY_ID),
	Field("geography_level_id", GEOGRAPHY_LEVEL_ID),
	Field("geography_name", GEOGRAPHY_NAME),
	Field("parent_ids", VectorType(GEOGRAPHY_ID))
])

ChangeGeographyStatus = RecordType("ChangeGeographyStatus", [
	Field("geography_id", GEOGRAPHY_ID),
	Field("is_active", IS_ACTIVE)
])

GetIndustries = RecordType("GetIndustries", [])

SaveIndustry = RecordType("SaveIndustry", [
	Field("industry_name", INDUSTRY_NAME)
])

UpdateIndustry = RecordType("UpdateIndustry", [
	Field("industry_id", INDUSTRY_ID),
	Field("industry_name", INDUSTRY_NAME)
])

ChangeIndustryStatus = RecordType("ChangeIndustryStatus", [
	Field("industry_id", INDUSTRY_ID),
	Field("is_active", IS_ACTIVE)
])

GetStatutoryNatures = RecordType("GetStatutoryNatures", [])

SaveStatutoryNature = RecordType("SaveStatutoryNature", [
	Field("statutory_nature_name", STATUTORY_NATURE_NAME)
])

UpdateStatutoryNature = RecordType("UpdateStatutoryNature", [
	Field("statutory_nature_id", STATUTORY_NATURE_ID),
	Field("statutory_nature_name", STATUTORY_NATURE_NAME)
])

ChangeStatutoryNatureStatus = RecordType("ChangeStatutoryNatureStatus", [
	Field("statutory_nature_id", STATUTORY_NATURE_ID),
	Field("is_active", IS_ACTIVE)
])

GetStatutoryLevels = RecordType("GetStatutoryLevels", [])

SaveStatutoryLevel = RecordType("SaveStatutoryLevel", [
	Field("country_id", COUNTRY_ID),
	Field("domain_id", DOMAIN_ID),
	Field("levels", LevelList),
])


GetStatutories = RecordType("GetStatutories", [])

SaveStatutory  = RecordType("SaveStatutory", [
	Field("statutory_level_id", STATUTORY_LEVEL_ID),
	Field("statutory_name", STATUTORY_NAME),
	Field("parent_ids", VectorType(STATUTORY_ID))
])

UpdateStatutory = RecordType("UpdateStatutory", [
	Field("statutory_id", STATUTORY_ID),
	Field("statutory_level_id", STATUTORY_LEVEL_ID),
	Field("statutory_name", STATUTORY_NAME),
	Field("parent_ids", VectorType(STATUTORY_ID))
])


Request = VariantType("Request", [
	GetGeographyLevels, SaveGeographyLevel,
	GetGeographies, SaveGeography,
	UpdateGeography, ChangeGeographyStatus,
	GetIndustries, SaveIndustry,
	UpdateIndustry, ChangeIndustryStatus,
	GetStatutoryNatures, SaveStatutoryNature,
	UpdateStatutoryNature, ChangeStatutoryNatureStatus,
	GetStatutoryLevels, SaveStatutoryLevel,
	GetStatutories, 
	SaveStatutory, UpdateStatutory

])

RequestFormat = RecordType("RequestFormat", [
	Field("session_token", SESSION_TOKEN),
	Field("request", Request)
])


#
# Response
#

GetGeographyLevelsSuccess = RecordType("GetGeographyLevelsSuccess", [
	Field("countries", VectorType(Country)),
	Field("geography_levels", MapType(COUNTRY_ID, LevelList))
])

SaveGeographyLevelSuccess = RecordType("SaveGeographyLevelSuccess", [])

DuplicateGeographyLevelsExists = RecordType("DuplicateGeographyLevelsExists", [])

UpdateGeographyLevelSuccess = RecordType("UpdateGeographyLevelSuccess", [])

InvalidGeographyLevelId = RecordType("InvalidGeographyLevelId", [])

GetGeographiesSuccess = RecordType("GetGeographiesSuccess", [
	Field("countries", VectorType(Country)),
	Field("geography_levels", MapType(COUNTRY_ID, LevelList)),
	Field("geographies", MapType(COUNTRY_ID, VectorType(Geography)))
])

SaveGeographySuccess = RecordType("SaveGeographySuccess", [])

GeographyNameAlreadyExists = RecordType("GeographyNameAlreadyExists", [])

InvalidGeographyId = RecordType("InvalidGeographyId", [])

ChangeGeographyStatusSuccess = RecordType("ChangeGeographyStatusSuccess", [])

GetIndustriesSuccess = RecordType("GetIndustriesSuccess", [
	Field("industries", VectorType(Industry))
])

SaveIndustrySuccess = RecordType("SaveIndustrySuccess", [])

IndustryNameAlreadyExists = RecordType("IndustryNameAlreadyExists", [])

UpdateIndustrySuccess = RecordType("UpdateIndustrySuccess", [])

InvalidIndustryId = RecordType("InvalidIndustryId", [])

ChangeIndustryStatusSuccess = RecordType("ChangeIndustryStatusSuccess", [])

GetStatutoryNaturesSuccess = RecordType("GetStatutoryNaturesSuccess", [
	Field("statutory_natures", VectorType(StatutoryNature))
])

SaveStatutoryNatureSuccess = RecordType("SaveStatutoryNatureSuccess", [])

StatutoryNatureNameAlreadyExists = RecordType("StatutoryNatureNameAlreadyExists", [])

UpdateStatutoryNatureSuccess = RecordType("UpdateStatutoryNatureSuccess", [])

InvalidStatutoryNatureId = RecordType("InvalidStatutoryNatureId", [])

ChangeStatutoryNatureStatusSuccess = RecordType("ChangeStatutoryNatureStatusSuccess", [])

DomainLevelMap = MapType(DOMAIN_ID, VectorType(Level))

GetStatutoryLevelsSuccess = RecordType("GetStatutoryLevelsSuccess", [
	Field("countries", VectorType(Country)),
	Field("domains", VectorType(Domain)),
	Field("statutory_levels", MapType(COUNTRY_ID, DomainLevelMap))
])

SaveStatutoryLevelSuccess = RecordType("SaveStatutoryLevelSuccess", [])

DuplicateStatutoryLevelsExists = RecordType("DuplicateStatutoryLevelsExists", [])

DomainStatutoryMap = MapType(DOMAIN_ID, VectorType(Statutory))

GetStatutoriesSuccess = RecordType("GetStatutoriesSuccess", [
	Field("countries", VectorType(Country)),
	Field("domains", VectorType(Domain)),
	Field("statutory_levels", MapType(COUNTRY_ID, DomainLevelMap)),
	Field("statutories", MapType(COUNTRY_ID, DomainStatutoryMap))
])

SaveStatutorySuccess = RecordType("SaveStatutorySuccess", [])

StatutoryNameAlreadyExists = RecordType("StatutoryNameAlreadyExists", [])

InvalidStatutoryId = RecordType("InvalidStatutoryId", [])


Response = VariantType("Response", [
	GetGeographyLevelsSuccess,
	SaveGeographyLevelSuccess, DuplicateGeographyLevelsExists,
	UpdateGeographyLevelSuccess, InvalidGeographyLevelId,
	GetGeographiesSuccess, 
	SaveGeographySuccess, GeographyNameAlreadyExists,
	InvalidGeographyId, ChangeGeographyStatusSuccess,
	GetIndustriesSuccess, SaveIndustrySuccess,
	IndustryNameAlreadyExists, UpdateIndustrySuccess,
	InvalidIndustryId, ChangeIndustryStatusSuccess,
	GetStatutoryNaturesSuccess,
	SaveStatutoryNatureSuccess, StatutoryNatureNameAlreadyExists,
	UpdateStatutoryNatureSuccess,
	ChangeStatutoryNatureStatusSuccess, InvalidStatutoryNatureId,
	GetStatutoryLevelsSuccess,
	SaveStatutoryLevelSuccess, DuplicateStatutoryLevelsExists,
	GetStatutoriesSuccess, SaveStatutorySuccess, StatutoryNameAlreadyExists,
	InvalidStatutoryId
])