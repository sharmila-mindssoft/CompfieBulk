from protocol.jsonvalidators import (parse_dictionary, parse_static_list)
from protocol.parse_structure import (
    parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_knowledgereport_GeographyMapping,
    parse_structure_Text,
    parse_structure_VectorType_RecordType_core_Domain,
    parse_structure_UnsignedIntegerType_32,
    parse_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory,
    parse_structure_VectorType_RecordType_core_Industry,
    parse_structure_VariantType_knowledgereport_Request,
    parse_structure_VectorType_RecordType_core_Country,
    parse_structure_MapType_UnsignedIntegerType_32_VectorType_RecordType_core_Geography,
    parse_structure_Bool, parse_structure_CustomTextType_50,
    parse_structure_OptionalType_SignedIntegerType_8,
    parse_structure_VectorType_RecordType_core_StatutoryNature,
    parse_structure_VectorType_RecordType_core_ComplianceFrequency,
    parse_structure_VectorType_Text,
    parse_structure_SignedIntegerType_8,
    parse_structure_CustomTextType_100,
    parse_structure_OptionalType_UnsignedIntegerType_32,
    parse_structure_OptionalType_CustomTextType_500,
    parse_structure_OptionalType_VectorType_RecordType_core_StatutoryDate,
    parse_structure_OptionalType_Text

)
from protocol.to_structure import (
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
    to_structure_VectorType_RecordType_core_StatutoryNature,
    to_structure_VectorType_RecordType_core_ComplianceFrequency,
    to_structure_VectorType_Text,
    to_structure_CustomTextType_100,
    to_structure_OptionalType_UnsignedIntegerType_32,
    to_structure_OptionalType_CustomTextType_500,
    to_structure_OptionalType_VectorType_RecordType_core_StatutoryDate,
    to_structure_OptionalType_Text,
    to_structure_VectorType_RecordType_knowledgereport_StatutoryMapping,
    to_structure_UnsignedIntegerType_32
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
    def __init__(
        self, country_id, domain_id, industry_id,
        statutory_nature_id, geography_id, level_1_statutory_id, frequency_id,
        record_count
    ):
        self.country_id = country_id
        self.domain_id = domain_id
        self.industry_id = industry_id
        self.statutory_nature_id = statutory_nature_id
        self.geography_id = geography_id
        self.level_1_statutory_id = level_1_statutory_id
        self.frequency_id = frequency_id
        self.record_count = record_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_id", "d_id", "i_id", "s_n_id", "g_id", "level_1_s_id", "f_id", "r_count"])
        country_id = data.get("c_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        domain_id = data.get("d_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        industry_id = data.get("i_id")
        industry_id = parse_structure_OptionalType_SignedIntegerType_8(industry_id)
        statutory_nature_id = data.get("s_n_id")
        statutory_nature_id = parse_structure_OptionalType_SignedIntegerType_8(statutory_nature_id)
        geography_id = data.get("g_id")
        geography_id = parse_structure_OptionalType_SignedIntegerType_8(geography_id)
        level_1_statutory_id = data.get("level_1_s_id")
        level_1_statutory_id = parse_structure_OptionalType_SignedIntegerType_8(level_1_statutory_id)
        frequency_id = data.get("f_id")
        frequency_id = parse_structure_OptionalType_SignedIntegerType_8(frequency_id)
        record_count = data.get("r_count")
        record_count = parse_structure_UnsignedIntegerType_32(record_count)
        return GetStatutoryMappingReportData(country_id, domain_id, industry_id, statutory_nature_id, geography_id, level_1_statutory_id, record_count)

    def to_inner_structure(self):
        return {
            "c_id": to_structure_SignedIntegerType_8(self.country_id),
            "d_id": to_structure_SignedIntegerType_8(self.domain_id),
            "i_id": to_structure_OptionalType_SignedIntegerType_8(self.industry_id),
            "s_n_id": to_structure_OptionalType_SignedIntegerType_8(self.statutory_nature_id),
            "g_id": to_structure_OptionalType_SignedIntegerType_8(self.geography_id),
            "level_1_s_id": to_structure_OptionalType_SignedIntegerType_8(self.level_1_statutory_id),
            "f_id": to_structure_OptionalType_SignedIntegerType_8(self.frequency_id),
            "r_count": to_structure_UnsignedIntegerType_32(self.record_count)
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

class GetDomainsReport(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetDomainsReport()

    def to_inner_structure(self):
        return {}

class GetCountriesReport(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetCountriesReport()

    def to_inner_structure(self):
        return {}


def _init_Request_class_map():
    classes = [
        GetStatutoryMappingReportFilters,
        GetStatutoryMappingReportData, GetGeographyReport,
        GetDomainsReport, GetCountriesReport
    ]
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
        geographies = parse_structure_MapType_UnsignedIntegerType_32_VectorType_RecordType_core_Geography(geographies)
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

class StatutoryMappingReport(object):
    def __init__(
        self, country_name,
        domain_name, industry_names,
        statutory_nature_name,
        geography_mappings,
        approval_status, is_active,
        act_name,
        compliance_id, statutory_provision,
        compliance_task, description,
        penal_consequences,
        frequency_id, statutory_dates, repeats_type_id,
        repeats_every, duration_type_id,
        duration, url
    ):
        self.country_name = country_name
        self.domain_name = domain_name
        self.industry_names = industry_names
        self.statutory_nature_name = statutory_nature_name
        self.geography_mappings = geography_mappings
        self.approval_status = approval_status
        self.is_active = is_active
        self.act_name = act_name
        self.compliance_id = compliance_id
        self.statutory_provision = statutory_provision
        self.compliance_task = compliance_task
        self.description = description
        self.penal_consequences = penal_consequences
        self.frequency_id = frequency_id
        self.statutory_dates = statutory_dates
        self.repeats_type_id = repeats_type_id
        self.repeats_every = repeats_every
        self.duration_type_id = duration_type_id
        self.duration = duration
        self.url = url

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "country_name",
            "domain_name", "industry_names",
            "statutory_nature_name",
            "geography_mappings", "approval_status", "is_active",
            "act_name",
            "compliance_id", "statutory_provision",
            "compliance_task", "description",
            "penal_consequences", "frequency_id",
            "statutory_dates", "repeats_type_id",
            "repeats_every", "duration_type_id",
            "duration", "url"
        ])
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        country_name = data.get("country_name")
        country_name = parse_structure_CustomTextType_50(country_name)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        domain_name = data.get("domain_name")
        domain_name = parse_structure_CustomTextType_50(domain_name)
        industry_names = data.get("industry_names")
        industry_names = parse_structure_Text(industry_names)
        statutory_nature_name = data.get("statutory_nature_name")
        statutory_nature_name = parse_structure_CustomTextType_50(statutory_nature_name)
        geography_mappings = data.get("geography_mappings")
        geography_mappings = parse_structure_VectorType_Text(geography_mappings)
        approval_status = data.get("approval_status")
        approval_status = parse_structure_SignedIntegerType_8(approval_status)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        act_name = data.get("act_name")
        act_name = parse_structure_CustomTextType_100(act_name)
        compliance_id = data.get("compliance_id")
        compliance_id = parse_structure_OptionalType_UnsignedIntegerType_32(compliance_id)
        statutory_provision = data.get("statutory_provision")
        statutory_provision = parse_structure_Text(statutory_provision)
        compliance_task = data.get("compliance_task")
        compliance_task = to_structure_Text(compliance_task)
        description = data.get("description")
        description = parse_structure_Text(description)
        penal_consequences = data.get("penal_consequences")
        penal_consequences = parse_structure_OptionalType_CustomTextType_500(penal_consequences)
        frequency_id = data.get("frequency_id")
        frequency_id = parse_structure_OptionalType_SignedIntegerType_8(frequency_id)
        statutory_dates = data.get("statutory_dates")
        statutory_dates = parse_structure_OptionalType_VectorType_RecordType_core_StatutoryDate(statutory_dates)
        repeats_type_id = data.get("repeats_type_id")
        repeats_type_id = parse_structure_OptionalType_UnsignedIntegerType_32(repeats_type_id)
        repeats_every = data.get("repeats_every")
        repeats_every = parse_structure_OptionalType_UnsignedIntegerType_32(repeats_every)
        duration_type_id = data.get("duration_type_id")
        duration_type_id = parse_structure_OptionalType_UnsignedIntegerType_32(duration_type_id)
        duration = data.get("duration")
        duration = parse_structure_OptionalType_UnsignedIntegerType_32(duration)
        url = data.get("url")
        url = parse_structure_OptionalType_Text(url)
        return StatutoryMappingReport(
            country_name, domain_name,
            industry_names,
            statutory_nature_name,
            geography_mappings, approval_status, is_active,
            act_name,
            compliance_id, statutory_provision,
            compliance_task, description,
            penal_consequences, frequency_id,
            statutory_dates, repeats_type_id,
            repeats_every, duration_type_id,
            duration, url
        )

    def to_structure(self):
        return {
            "country_name": to_structure_CustomTextType_50(self.country_name),
            "domain_name": to_structure_CustomTextType_50(self.domain_name),
            "industry_names": to_structure_Text(self.industry_names),
            "statutory_nature_name": to_structure_CustomTextType_50(self.statutory_nature_name),
            "geography_mappings": to_structure_VectorType_Text(self.geography_mappings),
            "approval_status": to_structure_SignedIntegerType_8(self.approval_status),
            "is_active": to_structure_Bool(self.is_active),
            "act_name": to_structure_CustomTextType_100(self.act_name),
            "compliance_id": to_structure_OptionalType_UnsignedIntegerType_32(self.compliance_id),
            "statutory_provision": to_structure_Text(self.statutory_provision),
            "compliance_task": to_structure_Text(self.compliance_task),
            "description": to_structure_Text(self.description),
            "penal_consequences": to_structure_OptionalType_CustomTextType_500(self.penal_consequences),
            "frequency_id": to_structure_OptionalType_SignedIntegerType_8(self.frequency_id),
            "statutory_dates": to_structure_OptionalType_VectorType_RecordType_core_StatutoryDate(self.statutory_dates),
            "repeats_type_id": to_structure_OptionalType_UnsignedIntegerType_32(self.repeats_type_id),
            "repeats_every": to_structure_OptionalType_UnsignedIntegerType_32(self.repeats_every),
            "duration_type_id": to_structure_OptionalType_UnsignedIntegerType_32(self.duration_type_id),
            "duration": to_structure_OptionalType_UnsignedIntegerType_32(self.duration),
            "url": to_structure_OptionalType_Text(self.url)

        }


class GetStatutoryMappingReportDataSuccess(Response):
    def __init__(self, country_id, domain_id, statutory_mappings, total_count):
        self.country_id = country_id
        self.domain_id = domain_id
        self.statutory_mappings = statutory_mappings
        self.total_count = total_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["country_id", "domain_id", "statutory_mappings", "total_count"])
        country_id = data.get("country_id")
        country_id = parse_structure_SignedIntegerType_8(country_id)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_SignedIntegerType_8(domain_id)
        statutory_mappings = data.get("statutory_mappings")
        statutory_mappings = to_structure_VectorType_RecordType_knowledgereport_StatutoryMapping(statutory_mappings)
        total_count = data.get("total_count")
        total_count = parse_structure_UnsignedIntegerType_32(total_count)
        return GetStatutoryMappingReportDataSuccess(
            country_id, domain_id, statutory_mappings, total_count
        )

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "statutory_mappings": to_structure_VectorType_RecordType_knowledgereport_StatutoryMapping(self.statutory_mappings),
            "total_count": to_structure_UnsignedIntegerType_32(self.total_count)
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
