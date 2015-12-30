from basics.types import VectorType, RecordType, VariantType, MapType, Field, OptionalType
from common import (COUNTRY_ID, DOMAIN_ID, INDUSTRY_ID, STATUTORY_NATURE_ID, GEOGRAPHY_ID,
	LEVEL_1_STATUTORY_ID, IS_ACTIVE, Text, SESSION_TOKEN)
from core import (StatutoryMapping, 
	Statutory, Country, Domain, Statutory,
	Industry, StatutoryNature, Geography)

__all__ = [
	"Request", "Response", "RequestFormat", "GeographyMapping", "MappingReport"
]

#
# Request
#

GetStatutoryMappingReportFilters = RecordType("GetStatutoryMappingReportFilters", [])

GetStatutoryMappingReportData = RecordType("GetStatutoryMappingReportData", [
	Field("country_id" , COUNTRY_ID),
	Field("domain_id" , DOMAIN_ID),
	Field("industry_id", OptionalType(INDUSTRY_ID)),
	Field("statutory_nature_id", OptionalType(STATUTORY_NATURE_ID)),
	Field("geography_id", OptionalType(GEOGRAPHY_ID)),
	Field("level_1_statutory_id", OptionalType(LEVEL_1_STATUTORY_ID))
])

GetGeographyReport = RecordType("GetGeographyReport", [])

Request = VariantType("Request", [
	GetStatutoryMappingReportFilters, GetStatutoryMappingReportData,
	GetGeographyReport
])

RequestFormat = RecordType("RequestFormat", [
	Field("session_token", SESSION_TOKEN),
	Field("request", Request)
])

#
# Response
#

DomainStatutoryMap = MapType(DOMAIN_ID, VectorType(Statutory))

GetStatutoryMappingReportFiltersSuccess = RecordType("GetStatutoryMappingReportFiltersSuccess", [
	Field("countries", VectorType(Country)),
	Field("domains", VectorType(Domain)),
	Field("industries", VectorType(Industry)),
	Field("statutory_natures", VectorType(StatutoryNature)),
	Field("geographies", MapType(COUNTRY_ID, VectorType(Geography))),
	Field("level_1_statutories", MapType(COUNTRY_ID, DomainStatutoryMap)),
])

MappingReport = RecordType("MappingReport", [
	Field("country_id", COUNTRY_ID),
    Field("domain_id",  DOMAIN_ID),
    Field("statutory_mappings", MapType(LEVEL_1_STATUTORY_ID, VectorType(StatutoryMapping)))
])

GetStatutoryMappingReportDataSuccess = RecordType("GetStatutoryMappingReportDataSuccess", [
	Field("country_wise_statutory_mappings", VectorType(MappingReport))
])

GeographyMapping = RecordType("GeographyMapping", [
	Field("geography", Text),
	Field("is_active", IS_ACTIVE)
])

GetGeographyReportSuccess = RecordType("GetGeographyReportSuccess", [
	Field("countries", VectorType(Country)),
	Field("geographies", MapType(COUNTRY_ID, VectorType(GeographyMapping)))	
])

Response = VariantType("Response", [
	GetStatutoryMappingReportFiltersSuccess,
	GetStatutoryMappingReportDataSuccess,
	GetGeographyReportSuccess
])