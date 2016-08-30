from protocol import (
    core, technomasters
)
from server.exceptionmessage import process_error
from server.constants import (CLIENT_LOGO_PATH, LOGO_URL)
from server.common import (
    datetime_to_string, get_date_time,
    string_to_datetime, remove_uploaded_file,
    convert_base64_to_file, new_uuid, convert_to_dict
)
from server.database.tables import *
from server.database.admin import (
    get_countries_for_user, get_domains_for_user
)
from server.database.validateclientuserrecord import ClientAdmin


def is_duplicate_group_name(db, group_name, client_id=None):
    condition = "group_name = %s "
    condition_val = [group_name]
    if client_id:
        condition += " AND client_id != %s"
        condition_val.append(client_id)
    return db.is_already_exists(tblClientGroups, condition, condition_val)


def is_duplicate_short_name(db, short_name, client_id=None):
    condition = "url_short_name = %s "
    condition_val = [short_name]
    if client_id:
        condition += "  AND client_id != %s"
        condition_val.append(client_id)
    return db.is_already_exists(tblClientGroups, condition, condition_val)


def get_client_countries(db, client_id):
    columns = "country_id"
    condition = "client_id = %s"
    condition_val = [client_id]
    rows = db.get_data(tblClientCountries, columns, condition, condition_val)
    country_ids = [
        r["country_id"] for r in rows
    ]
    return country_ids


def is_logo_in_image_format(logo):
    exten = logo.file_name.split('.')[1]
    if exten in ["png", "jpg", "jpeg"]:
        return True
    else:
        return False


def is_unit_exists_under_domain(db, domain, client_id):
    columns = "count(*) as units"
    condition = " FIND_IN_SET(%s, domain_ids) and client_id = %s "
    condition_val = [domain, client_id]
    rows = db.get_data(tblUnits, columns, condition, condition_val)
    if rows[0]["units"] > 0:
        return True
    else:
        return False


def is_deactivated_existing_country(db, client_id, country_ids):
    existing_country_ids = get_client_countries(db, client_id)
    current_countries = [int(x) for x in country_ids]
    for country in existing_country_ids:
        if country not in current_countries:
            if is_unit_exists_under_country(db, country, client_id):
                return True
            else:
                continue
        else:
            continue
    return False


def is_deactivated_existing_domain(db, client_id, domain_ids):
    existing_domain_ids = get_client_domains(db, client_id)
    current_domains = [int(x) for x in domain_ids]
    for domain in existing_domain_ids:
        if domain not in current_domains:
            if is_unit_exists_under_domain(db, domain, client_id):
                return True
            else:
                continue
        else:
            continue
    return False


def get_client_ids(db):
    columns = "client_id"
    condition = "1"
    rows = db.get_data(
        tblUserClients, columns, condition
    )
    client_ids = []
    if rows:
        client_ids.append(str(rows[0]["client_id"]))
    return client_ids


def get_user_client_countries(db, session_user):
    client_ids_list = get_client_ids(db)
    if len(client_ids_list) > 0:
        country_ids = []
        for client_id in client_ids_list:
            country_ids.extend(get_client_countries(db, int(client_id)))
        columns = "DISTINCT country_id as country_id, country_name, is_active"
        condition = "country_id in (%s) and is_active = 1 "
        condition_val = [",".join(str(x) for x in country_ids)]
        order = " ORDER BY country_name "
        result = db.get_data(
            tblCountries, columns, condition, condition_val, order
        )
        if result:
            return return_countries(result)
    else:
        return get_countries_for_user(db, session_user)


def return_countries(data):
    fn = core.Country
    results = [
        fn(
           d["country_id"], d["country_name"], bool(d["is_active"])
        ) for d in data
    ]
    return results


def get_client_domains(db, client_id):
    columns = "domain_id"
    condition = "client_id = %s "
    condition_val = [client_id]
    rows = db.get_data(tblClientDomains, columns, condition, condition_val)
    domain_ids = [
        int(r["domain_id"]) for r in rows
    ]
    return domain_ids


def get_user_client_domains(db, session_user):
    client_ids_list = get_client_ids(db)
    if len(client_ids_list) > 0:
        domain_ids = []
        for client_id in client_ids_list:
            domain_ids.extend(get_client_domains(db, int(client_id)))
        columns = ["domain_id", "domain_name", "is_active"]
        condition = "domain_id in (%s) and is_active = 1 "
        condition += " ORDER BY domain_name "
        condition_val = [",".join(str(x) for x in domain_ids)]
        result = db.get_data(
            tblDomains, columns, condition, condition_val
        )
        return return_domains(result)
    else:
        return get_domains_for_user(db, session_user)


def return_domains(data):
    fn = core.Domain
    results = [
        fn(
            d["domain_id"], d["domain_name"], bool(d["is_active"])
        ) for d in data
    ]
    return results


def get_techno_users(db):
    # Getting techno user countries
    query = " SELECT t1.country_id, t1.user_id " + \
        " FROM tbl_user_countries t1 " + \
        " INNER JOIN tbl_users t2 ON t2.user_id = t1.user_id  " + \
        " INNER JOIN tbl_user_groups t3 ON " + \
        " t2.user_group_id = t3.user_group_id " + \
        " AND t3.form_category_id = 3"
    rows = db.select_all(query)

    countries = []
    if rows:
        country_columns = [
            "country_id", "user_id"
        ]
        countries = convert_to_dict(rows, country_columns)

    # Getting techno user domains
    query = "SELECT t1.domain_id, t1.user_id FROM tbl_user_domains t1 " + \
            " INNER JOIN tbl_users t2 ON t2.user_id = t1.user_id " + \
            " INNER JOIN tbl_user_groups t3 ON " + \
            " t2.user_group_id = t3.user_group_id AND t3.form_category_id = 3"
    rows = db.select_all(query)

    domains = []
    if rows:
        domain_columns = [
            "domain_id", "user_id"
        ]
        domains = convert_to_dict(rows, domain_columns)

    user_country_map = {}
    for country in countries:
        user_id = int(country["user_id"])
        if user_id not in user_country_map:
            user_country_map[user_id] = []
        user_country_map[user_id].append(
            country["country_id"]
        )

    user_domain_map = {}
    for domain in domains:
        user_id = int(domain["user_id"])
        if user_id not in user_domain_map:
            user_domain_map[user_id] = []
        user_domain_map[user_id].append(
            domain["domain_id"]
        )

    # Getting Techno users
    columns = [
        "user_id", "concat(employee_code,'-',employee_name) as e_name",
        "is_active"
    ]
    condition = "user_group_id in (select user_group_id " + \
        " from tbl_user_groups " + \
        " where form_category_id = 3 )"
    rows = db.get_data(tblUsers, columns, condition)
    return return_techno_users(rows, user_country_map, user_domain_map)


