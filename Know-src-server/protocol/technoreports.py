from protocol.jsonvalidators import (
    parse_dictionary, parse_static_list,
    to_structure_dictionary_values, parse_VariantType, to_VariantType
)
# Request
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

class GetClientDetailsReportFilters(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetClientDetailsReportFilters()

    def to_inner_structure(self):
        return {
        }

class GetGroupAdminReportData(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetGroupAdminReportData()

    def to_inner_structure(self):
        return {
        }

class ExportGroupAdminReportData(Request):
    def __init__(self, client_id, country_id, csv):
        self.client_id = client_id
        self.country_id = country_id
        self.csv = csv

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["client_id", "country_id", "csv"])
        client_id = data.get("client_id")
        country_id = data.get("country_id")
        csv = data.get("csv")
        return ExportGroupAdminReportData(client_id, country_id, csv)

    def to_inner_staructure(self):
        return {
            "client_id": self.client_id,
            "country_id": self.country_id,
            "csv": self.csv
        }

class GetClientAgreementReportFilters(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetClientAgreementReportFilters()

    def to_inner_structure(self):
        return {
        }

class GetClientAgreementReportData(Request):
    def __init__(
        self, country_id, client_id, business_group_id, legal_entity_id, domain_id, contract_from, contract_to, csv, from_count, page_count, country_name):
        self.country_id = country_id
        self.client_id = client_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count
        self.country_name = country_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "client_id", "business_group_id", "legal_entity_id", "domain_id_optional", "contract_from_optional", "contract_to_optional", "csv", "from_count", "page_count", "country_name"
        ])
        country_id = data.get("country_id")
        client_id = data.get("client_id")
        business_group_id = data.get("business_group_id")
        legal_entity_id = data.get("legal_entity_id")
        domain_id = data.get("domain_id_optional")
        contract_from = data.get("contract_from_optional")
        contract_to = data.get("contract_to_optional")
        csv = data.get("csv")
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        country_name = data.get("country_name")

        return GetClientAgreementReportData(
            country_id, client_id, business_group_id, legal_entity_id, domain_id, contract_from, contract_to, csv, from_count, page_count, country_name
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "client_id": self.client_id,
            "business_group_id": self.business_group_id,
            "legal_entity_id": self.legal_entity_id,
            "domain_id_optional": self.domain_id_optional,
            "contract_from": self.contract_from,
            "contract_to": self.contract_to,
            "csv": self.csv,
            "from_count": self.from_count,
            "page_count": self.page_count,
            "country_name": self.country_name
        }

class GetDomainwiseAgreementReportData(Request):
    def __init__(
        self, country_id, client_id, business_group_id, legal_entity_id, domain_id, contract_from, contract_to, csv, from_count, page_count, country_name, domain_name
    ):
        self.country_id = country_id
        self.client_id = client_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count
        self.country_name = country_name
        self.domain_name = domain_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "client_id", "business_group_id", "legal_entity_id", "domain_id", "contract_from_optional", "contract_to_optional", "csv", "from_count", "page_count", "country_name", "domain_name"
        ])
        country_id = data.get("country_id")
        client_id = data.get("client_id")
        business_group_id = data.get("business_group_id")
        legal_entity_id = data.get("legal_entity_id")
        domain_id = data.get("domain_id")
        contract_from = data.get("contract_from_optional")
        contract_to = data.get("contract_to_optional")
        csv = data.get("csv")
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        country_name = data.get("country_name")
        domain_name = data.get("domain_name")

        return GetDomainwiseAgreementReportData(
            country_id, client_id, business_group_id, legal_entity_id, domain_id, contract_from, contract_to, csv, from_count, page_count, country_name, domain_name
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "client_id": self.client_id,
            "business_group_id": self.business_group_id,
            "legal_entity_id": self.legal_entity_id,
            "domain_id_optional": self.domain_id_optional,
            "contract_from": self.contract_from,
            "contract_to": self.contract_to,
            "csv": self.csv,
            "from_count": self.from_count,
            "page_count": self.page_count,
            "country_name": self.country_name,
            "domain_name": self.domain_name
        }

class GetOrganizationWiseUnitCount(Request):
    def __init__(
        self, legal_entity_id, domain_id
    ):
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "legal_entity_id", "domain_id"
        ])
        legal_entity_id = data.get("legal_entity_id")
        domain_id = data.get("domain_id")

        return GetOrganizationWiseUnitCount(
            legal_entity_id, domain_id
        )

    def to_inner_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id,
            "domain_id": self.domain_id,
        }

class GetStatutoryNotificationsFilters(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetStatutoryNotificationsFilters()

    def to_inner_structure(self):
        return {
        }

class GetStatutoryNotificationsReportData(Request):
    def __init__(
        self, country_id, domain_id, statutory_id_optional,
        from_date_optional, to_date_optional, from_count, page_count
    ):
        self.country_id = country_id
        self.domain_id = domain_id
        self.statutory_id_optional = statutory_id_optional
        self.from_date_optional = from_date_optional
        self.to_date_optional = to_date_optional
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "domain_id", "statutory_id_optional",
            "from_date_optional", "to_date_optional", "from_count", "page_count"
        ])
        country_id = data.get("country_id")
        domain_id = data.get("domain_id")
        statutory_id_optional = data.get("statutory_id_optional")
        from_date_optional = data.get("from_date_optional")
        to_date_optional = data.get("to_date_optional")
        from_count = data.get("from_count")
        page_count = data.get("page_count")

        return GetStatutoryNotificationsReportData(
            country_id, domain_id, statutory_id_optional,
            from_date_optional, to_date_optional, from_count, page_count
        )

    def to_inner_structure(self):
        return {
            "country_id" : self.country_id,
            "domain_id" : self.domain_id,
            "statutory_id_optional" : self.statutory_id_optional,
            "from_date_optional": self.from_date_optional,
            "to_date_optional": self.to_date_optional,
            "from_count": self.from_count,
            "page_count": self.page_count
        }

class GetAssignedStatutoryReportFilters(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetAssignedStatutoryReportFilters()

    def to_inner_structure(self):
        return {
        }

class GetAssignedStatutoryReport(Request):
    def __init__(self, country_id, domain_id_optional, group_id, business_group_id, legal_entity_id, map_text, unit_id, c_task, csv, from_count, page_count):
        self.country_id = country_id
        self.domain_id_optional = domain_id_optional
        self.group_id = group_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.map_text = map_text
        self.unit_id = unit_id
        self.c_task = c_task
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "c_id", "domain_id_optional", "client_id", "bg_id", "le_id",
            "map_text", "unit_id", "c_task", "csv", "from_count", "page_count"
        ])
        country_id = data.get("c_id")
        domain_id_optional = data.get("domain_id_optional")
        group_id = data.get("client_id")
        business_group_id = data.get("bg_id")
        legal_entity_id = data.get("le_id")
        map_text = data.get("map_text")
        unit_id = data.get("unit_id")
        c_task = data.get("c_task")
        csv = data.get("csv")
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        return GetAssignedStatutoryReport(
            country_id, domain_id_optional, group_id, business_group_id,
            legal_entity_id, map_text, unit_id, c_task, csv,
            from_count, page_count
        )

    def to_inner_structure(self):
        data = {
            "c_id": self.country_id,
            "domain_id_optional": self.domain_id_optional,
            "client_id": self.group_id,
            "bg_id": self.business_group_id,
            "le_id": self.legal_entity_id,
            "map_text": self.map_text,
            "unit_id": self.unit_id,
            "c_task": self.c_task,
            "csv": self.csv,
            "from_count": self.from_count,
            "page_count": self.page_count
        }
        return data


