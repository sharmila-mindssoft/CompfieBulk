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
        return ApproveUnit(data)

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
        GetClientGroupApprovalList, ApproveClientGroup
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


class GetClientUnitApprovalListSuccess(object):
    def __init__(
        self, unit_approval_list
    ):
        self.unit_approval_list = unit_approval_list

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "unit_approval_list"
        ])
        unit_approval_list = data.get("unit_approval_list")
        return GetClientUnitApprovalListSuccess(unit_approval_list)

    def to_structure(self):
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
        self, unit_id, approval_status, reason
    ):
        self.unit_id = unit_id
        self.approval_status = approval_status
        self.reason = reason

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "unit_id", "approval_status", "reason"
        ])
        unit_id = data.get("unit_id")
        approval_status = data.get("approval_status")
        reason = data.get("reason")
        return UnitApprovalDetails(
            unit_id, approval_status, reason
        )

    def to_structure(self):
        return {
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
        self, client_id, group_name, username, le_count,
        is_active, country_ids
    ):
        self.client_id = client_id
        self.group_name = group_name
        self.username = username
        self.le_count = le_count
        self.is_active = is_active
        self.country_ids = country_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "client_id", "group_name", "username", "le_count",
            "is_active", "country_ids"
        ])
        client_id = data.get("client_id")
        group_name = data.get("group_name")
        username = data.get("username")
        le_count = data.get("le_count")
        is_active = data.get("is_active")
        country_ids = data.get("country_ids")
        return UnitApprovalDetails(
            client_id, group_name, username, le_count,
            is_active, country_ids
        )

    def to_structure(self):
        return {
            "client_id": self.client_id,
            "group_name": self.group_name,
            "username": self.username,
            "le_count": self.le_count,
            "is_active": self.is_active,
            "country_ids": self.country_ids
        }


class GetClientGroupApprovalListSuccess(Response):
    def __init__(
        self, countries, group_approval_list
    ):
        self.countries = countries
        self.group_approval_list = group_approval_list

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["countries", "group_approval_list"])
        countries = data.get("countries")
        group_approval_list = data.get("group_approval_list")
        return GetClientGroupApprovalListSuccess(
            countries, group_approval_list
        )

    def to_inner_structure(self):
        return {
            "countries": self.countries,
            "group_approval_list": self.group_approval_list
        }


class ClientGroupApprovalDetails(object):
    def __init__(
        self, client_id, approval_status, reason
    ):
        self.client_id = client_id
        self.approval_status = approval_status
        self.reason = reason

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "client_id", "approval_status", "reason"
        ])
        client_id = data.get("client_id")
        approval_status = data.get("approval_status")
        reason = data.get("reason")
        return ClientGroupApprovalDetails(
            client_id, approval_status, reason
        )

    def to_structure(self):
        return {
            "client_id": self.client_id,
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


def _init_Response_class_map():
    classes = [
        GetClientUnitApprovalListSuccess, GetEntityApprovalListSuccess,
        ApproveUnitSuccess, GetClientGroupApprovalListSuccess,
        ApproveClientGroupSuccess
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