def return_techno_users(users, user_country_map, user_domain_map):
    fn = core.ClientInchargePersons
    results = [
        fn(
            int(user["user_id"]), user["e_name"],
            bool(user["is_active"]),
            user_country_map[int(user["user_id"])],
            user_domain_map[int(user["user_id"])]
        ) for user in users
    ]
    return results


def get_group_company_details(db):
    columns = [
        "client_id", "group_name", "email_id", "logo_url",
        "contract_from", "contract_to",
        "no_of_user_licence", "total_disk_space",
        "is_sms_subscribed",  "incharge_persons",
        "is_active", "url_short_name"
    ]
    condition = "1 ORDER BY group_name"
    rows = db.get_data(tblClientGroups, columns, condition)
    return return_group_company_details(db, rows)


def return_group_company_details(db, result):
    client_list = []
    for client_row in result:
        client_id = client_row["client_id"]
        group_name = client_row["group_name"]
        email_id = client_row["email_id"]
        file_parts = client_row["logo_url"].split("-")
        etn_parts = client_row["logo_url"].split(".")
        original_file_name = "%s.%s" % (file_parts[0], etn_parts[1])
        logo_url = "/%s/%s" % (LOGO_URL, client_row["logo_url"])
        contract_from = datetime_to_string(client_row["contract_from"])
        contract_to = datetime_to_string(client_row["contract_to"])
        no_of_user_licence = client_row["no_of_user_licence"]
        total_disk_space = round(
            client_row["total_disk_space"] / (1024 * 1024 * 1024))
        is_sms_subscribed = True if client_row[
            "is_sms_subscribed"
        ] == 1 else False
        incharge_persons = [
            int(x) for x in client_row["incharge_persons"].split(",")
        ]
        is_active = True if client_row["is_active"] == 1 else False
        short_name = client_row["url_short_name"]

        country_ids = get_client_countries(db, client_id)
        domain_ids = get_client_domains(db, client_id)
        date_configurations = get_date_configurations(db, client_id)
        client_list.append(
            core.GroupCompanyDetail(
                client_id, group_name, domain_ids,
                country_ids, incharge_persons, original_file_name,
                logo_url, contract_from,
                contract_to, no_of_user_licence, total_disk_space,
                is_sms_subscribed, email_id,
                is_active, short_name, date_configurations
            )
        )
    return client_list


def save_client_group_data(db, client_group, session_user):
    current_time_stamp = get_date_time()
    contract_from = string_to_datetime(client_group.contract_from)
    contract_to = string_to_datetime(client_group.contract_to)
    is_sms_subscribed = 0 if client_group.is_sms_subscribed is False else 1

    file_name = save_client_logo(client_group.logo)

    columns = [
        "group_name", "email_id", "logo_size", "contract_from",
        "contract_to", "no_of_user_licence",
        "total_disk_space", "is_sms_subscribed", "url_short_name",
        "incharge_persons", "is_active", "created_by", "created_on",
        "updated_by", "updated_on", "logo_url"
    ]
    values = [
        client_group.group_name, client_group.email_id,
        client_group.logo.file_size, contract_from, contract_to,
        client_group.no_of_user_licence, (
            client_group.file_space * (1024 * 1024 * 1024)),
        is_sms_subscribed, client_group.short_name,
        ','.join(str(x) for x in client_group.incharge_persons),
        1, session_user,
        current_time_stamp, session_user, current_time_stamp, file_name

    ]

    if file_name is not None:
        client_id = db.insert(tblClientGroups, columns, values)
        if client_id is False:
            raise process_error("E040")
    else:
        raise process_error("E062")

    # columns = ["logo_url"]
    # values = [file_name]>>>
    # condition = "client_id = %s" % client_id
    # db.update(tblClientGroups, columns, values, condition)
    action = "Created Client \"%s\" " % client_group.group_name
    db.save_activity(session_user, 18, action)
    print "save client_group", client_id
    return client_id


def get_date_configurations(db, client_id):
    columns = "country_id, domain_id, period_from, period_to"
    condition = "client_id=%s"
    condition_val = [client_id]
    result = db.get_data(
        tblClientConfigurations, columns, condition,
        condition_val
    )
    return return_client_configuration(result)


def return_client_configuration(configurations):
    fn = core.ClientConfiguration
    results = [
        fn(
            configuration["country_id"], configuration["domain_id"],
            configuration["period_from"], configuration["period_to"]
        ) for configuration in configurations
    ]
    return results


def get_server_details(db):
    columns = ["ip", "server_username", "server_password", "port"]
    condition = "server_full = 0 "
    _order = "ORDER BY length ASC limit 1"
    rows = db.get_data(
        tblDatabaseServer, columns, condition,
        condition_val=None, order=_order
    )
    return rows


def save_client_countries(db, client_id, country_ids):
    values_list = []
    columns = ["client_id", "country_id"]
    condition = "client_id = %s "
    db.delete(tblClientCountries, condition, [client_id])
    for country_id in country_ids:
        values_tuple = (client_id, country_id)
        values_list.append(values_tuple)
    res = db.bulk_insert(tblClientCountries, columns, values_list)
    if res is False:
        raise process_error("E041")
    print "save_client_countries ", res
    return res


def save_client_domains(db, client_id, domain_ids):
    old_d = get_client_domains(db, client_id)
    new_id = []
    values_list = []
    columns = ["client_id", "domain_id"]
    condition = "client_id = %s "
    db.delete(tblClientDomains, condition, [client_id])
    for domain_id in domain_ids:
        if int(domain_id) not in old_d:
            new_id.append(str(domain_id))
        values_tuple = (client_id, domain_id)
        values_list.append(values_tuple)
    if len(new_id) > 0:
        update_client_domain_status(db, client_id, new_id)
    res = db.bulk_insert(tblClientDomains, columns, values_list)
    if res is False:
        raise process_error("E042")
    print "save client domains ", res
    return res


def update_client_domain_status(db, client_id, domain_ids):
    q = "update tbl_client_replication_status set is_new_data =1, " + \
        " is_new_domain = 1, domain_id = %s where client_id = %s"
    db.execute(q, [
        str((','.join(domain_ids))),
        client_id
    ])


