from sets import Set
from distribution.jsonvalidators import (
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

def to_structure_RecordType_protocol_Company(data):
    from distribution import protocol
    return protocol.Company.to_structure(data)

def to_structure_RecordType_protocol_Request_GetCompanyServerDetails(data):
    from distribution import protocol
    return protocol.Request.to_structure(data)

def to_structure_UnsignedIntegerType_8(data):
    return parse_number(data, 0, 255)

def to_structure_UnsignedIntegerType_32(data):
    return parse_number(data, 0, 4294967295)

def to_structure_VectorType_RecordType_protocol_Company(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_RecordType_protocol_Company(item))
    return lst

def to_structure_Text(data):
    return parse_string(data)

def to_structure_VariantType_protocol_Response(data):
    from distribution import protocol
    return protocol.Response.to_structure(data)

def to_structure_VariantType_protocol_Request(data):
    from distribution import protocol
    return protocol.Request.to_structure(data)

def to_structure_RecordType_protocol_IPAddress(data):
    from distribution import protocol
    return protocol.IPAddress.to_structure(data)

def to_structure_RecordType_protocol_Response_CompanyServerDetails(data):
    from distribution import protocol
    return protocol.Response.to_structure(data)

