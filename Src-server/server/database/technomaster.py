from protocol import (
    core
)
from server.constants import (CLIENT_LOGO_PATH)
from server.common import (
    datetime_to_string, convert_to_dict, get_date_time,
    string_to_datetime, remove_uploaded_file,
    convert_base64_to_file, new_uuid
)
from server.database.tables import *
from server.database.admin import (
    get_countries_for_user, get_domains_for_user
)


def generate_new_client_id(db):
    return db.get_new_id("client_id", tblClientGroups)

def is_duplicate_group_name(db, group_name, client_id):
    condition = "group_name = %s AND client_id != %s"
    condition_val = [group_name, client_id]
    return db.is_already_exists(tblClientGroups, condition, condition_val)

def is_duplicate_short_name(db, short_name, client_id):
    condition = "url_short_name = %s AND client_id != %s"
    condition_val = [short_name, client_id]
    return db.is_already_exists(tblClientGroups, condition, condition_val)

def get_client_countries(db, client_id):
    columns = "group_concat(country_id) as country_id"
    condition = "client_id = %s"
    rows = db.get_data(tblClientCountries, columns, condition, [client_id])
    return rows[0]["country_id"]

def is_logo_in_image_format(logo):
    # name = logo.file_name.split('.')[0]
    exten = logo.file_name.split('.')[1]
    if exten in ["png", "jpg", "jpeg"]:
        return True
    else:
        return False

def get_user_client_countries(db, session_user):
    client_ids = get_client_ids(db)
    if client_ids is not None:
        client_ids_list = client_ids.split(",")
        country_ids = []
        for client_id in client_ids_list:
            countries = get_client_countries(db, int(client_id))
            if countries is not None:
                country_ids += countries.split(",")
        columns = "DISTINCT country_id, country_name, is_active"
        condition = "country_id in (%s) and is_active = 1 ORDER BY country_name"
        result = db.get_data(
            tblCountries, columns, condition, [",".join(str(x) for x in country_ids)]
        )
        if result:
            return return_countries(result)
    else :
        return get_countries_for_user(db, session_user)

def return_countries(data) :
    results = []
    for d in data :
        results.append(core.Country(
            d["country_id"], d["country_name"], bool(d["is_active"])
        ))
    return results

def get_client_domains(db, client_id):
    columns = "group_concat(domain_id) as domain_id"
    condition = "client_id ='%d'"
    rows = db.get_data(tblClientDomains, columns, condition, [client_id])
    return rows[0][0]

def get_user_client_domains(db, session_user):
    client_ids = get_client_ids(db)
    if client_ids is not None:
        client_ids_list = client_ids.split(",")
        domain_ids = []
        for client_id in client_ids_list:
            domain_ids += get_client_domains(db, int(client_id)).split(",")
        columns = ["domain_id", "domain_name", "is_active"]
        condition = "domain_id in (%s) and is_active = 1 ORDER BY domain_name "
        result = db.get_data(
            tblDomains, columns, condition, [",".join(str(x) for x in domain_ids)]
        )
        return return_domains(result)
    else :
        return get_domains_for_user(db, session_user)

def return_domains(data):
    results = []
    for d in data :
        results.append(core.Domain(
            d["domain_id"], d["domain_name"], bool(d["is_active"])
        ))
    return results

def get_techno_users(db):
    columns = [
        "user_id", "concat(employee_code,'-',employee_name)",
        "is_active",
        "(select group_concat(country_id) from  %s uc where u.user_id = uc.user_id)" % tblUserCountries,
        "(select group_concat(domain_id) from  %s ud where u.user_id = ud.user_id)" % tblUserDomains
    ]
    condition = "user_group_id in (select user_group_id from \
         %s where form_category_id = 3 )" % (
            tblUserGroups
        )
    rows = db.get_data(tblUsers + " u", columns, condition)
    columns = ["user_id", "employee_name", "is_active", "countries", "domains"]
    users = convert_to_dict(rows, columns)
    return return_techno_users(users)

def return_techno_users(users):
    results = []
    for user in users :
        results.append(
            core.ClientInchargePersons(
                user["user_id"], user["employee_name"],
                bool(user["is_active"]), [int(x) for x in user["countries"].split(',')],
                [int(x) for x in user["domains"].split(",")]
            )
        )
    return results

