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


class UploadClientUnitsBulkCSV(Request):
    def __init__(self, bu_client_id, bu_group_name, csv_name, csv_data, csv_size):
        self.bu_client_id = bu_client_id
        self.bu_group_name = bu_group_name
        self.csv_name = csv_name
        self.csv_data = csv_data
        self.csv_size = csv_size

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["bu_client_id", "bu_group_name", "csv_name", "csv_data", "csv_size"])
        return UploadClientUnitsBulkCSV(
            data.get("bu_client_id"), data.get("bu_group_name"),
            data.get("csv_name"), data.get("csv_data"),
            data.get("csv_size")
        )

    def to_inner_structure(self):
        return {
            "bu_client_id": self.bu_client_id,
            "bu_group_name": self.bu_group_name,
            "csv_name": self.csv_name,
            "csv_data": self.csv_data,
            "csv_size": self.csv_size
        }

def _init_Request_class_map():
    classes = [
        UploadClientUnitsBulkCSV
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


class UploadClientUnitBulkCSVSuccess(Response):
    def __init__(self, total, valid, invalid):
        self.total = total
        self.valid = valid
        self.invalid = invalid

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["total", "valid", "invalid"])
        return UploadClientUnitBulkCSVSuccess(
            data.get("total"), data.get("valid"), data.get("invalid")
        )

    def to_inner_structure(self):
        return {
            "total": self.total,
            "valid": self.valid,
            "invalid": self.invalid
        }


class UploadClientUnitBulkCSVFailed(Response):
    def __init__(
        self, invalid_file, mandatory_error, max_length_error, duplicate_error,
        invalid_char_error, invalid_data_error, inactive_error,not_found_error,
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
        return UploadClientUnitBulkCSVFailed(
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
        UploadClientUnitBulkCSVSuccess,
        UploadClientUnitBulkCSVFailed
    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()


#
# RequestFormat
#
client_units = "bulkupload.buapiprotocol.buclientunitsprotocol"
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
            request, client_units, "Request"
        )
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": to_VariantType(
                self.request, client_units, "Response"
            ),
        }
