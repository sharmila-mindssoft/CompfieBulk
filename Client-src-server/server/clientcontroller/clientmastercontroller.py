import collections
from clientprotocol import (clientmasters, clientcore)
from server.clientdatabase.tables import *
from server.clientdatabase.clientmaster import *
from server.clientdatabase.general import (
    get_domains_for_user, verify_password,
    get_countries_for_user, get_countries, get_domains,
    get_business_groups_for_user, get_legal_entities_for_user,
    get_divisions_for_user, get_units_for_user, have_compliances,
    is_seating_unit, get_user_company_details, is_primary_admin,
    is_service_proivder_user, is_old_primary_admin
    )
__all__ = [
    "process_client_master_requests"
]

########################################################
# To Redirect the requests to the corresponding
# functions
########################################################
def process_client_master_requests(request, db, session_user, client_id):
    request = request.request

    if type(request) is clientmasters.GetServiceProviders:
        result = process_get_service_providers(
            db, request, session_user
        )

    elif type(request) is clientmasters.SaveServiceProvider:
        result = process_save_service_provider(
            db, request, session_user
        )

    elif type(request) is clientmasters.UpdateServiceProvider:
        result = process_update_service_provider(
            db, request, session_user
        )

    elif type(request) is clientmasters.ChangeServiceProviderStatus:
        result = process_change_service_provider_status(
            db, request, session_user
        )

    elif type(request) is clientmasters.GetUserPrivileges:
        result = process_get_user_privileges(
            db, request, session_user
        )

    elif type(request) is clientmasters.SaveUserPrivileges:
        result = process_save_user_privileges(
            db, request, session_user
        )

    elif type(request) is clientmasters.UpdateUserPrivileges:
        result = process_update_user_privileges(
            db, request, session_user
        )

    elif type(request) is clientmasters.ChangeUserPrivilegeStatus:
        result = process_change_user_privilege_status(
            db, request, session_user
        )

    elif type(request) is clientmasters.GetClientUsers:
        result = process_get_client_users(db, request, session_user)

    elif type(request) is clientmasters.SaveClientUser:
        result = process_save_client_user(db, request, session_user, client_id)

    elif type(request) is clientmasters.UpdateClientUser:
        result = process_update_client_user(
            db, request, session_user, client_id
        )

    elif type(request) is clientmasters.ChangeClientUserStatus:
        result = process_change_client_user_status(
            db, request, session_user, client_id
        )

    elif type(request) is clientmasters.ChangeAdminStatus:
        result = process_change_admin_status(
            db, request, session_user
        )

    elif type(request) is clientmasters.GetUnits:
        result = process_get_units(db, request, session_user)

    elif type(request) is clientmasters.CloseUnit:
        result = process_close_unit(db, request, session_user)

    elif type(request) is clientmasters.GetAuditTrails:
        result = process_get_audit_trails(db, request, session_user)

    elif type(request) is clientmasters.GetUnitClosureData:
        result = process_get_unit_closure_data(db, request, session_user)

    elif type(request) is clientmasters.GetUnitClosureUnitData:
        result = process_get_unit_closure_unit_data(db, request, session_user)

    elif type(request) is clientmasters.SaveUnitClosureData:
        result = process_save_unit_closure_unit_data(db, request, session_user)

    elif type(request) is clientmasters.UserManagementPrerequisite:
        result = process_UserManagementAddPrerequisite(db, request, session_user)

    return result

########################################################
# To get the list of all service providers
########################################################
def process_get_service_providers(db, request, session_user):
    service_provider_list = get_service_provider_details_list(db)
    return clientmasters.GetServiceProvidersSuccess(
        service_providers=service_provider_list)


########################################################
# To validate and Save service provider
########################################################
def process_save_service_provider(db, request, session_user):
    # create fail class for false res status
    service_provider_id = None
    if is_duplicate_service_provider(db, service_provider_id,
                                     request.service_provider_name, request.short_name):
        return clientmasters.ServiceProviderNameAlreadyExists()
    res = save_service_provider(db, request, session_user)
    if(res):
        return clientmasters.SaveServiceProviderSuccess()


