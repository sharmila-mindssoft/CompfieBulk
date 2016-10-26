from corecontroller import process_admin_forms
from server.emailcontroller import EmailHandler as email
from protocol import login, mobile
from server.constants import (
    KNOWLEDGE_URL, CAPTCHA_LENGTH, NO_OF_FAILURE_ATTEMPTS
)

from server import logger
from server.common import (
    encrypt, new_uuid, generate_random
)
from server.database.tables import *
from server.database.login import *

__all__ = [
    "process_login_request",
    "process_login", "process_forgot_password",
    "process_reset_token",
    "process_reset_password",
    "process_change_password",
    "process_logout"
]


def process_login_request(request, db, session_user_ip):
    if type(request) is login.Login:
        logger.logKnowledgeApi("Login", "process begin")
        result = process_login(db, request, session_user_ip)
        logger.logKnowledgeApi("Login", "process end")

    elif type(request) is login.ForgotPassword:
        logger.logKnowledgeApi("ForgotPassword", "process begin")
        result = process_forgot_password(db, request)
        logger.logKnowledgeApi("ForgotPassword", "process end")

    elif type(request) is login.ResetTokenValidation:
        logger.logKnowledgeApi("ResetTokenValidation", "process begin")
        result = process_reset_token(db, request)
        logger.logKnowledgeApi("ResetTokenValidation", "process end")

    elif type(request) is login.ResetPassword:
        logger.logKnowledgeApi("ResetPassword", "process begin")
        result = process_reset_password(db, request)
        logger.logKnowledgeApi("ResetPassword", "process end")

    elif type(request) is login.ChangePassword:
        logger.logKnowledgeApi("ChangePassword", "process begin")
        result = process_change_password(db, request)
        logger.logKnowledgeApi("ChangePassword", "process end")

    elif type(request) is login.Logout:
        logger.logKnowledgeApi("Logout", "process begin")
        result = process_logout(db, request)
        logger.logKnowledgeApi("Logout", "process end")

    elif type(request) is login.CheckRegistrationToken:
        logger.logKnowledgeApi("CheckRegistrationToken", "process begin")
        result = process_validate_rtoken(db, request)
        logger.logKnowledgeApi("CheckRegistrationToken", "process end")

    elif type(request) is login.SaveRegistraion:
        logger.logKnowledgeApi("SaveRegistraion", "process begin")
        result = process_save_logindetails(db, request)
        logger.logKnowledgeApi("SaveRegistraion", "process end")

    print result

    return result


def process_login(db, request, session_user_ip):
    login_type = request.login_type
    username = request.username
    password = request.password
    encrypt_password = encrypt(password)
    response = verify_login(db, username, encrypt_password)
    verified_username = response[0]
    verified_login = response[1]
    user_info = response[2]
    forms = response[3]
    user_id = verified_username.get('user_id')

    user_category_id = verified_login.get('user_category_id')

    if verified_username.get('username') is None:
        return login.InvalidUserName()
    elif user_id is None:
        save_login_failure(db, user_id, session_user_ip)
        rows = get_login_attempt_and_time(db, user_id)
        no_of_attempts = 0
        if rows:
            no_of_attempts = rows[0]["login_attempt"]
        if no_of_attempts >= NO_OF_FAILURE_ATTEMPTS:
            captcha_text = generate_random(CAPTCHA_LENGTH)
        else:
            captcha_text = None
        return login.InvalidCredentials(captcha_text)

    else:
        if login_type.lower() == "web":
            delete_login_failure_history(db, user_id)
            if user_category_id <= 2:
                return admin_login_response(
                    db, session_user_ip, verified_login, forms)
            else:
                return user_login_response(
                    db, session_user_ip, user_info, forms)
        else:
            pass


def mobile_user_login_respone(db, data, request, ip):
    login_type = request.login_type
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
    form_ids = [int(x) for x in data["form_ids"].split(",")]
    if 11 not in form_ids:
        return login.InvalidMobileCredentials()
    employee = "%s - %s" % (employee_code, employee_name)
    session_token = add_session(db, user_id, session_type, ip, employee)
    return mobile.UserLoginResponseSuccess(
        data["user_id"],
        data["employee_name"],
        session_token
    )

