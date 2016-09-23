from protocol.jsonvalidators import (
    parse_dictionary, parse_static_list,
    parse_VariantType, to_VariantType,
    to_dictionary_values
)
# from protocol.parse_structure import (
#     parse_structure_CustomTextType_50
# )
# from protocol.to_structure import (
#     to_structure_CustomTextType_50
# )


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


class GetClientUnitApprovalList(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetClientUnitApprovalList()

    def to_inner_structure(self):
        return {
        }


def _init_Request_class_map():
    classes = [GetClientUnitApprovalList]
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
    def parse_inner_structure(data):
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
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "unit_approval_list"
        ])
        unit_approval_list = data.get("unit_approval_list")
        return GetClientUnitApprovalListSuccess(unit_approval_list)

    def to_structure(self):
        data = {
            "unit_approval_list": self.unit_approval_list
        }
        return to_dictionary_values(data, "GetClientUnitApprovalListSuccess")


def _init_Response_class_map():
    classes = [GetClientUnitApprovalListSuccess]
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