def get_group_company_details(db):
    columns = [
        "client_id", "group_name", "email_id", "logo_url",
        "contract_from", "contract_to"
        "no_of_user_licence", "total_disk_space",
        "is_sms_subscribed",  "incharge_persons"
        "is_active", "url_short_name"
    ]
    condition = "1 ORDER BY group_name"
    rows = db.get_data(tblClientGroups, columns, condition)
    return return_group_company_details(rows)

def return_group_company_details(result):
    client_list = []
    for client_row in result:
        client_id = client_row["client_id"]
        group_name = client_row["group_name"]
        email_id = client_row["email_id"]
        file_parts = client_row["logo_url"].split("-")
        etn_parts = client_row["logo_url"].split(".")
        original_file_name = "%s.%s" % (file_parts[0], etn_parts[1])
        logo_url = "/%s/%s" % (LOGO_URL, client_row[3])
        contract_from = datetime_to_string(client_row["contract_from"])
        contract_to = datetime_to_string(client_row["contract_to"])
        no_of_user_licence = client_row["no_of_user_licence"]
        total_disk_space = client_row["total_disk_space"] / 1000000000
        is_sms_subscribed = True if client_row["is_sms_subscribed"] == 1 else False
        incharge_persons = [int(x) for x in client_row["incharge_persons"].split(",")]
        is_active = True if client_row["is_active"] == 1 else False
        short_name = client_row["url_short_name"]

        client_countries = get_client_countries(db, client_id)
        country_ids = None if client_countries is None else [int(x) for x in client_countries.split(",")]
        client_domains = get_client_domains(db, client_id)
        domain_ids = None if client_domains is None else [int(x) for x in client_domains.split(",")]
        date_configurations = get_date_configurations(db, client_id)
        client_list.append(
            core.GroupCompanyDetail(
                client_id, group_name, domain_ids,
                country_ids, incharge_persons, original_file_name, logo_url, contract_from,
                contract_to, no_of_user_licence, total_disk_space, is_sms_subscribed, email_id,
                is_active, short_name, date_configurations
            )
        )
    return client_list


def get_date_configurations(client_id):
    columns = "country_id, domain_id, period_from, period_to"
    condition = "client_id=%s" % client_id
    result = db.get_data(tblClientConfigurations, columns, condition)
    return return_client_configuration(result)

def return_client_configuration(configurations):
    results = []
    for configuration in configurations :
        results.append(core.ClientConfiguration(
            configuration["country_id"], configuration["domain_id"],
            configuration["period_from"], configuration["period_to"]
        ))
    return results

def get_server_details(db):
    columns = ["ip", "server_username", "server_password", "port"]
    condition = "server_full = 0 "
    _order = "ORDER BY length ASC limit 1"
    rows = db.get_data(tblDatabaseServer, columns, condition, condition_val=None, order=_order)
    return rows

def save_client_countries(db, client_id, country_ids):
    values_list = []
    columns = ["client_id", "country_id"]
    condition = "client_id = '%d'" % client_id
    db.delete(tblClientCountries, condition)
    for country_id in country_ids:
        values_tuple = (client_id, country_id)
        values_list.append(values_tuple)
    return db.bulk_insert(tblClientCountries, columns, values_list)

def save_client_domains(db, client_id, domain_ids):
    old_d = get_client_domains(db, client_id)
    print "old_d"
    print old_d
    if old_d is not None :
        old_d = old_d.split(',')
        print old_d
    else :
        old_d = []
    new_id = []

    values_list = []
    columns = ["client_id", "domain_id"]
    condition = "client_id = '%d'" % client_id
    db.delete(tblClientDomains, condition)
    for domain_id in domain_ids:
        print "domain id not in old"
        print domain_id, old_d
        if str(domain_id) not in old_d :
            new_id.append(str(domain_id))
        values_tuple = (client_id, domain_id)
        values_list.append(values_tuple)
    if len(new_id) > 0 :
        update_client_domain_status(db, client_id, new_id)
    return db.bulk_insert(tblClientDomains, columns, values_list)

def update_client_domain_status(db, client_id, domain_ids) :
    q = "update tbl_client_replication_status set is_new_data =1, \
        is_new_domain = 1, domain_id = %s where client_id = %s"
    # print q
    db.execute(q, [
        str((','.join(domain_ids))),
        client_id
    ])

