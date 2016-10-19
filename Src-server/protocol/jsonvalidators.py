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
    print "x"
    print x
    print type(x)
    # print len(x)
    if x is None:
        raise empty_error()
    if type(x) is not list:
        print "yes list"
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
        print "parse bg"
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
    print field_name, param, val
    _type = param.get('type')
    _length = param.get('length')
    _is_optional = param.get('is_optional')
    _validation_method = param.get('validation_method')
    # if param is None:
    #     val = parse_vector_type_record_type(val)
    #     continue
    if _type == 'STRING':
        assert _length is not None
        assert _validation_method is not None
        if _is_optional is False:
            val = parse_custom_string(val, _length)
        else:
            val = parse_optional_custom_string(val, _length)

    elif _type == 'TEXT':
        if _is_optional is False:
            val = parse_string(val)
        else:
            val = parse_optional_string(val)

    elif _type == 'INT':
        assert _length is not None
        if _is_optional is False:
            val = parse_number(val, 0, _length)
        else:
            val = parse_optional_number(val, 0, _length)

    elif _type == 'BOOL':
        assert _length is None
        assert _validation_method is None
        if _is_optional is False:
            val = parse_bool(val)
        else:
            val = parse_optional_bool(val)

    elif _type == 'VECTOR_TYPE_STRING':
        # list_of_string by default support optional
        assert _validation_method is None
        if _is_optional is False:
            val = parse_string_list(val, string_length=_length)
        else:
            val = parse_optional_string_list(
                val, string_length=_length)

    elif _type == 'VECTOR_TYPE_INT':
        # list_of_int by default support optional
        assert _validation_method is None
        if _is_optional is False:
            val = parse_int_list(val, int_length=_length)
        else:
            val = parse_optional_int_list(
                val, int_length=param.get('length'))

    return val


def parse_dictionary_values(x, field_names=[], is_validation_and_parse=False):
    for field_name in field_names:
        val = x.get(field_name)
        param = api_params.get(field_name)
        if param is None:
            raise ValueError('%s is not configured in settings' % (field_name))

        _type = param.get('type')
        _module_name = param.get('module_name')
        _class_name = param.get('class_name')
        _validation_method = param.get('validation_method')

        if _type == 'VECTOR_TYPE':
            assert _module_name is not None
            assert _class_name is not None
            val = parse_VectorType(
                _module_name, _class_name, val
            )
            if is_validation_and_parse is True:
                x[field_name] = val
        elif _type == 'MAP_TYPE':
            print param
            print field_name
            print val
            assert _module_name is not None
            assert _class_name is not None
            assert _validation_method is not None
            val = parse_MapType(
                _module_name, _class_name,
                _validation_method, val
            )
            if is_validation_and_parse is True:
                x[field_name] = val

        elif _type == 'MAP_TYPE_VECTOR_TYPE':
            print 'parse_dictionary_values'
            map = {}
            print val
            print '-------------------'

            for key, value in val.items():
                print '-------------------'
                key = _validation_method(key)
                print key
                vals = []
                if type(value) is list :
                    for l in value :
                        vals.append(to_RecordType(_module_name, _class_name, value))
                map[key] = vals
                val = map

        elif _type == 'RECORD_TYPE' :
            assert _module_name is not None
            assert _class_name is not None
            val = parse_RecordType(_module_name, _class_name, val)

        elif _type == 'ENUM_TYPE':
            assert _module_name is not None
            assert _class_name is not None
            val = parse_EnumType(_module_name, _class_name, val)

        else:
            val = parse_values(field_name, param, val)
        if(
            val is not None and
            _validation_method is not None and
            _type != "MAP_TYPE"
        ):
            val = _validation_method(val)
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

        _type = param.get('type')
        print _type, field_name
        _module_name = param.get('module_name')
        _class_name = param.get('class_name')
        _validation_method = param.get('validation_method')
        if param is None:
            raise ValueError('%s is not configured in settings' % (field_name))

        if _type == 'VECTOR_TYPE':
            assert _module_name is not None
            assert _class_name is not None
            val = to_VectorType(
                _module_name, _class_name, val
            )
            val = to_vector_type_record_type(val)

        elif _type == 'MAP_TYPE':
            print param
            print field_name
            print val
            assert _module_name is not None
            assert _class_name is not None
            assert _validation_method is not None
            val = to_MapType(
                _module_name, _class_name,
                _validation_method, val
            )
        elif _type == 'MAP_TYPE_VECTOR_TYPE':
            map = {}
            print val
            print '-------------------'

            for key, value in val.items():
                print '-------------------'
                key = _validation_method(key)
                print key
                vals = []
                if type(value) is list :
                    for l in value :
                        vals.append(to_RecordType(_module_name, _class_name, value))
                map[key] = vals
                val = map
        elif _type == 'RECORD_TYPE' :
            assert _module_name is not None
            assert _class_name is not None
            val = to_RecordType(_module_name, _class_name, val)

        elif _type == 'ENUM_TYPE':
            assert _module_name is not None
            assert _class_name is not None
            val = to_EnumType(_module_name, _class_name, val)
        else:
            val = parse_values(field_name, param, val)

        if(
            val is not None and _validation_method is not None and
            _type != 'MAP_TYPE'
        ):
            val = _validation_method(val)

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
    print "inside item"
    for item in data:
        print item
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
    print '-------------------'

    for key, value in data.items():
        print '-------------------'
        key = validation_method(key)
        dict_value = to_RecordType(module_name, class_name, value)
        map[key] = dict_value
    return map

def parse_EnumType(module_name, class_name, data):
    return parse_RecordType(module_name, class_name, data)

def to_EnumType(module_name, class_name, data):
    return to_RecordType(module_name, class_name, data)
