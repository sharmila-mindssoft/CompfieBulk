from server.clientdatabase.tables import *
from server.emailcontroller import EmailHandler as email
from clientprotocol import clientlogin, clientmobile
from server.constants import (
    CLIENT_URL, CAPTCHA_LENGTH, NO_OF_FAILURE_ATTEMPTS
)
from server import logger
from server.clientdatabase.login import *

from server.common import (
    encrypt, new_uuid, generate_random
)

from server.clientdatabase.general import (
    get_form_ids_for_admin, get_report_form_ids,
    verify_username,
    validate_reset_token, update_password, delete_used_token,
    remove_session, update_profile, verify_password, get_user_name_by_id,
    get_user_forms, get_forms_by_category, get_legal_entity_info, get_country_info, get_themes
    )
from server.exceptionmessage import client_process_error
from server.clientcontroller.corecontroller import process_user_forms
from server.clientdatabase.savetoknowledge import *

__all__ = [
    "process_login_request",
    "process_login", "process_forgot_password",
    "process_reset_token",
    "process_reset_password",
    "process_change_password",
    "process_logout"
]


def process_login_request(
    request, db, company_id, session_user_ip
):
    print "process_login_request============================="

    if type(request) is clientlogin.Login:
        logger.logClientApi("Login", "begin")
        result = process_login(db, request, company_id, session_user_ip)
        logger.logClientApi("Login", "end")
    elif type(request) is clientlogin.ForgotPassword:
        logger.logClientApi("ForgotPassword", "begin")
        result = process_forgot_password(db, request)
        logger.logClientApi("ForgotPassword", "end")

    elif type(request) is clientlogin.ResetTokenValidation:
        logger.logClientApi("ResetTokenValidation", "begin")
        result = process_reset_token(db, request)
        logger.logClientApi("ResetTokenValidation", "end")

    elif type(request) is clientlogin.ResetPassword:
        logger.logClientApi("ResetPassword", "begin")
        result = process_reset_password(db, request)
        logger.logClientApi("ResetPassword", "end")

    elif type(request) is clientlogin.ChangePassword:
        logger.logClientApi("ResetPassword", "begin")
        result = process_change_password(db, company_id, request)
        logger.logClientApi("ResetPassword", "end")

    elif type(request) is clientlogin.Logout:
        logger.logClientApi("Logout", "begin")
        result = process_logout(db, request)
        logger.logClientApi("Logout", "end")

    elif type(request) is clientlogin.UpdateUserProfile:
        logger.logClientApi("UpdateUserProfile", "begin")
        result = process_update_profile(db, request)
        logger.logClientApi("UpdateUserProfile", "end")

    elif type(request) is clientlogin.CheckRegistrationToken:
        print "login-controller>>72"
        result = process_validate_rtoken(db, request)

    elif type(request) is clientlogin.SaveRegistration:
        result = process_save_logindetails(db, request, company_id)

    elif type(request) is clientlogin.CheckUsername:
        result = process_check_username(db, request)

    return result


def invalid_credentials(db, user_id, session_user_ip):
    save_login_failure(db, user_id, session_user_ip)
    rows = get_login_attempt_and_time(db, user_id)
    no_of_attempts = 0
    if rows:
        no_of_attempts = rows[0]["login_attempt"]
    if no_of_attempts >= NO_OF_FAILURE_ATTEMPTS:
        captcha_text = generate_random(CAPTCHA_LENGTH)
    else:
        captcha_text = None
    return clientlogin.InvalidCredentials(captcha_text)


def process_login(db, request, client_id, session_user_ip):
    login_type = request.login_type
    username = request.username
    password = request.password
    short_name = request.short_name
    encrypt_password = encrypt(password)
    user_ip = session_user_ip
    logger.logLogin("info", user_ip, username, "Login process begin")
    user_id = verify_username(db, username)
    if user_id is None:
        return clientlogin.InvalidCredentials(None)
    else:
        response = verify_login(db, username, encrypt_password)
        print response
    if login_type.lower() == "web":
        if response is "ContractExpired":
            logger.logLogin("info", user_ip, username, "ContractExpired")
            return clientlogin.ContractExpired()
        elif response is False:
            logger.logLogin("info", user_ip, username, "Login process end")
            return invalid_credentials(db, user_id, session_user_ip)
        else:
            print "user_login_response"
            logger.logLogin("info", user_ip, username, "Login process end")
            delete_login_failure_history(db, user_id)
            return user_login_response(db, response, client_id, user_ip, short_name)

    else:
        if response is True:
            logger.logLogin("info", user_ip, username, "Login process end")
            delete_login_failure_history(db, user_id)
            return mobile_user_admin_response(
                db, login_type, client_id, user_ip
            )
        else:
            if response is "ContractExpired":
                logger.logLogin("info", user_ip, username, "ContractExpired")
                return clientlogin.ContractExpired()
            elif response is False:
                logger.logLogin("info", user_ip, username, "Login process end")
                return invalid_credentials(db, user_id, session_user_ip)
            else:
                logger.logLogin("info", user_ip, username, "Login process end")
                delete_login_failure_history(db, user_id)
                return mobile_user_login_respone(
                    db, response, login_type, client_id, user_ip
                )


