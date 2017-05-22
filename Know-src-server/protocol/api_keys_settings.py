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
    'user_client_id': {'type': 'INT', 'length': None, 'validation_methods': None, 'is_optional': True},
    'captcha_text': {'type': 'STRING', 'length': CAPTCHA_LENGTH, 'validation_method': is_alpha_numeric, 'is_optional': True},

    'd_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'd_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet_withdot, 'is_optional': False},
    'is_active': {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': False},
    'is_approved': {'type': 'INT', 'length': 5, 'validation_method': None, 'is_optional': False},
    'is_admin': {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': False},
    'is_delete': {'type': 'INT', 'length': 5, 'validation_method': None, 'is_optional': False},

    'csv': {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': False},
    'from_count': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'total_count': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},

    'c_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'c_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet_withdot, 'is_optional': False},
    'c_ids': {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': False},

    'form_id': {'type': 'INT', 'length': 100, 'validation_method': None, 'is_optional': False},

    'form_name': {'type': 'STRING', 'length': 50, 'validation_method': allow_specialchar, 'is_optional': False},
    'form_url': {'type': 'TEXT', 'length': 250, 'validation_method': is_url, 'is_optional': False},
    'parent_menu': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': True},
    'form_type': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},

    'user_group_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'user_group_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},

    'l_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'l_position': {'type': 'INT', 'length': 10, 'validation_method': None, 'is_optional': False},
    'l_name': {'type': 'STRING', 'length': 50, 'validation_method': is_address, 'is_optional': True},

    'geography_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'geography_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet_withdot, 'is_optional': False},
    'parent_ids': {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'mapping': {'type': 'VECTOR_TYPE_STRING', 'length': 1000, 'validation_method': is_mapping, 'is_optional': False},
    'statutory_map': {'type': 'TEXT', 'length': 1000, 'validation_method': is_mapping, 'is_optional': False},
    'geography': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': False},

    'industry_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'industry_name': {'type': 'STRING', 'length': 50, 'validation_method': is_industry, 'is_optional': False},
    'industry_id_optional': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},

    'organization_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'organization_name': {'type': 'STRING', 'length': 50, 'validation_method': is_industry, 'is_optional': False},

    'statutory_nature_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'statutory_nature_name': {'type': 'STRING', 'length': 50, 'validation_method': is_address, 'is_optional': False},

    'statutory_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'statutory_name': {'type': 'STRING', 'length': 100, 'validation_method': is_alpha_numeric, 'is_optional': False},
    "document_name": {'type': 'TEXT', 'length': 500, 'validation_method': None, 'is_optional': False},
    'compliance_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'compliance_name': {'type': 'TEXT', 'length': 500, 'validation_method': None, 'is_optional': False},
    'url': {'type': 'TEXT', 'length': 500, 'validation_method': None, 'is_optional': True},

    "m_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'comp_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'comp_name': {'type': 'STRING', 'length': 500, 'validation_method': allow_specialchar, 'is_optional': False},

    's_provision': {'type': 'STRING', 'length': 500, 'validation_method': allow_specialchar, 'is_optional': False},
    's_pro_map': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': False},
    'reference': {'type': 'TEXT', 'length': 500, 'validation_method': None, 'is_optional': True},
    'refer': {'type': 'TEXT', 'length': 500, 'validation_method': None, 'is_optional': True},
    'locat': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': True},
    'comp_task': {'type': 'STRING', 'length': 100, 'validation_method': allow_specialchar, 'is_optional': False},
    'c_task': {'type': 'STRING', 'length': 200, 'validation_method': allow_specialchar, 'is_optional': False},
    'description': {'type': 'TEXT', 'length': 500, 'validation_method': allow_specialchar, 'is_optional': False},
    'descrip': {'type': 'TEXT', 'length': 500, 'validation_method': allow_specialchar, 'is_optional': False},
    'doc_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'f_f_list': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'core', 'class_name': 'FileList'},
    'p_consequences': {'type': 'STRING', 'length': 500, 'validation_method': allow_specialchar, 'is_optional': True},
    'p_cons': {'type': 'STRING', 'length': 500, 'validation_method': allow_specialchar, 'is_optional': True},
    'f_id': {'type': 'INT', 'length': 10, 'validation_method': None, 'is_optional': False},
    'frequency_id': {'type': 'INT', 'length': 10, 'validation_method': None, 'is_optional': True},
    'statu_dates': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'core', 'class_name': 'StatutoryDate'},
    'statutory_month': {'type': 'INT', 'length': 12, 'validation_method': None, 'is_optional': True},
    'statutory_date': {'type': 'INT', 'length': 31, 'validation_method': None, 'is_optional': True},
    'trigger_before_days': {'type': 'INT', 'length': 100, 'validation_method': None, 'is_optional': True},
    'repeat_by': {'type': 'INT', 'length': 2, 'validation_method': None, 'is_optional': True},
    'r_type_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'r_every': {'type': 'INT', 'length': 100, 'validation_method': None, 'is_optional': True},
    'd_type_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'duration': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'duration_type_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'duration_type': {'type': 'TEXT', 'length': 10, 'validation_method': None, 'is_optional': True},
    'repeat_type_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'repeat_type': {'type': 'TEXT', 'length': 10, 'validation_method': None, 'is_optional': True},
    'frequency': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},
    'freq': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},
    'summary': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': True},
    's_m_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'a_status': {'type': 'INT', 'length': 5, 'validation_method': None, 'is_optional': True},
    'comp_status': {'type': 'INT', 'length': 5, 'validation_method': None, 'is_optional': True},
    'r_reason': {'type': 'STRING', 'length': 500, 'validation_method': is_alpha_numeric, 'is_optional': True},
    's_pro': {'type': 'STRING', 'length': 500, 'validation_method': allow_specialchar, 'is_optional': False},
    'n_text': {'type': 'STRING', 'length': 500, 'validation_method': is_alpha_numeric, 'is_optional': True},
    's_mappings': {'type': 'VECTOR_TYPE', 'module_name': 'knowledgetransaction', 'class_name': 'ApproveMapping'},
    'tr_type': {'type': 'INT', 'length': 2, 'validation_method': None, 'is_optional': False},
    'c_by': {'type': 'TEXT', 'length': 10000, 'validation_method': None, 'is_optional': False},
    'c_on': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': False},
    'u_by': {'type': 'TEXT', 'length': 10000, 'validation_method': None, 'is_optional': True},
    'u_on': {'type': 'TEXT', 'length': 10000, 'validation_method': None, 'is_optional': True},
    'map_text': {'type': 'TEXT', 'length': 10000, 'validation_method': None, 'is_optional': True},
    'statutory_mapping_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},

    'compliance_frequency': {'type': 'VECTOR_TYPE', 'module_name': 'generalprotocol', 'class_name': 'ComplianceFrequency'},
    'compliance_repeat_type': {'type': 'VECTOR_TYPE', 'module_name': 'generalprotocol', 'class_name': 'ComplianceRepeatType'},
    'compliance_approval_status': {'type': 'VECTOR_TYPE', 'module_name': 'generalprotocol', 'class_name': 'StatutoryApprovalStatus'},
    'compliance_duration_type': {'type': 'VECTOR_TYPE', 'module_name': 'generalprotocol', 'class_name': 'ComplianceDurationType'},
    'statu_mappings': {'type': 'VECTOR_TYPE', 'length': 100000, 'validation_method': None, 'module_name': 'core', 'class_name': 'StatutoryMapping'},
    'r_count': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "industry_ids": {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "industry_names": {'type': 'VECTOR_TYPE_STRING', 'length': 100000, 'validation_method': is_alpha_numeric, 'is_optional': False},
    "i_names": {'type': 'VECTOR_TYPE_STRING', 'length': 100000, 'validation_method': is_alpha_numeric, 'is_optional': False},
    "statutory_ids": {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "s_maps": {'type': 'VECTOR_TYPE_STRING', 'length': 1000, 'validation_method': is_alpha_numeric, 'is_optional': False},
    "compliances": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', 'class_name': 'Compliance'},
    "compliance_names": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', 'class_name': 'Compliance_Download'},
    "geography_ids": {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "geo_maps": {'type': 'VECTOR_TYPE_STRING', 'length': 1000, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'comp_approval_status': {'type': 'TEXT', 'length': 50, 'validation_method': None, 'is_optional': False},
    'approval_status_id': {'type': 'INT', 'length': 7, 'validation_method': None, 'is_optional': False},
    'active_status_id': {'type': 'INT', 'length': 7, 'validation_method': None, 'is_optional': False},
    'a_s_id': {'type': 'INT', 'length': 7, 'validation_method': None, 'is_optional': False},
    'approval_status_text': {'type': 'TEXT', 'length': 100, 'validation_method': allow_specialchar, 'is_optional': False},
    'a_s_t': {'type': 'TEXT', 'length': 100, 'validation_method': allow_specialchar, 'is_optional': False},

    'levels': {'type': 'VECTOR_TYPE', 'module_name': 'knowledgemaster', 'class_name': 'Level'},
    "geography_levels": {'type': 'MAP_TYPE', 'validation_method': is_numeric, 'module_name': 'core', "class_name": "GeographyLevel"},
    "geographies": {'type': 'MAP_TYPE', 'validation_method': is_numeric, 'module_name': 'core', "class_name": "Geography"},
    "geography_report": {'type': 'VECTOR_TYPE', 'validation_method': None, 'module_name': 'knowledgereport', "class_name": "GeographyMapping"},
    "geography_mapping": {'type': 'TEXT', 'length': 10000, 'validation_method': None, 'is_optional': False},
    "statutory_natures": {'type': 'VECTOR_TYPE', 'validation_method': None, 'module_name': 'core', "class_name": "StatutoryNature"},
    "statutory_levels": {'type': 'MAP_TYPE', 'validation_method': is_numeric, 'module_name': 'core', "class_name": "Level"},
    "statutories": {'type': 'MAP_TYPE', 'validation_method': is_numeric, 'module_name': 'core', 'class_name': 'Statutory'},

    'file_size': {'type': 'INT', 'length': 52949672950, 'validation_method': None, 'is_optional': True},
    'file_name': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': True},
    'file_content': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': True},

    'validity_days_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'validity_days': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "validity_date_settings": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "ValidityDates"},
    "country_domain_mappings": {},

    'group_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'client_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'group_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'grp_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'ct_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'ct_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},

    'country_names': {'type': 'TEXT', 'length': 10000, 'validation_method': None, 'is_optional': False},
    'next_unit_code': {'type': 'INT', 'length': None, 'validation_method': None, "is_optional": False},

    "domain_details": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'generalprotocol', "class_name": "EntityDomainDetails"},
    "business_group": {'type': 'RECORD_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'core', "class_name": "ClientBusinessGroup"},
    "logo": {'type': 'RECORD_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'core', "class_name": "FileList"},
    "new_logo": {'type': 'RECORD_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'core', "class_name": "FileList"},
    'old_logo': {'type': 'TEXT', 'length': 500, 'validation_method': None, 'is_optional': True},
    'no_of_legal_entities': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "activation_date": {'type': 'TEXT', 'length': 10, 'validation_method': None, 'is_optional': True},
    'no_of_assigned_legal_entities': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'user_ids': {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'legal_entity_ids': {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': False},

    'email_id': {'type': 'TEXT', 'length': 100, 'validation_method': None, 'is_optional': True},
    'business_group_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'b_grp_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'business_group_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'b_grp_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'legal_entity_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'legal_entity_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'l_e_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'no_of_licence': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'no_of_view_licence': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'file_space': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'is_sms_subscribed': {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': False},
    'contract_from': {'type': 'TEXT', 'length': 11, 'validation_method': None, 'is_optional': False},
    'contract_from_optional': {'type': 'TEXT', 'length': 11, 'validation_method': None, 'is_optional': True},
    'contract_to': {'type': 'TEXT', 'length': 11, 'validation_method': None, 'is_optional': False},
    'contract_to_optional': {'type': 'TEXT', 'length': 11, 'validation_method': None, 'is_optional': True},
    "legal_entity_details": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "LegalEntityDetails"},
    "date_configurations": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "ClientConfiguration"},
    "org": {},
    "month_from": {'type': 'INT', 'length': 12, 'validation_method': None, 'is_optional': True},
    "month_to": {'type': 'INT', 'length': 12, 'validation_method': None, 'is_optional': True},
    "notification_type": {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},
    "org_info": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'clientcoordinationmaster', "class_name": "LegalEntityOrganisation"},

    'unit_approval_list': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'clientcoordinationmaster', "class_name": "UnitApproval"},
    'unit_list': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "UnitDetails"},
    'client_unit_list': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "UnitList"},
    'unit_count': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'division_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'div_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'category_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'cat_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'unit_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'u_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'unit_code': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'u_code': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'unit_name': {'type': 'TEXT', 'length': 50, 'validation_metunithod': is_alpha_numeric, 'is_optional': False},
    'u_name': {'type': 'TEXT', 'length': 160, 'validation_metunithod': is_alpha_numeric, 'is_optional': False},
    'address': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': True},
    'postal_code': {'type': 'INT', 'length': None, 'validation_method': is_numeric, 'is_optional': False},
    'domain_names': {'type': 'VECTOR_TYPE_STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'org_names': {'type': 'VECTOR_TYPE_STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'org_names_list': {},
    'entity_unit_approval_list': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'clientcoordinationmaster', "class_name": "EntityUnitApproval"},
    "unit_approval_details": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'clientcoordinationmaster', "class_name": "UnitApprovalDetails"},
    'reason': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': True},
    'd_reason': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': True},
    'approval_status': {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': False},
    'message': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': False},
    'extra_details': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': True},

    "group_approval_list": {'type': 'VECTOR_TYPE', 'length': None, 'validaCategorytion_method': None, 'is_optional': False, 'module_name': 'clientcoordinationmaster', "class_name": "ClientGroupApproval"},
    "countries": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "Country"},
    "domains": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "Domain"},
    "dms": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'domaintransactionprotocol', "class_name": "LegalentityDomains"},
    "industries": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "Industry"},

    "industry_name_id": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "Industries"},
    "groups": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "ClientGroup"},
    "re_assign_groups": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "ReassignClientGroup"},

    "clients": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "Client"},
    "grps": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "Client"},

    "unit_legal_entity": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'core', "class_name": "UnitLegalEntity"},
    "lety": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'core', "class_name": "AssignUnitLegalEntity"},

    "admin_legal_entity": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'admin', "class_name": "LegalEntity"},
    "group_company_list": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "GroupCompanyForUnitCreation"},
    "business_group_list": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'core', "class_name": "BusinessGroup"},
    "divisions": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'core', "class_name": "Division"},
    "divs": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'core', "class_name": "Division"},

    "user_categories": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'core', "class_name": "UserCategory"},

    "assign_le_list": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'generalprotocol', "class_name": "AssignLegalEntity"},
    "unassign_legal_entities": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'generalprotocol', "class_name": "UnAssignLegalEntity"},
    "view_assigned_legal_entities": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'generalprotocol', "class_name": "AssignedLegalEntity"},

    'le_count': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "country_ids": {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "client_group_approval_details": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'clientcoordinationmaster', "class_name": "ClientGroupApprovalDetails"},
    "client_domains": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "Domain"},

    "notifications": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'generalprotocol', "class_name": "Notification"},
    "audit_trail_details": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'generalprotocol', "class_name": "AuditTrail"},
    "audit_trail_countries": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'generalprotocol', "class_name": "AuditTrailCountries"},
    "form_categories":  {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'generalprotocol', "class_name": "FormCategory"},
    "user_group_details":  {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "UserGroup"},
    'no_of_users': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "forms":  {'type': 'MAP_TYPE', 'length': None, 'validation_method': is_numeric, 'is_optional': False, 'module_name': 'generalprotocol', "class_name": "Menu"},

    "menus":  {'type': 'MAP_TYPE_VECTOR_TYPE', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False, 'module_name': 'generalprotocol', "class_name": "Form"},
    "menu": {'type': 'RECORD_TYPE', 'length': None, 'validation_method': None, 'module_name': 'generalprotocol', 'class_name': 'Menu'},

    'user_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "username_id": {'type': 'TEXT', 'length': 100, 'validation_method': None, 'is_optional': True},
    "employee_name": {'type': 'TEXT', 'length': 50, 'validation_method': None, 'is_optional': False},
    "employee_code": {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    "contact_no": {'type': 'TEXT', 'length': 12, 'validation_method': None, 'is_optional': True},
    "mobile_no": {'type': 'TEXT', 'length': 12, 'validation_method': None, 'is_optional': False},
    "designation": {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    "domain_ids": {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "user_groups": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "UserGroup"},
    "user_details": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "UserDetails"},
    "industries_list": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "Industries"},
    "unit_geographies_list": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "UnitGeographyMapping"},
    "unit_geography_level_list": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "UnitGeographyLevel"},
    "unit_industries_list": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "UnitIndustries"},
    "d_ids": {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "i_ids": {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'i_ids_list': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'core', 'class_name': 'DomainIndustryList'},
    "cg": {'type': 'TEXT', 'length': 200, 'validation_method': None, 'is_optional': True},
    "cl_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "d": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technomasters', "class_name": "DIVISION"},
    "le": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technomasters', "class_name": "LEGAL_ENTITY"},
    "units": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technomasters', "class_name": "UNIT"},
    "unit_id_name": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'core', "class_name": "Unit"},
    "categories": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "Category"},
    "cates": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "Category"},

    "ug_name": {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    "user_group_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "ug_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "form_ids": {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "f_ids": {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "form_category_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "fc_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "form_category": {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    "user_category_id": {'type': 'INT', 'length': 10, 'validation_method': None, 'is_optional': False},
    "user_category_name": {'type': 'STRING', 'length': 100, 'validation_method': is_alphabet, 'is_optional': False},

    "le_db_server_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "db_server_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "db_server_name": {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    "client_db_server_id": {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': True},
    "client_db_server_name": {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    "database_server_ip": {'type': 'TEXT', 'length': 50, 'validation_method': None, 'is_optional': True},
    "port": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "db_servers": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "DBServer"},
    "no_of_clients": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},

    "client_server_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "client_server_name": {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    "client_servers": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "ClientServer"},

    "file_server_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "file_server_name": {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    "file_servers": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "FileServerList"},

    "old_grp_app_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "old_grp_db_s_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "old_le_db_s_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "old_le_f_s_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "new_cl_ids": {'type': 'TEXT', 'length': 50, 'validation_method': None, 'is_optional': True},
    "new_grp_le_ids": {'type': 'TEXT', 'length': 50, 'validation_method': None, 'is_optional': True},
    "new_le_le_ids": {'type': 'TEXT', 'length': 50, 'validation_method': None, 'is_optional': True},
    "new_le_f_s_ids": {'type': 'TEXT', 'length': 50, 'validation_method': None, 'is_optional': True},

    "client_dbs": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "ClientDatabase"},
    "client_groups": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "ClientGroup"},
    "client_legal_entities": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "LegalEntity"},
    "allocate_db_list": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'consoleadmin', "class_name": "AllocateDBList"},
    "business_groups_country": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "ClientBusinessGroupCountry"},
    "legal_entities": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "LegalEntity"},
    "business_groups": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "BusinessGroup"},
    "bgrps": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "BusinessGroup"},
    "client_server_name_and_id": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "ClientServerNameAndID"},
    "db_server_name_and_id": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "DBServerNameAndID"},
    "file_server_list": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "AllocateFileServerList"},
    "machine_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "machine_name": {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    "client_database_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},

    "file_storages": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "FileStorage"},

    "auto_deletion_entities": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "EntitiesWithAutoDeletion"},
    "auto_deletion_units": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "Unit"},
    "deletion_period": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "deletion_year": {'type': 'INT', 'length': 100, 'validation_method': None, 'is_optional': True},
    "auto_deletion_details": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "AutoDeletionDetail"},

    "knowledge_managers": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "User"},
    "knowledge_users": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "User"},
    "techno_managers": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "User"},
    "techno_users": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "User"},
    "domain_managers": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "User"},
    "domain_users": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "User"},
    "user_mappings": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "UserMapping"},
    "cc_manager_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "user_mapping_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},

    "t_m_reassign": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "UserInfo"},
    "t_e_reassign": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "UserInfo"},
    "d_m_reassign": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "UserInfo"},
    "d_e_reassign": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "UserInfo"},
    "country_domains": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "CountryWiseDomain"},
    "country_domains_parent": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "CountryWiseDomainParent"},
    "t_user_info": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "TechnoEntity"},
    "d_user_info": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "DomainUnit"},

    "techno_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "location": {'type': 'TEXT', 'length': 500, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'd_u_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'gt_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},

    'reassign_from': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'reassign_to': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    't_e_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'executive_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'old_t_e_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'd_e_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},

    't_manager_info': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "ReassignTechnoManager"},
    't_executive_info': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "ReassignTechnoExecutive"},
    'd_manager_info': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "ReassignDomainManager"},
    'd_executive_info': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "ReassignDomainExecutive"},

    "user_mapping_users": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "UserMappingUsers"},
    "child_users": {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "parent_user_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "child_user_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "remarks": {'type': 'TEXT', 'length': 500, 'is_optional': True},
    "p_user_ids": {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "new_child_users": {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "new_child_user_names": {'type': 'VECTOR_TYPE_STRING', 'length': 100000, 'validation_method': is_alpha_numeric, 'is_optional': True},

    'bg_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'bg_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'dv_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'le_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'le_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    "statu_units": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'domaintransactionprotocol', "class_name": "StatutoryUnits"},

    'le_ids': {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'grp_ids': {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'entity_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},

    "unassigned_units": {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': True},
    "unassigned_units_list": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technomasters', "class_name": "UnassignedUnit"},
    "assigned_units_list": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technomasters', "class_name": "AssignedUnit"},
    "assigned_unit_details_list": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technomasters', "class_name": "AssignedUnitDetails"},
    "domain_manager_users": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "User"},
    "mapped_domain_users": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "DomainUser"},
    "active_units": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technomasters', "class_name": "ActiveUnit"},
    'division_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'dv_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'div_cnt': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'unit_cnt': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "division_units": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technomasters', "class_name": "UnitDivision"},
    "division_category": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'technomasters', "class_name": "DivisionCategory"},
    "countries_units": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "UnitCountries"},
    "user_group_name": {'type': 'string', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},

    "user_type": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "old_user_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "new_user_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "assigned_ids": {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': False},

    "assigned_legal_entities": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "AssignedLegalEntities"},
    "assigned_units": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "AssignedUnits"},
    "assigned_clients": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "AssignedClient"},
    "client_agreement_list": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technoreports', "class_name": "ClientAgreementList"},
    'group_admin_email': {'type': 'TEXT', 'length': 100, 'validation_method': None, 'is_optional': False},
    "total_licence": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "used_licence": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'used_file_space': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "domain_count": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "domain_total_unit": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "domain_used_unit": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'legal_entity_admin_email': {'type': 'TEXT', 'length': 100, 'validation_method': None, 'is_optional': True},
    "legal_entity_admin_contactno": {'type': 'TEXT', 'length': 12, 'validation_method': None, 'is_optional': True},
    'link': {'type': 'TEXT', 'length': 500, 'validation_method': None, 'is_optional': True},
    "domainwise_agreement_list": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technoreports', "class_name": "DomainwiseAgreementList"},
    "organizationwise_unit_count_list": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technoreports', "class_name": "OrganizationwiseUnitCountList"},
    "client_group_master" : {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "ClientGroupMaster"},
    "level_1_statutories_list": {'type': 'VECTOR_TYPE_STRING', 'length': 100000, 'validation_method': is_alpha_numeric, 'is_optional': False},
    "statutories_for_assigning": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'domaintransactionprotocol', "class_name": "AssignStatutoryCompliance"},
    "statutories_for_multiple": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'domaintransactionprotocol', "class_name": "AssignStatutoryComplianceMultiple"},
    "category_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "cat_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "domain_id_optional": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "unit_ids": {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "comp_ids": {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "organizations": {'type': 'VECTOR_TYPE_STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    "level_1_statutory_index": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "statutory_provision": {'type': 'TEXT', 'length': 500, 'validation_method': None, 'is_optional': False},
    "locations": {'type': 'VECTOR_TYPE_STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    "compliances_applicablity_status": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'domaintransactionprotocol', "class_name": "SaveComplianceStatus"},
    "level_1_statutory_wise_compliances": {},
    "assigned_statutories": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'domaintransactionprotocol', "class_name": "AssignedStatutories"},
    "assigned_statutories_approve": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'domaintransactionprotocol', "class_name": "AssignedStatutoriesApprove"},
    "unit_code_with_name": {'type': 'TEXT', 'length': 150, 'validation_method': None, 'is_optional': False},
    "submission_status": {'type': 'INT', 'length': 4, 'validation_method': None, 'is_optional': True},
    "s_s": {'type': 'INT', 'length': 5, 'validation_method': None, 'is_optional': True},
    "client_statutory_id": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "submission_type": {'type': 'TEXT', 'length': 10, 'validation_method': None, 'is_optional': False},
    "compliance_applicability_status": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "statutory_applicability_status": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "statutory_opted_status": {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'notification_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'notification_text': {'type': 'TEXT', 'length': 500, 'validation_method': None, 'is_optional': False},
    'action': {'type': 'TEXT', 'length': 500, 'validation_method': None, 'is_optional': False},
    'has_read': {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': False},
    "from_date": {'type': 'TEXT', 'length': 20, 'validation_method': None, 'is_optional': True},
    "to_date": {'type': 'TEXT', 'length': 20, 'validation_method': None, 'is_optional': True},
    "date_and_time": {'type': 'STRING', 'length': 20, 'validation_method': is_alpha_numeric, 'is_optional': False},
    "date": {'type': 'TEXT', 'length': 20, 'validation_method': None, 'is_optional': True},
    'record_count': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'page_count': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'total_records': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'job_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "audit_trails": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'generalprotocol', "class_name": "AuditTrail"},
    "users": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "User"},
    "forms_list": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'generalprotocol', "class_name": "AuditTrailForm"},
    'user_id_search': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'form_id_search': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "file_list": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "FileList"},

    "usermapping_groupdetails": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "UserMappingGroupDetails"},
    "usermapping_unit": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "UserMappingUnitDetails"},
    "usermapping_legal_entities": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "ClientLegalEntity"},
    "usermapping_business_groups": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "ClientBusinessGroup"},
    'client_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'unit_code_name': {'type': 'TEXT', 'length': 10000, 'validation_method': None, 'is_optional': True},
    'techno_manager': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'techno_user': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    "techno_details": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "UserMappingReportTechno"},
    "unit_domains": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "UserMappingReportDomain"},
    "domains_organization_list": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "UnitDomainOrganisation"},

    "country_info": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'knowledgetransaction', "class_name": "CountryInfo"},
    "domain_info": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'knowledgetransaction', "class_name": "DomainInfo"},
    "organisation_info": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'knowledgetransaction', "class_name": "OrganisationInfo"},
    "nature_info": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'knowledgetransaction', "class_name": "StatutoryNatureInfo"},
    "statutory_info": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'knowledgetransaction', "class_name": "StatutoryInfo"},
    "geography_info": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'knowledgetransaction', "class_name": "GeographyInfo"},
    "geography_level_info": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "UnitGeographyLevel"},

    "mapped_comps": {'type': 'VECTOR_TYPE', 'is_optional': False, 'module_name': 'core', "class_name": "MappedCompliance"},
    "s_pids": {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "s_pnames": {'type': 'VECTOR_TYPE_SRTING', 'length': 100, 'validation_method': is_alpha_numeric, 'is_optional': True},

    "statutory_groups": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technoreports', "class_name": "ClientGroup"},
    "statutory_units": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technoreports', "class_name": "ComplianceUnits"},
    "statutory_business_groups": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technoreports', "class_name": "ClientBusinessGroup"},
    "statutory_compliances": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technoreports', "class_name": "ComplianceStatutory"},
    "compfie_admin": {'type': 'TEXT', 'length': 500, 'validation_method': None, 'is_optional': True},
    "client_admin": {'type': 'TEXT', 'length': 500, 'validation_method': None, 'is_optional': True},
    "admin_update": {'type': 'TEXT', 'length': 500, 'validation_method': None, 'is_optional': True},
    "client_update": {'type': 'TEXT', 'length': 500, 'validation_method': None, 'is_optional': True},
    "unit_groups": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technoreports', "class_name": "StatutorySettingUnitGroup"},
    "act_groups": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technoreports', "class_name": "StatutorySettingActGroup"},
    "compliance_statutories_list": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technoreports', "class_name": "StatutorySettingCompliances"},
    "level_one_statutories": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "Level1StatutoryList"},
    'compliance_task': {'type': 'STRING', 'length': 100, 'validation_method': is_alpha_numeric, 'is_optional': False},
    "statutory_notifictions_list": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technoreports', "class_name": "StatutoryNotificationList"},
    'statutory_id_optional': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'from_date_optional': {'type': 'TEXT', 'length': 11, 'validation_method': None, 'is_optional': True},
    'to_date_optional': {'type': 'TEXT', 'length': 11, 'validation_method': None, 'is_optional': True},
    'notification_date': {'type': 'TEXT', 'length': 11, 'validation_method': None, 'is_optional': False},
    "mapped_compliances": {'type': 'VECTOR_TYPE', 'is_optional': False, 'module_name': 'core', "class_name": "MappedCompliance"},

    "unit_creation_informed": {'type': 'INT', 'length': 3, 'validation_method': None, 'is_optional': True},
    "statutory_assigned_informed": {'type': 'INT', 'length': 3, 'validation_method': None, 'is_optional': True},
    "groupadmin_groupList": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'technotransactions', "class_name": "GroupAdmin_GroupList"},
    "groupadmin_unitList": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'technotransactions', "class_name": "GroupAdmin_UnitList"},
    "emp_code_name": {'type': 'TEXT', 'length': 200, 'validation_method': None, 'is_optional': True},
    'statutory_count': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'grp_mode': {'type': 'string', 'length': 50, 'validation_method': None, 'is_optional': False},
    "u_m_none": {'type': 'TEXT', 'length': 1000, 'validation_method': None, 'is_optional': True},
    "usermapping_domain": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technoreports', "class_name": "UserMappingDomain"},
    "country_wise_domain": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "CountryWiseDomain"},
    "units_report" : {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technoreports', "class_name": "ClientUnitDetailsReport"},
    "units_list" : {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technoreports', "class_name": "ClientUnitList"},
    "closed_on": {'type': 'TEXT', 'length': 200, 'validation_method': None, 'is_optional': True},
    "check_date": {'type': 'TEXT', 'length': 200, 'validation_method': None, 'is_optional': True},
    "created_on": {'type': 'TEXT', 'length': 200, 'validation_method': None, 'is_optional': True},
    "unit_email_date": {'type': 'TEXT', 'length': 15, 'validation_method': None, 'is_optional': True},
    "statutory_email_date": {'type': 'TEXT', 'length': 15, 'validation_method': None, 'is_optional': True},
    "registration_email_date": {'type': 'TEXT', 'length': 15, 'validation_method': None, 'is_optional': True},
    "groupadmin_clients": {'type': 'VECTOR_TYPE', 'is_optional': False, 'module_name': 'technoreports', "class_name": "GroupAdminClientGroup"},
    "group_admin_countries": {'type': 'VECTOR_TYPE', 'is_optional': False, 'module_name': 'technoreports', "class_name": "GroupAdminCountry"},
    "group_admin_list": {'type': 'VECTOR_TYPE', 'is_optional': False, 'module_name': 'technoreports', "class_name": "GroupAdminClientGroupData"},
    "client_ids": {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "reassign_user_clients": {'type': 'VECTOR_TYPE', 'is_optional': True, 'module_name': 'technoreports', "class_name": "ReassignUserClients"},
    "reassign_user_list": {'type': 'VECTOR_TYPE', 'is_optional': True, 'module_name': 'technoreports', "class_name": "ReassignedUserList"},
    "reassign_domains": {'type': 'VECTOR_TYPE', 'is_optional': True, 'module_name': 'technoreports', "class_name": "ReassignUserDomainList"},
    "reassign_domains_list": {'type': 'VECTOR_TYPE', 'is_optional': True, 'module_name': 'technoreports', "class_name": "ReassignedDomainUserList"},
    'group_id_none': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "legalentity_closure": {'type': 'VECTOR_TYPE', 'is_optional': True, 'module_name': 'technotransactions', "class_name": "LegalEntityClosure"},
    "closed_remarks": {'type': 'TEXT', 'length': 500, 'validation_method': None, 'is_optional': True},
    "messages": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'generalprotocol', "class_name": "Message"},
    'message_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'message_heading': {'type': 'TEXT', 'length': 500, 'validation_method': None, 'is_optional': False},
    'message_text': {'type': 'TEXT', 'length': 500, 'validation_method': None, 'is_optional': False},
    "created_by": {'type': 'TEXT', 'length': 50, 'validation_method': None, 'is_optional': False},
    "statutory_notifications": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'generalprotocol', "class_name": "StatutoryNotification"},
    'notification_heading': {'type': 'TEXT', 'length': 500, 'validation_method': None, 'is_optional': False},
    "level_1_statutories": {'type': 'MAP_TYPE', 'length': None, 'validation_method': is_numeric, 'is_optional': False, 'module_name': 'core', "class_name": "Statutory"},

    "knowledgeusers": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'module_name': 'core', 'class_name': 'ChildUsers'},
    'a_i_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'a_s_n_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'a_c_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'a_d_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'a_u_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'map_list': {'type': 'VECTOR_TYPE', 'length': 100000, 'validation_method': None, 'module_name': 'mobile', 'class_name': 'MappingApproveInfo'},
    'comp_lists': {'type': 'VECTOR_TYPE', 'length': 100000, 'validation_method': None, 'module_name': 'mobile', 'class_name': 'MappingComplianceInfo'},
    'approv_mappings': {'type': 'VECTOR_TYPE', 'length': 100000, 'validation_method': None, 'module_name': 'knowledgetransaction', 'class_name': 'MappingApproveInfo'},
    'comp_list': {'type': 'VECTOR_TYPE', 'length': 100000, 'validation_method': None, 'module_name': 'knowledgetransaction', 'class_name': 'ComplianceList'},
    "typelistedit": {'type': 'TEXT', 'length': 50, 'validation_method': None, 'is_optional': True},
    'a_g_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    "approve_assigned_statutories": {'type': 'VECTOR_TYPE', 'length': 100000, 'validation_method': None, 'module_name': 'technoreports', 'class_name': 'ApproveAssignedStatutories'},
    "legal_entities_list": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "LegalEntityList"},
    'is_closed': {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': False},

    "ip_setting_forms": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "Form"},
    "ips_list": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "IPSettingsList"},
    "group_ips_list": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "GroupIPDetails"},

    'statutory_mappings': {'type': 'VECTOR_TYPE', 'length': 100000, 'validation_method': None, 'module_name': 'knowledgereport', 'class_name': 'StatutoryMappingReport'},
    'is_created': {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': False},
    "console_cl_ids": {'type': 'TEXT', 'length': 50, 'validation_method': None, 'is_optional': True},
    "console_le_ids": {'type': 'TEXT', 'length': 50, 'validation_method': None, 'is_optional': True},
    "console_le_le_ids": {'type': 'TEXT', 'length': 50, 'validation_method': None, 'is_optional': True},
    "console_f_le_ids": {'type': 'TEXT', 'length': 50, 'validation_method': None, 'is_optional': True},
    'ip_optional': {'type': 'TEXT', 'length': 100, 'validation_method': None, 'is_optional': True},
    'group_info': {'type': 'VECTOR_TYPE', 'length': 100000, 'validation_method': None, 'module_name': 'clientcoordinationmaster', 'class_name': 'GroupInfo'},
    'old_d_e_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    "mapped_country_domains": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "CountryWiseDomain"},
    "mapped_techno_users": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "MappedUser"},

    'complied_count': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'delayed_compliance_count': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'inprogress_compliance_count': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'not_complied_count': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'filter_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'ageing': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'service_provider_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'contact_person': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'statutory_nature': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    "applicable_units": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'domaintransactionprotocol', "class_name": "ApplicableUnit"},
    "audit_client_users": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "AuditTrailClientUser"},
    "client_audit_details": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'generalprotocol', "class_name": "AuditTrailForm"},
    "client_audit_units": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "AuditUnits"},
    "d_o_names": {'type': 'TEXT', 'length': 100, 'validation_method': None, 'is_optional': True},
    "le_expiry_days": {'type': 'TEXT', 'length': 100, 'validation_method': None, 'is_optional': True},
    "assign_count": {'type': 'VECTOR_TYPE_INT', 'length': 100000, 'validation_method': None, 'is_optional': True},
    "error": {'type': 'TEXT', 'length': 500, 'validation_method': None, 'is_optional': True},
    'is_register': {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': False},
    'm_count': {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    's_count': {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    'insertValText': {'type': 'TEXT', 'length': 500, 'validation_method': None, 'is_optional': True},
    "resend_email_date": {'type': 'TEXT', 'length': 15, 'validation_method': None, 'is_optional': True},
    'o_le_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'o_bg_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'o_contract_from': {'type': 'TEXT', 'length': 11, 'validation_method': None, 'is_optional': True},
    'o_contract_to': {'type': 'TEXT', 'length': 11, 'validation_method': None, 'is_optional': True},
    'o_file_space': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'o_no_of_licence': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'o_no_of_view_licence': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'o_group_admin_email_id': {'type': 'TEXT', 'length': 100, 'validation_method': None, 'is_optional': True},
    'o_count': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},

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
api_params['act_name'] = api_params.get('statutory_name')
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
api_params['d_names'] = api_params.get('mapping')
api_params["org_id"] = api_params.get("industry_id")
api_params["org_name"] = api_params.get("industry_name")
api_params["rcount"] = api_params.get("total_records")
api_params["count"] = api_params.get("total_records")
api_params["unit_total"] = api_params.get("total_records")
api_params["page_limit"] = api_params.get("total_records")
api_params["days_left"] = api_params.get("total_records")
api_params["allow_enable"] = api_params.get("is_active")
api_params["is_file_removed"] = api_params.get("is_active")
api_params["allow_domain_edit"] = api_params.get("is_active")
api_params['compliance_applicable_status'] = api_params.get('is_active')
api_params['assignee_name'] = api_params.get('employee_name')
api_params['statutory'] = api_params.get('employee_name')
api_params['opted_status'] = api_params.get('is_active')
api_params['compliance_opted_status'] = api_params.get('is_active')
api_params['user_level'] = api_params.get('l_position')
api_params['start_date'] = api_params.get('contract_from')
api_params['due_date'] = api_params.get('contract_from')
api_params['year'] = api_params.get('contract_from')
api_params['not_applicable_remarks'] = api_params.get('remarks')
api_params['compliance_remarks'] = api_params.get('contract_from')

api_params['compliance_description'] = api_params.get('description')
api_params['validity_date'] = api_params.get('contract_from')
api_params['next_due_date'] = api_params.get('contract_from')
api_params['seating_unit_id'] = api_params.get('unit_id')
api_params['service_provider_id'] = api_params.get('unit_id')
api_params['format_file_name'] = api_params.get('file_name')
api_params['file_names'] = api_params.get('file_name')
api_params['download_url'] = api_params.get('url')

api_params['is_new_data'] = api_params.get('is_active')
api_params['is_new_domain'] = api_params.get('is_active')
