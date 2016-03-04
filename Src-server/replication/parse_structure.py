from sets import Set
from replication.jsonvalidators import (
    parse_bool,
    parse_number,
    parse_point_numbers,
    parse_string,
    parse_custom_string,
    parse_bytes,
    parse_list,
    parse_dictionary,
    parse_enum,
    parse_date
)

def parse_structure_RecordType_protocol_Response_GetChangesSuccess(data):
    from replication import protocol
    return protocol.Response.parse_structure(data)

def parse_structure_Text(data):
    return parse_string(data)

def parse_structure_VariantType_protocol_Response(data):
    from replication import protocol
    return protocol.Response.parse_structure(data)

def parse_structure_RecordType_protocol_Change(data):
    from replication import protocol
    return protocol.Change.parse_structure(data)

def parse_structure_SignedIntegerType_64(data):
    return parse_number(data, -9223372036854775808, 9223372036854775807)

def parse_structure_RecordType_protocol_Response_InvalidReceivedCount(data):
    from replication import protocol
    return protocol.Response.parse_structure(data)

def parse_structure_RecordType_protocol_GetChanges(data):
    from replication import protocol
    return protocol.GetChanges.parse_structure(data)

def parse_structure_VectorType_RecordType_protocol_Change(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_protocol_Change(item))
    return lst

def parse_structure_OptionalType_Text(data):
    if data is '' or data is None : return None
    return parse_structure_Text(data)