def mobile_user_admin_response(db, login_type, client_id, ip):
    if login_type.lower() == "web":
        session_type = 1
    elif login_type.lower() == "android":
        session_type = 2
    elif login_type.lower() == "ios":
        session_type = 3
    elif login_type.lower() == "blackberry":
        session_type = 4

    column = "user_id"
    condition = " is_active = 1 and is_primary_admin = 1 "
    rows = db.get_data(tblUsers, column, condition)
    user_id = rows[0]["user_id"]
    session_token = add_session(
        db, user_id, session_type, ip, "Administrator", client_id
    )
    # menu = process_user_forms(db, form_ids, client_id, 1)
    employee_name = "Administrator"
    client_info = get_client_group(db)
    group_name = client_info["group_name"]
    group_id = client_info["client_id"]
    configuration = get_client_configuration(db)

    return clientmobile.ClientUserLoginResponseSuccess(
        user_id,
        employee_name,
        session_token,
        group_id,
        group_name,
        configuration,
        True, True, True
    )


def mobile_user_login_respone(db, data, login_type, client_id, ip):
    if login_type.lower() == "web":
        session_type = 1
    elif login_type.lower() == "android":
        session_type = 2
    elif login_type.lower() == "ios":
        session_type = 3
    elif login_type.lower() == "blackberry":
        session_type = 4
    user_id = data["user_id"]
    employee_name = data["employee_name"]
    employee_code = data["employee_code"]
    employee = "%s - %s" % (employee_code, employee_name)
    session_token = add_session(
        db, user_id, session_type, ip, employee, client_id
    )
    client_info = get_client_group(db)
    group_name = client_info["group_name"]
    group_id = client_info["client_id"]
    configuration = get_client_configuration(db)
    form_ids = data["form_ids"]
    is_promoted_admin = int(data["is_admin"])
    if is_promoted_admin == 1:
        form_ids = "%s, 3, 4, 6, 7, 8" % (form_ids)
        form_ids_list = form_ids.split(",")
        if 1 not in form_ids_list:
            form_ids_list.append(1)
        report_form_ids = get_report_form_ids(db).split(",")
        for form_id in report_form_ids:
            if form_id not in form_ids_list:
                form_ids_list.append(form_id)
        form_ids = ",".join(str(x) for x in form_ids_list)
    form_ids = [int(x) for x in form_ids.split(",")]
    dashboard = compliance_task = compliance_approve = False
    if 1 in form_ids :
        dashboard = True
    if 11 in form_ids :
        compliance_task = True
    if 9 in form_ids :
        compliance_approve = True
    # menu = process_user_forms(db, form_ids, client_id, 0)
    return clientmobile.ClientUserLoginResponseSuccess(
        data["user_id"],
        data["employee_name"],
        session_token,
        group_id,
        group_name,
        configuration,
        dashboard,
        compliance_task,
        compliance_approve
    )


def user_login_response(db, data, client_id, ip, short_name):
    cat_id = data["user_category_id"]
    user_id = data["user_id"]
    email_id = data["email_id"]
    address = data["address"]
    session_type = 1  # web
    employee_name = data["employee_name"]
    employee_code = data["employee_code"]
    if employee_code is None :
        employee = employee_name
    else :
        employee = "%s - %s" % (employee_code, employee_name)
    username = data["username"]
    mobile_no = data["mobile_no"]
    session_token = add_session(
        db, cat_id, user_id, session_type, ip, employee, client_id
    )
    contact_no = data["contact_no"]
    user_group_name = data["user_group_name"]
    le_info = get_legal_entity_info(db, user_id, cat_id)
    c_info = get_country_info(db, user_id, cat_id)
    theme = get_themes(db, user_id)

    if len(le_info) == 0:
        return clientlogin.LegalEntityNotAvailable()
    if cat_id == 1 :
        forms = get_forms_by_category(db, cat_id)
    else :
        forms = get_user_forms(db, user_id, cat_id)
    print forms
    menu = process_user_forms(
        db, forms, short_name
    )

    return clientlogin.UserLoginSuccess(
        user_id, session_token, email_id, user_group_name,
        menu, employee_name, employee_code, contact_no, address,
        client_id, username, mobile_no, le_info, c_info, theme
    )


