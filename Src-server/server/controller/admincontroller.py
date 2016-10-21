########################################################
# This Controller will handle Knowledge User, Usergroup
# related requests
#
# In this module "db" is an object of "KnowledgeDatabase"
########################################################
from protocol import (admin, core, login)
from corecontroller import process_user_menus
from generalcontroller import validate_user_session, validate_user_forms
from server import logger
from server.database.tables import *
from server.database.admin import *
__all__ = [
    "process_admin_request", "get_user_groups"
]

forms = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


########################################################
# To Redirect Requests to Functions
########################################################
def process_admin_request(request, db):
    session_token = request.session_token
    request_frame = request.request
    session_user = validate_user_session(db, session_token)
    if session_user is not None:
        admin_user_type = 0
        is_valid = validate_user_forms(
            db, session_user, forms, request_frame, admin_user_type
        )
        if is_valid is not True:
            return login.InvalidSessionToken()

    if session_user is None:
        return login.InvalidSessionToken()
    if type(request_frame) is admin.GetUserGroups:
        logger.logKnowledgeApi("GetUserGroups", " process begin")
        result = get_user_groups(db, request_frame, session_user)
        logger.logKnowledgeApi("GetUserGroups", "process end")

    elif type(request_frame) is admin.SaveUserGroup:
        logger.logKnowledgeApi("SaveUserGroup", "process begin")
        result = save_user_group_record(db, request_frame, session_user)
        logger.logKnowledgeApi("SaveUserGroup", "process end")

    elif type(request_frame) is admin.UpdateUserGroup:
        logger.logKnowledgeApi("UpdateUserGroup", "process begin")
        result = update_user_groups(db, request_frame, session_user)
        logger.logKnowledgeApi("UpdateUserGroup", "process end")

    elif type(request_frame) is admin.ChangeUserGroupStatus:
        logger.logKnowledgeApi("ChangeUserGroupStatus", "process begin")
        result = change_user_group_status(db, request_frame, session_user)
        logger.logKnowledgeApi("ChangeUserGroupStatus", "process end")

    elif type(request_frame) is admin.GetUsers:
        logger.logKnowledgeApi("GetUsers", "process begin")
        result = get_users(db, request_frame, session_user)
        logger.logKnowledgeApi("ChangeUserGroupStatus", "process end")

    elif type(request_frame) is admin.SaveUser:
        logger.logKnowledgeApi("SaveUser", "process begin")
        result = save_user_record(db, request_frame, session_user)
        logger.logKnowledgeApi("SaveUser", "process end")

    elif type(request_frame) is admin.UpdateUser:
        logger.logKnowledgeApi("UpdateUser", "process begin")
        result = update_user_record(db, request_frame, session_user)
        logger.logKnowledgeApi("UpdateUser", "process end")

    elif type(request_frame) is admin.ChangeUserStatus:
        logger.logKnowledgeApi("ChangeUserStatus", "process begin")
        result = change_user_status(db, request_frame, session_user)
        logger.logKnowledgeApi("ChangeUserStatus", "process end")

    elif type(request_frame) is admin.GetValidityDateList:
        logger.logKnowledgeApi("GetValidityDateList", "process begin")
        result = process_getvaliditydate_request(
            db, request_frame, session_user)
        logger.logKnowledgeApi("GetValidityDateList", "process end")

    elif type(request_frame) is admin.SaveValidityDateSettings:
        logger.logKnowledgeApi("SaveValidityDateSettings", "process begin")
        result = process_save_validity_date_settings(
            db, request_frame, session_user)
        logger.logKnowledgeApi("SaveValidityDateSettings", "process end")

    elif type(request_frame) is admin.GetUserMappings:
        logger.logKnowledgeApi("GetUserMappings", "process begin")
        result = process_get_user_mappings(db, session_user)
        logger.logKnowledgeApi("GetUserMappings", "process end")

    elif type(request_frame) is admin.SaveUserMappings:
        logger.logKnowledgeApi("SaveUserMappings", "process begin")
        result = process_save_user_mappings(db, request_frame, session_user)
        logger.logKnowledgeApi("SaveUserMappings", "process end")
    return result


########################################################
# To Retrieve category wise forms from database
########################################################
def return_forms(row):
    result = []
    for r in row :
        parent_menu = None if (r["parent_menu"] == None) else r["parent_menu"]
        frm = core.Form(
            r["form_id"], r["form_name"], r["form_url"],
            parent_menu, r["form_type"]
        )
        result.append(frm)
    return result