def save_incharge_persons(db, client_group, client_id):
    columns = ["client_id", "user_id"]
    values_list = []
    condition = "client_id='%d'" % client_id
    db.delete(tblUserClients, condition)
    for incharge_person in client_group.incharge_persons:
        values_tuple = (client_id, incharge_person)
        values_list.append(values_tuple)
    return db.bulk_insert(tblUserClients, columns, values_list)

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
    return db.insert(tblClientUsers, columns, values)

def notify_incharge_persons(db, client_group):
    notification_text = "Client %s has been assigned" % client_group.group_name
    link = "/knowledge/client-unit"

    notification_id = db.insert(
        tblNotifications, ["notification_text", "link"],
        [notification_text, link]
    )

    columns = ["notification_id", "user_id", "read_status"]
    values_list = []
    for incharge_person in client_group.incharge_persons:
        values_tuple = (notification_id, incharge_person, 0)
        values_list.append(values_tuple)
    return db.bulk_insert(
        tblNotificationsStatus, columns, values_list
    )

def is_unit_exists_under_domain(db, domain, client_id):
    columns = "count(*) as units"
    condition = " FIND_IN_SET(%s, domain_ids) and client_id = %s "
    condition_val = [domain, client_id]
    rows = db.get_data(tblUnits, columns, condition, condition_val)
    if rows[0]["units"] > 0:
        return True
    else:
        return False

def is_unit_exists_under_country(db, country, client_id):
    columns = "count(*) as units"
    condition = "country_id = %s and client_id = %s "
    condition_val = [country, client_id]
    rows = db.get_data(tblUnits, columns, condition, condition_val)
    if rows[0]["units"] > 0:
        return True
    else:
        return False

def is_deactivated_existing_country(db, client_id, country_ids):
    existing_countries = get_client_countries(db, client_id)
    existing_countries_list = None
    if existing_countries is not None:
        existing_countries_list = [int(x) for x in existing_countries.split(",")]
    current_countries = [int(x) for x in country_ids]
    for country in existing_countries_list:
        if country not in current_countries:
            if is_unit_exists_under_country(db, country, client_id):
                return True
            else:
                continue
        else:
            continue
    return False

def validate_no_of_user_licence(db, no_of_user_licence, client_id):
    column = "count(*) as license"
    condition = "client_id = %s " % client_id
    rows = db.get_data(tblClientUsers, column, condition)
    current_no_of_users = int(rows[0]["license"])
    if no_of_user_licence < current_no_of_users:
        return True
    else:
        return False

def validate_total_disk_space(db, file_space, client_id):
    settings_columns = "total_disk_space_used"
    condition = "client_id = %s " % client_id
    rows = db.get_data(tblClientGroups, settings_columns, condition)
    used_space = int(rows[0]["total_disk_space_used"])
    if file_space < used_space:
        return True
    else:
        return False

def save_client_logo(logo, client_id):
    # file_size = logo.file_size
    name = logo.file_name.split('.')[0]
    exten = logo.file_name.split('.')[1]
    auto_code = new_uuid()
    file_name = "%s-%s.%s" % (name, auto_code, exten)
    convert_base64_to_file(file_name, logo.file_content, CLIENT_LOGO_PATH)
    return file_name

def update_client_logo(db, logo, client_id):
    column = "logo_url"
    condition = "client_id = %s " % client_id
    rows = db.get_data(tblClientGroups, column, condition)
    old_file_name = rows[0]["logo_url"]
    old_file_path = "%s/%s" % (CLIENT_LOGO_PATH, old_file_name)
    remove_uploaded_file(old_file_path)
    return save_client_logo(logo, client_id)


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
        client_group.no_of_user_licence, client_group.file_space * 1000000000,
        is_sms_subscribed,
        ','.join(str(x) for x in client_group.incharge_persons), session_user,
        current_time_stamp
    ]
    if client_group.logo is not None:
        columns.append("logo_url")
        columns.append("logo_size")
        file_name = update_client_logo(client_group.logo, client_group.client_id)
        values.append(file_name)
        values.append(client_group.logo.file_size)

    condition = "client_id = '%s'"
    values.append(client_group.client_id)

    action = "Updated Client \"%s\"" % client_group.group_name
    db.save_activity(session_user, 18, action)

    return db.update(tblClientGroups, columns, values, condition)