########################################################
# To validate and Update service provider
########################################################
def process_update_service_provider(db, request, session_user):
    if db.is_invalid_id(
        tblServiceProviders,
        "service_provider_id",
        request.service_provider_id
    ):
        return clientmasters.InvalidServiceProviderId()
    elif is_duplicate_service_provider(
        db,
        request.service_provider_id,
        request.service_provider_name
    ):
        return clientmasters.ServiceProviderNameAlreadyExists()
    elif update_service_provider(db, request, session_user):
        return clientmasters.UpdateServiceProviderSuccess()


########################################################
# To validate and change the status of service provider
########################################################
def process_change_service_provider_status(
    db, request, session_user
):
    is_active = 0 if request.is_active is False else 1
    if db.is_invalid_id(
        tblServiceProviders,
        "service_provider_id",
        request.service_provider_id
    ):
        return clientmasters.InvalidServiceProviderId()
    # elif is_service_provider_in_contract(
    #     db, request.service_provider_id
    # ) is False:
    #     return clientmasters.CannotChangeStatusOfContractExpiredSP()
    elif is_user_exists_under_service_provider(
        db, request.service_provider_id
    ):
        return clientmasters.CannotDeactivateUserExists()
    elif update_service_provider_status(
        db,
        request.service_provider_id,
        is_active, session_user
    ):
        return clientmasters.ChangeServiceProviderStatusSuccess() 

########################################################
# User Management Add Prerequisite
########################################################
def process_UserManagementAddPrerequisite(db, request, session_user):
    userCategory = {}
    userGroup = {}
    businessGroup = {}
    legalEntity = {}
    groupCategory = {}
    groupDivision = {}
    legalDomains = {}
    legalUnits = {}

    userCategory = process_UserManagement_category(db)
    userGroup = process_UserManagement_UserGroup(db)
    businessGroup = process_UserManagement_BusinessGroup(db)
    legalEntity = process_UserManagement_LegalEntity(db)
    groupDivision = process_UserManagement_GroupDivision(db)
    groupCategory = process_UserManagement_GroupCategory(db)
    legalDomains = process_UserManagement_LegalDomains(db)
    legalUnits = process_UserManagement_LegalUnits(db)

    return clientmasters.GetUserManagementPrerequisiteSuccess(
        user_category=userCategory,
        user_group=userGroup,
        business_group=businessGroup,
        legal_entity=legalEntity,
        group_division=groupDivision,
        group_category=groupCategory,
        legal_Domains=legalDomains,
        legal_units=legalUnits
    )

########################################################
# To get all client forms to load in User privilege form
########################################################
def process_get_forms(db, cat_id):
    result_rows = get_forms(db, cat_id)
    forms = []
    for row in result_rows:
        parent_menu = None if (
            row["parent_menu"] == None) else row["parent_menu"]
        form = clientcore.Form(
            form_id=row["form_id"],
            form_name=row["form_name"],
            form_url=row["form_url"],
            parent_menu=parent_menu,
            form_type=row["form_type"]
        )
        forms.append(form)
    return process_user_menus(forms)


########################################################
# User Management - Load User Category
########################################################
def process_UserManagement_category(db):
    resultRows = userManagement_GetUserCategory(db)
    userCategoryList = []
    for row in resultRows:
        userCategoryId = int(row["user_category_id"])
        userCategoryName = row["user_category_name"]
        userCategoryList.append(
            clientcore.ClientUsercategory_UserManagement(userCategoryId, userCategoryName)
        )
    return userCategoryList

########################################################
# User Management - Load User Group
########################################################
def process_UserManagement_UserGroup(db):
    resultRows = userManagement_GetUserGroup(db)
    userGroupList = []
    for row in resultRows:
        userGroupId = int(row["user_group_id"])
        userGroupName = row["user_group_name"]
        userCategoryId = int(row["user_category_id"])
        userGroupList.append(
            clientcore.ClientUserGroup_UserManagement(userGroupId, userGroupName, userCategoryId)
        )
    return userGroupList
########################################################
# User Management - Load Business Group
########################################################
def process_UserManagement_BusinessGroup(db):
    resultRows = userManagement_GetBusinessGroup(db)
    businessGroupList = []
    for row in resultRows:
        businessGroupId = row["business_group_id"]
        businessGroupName = row["business_group_name"]
        businessGroupList.append(
            clientcore.ClientUserBusinessGroup_UserManagement(businessGroupId, businessGroupName)
        )
    return businessGroupList
