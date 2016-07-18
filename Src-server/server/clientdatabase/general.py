from server.common import (
    encrypt
    )

all__ = [
    "get_countries_for_user",
    "get_domains_for_user",
    "get_business_groups_for_user",
    "get_legal_entities_for_user",
    "get_divisions_for_user",
    "get_group_name",
    "get_country_wise_domain_month_range",
    "get_units_for_user",
    "get_client_users",
    "get_user_domains",
    "get_user_countries",
    "verify_username",
    "verify_password",
    "get_countries",
    "get_domains",
    "is_primary_admin",
    "have_compliances",
    "is_seating_unit",
    "is_admin",
    "get_user_unit_ids",
    "is_two_levels_of_approval",
    "get_user_company_details",
    "get_client_level_1_statutoy",
    "get_service_providers",
    "get_client_compliances",
    "get_client_settings",
    "get_admin_info",
    "validate_compliance_due_date",
    "get_compliance_frequency",
    "get_users",
    "get_users_by_id",
    "get_users_by_unit_and_domain",
    "get_compliance_name_by_id",
    "is_space_available",
    "update_used_space",
    "save_compliance_activity",
    "save_compliance_notification",
    "get_email_id_for_users",
    "get_user_email_name",
    "calculate_due_date",
    "filter_out_due_dates",
    "convert_base64_to_file",
    "get_user_name_by_id",
    "get_form_ids_for_admin",
    "get_report_form_ids",
    "get_client_id_from_short_name",
    "validate_reset_token",
    "remove_session",
    "update_profile",
    "is_service_proivder_user"

]


 def get_admin_id(db):
    columns = "admin_id"
    condition = "1"
    rows = db.get_data(tblAdmin, columns, condition)
    return rows[0][0]

def get_countries_for_user(db, user_id, client_id=None) :
    admin_id = get_admin_id(db)
    query = "SELECT distinct t1.country_id, t1.country_name, \
        t1.is_active FROM tbl_countries t1 "
    if user_id > 0 and user_id != admin_id:
        query = query + " INNER JOIN tbl_user_countries t2 \
            ON t1.country_id = t2.country_id WHERE t2.user_id = %s" % (
                user_id
            )
    rows = db.select_all(query)
    columns = ["country_id", "country_name", "is_active"]
    result = db.convert_to_dict(rows, columns)
    return return_countries(result)

def return_countries(data) :
    results = []

    for d in data :
        results.append(core.Country(
            d["country_id"], d["country_name"], bool(d["is_active"])
        ))
    return results

def get_domains_for_user(db, user_id, client_id=None) :
    admin_id = get_admin_id(db)
    query = "SELECT distinct t1.domain_id, t1.domain_name, \
        t1.is_active FROM tbl_domains t1 "
    if user_id > 0 and user_id != admin_id:
        query = query + " INNER JOIN tbl_user_domains t2 ON \
            t1.domain_id = t2.domain_id WHERE t2.user_id = %s" % (user_id)
    rows = db.select_all(query)
    columns = ["domain_id", "domain_name", "is_active"]
    result = db.convert_to_dict(rows, columns)
    return return_domains(result)

def return_domains(data):
    results = []
    for d in data :
        results.append(core.Domain(
            d["domain_id"], d["domain_name"], bool(d["is_active"])
        ))
    return results

def get_business_groups_for_user(db, business_group_ids):
    columns = "business_group_id, business_group_name"
    condition = "1"
    if business_group_ids is not None:
        condition = "business_group_id in (%s) ORDER BY business_group_name" % business_group_ids
    rows = db.get_data(
        tblBusinessGroups, columns, condition
    )
    columns = ["business_group_id", "business_group_name"]
    result = db.convert_to_dict(rows, columns)
    return return_business_groups(result)

def return_business_groups(business_groups):
    results = []
    for business_group in business_groups :
        results.append(core.ClientBusinessGroup(
            business_group["business_group_id"],
            business_group["business_group_name"]
        ))
    return results

def get_legal_entities_for_user(db, legal_entity_ids):
    columns = "legal_entity_id, legal_entity_name, business_group_id"
    condition = "1"
    if legal_entity_ids is not None:
        condition = "legal_entity_id in (%s) ORDER BY legal_entity_name" % legal_entity_ids
    rows = db.get_data(
        tblLegalEntities, columns, condition
    )
    columns = ["legal_entity_id", "legal_entity_name", "business_group_id"]
    result = db.convert_to_dict(rows, columns)
    return return_legal_entities(result)

def return_legal_entities(legal_entities):
    results = []
    for legal_entity in legal_entities :
        b_group_id = None
        if legal_entity["business_group_id"] > 0:
            b_group_id = int(legal_entity["business_group_id"])
        results.append(core.ClientLegalEntity(
            legal_entity["legal_entity_id"],
            legal_entity["legal_entity_name"],
            b_group_id
        ))
    return results

