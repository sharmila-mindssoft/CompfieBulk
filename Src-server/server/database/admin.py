import threading
from protocol import core
from server.database.tables import *
from server.common import (
    convert_to_dict, get_date_time,
    generate_and_return_password
)
from server.emailcontroller import EmailHandler as email
from server.exceptionmessage import process_error

__all__ = [
    "get_domains_for_user", "save_domain",
    "check_duplicate_domain", "get_domain_by_id",
    "update_domain", "check_domain_id_to_deactivate",
    "update_domain_status",
    "get_countries_for_user", "get_country_by_id",
    "check_duplicate_country", "save_country",
    "update_country", "check_country_id_to_deactivate",
    "update_country_status",
    "get_forms", "get_form_categories",
    "is_duplicate_user_group_name",
    "is_user_exists_under_user_group",
    "generate_new_user_group_id", "get_user_groups_from_db",
    "save_user_group", "update_user_group",
    "update_user_group_status",
    "get_detailed_user_list", "is_duplicate_email",
    "is_duplicate_employee_code",
    "save_user", "update_user",
    "update_user_status",
    "get_user_group_detailed_list",
    "get_user_countries", "get_user_domains"
]


#
# Domain
#

def get_domains_for_user(db, user_id) :
    # query = "CALL sp_get_domains_for_user (%s)" % (user_id)
    query = "SELECT distinct t1.domain_id, t1.domain_name, \
        t1.is_active FROM tbl_domains t1 "
    if user_id > 0 :
        query = query + " INNER JOIN tbl_user_domains t2 ON \
            t1.domain_id = t2.domain_id WHERE t2.user_id = %s \
            AND t1.is_active=1 "
    query = query + " ORDER BY t1.domain_name"
    if user_id > 0 :
        rows = db.select_all(query, [user_id])
    else :
        rows = db.select_all(query)
    result = []
    if rows :
        columns = ["domain_id", "domain_name", "is_active"]
        result = convert_to_dict(rows, columns)
    return return_domains(result)

def return_domains(data):
    results = []
    for d in data :
        results.append(core.Domain(
            d["domain_id"], d["domain_name"], bool(d["is_active"])
        ))
    return results

def save_domain(db, domain_name, user_id) :
    created_on = get_date_time()
    query = "INSERT INTO tbl_domains(domain_name, \
        created_by, created_on) \
        VALUES (%s, %s, %s) "
    res = db.execute(query, [
        domain_name, user_id, created_on
    ])
    if res is False :
        raise process_error("E024")
    action = "Add Domain - \"%s\"" % domain_name
    db.save_activity(user_id, 2, action)
    return True

def check_duplicate_domain(db, domain_name, domain_id) :
    isDuplicate = False
    query = "SELECT count(1) FROM tbl_domains WHERE domain_name = %s "

    if domain_id is not None :
        query = query + " AND domain_id != %s"
        param = [domain_name, domain_id]
    else :
        param = [domain_name]

    row = db.select_one(query, param)

    if row[0] > 0 :
        isDuplicate = True

    return isDuplicate

def get_domain_by_id(db, domain_id) :
    q = "SELECT domain_name FROM tbl_domains \
        WHERE domain_id=%s"
    row = db.select_one(q, [domain_id])
    domain_name = None
    if row :
        domain_name = row[0]
    return domain_name

def update_domain(db, domain_id, domain_name, updated_by) :
    oldData = get_domain_by_id(db, domain_id)
    if oldData is None :
        return False
    else :
        query = "UPDATE tbl_domains SET domain_name = %s, \
        updated_by = %s WHERE domain_id = %s"
        if db.execute(query, [domain_name, updated_by, domain_id]) :
            action = "Edit Domain - \"%s\"" % domain_name
            db.save_activity(updated_by, 2, action)
            return True
        else :
            raise process_error("E025")

def check_domain_id_to_deactivate(db, domain_id) :
    q = "SELECT count(*) from tbl_statutory_mappings where domain_id = %s"
    row = db.select_one(q, [domain_id])
    if row[0] > 0 :
        return False
    else :
        q = "SELECT count(*) from tbl_client_domains where domain_id = %s "
        row = db.select_one(q, [domain_id])
        if row[0] > 0 :
            return False
    return True

def update_domain_status(db, domain_id, is_active, updated_by) :
    oldData = get_domain_by_id(db, domain_id)
    if oldData is None :
        return False
    else :
        query = "UPDATE tbl_domains SET is_active = %s, \
        updated_by = %s WHERE domain_id = %s"
        if db.execute(query, [is_active, updated_by, domain_id]) :
            if is_active == 0 :
                status = "deactivated"
            else:
                status = "activated"
            action = "Domain %s status  - %s" % (oldData, status)
            db.save_activity(updated_by, 2, action)
            return True
        else :
            raise process_error("E026")

