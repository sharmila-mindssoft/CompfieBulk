from replication.jsonvalidators import (parse_dictionary, parse_static_list)
from replication.parse_structure import (
    parse_structure_VectorType_RecordType_protocol_Change,
    parse_structure_Text, parse_structure_SignedIntegerType_64,
    parse_structure_OptionalType_Text,
    parse_structure_Bool,
    parse_structure_VectorType_RecordType_protocol_Client
)
from replication.to_structure import (
    to_structure_VectorType_RecordType_protocol_Change,
    to_structure_Text, to_structure_SignedIntegerType_64,
    to_structure_OptionalType_Text,
    to_structure_Bool,
    to_structure_VectorType_RecordType_protocol_Client
)

#
# Change
#

class Change(object):
    def __init__(self, audit_trail_id, tbl_name, tbl_auto_id, column_name, value, client_id, action):
        self.audit_trail_id = audit_trail_id
        self.tbl_name = tbl_name
        self.tbl_auto_id = tbl_auto_id
        self.column_name = column_name
        self.value = value
        self.client_id = client_id
        self.action = action

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["audit_trail_id", "tbl_name", "tbl_auto_id", "column_name", "value", "client_id", "action"])
        audit_trail_id = data.get("audit_trail_id")
        audit_trail_id = parse_structure_SignedIntegerType_64(audit_trail_id)
        tbl_name = data.get("tbl_name")
        tbl_name = parse_structure_Text(tbl_name)
        tbl_auto_id = data.get("tbl_auto_id")
        tbl_auto_id = parse_structure_SignedIntegerType_64(tbl_auto_id)
        column_name = data.get("column_name")
        column_name = parse_structure_Text(column_name)
        value = data.get("value")
        value = parse_structure_OptionalType_Text(value)
        client_id = data.get("client_id")
        client_id = parse_structure_SignedIntegerType_64(client_id)
        action = data.get("action")
        action = parse_structure_Text(action)
        return Change(audit_trail_id, tbl_name, tbl_auto_id, column_name, value, client_id, action)

    def to_structure(self):
        return {
            "audit_trail_id": to_structure_SignedIntegerType_64(self.audit_trail_id),
            "tbl_name": to_structure_Text(self.tbl_name),
            "tbl_auto_id": to_structure_SignedIntegerType_64(self.tbl_auto_id),
            "column_name": to_structure_Text(self.column_name),
            "value": to_structure_OptionalType_Text(self.value),
            "client_id": to_structure_SignedIntegerType_64(self.client_id),
            "action": to_structure_Text(self.action),
        }

class Client(object):
    def __init__(self, client_id, is_new_data, is_new_domain, domain_id):
        self.client_id = client_id
        self.is_new_data = is_new_data
        self.is_new_domain = is_new_domain
        self.domain_id = domain_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["client_id", "is_new_data", "is_new_domain", "domain_id"])
        client_id = data.get("client_id")
        client_id = parse_structure_SignedIntegerType_64(client_id)
        is_new_data = data.get("is_new_data")
        is_new_data = parse_structure_Bool(is_new_data)
        is_new_domain = data.get("is_new_domain")
        is_new_domain = parse_structure_Bool(is_new_domain)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_OptionalType_Text(domain_id)
        return Client(client_id, is_new_data, is_new_domain, domain_id)

    def to_structure(self):
        return {
            "client_id": to_structure_SignedIntegerType_64(self.client_id),
            "is_new_data": to_structure_Bool(self.is_new_data),
            "is_new_domain": to_structure_Bool(self.is_new_domain),
            "domain_id": to_structure_OptionalType_Text(self.domain_id)
        }

#
# GetChanges
#

class GetChanges(object):
    def __init__(self, client_id, received_count):
        self.client_id = client_id
        self.received_count = received_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["client_id", "received_count"])
        client_id = data.get("client_id")
        client_id = parse_structure_SignedIntegerType_64(client_id)
        received_count = data.get("received_count")
        received_count = parse_structure_SignedIntegerType_64(received_count)
        return GetChanges(client_id, received_count)

    def to_structure(self):
        return {
            "client_id": to_structure_SignedIntegerType_64(self.client_id),
            "received_count": to_structure_SignedIntegerType_64(self.received_count),
        }

class GetClientChanges(object):
    def __init__(self):
        pass

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [])
        return GetClientChanges()

    def to_structure(self):
        return {
        }


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

class GetChangesSuccess(Response):
    def __init__(self, changes):
        self.changes = changes

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["changes"])
        changes = data.get("changes")
        changes = parse_structure_VectorType_RecordType_protocol_Change(changes)
        return GetChangesSuccess(changes)

    def to_inner_structure(self):
        return {
            "changes": to_structure_VectorType_RecordType_protocol_Change(self.changes),
        }

class GetClientChangesSuccess(Response):
    def __init__(self, clients):
        self.clients = clients

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["clients"])
        clients = data.get("clients")
        clients = parse_structure_VectorType_RecordType_protocol_Client(clients)
        return GetClientChangesSuccess(clients)

    def to_inner_structure(self):
        return {
            "clients": to_structure_VectorType_RecordType_protocol_Client(self.clients),
        }


class GetDelReplicatedSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetDelReplicatedSuccess()

    def to_inner_structure(self):
        return {
        }

class InvalidReceivedCount(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidReceivedCount()

    def to_inner_structure(self):
        return {
        }


def _init_Response_class_map():
    classes = [GetChangesSuccess, GetClientChangesSuccess, InvalidReceivedCount, GetDelReplicatedSuccess]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()
