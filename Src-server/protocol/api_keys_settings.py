'''
    #api_values_settings : This page will have all the values validation info like
    key_name : 'key_name' will be in string this key_name will be act as key in json. ex: 'country_name'

    @type: twhich define the format or type of value and this can be any one of value_formats from below list.
    @length: length of the value with corresponding type. this value is optional except string and int type.
    @validation_method: this will be function name to validate value. this value is optional except string and int type.
    @is_optional: is True when it allows None values.

### value_type = [string, text, int, bool, vector_type_string, vector_type_int]
### validation_method = [is_alphabet, is_alphanumeric, is_date, is_address ]
example
    {
        'country_name': string, 50, is_alphabet
    }
'''
from protocol.api_key_validation import *

__all__ = [
    'api_params'
]

api_params = {
    'session_token':{'type':'text', 'length':50, 'validation_method': None, 'is_optional': False},

    'd_id': {'type': 'int', 'length': 500, 'validation_method': None, 'is_optional': False},
    'd_name': {'type': 'string', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},
    'is_active': {'type': 'bool', 'length': None, 'validation_method': None, 'is_optional': False},

    'c_id': {'type': 'int', 'length': 500, 'validation_method': None, 'is_optional': False},
    'c_name': {'type': 'string', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},

    'form_id': {'type': 'int', 'length': 100, 'validation_method': None, 'is_optional': False},
    'form_name': {'type': 'string', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},
    'form_url': {'type': 'string', 'length': 250, 'validation_method': is_url, 'is_optional': False},
    'parent_menu': {'type': 'string', 'length': 50, 'validation_method': is_alphabet, 'is_optional': True},
    'form_type': {'type': 'string', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},

    'user_group_id': {'type': 'int', 'length': 1000, 'validation_method': None, 'is_optional': False},
    'user_group_name': {'type': 'string', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},

    'l_id': {'type': 'int', 'length': 10000, 'validation_method': None, 'is_optional': True},
    'l_position' : {'type': 'int', 'length': 10, 'validation_method': None, 'is_optional': False},
    'l_name': {'type': 'string', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},

    'geography_id': {'type': 'int', 'length': 100000, 'validation_method': None, 'is_optional': False},
    'geography_name': {'type': 'string', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},
    'parent_ids': {'type': 'vector_type_int', 'length': 100000, 'validation_method': None, 'is_optional': False},
    'mapping': {'type': 'vector_type_string', 'length': 1000, 'validation_method': is_mapping, 'is_optional': False},

    'industry_id': {'type': 'int', 'length': 10000, 'validation_method': None, 'is_optional': False},
    'industry_name': {'type': 'string', 'length': 50, 'validation_method': is_industry, 'is_optional': False},

    'statutory_nature_id': {'type': 'int', 'length': 500, 'validation_method': None, 'is_optional': False},
    'statutory_nature_name': {'type': 'string', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},

    'statutory_id': {'type': 'int', 'length': 100000, 'validation_method': None, 'is_optional': False},
    'statutory_name': {'type': 'string', 'length': 100, 'validation_method': is_alphabet, 'is_optional': False},

    'file_size': {'type': 'int', 'length': 52949672950, 'validation_method': None, 'is_optional': False},
    'file_name': {'type': 'text', 'length': None, 'validation_method': None, 'is_optional': False},
    'file_content': {'type': 'text', 'length': None, 'validation_method': None, 'is_optional': True},

    'validity_days_id': {'type': 'int', 'length': 10000, 'validation_method': None, 'is_optional': True},
    'validity_days': {'type': 'int', 'length': 365, 'validation_method': None, 'is_optional': True},

    'group_id': {'type': 'int', 'length': 10000, 'validation_method': None, 'is_optional': False},
    'group_name': {'type': 'string', 'length': 50, 'validation_method': None, 'is_optional': False},
    'country_names': {'type': 'string', 'length': 10000, 'validation_method': None, 'is_optional': False},
    'no_of_legal_entities': {'type': 'int', 'length': None, 'validation_method': None, 'is_optional': False},
    'username': {'type': 'string', 'length': 100, 'validation_method': None, 'is_optional': False},
    'legal_entity_name': {'type': 'string', 'length': 50, 'validation_method': None, 'is_optional': False},
    'no_of_licence': {'type': 'int', 'length': 10000, 'validation_method': None, 'is_optional': False},
    'file_space': {'type': 'int', 'length': 100000000, 'validation_method': None, 'is_optional': False},
    'is_sms_subscribed': {'type': 'bool', 'length': None, 'validation_method': None, 'is_optional': False},
    'contract_from': {'type': 'string', 'length': 11, 'validation_method': None, 'is_optional': False},
    'contract_to': {'type': 'string', 'length': 11, 'validation_method': None, 'is_optional': False},
    
    'unit_approval_list': {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'clientcoordinationmaster', "class_name":"UnitApproval"},
}

api_params['domain_id'] = api_params.get('d_id')
api_params['domain_name'] = api_params.get('d_name')
api_params['country_id'] = api_params.get('c_id')
api_params['country_name'] = api_params.get('c_name')
api_params['level_id'] = api_params.get('l_id')
api_params['level_position'] = api_params.get('l_position')
api_params['level_name'] = api_params.get('l_name')
api_params['username'] = api_params.get('u_name')
api_params['group_name'] = api_params.get('g_name')
api_params['legal_entity_name'] = api_params.get('l_e_name')
api_params['parent_id'] = api_params.get('geography_id')
api_params['parent_mappings'] = api_params.get('mapping')
api_params['level_1_statutory_id'] = api_params.get('statutory_id')
api_params['level_1_statutory_name'] = api_params.get('statutory_name')
api_params['no_of_licence'] = api_params.get('n_o_l')
api_params['file_space'] = api_params.get('f_s')
api_params['is_sms_subscribed'] = api_params.get('sms')
api_params['contract_from'] = api_params.get('c_f')
api_params['contract_to'] = api_params.get('c_t')