########################################################
# User Management - Load Legal Entity
########################################################
def process_UserManagement_LegalEntity(db):
    resultRows = userManagement_GetLegalEntity(db)
    legalEntityList = []
    for row in resultRows:
        legalEntityId = int(row["legal_entity_id"])
        businessGroupId = row["business_group_id"]
        legalEntityName = row["legal_entity_name"]
        legalEntityList.append(
            clientcore.ClientUserLegalEntity_UserManagement(legalEntityId,
                                                            businessGroupId, legalEntityName)
        )
    return legalEntityList
########################################################
# User Management - Load Group Division
########################################################
def process_UserManagement_GroupDivision(db):
    resultRows = userManagement_GetDivision(db)
    divisionList = []
    for row in resultRows:
        divisionId = row["division_id"]
        divisionName = row["division_name"]
        legalEntityId = row["legal_entity_id"]
        businessGroupId = row["business_group_id"]
        divisionList.append(
            clientcore.ClientUserDivision_UserManagement(divisionId, divisionName,
                                                         legalEntityId, businessGroupId)
        )
    return divisionList

########################################################
# User Management - Load Group Category
########################################################
def process_UserManagement_GroupCategory(db):
    resultRows = userManagement_GetGroupCategory(db)
    categoryList = []
    for row in resultRows:
        categoryId = row["category_id"]
        categoryName = row["category_name"]
        legalEntityId = row["legal_entity_id"]
        businessGroupId = row["business_group_id"]
        divisionId = row["division_id"]
        categoryList.append(
            clientcore.ClientGroupCategory_UserManagement(categoryId, categoryName,
                                                          legalEntityId, businessGroupId, divisionId)
        )
    return categoryList

########################################################
# User Management - Load Legal Entity Domains
########################################################
def process_UserManagement_LegalDomains(db):
    resultRows = userManagement_GetLegalEntity_Domain(db)
    domainList = []
    for row in resultRows:
        legalEntityId = row["legal_entity_id"]
        domain_id = row["domain_id"]
        domain_name = row["domain_name"]
        domainList.append(
            clientcore.ClientLegalDomains_UserManagement(legalEntityId, domain_id, domain_name)
        )
    return domainList
########################################################
# User Management - Load Legal Entity Units
########################################################
def process_UserManagement_LegalUnits(db):
    resultRows = userManagement_GetLegalEntity_Units(db)
    unitList = []
    for row in resultRows:
        unit_id = row["unit_id"]
        business_group_id = row["business_group_id"]
        legal_entity_id = row["legal_entity_id"]
        division_id = row["division_id"]
        category_id = row["category_id"]
        unit_code = row["unit_code"]
        unit_name = row["unit_name"]
        address = row["address"]
        postal_code = str(row["postal_code"])
        unitList.append(
            clientcore.ClientLegalUnits_UserManagement(unit_id, business_group_id, legal_entity_id,
                                                       division_id, category_id, unit_code,
                                                       unit_name, address, postal_code)
        )
    return unitList
    
########################################################
# To get all user groups with details
########################################################
def process_get_user_privilege_details_list(db):
    user_group_list = get_user_privilege_details_list(db)

    #print user_group_list
    return user_group_list


########################################################
# To get all user groups list
########################################################
def process_get_user_privileges(db, request, session_user):
    # call form category
    # loop user category
    # process_get_forms --> process_get_menus -- > append to dictionary key
    form_category = {}
    user_category = {}
    for cat_id in [2, 3, 4, 5, 6] :
        category_wise_forms = process_get_forms(db, cat_id)
        form_category[cat_id] = category_wise_forms
    user_category = process_get_user_category(db)
    user_group_list = process_get_user_privilege_details_list(db)
    return clientmasters.GetUserPrivilegesSuccess(
        forms=form_category,
        user_groups=user_group_list,
        user_category=user_category
    )


########################################################
# To save User privileges
########################################################
def process_save_user_privileges(db, request, session_user):
    if is_duplicate_user_privilege(
        db, request.user_category_id, request.user_group_name
    ):
        return clientmasters.UserGroupNameAlreadyExists()
    user_group_id = save_user_privilege(
        db, request, session_user
    )
    if(user_group_id):
        return clientmasters.SaveUserPrivilegesSuccess()