class GetComplianceTaskFilter(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetComplianceTaskFilter()

    def to_inner_structure(self):
        return {
        }

class GetUserMappingReportFilters(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetUserMappingReportFilters()

    def to_inner_structure(self):
        return {
        }

class GetUserMappingDetailsReportData(Request):
    def __init__(
        self, country_id, client_id, legal_entity_id, u_m_none, csv, from_count, page_count
    ):
        self.country_id = country_id
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.u_m_none = u_m_none
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "client_id", "legal_entity_id", "u_m_none", "csv", "from_count", "page_count"
        ])
        country_id = data.get("country_id")
        client_id = data.get("client_id")
        legal_entity_id = data.get("legal_entity_id")
        u_m_none = data.get("u_m_none")
        csv = data.get("csv")
        from_count = data.get("from_count")
        page_count = data.get("page_count")

        return GetUserMappingDetailsReportData(
            country_id, client_id, legal_entity_id, u_m_none, csv, from_count, page_count
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "client_id": self.client_id,
            "legal_entity_id": self.legal_entity_id,
            "u_m_none": self.u_m_none,
            "csv": self.csv,
            "from_count": self.from_count,
            "page_count": self.page_count
        }

class GetAssignedUserClientGroups(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetAssignedUserClientGroups()

    def to_inner_structure(self):
        return {
        }

class GetReassignUserReportData(Request):
    def __init__(self, user_category_id, user_id, group_id_none):
        self.user_category_id = user_category_id
        self.user_id = user_id
        self. group_id_none = group_id_none

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "user_category_id", "user_id", "group_id_none"
        ])
        user_category_id = data.get("user_category_id")
        user_id = data.get("user_id")
        group_id_none = data.get("group_id_none")
        return GetReassignUserReportData(
            user_category_id, user_id, group_id_none
        )

    def to_inner_structure(self):
        data = {
            "user_category_id": self.user_category_id,
            "user_id": self.user_id,
            "group_id_none": self.group_id_none,
        }
        return data

class ExportReassignUserReportData(Request):
    def __init__(self, user_category_id, user_id, group_id_none, u_m_none, csv):
        self.user_category_id = user_category_id
        self.user_id = user_id
        self. group_id_none = group_id_none
        self.u_m_none = u_m_none
        self.csv = csv

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "user_category_id", "user_id", "group_id_none", "u_m_none", "csv"
        ])
        user_category_id = data.get("user_category_id")
        user_id = data.get("user_id")
        group_id_none = data.get("group_id_none")
        u_m_none = data.get("u_m_none")
        csv = data.get("csv")
        return ExportReassignUserReportData(
            user_category_id, user_id, group_id_none, u_m_none, csv
        )

    def to_inner_structure(self):
        data = {
            "user_category_id": self.user_category_id,
            "user_id": self.user_id,
            "group_id_none": self.group_id_none,
            "u_m_none": self.u_m_none,
            "csv": self.csv
        }
        return data

class GetAssignedStatutoriesList(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetAssignedStatutoriesList()

    def to_inner_structure(self):
        return {
        }

class GetReassignUserDomainReportData(Request):
    def __init__(self, user_category_id, user_id, group_id_none, bg_id, le_id, d_id):
        self.user_category_id = user_category_id
        self.user_id = user_id
        self. group_id_none = group_id_none
        self.bg_id = bg_id
        self.le_id = le_id
        self.d_id = d_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "user_category_id", "user_id", "group_id_none", "bg_id", "le_id", "d_id"
        ])
        user_category_id = data.get("user_category_id")
        user_id = data.get("user_id")
        group_id_none = data.get("group_id_none")
        bg_id = data.get("bg_id")
        le_id = data.get("le_id")
        d_id = data.get("d_id")
        return GetReassignUserDomainReportData(
            user_category_id, user_id, group_id_none, bg_id, le_id, d_id
        )

    def to_inner_structure(self):
        data = {
            "user_category_id": self.user_category_id,
            "user_id": self.user_id,
            "group_id_none": self.group_id_none,
            "bg_id": self.bg_id,
            "le_id": self.le_id,
            "d_id": self.d_id,
        }
        return data

class GetComplianceStatutoriesList(Request):
    def __init__(self, unit_id, d_id):
        self.unit_id = unit_id
        self.d_id = d_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["unit_id", "d_id"])
        unit_id = data.get("unit_id")
        d_id = data.get("d_id")

        return GetComplianceStatutoriesList(unit_id, d_id)

    def to_inner_structure(self):
        data = {
            "unit_id": self.unit_id,
            "d_id": self.d_id,
        }
        return data

class ExportClientDetailsReportData(Request):
    def __init__(
        self, country_id, client_id, legal_entity_id, u_m_none, csv
    ):
        self.country_id = country_id
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.u_m_none = u_m_none
        self.csv = csv

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "client_id", "legal_entity_id", "u_m_none", "csv"
        ])
        country_id = data.get("country_id")
        client_id = data.get("client_id")
        legal_entity_id = data.get("legal_entity_id")
        u_m_none = data.get("u_m_none")
        csv = data.get("csv")

        return ExportClientDetailsReportData(
            country_id, client_id, legal_entity_id, u_m_none, csv
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "client_id": self.client_id,
            "legal_entity_id": self.legal_entity_id,
            "u_m_none": self.u_m_none,
            "csv": self.csv,
        }

class GetClientDetailsReportData(Request):
    def __init__(
        self, country_id, client_id, legal_entity_id, u_m_none
    ):
        self.country_id = country_id
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.u_m_none = u_m_none

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "client_id", "legal_entity_id", "u_m_none"
        ])
        country_id = data.get("country_id")
        client_id = data.get("client_id")
        legal_entity_id = data.get("legal_entity_id")
        u_m_none = data.get("u_m_none")

        return GetClientDetailsReportData(
            country_id, client_id, legal_entity_id, u_m_none
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "client_id": self.client_id,
            "legal_entity_id": self.legal_entity_id,
            "u_m_none": self.u_m_none,
        }

def _init_Request_class_map():
    classes = [
        GetClientDetailsReportFilters,
        GetClientDetailsReportData,
        GetStatutoryNotificationsFilters,
        GetStatutoryNotificationsReportData,
        GetAssignedStatutoryReportFilters,
        GetAssignedStatutoryReport,
        GetComplianceTaskFilter,
        GetClientAgreementReportFilters,
        GetClientAgreementReportData,
        GetDomainwiseAgreementReportData,
        GetOrganizationWiseUnitCount,
        GetUserMappingReportFilters,
        GetUserMappingDetailsReportData,
        GetGroupAdminReportData,
        GetAssignedUserClientGroups,
        GetReassignUserReportData,
        GetReassignUserDomainReportData,
        GetAssignedStatutoriesList,
        GetComplianceStatutoriesList,
        ExportClientDetailsReportData,
        ExportReassignUserReportData,
        ExportGroupAdminReportData
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

class GetClientDetailsReportFiltersSuccess(Response):
    def __init__(self, countries, domains_organization_list, statutory_groups, statutory_business_groups, units_report, industry_name_id):
        self.countries = countries
        self.domains_organization_list = domains_organization_list
        self.statutory_groups = statutory_groups
        self.statutory_business_groups = statutory_business_groups
        self.units_report = units_report
        self.industry_name_id = industry_name_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains_organization_list", "statutory_groups", "statutory_business_groups", "units_report", "industry_name_id"])
        countries = data.get("countries")
        domains_organization_list = data.get("domains_organization_list")
        statutory_groups = data.get("statutory_groups")
        statutory_business_groups = data.get("statutory_business_groups")
        units_report = data.get("units_report")
        industry_name_id = data.get("industry_name_id")
        return GetClientDetailsReportFiltersSuccess(countries, domains_organization_list, statutory_groups, statutory_business_groups, units_report, industry_name_id)

    def to_inner_structure(self):
        data = {
            "countries": self.countries,
            "domains_organization_list": self.domains_organization_list,
            "statutory_groups": self.statutory_groups,
            "statutory_business_groups": self.statutory_business_groups,
            "units_report": self.units_report,
            "industry_name_id": self.industry_name_id,
        }
        return data

class GetClientDetailsReportDataSuccess(Response):
    def __init__(self, units_list):
        self.units_list = units_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["units_list"])
        units_list = data.get("units_list")
        return GetClientDetailsReportDataSuccess(units_list)

    def to_inner_structure(self):
        return {
            "units_list": self.units_list
        }

