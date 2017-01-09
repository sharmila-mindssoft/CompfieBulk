'''
    #api_values_settings:This page will have all the values validation info like
    key_name:'key_name' will be in STRING this key_name will be act as key in json. ex: 'country_name'

    @type: twhich define the format or type of value and this can be any one of value_formats from below list.
    @length: length of the value with corresponding type. this value is optional except STRING and INT type.
    @validation_method: this will be function name to validate value. this value is optional except STRING and INT type.
    @is_optional: is True when it allows None values.

### value_type = [STRING, TEXT, INT, BOOL, VECTOR_TYPE_STRING, VECTOR_TYPE_INT, VECTOR_TYPE, ENUM_TYPE]
### validation_method = [is_alphabet, is_alphanumeric, is_date, is_address ]
'''

from clientprotocol.api_key_validation_client import *
from server.constants import CAPTCHA_LENGTH

__all__ = [
    'api_params'
]

def make_int_field(length=1000, is_optional=False):
    return {'type': 'INT', 'length': length, 'is_optional': is_optional}

def make_string_field(length=100, is_optional=False, validfun=allow_specialchar):
    return {'type': 'STRING', 'length': length , 'validation_method': validfun, 'is_optional': is_optional}

def make_text_field(length=100, is_optional=False):
    return {'type': 'TEXT', 'length': length , 'is_optional': is_optional}

def make_vector_type_field(module, klass_name, is_optional=False):
    return {'type': 'VECTOR_TYPE', 'is_optional': is_optional, 'module_name': module, "class_name": klass_name}

def make_vector_type_int(length=100, is_optional=False):
    return {'type': 'VECTOR_TYPE_INT', 'length': length, 'is_optional': is_optional}

def make_bool_field():
    return {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': False}

def make_enum_type(module, klass_name):
    return {'type': 'ENUM_TYPE', 'module_name': module, 'class_name': klass_name}

def make_map_type(module, klass_name, validfun=is_numeric, is_optional=False):
    return {'type': 'MAP_TYPE', 'validation_method': validfun, 'is_optional': is_optional, 'module_name': module, "class_name": klass_name}

def make_map_type_vector_type(module, klass_name, length=50, validfun=is_alphabet):
    return {'type': 'MAP_TYPE_VECTOR_TYPE', 'length': length, 'validation_method': validfun, 'is_optional': False, 'module_name': module, "class_name": klass_name}

api_params = {
    'request': {},
    'session_token': make_text_field(length=50),
    'reset_token':  make_text_field(length=50),

    'new_password': make_text_field(length=20),
    'current_password': make_text_field(length=20),

    'login_type': make_enum_type("clientcore", "SESSION_TYPE"),
    'username': make_text_field(length=100),
    'password': make_text_field(length=100),
    'short_name': make_text_field(length=50),
    'ip': make_text_field(length=50),
    'user_client_id': make_int_field(is_optional=True),
    'captcha_text': make_string_field(length=CAPTCHA_LENGTH, is_optional=True, validfun=is_alpha_numeric),
    'form_id': make_int_field(length=100),
    'form_name': make_string_field(length=50, validfun=allow_specialchar),
    'form_url': make_string_field(length=250, validfun=is_url),
    'parent_menu': make_string_field(length=50, is_optional=True, validfun=is_alphabet),
    'form_type': make_string_field(length=50, validfun=is_alphabet),

    'u_g_id': make_int_field(is_optional=True),
    'u_g_name': make_string_field(length=50, validfun=is_alpha_numeric, is_optional=True),
    'is_active': make_bool_field(),
    'u_c_id': make_int_field,
    'f_ids': make_vector_type_int(length=1000, is_optional=True),
    'u_c_name': make_string_field(length=50, validfun=is_alpha_numeric),
    "forms": make_map_type("clientcore", "Menu"),
    "menus": make_map_type_vector_type("clientcore", "Form"),

    "user_groups": make_vector_type_field("clientcore", "ClientUserGroup"),
    "user_category": make_vector_type_field("clientcore", "ClientUsercategory"),

    'form_ids': make_int_field(),

    "entity_info": make_vector_type_field(module="clientcode", klass_name="LegalEntityInfo"),
    "ct_id": make_int_field(),
    "le_id": make_int_field(),
    "le_name": make_string_field(),
    "bg_name": make_string_field(is_optional=True),
    "bg_id": make_int_field(is_optional=True),
    "usr_id": make_int_field(),
    "email_id": make_string_field(validfun=allow_specialchar),
    "emp_name": make_string_field(is_optional=True),
    "emp_code": make_string_field(is_optional=True),
    "con_no": make_string_field(is_optional=True),
    "mob_no": make_string_field(is_optional=True),
    "address": make_text_field(is_optional=True),
    "menu":  make_map_type_vector_type("clientcore", "Form"),

    "u_id": make_int_field(),
    "u_name": make_string_field(),
    "c_name": make_string_field(),
    "c_id": make_int_field(),
    "c_name": make_string_field(),
    "d_name": make_string_field(),
    "div_name": make_string_field(is_optional=True),
    "is_closed": make_bool_field(),
    "is_new": make_bool_field(),
    "statutories": make_vector_type_field(module="clienttransactions", klass_name="UnitStatutoryCompliances")
}
