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

    'validity_days_id': {'type': 'int', 'length': 10000, 'validation_method':None, 'is_optional': True},
    'validity_days': {'type': 'int', 'length': 365, 'validation_method':None, 'is_optional': True}
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
