from server.controller.corecontroller import process_user_forms
from server.emailcontroller import EmailHandler as email
from protocol import login, mobile
from server.constants import (
    CLIENT_URL
)
from server import logger

__all__ = [
    "process_login_request",
    "process_login", "process_forgot_password",
    "process_reset_token",
    "process_reset_password",
    "process_change_password",
    "process_logout"
]

def process_login_request(request, db, company_id, session_user_ip) :
    if type(request) is login.Login:
        logger.logClientApi("Login", "begin")
        result = process_login(db, request, company_id, session_user_ip)
        logger.logClientApi("Login", "end")

    elif type(request) is login.ForgotPassword :
        logger.logClientApi("ForgotPassword", "begin")
        result = process_forgot_password(db, request)
        logger.logClientApi("ForgotPassword", "end")

    elif type(request) is login.ResetTokenValidation :
        logger.logClientApi("ResetTokenValidation", "begin")
        result = process_reset_token(db, request)
        logger.logClientApi("ResetTokenValidation", "end")

    elif type(request) is login.ResetPassword :
        logger.logClientApi("ResetPassword", "begin")
        result = process_reset_password(db, request)
        logger.logClientApi("ResetPassword", "end")

    elif type(request) is login.ChangePassword :
        logger.logClientApi("ResetPassword", "begin")
        result = process_change_password(db, request)
        logger.logClientApi("ResetPassword", "end")

    elif type(request) is login.Logout:
        logger.logClientApi("Logout", "begin")
        result = process_logout(db, request)
        logger.logClientApi("Logout", "end")

    return result

def process_login(db, request, client_id, session_user_ip):
    login_type = request.login_type
    username = request.username
    password = request.password
    encrypt_password = db.encrypt(password)
    user_ip = session_user_ip
    logger.logLogin("info", user_ip, username, "Login process begin")
    if db.is_contract_not_started():
        print "inside contract not startd"
        return login.ContractNotYetStarted()
    elif not db.is_configured():
        logger.logLogin("info", user_ip, username, "NotConfigured")
        return login.NotConfigured()
    elif not db.is_in_contract():
        logger.logLogin("info", user_ip, username, "ContractExpired")
        return login.ContractExpired()
    elif not db.is_client_active(client_id):
        logger.logLogin("info", user_ip, username, "InvalidCredentials")
        return login.InvalidCredentials()
    else:
        response = db.verify_login(username, encrypt_password)
    if login_type.lower() == "web":
        if response is True:
            logger.logLogin("info", user_ip, username, "Login process end")
            return admin_login_response(db, client_id, user_ip)
        else :
            if type(response) is not bool:
                logger.logLogin("info", user_ip, username, "Login process end")
                return user_login_response(db, response, client_id, user_ip)
            else :
                logger.logLogin("info", user_ip, username, "Login process end")
                return login.InvalidCredentials()
    else :
        if response is True :
            logger.logLogin("info", user_ip, username, "Login process end")
            return mobile_user_admin_response(db, login_type, client_id, user_ip)
        else :
            if type(response) is not bool:
                logger.logLogin("info", user_ip, username, "Login process end")
                return mobile_user_login_respone(db, response, login_type, client_id, user_ip)
            else :
                logger.logLogin("info", user_ip, username, "Login process end")
                return login.InvalidCredentials()


def mobile_user_admin_response(db, login_type, client_id, ip):
    if login_type.lower() == "web" :
        session_type = 1
    elif login_type.lower() == "android" :
        session_type = 2
    elif login_type.lower() == "ios" :
        session_type = 3
    elif login_type.lower() == "blackberry" :
        session_type = 4

    column = "admin_id"
    condition = "1"
    rows = db.get_data(db.tblAdmin, column, condition)
    user_id = rows[0][0]
    session_token = db.add_session(
        user_id, session_type, ip, "Administrator", client_id
    )
    form_ids = db.get_form_ids_for_admin()
    menu = process_user_forms(db, form_ids, client_id, 1)
    employee_name = "Administrator"
    client_info = db.get_client_group()
    group_name = client_info["group_name"]
    group_id = client_info["client_id"]
    configuration = db.get_client_configuration()

    return mobile.ClientUserLoginResponseSuccess(
        user_id,
        employee_name,
        session_token,
        group_id,
        group_name,
        configuration,
        menu
    )

