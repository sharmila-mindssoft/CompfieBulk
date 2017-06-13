import collections
from server.jsontocsvconverter import ConvertJsonToCSV
from clientprotocol import (clientmasters, clientcore, clientreport)
from server.clientdatabase.tables import *
from server.clientdatabase.clientmaster import *
from server.common import datetime_to_string

from server.common import (
    datetime_to_string_time,
    get_date_time_in_date, datetime_to_string
)

__all__ = [
    "process_client_master_requests"
]

########################################################
# To Redirect the requests to the corresponding
# functions
########################################################
def process_client_master_requests(request, db, session_user, client_id, session_category):
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

    elif type(request) is clientmasters.BlockServiceProvider:
        result = process_block_service_provider(
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

    # elif type(request) is clientmasters.GetClientUsers:
    #     result = process_get_client_users(db, request, session_user)

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

    elif type(request) is clientmasters.GetUnitClosureData:
        result = process_get_unit_closure_data(db, request, session_user)

    elif type(request) is clientmasters.GetUnitClosureUnitData:
        result = process_get_unit_closure_unit_data(db, request, session_user)

    elif type(request) is clientmasters.SaveUnitClosureData:
        result = process_save_unit_closure_unit_data(db, request, session_user)

    elif type(request) is clientmasters.UserManagementPrerequisite:
        result = process_UserManagementAddPrerequisite(db, request, session_user, session_category)

    elif type(request) is clientmasters.GetServiceProviderDetailsReportFilters:
        result = get_service_provider_details_report_filter_data(
            db, request, session_user)

    elif type(request) is clientmasters.GetServiceProviderDetailsReport:
        result = get_service_provider_details_report(
            db, request, session_user
        )

    elif type(request) is clientmasters.GetAuditTrailReportFilters:
        result = get_audit_trail_report_filters(
            db, request, session_user, client_id
        )

    elif type(request) is clientmasters.GetLogintraceReportFilters:
        result = get_login_trace_report_filters(
            db, request, session_user, client_id
        )

    elif type(request) is clientmasters.GetLoginTraceReportData:
        result = get_login_trace_report_data(
            db, request, session_user, client_id
        )

    elif type(request) is clientmasters.GetUserProfile:
        result = get_user_profile(
            db, request, session_user, client_id
        )

    elif type(request) is clientmasters.UpdateUserProfile:
        result = update_user_profile(
            db, request, session_user, client_id
        )

    elif type(request) is clientmasters.UserManagementList:
        result = process_UserManagement_list(db, request, session_user, session_category)

    elif type(request) is clientmasters.UserManagementEditView:
        result = process_UserManagement_EditView(db, request, session_user)

    elif type(request) is clientmasters.BlockUser:
        result = process_block_user(db, request, session_user)

    elif type(request) is clientmasters.ResendRegistrationEmail:
        result = process_resend_registration_email(db, request, session_user, client_id)

    elif type(request) is clientmasters.EmployeeCodeExists:
        result = process_employeecode_exists(db, request, session_user, client_id)

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
        request.service_provider_name,
        request.short_name
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
    elif is_service_provider_in_contract(
        db, request.service_provider_id
    ) is False:
        return clientmasters.CannotChangeStatusOfContractExpiredSP()

    if update_service_provider_status(
        db,
        request.service_provider_id,
        is_active, session_user
    ):
        return clientmasters.ChangeServiceProviderStatusSuccess()

########################################################
# To block the service provider
########################################################
def process_block_service_provider(
    db, request, session_user
):
    is_blocked = 0 if request.is_blocked is False else 1

    if block_service_provider(
        db,
        request.service_provider_id,
        request.remarks,
        is_blocked, session_user
    ):
        return clientmasters.BlockServiceProviderSuccess()

########################################################
# To Disable user
########################################################
def process_block_user(
    db, request, session_user
):
    is_blocked = 0 if request.is_blocked is False else 1

    user_category_id = get_user_Category_by_user_id(db, request.user_id)

    if user_category_id == 2:
        if request.is_blocked is True:
            update_licence_viewonly(db, "LESS")
        elif request.is_blocked is False:
            if (get_no_of_remaining_licence_Viewonly(db) <= 0):
                return clientmasters.UserLimitExceeds()
            else:
                update_licence_viewonly(db, "ADD")
    else:
        resultRows = get_user_legal_entity_by_user_id(db, request.user_id)

        for row in resultRows:
            legal_entity_id = int(row["legal_entity_id"])
            if request.is_blocked is True:
                update_licence(db, legal_entity_id, "LESS")
            elif request.is_blocked is False:
                update_licence(db, legal_entity_id, "ADD")

    if block_user(
        db,
        request.user_id,
        request.remarks,
        is_blocked, session_user
    ):
        return clientmasters.BlockUserSuccess()

########################################################
# To Resend Registration Email user
########################################################
def process_resend_registration_email(
    db, request, session_user, client_id
):
    if resend_registration_email(
        db, request.user_id, session_user, client_id
    ):
        return clientmasters.ResendRegistrationEmailSuccess()

########################################################
# Check Employee Code Exists
########################################################
def process_employeecode_exists(
    db, request, session_user, client_id
):
    if request.mode == "SAVE":
        if is_duplicate_employee_code(db, request.employee_code.replace(" ", ""), user_id_optional=None):
            return clientmasters.EmployeeCodeAlreadyExists()
        else:
            return clientmasters.EmployeeCodeSuccess()
    else:
        if is_duplicate_employee_code(db, request.employee_code.replace(" ", ""), request.user_id_optional):
            return clientmasters.EmployeeCodeAlreadyExists()
        else:
            return clientmasters.EmployeeCodeSuccess()

########################################################
# User Management Add Prerequisite
########################################################
def process_UserManagementAddPrerequisite(db, request, session_user, session_category):
    userCategory = {}
    userGroup = {}
    businessGroup = {}
    legalEntity = {}
    groupCategory = {}
    groupDivision = {}
    legalDomains = {}
    legalUnits = {}
    serviceProviders = {}

    userCategory = process_UserManagement_category(db, session_category)
    userGroup = process_UserManagement_UserGroup(db)
    businessGroup = process_UserManagement_BusinessGroup(db)
    legalEntity = process_UserManagement_LegalEntity(db)
    groupDivision = process_UserManagement_GroupDivision(db)
    groupCategory = process_UserManagement_GroupCategory(db)
    legalDomains = process_UserManagement_LegalDomains(db)
    legalUnits = process_UserManagement_LegalUnits(db)
    serviceProviders = process_UserManagement_ServiceProviders(db)

    return clientmasters.GetUserManagementPrerequisiteSuccess(
        user_category=userCategory,
        user_group=userGroup,
        business_group=businessGroup,
        legal_entity=legalEntity,
        group_division=groupDivision,
        group_category=groupCategory,
        legal_Domains=legalDomains,
        legal_units=legalUnits,
        service_providers=serviceProviders
    )
########################################################
# User Management - List users
########################################################
def process_UserManagement_list(db, request, session_user, session_category):
    legalEntities = {}
    users = {}

    legalEntities = process_UserManagement_list_LegalEntities(db, request, session_user)
    users = process_UserManagement_list_users(db, request, session_user, session_category)

    return clientmasters.UserManagementListSuccess(
        legal_entities=legalEntities,
        users=users)

########################################################
# User Management - Edit View
########################################################
def process_UserManagement_EditView(db, request, session_user):
    users = {}
    legalEntities = {}
    domains = {}
    units = {}

    legalEntities = process_UserManagement_EditView_LegalEntities(db, request, session_user)
    users = process_UserManagement_EditView_users(db, request, session_user)
    domains = process_UserManagement_EditView_Domains(db, request, session_user)
    units = process_UserManagement_EditView_Units(db, request, session_user)

    return clientmasters.UserManagementEditViewSuccess(
        users=users,
        legal_entities=legalEntities,
        domains=domains,
        units=units)

########################################################
# To get all client forms to load in User privilege form
########################################################
def process_get_forms(db, cat_id):
    result_rows = get_forms(db, cat_id)
    # print result_rows;
    forms = []
    for row in result_rows:
        parent_menu = None if (row["parent_menu"] == None) else row["parent_menu"]
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
# To get all client Menu to load in User privilege form
########################################################
def process_get_user_category(db):
    result_rows = get_user_category(db)
    user_category_list = []
    for row in result_rows:
        user_category_id = int(row["user_category_id"])
        user_category_name = row["user_category_name"]
        user_category_list.append(
            clientcore.ClientUsercategory(user_category_id, user_category_name)
        )
    return user_category_list

########################################################
# User Management - Load User Category
########################################################
def process_UserManagement_category(db, session_category):
    resultRows = userManagement_GetUserCategory(db, session_category)
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
        print "businessGroupId>>>>>", businessGroupId
        legal_entity_ids = userManagement_legalentity_for_BusinessGroup(db, businessGroupId)
        
        businessGroupList.append(
            clientcore.ClientUserBusinessGroup_UserManagement(businessGroupId, businessGroupName, legal_entity_ids)
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
        le_admin = row["le_admin"]
        legalEntityList.append(
            clientcore.ClientUserLegalEntity_UserManagement(legalEntityId,
                                                            businessGroupId, legalEntityName, le_admin)
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
        domains = userManagement_domains_for_Units(db, unit_id)
        unitList.append(
            clientcore.ClientLegalUnits_UserManagement(unit_id, business_group_id, legal_entity_id,
                                                       division_id, category_id, unit_code,
                                                       unit_name, address, postal_code, domains)
        )
    return unitList
########################################################
# User Management - Service Providers
########################################################
def process_UserManagement_ServiceProviders(db):
    resultRows = userManagement_GetServiceProviders(db)
    spList = []
    for row in resultRows:
        service_provider_id = row["service_provider_id"]
        service_provider_name = row["service_provider_name"]
        short_name = row["short_name"]
        spList.append(
            clientcore.ClientServiceProviders_UserManagement(service_provider_id,
                                                             service_provider_name, short_name)
        )
    return spList
########################################################
# User Management List - Get legal entities
########################################################
def process_UserManagement_list_LegalEntities(db, request, session_user):
    resultRows = userManagement_list_GetLegalEntities(db)
    leList = []
    for row in resultRows:
        country_name = row["country_name"]
        business_group_name = row["business_group_name"]
        legal_entity_id = row["legal_entity_id"]
        legal_entity_name = row["legal_entity_name"]
        contract_from = datetime_to_string(row["contract_from"])
        contract_to = datetime_to_string(row["contract_to"])
        total_licence = row["total_licence"]
        used_licence = row["used_licence"]
        leList.append(
            clientcore.ClientLegalEntities_UserManagementList(country_name, business_group_name,
                                                              legal_entity_id, legal_entity_name,
                                                              contract_from, contract_to,
                                                              total_licence, used_licence)
        )
    return leList

########################################################
# User Management List - Get Users
########################################################
def process_UserManagement_list_users(db, request, session_user, session_category):
    resultRows = userManagement_list_GetUsers(db, session_category)
    userList = []
    for row in resultRows:
        user_id = row["user_id"]
        user_category_id = row["user_category_id"]
        employee_code = row["employee_code"]
        employee_name = row["employee_name"]
        username = row["username"]
        email_id = row["email_id"]
        mobile_no = row["mobile_no"]
        legal_entity_id = row["legal_entity_id"]
        is_active = bool(row["is_active"])
        is_disable = bool(row["is_disable"])
        unblock_days = row["unblock_days"]
        seating_unit = row["seating_unit"]
        legal_entity_ids = userManagement_legalentity_for_User(db, user_id)
        # le_ids
        userList.append(
            clientcore.ClientUsers_UserManagementList(user_id, user_category_id,
                                                      employee_code, employee_name,
                                                      username, email_id,
                                                      mobile_no, legal_entity_id, is_active,
                                                      is_disable, unblock_days, seating_unit, legal_entity_ids)
        )
    return userList

########################################################
# User Management List - Edit View User Details
########################################################
def process_UserManagement_EditView_users(db, request, session_user):
    userID = request.user_id

    resultRows = userManagement_EditView_GetUsers(db, userID)
    userList = []
    for row in resultRows:
        user_id = row["user_id"]
        user_category_id = row["user_category_id"]
        seating_unit_id = row["seating_unit_id"]
        service_provider_id = row["service_provider_id"]
        user_level  = row["user_level"]
        user_group_id = row["user_group_id"]
        email_id = row["email_id"]
        employee_code = row["employee_code"]
        employee_name = row["employee_name"]
        contact_no = row["contact_no"]
        mobile_no = row["mobile_no"]
        address = row["address"]
        is_service_provider = bool(row["is_service_provider"])
        is_active = bool(row["is_active"])
        is_disable = bool(row["is_disable"])
        userList.append(
            clientcore.ClientUsers_UserManagement_EditView_Users(user_id, user_category_id, seating_unit_id, service_provider_id,
                                                                 user_level,user_group_id, email_id, employee_code, employee_name,
                                                                 contact_no, mobile_no, address, is_service_provider,
                                                                 is_active, is_disable)
        )
    return userList

########################################################
# User Management List - Edit View User Details - Legal Entities
########################################################
def process_UserManagement_EditView_LegalEntities(db, request, session_user):
    userID = request.user_id

    resultRows = userManagement_EditView_GetLegalEntities(db, userID)
    legalEntityList = []

    for row in resultRows:
        user_id = row["user_id"]
        legal_entity_id = row["legal_entity_id"]
        business_group_id = row["business_group_id"]

        legalEntityList.append(
            clientcore.ClientUsers_UserManagement_EditView_LegalEntities(user_id,
                                                                         legal_entity_id,
                                                                         business_group_id)
        )
    return legalEntityList

########################################################
# User Management List - Edit View User Details - Domains
########################################################
def process_UserManagement_EditView_Domains(db, request, session_user):
    userID = request.user_id

    resultRows = userManagement_EditView_GetDomains(db, userID)
    domainList = []

    for row in resultRows:
        user_id = row["user_id"]
        legal_entity_id = row["legal_entity_id"]
        domain_id = row["domain_id"]

        domainList.append(
            clientcore.ClientUsers_UserManagement_EditView_Domains(user_id, legal_entity_id, domain_id)
        )
    return domainList

########################################################
# User Management List - Edit View User Details - Domains
########################################################
def process_UserManagement_EditView_Units(db, request, session_user):
    userID = request.user_id

    resultRows = userManagement_EditView_GetUnits(db, userID)
    unitList = []

    for row in resultRows:
        user_id = row["user_id"]
        legal_entity_id = row["legal_entity_id"]
        unit_id = row["unit_id"]
        business_group_id = row["business_group_id"]
        division_id = row["division_id"]
        category_id = row["category_id"]

        unitList.append(
            clientcore.ClientUsers_UserManagement_EditView_Units(user_id, legal_entity_id, unit_id,
                                                                 business_group_id, division_id, category_id)
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
        db, request.user_category_id, request.user_group_name, request.user_group_id
    ):

        return clientmasters.UserGroupNameAlreadyExists()
    elif update_user_privilege(db, request, session_user):
        return clientmasters.UpdateUserPrivilegesSuccess()


########################################################
# To change the status of user privilege
########################################################
def process_change_user_privilege_status(db, request, session_user):
    if db.is_invalid_id(tblUserGroups, "user_group_id", request.user_group_id):
        return clientmasters.InvalidUserGroupId()
    elif is_user_exists_under_user_group(db, request.user_group_id):
        return clientmasters.CannotDeactivateUserExists()
    elif update_user_privilege_status(db, request.user_group_id, request.is_active, session_user):
        return clientmasters.ChangeUserPrivilegeStatusSuccess()

########################################################
# To validate and save a user
########################################################
def process_save_client_user(db, request, session_user, client_id):

    # Check Viewonly Licence Count
    if request.user_category==2:
        if (get_no_of_remaining_licence_Viewonly(db) <= 0):
            return clientmasters.UserLimitExceeds()
        else:
            update_licence_viewonly(db, "ADD")
    else:
        resultRows = get_no_of_remaining_licence(db, request.user_entity_ids)
        for row in resultRows:
            legal_entity_id = int(row["legal_entity_id"])
            remaining_licence = int(row["remaining_licence"])
            if remaining_licence <=0:
                return clientmasters.UserLimitExceeds()
            else:
                update_licence(db, legal_entity_id, "ADD")

    if is_duplicate_employee_code(db, request.employee_code.replace(" ", ""), user_id=None):
        return clientmasters.EmployeeCodeAlreadyExists()
    # Commented for functionality check
    # if is_already_assigned_units (db,request.user_unit_ids, request.user_domain_ids):
    #     return clientmasters.UnitsAlreadyAssigned()

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
    # elif is_duplicate_employee_name(
    #     db, request.employee_name, user_id=request.user_id
    # ):
    #     return clientmasters.EmployeeNameAlreadyExists()
    elif update_user(db, request, session_user, client_id):
        return clientmasters.UpdateClientUserSuccess()


########################################################
# To change the status of a user
########################################################
def process_change_client_user_status(db, request, session_user, client_id):
    # if db.is_invalid_id(tblUsers, "user_id", request.user_id):
    #     return clientmasters.InvalidUserId()
    # if is_old_primary_admin(db, request.user_id):
    #     return clientmasters.CannotChangeOldPrimaryAdminStatus()
    # elif is_primary_admin(db, request.user_id):
    #     return clientmasters.CannotChangePrimaryAdminStatus()
    # if have_compliances(db, request.user_id) and request.is_active in [False, 0]:
    #     return clientmasters.ReassignCompliancesBeforeDeactivate()
    if update_user_status(
        db,
        request.user_id,
        request.active_status,
        request.employee_name,
        session_user, client_id
    ):
        return clientmasters.ChangeClientUserStatusSuccess()

########################################################
# To get audit trails related to the given user
########################################################

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
    if "Dashboard" in menus:
        new_menu["Dashboard"] = menus["Dashboard"]
    if "Master" in menus:
        new_menu["Master"] = menus["Master"]
    if "Transaction" in menus:
        new_menu["Transaction"] = menus["Transaction"]
    if "Report" in menus:
        new_menu["Report"] = menus["Report"]
    if "Settings" in menus:
        new_menu["Settings"] = menus["Settings"]
    # if "My Accounts" in menus:
    #     new_menu["My Accounts"] = menus["My Accounts"]
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
    # password = request.password
    remarks = request.closed_remarks

    if not is_invalid_id(db, "unit_id", unit_id):
        return clientmasters.InvalidUnitId()
    else:
        result = save_unit_closure_data(db, session_user, unit_id, remarks, action_mode)
        if result is True:
            return clientmasters.SaveUnitClosureSuccess()

###############################################################################################
# Objective: To get service providers and its users list
# Parameter: request object and the client id
# Result: list of record sets which contains service providers and users its
###############################################################################################
def get_service_provider_details_report_filter_data(db, request, session_user):
    service_providers_list = get_service_providers_list(db)
    service_providers_users_list = get_service_providers_user_list(db)
    service_providers_status_list = get_service_provider_status(db)
    return clientmasters.GetServiceProviderDetailsFilterSuccess(
        sp_list=service_providers_list,
        sp_user_list=service_providers_users_list,
        sp_status_list=service_providers_status_list
    )

###############################################################################################
# Objective: To get service providers details and user details
# Parameter: request object and the client id
# Result: list of record sets which contains service providers details
###############################################################################################
def get_service_provider_details_report(db, request, session_user):
    service_providers_status_list, total_record = get_service_provider_details_report_data(db, request)
    return clientmasters.GetServiceProviderDetailsReportSuccess(
        sp_details_list=service_providers_status_list, total_count=total_record
    )


###############################################################################################
# Objective: To get users and forms list under legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains forms and users list
###############################################################################################
def get_audit_trail_report_filters(db, request, session_user, client_id):
    legal_entity_id = request.legal_entity_id
    audit_users_list = get_audit_users_list(db, legal_entity_id)
    audit_forms_list = get_audit_forms_list(db)
    return clientmasters.GetAuditTrailFilterSuccess(
        audit_users_list=audit_users_list, audit_forms_list=audit_forms_list
    )

###############################################################################################
# Objective: To get users list
# Parameter: request object and the client id
# Result: list of record sets which contains users list
###############################################################################################
def get_login_trace_report_filters(db, request, session_user, client_id):
    audit_users_list = get_login_users_list(db)
    return clientmasters.GetLoginTraceFilterSuccess(
        audit_users_list=audit_users_list
    )

###############################################################################################
# Objective: To get activity log of login under user
# Parameter: request object and the client id
# Result: list of record sets which contains activity log of login
###############################################################################################
def get_login_trace_report_data(db, request, session_user, client_id):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "LoginTraceReport"
        )
        if converter.FILE_DOWNLOAD_PATH is None:
            return clientreport.ExportToCSVEmpty()
        else:
            return clientreport.ExportToCSVSuccess(
                link=converter.FILE_DOWNLOAD_PATH
            )
    else:
        result, total_record = process_login_trace_report(db, request, client_id)
        return clientmasters.GetLoginTraceReportDataSuccess(log_trace_activities=result, total_count=total_record)


###############################################################################################
# Objective: To get user details
# Parameter: request object and the client id
# Result: logged user details under the client
###############################################################################################
def get_user_profile(db, request, session_user, client_id):
    result = get_user_info(db, session_user, client_id)
    return clientmasters.GetUserProfileSuccess(user_profile=result)

###############################################################################################
# Objective: To update user details
# Parameter: request object and the client id
# Result: updates user details
###############################################################################################
def update_user_profile(db, request, session_user, client_id):
    result = update_profile(db, session_user, request)
    if result is True:
        return clientmasters.UpdateUserProfileSuccess()
