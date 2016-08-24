from server.clientdatabase.tables import *

from server.common import (
   convert_to_dict, new_uuid, get_date_time, get_date_time_in_date
)

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
    "get_login_attempt_and_time"

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
    data_columns = [
        "user_id", "user_group_id", "email_id",
        "employee_name", "employee_code", "contact_no",
        "user_group_name", "form_ids", "is_admin",
        "service_provider_id", "is_primary_admin"
    ]
    query = "SELECT t1.user_id, t1.user_group_id, t1.email_id, " + \
        " t1.employee_name, t1.employee_code, t1.contact_no, " + \
        " t2.user_group_name, t2.form_ids, t1.is_admin, " + \
        " t1.service_provider_id, t1.is_primary_admin " + \
        " FROM tbl_users t1 LEFT JOIN tbl_user_groups t2 " + \
        " ON t1.user_group_id = t2.user_group_id " + \
        " WHERE t1.password= %s and t1.email_id= %s and t1.is_active=1"

    data_list = db.select_one(query, [password, username])
    print data_list
    if data_list is None:
        return False
    else:
        result = convert_to_dict(data_list, data_columns)
        if result["is_primary_admin"] == 1:
            return True
        if is_service_proivder_user(db, result["user_id"]):
            if (
                is_service_provider_in_contract(
                    db, result["service_provider_id"]
                )
            ):
                # result["client_id"] = client_id
                return result
            else:
                return "ContractExpired"
        else:
            return result


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
    query = "INSERT INTO tbl_user_sessions " + \
        " (session_token, user_id, session_type_id, last_accessed_time) " + \
        " VALUES (%s, %s, %s, %s);"
    db.execute(query, (session_id, user_id, session_type_id, updated_on))

    # action = "Log In by - \"%s\" from \"%s\"" % ( employee, ip)
    action = "Log In by - \"%s\" " % (employee)
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
        info = core.ClientConfiguration(
            r["country_id"],
            r["domain_id"],
            r["period_from"],
            r["period_to"]
        )
        c_list.append(info)

    return c_list


def clear_old_session(db, user_id, session_type_id, client_id=None):
    query = "DELETE FROM tbl_user_sessions " + \
        " WHERE user_id=%s and session_type_id=%s"
    db.execute(query, (
        user_id, session_type_id
    ))


def check_and_update_login_attempt(db, user_id):
    current_date_time = get_date_time_in_date()
    rows = get_login_attempt_and_time(db, user_id)
    if(rows):
        last_login_time = rows[0]["login_time"]
        diff = relativedelta.relativedelta(current_date_time, last_login_time)
        if diff.hours > 2 or diff.days > 0:
            db.update(
                tblUserLoginHistory, ["login_attempt"], [0],
                " user_id=%s " % user_id
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
        increament_cond = " user_id = %s " % (user_id)
        db.increment(tblUserLoginHistory, increament_column, increament_cond)


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
