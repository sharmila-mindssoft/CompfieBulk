from replication.protocol import (
    Change, Client
)

from distribution.protocol import (
    Company, IPAddress
)

from server.common import (
    convert_to_dict, datetime_to_string,
    string_to_datetime, datetime_to_string_time
)
from server.database.tables import *
from protocol import (general, core)
#
# Companies
#
__all__ = [
    "get_trail_id",
    "get_trail_log",
    "get_trail_log_for_domain",
    "remove_trail_log", "get_servers",
    "get_client_replication_list",
    "update_client_replication_status",
    "update_client_domain_status", "get_user_forms",
    "get_user_form_ids", "get_notifications",
    "get_user_type",
    "get_compliance_duration", "get_compliance_repeat",
    "get_compliance_frequency", "get_approval_status",
    "get_audit_trails",
    "update_profile"
]


def get_trail_id(db):
    query = "select IFNULL(MAX(audit_trail_id), 0) as audit_trail_id " + \
        " from tbl_audit_log;"
    row = db.select_one(query)
    trail_id = row[0]
    return trail_id


def get_trail_log(db, client_id, received_count):
    query = "SELECT "
    query += "  audit_trail_id, tbl_name, tbl_auto_id,"
    query += "  column_name, value, client_id, action"
    query += " from tbl_audit_log WHERE audit_trail_id > %s "
    query += " AND (client_id = 0 OR client_id= %s) LIMIT 100;"

    rows = db.select_all(query, [received_count, client_id])
    results = []
    if rows:
        columns = [
            "audit_trail_id", "tbl_name", "tbl_auto_id",
            "column_name", "value", "client_id", "action"
        ]
        results = convert_to_dict(rows, columns)
    if len(results) == 0:
        update_client_replication_status(db, client_id, received_count)
    return return_changes(results)


def get_trail_log_for_domain(
    db, client_id, domain_id, received_count, actual_count
):
    q = "SELECT tbl_auto_id from tbl_audit_log where audit_trail_id > %s " + \
        " and audit_trail_id < %s " + \
        " AND tbl_name = 'tbl_compliances' " + \
        " AND column_name = 'domain_id' " + \
        " AND value = %s limit 10"
    q_rows = db.select_all(q, [received_count, actual_count, domain_id])
    auto_id = []
    for r in q_rows:
        auto_id.append(str(r[0]))

    rows = None
    if len(auto_id) > 0:
        query = "SELECT "
        query += "  audit_trail_id, tbl_name, tbl_auto_id,"
        query += "  column_name, value, client_id, action"
        query += " from tbl_audit_log WHERE tbl_name = 'tbl_compliances' " + \
            " AND audit_trail_id> %s AND " + \
            " tbl_auto_id IN (%s) "
        rows = db.select_all(query, [
            received_count,
            ','.join(auto_id)
        ])
    results = []
    if rows:
        columns = [
            "audit_trail_id", "tbl_name", "tbl_auto_id",
            "column_name", "value", "client_id", "action"
        ]
        results = convert_to_dict(rows, columns)
    if len(results) == 0:
        update_client_replication_status(
            db, client_id, 0, type="domain_trail_id"
        )
    return return_changes(results)


def return_changes(data):
    results = []
    for d in data:
        change = Change(
            int(d["audit_trail_id"]),
            d["tbl_name"],
            int(d["tbl_auto_id"]),
            d["column_name"],
            d["value"],
            int(d["client_id"]),
            d["action"]
        )
        results.append(change)
    return results


def remove_trail_log(db, client_id, received_count):
    q = "delete from tbl_audit_log where audit_trail_id <= %s " + \
        " and client_id = %s"
    db.execute(q, [received_count, client_id])


def get_servers(db):
    query = "SELECT client_id, machine_id, database_ip, "
    query += "database_port, database_username, "
    query += "database_password, client_short_name, "
    query += "database_name, server_ip, server_port "
    query += "FROM tbl_client_database"
    rows = db.select_all(query)
    results = []
    if rows:
        columns = [
            "client_id", "machine_id", "database_ip",
            "database_port", "database_username",
            "database_password", "client_short_name",
            "database_name", "server_ip", "server_port"
        ]
        results = convert_to_dict(rows, columns)
    return return_companies(results)


def return_companies(data):
    results = []
    for d in data:
        database_ip = IPAddress(
            d["database_ip"],
            int(d["database_port"])
        )
        company_server_ip = IPAddress(
            d["server_ip"],
            int(d["server_port"])
        )
        results.append(Company(
            int(d["client_id"]),
            d["client_short_name"],
            d["database_username"],
            d["database_password"],
            d["database_name"],
            database_ip,
            company_server_ip
        ))
    return results


