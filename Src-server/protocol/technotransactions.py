from protocol.jsonvalidators import (
    parse_dictionary, parse_static_list, parse_VariantType,
    to_VariantType, to_structure_dictionary_values
)
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
    parse_structure_maptype_signedIntegerType_8_VectorType_RecordType_core_ComplianceApplicability,
    parse_structure_CustomTextType_20

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
    to_structure_UnsignedIntegerType_32,
    to_structure_CustomTextType_20

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


class GetAssignedStatutories(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetAssignedStatutories()

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
        return GetAssignedStatutoriesById(client_statutory_id)

    def to_inner_structure(self):
        return {
            "client_statutory_id": self.client_statutory_id,
        }


class GetAssignedStatutoryWizardOneData(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetAssignedStatutoryWizardOneData()

    def to_inner_structure(self):
        return {}


class GetAssignedStatutoryWizardTwoData(Request):
    def __init__(
        self, client_id, business_group_id, legal_entity_id, division_id,
        category_id, domain_id_optional, unit_ids
    ):
        self.client_id = client_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.category_id = category_id
        self.domain_id_optional = domain_id_optional
        self.unit_ids = unit_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "client_id", "business_group_id", "legal_entity_id", "division_id",
            "category_id", "domain_id_optional", "unit_ids"
        ])
        client_id = data.get("client_id")
        business_group_id = data.get("business_group_id")
        legal_entity_id = data.get("legal_entity_id")
        division_id = data.get("division_id")
        category_id = data.get("category_id")
        domain_id_optional = data.get("domain_id_optional")
        unit_ids = data.get("unit_ids")
        return GetAssignedStatutoryWizardTwoData(
            client_id, business_group_id, legal_entity_id, division_id,
            category_id, domain_id_optional, unit_ids
        )

    def to_inner_structure(self):
        return {
            "client_id": self.client_id,
            "business_group_id": self.business_group_id,
            "legal_entity_id": self.legal_entity_id,
            "division_id": self.division_id,
            "category_id": self.category_id,
            "domain_id_optional": self.domain_id_optional,
            "unit_ids": self.unit_ids
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


class ComplianceApplicablityStatus(object):
    def __init__(
        self, compliance_id, compliance_applicability_status,
        is_saved, statutory_applicability_status
    ):
        self.compliance_id = compliance_id
        self.compliance_applicability_status = compliance_applicability_status
        self.is_saved = is_saved
        self.statutory_applicability_status = statutory_applicability_status

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "compliance_id", "compliance_applicability_status",
                "statutory_applicability_status", "is_saved"
            ]
        )
        return ComplianceApplicablityStatus(
            data.get("compliance_id"),  data.get("compliance_applicability_status"),
            data.get("statutory_applicability_status"), data.get("is_saved")
        )

    def to_structure(self):
        return {
            "compliance_id": self.compliance_id,
            "compliance_applicability_status": self.compliance_applicability_status,
            "statutory_applicability_status": self.statutory_applicability_status,
            "is_saved": self.is_saved
        }


class SaveAssignedStatutory(Request):
    def __init__(
        self, client_statutory_id, unit_id_name, client_id, compliances_applicablity_status,
        level_1_statutory_wise_compliances , unit_ids, submission_type
    ):
        self.client_statutory_id = client_statutory_id
        self.unit_id_name = unit_id_name
        self.client_id = client_id
        self.unit_ids = unit_ids
        self.compliances_applicablity_status = compliances_applicablity_status
        self.level_1_statutory_wise_compliances = level_1_statutory_wise_compliances
        self.submission_type = submission_type

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "client_statutory_id", "unit_id_name", "client_id", "compliances_applicablity_status",
                "level_1_statutory_wise_compliances", "unit_ids", "submission_type"
            ]
        )
        return SaveAssignedStatutory(
            data.get("client_statutory_id"), data.get("unit_id_name"),  data.get("client_id"),
            data.get("compliances_applicablity_status"),
            data.get("level_1_statutory_wise_compliances"), data.get("unit_ids"),
            data.get("submission_type")
        )

    def to_inner_structure(self):
        return {
            "client_statutory_id": self.client_statutory_id,
            "unit_id_name": self.unit_id_name,
            "client_id": self.client_id,
            "unit_ids": self.unit_ids,
            "compliances_applicablity_status": self.compliances_applicablity_status,
            "unit_ids": self.unit_ids,
            "submission_type": self.submission_type
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
        GetAssignedStatutories,
        GetAssignedStatutoriesById,
        GetAssignedStatutoryWizardOneData,
        GetAssignedStatutoryWizardTwoData,
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
        print "inner: %s" % inner
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


class GetAssignedStatutoriesSuccess(Response):
    def __init__(self, assigned_statutories):
        self.assigned_statutories = assigned_statutories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["assigned_statutories"])
        assigned_statutories = data.get("assigned_statutories")
        return GetAssignedStatutoriesSuccess(assigned_statutories)

    def to_inner_structure(self):
        return {
            "assigned_statutories": self.assigned_statutories,
        }


