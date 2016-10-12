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
    'session_token': {'type': 'text', 'length': 50, 'validation_method': None, 'is_optional': False},
    'login_type': {'type': ''},
    'username': {},
    'password': {},
    'short_name': {},
    'ip': {},

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

    'l_id': {'type': 'int', 'length': 10000, 'validation_method': None, 'is_optional': True},
    'l_position' : {'type': 'int', 'length': 10, 'validation_method': None, 'is_optional': False},
    'l_name': {'type': 'string', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},

    'geography_id': {'type': 'int', 'length': 100000, 'validation_method': None, 'is_optional': False},
    'geography_name': {'type': 'string', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},
    'parent_ids': {'type': 'vector_type_int', 'length': 100000, 'validation_method': None, 'is_optional': False},
    'mapping': {'type': 'string', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},

    'industry_id': {'type': 'int', 'length': 10000, 'validation_method': None, 'is_optional': False},
    'industry_name': {'type': 'string', 'length': 50, 'validation_method': is_industry, 'is_optional': False},

    'bg_id': {'type': 'int', 'length': 10000, 'validation_method': None, 'is_optional': True},
    'bg_name': {'type': 'string', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'dv_id': {'type': 'int', 'length': 10000, 'validation_method': None, 'is_optional': True},
    'le_id': {'type': 'int', 'length': 10000, 'validation_method': None, 'is_optional': False},

    'statutory_nature_id': {'type': 'int', 'length': 500, 'validation_method': None, 'is_optional': False},
    'statutory_nature_name': {'type': 'string', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},

    'statutory_id': {'type': 'int', 'length': 100000, 'validation_method': None, 'is_optional': False},
    'statutory_name': {'type': 'string', 'length': 100, 'validation_method': is_alphabet, 'is_optional': False},

    'file_size': {'type': 'int', 'length': 52949672950, 'validation_method': None, 'is_optional': False},
    'file_name': {'type': 'text', 'length': None, 'validation_method': None, 'is_optional': False},
    'file_content': {'type': 'text', 'length': None, 'validation_method': None, 'is_optional': True},

    'validity_days_id': {'type': 'int', 'length': 10000, 'validation_method': None, 'is_optional': True},
    'validity_days': {'type': 'int', 'length': 365, 'validation_method': None, 'is_optional': True},
    "validity_date_settings" : {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'core', "class_name":"ValidityDates"},

    'group_id': {'type': 'int', 'length': 10000, 'validation_method': None, 'is_optional': False},
    'client_id': {'type': 'int', 'length': 10000, 'validation_method': None, 'is_optional': False},
    'group_name': {'type': 'string', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'country_names': {'type': 'string', 'length': 10000, 'validation_method': None, 'is_optional': False},

    'no_of_legal_entities': {'type': 'int', 'length': None, 'validation_method': None, 'is_optional': False},
    'email_id': {'type': 'text', 'length': 100, 'validation_method': None, 'is_optional': False},
    'business_group_id': {'type': 'int', 'length': 10000, 'validation_method': None, 'is_optional': True},
    'business_group_name': {'type': 'string', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'legal_entity_id': {'type': 'int', 'length': 10000, 'validation_method': None, 'is_optional': False},
    'legal_entity_name': {'type': 'string', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'no_of_licence': {'type': 'int', 'length': 10000, 'validation_method': None, 'is_optional': False},
    'file_space': {'type': 'int', 'length': 100000000, 'validation_method': None, 'is_optional': False},
    'is_sms_subscribed': {'type': 'bool', 'length': None, 'validation_method': None, 'is_optional': False},
    'contract_from': {'type': 'string', 'length': 11, 'validation_method': None, 'is_optional': False},
    'contract_to': {'type': 'string', 'length': 11, 'validation_method': None, 'is_optional': False},

    'unit_approval_list': {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'clientcoordinationmaster', "class_name":"UnitApproval"},
    'unit_list': {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'core', "class_name":"Unit"},
    'unit_id': {'type': 'int', 'length': 100000, 'validation_method': None, 'is_optional': False},
    'unit_count': {'type': 'int', 'length': 100000, 'validation_method': None, 'is_optional': False},
    'division_name': {'type': 'string', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'category_name': {'type': 'string', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'unit_code': {'type': 'string', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'unit_name': {'type': 'string', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'address': {'type': 'text', 'length': None, 'validation_method': None, 'is_optional': True},
    'postal_code': {'type': 'int', 'length': 1000000, 'validation_method': is_numeric, 'is_optional': False},
    'domain_names': {'type': 'vector_type_string', 'length': 50, 'validation_method': None, 'is_optional': False},
    'org_names': {'type': 'vector_type_string', 'length': 50, 'validation_method': None, 'is_optional': False},
    'entity_unit_approval_list': {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'clientcoordinationmaster', "class_name":"EntityUnitApproval"},
    "unit_approval_details": {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'clientcoordinationmaster', "class_name":"UnitApprovalDetails"},
    'reason': {'type': 'text', 'length': None, 'validation_method': None, 'is_optional': False},
    'approval_status': {'type': 'bool', 'length': None, 'validation_method': None, 'is_optional': False},

    "group_approval_list" : {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'clientcoordinationmaster', "class_name":"ClientGroupApproval"},
    "countries" : {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'core', "class_name":"Country"},
    "domains" : {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'core', "class_name":"Domain"},
    "industries" : {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'core', "class_name":"Industry"},
    "unit_legal_entity" : {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name':'core', "class_name":"UnitLegalEntity"},
    "group_company_list" : {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'core', "class_name":"GroupCompanyForUnitCreation"},
    "business_group_list" : {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name':'core', "class_name":"BusinessGroup"},
    "divisions" : {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name':'core', "class_name":"Division"},
    'le_count': {'type': 'int', 'length': 100000, 'validation_method': None, 'is_optional': False},
    "country_ids": {'type': 'vector_type_int', 'length': 100000, 'validation_method': None, 'is_optional': False},
    "client_group_approval_details": {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'clientcoordinationmaster', "class_name":"ClientGroupApprovalDetails"},
    "client_domains": {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'core', "class_name":"Domain"},

    "notifications" : {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'general', "class_name":"Notification"},
    "audit_trail_details" : {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'general', "class_name":"AuditTrail"},
    "form_categories":  {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'core', "class_name":"FormCategory"},
    "user_group_details":  {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'admin', "class_name":"UserGroup"},
    'no_of_users': {'type': 'int', 'length': 10000, 'validation_method': None, 'is_optional': False},
    "forms":  {'type':'map_type', 'length': None, 'validation_method': is_numeric, 'is_optional': False, 'module_name':'core', "class_name":"Menu"},

    "employee_name": {'type': 'string', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},
    "employee_code": {'type': 'string', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    "contact_no": {'type': 'text', 'length': 12, 'validation_method': None, 'is_optional': True},
    "designation": {'type': 'string', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    "domain_ids": {'type': 'vector_type_int', 'length': 100000, 'validation_method': None, 'is_optional': False},
    "user_groups":  {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'core', "class_name":"UserGroup"},
    "user_details":{'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'core', "class_name":"UserDetails"},
    "industries_list" : {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'core', "class_name":"Industries"},
    "unit_geographies_list" : {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'core', "class_name":"UnitGeographyMapping"},
    "unit_geography_level_list" : {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'core', "class_name":"UnitGeographyLevel"},
    "unit_industries_list" : {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'core', "class_name":"UnitIndustries"},
    "d_ids": {'type': 'vector_type_int', 'length': 100000, 'validation_method': None, 'is_optional': False},
    "i_ids": {'type': 'vector_type_int', 'length': 100000, 'validation_method': None, 'is_optional': False},
    "cg": {'type': 'string', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},
    "cl_id": {'type': 'int', 'length': 500, 'validation_method': None, 'is_optional': False},
    "d": {'type': 'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'technomasters', "class_name":"DIVISION"},
    "business_group": {'type': 'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'technomasters', "class_name":"BUSINESS_GROUP"},
    "le": {'type': 'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'technomasters', "class_name":"LEGAL_ENTITY"},
    "units": {'type':'vector_type', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'technomasters', "class_name":"UNIT"},

    "user_group_name": {'type': 'string', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    "user_group_id" : {'type': 'int', 'length': 100000, 'validation_method': None, 'is_optional': False},
    "form_ids": {'type': 'vector_type_int', 'length': 100000, 'validation_method': None, 'is_optional': False},
    "form_category_id" : {'type': 'int', 'length': 100000, 'validation_method': None, 'is_optional': False},
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
