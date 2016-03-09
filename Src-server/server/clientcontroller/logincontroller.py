from server.controller.corecontroller import process_user_forms
from server.emailcontroller import EmailHandler as email
from protocol import login
from server.constants import (
    CLIENT_URL, KNOWLEDGE_URL
)


__all__ = [
    "process_login_request",
    "process_login", "process_forgot_password",
    "process_reset_token",
    "process_reset_password",
    "process_change_password",
    "process_logout"
]

def process_login_request(request, db, company_id) :
    if type(request) is login.Login:
        return process_login(db, request, company_id)

    if type(request) is login.ForgotPassword :
        return process_forgot_password(db, request)

    if type(request) is login.ResetTokenValidation :
        return process_reset_token(db, request)

    if type(request) is login.ResetPassword :
        return process_reset_password(db, request)

    if type(request) is login.ChangePassword :
        return process_change_password(db, request)

    if type(request) is login.Logout:
        return process_logout(db, request)


def process_login(db, request, client_id):
    username = request.username
    password = request.password
    encrypt_password = db.encrypt(password)
    if db.is_contract_not_started():
        return login.InvalidCredentials()
    elif not db.is_in_contract():
        return login.ContractExpired()
    elif not db.is_client_active(client_id):
        return login.InvalidCredentials()
    else:
        response = db.verify_login(username, encrypt_password)
    if response is True:
        return admin_login_response(db, client_id, request.ip)
    else :
        if bool(response):
            return user_login_response(db, response, client_id, request.ip)
        else :
            return login.InvalidCredentials()


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
        form_ids = "%s, 3, 4, 6, 7, 8" % (form_ids)
        form_ids_list = form_ids.split(",")
        if 1 not in form_ids_list:
            form_ids_list.append(1)
        report_form_ids = db.get_report_form_ids().split(",")
        for form_id in report_form_ids:
            if form_id not in form_ids_list:
                form_ids_list.append(form_id)
        form_ids = ",".join(str(x) for x in  form_ids_list)
    menu = process_user_forms(db, form_ids, client_id, 0)
    return login.UserLoginSuccess(
        user_id, session_token, email_id, user_group_name,
        menu, employee_name, employee_code, contact_no, None, None,
        client_id, bool(is_promoted_admin)
    )

def admin_login_response(db, client_id, ip):
    user_id = 0
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
    reset_link = "%s%s/ForgotPassword?reset_token=%s" % (
        CLIENT_URL, short_name, reset_token)
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
    session_token = client_info[1]
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