def save_incharge_persons(db, client_group, client_id):
    columns = ["client_id", "user_id"]
    values_list = []
    condition = "client_id= %s "
    db.delete(tblUserClients, condition, [client_id])
    for incharge_person in client_group.incharge_persons:
        values_tuple = (client_id, incharge_person)
        values_list.append(values_tuple)
    r = db.bulk_insert(tblUserClients, columns, values_list)
    if r is False:
        raise process_error("E043")
    print "save incharge_person ", r
    return r


def save_client_user(db, client_group, session_user, client_id=None):
    if client_id is None:
        client_id = client_group.client_id
    columns = [
        "client_id", "user_id",  "email_id",
        "employee_name", "created_on", "is_primary_admin", "is_active"
    ]
    values = [
        client_id, 0, client_group.email_id, "Admin",
        get_date_time(), 1, 1
    ]
    r = db.insert(tblClientUsers, columns, values)
    if r is False:
        raise process_error("E044")
    print "save client user ", r
    return r


def notify_incharge_persons(db, client_group):
    notification_text = "Client %s has been assigned" % client_group.group_name
    link = "/knowledge/client-unit"

    notification_id = db.insert(
        tblNotifications, ["notification_text", "link"],
        [notification_text, link]
    )
    if notification_id is False:
        raise process_error("E045")

    columns = ["notification_id", "user_id", "read_status"]
    values_list = []
    for incharge_person in client_group.incharge_persons:
        values_tuple = (notification_id, incharge_person, 0)
        values_list.append(values_tuple)
    r = db.bulk_insert(
        tblNotificationsStatus, columns, values_list
    )
    if r is False:
        raise process_error("E045")
    return r


def is_unit_exists_under_country(db, country, client_id):
    columns = "count(*) as units"
    condition = "country_id = %s and client_id = %s "
    condition_val = [country, client_id]
    rows = db.get_data(tblUnits, columns, condition, condition_val)
    if rows[0]["units"] > 0:
        return True
    else:
        return False


def validate_no_of_user_licence(db, no_of_user_licence, client_id):
    column = "count(*) as license"
    condition = "client_id = %s "
    condition_val = [client_id]
    rows = db.get_data(
        tblClientUsers, column, condition, condition_val
    )
    current_no_of_users = int(rows[0]["license"])
    if no_of_user_licence < current_no_of_users:
        return True
    else:
        return False


def validate_total_disk_space(db, file_space, client_id):
    settings_columns = "total_disk_space_used"
    condition = "client_id = %s "
    condition_val = [client_id]
    rows = db.get_data(
        tblClientGroups, settings_columns,
        condition, condition_val
    )
    used_space = int(rows[0]["total_disk_space_used"])
    if file_space < used_space:
        return True
    else:
        return False


def save_client_logo(logo):
    # file_size = logo.file_size
    name = logo.file_name.split('.')[0]
    exten = logo.file_name.split('.')[1]
    auto_code = new_uuid()
    file_name = "%s-%s.%s" % (name, auto_code, exten)
    try :
        convert_base64_to_file(file_name, logo.file_content, CLIENT_LOGO_PATH)
        return file_name
    except Exception, e :
        print e
        return None


def update_client_logo(db, logo, client_id):
    column = "logo_url"
    condition = "client_id = %s "
    condition_val = [client_id]
    rows = db.get_data(
        tblClientGroups, column, condition, condition_val
    )
    old_file_name = rows[0]["logo_url"]
    old_file_path = "%s/%s" % (CLIENT_LOGO_PATH, old_file_name)
    remove_uploaded_file(old_file_path)
    return save_client_logo(logo)


def update_client_group_record(db, client_group, session_user):
    current_time_stamp = get_date_time()
    contract_from = string_to_datetime(client_group.contract_from)
    contract_to = string_to_datetime(client_group.contract_to)
    is_sms_subscribed = 0 if client_group.is_sms_subscribed is False else 1
    columns = [
        "group_name", "contract_from", "contract_to", "no_of_user_licence",
        "total_disk_space", "is_sms_subscribed", "incharge_persons",
        "updated_by", "updated_on"
    ]
    values = [
        client_group.group_name, contract_from, contract_to,
        client_group.no_of_user_licence, client_group.file_space * (1024 * 1024 * 1024),
        is_sms_subscribed,
        ','.join(str(x) for x in client_group.incharge_persons), session_user,
        current_time_stamp
    ]
    if client_group.logo is not None:
        columns.append("logo_url")
        columns.append("logo_size")
        file_name = update_client_logo(
            client_group.logo, client_group.client_id
        )
        values.append(file_name)
        values.append(client_group.logo.file_size)

    condition = "client_id = %s"
    values.append(client_group.client_id)
    if db.update(tblClientGroups, columns, values, condition):
        action = "Updated Client \"%s\"" % client_group.group_name
        db.save_activity(session_user, 18, action)
        return True
    else:
        raise process_error("E046")


def get_client_db_info(db, client_id=None):
    columns = "database_ip, client_id, "
    columns += " database_username, database_password, database_name"
    condition = condition_val = None
    if client_id is not None:
        condition = "client_id = %s "
        condition_val = [client_id]
    return db.get_data(
        "tbl_client_database", columns, condition, condition_val
    )


def replicate_client_countries_and_domains(
    db, client_id, country_ids, domain_ids
):
    rows = get_client_db_info(db, client_id)
    ip = rows[0]["database_ip"]
    username = rows[0]["database_username"]
    password = rows[0]["database_password"]
    dbname = rows[0]["database_name"]

    conn = db._db_connect(ip, username, password, dbname)
    cursor = conn.cursor()

    delete_countries_query = "delete from tbl_countries"
    delete_domains_query = "delete from tbl_domains"

    cursor.execute(delete_countries_query)
    cursor.execute(delete_domains_query)
    columns = "country_id, country_name, is_active"
    condition, condition_val = db.generate_tuple_condition(
        "country_id", country_ids)
    country_rows = db.get_data(
        tblCountries, columns, condition, [condition_val])
    country_values_list = [
        (
            int(country["country_id"]),
            country["country_name"],
            country["is_active"]
        ) for country in country_rows
    ]

    columns = "domain_id, domain_name, is_active"
    condition, condition_val = db.generate_tuple_condition(
        "domain_id", domain_ids)
    domain_rows = db.get_data(tblDomains, columns, condition, [condition_val])
    domain_values_list = [
        (
            int(domain["domain_id"]),
            domain["domain_name"],
            domain["is_active"]
        ) for domain in domain_rows
    ]

    insert_countries_query = "INSERT INTO tbl_countries " + \
        " VALUES %s" % ','.join(str(x) for x in country_values_list)

    insert_domains_query = "INSERT INTO tbl_domains " + \
        " VALUES %s" % ','.join(str(x) for x in domain_values_list)

    cursor.execute(insert_countries_query)
    cursor.execute(insert_domains_query)
    conn.commit()
    return True


