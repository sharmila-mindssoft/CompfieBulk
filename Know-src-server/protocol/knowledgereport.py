from protocol.jsonvalidators import (
    parse_dictionary, parse_static_list,
    to_structure_dictionary_values,  parse_VariantType,
    to_VariantType
)

#
# Request
#

class Request(object):
    def to_structure(self):
        name = type(self).__name__
        inner = self.to_inner_structure()
        if type(inner) is dict:
            inner = to_structure_dictionary_values(inner)
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
        record_count, page_count
    ):
        self.country_id = country_id
        self.domain_id = domain_id
        self.industry_id = industry_id
        self.statutory_nature_id = statutory_nature_id
        self.geography_id = geography_id
        self.level_1_statutory_id = level_1_statutory_id
        self.frequency_id = frequency_id
        self.record_count = record_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_id", "d_id", "a_i_id", "a_s_n_id", "a_g_id", "statutory_id_optional", "frequency_id", "r_count", "page_count"])
        country_id = data.get("c_id")
        domain_id = data.get("d_id")
        industry_id = data.get("a_i_id")
        statutory_nature_id = data.get("a_s_n_id")
        geography_id = data.get("a_g_id")
        level_1_statutory_id = data.get("statutory_id_optional")
        frequency_id = data.get("frequency_id")
        record_count = data.get("r_count")
        page_count = data.get("page_count")
        return GetStatutoryMappingReportData(country_id, domain_id, industry_id, statutory_nature_id, geography_id, level_1_statutory_id, frequency_id, record_count, page_count)

    def to_inner_structure(self):
        return {
            "c_id": self.country_id,
            "d_id": self.domain_id,
            "a_i_id": self.industry_id,
            "a_s_n_id": self.statutory_nature_id,
            "a_g_id": self.geography_id,
            "statutory_id_optional": self.level_1_statutory_id,
            "frequency_id": self.frequency_id,
            "r_count": self.record_count,
            "page_count": self.page_count
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
        if type(inner) is dict:
            inner = to_structure_dictionary_values(inner)
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
        data = parse_dictionary(data, ["countries", "domains", "industries", "statutory_natures", "geographies", "level_one_statutories"])
        countries = data.get("countries")
        domains = data.get("domains")
        industries = data.get("industries")
        statutory_natures = data.get("statutory_natures")
        geographies = data.get("geographies")
        level_1_statutories = data.get("level_one_statutories")
        return GetStatutoryMappingReportFiltersSuccess(countries, domains, industries, statutory_natures, geographies, level_1_statutories)

    def to_inner_structure(self):
        return {
            "countries": self.countries,
            "domains": self.domains,
            "industries": self.industries,
            "statutory_natures": self.statutory_natures,
            "geographies": self.geographies,
            "level_one_statutories": self.level_1_statutories,
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
        duration, url, summary
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
        self.summary = summary

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "country_name",
            "domain_name", "industry_names",
            "statutory_nature_name",
            "geo_maps", "approval_status_id", "is_active",
            "act_name",
            "comp_id", "s_pro_map",
            "c_task", "description",
            "p_consequences", "frequency_id",
            "statu_dates", "r_type_id",
            "r_every", "d_type_id",
            "duration", "url", "summary"
        ])
        country_name = data.get("country_name")
        domain_name = data.get("domain_name")
        industry_names = data.get("industry_names")
        statutory_nature_name = data.get("statutory_nature_name")
        geography_mappings = data.get("geo_maps")
        approval_status = data.get("approval_status_id")
        is_active = data.get("is_active")
        act_name = data.get("act_name")
        compliance_id = data.get("comp_id")
        statutory_provision = data.get("s_pro_map")
        compliance_task = data.get("c_task")
        description = data.get("description")
        penal_consequences = data.get("p_consequences")
        frequency_id = data.get("frequency_id")
        statutory_dates = data.get("statu_dates")
        repeats_type_id = data.get("r_type_id")
        repeats_every = data.get("r_every")
        duration_type_id = data.get("d_type_id")
        duration = data.get("duration")
        url = data.get("url")
        summary = data.get("summary")
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
            duration, url, summary
        )

    def to_structure(self):
        return {
            "country_name": self.country_name,
            "domain_name": self.domain_name,
            "industry_names": self.industry_names,
            "statutory_nature_name": self.statutory_nature_name,
            "geo_maps": self.geography_mappings,
            "approval_status_id": self.approval_status,
            "is_active": self.is_active,
            "act_name": self.act_name,
            "comp_id": self.compliance_id,
            "s_pro_map": self.statutory_provision,
            "c_task": self.compliance_task,
            "description": self.description,
            "p_consequences": self.penal_consequences,
            "frequency_id": self.frequency_id,
            "statu_dates": self.statutory_dates,
            "r_type_id": self.repeats_type_id,
            "r_every": self.repeats_every,
            "d_type_id": self.duration_type_id,
            "duration": self.duration,
            "url": self.url,
            "summary": self.summary

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
    def __init__(self, countries, geography_report):
        self.countries = countries
        self.geography_report = geography_report

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "geography_report"])
        countries = data.get("countries")
        geography_report = data.get("geography_report")
        return GetGeographyReportSuccess(countries, geography_report)

    def to_inner_structure(self):
        data = {
            "countries": self.countries,
            "geography_report": self.geography_report,
        }
        return data


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
        request = parse_VariantType(
            request, "knowledgereport", "Request"
        )
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": to_VariantType(
                self.request, "knowledgereport", "Response"
            )
        }

#
# GeographyMapping
#

class GeographyMapping(object):
    def __init__(self, country_id, geography_mapping, is_active):
        self.country_id = country_id
        self.geography_mapping = geography_mapping
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["country_id", "geography_mapping", "is_active"])
        country_id = data.get("country_id")
        geography_mapping = data.get("geography_mapping")
        is_active = data.get("is_active")
        return GeographyMapping(country_id, geography_mapping, is_active)

    def to_structure(self):
        data = {
            "country_id": self.country_id,
            "geography_mapping": self.geography_mapping,
            "is_active": self.is_active,
        }
        return data
