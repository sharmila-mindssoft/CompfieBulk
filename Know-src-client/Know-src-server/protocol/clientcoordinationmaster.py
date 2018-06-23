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
        return _Request_class_map[name].parse_structure(data)

    @staticmethod
    def parse_inner_structure(data):
        raise NotImplementedError


class GetClientUnitApprovalList(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data)
        return GetClientUnitApprovalList()

    def to_inner_structure(self):
        return {}


class GetEntityApprovalList(Request):
    def __init__(self, legal_entity_id):
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["legal_entity_id"])
        legal_entity_id = data["legal_entity_id"]
        return GetEntityApprovalList(legal_entity_id)

    def to_inner_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id
        }


class ApproveUnit(Request):
    def __init__(self, unit_approval_details):
        self.unit_approval_details = unit_approval_details

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_approval_details"])
        unit_approval_details = data.get("unit_approval_details")
        return ApproveUnit(unit_approval_details)

    def to_inner_structure(self):
        return {
            "unit_approval_details": self.unit_approval_details
        }


class GetClientGroupApprovalList(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data)
        return GetClientGroupApprovalList()

    def to_inner_structure(self):
        return {}


class GetLegalEntityInfo(Request):
    def __init__(self, entity_id):
        self.entity_id = entity_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["le_id"])
        return GetLegalEntityInfo(data.get("le_id"))

    def to_inner_structure(self):
        return {
            "le_id": self.entity_id
        }

class ApproveClientGroup(Request):
    def __init__(self, client_group_approval_details):
        self.client_group_approval_details = client_group_approval_details

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["client_group_approval_details"])
        client_group_approval_details = data.get("client_group_approval_details")
        return ApproveClientGroup(client_group_approval_details)

    def to_inner_structure(self):
        return {
            "client_group_approval_details": self.client_group_approval_details
        }


def _init_Request_class_map():
    classes = [
        GetClientUnitApprovalList, GetEntityApprovalList, ApproveUnit,
        GetClientGroupApprovalList, ApproveClientGroup,
        GetLegalEntityInfo
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
        print "inner : %s" % inner
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
        return _Response_class_map[name].parse_structure(data)

    @staticmethod
    def parse_inner_structure(data):
        raise NotImplementedError


class UnitApproval(object):
    def __init__(
        self, legal_entity_id, legal_entity_name, country_name,
        business_group_name, group_name, unit_count
    ):
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.country_name = country_name
        self.business_group_name = business_group_name
        self.group_name = group_name
        self.unit_count = unit_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "legal_entity_id", "legal_entity_name", "country_name",
            "business_group_name", "group_name", "unit_count"
        ])
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_name = data.get("legal_entity_name")
        country_name = data.get("country_name")
        business_group_name = data.get("business_group_name")
        group_name = data.get("group_name")
        unit_count = data.get("unit_count")
        return UnitApproval(
            legal_entity_id, legal_entity_name, country_name,
            business_group_name, group_name, unit_count
        )

    def to_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id,
            "legal_entity_name": self.legal_entity_name,
            "country_name": self.country_name,
            "business_group_name": self.business_group_name,
            "group_name": self.group_name,
            "unit_count": self.unit_count
        }


class GetClientUnitApprovalListSuccess(Response):
    def __init__(
        self, unit_approval_list
    ):
        self.unit_approval_list = unit_approval_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "unit_approval_list"
        ])
        unit_approval_list = data.get("unit_approval_list")
        return GetClientUnitApprovalListSuccess(unit_approval_list)

    def to_inner_structure(self):
        print "self.unit_approval_list: %s" % self.unit_approval_list
        return {
            "unit_approval_list": self.unit_approval_list
        }


class EntityUnitApproval(object):
    def __init__(
        self, unit_id, division_name, category_name, unit_code, unit_name,
        address, postal_code, geography_name, domain_names, org_names
    ):
        self.unit_id = unit_id
        self.division_name = division_name
        self.category_name = category_name
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.address = address
        self.postal_code = postal_code
        self.geography_name = geography_name
        self.domain_names = domain_names
        self.org_names = org_names

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "unit_id", "division_name", "category_name", "unit_code",
            "unit_name", "address", "postal_code", "geography_name",
            "domain_names", "org_names"
        ])
        unit_id = data.get("unit_id")
        division_name = data.get("division_name")
        category_name = data.get("category_name")
        unit_code = data.get("unit_code")
        unit_name = data.get("unit_name")
        address = data.get("address")
        postal_code = data.get("postal_code")
        geography_name = data.get("geography_name")
        domain_names = data.get("domain_names")
        org_names = data.get("org_names")
        return EntityUnitApproval(
            unit_id, division_name, category_name, unit_code, unit_name,
            address, postal_code, geography_name, domain_names, org_names
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id,
            "division_name": self.division_name,
            "category_name": self.category_name,
            "unit_code": self.unit_code,
            "unit_name": self.unit_name,
            "address": self.address,
            "postal_code": self.postal_code,
            "geography_name": self.geography_name,
            "domain_names": self.domain_names,
            "org_names": self.org_names
        }