#
# Country
#
def get_user_countries(db, user_id):
    columns = "group_concat(country_id) as country_id"
    condition = " user_id = %s"
    condition_val = [str(user_id)]
    rows = db.get_data(tblUserCountries, columns, condition, condition_val)
    return rows[0]["country_id"]

def get_user_domains(db, user_id):
    columns = "group_concat(domain_id) as domain_id"
    condition = " user_id = %s"
    condition_val = (str(user_id))
    rows = db.get_data(tblUserDomains, columns, condition, condition_val)
    return rows[0]["domain_id"]


def get_countries_for_user(db, user_id) :

    query = "SELECT distinct t1.country_id, t1.country_name, \
        t1.is_active FROM tbl_countries t1 "
    if user_id > 0 :
        query = query + " INNER JOIN tbl_user_countries t2 \
            ON t1.country_id = t2.country_id WHERE t2.user_id = %s \
            AND t1.is_active = 1 "
    query = query + " ORDER BY t1.country_name"
    if user_id > 0 :
        rows = db.select_all(query, [user_id])
    else :
        rows = db.select_all(query)
    result = []
    if rows :
        columns = ["country_id", "country_name", "is_active"]
        result = convert_to_dict(rows, columns)
    return return_countries(result)

def return_countries(data) :
    results = []

    for d in data :
        results.append(core.Country(
            d["country_id"], d["country_name"], bool(d["is_active"])
        ))
    return results

def get_country_by_id(db, country_id) :
    q = "SELECT country_name FROM tbl_countries \
        WHERE country_id= %s "
    row = db.select_one(q, [country_id])
    country_name = row[0]
    return country_name

def check_duplicate_country(db, country_name, country_id) :
    isDuplicate = False
    query = "SELECT count(*) FROM tbl_countries WHERE country_name = %s "
    param = [str(country_name)]
    if country_id is not None :
        query = query + " AND country_id != %s"
        param = [str(country_name), str(country_id)]
    row = db.select_one(query, param)
    if row[0] > 0 :
        isDuplicate = True

    return isDuplicate

def save_country(db, country_name, created_by) :
    created_on = get_date_time()

    query = "INSERT INTO tbl_countries(country_name, created_by, created_on) \
        VALUES (%s, %s, %s) "
    if db.execute(query, (
        country_name, created_by, created_on
    ))  :
        action = "Add Country - \"%s\"" % country_name
        db.save_activity(created_by, 1, action)
        return True
    else :
        raise process_error("E027")

def update_country(db, country_id, country_name, updated_by) :
    oldData = get_country_by_id(db, country_id)
    if oldData is None :
        return False
    else :
        query = "UPDATE tbl_countries SET country_name = %s, \
        updated_by = %s WHERE country_id = %s"
        if db.execute(query, (
            country_name, updated_by, country_id
        )) :
            action = "Edit Country - \"%s\"" % country_name
            db.save_activity(updated_by, 1, action)
            return True
        else :
            raise process_error("E028")

def check_country_id_to_deactivate(db, country_id) :
    q = "SELECT count(*) from tbl_statutory_mappings where country_id = %s"
    row = db.select_one(q, [country_id])
    if row[0] > 0 :
        return False
    else :
        q = "SELECT count(*) from tbl_client_countries where country_id = %s "
        row = db.select_one(q, [country_id])
        if row[0] > 0 :
            return False
    return True


def update_country_status(db, country_id, is_active, updated_by) :
    oldData = get_country_by_id(db, country_id)
    if oldData is None :
        return False
    else :
        query = "UPDATE tbl_countries SET is_active = %s, \
        updated_by = %s WHERE country_id = %s"
        if is_active == 0:
            status = "deactivated"
        else:
            status = "activated"
        if db.execute(query, [
            is_active, updated_by, country_id
        ]) :
            action = "Country %s status  - %s" % (oldData, status)
            db.save_activity(updated_by, 1, action)
            return True
        else :
            raise process_error("E029")
#
#   Forms
#
def get_forms(db):
    columns = "tf.form_id, tf.form_category_id, tfc.form_category, \
    tf.form_type_id, tft.form_type, tf.form_name, tf.form_url, \
    tf.form_order, tf.parent_menu "
    tables = [tblForms, tblFormCategory, tblFormType]
    aliases = ["tf", "tfc", "tft"]
    join_conditions = [
        "tf.form_category_id = tfc.form_category_id",
        "tf.form_type_id = tft.form_type_id"
    ]
    where_condition = " tf.form_category_id in (3,2,4) order by tf.form_order"
    join_type = "left join"

    rows = db.get_data_from_multiple_tables(
        columns, tables, aliases, join_type,
        join_conditions, where_condition
    )
    return rows

