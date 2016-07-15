from server.common import (
    )
from server.clientdatabase.general import (
    get_user_company_details, get_countries_for_user,
    )

all__ = [
	"is_configured",
    "is_in_contract",
    "is_client_active",
    "verify_login",
    "is_contract_not_started",
    "add_session",
    "get_client_group",
    "get_client_configuration"

    ]

def is_configured(db):
    columns = "count(1)"
    condition = "1"
    rows = db.get_data(
        tblClientGroups, columns, condition
    )
    if rows[0][0] <= 0:
        return False
    else:
        return True

def is_in_contract(db):
    columns = "count(1)"
    condition = "now() between contract_from and DATE_ADD(contract_to, INTERVAL 1 DAY)"
    rows = db.get_data(
        tblClientGroups, columns, condition
    )
    if rows[0][0] <= 0:
        return False
    else:
        return True

def is_contract_not_started(db):
    columns = "count(1)"
    condition = "now() < contract_from"
    rows = db.get_data(
        tblClientGroups, columns, condition
    )
    if rows[0][0] <= 0:
        return False
    else:
        return True

def is_client_active(client_id):
    db_con = Database(
        KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
        KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
    )
    db_con.connect()
    db_con.begin()
    db_cur = db_con.cursor()
    q = "select count(*) from tbl_client_groups where \
    client_id = '%d' and is_active = 1" % client_id
    db_cur.execute(q)
    rows = db_cur.fetchall()
    db_con.commit()
    db_con.close()
    if rows[0][0] > 0:
        return True
    else:
        return False

def verify_login(db, username, password):
    tblAdminCondition = "password='%s' and username='%s'" % (
        password, username
    )
    admin_details = db.get_data(
        "tbl_admin", "*", tblAdminCondition
    )
    if (len(admin_details) == 0) :
        data_columns = [
            "user_id", "user_group_id", "email_id",
            "employee_name", "employee_code", "contact_no",
            "user_group_name", "form_ids", "is_admin",
            "service_provider_id"
        ]
        query = "SELECT t1.user_id, t1.user_group_id, t1.email_id, \
            t1.employee_name, t1.employee_code, t1.contact_no, \
            t2.user_group_name, t2.form_ids, t1.is_admin, \
            t1.service_provider_id \
            FROM tbl_users t1 INNER JOIN tbl_user_groups t2\
            ON t1.user_group_id = t2.user_group_id \
            WHERE t1.password='%s' and t1.email_id='%s' and t1.is_active=1" % (
                password, username
            )
        data_list = db.select_one(query)
        if data_list is None :
            return False
        else :
            result = db.convert_to_dict(data_list, data_columns)
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
    else :
        return True

def add_session(
    db, user_id, session_type_id, ip,
    employee, client_id=None
) :
    if client_id is not None:
        clear_old_session(db, user_id, session_type_id, client_id)
    else:
        clear_old_session(db, user_id, session_type_id)
    session_id = new_uuid()
    if client_id is not None:
        session_id = "%s-%s" % (client_id, session_id)
    updated_on = get_date_time()
    query = "INSERT INTO tbl_user_sessions \
        (session_token, user_id, session_type_id, last_accessed_time) \
        VALUES (%s, %s, %s, %s);"
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
    if row :
        result = db.convert_to_dict(row, ["client_id", "group_name"])
    return result

def get_client_configuration(db):
    q = "SELECT country_id, domain_id, period_from, period_to from tbl_client_configurations"
    rows = db.select_all(q)
    result = []
    if rows :
        result = db.convert_to_dict(rows, ["country_id", "domain_id", "period_from", "period_to"])
    c_list = []
    for r in result :
        info = core.ClientConfiguration(
            r["country_id"],
            r["domain_id"],
            r["period_from"],
            r["period_to"]
        )
        c_list.append(info)

    return c_list