class GetStatutoryNotificationsFiltersSuccess(Response):
    def __init__(self, countries, domains, level_one_statutories):
        self.countries = countries
        self.domains = domains
        self.level_one_statutories = level_one_statutories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "level_one_statutories"])
        countries = data.get("countries")
        domains = data.get("domains")
        level_one_statutories = data.get("level_one_statutories")
        return GetStatutoryNotificationsFiltersSuccess(countries, domains, level_one_statutories)

    def to_inner_structure(self):
        return {
            "countries": self.countries,
            "domains": self.domains,
            "level_one_statutories": self.level_one_statutories
        }

class GetStatutoryNotificationsReportDataSuccess(Response):
    def __init__(self, statutory_notifictions_list, total_count):
        self.statutory_notifictions_list = statutory_notifictions_list
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutory_notifictions_list"])
        statutory_notifictions_list = data.get("statutory_notifictions_list")
        total_count = data.get("total_count")

        return GetStatutoryNotificationsReportDataSuccess(statutory_notifictions_list, total_count)

    def to_inner_structure(self):
        return {
            "statutory_notifictions_list": self.statutory_notifictions_list,
            "total_count": self.total_count
        }

class GetAssignedStatutoryReportFiltersSuccess(Response):
    def __init__(self, countries, domains, statutory_groups, statutory_business_groups, statutory_units, statutory_compliances):
        self.countries = countries
        self.domains = domains
        self.statutory_groups = statutory_groups
        self.statutory_business_groups = statutory_business_groups
        self.statutory_units = statutory_units
        self.statutory_compliances = statutory_compliances

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "statutory_groups", "statutory_business_groups", "statutory_units", "statutory_compliances"])
        countries = data.get("countries")
        domains = data.get("domains")
        statutory_groups = data.get("statutory_groups")
        statutory_business_groups = data.get("statutory_business_groups")
        statutory_units = data.get("statutory_units")
        statutory_compliances = data.get("statutory_compliances")
        return GetAssignedStatutoryReportFiltersSuccess(countries, domains, statutory_groups, statutory_business_groups, statutory_units, statutory_compliances)

    def to_inner_structure(self):
        data = {
            "countries": self.countries,
            "domains": self.domains,
            "statutory_groups": self.statutory_groups,
            "statutory_business_groups": self.statutory_business_groups,
            "statutory_units": self.statutory_units,
            "statutory_compliances": self.statutory_compliances,
        }
        return data

class GetAssignedStatutoryReportSuccess(Response):
    def __init__(self, unit_groups, act_groups, compliance_statutories_list, total_count):
        self.unit_groups = unit_groups
        self.act_groups = act_groups
        self.compliance_statutories_list = compliance_statutories_list
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["unit_groups", "act_groups", "compliance_statutories_list", "total_count"])
        unit_groups = data.get("unit_groups")
        act_groups = data.get("act_groups")
        compliance_statutories_list = data.get("compliance_statutories_list")
        total_count = data.get("total_count")
        return GetAssignedStatutoryReportSuccess(unit_groups, act_groups, compliance_statutories_list, total_count)

    def to_inner_structure(self):
        data = {
            "unit_groups": self.unit_groups,
            "act_groups": self.act_groups,
            "compliance_statutories_list": self.compliance_statutories_list,
            "total_count": self.total_count
        }
        return data

# user mapping report - filter success

class GetUserMappingReportFiltersSuccess(Response):
    def __init__(self, countries, usermapping_groupdetails, usermapping_business_groups, usermapping_legal_entities, usermapping_unit):
        self.countries = countries
        self.usermapping_groupdetails = usermapping_groupdetails
        self.usermapping_business_groups = usermapping_business_groups
        self.usermapping_legal_entities = usermapping_legal_entities
        self.usermapping_unit = usermapping_unit

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "usermapping_groupdetails", "usermapping_business_groups", "usermapping_legal_entities", "usermapping_unit"])
        countries = data.get("countries")
        usermapping_groupdetails = data.get("usermapping_groupdetails")
        usermapping_business_groups = data.get("usermapping_business_groups")
        usermapping_legal_entities = data.get("usermapping_legal_entities")
        usermapping_unit = data.get("usermapping_unit")
        return GetUserMappingReportFiltersSuccess(countries, usermapping_groupdetails, usermapping_business_groups, usermapping_legal_entities, usermapping_unit)

    def to_inner_structure(self):
        data = {
            "countries": self.countries,
            "usermapping_groupdetails": self.usermapping_groupdetails,
            "usermapping_business_groups": self.usermapping_business_groups,
            "usermapping_legal_entities": self.usermapping_legal_entities,
            "usermapping_unit": self.usermapping_unit,
        }
        return data

# user mapping report - filter success

class GetUserMappingReportDataSuccess(Response):
    def __init__(self, techno_details, unit_domains, usermapping_domain, total_count):
        self.techno_details = techno_details
        self.unit_domains = unit_domains
        self.usermapping_domain = usermapping_domain
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["techno_details", "unit_domains", "usermapping_domain", "total_count"])
        techno_details = data.get("techno_details")
        unit_domains = data.get("unit_domains")
        usermapping_domain = data.get("usermapping_domain")
        total_count = data.get("total_count")
        return GetUserMappingReportDataSuccess(techno_details, unit_domains, usermapping_domain, total_count)

    def to_inner_structure(self):
        data = {
            "techno_details": self.techno_details,
            "unit_domains": self.unit_domains,
            "usermapping_domain": self.usermapping_domain,
            "total_count": self.total_count,
        }
        return data

class GetClientAgreementReportFiltersSuccess(Response):
    def __init__(self, countries, domains, groups, business_groups, unit_legal_entity):
        self.countries = countries
        self.domains = domains
        self.groups = groups
        self.business_groups = business_groups
        self.unit_legal_entity = unit_legal_entity

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "groups", "business_groups", "unit_legal_entity"])
        countries = data.get("countries")
        domains = data.get("domains")
        groups = data.get("client_group_master")
        business_groups = data.get("business_groups")
        unit_legal_entity = data.get("unit_legal_entity")

        return GetClientAgreementReportFiltersSuccess(countries, domains, groups, business_groups, unit_legal_entity)

    def to_inner_structure(self):
        return {
            "countries": self.countries,
            "domains": self.domains,
            "client_group_master": self.groups,
            "business_groups": self.business_groups,
            "unit_legal_entity": self.unit_legal_entity
        }