def return_forms(form_ids=None):
    columns = ["form_id", "form_name"]
    condition = " form_id != '26' "
    if form_ids is not None:
        condition += " AND form_id in (%s) " % form_ids
    forms = db.get_data(tblForms, columns, condition)
    results = []
    for form in forms:
        results.append(general.AuditTrailForm(form[0], form[1]))
    return results

def get_form_categories(db):
    columns = "form_category_id, form_category"
    condition = " form_category_id in (2,3)"
    rows = db.get_data(tblFormCategory, columns, condition)
    return rows

#
#   Admin User Group
#
def is_duplicate_user_group_name(db, user_group_name, user_group_id=None):
    if user_group_id is not None :
        condition = "user_group_name = %s AND user_group_id != %s" % (
            user_group_name, user_group_id
        )
    else :
        condition = "user_group_name = %s" % (
            user_group_name
        )
    return db.is_already_exists(tblUserGroups, condition)

def is_user_exists_under_user_group(db, user_group_id):
    columns = "count(0) as count"
    condition = "user_group_id = %s"
    condition_val = [user_group_id]
    rows = db.get_data(
        tblUsers, columns, condition, condition_val
    )
    print "is_duplicate", rows
    if rows[0]["count"] > 0:
        return True
    else:
        return False

def generate_new_user_group_id(db) :
    return db.get_new_id("user_group_id", tblUserGroups)

def get_user_group_detailed_list(db) :
    columns = "ug.user_group_id, user_group_name, form_category_id, " + \
                "form_ids, is_active, (select count(*) from %s u where \
                ug.user_group_id = u.user_group_id) as count" % (tblUsers)
    tables = tblUserGroups+" ug"
    where_condition = " 1 order by user_group_name"
    rows = db.get_data(tables, columns, where_condition)
    return rows

def get_user_groups_from_db(db):
    columns = "user_group_id, user_group_name, is_active"
    where_condition = "1 order by user_group_name"
    rows = db.get_data(tblUserGroups, columns, where_condition)
    return rows

def save_user_group(
    db, user_group_name,
    form_category_id, form_ids
):
    time_stamp = str(get_date_time())
    columns = "( user_group_name, form_category_id, form_ids, \
    is_active, created_on, created_by, updated_on, updated_by)"
    forms = ",".join(str(x) for x in form_ids)
    values = [
        user_group_name, form_category_id,
        forms, 1, time_stamp,
        0, time_stamp, 0
    ]
    new_id = db.insert(tblUserGroups, columns, values)
    if new_id :
        action = "Created User Group \"%s\"" % user_group_name
        db.save_activity(0, 3, action)
        return True
    else :
        raise process_error("E030")

def update_user_group(
    db, user_group_id, user_group_name,
    form_category_id, form_ids
):

    time_stamp = get_date_time()
    columns = [
        "user_group_name", "form_category_id", "form_ids", "updated_on",
        "updated_by"
    ]
    values = [
        user_group_name, form_category_id,
        ",".join(str(x) for x in form_ids), time_stamp, 0
    ]
    condition = "user_group_id=%s" % user_group_id
    if db.update(tblUserGroups, columns, values, condition) :
        action = "Updated User Group \"%s\"" % user_group_name
        db.save_activity(0, 3, action)
    else :
        raise process_error("E031")

def update_user_group_status(db, user_group_id, is_active):
    time_stamp = get_date_time()
    columns = ["is_active", "updated_by", "updated_on"]
    values = [is_active, 0, time_stamp]
    condition = "user_group_id='%d'" % user_group_id
    result = db.update(tblUserGroups, columns, values, condition)
    if result is False :
        raise process_error("E032")
    action_columns = "user_group_name"
    rows = db.get_data(tblUserGroups, action_columns, condition)
    user_group_name = rows[0]["user_group_name"]
    action = ""
    if is_active == 0:
        action = "Deactivated User Group \"%s\"" % user_group_name
    else:
        action = "Activated User Group \"%s\"" % user_group_name
    db.save_activity(0, 3, action)
    return result

#
# Admin User
#
def get_detailed_user_list(db):
    columns = "user_id, email_id, user_group_id, employee_name, employee_code, \
        contact_no, address, designation, is_active"
    condition = "1"
    rows = db.get_data(tblUsers, columns, condition)
    return rows

def is_duplicate_email(db, email_id, user_id=None):
    if user_id is not None :
        condition = "email_id =%s AND user_id != %s"
        condition_val = [
            email_id, user_id
        ]
    else :
        condition = "email_id =%s "
        condition_val = [email_id]
    return db.is_already_exists(tblUsers, condition, condition_val)

def is_duplicate_employee_code(db, employee_code, user_id=None):
    if user_id is not None :
        condition = "employee_code =%s AND user_id != %s"
        condition_val = [
            employee_code, user_id
        ]
    else :
        condition = "employee_code =%s "
        condition_val = [employee_code]

    return db.is_already_exists(tblUsers, condition, condition_val)

