from server.clientdatabase.tables import *
from server.controller.corecontroller import process_user_forms
from server.emailcontroller import EmailHandler as email
from protocol import login, mobile
from server.constants import (
    CLIENT_URL, CAPTCHA_LENGHT, NO_OF_FAILURE_ATTEMPTS
)
from server import logger
from server.clientdatabase.login import *

from server.common import (
    encrypt, new_uuid, generate_random
)

from server.clientdatabase.general import (
    get_form_ids_for_admin, get_report_form_ids,
    verify_username, get_client_id_from_short_name,
    validate_reset_token, update_password, delete_used_token,
    remove_session, update_profile, verify_password
    )

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
    if type(request) is login.Login:
        logger.logClientApi("Login", "begin")
        result = process_login(db, request, company_id, session_user_ip)
        logger.logClientApi("Login", "end")
    elif type(request) is login.ForgotPassword:
        logger.logClientApi("ForgotPassword", "begin")
        result = process_forgot_password(db, request)
        logger.logClientApi("ForgotPassword", "end")

    elif type(request) is login.ResetTokenValidation:
        logger.logClientApi("ResetTokenValidation", "begin")
        result = process_reset_token(db, request)
        logger.logClientApi("ResetTokenValidation", "end")

    elif type(request) is login.ResetPassword:
        logger.logClientApi("ResetPassword", "begin")
        result = process_reset_password(db, request)
        logger.logClientApi("ResetPassword", "end")

    elif type(request) is login.ChangePassword:
        logger.logClientApi("ResetPassword", "begin")
        result = process_change_password(db, request)
        logger.logClientApi("ResetPassword", "end")

    elif type(request) is login.Logout:
        logger.logClientApi("Logout", "begin")
        result = process_logout(db, request)
        logger.logClientApi("Logout", "end")

    elif type(request) is login.UpdateUserProfile:
        logger.logClientApi("Logout", "begin")
        result = process_update_profile(db, request)
        logger.logClientApi("Logout", "end")

    return result


def invalid_credentials(db, user_id, session_user_ip):
    save_login_failure(db, user_id, session_user_ip)
    rows = get_login_attempt_and_time(db, user_id)
    no_of_attempts = 0
    if rows:
        no_of_attempts = rows[0]["login_attempt"]
    if no_of_attempts >= NO_OF_FAILURE_ATTEMPTS:
        captcha_text = generate_random(CAPTCHA_LENGHT)
    else:
        captcha_text = None
    return login.InvalidCredentials(captcha_text)


