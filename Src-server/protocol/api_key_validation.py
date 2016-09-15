import re

def expectation_error(expected, received) :
    msg = "expected %s, but received: %s"
    return ValueError(msg % (expected, str(received)))

def is_alphabet(value):
    r = re.compile("^[a-zA-Z ]*$")  # a-z with space
    if r.match(value):
        return value
    else :
        raise expectation_error('a alphabets', value)

def is_numeric(value):
    r = re.compile("^[0-9 ]*$")  # 0-9 with space
    if r.match(value):
        return value
    else :
        raise expectation_error('a numeric', value)


def is_alpha_numeric(value):
    r = re.compile("^[a-zA-Z0-9 ]*$")  # a-z and 0-9 with space
    if r.match(value):
        return value
    else :
        raise expectation_error('a alphanumerics', value)

def is_address(value):
    r = re.compile("^[a-zA-Z0-9_.,-@# ]*$")  # a-z0-9 with special char and space
    if r.match(value):
        return value
    else :
        raise expectation_error('a alphanumerics with _.,-@#', value)

def is_url(value):
    r = re.compile("^[a-z/-]*$")  # a-z with space
    if r.match(value):
        return value
    else :
        raise expectation_error('a url', value)

def is_mapping(value):
    r = re.compile("^[a-zA-Z>>- ]*$")  # a-z with space
    if r.match(value):
        return value
    else :
        raise expectation_error('a string', value)

def is_industry(value):
    r = re.compile("^[a-zA-Z &]*$")  # a-z with space
    if r.match(value):
        return value
    else :
        raise expectation_error('a alphabets', value)