class GetEntityApprovalListSuccess(Response):
    def __init__(self, entity_unit_approval_list):
        self.entity_unit_approval_list = entity_unit_approval_list

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["entity_unit_approval_list"])
        entity_unit_approval_list = data["entity_unit_approval_list"]
        return GetEntityApprovalListSuccess(entity_unit_approval_list)

    def to_inner_structure(self):
        return {
            "entity_unit_approval_list": self.entity_unit_approval_list
        }


class UnitApprovalDetails(object):
    def __init__(
        self, legal_entity_name, unit_id, approval_status, reason
    ):
        self.legal_entity_name = legal_entity_name
        self.unit_id = unit_id
        self.approval_status = approval_status
        self.reason = reason

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "legal_entity_name", "unit_id", "approval_status", "reason"
        ])
        legal_entity_name = data.get("legal_entity_name")
        unit_id = data.get("unit_id")
        approval_status = data.get("approval_status")
        reason = data.get("reason")
        return UnitApprovalDetails(
            legal_entity_name, unit_id, approval_status, reason
        )

    def to_structure(self):
        return {
            "legal_entity_name": self.legal_entity_name,
            "unit_id": self.unit_id,
            "approval_status": self.approval_status,
            "reason": self.reason
        }


class ApproveUnitSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data)
        return ApproveUnitSuccess()

    def to_inner_structure(self):
        return {}


class ClientGroupApproval(object):
    def __init__(
        self, client_id, group_name, short_name, email_id,
        entity_name, entity_id, country_name
    ):
        self.client_id = client_id
        self.group_name = group_name
        self.short_name = short_name
        self.email_id = email_id
        self.entity_id = entity_id
        self.entity_name = entity_name
        self.country_name = country_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "gt_id", "group_name", "short_name",
            "email_id", "le_name", "le_id", "c_name"
        ])
        return UnitApprovalDetails(
            data.get("gt_id"), data.get("group_name"),
            data.get("short_name"), data.get("email_id"),
            data.get("le_name"), data.get("le_id"),
            data.get("c_name")
        )

    def to_structure(self):
        return {
            "gt_id": self.client_id,
            "group_name": self.group_name,
            "short_name": self.short_name,
            "email_id": self.email_id,
            "le_name": self.entity_name,
            "le_id": self.entity_id,
            "c_name": self.country_name
        }


class GroupInfo(object):
    def __init__(
        self, client_id, client_name, short_name, country_ids
    ):
        self.client_id = client_id
        self.client_name = client_name
        self.short_name = short_name
        self.country_ids = country_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["ct_id", "ct_name", "short_name", "c_ids"])

        return GroupInfo(
            data.get("ct_id"), data.get("ct_name"), data.get("short_name"),
            data.get("c_ids")
        )

    def to_structure(self):
        return {
            "ct_id": self.client_id,
            "ct_name": self.client_name,
            "short_name": self.short_name,
            "c_ids": self.country_ids
        }

class GetClientGroupApprovalListSuccess(Response):
    def __init__(
        self, countries, groups, group_approval_list
    ):
        self.countries = countries
        self.groups = groups
        self.group_approval_list = group_approval_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "group_info" "group_approval_list"])
        countries = data.get("countries")
        group_approval_list = data.get("group_approval_list")
        return GetClientGroupApprovalListSuccess(
            countries, data.get("group_info"),
            group_approval_list
        )

    def to_inner_structure(self):
        return {
            "countries": self.countries,
            "group_info": self.groups,
            "group_approval_list": self.group_approval_list
        }


class ClientGroupApprovalDetails(object):
    def __init__(
        self, client_id, entity_id, entity_name, approval_status, reason
    ):
        self.client_id = client_id
        self.entity_id = entity_id
        self.entity_name = entity_name
        self.approval_status = approval_status
        self.reason = reason

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "ct_id", "le_id", "le_name", "approval_status", "reason"
        ])
        client_id = data.get("ct_id")
        entity_id = data.get("le_id")
        entity_name = data.get("le_name")
        approval_status = data.get("approval_status")
        reason = data.get("reason")
        return ClientGroupApprovalDetails(
            client_id, entity_id, entity_name, approval_status, reason
        )

    def to_structure(self):
        return {
            "ct_id": self.client_id,
            "le_id": self.entity_id,
            "le_name": self.entity_name,
            "approval_status": self.approval_status,
            "reason": self.reason
        }


class ApproveClientGroupSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data)
        return ApproveClientGroupSuccess()

    def to_inner_structure(self):
        return {}

class GetLegalEntityInfoSuccess(Response):
    def __init__(
        self, entity_id, business_group_name, contract_from, contract_to,
        file_space, total_licence, view_licence, remarks, org_info, o_le_name, o_business_group_name, o_contract_from, o_contract_to,
        o_file_space, o_total_licence, o_view_licence, o_group_admin_email_id
    ):
        self.entity_id = entity_id
        self.business_group_name = business_group_name
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.file_space = file_space
        self.total_licence = total_licence
        self.view_licence = view_licence
        self.remarks = remarks
        self.org_info = org_info
        self.o_le_name = o_le_name
        self.o_business_group_name = o_business_group_name
        self.o_contract_from = o_contract_from
        self.o_contract_to = o_contract_to
        self.o_file_space = o_file_space
        self.o_total_licence = o_total_licence
        self.o_view_licence = o_view_licence
        self.o_group_admin_email_id = o_group_admin_email_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "le_id", "bg_name", "contract_from", "contract_to",
            "file_space", "no_of_licence", "no_of_view_licence", "remarks", "org_info",
            "o_le_name", "o_bg_name", "o_contract_from", "o_contract_to",
            "o_file_space", "o_no_of_licence", "o_no_of_view_licence", "o_group_admin_email_id"
        ])
        return GetLegalEntityInfoSuccess(
            data.get("le_id"), data.get("bg_name"), data.get("contract_from"),
            data.get("contract_to"), data.get("file_space"),
            data.get("no_of_licence"), data.get("no_of_view_licence"), data.get("remarks"), data.get("org_info"),
            data.get("o_le_name"), data.get("o_bg_name"), data.get("o_contract_from"),
            data.get("o_contract_to"), data.get("o_file_space"),
            data.get("o_no_of_licence"), data.get("o_no_of_view_licence"), data.get("o_group_admin_email_id")
        )

    def to_inner_structure(self):
        return {
            "le_id": self.entity_id,
            "bg_name": self.business_group_name,
            "contract_from": self.contract_from,
            "contract_to": self.contract_to,
            "file_space": self.file_space,
            "no_of_licence": self.total_licence,
            "org_info": self.org_info,
            "remarks": self.remarks,
            "no_of_view_licence": self.view_licence,
            "o_le_name": self.o_le_name,
            "o_bg_name": self.o_business_group_name,
            "o_contract_from": self.o_contract_from,
            "o_contract_to": self.o_contract_to,
            "o_file_space": self.o_file_space,
            "o_no_of_licence": self.o_total_licence,
            "o_no_of_view_licence": self.o_view_licence,
            "o_group_admin_email_id": self.o_group_admin_email_id
        }

def _init_Response_class_map():
    classes = [
        GetClientUnitApprovalListSuccess, GetEntityApprovalListSuccess,
        ApproveUnitSuccess, GetClientGroupApprovalListSuccess,
        ApproveClientGroupSuccess, GetLegalEntityInfoSuccess
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
            request, "clientcoordinationmaster", "Request"
        )
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": to_VariantType(
                self.request, "clientcoordinationmaster", "Response"
            )
        }


class LegalEntityOrganisation(object):
    def __init__(self, entity_id, domain_id, domain_name, organisation_id, organisation_name, count, o_count):
        self.entity_id = entity_id
        self.domain_id = domain_id
        self.domain_name = domain_name
        self.organisation_id = organisation_id
        self.organisation_name = organisation_name
        self.count = count
        self.o_count = o_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["le_id", "d_id", "d_name", "org_id", "org_name", "count", "o_count"])
        return LegalEntityOrganisation(
            data.get("le_id"), data.get("d_id"), data.get("d_name"),
            data.get("org_id"), data.get("org_name"),
            data.get("count"), data.get("o_count")
        )

    def to_structure(self):
        return {
            "le_id": self.entity_id,
            "d_id": self.domain_id,
            "d_name": self.domain_name,
            "org_id": self.organisation_id,
            "org_name": self.organisation_name,
            "count": self.count,
            "o_count": self.o_count
        }
