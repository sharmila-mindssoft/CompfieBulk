from server.database.tables import *
from server.common import (
    get_date_time, new_uuid, encrypt,
    get_date_time_in_date
)
from server.constants import SESSION_CUTOFF
from dateutil import relativedelta

__all__ = [
    "verify_login",
    "add_session",
    "verify_password",
    "validate_reset_token", "update_password",
    "delete_used_token", "remove_session",
    "save_login_failure", "delete_login_failure_history",
    "get_login_attempt_and_time", "save_login_details",
    "validate_email_token", "check_username_duplicate"
]


########################################################
# To Check Login credentials
########################################################
def verify_login(db, username, password):

    args = [username, password]
    expected_result = 4
    result = db.call_proc_with_multiresult_set(
       "sp_verify_login", args, expected_result
    )
    '''
        'sp_verify_login' this procedure will return
        3 result-set which are validation-result, Users info and User's Forms.
    '''
    user_info = forms = response = {}

    if len(result[1]) == 0 and len(result[0]) > 0 :
        user_id = result[0][0].get("user_id")
        username = result[0][0].get("username")
        is_login = False

    elif len(result[1]) == 0 and len(result[0]) == 0 :
        user_id = None
        username = None
        is_login = False
    else :
        is_login = True
        user_id = result[1][0].get("user_id")
        user_category_id = result[1][0].get('user_category_id')
        username = result[0][0].get("username")
        response = result[1][0]
        if user_id is None:
            user_info = None
            forms = None
        elif user_category_id <= 2:
            user_info = None
            forms = result[2]
        elif user_category_id > 2:
            user_info = result[2]
            forms = result[3]
    return (is_login, user_id, username, response, user_info, forms)

########################################################
# To clear user session
########################################################
def clear_old_session(db, user_id, session_type_id, client_id=None):
    query = "DELETE FROM tbl_user_sessions " + \
        " WHERE user_id=%s and session_type_id=%s OR " + \
        " last_accessed_time < DATE_SUB(NOW(),INTERVAL %s MINUTE) "

    db.execute(query, (
        user_id, session_type_id, int(SESSION_CUTOFF)
    ))


########################################################
# Adds User session
########################################################
def add_session(
    db, user_id, session_type_id, ip,
    employee, client_id=None
):
    if client_id is not None:
        clear_old_session(db, user_id, session_type_id, client_id)
    else:
        clear_old_session(db, user_id, session_type_id)
    session_id = new_uuid()
    if client_id is not None:
        session_id = "%s-%s" % (client_id, session_id)
    updated_on = get_date_time()
    query = " INSERT INTO tbl_user_sessions " + \
        " (session_token, user_id, session_type_id, " + \
        " last_accessed_time) VALUES (%s, %s, %s, %s);"
    db.execute(query, (session_id, user_id, session_type_id, updated_on))

    # action = "Log In by - \"%s\" from \"%s\"" % ( employee, ip)
    action = "Log In by - \"%s\" " % (employee)
    db.save_activity(user_id, 0, action)

    return session_id

# def get_user_form_ids(db, user_id):
#     if user_id == 0:
#         return "1, 2, 3, 4"
#     q = "select t1.form_ids from tbl_user_groups t1 " + \
#         " INNER JOIN tbl_users t2 on t1.user_group_id = t2.user_group_id " + \
#         " AND t2.user_id = %s"
#     row = db.select_one(q, [user_id])
#     if row:
#         return row[0]
#     else:
#         return None


def verify_password(db, password, user_id):
    columns = "count(1)"
    encrypted_password = encrypt(password)
    condition = "1"

    condition = "password=%s and user_id=%s"
    condition_val = [encrypted_password, user_id]
    rows = db.get_data("tbl_user_login_details", columns, condition, condition_val)
    if(int(rows[0]["count(1)"]) <= 0):
        return False
    else:
        return True


########################################################
# Check whether the given reset token is valid
########################################################
def validate_reset_token(db, reset_token):
    email_verification_column = "user_id"
    email_verification_condition = " verification_code=%s"
    email_verification_condition_val = [reset_token]
    email_verification_rows = db.get_data(
        tblEmailVerification, email_verification_column,
        email_verification_condition, email_verification_condition_val
    )
    if email_verification_rows:
        user_id = email_verification_rows[0]["user_id"]
        if user_id == 0:  # Returning if user is admin
            return user_id
        else:  # Checking if user is active
            user_column = "user_id"
            user_condition = "user_id = %s and is_active = 1"
            user_condition_val = [user_id]
            user_rows = db.get_data(
                tblUsers, user_column, user_condition, user_condition_val
            )
            if user_rows:
                return user_id
            else:
                return None
    else:
        return None


def update_password(db, password, user_id):
    result = db.call_proc_with_multiresult_set(
        "sp_tbl_user_login_details_update",
        (user_id, encrypt(password)), 1
    )
    employee_name = result[0][0]["username"]

    action = "\"%s\" has updated his/her password" % (employee_name)
    db.save_activity(user_id, 0, action)

    if result:
        return True
    else:
        return False


########################################################
# Deletes a reset token, once it is used
########################################################
def delete_used_token(db, reset_token):
    condition = " verification_code=%s"
    if db.delete(tblEmailVerification, condition, [reset_token]):
        return True
    else:
        return False


def remove_session(db, session_token):
    db.delete(tblUserSessions, "session_token=%s", [session_token])


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
    result = db.call_proc_with_multiresult_set(
        "sp_save_login_failure",
        [user_id, session_user_ip, get_date_time()], 2
    )
    saved_info = result[1][0]
    return saved_info


def delete_login_failure_history(db, user_id):
    condition = " user_id=%s"
    condition_val = [user_id]
    db.delete(tblUserLoginHistory, condition, condition_val)


def get_login_attempt_and_time(db, user_id):
    columns = ["login_attempt", "login_time"]
    condition = " user_id=%s "
    condition_val = [user_id]
    rows = db.get_data(
        tblUserLoginHistory, columns, condition, condition_val
    )
    return rows

def validate_email_token(db, token):
    rows = db.call_proc(
        "sp_validate_token", (token, ))
    if rows :
        user_id = rows[0].get("user_id")
        if user_id is None :
            return False
        else:
            return user_id
    else :
        return False

def save_login_details(db, token, username, password):
    db.call_insert_proc(
        "sp_tbl_user_login_details_save",
        (token, username, password)
    )
    return True

def check_username_duplicate(db, uname):
    res = db.call_proc("sp_tbl_user_login_checkusername", (uname, ))
    count = res[0]['uname']
    if count > 0 :
        return False

    return True
