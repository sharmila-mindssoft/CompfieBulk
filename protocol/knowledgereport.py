from basics.types import VectorType, RecordType, VariantType, MapType, Field
from common import (COUNTRY_ID, DOMAIN_ID, INDUSTRY_ID, STATUTORY_NATURE_ID, GEOGRAPHY_ID,
	LEVEL_1_STATUTORY_ID, IS_ACTIVE, Text)
from core import (StatutoryMapping, 
	Statutory, Country, Domain, Statutory,
	Industry, StatutoryNature, Geography)

__all__ = [
	"Request", "Response"
]

#
# Request
#

GetStatutoryMappingReportFilters = RecordType("GetStatutoryMappingReportFilters", [])

GetStatutoryMappingReportData = RecordType("GetStatutoryMappingReportData", [
	Field("country_id" , COUNTRY_ID),
	Field("domain_id" , DOMAIN_ID),
	Field("industry_id", INDUSTRY_ID),
	Field("statutory_nature_id", STATUTORY_NATURE_ID),
	Field("geography_id", GEOGRAPHY_ID),
	Field("level_1_statutory_id", LEVEL_1_STATUTORY_ID)
])

GetGeographyReport = RecordType("GetGeographyReport", [])

Request = VariantType("Request", [
	GetStatutoryMappingReportFilters, GetStatutoryMappingReportData,
	GetGeographyReport
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