class GetClientAgreementReportDataSuccess(Response):
    def __init__(self, client_agreement_list, total_count):
        self.client_agreement_list = client_agreement_list
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["client_agreement_list", "total_count"])
        client_agreement_list = data.get("client_agreement_list")
        total_count = data.get("total_count")
        return GetClientAgreementReportDataSuccess(client_agreement_list, total_count)

    def to_inner_structure(self):
        return {
            "client_agreement_list": self.client_agreement_list,
            "total_count": self.total_count
        }

class GetDomainwiseAgreementReportDataSuccess(Response):
    def __init__(self, domainwise_agreement_list, total_count):
        self.domainwise_agreement_list = domainwise_agreement_list
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domainwise_agreement_list", "total_count"])
        domainwise_agreement_list = data.get("domainwise_agreement_list")
        total_count = data.get("total_count")
        return GetDomainwiseAgreementReportDataSuccess(domainwise_agreement_list, total_count)

    def to_inner_structure(self):
        return {
            "domainwise_agreement_list": self.domainwise_agreement_list,
            "total_count": self.total_count
        }

class GetOrganizationWiseUnitCountSuccess(Response):
    def __init__(self, organizationwise_unit_count_list):
        self.organizationwise_unit_count_list = organizationwise_unit_count_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["organizationwise_unit_count_list"])
        organizationwise_unit_count_list = data.get("organizationwise_unit_count_list")
        return GetOrganizationWiseUnitCountSuccess(organizationwise_unit_count_list)

    def to_inner_structure(self):
        return {
            "organizationwise_unit_count_list": self.organizationwise_unit_count_list
        }

class ExportToCSVSuccess(Response):
    def __init__(self, link):
        self.link = link

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["link"])
        link = data.get("link")
        return ExportToCSVSuccess(link)

    def to_inner_structure(self):
        return {
            "link" : self.link
        }

class GetGroupAdminReportDataSuccess(Response):
    def __init__(self, groupadmin_clients, group_admin_countries, group_admin_list):
        self.groupadmin_clients = groupadmin_clients
        self.group_admin_countries = group_admin_countries
        self.group_admin_list = group_admin_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["groupadmin_clients", "group_admin_countries", "group_admin_list"])
        groupadmin_clients = data.get("groupadmin_clients")
        group_admin_countries = data.get("group_admin_countries")
        group_admin_list = data.get("group_admin_list")
        return GetGroupAdminReportDataSuccess(groupadmin_clients, group_admin_countries, group_admin_list)

    def to_inner_structure(self):
        data = {
            "groupadmin_clients": self.groupadmin_clients,
            "group_admin_countries": self.group_admin_countries,
            "group_admin_list": self.group_admin_list,
        }
        return data

class GetAssignedUserClientGroupsSuccess(Response):
    def __init__(self, user_categories, reassign_user_clients, clients, reassign_domains):
        self.user_categories = user_categories
        self.reassign_user_clients = reassign_user_clients
        self.clients = clients
        self.reassign_domains = reassign_domains

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_categories", "reassign_user_clients", "clients", "reassign_domains"])
        user_categories = data.get("user_categories")
        reassign_user_clients = data.get("reassign_user_clients")
        clients = data.get("clients")
        reassign_domains = data.get("reassign_domains")
        return GetAssignedUserClientGroupsSuccess(user_categories, reassign_user_clients, clients, reassign_domains)

    def to_inner_structure(self):
        data = {
            "user_categories": self.user_categories,
            "reassign_user_clients": self.reassign_user_clients,
            "clients": self.clients,
            "reassign_domains": self.reassign_domains,
        }
        return data

class ReassignUserReportDataSuccess(Response):
    def __init__(self, reassign_user_list):
        self.reassign_user_list = reassign_user_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["reassign_user_list"])
        reassign_user_list = data.get("reassign_user_list")
        return ReassignUserReportDataSuccess(reassign_user_list)

    def to_inner_structure(self):
        data = {
            "reassign_user_list": self.reassign_user_list,
        }
        return data

class ReassignUserDomainReportDataSuccess(Response):
    def __init__(self, reassign_domains_list):
        self.reassign_domains_list = reassign_domains_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["reassign_domains_list"])
        reassign_domains_list = data.get("reassign_domains_list")
        return ReassignUserDomainReportDataSuccess(reassign_domains_list)

    def to_inner_structure(self):
        data = {
            "reassign_domains_list": self.reassign_domains_list,
        }
        return data

class ApproveAssignedStatutoriesListSuccess(Response):
    def __init__(self, approve_assigned_statutories):
        self.approve_assigned_statutories = approve_assigned_statutories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["approve_assigned_statutories"])
        approve_assigned_statutories = data.get("approve_assigned_statutories")
        return ApproveAssignedStatutoriesListSuccess(approve_assigned_statutories)

    def to_inner_structure(self):
        data = {
            "approve_assigned_statutories": self.approve_assigned_statutories,
        }
        return data

class ExportToCSVEmpty(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ExportToCSVEmpty()

    def to_inner_structure(self):
        return {
        }

def _init_Response_class_map():
    classes = [
                GetClientDetailsReportFiltersSuccess, GetClientDetailsReportDataSuccess, GetStatutoryNotificationsFiltersSuccess,
                GetStatutoryNotificationsReportDataSuccess, GetAssignedStatutoryReportFiltersSuccess, GetAssignedStatutoryReportSuccess,
                GetClientAgreementReportFiltersSuccess, GetClientAgreementReportDataSuccess, GetDomainwiseAgreementReportDataSuccess,
                GetOrganizationWiseUnitCountSuccess, ExportToCSVSuccess, GetUserMappingReportFiltersSuccess, GetUserMappingReportDataSuccess,
                GetGroupAdminReportDataSuccess, GetAssignedUserClientGroupsSuccess, ReassignUserReportDataSuccess,
                ReassignUserDomainReportDataSuccess, ApproveAssignedStatutoriesListSuccess, ExportToCSVEmpty
            ]

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
            request, "technoreports", "Request"
        )
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request":  to_VariantType(
                self.request, "technoreports", "Request"
            )
        }

#
# UNIT_WISE_ASSIGNED_STATUTORIES
#

