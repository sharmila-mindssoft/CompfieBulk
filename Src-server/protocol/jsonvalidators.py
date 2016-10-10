import datetime
from collections import OrderedDict
from protocol.api_keys_settings import api_params

__all__ = [
    "parse_bool",
    "parse_number",
    "parse_point_numbers",
    "parse_string",
    "parse_custom_string",
    "parse_bytes",
    "parse_list",
    "parse_static_list",
    "parse_dictionary",
    "parse_enum",
    "parse_date",
    "parse_VariantType",
    "to_VariantType"
]


#
# JSON structure parsing helpers
#
def expectation_error(expected, received):
    msg = "expected %s, but received: %s"
    return ValueError(msg % (expected, str(received)))


def empty_error():
    return ValueError("null is not allowed")


def parse_bool(x):
    if x is None:
        raise empty_error()
    if type(x) not in (bool,):
        raise expectation_error("a bool", x)
    return x


def parse_optional_bool(x):
    if x is None:
        return None
    return parse_bool(x)


def parse_number(x, min_value, max_value):
    if x is None:
        raise empty_error()
    if type(x) not in (int, long):
        raise expectation_error("a number", x)
    if x >= min_value and x <= max_value:
        return x
    else:
        msg = "a number between %s and %s" % (
            min_value, max_value
        )
        # msg = "a number greater than 0"
        raise expectation_error(msg, x)


def parse_optional_number(x, min_value, max_value):
    if x is None:
        return None
    return parse_number(x, min_value, max_value)


def parse_point_numbers(x):
    if x is None:
        raise empty_error()
    if type(x) not in (int, long, float):
        raise expectation_error("a number", x)
    return x


def parse_string(x):
    if x is None:
        raise empty_error()
    # elif x  == "":
    #     raise empty_error()
    t = type(x)
    if (x.find('>>') < 0):
        x = x.replace(">", "")
        x = x.replace("<", "")
    if t is unicode:
        x = x.encode("utf-8")
        # x = x.replace("'", "")
        return x
    elif t is str:
        # x = x.replace("'", "")
        return x
    else:
        raise expectation_error("a string", x)


def parse_optional_string(x):
    if x is None:
        return None
    return parse_string(x)


def parse_custom_string(x, length):
    if x is None:
        raise empty_error()
    # elif x is "":
    #     raise empty_error()
    t = type(x)
    if (x.find('>>') < 0):
        x = x.replace(">", "")
        x = x.replace("<", "")

    custom_string = None
    if t is unicode:
        x = x.encode("utf-8")
        # x = x.replace("'", "")
        custom_string = x
    elif t is str:
        # x = x.replace("'", "")
        custom_string = x
    else:
        raise expectation_error("a string", x)
    if len(custom_string) > length:
        raise expectation_error(
            "a string with max length(%s)" % (
                length,
            ),
            x
        )
    return custom_string


def parse_optional_custom_string(x, length):
    if x is None:
        return None
    return parse_custom_string(x, length)


def parse_bytes(x):
    if x is None:
        raise empty_error()
    # elif x  == "":
    #     raise empty_error()
    t = type(x)
    if t is unicode:
        return x
    elif t is str:
        return x.decode("utf8")
    else:
        raise expectation_error("a byte", x)


def parse_list(x, length=0):
    if x is None:
        raise empty_error()
    if type(x) is not list:
        raise expectation_error("a list", x)
    if len(x) <= length or length == 0:
        return x
    else:
        msg = "a list with %s items" % (length,)
        raise expectation_error(msg, x)


def parse_static_list(x, length=0):
    if x is None:
        raise empty_error()
    if type(x) is not list:
        raise expectation_error("a list", x)
    if len(x) == length:
        return x
    else:
        msg = "a list with %s items" % (length,)
        raise expectation_error(msg, x)


def parse_dictionary(x, field_names=[]):
    if x is None:
        raise empty_error()
    if (type(x) is not dict) and (type(x) is not OrderedDict):
        raise expectation_error("a dict", x)
    for field_name in field_names:
        if field_name not in x.keys():
            msg = "key \"%s\" is missing in the dictionary" % (
                field_name
            )
            raise expectation_error(msg, x)
    if len(field_names) > 0:
        x = parse_dictionary_values(x, field_names, True)

    return x


def parse_enum(x, items):
    if x is None:
        raise empty_error()
    x = parse_string(x)
    if x not in items:
        msg = "a string value any one of  %s" % (
            ",".join(items)
        )
        raise expectation_error(msg, x)
    return x


def parse_date(x):
    if x is None:
        raise empty_error()
    x = parse_string(x)
    try:
        return datetime.strptime(x, "%d/%m/%Y")
    except Exception, e:
        print e
        return None


def parse_string_list(x, length=0, string_length=0):
    if x is None:
        raise None
    if type(x) is not list:
        raise expectation_error("a list ", x)
    for y in x:
        if type(y) not in [str, unicode]:
            raise expectation_error("a list with string values ", x)
        else:
            y = parse_custom_string(y, string_length)
    return x


def parse_optional_string_list(x, length=0, string_length=0):
    if x is None:
        return None
    return parse_string_list(x, length, string_length)


def parse_int_list(x, length=0, int_length=0):
    if x is None:
        raise None
    if type(x) is not list:
        raise expectation_error("a list ", x)
    for y in x:
        if type(y) is not int:
            raise expectation_error("a list with integer values ", x)
        else:
            y = parse_number(y, 0, int_length)
    return x


def parse_optional_int_list(x, length=0, int_length=0):
    if x is None:
        return None
    return parse_int_list(x, length, int_length)


