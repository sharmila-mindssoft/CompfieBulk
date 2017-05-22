from replication.protocol import (
    Change, Client
)

from distribution.protocol import (
    Company, IPAddress, Server, FileServer, IPInfo
)

from server.common import (
    datetime_to_string,
    string_to_datetime, datetime_to_string_time
)
from server.database.tables import *
from server.database.admin import *
from server.exceptionmessage import fetch_error
from protocol import (generalprotocol, core)
from server import logger
import traceback
#
# Companies
#
__all__ = [
    "get_trail_id",
    "get_trail_log",
    "get_trail_log_for_domain",
    "remove_trail_log", "get_servers", "get_group_servers",
    "get_group_server_info", "get_group_servers_db_info",
    "get_client_replication_list",
    "update_client_replication_status",
    "update_client_domain_status", "get_user_forms",
    "get_user_form_ids", "get_notifications",
    "get_user_type",
    "get_compliance_duration", "get_compliance_repeat",
    "get_compliance_frequency", "get_approval_status",
    "get_audit_trails",
    "update_profile", "return_compliance_duration",
    "return_compliance_repeat", "return_compliance_frequency",
    "return_approval_status",
    "update_statutory_notification_status",
    "get_short_name",
    "update_message_status",
    "validate_user_rights"
]


def get_trail_id(db):
    query = "select IFNULL(MAX(audit_trail_id), 0) as audit_trail_id " + \
        " from tbl_audit_log;"
    row = db.select_one(query)
    trail_id = row["audit_trail_id"]
    return trail_id


def get_trail_log(db, client_id, received_count, is_group):
    query = "SELECT "
    query += "  audit_trail_id, tbl_name, tbl_auto_id,"
    query += "  column_name, value, client_id, action, legal_entity_id"
    query += " from tbl_audit_log WHERE audit_trail_id > %s "
    if is_group :
        query += " AND client_id= %s"
        param = [received_count, client_id]
    else :
        query += " AND (legal_entity_id=0 or legal_entity_id= %s)"
        query += " AND (client_id = 0 or client_id = (select client_id from tbl_legal_entities where legal_entity_id = %s))"

        param = [received_count, client_id, client_id]

    query += " LIMIT 200;"

    rows = db.select_all(query, param)

    results = rows
    if len(rows) == 0:
        update_client_replication_status(db, client_id, received_count, is_group)
    return return_changes(results)


def get_trail_log_for_domain(
    db, client_id, domain_id, received_count, actual_count
):
    q = "SELECT tbl_auto_id from tbl_audit_log where audit_trail_id > %s " + \
        " and audit_trail_id < %s " + \
        " AND tbl_name = 'tbl_compliances' " + \
        " AND column_name = 'domain_id' " + \
        " AND value = %s limit 100"
    q_rows = db.select_all(q, [received_count, actual_count, domain_id])
    print q_rows
    auto_id = []
    for r in q_rows:
        auto_id.append(str(r["tbl_auto_id"]))

    rows = None
    results = []
    if len(auto_id) > 0:
        query = "SELECT "
        query += "  audit_trail_id, tbl_name, tbl_auto_id,"
        query += "  column_name, value, client_id, action, legal_entity_id"
        query += " from tbl_audit_log WHERE tbl_name = 'tbl_compliances' " + \
            " AND audit_trail_id> %s AND " + \
            " tbl_auto_id IN (%s) "
        rows = db.select_all(query, [
            received_count,
            ','.join(auto_id)
        ])
        results = rows
        # print rows

    if len(auto_id) == 0:
        update_client_replication_status(
            db, client_id, 0, 0, "domain_trail_id"
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
            d["action"],
            d["legal_entity_id"]
        )
        results.append(change)
    return results


def remove_trail_log(db, client_id, received_count):
    q = "delete from tbl_audit_log where audit_trail_id <= %s " + \
        " and legal_entity_id = %s"
    db.execute(q, [received_count, client_id])


def get_servers(db):
    query = "select t2.database_ip, t2.database_port, ct1.database_username, ct1.database_password," + \
        " ct1.database_name , t1.client_id, t1.legal_entity_id, t4.short_name, " + \
        " t3.machine_id, t3.machine_name, t3.ip as server_ip, t3.port as server_port, ct1.is_group " + \
        " from tbl_client_database as t1 " + \
        " inner join tbl_client_database_info as ct1 on t1.client_database_id = ct1.client_database_id " + \
        " inner join tbl_database_server as t2 on t1.database_server_id = t2.database_server_id " + \
        " inner join tbl_application_server as t3 on t1.machine_id = t3.machine_id " + \
        " inner join tbl_client_groups as t4 on t1.client_id = t4.client_id "
    rows = db.select_all(query)
    return return_companies(rows)

