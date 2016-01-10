import json
from protocol.jsonvalidators import (parse_enum, parse_dictionary, parse_static_list)
from protocol.parse_structure import (
    parse_structure_VariantType_technotransactions_Request,
    parse_structure_EnumType_core_ASSIGN_STATUTORY_SUBMISSION_STATUS,
    parse_structure_EnumType_core_ASSIGN_STATUTORY_SUBMISSION_TYPE,
    parse_structure_VectorType_RecordType_core_AssignedStatutory,
    parse_structure_VectorType_RecordType_technotransactions_UNIT,
    parse_structure_VectorType_RecordType_core_LegalEntity,
    parse_structure_OptionalType_CustomTextType_50,
    parse_structure_UnsignedIntegerType_32,
    parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level,
    parse_structure_VectorType_RecordType_core_Industry,
    parse_structure_VectorType_RecordType_core_GroupCompany,
    parse_structure_VectorType_RecordType_core_Country,
    parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Geography,
    parse_structure_VectorType_RecordType_core_Division,
    parse_structure_VectorType_RecordType_core_BusinessGroup,
    parse_structure_OptionalType_SignedIntegerType_8,
    parse_structure_VectorType_RecordType_technotransactions_ASSIGNED_STATUTORIES,
    parse_structure_CustomTextType_50,
    parse_structure_VectorType_RecordType_core_Domain,
    parse_structure_CustomTextType_100,
    parse_structure_VectorType_UnsignedIntegerType_32
)
from protocol.to_structure import (
    to_structure_VariantType_technotransactions_Request,
    to_structure_EnumType_core_ASSIGN_STATUTORY_SUBMISSION_STATUS,
    to_structure_EnumType_core_ASSIGN_STATUTORY_SUBMISSION_TYPE,
    to_structure_VectorType_RecordType_core_AssignedStatutory,
    to_structure_VectorType_RecordType_technotransactions_UNIT,
    to_structure_VectorType_RecordType_core_LegalEntity,
    to_structure_OptionalType_CustomTextType_50,
    to_structure_SignedIntegerType_8,
    to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level,
    to_structure_VectorType_RecordType_core_Industry,
    to_structure_VectorType_RecordType_core_GroupCompany,
    to_structure_VectorType_RecordType_core_Country,
    to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Geography,
    to_structure_VectorType_RecordType_core_Division,
    to_structure_VectorType_RecordType_core_BusinessGroup,
    to_structure_OptionalType_SignedIntegerType_8,
    to_structure_VectorType_RecordType_technotransactions_ASSIGNED_STATUTORIES,
    to_structure_CustomTextType_50,
    to_structure_VectorType_RecordType_core_Domain,
    to_structure_CustomTextType_100,
    to_structure_VectorType_UnsignedIntegerType_32
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

class GetAssignedStatutoriesById(Request):
    def __init__(self, submission_status, client_saved_statutory_id, client_assigned_statutory_id):
        self.submission_status = submission_status
        self.client_saved_statutory_id = client_saved_statutory_id
        self.client_assigned_statutory_id = client_assigned_statutory_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["submission_status", "client_saved_statutory_id", "client_assigned_statutory_id"])
        submission_status = data.get("submission_status")
        submission_status = parse_structure_EnumType_core_ASSIGN_STATUTORY_SUBMISSION_TYPE(submission_status)
        client_saved_statutory_id = data.get("client_saved_statutory_id")
        client_saved_statutory_id = parse_structure_UnsignedIntegerType_32(client_saved_statutory_id)
        client_assigned_statutory_id = data.get("client_assigned_statutory_id")
        client_assigned_statutory_id = parse_structure_UnsignedIntegerType_32(client_assigned_statutory_id)
        return GetAssignedStatutoriesById(submission_status, client_saved_statutory_id, client_assigned_statutory_id)

    def to_inner_structure(self):
        return {
            "submission_status": to_structure_EnumType_core_ASSIGN_STATUTORY_SUBMISSION_TYPE(self.submission_status),
            "client_saved_statutory_id": to_structure_SignedIntegerType_8(self.client_saved_statutory_id),
            "client_assigned_statutory_id": to_structure_SignedIntegerType_8(self.client_assigned_statutory_id),
        }

