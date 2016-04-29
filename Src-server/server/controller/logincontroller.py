from corecontroller import process_user_forms
from server.emailcontroller import EmailHandler as email
from protocol import login, mobile
from server.constants import (
    KNOWLEDGE_URL
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

def process_login_request(request, db, session_user_ip) :
    if type(request) is login.Login:
        logger.logKnowledgeApi("Login", "process begin")
        result = process_login(db, request, session_user_ip)
        logger.logKnowledgeApi("Login", "process end")

    if type(request) is login.ForgotPassword :
        logger.logKnowledgeApi("ForgotPassword", "process begin")
        result = process_forgot_password(db, request)
        logger.logKnowledgeApi("ForgotPassword", "process end")

    if type(request) is login.ResetTokenValidation :
        logger.logKnowledgeApi("ResetTokenValidation", "process begin")
        result = process_reset_token(db, request)
        logger.logKnowledgeApi("ResetTokenValidation", "process end")

    if type(request) is login.ResetPassword :
        logger.logKnowledgeApi("ResetPassword", "process begin")
        result = process_reset_password(db, request)
        logger.logKnowledgeApi("ResetPassword", "process end")

    if type(request) is login.ChangePassword :
        logger.logKnowledgeApi("ChangePassword", "process begin")
        result = process_change_password(db, request)
        logger.logKnowledgeApi("ChangePassword", "process end")

    if type(request) is login.Logout:
        logger.logKnowledgeApi("Logout", "process begin")
        result = process_logout(db, request)
        logger.logKnowledgeApi("Logout", "process end")

    return result

def process_login(db, request, session_user_ip):
    login_type = request.login_type
    username = request.username
    password = request.password
    encrypt_password = db.encrypt(password)
    response = db.verify_login(username, encrypt_password)
    if response is True:
        return admin_login_response(db, session_user_ip)
    else :
        if bool(response):
            if login_type.lower() == "web" :
                return user_login_response(db, response, session_user_ip)
            else :
                return mobile_user_login_respone(db, response, request, session_user_ip)
        else :
            return login.InvalidCredentials()


def mobile_user_login_respone(db, data, request, ip):
    login_type = request.login_type
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
    form_ids = [int(x) for x in data["form_ids"].split(",")]
    if 11 not in form_ids :
        return login.InvalidCredentials()
    employee = "%s - %s" % (employee_code, employee_name)
    session_token = db.add_session(user_id, session_type, ip, employee)
    return mobile.UserLoginResponseSuccess(
        data["user_id"],
        data["employee_name"],
        session_token
    )

def user_login_response(db, data, ip):
    user_id = data["user_id"]
    email_id = data["email_id"]
    session_type = 1 #web
    employee_name = data["employee_name"]
    employee_code = data["employee_code"]
    employee = "%s - %s" % (employee_code, employee_name)
    session_token = db.add_session(user_id, session_type, ip, employee)
    contact_no = data["contact_no"]
    address = None if data["address"] == "" else data["address"]
    designation = None if data["designation"] == "" else data["designation"]
    user_group_name = data["user_group_name"]
    form_ids = data["form_ids"]
    menu = process_user_forms(db, form_ids)
    # db.save_user_login_history(user_id)
    return login.UserLoginSuccess(
        int(user_id), session_token, email_id, user_group_name,
        menu, employee_name, employee_code, contact_no, address,
        designation, None, bool(1)
    )

def admin_login_response(db, ip):
    user_id = 0
    email_id = None
    session_type = 1 #web
    session_token = db.add_session(user_id, session_type, ip, "Administrator")
    menu = process_user_forms(db, "1,2,3,4")
    employee_name = "Administrator"
    return login.AdminLoginSuccess(user_id, session_token, email_id, menu, employee_name, None)

def process_forgot_password(db, request):
    user_id = db.verify_username(request.username)
    if user_id != None:
        send_reset_link(db, user_id, request.username)
        return login.ForgotPasswordSuccess()
    else:
        return login.InvalidUserName()

def send_reset_link(db, user_id, username):
    reset_token = db.new_uuid()
    reset_link = "%s/reset-password/%s" % (
        KNOWLEDGE_URL, reset_token
    )

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
    user_id = db.validate_reset_token(request.reset_token)
    if user_id != None:
        return login.ResetSessionTokenValidationSuccess()
    else:
        return login.InvalidResetToken()


def process_reset_password(db, request):
    user_id = db.validate_reset_token(request.reset_token)
    if user_id != None:
        if db.update_password(request.new_password, user_id):
            if db.delete_used_token(request.reset_token):
                return login.ResetPasswordSuccess()
            else:
                print "Failed to delete used token"
        else:
            return login.EnterDifferentPassword()
    else:
        return login.InvalidResetToken()

def process_change_password(db, request):
    session_user = db.validate_session_token(request.session_token)
    if db.verify_password(request.current_password, session_user):
        db.update_password(request.new_password, session_user)
        return login.ChangePasswordSuccess()
    else :
        return login.InvalidCurrentPassword()


def process_logout(db, request):
    return login.LogoutSuccess()
