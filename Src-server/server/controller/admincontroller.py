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
        logger.logClientApi("GetUserGroups", " process begin")
        result = get_user_groups(db, request_frame, session_user)
        logger.logClientApi("GetUserGroups", "process end")

    if type(request_frame) is admin.SaveUserGroup:
        logger.logClientApi("SaveUserGroup", "process begin")
        result = save_user_group(db, request_frame, session_user)
        logger.logClientApi("SaveUserGroup", "process end")

    if type(request_frame) is admin.UpdateUserGroup:
        logger.logClientApi("UpdateUserGroup", "process begin")
        result = update_user_group(db, request_frame, session_user)
        logger.logClientApi("UpdateUserGroup", "process end")

    if type(request_frame) is admin.ChangeUserGroupStatus:
        logger.loginClientApi("ChangeUserGroupStatus", "process begin")
        result = change_user_group_status(db, request_frame, session_user)
        logger.loginClientApi("ChangeUserGroupStatus", "process end")

    if type(request_frame) is admin.GetUsers:
        logger.loginClientApi("GetUsers", "process begin")
        result = get_users(db, request_frame, session_user)
        logger.loginClientApi("ChangeUserGroupStatus", "process end")

    if type(request_frame) is admin.SaveUser:
        logger.loginClientApi("SaveUser", "process begin")
        result = save_user(db, request_frame, session_user)
        logger.loginClientApi("SaveUser", "process end")

    if type(request_frame) is admin.UpdateUser:
        logger.loginClientApi("UpdateUser", "process begin")
        result = update_user(db, request_frame, session_user)
        logger.loginClientApi("UpdateUser", "process end")

    if type(request_frame) is admin.ChangeUserStatus:
        logger.loginClientApi("ChangeUserStatus", "process begin")
        result = change_user_status(db, request_frame, session_user)
        logger.loginClientApi("ChangeUserStatus", "process begin")
    return result


########################################################
# To Retrieve category wise forms from database
########################################################
def get_forms(db) :
    result_rows = db.get_forms()
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
def get_user_group_detailed_list(db):
    user_group_list = []
    rows = db.get_user_group_detailed_list()
    for row in rows:
        user_group_id = int(row[0])
        user_group_name = row[1]
        form_category_id = row[2]
        no_of_users = row[5]
        if len(row[3]) > 1 :
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
    rows = db.get_form_categories()
    for row in rows:
        formCategoryList.append(core.FormCategory(row[0], row[1]))
    return formCategoryList

########################################################
# To handle get user group list request
########################################################
def get_user_groups(db, request_frame, session_user):
    forms = get_forms(db)
    form_categories = get_form_categories(db)
    user_group_list = get_user_group_detailed_list(db)
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
    user_group_id = db.generate_new_user_group_id()
    if db.is_duplicate_user_group_name(user_group_id, user_group_name) :
        return admin.GroupNameAlreadyExists()
    elif db.save_user_group(
        user_group_id, user_group_name,
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
    if db.is_invalid_id(db.tblUserGroups, "user_group_id", user_group_id) :
        return admin.InvalidUserGroupId()
    elif db.is_duplicate_user_group_name(user_group_id, user_group_name) :
        return admin.GroupNameAlreadyExists()
    elif db.update_user_group(
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
    if db.is_invalid_id(db.tblUserGroups, "user_group_id", user_group_id):
        return admin.InvalidUserGroupId()
    elif db.is_user_exists_under_user_group(
        request.user_group_id
    ):
        return admin.CannotDeactivateUserExists()
    elif db.update_user_group_status(user_group_id, is_active):
        return admin.ChangeUserGroupStatusSuccess()

########################################################
# To get Users List with user details
########################################################
def get_users(db, request_frame, session_user):
    domain_list = db.get_domains_for_user(0)
    country_list = db.get_countries_for_user(0)
    user_group_list = []
    user_list = []

    user_group_rows = db.get_user_groups()
    for user_group_row in user_group_rows:
        user_group_id = user_group_row[0]
        user_group_name = user_group_row[1]
        is_active = True if user_group_row[2] == 1 else False
        user_group_list.append(core.UserGroup(user_group_id, user_group_name, is_active))

    user_rows = db.get_detailed_user_list()
    columns = "user_id, email_id, user_group_id, employee_name, employee_code, " + \
            "contact_no, address, designation, is_active"
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
        country_ids = [int(x) for x in db.get_user_countries(user_id).split(",")]
        domain_ids = [int(x) for x in db.get_user_domains(user_id).split(",")]
        user_list.append(core.UserDetails(user_id, email_id, user_group_id,
            employee_name, employee_code, contact_no, address, designation,
            country_ids, domain_ids, is_active))

    return admin.GetUsersSuccess(user_groups = user_group_list,
        countries = country_list, domains=domain_list, users=user_list)

########################################################
# To Handle Save user request
########################################################
def save_user(db, request, session_user):
    user_id = db.generate_new_user_id()
    email_id = request.email_id
    user_group_id = request.user_group_id
    employee_name = request.employee_name
    employee_code = request.employee_code
    contact_no = request.contact_no
    address =  None if request.address == "" else request.address
    designation =  None if request.designation == "" else request.designation
    country_ids = request.country_ids
    domain_ids = request.domain_ids
    if db.is_duplicate_email(email_id, user_id) :
        return admin.EmailIDAlreadyExists()
    elif db.is_duplicate_employee_code(employee_code, user_id) :
        return admin.EmployeeCodeAlreadyExists()
    elif db.save_user(user_id, email_id, user_group_id, employee_name,
     employee_code, contact_no, address, designation, country_ids, domain_ids) :
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
    address =  request.address
    designation =  request.designation
    country_ids = request.country_ids
    domain_ids = request.domain_ids
    if db.is_invalid_id(db.tblUsers, "user_id", user_id):
        return admin.InvalidUserId()
    elif db.is_duplicate_employee_code(employee_code, user_id) :
        return admin.EmployeeCodeAlreadyExists()
    elif db.update_user(user_id, user_group_id, employee_name, employee_code,
        contact_no, address, designation, country_ids, domain_ids) :
        return admin.UpdateUserSuccess()

########################################################
# To Change the status of user
########################################################
def change_user_status(db, request, session_user):
    user_id = request.user_id
    is_active = 0 if request.is_active == False else 1
    if db.is_invalid_id(db.tblUsers, "user_id", user_id):
        return admin.InvalidUserId()
    elif db.update_user_status(user_id, is_active):
        return admin.ChangeUserStatusSuccess()