class GetAssignedStatutoryWizardOneData(Request):
    def __init__(self, country_id):
        self.country_id = country_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id"])
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        return GetAssignedStatutoryWizardOneData(country_id)

    def to_inner_structure(self):
        return {
            "country_id": to_structure_UnSignedIntegerType_32(self.country_id)
        }

class GetStatutoryWizardTwoData(Request):
    def __init__(self, geography_id, industry_id, domain_id):
        self.geography_id = geography_id
        self.industry_id = industry_id
        self.domain_id = domain_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["geography_id", "industry_id", "domain_id"])
        geography_id = data.get("geography_id")
        geography_id = parse_structure_UnsignedIntegerType_32(geography_id)
        industry_id = data.get("industry_id")
        industry_id = parse_structure_UnsignedIntegerType_32(industry_id)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        return GetStatutoryWizardTwoData(geography_id, industry_id, domain_id)

    def to_inner_structure(self):
        return {
            "geography_id": to_structure_SignedIntegerType_8(self.geography_id),
            "industry_id": to_structure_SignedIntegerType_8(self.industry_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
        }

class SaveAssignedStatutory(Request):
    def __init__(self, submission_type, client_saved_statutory_id, client_assigned_statutory_id, assigned_statutories):
        self.submission_type = submission_type
        self.client_saved_statutory_id = client_saved_statutory_id
        self.client_assigned_statutory_id = client_assigned_statutory_id
        self.assigned_statutories = assigned_statutories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["submission_type", "client_saved_statutory_id", "client_assigned_statutory_id", "assigned_statutories"])
        submission_type = data.get("submission_type")
        submission_type = parse_structure_EnumType_core_ASSIGN_STATUTORY_SUBMISSION_TYPE(submission_type)
        client_saved_statutory_id = data.get("client_saved_statutory_id")
        client_saved_statutory_id = parse_structure_UnsignedIntegerType_32(client_saved_statutory_id)
        client_assigned_statutory_id = data.get("client_assigned_statutory_id")
        client_assigned_statutory_id = parse_structure_UnsignedIntegerType_32(client_assigned_statutory_id)
        assigned_statutories = data.get("assigned_statutories")
        assigned_statutories = parse_structure_VectorType_RecordType_core_AssignedStatutory(assigned_statutories)
        return SaveAssignedStatutory(submission_type, client_saved_statutory_id, client_assigned_statutory_id, assigned_statutories)

    def to_inner_structure(self):
        return {
            "submission_type": to_structure_EnumType_core_ASSIGN_STATUTORY_SUBMISSION_TYPE(self.submission_type),
            "client_saved_statutory_id": to_structure_SignedIntegerType_8(self.client_saved_statutory_id),
            "client_assigned_statutory_id": to_structure_SignedIntegerType_8(self.client_assigned_statutory_id),
            "assigned_statutories": to_structure_VectorType_RecordType_core_AssignedStatutory(self.assigned_statutories),
        }


def _init_Request_class_map():
    classes = [GetAssignedStatutoriesList, GetAssignedStatutoriesById, GetAssignedStatutoryWizardOneData, GetStatutoryWizardTwoData, SaveAssignedStatutory]
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

class GetAssignedStatutoriesListSuccess(Response):
    def __init__(self, assigned_statutories):
        self.assigned_statutories = assigned_statutories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["assigned_statutories"])
        assigned_statutories = data.get("assigned_statutories")
        assigned_statutories = parse_structure_VectorType_RecordType_technotransactions_ASSIGNED_STATUTORIES(assigned_statutories)
        return GetAssignedStatutoriesListSuccess(assigned_statutories)

    def to_inner_structure(self):
        return {
            "assigned_statutories": to_structure_VectorType_RecordType_technotransactions_ASSIGNED_STATUTORIES(self.assigned_statutories),
        }

