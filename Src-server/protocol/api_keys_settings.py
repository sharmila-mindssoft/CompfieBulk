'''
    #api_values_settings : This page will have all the values validation info like
    key_name : 'key_name' will be in string this key_name will be act as key in json. ex: 'country_name'

    @type: twhich define the format or type of value and this can be any one of value_formats from below list.
    @length: length of the value with corresponding type. this value is optional except string and INT type.
    @validation_method: this will be function name to validate value. this value is optional except string and INT type.
    @is_optional: is True when it allows None values.

### value_type = [STRING, TEXT, INT, BOOL, VECTOR_TYPE_STRING, VECTOR_TYPE_INT, VECTOR_TYPE, ENUM_TYPE]
### validation_method = [is_alphabet, is_alphanumeric, is_date, is_address ]
example
    {
        'country_name': STRING, 50, is_alphabet
    }
'''
from protocol.api_key_validation import *

__all__ = [
    'api_params'
]

api_params = {
    'session_token': {'type': 'TEXT', 'length': 50, 'validation_method': None, 'is_optional': False},
    'login_type': {'type': ''},
    'username': {},
    'password': {},
    'short_name': {},
    'ip': {},

    'd_id': {'type': 'INT', 'length': 500, 'validation_method': None, 'is_optional': False},
    'd_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},
    'is_active': {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': False},

    'c_id': {'type': 'INT', 'length': 500, 'validation_method': None, 'is_optional': False},
    'c_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},

    'form_id': {'type': 'INT', 'length': 100, 'validation_method': None, 'is_optional': False},
    'form_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},
    'form_url': {'type': 'STRING', 'length': 250, 'validation_method': is_url, 'is_optional': False},
    'parent_menu': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': True},
    'form_type': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},

    'user_group_id': {'type': 'INT', 'length': 1000, 'validation_method': None, 'is_optional': False},
    'user_group_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},

    'l_id': {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': True},
    'l_position' : {'type': 'INT', 'length': 10, 'validation_method': None, 'is_optional': False},
    'l_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},

    'geography_id': {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    'geography_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},
    'parent_ids': {'type': 'VECTOR_TYPE_INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    'mapping': {'type': 'VECTOR_TYPE_STRING', 'length': 1000, 'validation_method': is_mapping, 'is_optional': False},

    'industry_id': {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': False},
    'industry_name': {'type': 'STRING', 'length': 50, 'validation_method': is_industry, 'is_optional': False},

    'statutory_nature_id': {'type': 'INT', 'length': 500, 'validation_method': None, 'is_optional': False},
    'statutory_nature_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},

    'statutory_id': {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    'statutory_name': {'type': 'STRING', 'length': 100, 'validation_method': is_alphabet, 'is_optional': False},

    'file_size': {'type': 'INT', 'length': 52949672950, 'validation_method': None, 'is_optional': False},
    'file_name': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': False},
    'file_content': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': True},

    'validity_days_id': {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': True},
    'validity_days': {'type': 'INT', 'length': 365, 'validation_method': None, 'is_optional': True},

    'group_id': {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': False},
    'group_name': {'type': 'STRING', 'length': 50, 'validation_method': None, 'is_optional': False},
    'country_names': {'type': 'STRING', 'length': 10000, 'validation_method': None, 'is_optional': False},

    'no_of_legal_entities': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'username': {'type': 'TEXT', 'length': 100, 'validation_method': None, 'is_optional': False},
    'legal_entity_name': {'type': 'STRING', 'length': 50, 'validation_method': None, 'is_optional': False},
    'no_of_licence': {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': False},
    'file_space': {'type': 'INT', 'length': 100000000, 'validation_method': None, 'is_optional': False},
    'is_sms_subscribed': {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': False},
    'contract_from': {'type': 'STRING', 'length': 11, 'validation_method': None, 'is_optional': False},
    'contract_to': {'type': 'STRING', 'length': 11, 'validation_method': None, 'is_optional': False},

    'unit_approval_list': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'clientcoordinationmaster', "class_name": "UnitApproval"},
    'unit_id': {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    'division_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'category_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'unit_code': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'unit_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'address': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': False},
    'postal_code': {'type': 'INT', 'length': 1000000, 'validation_method': is_numeric, 'is_optional': False},
    'domain_names': {'type': 'VECTOR_TYPE_STRING', 'length': 50, 'validation_method': None, 'is_optional': False},
    'org_names': {'type': 'VECTOR_TYPE_STRING', 'length': 50, 'validation_method': None, 'is_optional': False},
    'entity_unit_approval_list': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'clientcoordinationmaster', "class_name": "EntityUnitApproval"},
}

api_params['domain_id'] = api_params.get('d_id')
api_params['domain_name'] = api_params.get('d_name')
api_params['country_id'] = api_params.get('c_id')
api_params['country_name'] = api_params.get('c_name')
api_params['level_id'] = api_params.get('l_id')
api_params['level_position'] = api_params.get('l_position')
api_params['level_name'] = api_params.get('l_name')
api_params['parent_id'] = api_params.get('geography_id')
api_params['parent_mappings'] = api_params.get('mapping')
api_params['level_1_statutory_id'] = api_params.get('statutory_id')
api_params['level_1_statutory_name'] = api_params.get('statutory_name')