def is_combination_already_exists(
    db, country_id, domain_id, client_id
):
    columns = "count(*) as v_exists"
    condition = " client_id = %s AND country_id = %s " + \
                " AND domain_id = %s"
    condition_val = [client_id, country_id, domain_id]
    rows = db.get_data(
        tblClientConfigurations, columns, condition, condition_val
    )
    if rows:
        if rows[0]["v_exists"] > 0:
            return True
        else:
            return False
    else:
        return False


def save_date_configurations(
    db, client_id, date_configurations, session_user
):
    current_time_stamp = get_date_time()
    insert_columns = [
        "client_id", "country_id", "domain_id", "period_from",
        "period_to", "updated_by", "updated_on"
    ]
    update_columns = ["period_from", "period_to"]
    for configuration in date_configurations:
        country_id = configuration.country_id
        domain_id = configuration.domain_id
        period_from = configuration.period_from
        period_to = configuration.period_to
        if is_combination_already_exists(db, country_id, domain_id, client_id):
            update_values = [period_from, period_to]
            update_condition = " client_id = %s AND country_id = %s " + \
                " AND domain_id = %s"
            update_values.extend([client_id, country_id, domain_id])
            r = db.update(
                tblClientConfigurations, update_columns,
                update_values, update_condition
            )
            if r is False:
                raise process_error("E048")

        else:
            insert_values = [
                client_id, country_id,
                domain_id, period_from, period_to,
                session_user, current_time_stamp
            ]
            r = db.insert(
                tblClientConfigurations, insert_columns, insert_values
            )
            if r is False:
                raise process_error("E047")


def is_unit_exists_under_client(db, client_id):
    column = "count(*) as units"
    condition = "client_id = %s and is_active = 1"
    condition_val = [client_id]
    rows = db.get_data(tblUnits, column, condition, condition_val)
    if rows[0]["units"] > 0:
        return True
    else:
        return False


def update_client_group_status(db, client_id, is_active, session_user):
    is_active = 1 if is_active is not False else 0
    columns = ["is_active", "updated_by", "updated_on"]
    values = [is_active, int(session_user), get_date_time(), client_id]
    condition = "client_id = %s"
    action_columns = ["group_name"]
    rows = db.get_data(
        tblClientGroups, action_columns, condition, [client_id]
    )
    group_name = rows[0]["group_name"]
    if is_active == 1:
        action = "Activated Client \"%s\"" % group_name
    else:
        action = "Deactivated Client \"%s\"" % group_name
    db.save_activity(session_user, 18, action)
    r = db.update(tblClientGroups, columns, values, condition)
    if r is False:
        raise process_error("E049")


def is_duplicate_business_group(
    db, business_group_id, business_group_name, client_id
):
    condition = "business_group_name = %s " + \
        " AND client_id = %s "
    condition_val = [business_group_name, client_id]
    if business_group_id is not None:
        condition += " AND business_group_id != %s "
        condition_val.append(business_group_id)
    return db.is_already_exists(tblBusinessGroups, condition, condition_val)


def save_business_group(db, client_id, b_name, user_id):
    user_id = int(user_id)
    current_time_stamp = get_date_time()
    columns = [
        "client_id", "business_group_name",
        "created_by", "created_on"
    ]
    values = [
        client_id, b_name,
        user_id, current_time_stamp
    ]
    new_id = db.insert(tblBusinessGroups, columns, values)

    if new_id is False:
        raise process_error("E050")
    else:
        action = "Created Business Group \"%s\"" % b_name
        db.save_activity(user_id, 19, action)
        return int(new_id)


def update_business_group(
    db, client_id, business_group_id, business_group_name, session_user
):
    current_time_stamp = get_date_time()
    columns = [
        "business_group_name", "updated_by", "updated_on"
    ]
    values = [
        business_group_name, session_user, current_time_stamp
    ]
    condition = "business_group_id = %s and client_id = %s "
    values.append(business_group_id)
    values.append(client_id)
    result = db.update(tblBusinessGroups, columns, values, condition)
    if result:
        action = "Updated Business Group \"%s\"" % business_group_name
        db.save_activity(session_user, 19, action)
        return result
    else:
        raise process_error("E051")


def is_duplicate_legal_entity(
    db, legal_entity_id, legal_entity_name, client_id
):
    condition = "legal_entity_name = %s " + \
        "  and client_id = %s"
    condition_val = [legal_entity_name, client_id]
    if legal_entity_id:
        condition += " AND legal_entity_id != %s "
        condition_val.append(legal_entity_id)
    return db.is_already_exists(tblLegalEntities, condition, condition_val)


def save_legal_entity(
    db, client_id, legal_entity_name,
    business_group_id, session_user
):
    session_user = int(session_user)
    current_time_stamp = get_date_time()
    columns = [
        "client_id", "legal_entity_name",
        "created_by", "created_on", "updated_by", "updated_on"
    ]
    values = [
        client_id, legal_entity_name,
        session_user, current_time_stamp, session_user, current_time_stamp
    ]

    if business_group_id is not None:
        columns.append("business_group_id")
        values.append(business_group_id)

    new_id = db.insert(tblLegalEntities, columns, values)
    if new_id is False:
        raise process_error("E052")
    else:
        action = "Created Legal Entity \"%s\"" % legal_entity_name
        db.save_activity(session_user, 19, action)
        return int(new_id)


def update_legal_entity(
    db, client_id, legal_entity_id, legal_entity_name,
    session_user
):
    columns = ["legal_entity_name", "updated_by", "updated_on"]
    values = [legal_entity_name, session_user, get_date_time()]
    condition = "legal_entity_id = %s and client_id = %s"
    values.extend([legal_entity_id, client_id])
    result = db.update(tblLegalEntities, columns, values, condition)
    if result:
        action = "Updated Legal Entity \"%s\"" % legal_entity_name
        db.save_activity(session_user, 19, action)
        return result
    else:
        raise process_error("E053")