def get_divisions_for_user(db, division_ids):
    columns = "division_id, division_name, legal_entity_id, business_group_id"
    condition = "1"
    if division_ids is not None:
        condition = "division_id in (%s) ORDER BY division_name" % division_ids
    rows = db.get_data(
        tblDivisions, columns, condition
    )
    columns = [
        "division_id", "division_name", "legal_entity_id",
        "business_group_id"
    ]
    result = db.convert_to_dict(rows, columns)
    return return_divisions(result)

def return_divisions(divisions):
    results = []
    for division in divisions :
        division_obj = core.ClientDivision(
            division["division_id"], division["division_name"],
            division["legal_entity_id"], division["business_group_id"]
        )
        results.append(division_obj)
    return results

def get_group_name(db):
    query = "SELECT group_name from %s " % tblClientGroups
    row = db.select_one(query)
    if row :
        return row[0]
    return "group_name"

def get_country_wise_domain_month_range(db):
    q = "SELECT t1.country_id, \
    (select country_name from tbl_countries where country_id = t1.country_id) country_name, \
    t1.domain_id,\
    (select domain_name from tbl_domains where domain_id = t1.domain_id)domain_name,\
    t1.period_from, t1.period_to from tbl_client_configurations t1 INNER JOIN \
    tbl_countries TC ON TC.country_id = t1.country_id  \
    INNER JOIN tbl_domains TD ON TD.domain_id = t1.domain_id"
    rows = db.select_all(q)
    columns = [
        "country_id", "country_name",
        "domain_id", "domain_name",
        "period_from", "period_to"
    ]
    result = db.convert_to_dict(rows, columns)

    country_wise = {}
    domain_info = []
    for r in result:
        country_name = r["country_name"].strip()
        domain_name = r["domain_name"]
        info = dashboard.DomainWiseYearConfiguration(
            country_name,
            domain_name,
            db.string_full_months.get(int(r["period_from"])),
            db.string_full_months.get(int(r["period_to"]))
        )
        domain_info = country_wise.get(country_name)
        if domain_info is None :
            domain_info = []

        domain_info.append(info)
        country_wise[country_name] = domain_info
    return country_wise

def get_units_for_user(db, unit_ids, client_id=None):
    columns = "unit_id, unit_code, unit_name, address, division_id, domain_ids, country_id,"
    columns += " legal_entity_id, business_group_id, is_active, is_closed"
    condition = "is_closed = 0"
    if unit_ids is not None:
        condition = "unit_id in (%s) ORDER BY unit_name" % unit_ids
    rows = db.get_data(
        tblUnits, columns, condition
    )
    columns = [
        "unit_id", "unit_code", "unit_name", "unit_address", "division_id","domain_ids", "country_id",
        "legal_entity_id", "business_group_id", "is_active", "is_closed"
    ]
    result = db.convert_to_dict(rows, columns)
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

 def get_client_users(db, client_id=None, unit_ids=None):
    columns = "user_id, employee_name, employee_code, is_active"
    condition = "1"
    if unit_ids is not None:
        condition += " and seating_unit_id in (%s)" % unit_ids
    rows = db.get_data(
        tblUsers, columns, condition
    )
    columns = ["user_id", "employee_name", "employee_code", "is_active"]
    result = db.convert_to_dict(rows, columns)
    return return_client_users(result)

def return_client_users(users):
    results = []
    for user in users :
        results.append(clientreport.User(
            user["user_id"], user["employee_code"], user["employee_name"]
        ))
    return results

def get_user_domains(db, user_id, client_id=None):
    columns = "domain_id"
    table = tblDomains
    result = None
    condition = 1
    if user_id > 0:
        table  = tblUserDomains
        condition = " user_id = '%d'" % user_id
    rows = db.get_data(
        table, columns, condition
    )
    result = ""
    if rows:
        for index, row in enumerate(rows):
            if index == 0:
                result += str(row[0])
            else:
                result += ", %s" % str(row[0])
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

def verify_username(db, username):
    columns = "count(*), user_id"
    condition = "email_id='%s' and is_active = 1" % (username)
    rows = db.get_data(
        tblUsers, columns, condition
    )
    count = rows[0][0]
    if count == 1:
        return rows[0][1]
    else:
        condition = "username='%s'" % username
        columns = "count(*)"
        rows = db.get_data(
            tblAdmin, columns, condition
        )
        count = rows[0][0]
        if count == 1:
            return 0
        else:
            return None

def verify_password(db, password, user_id, client_id=None):
    columns = "count(*)"
    encrypted_password = encrypt(password)
    condition = "1"
    rows = None
    if user_id == 0:
        condition = "password='%s'" % (encrypted_password)
        rows = db.get_data(
           tblAdmin, columns, condition
        )
    else:
        condition = "password='%s' and user_id='%d'" % (
            encrypted_password, user_id
        )
        rows = db.get_data(
            tblUsers, columns, condition
        )
    if(int(rows[0][0]) <= 0):
        return False
    else:
        return True

