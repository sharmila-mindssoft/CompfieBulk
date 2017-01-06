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

api_params['domain_id'] = api_params.get('d_id')
api_params['domain_name'] = api_params.get('d_name')
api_params['country_id'] = api_params.get('c_id')
api_params['country_ids'] = api_params.get('c_ids')
api_params['country_name'] = api_params.get('c_name')
api_params['level_id'] = api_params.get('l_id')
api_params['level_position'] = api_params.get('l_position')
api_params['level_name'] = api_params.get('l_name')
api_params['active'] = api_params.get('is_active')
api_params['is_editable'] = api_params.get('is_active')
api_params['is_disable'] = api_params.get('is_active')
api_params['is_remove'] = api_params.get('is_active')
api_params['is_exists'] = api_params.get('is_active')
api_params['is_common'] = api_params.get('is_active')
api_params['is_admin'] = api_params.get('is_active')
api_params['applicable'] = api_params.get('is_active')
api_params['not_applicable'] = api_params.get('is_active')
api_params['not_at_all_applicable'] = api_params.get('is_active')
api_params['is_saved'] = api_params.get('is_active')
api_params['is_new'] = api_params.get('is_active')
api_params['is_rejected'] = api_params.get('is_active')
api_params['parent_id'] = api_params.get('geography_id')
api_params['parent_mappings'] = api_params.get('mapping')
api_params['p_maps'] = api_params.get('s_pnames')
api_params['level_1_statutory_id'] = api_params.get('statutory_id')
api_params['level_1_s_id'] = api_params.get('statutory_id')
api_params['level_1_statutory_name'] = api_params.get('statutory_name')
api_params['level_1_s_name'] = api_params.get('statutory_name')
api_params['g_l_id'] = api_params.get('level_id')
api_params['g_name'] = api_params.get('geography_name')
api_params['p_ids'] = api_params.get('s_pids')
api_params['p_names'] = api_params.get('s_pnames')
api_params['g_id'] = api_params.get('geography_id')
api_params['p_id'] = api_params.get('geography_id')
api_params['g_ids'] = api_params.get('statutory_ids')
api_params['i_name'] = api_params.get('industry_name')
api_params['i_id'] = api_params.get('industry_id')
api_params['i_ids'] = api_params.get('industry_ids')
api_params['s_n_name'] = api_params.get('statutory_nature_name')
api_params['s_n_id'] = api_params.get('statutory_nature_id')
api_params['s_l_id'] = api_params.get('level_id')
api_params['s_name'] = api_params.get('statutory_name')
api_params['s_id'] = api_params.get('statutory_id')
api_params['s_ids'] = api_params.get('statutory_ids')
api_params['mappings'] = api_params.get('mapping')
api_params['u_cat_id'] = api_params.get('user_category_id')
api_params['captcha'] = api_params.get('captcha_text')
api_params['token'] = api_params.get('reset_token')
api_params['uname'] = api_params.get('username')
api_params['pword'] = api_params.get('password')
api_params['c_names'] = api_params.get('mapping')
api_params["org_id"] = api_params.get("industry_id")
api_params["org_name"] = api_params.get("industry_name")
api_params["rcount"] = api_params.get("total_records")
