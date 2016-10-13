from protocol.jsonvalidators import (parse_dictionary, parse_static_list)
from protocol.parse_structure import (
    parse_structure_VariantType_knowledgereport_Request

)
from protocol.to_structure import (
    to_structure_VariantType_knowledgereport_Request,
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
        domain_id = data.get("d_id")
        industry_id = data.get("i_id")
        statutory_nature_id = data.get("s_n_id")
        geography_id = data.get("g_id")
        level_1_statutory_id = data.get("level_1_s_id")
        frequency_id = data.get("f_id")
        record_count = data.get("r_count")
        return GetStatutoryMappingReportData(country_id, domain_id, industry_id, statutory_nature_id, geography_id, level_1_statutory_id, frequency_id, record_count)

    def to_inner_structure(self):
        return {
            "c_id": self.country_id,
            "d_id": self.domain_id,
            "i_id": self.industry_id,
            "s_n_id": self.statutory_nature_id,
            "g_id": self.geography_id,
            "level_1_s_id": self.level_1_statutory_id,
            "f_id": self.frequency_id,
            "r_count": self.record_count
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
        domains = data.get("domains")
        industries = data.get("industries")
        statutory_natures = data.get("statutory_natures")
        geographies = data.get("geographies")
        level_1_statutories = data.get("level_1_statutories")
        return GetStatutoryMappingReportFiltersSuccess(countries, domains, industries, statutory_natures, geographies, level_1_statutories)

    def to_inner_structure(self):
        return {
            "countries": self.countries,
            "domains": self.domains,
            "industries": self.industries,
            "statutory_natures": self.statutory_natures,
            "geographies": self.geographies,
            "level_1_statutories": self.level_1_statutories,
            "compliance_frequency": self.compliance_frequency,
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
        country_name = data.get("country_name")
        domain_name = data.get("domain_name")
        industry_names = data.get("industry_names")
        statutory_nature_name = data.get("statutory_nature_name")
        geography_mappings = data.get("geography_mappings")
        approval_status = data.get("approval_status")
        is_active = data.get("is_active")
        act_name = data.get("act_name")
        compliance_id = data.get("compliance_id")
        statutory_provision = data.get("statutory_provision")
        compliance_task = data.get("compliance_task")
        description = data.get("description")
        penal_consequences = data.get("penal_consequences")
        frequency_id = data.get("frequency_id")
        statutory_dates = data.get("statutory_dates")
        repeats_type_id = data.get("repeats_type_id")
        repeats_every = data.get("repeats_every")
        duration_type_id = data.get("duration_type_id")
        duration = data.get("duration")
        url = data.get("url")
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
            "country_name": self.country_name,
            "domain_name": self.domain_name,
            "industry_names": self.industry_names,
            "statutory_nature_name": self.statutory_nature_name,
            "geography_mappings": self.geography_mappings,
            "approval_status": self.approval_status,
            "is_active": self.is_active,
            "act_name": self.act_name,
            "compliance_id": self.compliance_id,
            "statutory_provision": self.statutory_provision,
            "compliance_task": self.compliance_task,
            "description": self.description,
            "penal_consequences": self.penal_consequences,
            "frequency_id": self.frequency_id,
            "statutory_dates": self.statutory_dates,
            "repeats_type_id": self.repeats_type_id,
            "repeats_every": self.repeats_every,
            "duration_type_id": self.duration_type_id,
            "duration": self.duration,
            "url": self.url

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
        domain_id = data.get("domain_id")
        statutory_mappings = data.get("statutory_mappings")
        total_count = data.get("total_count")
        return GetStatutoryMappingReportDataSuccess(
            country_id, domain_id, statutory_mappings, total_count
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "domain_id": self.domain_id,
            "statutory_mappings": self.statutory_mappings,
            "total_count": self.total_count
        }

class GetGeographyReportSuccess(Response):
    def __init__(self, countries, geographies):
        self.countries = countries
        self.geographies = geographies

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "geography_report"])
        countries = data.get("countries")
        geographies = data.get("geography_report")
        return GetGeographyReportSuccess(countries, geographies)

    def to_inner_structure(self):
        return {
            "countries": self.countries,
            "geography_report": self.geographies,
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
        is_active = data.get("is_active")
        return GeographyMapping(geography, is_active)

    def to_structure(self):
        return {
            "geography": self.geography,
            "is_active": self.is_active,
        }
