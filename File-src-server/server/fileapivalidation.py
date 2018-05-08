from collections import OrderedDict
# import fileprotocol

def make_int_field(length=10000, is_optional=False):
    return {'type': 'INT', 'length': length, 'is_optional': is_optional}

def make_text_field(length=100, is_optional=False):
    return {'type': 'TEXT', 'length': length , 'is_optional': is_optional}

def make_vector_type_field(module, klass_name, is_optional=False):
    return {'type': 'VECTOR_TYPE', 'is_optional': is_optional, 'module_name': module, "class_name": klass_name}

api_params = {
    "request": {},
    "session_token": make_text_field(length=50),
    "ct_id": make_int_field(),
    "c_id": make_int_field(),
    "le_id": make_int_field(),
    "u_id": make_int_field(),
    "d_id": make_int_field(),
    "start_date": make_text_field(),
    "file_name": make_text_field(),
    "file_content": make_text_field(length=62914560),
    "file_info": make_vector_type_field(module="fileprotocol", klass_name="FileList"),
    "formulate_info": make_text_field(),
    "extra_details": make_text_field(),
    "unique_code": make_text_field(),
    "del_date": make_text_field()

}


#
# JSON structure parsing helpers
#
def expectation_error(expected, received):
    msg = "expected %s, but received: %s"
    return ValueError(msg % (expected, str(received)))


def empty_error():
    return ValueError("null is not allowed")


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


def parse_string(x):
    if x is None:
        raise empty_error()
    # elif x  == "":
    #     raise empty_error()
    t = type(x)
    if t not in [str, unicode] :
        raise expectation_error("a string ", x)
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
    if t not in [str, unicode] :
        raise expectation_error("a string ", x)

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

def return_import(module, class_name):
    mod = __import__("server."+module, fromlist=[class_name])
    klass = getattr(mod, class_name)
    return klass

def parse_RecordType(module_name, class_name, data):
    klass = return_import(module_name, class_name)
    return klass.parse_structure(data)

def parse_VectorType(module_name, class_name, data):
    data = parse_list(data, 0)
    lst = []
    for item in data:
        lst.append(
            parse_RecordType(module_name, class_name, item)
        )
    return lst

def parse_optional_custom_string(x, length):
    if x is None:
        return None
    return parse_custom_string(x, length)

def parse_values(field_name, param, val, type="To"):
    _type = param.get('type')
    _length = param.get('length')
    _is_optional = param.get('is_optional')
    _validation_method = param.get('validation_method')

    if _type == 'STRING':

        assert _length is not None
        assert _validation_method is not None
        if _is_optional is False:
            if len(val) == 0:
                raise expectation_error(
                    "a string with max length(%s) for %s" % (
                        _length, field_name
                    ),
                    val
                )
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

    return val

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
        _is_optional = param.get("is_optional")
        if _type == 'VECTOR_TYPE':
            assert _module_name is not None
            assert _class_name is not None
            if _is_optional is False or val is not None:
                val = parse_VectorType(
                    _module_name, _class_name, val
                )
            if is_validation_and_parse is True:
                x[field_name] = val
        else:
            val = parse_values(field_name, param, val, "parse")
        if(
            val is not None and
            _validation_method is not None and
            _type != "MAP_TYPE" and type(val) != list
        ):
            val = _validation_method(val)
    return x
