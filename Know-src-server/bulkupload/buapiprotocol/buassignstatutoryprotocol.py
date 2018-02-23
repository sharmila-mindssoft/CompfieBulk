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


class GetClientInfo(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetClientInfo()

    def to_inner_structure(self):
        return {
        }

class DownloadAssignStatutory(Request):
    def __init__( self, cl_id, le_id, d_ids, u_ids, cl_name, le_name, d_names, u_names):
        self.cl_id = cl_id
        self.le_id = le_id
        self.d_ids = d_ids
        self.u_ids = u_ids
        self.cl_name = cl_name
        self.le_name = le_name
        self.d_names = d_names
        self.u_names = u_names

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["cl_id", "le_id", "d_ids", "u_ids", "cl_name", "le_name", "d_names", "u_names"])
        return DownloadAssignStatutory(
            data.get("cl_id"), data.get("le_id"), data.get("d_ids"), data.get("u_ids"), 
            data.get("cl_name"), data.get("le_name"), data.get("d_names"), data.get("u_names")
        )

    def to_inner_structure(self):
        return {
            "cl_id": self.cl_id,
            "le_id": self.le_id,
            "d_ids": self.d_ids,
            "u_ids": self.u_ids,
            "cl_name": self.cl_name,
            "le_name": self.le_name,
            "d_names": self.d_names,
            "u_names": self.u_names,
        }

class UploadAssignStatutoryCSV(Request):
    def __init__(self, csv_name, csv_data, csv_size, cl_id, le_id, d_ids, le_name, d_names):
        self.csv_name = csv_name
        self.csv_data = csv_data
        self.csv_size = csv_size
        self.cl_id = cl_id
        self.le_id = le_id
        self.d_ids = d_ids
        self.le_name = le_name
        self.d_names = d_names

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["csv_name", "csv_data", "csv_size", "cl_id", "le_id", "d_ids", "le_name", "d_names"])
        return UploadAssignStatutoryCSV(
            data.get("csv_name"), data.get("csv_data"), data.get("csv_size"), data.get("cl_id"), data.get("le_id"), data.get("d_ids"),
            data.get("le_name"), data.get("d_names")
        )

    def to_inner_structure(self):
        return {
            "csv_name": self.csv_name,
            "csv_data": self.csv_data,
            "csv_size": self.csv_size,
            "cl_id": self.cl_id,
            "le_id": self.le_id,
            "d_ids": self.d_ids,
            "le_name": self.le_name,
            "d_names": self.d_names
        }

class GetAssignStatutoryForApprove(Request):
    def __init__(self, cl_id, le_id):
        self.cl_id = cl_id
        self.le_id = le_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["cl_id", "le_id"])
        return GetAssignStatutoryForApprove(
            data.get("cl_id"), data.get("le_id")
        )

    def to_inner_structure(self):
        return {
            "cl_id": self.cl_id,
            "le_id": self.le_id
        }

def _init_Request_class_map():
    classes = [
        GetClientInfo, DownloadAssignStatutory, UploadAssignStatutoryCSV,
        GetAssignStatutoryForApprove
    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Request_class_map = _init_Request_class_map()




class Clients(object):
    def __init__(
        self, cl_id, cl_name
    ):
        self.cl_id = cl_id
        self.cl_name = cl_name
        
    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "cl_id", "cl_name"
        ])
        return Clients(
            data.get("cl_id"), data.get("cl_name")
        )

    def to_structure(self):
        return {
            "cl_id": self.cl_id,
            "cl_name": self.cl_name
        }

class LegalEntites(object):
    def __init__(
        self, cl_id, le_id, le_name, domains
    ):
        self.cl_id = cl_id
        self.le_id = le_id
        self.le_name = le_name
        self.domains = domains
        
    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "cl_id", "le_id", "le_name", "domains"
        ])
        return LegalEntites(
            data.get("cl_id"), data.get("le_id"), data.get("le_name"), data.get("domains")
        )

    def to_structure(self):
        return {
            "cl_id": self.cl_id,
            "le_id": self.le_id,
            "le_name": self.le_name,
            "domains": self.domains
        }

