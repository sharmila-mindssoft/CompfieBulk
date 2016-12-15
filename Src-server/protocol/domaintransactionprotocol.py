from protocol.jsonvalidators import (
    parse_dictionary, parse_static_list, parse_VariantType,
    to_VariantType, to_structure_dictionary_values
)
from protocol.parse_structure import (
    parse_structure_UnsignedIntegerType_32,
    parse_structure_MapType_UnsignedIntegerType_32_Bool,
    parse_structure_Bool,
    parse_structure_OptionalType_CustomTextType_500,

)
from protocol.to_structure import (
    to_structure_UnsignedIntegerType_32,
    to_structure_MapType_UnsignedIntegerType_32_Bool,
    to_structure_Bool,
    to_structure_OptionalType_CustomTextType_500,
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


class GetAssignedStatutoryWizardOneUnits(Request):
    def __init__(
        self, client_id, business_group_id, legal_entity_id,
        division_id, category_id,  domain_id
    ):
        self.client_id = client_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.category_id = category_id
        self.domain_id = domain_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["ct_id", "bg_id", "le_id", "dv_id", "cat_id", "d_id"])
        client_id = data.get("ct_id")
        business_group_id = data.get("bg_id")
        legal_entity_id = data.get("le_id")
        division_id = data.get("dv_id")
        category_id = data.get("cat_id")
        domain_id = data.get("d_id")
        return GetAssignedStatutoryWizardOneUnits(
            client_id, business_group_id, legal_entity_id, division_id, category_id, domain_id
        )

    def to_inner_structure(self):
        return {
            "ct_id": self.client_id,
            "bg_id": self.business_group_id,
            "le_id": self.legal_entity_id,
            "dv_id": self.division_id,
            "cat_id": self.category_id,
            "d_id": self.domain_id
        }

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

def _init_Request_class_map():
    classes = [
        GetAssignedStatutories,
        GetAssignedStatutoriesById,
        GetAssignedStatutoryWizardOneData,
        GetAssignedStatutoryWizardTwoData,
        SaveAssignedStatutory,
        GetAssignedStatutoryWizardOneUnits
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

class getGroupAdminGroupsUnitsSuccess(Response):
    def __init__(self, groupadmin_groupList, groupadmin_unitList):
        self.groupadmin_groupList = groupadmin_groupList
        self.groupadmin_unitList = groupadmin_unitList

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "groupadmin_groupList", "groupadmin_unitList"
        ])
        groupadmin_groupList = data.get("groupadmin_groupList")
        groupadmin_unitList = data.get("groupadmin_unitList")
        return getGroupAdminGroupsUnitsSuccess(
            groupadmin_groupList, groupadmin_unitList
        )

    def to_inner_structure(self):
        print "inside protocol"
        return {
            "groupadmin_groupList": self.groupadmin_groupList,
            "groupadmin_unitList": self.groupadmin_unitList,
        }

class GetAssignedStatutoryWizardOneDataSuccess(Response):
    def __init__(
        self, clients, business_groups, unit_legal_entity, divisions,
        categories, domains
    ):
        self.clients = clients
        self.business_groups = business_groups
        self.unit_legal_entity = unit_legal_entity
        self.divisions = divisions
        self.categories = categories
        self.domains = domains

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "grps", "bgrps", "lety",
                "divs", "cates", "dms"
            ])
        clients = data.get("grps")
        business_groups = data.get("bgrps")
        unit_legal_entity = data.get("lety")
        divisions = data.get("divs")
        categories = data.get("cates")
        domains = data.get("dms")

        return GetAssignedStatutoryWizardOneDataSuccess(
            clients, business_groups, unit_legal_entity, divisions,
            categories, domains
        )

    def to_inner_structure(self):
        return {
            "grps": self.clients,
            "bgrps": self.business_groups,
            "lety": self.unit_legal_entity,
            "divs": self.divisions,
            "cates": self.categories,
            "dms": self.domains,

        }

