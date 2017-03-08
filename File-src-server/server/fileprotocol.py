# File Protocol
#
# Request
#

def parse_static_list(x, length=0):
    if x is None:
        raise ValueError("null is not allowed")
    if type(x) is not list:
        raise ValueError("expected a list, but received:", x)
    if len(x) == length:
        return x
    else:
        msg = "expected a list with %s items" % (length,)
        raise ValueError(msg, x)

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
        self, client_id, legal_entity_id, country_id, unit_id, domain_id,  start_date, file_content,
        file_name
    ):
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.country_id = country_id
        self.domain_id = domain_id
        self.start_date = start_date
        self.file_content = file_content
        self.file_name = file_name

    @staticmethod
    def parse_inner_structure(data):
        return UploadComplianceTaskFile(
            data.get("ct_id"),
            data.get("le_id"), data.get("c_id"), data.get("d_id"),
            data.get("start_date"), data.get("file_content"),
            data.get("file_name")
        )

    def to_inner_structure(self):
        return {
            "ct_id": self.client_id,
            "le_id": self.legal_entity_id,
            "c_id": self.country_id,
            "d_id": self.domain_id,
            "start_date": self.start_date,
            "file_content": self.file_content,
            "file_name": self.file_name
        }

def _init_Request_class_map():
    classes = [UploadComplianceTaskFile]
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

class UploadFileSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        return UploadFileSuccess()

    def to_inner_structure(self):
        return {}

def _init_Response_class_map():
    classes = [
        UploadFileSuccess

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
        # data = parse_dictionary(data, ["session_token", "request"])
        session_token = data.get("session_token")
        request = data.get("request")
        request = Request.parse_structure(request)
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": Request.to_structure(self.request)
        }