def get_client_db_info(client_id=None):
    columns = "database_ip, client_id, "
    columns += " database_username, database_password, database_name"
    condition = "1"
    if client_id is not None:
        condition = "client_id = '%d'" % client_id
    return db.get_data("tbl_client_database", columns, condition)

def replicate_client_countries_and_domains(db, client_id, country_ids, domain_ids):
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

    columns = "CAST(country_id as UNSIGNED), country_name, is_active"
    condition = "country_id in (%s)" % ','.join(str(x) for x in country_ids)
    country_rows = db.get_data(tblCountries, columns, condition)

    country_values_list = []
    for country in country_rows:
        country_values_tuple = (int(country[0]), country[1], country[2])
        country_values_list.append(country_values_tuple)

    columns = "CAST(domain_id as UNSIGNED), domain_name, is_active"
    condition = "domain_id in (%s)" % ','.join(str(x) for x in domain_ids)
    domain_rows = db.get_data(tblDomains, columns, condition)

    domain_values_list = []
    for domain in domain_rows:
        domain_values_tuple = (int(domain[0]), domain[1], domain[2])
        domain_values_list.append(domain_values_tuple)

    insert_countries_query = '''INSERT INTO tbl_countries \
    VALUES %s''' % ','.join(str(x) for x in country_values_list)

    insert_domains_query = '''INSERT INTO tbl_domains \
    VALUES %s''' % ','.join(str(x) for x in domain_values_list)

    cursor.execute(insert_countries_query)
    cursor.execute(insert_domains_query)
    conn.commit()
    return True

def is_combination_already_exists(
    db, country_id, domain_id, client_id
):
    columns = "count(*) as exists"
    condition = " client_id = %s AND country_id = %s \
            AND domain_id = %s"
    condition_val = [client_id, country_id, domain_id]
    rows = db.get_data(tblClientConfigurations, columns, condition, condition_val)
    if rows[0]["exists"] > 0:
        return True
    else:
        return False

def save_date_configurations(db, client_id, date_configurations, session_user):
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
            update_condition = " client_id = %s AND country_id = %s \
            AND domain_id = %s" % (
                client_id, country_id, domain_id
            )
            db.update(
                tblClientConfigurations, update_columns, update_values, update_condition
            )
        else:
            insert_values = [
                client_id, country_id,
                domain_id, period_from, period_to, session_user, current_time_stamp
            ]
            db.insert(
                tblClientConfigurations, insert_columns, insert_values
            )

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
    values = [is_active, int(session_user), get_date_time()]
    condition = "client_id = %s"
    condition_val = [client_id]
    action = ""
    action_columns = "group_name"
    rows = db.get_data(tblClientGroups, action_columns, condition, condition_val)
    group_name = rows[0][0]
    if is_active == 1:
        action = "Activated Client \"%s\"" % group_name
    else:
        action = "Deactivated Client \"%s\"" % group_name
    db.save_activity(session_user, 18, action)

    return db.update(tblClientGroups, columns, values, condition)

def is_duplicate_business_group(db, business_group_id, business_group_name, client_id):
    condition = "business_group_name = %s AND business_group_id != %s and client_id = %s "
    condition_val = [business_group_name, business_group_id, client_id]
    return self.is_already_exists(self.tblBusinessGroups, condition, condition_val)

def save_business_group(db, client_id, b_name, user_id):
    current_time_stamp = get_date_time()
    columns = [
        "client_id", "business_group_id", "business_group_name",
        "created_by", "created_on", "updated_by", "updated_on"
    ]
    values = [
        client_id, business_group_id, business_group_name,
        session_user, current_time_stamp,
        session_user, current_time_stamp
    ]
    new_id = db.insert(tblBusinessGroups, columns, values)

    if new_id is False :
        return False
    else :
        action = "Created Business Group \"%s\"" % business_group_name
        db.save_activity(session_user, 19, action)
        return new_id

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
    if result :
        action = "Updated Business Group \"%s\"" % business_group_name
        db.save_activity(session_user, 19, action)
    return result

