from clientprotocol.jsonvalidators_client import (
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

class GetCompletedTask_Domains(Request):
    def __init__(self, c_id):
        self.c_id = c_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id"])
        return GetCompletedTask_Domains(
            data.get("le_id")
        )

    def to_inner_structure(self):
        return {
            "le_id": self.le_id
        }

####################################################
# Get Completed Task Current Year (Past Data)
####################################################
class GetDownloadData(Request):
    def __init__(
        self, legal_entity_id, unit_id, domain_id,
        compliance_frequency, start_count
    ):
        self.legal_entity_id = legal_entity_id
        self.unit_id = unit_id
        self.domain_id = domain_id
        self.compliance_frequency = compliance_frequency
        self.start_count = start_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "le_id", "unit_id", "domain_id", "compliance_task_frequency",
            "start_count"
        ])
        return GetDownloadData(
            data.get("le_id"), data.get("unit_id"), data.get("domain_id"),
            data.get("level_1_statutory_name"), data.get("compliance_task_frequency"),
            data.get("start_count")
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id, "unit_id": self.unit_id, "domain_id": self.domain_id,
            "compliance_task_frequency": self.compliance_frequency,
            "start_count": self.start_count
        }


def _init_Request_class_map():
    classes = [
        GetCompletedTask_Domains,
        GetDownloadData
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

class Domains(object):
    def __init__(
        self, le_id, d_id, d_name
    ):
        self.le_id = le_id
        self.d_id = d_id
        self.d_name = d_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "le_id", "d_id", "d_name"
        ])
        return Units(
            data.get("le_id"), data.get("d_id"), data.get("d_name")
        )

    def to_structure(self):
        return{
            "le_id": self.le_id,
            "d_id": self.d_id,
            "d_name": self.d_name
        }

class GetCompletedTask_DomainsSuccess(Response):
    def __init__(self, domain_list):
        self.domain_list = domain_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, ["domain_list"])
        domain_list = data.get("domain_list")
        return GetCompletedTask_DomainsSuccess(domain_list)

    def to_inner_structure(self):
        return {
            "domain_list": self.domain_list
        }

def _init_Response_class_map():
    classes = [
        GetCompletedTask_DomainsSuccess
    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()


#
# RequestFormat
#
statutory_mapping = "bulkupload.buapiprotocol.bustatutorymappingprotocol"
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
            request, statutory_mapping, "Request"
        )
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": to_VariantType(
                self.request, statutory_mapping, "Response"
            ),
        }
