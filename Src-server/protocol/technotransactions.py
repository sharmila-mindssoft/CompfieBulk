from protocol.jsonvalidators import (parse_dictionary, parse_static_list)
from protocol.parse_structure import (
    parse_structure_VariantType_technotransactions_Request,
    parse_structure_EnumType_core_ASSIGN_STATUTORY_SUBMISSION_TYPE,
    parse_structure_VectorType_RecordType_core_AssignedStatutory,
    parse_structure_VectorType_RecordType_technotransactions_UNIT,
    parse_structure_VectorType_RecordType_core_LegalEntity,
    parse_structure_OptionalType_CustomTextType_50,
    parse_structure_UnsignedIntegerType_32,
    parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level,
    parse_structure_VectorType_RecordType_core_Industry,
    parse_structure_VectorType_RecordType_core_GroupCompany,
    parse_structure_MapType_UnsignedIntegerType_32_VectorType_RecordType_core_Geography,
    parse_structure_VectorType_RecordType_core_Division,
    parse_structure_VectorType_RecordType_core_BusinessGroup,
    parse_structure_OptionalType_SignedIntegerType_8,
    parse_structure_VectorType_RecordType_technotransactions_ASSIGNED_STATUTORIES,
    parse_structure_CustomTextType_50,
    parse_structure_VectorType_RecordType_core_Domain,
    parse_structure_CustomTextType_100,
    parse_structure_VectorType_UnsignedIntegerType_32,
    parse_structure_OptionalType_UnsignedIntegerType_32,
    parse_structure_MapType_UnsignedIntegerType_32_Bool,
    parse_structure_VectorType_RecordType_technotransactions_AssignedStatutoryCompliance,
    parse_structure_Bool,
    parse_structure_OptionalType_CustomTextType_500,
    parse_structure_SignedIntegerType_8,
    parse_structure_maptype_signedIntegerType_8_VectorType_RecordType_core_ComplianceApplicability

)
from protocol.to_structure import (
    to_structure_VariantType_technotransactions_Request,
    to_structure_EnumType_core_ASSIGN_STATUTORY_SUBMISSION_TYPE,
    to_structure_VectorType_RecordType_core_AssignedStatutory,
    to_structure_VectorType_RecordType_technotransactions_UNIT,
    to_structure_VectorType_RecordType_core_LegalEntity,
    to_structure_OptionalType_CustomTextType_50,
    to_structure_SignedIntegerType_8,
    to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Level,
    to_structure_VectorType_RecordType_core_Industry,
    to_structure_VectorType_RecordType_core_GroupCompany,
    to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Geography,
    to_structure_VectorType_RecordType_core_Division,
    to_structure_VectorType_RecordType_core_BusinessGroup,
    to_structure_OptionalType_SignedIntegerType_8,
    to_structure_VectorType_RecordType_technotransactions_ASSIGNED_STATUTORIES,
    to_structure_CustomTextType_50,
    to_structure_VectorType_RecordType_core_Domain,
    to_structure_CustomTextType_100,
    to_structure_VectorType_UnsignedIntegerType_32,
    to_structure_OptionalType_UnsignedIntegerType_32,
    to_structure_MapType_UnsignedIntegerType_32_Bool,
    to_structure_VectorType_RecordType_technotransactions_AssignedStatutoryCompliance,
    to_structure_Bool,
    to_structure_OptionalType_CustomTextType_500,
    to_structure_maptype_signedIntegerType_8_VectorType_RecordType_core_ComplianceApplicability,
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
    def __init__(self, client_statutory_id):
        self.client_statutory_id = client_statutory_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["client_statutory_id"])
        client_statutory_id = data.get("client_statutory_id")
        client_statutory_id = parse_structure_UnsignedIntegerType_32(client_statutory_id)
        return GetAssignedStatutoriesById(client_statutory_id)

    def to_inner_structure(self):
        return {
            "client_statutory_id": to_structure_SignedIntegerType_8(self.client_statutory_id),
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
            "country_id": to_structure_UnsignedIntegerType_32(self.country_id)
        }