def is_duplicate_legal_entity(db, legal_entity_id, legal_entity_name, client_id):
    condition = "legal_entity_name = %s AND legal_entity_id != %s and client_id = %s"
    condition_val = [legal_entity_name, legal_entity_id, client_id]
    return db.is_already_exists(tblLegalEntities, condition, condition_val)

def save_legal_entity(
    db, client_id, legal_entity_name,
    business_group_id, session_user
):
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
    if new_id is False :
        return False
    else :
        action = "Created Legal Entity \"%s\"" % legal_entity_name
        db.save_activity(session_user, 19, action)
        return new_id

def update_legal_entity(
    db, client_id, legal_entity_id, legal_entity_name,
    session_user
):
    columns = ["legal_entity_name", "updated_by", "updated_on"]
    values = [legal_entity_name, session_user, get_date_time()]
    condition = "legal_entity_id = %s and client_id = %s"
    values.extend([legal_entity_id, client_id])
    result = db.update(tblLegalEntities, columns, values, condition)
    if result :
        action = "Updated Legal Entity \"%s\"" % legal_entity_name
        db.save_activity(session_user, 19, action)
    return result

def is_duplicate_division(db, division_id, division_name, client_id):
    condition = "division_name = %s AND division_id != %s and client_id = %s "
    condition_val = [division_name, division_id, client_id]
    return db.is_already_exists(self.tblDivisions, condition, condition_val)

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

    new_id = self.insert(self.tblDivisions, columns, values)
    if new_id is False :
        return False
    else :
        action = "Created Division \"%s\"" % division_name
        self.save_activity(session_user, 19, action)

        return new_id

def update_division(db, client_id, division_id, division_name, session_user):
    current_time_stamp = get_date_time()
    columns = ["division_name", "updated_by", "updated_on"]
    values = [division_name, session_user, current_time_stamp]
    condition = "division_id = %s and client_id = %s"
    values.extend([division_id, client_id])
    result = db.update(tblDivisions, columns, values, condition)
    if result :
        action = "Updated Division \"%s\"" % division_name
        self.save_activity(session_user, 19, action)

    return result

def is_duplicate_unit_code(db, unit_id, unit_code, client_id):
    condition = "unit_code = %s AND unit_id != %s and client_id = %s"
    condition_val = [unit_code, unit_id, client_id]
    return db.is_already_exists(tblUnits, condition, condition_val)

def is_duplicate_unit_name(db, unit_id, unit_name, client_id):
    condition = "unit_name = %s AND unit_id != %s and client_id = %s"
    condition_val = [unit_name, unit_id, client_id]
    return db.is_already_exists(tblUnits, condition, condition_val)

def save_unit(db, client_id,  units, business_group_id, legal_entity_id, division_id, session_user):
    current_time_stamp = str(get_date_time())
    columns = [
        "client_id", "legal_entity_id", "country_id", "geography_id", "industry_id",
        "domain_ids", "unit_code", "unit_name", "address", "postal_code",
        "is_active", "created_by",
        "created_on", "updated_by", "updated_on"
    ]
    if business_group_id is not None:
        columns.append("business_group_id")
    if division_id is not None:
        columns.append("division_id")
    values_list = []
    unit_names = []
    for unit in units :
        domain_ids = ",".join(str(x) for x in unit.domain_ids)
        # Note values in list format if bulk insert denai list than values must be in tuple test and confirm
        vals = [
            client_id, legal_entity_id, unit.country_id,
            unit.geography_id, unit.industry_id, domain_ids,
            unit.unit_code.upper(), unit.unit_name, unit.unit_address,
            unit.postal_code, 1, session_user, current_time_stamp, session_user,
            current_time_stamp
        ]
        if business_group_id is not None :
            vals.append(business_group_id)
        if division_id is not None :
            vals.append(division_id)
        values_list.append(vals)
        unit_names.append("\"%s - %s\"" % (str(unit.unit_code).upper(), unit.unit_name))

    result = db.bulk_insert(tblUnits, columns, values_list)

    action = "Created following Units %s" % (",".join(unit_names))
    db.save_activity(session_user, 19, action)

    return result

