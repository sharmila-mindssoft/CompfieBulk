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
            "le_ids": self.legal_entity_ids
        }

class GetEscalationChart(Request):
    def __init__(self, legal_entity_ids):
        self.legal_entity_ids = legal_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_ids"])
        return GetEscalationChart(data.get("le_ids"))

    def to_inner_structure(self):
        return {
            "le_ids": self.legal_entity_ids
        }

class GetNotCompliedChart(Request):
    def __init__(self, legal_entity_ids):
        self.legal_entity_ids = legal_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_ids"])
        return GetNotCompliedChart(data.get("le_ids"))

    def to_inner_structure(self):
        return {
            "le_ids": self.legal_entity_ids
        }

class GetRiskChart(Request):
    def __init__(self, legal_entity_ids):
        self.legal_entity_ids = legal_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_ids"])
        return GetRiskChart(data.get("le_ids"))

    def to_inner_structure(self):
        return {
            "le_ids": self.legal_entity_ids
        }

class GetTrendChart(Request):
    def __init__(self, legal_entity_ids):
        self.legal_entity_ids = legal_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_ids"])
        return GetTrendChart(data.get("le_ids"))

    def to_inner_structure(self):
        return {
            "le_ids": self.legal_entity_ids
        }

class GetUserScoreCard(Request):
    def __init__(self, legal_entity_ids):
        self.legal_entity_ids = legal_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_ids"])
        return GetUserScoreCard(data.get("le_ids"))

    def to_inner_structure(self):
        return {
            "le_ids": self.legal_entity_ids
        }

class GetDomainScoreCard(Request):
    def __init__(self, legal_entity_ids):
        self.legal_entity_ids = legal_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_ids"])
        return GetDomainScoreCard(data.get("le_ids"))

    def to_inner_structure(self):
        return {
            "le_ids": self.legal_entity_ids
        }

class GetCalendarView(Request):
    def __init__(self, legal_entity_ids):
        self.legal_entity_ids = legal_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_ids"])
        return GetCalendarView(data.get("le_ids"))

    def to_inner_structure(self):
        return {
            "le_ids": self.legal_entity_ids
        }

def _init_Request_class_map():
    classes = [

        GetComplianceChart, GetEscalationChart, GetNotCompliedChart,
        GetRiskChart, GetTrendChart,
        GetUserScoreCard, GetDomainScoreCard,
        GetCalendarView
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


class ChartSuccess(Response):
    def __init__(self, chart_title, xaxis_name, xaxis, yaxis_name, yaxis, chart_data):
        self.chart_title = chart_title
        self.xaxis_name = xaxis_name
        self.xaxis = xaxis
        self.yaxis_name = yaxis_name
        self.yaxis = yaxis
        self.chart_data = chart_data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "chart_title", "xaxis_name", "xaxis", "yaxis_name", "yaxis",
            "widget_data"
        ])
        return ChartSuccess(
            data.get("chart_title"), data.get("xaxis_name"),
            data.get("xaxis"), data.get("yaxis_name"), data.get("yaxis"),
            data.get("widget_data")
        )

    def to_inner_structure(self):
        return {
            "chart_title": self.chart_title,
            "xaxis_name": self.xaxis_name,
            "xaxis": self.xaxis,
            "yaxis_name": self.yaxis_name,
            "yaxis": self.yaxis,
            "widget_data": self.chart_data
        }


def _init_Response_class_map():
    classes = [
        ChartSuccess

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
        request = Request.parse_structure(request)
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": Request.to_structure(self.request)
        }