class Units(object):
    def __init__(
        self, cl_id, le_id, u_id, u_name, d_ids
    ):
        self.cl_id = cl_id
        self.le_id = le_id
        self.u_id = u_id
        self.u_name = u_name
        self.d_ids = d_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "cl_id", "le_id", "u_id", "u_name", "d_ids"
        ])
        return Units(
            data.get("cl_id"), data.get("le_id"), data.get("u_id"), data.get("u_name"), data.get("d_ids")
        )

    def to_structure(self):
        return {
            "cl_id": self.cl_id,
            "le_id": self.le_id,
            "u_id": self.u_id,
            "u_name": self.u_name,
            "d_ids": self.d_ids
        }

class Domains(object):
    def __init__(
        self, d_id, d_name
    ):
        self.d_id = d_id
        self.d_name = d_name
        
    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "d_id", "d_name"
        ])
        return Units(
            data.get("d_id"), data.get("d_name")
        )

    def to_structure(self):
        return {
            "d_id": self.d_id,
            "d_name": self.d_name
        }


class PendingCsvListAssignStatutory(object):
    def __init__(
        self, csv_id, csv_name, uploaded_by,
        uploaded_on, no_of_records, action_count, download_file
    ):
        self.csv_id = csv_id
        self.csv_name = csv_name
        self.uploaded_by = uploaded_by
        self.uploaded_on = uploaded_on
        self.no_of_records = no_of_records
        self.action_count = action_count
        self.download_file = download_file

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "csv_id", "csv_name", "uploaded_by", "uploaded_on",
            "no_of_records", "action_count", "download_file"

        ])
        return PendingCsvListAssignStatutory(
            data.get("csv_id"), data.get("csv_name"), data.get("uploaded_by"),
            data.get("uploaded_on"), data.get("no_of_records"), data.get("download_file")
        )

    def to_structure(self):
        return {
            "csv_id": self.csv_id,
            "csv_name": self.csv_name,
            "uploaded_by": self.uploaded_by,
            "uploaded_on": self.uploaded_on,
            "no_of_records": self.no_of_records,
            "action_count": self.action_count,
            "download_file": self.download_file
        }

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


class GetClientInfoSuccess(Response):
    def __init__(self, clients, legalentites, units):
        self.clients = clients
        self.legalentites = legalentites
        self.units = units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, ["clients", "legalentites", "units"])
        clients = data.get("clients")
        legalentites = data.get("legalentites")
        units = data.get("units")
        return GetClientInfoSuccess(
            clients, legalentites, units
        )

    def to_inner_structure(self):
        return {
            "clients": self.clients,
            "legalentites": self.legalentites,
            "units": self.units

        }

class DownloadAssignStatutorySuccess(Response):
    def __init__(self, link):
        self.link = link

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, ["link"])
        link = data.get("link")
        
        return DownloadAssignStatutorySuccess(
            link
        )

    def to_inner_structure(self):
        return {
            "link": self.link
        }


class UploadAssignStatutoryCSVSuccess(Response):
    def __init__(self, total, valid, invalid):
        self.total = total
        self.valid = valid
        self.invalid = invalid

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["total", "valid", "invalid"])
        return UploadAssignStatutoryCSVSuccess(
            data.get("total"), data.get("valid"), data.get("invalid")
        )

    def to_inner_structure(self):
        return {
            "total": self.total,
            "valid": self.valid,
            "invalid": self.invalid
        }


class UploadAssignStatutoryCSVFailed(Response):
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
        return UploadAssignStatutoryCSVFailed(
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

class GetAssignStatutoryForApproveSuccess(Response):
    def __init__(self, pending_csv_list_as):
        self.pending_csv_list_as = pending_csv_list_as

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["pending_csv_list_as"])
        return GetAssignStatutoryForApproveSuccess(
            data.get("pending_csv_list_as")
        )

    def to_inner_structure(self):
        return {
            "pending_csv_list_as": self.pending_csv_list_as
        }

def _init_Response_class_map():
    classes = [
        GetClientInfoSuccess, DownloadAssignStatutorySuccess,
        UploadAssignStatutoryCSVSuccess, UploadAssignStatutoryCSVFailed,
        GetAssignStatutoryForApproveSuccess
    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()


#
# RequestFormat
#
assign_statutory = "bulkupload.buapiprotocol.buassignstatutoryprotocol"
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
            request, assign_statutory, "Request"
        )
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": to_VariantType(
                self.request, assign_statutory, "Response"
            ),
        }
