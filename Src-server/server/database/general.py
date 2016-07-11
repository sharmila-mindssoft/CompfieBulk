from replication.protocol import (
    Change, Client
)

from distribution.protocol import (
    Company, IPAddress
)

from server.common import (
    convert_to_dict, datetime_to_string
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
    "get_compliance_frequency", "get_approval_status"
]

def get_trail_id(db):
    query = "select IFNULL(MAX(audit_trail_id), 0) as audit_trail_id from tbl_audit_log;"
    row = db.select_one(query)
    trail_id = row[0]
    return trail_id

def get_trail_log(db, client_id, received_count):
    query = "SELECT "
    query += "  audit_trail_id, tbl_name, tbl_auto_id,"
    query += "  column_name, value, client_id, action"
    query += " from tbl_audit_log WHERE audit_trail_id>%s AND (client_id = 0 OR client_id=%s) LIMIT 100;"

    rows = db.select_all(query, (received_count, client_id))
    results = []
    if rows :
        columns = [
            "audit_trail_id", "tbl_name", "tbl_auto_id",
            "column_name", "value", "client_id", "action"
        ]
        results = convert_to_dict(rows, columns)
    if len(results) == 0 :
        update_client_replication_status(db, client_id, received_count)
    return return_changes(results)

def get_trail_log_for_domain(db, client_id, domain_id, received_count, actual_count):
    q = "SELECT tbl_auto_id from tbl_audit_log where audit_trail_id > %s and audit_trail_id < %s \
        AND tbl_name = 'tbl_compliances' \
        AND column_name = 'domain_id' \
        AND value = %s limit 10"
    q_rows = db.select_all(q, (received_count, actual_count, domain_id))
    auto_id = []
    # print q
    for r in q_rows :
        auto_id.append(str(r[0]))

    rows = None
    if len(auto_id) > 0 :
        query = "SELECT "
        query += "  audit_trail_id, tbl_name, tbl_auto_id,"
        query += "  column_name, value, client_id, action"
        query += " from tbl_audit_log WHERE tbl_name = 'tbl_compliances' \
            AND audit_trail_id>%s AND  \
            tbl_auto_id IN (%s)  "
        # print "-"
        # print query
        rows = db.select_all(query, (
            received_count,
            ','.join(auto_id)
        ))
    results = []
    if rows :
        columns = [
            "audit_trail_id", "tbl_name", "tbl_auto_id",
            "column_name", "value", "client_id", "action"
        ]
        results = convert_to_dict(rows, columns)
    # print len(results)
    if len(results) == 0 :
        update_client_replication_status(db, client_id, 0, type="domain_trail_id")
    return return_changes(results)

def return_changes(data):
    results = []
    for d in data :
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
    q = "delete from tbl_audit_log where audit_trail_id < %s and client_id = %s"
    db.execute(q, (received_count, client_id))

def get_servers(db):
    query = "SELECT client_id, machine_id, database_ip, "
    query += "database_port, database_username, "
    query += "database_password, client_short_name, "
    query += "database_name, server_ip, server_port "
    query += "FROM tbl_client_database"
    rows = db.select_all(query)
    results = []
    if rows :
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
    for d in data :
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

def get_client_replication_list(db) :
    q = "select client_id, is_new_data, is_new_domain, domain_id from tbl_client_replication_status \
        where is_new_data = 1"
    rows = db.select_all(q)
    results = []
    if rows :
        column = [
            "client_id", "is_new_data", "is_new_domain", "domain_id"
        ]
        results = convert_to_dict(rows, column)
        # print results
    return _return_clients(results)

def _return_clients(data):
    results = []
    for d in data :
        results.append(Client(
            int(d["client_id"]),
            bool(d["is_new_data"]),
            bool(d["is_new_domain"]),
            d["domain_id"]
        ))
    return results

def update_client_replication_status(db, client_id, received_count, type=None):
    if type is None :
        q = "update tbl_client_replication_status set is_new_data = 0 where client_id = %s" % (client_id)
        remove_trail_log(db, client_id, received_count)
    else :
        q = "update tbl_client_replication_status set is_new_domain = 0, domain_id = '' where client_id = %s"
    # print q
    db.execute(q, (client_id))

