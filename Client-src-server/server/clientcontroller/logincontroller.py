from server.clientdatabase.tables import *
from server.emailcontroller import EmailHandler as email
from clientprotocol import clientlogin
from server.constants import (
    CLIENT_URL, CAPTCHA_LENGTH, NO_OF_FAILURE_ATTEMPTS
)
from server import logger
from server.clientdatabase.login import *

from server.common import (
    encrypt, new_uuid, generate_random
)

from server.clientdatabase.general import (
    verify_username,
    validate_reset_token, update_password, delete_used_token,
    remove_session, update_profile, verify_password, get_user_name_by_id,
    get_user_forms, get_forms_by_category, get_legal_entity_info, get_country_info, get_themes,
    verify_username_forgotpassword
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
    if type(request) is clientlogin.Login:
        result = process_login(db, request, company_id, session_user_ip)

    elif type(request) is clientlogin.ForgotPassword:
        result = process_forgot_password(db, request)

    elif type(request) is clientlogin.ResetTokenValidation:
        result = process_reset_token(db, request)

    elif type(request) is clientlogin.ResetPassword:
        result = process_reset_password(db, request)

    elif type(request) is clientlogin.ChangePassword:
        result = process_change_password(db, company_id, request)

    elif type(request) is clientlogin.Logout:
        result = process_logout(db, request, session_user_ip)

    elif type(request) is clientlogin.UpdateUserProfile:
        result = process_update_profile(db, request)

    elif type(request) is clientlogin.CheckRegistrationToken:
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

    short_name = request.short_name
    encrypt_password = encrypt(request.password)
    user_ip = session_user_ip
    user_id = verify_username(db, username)

    if user_id is None:
        return clientlogin.InvalidCredentials(None)
    else:
        response = verify_login(db, username, encrypt_password)
        print response

    if response is False:
        return invalid_credentials(db, user_id, session_user_ip)
    elif response == "blocked" or response == "disabled" :
        return clientlogin.DisabledUser()
    else:
        delete_login_failure_history(db, user_id)
        return user_login_response(db, response, client_id, user_ip, short_name, login_type.lower())

def user_login_response(db, data, client_id, ip, short_name, login_type):
    cat_id = data["user_category_id"]
    user_id = data["user_id"]

    le_info = get_legal_entity_info(db, user_id, cat_id)
    if len(le_info) == 0:
            return clientlogin.InvalidCredentials(None)

    email_id = data["email_id"]
    address = data["address"]
    if login_type.lower() == "android" :
        session_type = 2
    elif login_type.lower() == "ios" :
        session_type = 3
    else :
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

    c_info = get_country_info(db, user_id, cat_id)
    if login_type == "web" :
        theme = get_themes(db, user_id)

        if cat_id == 1 :
            forms = get_forms_by_category(db, cat_id)
        else :
            forms = get_user_forms(db, user_id, cat_id)

        menu = process_user_forms(
            db, forms, short_name
        )

        return clientlogin.UserLoginSuccess(
            user_id, session_token, email_id, user_group_name,
            menu, employee_name, employee_code, contact_no, address,
            client_id, username, mobile_no, le_info, c_info, theme,
            cat_id
        )

    else :
        show_dashboard = True   # 34
        show_approval = True   # 9
        show_task = False   # 35
        if cat_id > 1 :
            show_dashboard = False
            show_approval = False
            forms = get_user_forms(db, user_id, cat_id)
            for f in forms :
                if f["form_id"] == 34 :
                    show_dashboard = True

                if f["form_id"] == 9 :
                    show_approval = True

                if f["form_id"] == 35 :
                    show_task = True

        return clientlogin.MobileUserLoginSuccess(
            user_id, session_token, email_id,
            employee_name, employee_code,
            client_id, le_info, c_info,
            cat_id, show_dashboard, show_approval, show_task
        )

def process_forgot_password(db, request):
    rows = verify_username_forgotpassword(db, request.username)
    if rows:
        send_reset_link(db, rows['user_id'], rows['email_id'], request.short_name)
        return clientlogin.ForgotPasswordSuccess()
    else:
        return clientlogin.InvalidUserName()

def send_reset_link(db, user_id, username, short_name):
    reset_token = new_uuid()
    reset_link = "%sreset_password/%s/%s" % (
        CLIENT_URL, short_name, reset_token)

    condition = "user_id = %s and verification_type_id = %s"
    condition_val = [user_id, 2]
    db.delete(tblEmailVerification, condition, condition_val)

    q = " INSERT INTO tbl_email_verification(user_id, verification_code, " + \
        " verification_type_id) VALUES (%s, %s, %s)"
    row = db.execute(q, [user_id, reset_token, 2])

    employee_name = get_user_name_by_id(db, user_id)
    if(row >= 0):
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
        if check_already_used_password(db, encrypt(request.new_password), user_id):
            update_password(db, request.new_password, user_id)
            delete_used_token(db, request.reset_token)
            return clientlogin.ResetPasswordSuccess()
        else:
            return clientlogin.EnterDifferentPassword()
    else:
        return clientlogin.InvalidResetToken()


def process_change_password(db, company_id, request):
    client_info = request.session_token.split("-")

    session_token = "%s-%s" % (
        company_id, client_info[2]
    )
    print session_token
    user_details = db.validate_session_token(session_token)
    session_user = int(user_details[0])
    if verify_password(db, request.current_password, session_user):
        if (request.current_password == request.new_password):
            return clientlogin.CurrentandNewPasswordSame()
        elif (request.current_password == request.confirm_password):
            return clientlogin.CurrentandConfirmPasswordSame()
        elif (request.new_password != request.confirm_password):
            return clientlogin.NewandConfirmPasswordNotSame()
        else:
            update_password(db, request.new_password, session_user)
            return clientlogin.ChangePasswordSuccess()
    else:
        return clientlogin.InvalidCurrentPassword()


def process_logout(db, request, user_ip):
    # save logout time
    session = request.session_token
    remove_session(db, session, user_ip)
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
