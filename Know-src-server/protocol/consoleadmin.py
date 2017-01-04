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
        return _Request_class_map[name].parse_structure(data)

    @staticmethod
    def parse_inner_structure(data):
        raise NotImplementedError


class GetDatabaseServerList(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data)
        return GetDatabaseServerList()

    def to_structure(self):
        return {
        }


class SaveDBServer(Request):
    def __init__(self, db_server_id, db_server_name, ip, port, username, password):
        self.db_server_id = db_server_id
        self.db_server_name = db_server_name
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["db_server_id", "db_server_name", "ip", "port", "username", "password"])
        db_server_id = data.get("db_server_id")
        db_server_name = data.get("db_server_name")
        ip = data.get("ip")
        port = data.get("port")
        username = data.get("username")
        password = data.get("password")
        return SaveDBServer(db_server_id, db_server_name, ip, port, username, password)

    def to_structure(self):
        return {
            "db_server_id": self.db_server_id,
            "db_server_name": self.db_server_name,
            "ip": self.ip,
            "port": self.port,
            "username": self.username,
            "password": self.password
        }


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
        return {
            "client_server_id": self.client_server_id,
            "client_server_name": self.client_server_name,
            "ip": self.ip,
            "port": self.port
        }

class GetFileServerList(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data)
        return GetFileServerList()

    def to_structure(self):
        return {
        }

class SaveFileServer(Request):
    def __init__(self, file_server_id, file_server_name, ip, port):
        self.file_server_id = file_server_id
        self.file_server_name = file_server_name
        self.ip = ip
        self.port = port

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["file_server_id", "file_server_name", "ip", "port"])
        file_server_id = data.get("file_server_id")
        file_server_name = data.get("file_server_name")
        ip = data.get("ip")
        port = data.get("port")
        return SaveFileServer(file_server_id, file_server_name, ip, port)

    def to_structure(self):
        return {
            "file_server_id": self.file_server_id,
            "file_server_name": self.file_server_name,
            "ip": self.ip,
            "port": self.port
        }

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
        return {
            "client_id": self.client_id,
            "legal_entity_id": self.legal_entity_id,
            "database_server_ip": self.database_server_ip,
            "machine_id": self.machine_id
        }


class GetFileStorage(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data)
        return GetFileStorage()

    def to_structure(self):
        return {
        }


class SaveFileStorage(Request):
    def __init__(
        self, client_id, legal_entity_id, machine_id
    ):
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.machine_id = machine_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "client_id", "legal_entity_id", "machine_id"
            ]
        )
        return SaveFileStorage(
            data.get("client_id"), data.get("legal_entity_id"),
            data.get("machine_id")
        )

    def to_structure(self):
        return {
            "client_id": self.client_id,
            "legal_entity_id": self.legal_entity_id,
            "machine_id": self.machine_id
        }


class GetAutoDeletionList(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data)
        return GetAutoDeletionList()

    def to_structure(self):
        return {
        }


class AutoDeletionDetail(Request):
    def __init__(
        self, client_id, legal_entity_id, unit_id, deletion_period
    ):
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.unit_id = unit_id
        self.deletion_period = deletion_period

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["client_id", "legal_entity_id", "unit_id", "deletion_period"]
        )
        return AutoDeletionDetail(
            data.get("client_id"), data.get("legal_entity_id"),
            data.get("unit_id"), data.get("deletion_period")
        )

    def to_structure(self):
        return {
            "client_id": self.client_id,
            "legal_entity_id": self.legal_entity_id,
            "unit_id": self.unit_id,
            "deletion_period": self.deletion_period
        }


class SaveAutoDeletion(Request):
    def __init__(
        self, auto_deletion_details
    ):
        self.auto_deletion_details = auto_deletion_details

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["auto_deletion_details"]
        )
        return SaveAutoDeletion(data.get("auto_deletion_details"))

    def to_structure(self):
        return {
            "auto_deletion_details": self.auto_deletion_details
        }


class GetIPSettingsList(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data)
        return GetIPSettingsList()

    def to_structure(self):
        return {
        }

class GetGroupIPDetails(Request):
    def __init__(
        self, client_id
    ):
        self.client_id = client_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["client_id"]
        )
        return GetGroupIPDetails(
            data.get("client_id")
        )

    def to_structure(self):
        return {
            "client_id": self.client_id,
        }