def user_login_response(db, ip, data, forms):
    data = data[0]
    user_id = data["user_id"]
    email_id = data["email_id"]
    session_type = 1  # web
    employee_name = data["employee_name"]
    employee_code = data["employee_code"]
    employee = "%s - %s" % (employee_code, employee_name)
    session_token = add_session(db, user_id, session_type, ip, employee)
    contact_no = data["contact_no"]
    address = None if data["address"] == "" else data["address"]
    designation = None if data["designation"] == "" else data["designation"]
    user_group_name = data["user_group_name"]
    # form_ids = data["form_ids"]
    # menu = process_user_forms(db, form_ids)
    menu = process_admin_forms(forms)
    # db.save_user_login_history(user_id)
    return login.UserLoginSuccess(
        int(user_id), session_token, email_id, user_group_name,
        menu, employee_name, employee_code, contact_no, address,
        designation, None, bool(1)
    )

def admin_login_response(db, ip, result, forms):
    user_id = result.get('user_id')
    user_category_id = result.get('user_category_id')
    if user_category_id == 1:
        name = "Compfie Admin"
    else:
        name = "Console Admin"
    email_id = None
    session_type = 1  # web
    session_token = add_session(db, user_id, session_type, ip, name)
    menu = process_admin_forms(forms)
    employee_name = "Administrator"
    return login.AdminLoginSuccess(
        user_id, session_token, email_id, menu,
        employee_name, None
    )

def process_forgot_password(db, request):
    email_id = request.username
    user_type = request.login_type
    user_id, employee_name = verify_username(
        db, email_id, user_type
    )
    if user_id is not None:
        send_reset_link(db, user_id, email_id, employee_name)
        return login.ForgotPasswordSuccess()
    else:
        return login.InvalidUserName()

def send_reset_link(db, user_id, email_id, employee_name):
    reset_token = new_uuid()
    reset_link = "%s/reset-password/%s" % (
        KNOWLEDGE_URL, reset_token
    )
    condition = "user_id = %s "
    condition_val = [user_id]
    db.delete(tblEmailVerification, condition, condition_val)
    columns = ["user_id", "verification_code"]
    values_list = [user_id, reset_token]
    db.insert(tblEmailVerification, columns, values_list)
    if email().send_reset_link(
        db, user_id, email_id, reset_link, employee_name
    ):
        return True
    else:
        print "Send email failed"

def process_reset_token(db, request):
    user_id = validate_reset_token(db, request.reset_token)
    if user_id is not None:
        return login.ResetSessionTokenValidationSuccess()
    else:
        return login.InvalidResetToken()

def process_reset_password(db, request):
    user_id = validate_reset_token(db, request.reset_token)
    if user_id is not None:
        if update_password(db, request.new_password, user_id):
            if delete_used_token(db, request.reset_token):
                return login.ResetPasswordSuccess()
            else:
                print "Failed to delete used token"
        else:
            return login.EnterDifferentPassword()
    else:
        return login.InvalidResetToken()

def process_change_password(db, request):
    session_user = db.validate_session_token(request.session_token)
    if verify_password(db, request.current_password, session_user):
        update_password(db, request.new_password, session_user)
        return login.ChangePasswordSuccess()
    else:
        return login.InvalidCurrentPassword()

def process_logout(db, request):
    session = request.session_token
    remove_session(db, session)
    return login.LogoutSuccess()

def process_validate_rtoken(db, request):
    token = request.reset_token
    if (validate_email_token(db, token)):
        captcha_text = generate_random(CAPTCHA_LENGTH)
        return login.CheckRegistrationTokenSuccess(captcha_text)
    else :
        return login.InvalidSessionToken()

def process_save_logindetails(db, request):
    username = request.username
    password = request.password
    # duplication username validation

    encrypt_password = encrypt(password)
    token = request.token
    if save_login_details(db, token, username, encrypt_password):
        return login.SaveRegistraionSuccess()
    else :
        return login.InvalidSessionToken()
