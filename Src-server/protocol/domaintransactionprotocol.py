from protocol.jsonvalidators import (
    parse_dictionary, parse_static_list, parse_VariantType,
    to_VariantType, to_structure_dictionary_values
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

class GetAssignedStatutoriesForApprove(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetAssignedStatutoriesForApprove()

    def to_inner_structure(self):
        return {}


class GetAssignedStatutoriesById(Request):
    def __init__(self, unit_id, domain_id):
        self.unit_id = unit_id
        self.domain_id = domain_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["u_id", "d_id"])
        unit_id = data.get("u_id")
        domain_id = data.get("d_id")
        return GetAssignedStatutoriesById(unit_id, domain_id)

    def to_inner_structure(self):
        return {
            "u_id": self.unit_id,
            "d_id": self.domain_id
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
        self, unit_ids, domain_id
    ):
        self.unit_ids = unit_ids
        self.domain_id = domain_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "unit_ids", "d_id"
        ])
        domain_id = data.get("d_id")
        unit_ids = data.get("unit_ids")
        return GetAssignedStatutoryWizardTwoData(
            unit_ids, domain_id
        )

    def to_inner_structure(self):
        return {
            "unit_ids": self.unit_ids,
            "d_id": self.domain_id
        }


class SaveAssignedStatutory(Request):
    def __init__(
        self, compliances_applicablity_status, submission_type
    ):
        self.compliances_applicablity_status = compliances_applicablity_status
        self.submission_type = submission_type

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "compliances_applicablity_status",
                "submission_status"
            ]
        )
        return SaveAssignedStatutory(
            data.get("compliances_applicablity_status"),
            data.get("submission_status")
        )

    def to_inner_structure(self):
        return {
            "compliances_applicablity_status": self.compliances_applicablity_status,
            "submission_status": self.submission_type
        }


class ApproveAssignedStatutory(Request):
    def __init__(
        self, unit_id, domain_id, client_statutory_id, compliance_ids,
        submission_type, remarks
    ):
        self.unit_id = unit_id
        self.domain_id = domain_id
        self.client_statutory_id = client_statutory_id
        self.compliance_ids = compliance_ids
        self.submission_type = submission_type
        self.remarks = remarks

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "u_id", "d_id", "client_statutory_id", "comp_ids"
                "submission_status", "remarks"
            ]
        )
        return SaveAssignedStatutory(
            data.get("u_id"),
            data.get("d_id"),
            data.get("client_statutory_id"),
            data.get("comp_ids"),
            data.get("submission_status"),
            data.get("remarks")
        )

    def to_inner_structure(self):
        return {
            "u_id": self.unit_id,
            "d_id": self.domain_id,
            "client_statutory_id": self.client_statutory_id,
            "comp_ids": self.compliance_ids,
            "submission_status": self.submission_type,
            "remarks": self.remarks
        }


class SaveComplianceStatus(object):
    def __init__(
        self, client_id, legal_entity_id, unit_id, domain_id,
        compliance_id, compliance_status,
        level_1_id, status, remarks, client_statutory_id

    ):
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.unit_id = unit_id
        self.domain_id = domain_id
        self.compliance_id = compliance_id
        self.compliance_status = compliance_status
        self.level_1_id = level_1_id
        self.status = status
        self.remarks = remarks
        self.client_statutory_id = client_statutory_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "ct_id", "le_id", "u_id", "d_id",
            "comp_id", "comp_status",
            "level_1_s_id",
            "a_status", "remarks", "client_statutory_id"
        ])

        client_id = data.get("ct_id")
        legal_entity_id = data.get("le_id")
        unit_id = data.get("u_id")
        domain_id = data.get("d_id")
        compliance_id = data.get("comp_id")
        compliance_status = data.get("comp_status")
        level_one_id = data.get("level_1_s_id")
        a_status = data.get("a_status")
        remarks = data.get("remarks")
        client_statutory_id = data.get("client_statutory_id")

        return SaveComplianceStatus(
            client_id, legal_entity_id,
            unit_id, domain_id, compliance_id, compliance_status,
            level_one_id, a_status, remarks,
            client_statutory_id
        )

    def to_structure(self):
        return {
            "ct_id": self.client_id,
            "le_id": self.legal_entity_id,
            "u_id": self.unit_id,
            "d_id": self.domain_id,
            "comp_id": self.compliance_id,
            "comp_status": self.compliance_status,
            "level_1_s_id": self.level_1_id,
            "a_status": self.status,
            "remarks": self.remarks,
            "client_statutory_id": self.client_statutory_id
        }

