from clientprotocol.jsonvalidators_client import (
    parse_number,
    parse_custom_string,
    parse_list,
)


def to_structure_VectorType(data, fn):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(fn(item))
    return lst


def to_structure_MapType(data, fn1, fn2):
    map = {}
    for key, value in data.items():
        key = fn1(key)
        value = fn2(value)
        map[key] = value
    return map


def to_structure_EnumType_core_SESSION_TYPE(data):
    from clientprotocol import core
    return core.SESSION_TYPE.to_structure(data)

def to_structure_EnumType_core_USER_TYPE(data):
    from clientprotocol import core
    return core.USER_TYPE.to_structure(data)

def to_structure_EnumType_core_COMPLIANCE_APPROVAL_STATUS(data):
    from clientprotocol import core
    return core.COMPLIANCE_APPROVAL_STATUS.to_structure(data)

def to_structure_EnumType_core_COMPLIANCE_ACTIVITY_STATUS(data):
    from clientprotocol import core
    return core.COMPLIANCE_ACTIVITY_STATUS.to_structure(data)

def to_structure_EnumType_core_COMPLIANCE_STATUS(data):
    from clientprotocol import core
    return core.COMPLIANCE_STATUS.to_structure(data)

def to_structure_EnumType_core_APPLICABILITY_STATUS(data):
    from clientprotocol import core
    return core.APPLICABILITY_STATUS.to_structure(data)

def to_structure_EnumType_core_REPEATS_TYPE(data):
    from clientprotocol import core
    return core.REPEATS_TYPE.to_structure(data)

def to_structure_EnumType_core_DURATION_TYPE(data):
    from clientprotocol import core
    return core.DURATION_TYPE.to_structure(data)

def to_structure_EnumType_core_APPROVAL_STATUS(data):
    from clientprotocol import core
    return core.APPROVAL_STATUS.to_structure(data)

def to_structure_OptionalType_EnumType_core_APPLICABILITY_STATUS(data):
    if data is None:
        return data
    return to_structure_EnumType_core_APPLICABILITY_STATUS(data)

def to_structure_EnumType_core_FILTER_TYPE(data):
    from clientprotocol import core
    return core.FILTER_TYPE.to_structure(data)

def to_structure_EnumType_core_COMPLIANCE_FREQUENCY(data):
    from clientprotocol import core
    return core.COMPLIANCE_FREQUENCY.to_structure(data)

# not complied enum type

def to_structure_EnumType_core_NOT_COMPLIED_TYPE(data):
    from clientprotocol import core
    return core.NOT_COMPLIED_TYPE.to_structure(data)


def to_structure_VectorType_UnsignedIntegerType_32(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_UnsignedIntegerType_32(item))
    return lst

def to_structure_UnsignedIntegerType_32(data):
    return parse_number(data, 0, 52949672950)

def to_structure_CustomTextType_50(data):
    return parse_custom_string(data, 50)

def to_structure_MapType_UnsignedInteger_32_VectorType_UnsignedInteger_32(data):
    data = parse_list(data)
    d = {}
    for key, value in data:
        key = to_structure_UnsignedIntegerType_32(key)
        value = to_structure_VectorType_UnsignedIntegerType_32(value)
        d[key] = value
    return d


def return_import(module, class_name):
    mod = __import__('protocol.'+module, fromlist=[class_name])
    klass = getattr(mod, class_name)
    return klass


def to_structure_MapType_CustomTextType_50_VectorType_UnsignedIntegerType_32(data):
    return to_structure_MapType(
        data, to_structure_CustomTextType_50,
        to_structure_UnsignedIntegerType_32
    )
