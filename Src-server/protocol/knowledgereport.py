import json
from protocol.jsonvalidators import (parse_enum, parse_dictionary, parse_static_list)
from protocol.parse_structure import (
parse_structure_VectorType_RecordType_knowledgereport_MappingReport,
    parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_knowledgereport_GeographyMapping,
    parse_structure_Text,
    parse_structure_VectorType_RecordType_core_Domain,
    parse_structure_SignedIntegerType_8,
    parse_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory,
    parse_structure_VectorType_RecordType_core_Industry,
    parse_structure_VariantType_knowledgereport_Request,
    parse_structure_VectorType_RecordType_core_Country,
    parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Geography,
    parse_structure_Bool, parse_structure_CustomTextType_50,
    parse_structure_OptionalType_SignedIntegerType_8,
    parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_StatutoryMapping,
    parse_structure_VectorType_RecordType_core_StatutoryNature,
    parse_structure_VectorType_RecordType_core_ComplianceFrequency
)
from protocol.to_structure import (
    to_structure_VectorType_RecordType_knowledgereport_MappingReport,
    to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_knowledgereport_GeographyMapping,
    to_structure_Text, to_structure_VectorType_RecordType_core_Domain,
    to_structure_SignedIntegerType_8,
    to_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory,
    to_structure_VectorType_RecordType_core_Industry,
    to_structure_VariantType_knowledgereport_Request,
    to_structure_VectorType_RecordType_core_Country,
    to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Geography,
    to_structure_Bool, to_structure_CustomTextType_50,
    to_structure_OptionalType_SignedIntegerType_8,
    to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_StatutoryMapping,
    to_structure_VectorType_RecordType_core_StatutoryNature,
    to_structure_VectorType_RecordType_core_ComplianceFrequency
)

#
# Request
#

class Request(object):
    def to_structure(self):
        name = type(self).__name__
        inner = self.to_inner_structure()
        return [name, inner]

    def to_inner_structure(self):
        raise NotImplementedError

    @staticmethod
    def parse_structure(data):
        data = parse_static_list(data, 2)
        name, data = data
        if _Request_class_map.get(name) is None:
            msg = "invalid request: " + name
            raise ValueError(msg)
        return _Request_class_map[name].parse_inner_structure(data)

    @staticmethod
    def parse_inner_structure(data):
        raise NotImplementedError

class GetStatutoryMappingReportFilters(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetStatutoryMappingReportFilters()

    def to_inner_structure(self):
        return {
        }

class GetStatutoryMappingReportData(Request):
    def __init__(self, country_id, domain_id, industry_id, statutory_nature_id, geography_id, level_1_statutory_id):
        self.country_id = country_id
        self.domain_id = domain_id
        self.industry_id = industry_id
        self.statutory_nature_id = statutory_nature_id
        self.geography_id = geography_id
        self.level_1_statutory_id = level_1_statutory_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "domain_id", "industry_id", "statutory_nature_id", "geography_id", "level_1_statutory_id"])
        country_id = data.get("country_id")
        country_id = parse_structure_SignedIntegerType_8(country_id)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_SignedIntegerType_8(domain_id)
        industry_id = data.get("industry_id")
        industry_id = parse_structure_OptionalType_SignedIntegerType_8(industry_id)
        statutory_nature_id = data.get("statutory_nature_id")
        statutory_nature_id = parse_structure_OptionalType_SignedIntegerType_8(statutory_nature_id)
        geography_id = data.get("geography_id")
        geography_id = parse_structure_OptionalType_SignedIntegerType_8(geography_id)
        level_1_statutory_id = data.get("level_1_statutory_id")
        level_1_statutory_id = parse_structure_OptionalType_SignedIntegerType_8(level_1_statutory_id)
        return GetStatutoryMappingReportData(country_id, domain_id, industry_id, statutory_nature_id, geography_id, level_1_statutory_id)

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "industry_id": to_structure_OptionalType_SignedIntegerType_8(self.industry_id),
            "statutory_nature_id": to_structure_OptionalType_SignedIntegerType_8(self.statutory_nature_id),
            "geography_id": to_structure_OptionalType_SignedIntegerType_8(self.geography_id),
            "level_1_statutory_id": to_structure_OptionalType_SignedIntegerType_8(self.level_1_statutory_id),
        }