def get_group_servers_db_info(db, group_id=None):
    query = "select t2.database_ip, t2.database_port, ct1.database_username, ct1.database_password," + \
        " ct1.database_name , t1.client_id, t1.legal_entity_id, t4.short_name, " + \
        " t3.machine_id, t3.machine_name, t3.ip as server_ip, t3.port as server_port, ct1.is_group " + \
        " from tbl_client_database as t1 " + \
        " inner join tbl_client_database_info as ct1 on t1.client_database_id = ct1.client_database_id and is_group = 1 " + \
        " inner join tbl_database_server as t2 on t1.database_server_id = t2.database_server_id " + \
        " inner join tbl_application_server as t3 on t1.machine_id = t3.machine_id " + \
        " inner join tbl_client_groups as t4 on t1.client_id = t4.client_id "

    param = []
    if group_id is not None :
        query += " WHERE t1.client_id=%s"
        param = [group_id]

    rows = db.select_all(query, param)
    return rows

def get_group_server_info(db, group_id=None):
    query = "select distinct t1.client_id, t1.legal_entity_id, t4.short_name, " + \
        " t2.ip as file_ip, t2.port as file_port, " + \
        " t3.machine_id, t3.machine_name, t3.ip as server_ip, t3.port as server_port " + \
        " from tbl_client_database as t1 " + \
        " inner join tbl_file_server as t2 on t1.file_server_id = t2.file_server_id " + \
        " inner join tbl_application_server as t3 on t1.machine_id = t3.machine_id " + \
        " inner join tbl_client_groups as t4 on t1.client_id = t4.client_id "
    param = []
    if group_id is not None :
        query += " WHERE t1.client_id=%s"
        param = [group_id]

    rows = db.select_all(query, param)
    return rows

def get_group_servers(db):
    rows = get_group_server_info(db)
    result = {}
    for r in rows :
        client_id = r["client_id"]
        company_server_ip = IPAddress(r["server_ip"], int(r["server_port"]))

        file_server_ip = IPAddress(r["file_ip"], r["file_port"])

        if result.get(client_id) is None :
            result[client_id] = Server(
                client_id, r["short_name"], company_server_ip,
                [FileServer(file_server_ip, r["legal_entity_id"])],
                True
            )
        else :
            result[client_id].file_server_info.append(
                FileServer(file_server_ip, r["legal_entity_id"])
            )

    return result.values()


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
        is_group = bool(d["is_group"])

        if is_group is True:
            company_id = d["client_id"]
        else:
            company_id = d["legal_entity_id"]
        results.append(Company(
            int(company_id),
            d["short_name"],
            d["database_username"],
            d["database_password"],
            d["database_name"],
            database_ip,
            company_server_ip,
            is_group
        ))
    return results

def get_ip_details(db):
    q = "select t1.client_id, t3.short_name, t1.form_id, t2.form_url, t1.ips " + \
        "from tbl_ip_settings as t1 " + \
        "inner join tbl_client_forms as t2 " + \
        "on t1.form_id = t2.form_id " + \
        "inner join tbl_client_groups as t3 on t1.client_id = t3.client_id"
    rows = db.select_all(q)
    data = {}
    for r in rows :
        short_name = r["short_name"]
        ips = r["ips"].split(',')
        form_url = r["form_url"]
        if data.get(short_name) is None :
            data[short_name] = []

        data[short_name].append(IPInfo(form_url, ips))
    return data

def get_client_replication_list(db):
    q = "select t1.client_id, t1.is_new_data, t1.domain_id, t1.is_new_domain, t1.is_group, " + \
        " if (t1.is_group = 1, 0, t2.client_id ) as group_id, " + \
        " if (t1.is_group = 1, 0, t2.country_id ) as country_id " + \
        " from tbl_client_replication_status as t1 " + \
        " left join tbl_legal_entities as t2 on t1.client_id = t2.legal_entity_id and is_created = 1 " + \
        " and is_approved = 1 " + \
        " where t1.is_new_data = 1 or is_new_domain = 1;"

    rows = db.select_all(q)
    return _return_clients(rows)


def _return_clients(data):
    results = []
    for d in data:
        results.append(Client(
            int(d["client_id"]),
            bool(d["is_new_data"]),
            bool(d["is_new_domain"]),
            d["domain_id"],
            bool(d["is_group"]),
            d["group_id"], d["country_id"]
        ))
    return results


