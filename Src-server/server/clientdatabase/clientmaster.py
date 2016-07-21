from server.clientdatabase.tables import *

from server.clientdatabase.general import (
    is_primary_admin, is_admin, get_user_unit_ids,
    get_users, get_users_by_id, get_user_countries,
    get_user_domains
)

from server.common import (
    datetime_to_string, get_date_time,
    string_to_datetime, generate_and_return_password, convert_to_dict
)

__all__ = [
    "get_service_provider_details_list",
    "generate_new_service_provider_id",
    "is_duplicate_service_provider",
    "save_service_provider",
    "update_service_provider",
    "is_service_provider_in_contract",
    "is_user_exists_under_service_provider",
    "update_service_provider_status",
    "get_forms",
    "generate_new_user_privilege_id",
    "is_duplicate_user_privilege",
    "get_user_privilege_details_list",
    "get_user_privileges",
    "save_user_privilege",
    "update_user_privilege",
    "is_user_exists_under_user_group",
    "update_user_privilege_status",
    "get_user_details",
    "get_service_providers",
    "get_no_of_remaining_licence",
    "is_duplicate_user_email",
    "is_duplicate_employee_code",
    "save_user",
    "update_user",
    "update_user_status",
    "update_admin_status",
    "get_units_closure_for_user",
    "close_unit",
    "get_audit_trails",
]

def get_service_provider_details_list(db, client_id):
    columns = "service_provider_id, service_provider_name, address, contract_from," + \
            "contract_to, contact_person, contact_no, is_active"
    rows = db.get_data(
        tblServiceProviders, columns, "1 ORDER BY service_provider_name"
    )
    columns = [
        "service_provider_id", "service_provider_name", "address", "contract_from",
        "contract_to", "contact_person", "contact_no", "is_active"
    ]
    result = convert_to_dict(rows, columns)
    return return_service_provider_details(result)

def return_service_provider_details(service_providers):
    results = []
    for service_provider in service_providers :
        service_provider_obj = core.ServiceProviderDetails(
            service_provider["service_provider_id"],
            service_provider["service_provider_name"],
            service_provider["address"],
            datetime_to_string(service_provider["contract_from"]),
            datetime_to_string(service_provider["contract_to"]),
            service_provider["contact_person"],
            service_provider["contact_no"],
            bool(service_provider["is_active"]))
        results.append(service_provider_obj)
    return results

#
#   Service Provider
#

def generate_new_service_provider_id(db, client_id) :
    return db.get_new_id("service_provider_id", tblServiceProviders,  client_id)

def is_duplicate_service_provider(
    db, service_provider_id, service_provider_name, client_id
):
    condition = "service_provider_name ='%s' AND service_provider_id != '%d'" % (
        service_provider_name, service_provider_id)
    return db.is_already_exists(tblServiceProviders, condition, client_id)

def save_service_provider(db, service_provider_id, service_provider, session_user, client_id):
    current_time_stamp = get_date_time()
    contract_from = string_to_datetime(service_provider.contract_from)
    contract_to = string_to_datetime(service_provider.contract_to)
    columns = [
        "service_provider_id", "service_provider_name", "address", "contract_from",
        "contract_to", "contact_person", "contact_no", "created_on", "created_by",
        "updated_on", "updated_by"
    ]
    values = [
        service_provider_id, service_provider.service_provider_name,
        service_provider.address, contract_from, contract_to,
        service_provider.contact_person, service_provider.contact_no,
        current_time_stamp, session_user, current_time_stamp, session_user
    ]
    result = db.insert(tblServiceProviders, columns, values, client_id)

    action = "Created Service Provider \"%s\"" % service_provider.service_provider_name
    db.save_activity(session_user, 2, action, client_id)

    return result

