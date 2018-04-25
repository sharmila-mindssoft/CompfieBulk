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
    def __init__(self, csv_name, csv_data, csv_size, legal_entity_id):
        self.csv_name = csv_name
        self.csv_data = csv_data
        self.csv_size = csv_size
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["csv_name", "csv_data", "csv_size","legal_entity_id"])
        return UploadCompletedTaskCurrentYearCSV(
            data.get("csv_name"), data.get("csv_data"), data.get("csv_size"), data.get("legal_entity_id")
        )

    def to_inner_structure(self):
        return {
            "csv_name": self.csv_name,
            "csv_data": self.csv_data,
            "csv_size": self.csv_size,
            "legal_entity_id": self.legal_entity_id
        }

class saveBulkRecords(Request):
    def __init__(self, new_csv_id, legal_entity_id):
        self.new_csv_id = new_csv_id
        self.legal_entity_id = legal_entity_id


    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["new_csv_id", "legal_entity_id"])
        return saveBulkRecords(
            data.get("new_csv_id"), data.get("legal_entity_id")
        )

    def to_inner_structure(self):
        return {
            "new_csv_id": self.new_csv_id,
            "legal_entity_id": self.legal_entity_id
        }

class GetCompletedTaskCsvUploadedList(Request):
    def __init__(self, legal_entity_id):
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["legal_entity_id"])
        return GetCompletedTaskCsvUploadedList(data.get("legal_entity_id"))

    def to_inner_structure(self):
        return{
            "legal_entity_id": self.legal_entity_id
        }

class CsvList(object):
    def __init__(self, csv_past_id, csv_name, uploaded_on, uploaded_by, total_records, total_documents, uploaded_documents, remaining_documents):
        self.csv_past_id = csv_past_id
        self.csv_name = csv_name
        self.uploaded_on = uploaded_on
        self.uploaded_by = uploaded_by
        self.total_records = total_records
        self.total_documents = total_documents
        self.uploaded_documents = uploaded_documents
        self.remaining_documents = remaining_documents

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["csv_past_id", "csv_name", "uploaded_on", "uploaded_by",
                                        "total_records", "total_documents", "uploaded_documents", "uploaded_documents"
                                        "remaining_documents"
        ])
        return CsvList(
            data.get("csv_past_id"), data.get("csv_name"), data.get("uploaded_on"),
            data.get("uploaded_by"), data.get("total_records"), data.get("total_documents"),
            data.get("uploaded_documents"), data.get("uploaded_documents"), data.get("remaining_documents")
        )

    def to_structure(self):
        return {
            "csv_past_id": self.csv_past_id,
            "csv_name": self.csv_name,
            "uploaded_on": self.uploaded_on,
            "uploaded_by": self.uploaded_by,
            "total_records": self.total_records,
            "total_documents": self.total_documents,
            "uploaded_documents": self.uploaded_documents,
            "remaining_documents": self.remaining_documents
        }


# class GetCompletedTaskCsvUploadedList(object):
#     def __init__(
#         self, csv_past_id, csv_name, uploaded_by, uploaded_on,
#         total_records, total_documents, uploaded_documents, remaining_documents
#     ):
#         self.csv_past_id = csv_past_id
#         self.csv_name = csv_name
#         self.uploaded_by = uploaded_by
#         self.uploaded_on = uploaded_on
#         self.total_records = total_records
#         self.total_documents = total_documents
#         self.uploaded_documents = uploaded_documents
#         self.remaining_documents = remaining_documents

#     @staticmethod
#     def parse_structure(data):
#         data = parse_dictionary(data, [
#             "csv_past_id", "csv_name", "uploaded_by", "uploaded_on",
#             "total_records", "total_documents", "uploaded_documents", "remaining_documents"

#         ])
#         return PendingCsvList(
#             data.get("csv_id"), data.get("csv_name"),
#             data.get("csv_id"), data.get("csv_name"), data.get("uploaded_by"),
#             data.get("uploaded_on"), data.get("no_of_records"),
#             data.get("approve_count"),
#             data.get("rej_count"),
#             data.get("download_file"), data.get("declined_count")
#         )

#     def to_structure(self):
#         return {
#             "csv_id": self.csv_id,
#             "csv_name": self.csv_name,
#             "uploaded_by": self.uploaded_by,
#             "uploaded_on": self.uploaded_on,
#             "no_of_records": self.no_of_records,
#             "approve_count": self.approve_count,
#             "rej_count": self.rej_count,
#             "download_file": self.download_file,
#             "declined_count": self.declined_count
#         }

