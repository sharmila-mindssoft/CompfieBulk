########################################################
# This Controller will handle Knowledge User, Usergroup
# related requests
#
# In this module "db" is an object of "KnowledgeDatabase"
########################################################
from protocol import (admin, core, generalprotocol)
from corecontroller import process_user_menus
from server.database.tables import *
from server.database.admin import *
from server.database.technomaster import (
    get_business_groups_for_user
)
from server.constants import USER_ENABLE_CUTOFF

__all__ = [
    "process_admin_request", "get_user_groups"
]


########################################################
# To Redirect Requests to Functions
########################################################
def process_admin_request(request, db, session_user):
    request_frame = request.request

    if type(request_frame) is admin.GetUserGroups:
        result = get_user_groups(db, request_frame, session_user)

    elif type(request_frame) is admin.SaveUserGroup:
        result = save_user_group_record(db, request_frame, session_user)

    elif type(request_frame) is admin.UpdateUserGroup:
        result = update_user_groups(db, request_frame, session_user)

    elif type(request_frame) is admin.ChangeUserGroupStatus:
        result = change_user_group_status(db, request_frame, session_user)

    elif type(request_frame) is admin.GetUsers:
        result = get_users(db, request_frame, session_user)

    elif type(request_frame) is admin.SaveUser:
        result = save_user_record(db, request_frame, session_user)

    elif type(request_frame) is admin.UpdateUser:
        result = update_user_record(db, request_frame, session_user)

    elif type(request_frame) is admin.ChangeUserStatus:
        result = change_user_status(db, request_frame, session_user)

    elif type(request_frame) is admin.ChangeDisableStatus:
        result = change_disable_status(db, request_frame, session_user)

    elif type(request_frame) is admin.SendRegistraion:
        result = send_user_registration_mail(db, request_frame, session_user)

    elif type(request_frame) is admin.GetValidityDateList:
        result = process_getvaliditydate_request(
            db, request_frame, session_user)

    elif type(request_frame) is admin.SaveValidityDateSettings:
        result = process_save_validity_date_settings(
            db, request_frame, session_user)

    elif type(request_frame) is admin.GetUserMappings:
        result = process_get_user_mappings(db, session_user)

    elif type(request_frame) is admin.SaveUserMappings:
        result = process_save_user_mappings(db, request_frame, session_user)

    elif type(request_frame) is admin.CheckUserMappings:
        result = process_check_user_mappings(db, request_frame, session_user)

    elif type(request_frame) is admin.GetReassignUserAccountFormdata:
        result = get_reassign_user_account_form_data(
            db, request_frame, session_user)

    elif type(request_frame) is admin.GetTechnoUserData:
        result = process_get_techno_user_info(db, request_frame)

    elif type(request_frame) is admin.GetDomainUserData:
        result = process_get_domain_user_info(db, request_frame)

    elif type(request_frame) is admin.SaveReassignTechnoManager:
        result = process_reassign_techno_manager(db, request_frame, session_user)

    elif type(request_frame) is admin.SaveReassignTechnoExecutive :
        result = process_reassign_techno_executiive(db, request_frame, session_user)

    elif type(request_frame) is admin.SaveReassignDomainManager:
        result = process_reassign_domain_manager(db, request_frame, session_user)

    elif type(request_frame) is admin.SaveReassignDomainExecutive :
        result = process_reassign_domain_executive(db, request_frame, session_user)

    elif type(request_frame) is admin.UserReplacement :
        result = process_user_replacement(db, request_frame, session_user)

    elif type(request_frame) is admin.CheckUserReplacement :
        result = process_check_user_replacement(db, request_frame, session_user)

    return result


########################################################
# To Retrieve category wise forms from database
########################################################
def return_forms(row):
    result = []
    for r in row :
        parent_menu = None if (r["parent_menu"] == None) else r["parent_menu"]
        frm = generalprotocol.Form(
            r["form_id"], r["form_name"], r["form_url"],
            parent_menu, r["form_type"]
        )
        result.append(frm)
    return result