def update_client_replication_status(
    db, client_id, received_count, is_group, type=None
):
    if type is None:
        q = "update tbl_client_replication_status set is_new_data = 0 " + \
            " where client_id = %s and is_group = %s"
        if is_group is False :
            remove_trail_log(db, client_id, received_count)
    else:
        q = "update tbl_client_replication_status set is_new_domain = 0, " + \
            " domain_id = '' where client_id = %s and is_group = %s"
    db.execute(q, [client_id, int(is_group)])


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


def get_admin_forms(db, username):
    result = db.call_proc(
       "sp_admin_getformcategory", (username,)
    )
    form_category_id = result[0]["fc_id"]
    return db.call_proc(
        "sp_tbl_forms_getadminforms", (form_category_id,))


#
# general controllers methods
#
def get_user_form_ids(db, user_id, admin_user_type=None):
    result = []
    procedure = "sp_tbl_forms_getuserformids"
    result = db.call_proc(procedure, [user_id, admin_user_type])
    if user_id == 0:
        f_ids = []
        for r in result:
            f_ids.append(str(r["form_id"]))
        return ','.join(f_ids)
    else:
        if result:
            return result[0]["form_id"]
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
        notifications.append(generalprotocol.Notification(
            row["notification_id"], row["notification_text"], row["link"],
            bool(row["created_on"]), datetime_to_string(row["created_on"])
        ))
    return notifications

def get_messages(
    db, from_count, page_count, session_user
):
    expected_result = 2
    args = [from_count, page_count, session_user]
    rows = db.call_proc_with_multiresult_set('sp_get_messages', args, expected_result)

    messages = []
    for row in rows[1]:
        messages.append(generalprotocol.Message(
            row["message_id"], row["message_heading"], row["message_text"], row["link"],
            row["created_by"], datetime_to_string_time(row["created_on"])
        ))
    return messages

def update_message_status(
    db, message_id, user_id, has_read, session_user
):
    result = db.call_update_proc(
        "sp_message_read_status",
        (message_id, user_id, has_read)
    )
    if result:
        return True
    else:
        return False

def get_statutory_notifications(
    db, from_count, page_count, session_user
):
    args = [from_count, page_count, session_user]
    rows = db.call_proc('sp_get_statutory_notifications', args)

    get_statutory_notifications = []
    for row in rows:
        get_statutory_notifications.append(generalprotocol.StatutoryNotification(
            row["notification_id"], row["user_id"], row["compliance_id"], row["notification_text"],
            row["created_by"], datetime_to_string_time(row["created_on"]), bool(row["read_status"])
        ))
    return get_statutory_notifications

def update_statutory_notification_status(
    db, notification_id, user_id, has_read, session_user
):
    result = db.call_update_proc(
        "sp_statutory_notification_read_status",
        (notification_id, user_id, has_read)
    )
    if result:
        return True
    else:
        return False


def return_compliance_duration(data):
    duration_list = []
    for d in data:
        duration = core.DURATION_TYPE(d["duration_type"])
        duration_list.append(
            generalprotocol.ComplianceDurationType(
                d["duration_type_id"], duration
            )
        )
    return duration_list

def get_compliance_duration(db):
    result = db.get_data(
        "tbl_compliance_duration_type",
        ["duration_type_id", "duration_type"], None
    )
    return return_compliance_duration(result)

def return_compliance_repeat(data):
    repeat_list = []
    for d in data:
        repeat = core.REPEATS_TYPE(d["repeat_type"])
        repeat_list.append(
            generalprotocol.ComplianceRepeatType(
                d["repeat_type_id"], repeat
            )
        )
    return repeat_list

def get_compliance_repeat(db):
    result = db.get_data(
        "tbl_compliance_repeat_type", ["repeat_type_id", "repeat_type"], None
    )
    return return_compliance_repeat(result)


def return_compliance_frequency(data):
    frequency_list = []
    for d in data:
        frequency = core.COMPLIANCE_FREQUENCY(
            d["frequency"]
        )
        c_frequency = generalprotocol.ComplianceFrequency(
            d["frequency_id"], frequency
        )
        frequency_list.append(c_frequency)
    return frequency_list


def get_compliance_frequency(db):
    result = db.call_proc(
        "sp_statutory_mapping_report_frequency", ()
    )
    return return_compliance_frequency(result)

def return_approval_status(data):
    approval_list = []
    for sts in enumerate(data):
        approve = core.APPROVAL_STATUS(sts[1])
        c_approval = generalprotocol.StatutoryApprovalStatus(
            sts[0], approve
        )
        approval_list.append(c_approval)
    return approval_list

def get_approval_status(db, approval_id=None):
    status = ("Pending", "Approved", "Rejected", "Approved & Notified")

    if approval_id is None:
        return return_approval_status(status)
    else:
        return status[int(approval_id)]


