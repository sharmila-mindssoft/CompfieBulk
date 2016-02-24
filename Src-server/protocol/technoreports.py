
from protocol.jsonvalidators import (parse_dictionary, parse_static_list)
from protocol.parse_structure import (
    parse_structure_VectorType_RecordType_core_Domain,
    parse_structure_VectorType_RecordType_core_AssignedStatutory,
    parse_structure_VariantType_technoreports_Request,
    parse_structure_VectorType_RecordType_core_LegalEntity,
    parse_structure_OptionalType_VectorType_SignedIntegerType_8,
    parse_structure_UnsignedIntegerType_32,
    parse_structure_VectorType_RecordType_core_Unit,
    parse_structure_OptionalType_VectorType_RecordType_core_BusinessGroup,
    parse_structure_VectorType_RecordType_core_GroupCompany,
    parse_structure_VectorType_RecordType_core_Country,
    parse_structure_VectorType_RecordType_core_Division,
    parse_structure_VectorType_RecordType_core_UnitDetails,
    parse_structure_VectorType_RecordType_technoreports_COUNTRY_WISE_NOTIFICATIONS,
    parse_structure_OptionalType_SignedIntegerType_8,
    parse_structure_VectorType_RecordType_technoreports_UNIT_WISE_ASSIGNED_STATUTORIES,
    parse_structure_CustomTextType_50,
    parse_structure_OptionalType_VectorType_RecordType_core_Division,
    parse_structure_OptionalType_Bool,
    parse_structure_CustomTextType_100,
    parse_structure_CustomTextType_250,
    parse_structure_VectorType_RecordType_core_BusinessGroup,
    parse_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory,
    parse_structure_OptionalType_UnsignedIntegerType_32,
    parse_structure_VectorType_RecordType_techno_report_UnitDetails,
    parse_structure_VectorType_RecordType_technoreports_NOTIFICATIONS,
    parse_structure_VectorType_SignedIntegerType_8,
    parse_structure_CustomTextType_20,
    parse_structure_CustomTextType_500
)
from protocol.to_structure import (
    to_structure_VectorType_RecordType_core_Domain,
    to_structure_VectorType_RecordType_core_AssignedStatutory,
    to_structure_VariantType_technoreports_Request,
    to_structure_VectorType_RecordType_core_LegalEntity,
    to_structure_OptionalType_VectorType_SignedIntegerType_8,
    to_structure_SignedIntegerType_8,
    to_structure_VectorType_RecordType_core_Unit,
    to_structure_OptionalType_VectorType_RecordType_core_BusinessGroup,
    to_structure_VectorType_RecordType_core_GroupCompany,
    to_structure_VectorType_RecordType_core_Country,
    to_structure_VectorType_RecordType_core_Division,
    to_structure_VectorType_RecordType_technoreports_COUNTRY_WISE_NOTIFICATIONS,
    to_structure_OptionalType_SignedIntegerType_8,
    to_structure_VectorType_RecordType_technoreports_UNIT_WISE_ASSIGNED_STATUTORIES,
    to_structure_CustomTextType_50,
    to_structure_OptionalType_VectorType_RecordType_core_Division,
    to_structure_OptionalType_Bool,
    to_structure_CustomTextType_100,
    to_structure_CustomTextType_250,
    to_structure_VectorType_RecordType_core_BusinessGroup,
    to_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory,
    to_structure_VectorType_RecordType_techno_report_UnitDetails,
    to_structure_CustomTextType_20,
    to_structure_OptionalType_UnsignedIntegerType_32,
    to_structure_UnsignedIntegerType_32,
    to_structure_VectorType_SignedIntegerType_8,
    to_structure_VectorType_RecordType_techno_report_GroupedUnits,
    to_structure_VectorType_RecordType_technoreports_NOTIFICATIONS,
    to_structure_CustomTextType_500
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

class GetClientDetailsReportData(Request):
    def __init__(self, country_id, group_id, business_group_id, legal_entity_id, division_id, unit_id, domain_ids):
        self.country_id = country_id
        self.group_id = group_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.unit_id = unit_id
        self.domain_ids = domain_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "group_id", "business_group_id", "legal_entity_id", "division_id", "unit_id", "domain_ids"])
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        group_id = data.get("group_id")
        group_id = parse_structure_UnsignedIntegerType_32(group_id)
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_OptionalType_SignedIntegerType_8(business_group_id)
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_OptionalType_SignedIntegerType_8(legal_entity_id)
        division_id = data.get("division_id")
        division_id = parse_structure_OptionalType_SignedIntegerType_8(division_id)
        unit_id = data.get("unit_id")
        unit_id = parse_structure_OptionalType_SignedIntegerType_8(unit_id)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_OptionalType_VectorType_SignedIntegerType_8(domain_ids)
        return GetClientDetailsReportData(country_id, group_id, business_group_id, legal_entity_id, division_id, unit_id, domain_ids)

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "group_id": to_structure_SignedIntegerType_8(self.group_id),
            "business_group_id": to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
            "legal_entity_id": to_structure_OptionalType_SignedIntegerType_8(self.legal_entity_id),
            "division_id": to_structure_OptionalType_SignedIntegerType_8(self.division_id),
            "unit_id": to_structure_OptionalType_SignedIntegerType_8(self.unit_id),
            "domain_ids": to_structure_OptionalType_VectorType_SignedIntegerType_8(self.domain_ids),
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
    def __init__(self, country_id, domain_id, level_1_statutory_id):
        self.country_id = country_id
        self.domain_id = domain_id
        self.level_1_statutory_id = level_1_statutory_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "domain_id", "level_1_statutory_id"])
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        level_1_statutory_id = data.get("level_1_statutory_id")
        level_1_statutory_id = parse_structure_OptionalType_SignedIntegerType_8(level_1_statutory_id)
        return GetStatutoryNotificationsReportData(country_id, domain_id, level_1_statutory_id)

    def to_inner_structure(self):
        return {
            "country_id" : to_structure_SignedIntegerType_8(self.country_id),
            "domain_id" : to_structure_SignedIntegerType_8(self.domain_id),
            "level_1_statutory_id" : to_structure_OptionalType_UnsignedIntegerType_32(self.level_1_statutory_id)
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
    def __init__(self, country_id, domain_id, group_id, business_group_id, legal_entity_id, division_id, unit_id, level_1_statutory_id, applicability_status):
        self.country_id = country_id
        self.domain_id = domain_id
        self.group_id = group_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.unit_id = unit_id
        self.level_1_statutory_id = level_1_statutory_id
        self.applicability_status = applicability_status

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "domain_id", "group_id", "business_group_id", "legal_entity_id", "division_id", "unit_id", "level_1_statutory_id", "applicability_status"])
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        group_id = data.get("group_id")
        group_id = parse_structure_OptionalType_SignedIntegerType_8(group_id)
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_OptionalType_SignedIntegerType_8(business_group_id)
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_OptionalType_SignedIntegerType_8(legal_entity_id)
        division_id = data.get("division_id")
        division_id = parse_structure_OptionalType_SignedIntegerType_8(division_id)
        unit_id = data.get("unit_id")
        unit_id = parse_structure_OptionalType_SignedIntegerType_8(unit_id)
        level_1_statutory_id = data.get("level_1_statutory_id")
        level_1_statutory_id = parse_structure_OptionalType_SignedIntegerType_8(level_1_statutory_id)
        applicability_status = data.get("applicability_status")
        applicability_status = parse_structure_OptionalType_Bool(applicability_status)
        return GetAssignedStatutoryReport(country_id, domain_id, group_id, business_group_id, legal_entity_id, division_id, unit_id, level_1_statutory_id, applicability_status)

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "group_id": to_structure_OptionalType_SignedIntegerType_8(self.group_id),
            "business_group_id": to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
            "legal_entity_id": to_structure_OptionalType_SignedIntegerType_8(self.legal_entity_id),
            "division_id": to_structure_OptionalType_SignedIntegerType_8(self.division_id),
            "unit_id": to_structure_OptionalType_SignedIntegerType_8(self.unit_id),
            "level_1_statutory_id": to_structure_OptionalType_SignedIntegerType_8(self.level_1_statutory_id),
            "applicability_status": to_structure_OptionalType_Bool(self.applicability_status),
        }


