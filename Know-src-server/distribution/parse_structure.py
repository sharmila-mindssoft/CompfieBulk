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

def parse_structure_RecordType_protocol_Company(data):
    from distribution import protocol
    return protocol.Company.parse_structure(data)

def parse_structure_RecordType_protocol_Request_GetCompanyServerDetails(data):
    from distribution import protocol
    return protocol.Request.parse_structure(data)

def parse_structure_UnsignedIntegerType_8(data):
    return parse_number(data, 0, 255)

def parse_structure_UnsignedIntegerType_32(data):
    return parse_number(data, 0, 4294967295)

def parse_structure_VectorType_RecordType_protocol_Company(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_RecordType_protocol_Company(item))
    return lst

def parse_structure_Text(data):
    return parse_string(data)

def parse_structure_VariantType_protocol_Response(data):
    from distribution import protocol
    return protocol.Response.parse_structure(data)

def parse_structure_VariantType_protocol_Request(data):
    from distribution import protocol
    return protocol.Request.parse_structure(data)

def parse_structure_RecordType_protocol_IPAddress(data):
    from distribution import protocol
    return protocol.IPAddress.parse_structure(data)

def parse_structure_RecordType_protocol_Response_CompanyServerDetails(data):
    from distribution import protocol
    return protocol.Response.parse_structure(data)