class GetAssignedStatutoriesByIdSuccess(Response):
    def __init__(self, country_name, group_name, business_group_name, legal_entity_name, division_name, unit_name, geography_name, domain_name, statutories):
        self.country_name = country_name
        self.group_name = group_name
        self.business_group_name = business_group_name
        self.legal_entity_name = legal_entity_name
        self.division_name = division_name
        self.unit_name = unit_name
        self.geography_name = geography_name
        self.domain_name = domain_name
        self.statutories = statutories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_name", "group_name", "business_group_name", "legal_entity_name", "division_name", "unit_name", "geography_name", "domain_name", "statutories"])
        country_name = data.get("country_name")
        country_name = parse_structure_CustomTextType_50(country_name)
        group_name = data.get("group_name")
        group_name = parse_structure_CustomTextType_50(group_name)
        business_group_name = data.get("business_group_name")
        business_group_name = parse_structure_OptionalType_CustomTextType_50(business_group_name)
        legal_entity_name = data.get("legal_entity_name")
        legal_entity_name = parse_structure_CustomTextType_50(legal_entity_name)
        division_name = data.get("division_name")
        division_name = parse_structure_OptionalType_CustomTextType_50(division_name)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_50(unit_name)
        geography_name = data.get("geography_name")
        geography_name = parse_structure_CustomTextType_50(geography_name)
        domain_name = data.get("domain_name")
        domain_name = parse_structure_CustomTextType_50(domain_name)
        statutories = data.get("statutories")
        statutories = parse_structure_VectorType_RecordType_core_AssignedStatutory(statutories)
        return GetAssignedStatutoriesByIdSuccess(country_name, group_name, business_group_name, legal_entity_name, division_name, unit_name, geography_name, domain_name, statutories)

    def to_inner_structure(self):
        return {
            "country_name": to_structure_CustomTextType_50(self.country_name),
            "group_name": to_structure_CustomTextType_50(self.group_name),
            "business_group_name": to_structure_OptionalType_CustomTextType_50(self.business_group_name),
            "legal_entity_name": to_structure_CustomTextType_50(self.legal_entity_name),
            "division_name": to_structure_OptionalType_CustomTextType_50(self.division_name),
            "unit_name": to_structure_CustomTextType_50(self.unit_name),
            "geography_name": to_structure_CustomTextType_50(self.geography_name),
            "domain_name": to_structure_CustomTextType_50(self.domain_name),
            "statutories": to_structure_VectorType_RecordType_core_AssignedStatutory(self.statutories),
        }

class GetAssignedStatutoryWizardOneDataSuccess(Response):
    def __init__(self, domains, industries, geography_levels, geographies, group_companies, business_groups, legal_entities, divisions, units):
        self.domains = domains
        self.industries = industries
        self.geography_levels = geography_levels
        self.geographies = geographies
        self.group_companies = group_companies
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.units = units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domains", "industries", "geography_levels", "geographies", "group_companies", "business_groups", "legal_entities", "divisions", "units"])
        domains = data.get("domains")
        domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        industries = data.get("industries")
        industries = parse_structure_VectorType_RecordType_core_Industry(industries)
        geography_levels = data.get("geography_levels")
        geography_levels = parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level(geography_levels)
        geographies = data.get("geographies")
        geographies = parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Geography(geographies)
        group_companies = data.get("group_companies")
        group_companies = parse_structure_VectorType_RecordType_core_GroupCompany(group_companies)
        business_groups = data.get("business_groups")
        business_groups = parse_structure_VectorType_RecordType_core_BusinessGroup(business_groups)
        legal_entities = data.get("legal_entities")
        legal_entities = parse_structure_VectorType_RecordType_core_LegalEntity(legal_entities)
        divisions = data.get("divisions")
        divisions = parse_structure_VectorType_RecordType_core_Division(divisions)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_technotransactions_UNIT(units)
        return GetAssignedStatutoryWizardOneDataSuccess(domains, industries, geography_levels, geographies, group_companies, business_groups, legal_entities, divisions, units)

    def to_inner_structure(self):
        return {
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "industries": to_structure_VectorType_RecordType_core_Industry(self.industries),
            "geography_levels": to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level(self.geography_levels),
            "geographies": to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Geography(self.geographies),
            "group_companies": to_structure_VectorType_RecordType_core_GroupCompany(self.group_companies),
            "business_groups": to_structure_VectorType_RecordType_core_BusinessGroup(self.business_groups),
            "legal_entities": to_structure_VectorType_RecordType_core_LegalEntity(self.legal_entities),
            "divisions": to_structure_VectorType_RecordType_core_Division(self.divisions),
            "units": to_structure_VectorType_RecordType_technotransactions_UNIT(self.units),
        }