class SaveIPSettings(Request):
    def __init__(
        self, group_ips_list
    ):
        self.group_ips_list = group_ips_list

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["group_ips_list"]
        )
        return SaveIPSettings(data.get("group_ips_list"))

    def to_structure(self):
        return {
            "group_ips_list": self.group_ips_list
        }

class DeleteIPSettings(Request):
    def __init__(
        self, client_id
    ):
        self.client_id = client_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["client_id"]
        )
        return DeleteIPSettings(
            data.get("client_id")
        )

    def to_structure(self):
        return {
            "client_id": self.client_id,
        }

def _init_Request_class_map():
    classes = [
        GetDatabaseServerList, SaveDBServer, GetClientServerList, SaveClientServer,
        GetAllocatedDBEnv, SaveAllocatedDBEnv, GetFileStorage, SaveFileStorage,
        GetAutoDeletionList, SaveAutoDeletion, GetFileServerList,
        SaveFileServer, GetIPSettingsList, GetGroupIPDetails, SaveIPSettings, DeleteIPSettings
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
        return _Response_class_map[name].parse_structure(data)

    @staticmethod
    def parse_inner_structure(data):
        raise NotImplementedError


class DBServer(object):
    def __init__(
        self, db_server_id, db_server_name, ip, port, username, password, no_of_clients
    ):
        self.db_server_id = db_server_id
        self.db_server_name = db_server_name
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.no_of_clients = no_of_clients

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
                "db_server_id", "db_server_name", "ip", "port", "username",
                "password", "no_of_clients"
            ])
        db_server_id = data.get("db_server_id")
        db_server_name = data.get("db_server_name")
        ip = data.get("ip")
        port = data.get("port")
        username = data.get("username")
        password = data.get("password")
        no_of_clients = data.get("no_of_clients")
        return DBServer(
            db_server_id, db_server_name, ip, port, username, password, no_of_clients)

    def to_structure(self):
        return {
            "db_server_id": self.db_server_id,
            "db_server_name": self.db_server_name,
            "ip": self.ip,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "no_of_clients": self.no_of_clients
        }


class GetDbServerListSuccess(Response):
    def __init__(self, db_servers):
        self.db_servers = db_servers

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["db_servers"])
        db_servers = data.get("db_servers")
        return GetDbServerListSuccess(db_servers)

    def to_inner_structure(self):
        return {
            "db_servers": self.db_servers
        }


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
        return {
            "client_server_id": self.client_server_id,
            "client_server_name": self.client_server_name,
            "ip": self.ip,
            "port": self.port,
            "no_of_clients": self.no_of_clients
        }


class GetClientServerListSuccess(Response):
    def __init__(self, client_servers):
        self.client_servers = client_servers

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["client_servers"])
        client_servers = data.get("client_servers")
        return GetClientServerListSuccess(client_servers)

    def to_inner_structure(self):
        return {
            "client_servers": self.client_servers
        }


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
        return {
            "client_id": self.client_id,
            "legal_entity_id": self.legal_entity_id,
            "machine_id": self.machine_id,
            "database_server_ip": self.database_server_ip
        }


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
        return {
            "client_id": self.client_id,
            "group_name": self.group_name
        }


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
        return {
            "legal_entity_id": self.legal_entity_id,
            "legal_entity_name": self.legal_entity_name,
            "client_id": self.client_id
        }


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
        return {
            "machine_id": self.machine_id,
            "machine_name": self.machine_name
        }


class FileServerList(object):
    def __init__(self, file_server_id, file_server_name, ip, port, no_of_clients):
        self.file_server_id = file_server_id
        self.file_server_name = file_server_name
        self.ip = ip
        self.port = port
        self.no_of_clients = no_of_clients

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["file_server_id", "filer_server_name", "ip", "port", "no_of_clients"])
        file_server_id = data.get("file_server_id")
        file_server_name = data.get("file_server_name")
        ip = data.get("ip")
        port = data.get("port")
        no_of_clients = data.get("no_of_clients")

        return FileServerList(file_server_id, file_server_name, ip, port, no_of_clients)

    def to_structure(self):
        return {
            "file_server_id": self.file_server_id,
            "file_server_name": self.file_server_name,
            "ip": self.ip,
            "port": self.port,
            "no_of_clients": self.no_of_clients
        }

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
        return {
            "db_server_name": self.db_server_name,
            "ip": self.ip
        }


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
        return {
            "client_dbs": self.client_dbs,
            "client_groups": self.client_groups,
            "client_legal_entities": self.client_legal_entities,
            "client_server_name_and_id": self.client_server_name_and_id,
            "db_server_name_and_id": self.db_server_name_and_id
        }


class SaveAllocatedDBEnvSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveAllocatedDBEnvSuccess()

    def to_inner_structure(self):
        return {}


class FileStorage(object):
    def __init__(
        self, client_id, legal_entity_id, machine_id
    ):
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.machine_id = machine_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data,
            [
                "client_id", "legal_entity_id", "machine_id"
            ]
        )
        client_id = data.get("client_id")
        legal_entity_id = data.get("legal_entity_id")
        machine_id = data.get("machine_id")
        return FileStorage(
            client_id, legal_entity_id, machine_id
        )

    def to_structure(self):
        return {
            "client_id": self.client_id,
            "legal_entity_id": self.legal_entity_id,
            "machine_id": self.machine_id
        }


class GetFileStorageSuccess(Response):
    def __init__(
        self, file_storages, client_groups, client_legal_entities,
        client_server_name_and_id
    ):
        self.file_storages = file_storages
        self.client_groups = client_groups
        self.client_legal_entities = client_legal_entities
        self.client_server_name_and_id = client_server_name_and_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "file_storages", "client_groups", "client_legal_entities",
                "client_server_name_and_id"
            ]
        )
        file_storages = data.get("file_storages")
        client_groups = data.get("client_groups")
        client_legal_entities = data.get("client_legal_entities")
        client_server_name_and_id = data.get("client_server_name_and_id")
        return GetFileStorageSuccess(
            file_storages, client_groups, client_legal_entities,
            client_server_name_and_id
        )

    def to_inner_structure(self):
        return {
            "file_storages": self.file_storages,
            "client_groups": self.client_groups,
            "client_legal_entities": self.client_legal_entities,
            "client_server_name_and_id": self.client_server_name_and_id
        }


class SaveFileStorageSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveFileStorageSuccess()

    def to_inner_structure(self):
        return {}


class EntitiesWithAutoDeletion(object):
    def __init__(
        self, legal_entity_id, legal_entity_name, client_id,
        unit_count, deletion_period, is_closed
    ):
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.client_id = client_id
        self.unit_count = unit_count
        self.deletion_period = deletion_period
        self.is_closed = is_closed

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "legal_entity_id", "legal_entity_name", "client_id",
                "unit_count", "deletion_period", "is_closed"
            ]
        )
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_name = data.get("legal_entity_name")
        client_id = data.get("client_id")
        unit_count = data.get("unit_count")
        deletion_period = data.get("deletion_period")
        is_closed = data.get("is_closed")
        return EntitiesWithAutoDeletion(
            legal_entity_id, legal_entity_name, client_id,
            unit_count, deletion_period, is_closed
        )

    def to_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id,
            "legal_entity_name": self.legal_entity_name,
            "client_id": self.client_id,
            "unit_count": self.unit_count,
            "deletion_period": self.deletion_period,
            "is_closed": self.is_closed
        }


class Unit(object):
    def __init__(
        self, unit_id, client_id, legal_entity_id, unit_code, unit_name,
        deletion_period, address
    ):
        self.unit_id = unit_id
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.deletion_period = deletion_period
        self.address = address

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "unit_id", "client_id", "legal_entity_id", "unit_code",
                "unit_name", "deletion_period", "address"
            ]
        )
        unit_id = data.get("unit_id")
        client_id = data.get("client_id")
        legal_entity_id = data.get("legal_entity_id")
        unit_code = data.get("unit_code")
        unit_name = data.get("unit_name")
        deletion_period = data.get("deletion_period")
        address = data.get("address")
        return Unit(
            unit_id, client_id, legal_entity_id, unit_code, unit_name,
            deletion_period, address
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id,
            "client_id": self.client_id,
            "legal_entity_id": self.legal_entity_id,
            "unit_code": self.unit_code,
            "unit_name": self.unit_name,
            "deletion_period": self.deletion_period,
            "address": self.address
        }

class Form(object):
    def __init__(
        self, form_id, form_name
    ):
        self.form_id = form_id
        self.form_name = form_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "form_id", "form_name"
            ]
        )
        form_id = data.get("form_id")
        form_name = data.get("form_name")
        
        return Unit(
            form_id, form_name
        )

    def to_structure(self):
        return {
            "form_id": self.form_id,
            "form_name": self.form_name
        }