def _init_Request_class_map():
    classes = [GetClientDetailsReportFilters, GetClientDetailsReportData, GetStatutoryNotificationsFilters, GetStatutoryNotificationsReportData,  GetAssignedStatutoryReportFilters, GetAssignedStatutoryReport]
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

class GetClientDetailsReportFiltersSuccess(Response):
    def __init__(self, countries, domains, group_companies, business_groups, legal_entities, divisions, units):
        self.countries = countries
        self.domains = domains
        self.group_companies = group_companies
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.units = units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "group_companies", "business_groups", "legal_entities", "divisions", "units"])
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        domains = data.get("domains")
        domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        group_companies = data.get("group_companies")
        group_companies = parse_structure_VectorType_RecordType_core_GroupCompany(group_companies)
        business_groups = data.get("business_groups")
        business_groups = parse_structure_OptionalType_VectorType_RecordType_core_BusinessGroup(business_groups)
        legal_entities = data.get("legal_entities")
        legal_entities = parse_structure_VectorType_RecordType_core_LegalEntity(legal_entities)
        divisions = data.get("divisions")
        divisions = parse_structure_OptionalType_VectorType_RecordType_core_Division(divisions)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_core_Unit(units)
        return GetClientDetailsReportFiltersSuccess(countries, domains, group_companies, business_groups, legal_entities, divisions, units)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "group_companies": to_structure_VectorType_RecordType_core_GroupCompany(self.group_companies),
            "business_groups": to_structure_OptionalType_VectorType_RecordType_core_BusinessGroup(self.business_groups),
            "legal_entities": to_structure_VectorType_RecordType_core_LegalEntity(self.legal_entities),
            "divisions": to_structure_OptionalType_VectorType_RecordType_core_Division(self.divisions),
            "units": to_structure_VectorType_RecordType_core_Unit(self.units),
        }

