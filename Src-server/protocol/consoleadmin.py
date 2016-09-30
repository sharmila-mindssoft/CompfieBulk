from protocol.jsonvalidators import (
    parse_dictionary, parse_static_list,
    parse_VariantType, to_VariantType,
    to_dictionary_values
)


#
# Request
#
class Request(object):
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
        if _Request_class_map.get(name) is None:
            msg = "invalid request: " + name
            raise ValueError(msg)
        return _Request_class_map[name].parse_structure(data)

    @staticmethod
    def parse_inner_structure(data):
        raise NotImplementedError


class GetDbServerList(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data)
        return GetDbServerList()

    def to_structure(self):
        return {
        }


class SaveDBServer(Request):
    def __init__(self, db_server_name, ip, port, username, password):
        self.db_server_name = db_server_name
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["db_server_name", "ip", "port", "username", "password"])
        db_server_name = data.get("db_server_name")
        ip = data.get("ip")
        port = data.get("port")
        username = data.get("username")
        password = data.get("password")
        return SaveDBServer(db_server_name, ip, port, username, password)

    def to_structure(self):
        data = {
            "db_server_name": self.db_server_name,
            "ip": self.ip,
            "port": self.port,
            "username": self.username,
            "password": self.password
        }
        return to_dictionary_values(data)


def _init_Request_class_map():
    classes = [
        GetDbServerList, SaveDBServer
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
        return _Response_class_map[name].parse_structure(data)

    @staticmethod
    def parse_inner_structure(data):
        raise NotImplementedError


class DBServer(object):
    def __init__(
        self, db_server_name, ip, port, username, password, no_of_clients
    ):
        self.db_server_name = db_server_name
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.no_of_clients = no_of_clients

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
                "db_server_name", "ip", "port", "username", "password",
                "no_of_clients"
            ])
        db_server_name = data.get("db_server_name")
        ip = data.get("ip")
        port = data.get("port")
        username = data.get("username")
        password = data.get("password")
        no_of_clients = data.get("no_of_clients")
        return DBServer(
            db_server_name, ip, port, username, password, no_of_clients)

    def to_structure(self):
        data = {
            "db_server_name": self.db_server_name,
            "ip": self.ip,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "no_of_clients": self.no_of_clients
        }
        return to_dictionary_values(data)


class GetDbServerListSuccess(Response):
    def __init__(self, db_servers):
        self.db_servers = db_servers

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["db_servers"])
        db_servers = data.get("db_servers")
        return GetDbServerListSuccess(db_servers)

    def to_inner_structure(self):
        data = {
            "db_servers": self.db_servers
        }
        return to_dictionary_values(data)


class SaveDBServerSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveDBServerSuccess()

    def to_inner_structure(self):
        return {}


def _init_Response_class_map():
    classes = [
        GetDbServerListSuccess, SaveDBServerSuccess
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
        request = parse_VariantType(
            request, "consoleadmin", "Request"
        )
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": to_VariantType(
                self.request, "consoleadmin", "Response"
            )
        }