def update_service_provider(db, service_provider, session_user, client_id):
    column = "count(*)"
    condition = "now() between contract_from and contract_to \
    and service_provider_id = '%d'" % service_provider.service_provider_id
    rows = db.get_data(tblServiceProviders, column, condition)
    if int(rows[0][0]) > 0:
        contract_status_before_update = True
    else:
        contract_status_before_update = False

    current_time_stamp = get_date_time()
    contract_from = string_to_datetime(service_provider.contract_from)
    contract_to = string_to_datetime(service_provider.contract_to)
    columns_list = [
        "service_provider_name", "address", "contract_from", "contract_to",
        "contact_person", "contact_no", "updated_on", "updated_by"
    ]
    values_list = [
        service_provider.service_provider_name, service_provider.address,
        contract_from, contract_to, service_provider. contact_person,
        service_provider.contact_no, current_time_stamp, session_user
    ]
    condition = "service_provider_id='%d'" % service_provider.service_provider_id
    result = db.update(tblServiceProviders, columns_list, values_list, condition, client_id)

    column = "count(*)"
    condition = "now() between contract_from and contract_to \
    and service_provider_id = '%d'" % service_provider.service_provider_id
    rows = db.get_data(tblServiceProviders, column, condition)

    if int(rows[0][0]) > 0:
        contract_status_after_update = True
    else:
        contract_status_after_update = False

    if contract_status_before_update is False and contract_status_after_update is True:
        update_service_provider_status(
            db, service_provider.service_provider_id,  1, session_user, client_id
        )
    elif contract_status_before_update is True and contract_status_after_update is False:
        update_service_provider_status(
            db, service_provider.service_provider_id,  0, session_user, client_id
        )

    action = "Updated Service Provider \"%s\"" % service_provider.service_provider_name
    db.save_activity(session_user, 2, action, client_id)

    return result

def is_service_provider_in_contract(db, service_provider_id):
    column = "count(1)"
    condition = "now() between contract_from and DATE_ADD(contract_to, INTERVAL 1 DAY)\
    and service_provider_id = '%d' and is_active = 1" % service_provider_id
    rows = db.get_data(tblServiceProviders, column, condition)
    if rows[0][0] > 0:
        return True
    else:
        return False

def is_user_exists_under_service_provider(db, service_provider_id):
    columns = "count(*)"
    condition = "service_provider_id = '%d'" % service_provider_id
    rows = db.get_data(
        tblUsers, columns, condition
    )
    if rows[0][0] > 0:
        return True
    else:
        return False

def update_service_provider_status(db, service_provider_id,  is_active, session_user, client_id):
    is_active = 1 if is_active is not False else 0
    columns = ["is_active", "updated_on" , "updated_by"]
    values = [is_active, get_date_time(), session_user]
    condition = "service_provider_id='%d'" % service_provider_id
    result = db.update(tblServiceProviders, columns, values, condition, client_id)

    action_column = "service_provider_name"
    rows = db.get_data(
        tblServiceProviders, action_column,
        condition
    )
    service_provider_name = rows[0][0]
    action = None
    if is_active == 1:
        action = "Activated Service Provider \"%s\"" % service_provider_name
    else:
        action = "Deactivated Service Provider \"%s\"" % service_provider_name
    db.save_activity(session_user, 2, action, client_id)

    return result

def get_forms(db, client_id):
    columns = "tf.form_id, tf.form_type_id, tft.form_type, "
    columns += "tf.form_name, tf.form_url, tf.form_order, tf.parent_menu"
    tables = [tblForms, tblFormType]
    aliases = ["tf",  "tft"]
    joinConditions = ["tf.form_type_id = tft.form_type_id"]
    whereCondition = " is_admin = 0 and tf.form_type_id not in (5) \
    order by tf.form_order, tf.form_name ASC"
    joinType = "left join"
    rows = db.get_data_from_multiple_tables(
        columns, tables, aliases, joinType,
        joinConditions, whereCondition
    )
    return rows

def generate_new_user_privilege_id(db, client_id) :
    return db.get_new_id("user_group_id", tblUserGroups, client_id)

def is_duplicate_user_privilege(
    db, user_group_id, user_privilege_name, client_id
):
    condition = "user_group_name ='%s' AND user_group_id != '%d'" % (
        user_privilege_name, user_group_id)
    return db.is_already_exists(tblUserGroups, condition)

def get_user_privilege_details_list(db, client_id):
    columns = "user_group_id, user_group_name, form_ids, is_active"
    rows = db.get_data(
        tblUserGroups, columns, "1 ORDER BY user_group_name"
    )
    return rows

