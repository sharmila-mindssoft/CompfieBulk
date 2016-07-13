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
    "validate_session_token",
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

def validate_session_token(db, client_id, session_token) :
    query = "SELECT t1.user_id, IFNULL(t2.is_service_provider, 0), IFNULL(t2.service_provider_id, 0) \
    FROM tbl_user_sessions t1 \
    INNER JOIN tbl_users t2 ON t1.user_id = t2.user_id AND t2.is_active = 1 \
        WHERE t1.session_token = '%s'" % (session_token)
    row = db.select_one(query)
    user_id = None
    if row :
        user_id = int(row[0])
        is_service_provider = int(row[1])
        service_id = int(row[2])
        if is_service_provider == 1 :
            res = is_service_provider_in_contract(db, service_id)
            if res :
                update_session_time(db, session_token)
                return user_id
        else :
            res = is_in_contract(db)
            if res :
                update_session_time(db, session_token)
                return user_id

    return None

def is_service_provider_in_contract(db, service_provider_id):
    column = "count(1)"
    condition = "now() between contract_from and DATE_ADD(contract_to, INTERVAL 1 DAY)\
    and service_provider_id = '%d' and is_active = 1" % service_provider_id
    rows = db.get_data(tblServiceProviders, column, condition)
    if rows[0][0] > 0:
        return True
    else:
        return False

def update_session_time(db, session_token):
    updated_on = db.get_date_time()
    q = "update tbl_user_sessions set \
    last_accessed_time='%s' where session_token = '%s' " % (
        str(updated_on), str(session_token)
    )
    db.execute(q)

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