def is_duplicate_division(db, division_id, division_name, client_id):
    condition = "division_name = %s  AND client_id = %s "
    condition_val = [division_name, client_id]
    if division_id is not None:
        condition += " AND division_id != %s "
        condition_val.append(division_id)
    return db.is_already_exists(tblDivisions, condition, condition_val)


def save_division(
    db, client_id, division_name, business_group_id,
    legal_entity_id, session_user
):
    current_time_stamp = get_date_time()
    columns = [
        "client_id", "division_name",
        "legal_entity_id", "created_by", "created_on",
        "updated_by", "updated_on"
    ]
    values = [
        client_id, division_name, legal_entity_id,
        session_user, current_time_stamp, session_user,
        current_time_stamp
    ]

    if business_group_id is not None:
        columns.append("business_group_id")
        values.append(business_group_id)

    new_id = db.insert(tblDivisions, columns, values)
    if new_id is False:
        raise process_error("E054")
    else:
        action = "Created Division \"%s\"" % division_name
        db.save_activity(session_user, 19, action)

        return int(new_id)


def update_division(db, client_id, division_id, division_name, session_user):
    current_time_stamp = get_date_time()
    columns = ["division_name", "updated_by", "updated_on"]
    values = [division_name, session_user, current_time_stamp]
    condition = "division_id = %s and client_id = %s"
    values.extend([division_id, client_id])
    result = db.update(tblDivisions, columns, values, condition)
    if result:
        action = "Updated Division \"%s\"" % division_name
        db.save_activity(session_user, 19, action)
        return result
    else:
        raise process_error("E055")


def is_duplicate_unit_code(db, unit_id, unit_code, client_id):
    condition = "unit_code = %s AND unit_id != %s and client_id = %s"
    condition_val = [unit_code, unit_id, client_id]
    return db.is_already_exists(tblUnits, condition, condition_val)


def is_duplicate_unit_name(db, unit_id, unit_name, client_id):
    condition = "unit_name = %s AND unit_id != %s and client_id = %s"
    condition_val = [unit_name, unit_id, client_id]
    return db.is_already_exists(tblUnits, condition, condition_val)


def save_unit(
    db, client_id,  units, business_group_id, legal_entity_id,
    division_id, session_user
):
    current_time_stamp = str(get_date_time())
    columns = [
        "client_id", "legal_entity_id", "country_id", "geography_id",
        "industry_id", "domain_ids", "unit_code", "unit_name",
        "address", "postal_code", "is_active", "created_by", "created_on"
    ]
    if business_group_id is not None:
        columns.append("business_group_id")
    if division_id is not None:
        columns.append("division_id")
    values_list = []
    unit_names = []
    for unit in units:
        domain_ids = ",".join(str(x) for x in unit.domain_ids)
        vals = [
            client_id, legal_entity_id, unit.country_id,
            unit.geography_id, unit.industry_id, domain_ids,
            unit.unit_code.upper(), unit.unit_name, unit.unit_address,
            unit.postal_code, 1, session_user, current_time_stamp
        ]
        if business_group_id is not None:
            vals.append(business_group_id)
        if division_id is not None:
            vals.append(division_id)
        values_list.append(vals)
        unit_names.append("\"%s - %s\"" % (
            str(unit.unit_code).upper(), unit.unit_name)
        )

    result = db.bulk_insert(tblUnits, columns, values_list)
    if result is False:
        raise process_error("E056")

    action = "Created following Units %s" % (",".join(unit_names))
    db.save_activity(session_user, 19, action)

    return result


def update_unit(db, client_id,  units, session_user):
    current_time_stamp = str(get_date_time())
    columns = [
        "country_id", "geography_id", "industry_id", "domain_ids",
        "unit_code", "unit_name", "address", "postal_code",
        "updated_by", "updated_on"
    ]
    for unit in units:
        domain_ids = ",".join(str(x) for x in unit.domain_ids)
        values = [
            unit.country_id, unit.geography_id, unit.industry_id, domain_ids,
            str(unit.unit_code), str(unit.unit_name), str(unit.unit_address),
            str(unit.postal_code), session_user, current_time_stamp
        ]
        condition = "client_id= %s and unit_id = %s"
        values.extend([client_id, unit.unit_id])
        res = db.update(tblUnits, columns, values, condition)
        if res:
            action = "Unit details updated for \"%s - %s\"" % (
                unit.unit_code, unit.unit_name
            )
            db.save_activity(session_user, 19, action)
        else:
            raise process_error("E057")

    return True


#
# get_clients
#
def get_user_clients(db, user_id):
    q = "select t1.client_id " + \
        " from tbl_client_groups t1 inner join " + \
        " tbl_user_clients t2 " + \
        " on t1.client_id = t2.client_id " + \
        " and t1.is_active = 1 and t2.user_id = %s "
    rows = db.select_all(q, [int(user_id)])
    client_ids = [
        int(r[0]) for r in rows
    ]
    return client_ids


def get_business_groups_for_user(db, user_id):
    result = {}
    client_ids = None
    if user_id is not None:
        client_ids = get_user_clients(db, user_id)
    columns = [
        "business_group_id", "business_group_name", "client_id"
    ]
    condition = "1"
    condition, condition_val = db.generate_tuple_condition(
        "client_id", client_ids
    )
    order = " order by business_group_name ASC"
    result = db.get_data(
        tblBusinessGroups, columns, condition, [condition_val], order
    )
    return return_business_groups(result)


def return_business_groups(business_groups):
    results = []
    for business_group in business_groups:
        results.append(core.BusinessGroup(
            business_group["business_group_id"],
            business_group["business_group_name"],
            business_group["client_id"]
        ))
    return results


def get_legal_entities_for_user(db, user_id):
    client_ids = None
    result = {}
    if user_id is not None:
        client_ids = get_user_clients(db, user_id)
    columns = [
        "legal_entity_id", "legal_entity_name", "business_group_id",
        "client_id"
    ]
    condition, condition_val = db.generate_tuple_condition(
        "client_id", client_ids
    )
    order = " order by legal_entity_name ASC"
    result = db.get_data(
        tblLegalEntities, columns, condition, [condition_val], order
    )
    return return_legal_entities(result)


def return_legal_entities(legal_entities):
    results = []
    for legal_entity in legal_entities:
        results.append(core.LegalEntity(
            legal_entity["legal_entity_id"], legal_entity["legal_entity_name"],
            legal_entity["business_group_id"], legal_entity["client_id"]
        ))
    return results