def get_user_privileges(db, client_id):
    columns = "user_group_id, user_group_name, is_active"
    rows = db.get_data(
        tblUserGroups, columns, "1 ORDER BY user_group_name"
    )

    columns = ["user_group_id", "user_group_name", "is_active"]
    result = convert_to_dict(rows, columns)
    return return_user_privileges(result)

def return_user_privileges(user_privileges):
    results = []
    for user_privilege in user_privileges :
        results.append(core.UserGroup(
            user_privilege["user_group_id"], user_privilege["user_group_name"],
            bool(user_privilege["is_active"])
        ))
    return results

def save_user_privilege(db, user_group_id, user_privilege, session_user, client_id):
    columns = [
        "user_group_id", "user_group_name", "form_ids", "is_active",
        "created_on", "created_by", "updated_on", "updated_by"
    ]
    values_list = [
        user_group_id, user_privilege.user_group_name,
        ",".join(str(x) for x in user_privilege.form_ids), 1,
        get_date_time(), session_user, get_date_time(),
        session_user
    ]
    result = db.insert(tblUserGroups, columns, values_list)

    action = "Created User Group \"%s\"" % user_privilege.user_group_name
    db.save_activity(session_user, 3, action, client_id)

    return result

def update_user_privilege(db, user_privilege, session_user, client_id):
    columns = ["user_group_name", "form_ids", "updated_on", "updated_by"]
    values = [
        user_privilege.user_group_name, ",".join(str(x) for x in user_privilege.form_ids),
        get_date_time(), session_user
    ]
    condition = "user_group_id='%d'" % user_privilege.user_group_id
    result = db.update(tblUserGroups, columns, values, condition)

    action = "Updated User Group \"%s\"" % user_privilege.user_group_name
    db.save_activity(session_user, 3, action)

    return result

def is_user_exists_under_user_group(db, user_group_id):
    columns = "count(*)"
    condition = "user_group_id = '%d'" % user_group_id
    rows = db.get_data(
        tblUsers, columns, condition
    )
    if rows[0][0] > 0:
        return True
    else:
        return False

def update_user_privilege_status(db, user_group_id, is_active, session_user, client_id):
    is_active = 0 if is_active is not True else 1
    columns = ["is_active", "updated_by", "updated_on"]
    values = [is_active, session_user, get_date_time()]
    condition = "user_group_id='%d'" % user_group_id
    result = db.update(tblUserGroups, columns, values, condition)

    action_column = "user_group_name"
    rows = db.get_data(
        tblUserGroups, action_column, condition
    )
    user_group_name = rows[0][0]
    action = None
    if is_active == 0:
        action = "Deactivated user group \"%s\"" % user_group_name
    else:
        action = "Activated user group \"%s\"" % user_group_name
    db.save_activity(session_user, 3, action, client_id)
    return result

def get_user_details(db, client_id, session_user):
    unit_ids = None
    if not is_primary_admin(db, session_user):
        unit_ids = get_user_unit_ids(db, session_user)
    columns = "user_id, email_id, user_group_id, employee_name," + \
        "employee_code, contact_no, seating_unit_id, user_level, " + \
        " is_admin, is_service_provider, service_provider_id, is_active, \
    is_primary_admin"
    condition = "1 ORDER BY employee_name"
    rows = db.get_data(
        tblUsers + " tu", columns, condition
    )
    columns = [
        "user_id", "email_id", "user_group_id", "employee_name",
        "employee_code", "contact_no", "seating_unit_id", "user_level",
        "is_admin", "is_service_provider", "service_provider_id", "is_active",
        "is_primary_admin"
    ]
    result = convert_to_dict(rows, columns)
    return return_user_details(db, result, client_id, unit_ids)