########################################################
# To update user privileges
########################################################
def process_update_user_privileges(db, request, session_user):
    if db.is_invalid_id(
        tblUserGroups, "user_group_id", request.user_group_id
    ):
        return clientmasters.InvalidUserGroupId()
    elif is_duplicate_user_privilege(
        db, request.user_category_id, request.user_group_name
    ):
        return clientmasters.UserGroupNameAlreadyExists()
    elif update_user_privilege(db, request, session_user):
        return clientmasters.UpdateUserPrivilegesSuccess()


########################################################
# To change the status of user privilege
########################################################
def process_change_user_privilege_status(db, request, session_user):
    if db.is_invalid_id(
        tblUserGroups, "user_group_id", request.user_group_id
    ):
        return clientmasters.InvalidUserGroupId()
    elif is_user_exists_under_user_group(
        db, request.user_group_id
    ):
        return clientmasters.CannotDeactivateUserExists()
    elif update_user_privilege_status(
        db, request.user_group_id, request.is_active, session_user
    ):
        return clientmasters.ChangeUserPrivilegeStatusSuccess()


########################################################
# To get the list of all users with details
########################################################
def process_get_client_users(db, request, session_user):
    user_company_info = get_user_company_details(
        db, session_user
    )
    unit_ids = user_company_info[0]
    division_ids = user_company_info[1]
    legal_entity_ids = user_company_info[2]
    business_group_ids = user_company_info[3]
    user_country_list = get_countries_for_user(db, session_user)
    user_domain_list = get_domains_for_user(db, session_user)
    country_list = get_countries(db)
    domain_list = get_domains(db)
    business_group_list = get_business_groups_for_user(
        db,
        business_group_ids
    )
    legal_entity_list = get_legal_entities_for_user(
        db,
        legal_entity_ids
    )
    division_list = get_divisions_for_user(
        db,
        division_ids
    )
    unit_list = get_units_for_user(db, None)
    session_user_unit_list = get_units_for_user(db, unit_ids)
    user_group_list = get_user_privileges(db)
    user_list = get_user_details(db)
    service_provider_list = get_service_providers(db)
    remaining_licence = get_no_of_remaining_licence(db)
    is_primary_user = is_primary_admin(db, session_user)
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
        is_primary_admin=is_primary_user
    )


########################################################
# To validate and save a user
########################################################
def process_save_client_user(db, request, session_user, client_id):
    # user_id = db.get_new_id("user_id", tblUsers)
    # if (get_no_of_remaining_licence(db) <= 0):
    #     return clientmasters.UserLimitExceeds()
    # elif is_duplicate_employee_code(
    #     db,
    #     request.employee_code.replace(" ", ""),
    #     user_id=None
    # ):
    #     return clientmasters.EmployeeCodeAlreadyExists()
    if save_user(db, request, session_user, client_id):        
        return clientmasters.SaveClientUserSuccess()

########################################################
# To validate and update user
########################################################
def process_update_client_user(db, request, session_user, client_id):
    if db.is_invalid_id(tblUsers, "user_id", request.user_id):
        return clientmasters.InvalidUserId()
    elif is_duplicate_employee_code(
        db,
        request.user_id,
        request.employee_code.replace(" ", "")
    ):
        return clientmasters.EmployeeCodeAlreadyExists()
    elif is_duplicate_employee_name(
        db, request.employee_name, user_id=request.user_id
    ):
        return clientmasters.EmployeeNameAlreadyExists()
    elif update_user(db, request, session_user, client_id):
        return clientmasters.UpdateClientUserSuccess()


########################################################
# To change the status of a user
########################################################
def process_change_client_user_status(db, request, session_user, client_id):
    if db.is_invalid_id(tblUsers, "user_id", request.user_id):
        return clientmasters.InvalidUserId()
    elif is_old_primary_admin(db, request.user_id):
        return clientmasters.CannotChangeOldPrimaryAdminStatus()
    elif is_primary_admin(db, request.user_id):
        return clientmasters.CannotChangePrimaryAdminStatus()
    elif have_compliances(
            db, request.user_id) and request.is_active in [False, 0]:
        return clientmasters.ReassignCompliancesBeforeDeactivate()
    elif update_user_status(
        db,
        request.user_id,
        request.is_active,
        request.employee_name,
        session_user, client_id
    ):
        return clientmasters.ChangeClientUserStatusSuccess()