def update_client_domain_status(db, client_id, domain_ids) :
    q = "update tbl_client_replication_status set is_new_data =1, \
        is_new_domain = 1, domain_id = '%s' where client_id = %s"
    # print q
    db.execute(q, (
            str((','.join(domain_ids))),
            client_id
        ))

def get_user_forms(db, form_ids):

    columns = "tf.form_id, tf.form_category_id, tfc.form_category, \
        tf.form_type_id, tft.form_type,\
        tf.form_name, tf.form_url, tf.form_order, tf.parent_menu"
    tables = ["tbl_forms", "tbl_form_category", "tbl_form_type"]
    aliases = ["tf", "tfc", "tft"]
    join_conditions = [
        "tf.form_category_id = tfc.form_category_id",
        "tf.form_type_id = tft.form_type_id"
    ]
    where_condition = " tf.form_id in (%s) order by tf.form_order" % (form_ids)

    join_type = "left join"
    rows = db.get_data_from_multiple_tables(
        columns, tables,
        aliases, join_type,
        join_conditions, where_condition
    )
    return rows

#
# general controllers methods
#

def get_user_form_ids(self, user_id) :
    if user_id == 0 :
        return "1, 2, 3, 4"
    q = "select t1.form_ids from tbl_user_groups t1 \
        INNER JOIN tbl_users t2 on t1.user_group_id = t2.user_group_id \
        AND t2.user_id = %s"
    row = self.select_one(q, (user_id))
    if row :
        return row[0]
    else :
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
    if session_user != 0 :
        user_type = get_user_type(db, session_user)

    columns = "tn.notification_id, notification_text, link, " + \
        "created_on, read_status"
    join_type = "left join"
    tables = [tblNotifications, tblNotificationsStatus]
    aliases = ["tn", "tns"]
    join_conditions = ["tn.notification_id = tns.notification_id"]
    where_condition = " tns.user_id ='%d' " % (
        session_user
    )
    if user_type == "Techno":
        where_condition += " AND link not like '%sstatutory%s' " % ("%" , "%")
    elif user_type == "Knowledge":
        where_condition += " AND link not like '%sclient%s'" % ("%" , "%")
    where_condition += "order by created_on DESC limit 30"
    rows = db.get_data_from_multiple_tables(
        columns, tables,
        aliases, join_type, join_conditions, where_condition
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
        for d in data :
            duration = core.DURATION_TYPE(d["duration_type"])
            duration_list.append(
                core.ComplianceDurationType(
                    d["duration_type_id"], duration
                )
            )
        return duration_list

    columns = ["duration_type_id", "duration_type"]
    rows = db.get_data("tbl_compliance_duration_type", "*", None)
    result = []
    if rows :
        result = convert_to_dict(rows, columns)
    return return_compliance_duration(result)

def get_compliance_repeat(db):

    def return_compliance_repeat(data):
        repeat_list = []
        for d in data :
            repeat = core.REPEATS_TYPE(d["repeat_type"])
            repeat_list.append(
                core.ComplianceRepeatType(
                    d["repeat_type_id"], repeat
                )
            )
        return repeat_list

    columns = ["repeat_type_id", "repeat_type"]
    rows = db.get_data("tbl_compliance_repeat_type", "*", None)
    result = []
    if rows :
        result = convert_to_dict(rows, columns)
    return return_compliance_repeat(result)

def get_compliance_frequency(db):

    def return_compliance_frequency(data) :
        frequency_list = []
        for d in data :
            frequency = core.COMPLIANCE_FREQUENCY(
                d["frequency"]
            )
            c_frequency = core.ComplianceFrequency(
                d["frequency_id"], frequency
            )
            frequency_list.append(c_frequency)
        return frequency_list

    columns = ["frequency_id", "frequency"]
    rows = db.get_data("tbl_compliance_frequency", "*", None)
    result = []
    if rows :
        result = convert_to_dict(rows, columns)
    return return_compliance_frequency(result)

def get_approval_status(db, approval_id=None):

    def return_approval_status(data):
        approval_list = []
        for sts in enumerate(data) :
            approve = core.APPROVAL_STATUS(sts[1])
            c_approval = core.StatutoryApprovalStatus(
                sts[0], approve
            )
            approval_list.append(c_approval)
        return approval_list

    status = ("Pending", "Approved", "Rejected", "Approved & Notified")

    if approval_id is None :
        return return_approval_status(status)
    else :
        return status[int(approval_id)]