def return_user_details(
    db, users, client_id, unit_ids=None
):
    unit_ids_list = []
    if unit_ids not in [None, "", "None"]:
        try :
            unit_ids_list = [int(x) for x in unit_ids.split(",")]
        except e :
            unit_ids_list = []
    results = []
    for user in users :
        query = "select unit_id from %s tuu where \
        user_id = '%d'" % (tblUserUnits, user["user_id"])
        rows = db.select_all(query)
        user_unit_ids = []
        for row in rows:
            user_unit_ids.append(row[0])
        if len(unit_ids_list) > 0:
            if len(user_unit_ids) > 0:
                if set(user_unit_ids) & set(unit_ids_list):
                    pass
                else:
                    continue
        countries = get_user_countries(db, user["user_id"], client_id)
        domains = get_user_domains(db, user["user_id"], client_id)
        units = get_user_unit_ids(db, user["user_id"], client_id)
        results.append(core.ClientUser(user["user_id"], user["email_id"],
            user["user_group_id"], user["employee_name"],
            user["employee_code"], user["contact_no"],
            user["seating_unit_id"], user["user_level"],
            [int(x) for x in countries.split(",")] if countries is not None else [],
            [int(x) for x in domains.split(",")] if domains is not None else [],
            [int(x) for x in units.split(",")] if units is not None else [],
            bool(user["is_admin"]), bool(user["is_service_provider"]),
            user["service_provider_id"], bool(user["is_active"]),
            bool(user["is_primary_admin"])
        ))
    return results

def get_service_providers(db, client_id=None):
    columns = "service_provider_id, service_provider_name, is_active"
    condition = "1"
    rows = db.get_data(
        tblServiceProviders, columns, condition
    )
    columns = ["service_provider_id", "service_provider_name", "is_active"]
    result = convert_to_dict(rows, columns)
    return return_service_providers(result)

def return_service_providers(service_providers):
    results = []
    for service_provider in service_providers :
        service_provider_obj = core.ServiceProvider(
            service_provider["service_provider_id"],
            service_provider["service_provider_name"],
            bool(service_provider["is_active"]))
        results.append(service_provider_obj)
    return results

def get_no_of_remaining_licence(db):
    columns = "count(*)"
    condition = "1"
    rows = db.get_data(tblUsers, columns, condition)
    no_of_licence_holders = rows[0][0]

    columns = "no_of_user_licence"
    rows = db.get_data(tblClientGroups, columns, condition)
    no_of_licence = rows[0][0]

    remaining_licence = int(no_of_licence) - int(no_of_licence_holders)
    return remaining_licence

def is_duplicate_user_email(db, user_id, email_id, client_id):
    flag1 = False
    flag2 = False
    columns = "count(*)"
    condition = "username = '%s'" % email_id
    rows = db.get_data(tblAdmin, columns, condition)
    if rows[0][0] > 0 :
        flag1 = True
    else:
        flag1 = False
    condition = "email_id ='%s' AND user_id != '%d'" % (
        email_id, user_id)
    flag2 = db.is_already_exists(tblUsers, condition, client_id)
    return (flag1 or flag2)

def is_duplicate_employee_code(db, user_id, employee_code, client_id):
    condition = "employee_code ='%s' AND user_id != '%d'" % (
        employee_code, user_id)
    return db.is_already_exists(tblUsers, condition, client_id)

