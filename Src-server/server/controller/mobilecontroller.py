from protocol import login, mobile
from server import logger
from server.database.tables import *
from server.database.login import *
from server.database.forms import *
from server.emailcontroller import EmailHandler as email
from server.constants import (
    KNOWLEDGE_URL
)
from server.common import (
    encrypt, new_uuid
)
from server.database.knowledgetransaction import (
    approve_statutory_mapping_list
)
from generalcontroller import (validate_user_session, validate_user_forms)

__all__ = [
    "process_mobile_request",
    "process_mobile_login", "process_mforgot_password",
    "process_mobile_logout"
]


def process_mobile_request(request, db, session_user_ip):
    print type(request)
    if type(request) is login.Login:
        logger.logKnowledgeApi("Login", "process begin")
        result = process_mobile_login(db, request, session_user_ip)
        logger.logKnowledgeApi("Login", "process end")

    elif type(request) is login.ForgotPassword:
        logger.logKnowledgeApi("ForgotPassword", "process begin")
        result = process_mforgot_password(db, request)
        logger.logKnowledgeApi("ForgotPassword", "process end")

    elif type(request) is login.Logout:
        logger.logKnowledgeApi("Logout", "process begin")
        result = process_mobile_logout(db, request)
        logger.logKnowledgeApi("Logout", "process end")

    else :
        result = None

    if type(request) is mobile.RequestFormat :
        forms = None
        session_token = request.session_token
        request_frame = request.request
        user_id = validate_user_session(db, session_token)
        if user_id is not None:
            is_valid = validate_user_forms(db, user_id, forms, request_frame)
            if is_valid is not True:
                return login.InvalidSessionToken()

        if user_id is None:
            return login.InvalidSessionToken()

        if type(request_frame) is mobile.GetApproveStatutoryMappings:
            logger.logKnowledgeApi("GetApproveStatutoryMappings", "process begin")
            result = process_get_approve_statutory_mappings(db, user_id)
            logger.logKnowledgeApi("GetApproveStatutoryMappings", "process end")

    return result

def process_mobile_login(db, request, session_user_ip):
    print session_user_ip
    login_type = request.login_type
    username = request.username
    password = request.password
    encrypt_password = encrypt(password)
    response = verify_login(db, username, encrypt_password)
    is_success = response[0]
    username = response[2]

    verified_login = response[3]
    user_info = response[4]
    forms = response[5]

    user_category_id = verified_login.get('user_category_id')
    if is_success is False and username is None:
        return login.InvalidCredentials(None)
    if is_success  :
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
    print form_ids
    if frmApproveStatutoryMapping not in form_ids:
        return login.InvalidMobileCredentials()

    employee = "%s - %s" % (employee_code, employee_name)
    session_token = add_session(db, user_id, session_type, ip, employee)
    return mobile.UserLoginResponseSuccess(
        data["user_id"],
        data["employee_name"],
        session_token
    )


def process_mforgot_password(db, request):
    login_type = request.login_type.lower()
    if login_type != "web" :
        is_mobile = True
    else :
        is_mobile = False
    user_id = db.verify_username(request.username, is_mobile)

    if user_id is not None:
        send_reset_link(db, user_id, request.username)
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

def process_mobile_logout(db, request):
    session = request.session_token
    remove_session(db, session)
    return login.LogoutSuccess()


def process_get_approve_statutory_mappings(db, user_id):
    statutory_mappings = approve_statutory_mapping_list(db, user_id)
    return mobile.GetApproveStatutoryMappingSuccess(
        statutory_mappings
    )
