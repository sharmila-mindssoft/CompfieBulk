from protocol import (clientmasters, core, login)
from server.controller.corecontroller import process_user_menus

__all__ = [
    "process_client_master_requests"
]

########################################################
# To Redirect the requests to the corresponding
# functions
########################################################
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

########################################################
# To get the list of all service providers
########################################################
def get_service_providers(db, request, session_user, client_id):
    service_provider_list = db.get_service_provider_details_list(client_id)
    return clientmasters.GetServiceProvidersSuccess(
        service_providers=service_provider_list)

########################################################
# To validate and Save service provider
########################################################
def save_service_provider(db, request, session_user, client_id):
    service_provider_id = db.generate_new_service_provider_id(client_id)
    if db.is_duplicate_service_provider(
        service_provider_id,
        request.service_provider_name, client_id
    ) :
        return clientmasters.ServiceProviderNameAlreadyExists()
    elif db.save_service_provider(
        service_provider_id, request, session_user, client_id
    ) :
        return clientmasters.SaveServiceProviderSuccess()


########################################################
# To validate and Update service provider
########################################################
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
    elif db.update_service_provider(request, session_user, client_id) :
        return clientmasters.UpdateServiceProviderSuccess()

########################################################
# To validate and change the status of service provider
########################################################
def change_service_provider_status(db, request, session_user, client_id):
    is_active = 0 if request.is_active is False else 1
    if db.is_invalid_id(
        db.tblServiceProviders,
        "service_provider_id",
        request.service_provider_id, client_id
    ):
        return clientmasters.InvalidServiceProviderId()
    elif not db.is_service_provider_in_contract(request.service_provider_id):
        return clientmasters.CannotChangeStatusOfContractExpiredSP()
    elif db.is_user_exists_under_service_provider(
        request.service_provider_id
    ):
        return clientmasters.CannotDeactivateUserExists()
    elif db.update_service_provider_status(
        request.service_provider_id,
        is_active, session_user, client_id
    ):
        return clientmasters.ChangeServiceProviderStatusSuccess()

########################################################
# To get all client forms to load in User privilege form
########################################################
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

########################################################
# To get all user groups with details
########################################################
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

########################################################
# To get all user groups list
########################################################
def get_user_privileges(db, request, session_user, client_id):
    forms = get_forms(db, client_id)
    user_group_list = get_user_privilege_details_list(db, client_id)
    return clientmasters.GetUserPrivilegesSuccess(
        forms=forms,
        user_groups=user_group_list
    )

########################################################
# To save User privileges
########################################################
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

########################################################
# To update user privileges
########################################################
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

########################################################
# To change the status of user privilege
########################################################
def change_user_privilege_status(db, request, session_user, client_id):
    if db.is_invalid_id(
        db.tblUserGroups, "user_group_id",
        request.user_group_id, client_id
    ):
        return clientmasters.InvalidUserGroupId()
    elif db.is_user_exists_under_user_group(
        request.user_group_id
    ):
        return clientmasters.CannotDeactivateUserExists()
    elif db.update_user_privilege_status(
        request.user_group_id, request.is_active,
        session_user, client_id
    ):
        return clientmasters.ChangeUserPrivilegeStatusSuccess()

########################################################
# To get the list of all users with details
########################################################
def get_client_users(db, request, session_user, client_id):
    user_company_info = db.get_user_company_details(
        session_user, client_id
    )
    unit_ids = user_company_info[0]
    division_ids = user_company_info[1]
    legal_entity_ids = user_company_info[2]
    business_group_ids = user_company_info[3]
    user_country_list = db.get_countries_for_user(session_user, client_id)
    user_domain_list = db.get_domains_for_user(session_user, client_id)
    country_list = db.get_countries()
    domain_list = db.get_domains()
    business_group_list = db.get_business_groups_for_user(
        business_group_ids
    )
    legal_entity_list = db.get_legal_entities_for_user(
        legal_entity_ids
    )
    division_list = db.get_divisions_for_user(
        division_ids
    )
    unit_list = db.get_units_for_user(None)
    session_user_unit_list = db.get_units_for_user(unit_ids)
    user_group_list = db.get_user_privileges(client_id)
    user_list = db.get_user_details(client_id, session_user)
    service_provider_list = db.get_service_providers(client_id)
    remaining_licence = db.get_no_of_remaining_licence()
    is_primary_admin = True if session_user == 0 else db.is_primary_admin(session_user)
    return clientmasters.GetClientUsersSuccess(
        user_countries=user_country_list,
        user_domains=user_domain_list,
        countries=country_list,
        domains=domain_list,
        business_groups=business_group_list,
        legal_entities=legal_entity_list,
        divisions=division_list,
        units=unit_list,
        session_user_units=session_user_unit_list,
        user_groups=user_group_list,
        users=user_list,
        service_providers=service_provider_list,
        remaining_licence=remaining_licence,
        is_primary_admin=is_primary_admin
    )

