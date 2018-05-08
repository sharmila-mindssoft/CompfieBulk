import json
from protocol import login, mobile, core
from server.database.tables import *
from server.database.login import *
from server.database.forms import *
from server.emailcontroller import EmailHandler as email
from server.constants import (
    KNOWLEDGE_URL
)
from server.common import (
    encrypt, new_uuid, datetime_to_string_time, make_summary
)
from server.database.knowledgetransaction import (
    save_approve_mapping
)


__all__ = [
    "process_mobile_request", "process_mobile_login_request",
    "process_mobile_login", "process_mforgot_password",
    "process_mobile_logout"
]


def process_mobile_login_request(request, db, session_user_ip):
    print type(request)
    if type(request) is login.Login:
        result = process_mobile_login(db, request, session_user_ip)

    elif type(request) is login.ForgotPassword:
        result = process_mforgot_password(db, request)

    elif type(request) is login.Logout:
        result = process_mobile_logout(db, request)

    else :
        result = None
    return result

def process_mobile_request(request, db, session_user_ip, user_id):
    if type(request) is mobile.RequestFormat :

        request_frame = request.request

        if type(request_frame) is mobile.GetApproveStatutoryMappings:
            result = process_get_approve_statutory_mappings(db, user_id)

        elif type(request_frame) is mobile.ApproveStatutoryMapping:
            result = process_approve_statutory_mapping(db, request_frame, user_id)

    return result

def process_mobile_login(db, request, session_user_ip):
    login_type = request.login_type
    username = request.username
    password = request.password
    encrypt_password = encrypt(password)
    try :
        response = verify_login(db, username, encrypt_password)
        is_success = response[0]
        if is_success is False :
            return login.InvalidCredentials(None)

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
    except Exception, e :
        print e

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

def approve_statutory_mapping_list(db, user_id):
    result = db.call_proc_with_multiresult_set("sp_tbl_statutory_mapping_approve_list", [user_id], 3)
    mappings = result[0]
    orgs = result[1]
    geo_info = result[2]

    def get_orgs(map_id):
        orgname = []
        for o in orgs :
            if o["statutory_mapping_id"] == map_id :
                orgname.append(o["organisation_name"])
        return orgname

    def get_geos(map_id):
        geo_names = []
        for g in geo_info :
            if g["statutory_mapping_id"] == map_id :
                geo_names.append(g["parent_names"] + ">>" + g["geography_name"])
        return geo_names

    compliance = []
    mapped = {}
    for m in mappings :

        map_id = m["statutory_mapping_id"]
        if mapped.get(map_id) is None :
            compliance = []

        if m["document_name"] is None :
            c_name = m["compliance_task"]
        else :
            c_name = m["document_name"] + " - " + m["compliance_task"]
        orgname = get_orgs(map_id)
        geo_names = get_geos(map_id)
        c_on = datetime_to_string_time(m["created_on"])

        u_on = None
        if m["updated_by"] is not None :
            u_on = datetime_to_string_time(m["updated_on"])

        map_text = json.loads(m["statutory_mapping"])
        map_text = ", ".join(map_text)

        statutory_dates = m["statutory_dates"]
        statutory_dates = json.loads(statutory_dates)
        date_list = []
        for date in statutory_dates:
            s_date = core.StatutoryDate(
                date["statutory_date"],
                date["statutory_month"],
                date["trigger_before_days"],
                date.get("repeat_by")
            )
            date_list.append(s_date)
        summary, dates = make_summary(date_list, m["frequency_id"], m)
        if dates is not None :
            summary += dates

        compliance.append(mobile.MappingComplianceInfo(
            m["compliance_id"], c_name, bool(m["is_active"]),
            m["created_by"], c_on, m["updated_by"],
            u_on, m["statutory_provision"],
            m["compliance_description"], m["penal_consequences"],
            m["freq_name"], summary, m["reference_link"],
            ", ".join(geo_names)
        ))

        mapped[map_id] = mobile.MappingApproveInfo(
            map_id, m["country_name"], m["domain_name"],
            m["statutory_nature_name"], orgname, map_text,
            compliance
        )

    return mapped.values()

def process_get_approve_statutory_mappings(db, user_id):
    statutory_mappings = approve_statutory_mapping_list(db, user_id)
    return mobile.GetApproveStatutoryMappingSuccess(
        statutory_mappings
    )


def process_approve_statutory_mapping(db, request_frame, user_id):
    data = request_frame.statutory_mappings
    result = save_approve_mapping(db, user_id, data)
    if result:
        return mobile.ApproveStatutoryMappingSuccess()