def get_forms_list(db):
    result_rows = get_forms(db)
    print result_rows
    print '\n\n'
    knowledge_manager_forms = return_forms(result_rows[0])
    knowledge_user_forms = return_forms(result_rows[1])
    techno_manager_forms = return_forms(result_rows[2])
    techno_user_forms = return_forms(result_rows[3])
    domain_manager_forms = return_forms(result_rows[4])
    domain_user_forms = return_forms(result_rows[5])

    # for row in result_rows:
    #     parent_menu = None if (
    #         row["parent_menu"] == None) else row["parent_menu"]
    #     form = core.Form(
    #         form_id=row["form_id"],
    #         form_name=row["form_name"],
    #         form_url=row["form_url"],
    #         parent_menu=parent_menu,
    #         form_type=row["form_type"]
    #     )
    #     if int(row["form_category_id"]) == 3:
    #         knowledge_user_forms.append(form)
    #     elif int(row["form_category_id"]) == 4:
    #         knowledge_manager_forms.append(form)
    #     elif int(row["form_category_id"]) == 5:
    #         cc_manager_forms.append(form)
    #     elif int(row["form_category_id"]) == 6:
    #         cc_user_forms.append(form)
    #     elif int(row["form_category_id"]) == 7:
    #         techno_user_forms.append(form)
    #     elif int(row["form_category_id"]) == 8:
    #         techno_manager_forms.append(form)
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
        formCategoryList.append(core.FormCategory(
            row["form_category_id"], row["form_category"])
        )
    return formCategoryList

def get_user_cetegories_db(db):
    userCategoryList = []
    rows = get_form_categories(db)
    for row in rows:
        userCategoryList.append(core.FormCategory(
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
    print form_ids
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
    domain_list = get_domains_for_user(db, 0)
    country_list = get_countries_for_user(db, 0)
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
            domain_ids.append(int(r["domain_id"]))
        return domain_ids

    def get_user_country(user_id, data):
        country_ids = []
        for r in data:
            country_ids.append(int(r["country_id"]))
        return country_ids

    user_rows = rows[0]
    for user_row in user_rows:
        user_id = user_row["user_id"]
        user_cat_id = user_row["user_categroy_id"]
        employee_name = user_row["employee_name"]
        employee_code = user_row["employee_code"]
        email_id = user_row["email_id"]
        user_group_id = user_row["user_group_id"]
        contact_no = user_row["contact_no"]
        mobile_no = user_row["mobile_no"]
        address = None if user_row["address"] == "" else user_row["address"]
        designation = None if (
            user_row["designation"] == "") else user_row["designation"]
        country_ids = get_user_country(user_id)
        domain_ids = get_user_domain(user_id)
        is_active = True if user_row["is_active"] == 1 else False
        is_disable = True if user_row["is_disable"] == 1 else False
        username = user_row["username"]
        user_list.append(
            core.UserDetails(
                user_id, user_cat_id,
                employee_name, employee_code,
                email_id, user_group_id,
                contact_no, mobile_no,
                address, designation,
                country_ids, domain_ids,
                is_active, is_disable,
                username
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
    user_group_id = request.user_group_id
    employee_name = request.employee_name
    employee_code = request.employee_code
    contact_no = request.contact_no
    address = request.address
    designation = request.designation
    country_ids = request.country_ids
    domain_ids = request.domain_ids
    if db.is_invalid_id(tblUsers, "user_id", user_id):
        return admin.InvalidUserId()
    elif is_duplicate_employee_code(
        db, employee_code, user_id
    ):
        return admin.EmployeeCodeAlreadyExists()
    elif update_user(
        db, user_id, user_group_id, employee_name, employee_code,
        contact_no, address, designation, country_ids, domain_ids,
        session_user
    ):
        return admin.UpdateUserSuccess()


###################################################################
# To Change the status of user
###################################################################
def change_user_status(db, request, session_user):
    user_id = request.user_id
    is_active = 0 if request.is_active is False else 1
    if db.is_invalid_id(tblUsers, "user_id", user_id):
        return admin.InvalidUserId()

    elif update_user_status(db, user_id, is_active):
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
    save_validity_date_settings(
        db, request.validity_date_settings, session_user)
    return admin.SaveValidityDateSettingsSuccess()


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
