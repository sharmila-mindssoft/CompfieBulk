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

class UploadCompletedTaskCurrentYearCSV(Request):
    def __init__(self, csv_name, csv_data, csv_size, cl_id, le_id, d_id, le_name, d_name):
        self.csv_name = csv_name
        self.csv_data = csv_data
        self.csv_size = csv_size
        self.cl_id = cl_id
        self.le_id = le_id
        self.d_id = d_id
        self.le_name = le_name
        self.d_name = d_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["csv_name", "csv_data", "csv_size", "cl_id", "le_id", "d_id", "le_name", "d_name"])
        return UploadCompletedTaskCurrentYearCSV(
            data.get("csv_name"), data.get("csv_data"), data.get("csv_size"), data.get("cl_id"), data.get("le_id"), data.get("d_id"),
            data.get("le_name"), data.get("d_name")
        )

    def to_inner_structure(self):
        return {
            "csv_name": self.csv_name,
            "csv_data": self.csv_data,
            "csv_size": self.csv_size,
            "cl_id": self.cl_id,
            "le_id": self.le_id,
            "d_id": self.d_id,
            "le_name": self.le_name,
            "d_name": self.d_name
        }

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

def _init_Request_class_map():
    classes = [
        GetCompletedTask_Domains,
        UploadCompletedTaskCurrentYearCSV
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

class UploadCompletedTaskCurrentYearCSVSuccess(Response):
    def __init__(self, total, valid, invalid):
        self.total = total
        self.valid = valid
        self.invalid = invalid

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["total", "valid", "invalid"])
        return UploadCompletedTaskCurrentYearCSVSuccess(
            data.get("total"), data.get("valid"), data.get("invalid")
        )

    def to_inner_structure(self):
        return {
            "total": self.total,
            "valid": self.valid,
            "invalid": self.invalid
        }


class UploadCompletedTaskCurrentYearCSVFailed(Response):
    def __init__(
        self, invalid_file, mandatory_error, max_length_error, duplicate_error,
        invalid_char_error, invalid_data_error, inactive_error,
        total, invalid
    ):
        self.invalid_file = invalid_file
        self.mandatory_error = mandatory_error
        self.max_length_error = max_length_error
        self.duplicate_error = duplicate_error
        self.invalid_char_error = invalid_char_error
        self.invalid_data_error = invalid_data_error
        self.inactive_error = inactive_error
        self.total = total
        self.invalid = invalid

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "invalid_file", "mandatory_error", "max_length_error", "duplicate_error",
            "invalid_char_error", "invalid_data_error", "inactive_error",
            "total", "invalid"
        ])
        return UploadCompletedTaskCurrentYearCSVFailed(
            data.get("invalid_file"), data.get("mandatory_error"),
            data.get("max_length_error"), data.get("duplicate_error"),
            data.get("invalid_char_error"), data.get("invalid_data_error"),
            data.get("inactive_error"),
            data.get("total"),
            data.get("invalid")
        )

    def to_inner_structure(self):
        return {
            "invalid_file" : self.invalid_file,
            "mandatory_error": self.mandatory_error,
            "max_length_error": self.max_length_error,
            "duplicate_error": self.duplicate_error,
            "invalid_char_error": self.invalid_char_error,
            "invalid_data_error": self.invalid_data_error,
            "inactive_error": self.inactive_error,
            "total": self.total,
            "invalid": self.invalid
        }

def _init_Response_class_map():
    classes = [
        GetCompletedTask_DomainsSuccess,
        UploadCompletedTaskCurrentYearCSVSuccess,
        UploadCompletedTaskCurrentYearCSVFailed

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