def get_forms_list(db):
    result_rows = get_forms(db)
    knowledge_manager_forms = return_forms(result_rows[0])
    knowledge_user_forms = return_forms(result_rows[1])
    techno_manager_forms = return_forms(result_rows[2])
    techno_user_forms = return_forms(result_rows[3])
    domain_manager_forms = return_forms(result_rows[4])
    domain_user_forms = return_forms(result_rows[5])

    result = {}  # result key is user_category_id
    result[3] = process_user_menus(knowledge_manager_forms)
    result[4] = process_user_menus(knowledge_user_forms)
    result[5] = process_user_menus(techno_manager_forms)
    result[6] = process_user_menus(techno_user_forms)
    result[7] = process_user_menus(domain_manager_forms)
    result[8] = process_user_menus(domain_user_forms)

    return result


########################################################
# To get list of user groups with it's details such as
# forms, form categories
########################################################
def process_user_group_detailed_list(db):
    user_group_list = []
    rows = get_user_group_detailed_list(db)
    usergroups = rows[0]
    formids = rows[1]
    for row in usergroups:
        user_group_id = int(row["user_group_id"])
        user_group_name = row["user_group_name"]
        user_category_id = row["user_category_id"]
        no_of_users = row["count"]
        form_ids = []
        for f in formids:
            if user_group_id == int(f["user_group_id"]) :
                form_ids.append(int(f["form_id"]))
        # if len(row["form_ids"]) >= 1:
        #     form_ids = [int(x) for x in row["form_ids"].split(",")]
        # else:
        #     form_ids = []
        is_active = False if row["is_active"] == 0 else True
        user_group_list.append(admin.UserGroup(
            user_group_id, user_group_name,
            user_category_id, form_ids, is_active, no_of_users
        ))
    return user_group_list


########################################################
# To get form categories list
########################################################
def get_form_categories_db(db):
    formCategoryList = []
    rows = get_form_categories(db)
    for row in rows:
        formCategoryList.append(generalprotocol.FormCategory(
            row["form_category_id"], row["form_category"])
        )
    return formCategoryList

def get_user_cetegories_db(db):
    userCategoryList = []
    rows = get_form_categories(db)
    for row in rows:
        userCategoryList.append(generalprotocol.FormCategory(
            row["user_category_id"], row["user_category_name"])
        )
    return userCategoryList


########################################################
# To handle get user group list request
########################################################
def get_user_groups(db, request_frame, session_user):
    forms = get_forms_list(db)
    form_categories = get_user_cetegories_db(db)
    user_group_list = process_user_group_detailed_list(db)
    result = admin.GetUserGroupsSuccess(
        form_categories=form_categories,
        forms=forms,
        user_groups=user_group_list
    )
    return result


########################################################
# To Handle Save user group request
########################################################
def save_user_group_record(db, request, session_user):
    user_group_name = request.user_group_name
    form_category_id = request.form_category_id
    # form_ids = ",".join(str(x) for x in request.form_ids)
    form_ids = request.form_ids
    if is_duplicate_user_group_name(db, user_group_name):
        return admin.GroupNameAlreadyExists()
    elif save_user_group(
        db, user_group_name, form_category_id, form_ids, session_user
    ):
        return admin.SaveUserGroupSuccess()


########################################################
# To Handle Update user group request
########################################################
def update_user_groups(db, request, session_user):
    user_group_id = request.user_group_id
    user_group_name = request.user_group_name
    form_category_id = request.form_category_id
    form_ids = request.form_ids
    if db.is_invalid_id(tblUserGroups, "user_group_id", user_group_id):
        return admin.InvalidUserGroupId()
    elif is_duplicate_user_group_name(db, user_group_name, user_group_id):
        return admin.GroupNameAlreadyExists()
    elif update_user_group(
        db, user_group_id, user_group_name,
        form_category_id, form_ids, session_user
    ):
        return admin.UpdateUserGroupSuccess()