def _init_Request_class_map():
    classes = [
        GetAssignedStatutories,
        GetAssignedStatutoriesForApprove,
        GetAssignedStatutoriesById,
        GetAssignedStatutoryWizardOneData,
        GetAssignedStatutoryWizardTwoData,
        SaveAssignedStatutory,
        GetAssignedStatutoryWizardOneUnits,
        ApproveAssignedStatutory
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
        return GetAssignedStatutoriesByIdSuccess(
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
        self, level_one_id, level_one_name, mapping_text,
        statutory_provision, compliance_id,
        document_name, compliance_name, description, organizations,
        level_one_status, level_one_remarks,
        compliance_status, is_saved,
        unit_id
    ):
        self.level_one_id = level_one_id
        self.level_one_name = level_one_name
        self.mapping_text = mapping_text
        self.statutory_provision = statutory_provision
        self.compliance_id = compliance_id
        self.document_name = document_name
        self.compliance_name = compliance_name
        self.description = description
        self.organizations = organizations

        self.level_one_status = level_one_status
        self.level_one_remarks = level_one_remarks
        self.compliance_status = compliance_status
        self.is_saved = is_saved
        self.unit_id = unit_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "level_1_s_id", "level_1_s_name", "map_text" "s_provision", "comp_id",
            "doc_name", "comp_name", "descrip", "org_names",

            "a_status", "remarks", "comp_status", "s_s",
        ])
        level_one_id = data.get("level_1_s_id")
        level_one_name = data.get("level_1_s_name")

        map_text = data.get("map_text")
        statutory_provision = data.get("s_provision")
        compliance_id = data.get("comp_id")
        document_name = data.get("doc_name")
        compliance_name = data.get("comp_name")
        description = data.get("descrip")
        organizations = data.get("org_names")

        level_one_status = data.get("a_status")
        level_one_remarks = data.get("remarks")
        compliance_status = data.get("compliance_status")
        is_saved = data.get("s_s")
        unit_id = data.get("u_id")

        return AssignStatutoryCompliance(
            level_one_id, level_one_name, map_text, statutory_provision, compliance_id,
            document_name, compliance_name, description, organizations,
            level_one_status, level_one_remarks, compliance_status,
            is_saved, unit_id
        )

    def to_structure(self):
        return {
            "level_1_s_id": self.level_one_id,
            "level_1_s_name": self.level_one_name,
            "map_text": self.mapping_text,
            "s_provision": self.statutory_provision,
            "comp_id": self.compliance_id,
            "doc_name": self.document_name,
            "comp_name": self.compliance_name,
            "descrip": self.description,
            "org_names": self.organizations,

            "a_status": self.level_one_status,
            "remarks": self.level_one_remarks,
            "comp_status": self.compliance_status,
            "s_s": self.is_saved,
            "u_id": self.unit_id
        }

class GetAssignedStatutoryWizardTwoDataSuccess(Response):
    def __init__(self, statutories_for_assigning):
        self.statutories_for_assigning = statutories_for_assigning

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "statutories_for_assigning"
        ])
        statutories_for_assigning = data.get("statutories_for_assigning")
        return GetAssignedStatutoryWizardTwoDataSuccess(
            statutories_for_assigning
        )

    def to_inner_structure(self):
        return {
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

class ApproveAssignedStatutorySuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ApproveAssignedStatutorySuccess()

    def to_inner_structure(self):
        return {}


def _init_Response_class_map():
    classes = [
        GetAssignedStatutoriesSuccess, GetAssignedStatutoriesByIdSuccess,
        GetAssignedStatutoryWizardOneDataSuccess,
        GetAssignedStatutoryWizardTwoDataSuccess,
        SaveAssignedStatutorySuccess,
        GetAssignedStatutoryWizardOneUnitsSuccess,
        ApproveAssignedStatutorySuccess
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
        approve_status, approved_status_id, client_statutory_id,
        legal_entity_id
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
        self.client_statutory_id = client_statutory_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "c_name", "ct_id", "grp_name", "b_grp_name",
            "l_e_name", "div_name",
            "u_id", "u_name", "g_name", "d_id",
            "d_name", "cat_name", "approval_status_text", "a_s_id",
            "client_statutory_id", "le_id"
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
        client_statutory_id = data.get("client_statutory_id")
        legal_entity_id = data.get("le_id")
        return AssignedStatutories(
            country_name,
            client_id, group_name, business_group_name,
            legal_entity_name, division_name,
            unit_code_with_name, geography_name, unit_id, domain_id,
            domain_name, category_name,
            submission_status, approved_status_id,
            client_statutory_id, legal_entity_id
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
            "a_s_id": self.approved_status_id,
            "client_statutory_id": self.client_statutory_id,
            "le_id": self.legal_entity_id
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
        self, unit_id, unit_code, unit_name, address, geography_name, client_statutory_id
    ):
        self.unit_id = unit_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.address = address
        self.geography_name = geography_name
        self.client_statutory_id = client_statutory_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "u_id", "unit_code", "u_name", "address", "g_name",
                "client_statutory_id"
            ]
        )
        unit_id = data.get("u_id")
        unit_code = data.get("unit_code")
        unit_name = data.get("u_name")
        address = data.get("address")
        geography = data.get("g_name")
        client_statutory_id = data.get("client_statutory_id")
        return StatutoryUnits(unit_id, unit_code, unit_name, address, geography, client_statutory_id)

    def to_structure(self):
        return {
            "u_id": self.unit_id,
            "unit_code": self.unit_code,
            "u_name": self.unit_name,
            "address": self.address,
            "g_name": self. geography_name,
            "client_statutory_id": self.client_statutory_id
        }