class ClientAgreementList(object):
    def __init__(
        self, legal_entity_id, domain_id, legal_entity_name, total_licence, used_licence, file_space, used_file_space,
        contract_from, contract_to, group_name, group_admin_email, is_closed, domain_count,
        d_name, domain_total_unit, activation_date, domain_used_unit, legal_entity_admin_contactno,
        legal_entity_admin_email, business_group_name
    ):
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.legal_entity_name = legal_entity_name
        self.total_licence = total_licence
        self.used_licence = used_licence
        self.file_space = file_space
        self.used_file_space = used_file_space
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.group_name = group_name
        self.group_admin_email = group_admin_email
        self.is_closed = is_closed
        self.domain_count = domain_count
        self.d_name = d_name
        self.domain_total_unit = domain_total_unit
        self.activation_date = activation_date
        self.domain_used_unit = domain_used_unit
        self.legal_entity_admin_contactno = legal_entity_admin_contactno
        self.legal_entity_admin_email = legal_entity_admin_email
        self.business_group_name = business_group_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "legal_entity_id",
                "domain_id",
                "legal_entity_name",
                "total_licence",
                "used_licence",
                "file_space",
                "used_file_space",
                "contract_from",
                "contract_to",
                "group_name",
                "group_admin_email",
                "is_closed",
                "domain_count",
                "d_name",
                "domain_total_unit",
                "activation_date",
                "domain_used_unit",
                "legal_entity_admin_contactno",
                "legal_entity_admin_email",
                "business_group_name"
                ]
        )

        legal_entity_id = data.get("legal_entity_id"),
        domain_id = data.get("domain_id"),
        legal_entity_name = data.get("legal_entity_name"),
        total_licence = data.get("total_licence"),
        used_licence = data.get("used_licence"),
        file_space = data.get("file_space"),
        used_file_space = data.get("used_file_space"),
        contract_from = data.get("contract_from"),
        contract_to = data.get("contract_to"),
        group_name = data.get("group_name"),
        group_admin_email = data.get("group_admin_email"),
        is_closed = data.get("is_closed"),
        domain_count = data.get("domain_count"),
        d_name = data.get("d_name"),
        domain_total_unit = data.get("domain_total_unit"),
        activation_date = data.get("activation_date"),
        domain_used_unit = data.get("domain_used_unit"),
        legal_entity_admin_contactno = data.get("legal_entity_admin_contactno"),
        legal_entity_admin_email = data.get("legal_entity_admin_email"),
        business_group_name = data.get("business_group_name")

        return ClientAgreementList(
            legal_entity_id, domain_id, legal_entity_name, total_licence, used_licence, file_space,
            used_file_space,
            contract_from, contract_to, group_name, group_admin_email, is_closed, domain_count,
            d_name, domain_total_unit, activation_date, domain_used_unit, legal_entity_admin_contactno,
            legal_entity_admin_email, business_group_name
        )

    def to_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id,
            "domain_id": self.domain_id,
            "legal_entity_name": self.legal_entity_name,
            "total_licence": self.total_licence,
            "used_licence": self.used_licence,
            "file_space": self.file_space,
            "used_file_space": self.used_file_space,
            "contract_from": self.contract_from,
            "contract_to": self.contract_to,
            "group_name": self.group_name,
            "group_admin_email": self.group_admin_email,
            "is_closed": self.is_closed,
            "domain_count": self.domain_count,
            "d_name": self.d_name,
            "domain_total_unit": self.domain_total_unit,
            "activation_date": self.activation_date,
            "domain_used_unit": self.domain_used_unit,
            "legal_entity_admin_contactno": self.legal_entity_admin_contactno,
            "legal_entity_admin_email": self.legal_entity_admin_email,
            "business_group_name": self.business_group_name
        }

class DomainwiseAgreementList(object):
    def __init__(
        self, legal_entity_id, domain_id, legal_entity_name,
        contract_from, contract_to, group_name, group_admin_email,
        domain_total_unit, activation_date, domain_used_unit, legal_entity_admin_contactno,
        legal_entity_admin_email, business_group_name
    ):
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.legal_entity_name = legal_entity_name
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.group_name = group_name
        self.group_admin_email = group_admin_email
        self.domain_total_unit = domain_total_unit
        self.activation_date = activation_date
        self.domain_used_unit = domain_used_unit
        self.legal_entity_admin_contactno = legal_entity_admin_contactno
        self.legal_entity_admin_email = legal_entity_admin_email
        self.business_group_name = business_group_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "legal_entity_id",
                "domain_id",
                "legal_entity_name",
                "contract_from",
                "contract_to",
                "group_name",
                "group_admin_email",
                "domain_total_unit",
                "activation_date",
                "domain_used_unit",
                "legal_entity_admin_contactno",
                "legal_entity_admin_email",
                "business_group_name"
            ]
        )

        legal_entity_id = data.get("legal_entity_id"),
        domain_id = data.get("domain_id"),
        legal_entity_name = data.get("legal_entity_name"),
        contract_from = data.get("contract_from"),
        contract_to = data.get("contract_to"),
        group_name = data.get("group_name"),
        group_admin_email = data.get("group_admin_email"),
        domain_total_unit = data.get("domain_total_unit"),
        activation_date = data.get("activation_date"),
        domain_used_unit = data.get("domain_used_unit"),
        legal_entity_admin_contactno = data.get("legal_entity_admin_contactno"),
        legal_entity_admin_email = data.get("legal_entity_admin_email"),
        business_group_name = data.get("business_group_name")

        return DomainwiseAgreementList(
            legal_entity_id, domain_id, legal_entity_name,
            contract_from, contract_to, group_name, group_admin_email,
            domain_total_unit, activation_date, domain_used_unit, legal_entity_admin_contactno,
            legal_entity_admin_email, business_group_name
        )

    def to_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id,
            "domain_id": self.domain_id,
            "legal_entity_name": self.legal_entity_name,
            "contract_from": self.contract_from,
            "contract_to": self.contract_to,
            "group_name": self.group_name,
            "group_admin_email": self.group_admin_email,
            "domain_total_unit": self.domain_total_unit,
            "activation_date": self.activation_date,
            "domain_used_unit": self.domain_used_unit,
            "legal_entity_admin_contactno": self.legal_entity_admin_contactno,
            "legal_entity_admin_email": self.legal_entity_admin_email,
            "business_group_name": self.business_group_name
        }

class OrganizationwiseUnitCountList(object):
    def __init__(
        self, domain_name, organization_name,
        domain_total_unit, domain_used_unit
    ):
        self.domain_name = domain_name
        self.organization_name = organization_name
        self.domain_total_unit = domain_total_unit
        self.domain_used_unit = domain_used_unit

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "domain_name",
                "organization_name",
                "domain_total_unit",
                "domain_used_unit"
            ]
        )

        domain_name = data.get("domain_name"),
        organization_name = data.get("organization_name"),
        domain_total_unit = data.get("domain_total_unit"),
        domain_used_unit = data.get("domain_used_unit")

        return OrganizationwiseUnitCountList(
            domain_name, organization_name,
            domain_total_unit, domain_used_unit
        )

    def to_structure(self):
        return {
            "domain_name": self.domain_name,
            "organization_name": self.organization_name,
            "domain_total_unit": self.domain_total_unit,
            "domain_used_unit": self.domain_used_unit
        }

#
# Statutory setting report
#

class ClientGroup(object):
    def __init__(self, country_id, client_id, short_name, is_active):
        self.country_id = country_id
        self.client_id = client_id
        self.short_name = short_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["country_id", "client_id", "short_name", "is_active"])
        country_id = data.get("country_id")
        client_id = data.get("client_id")
        short_name = data.get("short_name")
        is_active = data.get("is_active")
        return ClientGroup(country_id, client_id, short_name, is_active)

    def to_structure(self):
        data = {
            "country_id": self.country_id,
            "client_id": self.client_id,
            "short_name": self.short_name,
            "is_active": self.is_active,
        }
        return data

class ClientBusinessGroup(object):
    def __init__(self, client_id, legal_entity_id, legal_entity_name, business_group_id, business_group_name, country_id):
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.business_group_id = business_group_id
        self.business_group_name = business_group_name
        self.country_id = country_id

    @staticmethod
    def parse_structure(data):

        data = parse_dictionary(data, ["client_id", "legal_entity_id", "legal_entity_name", "business_group_id", "business_group_name", "country_id"])
        client_id = data.get("client_id")
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_name = data.get("legal_entity_name")
        business_group_id = data.get("business_group_id")
        business_group_name = data.get("business_group_name")
        country_id = data.get("country_id")
        return ClientBusinessGroup(client_id, legal_entity_id, legal_entity_name, business_group_id, business_group_name, country_id)

    def to_structure(self):
        data = {
            "client_id": self.client_id,
            "legal_entity_id": self.legal_entity_id,
            "legal_entity_name": self.legal_entity_name,
            "business_group_id": self.business_group_id,
            "business_group_name": self.business_group_name,
            "country_id": self.country_id
        }
        return data

