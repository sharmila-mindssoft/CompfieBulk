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

forms = [3, 4]

########################################################
# To Redirect Requests to Functions
########################################################
def process_admin_request(request, db) :
    session_token = request.session_token
    request_frame = request.request
    session_user = validate_user_session(db, session_token)
    if session_user is not None :
        is_valid = validate_user_forms(db, session_user, forms, request_frame)
        if is_valid is not True :
            return login.InvalidSessionToken()

    if session_user is None:
        return login.InvalidSessionToken()

    if type(request_frame) is admin.GetUserGroups:
        logger.logKnowledgeApi("GetUserGroups", " process begin")
        result = get_user_groups(db, request_frame, session_user)
        logger.logKnowledgeApi("GetUserGroups", "process end")

    if type(request_frame) is admin.SaveUserGroup:
        logger.logKnowledgeApi("SaveUserGroup", "process begin")
        result = save_user_group(db, request_frame, session_user)
        logger.logKnowledgeApi("SaveUserGroup", "process end")

    if type(request_frame) is admin.UpdateUserGroup:
        logger.logKnowledgeApi("UpdateUserGroup", "process begin")
        result = update_user_group(db, request_frame, session_user)
        logger.logKnowledgeApi("UpdateUserGroup", "process end")

    if type(request_frame) is admin.ChangeUserGroupStatus:
        logger.logKnowledgeApi("ChangeUserGroupStatus", "process begin")
        result = change_user_group_status(db, request_frame, session_user)
        logger.logKnowledgeApi("ChangeUserGroupStatus", "process end")

    if type(request_frame) is admin.GetUsers:
        logger.logKnowledgeApi("GetUsers", "process begin")
        result = get_users(db, request_frame, session_user)
        logger.logKnowledgeApi("ChangeUserGroupStatus", "process end")

    if type(request_frame) is admin.SaveUser:
        logger.logKnowledgeApi("SaveUser", "process begin")
        result = save_user(db, request_frame, session_user)
        logger.logKnowledgeApi("SaveUser", "process end")

    if type(request_frame) is admin.UpdateUser:
        logger.logKnowledgeApi("UpdateUser", "process begin")
        result = update_user(db, request_frame, session_user)
        logger.logKnowledgeApi("UpdateUser", "process end")

    if type(request_frame) is admin.ChangeUserStatus:
        logger.logKnowledgeApi("ChangeUserStatus", "process begin")
        result = change_user_status(db, request_frame, session_user)
        logger.logKnowledgeApi("ChangeUserStatus", "process end")
    return result


########################################################
# To Retrieve category wise forms from database
########################################################
def get_forms_list(db) :
    result_rows = get_forms(db)
    knowledge_forms = []
    techno_forms = []
    for row in result_rows:
        parent_menu = None if row[8] == None else row[8]
        if int(row[1]) == 2:
            form = core.Form(
                form_id=row[0],
                form_name=row[5],
                form_url=row[6],
                parent_menu=parent_menu,
                form_type=row[4]
            )
            knowledge_forms.append(form)
        elif int(row[1]) == 3:
            form = core.Form(
                form_id=row[0],
                form_name=row[5],
                form_url=row[6],
                parent_menu=parent_menu,
                form_type=row[4]
            )
            techno_forms.append(form)
        else:
            form = core.Form(
                form_id=row[0],
                form_name=row[5],
                form_url=row[6],
                parent_menu=parent_menu,
                form_type=row[4]
            )
            knowledge_forms.append(form)
            if form.form_name == "Audit Trail":
                techno_forms.append(form)

    result = {}
    result[2] = process_user_menus(knowledge_forms)
    result[3] = process_user_menus(techno_forms)
    return result

########################################################
# To get list of user groups with it's details such as
# forms, form categories
########################################################
def process_user_group_detailed_list(db):
    user_group_list = []
    rows = get_user_group_detailed_list(db)
    for row in rows:
        user_group_id = int(row[0])
        user_group_name = row[1]
        form_category_id = row[2]
        no_of_users = row[5]
        if len(row[3]) >= 1 :
            form_ids = [int(x) for x in row[3].split(",")]
        else :
            form_ids = []
        is_active = False if row[4] == 0 else True
        user_group_list.append(admin.UserGroup(
            user_group_id, user_group_name,
            form_category_id, form_ids, is_active, no_of_users
        ))
    return user_group_list

########################################################
# To get form categories list
########################################################
def get_form_categories(db):
    formCategoryList = []
    rows = get_form_categories(db)
    for row in rows:
        formCategoryList.append(core.FormCategory(row[0], row[1]))
    return formCategoryList