########################################################
# To promote or demote a user from promoted admin status
########################################################
def process_change_admin_status(db, request, session_user):
    if db.is_invalid_id(tblUsers, "user_id", request.user_id):
        return clientmasters.InvalidUserId()
    elif is_primary_admin(db, request.user_id):
        return clientmasters.CannotChangePrimaryAdminStatus()
    elif is_service_proivder_user(db, request.user_id):
        return clientmasters.CannotPromoteServiceProvider()
    elif update_admin_status(
        db,
        request.user_id,
        request.is_admin, request.employee_name,
        session_user
    ):
        return clientmasters.ChangeAdminStatusSuccess()


########################################################
# To get all the units under the given client
########################################################
def process_get_units(db, request, session_user):
    user_company_info = get_user_company_details(
        db,
        session_user
    )
    unit_ids = user_company_info[0]
    division_ids = user_company_info[1]
    legal_entity_ids = user_company_info[2]
    business_group_ids = user_company_info[3]
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
def process_close_unit(db, request, session_user):
    session_user = session_user
    password = request.password
    if verify_password(db, password, session_user):
        if is_seating_unit(db, request.unit_id):
            return clientmasters.CannotCloseUnit()
        else:
            close_unit(db, request.unit_id, request.unit_name, session_user)
            return clientmasters.CloseUnitSuccess()
    else:
        return clientmasters.InvalidPassword()


########################################################
# To get audit trails related to the given user
########################################################
def process_get_audit_trails(db, request, session_user):
    from_count = request.record_count
    to_count = request.page_count
    from_date = request.from_date
    to_date = request.to_date
    user_id = request.user_id
    form_id = request.form_id
    audit_trails = get_audit_trails(
        db, session_user, from_count, to_count,
        from_date, to_date, user_id, form_id
    )
    return audit_trails

def process_user_menus(form_list):
    menus = {}
    for form in form_list:
        form_type = form.form_type
        # print "form_name: %s, form_type: %s" % (form.form_name, form.form_type)
        _forms = menus.get(form_type)
        if _forms is None:
            _forms = []
        _forms.append(form)
        menus[form_type] = _forms
    menus = reorder_menu(menus)
    # print menus
    return clientcore.Menu(menus)
    # return menus


def reorder_menu(menus):
    new_menu = collections.OrderedDict()
    if "Home" in menus:
        new_menu["Home"] = menus["Home"]
    if "Master" in menus:
        new_menu["Master"] = menus["Master"]
    if "Transaction" in menus:
        new_menu["Transaction"] = menus["Transaction"]
    if "Report" in menus:
        new_menu["Report"] = menus["Report"]
    if "Settings" in menus:
        new_menu["Settings"] = menus["Settings"]
    if "My Accounts" in menus:
        new_menu["My Accounts"] = menus["My Accounts"]
    return new_menu


########################################################
# To get unit closure legal entity list under client id
########################################################
def process_get_unit_closure_data(db, request, session_user):
    print "user"
    print session_user
    unit_closure_legal_entities = get_unit_closure_legal_entities(db, session_user)
    print "controller"
    print unit_closure_legal_entities
    return clientmasters.GetUnitClosureDataSuccess(unit_closure_legal_entities)

########################################################
# To get unit closure units list under legal entity id
########################################################
def process_get_unit_closure_unit_data(db, request, session_user):
    unit_closure_units = get_unit_closure_units_list(db, request)
    return clientmasters.GetUnitClosureUnitDataSuccess(unit_closure_units)

########################################################
# To save unit closure units data under unit id
########################################################
def process_save_unit_closure_unit_data(db, request, session_user):
    session_user = int(session_user)
    unit_id = request.unit_id
    action_mode = request.grp_mode
    password = request.password
    remarks = request.closed_remarks

    if not is_invalid_id(db, "unit_id", unit_id):
        return clientmasters.InvalidUnitId()
    else:
        if verify_password(db, password, session_user):
            result = save_unit_closure_data(db, session_user, password, unit_id, remarks, action_mode)
            if result is True:
                return clientmasters.SaveUnitClosureSuccess()
        else:
            return clientmasters.InvalidPassword()