def save_user(
    db, email_id, user_group_id, employee_name,
    employee_code, contact_no, address, designation, country_ids, domain_ids
):
    result1 = False
    result2 = False
    result3 = False
    current_time_stamp = get_date_time()
    user_columns = [
        "email_id", "user_group_id", "password", "employee_name",
        "employee_code", "contact_no", "is_active",
        "created_on", "created_by", "updated_on", "updated_by"
    ]
    encrypted_password, password = generate_and_return_password()
    user_values = [
        email_id, user_group_id, encrypted_password,
        employee_name, employee_code, contact_no,  1,
        current_time_stamp, 0, current_time_stamp, 0
    ]
    if address is not None:
        user_columns.append("address")
        user_values.append(address)
    if designation is not None:
        user_columns.append("designation")
        user_values.append(designation)
    new_id = db.insert(tblUsers, user_columns, user_values)
    print new_id
    if new_id is False :
        raise process_error("E033")
    else :
        user_id = new_id
        result1 = True
    country_columns = ["user_id", "country_id"]
    country_values_list = []
    for country_id in country_ids:
        country_value_tuple = (user_id, int(country_id))
        country_values_list.append(country_value_tuple)
    result2 = db.bulk_insert(tblUserCountries, country_columns, country_values_list)
    if result2 is False :
        raise process_error("E034")
    domain_columns = ["user_id", "domain_id"]
    domain_values_list = []
    for domain_id in domain_ids:
        domain_value_tuple = (user_id, int(domain_id))
        domain_values_list.append(domain_value_tuple)
    result3 = db.bulk_insert(tblUserDomains, domain_columns, domain_values_list)
    if result3 is False :
        raise process_error("E035")
    action = "Created User \"%s - %s\"" % (employee_code, employee_name)
    db.save_activity(0, 4, action)
    notify_user_thread = threading.Thread(
        target=notify_user, args=[
            email_id, password, employee_name, employee_code
        ]
    )
    notify_user_thread.start()
    return (result1 and result2 and result3)

def notify_user(
    email_id, password, employee_name, employee_code
):
    try:
        email().send_knowledge_user_credentials(
            email_id, password, employee_name, employee_code
        )
    except Exception, e:
        print "Error while sending email : {}".format(e)

def update_user(
    db, user_id, user_group_id, employee_name, employee_code, contact_no,
    address, designation, country_ids, domain_ids
):
    result1 = False
    result2 = False
    result3 = False

    current_time_stamp = get_date_time()
    user_columns = [
        "user_group_id", "employee_name", "employee_code",
        "contact_no", "address", "designation",
        "updated_on", "updated_by"
    ]
    user_values = [
        user_group_id, employee_name, employee_code, contact_no,
        address, designation, current_time_stamp, 0, user_id
    ]
    user_condition = "user_id = %s"
    user_condition_val = [user_id]
    result1 = db.update(tblUsers, user_columns, user_values, user_condition)
    if result1 is False :
        raise process_error("E036")
    db.delete(tblUserCountries, user_condition, user_condition_val)
    db.delete(tblUserDomains, user_condition, user_condition_val)

    country_columns = ["user_id", "country_id"]
    country_values_list = []
    for country_id in country_ids:
        country_value_tuple = (user_id, int(country_id))
        country_values_list.append(country_value_tuple)
    result2 = db.bulk_insert(
        tblUserCountries, country_columns,
        country_values_list
    )
    if result2 is False :
        raise process_error("E037")
    domain_columns = ["user_id", "domain_id"]
    domain_values_list = []
    for domain_id in domain_ids:
        domain_value_tuple = (user_id, int(domain_id))
        domain_values_list.append(domain_value_tuple)
    result3 = db.bulk_insert(
        tblUserDomains, domain_columns,
        domain_values_list
    )
    if result3 is False :
        raise process_error("E038")
    action = "Updated User \"%s - %s\"" % (employee_code, employee_name)
    db.save_activity(0, 4, action)

    return (result1 and result2 and result3)

def update_user_status(db, user_id, is_active):
    columns = ["is_active", "updated_on" , "updated_by"]
    values = [is_active, get_date_time(), 0]
    condition = "user_id='%d'" % user_id
    result = db.update(tblUsers, columns, values, condition)
    if result is False :
        raise process_error("E039")
    action_columns = "employee_name, employee_code"
    rows = db.get_data(tblUsers, action_columns, condition)
    employee_name = rows[0]["employee_name"]
    employee_code = rows[0]["employee_code"]
    action = ""
    if is_active == 1:
        action = "Activated User \"%s - %s\"" % (employee_code, employee_name)
    else:
        action = "Dectivated User \"%s - %s\"" % (employee_code, employee_name)
    db.save_activity(0, 4, action)
    return result
