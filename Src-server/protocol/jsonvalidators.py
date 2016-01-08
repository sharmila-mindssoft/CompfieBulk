__all__ = [
    "parse_bool",
    "parse_number",
    "parse_point_numbers",
    "parse_string",
    "parse_custom_string"
    "parse_bytes",
    "parse_list",
    "parse_static_list",
    "parse_dictionary",
    "parse_enum",
    "parse_date"
]


#
# JSON structure parsing helpers
#

def expectation_error(expected, received) :
    msg = "expected %s, but received: %s"
    return ValueError(msg % (expected, repr(received)))

def empty_error():
    return ValueError("null is not allowed")

def parse_bool(x) :
    if x is None:
        raise empty_error()
    if type(x) not in (bool,) :
        raise expectation_error("a bool", x)
    return x

def parse_number(x, min_value, max_value) :
    if x is None:
        raise empty_error()
    if type(x) not in (int, long) :
        raise expectation_error("a number", x)
    if x >= min_value and x <= max_value:
        return x
    else:
        msg = "a number between %s and %s" % (
            min_value, max_value
        )
        raise expectation_error(msg, x)

def parse_point_numbers(x) :
    if x is None:
        raise empty_error()
    if type(x) not in (int, long, float) :
        raise expectation_error("a number", x)
    return x

def parse_string(x) :
    if x is None:
        raise empty_error()
    t = type(x)
    if t is unicode :
        return x.encode("utf8")
    elif t is str :
        return x
    else :
        raise expectation_error("a string", x)

def parse_custom_string(x, length) :
    if x is None:
        raise empty_error()
    t = type(x)
    custom_string = None
    if t is unicode :
        custom_string = x.encode("utf8")
    elif t is str :
        custom_string = x
    else :
        raise expectation_error("a string", x)
    if len(custom_string) > length:
        raise expectation_error(
            "a string with max length(%s)" % (
                length,
            ),
            x
        )
    return custom_string

def parse_bytes(x) :
    if x is None:
        raise empty_error()
    t = type(x)
    if t is unicode :
        return x
    elif t is str :
        return x.decode("utf8")
    else :
        raise expectation_error("a byte", x)

def parse_list(x, length=0) :
    if x is None:
        raise empty_error()
    if type(x) is not list :
        raise expectation_error("a list", x)
    if len(x) <= length or length == 0:
        return x
    else:
        msg = "a list with %s items" % (length,)
        raise expectation_error(msg, x)

def parse_static_list(x, length=0) :
    if x is None:
        raise empty_error()
    if type(x) is not list :
        raise expectation_error("a list", x)
    if len(x) == length:
        return x
    else:
        msg = "a list with %s items" % (length,)
        raise expectation_error(msg, x)

def parse_dictionary(x, field_names=[]) :
    if x is None:
        raise empty_error()
    if type(x) is not dict :
        raise expectation_error("a dict", x)
    for field_name in field_names:
        if field_name not in x.keys():
            msg = "key \"%s\" is missing in the dictionary" % (
                field_name
            )
            raise expectation_error(msg, x)
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

def parse_date(x) :
    if x is None:
        raise empty_error()
    x = parse_string(x)
    try:
        return datetime.strptime(x, "%d/%m/%Y")
    except Exception, e:
        print e
        return None