def get_client_replication_list(db):
    q = "select client_id, is_new_data, is_new_domain, " + \
        " domain_id from tbl_client_replication_status " + \
        " where is_new_data = 1"
    rows = db.select_all(q)
    results = []
    if rows:
        column = [
            "client_id", "is_new_data", "is_new_domain", "domain_id"
        ]
        results = convert_to_dict(rows, column)
    return _return_clients(results)


def _return_clients(data):
    results = []
    for d in data:
        results.append(Client(
            int(d["client_id"]),
            bool(d["is_new_data"]),
            bool(d["is_new_domain"]),
            d["domain_id"]
        ))
    return results


def update_client_replication_status(
    db, client_id, received_count, type=None
):
    if type is None:
        q = "update tbl_client_replication_status set is_new_data = 0 " + \
            " where client_id = %s"
        remove_trail_log(db, client_id, received_count)
    else:
        q = "update tbl_client_replication_status set is_new_domain = 0, " + \
            " domain_id = '' where client_id = %s"
    db.execute(q, [client_id])


def update_client_domain_status(db, client_id, domain_ids):
    q = "update tbl_client_replication_status set is_new_data =1, " + \
        " is_new_domain = 1, domain_id = %s where client_id = %s"
    db.execute(q, (
            str((','.join(domain_ids))),
            client_id
        ))


def get_user_forms(db, form_ids):
    columns = "tf.form_id, tf.form_category_id, tfc.form_category," + \
        " tf.form_type_id, tft.form_type, " + \
        " tf.form_name, tf.form_url, tf.form_order, tf.parent_menu"
    tables = ["tbl_forms", "tbl_form_category", "tbl_form_type"]
    aliases = ["tf", "tfc", "tft"]
    join_conditions = [
        "tf.form_category_id = tfc.form_category_id",
        "tf.form_type_id = tft.form_type_id"
    ]
    form_ids_list = [int(x) for x in form_ids.split(",")]
    where_condition, where_condition_val = db.generate_tuple_condition(
        "tf.form_id", form_ids_list
    )
    where_condition += " order by tf.form_order "
    join_type = "left join"
    rows = db.get_data_from_multiple_tables(
        columns, tables,
        aliases, join_type,
        join_conditions, where_condition,
        [where_condition_val]
    )
    return rows

#
# general controllers methods
#


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

#
#   Notifications
#


def get_user_type(db, user_id):
    columns = "user_group_id"
    condition = "user_id = %s"
    condition_val = [user_id]
    result = db.get_data(tblUsers, columns, condition, condition_val)
    user_group_id = result[0]["user_group_id"]

    columns = "form_category_id"
    condition = "user_group_id = %s"
    result = db.get_data(tblUserGroups, columns, condition, [user_group_id])
    if result[0]["form_category_id"] in [2, "2"]:
        return "Knowledge"
    else:
        return "Techno"


def get_notifications(
    db, notification_type, session_user, client_id=None
):
    user_type = None
    if session_user != 0:
        user_type = get_user_type(db, session_user)

    columns = "tn.notification_id, notification_text, link, " + \
        "created_on, read_status"
    join_type = "left join"
    tables = [tblNotifications, tblNotificationsStatus]
    aliases = ["tn", "tns"]
    join_conditions = ["tn.notification_id = tns.notification_id"]
    where_condition = " tns.user_id =%s "
    where_condition_val = [session_user]
    if user_type == "Techno":
        where_condition += " AND link not like %s "
        cond = "%sstatutory%s" % ("%", "%")
        where_condition_val.append(cond)
    elif user_type == "Knowledge":
        where_condition += " AND link not like %s "
        cond = "%client%s" % ("%", "%")
        where_condition_val.append(cond)
    where_condition += "order by created_on DESC limit 30"
    rows = db.get_data_from_multiple_tables(
        columns, tables,
        aliases, join_type, join_conditions, where_condition,
        where_condition_val
    )
    notifications = []
    for row in rows:
        notifications.append(general.Notification(
            row["notification_id"], row["notification_text"], row["link"],
            bool(row["created_on"]), datetime_to_string(row["created_on"])
        ))
    return notifications


def get_compliance_duration(db):
    def return_compliance_duration(data):
        duration_list = []
        for d in data:
            duration = core.DURATION_TYPE(d["duration_type"])
            duration_list.append(
                core.ComplianceDurationType(
                    d["duration_type_id"], duration
                )
            )
        return duration_list
    result = db.get_data(
        "tbl_compliance_duration_type",
        ["duration_type_id", "duration_type"], None
    )
    return return_compliance_duration(result)


def get_compliance_repeat(db):
    def return_compliance_repeat(data):
        repeat_list = []
        for d in data:
            repeat = core.REPEATS_TYPE(d["repeat_type"])
            repeat_list.append(
                core.ComplianceRepeatType(
                    d["repeat_type_id"], repeat
                )
            )
        return repeat_list
    result = db.get_data(
        "tbl_compliance_repeat_type", ["repeat_type_id", "repeat_type"], None
    )
    return return_compliance_repeat(result)


