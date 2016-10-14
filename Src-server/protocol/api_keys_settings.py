'''
    #api_values_settings : This page will have all the values validation info like
    key_name : 'key_name' will be in STRING this key_name will be act as key in json. ex: 'country_name'

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

    'new_password' : {'type': 'TEXT', 'length': 20, 'validation_method': None, 'is_optional': False},
    'current_password' : {'type': 'TEXT', 'length': 20, 'validation_method': None, 'is_optional': False},

    'login_type': {'type': 'ENUM_TYPE', 'length': None,  'validation_method': None, 'module_name': 'core', 'class_name': 'SESSION_TYPE'},
    'username': {'type': 'TEXT', 'length': 100, 'validation_method': None, 'is_optional': False},
    'password': {'type': 'TEXT', 'length': 20, 'validation_method': None, 'is_optional': False},
    'short_name': {'type': 'TEXT', 'length': 100, 'validation_method': None, 'is_optional': True},
    'ip': {'type': 'TEXT', 'length': 100, 'validation_method': None, 'is_optional': False},
    'user_client_id': {'type': 'INT', 'length': 500, 'validation_methods': None, 'is_optional': True},
    'captcha_text': {'type': 'STRING', 'length': 10, 'validation_method': is_alpha_numeric, 'is_optional': True},

    'd_id': {'type': 'INT', 'length': 500, 'validation_method': None, 'is_optional': False},
    'd_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},
    'is_active': {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': False},
    'is_approved': {'type': 'INT', 'length': 3, 'validation_method': None, 'is_optional': False},
    'is_admin': {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': False},

    'c_id': {'type': 'INT', 'length': 500, 'validation_method': None, 'is_optional': False},
    'c_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},

    'form_id': {'type': 'INT', 'length': 100, 'validation_method': None, 'is_optional': False},

    'form_name': {'type': 'STRING', 'length': 50, 'validation_method': allow_specialchar, 'is_optional': False},
    'form_url': {'type': 'STRING', 'length': 250, 'validation_method': is_url, 'is_optional': False},
    'parent_menu': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': True},
    'form_type': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},

    'user_group_id': {'type': 'INT', 'length': 1000, 'validation_method': None, 'is_optional': False},
    'user_group_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},

    'l_id': {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': True},
    'l_position' : {'type': 'INT', 'length': 10, 'validation_method': None, 'is_optional': False},
    'l_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},

    'geography_id': {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    'geography_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},
    'parent_ids': {'type': 'VECTOR_TYPE_INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    'mapping': {'type': 'VECTOR_TYPE_STRING', 'length': 1000, 'validation_method': is_mapping, 'is_optional': False},
    'geography': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': False},

    'industry_id': {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': False},
    'industry_name': {'type': 'STRING', 'length': 50, 'validation_method': is_industry, 'is_optional': False},

    'statutory_nature_id': {'type': 'INT', 'length': 500, 'validation_method': None, 'is_optional': False},
    'statutory_nature_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},

    'statutory_id': {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    'statutory_name': {'type': 'STRING', 'length': 100, 'validation_method': is_alphabet, 'is_optional': False},

    'compliance_name': {'type': 'STRING', 'length': 500, 'validation_method': None, 'is_optional': False},
    'url': {'type': 'STRING', 'length': 500, 'validation_method': None, 'is_optional': False},

    'comp_id': {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': True},
    's_provision': {'type': 'STRING', 'length': 500, 'validation_method': None, 'is_optional': False},
    'c_task': {'type': 'STRING', 'length': 100, 'validation_method': None, 'is_optional': False},
    'description': {'type': 'STRING', 'length': 500, 'validation_method': None, 'is_optional': False},
    'doc_name': {'type': 'STRING', 'length': 50, 'validation_method': None, 'is_optional': True},
    'f_f_list': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'core', 'class_name': 'FileList'},
    'p_consequences': {'type': 'STRING', 'length': 500, 'validation_method': None, 'is_optional': True},
    'f_id': {'type': 'INT', 'length': '', 'validation_method': '', 'is_optional': True},
    'statu_dates': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'core', 'class_name': 'StatutoryDate'},
    'r_type_id': {'type': 'INT', 'length': 50, 'validation_method': None, 'is_optional': True},
    'r_every': {'type': 'INT', 'length': 50, 'validation_method': None, 'is_optional': True},
    'd_type_id': {'type': 'INT', 'length': 50, 'validation_method': None, 'is_optional': True},
    'duration': {'type': 'INT', 'length': 50, 'validation_method': None, 'is_optional': True},
    'frequency': {'type': 'STRING', 'length': 50, 'validation_method': None, 'is_optional': True},
    'summary': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': True},
    's_m_id': {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    'a_status': {'type': 'INT', 'length': 5, 'validation_method': None, 'is_optional': False},
    'r_reason': {'type': 'STRING', 'length': 500, 'validation_method': None, 'is_optional': True},
    's_provision': {'type': 'STRING', 'length': 500, 'validation_method': None, 'is_optional': False},
    'n_text': {'type': 'STRING', 'length': 500, 'validation_method': None, 'is_optional': True},
    's_mappings': {'type': 'VECTOR_TYPE', 'module_name': 'knowledgetransaction', 'class_name': 'ApproveMapping'},

    'compliance_frequency': {'type': 'VECTOR_TYPE', 'module_name': 'core', 'class_name': 'ComplianceFrequency'},
    'compliance_repeat_type': {'type': 'VECTOR_TYPE', 'module_name': 'core', 'class_name': 'ComplianceRepeatType'},
    'compliance_approval_status': {'type': 'VECTOR_TYPE', 'module_name': 'core', 'class_name': 'StatutoryApprovalStatus'},
    'compliance_duration_type': {'type': 'VECTOR_TYPE', 'module_name': 'core', 'calss_name': 'ComplianceDurationType'},
    'statu_mappings': {'type': 'MAP_TYPE', 'length': 100000, 'validation_method': is_numeric, 'module_name': 'core', 'class_name': 'StatutoryMapping'},
    'r_count': {'type': 'INT', 'length': 1000000, 'validation_method': None, 'is_optional': False},
    "industry_ids": {'type': 'VECTOR_TYPE_INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    "industry_names": {'type': 'VECTOR_TYPE_STRING', 'length': 100000, 'validation_method': None, 'is_optional': False},
    "statutory_ids": {'type': 'VECTOR_TYPE_INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    "statutory_mappings": {'type': 'VECTOR_TYPE_STRING', 'length': 100, 'validation_method': None, 'is_optional': False},
    "compliances": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', 'class_name': 'Compliance'},
    "compliance_names": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', 'class_name': 'Compliance_Download'},
    "geography_ids": {'type': 'VECTOR_TYPE_INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    "geography_mappings": {'type': 'VECTOR_TYPE_STRING', 'length': 100, 'validation_method': None, 'is_optional': False},
    'approval_status': {'type': 'INT', 'length': 50, 'validation_method': None, 'is_optional': False},
    'approval_status_text': {'type': 'STRING', 'length': 100, 'validation_method': None, 'is_optional': False},

    'levels': {'type': 'VECTOR_TYPE', 'module_name': 'knowledgemaster', 'class_name': 'Level'},
    "geography_levels": {'type': 'MAP_TYPE', 'validation_method': is_numeric, 'module_name': 'core', "class_name": "Level"},
    "geographies": {'type': 'MAP_TYPE', 'validation_method': is_alphabet, 'module_name': 'core', "class_name": "Geography"},
    "geography_report": {'type': 'MAP_TYPE', 'validation_method': is_alphabet, 'module_name': 'knowledgereport', "class_name": "GeographyMapping"},
    "statutory_natures": {'type': 'VECTOR_TYPE', 'validation_method': is_alphabet, 'module_name': 'core', "class_name": "StatutoryNature"},
    "statutory_levels": {'type': 'MAP_TYPE', 'validation_method': is_numeric, 'module_name': 'core', "class_name": "Level"},
    "statutories": {'type': 'MAP_TYPE', 'validation_method': is_numeric, 'module_name': 'core', 'class_name': 'Statutory'},

    'file_size': {'type': 'INT', 'length': 52949672950, 'validation_method': None, 'is_optional': False},
    'file_name': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': False},
    'file_content': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': True},

    'validity_days_id': {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': True},
    'validity_days': {'type': 'INT', 'length': 365, 'validation_method': None, 'is_optional': True},
    "validity_date_settings" : {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "ValidityDates"},
    "country_domain_mappings": {},

    'group_id': {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': False},
    'client_id': {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': True},
    'group_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},

    'country_names': {'type': 'TEXT', 'length': 10000, 'validation_method': None, 'is_optional': False},
    'next_unit_code': {'type': 'INT', 'length': 1000000, 'validation_method': None, "is_optional": False},

    "domain_details": {'type':'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'core', "class_name":"EntityDomainDetails"},
    "business_group": {'type': 'RECORD_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'core', "class_name": "ClientBusinessGroup"},
    "logo": {'type': 'RECORD_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'core', "class_name": "FileList"},
    "new_logo": {'type': 'RECORD_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'core', "class_name": "FileList"},
    'old_logo': {'type': 'TEXT', 'length': 500, 'validation_method': None, 'is_optional': True},
    'no_of_legal_entities': {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': False},
    "activation_date": {'type': 'TEXT', 'length': 10, 'validation_method': None, 'is_optional': True},

    'email_id': {'type': 'TEXT', 'length': 100, 'validation_method': None, 'is_optional': True},
    'business_group_id': {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': True},
    'business_group_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'legal_entity_id': {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': True},
    'legal_entity_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'no_of_licence': {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': False},
    'no_of_view_licence': {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': False},
    'file_space': {'type': 'INT', 'length': 100000000, 'validation_method': None, 'is_optional': False},
    'is_sms_subscribed': {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': False},
    'contract_from': {'type': 'TEXT', 'length': 11, 'validation_method': None, 'is_optional': False},
    'contract_to': {'type': 'TEXT', 'length': 11, 'validation_method': None, 'is_optional': False},
    "legal_entity_details": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "LegalEntityDetails"},
    "date_configurations": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "ClientConfiguration"},
    "org": {},
    "period_from": {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': True},
    "period_to": {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': True},
    "notification_type": {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},

    'unit_approval_list': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'clientcoordinationmaster', "class_name": "UnitApproval"},
    'unit_list': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "Unit"},
    'unit_id': {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    'unit_count': {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    'division_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'category_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'unit_code': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'unit_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'address': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': True},
    'postal_code': {'type': 'INT', 'length': 1000000, 'validation_method': is_numeric, 'is_optional': False},
    'domain_names': {'type': 'VECTOR_TYPE_STRING', 'length': 50, 'validation_method': None, 'is_optional': False},
    'org_names': {'type': 'VECTOR_TYPE_STRING', 'length': 50, 'validation_method': None, 'is_optional': False},
    'entity_unit_approval_list': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'clientcoordinationmaster', "class_name": "EntityUnitApproval"},
    "unit_approval_details": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'clientcoordinationmaster', "class_name": "UnitApprovalDetails"},
    'reason': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': False},
    'approval_status': {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': False},

    'message': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': False},
    'extra_details': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': True},


    "group_approval_list" : {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'clientcoordinationmaster', "class_name": "ClientGroupApproval"},
    "countries" : {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "Country"},
    "domains" : {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "Domain"},
    "industries" : {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "Industry"},

    "industry_name_id": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "Industries"},
    "groups" : {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "ClientGroup"},
    "unit_legal_entity" : {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'core', "class_name": "UnitLegalEntity"},
    "group_company_list" : {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "GroupCompanyForUnitCreation"},
    "business_group_list" : {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'core', "class_name": "BusinessGroup"},
    "divisions" : {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': True, 'module_name': 'core', "class_name": "Division"},

    'le_count': {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    "country_ids": {'type': 'VECTOR_TYPE_INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    "client_group_approval_details": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'clientcoordinationmaster', "class_name": "ClientGroupApprovalDetails"},
    "client_domains": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "Domain"},

    "notifications" : {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'general', "class_name": "Notification"},
    "audit_trail_details" : {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'general', "class_name": "AuditTrail"},
    "form_categories":  {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "FormCategory"},
    "user_group_details":  {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'admin', "class_name": "UserGroup"},
    'no_of_users': {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': False},
    "forms":  {'type': 'MAP_TYPE', 'length': None, 'validation_method': is_numeric, 'is_optional': False, 'module_name': 'core', "class_name": "Menu"},

    "menus":  {'type': 'MAP_TYPE_VECTOR_TYPE', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False, 'module_name': 'core', "class_name": "Form"},
    "menu": {'type': 'RECORD_TYPE', 'length': None, 'validation_method': None, 'module_name': 'core', 'class_name': 'Menu'},

    'user_id': {'type': 'INT', 'length': 1000, 'validation_method': None, 'is_optional': False},
    "employee_name": {'type': 'TEXT', 'length': 50, 'validation_method': None, 'is_optional': False},
    "employee_code": {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    "contact_no": {'type': 'TEXT', 'length': 12, 'validation_method': None, 'is_optional': True},
    "designation": {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    "domain_ids": {'type': 'VECTOR_TYPE_INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    "user_groups": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "UserGroup"},
    "user_details": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "UserDetails"},
    "industries_list" : {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "Industries"},
    "unit_geographies_list" : {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "UnitGeographyMapping"},
    "unit_geography_level_list" : {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "UnitGeographyLevel"},
    "unit_industries_list" : {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "UnitIndustries"},
    "d_ids": {'type': 'VECTOR_TYPE_INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    "i_ids": {'type': 'VECTOR_TYPE_INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    "cg": {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': False},
    "cl_id": {'type': 'INT', 'length': 500, 'validation_method': None, 'is_optional': False},
    "d": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technomasters', "class_name": "DIVISION"},
    "le": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technomasters', "class_name": "LEGAL_ENTITY"},
    "units": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'technomasters', "class_name": "UNIT"},

    "ug_name": {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    "user_group_id" : {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    "ug_id" : {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    "form_ids": {'type': 'VECTOR_TYPE_INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    "f_ids": {'type': 'VECTOR_TYPE_INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    "form_category_id" : {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    "fc_id" : {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    "form_category": {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},

    "db_server_name": {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    "database_server_ip": {'type': 'TEXT', 'length': 50, 'validation_method': None, 'is_optional': False},
    "port": {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': False},
    "db_servers": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "DBServer"},
    "no_of_clients": {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': False},

    "client_server_id": {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': True},
    "client_server_name": {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    "client_servers": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "ClientServer"},

    "client_dbs": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "ClientDatabase"},
    "client_groups": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "ClientGroup"},
    "client_legal_entities": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "LegalEntity"},
    "legal_entities": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "LegalEntity"},
    "business_groups": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'core', "class_name": "BusinessGroup"},
    "client_server_name_and_id": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "ClientServerNameAndID"},
    "db_server_name_and_id": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "DBServerNameAndID"},
    "machine_id": {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': True},
    "machine_name": {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},

    "file_storages": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "FileStorage"},

    "auto_deletion_entities": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "EntitiesWithAutoDeletion"},
    "auto_deletion_units": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "Unit"},
    "deletion_period": {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': True},
    "deletion_year": {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': True},
    "auto_deletion_details": {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': 'consoleadmin', "class_name": "AutoDeletionDetail"},

    "knowledge_managers": {'type':'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'admin', "class_name":"User"},
    "knowledge_users": {'type':'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'admin', "class_name":"User"},
    "techno_managers": {'type':'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'admin', "class_name":"User"},
    "techno_users": {'type':'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'admin', "class_name":"User"},
    "domain_managers": {'type':'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'admin', "class_name":"User"},
    "domain_users": {'type':'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'admin', "class_name":"User"},
    "user_mappings": {'type':'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'admin', "class_name":"UserMapping"},
    "cc_manager_id": {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': True},
    "user_mapping_id": {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': True},

    "user_mapping_users": {'type':'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name':'admin', "class_name":"UserMappingUsers"},
    "child_users": {'type': 'VECTOR_TYPE_INT', 'length': 100000, 'validation_method': None, 'is_optional': False},
    "parent_user_id": {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': True},
    "child_user_id": {'type': 'INT', 'length': 100000, 'validation_method': None, 'is_optional': True},
    "remarks":{'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': True},

    'bg_id': {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': True},
    'bg_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'dv_id': {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': True},
    'le_id': {'type': 'INT', 'length': 10000, 'validation_method': None, 'is_optional': False},
}

api_params['domain_id'] = api_params.get('d_id')
api_params['domain_name'] = api_params.get('d_name')
api_params['country_id'] = api_params.get('c_id')
api_params['country_name'] = api_params.get('c_name')
api_params['level_id'] = api_params.get('l_id')
api_params['level_position'] = api_params.get('l_position')
api_params['level_name'] = api_params.get('l_name')
api_params['is_remove'] = api_params.get('is_active')
api_params['is_exists'] = api_params.get('is_active')
api_params['is_admin'] = api_params.get('is_active')
api_params['parent_id'] = api_params.get('geography_id')
api_params['parent_mappings'] = api_params.get('mapping')
api_params['level_1_statutory_id'] = api_params.get('statutory_id')
api_params['level_1_s_id'] = api_params.get('statutory_id')
api_params['level_1_statutory_name'] = api_params.get('statutory_name')
api_params['g_l_id'] = api_params.get('level_id')
api_params['g_name'] = api_params.get('geography_name')
api_params['p_ids'] = api_params.get('parent_ids')
api_params['p_names'] = api_params.get('mapping')
api_params['g_id'] = api_params.get('geography_id')
api_params['g_ids'] = api_params.get('geography_id')
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
