from protocol.jsonvalidators import (
    parse_number,
    parse_list,
    parse_dictionary
)


def to_structure_VectorType_UnsignedIntegerType_32(data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(to_structure_UnsignedIntegerType_32(item))
    return lst

def to_structure_UnsignedIntegerType_32(data):
    return parse_number(data, 0, 52949672950)

def to_structure_EnumType_core_REPEATS_TYPE(data):
    from protocol import core
    return core.REPEATS_TYPE.to_structure(data)

def to_structure_EnumType_core_DURATION_TYPE(data):
    from protocol import core
    return core.DURATION_TYPE.to_structure(data)

def to_structure_EnumType_core_COMPLIANCE_FREQUENCY(data):
    from protocol import core
    return core.COMPLIANCE_FREQUENCY.to_structure(data)

def to_structure_MapType_UnsignedInteger_32_VectorType_UnsignedInteger_32(
    data
):
    data = parse_dictionary(data)
    dict = {}
    for key, value in data.items():
        key = to_structure_UnsignedIntegerType_32(key)
        value = to_structure_VectorType_UnsignedIntegerType_32(value)
        dict[key] = value
    return dict


def return_import(module, class_name):
    mod = __import__('protocol.'+module, fromlist=[class_name])
    klass = getattr(mod, class_name)
    return klass