########################################################
# To validate and save a user
########################################################
def save_client_user(db, request, session_user, client_id):
    user_id = db.generate_new_user_id(client_id)
    if (db.get_no_of_remaining_licence() <= 0):
        return clientmasters.UserLimitExceeds()
    elif db.is_duplicate_user_email(user_id, request.email_id, client_id) :
        return clientmasters.EmailIdAlreadyExists()
    elif db.is_duplicate_employee_code(
        user_id,
        request.employee_code.replace(" ",""), client_id
    ):
        return clientmasters.EmployeeCodeAlreadyExists()
    elif db.save_user(user_id, request, session_user, client_id) :
        return clientmasters.SaveClientUserSuccess()

########################################################
# To validate and update user
########################################################
def update_client_user(db, request, session_user, client_id):
    if db.is_invalid_id(db.tblUsers, "user_id", request.user_id, client_id) :
        return clientmasters.InvalidUserId()
    elif db.is_duplicate_employee_code(
        request.user_id,
        request.employee_code.replace(" ",""), client_id
    ):
        return clientmasters.EmployeeCodeAlreadyExists()
    elif db.update_user(request, session_user, client_id) :
        return clientmasters.UpdateClientUserSuccess()

########################################################
# To change the status of a user
########################################################
def change_client_user_status(db, request, session_user, client_id):
    if db.is_invalid_id(db.tblUsers, "user_id", request.user_id, client_id) :
        return clientmasters.InvalidUserId()
    elif db.is_primary_admin(request.user_id):
        return clientmasters.CannotChangePrimaryAdminStatus()
    elif db.have_compliances(request.user_id) and request.is_active in [False, 0]:
        return clientmasters.ReassignCompliancesBeforeDeactivate()
    elif db.update_user_status(
        request.user_id,
        request.is_active, session_user, client_id
    ):
        return clientmasters.ChangeClientUserStatusSuccess()

########################################################
# To promote or demote a user from promoted admin status
########################################################
def change_admin_status(db, request, session_user, client_id):
    if db.is_invalid_id(db.tblUsers, "user_id", request.user_id, client_id) :
        return clientmasters.InvalidUserId()
    elif db.is_primary_admin(request.user_id):
        return clientmasters.CannotChangePrimaryAdminStatus()
    elif db.is_service_proivder_user(request.user_id):
        return clientmasters.CannotPromoteServiceProvider()
    elif db.update_admin_status(
        request.user_id,
        request.is_admin, session_user, client_id
    ):
        return clientmasters.ChangeAdminStatusSuccess()

########################################################
# To get all the units under the given client
########################################################
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

########################################################
# To close a unit
########################################################
def close_unit(db, request, session_user, client_id):
    session_user = session_user
    password = request.password
    if db.is_seating_unit(request.unit_id):
        return clientmasters.CannotCloseUnit()
    elif db.verify_password(password, session_user, client_id):
        db.close_unit(request.unit_id, session_user)
        return clientmasters.CloseUnitSuccess()
    else:
        return clientmasters.InvalidPassword()

########################################################
# To get audit trails related to the given user
########################################################
def get_audit_trails(db, request, session_user, client_id):
    audit_trails = db.get_audit_trails(session_user, client_id)
    return audit_trails
