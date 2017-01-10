'''
    #api_values_settings:This page will have all the values validation info like
    key_name:'key_name' will be in STRING this key_name will be act as key in json. ex: 'country_name'

    @type: twhich define the format or type of value and this can be any one of value_formats from below list.
    @length: length of the value with corresponding type. this value is optional except STRING and INT type.
    @validation_method: this will be function name to validate value. this value is optional except STRING and INT type.
    @is_optional: is True when it allows None values.

### value_type = [STRING, TEXT, INT, BOOL, VECTOR_TYPE_STRING, VECTOR_TYPE_INT, VECTOR_TYPE, ENUM_TYPE]
### validation_method = [is_alphabet, is_alphanumeric, is_date, is_address, is_numeric ]
'''

from protocol.api_key_validation import *
from server.constants import CAPTCHA_LENGTH

__all__ = [
    'api_params'
]

api_params = {
    'request': {},
    'session_token': {'type': 'TEXT', 'length': 50, 'validation_method': None, 'is_optional': False},
    'reset_token': {'type': 'TEXT', 'length': 50, 'validation_method': None, 'is_optional': False},

    'new_password': {'type': 'TEXT', 'length': 20, 'validation_method': None, 'is_optional': False},
    'current_password': {'type': 'TEXT', 'length': 20, 'validation_method': None, 'is_optional': False},

    'login_type': {'type': 'ENUM_TYPE', 'length': None,  'validation_method': None, 'module_name': 'core', 'class_name': 'SESSION_TYPE'},
    'username': {'type': 'TEXT', 'length': 100, 'validation_method': None, 'is_optional': False},
    'password': {'type': 'TEXT', 'length': 20, 'validation_method': None, 'is_optional': False},
    'short_name': {'type': 'TEXT', 'length': 100, 'validation_method': None, 'is_optional': True},
    'ip': {'type': 'TEXT', 'length': 100, 'validation_method': None, 'is_optional': False},
    'user_client_id': {'type': 'INT', 'length': 500, 'validation_methods': None, 'is_optional': True},
    'captcha_text': {'type': 'STRING', 'length': CAPTCHA_LENGTH, 'validation_method': is_alpha_numeric, 'is_optional': True},

    'form_id': {'type': 'INT', 'length': 100, 'validation_method': None, 'is_optional': False},

    'form_name': {'type': 'STRING', 'length': 50, 'validation_method': allow_specialchar, 'is_optional': False},
    'form_url': {'type': 'TEXT', 'length': 250, 'validation_method': is_url, 'is_optional': False},
    'parent_menu': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': True},
    'form_type': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},

    "s_p_id": {'type': 'INT', 'length': 11, 'validation_method':None, 'is_optional': False},
    "s_p_name": {'type': 'STRING', 'length': 50, 'validation_method':is_alpha_numeric, 'is_optional': False},
    "s_p_short": {'type': 'STRING', 'length': 20, 'validation_method':is_alpha_numeric, 'is_optional': False},
    "cont_from": {'type': 'TEXT', 'length': 20, 'validation_method':None, 'is_optional': False},
    "cont_to": {'type': 'TEXT', 'length': 20, 'validation_method':None, 'is_optional': False},
    "cont_person": {'type': 'STRING', 'length': 50, 'validation_method':is_alphabet, 'is_optional': False},
    "cont_no": {'type': 'TEXT', 'length': 20, 'validation_method':None, 'is_optional': False},
    "e_id": {'type': 'STRING', 'length': 100, 'validation_method':is_alpha_numeric, 'is_optional': False},
    "mob_no": {'type': 'TEXT', 'length': 20, 'validation_method':None, 'is_optional': True},
    "address": {'type': 'TEXT', 'length': 500, 'validation_method':None, 'is_optional': True},
    "is_active": {'type': 'BOOL', 'length': None, 'validation_method':None, 'is_optional': True},
    "status_changed_by": {'type': 'INT', 'length': 11, 'validation_method':is_numeric, 'is_optional': True},
    "status_changed_on": {'type': 'TEXT', 'length': 20, 'validation_method':None, 'is_optional': True},
    "is_blocked": {'type': 'BOOL', 'length': None, 'validation_method':None, 'is_optional': False},    
    "unblock_days": {'type': 'INT', 'length': 10, 'validation_method':is_numeric, 'is_optional': True},
    "blocked_by": {'type': 'INT', 'length': 11, 'validation_method':is_numeric, 'is_optional': True},
    "blocked_on": {'type': 'STRING', 'length': 20, 'validation_method':None, 'is_optional': True},
    "remarks": {'type': 'TEXT', 'length': 500, 'validation_method':None, 'is_optional': True},
    "created_by": {'type': 'INT', 'length': 11, 'validation_method':is_numeric, 'is_optional': True},
    "created_on": {'type': 'TEXT', 'length': 20, 'validation_method':None, 'is_optional': True},
    "updated_by": {'type': 'INT', 'length': 11, 'validation_method':is_numeric, 'is_optional': True},
    "updated_on": {'type': 'TEXT', 'length': 20, 'validation_method':None, 'is_optional': True},
    "service_providers": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method':None, 'is_optional': False,'module_name': 'core', "class_name": "ServiceProviderDetails"},
    

    'u_g_id': {'type': 'INT', 'length': 1000, 'validation_method': None, 'is_optional': False},
    'u_g_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'is_active': {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': False},
    'u_c_id': {'type': 'INT', 'length': 1000, 'validation_method': None, 'is_optional': False},
    'f_ids': {'type': 'VECTOR_TYPE_INT', 'length': 1000, 'validation_method': None, 'is_optional': True},
    'u_c_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    "forms":  {'type': 'MAP_TYPE', 'length': None, 'validation_method': is_numeric, 'is_optional': False, 'module_name': 'core', "class_name": "Menu"},
    "menus":  {'type': 'MAP_TYPE_VECTOR_TYPE', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False, 'module_name': 'core', "class_name": "Form"},
    "user_groups": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "ClientUserGroup"},
    "user_category": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "ClientUsercategory"},    
    'form_ids': {'type': 'INT', 'length': 100, 'validation_method': None, 'is_optional': False},

    }