def parse_values(field_name, param, val):
    # if param is None:
    #     val = parse_vector_type_record_type(val)
    #     continue
    if param.get('type') == 'STRING':
        assert param.get('length') is not None
        assert param.get('validation_method') is not None
        if param.get('is_optional') is False:
            val = parse_custom_string(val, param.get('length'))
        else:
            val = parse_optional_custom_string(val, param.get('length'))

    elif param.get('type') == 'TEXT':
        if param.get('is_optional') is False:
            val = parse_string(val)
        else:
            val = parse_optional_string(val)

    elif param.get('type') == 'INT':
        assert param.get('length') is not None
        if param.get('is_optional') is False:
            val = parse_number(val, 0, param.get('length'))
        else:
            val = parse_optional_number(val, 0, param.get('length'))

    elif param.get('type') == 'BOOL':
        assert param.get('length') is None
        assert param.get('validation_method') is None
        if param.get('is_optional') is False:
            val = parse_bool(val)
        else:
            val = parse_optional_bool(val)

    elif param.get('type') == 'VECTOR_TYPE_STRING':
        # list_of_string by default support optional
        assert param.get('validation_method') is None
        if param.get('is_optional') is False:
            val = parse_string_list(val, string_length=param.get('length'))
        else:
            val = parse_optional_string_list(
                val, string_length=param.get('length'))

    elif param.get('type') == 'VECTOR_TYPE_INT':
        # list_of_int by default support optional
        assert param.get('validation_method') is None
        if param.get('is_optional') is False:
            val = parse_int_list(val, int_length=param.get('length'))
        else:
            val = parse_optional_int_list(
                val, int_length=param.get('length'))

    elif param.get('type') == 'ENUM_TYPE':
            assert param.get('class_name') is not None
            # val = parse

    return val


def parse_dictionary_values(x, field_names=[], is_validation_and_parse=False):
    for field_name in field_names:
        val = x.get(field_name)
        param = api_params.get(field_name)
        if param is None:
            raise ValueError('%s is not configured in settings' % (field_name))

        if param.get('type') == 'VECTOR_TYPE':
            assert param.get('module_name') is not None
            assert param.get('class_name') is not None
            val = parse_VectorType(
                param.get('module_name'), param.get('class_name'), val
            )
            if is_validation_and_parse is True:
                x[field_name] = val
        elif param.get('type') == 'MAP_TYPE':
            assert param.get('module_name') is not None
            assert param.get('class_name') is not None
            assert param.get('validation_method') is not None
            val = parse_MapType(
                param.get('module_name'), param.get('class_name'),
                param.get('validation_method'), val
            )
            if is_validation_and_parse is True:
                x[field_name] = val
        else:
            val = parse_values(field_name, param, val)
        if(
            val is not None and
            param.get('validation_method') is not None and
            param.get("type") != "map_type"
        ):
            val = param.get('validation_method')(val)
    return x


def to_vector_type_record_type(value):
    final_list = []
    if type(value) is list:
        for v in value:
            v = to_structure_dictionary_values(v)
            final_list.append(v)
    return final_list


def to_structure_dictionary_values(x):
    keys = x.keys()
    if len(keys) == 0:
        return {}
    for field_name in keys:
        val = x.get(field_name)
        param = api_params.get(field_name)
        if param is None:
            raise ValueError('%s is not configured in settings' % (field_name))

        if param.get('type') == 'VECTOR_TYPE':
            assert param.get('module_name') is not None
            assert param.get('class_name') is not None
            val = to_VectorType(
                param.get('module_name'), param.get('class_name'), val
            )
            val = to_vector_type_record_type(val)

        elif param.get('type') == 'MAP_TYPE':
            assert param.get('module_name') is not None
            assert param.get('class_name') is not None
            assert param.get('validation_method') is not None
            val = to_MapType(
                param.get('module_name'), param.get('class_name'),
                param.get("validation_method"), val
            )
        else:
            val = parse_values(field_name, param, val)

        if(
            val is not None and param.get('validation_method') is not None and
            param.get('type') != 'MAP_TYPE'
        ):
            val = param.get('validation_method')(val)

        x[field_name] = val
    return x

    # if klass is not None:
    #     return [
    #         klass, x
    #     ]


def return_import(module, class_name):
    mod = __import__('protocol.'+module, fromlist=[class_name])
    klass = getattr(mod, class_name)
    return klass


def parse_VariantType(data, module_name, class_name):
    klass = return_import(module_name, class_name)
    return klass.parse_structure(data)


def to_VariantType(data, module_name, class_name):
    klass = return_import(module_name, class_name)
    return klass.to_structure(data)


def parse_RecordType(module_name, class_name, data):
    klass = return_import(module_name, class_name)
    return klass.parse_structure(data)


def to_RecordType(module_name, class_name, data):
    klass = return_import(module_name, class_name)
    return klass.to_structure(data)


def parse_VectorType(module_name, class_name, data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(
            parse_RecordType(module_name, class_name, item)
        )
    return lst


def to_VectorType(module_name, class_name, data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(
            to_RecordType(module_name, class_name, item)
        )
    return lst


def parse_MapType(module_name, class_name, validation_method, data):
    map = {}
    for key, value in data.items():
        key = validation_method(key)
        parsed_value = parse_RecordType(module_name, class_name, value)
        map[key] = parsed_value
    return map


def to_MapType(module_name, class_name, validation_method, data):
    map = {}
    for key, value in data.items():
        key = validation_method(key)
        dict_value = to_RecordType(module_name, class_name, value)
        map[key] = dict_value
    return map