def get_countries(db):
    query = "SELECT distinct t1.country_id, t1.country_name, \
        t1.is_active FROM tbl_countries t1 "
    rows = db.select_all(query)
    columns = ["country_id", "country_name", "is_active"]
    result = db.convert_to_dict(rows, columns)
    return return_countries(result)

def get_domains(db):
    query = "SELECT distinct t1.domain_id, t1.domain_name, \
        t1.is_active FROM tbl_domains t1 "
    rows = db.select_all(query)
    columns = ["domain_id", "domain_name", "is_active"]
    result = db.convert_to_dict(rows, columns)
    return return_domains(result)

def is_primary_admin(db, user_id):
    column = "count(1)"
    condition = "user_id = '%d' and is_primary_admin = 1" % user_id
    rows = db.get_data(tblUsers, column, condition)
    if rows[0][0] > 0 or user_id == 0:
        return True
    else:
        return False

def have_compliances(db, user_id):
        column = "count(*)"
        condition = "assignee = '%d' and is_active = 1" % user_id
        rows = db.get_data(tblAssignedCompliances, column, condition)
        no_of_compliances = rows[0][0]
        if no_of_compliances > 0:
            return True
        else:
            return False

def is_seating_unit(db, unit_id):
    column = "count(*)"
    condition = "seating_unit_id ='%d'" % unit_id
    rows = db.get_data(tblUsers, column, condition)
    user_count = rows[0][0]
    if user_count > 0:
        return True
    else:
        return False

def is_admin(db, user_id):
    if user_id == 0:
        return True
    else:
        columns = "count(*)"
        condition = "(is_admin = 1 or is_primary_admin = 1) and user_id = '%d'" % user_id
        rows = db.get_data(tblUsers, columns, condition)
        if rows[0][0] > 0:
            return True
        else:
            return False

def get_user_unit_ids(db, user_id, client_id=None):
    columns = "unit_id"
    table = tblUnits
    result = None
    condition = 1
    if user_id > 0:
        table = tblUserUnits
        condition = " user_id = '%d'" % user_id
    rows = db.get_data(
        table, columns, condition
    )
    if rows :
        result = ""
        for index, row in enumerate(rows):
            if index == 0:
                result += str(row[0])
            else:
                result += ",%s" % str(row[0])
    return result

def is_two_levels_of_approval(db):
    columns = "two_levels_of_approval"
    rows = db.get_data(tblClientGroups, columns, "1")
    return rows[0][0]

def get_user_company_details(db, user_id, client_id=None):
    admin_id = get_admin_id(db)
    columns = "unit_id"
    condition = " 1 "
    rows = None
    if user_id > 0 and user_id != admin_id:
        condition = "  user_id = '%d'" % user_id
        rows = db.get_data(
            tblUserUnits, columns, condition
        )
    else:
        rows = db.get_data(
            tblUnits, columns, condition
        )
    unit_ids = None
    division_ids = None
    legal_entity_ids = None
    business_group_ids = None
    if len(rows) > 0:
        result = []
        for row in rows:
            result.append(row[0])
        unit_ids = ",".join(str(x) for x in result)

    if unit_ids not in [None, "None", ""]:
        columns = "group_concat(distinct division_id), group_concat(distinct legal_entity_id), \
        group_concat(distinct business_group_id)"
        unit_condition = "1"
        if unit_ids is not None :
            unit_condition = "unit_id in (%s)" % unit_ids
        rows = db.get_data(
            tblUnits , columns, unit_condition
        )
        division_ids = rows[0][0]
        legal_entity_ids = rows[0][1]
        business_group_ids = rows[0][2]

    return unit_ids, division_ids, legal_entity_ids, business_group_ids

def get_client_level_1_statutoy(db, user_id, client_id=None) :
    query = "SELECT (case when (LEFT(statutory_mapping,INSTR(statutory_mapping,'>>')-1) = '') \
            THEN \
            statutory_mapping \
            ELSE \
            LEFT (statutory_mapping,INSTR(statutory_mapping,'>>')-1) \
            END ) as statutory \
            FROM tbl_compliances GROUP BY statutory"
    rows = db.select_all(query)
    columns = ["statutory"]
    result = db.convert_to_dict(rows, columns)
    return return_client_level_1_statutories(result)

def return_client_level_1_statutories(data) :
    results = []
    for d in data :
        results.append(
            d["statutory"]
        )
    return results

def get_service_providers(db, client_id=None):
    columns = "service_provider_id, service_provider_name, is_active"
    condition = "1"
    rows = db.get_data(
        tblServiceProviders, columns, condition
    )
    columns = ["service_provider_id", "service_provider_name", "is_active"]
    result = db.convert_to_dict(rows, columns)
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

def get_client_compliances(db, user_id, client_id=None) :
    query = "SELECT compliance_id, document_name ,compliance_task \
            FROM tbl_compliances"
    rows = db.select_all(query, client_id)
    columns = ["compliance_id", "document_name", "compliance_name"]
    result = db.convert_to_dict(rows, columns)
    return return_client_compliances(result)