def save_user(db, user_id, user, session_user, client_id):
    result1 = None
    result2 = None
    result3 = None
    current_time_stamp = get_date_time()
    user.is_service_provider = 0 if user.is_service_provider is False else 1
    columns = [
        "user_id", "user_group_id", "email_id", "password", "employee_name",
        "employee_code", "contact_no", "user_level",
        "is_admin", "is_service_provider", "created_by", "created_on",
        "updated_by", "updated_on"
    ]
    encrypted_password, password = generate_and_return_password()
    values = [
        user_id, user.user_group_id, user.email_id,
        encrypted_password, user.employee_name,
        user.employee_code.replace(" ", ""), user.contact_no, user.user_level,
        0, user.is_service_provider, session_user, current_time_stamp,
        session_user, current_time_stamp
    ]
    if user.is_service_provider == 1:
        columns.append("service_provider_id")
        values.append(user.service_provider_id)
    else:
        columns.append("seating_unit_id")
        values.append(user.seating_unit_id)

    result1 = db.insert(tblUsers, columns, values, client_id)

    db_con = Database(
        KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
        KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
    )
    db_con.connect()
    db_con.begin()
    columns = "client_id, user_id, email_id, employee_name, \
    employee_code, contact_no, created_on, is_admin, is_active"
    if user.seating_unit_id is not None:
        columns += ", seating_unit_id"
    q = "INSERT INTO tbl_client_users ({}) values ('{}', '{}', '{}', '{}', \
    '{}', '{}', now(), 0, 1".format(
        columns, client_id, user_id, user.email_id, user.employee_name,
        user.employee_code, user.contact_no
    )

    if user.seating_unit_id is not None:
        q += ",'{}')".format(user.seating_unit_id)
    else:
        q += ")"
    db_con.execute(q)
    db_con.commit()
    db_con.close()

    country_columns = ["user_id", "country_id"]
    country_values_list = []
    for country_id in user.country_ids:
        country_value_tuple = (user_id, int(country_id))
        country_values_list.append(country_value_tuple)
    result2 = db.bulk_insert(tblUserCountries, country_columns, country_values_list, client_id)

    domain_columns = ["user_id", "domain_id"]
    domain_values_list = []
    for domain_id in user.domain_ids:
        domain_value_tuple = (user_id, int(domain_id))
        domain_values_list.append(domain_value_tuple)
    result3 = db.bulk_insert(tblUserDomains, domain_columns, domain_values_list, client_id)

    unit_columns = ["user_id", "unit_id"]
    unit_values_list = []
    for unit_id in user.unit_ids:
        unit_value_tuple = (user_id, int(unit_id))
        unit_values_list.append(unit_value_tuple)
    result4 = db.bulk_insert(tblUserUnits, unit_columns, unit_values_list, client_id)

    action = "Created user \"%s - %s\"" % (user.employee_code, user.employee_name)
    db.save_activity(session_user, 4, action, client_id)
    short_name = get_short_name_from_client_id(db, client_id)
    notify_user_thread = threading.Thread(
        target=notify_user, args=[
            short_name, user.email_id, password, user.employee_name, user.employee_code
        ]
    )
    notify_user_thread.start()
    return (result1 and result2 and result3 and result4)

def update_user(db, user, session_user, client_id):
    result1 = None
    result2 = None
    result3 = None
    result4 = None

    current_time_stamp = get_date_time()
    user.is_service_provider = 0 if user.is_service_provider is False else 1
    columns = [
        "user_group_id", "employee_name", "employee_code",
        "contact_no", "seating_unit_id", "user_level",
        "is_service_provider", "updated_on", "updated_by"
    ]
    values = [
        user.user_group_id, user.employee_name, user.employee_code.replace(" ", ""),
        user.contact_no, user.seating_unit_id, user.user_level,
        user.is_service_provider, current_time_stamp, session_user
    ]
    condition = "user_id='%d'" % user.user_id

    if user.is_service_provider == 1:
        columns.append("service_provider_id")
        values.append(user.service_provider_id)
    else:
        columns.append("seating_unit_id")
        values.append(user.seating_unit_id)

    result1 = db.update(tblUsers, columns, values, condition, client_id)
    db.delete(tblUserCountries, condition, client_id)
    db.delete(tblUserDomains, condition, client_id)
    db.delete(tblUserUnits, condition, client_id)

    country_columns = ["user_id", "country_id"]
    country_values_list = []
    for country_id in user.country_ids:
        country_value_tuple = (user.user_id, int(country_id))
        country_values_list.append(country_value_tuple)
    result2 = db.bulk_insert(tblUserCountries, country_columns, country_values_list, client_id)

    domain_columns = ["user_id", "domain_id"]
    domain_values_list = []
    for domain_id in user.domain_ids:
        domain_value_tuple = (user.user_id, int(domain_id))
        domain_values_list.append(domain_value_tuple)
    result3 = db.bulk_insert(tblUserDomains, domain_columns, domain_values_list, client_id)

    db_con = Database(
        KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
        KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
    )
    db_con.connect()
    db_con.begin()
    condition = "where client_id ='{}' and user_id = '{}'".format(client_id, user.user_id)
    q = "UPDATE tbl_client_users set \
    employee_name = '{}', employee_code = '{}', \
    contact_no = '{}' ".format(
         user.employee_name, user.employee_code, user.contact_no,
         user.seating_unit_id
    )
    if user.seating_unit_id is not None:
        q += ", seating_unit_id = '{}' {}".format(user.seating_unit_id, condition)
    else:
        q += condition
    db_con.execute(q)
    db_con.commit()
    db_con.close()

    unit_columns = ["user_id", "unit_id"]
    unit_values_list = []
    for unit_id in user.unit_ids:
        unit_value_tuple = (user.user_id, int(unit_id))
        unit_values_list.append(unit_value_tuple)
    result4 = db.bulk_insert(tblUserUnits, unit_columns, unit_values_list, client_id)

    action = "Updated user \"%s - %s\"" % (user.employee_code, user.employee_name)
    db.save_activity(session_user, 4, action, client_id)

    return (result1 and result2 and result3 and result4)