class GroupedUnits(object):
    def __init__(self, division_id, legal_entity_id, business_group_id, units):
        self.division_id = division_id
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id
        self.units = units

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["division_id", "legal_entity_id", "business_group_id", "units"])
        division_id = data.get("division_id")
        division_id = parse_structure_OptionalType_UnsignedIntegerType_32(division_id)
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_UnsignedIntegerType_32(legal_entity_id)
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_OptionalType_UnsignedIntegerType_32(business_group_id)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_techno_report_UnitDetails(units)
        return GroupedUnits(division_id, legal_entity_id, business_group_id, units)

    def to_structure(self):
        return {
            "division_id": to_structure_OptionalType_UnsignedIntegerType_32(self.division_id),
            "legal_entity_id": to_structure_UnsignedIntegerType_32(self.legal_entity_id),
            "business_group_id": to_structure_OptionalType_UnsignedIntegerType_32(self.business_group_id),
            "units" : to_structure_VectorType_RecordType_techno_report_UnitDetails(self.units)
        }


class UnitDetails(object):
    def __init__(self, unit_id, geography_name, unit_code, unit_name, unit_address, postal_code, domain_ids):
        self.unit_id = unit_id
        self.geography_name = geography_name
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.unit_address = unit_address
        self.postal_code = postal_code
        self.domain_ids = domain_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_id", "geography_name", "unit_code", "unit_name", "unit_address", "postal_code", "domain_ids"])
        unit_id = data.get("unit_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        geography_name = data.get("geography_name")
        geography_name = parse_structure_CustomTextType_250(geography_name)
        unit_code = data.get("unit_code")
        unit_code = parse_structure_CustomTextType_20(unit_code)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_50(unit_name)
        unit_address = data.get("unit_address")
        unit_address = parse_structure_CustomTextType_250(unit_address)
        postal_code = data.get("postal_code")
        postal_code = parse_structure_UnsignedIntegerType_32(postal_code)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        return UnitDetails(unit_id, geography_name, unit_code, unit_name, unit_address, postal_code, domain_ids)

    def to_structure(self):
        return {
            "unit_id": to_structure_UnsignedIntegerType_32(self.unit_id),
            "geography_name": to_structure_CustomTextType_250(self.geography_name),
            "unit_code": to_structure_CustomTextType_20(self.unit_code),
            "unit_name": to_structure_CustomTextType_50(self.unit_name),
            "unit_address": to_structure_CustomTextType_250(self.unit_address),
            "postal_code": to_structure_UnsignedIntegerType_32(self.postal_code),
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids)
        }


class GetClientDetailsReportDataSuccess(Response):
    def __init__(self, units):
        self.units = units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["units"])
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_core_UnitDetails(units)
        return GetClientDetailsReportDataSuccess(units)

    def to_inner_structure(self):
        return {
            "units": to_structure_VectorType_RecordType_techno_report_GroupedUnits(self.units)
        }