def return_client_compliances(data) :
    results = []
    for d in data :
        compliance_name = d["compliance_name"]
        if d["document_name"] not in ["None", None, ""]:
            compliance_name = "%s - %s" % (d["document_name"], compliance_name)
        results.append(core.ComplianceFilter(
            d["compliance_id"], compliance_name
        ))
    return results

def calculate_ageing(due_date, frequency_type=None, completion_date=None, duration_type=None):
    current_time_stamp = get_date_time()
    compliance_status = "-"
    # due_date = self.localize(due_date)
    if frequency_type == "On Occurrence":
        r = relativedelta.relativedelta(due_date, current_time_stamp)
        if completion_date is not None:
            r = relativedelta.relativedelta(due_date, completion_date)
            if r.days < 0 and r.hours < 0 and r.minutes < 0:
                compliance_status = "On Time"
            else:
                if r.days == 0:
                    if duration_type in ["2", 2]:
                        compliance_status = "Delayed by %d.%d hour(s) " % (
                            abs(r.hours), abs(r.minutes)
                        )
                    else:
                        compliance_status = "Delayed by 1 day "
                else:
                    if duration_type in ["2", 2]:
                        compliance_status = "Delayed by %d.%d hour(s)" % (
                           ( abs(r.days) * 4 + abs(r.hours)), abs(r.minutes)
                        )
                    else:
                        compliance_status = "Delayed by %d day(s)" % (
                            abs(r.days)
                        )
                return r.days, compliance_status
        else:
            if r.days >= 0 and r.hours >= 0 and r.minutes >= 0:
                if r.days == 0:
                    if duration_type in ["2", 2]:
                        compliance_status = " %d.%d hour(s) left" % (
                            abs(r.hours), abs(r.minutes)
                        )
                    else:
                        compliance_status = "1 Day left"
                else:
                    if duration_type in ["2", 2]:
                        compliance_status = "%d.%d hour(s) left" % (
                           ( abs(r.days) * 24 + abs(r.hours)), abs(r.minutes)
                        )
                    else:
                        compliance_status = " %d day(s) left" % (
                            abs(r.days)
                        )
            else:
                if r.days == 0:
                    if duration_type in ["2", 2]:
                        compliance_status = "Overdue by %d.%d hour(s) " % (
                            abs(r.hours), abs(r.minutes)
                        )
                    else:
                        compliance_status = "Overdue by 1 day "
                else:
                    if duration_type in ["2", 2]:
                        compliance_status = "Overdue by %d.%d hours" % (
                           (abs(r.days) * 24 + abs(r.hours)), abs(r.minutes)
                        )
                    else:
                        compliance_status = "Overdue by %d day(s)" %(
                            abs(r.days)
                        )
            return r.days, compliance_status
    else:
        if completion_date is not None:
            compliance_status = "On Time"
            if due_date not in [None, "None", 0]:
                if type(due_date) == datetime.datetime:
                    due_date = due_date.date()
                if type(completion_date) == datetime.datetime:
                    completion_date = completion_date.date()
                r = relativedelta.relativedelta(due_date, completion_date)
                if r.days < 0:
                    compliance_status = "Delayed by %d day(s)" % abs(r.days)
                return r.days, compliance_status
        else:
            if due_date not in [None, "None", 0]:
                r = relativedelta.relativedelta(due_date.date(), current_time_stamp.date())
                compliance_status = " %d days left" % abs(r.days+1)
                if r.days < 0:
                    compliance_status = "Overdue by %d day(s)" % abs(r.days)
                    return r.days, compliance_status
    return 0, compliance_status

def get_client_settings(db):
    query = "SELECT two_levels_of_approval \
        FROM tbl_client_groups"
    row = db.select_one(query)
    if row:
        return bool(int(row[0]))

def get_admin_info(db):
    query = "SELECT admin_id from tbl_admin"
    row = db.select_one(query)
    return int(row[0])

def validate_compliance_due_date(db, request):
    c_ids = []
    for c in request.compliances :
        c_ids.append(c.compliance_id)
        q = "SELECT compliance_id, compliance_task, statutory_dates, repeats_type_id from tbl_compliances \
            where compliance_id = %s" % int(c.compliance_id)
        row = db.select_one(q)
        if row :
            comp_id = row[0]
            task = row[1]
            s_dates = json.loads(row[2])
            repeats_type_id = row[3]
            due_date, due_date_list, date_list = self.set_new_due_date(s_dates, repeats_type_id, comp_id)

            if c.due_date not in [None, ""] and due_date not in [None, ""]:
                t_due_date = datetime.datetime.strptime(c.due_date, "%d-%b-%Y")
                n_due_date = datetime.datetime.strptime(due_date, "%d-%b-%Y")
                if (n_due_date < t_due_date) :
                    # Due date should be lessthen statutory date
                    return False, task
    return True, None