class IPSettingsList(object):
    def __init__(
        self, client_id, form_id, group_name
    ):
        self.client_id = client_id
        self.form_id = form_id
        self.group_name = group_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "client_id", "form_id", "group_name"
            ]
        )
        client_id = data.get("client_id")
        form_id = data.get("form_id")
        group_name = data.get("group_name")
        
        return Unit(
            client_id, form_id, group_name
        )

    def to_structure(self):
        return {
            "client_id": self.client_id,
            "form_id": self.form_id,
            "group_name": self.group_name
        }

class GroupIPDetails(object):
    def __init__(
        self, form_id, ip, client_id
    ):
        self.form_id = form_id
        self.ip = ip
        self.client_id = client_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "form_id", "ip", "client_id"
            ]
        )
        form_id = data.get("form_id")
        ip = data.get("ip")
        client_id = data.get("client_id")
        
        return GroupIPDetails(
            form_id, ip, client_id
        )

    def to_structure(self):
        return {
            "form_id": self.form_id,
            "ip": self.ip,
            "client_id": self.client_id
        }

class GetAutoDeletionListSuccess(Response):
    def __init__(
        self, client_groups, auto_deletion_entities, auto_deletion_units
    ):
        self.client_groups = client_groups
        self.auto_deletion_entities = auto_deletion_entities
        self.auto_deletion_units = auto_deletion_units

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "client_groups", "auto_deletion_entities",
                "auto_deletion_units"
            ]
        )
        client_groups = data.get("client_groups")
        auto_deletion_entities = data.get("auto_deletion_entities")
        auto_deletion_units = data.get("auto_deletion_units")
        return GetAutoDeletionListSuccess(
            client_groups, auto_deletion_entities, auto_deletion_units
        )

    def to_inner_structure(self):
        return {
            "client_groups": self.client_groups,
            "auto_deletion_entities": self.auto_deletion_entities,
            "auto_deletion_units": self.auto_deletion_units
        }

class GetFileServerListSuccess(Response):
    def __init__(self, file_servers):
        self.file_servers = file_servers

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["file_servers"])
        file_servers = data.get("file_servers")
        return GetFileServerListSuccess(file_servers)

    def to_inner_structure(self):
        return {
            "file_servers": self.file_servers
        }

class FileServerNameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return FileServerNameAlreadyExists()

    def to_inner_structure(self):
        return {}

class SaveFileServerSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveFileServerSuccess()

    def to_inner_structure(self):
        return {}

class SaveAutoDeletionSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveAutoDeletionSuccess()

    def to_inner_structure(self):
        return {}


class GetIPSettingsListSuccess(Response):
    def __init__(
        self, client_groups, ip_setting_forms, ips_list
    ):
        self.client_groups = client_groups
        self.ip_setting_forms = ip_setting_forms
        self.ips_list = ips_list

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "client_groups", "ip_setting_forms", "ips_list"
            ]
        )
        client_groups = data.get("client_groups")
        ip_setting_forms = data.get("ip_setting_forms")
        ips_list = data.get("ips_list")
        return GetAutoDeletionListSuccess(
            client_groups, ip_setting_forms, ips_list
        )

    def to_inner_structure(self):
        return {
            "client_groups": self.client_groups,
            "ip_setting_forms": self.ip_setting_forms,
            "ips_list": self.ips_list
        }

class GetGroupIPDetailsSuccess(Response):
    def __init__(
        self, group_ips_list
    ):
        self.group_ips_list = group_ips_list

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
               "group_ips_list"
            ]
        )
        group_ips_list = data.get("group_ips_list")
        return GetGroupIPDetailsSuccess(
            group_ips_list
        )

    def to_inner_structure(self):
        return {
            "group_ips_list": self.group_ips_list
        }

class SaveIPSettingsSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveIPSettingsSuccess()

    def to_inner_structure(self):
        return {}

class DeleteIPSettingsSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return DeleteIPSettingsSuccess()

    def to_inner_structure(self):
        return {}

def _init_Response_class_map():
    classes = [
        GetDbServerListSuccess, SaveDBServerSuccess, DBServerNameAlreadyExists,
        GetClientServerListSuccess, SaveClientServerSuccess,
        ClientServerNameAlreadyExists, GetAllocatedDBEnvSuccess,
        GetAllocatedDBEnvSuccess, SaveAllocatedDBEnvSuccess,
        GetFileStorageSuccess, SaveFileStorageSuccess,
        GetAutoDeletionListSuccess, SaveAutoDeletionSuccess,
        GetFileServerListSuccess, SaveFileServerSuccess, FileServerNameAlreadyExists,
        GetIPSettingsListSuccess, GetGroupIPDetailsSuccess, DeleteIPSettingsSuccess
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
