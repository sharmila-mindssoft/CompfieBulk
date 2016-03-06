from protocol import (clientmasters, core, login)
from server.controller.corecontroller import process_user_menus

__all__ = [
    "process_client_master_requests"
]

def process_client_master_requests(request, db) :
    session_token = request.session_token
    client_info = session_token.split("-")
    request = request.request
    client_id = int(client_info[0])
    session_user = db.validate_session_token(client_id, session_token)
    if session_user is None:
        return login.InvalidSessionToken()

    if type(request) is clientmasters.GetServiceProviders:
        return get_service_providers(db, request, session_user, client_id)

    if type(request) is clientmasters.SaveServiceProvider:
        return save_service_provider(db, request, session_user, client_id)

    if type(request) is clientmasters.UpdateServiceProvider:
        return update_service_provider(db, request, session_user, client_id)

    if type(request) is clientmasters.ChangeServiceProviderStatus:
        return change_service_provider_status(
            db, request, session_user, client_id
        )

    if type(request) is clientmasters.GetUserPrivileges:
        return get_user_privileges(db, request, session_user, client_id)

    if type(request) is clientmasters.SaveUserPrivileges:
        return save_user_privileges(db, request, session_user, client_id)

    if type(request) is clientmasters.UpdateUserPrivileges:
        return update_user_privileges(db, request, session_user, client_id)

    if type(request) is clientmasters.ChangeUserPrivilegeStatus:
        return change_user_privilege_status(
            db, request, session_user, client_id
        )

    if type(request) is clientmasters.GetClientUsers:
        return get_client_users(db, request, session_user, client_id)

    if type(request) is clientmasters.SaveClientUser:
        return save_client_user(db, request, session_user, client_id)

    if type(request) is clientmasters.UpdateClientUser:
        return update_client_user(db, request, session_user, client_id)

    if type(request) is clientmasters.ChangeClientUserStatus:
        return change_client_user_status(db, request, session_user, client_id)

    if type(request) is clientmasters.ChangeAdminStatus:
        return change_admin_status(db, request, session_user, client_id)

    if type(request) is clientmasters.GetUnits:
        return get_units(db, request, session_user, client_id)

    if type(request) is clientmasters.CloseUnit:
        return close_unit(db, request, session_user, client_id)

    if type(request) is clientmasters.GetAuditTrails:
        return get_audit_trails(db, request, session_user, client_id)

def get_service_providers(db, request, session_user, client_id):
    service_provider_list = db.get_service_provider_details_list(client_id)
    return clientmasters.GetServiceProvidersSuccess(
        service_providers=service_provider_list)

def save_service_provider(db, request, session_user, client_id):
    service_provider_id = db.generate_new_service_provider_id(client_id)
    if db.is_duplicate_service_provider(
        service_provider_id,
        request.service_provider_name, client_id
    ) :
        return clientmasters.ServiceProviderNameAlreadyExists()
    elif db.is_duplicate_service_provider_contact_no(
        service_provider_id,
        request.contact_no, client_id
    ) :
        return clientmasters.ContactNumberAlreadyExists()
    elif db.save_service_provider(
        service_provider_id, request, session_user, client_id
    ) :
        return clientmasters.SaveServiceProviderSuccess()

def update_service_provider(db, request, session_user, client_id):
    if db.is_invalid_id(
        db.tblServiceProviders,
        "service_provider_id",
        request.service_provider_id, client_id
    ):
        return clientmasters.InvalidServiceProviderId()
    elif db.is_duplicate_service_provider(
        request.service_provider_id,
        request.service_provider_name, client_id
    ) :
        return clientmasters.ServiceProviderNameAlreadyExists()
    elif db.is_duplicate_service_provider_contact_no(
        request.service_provider_id,
        request.contact_no, client_id
    ) :
        return clientmasters.ContactNumberAlreadyExists()
    elif db.update_service_provider(request, session_user, client_id) :
        return clientmasters.UpdateServiceProviderSuccess()

def change_service_provider_status(db, request, session_user, client_id):
    is_active = 0 if request.is_active is False else 1
    if db.is_invalid_id(
        db.tblServiceProviders,
        "service_provider_id",
        request.service_provider_id, client_id
    ):
        return clientmasters.InvalidServiceProviderId()
    elif db.update_service_provider_status(
        request.service_provider_id,
        is_active, session_user, client_id
    ):
        return clientmasters.ChangeServiceProviderStatusSuccess()

def get_forms(db, client_id) :
    result_rows = db.get_forms(client_id)
    forms = []
    for row in result_rows:
        parent_menu = None if row[6] == None else row[6]
        form = core.Form(
            form_id=row[0],
            form_name=row[3],
            form_url=row[4],
            parent_menu=parent_menu,
            form_type=row[2]
        )
        forms.append(form)
    return process_user_menus(forms)

def get_user_privilege_details_list(db, client_id):
    user_group_list = []
    rows = db.get_user_privilege_details_list(client_id)
    for row in rows:
        user_group_id = int(row[0])
        user_group_name = row[1]
        form_ids = [int(x) for x in row[2].split(",")]
        is_active = bool(row[3])
        user_group_list.append(
            clientmasters.ClientUserGroup(
                user_group_id,
                user_group_name, form_ids, is_active
            )
        )
    return user_group_list

def get_user_privileges(db, request, session_user, client_id):
    forms = get_forms(db, client_id)
    user_group_list = get_user_privilege_details_list(db, client_id)
    return clientmasters.GetUserPrivilegesSuccess(
        forms=forms,
        user_groups=user_group_list
    )

