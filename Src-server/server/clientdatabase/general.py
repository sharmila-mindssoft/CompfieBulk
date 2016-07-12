
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
    "get_user_domains"
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