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


class GetStatutoryMappingCsvUploadedList(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetStatutoryMappingCsvUploadedList()

    def to_inner_structure(self):
        return {
        }


def _init_Request_class_map():
    classes = [
        GetStatutoryMappingCsvUploadedList
    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Request_class_map = _init_Request_class_map()

class CsvList(object):
    def __init__(self, c_id, c_name, d_id, d_name, csv_id, csv_name, no_of_records, no_of_documents, uploaded_document):
        self.c_id = c_id
        self.c_name = c_name
        self.d_id = d_id
        self.d_name = d_name
        self.csv_id = csv_id
        self.csv_name = csv_name
        self.no_of_records = no_of_records
        self.no_of_documents = no_of_documents
        self.uploaded_document = uploaded_document

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "c_id", "c_name", "d_id", "d_name", "csv_id", "csv_name",
            "no_of_records", "no_of_documents", "uploaded_documents"
        ])
        return CsvList(
            data.get("c_id"), data.get("c_name"), data.get("d_id"),
            data.get("d_name"), data.get("csv_id"), data.get("csv_name"),
            data.get("no_of_records"), data.get("no_of_documents"),
            data.get("uploaded_documents")
        )

    def to_structure(self):
        return {
            "c_id": self.c_id,
            "c_name": self.c_name,
            "d_id": self.d_id,
            "d_name": self.d_name,
            "csv_id": self.csv_id,
            "csv_name": self.csv_name,
            "no_of_records": self.no_of_records,
            "no_of_documents": self.no_of_documents,
            "uploaded_documents": self.uploaded_document
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


class GetStatutoryMappingCsvUploadedListSuccess(Response):
    def __init__(self, upload_more, csv_list):
        self.upload_more = upload_more
        self.csv_list = csv_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, ["upload_more", "csv_list"])
        upload_more = data.get("upload_more")
        csv_list = data.get("csv_list")
        return GetStatutoryMappingCsvUploadedListSuccess(
            upload_more, csv_list
        )

    def to_inner_structure(self):
        return {
            "upload_more": self.upload_more,
            "csv_list": self.csv_list
        }

def _init_Response_class_map():
    classes = [
        GetStatutoryMappingCsvUploadedListSuccess
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