########################################################
# To handle get user group list request
########################################################
def get_user_groups(db, request_frame, session_user):
    forms = get_forms_list(db)
    form_categories = get_form_categories(db)
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
def save_user_group(db, request, session_user):
    user_group_name = request.user_group_name
    form_category_id = request.form_category_id
    form_ids = request.form_ids
    if is_duplicate_user_group_name(db, user_group_name, user_group_id) :
        return admin.GroupNameAlreadyExists()
    elif save_user_group(
        db,
        user_group_name,
        form_category_id, form_ids
    ):
        return admin.SaveUserGroupSuccess()

########################################################
# To Handle Update user group request
########################################################
def update_user_group(db, request, session_user):
    user_group_id = request.user_group_id
    user_group_name = request.user_group_name
    form_category_id = request.form_category_id
    form_ids = request.form_ids
    if db.is_invalid_id(tblUserGroups, "user_group_id", user_group_id) :
        return admin.InvalidUserGroupId()
    elif is_duplicate_user_group_name(db, user_group_name, user_group_id) :
        return admin.GroupNameAlreadyExists()
    elif update_user_group(
        db,
        user_group_id, user_group_name,
        form_category_id, form_ids
    ) :
        return admin.UpdateUserGroupSuccess()

########################################################
# To Change the status of user group
########################################################
def change_user_group_status(db, request, session_user):
    user_group_id = request.user_group_id
    is_active = 0 if request.is_active is False else 1
    if db.is_invalid_id(tblUserGroups, "user_group_id", user_group_id):
        return admin.InvalidUserGroupId()
    elif is_user_exists_under_user_group(
        db, request.user_group_id
    ):
        return admin.CannotDeactivateUserExists()
    elif update_user_group_status(db, user_group_id, is_active):
        return admin.ChangeUserGroupStatusSuccess()

########################################################
# To get Users List with user details
########################################################
def get_users(db, request_frame, session_user):
    domain_list = get_domains_for_user(db, 0)
    country_list = get_countries_for_user(db, 0)
    user_group_list = []
    user_list = []

    user_group_rows = get_user_groups(db)
    for user_group_row in user_group_rows:
        user_group_id = user_group_row[0]
        user_group_name = user_group_row[1]
        is_active = True if user_group_row[2] == 1 else False
        user_group_list.append(core.UserGroup(user_group_id, user_group_name, is_active))

    user_rows = get_detailed_user_list(db)
    # columns = "user_id, email_id, user_group_id, employee_name, employee_code, " + \
    #         "contact_no, address, designation, is_active"
    for user_row in user_rows:
        user_id = user_row[0]
        email_id = user_row[1]
        user_group_id = user_row[2]
        employee_name = user_row[3]
        employee_code = user_row[4]
        contact_no = user_row[5]
        address = None if user_row[6] == "" else user_row[6]
        designation = None if user_row[7] == "" else user_row[7]
        is_active = True if user_row[8] == 1 else False
        country_ids = [int(x) for x in get_user_countries(db, user_id).split(",")]
        domain_ids = [int(x) for x in get_user_domains(db, user_id).split(",")]
        user_list.append(
            core.UserDetails(
                user_id, email_id, user_group_id,
                employee_name, employee_code, contact_no, address, designation,
                country_ids, domain_ids, is_active
            )
        )

    return admin.GetUsersSuccess(
        user_groups=user_group_list,
        countries=country_list,
        domains=domain_list,
        users=user_list
    )

########################################################
# To Handle Save user request
########################################################
def save_user(db, request, session_user):
    # user_id = db.generate_new_user_id()
    email_id = request.email_id
    user_group_id = request.user_group_id
    employee_name = request.employee_name
    employee_code = request.employee_code
    contact_no = request.contact_no
    address = None if request.address == "" else request.address
    designation = None if request.designation == "" else request.designation
    country_ids = request.country_ids
    domain_ids = request.domain_ids
    if is_duplicate_email(db, email_id, user_id) :
        return admin.EmailIDAlreadyExists()
    elif is_duplicate_employee_code(db, employee_code, user_id) :
        return admin.EmployeeCodeAlreadyExists()
    elif save_user(
        db, email_id, user_group_id, employee_name,
        employee_code, contact_no, address, designation, country_ids, domain_ids
    ) :
        return admin.SaveUserSuccess()

########################################################
# To Handle Update user request
########################################################
def update_user(db, request, session_user):
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
    elif is_duplicate_employee_code(db, employee_code, user_id) :
        return admin.EmployeeCodeAlreadyExists()
    elif update_user(
        db, user_id, user_group_id, employee_name, employee_code,
        contact_no, address, designation, country_ids, domain_ids
    ) :
        return admin.UpdateUserSuccess()

########################################################
# To Change the status of user
########################################################
def change_user_status(db, request, session_user):
    user_id = request.user_id
    is_active = 0 if request.is_active is False else 1
    if db.is_invalid_id(tblUsers, "user_id", user_id):
        return admin.InvalidUserId()
    elif update_user_status(db, user_id, is_active):
        return admin.ChangeUserStatusSuccess()