class GetGeographyReport(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetGeographyReport()

    def to_inner_structure(self):
        return {
        }


def _init_Request_class_map():
    classes = [GetStatutoryMappingReportFilters, GetStatutoryMappingReportData, GetGeographyReport]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Request_class_map = _init_Request_class_map()

#
# Response
#

class Response(object):
    def to_structure(self):
        name = type(self).__name__
        inner = self.to_inner_structure()
        return [name, inner]

    def to_inner_structure(self):
        raise NotImplementedError

    @staticmethod
    def parse_structure(data):
        data = parse_static_list(data, 2)
        name, data = data
        if _Response_class_map.get(name) is None:
            msg = "invalid request: " + name
            raise ValueError(msg)
        return _Response_class_map[name].parse_inner_structure(data)

    @staticmethod
    def parse_inner_structure(data):
        raise NotImplementedError

class GetStatutoryMappingReportFiltersSuccess(Response):
    def __init__(
        self, countries, domains, 
        industries, statutory_natures, geographies, 
        level_1_statutories, compliance_frequency
    ):
        self.countries = countries
        self.domains = domains
        self.industries = industries
        self.statutory_natures = statutory_natures
        self.geographies = geographies
        self.level_1_statutories = level_1_statutories
        self.compliance_frequency = compliance_frequency

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "industries", "statutory_natures", "geographies", "level_1_statutories"])
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        domains = data.get("domains")
        domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        industries = data.get("industries")
        industries = parse_structure_VectorType_RecordType_core_Industry(industries)
        statutory_natures = data.get("statutory_natures")
        statutory_natures = parse_structure_VectorType_RecordType_core_StatutoryNature(statutory_natures)
        geographies = data.get("geographies")
        geographies = parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Geography(geographies)
        level_1_statutories = data.get("level_1_statutories")
        level_1_statutories = parse_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(level_1_statutories)
        compliance_frequency = data.get("compliance_frequency")
        compliance_frequency = parse_structure_VectorType_RecordType_core_ComplianceFrequency(compliance_frequency)
        return GetStatutoryMappingReportFiltersSuccess(countries, domains, industries, statutory_natures, geographies, level_1_statutories)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "industries": to_structure_VectorType_RecordType_core_Industry(self.industries),
            "statutory_natures": to_structure_VectorType_RecordType_core_StatutoryNature(self.statutory_natures),
            "geographies": to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Geography(self.geographies),
            "level_1_statutories": to_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(self.level_1_statutories),
            "compliance_frequency": to_structure_VectorType_RecordType_core_ComplianceFrequency(self.compliance_frequency),
        }

class GetStatutoryMappingReportDataSuccess(Response):
    def __init__(self, country_wise_statutory_mappings):
        self.country_wise_statutory_mappings = country_wise_statutory_mappings

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_wise_statutory_mappings"])
        country_wise_statutory_mappings = data.get("country_wise_statutory_mappings")
        country_wise_statutory_mappings = parse_structure_VectorType_RecordType_knowledgereport_MappingReport(country_wise_statutory_mappings)
        return GetStatutoryMappingReportDataSuccess(country_wise_statutory_mappings)

    def to_inner_structure(self):
        return {
            "country_wise_statutory_mappings": to_structure_VectorType_RecordType_knowledgereport_MappingReport(self.country_wise_statutory_mappings),
        }

class GetGeographyReportSuccess(Response):
    def __init__(self, countries, geographies):
        self.countries = countries
        self.geographies = geographies

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "geographies"])
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        geographies = data.get("geographies")
        geographies = parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_knowledgereport_GeographyMapping(geographies)
        return GetGeographyReportSuccess(countries, geographies)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "geographies": to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_knowledgereport_GeographyMapping(self.geographies),
        }


def _init_Response_class_map():
    classes = [GetStatutoryMappingReportFiltersSuccess, GetStatutoryMappingReportDataSuccess, GetGeographyReportSuccess]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()

#
# RequestFormat
#

class RequestFormat(object):
    def __init__(self, session_token, request):
        self.session_token = session_token
        self.request = request

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["session_token", "request"])
        session_token = data.get("session_token")
        session_token = parse_structure_CustomTextType_50(session_token)
        request = data.get("request")
        request = parse_structure_VariantType_knowledgereport_Request(request)
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": to_structure_CustomTextType_50(self.session_token),
            "request": to_structure_VariantType_knowledgereport_Request(self.request),
        }

#
# GeographyMapping
#

class GeographyMapping(object):
    def __init__(self, geography, is_active):
        self.geography = geography
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["geography", "is_active"])
        geography = data.get("geography")
        geography = parse_structure_Text(geography)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return GeographyMapping(geography, is_active)

    def to_structure(self):
        return {
            "geography": to_structure_Text(self.geography),
            "is_active": to_structure_Bool(self.is_active),
        }

#
# MappingReport
#

class MappingReport(object):
    def __init__(self, country_id, domain_id, statutory_mappings):
        self.country_id = country_id
        self.domain_id = domain_id
        self.statutory_mappings = statutory_mappings

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["country_id", "domain_id", "statutory_mappings"])
        country_id = data.get("country_id")
        country_id = parse_structure_SignedIntegerType_8(country_id)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_SignedIntegerType_8(domain_id)
        statutory_mappings = data.get("statutory_mappings")
        statutory_mappings = parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_StatutoryMapping(statutory_mappings)
        return MappingReport(country_id, domain_id, statutory_mappings)

    def to_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "statutory_mappings": to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_StatutoryMapping(self.statutory_mappings),
        }

