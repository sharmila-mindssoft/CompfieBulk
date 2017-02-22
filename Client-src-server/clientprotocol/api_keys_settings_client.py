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

def make_int_field(length=10000, is_optional=False):
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

def make_widget_type():
    # customized widget data from backend
    return {'type': 'WIDGET_TYPE'}

def make_reccord_type(module, klass_name):
    return {'type': 'RECORD_TYPE', 'module_name': module, 'class_name': klass_name}

api_params = {
    'request': {},
    'session_token': make_text_field(length=50),
    'reset_token':  make_text_field(length=50),
    'new_password': make_text_field(length=20),
    'current_password': make_text_field(length=20),
    'login_type': make_enum_type("clientcore", "SESSION_TYPE"),
    'username': make_text_field(length=100),
    'user_name': make_text_field(length=100, is_optional=True),
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

    'u_g_id': make_int_field(is_optional=True), # User Priviliges, User Management
    'u_g_name': make_string_field(length=50, validfun=is_alpha_numeric, is_optional=True), # User Priviliges, User Management

    'is_active': make_bool_field(),
    'u_c_id': make_int_field(), # User Priviliges, User Management
    'f_ids': make_vector_type_int(length=1000, is_optional=True),
    'u_c_name': make_string_field(length=50, validfun=is_alpha_numeric), # User Priviliges, User Management
    "forms": make_map_type("clientcore", "Menu"),
    "menus": make_map_type_vector_type("clientcore", "Form"),
    "user_groups": make_vector_type_field("clientcore", "ClientUserGroup"),
    "user_category": make_vector_type_field("clientcore", "ClientUsercategory"),
    'form_ids': make_int_field(),
    "country_info": make_vector_type_field(module="clientcore", klass_name="Country"),
    "entity_info": make_vector_type_field(module="clientcore", klass_name="LegalEntityInfo"),
    "ct_id": make_int_field(),
    "le_id": make_int_field(),
    "le_ids": make_vector_type_int(),
    "le_name": make_string_field(),

    "bg_name": make_string_field(is_optional=True), # User Management, Other forms
    "bg_id": make_int_field(is_optional=True), # User Management, Other forms
    "cat_id": make_int_field(is_optional=True), # User Management, Other forms    
    "cat_name": make_string_field(length=50, validfun=is_alpha_numeric, is_optional=True), # User Management, Other forms
    "usr_id": make_int_field(),    

    "email_id": make_string_field(validfun=allow_specialchar),
    "user_email_id": make_string_field(validfun=allow_specialchar),
    "emp_name": make_string_field(is_optional=True),
    "emp_code": make_string_field(is_optional=True),
    "con_no": make_text_field(is_optional=True),
    "mob_no": make_text_field(is_optional=True),
    "address": make_text_field(is_optional=True),
    "menu":  make_map_type_vector_type("clientcore", "Form"),
    "user_level": make_int_field(is_optional=True),
    "sp_id": make_int_field(is_optional=True),
    "s_u_id": make_int_field(is_optional=True),
    "s_u_name": make_string_field(is_optional=True),
    "is_assignee": make_bool_field(is_optional=True),
    "is_approver": make_bool_field(is_optional=True),
    "is_concurrence": make_bool_field(is_optional=True),
    "u_id": make_int_field(),
    "u_ids": make_vector_type_int(is_optional=True),
    "u_name": make_string_field(),
    "c_name": make_string_field(),
    "c_id": make_int_field(),
    "c_ids": make_vector_type_int(),
    "c_names": make_vector_type_string(),
    "d_id": make_int_field(is_optional=True), # User Management , Other Forms
    "d_ids": make_vector_type_int(),
    "d_name": make_string_field(is_optional=True), # User Management, Other Forms
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
    "doc_name": make_string_field(validfun=allow_specialchar),
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
    "country_id": make_int_field(is_optional=True),
    "domain_id": make_int_field(length=10000),
    "organisation_id": make_int_field(is_optional=True),
    "organisation_name": make_string_field(is_optional=True),
    "d_i_names": make_vector_type_string(),
    "is_closed": make_bool_field(),
    'postal_code': make_int_field(length=1000000, is_optional=False),
    'division_name': make_string_field(length=50, validfun=is_alpha_numeric, is_optional=True),
    'category_name': make_string_field(length=50, validfun=is_alpha_numeric, is_optional=True),
    'geography_name': make_string_field(length=50, validfun=is_alpha_numeric, is_optional=True),
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
    "unit_status_id": make_int_field(is_optional=True),
    "unit_status": make_string_field(is_optional=True),
    "assignee": make_int_field(is_optional=True),
    "assignee_name": make_text_field(is_optional=True),
    "concurrence_person": make_int_field(is_optional=True),
    "concurrer_name": make_text_field(is_optional=True),
    "approval_person": make_int_field(is_optional=True),
    "approver_name": make_text_field(is_optional=True),
    "due_from_date": make_text_field(is_optional=True),
    "due_to_date": make_text_field(is_optional=True),
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
    "i_ids": make_vector_type_int(),
    "compliance_description": make_text_field(length=500),
    "notification_text": make_text_field(length=500),
    "created_on": make_text_field(is_optional=True),
    "s_p_status_id": make_int_field(is_optional=True),
    "s_p_status": make_string_field(),
    "contract_period": make_text_field(is_optional=True),
    "sp_status_date": make_text_field(is_optional=True),
    "user_status": make_string_field(),
    "user_status_date": make_text_field(is_optional=True),
    "unit_count": make_int_field(is_optional=True),
    "form_id_optional": make_int_field(is_optional=True),
    "action": make_text_field(length=500, is_optional=True),
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
    "cat_infos": make_vector_type_field(module="clientcore", klass_name="ClientCategory", is_optional=True),
    "units": make_vector_type_field(module="clientcore", klass_name="ClientUnit"),
    "unit_closure_legal_entities": make_vector_type_field(module="clientcore", klass_name="UnitClosureLegalEntity"),
    "unit_closure_units": make_vector_type_field(module="clientcore", klass_name="UnitClosure_Units"),
    "acts": make_vector_type_field(module="clientcore", klass_name="ClientAct"),
    "compliances": make_vector_type_field(module="clientcore", klass_name="ComplianceFilter"),
    "legal_entity_users": make_vector_type_field(module="clientcore", klass_name="LegalEntityUser"),
    "assign_unit_infos": make_vector_type_field(module="clienttransactions", klass_name="ASSIGN_COMPLIANCE_UNITS"),
    "assign_user_info": make_vector_type_field(module="clienttransactions", klass_name="ASSIGN_COMPLIANCE_USER"),
    "two_level_approve": make_bool_field(),
    "client_admin": make_int_field(),

    "service_providers": make_vector_type_field(module="clientcore", klass_name="ServiceProviderDetails"),
    "s_p_id" : make_int_field(),
    "s_p_name": make_string_field(is_optional=True),
    "s_p_short": make_string_field(is_optional=True),
    "cont_from": make_text_field(is_optional=True),
    "cont_to": make_text_field(is_optional=True),
    "cont_person": make_string_field(is_optional=True),
    "cont_no": make_text_field(is_optional=True),
    "mob_no": make_text_field(),
    "e_id": make_text_field(),
    "address": make_string_field(length=500, is_optional=True),
    "remarks": make_string_field(is_optional=True),
    "is_blocked": make_bool_field(),
    "unblock_days": make_int_field(),

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
    "frequency": make_string_field(),
    "rs_unit_list": make_vector_type_field(module="clientcore", klass_name="ReviewSettingsUnits"),
    "u_code": make_string_field(),
    "u_name": make_string_field(),
    "g_name": make_text_field(),
    "timeline":   make_string_field(),
    "rs_compliance_list":  make_vector_type_field(module="clientcore", klass_name="ReviewSettingsCompliance"),
    "r_every": make_int_field(is_optional=True),
    "s_dates": make_vector_type_field(module="clientcore", klass_name="StatutoryDate"),
    "statu_dates": make_vector_type_field(module="clientcore", klass_name="StatutoryDate"),
    "old_statu_dates": make_vector_type_field(module="clientcore", klass_name="StatutoryDate"),
    "trigger_before_days": make_int_field(is_optional=True),
    "due_date": make_text_field(length=20, is_optional=True),
    "statutory_date": make_int_field(is_optional=True),
    "statutory_month": make_int_field(is_optional=True),
    "d_date": make_text_field(length=20, is_optional=True),
    "v_date": make_text_field(length=20, is_optional=True),
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
    "reassigned_history_list": make_vector_type_field(module="clientcore", klass_name="ReassignedHistoryReportSuccess", is_optional=True),
    "act_name": make_string_field(),
    "from_date": make_text_field(length=20, is_optional=True),
    "to_date": make_text_field(length=20, is_optional=True),
    "assigned_date": make_text_field(length=20, is_optional=True),
    "assigned": make_string_field(),
    "reason": make_string_field(),
    "f_count": make_int_field(),
    "t_count": make_int_field(),
    'total': make_int_field(is_optional=False),
    'new_user': make_text_field(is_optional=True),
    'old_user': make_text_field(is_optional=True),
    'remarks': make_text_field(length=500, is_optional=True),
    'assigned_on': make_text_field(length=20, is_optional=True),
    'unit': make_text_field(is_optional=True),
    'status_report_consolidated_list': make_vector_type_field(module="clientcore", klass_name="GetStatusReportConsolidatedSuccess", is_optional=True),
    'status_name': make_string_field(),
    'compliance_activity_id': make_int_field(),
    'compliance_history_id': make_int_field(),
    'compliance_name': make_text_field(is_optional=True),
    'activity_on': make_text_field(length=20, is_optional=True),
    'uploaded_document': make_text_field(is_optional=True),
    'user_name': make_text_field(is_optional=True),
    'statutory_settings_unit_Wise_list': make_vector_type_field(module="clientcore", klass_name="GetStatutorySettingsUnitWiseSuccess", is_optional=True),
    'document_name': make_text_field(is_optional=True),
    "repeats_type_id": make_int_field(is_optional=True),
    "repeats_type": make_string_field(is_optional=True),
    "rs_compliances": make_vector_type_field(module="clienttransaction", klass_name="SaveReviewSettingsComplianceDict"),
    "m_name_from": make_string_field(),
    "m_name_to": make_string_field(),
    "cat_info": make_vector_type_field(module="clientcore", klass_name="Category", is_optional=True),
    "usr_by": make_text_field(is_optional=True),
    "usr_on": make_text_field(is_optional=True),
    "is_locked": make_bool_field(),
    "allow_unlock": make_bool_field(),
    "lock": make_bool_field(),
    "is_new": make_bool_field(),
    "c_c_id": make_int_field(),
    "a_status": make_bool_field(),
    "n_a_remarks": make_text_field(is_optional=True),
    "c_o_status": make_bool_field(),
    "c_remarks": make_text_field(is_optional=True),
    "update_statutories": make_vector_type_field(module="clienttransactions", klass_name="UpdateStatutoryCompliance"),
    "s_s": make_int_field(),
    "is_saved": make_bool_field(),

    "c_name":make_text_field(),
    "b_g_name":make_text_field(is_optional=True),
    "le_name":make_text_field(), # User Management & Other forms
    "cont_from":make_text_field(),
    "cont_to":make_text_field(),
    "total_licences":make_int_field(),
    "used_licences":make_int_field(),
    "le_id":make_int_field(), # User Management & Other forms
    "user_id":make_int_field(),
    "u_cat_id":make_int_field(),
    "u_g_id":make_int_field(),
    "emp_name":make_text_field(),
    "emp_code":make_text_field(),
    "cont_no":make_text_field(is_optional=True),
    "mob_no":make_text_field(),
    "email_id":make_text_field(),
    "user_name":make_text_field(),
    "resend_mail":make_bool_field(),
    "is_active":make_bool_field(),
    "is_disable":make_bool_field(),
    "reason":make_text_field(),
    "unblock":make_text_field(),
    "u_level":make_int_field(is_optional=True),
    "s_unit":make_int_field(is_optional=True),
    "is_sp":make_bool_field(),
    "sp_id":make_int_field(is_optional=True),

    "u_dm_id":make_int_field(),# User Management
    "u_dm_name":make_text_field(), # User Management
    "u_unt_id":make_int_field(), # User Management
    "u_unt_code":make_string_field(), # User Management
    "u_unt_name":make_string_field(), # User Management
    "u_unt_address":make_string_field(), # User Management
    "u_unt_postal":make_string_field(), # User Management
    "user_domain_ids": make_vector_type_field(module="clientcore", klass_name="UserDomains"), # User Management
    "user_unit_ids": make_vector_type_field(module="clientcore", klass_name="UserUnits"), # User Management    
    "user_entity_ids": make_vector_type_int(length=1000), # User Management
    "um_user_category": make_vector_type_field(module="clientcore", klass_name="ClientUsercategory_UserManagement"), # User Management
    "um_user_group": make_vector_type_field(module="clientcore", klass_name="ClientUserGroup_UserManagement"), # User Management
    "um_legal_entity": make_vector_type_field(module="clientcore", klass_name="ClientUserLegalEntity_UserManagement"), # User Management
    "um_business_group": make_vector_type_field(module="clientcore", klass_name="ClientUserBusinessGroup_UserManagement"), # User Management
    "um_group_division": make_vector_type_field(module="clientcore", klass_name="ClientUserDivision_UserManagement"), # User Management
    "um_group_category": make_vector_type_field(module="clientcore", klass_name="ClientGroupCategory_UserManagement"), # User Management
    "um_legal_domain": make_vector_type_field(module="clientcore", klass_name="ClientLegalDomains_UserManagement"), # User Management
    "um_legal_units": make_vector_type_field(module="clientcore", klass_name="ClientLegalUnits_UserManagement"), # User Management
    "um_legal_entities": make_vector_type_field(module="clientcore", klass_name="ClientLegalEntity_UserManagement"), # User Management

    "captcha": make_string_field(length=CAPTCHA_LENGTH, is_optional=True, validfun=is_alpha_numeric), # User Registration
    "uname":  make_string_field(length=20, validfun=is_alpha_numeric, is_optional=True), # User Registration
    "token": make_string_field(length=100, is_optional=True, validfun=is_alpha_numeric), # User Registration
    'pword': make_text_field(length=20), # User Registration


    "assign_units": make_vector_type_field(module="clienttransactions", klass_name="ASSIGN_COMPLIANCE_UNITS"),
    "comp_frequency": make_vector_type_field(module="clientcore", klass_name="ComplianceFrequency"),
    "usr_cat_id": make_int_field(),
    "u_l": make_int_field(is_optional=True),
    "sp_short_name": make_text_field(length=50, is_optional=True),
    "assign_users": make_vector_type_field(module="clienttransactions", klass_name="Users"),
    "t_l_approve": make_bool_field(),
    "freq": make_text_field(),
    "statu_dates": make_vector_type_field(module="clientcore", klass_name="StatutoryDate"),
    "applicable_units": make_vector_type_int(),
    "summary": make_text_field(is_optional=True),
    "due_date_list": make_vector_type_string(is_optional=True),
    "assign_statutory": make_map_type_vector_type(module="clienttransactions", klass_name="UNIT_WISE_STATUTORIES"),
    "level_one_name": make_vector_type_string(length=150),
    "unit_wise_status": make_vector_type_field(module="clienttransactions", klass_name="ComplianceUnitApplicability"),
    "assign_compliances": make_vector_type_field(module="clienttransactions", klass_name="ASSIGNED_COMPLIANCE"),
    "d_months": make_map_type_vector_type(module="dashboard", klass_name="DomainWiseYearConfiguration"),
    "le_did_infos": make_vector_type_field(module="dashboard", klass_name="ClientLegalEntityInfo"),
    "d_info": make_vector_type_field(module="clientcore", klass_name="DomainInfo"),
    "filter_type": make_enum_type(module="clientcore", klass_name="FILTER_TYPE"),
    "filter_ids": make_vector_type_int(is_optional=True),
    "filter_id": make_int_field(),
    "chart_year": make_int_field(length=10000),
    "chart_data": make_vector_type_field(module="dashboard", klass_name="ChartDataMap"),
    "filter_type_id": make_int_field(),
    "c_data": make_vector_type_field(module="clientcore", klass_name="NumberOfCompliances"),
    "complied_count": make_int_field(length=10000),
    "delayed_compliance_count": make_int_field(),
    "inprogress_compliance_count": make_int_field(),
    "complied_compliances_count": make_int_field(),
    "total_compliances": make_int_field(),
    "not_complied_count": make_int_field(length=100000),
    "year": make_text_field(),
    "compliance_status": make_enum_type(module="clientcore", klass_name="COMPLIANCE_STATUS"),
    "record_count": make_int_field(length="100000"),
    "drill_down_data": make_vector_type_field(module="dashboard", klass_name="DrillDownData"),
    "indus_name": make_text_field(),
    "drill_compliances": make_map_type_vector_type(module="dashboard", klass_name="Level1Compliance", validfun=allow_specialchar),
    "status": make_enum_type(module="clientcore", klass_name="COMPLIANCE_STATUS"),
    "ageing": make_text_field(),
    "cat_name": make_text_field(is_optional=True),
    "es_chart_data": make_vector_type_field(module="dashboard", klass_name="EscalationData"),
    "years": make_vector_type_int(length=10000),
    "delayed": make_vector_type_field(module="dashboard", klass_name="DrillDownData"),
    "not_complied": make_vector_type_field(module="dashboard", klass_name="DrillDownData"),
    "divisions": make_vector_type_field(module="clientreport", klass_name="Divisions"),
    "categories": make_vector_type_field(module="clientreport", klass_name="Category"),
    "units_list": make_vector_type_field(module="clientreport", klass_name="UnitList"),
    "domains_organisations_list": make_vector_type_field(module="clientreport", klass_name="DomainsOrganisation"),
    "unit_status_list": make_vector_type_field(module="clientreport", klass_name="UnitStatus"),
    "unit_list_report": make_vector_type_field(module="clientreport", klass_name="UnitListReport"),
    "stat_notf_list_report": make_vector_type_field(module="clientreport", klass_name="StatutoryNotificationReport"),
    "sp_user_list": make_vector_type_field(module="clientmasters", klass_name="ServiceProviderUsers"),
    "sp_status_list": make_vector_type_field(module="clientmasters", klass_name="ServiceProvidersStatus"),
    "sp_details_list": make_vector_type_field(module="clientmasters", klass_name="ServiceProvidersDetailsList"),
    "audit_activities": make_vector_type_field(module="clientreport", klass_name="AuditTrailActivities"),
    "audit_users_list": make_vector_type_field(module="clientmasters", klass_name="AuditTrailUsers"),
    "audit_forms_list": make_vector_type_field(module="clientmasters", klass_name="AuditTrailForms"),
    "log_trace_activities": make_vector_type_field(module="clientmasters", klass_name="LoginTraceActivities"),
    "user_profile": make_vector_type_field(module="clientmasters", klass_name="UserProfile"),
    "T_0_to_30_days_count": make_int_field(length=10000),
    "T_31_to_60_days_count": make_int_field(length=10000),
    "T_61_to_90_days_count": make_int_field(length=10000),
    "Above_90_days_count": make_int_field(length=10000),
    "not_complied_type": make_enum_type(module="clientcore", klass_name="NOT_COMPLIED_TYPE"),
    "applicability_status": make_enum_type(module="clientcore", klass_name="APPLICABILITY_STATUS"),
    "r_drill_down_data": make_vector_type_field(module="dashboard", klass_name="ApplicableDrillDown"),
    "level1_statutory_name": make_text_field(),
    "ap_compliances": make_map_type(module="dashboard", klass_name="Compliance", validfun=allow_specialchar),
    "format_file_list": make_vector_type_field(module="clientcore", klass_name="FileList", is_optional=True),
    "p_cons": make_text_field(is_optional=True),
    "download_url": make_text_field(is_optional=True),
    "t_drill_down_data": make_vector_type_field(module="dashboard", klass_name="TrendDrillDownData"),
    "t_compliances": make_map_type(module="dashboard", klass_name="TrendCompliance", validfun=allow_specialchar),
    "not_opted_count": make_int_field(length=10000),
    "unassign_count": make_int_field(length=10000),
    "rejected_count": make_int_field(length=10000),
    "not_complied_count": make_int_field(length=10000),
    "n_drill_down_data": make_vector_type_field(module="dashboard", klass_name="DrillDownData"),

    "trend_data" : make_vector_type_field(module="dashboard", klass_name="TrendCompliedMap"),

    "chart_title": make_text_field(),
    "xaxis_name": make_text_field(),
    "xaxis": make_vector_type_string(),
    "yaxis_name": make_text_field(),
    "yaxis": make_vector_type_string(),
    "widget_data": make_widget_type(),

    "business_groups": make_vector_type_field(module="clientcore", klass_name="ClientBusinessGroup"),
    "legal_entities": make_vector_type_field(module="dashboard", klass_name="ClientLegalEntityInfo"),
    "client_divisions": make_vector_type_field(module="clientcore", klass_name="ClientDivision"),
    "client_categories": make_vector_type_field(module="clientcore", klass_name="Category"),
    "client_users": make_vector_type_field(module="clientreport", klass_name="User"),

    'domain_score_card_list': make_vector_type_field(module="clientcore", klass_name="GetDomainScoreCardSuccess", is_optional=True),
    "assigned_count": make_int_field(length=10000),
    "unassigned_count": make_int_field(length=10000),
    "units_wise_count": make_vector_type_field(module="clientcore", klass_name="GetDomainWiseUnitScoreCardSuccess", is_optional=True),
    "delayed_count": make_int_field(length=10000),
    "inprogress_count": make_int_field(length=10000),
    "overdue_count": make_int_field(length=10000),
    "users": make_vector_type_field(module="clientcore", klass_name="LegalEntityUser"),
    "assingee_data": make_vector_type_field(module="dashboard", klass_name="AssigneeChartData"),
    "assignee_wise_details": make_vector_type_field(module="dashboard", klass_name="AssigneeWiseDetails"),
    "domain_wise_details": make_vector_type_field(module="dashboard", klass_name="DomainWise"),

    "reassigned_count": make_int_field(length=10000),
    "year_wise_data": make_vector_type_field(module="dashboard", klass_name="YearWise"),
    "sdelayed_compliance": make_reccord_type(module="dashboard", klass_name="DelayedCompliance"),
    "reassigned_compliances": make_vector_type_field(module="dashboard", klass_name="RessignedCompliance", is_optional=True),

    "reassigned_from": make_text_field(),
    "start_date": make_text_field(),
    "due_date": make_text_field(),
    "due_date": make_text_field(),
    "reassigned_date": make_text_field(),
    "completed_date": make_text_field(),

    "description": make_text_field(),
    "complied": make_map_type(module="dashboard", klass_name="AssigneeWiseLevel1Compliance", validfun=allow_specialchar),
    "delayed_map": make_map_type(module="dashboard", klass_name="AssigneeWiseLevel1Compliance", validfun=allow_specialchar),
    "inprogress_map": make_map_type(module="dashboard", klass_name="AssigneeWiseLevel1Compliance", validfun=allow_specialchar),
    "not_complied_map": make_map_type(module="dashboard", klass_name="AssigneeWiseLevel1Compliance", validfun=allow_specialchar),
    "assignee_wise_drill_down": make_reccord_type(module="dashboard", klass_name="AssigneeWiseCompliance"),
    "assignee_id": make_int_field(),
    "start_count": make_int_field(),
    "w_id": make_int_field(),
    "width": make_text_field(),
    "height": make_text_field(),
    "pin_status": make_bool_field(),
    "widget_info": make_vector_type_field(module="clienttransactions", klass_name="WidgetInfo")
}