class GetStatutoryWizardTwoData(Request):
    def __init__(self, country_id, geography_id, industry_id, domain_id, unit_id):
        self.country_id = country_id
        self.geography_id = geography_id
        self.industry_id = industry_id
        self.domain_id = domain_id
        self.unit_id = unit_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "geography_id", "industry_id", "domain_id", "unit_id"])
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        geography_id = data.get("geography_id")
        geography_id = parse_structure_UnsignedIntegerType_32(geography_id)
        industry_id = data.get("industry_id")
        industry_id = parse_structure_UnsignedIntegerType_32(industry_id)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        unit_id = data.get("unit_id")
        unit_id = parse_structure_OptionalType_SignedIntegerType_8(unit_id)
        return GetStatutoryWizardTwoData(country_id, geography_id, industry_id, domain_id, unit_id)

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "geography_id": to_structure_SignedIntegerType_8(self.geography_id),
            "industry_id": to_structure_SignedIntegerType_8(self.industry_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "unit_id": to_structure_SignedIntegerType_8(self.unit_id)
        }

class AssignedStatutoryCompliance(object):
    def __init__(
        self, level_1_statutory_id, compliances,
        applicable_status, not_applicable_remarks
    ):
        self.level_1_statutory_id = level_1_statutory_id
        self.compliances = compliances
        self.applicable_status = applicable_status
        self.not_applicable_remarks = not_applicable_remarks

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["level_1_s_id", "compliances", "a_status", "n_a_remarks"])
        level_1_statutory_id = data.get("level_1_s_id")
        level_1_statutory_id = parse_structure_UnsignedIntegerType_32(level_1_statutory_id)
        compliances = data.get("compliances")
        compliances = parse_structure_MapType_UnsignedIntegerType_32_Bool(compliances)
        applicable_status = data.get("a_status")
        applicable_status = parse_structure_Bool(applicable_status)
        not_applicable_remarks = data.get("n_a_remarks")
        not_applicable_remarks = parse_structure_OptionalType_CustomTextType_500(not_applicable_remarks)
        return AssignedStatutoryCompliance(level_1_statutory_id, compliances, applicable_status, not_applicable_remarks)

    def to_structure(self):
        return {
            "level_1_s_id": to_structure_UnsignedIntegerType_32(self.level_1_statutory_id),
            "compliances": to_structure_MapType_UnsignedIntegerType_32_Bool(self.compliances),
            "a_status": to_structure_Bool(self.applicable_status),
            "n_a_remarks": to_structure_OptionalType_CustomTextType_500(self.not_applicable_remarks)
        }