#
#   Audit Trail
#
def return_forms(forms):
    result = []
    for f in forms :
        result.append(
            generalprotocol.AuditTrailForm(f["form_id"], f["form_name"])
        )

    return result


def get_users(db, condition="1", condition_val=None):
    columns = "user_id, employee_name, employee_code, is_active"
    rows = db.get_data(tblUsers, columns, condition, condition_val)
    return rows


def return_users(users):
    result = []
    for u in users :
        if u["user_category_id"] == 2:
            employee_name = "Console Admin"
        else:
            employee_name = "%s - %s" % (u["employee_code"], u["employee_name"])
        result.append(
            core.User(
                u["user_id"], u["user_category_id"], employee_name, bool(u["is_active"])
            )
        )
    return result

def return_client_users(users):
    result = []
    for u in users :
        employee_name = "%s - %s" % (u["employee_code"], u["employee_name"])
        result.append(
            core.AuditTrailClientUser(
                u["user_id"], u["user_category_id"], u["user_category_name"], employee_name, bool(u["is_active"]),
                u["client_id"], u["legal_entity_id"], u["unit_id"]
            )
        )
    return result

def get_user_cetegories_db(db):
    userCategoryList = []
    rows = get_form_categories(db)
    for row in rows:
        userCategoryList.append(core.UserCategory(
            row["user_category_id"], row["user_category_name"])
        )
    return userCategoryList

###############################################################################
#  To get list of activity log under a form or user
#  Parameters : Object of database, Received request
#  Return Type : Returns List of object of activities log
###############################################################################
def get_audit_trails(
    db, session_user, from_count, to_count,
    from_date, to_date, user_id, form_id,
    category_id, client_id, legal_entity_id, unit_id
):
    if user_id is None:
        user_id = '%'
    if form_id is None :
        form_id = '%'
    if category_id is None :
        category_id = '%'
    if unit_id is None :
        unit_id = '%'
    if legal_entity_id is None :
        legal_entity_id = '%'
    from_date = string_to_datetime(from_date).date()
    to_date = string_to_datetime(to_date).date()
    args = [from_date, to_date, user_id, form_id, category_id, from_count, to_count]
    expected_result = 2
    print client_id
    print args
    if client_id is None:
        result = db.call_proc_with_multiresult_set('sp_get_audit_trails', args, expected_result)
    else:
        args = [from_date, to_date, user_id, form_id, category_id, client_id, legal_entity_id, unit_id, from_count, to_count]
        result = db.call_proc_with_multiresult_set('sp_get_client_audit_trails', args, expected_result)
    '''
        'sp_get_audit_trails' this procedure will return four result-set which are Forms, Users, Activity_log_data and Activity_log total
    '''

    activity_log = result[0]
    total = result[1]

    assert len(total) > 0
    c_total = total[0]["total"]

    audit_trail_details = []
    for row in activity_log:
        user_id = row["user_id"]
        user_category_id = row["user_category_id"]
        form_id = row["form_id"]
        action = row["action"]
        date = datetime_to_string_time(row["created_on"])
        audit_trail_details.append(
            generalprotocol.AuditTrail(user_id, user_category_id, form_id, action, date)
        )
    return generalprotocol.GetAuditTrailSuccess(audit_trail_details, c_total)

###############################################################################
#  To get list of User category
#  Parameters : Object of database
#  Return Type : Returns List of object of user category
###############################################################################
def get_user_cetegories_audit_trail(db):
    userCategoryList = []
    rows = db.call_proc("sp_audit_trail_usercategory_list", None)
    j = 0
    for row in rows:
        j = j + 1
        userCategoryList.append(core.UserCategory(
            row["user_category_id"], row["user_category_name"])
        )
    j = j + 1
    userCategoryList.append(core.UserCategory(
        j, "Client"
    ))
    return userCategoryList