def get_compliance_frequency(db):
    def return_compliance_frequency(data):
        frequency_list = []
        for d in data:
            frequency = core.COMPLIANCE_FREQUENCY(
                d["frequency"]
            )
            c_frequency = core.ComplianceFrequency(
                d["frequency_id"], frequency
            )
            frequency_list.append(c_frequency)
        return frequency_list
    result = db.get_data(
        "tbl_compliance_frequency",
        ["frequency_id", "frequency"], None
    )
    return return_compliance_frequency(result)


def get_approval_status(db, approval_id=None):
    def return_approval_status(data):
        approval_list = []
        for sts in enumerate(data):
            approve = core.APPROVAL_STATUS(sts[1])
            c_approval = core.StatutoryApprovalStatus(
                sts[0], approve
            )
            approval_list.append(c_approval)
        return approval_list

    status = ("Pending", "Approved", "Rejected", "Approved & Notified")

    if approval_id is None:
        return return_approval_status(status)
    else:
        return status[int(approval_id)]


#
#   Audit Trail
#
def return_forms(db, form_ids=None):
    columns = "form_id, form_name"
    condition = " form_id != 26 "
    condition_val = None
    if form_ids is not None:
        condition += " AND "
        form_ids_list = [int(x) for x in form_ids.split(",")]
        condition, condition_val = db.generate_tuple_condition(
            "form_id", form_ids_list)
    forms = db.get_data(tblForms, columns, condition, [condition_val])
    results = []
    for form in forms:
        results.append(
            general.AuditTrailForm(form["form_id"], form["form_name"])
        )
    return results


def get_users(db, condition="1", condition_val=None):
    columns = "user_id, employee_name, employee_code, is_active"
    rows = db.get_data(tblUsers, columns, condition, condition_val)
    return rows


def return_users(db, condition="1", condition_val=None):
    user_rows = get_users(db, condition, condition_val)
    results = []
    for user in user_rows:
        employee_name = "%s - %s" % (
            user["employee_code"], user["employee_name"]
        )
        results.append(core.User(
            user["user_id"], employee_name, bool(user["is_active"])
        ))
    return results


def get_audit_trails(
    db, session_user, from_count, to_count,
    from_date, to_date, user_id, form_id
):
    form_column = ["form_id"]
    form_condition = "form_type_id != 3"
    rows = db.get_data(
        tblForms, form_column, form_condition
    )
    forms = None
    form_ids = [int(row["form_id"]) for row in rows]
    forms = return_forms(
        db, ",".join(str(x) for x in form_ids)
    )

    query = " SELECT user_id from tbl_users where user_group_id = ( " + \
        " SELECT user_group_id from tbl_users where user_id = %s ) "
    rows = db.select_all(query, [session_user])
    result = convert_to_dict(rows, ["user_id"])
    user_ids = []
    for row in result:
        user_ids.append(row["user_id"])
    condition, condition_val = db.generate_tuple_condition("user_id", user_ids)
    users = return_users(db, condition, [condition_val])

    from_date = string_to_datetime(from_date).date()
    to_date = string_to_datetime(to_date).date()
    where_qry = "1"
    where_qry_val = []
    if from_date is not None and to_date is not None:
        where_qry += " AND  date(created_on) between %s AND %s "
        where_qry_val.extend([from_date, to_date])
    if user_id is not None:
        where_qry += " AND user_id = %s "
        where_qry_val.append(user_id)
    if form_id is not None:
        where_qry += " AND form_id = %s "
        where_qry_val.append(form_id)
    columns = "user_id, form_id, action, created_on"
    where_qry += " AND %s " % (condition)
    where_qry_val.append(condition_val)
    where_qry += " ORDER BY created_on DESC"

    c_rows = db.get_data(tblActivityLog, "count(0) as total", where_qry, where_qry_val)
    c_total = 0
    for c in c_rows :
        c_total = c["total"]

    where_qry += " LIMIT %s, %s"
    where_qry_val.extend([from_count, to_count])
    rows = db.get_data(tblActivityLog, columns, where_qry, where_qry_val)
    audit_trail_details = []
    for row in rows:
        user_id = row["user_id"]
        form_id = row["form_id"]
        action = row["action"]
        date = datetime_to_string_time(row["created_on"])
        audit_trail_details.append(
            general.AuditTrail(user_id, form_id, action, date)
        )
    return general.GetAuditTrailSuccess(audit_trail_details, users, forms, c_total)


#
#   Update Profile
#
def update_profile(db, contact_no, address, session_user):
    columns = ["contact_no", "address"]
    condition = "user_id= %s"
    values = [contact_no, address, session_user]
    db.update(tblUsers, columns, values, condition)