def update_user_status(db, user_id, is_active, session_user, client_id):
    columns = [
        "is_active", "updated_on", "updated_by"
    ]
    is_active = 1 if is_active is not False else 0
    values = [
        is_active, get_date_time(), session_user
    ]
    condition = "user_id = '%d'" % user_id
    db_con = Database(
        KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
        KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
    )
    db_con.connect()
    db_con.begin()
    q = "UPDATE tbl_client_users set is_active = '{}' where \
    user_id = '{}'".format(
        is_active, user_id
    )
    db_con.execute(q)
    db_con.commit()
    db_con.close()

    action_column = "employee_code, employee_name"
    rows = db.get_data(
        tblUsers, action_column, condition
    )
    employee_code = rows[0][0]
    employee_name = rows[0][1]
    if is_active == 1:
        action = "Activated user \"%s - %s\"" % (employee_code, employee_name)
    else:
        action = "Dectivated user \"%s - %s\"" % (employee_code, employee_name)
    db.save_activity(session_user, 4, action, client_id)

    return db.update(tblUsers, columns, values, condition, client_id)

def update_admin_status(db, user_id, is_admin, session_user, client_id):
    columns = ["is_admin", "updated_on" , "updated_by"]
    is_admin = 1 if is_admin is not False else 0
    values = [is_admin, get_date_time(), session_user]
    condition = "user_id='%d'" % user_id
    result = db.update(tblUsers, columns, values, condition, client_id)

    action_column = "employee_code, employee_name"
    rows = db.get_data(
        tblUsers, action_column, condition
    )
    employee_code = rows[0][0]
    employee_name = rows[0][1]

    db_con = Database(
        KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
        KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
    )
    db_con.connect()
    db_con.begin()
    q = "UPDATE tbl_client_users set is_admin = '{}' where \
    user_id = '{}'".format(
        is_admin, user_id
    )
    db_con.execute(q)
    db_con.commit()
    db_con.close()

    action = None
    if is_admin == 0:
        action = "User \"%s - %s\" was demoted from admin status" % (employee_code, employee_name)
    else:
        action = "User \"%s - %s\" was promoted to admin status" % (employee_code, employee_name)
    db.save_activity(session_user, 4, action, client_id)

    return result

def get_units_closure_for_user(db, unit_ids):
    columns = "unit_id, unit_code, unit_name, address, division_id, domain_ids, country_id,"
    columns += " legal_entity_id, business_group_id, is_active, is_closed"
    condition = "1"
    if unit_ids is not None:
        condition = "unit_id in (%s)  ORDER BY unit_id ASC" % unit_ids
    rows = db.get_data(
        tblUnits, columns, condition
    )
    columns = [
        "unit_id", "unit_code", "unit_name", "unit_address", "division_id", "domain_ids", "country_id",
        "legal_entity_id", "business_group_id", "is_active", "is_closed"
    ]

    result = convert_to_dict(rows, columns)
    return return_units(result)

def return_units(units):
    results = []
    for unit in units :
        division_id = None
        b_group_id = None
        if unit["division_id"] > 0 :
            division_id = unit["division_id"]
        if unit["business_group_id"] > 0 :
            b_group_id = unit["business_group_id"]
        results.append(core.ClientUnit(
            unit["unit_id"], division_id, unit["legal_entity_id"],
            b_group_id, unit["unit_code"],
            unit["unit_name"], unit["unit_address"], bool(unit["is_active"]),
            [int(x) for x in unit["domain_ids"].split(",")], unit["country_id"],
            bool(unit["is_closed"])
        ))
    return results