class GetStatutoryNotificationsFiltersSuccess(Response):
    def __init__(self, countries, domains, level_1_statutories):
        self.countries = countries
        self.domains = domains
        self.level_1_statutories = level_1_statutories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "level_1_statutories"])
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        domains = data.get("domains")
        domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        level_1_statutories = data.get("level_1_statutories")
        level_1_statutories = parse_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(level_1_statutories)
        return GetStatutoryNotificationsReportDataSuccess(countries, domains, level_1_statutories)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "level_1_statutories": to_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(self.level_1_statutories)
        }

class GetStatutoryNotificationsReportDataSuccess(Response):
    def __init__(self, countries, domains, level_1_statutories, country_wise_notifications):
        self.countries = countries
        self.domains = domains
        self.level_1_statutories = level_1_statutories
        self.country_wise_notifications = country_wise_notifications

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "level_1_statutories", "country_wise_notifications"])
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        domains = data.get("domains")
        domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        level_1_statutories = data.get("level_1_statutories")
        level_1_statutories = parse_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(level_1_statutories)
        country_wise_notifications = data.get("country_wise_notifications")
        country_wise_notifications = parse_structure_VectorType_RecordType_technoreports_COUNTRY_WISE_NOTIFICATIONS(country_wise_notifications)
        return GetStatutoryNotificationsReportDataSuccess(countries, domains, level_1_statutories, country_wise_notifications)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "level_1_statutories": to_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(self.level_1_statutories),
            "country_wise_notifications": to_structure_VectorType_RecordType_technoreports_COUNTRY_WISE_NOTIFICATIONS(self.country_wise_notifications),
        }

class GetAssignedStatutoryReportFiltersSuccess(Response):
    def __init__(self, countries, domains, groups, business_groups, legal_entities, divisions, units, level_1_statutories):
        self.countries = countries
        self.domains = domains
        self.groups = groups
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.units = units
        self.level_1_statutories = level_1_statutories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "groups", "business_groups", "legal_entities", "divisions", "units", "level_1_statutories"])
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        domains = data.get("domains")
        domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        groups = data.get("groups")
        groups = parse_structure_VectorType_RecordType_core_GroupCompany(groups)
        business_groups = data.get("business_groups")
        business_groups = parse_structure_VectorType_RecordType_core_BusinessGroup()
        legal_entities = data.get("legal_entities")
        legal_entities = parse_structure_VectorType_RecordType_core_LegalEntity(legal_entities)
        divisions = data.get("divisions")
        divisions = parse_structure_VectorType_RecordType_core_Division(divisions)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_core_Unit(units)
        level_1_statutories = data.get("level_1_statutories")
        level_1_statutories = parse_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(level_1_statutories)
        return GetAssignedStatutoryReportFiltersSuccess(countries, domains, groups, business_groups, legal_entities, divisions, units, level_1_statutories)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "groups": to_structure_VectorType_RecordType_core_GroupCompany(self.groups),
            "business_groups": to_structure_VectorType_RecordType_core_BusinessGroup(self.business_groups),
            "legal_entities": to_structure_VectorType_RecordType_core_LegalEntity(self.legal_entities),
            "divisions": to_structure_VectorType_RecordType_core_Division(self.divisions),
            "units": to_structure_VectorType_RecordType_core_Unit(self.units),
            "level_1_statutories": to_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(self.level_1_statutories),
        }

class GetAssignedStatutoryReportSuccess(Response):
    def __init__(self, unit_wise_assigned_statutories):
        self.unit_wise_assigned_statutories = unit_wise_assigned_statutories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["unit_wise_assigned_statutories"])
        unit_wise_assigned_statutories = data.get("unit_wise_assigned_statutories")
        unit_wise_assigned_statutories = parse_structure_VectorType_RecordType_technoreports_UNIT_WISE_ASSIGNED_STATUTORIES(unit_wise_assigned_statutories)
        return GetAssignedStatutoryReportSuccess(unit_wise_assigned_statutories)

    def to_inner_structure(self):
        return {
            "unit_wise_assigned_statutories": to_structure_VectorType_RecordType_technoreports_UNIT_WISE_ASSIGNED_STATUTORIES(self.unit_wise_assigned_statutories),
        }


def _init_Response_class_map():
    classes = [GetClientDetailsReportFiltersSuccess, GetClientDetailsReportDataSuccess, GetStatutoryNotificationsFiltersSuccess, GetStatutoryNotificationsReportDataSuccess, GetAssignedStatutoryReportFiltersSuccess, GetAssignedStatutoryReportSuccess]
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
        request = parse_structure_VariantType_technoreports_Request(request)
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": to_structure_CustomTextType_50(self.session_token),
            "request": to_structure_VariantType_technoreports_Request(self.request),
        }

