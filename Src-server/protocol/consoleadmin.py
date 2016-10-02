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


class GetClientServerList(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data)
        return GetClientServerList()

    def to_structure(self):
        return {
        }


class SaveClientServer(Request):
    def __init__(self, client_server_id, client_server_name, ip, port):
        self.client_server_id = client_server_id
        self.client_server_name = client_server_name
        self.ip = ip
        self.port = port

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["client_server_id", "client_server_name", "ip", "port"])
        client_server_id = data.get("client_server_id")
        client_server_name = data.get("client_server_name")
        ip = data.get("ip")
        port = data.get("port")
        return SaveClientServer(client_server_id, client_server_name, ip, port)

    def to_structure(self):
        data = {
            "client_server_id": self.client_server_id,
            "client_server_name": self.client_server_name,
            "ip": self.ip,
            "port": self.port
        }
        return to_dictionary_values(data)


class GetAllocatedDBEnv(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data)
        return GetAllocatedDBEnv()

    def to_structure(self):
        return {
        }


class SaveAllocatedDBEnv(Request):
    def __init__(
        self, client_id, legal_entity_id, database_server_ip, machine_id
    ):
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.database_server_ip = database_server_ip
        self.machine_id = machine_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "client_id", "legal_entity_id",
                "database_server_ip", "machine_id"
            ]
        )
        return SaveAllocatedDBEnv(
            data.get("client_id"), data.get("legal_entity_id"),
            data.get("database_server_ip"), data.get("machine_id")
        )

    def to_structure(self):
        data = {
            "client_id": self.client_id,
            "legal_entity_id": self.legal_entity_id,
            "database_server_ip": self.database_server_ip,
            "machine_id": self.machine_id
        }
        return to_dictionary_values(data)


def _init_Request_class_map():
    classes = [
        GetDbServerList, SaveDBServer, GetClientServerList, SaveClientServer,
        GetAllocatedDBEnv, SaveAllocatedDBEnv
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


class DBServerNameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return DBServerNameAlreadyExists()

    def to_inner_structure(self):
        return {}


class ClientServer(object):
    def __init__(
        self, client_server_id, client_server_name, ip, port, no_of_clients
    ):
        self.client_server_id = client_server_id
        self.client_server_name = client_server_name
        self.ip = ip
        self.port = port
        self.no_of_clients = no_of_clients

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
                "client_server_id", "client_server_name",
                "ip", "port", "no_of_clients"
            ])
        client_server_id = data.get("client_server_id")
        client_server_name = data.get("client_server_name")
        ip = data.get("ip")
        port = data.get("port")
        no_of_clients = data.get("no_of_clients")
        return ClientServer(
            client_server_id, client_server_name, ip, port, no_of_clients
        )

    def to_structure(self):
        data = {
            "client_server_id": self.client_server_id,
            "client_server_name": self.client_server_name,
            "ip": self.ip,
            "port": self.port,
            "no_of_clients": self.no_of_clients
        }
        return to_dictionary_values(data)


class GetClientServerListSuccess(Response):
    def __init__(self, client_servers):
        self.client_servers = client_servers

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["client_servers"])
        client_servers = data.get("client_servers")
        return GetClientServerListSuccess(client_servers)

    def to_inner_structure(self):
        data = {
            "client_servers": self.client_servers
        }
        return to_dictionary_values(data)


class SaveClientServerSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveClientServerSuccess()

    def to_inner_structure(self):
        return {}


class ClientServerNameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ClientServerNameAlreadyExists()

    def to_inner_structure(self):
        return {}


class ClientDatabase(object):
    def __init__(
        self, client_id, legal_entity_id, machine_id, database_server_ip
    ):
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.machine_id = machine_id
        self.database_server_ip = database_server_ip

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data,
            [
                "client_id", "legal_entity_id",
                "machine_id", "database_server_ip"
            ]
        )
        client_id = data.get("client_id")
        legal_entity_id = data.get("legal_entity_id")
        machine_id = data.get("machine_id")
        database_server_ip = data.get("database_server_ip")
        return ClientDatabase(
            client_id, legal_entity_id, machine_id, database_server_ip
        )

    def to_structure(self):
        data = {
            "client_id": self.client_id,
            "legal_entity_id": self.legal_entity_id,
            "machine_id": self.machine_id,
            "database_server_ip": self.database_server_ip
        }
        return to_dictionary_values(data)