########################################################
# To Change the status of user group
########################################################
def change_user_group_status(db, request, session_user):
    user_group_id = request.user_group_id
    ug_name = request.user_group_name
    is_active = 0 if request.is_active is False else 1
    if db.is_invalid_id(tblUserGroups, "user_group_id", user_group_id):
        return admin.InvalidUserGroupId()
    elif is_user_exists_under_user_group(
        db, request.user_group_id
    ):
        return admin.CannotDeactivateUserExists()
    elif update_user_group_status(db, user_group_id, ug_name, is_active, session_user):
        return admin.ChangeUserGroupStatusSuccess()


########################################################
# To get Users List with user details
########################################################
def get_users(db, request_frame, session_user):
    domain_list = get_domains_for_user(db, session_user)
    country_list = get_countries_for_user(db, session_user)
    user_group_list = []
    user_list = []
    user_cat_list = []
    user_group_rows = get_user_groups_from_db(db)

    for user_group_row in user_group_rows[0]:
        user_group_id = user_group_row["user_group_id"]
        user_cat_id = user_group_row["user_category_id"]
        user_group_name = user_group_row["user_group_name"]
        is_active = True if user_group_row["is_active"] == 1 else False
        user_group_list.append(
            core.UserGroup(user_group_id, user_cat_id, user_group_name, is_active)
        )

    for r in user_group_rows[1]:
        user_cat_list.append(
            core.UserCategory(r["user_category_id"], r["user_category_name"])
        )

    rows = get_detailed_user_list(db)

    def get_user_domain(user_id, data):
        domain_ids = []
        for r in data:
            if int(r["user_id"]) == user_id:
                domain_ids.append(admin.CountryWiseDomain(int(r["country_id"]), int(r["domain_id"])))
        return domain_ids

    def get_user_country(user_id, data):
        country_ids = []
        for r in data:
            if int(r["user_id"]) == user_id:
                country_ids.append(int(r["country_id"]))
        return country_ids

    user_rows = rows[0]
    for user_row in user_rows:
        user_id = user_row["user_id"]
        user_cat_id = user_row["user_category_id"]
        user_cat_name = user_row["user_category_name"]
        employee_name = user_row["employee_name"]
        employee_code = user_row["employee_code"]
        email_id = user_row["email_id"]
        user_group_id = user_row["user_group_id"]
        contact_no = user_row["contact_no"]
        mobile_no = user_row["mobile_no"]
        address = None if user_row["address"] == "" else user_row["address"]
        designation = None if (
            user_row["designation"] == "") else user_row["designation"]
        country_ids = get_user_country(user_id, rows[2])
        domain_ids = get_user_domain(user_id, rows[1])
        is_active = True if user_row["is_active"] == 1 else False
        is_disable = True if user_row["is_disable"] == 1 else False
        username = user_row["username"]
        days_left = user_row["days_left"]

        allow_enable = True
        if is_disable is True and days_left > USER_ENABLE_CUTOFF :
            allow_enable = False

        user_list.append(
            core.UserDetails(
                user_id, user_cat_id,
                user_cat_name,
                employee_name, employee_code,
                email_id, user_group_id,
                contact_no, mobile_no,
                address, designation,
                country_ids, domain_ids,
                is_active, is_disable,
                username, allow_enable, days_left, user_row["disable_reason"]
            )
        )

    return admin.GetUsersSuccess(
        user_groups=user_group_list,
        countries=country_list,
        domains=domain_list,
        user_categories=user_cat_list,
        users=user_list
    )


