from clientprotocol.jsonvalidators_client import (parse_dictionary, parse_static_list, to_structure_dictionary_values)
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

class GetComplianceChart(Request):
    def __init__(self, legal_entity_ids):
        self.legal_entity_ids = legal_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_ids"])
        return GetComplianceChart(data.get("le_ids"))

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_ids
        }

def _init_Request_class_map():
    classes = [
        GetComplianceChart
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


class GetComplianceChartSuccess(Request):
    def __init__(self, legal_entity_ids):
        self.legal_entity_ids = legal_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_ids"])
        return GetComplianceChartSuccess(data.get("le_ids"))

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_ids
        }


def _init_Response_class_map():
    classes = [
        GetComplianceChartSuccess
    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()
