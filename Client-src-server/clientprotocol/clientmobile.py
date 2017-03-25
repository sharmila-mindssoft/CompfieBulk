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


class GetVersions(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetVersions()

    def to_inner_structure(self):
        return {
        }


class GetUsers(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetUsers()

    def to_inner_structure(self):
        return {
        }


def _init_Request_class_map():
    classes = [
        GetVersions,
        GetUsers,


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


class GetVersionsSuccess(Response):
    def __init__(
        self, unit_details_version, user_details_version,
        compliance_applicability_version, compliance_history_version,
        reassign_history_version
    ):
        self.unit_details_version = unit_details_version
        self.user_details_version = user_details_version
        self.compliance_applicability_version = compliance_applicability_version
        self.compliance_history_version = compliance_history_version
        self.reassign_history_version = reassign_history_version

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "unit_details_version", "user_details_version",
                "compliance_applicability_version",
                "compliance_history_version",
                "reassign_history_version"
            ]
        )
        unit_details_version = data.get("unit_details_version")

        user_details_version = data.get("user_details_version")
        compliance_applicability_version = data.get(
            "compliance_applicability_version")
        compliance_history_version = data.get("compliance_history_version")
        reassign_history_version = data.get("reassign_history_version")
        return GetVersionsSuccess(
            unit_details_version, user_details_version,
            compliance_applicability_version, compliance_history_version,
            reassign_history_version
        )

    def to_inner_structure(self):
        return {
            "unit_details_version": self.unit_details_version,
            "user_details_version": self.user_details_version,
            "compliance_applicability_version": self.compliance_applicability_version,
            "compliance_history_version": self.compliance_history_version,
            "reassign_history_version": self.reassign_history_version
        }


class GetUsersList(object):
    def __init__(
        self, user_id, user_name
    ):
        self.user_id = user_id
        self.user_name = user_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "user_id", "user_name"
            ]
        )
        user_id = data.get("user_id")
        user_name = data.get("user_name")
        return GetUsersList(
            user_id, user_name
        )

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name
        }


class GetUsersSuccess(Response):
    def __init__(self, user_list):
        self.user_list = user_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_list"])
        user_list = data.get("user_list")

        return GetUsersSuccess(user_list)

    def to_inner_structure(self):
        return self.user_list


def _init_Response_class_map():
    classes = [

        GetVersionsSuccess,
        GetUsersSuccess,
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
