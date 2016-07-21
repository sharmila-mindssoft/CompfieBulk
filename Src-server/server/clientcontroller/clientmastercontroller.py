import time
from protocol import (clientmasters, core, login)
from server.controller.corecontroller import process_user_menus
from server.constants import RECORD_DISPLAY_COUNT
from server import logger
from server.clientdatabase.clientmaster import *
from server.clientdatabase.general import (
    get_domains_for_user,
    get_countries_for_user, get_countries, get_domains,
    get_business_groups_for_user, get_legal_entities_for_user,
    get_divisions_for_user, get_units_for_user, have_compliances,
    is_seating_unit
    )
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
    session_user = db.validate_session_token(session_token)
    if session_user is None:
        return login.InvalidSessionToken()

    if type(request) is clientmasters.GetServiceProviders:
        logger.logClientApi("GetServiceProviders - " + str(client_id), "process begin")
        logger.logClientApi("------", str(time.time()))
        result = process_get_service_providers(db, request, session_user, client_id)
        logger.logClientApi("GetServiceProviders", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientmasters.SaveServiceProvider:
        logger.logClientApi("SaveServiceProvider - " + str(client_id), "process begin")
        logger.logClientApi("------", str(time.time()))
        result = process_save_service_provider(db, request, session_user, client_id)
        logger.logClientApi("SaveServiceProvider", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientmasters.UpdateServiceProvider:
        logger.logClientApi("UpdateServiceProvider - " + str(client_id), "process begin")
        logger.logClientApi("------", str(time.time()))
        result = process_update_service_provider(db, request, session_user, client_id)
        logger.logClientApi("UpdateServiceProvider", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientmasters.ChangeServiceProviderStatus:
        logger.logClientApi("ChangeServiceProviderStatus - " + str(client_id), "process begin")
        logger.logClientApi("------", str(time.time()))
        result = process_change_service_provider_status(
            db, request, session_user, client_id
        )
        logger.logClientApi("ChangeServiceProviderStatus", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientmasters.GetUserPrivileges:
        logger.logClientApi("GetUserPrivileges - " + str(client_id), "process begin")
        logger.logClientApi("------", str(time.time()))
        result = process_get_user_privileges(db, request, session_user, client_id)
        logger.logClientApi("GetUserPrivileges", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientmasters.SaveUserPrivileges:
        logger.logClientApi("SaveUserPrivileges - " + str(client_id), "process begin")
        logger.logClientApi("------", str(time.time()))
        result = process_save_user_privileges(db, request, session_user, client_id)
        logger.logClientApi("SaveUserPrivileges", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientmasters.UpdateUserPrivileges:
        logger.logClientApi("UpdateUserPrivileges - " + str(client_id), "process begin")
        logger.logClientApi("------", str(time.time()))
        result = process_update_user_privileges(db, request, session_user, client_id)
        logger.logClientApi("UpdateUserPrivileges", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientmasters.ChangeUserPrivilegeStatus:
        logger.logClientApi("ChangeUserPrivilegeStatus - " + str(client_id), "process begin")
        logger.logClientApi("------", str(time.time()))
        result = process_change_user_privilege_status(
            db, request, session_user, client_id
        )
        logger.logClientApi("ChangeUserPrivilegeStatus", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientmasters.GetClientUsers:
        logger.logClientApi("GetClientUsers - " + str(client_id), "process begin")
        logger.logClientApi("------", str(time.time()))
        result = process_get_client_users(db, request, session_user, client_id)
        logger.logClientApi("GetClientUsers", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientmasters.SaveClientUser:
        logger.logClientApi("SaveClientUser - " + str(client_id), "process begin")
        logger.logClientApi("------", str(time.time()))
        result = process_save_client_user(db, request, session_user, client_id)
        logger.logClientApi("SaveClientUser", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientmasters.UpdateClientUser:
        logger.logClientApi("UpdateClientUser - " + str(client_id), "process begin")
        logger.logClientApi("------", str(time.time()))
        result = process_update_client_user(db, request, session_user, client_id)
        logger.logClientApi("UpdateClientUser", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientmasters.ChangeClientUserStatus:
        logger.logClientApi("ChangeClientUserStatus - " + str(client_id), "process begin")
        logger.logClientApi("------", str(time.time()))
        result = process_change_client_user_status(db, request, session_user, client_id)
        logger.logClientApi("ChangeClientUserStatus", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientmasters.ChangeAdminStatus:
        logger.logClientApi("ChangeAdminStatus - " + str(client_id), "process begin")
        logger.logClientApi("------", str(time.time()))
        result = process_change_admin_status(db, request, session_user, client_id)
        logger.logClientApi("ChangeAdminStatus", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientmasters.GetUnits:
        logger.logClientApi("GetUnits - " + str(client_id), "process begin")
        logger.logClientApi("------", str(time.time()))
        result = process_get_units(db, request, session_user, client_id)
        logger.logClientApi("GetUnits", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientmasters.CloseUnit:
        logger.logClientApi("CloseUnit - " + str(client_id), "process begin")
        logger.logClientApi("------", str(time.time()))
        result = process_close_unit(db, request, session_user, client_id)
        logger.logClientApi("CloseUnit", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientmasters.GetAuditTrails:
        logger.logClientApi("GetAuditTrails - " + str(client_id), "process begin")
        logger.logClientApi("------", str(time.time()))
        result = process_get_audit_trails(db, request, session_user, client_id)
        logger.logClientApi("GetAuditTrails", "process end")
        logger.logClientApi("------", str(time.time()))

    return result

########################################################
# To get the list of all service providers
########################################################
def process_get_service_providers(db, request, session_user, client_id):
    service_provider_list = get_service_provider_details_list(db, client_id)
    return clientmasters.GetServiceProvidersSuccess(
        service_providers=service_provider_list)

########################################################
# To validate and Save service provider
########################################################
def process_save_service_provider(db, request, session_user, client_id):
    service_provider_id = generate_new_service_provider_id(db, client_id)
    if is_duplicate_service_provider(db,
        service_provider_id,
        request.service_provider_name, client_id
    ) :
        return clientmasters.ServiceProviderNameAlreadyExists()
    elif save_service_provider(db, 
        service_provider_id, request, session_user, client_id
    ) :
        return clientmasters.SaveServiceProviderSuccess()


########################################################
# To validate and Update service provider
########################################################
def process_update_service_provider(db, request, session_user, client_id):
    if db.is_invalid_id(
        tblServiceProviders,
        "service_provider_id",
        request.service_provider_id, client_id
    ):
        return clientmasters.InvalidServiceProviderId()
    elif is_duplicate_service_provider(db, 
        request.service_provider_id,
        request.service_provider_name, client_id
    ) :
        return clientmasters.ServiceProviderNameAlreadyExists()
    elif update_service_provider(db, request, session_user, client_id) :
        return clientmasters.UpdateServiceProviderSuccess()

########################################################
# To validate and change the status of service provider
########################################################
def process_change_service_provider_status(db, request, session_user, client_id):
    is_active = 0 if request.is_active is False else 1
    if db.is_invalid_id(
        tblServiceProviders,
        "service_provider_id",
        request.service_provider_id, client_id
    ):
        return clientmasters.InvalidServiceProviderId()
    elif not is_service_provider_in_contract(db, request.service_provider_id):
        return clientmasters.CannotChangeStatusOfContractExpiredSP()
    elif is_user_exists_under_service_provider(db, 
        request.service_provider_id
    ):
        return clientmasters.CannotDeactivateUserExists()
    elif update_service_provider_status(db, 
        request.service_provider_id,
        is_active, session_user, client_id
    ):
        return clientmasters.ChangeServiceProviderStatusSuccess()

########################################################
# To get all client forms to load in User privilege form
########################################################
def process_get_forms(db, client_id) :
    result_rows = get_forms(db, client_id)
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
def process_get_user_privilege_details_list(db, client_id):
    user_group_list = []
    rows = get_user_privilege_details_list(db, client_id)
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
def process_get_user_privileges(db, request, session_user, client_id):
    forms = process_get_forms(db, client_id)
    user_group_list = process_get_user_privilege_details_list(db, client_id)
    return clientmasters.GetUserPrivilegesSuccess(
        forms=forms,
        user_groups=user_group_list
    )

########################################################
# To save User privileges
########################################################
def process_save_user_privileges(db, request, session_user, client_id):
    user_group_id = generate_new_user_privilege_id(db, client_id)
    if is_duplicate_user_privilege(db, 
        user_group_id,
        request.user_group_name, client_id
    ) :
        return clientmasters.UserGroupNameAlreadyExists()
    elif save_user_privilege(db, 
        user_group_id, request, session_user, client_id
    ) :
        return clientmasters.SaveUserPrivilegesSuccess()

########################################################
# To update user privileges
########################################################
def process_update_user_privileges(db, request, session_user, client_id):
    if db.is_invalid_id(
        tblUserGroups, "user_group_id",
        request.user_group_id, client_id
    ):
        return clientmasters.InvalidUserGroupId()
    elif is_duplicate_user_privilege(db, 
        request.user_group_id,
        request.user_group_name, client_id
    ) :
        return clientmasters.UserGroupNameAlreadyExists()
    elif update_user_privilege(db, request, session_user, client_id) :
        return clientmasters.UpdateUserPrivilegesSuccess()

########################################################
# To change the status of user privilege
########################################################
def process_change_user_privilege_status(db, request, session_user, client_id):
    if db.is_invalid_id(
        tblUserGroups, "user_group_id",
        request.user_group_id, client_id
    ):
        return clientmasters.InvalidUserGroupId()
    elif is_user_exists_under_user_group(db, 
        request.user_group_id
    ):
        return clientmasters.CannotDeactivateUserExists()
    elif update_user_privilege_status(db, 
        request.user_group_id, request.is_active,
        session_user, client_id
    ):
        return clientmasters.ChangeUserPrivilegeStatusSuccess()

########################################################
# To get the list of all users with details
########################################################
def process_get_client_users(db, request, session_user, client_id):
    user_company_info = get_user_company_details(db,
        session_user, client_id
    )
    #import from general.py
    unit_ids = user_company_info[0]
    division_ids = user_company_info[1]
    legal_entity_ids = user_company_info[2]
    business_group_ids = user_company_info[3]
    user_country_list = get_countries_for_user(db, session_user, client_id)
    user_domain_list = get_domains_for_user(db, session_user, client_id)
    country_list = get_countries(db)
    domain_list = get_domains(db)
    business_group_list = get_business_groups_for_user(db, 
        business_group_ids
    )
    legal_entity_list = get_legal_entities_for_user(db, 
        legal_entity_ids
    )
    division_list = get_divisions_for_user(db,
        division_ids
    )
    unit_list = get_units_for_user(db, None)
    session_user_unit_list = get_units_for_user(db, unit_ids)
    user_group_list = get_user_privileges(db, client_id)
    user_list = get_user_details(db, client_id, session_user)
    service_provider_list = get_service_providers(db, client_id)
    remaining_licence = get_no_of_remaining_licence(db)
    is_primary_admin = True if session_user == 0 else is_primary_admin(db, session_user)
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
def process_save_client_user(db, request, session_user, client_id):
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
def process_update_client_user(db, request, session_user, client_id):
    if db.is_invalid_id(tblUsers, "user_id", request.user_id, client_id) :
        return clientmasters.InvalidUserId()
    elif is_duplicate_employee_code(db, 
        request.user_id,
        request.employee_code.replace(" ",""), client_id
    ):
        return clientmasters.EmployeeCodeAlreadyExists()
    elif update_user(db, request, session_user, client_id) :
        return clientmasters.UpdateClientUserSuccess()

########################################################
# To change the status of a user
########################################################
def process_change_client_user_status(db, request, session_user, client_id):
    if db.is_invalid_id(tblUsers, "user_id", request.user_id, client_id) :
        return clientmasters.InvalidUserId()
    elif is_primary_admin(db, request.user_id):
        return clientmasters.CannotChangePrimaryAdminStatus()
    elif have_compliances(db, request.user_id) and request.is_active in [False, 0]:
        return clientmasters.ReassignCompliancesBeforeDeactivate()
    elif update_user_status(db, 
        request.user_id,
        request.is_active, session_user, client_id
    ):
        return clientmasters.ChangeClientUserStatusSuccess()

########################################################
# To promote or demote a user from promoted admin status
########################################################
def process_change_admin_status(db, request, session_user, client_id):
    if db.is_invalid_id(tblUsers, "user_id", request.user_id, client_id) :
        return clientmasters.InvalidUserId()
    elif is_primary_admin(db, request.user_id):
        return clientmasters.CannotChangePrimaryAdminStatus()
    elif is_service_proivder_user(db, request.user_id):
        return clientmasters.CannotPromoteServiceProvider()
    elif update_admin_status(db, 
        request.user_id,
        request.is_admin, session_user, client_id
    ):
        return clientmasters.ChangeAdminStatusSuccess()

########################################################
# To get all the units under the given client
########################################################
def process_get_units(db, request, session_user, client_id):
    user_company_info = get_user_company_details(db, 
        session_user, client_id
    )
    unit_ids = user_company_info[0]
    division_ids = user_company_info[1]
    legal_entity_ids = user_company_info[2]
    business_group_ids = user_company_info[3]
    #import from general.py
    business_group_list = get_business_groups_for_user(
        db, business_group_ids
    )
    legal_entity_list = get_legal_entities_for_user(
        db, legal_entity_ids
    )
    division_list = get_divisions_for_user(
        db, division_ids
    )
    unit_list = get_units_closure_for_user(db, unit_ids)
    return clientmasters.GetUnitsSuccess(
        business_groups=business_group_list,
        legal_entities=legal_entity_list,
        divisions=division_list,
        units=unit_list
    )

########################################################
# To close a unit
########################################################
def process_close_unit(db, request, session_user, client_id):
    session_user = session_user
    password = request.password
    #import from general.py
    if verify_password(db, password, session_user, client_id):
        if is_seating_unit(db, request.unit_id):
            return clientmasters.CannotCloseUnit()
        else:
            close_unit(db, request.unit_id, session_user)
            return clientmasters.CloseUnitSuccess()
    else:
        return clientmasters.InvalidPassword()

########################################################
# To get audit trails related to the given user
########################################################
def process_get_audit_trails(db, request, session_user, client_id):
    from_count = request.record_count
    to_count = RECORD_DISPLAY_COUNT
    from_date = request.from_date
    to_date = request.to_date
    user_id = request.user_id
    form_id = request.form_id
    audit_trails = get_audit_trails(
        db, session_user, client_id, from_count, to_count,
        from_date, to_date, user_id, form_id
    )
    return audit_trails