########################################################
# To Handle Save user request
########################################################
def save_user_record(db, request, session_user):
    # user_id = db.generate_new_user_id()
    user_category_id = request.user_category_id
    email_id = request.email_id
    user_group_id = request.user_group_id
    employee_name = request.employee_name
    employee_code = request.employee_code
    contact_no = request.contact_no
    mobile_no = request.mobile_no
    address = None if request.address == "" else request.address
    designation = None if request.designation == "" else request.designation
    country_ids = request.country_ids
    domain_ids = request.domain_ids
    # if is_duplicate_email(db, email_id):
    #     return admin.EmailIDAlreadyExists()
    if is_duplicate_employee_code(db, employee_code):
        return admin.EmployeeCodeAlreadyExists()
    elif save_user(
        db, user_category_id, email_id, user_group_id, employee_name,
        employee_code, contact_no, mobile_no, address, designation,
        country_ids, domain_ids, session_user
    ):
        return admin.SaveUserSuccess()


#################################################################
# To Handle Update user request
#################################################################
def update_user_record(db, request, session_user):
    user_id = request.user_id
    user_category_id = request.user_category_id
    email_id = request.email_id
    user_group_id = request.user_group_id
    employee_name = request.employee_name
    employee_code = request.employee_code
    contact_no = request.contact_no
    mobile_no = request.mobile_no
    address = None if request.address == "" else request.address
    designation = None if request.designation == "" else request.designation
    country_ids = request.country_ids
    domain_ids = request.domain_ids

    if db.is_invalid_id(tblUsers, "user_id", user_id):
        return admin.InvalidUserId()
    elif is_duplicate_employee_code(
        db, employee_code, user_id
    ):
        return admin.EmployeeCodeAlreadyExists()
    elif update_user(
        db, user_id, user_category_id, email_id, user_group_id, employee_name,
        employee_code, contact_no, mobile_no, address, designation,
        country_ids, domain_ids, session_user
    ):
        return admin.UpdateUserSuccess()

#
#  User Registraion process
#
def send_user_registration_mail(db, request, session_user):
    res = save_registraion_token(db, request.user_id, request.username, request.email_id)
    if res :
        return admin.SendRegistraionSuccess()
    else :
        print "send email failed"

###################################################################
# To Change the status of user
###################################################################
def change_user_status(db, request, session_user):
    user_id = request.user_id
    is_active = int(request.is_active)
    if db.is_invalid_id(tblUsers, "user_id", user_id):
        return admin.InvalidUserId()
    elif is_user_idle(db, user_id) is False:
        return admin.CannotDisableUserTransactionExists()

    elif update_user_status(db, user_id, is_active, session_user):
        return admin.ChangeUserStatusSuccess()


###################################################################
# To disable user
###################################################################
def change_disable_status(db, request, session_user):
    user_id = request.user_id
    is_active = int(request.is_active)
    remarks = request.remarks
    if db.is_invalid_id(tblUsers, "user_id", user_id):
        return admin.InvalidUserId()
    elif is_user_idle(db, user_id) is False:
        return admin.CannotDisableUserTransactionExists()
    elif update_disable_status(db, user_id, is_active, remarks, session_user):
        return admin.ChangeUserStatusSuccess()

################################################################
# To Get list of Countries, domains and Validity Dates
################################################################
def process_getvaliditydate_request(db, request, session_user):
    countries = get_mapped_countries(db)
    domains = get_mapped_domains(db)
    validity_dates = get_validity_dates(db)
    country_domain_mappings = get_country_domain_mappings(db)
    return admin.GetValidityDateListSuccess(
        countries=countries,
        domains=domains,
        validity_dates=validity_dates,
        country_domain_mappings=country_domain_mappings
    )


################################################################
# To save validity date settings
################################################################
def process_save_validity_date_settings(db, request, session_user):
    return save_validity_date_settings(
        db, request.validity_date_settings, session_user)

def process_get_user_mappings(db, session_user):
    (
        countries, domains, knowledge_managers, knowledge_users,
        techno_managers, techno_users, domain_managers, domain_users,
        user_mappings
    ) = get_user_mapping_form_data(db, session_user)
    return admin.GetUserMappingsSuccess(
        countries=countries, domains=domains,
        knowledge_managers=knowledge_managers, knowledge_users=knowledge_users,
        techno_managers=techno_managers, techno_users=techno_users,
        domain_managers=domain_managers, domain_users=domain_users,
        user_mappings=user_mappings
    )