class GetAssignedStatutoriesByIdSuccess(Response):
    def __init__(self, level_1_statutories_list, statutories_for_assigning):
        self.level_1_statutories_list = level_1_statutories_list
        self.statutories_for_assigning = statutories_for_assigning

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "level_1_statutories_list", "statutories_for_assigning"
        ])
        level_1_statutories_list = data.get("level_1_statutories_list")
        statutories_for_assigning = data.get("statutories_for_assigning")
        return GetAssignedStatutoryWizardTwoDataSuccess(
            level_1_statutories_list, statutories_for_assigning
        )

    def to_inner_structure(self):
        return {
            "level_1_statutories_list": self.level_1_statutories_list,
            "statutories_for_assigning": self.statutories_for_assigning,
        }


class GetAssignedStatutoryWizardOneDataSuccess(Response):
    def __init__(
        self, clients, business_groups, unit_legal_entity, divisions,
        categories, domains, unit_id_name
    ):
        self.clients = clients
        self.business_groups = business_groups
        self.unit_legal_entity = unit_legal_entity
        self.divisions = divisions
        self.categories = categories
        self.domains = domains
        self.unit_id_name = unit_id_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "clients", "business_groups", "unit_legal_entity",
                "divisions", "categories", "domains", "unit_id_name"
            ])
        clients = data.get("clients")
        business_groups = data.get("business_groups")
        unit_legal_entity = data.get("unit_legal_entity")
        divisions = data.get("divisions")
        categories = data.get("categories")
        domains = data.get("domains")
        unit_id_name = data.get("unit_id_name")
        return GetAssignedStatutoryWizardOneDataSuccess(
            clients, business_groups, unit_legal_entity, divisions,
            categories, domains, unit_id_name
        )

    def to_inner_structure(self):
        return {
            "clients": self.clients,
            "business_groups": self.business_groups,
            "unit_legal_entity": self.unit_legal_entity,
            "divisions": self.divisions,
            "categories": self.categories,
            "domains": self.domains,
            "unit_id_name": self.unit_id_name
        }


class AssignStatutoryCompliance(object):
    def __init__(
        self, level_1_statutory_index, statutory_provision, compliance_id,
        document_name, compliance_name, description, organizations, locations
    ):
        self.level_1_statutory_index = level_1_statutory_index
        self.statutory_provision = statutory_provision
        self.compliance_id = compliance_id
        self.document_name = document_name
        self.compliance_name = compliance_name
        self.description = description
        self.organizations = organizations
        self.locations = locations

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "level_1_statutory_index", "statutory_provision", "compliance_id",
            "document_name", "compliance_name", "description",
            "organizations", "locations"
        ])
        level_1_statutory_index = data.get("level_1_statutory_index")
        statutory_provision = data.get("statutory_provision")
        compliance_id = data.get("compliance_id")
        document_name = data.get("document_name")
        compliance_name = data.get("compliance_name")
        description = data.get("description")
        organizations = data.get("organizations")
        locations = data.get("locations")
        return AssignStatutoryCompliance(
            level_1_statutory_index, statutory_provision, compliance_id,
            document_name, compliance_name, description,
            organizations, locations
        )

    def to_structure(self):
        return {
            "level_1_statutory_index": self.level_1_statutory_index,
            "statutory_provision": self.statutory_provision,
            "compliance_id": self.compliance_id,
            "document_name": self.document_name,
            "compliance_name": self.compliance_name,
            "description": self.description,
            "organizations": self.organizations,
            "locations": self.locations
        }