def _init_Request_class_map():
    classes = [
        UploadCompletedTaskCurrentYearCSV,
        saveBulkRecords,
        GetCompletedTaskCsvUploadedList
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

class GetCompletedTaskCsvUploadedListSuccess(Response):
    def __init__(self, csv_list):
        self.csv_list = csv_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["csv_list"])
        csv_list = data.get("csv_list")
        return GetCompletedTaskCsvUploadedListSuccess(csv_list)

    def to_inner_structure(self):
        return {
            "csv_list": self.csv_list
        }

class UploadCompletedTaskCurrentYearCSVSuccess(Response):
    def __init__(self, total, valid, invalid, new_csv_id, csv_name, doc_count, doc_names):
        self.total = total
        self.valid = valid
        self.invalid = invalid
        self.new_csv_id = new_csv_id
        self.csv_name = csv_name
        self.doc_count = doc_count
        self.doc_names = doc_names

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["total", "valid", "invalid", "new_csv_id", "csv_name", "doc_count", "doc_names"])
        return UploadCompletedTaskCurrentYearCSVSuccess(
            data.get("total"), data.get("valid"), data.get("invalid"),
            data.get("new_csv_id"), data.get("csv_name"), data.get("doc_count"),
            data.get("doc_names")
        )

    def to_inner_structure(self):
        return {
            "total": self.total,
            "valid": self.valid,
            "invalid": self.invalid,
            "new_csv_id": self.new_csv_id,
            "csv_name": self.csv_name,
            "doc_count": self.doc_count,
            "doc_names": self.doc_names
        }


class UploadCompletedTaskCurrentYearCSVFailed(Response):
    def __init__(
        self, invalid_file, mandatory_error, max_length_error, duplicate_error,
        invalid_char_error, invalid_data_error, inactive_error, total, invalid
    ):
        # total, invalid
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
            "invalid_file", "mandatory_error", "max_length_error",
            "duplicate_error", "invalid_char_error", "invalid_data_error",
            "inactive_error", "total", "invalid"
        ])

        return UploadCompletedTaskCurrentYearCSVFailed(
            data.get("invalid_file"), data.get("mandatory_error"),
            data.get("max_length_error"), data.get("duplicate_error"),
            data.get("invalid_char_error"), data.get("invalid_data_error"),
            data.get("inactive_error"), data.get("total"), data.get("invalid")
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

class saveBulkRecordSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return saveBulkRecordSuccess()

    def to_inner_structure(self):
        return{}

class CsvListSuccess(object):
    def __init__(self, csv_past_id, csv_name, uploaded_by, uploaded_on, total_records, total_documents, uploaded_documents, remaining_documents):
        self.csv_past_id = csv_past_id
        self.csv_name = csv_name
        self.uploaded_by = uploaded_by
        self.uploaded_on = uploaded_on
        self.total_records = total_records
        self.total_documents = total_documents
        self.uploaded_documents = uploaded_documents
        self.remaining_documents = remaining_documents

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["csv_past_id", "csv_name", "uploaded_by", "uploaded_on",
                                        "total_records", "total_documents", "uploaded_documents", "uploaded_documents"
        ])
        return CsvList(
            data.get("csv_past_id"), data.get("csv_name"), data.get("uploaded_by"),
            data.get("uploaded_on"), data.get("total_records"), data.get("total_documents"),
            data.get("uploaded_documents"), data.get("uploaded_documents")
        )

    def to_structure(self):
        return {
            "csv_past_id": self.csv_past_id,
            "csv_name": self.csv_name,
            "uploaded_by": self.uploaded_by,
            "uploaded_on": self.uploaded_on,
            "total_records": self.total_records,
            "total_documents": self.total_documents,
            "uploaded_documents": self.uploaded_documents
        }


def _init_Response_class_map():
    classes = [
        UploadCompletedTaskCurrentYearCSVSuccess,
        UploadCompletedTaskCurrentYearCSVFailed,
        saveBulkRecordSuccess,
        GetCompletedTaskCsvUploadedListSuccess
    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()


#
# RequestFormat
#
completed_task = "bulkupload.buapiprotocol.bucompletedtaskcurrentyearprotocol"


# class RequestFormat(object):
#     def __init__(self, session_token, request):
#         self.session_token = session_token
#         self.request = request

#     @staticmethod
#     def parse_structure(data):
#         print "parse_structure>>252"
#         data = parse_dictionary(data, ["session_token", "request"])
#         session_token = data.get("session_token")
#         request = data.get("request")
#         print "completed_task>>>", completed_task
#         request = parse_VariantType(
#             request, completed_task, "Request"
#         )
#         return RequestFormat(session_token, request)

#     def to_structure(self):
#         return {
#             "session_token": self.session_token,
#             "request": to_VariantType(
#                 self.request, completed_task, "Response"
#             ),
#         }


class RequestFormat(object):
    def __init__(self, session_token, request):
        print"session_token>>>", session_token
        print "request>>>", request
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
            "session_token": self.session_token, "request": Request.to_structure(self.request)
        }