def get_compliance_frequency(db, client_id, condition="1"):
    columns = "frequency_id, frequency"
    rows = db.get_data(
        tblComplianceFrequency, columns, condition
    )
    compliance_frequency = []
    for row in rows:
        compliance_frequency.append(
            core.ComplianceFrequency(
                row[0],
                core.COMPLIANCE_FREQUENCY(row[1])
                )
            )
    return compliance_frequency

def get_user_ids_by_unit_and_domain(
        db, unit_id, domain_id
    ):
    unit_user_rows = db.get_data(
        tblUserUnits, "user_id" , "unit_id = '%d'" % unit_id
    )
    unit_users = []
    for unit_user in unit_user_rows:
        unit_users.append(unit_user[0])

    domain_user_rows = db.get_data(
        tblUserDomains, "user_id" , "domain_id = '%d'" % domain_id
    )
    domain_users = []
    for domain_user in domain_user_rows:
        domain_users.append(domain_user[0])

    users = list(set(unit_users).intersection(domain_users))
    user_ids = None
    if len(users) > 0:
        user_ids = ",".join(str(x) for x in users)
    else:
        user_ids = None
    return user_ids

def get_users_by_unit_and_domain(
        db, unit_id, domain_id
    ):
    user_ids = get_user_ids_by_unit_and_domain(
        db, unit_id, domain_id
    )
    result = []
    if user_ids is not None:
        columns = "user_id, employee_name, employee_code, is_active"
        condition = " is_active = 1 and user_id in (%s)" % user_ids
        rows = db.get_data(
            tblUsers, columns, condition
        )
        columns = ["user_id", "employee_name", "employee_code", "is_active"]
        result = db.convert_to_dict(rows, columns)
    return return_users(result)

def get_users(db, client_id):
        columns = "user_id, employee_name, employee_code, is_active"
        condition = "1"
        rows = db.get_data(
            tblUsers, columns, condition
        )
        columns = ["user_id", "employee_name", "employee_code", "is_active"]
        result = db.convert_to_dict(rows, columns)
        return return_users(result)

def get_users_by_id(db, user_ids, client_id):
    columns = "user_id, employee_name, employee_code, is_active"
    condition = " user_id in (%s)" % user_ids
    rows = db.get_data(
        tblUsers, columns, condition
    )
    columns = ["user_id", "employee_name", "employee_code", "is_active"]
    result = db.convert_to_dict(rows, columns)
    return return_users(result)

def return_users(users):
    results = []
    for user in users :
        if user["employee_code"] is not None:
            employee_name = "%s - %s" % (user["employee_code"],user["employee_name"])
        else:
            employee_name = "Administrator"
        results.append(core.User(
            user["user_id"], employee_name, bool(user["is_active"])
        ))
    return results

def get_compliance_name_by_id(db, compliance_id):
    column = "document_name, compliance_task"
    condition = "compliance_id = '%d'" % compliance_id
    rows = db.get_data(tblCompliances, column, condition)
    compliance_name = ""
    if rows[0][0] is not None:
        if str(rows[0][0])  == "None" :
            compliance_name = rows[0][1]
        else :
            compliance_name += rows[0][0]+" - "+rows[0][1]
    else:
        compliance_name = rows[0][1]
    return compliance_name

def is_space_available(db, upload_size):
    columns = "total_disk_space - total_disk_space_used"
    rows = db.get_data(tblClientGroups, columns, "1")
    remaining_space = rows[0][0]
    if upload_size < remaining_space:
        return True
    else:
        return False

def update_used_space(db, file_size):
    columns = "total_disk_space_used"
    condition = "1"
    db.increment( tblClientGroups, columns, condition, value = file_size)

    total_used_space = 0

    rows = db.get_data(tblClientGroups, "total_disk_space_used, client_id", "1")
    client_id = rows[0][1]
    if rows[0][0] is not None:
        total_used_space = int(rows[0][0])

    db_con = Database(
        KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
        KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
    )
    db_con.connect()
    db_con.begin()
    q = "UPDATE tbl_client_groups set total_disk_space_used = '%d' where client_id = '%d'" % (
        total_used_space, client_id
    )
    db_con.execute(q)
    db_con.commit()
    db_con.close()

def save_compliance_activity(
    db, unit_id, compliance_id, activity_status, compliance_status,
    remarks
):
    compliance_activity_id = db.get_new_id(
        "compliance_activity_id", tblComplianceActivityLog,
    )
    date = get_date_time()
    columns = [
        "compliance_activity_id", "unit_id", "compliance_id",
        "activity_date", "activity_status", "compliance_status",
        "updated_on"
    ]
    values = [
        compliance_activity_id, unit_id, compliance_id, date, activity_status,
        compliance_status,  date
    ]
    if remarks:
        columns.append("remarks")
        values.append(remarks)
    db.insert(
       tblComplianceActivityLog, columns, values
    )

