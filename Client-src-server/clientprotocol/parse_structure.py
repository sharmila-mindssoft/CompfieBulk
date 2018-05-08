from clientprotocol.jsonvalidators_client import (
    parse_number,
    parse_custom_string,
    parse_list,
)


def parse_structure_VectorType(data, fn):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(fn(item))
    return lst


def parse_structure_MapType(data, fn1, fn2):
    map = {}
    for key, value in data.items():
        key = fn1(key)
        value = fn2(value)
        map[key] = value
    return map


def parse_structure_EnumType_core_SESSION_TYPE(data):
    from clientprotocol import core
    return core.SESSION_TYPE.parse_structure(data)

def parse_structure_EnumType_core_USER_TYPE(data):
    from clientprotocol import core
    return core.USER_TYPE.parse_structure(data)

def parse_structure_EnumType_core_COMPLIANCE_APPROVAL_STATUS(data):
    from clientprotocol import core
    return core.COMPLIANCE_APPROVAL_STATUS.parse_structure(data)

def parse_structure_EnumType_core_COMPLIANCE_ACTIVITY_STATUS(data):
    from clientprotocol import core
    return core.COMPLIANCE_ACTIVITY_STATUS.parse_structure(data)

def parse_structure_EnumType_core_COMPLIANCE_STATUS(data):
    from clientprotocol import core
    return core.COMPLIANCE_STATUS.parse_structure(data)

def parse_structure_EnumType_core_APPLICABILITY_STATUS(data):
    from clientprotocol import core
    return core.APPLICABILITY_STATUS.parse_structure(data)

def parse_structure_EnumType_core_REPEATS_TYPE(data):
    from clientprotocol import core
    return core.REPEATS_TYPE.parse_structure(data)

def parse_structure_EnumType_core_DURATION_TYPE(data):
    from clientprotocol import core
    return core.DURATION_TYPE.parse_structure(data)

def parse_structure_EnumType_core_APPROVAL_STATUS(data):
    from clientprotocol import core
    return core.APPROVAL_STATUS.parse_structure(data)

def parse_structure_OptionalType_EnumType_core_APPLICABILITY_STATUS(data):
    if data is None:
        return data
    return parse_structure_EnumType_core_APPLICABILITY_STATUS(data)

def parse_structure_EnumType_core_FILTER_TYPE(data):
    from clientprotocol import core
    return core.FILTER_TYPE.parse_structure(data)

def parse_structure_EnumType_core_COMPLIANCE_FREQUENCY(data):
    from clientprotocol import core
    return core.COMPLIANCE_FREQUENCY.parse_structure(data)

# not complied enum type

def parse_structure_EnumType_core_NOT_COMPLIED_TYPE(data):
    from clientprotocol import core
    return core.NOT_COMPLIED_TYPE.parse_structure(data)


def parse_structure_VectorType_UnsignedIntegerType_32(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(parse_structure_UnsignedIntegerType_32(item))
    return lst

def parse_structure_UnsignedIntegerType_32(data):
    return parse_number(data, 0, 52949672950)

def parse_structure_CustomTextType_50(data):
    return parse_custom_string(data, 50)

def parse_structure_MapType_UnsignedInteger_32_VectorType_UnsignedInteger_32(data):
    data = parse_list(data)
    d = {}
    for key, value in data:
        key = parse_structure_UnsignedIntegerType_32(key)
        value = parse_structure_VectorType_UnsignedIntegerType_32(value)
        d[key] = value
    return d


def return_import(module, class_name):
    mod = __import__('protocol.'+module, fromlist=[class_name])
    klass = getattr(mod, class_name)
    return klass


def parse_structure_MapType_CustomTextType_50_VectorType_UnsignedIntegerType_32(data):
    return parse_structure_MapType(
        data, parse_structure_CustomTextType_50,
        parse_structure_UnsignedIntegerType_32
    )
