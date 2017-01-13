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

def make_vector_type_string(length=100, is_optional=False, validfun=allow_specialchar):
    return {'type': 'VECTOR_TYPE_STRING', 'length': length, 'is_optional': is_optional, 'validation_method': validfun}

def make_bool_field(is_optional=False):
    return {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': is_optional}

def make_enum_type(module, klass_name):
    return {'type': 'ENUM_TYPE', 'module_name': module, 'class_name': klass_name}

def make_map_type(module, klass_name, validfun=is_numeric, is_optional=False):
    return {'type': 'MAP_TYPE', 'validation_method': validfun, 'is_optional': is_optional, 'module_name': module, "class_name": klass_name}

def make_map_type_vector_type(module, klass_name, length=50, validfun=is_alphabet):
    return {'type': 'MAP_TYPE_VECTOR_TYPE', 'length': length, 'validation_method': validfun, 'is_optional': False, 'module_name': module, "class_name": klass_name}

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
    'legal_entity_id': {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': True},
    'legal_entity_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    "unit_closure_legal_entities": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'clientcore', "class_name": "UnitClosureLegalEntity"},
    'unit_id': {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': True},
    'unit_code': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'unit_name': {'type': 'TEXT', 'length': 50, 'validation_metunithod': is_alpha_numeric, 'is_optional': False},
    'address': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': True},
    'postal_code': {'type': 'INT', 'length': 1000000, 'validation_method': is_numeric, 'is_optional': False},
    'division_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'category_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'business_group_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'is_active': {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': False},
    "closed_on": {'type': 'TEXT', 'length': 200, 'validation_method': None, 'is_optional': True},
    'validity_days': {'type': 'INT', 'length': 365, 'validation_method': None, 'is_optional': True},
    "unit_closure_units": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'clientcore', "class_name": "UnitClosure_Units"},
    'grp_mode': {'type': 'string', 'length': 50, 'validation_method': None, 'is_optional': False},
    "closed_remarks": {'type': 'TEXT', 'length': 500, 'validation_method': None, 'is_optional': True},
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

    "entity_info": make_vector_type_field(module="clientcore", klass_name="LegalEntityInfo"),
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
    "user_level": make_int_field(is_optional=True),
    "sp_id": make_int_field(),
    "s_u_id": make_int_field(is_optional=True),
    "s_u_name": make_string_field(is_optional=True),
    "is_assignee": make_bool_field(),
    "is_approver": make_bool_field(),
    "is_concurrence": make_bool_field(),

    "u_id": make_int_field(),
    "u_ids": make_vector_type_int(is_optional=True),
    "u_name": make_string_field(),
    "c_name": make_string_field(),
    "c_id": make_int_field(),
    "c_name": make_string_field(),
    "c_ids": make_vector_type_int(),
    "c_names": make_vector_type_string(),
    "d_id": make_int_field(),
    "d_ids": make_vector_type_int(),
    "d_name": make_string_field(),
    "d_names": make_vector_type_string(),
    "div_id": make_int_field(),
    "div_name": make_string_field(is_optional=True),
    "is_closed": make_bool_field(),
    "is_new": make_bool_field(),
    "is_active": make_bool_field(),
    "statutories": make_vector_type_field(module="clienttransactions", klass_name="UnitStatutoryCompliances"),
    "tot_count": make_int_field(length=100000),
    "applicable_statu": make_vector_type_field(module="clienttransactions", klass_name="ComplianceApplicability"),
    "lone_statu_name": make_string_field(length=200),
    "app_status": make_bool_field(),
    "opt_status": make_bool_field(),
    "not_app_remarks": make_text_field(length=500, is_optional=True),
    "c_comp_id": make_int_field(),
    "comp_id": make_int_field(),
    "comp_name": make_string_field(),
    "descp": make_text_field(length=500),
    "s_prov": make_text_field(length=500),
    "comp_app_status": make_bool_field(),
    "comp_opt_status": make_bool_field(),
    "comp_remarks": make_text_field(length=500, is_optional=True),
    "r_count": make_int_field(length=100000),

    "countries": make_vector_type_field(module="clientcore", klass_name="Country"),
    "domains": make_vector_type_field(module="clientcore", klass_name="Domain"),
    "bg_groups": make_vector_type_field(module="clientcore", klass_name="ClientBusinessGroup"),
    "le_infos": make_vector_type_field(module="clientcore", klass_name="ClientLegalEntity"),
    "div_infos": make_vector_type_field(module="clientcore", klass_name="ClientDivision"),

    "assign_unit_infos": make_vector_type_field(module="clienttransactions", klass_name="ASSIGN_COMPLIANCE_UNITS"),
    "assign_user_info": make_vector_type_field(module="clienttransactions", klass_name="ASSIGN_COMPLIANCE_USER"),
    "two_level_approve": make_bool_field(),
    "client_admin": make_int_field()
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