def save_compliance_notification(
    db, compliance_history_id, notification_text, category, action
):
    notification_id = db.get_new_id(
        "notification_id", tblNotificationsLog
    )
    current_time_stamp = get_date_time()

    # Get history details from compliance history id
    history_columns = "unit_id, compliance_id, completed_by, concurred_by, \
    approved_by"
    history_condition = "compliance_history_id = '%d'" % compliance_history_id
    history_rows = db.get_data(
        tblComplianceHistory, history_columns, history_condition
    )
    history_columns_list = [
        "unit_id", "compliance_id", "completed_by",
        "concurred_by", "approved_by"
    ]
    history = db.convert_to_dict(history_rows[0], history_columns_list)
    unit_id = history["unit_id"]
    compliance_id = history["compliance_id"]

    # Getting Unit details from unit_id
    unit_columns = "country_id, business_group_id, legal_entity_id, division_id"
    unit_condition = "unit_id = '%d'" % int(unit_id)
    unit_rows = db.get_data(tblUnits, unit_columns, unit_condition)
    unit_columns_list = [
        "country_id", "business_group_id", "legal_entity_id", "division_id"
    ]
    unit = db.convert_to_dict(unit_rows[0], unit_columns_list)

    # Getting compliance_details from compliance_id
    compliance_columns = "domain_id"
    compliance_condition = "compliance_id = '%d'" % compliance_id
    compliance_rows = db.get_data(
        tblCompliances, compliance_columns, compliance_condition
    )
    domain_id = compliance_rows[0][0]

    # Saving notification
    columns = [
        "notification_id", "country_id", "domain_id", "business_group_id",
        "legal_entity_id", "division_id", "unit_id", "compliance_id",
        "assignee", "concurrence_person", "approval_person", "notification_type_id",
        "notification_text", "extra_details", "created_on"
    ]
    extra_details = "%d-%s" % (compliance_history_id, category)
    values = [
        notification_id, unit["country_id"], domain_id, unit["business_group_id"],
        unit["legal_entity_id"], unit["division_id"], unit_id, compliance_id,
        history["completed_by"], history["concurred_by"], history["approved_by"],
        1, notification_text, extra_details, current_time_stamp
    ]
    db.insert(tblNotificationsLog, columns, values)

    # Saving in user log
    columns = [
        "notification_id", "read_status", "updated_on", "user_id"
    ]
    values = [
        notification_id, 0, current_time_stamp
    ]
    if action.lower() == "concur":
        values.append(int(history["concurred_by"]))
    elif action.lower() == "approve":
        values.append(int(history["approved_by"]))
    elif action.lower() == "concurred":
        values.append(int(history["completed_by"]))
    elif action.lower() == "approvedtoassignee":
        values.append(int(history["completed_by"]))
    elif action.lower() == "approvedtoconcur":
        values.append(int(history["concurred_by"]))
    elif action.lower() == "concurrejected":
        values.append(int(history["completed_by"]))
    elif action.lower() == "approverejectedtoassignee":
        values.append(int(history["completed_by"]))
    elif action.lower() == "approverejectedtoconcur":
        values.append(int(history["concurred_by"]))
    elif action.lower() == "started":
        values.append(int(history["completed_by"]))
    return db.insert(tblNotificationUserLog, columns, values)

def get_user_countries(db, user_id, client_id=None):
    columns = "group_concat(country_id)"
    table = tblCountries
    result = None
    condition = 1
    if user_id > 0:
        table = tblUserCountries
        condition = " user_id = '%d'" % user_id
    rows = db.get_data(
        table, columns, condition
    )
    if rows :
        result = rows[0][0]
    return result

def get_email_id_for_users(db, user_id):
    if user_id == 0 :
        q = "SELECT 'Administrator', username from tbl_admin where admin_id = %s" % (
            user_id
        )
        pass
    else :
        q = "SELECT employee_name, email_id from tbl_users where user_id = %s" % (
            user_id
        )
    row = db.select_one(q)
    if row :
        return row[0], row[1]
    else :
        return None

def get_user_email_name(db, user_ids):
    user_id_list = [int(x) for x in user_ids.split(",")]
    admin_email = None
    index = None
    if 0 in user_id_list:
        index = user_id_list.index(0)
        column = "username"
        admin_rows = db.get_data(tblAdmin, column, "1")
        user_id_list.remove(0)
        admin_email = admin_rows[0][0]
    column = "email_id, employee_name"
    condition = "user_id in (%s)" % ",".join(str(x) for x in user_ids)
    rows = db.get_data(
        tblUsers, column, condition
    )
    email_ids = ""
    employee_name = ""
    for index, row in enumerate(rows):
        if index == 0:
            if row[1] is not None:
                employee_name += "%s" % row[1]
            email_ids += "%s" % row[0]
        else:
            if row[1] is not None:
                employee_name += ", %s" % row[1]
            email_ids += ", %s" % row[0]
    if admin_email is not None:
        employee_name += "Administrator"
        email_ids += admin_email

    return email_ids, employee_name