def get_divisions_for_user(db, user_id):
    client_ids = None
    result = {}
    if user_id is not None:
        client_ids = get_user_clients(db, user_id)
    columns = [
        "division_id", "division_name", "legal_entity_id",
        "business_group_id", "client_id"
    ]
    condition, condition_val = db.generate_tuple_condition(
        "client_id", client_ids
    )
    order = " order by division_name ASC "
    result = db.get_data(
        tblDivisions, columns, condition, [condition_val], order
    )
    return return_divisions(result)


def return_divisions(divisions):
    results = []
    for division in divisions:
        division_obj = core.Division(
            division["division_id"], division["division_name"],
            division["legal_entity_id"], division["business_group_id"],
            division["client_id"]
        )
        results.append(division_obj)
    return results


def get_units_for_user(db, user_id):
    client_ids = None
    result = {}
    if user_id is not None:
        client_ids = get_user_clients(db, user_id)
    columns = [
        "unit_id", "unit_code", "unit_name",
        "address", "division_id",
        "legal_entity_id", "business_group_id",
        "client_id", "is_active", "geography_id",
        "industry_id", "domain_ids"
    ]
    condition, condition_val = db.generate_tuple_condition(
        "client_id", client_ids
    )
    order = " order by unit_name ASC "
    result = db.get_data(tblUnits, columns, condition, [condition_val], order)
    return return_units(result)


def return_units(units):
    results = []
    for unit in units:
        results.append(core.Unit(
            unit["unit_id"], unit["division_id"], unit["legal_entity_id"],
            unit["business_group_id"], unit["client_id"], unit["unit_code"],
            unit["unit_name"], unit["address"], bool(unit["is_active"])
        ))
    return results


def get_unit_details_for_user(db, user_id):
    business_group_column = "(select business_group_name " + \
        " from tbl_business_groups " + \
        " where business_group_id = t1.business_group_id) as b_group"
    legal_entity_column = "(select legal_entity_name " + \
        " from tbl_legal_entities " + \
        " where legal_entity_id = t1.legal_entity_id) as l_entity"
    division_column = "(select division_name " + \
        " from tbl_divisions " + \
        " where division_id = t1.division_id) as division"
    group_column = "(select group_name " + \
        " from tbl_client_groups " + \
        " where client_id = t1.client_id) as group_name "
    columns = [
        "t1.unit_id", "t1.client_id", "t1.business_group_id",
        "t1.legal_entity_id", "t1.division_id", "t1.country_id",
        "t1.geography_id", "t1.industry_id", "t1.unit_code",
        "t1.unit_name", "t1.address", "t1.postal_code",
        "t1.domain_ids", "t1.is_active",
        business_group_column, legal_entity_column,
        division_column, group_column
    ]
    tables = [tblUnits, tblUserClients, tblUserCountries]
    aliases = ["t1", "t2", "t3"]
    join_type = "INNER JOIN"
    join_condition = [
        "t1.client_id = t2.client_id",
        "t1.country_id = t3.country_id and t2.user_id = t3.user_id",
    ]
    where_condition = "t2.user_id = %s "
    where_condition += " order by group_name, b_group, l_entity, division"
    where_condition_val = [user_id]
    result = db.get_data_from_multiple_tables(
        columns, tables, aliases, join_type,
        join_condition, where_condition, where_condition_val
    )
    return return_unit_details(result)


def return_unit_details(result):
    unit_details = {}
    country_unit_map = {}
    unit_client_map = {}
    for r in result:
        business_group_id = int(r["business_group_id"]) if(
            r["business_group_id"] is not None) else 0
        legal_entity_id = int(r["legal_entity_id"])
        division_id = int(r["division_id"]) if(
            r["division_id"] is not None) else 0
        unit_id = int(r["unit_id"])
        country_id = int(r["country_id"])
        client_id = int(r["client_id"])

        unit = technomasters.UnitDetails(
            r["unit_id"], r["geography_id"],
            r["unit_code"], r["unit_name"],
            r["industry_id"], r["address"],
            r["postal_code"],
            [int(x) for x in r["domain_ids"].split(",")],
            bool(r["is_active"])
        )
        if country_id not in country_unit_map:
            country_unit_map[country_id] = []
        country_unit_map[country_id].append(unit_id)
        unit_client_map[unit_id] = client_id
        if business_group_id not in unit_details:
            unit_details[business_group_id] = {}
        if legal_entity_id not in unit_details[business_group_id]:
            unit_details[business_group_id][legal_entity_id] = {}
        if division_id not in unit_details[business_group_id][legal_entity_id]:
            unit_details[
                business_group_id][legal_entity_id][division_id] = {}
        if country_id not in unit_details[
                business_group_id][legal_entity_id][division_id]:
            unit_details[business_group_id][
                    legal_entity_id][division_id][country_id] = {}
        if client_id not in unit_details[
                business_group_id][legal_entity_id][division_id][country_id]:
            unit_details[business_group_id][
                legal_entity_id][division_id][country_id][client_id] = []
        unit_details[business_group_id][
            legal_entity_id][division_id][country_id][client_id].append(unit)

    final_list = []
    for business_group_id in unit_details:
        for legal_entity_id in unit_details[business_group_id]:
            for division_id in unit_details[
                    business_group_id][legal_entity_id]:
                for country_id in unit_details[
                        business_group_id][legal_entity_id][division_id]:
                    for client_id in unit_details[
                            business_group_id][
                            legal_entity_id][division_id][country_id]:
                        units = unit_details[
                            business_group_id
                        ][legal_entity_id][division_id][country_id][client_id]
                        is_active = False
                        for unit in units:
                            is_active = is_active and unit.is_active
                        final_list.append(
                            technomasters.Unit(
                                None if(
                                    business_group_id == 0
                                ) else business_group_id,
                                legal_entity_id,
                                None if(division_id == 0) else division_id,
                                client_id, {country_id: units},
                                is_active
                            )
                        )
    return final_list


# def return_unit_details(result):
#     legal_entity_wise = {}
#     for r in result:
#         unit = technomasters.UnitDetails(
#             r["unit_id"], r["geography_id"],
#             r["unit_code"], r["unit_name"],
#             r["industry_id"], r["address"],
#             r["postal_code"],
#             [int(x) for x in r["domain_ids"].split(",")],
#             bool(r["is_active"])
#         )

#         legal_wise = legal_entity_wise.get(r["legal_entity_id"])
#         if legal_wise is None:
#             legal_wise = technomasters.Unit(
#                 r["business_group_id"], r["legal_entity_id"],
#                 r["division_id"], r["client_id"],
#                 {r["country_id"]: [unit]},
#                 bool(1)
#             )
#         else:
#             country_wise_units = legal_wise.units