class ClientGroup(object):
    def __init__(self, client_id, group_name):
        self.client_id = client_id
        self.group_name = group_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["client_id", "group_name"])
        client_id = data.get("client_id")
        group_name = data.get("group_name")
        return ClientGroup(client_id, group_name)

    def to_structure(self):
        data = {
            "client_id": self.client_id,
            "group_name": self.group_name
        }
        return to_dictionary_values(data)


class LegalEntity(object):
    def __init__(self, legal_entity_id, legal_entity_name, client_id):
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.client_id = client_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["legal_entity_id", "legal_entity_name", "client_id"])
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_name = data.get("legal_entity_name")
        client_id = data.get("client_id")
        return LegalEntity(legal_entity_id, legal_entity_name, client_id)

    def to_structure(self):
        data = {
            "legal_entity_id": self.legal_entity_id,
            "legal_entity_name": self.legal_entity_name,
            "client_id": self.client_id
        }
        return to_dictionary_values(data)


class ClientServerNameAndID(object):
    def __init__(self, machine_id, machine_name):
        self.machine_id = machine_id
        self.machine_name = machine_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["machine_id", "machine_name"])
        machine_id = data.get("machine_id")
        machine_name = data.get("machine_name")
        return ClientServerNameAndID(machine_id, machine_name)

    def to_structure(self):
        data = {
            "machine_id": self.machine_id,
            "machine_name": self.machine_name
        }
        return to_dictionary_values(data)


class DBServerNameAndID(object):
    def __init__(self, db_server_name, ip):
        self.db_server_name = db_server_name
        self.ip = ip

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["db_server_name", "ip"])
        db_server_name = data.get("db_server_name")
        ip = data.get("ip")
        return DBServerNameAndID(db_server_name, ip)

    def to_structure(self):
        data = {
            "db_server_name": self.db_server_name,
            "ip": self.ip
        }
        return to_dictionary_values(data)


class GetAllocatedDBEnvSuccess(Response):
    def __init__(
        self, client_dbs, client_groups, client_legal_entities,
        client_server_name_and_id, db_server_name_and_id
    ):
        self.client_dbs = client_dbs
        self.client_groups = client_groups
        self.client_legal_entities = client_legal_entities
        self.client_server_name_and_id = client_server_name_and_id
        self.db_server_name_and_id = db_server_name_and_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "client_dbs", "client_groups", "client_legal_entities",
                "client_server_name_and_id", "db_server_name_and_id"
            ]
        )
        client_dbs = data.get("client_dbs")
        client_groups = data.get("client_groups")
        client_legal_entities = data.get("client_legal_entities")
        client_server_name_and_id = data.get("client_server_name_and_id")
        db_server_name_and_id = data.get("db_server_name_and_id")
        return GetAllocatedDBEnvSuccess(
            client_dbs, client_groups, client_legal_entities,
            client_server_name_and_id, db_server_name_and_id
        )

    def to_inner_structure(self):
        data = {
            "client_dbs": self.client_dbs,
            "client_groups": self.client_groups,
            "client_legal_entities": self.client_legal_entities,
            "client_server_name_and_id": self.client_server_name_and_id,
            "db_server_name_and_id": self.db_server_name_and_id
        }
        return to_dictionary_values(data)


class SaveAllocatedDBEnvSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveAllocatedDBEnvSuccess()

    def to_inner_structure(self):
        return {}


def _init_Response_class_map():
    classes = [
        GetDbServerListSuccess, SaveDBServerSuccess, DBServerNameAlreadyExists,
        GetClientServerListSuccess, SaveClientServerSuccess,
        ClientServerNameAlreadyExists, GetAllocatedDBEnvSuccess,
        GetAllocatedDBEnvSuccess, SaveAllocatedDBEnvSuccess
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