def calculate_from_and_to_date_for_domain(db, country_id, domain_id):
    columns = "contract_from, contract_to"
    rows = db.get_data(tblClientGroups, columns, "1")
    contract_from = rows[0][0]
    contract_to = rows[0][1]

    columns = "period_from, period_to"
    condition = "country_id = '%d' and domain_id = '%d'" % (
        country_id, domain_id
    )
    rows = db.get_data(tblClientConfigurations, columns, condition)
    period_from = rows[0][0]
    period_to = rows[0][1]

    to_date = contract_from
    current_year = to_date.year
    previous_year = current_year-1
    from_date = datetime.date(previous_year, period_from, 1)
    r = relativedelta.relativedelta(to_date, from_date)
    no_of_years = r.years
    no_of_months = r.months
    if no_of_years is not 0 or no_of_months >= 12:
        from_date = datetime.date(current_year, period_from, 1)
    return from_date, to_date

def calculate_due_date(
    db, country_id, domain_id, statutory_dates=None, repeat_by=None,
    repeat_every=None, due_date=None
):
    def is_future_date(test_date):
        result = False
        current_date = datetime.date.today()
        if type(test_date) == datetime.datetime:
            test_date = test_date.date()
        if ((current_date - test_date).days < 0):
            result = True
        return result
    from_date, to_date = calculate_from_and_to_date_for_domain(db, country_id, domain_id)
    due_dates = []
    summary = ""
    # For Monthly Recurring compliances
    if statutory_dates and len(json.loads(statutory_dates)) > 1:
        summary += "Every {} month(s) (".format(repeat_every)
        for statutory_date in json.loads(statutory_dates):
            date = statutory_date["statutory_date"]
            month = statutory_date["statutory_month"]
            summary += "{} {} ".format(self.string_months[month], date)
            current_date = datetime.datetime.today().date()
            due_date_guess = datetime.date(current_date.year, month, date)
            real_due_date = None
            if is_future_date(due_date_guess):
                real_due_date = datetime.date(current_date.year - 1, month, date)
            else:
                real_due_date = due_date_guess
            if from_date <= real_due_date <= to_date:
                due_dates.append(
                    real_due_date
                )
            else:
                continue
        summary += ")"
    elif repeat_by:
        date_details = ""
        if statutory_dates not in ["None", None, ""]:
            statutory_date_json = json.loads(statutory_dates)
            if len(statutory_date_json) > 0:
                date_details += "({})".format(statutory_date_json[0]["statutory_date"])
        # For Compliances Recurring in days
        if repeat_by == 1:  # Days
            summary = "Every {} day(s)".format(repeat_every)
            previous_year_due_date = datetime.date(
                due_date.year - 1, due_date.month, due_date.day
            )
            if from_date <= previous_year_due_date <= to_date:
                due_dates.append(previous_year_due_date)
            iter_due_date = previous_year_due_date
            while not is_future_date(iter_due_date):
                iter_due_date = iter_due_date + datetime.timedelta(days=repeat_every)
                if from_date <= iter_due_date <= to_date:
                    due_dates.append(iter_due_date)
        elif repeat_by == 2:   # Months
            summary = "Every {} month(s) {}".format(repeat_every, date_details)
            iter_due_date = due_date
            while iter_due_date > from_date:
                iter_due_date = iter_due_date + relativedelta.relativedelta(months=-repeat_every)
                if from_date <= iter_due_date <= to_date:
                    due_dates.append(iter_due_date)
        elif repeat_by == 3:   # Years
            summary = "Every {} year(s) {}".format(repeat_every, date_details)
            year = from_date.year
            while year <= to_date.year:
                due_date = datetime.date(
                    year, due_date.month, due_date.day
                )
                if from_date <= due_date  <= to_date:
                    due_dates.append (due_date)
                year += 1
    if len(due_dates) > 2:
        if due_dates[0] > due_dates[1]:
            due_dates.reverse()
    return due_dates, summary

