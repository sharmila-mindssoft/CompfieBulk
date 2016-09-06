from server.database.tables import *
from server.common import (
    convert_to_dict, get_date_time, new_uuid, encrypt,
    get_date_time_in_date
)
from server.constants import SESSION_CUTOFF
from dateutil import relativedelta

__all__ = [
    "verify_login",
    "add_session",
    "verify_username", "verify_password",
    "validate_reset_token", "update_password",
    "delete_used_token", "remove_session",
    "save_login_failure", "delete_login_failure_history",
    "get_login_attempt_and_time"
]


########################################################
# To Check Login credentials
########################################################
def verify_login(db, username, password):
    tblAdminCondition = "password=%s and username=%s"
    admin_details = db.get_data(
        "tbl_admin", ["username", "password"],
        tblAdminCondition,
        (password, username)
    )
    if (len(admin_details) == 0):
        data_columns = [
            "user_id", "user_group_id", "email_id",
            "employee_name", "employee_code",
            "contact_no", "address",
            "designation", "user_group_name", "form_ids"
        ]
        query = "SELECT t1.user_id, t1.user_group_id, t1.email_id, " + \
            " t1.employee_name, t1.employee_code, t1.contact_no, " + \
            " t1.address, t1.designation, " + \
            " t2.user_group_name, t2.form_ids " + \
            " FROM tbl_users t1 INNER JOIN tbl_user_groups t2 " + \
            " ON t1.user_group_id = t2.user_group_id " + \
            " WHERE t1.password=%s and t1.email_id=%s and t1.is_active=1"
        data_list = db.select_one(query, [password, username])
        if data_list is None:
            return False
        else:
            return convert_to_dict(data_list, data_columns)
    else:
        return True


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

def get_user_form_ids(db, user_id):
    if user_id == 0:
        return "1, 2, 3, 4"
    q = "select t1.form_ids from tbl_user_groups t1 " + \
        " INNER JOIN tbl_users t2 on t1.user_group_id = t2.user_group_id " + \
        " AND t2.user_id = %s"
    row = db.select_one(q, [user_id])
    if row:
        return row[0]
    else:
        return None

def verify_username(db, username, is_mobile=False):
    user_columns = ["user_id", "employee_name"]
    param = [username]
    # checking in tbl_users
    user_query = "SELECT user_id, employee_name  FROM tbl_users " + \
        " WHERE email_id = %s and is_active = 1"
    user_rows = db.select_all(user_query, param)
    if user_rows:
        result = convert_to_dict(user_rows, user_columns)
        if is_mobile is True :
                forms = get_user_form_ids(db, int(result[0]["user_id"]))
                form_ids = [int(x) for x in forms.split(",")]
                if 11 in form_ids :
                    return (
                        result[0]["user_id"],
                        result[0]["employee_name"]
                    )
                else :
                    return None
        else :
            return (
                result[0]["user_id"],
                result[0]["employee_name"]
            )
    else:  # checking in tbl_admin
        admin_query = " SELECT count(username) as count FROM tbl_admin " + \
            " WHERE username = %s"
        admin_rows = db.select_all(admin_query, param)
        count = admin_rows[0][0]
        if count > 0:
            return (0, "Administrator")
        else:
            return (None, None)


def verify_password(db, password, user_id):
    columns = "count(1)"
    encrypted_password = encrypt(password)
    condition = "1"
    rows = None
    if user_id == 0:
        condition = "password=%s"
        condition_val = [encrypted_password]
        rows = db.get_data(tblAdmin, columns, condition, condition_val)
    else:
        condition = "password=%s and user_id=%s"
        condition_val = [encrypted_password, user_id]
        rows = db.get_data(tblUsers, columns, condition, condition_val)
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
    columns = ["password"]
    values = [encrypt(password)]
    condition = "1"
    result = False
    if user_id != 0:
        condition = " user_id=%s"
        values.append(user_id)
        result = db.update(tblUsers, columns, values, condition)
    else:
        result = db.update(tblAdmin, columns, values, condition)

    if user_id != 0:
        columns = "employee_code, employee_name"
        condition = "user_id =%s"
        condition_val = [user_id]
        rows = db.get_data(tblUsers, columns, condition, condition_val)
        employee_name = rows[0]["employee_name"]
        if rows[0]["employee_code"] is not None:
            employee_name = "%s - %s" % (
                rows[0]["employee_code"], rows[0]["employee_name"]
            )
    else:
        employee_name = "Administrator"

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
        db.increment(
            tblUserLoginHistory, increament_column, increament_cond,
            condition_val=[user_id]
        )


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