def mobile_user_login_respone(db, data, login_type, client_id, ip):
    if login_type.lower() == "web" :
        session_type = 1
    elif login_type.lower() == "android" :
        session_type = 2
    elif login_type.lower() == "ios" :
        session_type = 3
    elif login_type.lower() == "blackberry" :
        session_type = 4
    user_id = data["user_id"]
    employee_name = data["employee_name"]
    employee_code = data["employee_code"]
    employee = "%s - %s" % (employee_code, employee_name)
    session_token = db.add_session(user_id, session_type, ip, employee, client_id)
    client_info = db.get_client_group()
    group_name = client_info["group_name"]
    group_id = client_info["client_id"]
    configuration = db.get_client_configuration()
    form_ids = data["form_ids"]
    is_promoted_admin = int(data["is_admin"])
    if is_promoted_admin == 1:
        form_ids = "%s, 3, 4, 6, 7, 8" % (form_ids)
        form_ids_list = form_ids.split(",")
        if 1 not in form_ids_list:
            form_ids_list.append(1)
        report_form_ids = db.get_report_form_ids().split(",")
        for form_id in report_form_ids:
            if form_id not in form_ids_list:
                form_ids_list.append(form_id)
        form_ids = ",".join(str(x) for x in form_ids_list)
    menu = process_user_forms(db, form_ids, client_id, 0)
    return mobile.ClientUserLoginResponseSuccess(
        data["user_id"],
        data["employee_name"],
        session_token,
        group_id,
        group_name,
        configuration,
        menu
    )

def user_login_response(db, data, client_id, ip):
    user_id = data["user_id"]
    email_id = data["email_id"]
    session_type = 1  # web
    employee_name = data["employee_name"]
    employee_code = data["employee_code"]
    employee = "%s - %s" % (employee_code, employee_name)
    session_token = db.add_session(user_id, session_type, ip, employee, client_id)
    contact_no = data["contact_no"]
    user_group_name = data["user_group_name"]
    form_ids = data["form_ids"]
    is_promoted_admin = int(data["is_admin"])
    if is_promoted_admin == 1:
        form_ids = "%s, 3, 4, 6, 7, 8, 24" % (form_ids)
        form_ids_list = form_ids.split(",")
        if 1 not in form_ids_list:
            form_ids_list.append(1)
        report_form_ids = db.get_report_form_ids().split(",")
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
    column = "admin_id"
    condition = "1"
    rows = db.get_data(db.tblAdmin, column, condition)
    user_id = rows[0][0]
    email_id = None
    session_type = 1  # web
    session_token = db.add_session(
        user_id, session_type, ip, "Administrator", client_id
    )
    form_ids = db.get_form_ids_for_admin()
    menu = process_user_forms(db, form_ids, client_id, 1)
    employee_name = "Administrator"
    return login.AdminLoginSuccess(
        user_id, session_token, email_id, menu, employee_name, client_id
    )

def process_forgot_password(db, request):
    user_id = db.verify_username(request.username)
    if user_id is not None:
        send_reset_link(db, user_id, request.username, request.short_name)
        return login.ForgotPasswordSuccess()
    else:
        return login.InvalidUserName()

def send_reset_link(db, user_id, username, short_name):
    reset_token = db.new_uuid()
    reset_link = "%sreset_password/%s/%s" % (
        CLIENT_URL, short_name, reset_token)

    condition = "user_id = '%d' " % user_id
    db.delete(db.tblEmailVerification, condition)

    columns = ["user_id", "verification_code"]
    values_list = [user_id, reset_token]
    if db.insert(db.tblEmailVerification, columns, values_list):
        if email().send_reset_link(db, user_id, username, reset_link):
            return True
        else:
            print "Send email failed"
    else:
        print "Saving reset token failed"

def process_reset_token(db, request):
    client_id = db.get_client_id_from_short_name(request.short_name)
    user_id = db.validate_reset_token(request.reset_token, client_id)
    if user_id is not None:
        return login.ResetSessionTokenValidationSuccess()
    else:
        return login.InvalidResetToken()

def process_reset_password(db, request):
    client_id = db.get_client_id_from_short_name(request.short_name)
    user_id = db.validate_reset_token(request.reset_token, client_id)
    if user_id is not None:
        db.update_password(request.new_password, user_id, client_id)
        db.delete_used_token(request.reset_token, client_id)
        return login.ResetPasswordSuccess()
    else:
        return login.InvalidResetToken()

def process_change_password(db, request):
    client_info = request.session_token.split("-")
    session_token = "{}-{}".format(client_info[0],client_info[2])
    client_id = int(client_info[0])
    session_user = db.validate_session_token(client_id, session_token)
    if db.verify_password(request.current_password, session_user, client_id):
        db.update_password(request.new_password, session_user, client_id)
        return login.ChangePasswordSuccess()
    else :
        return login.InvalidCurrentPassword()


def process_logout(db, request):
    # save logout time
    return login.LogoutSuccess()