class GetAssignedStatutoryWizardTwoDataSuccess(Response):
    def __init__(self, level_1_statutories_list, statutories_for_assigning):
        self.level_1_statutories_list = level_1_statutories_list
        self.statutories_for_assigning = statutories_for_assigning

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "level_1_statutories_list", "statutories_for_assigning"
        ])
        level_1_statutories_list = data.get("level_1_statutories_list")
        statutories_for_assigning = data.get("statutories_for_assigning")
        return GetAssignedStatutoryWizardTwoDataSuccess(
            level_1_statutories_list, statutories_for_assigning
        )

    def to_inner_structure(self):
        return {
            "level_1_statutories_list": self.level_1_statutories_list,
            "statutories_for_assigning": self.statutories_for_assigning,
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
    classes = [
        GetAssignedStatutoriesSuccess, GetAssignedStatutoriesByIdSuccess,
        GetAssignedStatutoryWizardOneDataSuccess,
        GetAssignedStatutoryWizardTwoDataSuccess,
        SaveAssignedStatutorySuccess
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
            request, "technotransactions", "Request"
        )
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": to_VariantType(
                self.request, "technotransactions", "Response"
            ),
        }

#
# ASSIGNED_STATUTORIES
#

class AssignedStatutories(object):
    def __init__(
        self, submission_status, client_statutory_id, country_id, country_name,
        client_id, group_name, business_group_id, business_group_name,
        legal_entity_id, legal_entity_name, division_id, division_name, unit_id, unit_code_with_name, 
        geography_id, geography_name, domain_ids, domain_names, category_id, category_name
    ):
        self.submission_status = submission_status
        self.client_statutory_id = client_statutory_id
        self.country_id = country_id
        self.country_name = country_name
        self.client_id = client_id
        self.group_name = group_name
        self.business_group_id = business_group_id
        self.business_group_name = business_group_name
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.division_id = division_id
        self.division_name = division_name
        self.unit_id = unit_id
        self.unit_code_with_name = unit_code_with_name
        self.geography_id = geography_id
        self.geography_name = geography_name
        self.domain_ids = domain_ids
        self.domain_names = domain_names
        self.category_id = category_id
        self.category_name = category_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "submission_status", "client_statutory_id", "country_id", "country_name",
            "client_id", "group_name", "busiess_group_id", "business_group_name",
            "legal_entity_id", "legal_entity_name", "division_id", "division_name",
            "unit_id", "unit_code_with_name", "geography_id", "geography_name", "domain_ids",
            "domain_names", "category_id", "category_name"
        ])
        submission_status = data.get("submission_status")
        client_statutory_id = data.get("client_statutory_id")
        country_id = data.get("country_id")
        country_name = data.get("country_name")
        client_id = data.get("client_id")
        group_name = data.get("group_name")
        business_group_id = data.get("business_group_id")
        business_group_name = data.get("business_group_name")
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_name = data.get("legal_entity_name")
        division_id = data.get("division_id")
        division_name = data.get("division_name")
        unit_id = data.get("unit_id")
        unit_code_with_name = data.get("unit_code_with_name")
        geography_id = data.get("geography_id")
        geography_name = data.get("geography_name")
        domain_ids = data.get("domain_ids")
        domain_names = data.get("domain_names")
        category_id = data.get("category_id")
        category_name = data.get("category_name")
        return AssignedStatutories(
            submission_status, client_statutory_id, country_id, country_name,
            client_id, group_name, business_group_id, business_group_name,
            legal_entity_id, legal_entity_name, division_id, division_name,
            unit_code_with_name, unit_name, geography_id, geography_name, domain_ids,
            domain_names, category_id, category_name
        )

    def to_structure(self):
        return {
            "submission_status": self.submission_status,
            "client_statutory_id": self.client_statutory_id,
            "country_id": self.country_id,
            "country_name": self.country_name,
            "client_id": self.client_id,
            "group_name": self.group_name,
            "business_group_id": self.business_group_id,
            "business_group_name": self.business_group_name,
            "legal_entity_id": self.legal_entity_id,
            "legal_entity_name": self.legal_entity_name,
            "division_id": self.division_id,
            "division_name": self.division_name,
            "unit_id": self.unit_id,
            "unit_code_with_name": self.unit_code_with_name,
            "geography_id": self.geography_id,
            "geography_name": self.geography_name,
            "domain_ids": self.domain_ids,
            "domain_names": self.domain_names,
            "category_id": self.category_id,
            "category_name": self.category_name
        }

