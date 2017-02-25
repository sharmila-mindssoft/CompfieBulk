from clientprotocol import (clientcore)
from server.clientdatabase.tables import *

from server.common import (
   convert_to_dict, new_uuid, get_date_time, get_date_time_in_date
)
from server.constants import SESSION_CUTOFF
from server.clientdatabase.general import (
    is_service_proivder_user, is_service_provider_in_contract
)
from server.clientdatabase.savetoknowledge import IsClientActive
from dateutil import relativedelta

__all__ = [
    "is_configured",
    "is_in_contract",
    "is_client_active",
    "verify_login",
    "is_contract_not_started",
    "add_session",
    "get_client_group",
    "get_client_configuration",
    "save_login_failure",
    "delete_login_failure_history",
    "get_login_attempt_and_time",
    "validate_email_token",
    "save_login_details",
    "check_username_duplicate",
    "get_user_id_from_token",
    "get_client_details_from_userid"
]


def is_configured(db):
    columns = "count(1) as configure"
    condition = "1"
    rows = db.get_data(
        tblClientGroups, columns, condition
    )
    if rows[0]["configure"] <= 0:
        return False
    else:
        return True


def is_in_contract(db):
    columns = "count(1)  as contract"
    condition = "now() between contract_from and " + \
        " DATE_ADD(contract_to, INTERVAL 1 DAY)"
    rows = db.get_data(
        tblClientGroups, columns, condition
    )
    if rows[0]["contract"] <= 0:
        return False
    else:
        return True


def is_contract_not_started(db):
    columns = "count(1) as contract"
    condition = "now() < contract_from"
    rows = db.get_data(
        tblClientGroups, columns, condition
    )
    if rows[0]["contract"] <= 0:
        return False
    else:
        return True

def is_client_active(client_id):
    t_obj = IsClientActive(client_id)
    return t_obj._is_client_active()


def verify_login(db, username, password):
    q = "SELECT t1.user_category_id, ul.username, t1.user_id, t1.email_id, " + \
        "t1.employee_name, t1.employee_code, t1.contact_no, t1.mobile_no, t1.address, t1.user_group_id, " + \
        " (select user_group_name from tbl_user_groups where user_group_id = t1.user_group_id) as user_group_name" + \
        " FROM tbl_user_login_details as ul  " + \
        " INNER JOIN tbl_users t1 on t1.user_id = ul.user_id " + \
        " WHERE ul.password= %s and ul.username = %s and ul.is_active=1 "
    #print q
    data_list = db.select_one(q, [password, username])
    if data_list is None:
        return False
    else:
        # verify legal entity is active
        # verity legal entity contract expired
        # verify service provider contract expired
        return data_list

def add_session(
    db, user_category_id, user_id, session_type_id, ip,
    employee, client_id
):

    clear_old_session(db, user_id, session_type_id, client_id)
    session_id = new_uuid()
    session_id = "%s-%s" % (client_id, session_id)
    updated_on = get_date_time()

    query = "INSERT INTO tbl_user_sessions " + \
        " (session_token, user_id, session_type_id, last_accessed_time) " + \
        " VALUES (%s, %s, %s, %s);"

    db.execute(query, (session_id, user_id, session_type_id, updated_on))

    action = "Log In by - \"%s\" from \"%s\"" % (employee, ip)
    # action = "Log In by - \"%s\" " % (employee)
    db.save_activity(user_id, 0, action)

    return session_id


#
# mobile_api
#
def get_client_group(db):
    q = "SELECT client_id, group_name from  tbl_client_groups"
    row = db.select_one(q)
    result = []
    if row:
        result = convert_to_dict(row, ["client_id", "group_name"])
    return result


def get_client_configuration(db):
    q = "SELECT country_id, domain_id, period_from, period_to " + \
        " from tbl_client_configurations"
    rows = db.select_all(q)
    result = []
    if rows:
        result = convert_to_dict(
            rows, ["country_id", "domain_id", "period_from", "period_to"]
        )
    c_list = []
    for r in result:
        info = clientcore.ClientConfiguration(
            r["country_id"],
            r["domain_id"],
            r["period_from"],
            r["period_to"]
        )
        c_list.append(info)

    return c_list


