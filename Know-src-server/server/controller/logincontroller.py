from corecontroller import process_admin_forms
from server.emailcontroller import EmailHandler as email
from protocol import login, mobile
from server.constants import (
    KNOWLEDGE_URL, CAPTCHA_LENGTH, NO_OF_FAILURE_ATTEMPTS,
    FORGOTPASSWORD_EXPIRY
)

from server.common import (
    encrypt, new_uuid, generate_random
)
from server.database.tables import *
from server.database.login import *
from server.database.forms import *
from server.common import (
    get_date_time, addHours, get_current_date
)

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
        result = process_login(db, request, session_user_ip)

    elif type(request) is login.ForgotPassword:
        result = process_forgot_password(db, request)

    elif type(request) is login.ResetTokenValidation:
        result = process_reset_token(db, request)

    elif type(request) is login.ResetPassword:
        result = process_reset_password(db, request)

    elif type(request) is login.ChangePassword:
        result = process_change_password(db, request)

    elif type(request) is login.Logout:
        result = process_logout(db, request)

    elif type(request) is login.CheckRegistrationToken:
        result = process_validate_rtoken(db, request)

    elif type(request) is login.SaveRegistraion:
        result = process_save_logindetails(db, request)

    elif type(request) is login.CheckUsername:
        result = process_check_username(db, request)

    return result


def process_login(db, request, session_user_ip):
    login_type = request.login_type
    username = request.username
    password = request.password
    encrypt_password = encrypt(password)
    response = verify_login(db, username, encrypt_password)
    is_success = response[0]
    user_id = response[1]
    username = response[2]

    # verified_username = response[0]
    verified_login = response[3]
    user_info = response[4]
    forms = response[5]
    m_count = response[6]
    s_count = response[7]
    # user_id = verified_username.get('user_id')

    user_category_id = verified_login.get('user_category_id')
    print user_category_id
    if user_category_id <= 2 :
        if is_success is False and username is None:
            return login.InvalidCredentials(None)
    else :
        if is_success == "disable" :
            return login.DisabledUser()
        elif is_success is False and username is None:
            return login.InvalidCredentials(None)

    if login_type.lower() == "web" :

        if is_success is False :
            rows = save_login_failure(db, user_id, session_user_ip)
            # rows = get_login_attempt_and_time(db, user_id)
            no_of_attempts = 0
            if rows:
                no_of_attempts = rows.get("login_attempt")
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
                        db, session_user_ip, verified_login, forms, m_count, s_count)
                else:
                    return user_login_response(
                        db, session_user_ip, user_info, forms, m_count, s_count)
    else :
        if user_category_id == 3 :
            return mobile_user_login_respone(db, login_type, session_user_ip, user_info, forms)
        else :
            return login.InvalidCredentials(None)


def mobile_user_login_respone(db, login_type, ip, data, forms):
    data = data[0]
    if login_type.lower() == "android":
        session_type = 2
    elif login_type.lower() == "ios":
        session_type = 3
    elif login_type.lower() == "blackberry":
        session_type = 4

    user_id = data["user_id"]
    employee_name = data["employee_name"]
    employee_code = data["employee_code"]

    form_ids = [int(x["form_id"]) for x in forms]
    if frmApproveStatutoryMapping not in form_ids:
        return login.InvalidMobileCredentials()

    employee = "%s - %s" % (employee_code, employee_name)
    session_token = add_session(db, user_id, session_type, ip, employee)
    return mobile.UserLoginResponseSuccess(
        data["user_id"],
        data["employee_name"],
        session_token
    )


def user_login_response(db, ip, data, forms, m_count, s_count):
    data = data[0]
    user_name = data["user_name"]
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
    mobile_no = data["mobile_no"]

    menu = process_admin_forms(forms)
    # db.save_user_login_history(user_id)
    return login.UserLoginSuccess(
        int(user_id), session_token, email_id, user_group_name,
        menu, employee_name, employee_code, contact_no, address,
        designation, None, bool(1), user_name, mobile_no,
        m_count, s_count
    )


def admin_login_response(db, ip, result, forms, m_count, s_count):
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
        employee_name, None, m_count, s_count
    )


def process_forgot_password(db, request):
    login_type = request.login_type.lower()
    if login_type != "web":
        is_mobile = True
    else:
        is_mobile = False
    rows = db.verify_username(request.username)
    if rows is 0:
        return login.InvalidUserName()
    else:
        send_reset_link(db, rows[0]['user_id'], rows[0]['email_id'], rows[0]['employee_name'])
        return login.ForgotPasswordSuccess()


def send_reset_link(db, user_id, email_id, employee_name):
    reset_token = new_uuid()
    reset_link = "%s/reset-password/%s" % (
        KNOWLEDGE_URL, reset_token
    )
    condition = "user_id = %s "
    condition_val = [user_id]
    current_time_stamp = get_current_date()
    expiredon = addHours(int(FORGOTPASSWORD_EXPIRY), current_time_stamp)

    db.delete(tblEmailVerification, condition, condition_val)
    columns = ["user_id", "verification_code", "verification_type_id", "expiry_date"]
    values_list = [user_id, reset_token, 2, expiredon]
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
        if check_already_used_password(db, request.new_password, user_id):
            if update_password(db, request.new_password, user_id):
                if delete_used_token(db, request.reset_token):
                    return login.ResetPasswordSuccess()
                else:
                    print "Failed to delete used token"
            else:
                return login.EnterDifferentPassword()
        else:
            return login.EnterDifferentPassword()
    else:
        return login.InvalidResetToken()

def process_change_password(db, request):
    session_user = db.validate_session_token(request.session_token)
    if verify_password(db, request.current_password, session_user):
        if verify_new_password(db, request.new_password, session_user):
            update_password(db, request.new_password, session_user)
            return login.ChangePasswordSuccess()
        else:
            return login.CurrentandNewPasswordSame()
    else:
        return login.InvalidCurrentPassword()

def process_logout(db, request):
    session = request.session_token
    remove_session(db, session)
    return login.LogoutSuccess()

def process_validate_rtoken(db, request):
    token = request.reset_token
    user_id = validate_email_token(db, token)
    if (user_id):
        captcha_text = generate_random(CAPTCHA_LENGTH)
        is_register = check_user_inactive(db, user_id)
        return login.CheckRegistrationTokenSuccess(captcha_text, is_register)
    else :
        return login.InvalidSessionToken()

def process_save_logindetails(db, request):
    username = request.username
    password = request.password
    # duplication username validation
    if check_username_duplicate(db, username) is False:
        return login.UsernameAlreadyExists()
    else :
        encrypt_password = encrypt(password)
        token = request.token
        if save_login_details(db, token, username, encrypt_password):
            return login.SaveRegistraionSuccess()
        else :
            return login.InvalidSessionToken()

def process_check_username(db, request):
    uname = request.username

    if check_username_duplicate(db, uname):
        return login.CheckUsernameSuccess()
    else :
        return login.UsernameAlreadyExists()