class GetAssignedStatutoryWizardOneUnitsSuccess(Response):
    def __init__(self, units):
        self.units = units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statu_units"])
        assigned_statutories = data.get("statu_units")
        return GetAssignedStatutoryWizardOneUnitsSuccess(assigned_statutories)

    def to_inner_structure(self):
        return {
            "statu_units": self.units,
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
        SaveAssignedStatutorySuccess,
        getGroupAdminGroupsUnitsSuccess,
        GetAssignedStatutoryWizardOneUnitsSuccess
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
            request, "domaintransactionprotocol", "Request"
        )
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": to_VariantType(
                self.request, "domaintransactionprotocol", "Response"
            ),
        }

#
# ASSIGNED_STATUTORIES
#

class AssignedStatutories(object):
    def __init__(
        self, country_name,
        client_id, group_name, business_group_name,
        legal_entity_name, division_name, unit_code_with_name,
        geography_name, unit_id, domain_id, domain_name, category_name,
        approve_status, approved_status_id
    ):
        self.country_name = country_name
        self.client_id = client_id
        self.group_name = group_name
        self.business_group_name = business_group_name
        self.legal_entity_name = legal_entity_name
        self.division_name = division_name
        self.unit_code_with_name = unit_code_with_name
        self.geography_name = geography_name
        self.unit_id = unit_id
        self.domain_id = domain_id
        self.domain_name = domain_name
        self.category_name = category_name
        self.submission_status = approve_status
        self.approved_status_id = approved_status_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "c_name", "ct_id", "grp_name", "b_grp_name",
            "l_e_name", "div_name",
            "u_id", "u_name", "g_name", "d_id",
            "d_name", "cat_name", "approval_status_text", "a_s_id"
        ])
        country_name = data.get("c_name")
        client_id = data.get("ct_id")
        group_name = data.get("grp_name")
        business_group_name = data.get("b_grp_name")
        legal_entity_name = data.get("l_e_name")
        division_name = data.get("div_name")
        unit_id = data.get("u_id")
        unit_code_with_name = data.get("u_name")
        geography_name = data.get("g_name")
        domain_id = data.get("d_id")
        domain_name = data.get("d_name")
        category_name = data.get("cat_name")
        submission_status = data.get("approval_status_text")
        approved_status_id = data.get("a_s_id")
        return AssignedStatutories(
            country_name,
            client_id, group_name, business_group_name,
            legal_entity_name, division_name,
            unit_code_with_name, geography_name, unit_id, domain_id,
            domain_name, category_name,
            submission_status, approved_status_id
        )

    def to_structure(self):
        return {

            "c_name": self.country_name,
            "ct_id": self.client_id,
            "grp_name": self.group_name,
            "b_grp_name": self.business_group_name,
            "l_e_name": self.legal_entity_name,
            "div_name": self.division_name,
            "u_id": self.unit_id,
            "u_name": self.unit_code_with_name,
            "g_name": self.geography_name,
            "d_id": self.domain_id,
            "d_name": self.domain_name,
            "cat_name": self.category_name,
            "approval_status_text": self.submission_status,
            "a_s_id": self.approved_status_id
        }

class LegalentityDomains(object):
    def __init__(
        self, legal_entity_id, domain_id, domain_name
    ):
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.domain_name = domain_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "legal_entity_id", "domain_id", "domain_name"
            ]
        )
        legal_entity_id = data.get("legal_entity_id")
        domain_id = data.get("domain_id")
        domain_name = data.get("domain_name")
        return LegalentityDomains(legal_entity_id, domain_id, domain_name)

    def to_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id,
            "domain_id": self. domain_id,
            "domain_name": self.domain_name
        }

class StatutoryUnits(object):
    def __init__(
        self, unit_id, unit_code, unit_name, address, geography_name
    ):
        self.unit_id = unit_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.address = address
        self.geography_name = geography_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "u_id", "unit_code", "u_name", "address", "g_name"
            ]
        )
        unit_id = data.get("u_id")
        unit_code = data.get("unit_code")
        unit_name = data.get("u_name")
        address = data.get("address")
        geography = data.get("g_name")
        return StatutoryUnits(unit_id, unit_code, unit_name, address, geography)

    def to_structure(self):
        return {
            "u_id": self.unit_id,
            "unit_code": self.unit_code,
            "u_name": self.unit_name,
            "address": self.address,
            "g_name": self. geography_name
        }