class GetStatutoryWizardTwoDataSuccess(Response):
    def __init__(self, statutories):
        self.statutories = statutories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutories"])
        statutories = data.get("statutories")
        statutories = parse_structure_VectorType_RecordType_core_AssignedStatutory(statutories)
        return GetStatutoryWizardTwoDataSuccess(statutories)

    def to_inner_structure(self):
        return {
            "statutories": to_structure_VectorType_RecordType_core_AssignedStatutory(self.statutories),
        }

class SaveAssignedStatutorySuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveAssignedStatutorySuccess()

    def to_inner_structure(self):
        return {
        }


def _init_Response_class_map():
    classes = [GetAssignedStatutoriesListSuccess, GetAssignedStatutoriesByIdSuccess, GetAssignedStatutoryWizardOneDataSuccess, GetStatutoryWizardTwoDataSuccess, SaveAssignedStatutorySuccess]
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
        request = parse_structure_VariantType_technotransactions_Request(request)
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": to_structure_CustomTextType_50(self.session_token),
            "request": to_structure_VariantType_technotransactions_Request(self.request),
        }

#
# ASSIGNED_STATUTORIES
#

class ASSIGNED_STATUTORIES(object):
    def __init__(self, submission_status, client_saved_statutory_id, client_assigned_statutory_id, country_name, group_name, business_group_name, legal_entity_name, division_name, unit_name, geography_name, domain_name):
        self.submission_status = submission_status
        self.client_saved_statutory_id = client_saved_statutory_id
        self.client_assigned_statutory_id = client_assigned_statutory_id
        self.country_name = country_name
        self.group_name = group_name
        self.business_group_name = business_group_name
        self.legal_entity_name = legal_entity_name
        self.division_name = division_name
        self.unit_name = unit_name
        self.geography_name = geography_name
        self.domain_name = domain_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["submission_status", "client_saved_statutory_id", "client_assigned_statutory_id", "country_name", "group_name", "business_group_name", "legal_entity_name", "division_name", "unit_name", "geography_name", "domain_name"])
        submission_status = data.get("submission_status")
        submission_status = parse_structure_EnumType_core_ASSIGN_STATUTORY_SUBMISSION_STATUS(submission_status)
        client_saved_statutory_id = data.get("client_saved_statutory_id")
        client_saved_statutory_id = parse_structure_UnsignedIntegerType_32(client_saved_statutory_id)
        client_assigned_statutory_id = data.get("client_assigned_statutory_id")
        client_assigned_statutory_id = parse_structure_UnsignedIntegerType_32(client_assigned_statutory_id)
        country_name = data.get("country_name")
        country_name = parse_structure_CustomTextType_50(country_name)
        group_name = data.get("group_name")
        group_name = parse_structure_CustomTextType_50(group_name)
        business_group_name = data.get("business_group_name")
        business_group_name = parse_structure_OptionalType_CustomTextType_50(business_group_name)
        legal_entity_name = data.get("legal_entity_name")
        legal_entity_name = parse_structure_CustomTextType_50(legal_entity_name)
        division_name = data.get("division_name")
        division_name = parse_structure_OptionalType_CustomTextType_50(division_name)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_50(unit_name)
        geography_name = data.get("geography_name")
        geography_name = parse_structure_CustomTextType_50(geography_name)
        domain_name = data.get("domain_name")
        domain_name = parse_structure_CustomTextType_50(domain_name)
        return ASSIGNED_STATUTORIES(submission_status, client_saved_statutory_id, client_assigned_statutory_id, country_name, group_name, business_group_name, legal_entity_name, division_name, unit_name, geography_name, domain_name)

    def to_structure(self):
        return {
            "submission_status": to_structure_EnumType_core_ASSIGN_STATUTORY_SUBMISSION_STATUS(self.submission_status),
            "client_saved_statutory_id": to_structure_SignedIntegerType_8(self.client_saved_statutory_id),
            "client_assigned_statutory_id": to_structure_SignedIntegerType_8(self.client_assigned_statutory_id),
            "country_name": to_structure_CustomTextType_50(self.country_name),
            "group_name": to_structure_CustomTextType_50(self.group_name),
            "business_group_name": to_structure_OptionalType_CustomTextType_50(self.business_group_name),
            "legal_entity_name": to_structure_CustomTextType_50(self.legal_entity_name),
            "division_name": to_structure_OptionalType_CustomTextType_50(self.division_name),
            "unit_name": to_structure_CustomTextType_50(self.unit_name),
            "geography_name": to_structure_CustomTextType_50(self.geography_name),
            "domain_name": to_structure_CustomTextType_50(self.domain_name),
        }