#             if country_wise_units is None:
#                 country_wise_units = {}

#             units = country_wise_units.get(r["country_id"])
#             if units is None:
#                 units = []
#             units.append(unit)

#             country_wise_units[r["country_id"]] = units

#             legal_wise.units = country_wise_units

#         legal_entity_wise[r["legal_entity_id"]] = legal_wise

#     data = legal_entity_wise.values()
#     return data


def get_group_companies_for_user_with_max_unit_count(db, user_id):
    result = {}
    client_ids = None
    if user_id is not None:
        client_ids = get_user_clients(db, user_id)
    columns = ["client_id", "group_name", "is_active"]
    condition, condition_val = db.generate_tuple_condition(
        "client_id", client_ids
    )
    condition += " AND is_active=1 "
    order = " order by group_name ASC "
    result = db.get_data(
        tblClientGroups, columns, condition, [condition_val], order
    )
    return return_group_companies_with_max_unit_count(db, result)


def return_group_companies_with_max_unit_count(db, group_companies):
    results = []
    for group_company in group_companies:
        countries = get_client_countries(db, group_company["client_id"])
        domains = get_client_domains(db, group_company["client_id"])
        next_auto_gen_no = get_next_auto_gen_number(
            db, group_company["group_name"], group_company["client_id"]
        )
        results.append(core.GroupCompanyForUnitCreation(
            group_company["client_id"], group_company["group_name"],
            bool(group_company["is_active"]), countries, domains,
            next_auto_gen_no
        ))
    return results


def get_next_auto_gen_number(db, group_name=None, client_id=None):
    if group_name is None:
        columns = ["group_name"]
        condition = "client_id = %s "
        condition_val = [client_id]
        rows = db.get_data(tblClientGroups, columns, condition, condition_val)
        if rows:
            group_name = rows[0]["group_name"]

    columns = ["count(*) as units"]
    condition = "client_id = %s "
    condition_val = [client_id]
    rows = db.get_data(tblUnits, columns, condition, condition_val)
    if rows:
        no_of_units = rows[0]["units"]
    group_name = group_name.replace(" ", "")
    unit_code_start_letters = group_name[:2].upper()

    columns = "TRIM(LEADING '%s' FROM unit_code) as code" % (
        unit_code_start_letters
    )
    condition = "unit_code like binary %s and " + \
        " CHAR_LENGTH(unit_code) = 7 and client_id= %s "
    # condition = condition % (
    #     str(unit_code_start_letters + '%'), client_id
    # )
    unit_code_start_letters = "%s%s" % (unit_code_start_letters, "%")
    condition_val = [unit_code_start_letters, client_id]
    rows = db.get_data(
        tblUnits, columns, condition, condition_val
    )
    auto_generated_unit_codes = []
    for row in rows:
        try:
            auto_generated_unit_codes.append(int(row["code"]))
        except Exception, ex:
            print ex
            continue
    next_auto_gen_no = 1
    if len(auto_generated_unit_codes) > 0:
        existing_max_unit_code = max(auto_generated_unit_codes)
        if existing_max_unit_code == no_of_units:
            next_auto_gen_no = no_of_units + 1
        else:
            next_auto_gen_no = existing_max_unit_code + 1
    return next_auto_gen_no


def reactivate_unit_data(db, client_id, unit_id, session_user):
    action_column = [
        "business_group_id", "legal_entity_id", "division_id",
        "country_id", "geography_id", "industry_id",
        "unit_code", "unit_name", "address",
        "postal_code", "domain_ids"
    ]
    condition = "unit_id = %s "
    condition_val = [unit_id]
    result = db.get_data(tblUnits, action_column, condition, condition_val)
    result = result[0]
    action = "Reactivated Unit \"%s-%s\"" % (
        result["unit_code"], result["unit_name"]
    )
    db.save_activity(session_user, 19, action)

    next_auto_gen_no = get_next_auto_gen_number(db, client_id=client_id)
    unit_code = group_name[:2].upper()
    if len(str(next_auto_gen_no)) == 1:
        unit_code += "0000"
    elif len(str(next_auto_gen_no)) == 2:
        unit_code += "000"
    elif len(str(next_auto_gen_no)) == 3:
        unit_code += "00"
    elif len(str(next_auto_gen_no)) == 4:
        unit_code += "0"
    unit_code += "%s" % (next_auto_gen_no)
    unit_columns = [
        "client_id", "is_active", "legal_entity_id",
        "country_id", "geography_id", "industry_id", "unit_code", "unit_name",
        "address", "postal_code", "domain_ids"
    ]
    values = [
        client_id, 1, result["legal_entity_id"],
        result["country_id"], result["geography_id"],
        result["industry_id"], unit_code, result["unit_name"],
        result["address"], result["postal_code"], result["domain_ids"]
    ]
    if result["business_group_id"] not in ["Null", "None", None, ""]:
        unit_columns.append("business_group_id")
        values.append(result["business_group_id"])
    if result["division_id"] not in ["Null", "None", None, ""]:
        unit_columns.append("division_id")
        values.append(result["division_id"])
    if db.insert(tblUnits, unit_columns, values):
        return unit_code, result["unit_name"]
    else:
        raise process_error("E058")


# def get_next_unit_auto_gen_no(db, client_id):
#     columns = "count(unit_id) as units"
#     condition = "client_id = %s"
#     condition_val = [client_id]
#     rows = db.get_data(tblUnits, columns, condition, condition_val)
#     no_of_units = rows[0]["units"]

#     group_columns = ["group_name"]
#     group_condition = "client_id = %s"
#     group_condition_val = [client_id]
#     group_company = db.get_data(
#         tblClientGroups, group_columns,
#         group_condition, group_condition_val
#     )

#     group_name = group_company[0]["group_name"].replace(" ", "")
#     unit_code_start_letters = group_name[:2].upper()