def process_login(db, request, client_id, session_user_ip):
    login_type = request.login_type
    username = request.username
    password = request.password
    encrypt_password = encrypt(password)
    user_ip = session_user_ip
    logger.logLogin("info", user_ip, username, "Login process begin")
    user_id = verify_username(db, username)
    if user_id is None:
        return login.InvalidUserName()
    elif is_contract_not_started(db):
        return login.ContractNotYetStarted()
    elif not is_configured(db):
        logger.logLogin("info", user_ip, username, "NotConfigured")
        return login.NotConfigured()
    elif not is_in_contract(db):
        logger.logLogin("info", user_ip, username, "ContractExpired")
        return login.ContractExpired()
    elif not is_client_active(client_id):
        logger.logLogin("info", user_ip, username, "InvalidCredentials")
        return invalid_credentials(db, user_id, session_user_ip)
    else:
        response = verify_login(db, username, encrypt_password)
    if login_type.lower() == "web":
        if response is True:
            logger.logLogin("info", user_ip, username, "Login process end")
            delete_login_failure_history(db, user_id)
            return admin_login_response(db, client_id, user_ip)
        else:
            if response is "ContractExpired":
                logger.logLogin("info", user_ip, username, "ContractExpired")
                return login.ContractExpired()
            elif response is False:
                logger.logLogin("info", user_ip, username, "Login process end")
                return invalid_credentials(db, user_id, session_user_ip)
            else:
                logger.logLogin("info", user_ip, username, "Login process end")
                delete_login_failure_history(db, user_id)
                return user_login_response(db, response, client_id, user_ip)

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
                return login.ContractExpired()
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
    # form_ids = get_form_ids_for_admin(db)
    # menu = process_user_forms(db, form_ids, client_id, 1)
    employee_name = "Administrator"
    client_info = get_client_group(db)
    group_name = client_info["group_name"]
    group_id = client_info["client_id"]
    configuration = get_client_configuration(db)

    return mobile.ClientUserLoginResponseSuccess(
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
    elif 9 in form_ids :
        compliance_task = True
    elif 11 in form_ids :
        compliance_approve = True
    # menu = process_user_forms(db, form_ids, client_id, 0)
    return mobile.ClientUserLoginResponseSuccess(
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


def user_login_response(db, data, client_id, ip):
    user_id = data["user_id"]
    email_id = data["email_id"]
    session_type = 1  # web
    employee_name = data["employee_name"]
    employee_code = data["employee_code"]
    employee = "%s - %s" % (employee_code, employee_name)
    session_token = add_session(
        db, user_id, session_type, ip, employee, client_id
    )
    contact_no = data["contact_no"]
    user_group_name = data["user_group_name"]
    form_ids = data["form_ids"]
    is_promoted_admin = int(data["is_admin"])
    if is_promoted_admin == 1:
        form_ids = "%s, 3, 4, 6, 7, 8, 24" % (form_ids)
        form_ids_list = form_ids.split(",")
        if 1 not in form_ids_list:
            form_ids_list.append(1)
        report_form_ids = get_report_form_ids(db).split(",")
        for form_id in report_form_ids:
            if form_id not in form_ids_list:
                form_ids_list.append(form_id)
        form_ids = ",".join(str(x) for x in form_ids_list)
    menu = process_user_forms(db, form_ids, client_id, 0)
    return login.UserLoginSuccess(
        user_id, session_token, email_id, user_group_name,
        menu, employee_name, employee_code, contact_no, None, None,
        client_id, bool(is_promoted_admin)
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
    return login.AdminLoginSuccess(
        user_id, session_token, email_id, menu, employee_name, client_id
    )


def process_forgot_password(db, request):
    user_id = verify_username(db, request.username)
    if user_id is not None:
        send_reset_link(db, user_id, request.username, request.short_name)
        return login.ForgotPasswordSuccess()
    else:
        return login.InvalidUserName()


def send_reset_link(db, user_id, username, short_name):
    reset_token = new_uuid()
    reset_link = "%sreset_password/%s/%s" % (
        CLIENT_URL, short_name, reset_token)

    condition = "user_id = '%d' " % user_id
    db.delete(tblEmailVerification, condition)

    columns = ["user_id", "verification_code"]
    values_list = [user_id, reset_token]
    if db.insert(tblEmailVerification, columns, values_list):
        if email().send_reset_link(db, user_id, username, reset_link):
            return True
        else:
            print "Send email failed"
    else:
        print "Saving reset token failed"


def process_reset_token(db, request):
    client_id = get_client_id_from_short_name(db, request.short_name)
    user_id = validate_reset_token(db, request.reset_token, client_id)
    if user_id is not None:
        return login.ResetSessionTokenValidationSuccess()
    else:
        return login.InvalidResetToken()


def process_reset_password(db, request):
    client_id = get_client_id_from_short_name(db, request.short_name)
    user_id = validate_reset_token(db, request.reset_token, client_id)
    if user_id is not None:
        update_password(db, request.new_password, user_id, client_id)
        delete_used_token(db, request.reset_token, client_id)
        return login.ResetPasswordSuccess()
    else:
        return login.InvalidResetToken()


def process_change_password(db, request):
    client_info = request.session_token.split("-")
    session_token = "{}-{}".format(
        client_info[0], client_info[2]
    )
    # client_id = int(client_info[0])
    session_user = db.validate_session_token(session_token)
    if verify_password(db, request.current_password, session_user):
        update_password(db, request.new_password, session_user)
        return login.ChangePasswordSuccess()
    else:
        return login.InvalidCurrentPassword()


def process_logout(db, request):
    # save logout time
    session = request.session_token
    remove_session(db, session)
    return login.LogoutSuccess()


def process_update_profile(db, request):
    client_info = request.session_token.split("-")
    session_token = "{}-{}".format(
        client_info[0],  client_info[1]
    )
    session_user = db.validate_session_token(session_token)
    update_profile(db, request.contact_no, request.address, session_user)
    return login.UpdateUserProfileSuccess(request.contact_no, request.address)