class SaveAssignedStatutory(Request):
    def __init__(
        self, country_id, client_id, geography_id,
        unit_ids, domain_id,
        submission_type, client_statutory_id,
        assigned_statutories
    ):
        self.country_id = country_id
        self.client_id = client_id
        self.geography_id = geography_id
        self.unit_ids = unit_ids
        self.domain_id = domain_id
        self.submission_type = submission_type
        self.client_statutory_id = client_statutory_id
        self.assigned_statutories = assigned_statutories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_id", "client_id", "g_id", "u_ids", "d_id",  "sub_type", "c_s_id", "a_statutories"])
        country_id = data.get("c_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        client_id = data.get("client_id")
        client_id = parse_structure_UnsignedIntegerType_32(client_id)
        geography_id = data.get("g_id")
        geography_id = parse_structure_UnsignedIntegerType_32(geography_id)
        unit_ids = data.get("u_ids")
        unit_ids = parse_structure_VectorType_UnsignedIntegerType_32(unit_ids)
        domain_id = data.get("d_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        submission_type = data.get("sub_type")
        submission_type = parse_structure_EnumType_core_ASSIGN_STATUTORY_SUBMISSION_TYPE(submission_type)
        client_statutory_id = data.get("c_s_id")
        client_statutory_id = parse_structure_OptionalType_UnsignedIntegerType_32(client_statutory_id)
        assigned_statutories = data.get("a_statutories")
        assigned_statutories = parse_structure_VectorType_RecordType_technotransactions_AssignedStatutoryCompliance(assigned_statutories)
        return SaveAssignedStatutory(country_id, client_id, geography_id, unit_ids, domain_id, submission_type, client_statutory_id, assigned_statutories)

    def to_inner_structure(self):
        return {
            "c_id": to_structure_UnsignedIntegerType_32(self.country_id),
            "client_id": to_structure_UnsignedIntegerType_32(self.client_id),
            "g_id": to_structure_UnsignedIntegerType_32(self.geography_id),
            "u_ids": to_structure_VectorType_UnsignedIntegerType_32(self.unit_ids),
            "d_id": to_structure_UnsignedIntegerType_32(self.domain_id),
            "sub_type": to_structure_EnumType_core_ASSIGN_STATUTORY_SUBMISSION_TYPE(self.submission_type),
            "c_s_id": to_structure_OptionalType_UnsignedIntegerType_32(self.client_statutory_id),
            "a_statutories": to_structure_VectorType_RecordType_technotransactions_AssignedStatutoryCompliance(self.assigned_statutories),
        }

class GetCountriesForGroup(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetCountriesForGroup()

    def to_inner_structure(self):
        return {
        }

def _init_Request_class_map():
    classes = [
        GetAssignedStatutoriesList,
        GetAssignedStatutoriesById,
        GetAssignedStatutoryWizardOneData,
        GetStatutoryWizardTwoData,
        SaveAssignedStatutory,
        GetCountriesForGroup
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
    def __init__(
        self, country_name, group_name, business_group_name,
        legal_entity_name, division_name, unit_name, geography_name,
        domain_name, statutories, new_compliances,
        industry_name
    ):
        self.country_name = country_name
        self.group_name = group_name
        self.business_group_name = business_group_name
        self.legal_entity_name = legal_entity_name
        self.division_name = division_name
        self.unit_name = unit_name
        self.geography_name = geography_name
        self.domain_name = domain_name
        self.statutories = statutories
        self.new_compliances = new_compliances
        self.industry_name = industry_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_name", "group_name", "business_group_name",
            "legal_entity_name", "division_name", "unit_name",
            "geography_name", "domain_name", "statutories",
            "new_compliances", "industry_name"
        ])
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
        unit_name = parse_structure_CustomTextType_100(unit_name)
        geography_name = data.get("geography_name")
        geography_name = parse_structure_CustomTextType_50(geography_name)
        domain_name = data.get("domain_name")
        domain_name = parse_structure_CustomTextType_50(domain_name)
        statutories = data.get("statutories")
        statutories = parse_structure_VectorType_RecordType_core_AssignedStatutory(statutories)
        new_compliances = data.get("new_compliances")
        new_compliances = parse_structure_maptype_signedIntegerType_8_VectorType_RecordType_core_ComplianceApplicability(new_compliances)
        industry_name = data.get("industry_name")
        industry_name = parse_structure_CustomTextType_100(industry_name)
        return GetAssignedStatutoriesByIdSuccess(
            country_name, group_name, business_group_name,
            legal_entity_name, division_name, unit_name, geography_name,
            domain_name, statutories, new_compliances,
            industry_name
        )

    def to_inner_structure(self):
        return {
            "country_name": to_structure_CustomTextType_50(self.country_name),
            "group_name": to_structure_CustomTextType_50(self.group_name),
            "business_group_name": to_structure_OptionalType_CustomTextType_50(self.business_group_name),
            "legal_entity_name": to_structure_CustomTextType_50(self.legal_entity_name),
            "division_name": to_structure_OptionalType_CustomTextType_50(self.division_name),
            "unit_name": to_structure_CustomTextType_100(self.unit_name),
            "geography_name": to_structure_CustomTextType_50(self.geography_name),
            "domain_name": to_structure_CustomTextType_50(self.domain_name),
            "statutories": to_structure_VectorType_RecordType_core_AssignedStatutory(self.statutories),
            "new_compliances": to_structure_maptype_signedIntegerType_8_VectorType_RecordType_core_ComplianceApplicability(self.new_compliances),
            "industry_name": to_structure_CustomTextType_100(self.industry_name)
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
        geographies = parse_structure_MapType_UnsignedIntegerType_32_VectorType_RecordType_core_Geography(geographies)
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
    def __init__(
        self, submission_status, client_statutory_id,
        country_id, country_name,
        client_id, group_name, business_group_name,
        legal_entity_name, division_name,
        unit_id, unit_name,
        geography_id, geography_name, domain_id, domain_name, industry_name
    ):
        self.submission_status = submission_status
        self.client_statutory_id = client_statutory_id
        self.country_id = country_id
        self.country_name = country_name
        self.client_id = client_id
        self.group_name = group_name
        self.business_group_name = business_group_name
        self.legal_entity_name = legal_entity_name
        self.division_name = division_name
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.geography_id = geography_id
        self.geography_name = geography_name
        self.domain_id = domain_id
        self.domain_name = domain_name
        self.industry_name = industry_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "submission_status", "client_statutory_id",
            "country_id", "country_name", "client_id",
            "group_name", "business_group_name", "legal_entity_name",
            "division_name", "unit_id", "unit_name",
            "geography_id", "geography_name",
            "domain_id", "domain_name", "industry_name"
        ])
        submission_status = data.get("submission_status")
        submission_status = parse_structure_SignedIntegerType_8(submission_status)
        client_statutory_id = data.get("client_statutory_id")
        client_statutory_id = parse_structure_UnsignedIntegerType_32(client_statutory_id)
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        country_name = data.get("country_name")
        country_name = parse_structure_CustomTextType_50(country_name)
        client_id = data.get("client_id")
        client_id = parse_structure_UnsignedIntegerType_32(client_id)
        group_name = data.get("group_name")
        group_name = parse_structure_CustomTextType_50(group_name)
        business_group_name = data.get("business_group_name")
        business_group_name = parse_structure_OptionalType_CustomTextType_50(business_group_name)
        legal_entity_name = data.get("legal_entity_name")
        legal_entity_name = parse_structure_CustomTextType_50(legal_entity_name)
        division_name = data.get("division_name")
        division_name = parse_structure_OptionalType_CustomTextType_50(division_name)
        unit_id = data.get("unit_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_100(unit_name)
        geography_id = data.get("geography_id")
        geography_id = parse_structure_UnsignedIntegerType_32(geography_id)
        geography_name = data.get("geography_name")
        geography_name = parse_structure_CustomTextType_50(geography_name)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        domain_name = data.get("domain_name")
        domain_name = parse_structure_CustomTextType_50(domain_name)
        industry_name = data.get("industry_name")
        industry_name = parse_structure_CustomTextType_50(industry_name)
        return ASSIGNED_STATUTORIES(
            submission_status, client_statutory_id,
            country_id, country_name, client_id, group_name,
            business_group_name, legal_entity_name,
            division_name, unit_id, unit_name, geography_id,
            geography_name, domain_id, domain_name, industry_name
        )

    def to_structure(self):
        return {
            "submission_status": to_structure_SignedIntegerType_8(self.submission_status),
            "client_statutory_id": to_structure_SignedIntegerType_8(self.client_statutory_id),
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "country_name": to_structure_CustomTextType_50(self.country_name),
            "client_id": to_structure_SignedIntegerType_8(self.client_id),
            "group_name": to_structure_CustomTextType_50(self.group_name),
            "business_group_name": to_structure_OptionalType_CustomTextType_50(self.business_group_name),
            "legal_entity_name": to_structure_CustomTextType_50(self.legal_entity_name),
            "division_name": to_structure_OptionalType_CustomTextType_50(self.division_name),
            "unit_id": to_structure_SignedIntegerType_8(self.unit_id),
            "unit_name": to_structure_CustomTextType_100(self.unit_name),
            "geography_id": to_structure_SignedIntegerType_8(self.geography_id),
            "geography_name": to_structure_CustomTextType_50(self.geography_name),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "domain_name": to_structure_CustomTextType_50(self.domain_name),
            "industry_name": to_structure_CustomTextType_50(self.industry_name)
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