class ComplianceUnits(object):
    def __init__(self, client_id, legal_entity_id, unit_id, unit_code, unit_name):
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.unit_id = unit_id
        self.unit_code = unit_code
        self.unit_name = unit_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["client_id", "legal_entity_id", "unit_id", "unit_code", "unit_name"])
        client_id = data.get("client_id")
        legal_entity_id = data.get("legal_entity_id")
        unit_id = data.get("unit_id")
        unit_code = data.get("unit_code")
        unit_name = data.get("unit_name")
        return ComplianceUnits(client_id, legal_entity_id, unit_id, unit_code, unit_name)

    def to_structure(self):
        data = {
            "client_id": self.client_id,
            "legal_entity_id": self.legal_entity_id,
            "unit_id": self.unit_id,
            "unit_code": self.unit_code,
            "unit_name": self.unit_name,
        }
        return data

class ComplianceStatutory(object):
    def __init__(self, client_id, legal_entity_id, unit_id, domain_id, statutory_id, compliance_id, c_task, document_name, statutory_name):
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.unit_id = unit_id
        self.domain_id = domain_id
        self.statutory_id = statutory_id
        self.compliance_id = compliance_id
        self.c_task = c_task
        self.document_name = document_name
        self.statutory_name = statutory_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["client_id", "legal_entity_id", "unit_id", "domain_id", "statutory_id", "compliance_id", "c_task", "document_name", "statutory_name"])
        client_id = data.get("client_id")
        legal_entity_id = data.get("legal_entity_id")
        unit_id = data.get("unit_id")
        domain_id = data.get("domain_id")
        statutory_id = data.get("statutory_id")
        compliance_id = data.get("compliance_id")
        c_task = data.get("c_task")
        document_name = data.get("document_name")
        statutory_name = data.get("statutory_name")
        return ComplianceStatutory(client_id, legal_entity_id, unit_id, domain_id, statutory_id, compliance_id, c_task, document_name, statutory_name)

    def to_structure(self):
        data = {
            "client_id": self.client_id,
            "legal_entity_id": self.legal_entity_id,
            "unit_id": self.unit_id,
            "domain_id": self.domain_id,
            "statutory_id": self.statutory_id,
            "compliance_id": self.compliance_id,
            "c_task": self.c_task,
            "document_name": self.document_name,
            "statutory_name": self.statutory_name,
        }
        return data

class StatutorySettingUnitGroup(object):
    def __init__(self, unit_id, unit_code, unit_name, address):
        self.unit_id = unit_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.address = address

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_id", "unit_code", "unit_name", "address"])
        unit_id = data.get("unit_id")
        unit_code = data.get("unit_code")
        unit_name = data.get("unit_name")
        address = data.get("address")
        return ComplianceStatutory(unit_id, unit_code, unit_name, address)

    def to_structure(self):
        data = {
            "unit_id": self.unit_id,
            "unit_code": self.unit_code,
            "unit_name": self.unit_name,
            "address": self.address,
        }
        return data

class StatutorySettingActGroup(object):
    def __init__(self, unit_id, statutory_id, map_text):
        self.unit_id = unit_id
        self.statutory_id = statutory_id
        self.map_text = map_text

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_id", "statutory_id", "map_text"])
        unit_id = data.get("unit_id")
        statutory_id = data.get("statutory_id")
        map_text = data.get("map_text")
        return ComplianceStatutory(unit_id, statutory_id, map_text)

    def to_structure(self):
        data = {
            "unit_id": self.unit_id,
            "statutory_id": self.statutory_id,
            "map_text": self.map_text,
        }
        return data

class StatutorySettingCompliances(object):
    def __init__(self, unit_id, statutory_mapping_id, statutory_provision, c_task, document_name, remarks, statutory_applicability_status, statutory_opted_status, compfie_admin, admin_update, client_admin, client_update, statutory_nature_name):
        self.unit_id = unit_id
        self.statutory_mapping_id = statutory_mapping_id
        self.statutory_provision = statutory_provision
        self.c_task = c_task
        self.document_name = document_name
        self.remarks = remarks
        self.statutory_applicability_status = statutory_applicability_status
        self.statutory_opted_status = statutory_opted_status
        self.compfie_admin = compfie_admin
        self.admin_update = admin_update
        self.client_admin = client_admin
        self.client_update = client_update
        self.statutory_nature_name = statutory_nature_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_id", "statutory_mapping_id", "statutory_provision", "c_task", "document_name", "remarks", "statutory_applicability_status", "statutory_opted_status", "compfie_admin", "admin_update", "client_admin", "client_update", "statutory_nature_name"])
        unit_id = data.get("unit_id")
        statutory_mapping_id = data.get("statutory_mapping_id")
        statutory_provision = data.get("statutory_provision")
        c_task = data.get("c_task")
        document_name = data.get("document_name")
        remarks = data.get("remarks")
        statutory_applicability_status = data.get("statutory_applicability_status")
        statutory_opted_status = data.get("statutory_opted_status")
        compfie_admin = data.get("compfie_admin")
        admin_update = data.get("admin_update")
        client_admin = data.get("client_admin")
        client_update = data.get("client_update")
        statutory_nature_name = data.get("statutory_nature_name")
        return ComplianceStatutory(unit_id, statutory_mapping_id, statutory_provision, c_task, document_name, remarks, statutory_applicability_status, statutory_opted_status, compfie_admin, admin_update, client_admin, client_update, statutory_nature_name)

    def to_structure(self):
        data = {
            "unit_id": self.unit_id,
            "statutory_mapping_id": self.statutory_mapping_id,
            "statutory_provision": self.statutory_provision,
            "c_task": self.c_task,
            "document_name": self.document_name,
            "remarks": self.remarks,
            "statutory_applicability_status": self.statutory_applicability_status,
            "statutory_opted_status": self.statutory_opted_status,
            "compfie_admin": self.compfie_admin,
            "admin_update": self.admin_update,
            "client_admin": self.client_admin,
            "client_update": self.client_update,
            "statutory_nature_name": self.statutory_nature_name
        }
        return data

#
# Domain
#

class UserMappingDomain(object):
    def __init__(
        self, domain_id, domain_name, is_active
    ):
        self.domain_id = domain_id
        self.domain_name = domain_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "domain_id", "domain_name", "is_active"
        ])
        domain_id = data.get("domain_id")
        domain_name = data.get("domain_name")
        is_active = data.get("is_active")
        return UserMappingDomain(
            domain_id, domain_name, is_active
        )

    def to_structure(self):
        data = {
            "domain_id": self.domain_id,
            "domain_name": self.domain_name,
            "is_active": self.is_active,
        }
        return to_structure_dictionary_values(data)

#
# Domain
#

