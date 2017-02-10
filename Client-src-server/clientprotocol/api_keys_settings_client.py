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
    'u_c_id': make_int_field(),
    'f_ids': make_vector_type_int(length=1000, is_optional=True),
    'u_c_name': make_string_field(length=50, validfun=is_alpha_numeric),
    "forms": make_map_type("clientcore", "Menu"),
    "menus": make_map_type_vector_type("clientcore", "Form"),

    "user_groups": make_vector_type_field("clientcore", "ClientUserGroup"),
    "user_category": make_vector_type_field("clientcore", "ClientUsercategory"),

    'form_ids': make_int_field(),

    "country_info": make_vector_type_field(module="clientcore", klass_name="Country"),
    "entity_info": make_vector_type_field(module="clientcore", klass_name="LegalEntityInfo"),
    "ct_id": make_int_field(),
    "le_id": make_int_field(),
    "le_name": make_string_field(),
    "bg_name": make_string_field(is_optional=True),
    "bg_id": make_int_field(is_optional=True),
    "cat_id": make_int_field(is_optional=True),
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
    "c_ids": make_vector_type_int(),
    "c_names": make_vector_type_string(),
    "d_id": make_int_field(),
    "d_ids": make_vector_type_int(),
    "d_name": make_string_field(),
    "d_names": make_vector_type_string(),
    "div_id": make_int_field(is_optional=True),
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
    "unit_id": make_int_field(length=10000, is_optional=True),
    "division_id": make_int_field(is_optional=True),
    "category_id": make_int_field(is_optional=True),
    "legal_entity_id": make_int_field(length=10000, is_optional=True),
    'legal_entity_name': make_string_field(length=50, validfun=is_alpha_numeric, is_optional=False),
    "business_group_id": make_int_field(is_optional=True),

    "unit_code": make_string_field(length=50, validfun=is_alpha_numeric, is_optional=False),
    "unit_name": make_string_field(length=50, validfun=is_alpha_numeric, is_optional=False),
    "address": make_text_field(is_optional=True),
    "country_id": make_int_field(is_optional=True),
    "domain_id": make_int_field(length=10000),
    "is_closed": make_bool_field(),

    'postal_code': make_int_field(length=1000000, is_optional=False),
    'division_name': make_string_field(length=50, validfun=is_alpha_numeric, is_optional=True),
    'category_name': make_string_field(length=50, validfun=is_alpha_numeric, is_optional=True),
    'business_group_name': make_string_field(length=50, validfun=is_alpha_numeric, is_optional=True),
    'is_active': make_bool_field(is_optional=False),
    "closed_on": make_text_field(length=200, is_optional=True),
    'validity_days': make_int_field(length=365, is_optional=True),
    'grp_mode': make_string_field(length=50, is_optional=False),
    "closed_remarks": make_text_field(length=500, is_optional=True),
    "compliance_id": make_int_field(length=10000, is_optional=True),
    "compliance_task": make_text_field(is_optional=True),
    "frequency_id": make_int_field(is_optional=True),
    "frequency_name": make_string_field(),
    "statutory_mapping": make_text_field(length=500, is_optional=True),
    "user_type_id": make_int_field(is_optional=True),
    "user_type": make_string_field(is_optional=True),
    "task_status_id": make_int_field(is_optional=True),
    "task_status": make_string_field(is_optional=True),
    "assignee": make_int_field(is_optional=True),
    "assignee_name": make_text_field(is_optional=True),
    "concurrence_person": make_int_field(is_optional=True),
    "concurrer_name": make_text_field(is_optional=True),
    "approval_person": make_int_field(is_optional=True),
    "approver_name": make_text_field(is_optional=True),
    "due_from_date": make_text_field(is_optional=True),
    "due_to_date": make_text_field(is_optional=True),
    "due_date": make_text_field(is_optional=True),
    "activity_date": make_text_field(is_optional=True),
    "activity_status": make_string_field(is_optional=True),
    "documents": make_text_field(is_optional=True),
    "completion_date": make_text_field(is_optional=True),
    "user_id": make_int_field(),
    "url": make_text_field(is_optional=True),
    "domain_name": make_string_field(),
    "sp_name": make_text_field(is_optional=True),
    "sp_id_optional": make_int_field(is_optional=True),
    "sp_ass_id_optional": make_int_field(is_optional=True),
    "sp_cc_id_optional": make_int_field(is_optional=True),
    "sp_app_id_optional": make_int_field(is_optional=True),
    "user_id_optional": make_int_field(is_optional=True),
    'user_category_id': make_int_field(),

    'csv': make_bool_field(is_optional=False),
    'from_count': make_int_field(is_optional=False),
    'page_count': make_int_field(is_optional=False),
    'total_count': make_int_field(is_optional=False),

    "act": make_text_field(is_optional=True),
    "c_task": make_text_field(is_optional=True),
    "user_id": make_int_field(),
    "employee_code": make_text_field(is_optional=True),
    "employee_name": make_string_field(),
    "link": make_text_field(length=500, is_optional=True),


    "countries": make_vector_type_field(module="clientcore", klass_name="Country"),
    "domains": make_vector_type_field(module="clientcore", klass_name="Domain"),
    "bg_groups": make_vector_type_field(module="clientcore", klass_name="ClientBusinessGroup"),
    "le_infos": make_vector_type_field(module="clientcore", klass_name="ClientLegalEntity"),
    "div_infos": make_vector_type_field(module="clientcore", klass_name="ClientDivision", is_optional=True),
    "units": make_vector_type_field(module="clientcore", klass_name="ClientUnit"),
    "acts": make_vector_type_field(module="clientcore", klass_name="ClientAct"),
    "compliances": make_vector_type_field(module="clientcore", klass_name="ComplianceFilter"),
    "legal_entity_users": make_vector_type_field(module="clientcore", klass_name="LegalEntityUser"),

    "unit_closure_legal_entities": make_vector_type_field(module="clientcore", klass_name="UnitClosureLegalEntity"),
    "unit_closure_units": make_vector_type_field(module="clientcore", klass_name="UnitClosure_Units"),

    "assign_unit_infos": make_vector_type_field(module="clienttransactions", klass_name="ASSIGN_COMPLIANCE_UNITS"),
    "assign_user_info": make_vector_type_field(module="clienttransactions", klass_name="ASSIGN_COMPLIANCE_USER"),
    "two_level_approve": make_bool_field(),
    "client_admin": make_int_field(),

    "unit_legal_entity": make_vector_type_field(module="clientreport", klass_name="UnitLegalEntity"),
    "act_legal_entity": make_vector_type_field(module="clientreport", klass_name="ActLegalEntity"),
    "compliance_task_list": make_vector_type_field(module="clientreport", klass_name="TaskLegalEntity"),
    "compliance_frequency_list": make_vector_type_field(module="clientreport", klass_name="ComplianceFrequency"),
    "compliance_user_type": make_vector_type_field(module="clientreport", klass_name="ComplianceUserType"),
    "compliance_task_status": make_vector_type_field(module="clientreport", klass_name="ComplianceTaskStatus"),
    "compliance_users": make_vector_type_field(module="clientreport", klass_name="ComplianceUsers"),
    "legal_entities_compliances": make_vector_type_field(module="clientreport", klass_name="LegalEntityWiseReport"),
    "compliance_frequency": make_vector_type_field(module="clientcore", klass_name="ComplianceFrequency"),
    "domain_list": make_vector_type_field(module="clientcore", klass_name="Domain"),
    "unit_compliances": make_vector_type_field(module="clientreport", klass_name="UnitWiseReport"),

    "sp_list": make_vector_type_field(module="clientreport", klass_name="ServiceProviders"),
    "sp_domains_list": make_vector_type_field(module="clientreport", klass_name="ServiceProviderDomains"),
    "sp_unit_list": make_vector_type_field(module="clientreport", klass_name="ServiceProviderUnits"),
    "sp_act_task_list": make_vector_type_field(module="clientreport", klass_name="ServiceProviderActList"),
    "sp_users_list": make_vector_type_field(module="clientreport", klass_name="ServiceProvidersUsers"),
    "sp_compliances": make_vector_type_field(module="clientreport", klass_name="LegalEntityWiseReport"),
    "le_users_list": make_vector_type_field(module="clientreport", klass_name="LegalEntityUsers"),
    "user_domains_list": make_vector_type_field(module="clientreport", klass_name="UserDomains"),
    "users_units_list": make_vector_type_field(module="clientreport", klass_name="UserUnits"),
    "user_act_task_list": make_vector_type_field(module="clientreport", klass_name="UsersActList"),
    "user_compliances": make_vector_type_field(module="clientreport", klass_name="UnitWiseReport"),

    "frequency_id": make_int_field(),
    "frequency": make_string_field(),
    "rs_unit_list": make_vector_type_field(module="clientcore", klass_name="ReviewSettingsUnits"),
    "u_code": make_string_field(),
    "u_name": make_string_field(),
    "g_name": make_string_field(),
    "timeline":   make_string_field(),
    "rs_compliance_list":  make_vector_type_field(module="clientcore", klass_name="ReviewSettingsCompliance"),
    "r_every": make_int_field(),
    "s_dates": make_vector_type_field(module="clientcore", klass_name="StatutoryDate"),
    "trigger_before_days": make_int_field(is_optional=True),
    "due_date": make_text_field(length=20, is_optional=True),
    "statu_date": make_int_field(is_optional=True),
    "statu_month": make_int_field(is_optional=True),
    "repeat_by": make_int_field(is_optional=True),
    "unit_ids": make_vector_type_int(length=1000, is_optional=False),
    "f_id": make_int_field(),
    "sno": make_int_field(),
    "month_from": make_int_field(),
    "month_to": make_int_field(),
    "level_1_s_name": make_string_field(),

    "cat_info": make_vector_type_field(module="clientcore", klass_name="Category", is_optional=True),
    "usr_by": make_text_field(is_optional=True),
    "usr_on": make_text_field(is_optional=True),
    "is_locked": make_bool_field(),
    "allow_unlock": make_bool_field(),
    "is_new": make_bool_field()
}