#
# COUNTRY_WISE_NOTIFICATIONS
#

class COUNTRY_WISE_NOTIFICATIONS(object):
    def __init__(self, country_id, domain_id, notifications):
        self.country_id = country_id
        self.domain_id = domain_id
        self.notifications = notifications

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["country_id", "domain_id", "notifications"])
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        notifications = data.get("notifications")
        notifications = parse_structure_VectorType_RecordType_technoreports_NOTIFICATIONS(notifications)
        return COUNTRY_WISE_NOTIFICATIONS(country_id, domain_id, notifications)

    def to_structure(self):
        return {
            "country_id": to_structure_OptionalType_UnsignedIntegerType_32(self.country_id),
            "domain_id": to_structure_OptionalType_UnsignedIntegerType_32(self.domain_id),
            "notifications": to_structure_VectorType_RecordType_technoreports_NOTIFICATIONS(self.notifications),
        }

#
# NOTIFICATIONS
#

class NOTIFICATIONS(object):
    def __init__(self, statutory_provision, notification_text, date_and_time):
        self.statutory_provision = statutory_provision
        self.notification_text = notification_text
        self.date_and_time = date_and_time

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["statutory_provision", "notification_text", "date_and_time"])
        statutory_provision = data.get("statutory_provision")
        statutory_provision = parse_structure_CustomTextType_500(statutory_provision)
        notification_text = data.get("notification_text")
        notification_text = parse_structure_CustomTextType_500(notification_text)
        date_and_time = data.get("date_and_time")
        date_and_time = parse_structure_CustomTextType_20(date_and_time)
        return NOTIFICATIONS(statutory_provision, notification_text, date_and_time)

    def to_structure(self):
        return {
            "statutory_provision": to_structure_CustomTextType_500(self.statutory_provision),
            "notification_text": to_structure_CustomTextType_500(self.notification_text),
            "date_and_time": to_structure_CustomTextType_20(self.date_and_time)
        }

#
# UNIT_WISE_ASSIGNED_STATUTORIES
#

class UNIT_WISE_ASSIGNED_STATUTORIES(object):
    def __init__(self, unit_id, unit_name, group_name, business_group_name, legal_entity_name, division_name, address, assigned_statutories):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.group_name = group_name
        self.business_group_name = business_group_name
        self.legal_entity_name = legal_entity_name
        self.division_name = division_name
        self.address = address
        self.assigned_statutories = assigned_statutories

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_id", "unit_name", "group_name", "business_group_name", "legal_entity_name", "division_name", "address", "assigned_statutories"])
        unit_id = data.get("unit_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_100(unit_name)
        group_name = data.get("group_name")
        group_name = parse_structure_CustomTextType_50(group_name)
        business_group_name = data.get("business_group_name")
        business_group_name = parse_structure_CustomTextType_50(business_group_name)
        legal_entity_name = data.get("parse_structure_CustomTextType_50")
        legal_entity_name = parse_structure_CustomTextType_50(legal_entity_name)
        division_name = data.get("division_name")
        division_name = parse_structure_CustomTextType_50(division_name)
        address = data.get("address")
        address = parse_structure_CustomTextType_500(address)
        assigned_statutories = data.get("assigned_statutories")
        assigned_statutories = parse_structure_VectorType_RecordType_core_AssignedStatutory(assigned_statutories)
        return UNIT_WISE_ASSIGNED_STATUTORIES(unit_id, unit_name, group_name, business_group_name, legal_entity_name, division_name, address, assigned_statutories)

    def to_structure(self):
        return {
            "unit_id": to_structure_UnsignedIntegerType_32(self.unit_id),
            "unit_name": to_structure_CustomTextType_100(self.unit_name),
            "group_name": to_structure_CustomTextType_50(self.group_name),
            "business_group_name": to_structure_CustomTextType_50(self.business_group_name),
            "legal_entity_name": to_structure_CustomTextType_50(self.legal_entity_name),
            "division_name": to_structure_CustomTextType_50(self.division_name),
            "address": to_structure_CustomTextType_250(self.address),
            "assigned_statutories": to_structure_VectorType_RecordType_core_AssignedStatutory(self.assigned_statutories),
        }