class ClientUnitDetailsReport(object):
    def __init__(
        self, country_id, client_id, legal_entity_id, business_group_id, unit_id, unit_code,
        unit_name, address, postal_code, is_active, closed_on, check_date, emp_code_name,
        created_on, division_name, category_name, d_ids, i_ids
    ):
        self.country_id = country_id
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id
        self.unit_id = unit_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.address = address
        self.postal_code = postal_code
        self.is_active = is_active
        self.closed_on = closed_on
        self.check_date = check_date
        self.emp_code_name = emp_code_name
        self.created_on = created_on
        self.division_name = division_name
        self.category_name = category_name
        self.d_ids = d_ids
        self.i_ids = i_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "country_id", "client_id", "legal_entity_id", "business_group_id", "unit_id", "unit_code",
            "unit_name", "address", "postal_code", "is_active", "closed_on", "check_date", "emp_code_name",
            "created_on", "division_name", "category_name", "d_ids", "i_ids"
        ])
        country_id = data.get("country_id")
        client_id = data.get("client_id")
        legal_entity_id = data.get("legal_entity_id")
        business_group_id = data.get("business_group_id")
        unit_id = data.get("unit_id")
        unit_code = data.get("unit_code")
        unit_name = data.get("unit_name")
        address = data.get("address")
        postal_code = data.get("postal_code")
        is_active = data.get("is_active")
        closed_on = data.get("closed_on")
        check_date = data.get("check_date")
        emp_code_name = data.get("emp_code_name")
        created_on = data.get("created_on")
        division_name = data.get("division_name")
        category_name = data.get("category_name")
        d_ids = data.get("d_ids")
        i_ids = data.get("i_ids")
        return ClientUnitDetailsReport(
            country_id, client_id, legal_entity_id, business_group_id, unit_id, unit_code,
            unit_name, address, postal_code, is_active, closed_on, check_date, emp_code_name,
            created_on, division_name, category_name, d_ids, i_ids
        )

    def to_structure(self):
        data = {
            "country_id": self.country_id,
            "client_id": self.client_id,
            "legal_entity_id": self.legal_entity_id,
            "business_group_id": self.business_group_id,
            "unit_id": self.unit_id,
            "unit_code": self.unit_code,
            "unit_name": self.unit_name,
            "address": self.address,
            "postal_code": self.postal_code,
            "is_active": self.is_active,
            "closed_on": self.closed_on,
            "check_date": self.check_date,
            "emp_code_name": self.emp_code_name,
            "created_on": self.created_on,
            "division_name": self.division_name,
            "category_name": self.category_name,
            "d_ids": self.d_ids,
            "i_ids": self.i_ids,
        }
        return to_structure_dictionary_values(data)

class ClientUnitList(object):
    def __init__(
        self, country_id, client_id, legal_entity_id, business_group_id, unit_id, unit_code,
        unit_name, address, postal_code, is_active, closed_on, check_date, emp_code_name,
        created_on, division_name, category_name, d_o_names
    ):
        self.country_id = country_id
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id
        self.unit_id = unit_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.address = address
        self.postal_code = postal_code
        self.is_active = is_active
        self.closed_on = closed_on
        self.check_date = check_date
        self.emp_code_name = emp_code_name
        self.created_on = created_on
        self.division_name = division_name
        self.category_name = category_name
        self.d_o_names = d_o_names

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "country_id", "client_id", "legal_entity_id", "business_group_id", "unit_id", "unit_code",
            "unit_name", "address", "postal_code", "is_active", "closed_on", "check_date", "emp_code_name",
            "created_on", "division_name", "category_name", "d_o_names"
        ])
        country_id = data.get("country_id")
        client_id = data.get("client_id")
        legal_entity_id = data.get("legal_entity_id")
        business_group_id = data.get("business_group_id")
        unit_id = data.get("unit_id")
        unit_code = data.get("unit_code")
        unit_name = data.get("unit_name")
        address = data.get("address")
        postal_code = data.get("postal_code")
        is_active = data.get("is_active")
        closed_on = data.get("closed_on")
        check_date = data.get("check_date")
        emp_code_name = data.get("emp_code_name")
        created_on = data.get("created_on")
        division_name = data.get("division_name")
        category_name = data.get("category_name")
        d_o_names = data.get("d_o_names")
        return ClientUnitList(
            country_id, client_id, legal_entity_id, business_group_id, unit_id, unit_code,
            unit_name, address, postal_code, is_active, closed_on, check_date, emp_code_name,
            created_on, division_name, category_name, d_o_names
        )

    def to_structure(self):
        data = {
            "country_id": self.country_id,
            "client_id": self.client_id,
            "legal_entity_id": self.legal_entity_id,
            "business_group_id": self.business_group_id,
            "unit_id": self.unit_id,
            "unit_code": self.unit_code,
            "unit_name": self.unit_name,
            "address": self.address,
            "postal_code": self.postal_code,
            "is_active": self.is_active,
            "closed_on": self.closed_on,
            "check_date": self.check_date,
            "emp_code_name": self.emp_code_name,
            "created_on": self.created_on,
            "division_name": self.division_name,
            "category_name": self.category_name,
            "d_o_names": self.d_o_names,
        }
        return to_structure_dictionary_values(data)

class StatutoryNotificationList(object):
    def __init__(
        self, statutory_name, compliance_task, description, notification_text, date
    ):
        self.statutory_name = statutory_name
        self.compliance_task = compliance_task
        self.description = description
        self.notification_text = notification_text
        self.date = date

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
            "statutory_name",
            "compliance_task",
            "description",
            "notification_text",
            "notification_date"
            ]
        )

        statutory_name = data.get("statutory_name"),
        compliance_task = data.get("compliance_task"),
        description = data.get("description"),
        notification_text = data.get("notification_text"),
        date = data.get("notification_date")

        return StatutoryNotificationList(
            statutory_name, compliance_task, description, notification_text,
            date
        )

    def to_structure(self):
        return {
            "statutory_name": self.statutory_name,
            "compliance_task": self.compliance_task,
            "description": self.description,
            "notification_text": self.notification_text,
            "notification_date": self.date
        }

class GroupAdminClientGroup(object):
    def __init__(self, client_id, group_name, is_active):
        self.client_id = client_id
        self.group_name = group_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["client_id", "group_name", "is_active"])
        client_id = data.get("client_id")
        group_name = data.get("group_name")
        is_active = data.get("is_active")
        return GroupAdminClientGroup(client_id, group_name, is_active)

    def to_structure(self):
        data = {
            "client_id": self.client_id,
            "group_name": self.group_name,
            "is_active": self.is_active,
        }
        return data

class GroupAdminCountry(object):
    def __init__(self, client_id, country_id, country_name, is_active):
        self.client_id = client_id
        self.country_id = country_id
        self.country_name = country_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["client_id", "country_id", "country_name", "is_active"])
        client_id = data.get("client_id")
        country_id = data.get("country_id")
        country_name = data.get("country_name")
        is_active = data.get("is_active")
        return GroupAdminClientGroup(client_id, country_id, country_name, is_active)

    def to_structure(self):
        data = {
            "client_id": self.client_id,
            "country_id": self.country_id,
            "country_name": self.country_name,
            "is_active": self.is_active,
        }
        return data

class GroupAdminClientGroupData(object):
    def __init__(
        self, client_id, legal_entity_id, legal_entity_name, unit_count, country_id,
        country_name, unit_email_date, statutory_email_date, registration_email_date,
        resend_email_date
    ):
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.unit_count = unit_count
        self.country_id = country_id
        self.country_name = country_name
        self.unit_email_date = unit_email_date
        self.statutory_email_date = statutory_email_date
        self.registration_email_date = registration_email_date
        self.resend_email_date = resend_email_date

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "client_id", "legal_entity_id", "legal_entity_name", "unit_count",
            "country_id", "country_name", "unit_email_date", "statutory_email_date",
            "registration_email_date", "resend_email_date"
        ])
        client_id = data.get("client_id")
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_name = data.get("legal_entity_name")
        unit_count = data.get("unit_count")
        country_id = data.get("country_id")
        country_name = data.get("country_name")
        unit_email_date = data.get("unit_email_date")
        statutory_email_date = data.get("statutory_email_date")
        registration_email_date = data.get("registration_email_date")
        resend_email_date = data.get("resend_email_date")

        return GroupAdminClientGroupData(
            client_id, legal_entity_id, legal_entity_name, unit_count,
            country_id, country_name, unit_email_date, statutory_email_date,
            registration_email_date, resend_email_date
        )

    def to_structure(self):
        data = {
            "client_id": self.client_id,
            "legal_entity_id": self.legal_entity_id,
            "legal_entity_name": self.legal_entity_name,
            "unit_count": self.unit_count,
            "country_id": self.country_id,
            "country_name": self.country_name,
            "unit_email_date": self.unit_email_date,
            "statutory_email_date": self.statutory_email_date,
            "registration_email_date": self.registration_email_date,
            "resend_email_date": self.resend_email_date,
        }
        return data