def filter_out_due_dates(db, unit_id, compliance_id, due_dates_list):
    # Checking same due date already exists
    if due_dates_list is not None and len(due_dates_list) > 0:
        formated_date_list = []
        for x in due_dates_list:
            x = str(x)
            x.replace(" ", "")
            formated_date_list.append('%s%s%s' % ("'", x, "'"))
        due_dates = ",".join(str(x) for x in formated_date_list)
        query = '''
            SELECT is_ok FROM
            (SELECT (CASE WHEN (unit_id = '{}' AND DATE(due_date) IN ({}) AND \
            compliance_id = '{}') THEN DATE(due_date) ELSE 'NotExists' END ) as
            is_ok FROM {} ) a WHERE is_ok != "NotExists"'''.format(
            unit_id, due_dates, compliance_id, self.tblComplianceHistory
        )
        rows = db.select_all(query)
        if len(rows) > 0:
            for row in rows:
                formated_date_list.remove("%s%s%s" % ("'", row[0], "'"))
        result_due_date = []
        for current_due_date_index, due_date in enumerate(formated_date_list):
            next_due_date = None

            if len(due_dates_list) < current_due_date_index + 1:
                continue
            else:
                if current_due_date_index == len(formated_date_list)-1 :
                    next_due_date = due_dates_list[current_due_date_index]
                else :
                    next_due_date = due_dates_list[current_due_date_index+1]
                columns = "count(*)"
                condition = "unit_id = '{}' AND due_date < {} AND compliance_id = '{}' AND \
                approve_status = 1 and validity_date > {} and validity_date > '{}'".format(
                    unit_id, due_date, compliance_id, due_date, next_due_date
                )
                rows = db.get_data(self.tblComplianceHistory, columns, condition)
                if rows[0][0] > 0:
                    continue
                else:
                    result_due_date.append(due_date)
        return result_due_date
    else:
        return []

def convert_base64_to_file(file_name, file_content, client_id):
    client_directory = "%s/%d" % (CLIENT_DOCS_BASE_PATH, client_id)
    file_path = "%s/%s" % (client_directory, file_name)
    if not os.path.exists(client_directory):
        os.makedirs(client_directory)
    remove_uploaded_file(file_path)
    if file_content is not None :
        new_file = open(file_path, "wb")
        new_file.write(file_content.decode('base64'))
        new_file.close()

def get_user_name_by_id(db, user_id, client_id=None):
    employee_name = None
    if user_id is not None and user_id != 0:
        columns = "employee_code, employee_name"
        condition = "user_id ='{}'".format(user_id)
        rows = db.get_data(
            tblUsers, columns, condition
        )
        if len(rows) > 0:
            employee_name = "{} - {}".format(rows[0][0], rows[0][1])
    else:
        employee_name = "Administrator"
    return employee_name

def get_form_ids_for_admin(db):
    columns = "group_concat(form_id)"
    condition = "is_admin = 1 OR form_type_id in (4,5) OR form_id in (1, 9,11,10,12)"
    rows = db.get_data(
        tblForms, columns, condition
    )
    return rows[0][0]

def get_report_form_ids(db):
    columns = "group_concat(form_id)"
    condition = " form_type_id = 3"
    rows = db.get_data(
        tblForms, columns, condition
    )
    return rows[0][0]

def get_client_id_from_short_name(db, short_name):
    columns = "client_id"
    condition = "url_short_name = '%s'" % short_name
    rows = db.get_data(
        "tbl_client_groups", columns, condition
    )
    return rows[0][0]

def validate_reset_token(db, reset_token, client_id):
    column = "count(*), user_id"
    condition = " verification_code='%s'" % reset_token
    rows = db.get_data(
        tblEmailVerification, column, condition
    )
    count = rows[0][0]
    user_id = rows[0][1]
    if count == 1:
        column = "count(*)"
        condition = "user_id = '%d' and is_active = 1" % user_id
        rows = db.get_data(tblUsers, column, condition)
        if rows[0][0] > 0 or user_id == 0:
            return user_id
        else:
            return None
    else:
        return None

def update_password(db, password, user_id, client_id):
    columns = ["password"]
    values = [encrypt(password)]
    condition = "1"
    result = False
    condition = " user_id='%d'" % user_id
    result = db.update(
        tblUsers, columns, values, condition, client_id
    )
    if is_primary_admin(db, user_id) or user_id == 0:
        result = db.update(
            tblAdmin, columns, values, "1", client_id
        )
    if user_id != 0:
        columns = "employee_code, employee_name"
        condition = "user_id = '%d'" % user_id
        rows = db.get_data(self.tblUsers, columns, condition)
        employee_name = rows[0][1]
        if rows[0][0] is not None:
            employee_name = "%s - %s" % (rows[0][0], rows[0][1])
    else:
        employee_name = "Administrator"

    action = "\"%s\" has updated his/her password" % ( employee_name)
    db.save_activity(user_id, 0, action)

    if result:
        return True
    else:
        return False

def delete_used_token(self, reset_token, client_id):
    condition = " verification_code='%s'" % reset_token
    if db.delete(tblEmailVerification, condition, client_id):
        return True
    else:
        return False

def remove_session(db, session_token):
        q = "delete from tbl_user_sessions where session_token = '%s'" % (session_token)
        db.execute(q)

def update_profile(db, contact_no, address, session_user):
    columns = ["contact_no", "address"]
    values = [contact_no, address]
    condition = "user_id= '%d'" % session_user
    db.update(tblUsers, columns, values, condition)

def is_service_proivder_user(db, user_id):
    column = "count(1)"
    condition = "user_id = '%d' and is_service_provider = 1" % user_id
    rows = db.get_data(tblUsers, column, condition)
    if rows[0][0] > 0:
        return True
    else:
        return False