def close_unit(db, unit_id, session_user):
    condition = "unit_id ='{}'".format(unit_id)
    columns = ["is_closed", "is_active"]
    values = [1, 0]
    result = db.update(
        tblUnits, columns, values, condition
    )

    columns = ["is_active"]
    values = [0]
    result = db.update(
        tblAssignedCompliances, columns, values, condition
    )

    db_con = Database(
        KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
        KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
    )
    db_con.connect()
    db_con.begin()
    q = "UPDATE tbl_units set is_active = 0 where unit_id = '%d'" % unit_id
    db_con.execute(q)
    db_con.commit()
    db_con.close()

    # columns = "client_statutory_id"
    # rows = db.get_data(tblClientStatutories, columns, condition)
    # if rows:
    #     client_statutory_id = rows[0][0]

    #     condition = "client_statutory_id='{}' and unit_id='{}'".format(
    #         client_statutory_id, unit_id
    #     )
    #     db.delete(tblClientStatutories, condition)

    #     condition = "client_statutory_id='{}' ".format(
    #         client_statutory_id
    #     )
    #     db.delete(tblClientCompliances, condition)

    action_column = "unit_code, unit_name"
    action_condition = "unit_id='{}'".format(unit_id)
    rows = db.get_data(
        tblUnits, action_column, action_condition
    )
    action = "Closed Unit \"%s - %s\"" % (rows[0][0], rows[0][1])
    db.save_activity(session_user, 5, action)

def get_audit_trails(
    db, session_user, client_id, from_count, to_count,
    from_date, to_date, user_id, form_id
):
    form_ids = None
    form_column = "group_concat(form_id)"
    form_condition = "form_type_id != 4"
    rows = db.get_data(
        tblForms, form_column, form_condition
    )
    form_ids = rows[0][0]
    forms = return_forms(db, client_id, form_ids)

    if not is_primary_admin(db, session_user) and not is_admin(db, session_user):
        unit_ids = get_user_unit_ids(db, session_user)
        query = "SELECT DISTINCT user_id FROM %s where unit_id in (%s)" % (
            tblUserUnits, unit_ids
        )
        rows = db.select_all(query)
        user_ids = ""
        for index, row in enumerate(rows):
            if index == 0:
                user_ids += str(row[0])
            else:
                user_ids += "%s%s" % (
                    ",", str(row[0])
                )
        users = get_users_by_id(db, user_ids, client_id)
    else:
        users = get_users(db, client_id)

    from_date = string_to_datetime(from_date).date()
    to_date = string_to_datetime(to_date).date()
    where_qry = "1"
    if from_date is not None and to_date is not None:
        where_qry += " AND  date(created_on) between '%s' AND '%s' " % (
            from_date, to_date

        )

    if user_id is not None:
        where_qry += " AND user_id = '%s'" % (user_id)
    if form_id is not None:
        where_qry += " AND form_id = '%s'" % (form_id)

    columns = "user_id, form_id, action, created_on"
    where_qry += ''' AND action not like "%sLog In by%s"
    ORDER BY activity_log_id DESC limit %s, %s ''' % (
        "%", "%", from_count, to_count
    )
    rows = db.get_data(
        tblActivityLog, columns, where_qry
    )
    audit_trail_details = []
    for row in rows:
        user_id = row[0]
        form_id = row[1]
        action = row[2]
        date = datetime_to_string_time(row[3])
        audit_trail_details.append(
            general.AuditTrail(user_id, form_id, action, date)
        )
    return general.GetAuditTrailSuccess(audit_trail_details, users, forms)

def return_forms(db, client_id, form_ids=None):
    columns = "form_id, form_name"
    condition = "form_id != 24"
    if form_ids is not None:
        condition += " AND form_id in (%s)" % form_ids
    forms = db.get_data(
        tblForms, columns, condition
    )
    results = []
    for form in forms:
        results.append(general.AuditTrailForm(form[0], form[1]))
    return results

def get_short_name_from_client_id(db, client_id):
    columns = "url_short_name"
    rows = db.get_data(
        tblClientGroups, columns, "1"
    )
    return rows[0][0]

def notify_user(
    short_name, email_id, password, employee_name, employee_code
):
    try:
        email.send_user_credentials(
            short_name, email_id, password, employee_name, employee_code
        )
    except Exception, e:
        logger.logClient("error", "clientdatabase.py-notify-user", e)
        print "Error while sending email : {}".format(e)