class ReassignUserClients(object):
    def __init__(
        self, user_id, user_category_id, emp_code_name, client_ids
    ):
        self.user_id = user_id
        self.user_category_id = user_category_id
        self.emp_code_name = emp_code_name
        self.client_ids = client_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id", "user_category_id", "emp_code_name", "client_ids"
        ])
        user_id = data.get("user_id")
        user_category_id = data.get("user_category_id")
        emp_code_name = data.get("emp_code_name")
        client_ids = data.get("client_ids")

        return GroupAdminClientGroupData(
            user_id, user_category_id, emp_code_name, client_ids
        )

    def to_structure(self):
        data = {
            "user_id": self.user_id,
            "user_category_id": self.user_category_id,
            "emp_code_name": self.emp_code_name,
            "client_ids": self.client_ids,
        }
        return data

class ReassignUserDomainList(object):
    def __init__(
        self, user_id, client_id, legal_entity_id, legal_entity_name,
        business_group_id, business_group_name, domain_id, domain_name
    ):
        self.user_id = user_id
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.business_group_id = business_group_id
        self.business_group_name = business_group_name
        self.domain_id = domain_id
        self.domain_name = domain_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id", "client_id", "legal_entity_id", "legal_entity_name",
            "business_group_id", "business_group_name", "domain_id", "domain_name"
        ])
        user_id = data.get("user_id")
        client_id = data.get("client_id")
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_name = data.get("legal_entity_name")
        business_group_id = data.get("business_group_id")
        business_group_name = data.get("business_group_name")
        domain_id = data.get("domain_id")
        domain_name = data.get("domain_name")

        return GroupAdminClientGroupData(
            user_id, client_id, legal_entity_id, legal_entity_name,
            business_group_id, business_group_name, domain_id, domain_name
        )

    def to_structure(self):
        data = {
            "user_id": self.user_id,
            "client_id": self.client_id,
            "legal_entity_id": self.legal_entity_id,
            "legal_entity_name": self.legal_entity_name,
            "business_group_id": self.business_group_id,
            "business_group_name": self.business_group_name,
            "domain_id": self.domain_id,
            "domain_name": self.domain_name
        }
        return data

class ReassignedUserList(object):
    def __init__(
        self, client_id, group_name, le_count, c_names, unit_email_date, emp_code_name, remarks,
        legal_entity_name
    ):
        self.client_id = client_id
        self.group_name = group_name
        self.le_count = le_count
        self.c_names = c_names
        self.unit_email_date = unit_email_date
        self.emp_code_name = emp_code_name
        self.remarks = remarks
        self.legal_entity_name = legal_entity_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "client_id", "group_name", "le_count", "c_names", "unit_email_date",
            "emp_code_name", "remarks", "legal_entity_name"
        ])
        client_id = data.get("client_id")
        group_name = data.get("group_name")
        le_count = data.get("le_count")
        c_names = data.get("c_names")
        unit_email_date = data.get("unit_email_date")
        emp_code_name = data.get("emp_code_name")
        remarks = data.get("remarks")
        legal_entity_name = data.get("legal_entity_name")
        return ReassignedUserList(
            client_id, group_name, le_count, c_names, unit_email_date, emp_code_name, remarks, legal_entity_name
        )

    def to_structure(self):
        data = {
            "client_id": self.client_id,
            "group_name": self.group_name,
            "le_count": self.le_count,
            "c_names": self.c_names,
            "unit_email_date": self.unit_email_date,
            "emp_code_name": self.emp_code_name,
            "remarks": self.remarks,
            "legal_entity_name": self.legal_entity_name
        }
        return data

class ReassignedDomainUserList(object):
    def __init__(
        self, unit_id, unit_code, unit_name, address, postal_code, geography_name,
        unit_email_date, emp_code_name, remarks
    ):
        self.unit_id = unit_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.address = address
        self.postal_code = postal_code
        self.geography_name = geography_name
        self.unit_email_date = unit_email_date
        self.emp_code_name = emp_code_name
        self.remarks = remarks

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "unit_id", "unit_code", "unit_name", "address", "postal_code",
            "geography_name", "unit_email_date", "emp_code_name", "remarks"
        ])
        unit_id = data.get("unit_id")
        unit_code = data.get("unit_code")
        unit_name = data.get("unit_name")
        address = data.get("address")
        postal_code = data.get("postal_code")
        geography_name = data.get("geography_name")
        unit_email_date = data.get("unit_email_date")
        emp_code_name = data.get("emp_code_name")
        remarks = data.get("remarks")
        return ReassignedUserList(
            unit_id, unit_code, unit_name, address, postal_code,
            geography_name, unit_email_date, emp_code_name, remarks
        )

    def to_structure(self):
        data = {
            "unit_id": self.unit_id,
            "unit_code": self.unit_code,
            "unit_name": self.unit_name,
            "address": self.address,
            "postal_code": self.postal_code,
            "geography_name": self.geography_name,
            "unit_email_date": self.unit_email_date,
            "emp_code_name": self.emp_code_name,
            "remarks": self.remarks,
        }
        return data

class ApproveAssignedStatutories(object):
    def __init__(
        self, country_name, group_name, legal_entity_name, business_group_name, division_name,
        category_name, unit_id, unit_name, domain_name, statutory_id, domain_id

    ):
        self.country_name = country_name
        self.group_name = group_name
        self.legal_entity_name = legal_entity_name
        self.business_group_name = business_group_name
        self.division_name = division_name
        self.category_name = category_name
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.domain_name = domain_name
        self.statutory_id = statutory_id
        self.domain_id = domain_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "country_name", "group_name", "legal_entity_name", "business_group_name",
            "division_name", "category_name", "unit_id", "unit_name", "domain_name",
            "statutory_id", "domain_id"
        ])
        country_name = data.get("country_name")
        group_name = data.get("group_name")
        legal_entity_name = data.get("legal_entity_name")
        business_group_name = data.get("business_group_name")
        division_name = data.get("division_name")
        category_name = data.get("category_name")
        unit_id = data.get("unit_id")
        unit_name = data.get("unit_name")
        domain_name = data.get("domain_name")
        statutory_id = data.get("statutory_id")
        domain_id = data.get("domain_id")

        return ReassignedUserList(
            country_name, group_name, legal_entity_name, business_group_name, division_name,
            category_name, unit_id, unit_name, domain_name, statutory_id, domain_id
        )

    def to_structure(self):
        data = {
            "country_name": self.country_name,
            "group_name": self.group_name,
            "legal_entity_name": self.legal_entity_name,
            "business_group_name": self.business_group_name,
            "division_name": self.division_name,
            "category_name": self.category_name,
            "unit_id": self.unit_id,
            "unit_name": self.unit_name,
            "domain_name": self.domain_name,
            "statutory_id": self.statutory_id,
            "domain_id": self.domain_id,
        }
        return data