#
# UNIT
#

class UNIT(object):
    def __init__(self, unit_id, unit_name, division_id, legal_entity_id, business_group_id, client_id, domain_ids, industry_id, geography_ids):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.division_id = division_id
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id
        self.client_id = client_id
        self.domain_ids = domain_ids
        self.industry_id = industry_id
        self.geography_ids = geography_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_id", "unit_name", "division_id", "legal_entity_id", "business_group_id", "client_id", "domain_ids", "industry_id", "geography_ids"])
        unit_id = data.get("unit_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_100(unit_name)
        division_id = data.get("division_id")
        division_id = parse_structure_OptionalType_SignedIntegerType_8(division_id)
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_UnsignedIntegerType_32(legal_entity_id)
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_OptionalType_SignedIntegerType_8(business_group_id)
        client_id = data.get("client_id")
        client_id = parse_structure_UnsignedIntegerType_32(client_id)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_UnsignedIntegerType_32(domain_ids)
        industry_id = data.get("industry_id")
        industry_id = parse_structure_UnsignedIntegerType_32(industry_id)
        geography_ids = data.get("geography_ids")
        geography_ids = parse_structure_VectorType_UnsignedIntegerType_32(geography_ids)
        return UNIT(unit_id, unit_name, division_id, legal_entity_id, business_group_id, client_id, domain_ids, industry_id, geography_ids)

    def to_structure(self):
        return {
            "unit_id": to_structure_SignedIntegerType_8(self.unit_id),
            "unit_name": to_structure_CustomTextType_100(self.unit_name),
            "division_id": to_structure_OptionalType_SignedIntegerType_8(self.division_id),
            "legal_entity_id": to_structure_SignedIntegerType_8(self.legal_entity_id),
            "business_group_id": to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
            "client_id": to_structure_SignedIntegerType_8(self.client_id),
            "domain_ids": to_structure_VectorType_UnsignedIntegerType_32(self.domain_ids),
            "industry_id": to_structure_SignedIntegerType_8(self.industry_id),
            "geography_ids": to_structure_VectorType_UnsignedIntegerType_32(self.geography_ids),
        }