def update_unit(db, client_id,  units, session_user):
    current_time_stamp = str(self.get_date_time())
    columns = [
        "country_id", "geography_id", "industry_id", "domain_ids", "unit_code", "unit_name",
        "address", "postal_code", "updated_by", "updated_on"
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
        if res :
            action = "Unit details updated for \"%s - %s\"" % (unit.unit_code, unit.unit_name)
            db.save_activity(session_user, 19, action)
        else :
            return False

    return True

#
# get_clients
#
def get_user_clients(db, user_id):
    result = None
    columns = "group_concat(client_id) as clients"
    if user_id > 0:
        table = tblUserClients
        condition = " user_id = %s "
    else:
        table = tblClientGroups
        condition = "is_active = 1"
    rows = db.get_data(table, columns, condition, [user_id])
    if rows is not None and len(rows) > 0:
        if rows[0]["clients"] is not None:
            columns = "group_concat(client_id) as clients"
            condition = "client_id in (%s) and is_active = 1" % (rows[0]["clients"])
            rows1 = db.get_data(self.tblClientGroups, columns, condition)
            if rows1:
                result = rows1[0]["clients"]
    return result

def get_business_groups_for_user(db, user_id):
    result = {}
    client_ids = None
    if user_id is not None:
        client_ids = get_user_clients(db, user_id)
    columns = [
        "business_group_id", "business_group_name", "client_id"
    ]
    condition = "1"
    if client_ids is not None:
        condition = "client_id in (%s) order by business_group_name ASC"
        result = db.get_data(tblBusinessGroups, columns, condition, [client_ids])
    return return_business_groups(result)

def return_business_groups(business_groups):
    results = []
    for business_group in business_groups :
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
    condition = "1"
    if client_ids is not None:
        condition = "client_id in (%s) order by legal_entity_name ASC"
        result = db.get_data(tblLegalEntities, columns, condition, [client_ids])

    return return_legal_entities(result)

def return_legal_entities(legal_entities):
    results = []
    for legal_entity in legal_entities :
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
    condition = "1"
    if client_ids is not None:
        condition = "client_id in (%s) order by division_name ASC"
        result = db.get_data(tblDivisions, columns, condition, [client_ids])
    return self.return_divisions(result)

def return_divisions(divisions):
    results = []
    for division in divisions :
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
        "unit_address", "division_id",
        "legal_entity_id", "business_group_id",
        "client_id", "is_active", "geography_id",
        "industry_id", "domain_ids"
    ]
    condition = "1"
    if client_ids is not None:
        condition = "client_id in (%s) order by unit_name ASC"
        result = db.get_data(tblUnits, columns, condition, [client_ids])
    return return_units(result)

def return_units(units):
    results = []
    for unit in units :
        results.append(core.Unit(
            unit["unit_id"], unit["division_id"], unit["legal_entity_id"],
            unit["business_group_id"], unit["client_id"], unit["unit_code"],
            unit["unit_name"], unit["unit_address"], bool(unit["is_active"])
        ))
    return results

def get_unit_details_for_user(db, user_id):
    columns = [
        "t1.unit_id", "t1.client_id", "t1.business_group_id",
        "t1.legal_entity_id", "t1.division_id", "t1.country_id",
        "t1.geography_id", "t1.industry_id", "t1.unit_code",
        "t1.unit_name", "t1.address", "t1.postal_code",
        "t1.domain_ids", "t1.is_active",
        "(select concat(business_group_id, '--', business_group_name)from tbl_business_groups where business_group_id = t1.business_group_id) as b_group",
        "(select concat(legal_entity_id, '--', legal_entity_name)from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as l_entity",
        "(select concat(division_id, '--', division_name) from tbl_divisions where division_id = t1.division_id) as l_entity",
        "(select group_name from tbl_client_groups where client_id = t1.client_id) as group_name "
    ]
    tables = [tblUnits, tblUserClients, tblUserCountries]
    aliases = ["t1", "t2", "t3"]
    join_type = "INNER JOIN"
    join_condition = [
        "t1.client_id = t2.client_id",
        "t1.country_id = t3.country_id and t2.user_id = t3.user_id",
    ]
    where_condition = "t2.user_id = %s " % (user_id)
    where_condition += " order by group_name, business_group_name, legal_entity_name, division_name"

    result = db.get_data_from_multiple_tables(
        columns, tables, aliases, join_type,
        join_condition, where_condition
    )

def return_unit_details(result):
    pass
