from fileapivalidation import (parse_dictionary, parse_static_list)
# File Protocol
#
# Request
#
__all__ = [
    "FileList"
]

class Request(object):
    def to_structure(self):
        name = type(self).__name__
        inner = self.to_inner_structure()
        # if type(inner) is dict:
        #     inner = to_structure_dictionary_values(inner)
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

class UploadComplianceTaskFile(Request):
    def __init__(
        self, legal_entity_id, country_id,  unit_id, domain_id,
        start_date, file_info
    ):
        self.legal_entity_id = legal_entity_id
        self.country_id = country_id
        self.unit_id = unit_id
        self.domain_id = domain_id
        self.start_date = start_date
        self.file_info = file_info

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "c_id", "u_id", "d_id", "start_date", "file_info"])
        return UploadComplianceTaskFile(
            data.get("le_id"), data.get("c_id"), data.get("u_id"),
            data.get("d_id"),
            data.get("start_date"), data.get("file_info")
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "c_id": self.country_id,
            "u_id": self.unit_id,
            "d_id": self.domain_id,
            "start_date": self.start_date,
            "file_info": self.file_info
        }

class RemoveFile(Request):
    def __init__(
        self, legal_entity_id, country_id,  unit_id, domain_id,
        start_date, file_name
    ):
        self.legal_entity_id = legal_entity_id
        self.country_id = country_id
        self.unit_id = unit_id
        self.domain_id = domain_id
        self.start_date = start_date
        self.file_name = file_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "c_id", "u_id", "d_id", "start_date", "file_name"])
        return RemoveFile(
            data.get("le_id"), data.get("c_id"), data.get("u_id"),
            data.get("d_id"),
            data.get("start_date"), data.get("file_name")
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "c_id": self.country_id,
            "u_id": self.unit_id,
            "d_id": self.domain_id,
            "start_date": self.start_date,
            "file_name": self.file_name
        }

class DownloadFile(Request):
    def __init__(
        self, legal_entity_id, country_id,  unit_id, domain_id,
        start_date, file_name
    ):
        self.legal_entity_id = legal_entity_id
        self.country_id = country_id
        self.unit_id = unit_id
        self.domain_id = domain_id
        self.start_date = start_date
        self.file_name = file_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "c_id", "u_id", "d_id", "start_date", "file_name"])
        return DownloadFile(
            data.get("le_id"), data.get("c_id"), data.get("u_id"),
            data.get("d_id"),
            data.get("start_date"), data.get("file_name")
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "c_id": self.country_id,
            "u_id": self.unit_id,
            "d_id": self.domain_id,
            "start_date": self.start_date,
            "file_name": self.file_name
        }

class FormulateDownload(Request):
    def __init__(self, formulate_info, legal_entity_id, extra_details, unique_code):
        self.formulate_info = formulate_info
        self.legal_entity_id = legal_entity_id
        self.extra_details = extra_details
        self.unique_code = unique_code

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["formulate_info", "le_id", "extra_details", "unique_code"])
        return FormulateDownload(
            data.get("formulate_info"), data.get("le_id"), data.get("extra_details"),
            data.get("unique_code")
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "formulate_info": self.formulate_info,
            "extra_details": self.extra_details,
            "unique_code": self.unique_code
        }

class FileList(object):
    def __init__(self, file_name, file_content):
        self.file_name = file_name
        self.file_content = file_content

    @staticmethod
    def parse_structure(data):
        return FileList(data.get("file_name"), data.get("file_content"))

    def to_structure(self):
        return {
            "file_name": self.file_name,
            "file_content": self.file_content
        }

def _init_Request_class_map():
    classes = [UploadComplianceTaskFile, RemoveFile, DownloadFile, FormulateDownload]
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
        # if type(inner) is dict:
        #     inner = to_structure_dictionary_values(inner)

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

class FileUploadSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        return FileUploadSuccess()

    def to_inner_structure(self):
        return {}


class FileUploadFailed(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        return FileUploadFailed()

    def to_inner_structure(self):
        return {}

class FileRemoved(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        return FileRemoved()

    def to_inner_structure(self):
        return {}

class FileRemoveFailed(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        return FileRemoveFailed()

    def to_inner_structure(self):
        return {}

class FormulateDownloadSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        return FormulateDownloadSuccess()

    def to_inner_structure(self):
        return {}

class FormulateDownloadFailed(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        return FormulateDownloadFailed()

    def to_inner_structure(self):
        return {}


def _init_Response_class_map():
    classes = [
        FileUploadSuccess, FileUploadFailed, FileRemoved, FileRemoveFailed,
        FormulateDownloadSuccess, FormulateDownloadFailed

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