def save_user_privileges(db, request, session_user, client_id):
    user_group_id = db.generate_new_user_privilege_id(client_id)
    if db.is_duplicate_user_privilege(
        user_group_id,
        request.user_group_name, client_id
    ) :
        return clientmasters.UserGroupNameAlreadyExists()
    elif db.save_user_privilege(
        user_group_id, request, session_user, client_id
    ) :
        return clientmasters.SaveUserPrivilegesSuccess()

def update_user_privileges(db, request, session_user, client_id):
    if db.is_invalid_id(
        db.tblUserGroups, "user_group_id",
        request.user_group_id, client_id
    ):
        return clientmasters.InvalidUserGroupId()
    elif db.is_duplicate_user_privilege(
        request.user_group_id,
        request.user_group_name, client_id
    ) :
        return clientmasters.UserGroupNameAlreadyExists()
    elif db.update_user_privilege(request, session_user, client_id) :
        return clientmasters.UpdateUserPrivilegesSuccess()

def change_user_privilege_status(db, request, session_user, client_id):
    if db.is_invalid_id(
        db.tblUserGroups, "user_group_id",
        request.user_group_id, client_id
    ):
        return clientmasters.InvalidUserGroupId()
    elif db.update_user_privilege_status(
        request.user_group_id, request.is_active,
        session_user, client_id
    ):
        return clientmasters.ChangeUserPrivilegeStatusSuccess()

def get_client_users(db, request, session_user, client_id):
    user_company_info = db.get_user_company_details(
        session_user, client_id
    )
    unit_ids = user_company_info[0]
    division_ids = user_company_info[1]
    legal_entity_ids = user_company_info[2]
    business_group_ids = user_company_info[3]
    country_list = db.get_countries_for_user(session_user, client_id)
    domain_list = db.get_domains_for_user(session_user, client_id)
    business_group_list = db.get_business_groups_for_user(
        business_group_ids
    )
    legal_entity_list = db.get_legal_entities_for_user(
        legal_entity_ids
    )
    division_list = db.get_divisions_for_user(
        division_ids
    )
    unit_list = db.get_units_for_user(unit_ids, client_id)
    user_group_list = db.get_user_privileges(client_id)
    user_list = db.get_user_details(client_id)
    service_provider_list = db.get_service_providers(client_id)
    return clientmasters.GetClientUsersSuccess(
        countries=country_list,
        domains=domain_list,
        business_groups=business_group_list,
        legal_entities=legal_entity_list,
        divisions=division_list,
        units=unit_list,
        user_groups=user_group_list,
        users=user_list,
        service_providers=service_provider_list)

def save_client_user(db, request, session_user, client_id):
    user_id = db.generate_new_user_id(client_id)
    if db.is_duplicate_user_email(user_id, request.email_id, client_id) :
        return clientmasters.EmailIdAlreadyExists()
    elif db.is_duplicate_employee_code(
        user_id,
        request.employee_code, client_id
    ):
        return clientmasters.EmployeeCodeAlreadyExists()
    elif db.is_duplicate_user_contact_no(
        user_id, request.contact_no, client_id
    ):
        return clientmasters.ContactNumberAlreadyExists()
    elif db.save_user(user_id, request, session_user, client_id) :
        return clientmasters.SaveClientUserSuccess()

def update_client_user(db, request, session_user, client_id):
    if db.is_invalid_id(db.tblUsers, "user_id", request.user_id, client_id) :
        return clientmasters.InvalidUserId()
    elif db.is_duplicate_employee_code(
        request.user_id,
        request.employee_code, client_id
    ):
        return clientmasters.EmployeeCodeAlreadyExists()
    elif db.is_duplicate_user_contact_no(
        request.user_id,
        request.contact_no, client_id
    ):
        return clientmasters.ContactNumberAlreadyExists()
    elif db.update_user(request, session_user, client_id) :
        return clientmasters.UpdateClientUserSuccess()

def change_client_user_status(db, request, session_user, client_id):
    if db.is_invalid_id(db.tblUsers, "user_id", request.user_id, client_id) :
        return clientmasters.InvalidUserId()
    elif db.update_user_status(
        request.user_id,
        request.is_active, session_user, client_id
    ):
        return clientmasters.ChangeClientUserStatusSuccess()

def change_admin_status(db, request, session_user, client_id):
    if db.is_invalid_id(db.tblUsers, "user_id", request.user_id, client_id) :
        return clientmasters.InvalidUserId()
    elif db.update_admin_status(
        request.user_id,
        request.is_admin, session_user, client_id
    ):
        return clientmasters.ChangeAdminStatusSuccess()

def get_units(db, request, session_user, client_id):
    user_company_info = db.get_user_company_details(
        session_user, client_id
    )
    unit_ids = user_company_info[0]
    division_ids = user_company_info[1]
    legal_entity_ids = user_company_info[2]
    business_group_ids = user_company_info[3]
    business_group_list = db.get_business_groups_for_user(
        business_group_ids
    )
    legal_entity_list = db.get_legal_entities_for_user(
        legal_entity_ids
    )
    division_list = db.get_divisions_for_user(
        division_ids
    )
    unit_list = db.get_units_closure_for_user(unit_ids)
    return clientmasters.GetUnitsSuccess(
        business_groups=business_group_list,
        legal_entities=legal_entity_list,
        divisions=division_list,
        units=unit_list
    )

def close_unit(db, request, session_user, client_id):
    session_user = session_user
    password = request.password

    if db.verify_password(password, session_user, client_id):
        db.close_unit(request.unit_id, session_user)
        return clientmasters.CloseUnitSuccess()
    else:
        return clientmasters.InvalidPassword()

def get_audit_trails(db, request, session_user, client_id):
    audit_trails = db.get_audit_trails(session_user, client_id)
    return audit_trails