#     columns = "TRIM(LEADING '%s' FROM unit_code) as code" % (
#         unit_code_start_letters
#     )
#     condition = "unit_code like binary '%s%s' and " + \
#         " CHAR_LENGTH(unit_code) = 7 and client_id= %s"
#     condition = condition % (unit_code_start_letters, "%", client_id)
#     rows = db.get_data(tblUnits, columns, condition)
#     auto_generated_unit_codes = []
#     for row in rows:
#         try:
#             auto_generated_unit_codes.append(int(row["code"]))
#         except Exception, ex:
#             print ex
#             continue
#     next_auto_gen_no = 1
#     if len(auto_generated_unit_codes) > 0:
#         existing_max_unit_code = max(auto_generated_unit_codes)
#         if existing_max_unit_code == no_of_units:
#             next_auto_gen_no = no_of_units + 1
#         else:
#             next_auto_gen_no = existing_max_unit_code + 1
#     unit_code = group_name[:2].upper()
#     if len(str(next_auto_gen_no)) == 1:
#         unit_code += "0000"
#     elif len(str(next_auto_gen_no)) == 2:
#         unit_code += "000"
#     elif len(str(next_auto_gen_no)) == 3:
#         unit_code += "00"
#     elif len(str(next_auto_gen_no)) == 4:
#         unit_code += "0"
#     unit_code += "%s" % (next_auto_gen_no)
#     return unit_code


def get_profiles(db, client_ids_list):
    ONE_GB = 1024 * 1024 * 1024
    profiles = []
    for client_id in client_ids_list:
        settings_rows = get_settings(db, client_id)
        contract_from = datetime_to_string(settings_rows[0]["contract_from"])
        contract_to = datetime_to_string(settings_rows[0]["contract_to"])
        no_of_user_licence = settings_rows[0]["no_of_user_licence"]
        file_space = settings_rows[0]["total_disk_space"]
        used_space = settings_rows[0]["total_disk_space_used"]
        licence_holder_rows = get_licence_holder_details(db, client_id)
        licence_holders = []
        for row in licence_holder_rows:
            employee_name = None
            unit_name = None
            if row["unit_name"] == None:
                unit_name = "-"
            else:
                unit_name = "%s - %s" % (row["unit_code"], row["unit_name"])
            user_id = row["user_id"]
            email_id = row["email_id"]
            contact_no = None if row["contact_no"] is "" else row["contact_no"]
            is_primary_admin = row["is_primary_admin"]
            is_active = row["is_active"]
            is_admin = row["is_admin"]
            if(row["employee_code"] == None):
                employee_name = row["employee_name"]
            elif (is_primary_admin == 1 and is_active == 1):
                employee_name = "Administrator"
            elif (is_primary_admin == 1 and is_active == 0):
                employee_name = "Old Administrator"
            else:
                employee_name = "%s - %s" % (
                    row["employee_code"], row["employee_name"]
                )
            address = row["address"]
            is_service_provider = False
            if unit_name == "-":
                if (is_primary_admin == 1 or is_admin == 1):
                    is_service_provider = False
                else:
                    is_service_provider = True

            used_val = round((used_space/ONE_GB), 2)

            licence_holders.append(
                technomasters.LICENCE_HOLDER_DETAILS(
                    user_id, employee_name, email_id, contact_no,
                    unit_name, address,
                    file_space/ONE_GB, used_val,
                    bool(is_active), bool(is_primary_admin),
                    is_service_provider
                )
            )

        remaining_licence = (no_of_user_licence) - len(licence_holder_rows)
        total_free_space = round(file_space/ONE_GB, 2)
        total_used_space = round(used_space/ONE_GB, 2)
        profile_detail = technomasters.PROFILE_DETAIL(
            str(contract_from),
            str(contract_to), no_of_user_licence, remaining_licence,
            total_free_space, total_used_space, licence_holders
        )
        profiles.append(technomasters.PROFILES(client_id, profile_detail))
    return profiles


def get_settings(db, client_id):
    settings_columns = [
        "contract_from", "contract_to", "no_of_user_licence",
        "total_disk_space", "total_disk_space_used"
    ]
    condition = "client_id = %s"
    condition_val = [client_id]
    return db.get_data(
        tblClientGroups, settings_columns, condition, condition_val
    )


def get_licence_holder_details(db, client_id):
    columns = [
        "tcu.user_id", "tcu.email_id", "tcu.employee_name",
        "tcu.employee_code", "tcu.contact_no",
        "tcu.is_primary_admin", "tu.unit_code", "tu.unit_name",
        "tu.address", "tcu.is_active", "tcu.is_admin"
    ]
    tables = [tblClientUsers, tblUnits]
    aliases = ["tcu", "tu"]
    join_type = "left join"
    join_conditions = ["tcu.seating_unit_id = tu.unit_id"]
    where_condition = "tcu.client_id = %s"
    where_condition_val = [client_id]
    return db.get_data_from_multiple_tables(
        columns, tables, aliases, join_type, join_conditions,
        where_condition, where_condition_val
    )


def get_group_companies_for_user(db, user_id):
    result = {}
    client_ids = None
    if user_id is not None:
        client_ids = get_user_clients(db, user_id)
    columns = ["client_id", "group_name", "is_active"]
    condition, condition_val = db.generate_tuple_condition(
        "client_id", client_ids
    )
    condition += " AND is_active = 1"
    order = " order by group_name ASC "
    result = db.get_data(
        tblClientGroups, columns, condition, [condition_val], order
    )
    return return_group_companies(db, result)


def return_group_companies(db, group_companies):
    results = []
    for group_company in group_companies:
        countries = get_client_countries(db, group_company["client_id"])
        domains = get_client_domains(db, group_company["client_id"])
        results.append(
            core.GroupCompany(
                group_company["client_id"], group_company["group_name"],
                bool(group_company["is_active"]), countries, domains
            )
        )
    return results


def create_new_admin(
    db, new_admin_id, old_admin_id, old_admin_name,
    client_id, session_user
):
    t_obj = ClientAdmin(db, new_admin_id, old_admin_id, client_id)
    result = t_obj.perform_promote_admin()
    if result is True:
        # Promoting to new admin in Knowledge db
        query = "update tbl_client_users set is_primary_admin = 1 " + \
            " where user_id = %s and client_id = %s"
        db.execute(query, [new_admin_id, client_id])

        # Deactivating old admin in Knowledge db
        query = "update tbl_client_users set is_active = 0 " + \
            " where user_id = %s and client_id = %s"
        db.execute(query, [old_admin_id, client_id])

        query = "update tbl_client_groups t1, " + \
            " (select email_id from tbl_client_users where user_id = %s " + \
            " and client_id = %s) t2 " + \
            " set t1.email_id = t2.email_id  where client_id = %s"
        db.execute(query, [
            old_admin_id, client_id, client_id
        ])
        action = None
        action = "User \"%s\" is promoted as Client Admin" % (old_admin_name)
        db.save_activity(session_user, 20, action)
        return True
    return result