def process_save_user_mappings(db, request, session_user):
    save_user_mappings(db, request, session_user)
    return admin.SaveUserMappingsSuccess()

def process_check_user_mappings(db, request, session_user):
    if check_user_mappings(db, request, session_user) is False:
        return admin.CannotRemoveUserTransactionExists()
    else:
        return admin.CheckUserMappingsSuccess()

def get_reassign_user_account_form_data(db, request, session_user):

    domains = get_domains_for_user(db, session_user)
    groups = get_reassign_client_groups(db, session_user)
    business_groups = get_business_groups_for_user(db, session_user)
    legal_entities = get_reassign_legal_entity(db, session_user)
    user_categories = get_categories_for_user(db, session_user)
    users = get_reassign_user_filters(db)
    techno_manager = users[0]
    techno_exe = users[1]
    domain_manager = users[2]
    domain_exe = users[3]
    return admin.GetReassignUserAccountFormdataSuccess(
        techno_manager, techno_exe, domain_manager,
        domain_exe, groups, business_groups,
        legal_entities, domains, user_categories
    )


# def process_save_reassign_user_account_request(db, request, session_user):
#     save_reassigned_user_account(db, request, session_user)
#     return admin.SaveReassignUserAccountSuccess()

def process_get_techno_user_info(db, request):
    user_id = request.user_id
    data = get_techno_user_data(db, user_id)
    return admin.GetTechnoUserDataSuccess(data)

def process_get_domain_user_info(db, request):
    user_id = request.domain_user_id
    entity_id = request.entity_id
    domain_id = request.domain_id
    group_id = request.group_id
    data = get_domain_user_data(db, user_id, group_id, entity_id, domain_id)
    return admin.GetDomainUserDataSuccess(data)

def process_reassign_techno_manager(db, request, session_user):
    user_from = request.reassign_from
    data = request.manager_info
    remarks = request.remarks
    result = save_reassign_techno_manager(db, user_from, data, remarks, session_user)
    if result :
        return admin.SaveReassignUserAccountSuccess()

def process_reassign_techno_executiive(db, request, session_user):
    user_from = request.reassign_from
    user_to = request.reassign_to
    data = request.manager_info
    remarks = request.remarks
    result = save_reassign_techno_executive(db, user_from, user_to, data, remarks, session_user)
    if result :
        return admin.SaveReassignUserAccountSuccess()

def process_reassign_domain_manager(db, request, session_user):
    user_from = request.reassign_from
    user_to = request.reassign_to
    domain_id = request.domain_id
    data = request.manager_info
    remarks = request.remarks
    result = save_reassign_domain_manager(
        db, user_from, user_to, domain_id, data,
        remarks, session_user
    )
    if result :
        return admin.SaveReassignUserAccountSuccess()

def process_reassign_domain_executive(db, request, session_user):
    user_from = request.reassign_from
    user_to = request.reassign_to
    domain_id = request.domain_id
    unit_ids = request.unit_ids
    remarks = request.remarks
    result = save_reassign_domain_executive(db, user_from, user_to, domain_id, unit_ids, remarks, session_user)
    if result :
        return admin.SaveReassignUserAccountSuccess()

def process_user_replacement(db, request, session_user):
    user_type = request.user_type
    user_from = request.user_from
    user_to = request.user_to
    remarks = request.remarks
    result = save_user_replacement(db, user_type, user_from, user_to, remarks, session_user)
    if result :
        return admin.UserReplacementSuccess()

def process_check_user_replacement(db, request, session_user):
    if check_user_replacement(db, request, session_user) is False:
        return admin.NoTransactionExists()
    else:
        return admin.CheckUserReplacementSuccess()