def clear_old_session(db, user_id, session_type_id, client_id=None):
    query = "DELETE FROM tbl_user_sessions " + \
        " WHERE user_id=%s and session_type_id=%s OR " + \
        " last_accessed_time < DATE_SUB(NOW(),INTERVAL %s MINUTE) "
    db.execute(query, (
        user_id, session_type_id, int(SESSION_CUTOFF)
    ))


def check_and_update_login_attempt(db, user_id):
    current_date_time = get_date_time_in_date()
    rows = get_login_attempt_and_time(db, user_id)
    if(rows):
        last_login_time = rows[0]["login_time"]
        diff = relativedelta.relativedelta(current_date_time, last_login_time)
        if diff.hours > 2 or diff.days > 0:
            db.update(
                tblUserLoginHistory, ["login_attempt"], [0, user_id],
                " user_id=%s "
            )


def save_login_failure(db, user_id, session_user_ip):
    check_and_update_login_attempt(db, user_id)
    columns = "user_id, ip, login_time"
    valueList = [(int(user_id), session_user_ip, get_date_time())]
    updateColumnsList = ["login_time", "ip"]
    if (
        db.on_duplicate_key_update(
            tblUserLoginHistory, columns, valueList, updateColumnsList
        )
    ):
        increament_column = ["login_attempt"]
        increament_cond = " user_id = %s "
        increament_cond_val = [user_id]
        db.increment(
            tblUserLoginHistory, increament_column, increament_cond,
            condition_val=increament_cond_val
        )


def delete_login_failure_history(db, user_id):
    condition = " user_id=%s"
    condition_val = [user_id]
    db.delete(tblUserLoginHistory, condition, condition_val)


def get_login_attempt_and_time(db, user_id):
    columns = ["login_attempt", "login_time"]
    condition = " user_id = %s "
    condition_val = [user_id]
    rows = db.get_data(
        tblUserLoginHistory, columns, condition, condition_val
    )
    return rows
#################################################################
# Validate Registration Token
#################################################################
def validate_email_token(db, token):
    q = "SELECT user_id, verification_code FROM tbl_email_verification " + \
        " WHERE expiry_date > convert_tz(utc_timestamp(),'+00:00','+05:30') AND verification_code = %s"
    rows = db.select_one(q, [token])
    if rows:
        user_id = rows.get("user_id")
        # print "userid>>>", user_id
        if user_id is None:
            return False
        else:
            return user_id
    else:
        return False
#################################################################
# Get Valid User ID
#################################################################
def get_user_id_from_token(db, token):
    columns = "user_id"
    condition = "verification_code = %s"
    condition_val = [token]
    rows = db.get_data(
        "tbl_email_verification", columns, condition, condition_val
    )
    return rows[0]["user_id"]
#################################################################
# Get User category ID, is_active
#################################################################
def get_client_details_from_userid(db, user_id):
    columns = "user_category_id, is_active"
    condition = "user_id = %s"
    condition_val = [user_id]
    rows = db.get_data(tblUsers, columns, condition, condition_val)
    return rows

#################################################################
# Delete Email Verification Token
#################################################################
def delete_emailverification_token(db, token):
    q = " DELETE FROM tbl_email_verification where verification_code = %s "
    db.execute(q, [token])
    return True

#################################################################
# Save login Details
#################################################################
def save_login_details(db, token, username, password):
    user_id = get_user_id_from_token(db, token)
    user_details = get_client_details_from_userid(db, user_id)
    user_category_id = user_details[0]["user_category_id"]
    is_active = user_details[0]["is_active"]    

    q = " INSERT INTO tbl_user_login_details(user_id, user_category_id, username, " + \
        " password, is_active) VALUES (%s, %s, %s, %s, %s) "
    db.execute(q, [user_id, user_category_id, username, password, is_active])

    delete_emailverification_token(db, token)

    return True
#################################################################
# Check User Name Duplication
#################################################################
def check_username_duplicate(db, uname):
    q = " SELECT count(0) as uname from tbl_user_login_details where username = %s "
    rows = db.select_one(q, [uname])    
    count = rows.get("uname")
    if count > 0:
        return False

    return True