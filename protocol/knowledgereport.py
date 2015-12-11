from protocol.common import *

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

#
# Response
#

DomainStatutoryMap = MapType(DOMAIN_ID, VectorType(Statutory))

GetStatutoryMappingReportFiltersSuccess = RecordType("GetStatutoryMappingReportFiltersSuccess"), [
	Field("countries", VectorType(Country)),
	Field("domains", VectorType(Domain)),
	Field("industries", VectorType(Industry)),
	Field("statutory_natures", VectorType(StatutoryNature)),
	Field("geographies", MapType(COUNTRY_ID, VectorType(Geography))),
	Field("level_1_statutories", MapType(COUNTRY_ID, DomainStatutoryMap))),
]

GetStatutoryMappingReportDataSuccess = RecordType("GetStatutoryMappingReportDataSuccess", [

])

GeographyMapping = RecordType("GeographyMapping", [
	Field("geography", Text),
	Field("is_active", IS_ACTIVE)
])

GetGeographyReportSuccess = RecordType("GetGeographyReportSuccess", [
	Field("countries", VectorType(Country)),
	Field("geographies", MapType(COUNTRY_ID, VectorType(GeographyMapping)))	
])