###############################################################################
#  To get list of users, user categories, forms
#  Parameters : Object of database
#  Return Type : Returns List of object of user category, forms, users list
###############################################################################
def get_audit_trail_filters(db):
    user_categories = get_user_cetegories_audit_trail(db)
    expected_result = 6
    result = db.call_proc_with_multiresult_set('sp_countries_for_audit_trails', (), expected_result)
    countries = result[0]
    audit_trail_countries = []
    for row in countries:
        user_id = row["user_id"]
        user_category_id = row["user_category_id"]
        country_id = row["country_id"]
        country_name = row["country_name"]
        audit_trail_countries.append(
            generalprotocol.AuditTrailCountries(user_id, user_category_id, country_id, country_name)
        )
    forms_list = return_forms(result[1])
    users = return_users(result[2])
    forms_log = result[3]
    audit_trail_details = []
    for row in forms_log:
        user_id = row["user_id"]
        user_category_id = row["user_category_id"]
        form_id = row["form_id"]
        action = row["action"]
        date = datetime_to_string_time(row["created_on"])
        audit_trail_details.append(
            generalprotocol.AuditTrail(user_id, user_category_id, form_id, action, date)
        )

    # client users
    audit_client_users = return_client_users(result[4])
    client_audit_details = return_forms(result[5])
    # for row in result[5]:
    #     client_audit_details.append(generalprotocol.ClientAuditTrail(
    #         row["user_id"], row["user_category_id"], row["form_id"], row["action"],
    #         datetime_to_string_time(row["created_on"]), row["client_id"],
    #         row["legal_entity_id"], row["unit_id"]
    #     ))

    # client details
    result = db.call_proc_with_multiresult_set("sp_audit_trail_client_user_filters", (), 6)
    print result
    clients = []
    for row in result[0]:
        clients.append(core.Client(
            row["client_id"], row["group_name"], bool(row["is_active"])
        ))

    business_group_list = []
    for row in result[1]:
        business_group_list.append(core.BusinessGroup(
            row["business_group_id"], row["business_group_name"],
            int(row["client_id"])
        ))

    unit_legal_entity = []
    for row in result[2]:
        unit_legal_entity.append(core.UnitLegalEntity(
            row["legal_entity_id"], row["legal_entity_name"],
            row["business_group_id"], int(row["client_id"]),
            row["country_id"], "0", 1
        ))

    divs = []
    for row in result[3]:
        divs.append(core.Division(
            row["division_id"], row["division_name"],
            row["legal_entity_id"], row["business_group_id"],
            int(row["client_id"])
        ))

    categories = []
    for row in result[4]:
        categories.append(core.Category(
            row["category_id"], row["category_name"], row["division_id"],
            row["legal_entity_id"], row["business_group_id"],
            int(row["client_id"])
        ))

    client_audit_units = []
    for row in result[5]:
        client_audit_units.append(core.AuditUnits(
            int(row["client_id"]), row["business_group_id"], row["legal_entity_id"],
            row["division_id"], row["category_id"], row["unit_id"],
            row["unit_name"]
        ))

    return generalprotocol.GetAuditTrailFilterSuccess(
        user_categories, audit_trail_countries, forms_list, users, audit_trail_details,
        audit_client_users, client_audit_details, clients, business_group_list,
        unit_legal_entity, divs, categories, client_audit_units
    )


#
#   Update Profile
#
def update_profile(db, contact_no, address, mobile_no, email_id, session_user):
    db.call_proc("sp_update_profile", (contact_no,address,mobile_no,email_id,session_user,))

    # columns = ["contact_no", "address", "mobile_no", "email_id"]
    # condition = "user_id= %s"
    # values = [contact_no, address, mobile_no, email_id, session_user]
    # db.update(tblUsers, columns, values, condition)

#
#   Verify Password
#
def verify_password(db, user_id, encrypt_password):

    row = db.call_proc("sp_verify_password", (user_id,encrypt_password,))
    # if int(row[0]["count"]) == 0:
    #     raise process_error("E065")
    # else
    return int(row[0]["count"])


#  get_short_name
def get_short_name(db, client_id):
    q = "select short_name from tbl_client_groups where client_id = %s"
    row = db.select_one(q, [client_id])
    return row.get("short_name")

def validate_user_rights(db, session_token, caller_name):
    print "validate_user_rights"
    try :
        user_id = db.validate_session_token(session_token)
        print "----------"
        print user_id

        print user_id, caller_name
        if user_id is True and caller_name not in ("/knowledge/home", "/knowledge/profile") :
            print user_id
            rows = db.call_proc_with_multiresult_set("sp_verify_user_rights", [user_id, caller_name], 2)
            print rows
            if rows :
                if rows[1][0].get("form_url") == caller_name :
                    return user_id
            else :
                return False
        elif user_id :
            return user_id
        else :
            return False

    except Exception, e :
        logger.logKnowledge("error", "validate_rights", str(traceback.format_exc()))
        logger.logKnowledge("error", "validate_rights", str(e))
        raise fetch_error()

def get_info_count(
    db, session_user
):
    expected_result = 2
    args = [session_user]
    rows = db.call_proc_with_multiresult_set('sp_info_count', args, expected_result)

    m_count = rows[0][0].get('m_count')
    s_count = rows[1][0].get('s_count')

    return m_count, s_count