def admin_login_response(db, client_id, ip):
    column = "user_id"
    condition = " is_active = 1 and is_primary_admin = 1"
    rows = db.get_data(tblUsers, column, condition)
    user_id = rows[0]["user_id"]
    email_id = None
    session_type = 1  # web
    session_token = add_session(
        db, user_id, session_type, ip, "Administrator", client_id
    )
    form_ids = get_form_ids_for_admin(db)
    menu = process_user_forms(db, form_ids, client_id, 1)
    employee_name = "Administrator"
    return clientlogin.AdminLoginSuccess(
        user_id, session_token, email_id, menu, employee_name, client_id
    )


def process_forgot_password(db, request):
    user_id = verify_username(db, request.username)
    if user_id is not None:
        send_reset_link(db, user_id, request.username, request.short_name)
        return clientlogin.ForgotPasswordSuccess()
    else:
        return clientlogin.InvalidUserName()


def send_reset_link(db, user_id, username, short_name):
    reset_token = new_uuid()
    reset_link = "%sreset_password/%s/%s" % (
        CLIENT_URL, short_name, reset_token)

    condition = "user_id = %s "
    db.delete(tblEmailVerification, condition, [user_id])

    columns = ["user_id", "verification_code"]
    values_list = [user_id, str(reset_token)]
    row_id = db.insert(tblEmailVerification, columns, values_list)
    employee_name = get_user_name_by_id(db, user_id)
    if(row_id >= 0):
        if email().send_reset_link(
            db, user_id, username, reset_link, employee_name
        ):
            return True
        else:
            raise client_process_error("E028")
    else:
        raise client_process_error("E029")


def process_reset_token(db, request):
    user_id = validate_reset_token(db, request.reset_token)
    if user_id is not None:
        return clientlogin.ResetSessionTokenValidationSuccess()
    else:
        return clientlogin.InvalidResetToken()


def process_reset_password(db, request):
    user_id = validate_reset_token(db, request.reset_token)
    if user_id is not None:
        update_password(db, request.new_password, user_id)
        delete_used_token(db, request.reset_token)
        return clientlogin.ResetPasswordSuccess()
    else:
        return clientlogin.InvalidResetToken()


def process_change_password(db, company_id, request):
    client_info = request.session_token.split("-")

    # session_token = "%s-%s" % (
    #     client_info[0], client_info[2]
    # )
    session_token = "%s-%s" % (
        company_id, client_info[2]
    )
    print session_token
    # client_id = int(client_info[0])
    user_details = db.validate_session_token(session_token)
    session_user = int(user_details[0])
    if verify_password(db, request.current_password, session_user):
        update_password(db, request.new_password, session_user)
        return clientlogin.ChangePasswordSuccess()
    else:
        return clientlogin.InvalidCurrentPassword()


def process_logout(db, request):
    # save logout time
    session = request.session_token
    remove_session(db, session)
    return clientlogin.LogoutSuccess()


def process_update_profile(db, request):
    client_info = request.session_token.split("-")
    session_token = "%s- %s" % (
        client_info[0],  client_info[1]
    )
    session_user = db.validate_session_token(session_token)
    update_profile(db, request.contact_no, request.address, session_user)
    return clientlogin.UpdateUserProfileSuccess(request.contact_no, request.address)

#############################################################################
# Check Registration Token Valid
#############################################################################
def process_validate_rtoken(db, request):
    token = request.reset_token
    if validate_email_token(db, token):
        captcha_text = generate_random(CAPTCHA_LENGTH)
        return clientlogin.CheckRegistrationTokenSuccess(captcha_text)
    else:
        return clientlogin.InvalidSessionToken()
#############################################################################
# Check Registration Token Valid
#############################################################################
def process_save_logindetails(db, request, company_id):
    username = request.username
    password = request.password
    # duplication username validation
    if check_username_duplicate(db, username) is False:
        return clientlogin.UsernameAlreadyExists()
    else:
        encrypt_password = encrypt(password)
        token = request.token
        if save_login_details(db, token, username, encrypt_password, company_id):
            return clientlogin.SaveRegistrationSuccess()
        else:
            return clientlogin.InvalidSessionToken()
#############################################################################
# Check Registration Token Valid
#############################################################################
def process_check_username(db, request):
    uname = request.username

    if check_username_duplicate(db, uname):
        return clientlogin.CheckUsernameSuccess()
    else :
        return clientlogin.UsernameAlreadyExists()

