from protocol import (core, technotransactions)
from server.common import (
    convert_to_dict, get_date_time, datetime_to_string
)
from server.database.tables import *
from server.database.knowledgemaster import (
    STATUTORY_PARENTS,
    get_statutory_master,
)
from server.exceptionmessage import process_error


def get_assigned_statutories_list(
    db, user_id
):
    query = "SELECT t1.client_statutory_id, t1.client_id, " + \
        " t1.geography_id, t1.country_id, t1.domain_id, t1.unit_id, " + \
        " t1.submission_type, t2.group_name, " + \
        " (select geography_name from tbl_geographies " + \
        " where geography_id = t1.geography_id ) geography_name, " + \
        " (select country_name from tbl_countries " + \
        " where country_id = t1.country_id )country_name, " + \
        " (select domain_name from tbl_domains " +\
        " where domain_id  = t1.domain_id )domain_name, " + \
        " t3.unit_name, t3.unit_code, " + \
        " (select business_group_name from tbl_business_groups " + \
        " where business_group_id =  " + \
        " t3.business_group_id ) business_group_name, " + \
        " (select legal_entity_name from tbl_legal_entities " + \
        " where legal_entity_id = t3.legal_entity_id )legal_entity_name, " + \
        " (select division_name from tbl_divisions " + \
        " where division_id = t3.division_id) division_name, " + \
        " (select industry_name from tbl_industries " + \
        " where industry_id = t3.industry_id )industry_name, " + \
        " t1.created_on " + \
        " FROM tbl_client_statutories t1 " + \
        " INNER JOIN tbl_client_groups t2 " + \
        " ON t1.client_id = t2.client_id " + \
        " INNER JOIN tbl_units t3 " + \
        " ON t1.unit_id = t3.unit_id " + \
        " INNER JOIN tbl_user_countries t11 " + \
        " ON t1.country_id = t11.country_id " + \
        " INNER JOIN tbl_user_domains t12 " + \
        " ON t1.domain_id = t12.domain_id " + \
        " AND t11.user_id = t12.user_id " + \
        " INNER JOIN tbl_user_clients t13 " + \
        " ON t1.client_id = t13.client_id " + \
        " AND t12.user_id = t13.user_id " + \
        " WHERE t13.user_id = %s"
    rows = db.select_all(query, [user_id])
    columns = [
        "client_statutory_id", "client_id", "geography_id",
        "country_id", "domain_id", "unit_id", "submission_type",
        "group_name", "geography_name", "country_name",
        "domain_name", "unit_name", "unit_code", "business_group_name",
        "legal_entity_name", "division_name", "industry_name", "assigned_date"
    ]
    result = convert_to_dict(rows, columns)
    return return_assign_statutory_list(result)


def return_assign_statutory_list(assigned_list):
    ASSIGNED_STATUTORIES_list = []
    for data in assigned_list:
        name = "%s - %s" % (data["unit_code"], data["unit_name"])
        ASSIGNED_STATUTORIES_list.append(
            technotransactions.ASSIGNED_STATUTORIES(
                int(data["submission_type"]),
                int(data["client_statutory_id"]),
                data["country_id"],
                data["country_name"],
                data["client_id"],
                data["group_name"],
                data["business_group_name"],
                data["legal_entity_name"],
                data["division_name"],
                data["unit_id"],
                name,
                data["geography_id"],
                data["geography_name"],
                data["domain_id"],
                data["domain_name"],
                data["industry_name"],
                datetime_to_string(data["assigned_date"])
            )
        )

    return technotransactions.GetAssignedStatutoriesListSuccess(
        ASSIGNED_STATUTORIES_list
    )


def get_assigned_statutories_by_id(db, client_statutory_id):
    query = "SELECT t1.client_statutory_id, t1.client_id, " + \
        " t1.geography_id, t1.country_id, t1.domain_id, t1.unit_id, " + \
        " t1.submission_type, t2.group_name, " + \
        " (select geography_name from tbl_geographies " + \
        " where geography_id = t1.geography_id )geography_name, " + \
        " (select country_name from tbl_countries " + \
        " where country_id = t1.country_id )country_name, " + \
        " (select domain_name from tbl_domains " + \
        " where domain_id  = t1.domain_id )domain_name, " + \
        " t3.unit_name, t3.unit_code, " + \
        " (select business_group_name from tbl_business_groups " + \
        " where business_group_id =  " + \
        " t3.business_group_id ) business_group_name, " + \
        " (select legal_entity_name from tbl_legal_entities " + \
        " where legal_entity_id = t3.legal_entity_id )legal_entity_name, " + \
        " (select division_name from tbl_divisions " + \
        " where division_id = t3.division_id) division_name, " + \
        " (select industry_name from tbl_industries " + \
        " where industry_id = t3.industry_id )industry_name, " + \
        " t3.industry_id " + \
        " FROM tbl_client_statutories t1 " + \
        " INNER JOIN tbl_client_groups t2 " + \
        " ON t1.client_id = t2.client_id " + \
        " INNER JOIN tbl_units t3 " + \
        " ON t1.unit_id = t3.unit_id " + \
        " WHERE t1.client_statutory_id = %s"
    param = [client_statutory_id]
    rows = db.select_one(query, param)
    columns = [
        "client_statutory_id", "client_id", "geography_id",
        "country_id", "domain_id", "unit_id", "submission_type",
        "group_name", "geography_name", "country_name",
        "domain_name", "unit_name", "unit_code",
        "business_group_name", "legal_entity_name",
        "division_name", "industry_name", "industry_id"
    ]
    result = convert_to_dict(rows, columns)
    return return_assigned_statutories_by_id(db, result)


def return_assigned_compliances_by_id(
    db, client_statutory_id, statutory_id=None, applicable_status=None
):
    if bool(STATUTORY_PARENTS) is False:
        get_statutory_master(db)
    if statutory_id is None:
        statutory_id = '%'
    if applicable_status is None:
        applicable_status = '%'
    query = "SELECT t1.client_statutory_id, t1.compliance_id, " + \
        " t1.statutory_id, t1.statutory_applicable, " + \
        " t1.statutory_opted, " + \
        " t1.not_applicable_remarks, " + \
        " t1.compliance_applicable, t1.compliance_opted, " + \
        " t1.compliance_remarks, " + \
        " t2.statutory_name, t3.compliance_task, t3.document_name, " + \
        " t3.statutory_mapping_id, " + \
        " t3.statutory_provision, t3.compliance_description, " + \
        " (SELECT statutory_nature_name from tbl_statutory_natures " + \
        " where statutory_nature_id = (select t.statutory_nature_id " + \
        " from tbl_statutory_mappings t " + \
        " where t.statutory_mapping_id = t3.statutory_mapping_id)), " + \
        " (select distinct level_position from tbl_statutory_levels " + \
        " where level_id = t2.level_id)level, " + \
        " t2.statutory_name, " + \
        " (SELECT statutory_mapping FROM tbl_statutory_mappings " + \
        " where statutory_mapping_id = t3.statutory_mapping_id) " + \
        " FROM tbl_client_compliances t1 " + \
        " INNER JOIN tbl_statutories t2 " + \
        " ON t2.statutory_id = t1.statutory_id " + \
        " INNER JOIN tbl_compliances t3 " + \
        " ON t3.compliance_id = t1.compliance_id " + \
        " WHERE " + \
        " t1.client_statutory_id = %s " + \
        " AND t1.statutory_id like %s " + \
        " AND  t1.compliance_applicable like %s " + \
        " ORDER BY level, statutory_name, compliance_id"
    rows = db.select_all(
        query, [
            client_statutory_id, statutory_id,
            applicable_status
        ]
    )
    columns = [
        "client_statutory_id", "compliance_id", "statutory_id",
        "statutory_applicable", "statutory_opted",
        "not_applicable_remarks", "compliance_applicable",
        "compliance_opted", "compliance_remarks",
        "statutory_name", "compliance_task", "document_name",
        "statutory_mapping_id",
        "statutory_provision", "compliance_description",
        "statutory_nature_name", "level", "statutory_name",
        "statutory_mapping"
    ]
    results = convert_to_dict(rows, columns)
    level_1_statutory_compliance = {}
    for r in results:
        compliance_opted = r["compliance_opted"]
        if compliance_opted is not None:
            compliance_opted = bool(compliance_opted)
        compliance_remarks = r["compliance_remarks"]
        statutory_opted = r["statutory_opted"]
        if statutory_opted is not None:
            statutory_opted = bool(statutory_opted)
        statutory_id = int(r["statutory_id"])
        statutory_name = r["statutory_name"]
        # mapping_id = int(r["statutory_mapping_id"])
        s_mapping = r["statutory_mapping"]
        level_map = s_mapping.split(">>")
        if len(level_map) == 1:
            level_map = None
        else:
            level_map = ">> ".join(level_map[-1:])
        if level_map:
            provision = "%s - %s" % (level_map, r["statutory_provision"])
        else:
            provision = r["statutory_provision"]
        document_name = r["document_name"]
        if document_name == "None":
            document_name = None
        if document_name:
            name = "%s - %s" % (document_name, r["compliance_task"])
        else:
            name = r["compliance_task"]
        compliance = core.ComplianceApplicability(
            r["compliance_id"],
            name,
            r['compliance_description'],
            provision,
            r["statutory_nature_name"],
            bool(r["compliance_applicable"]),
            compliance_opted,
            compliance_remarks
        )
        compliance_list = []
        saved_data = level_1_statutory_compliance.get(statutory_name)
        if saved_data is None:
            compliance_list.append(compliance)
            s_data = core.AssignedStatutory(
                statutory_id,
                r["statutory_name"],
                compliance_list,
                bool(r["statutory_applicable"]),
                statutory_opted,
                r["not_applicable_remarks"]
            )
            level_1_statutory_compliance[statutory_name] = s_data
        else:
            compliance_list = saved_data.compliances
            compliance_list.append(compliance)
            saved_data.compliances = compliance_list
            level_1_statutory_compliance[statutory_name] = saved_data

    final_statutory_list = []
    for key in sorted(level_1_statutory_compliance):
        final_statutory_list.append(
            level_1_statutory_compliance.get(key)
        )

    return final_statutory_list


def get_unassigned_compliances(
    db, country_id, domain_id, industry_id,
    geography_id, unit_id
):
    q = "select parent_ids from tbl_geographies where geography_id = %s"
    row = db.select_one(q, [int(geography_id)])
    if row:
        parent_ids = [int(x) for x in row[0].split(',')[:-1]]
        if len(parent_ids) == 1:
            parent_ids.append(0)
    else:
        parent_ids = []

    query = "SELECT distinct " + \
        " t2.compliance_id, t2.compliance_task, t2.document_name," + \
        " t2.statutory_provision, t2.compliance_description, " + \
        " t5.statutory_id, t.statutory_nature_name " + \
        " FROM tbl_statutory_mappings t1" + \
        " INNER JOIN tbl_compliances t2 " + \
        " ON t1.statutory_mapping_id = t2.statutory_mapping_id " + \
        " INNER JOIN tbl_statutory_industry t3 " + \
        " ON t1.statutory_mapping_id = t3.statutory_mapping_id" + \
        " INNER JOIN tbl_statutory_geographies t4 " + \
        " ON t1.statutory_mapping_id = t4.statutory_mapping_id " + \
        " INNER JOIN tbl_statutory_statutories t5 " + \
        " ON t1.statutory_mapping_id = t5.statutory_mapping_id " + \
        " INNER JOIN tbl_statutory_natures t" + \
        " ON t1.statutory_nature_id = t.statutory_nature_id" + \
        " WHERE t1.is_active = 1 AND t2.is_active = 1 " + \
        " ANd t1.approval_status IN (1, 3) " + \
        " AND t1.domain_id = %s " + \
        " AND t1.country_id = %s " + \
        " AND t3.industry_id = %s " + \
        " AND t4.geography_id" + \
        " IN ( " + \
        " SELECT g.geography_id " + \
        " FROM tbl_geographies g " + \
        " WHERE g.geography_id = %s " + \
        " OR g.parent_ids LIKE %s OR t4.geography_id IN %s )" + \
        " AND t2.compliance_id NOT IN ( " + \
        " SELECT distinct c.compliance_id " + \
        " FROM tbl_client_compliances c " + \
        " INNER JOIN tbl_client_statutories s" + \
        " ON c.client_statutory_id = s.client_statutory_id" + \
        " AND s.domain_id = %s " + \
        " AND s.unit_id = %s " + \
        " ) "
    rows = db.select_all(query, [
        domain_id, country_id, industry_id, geography_id,
        str("%" + str(geography_id) + ",%"),
        tuple(parent_ids),
        domain_id, unit_id
    ])
    print rows
    columns = [
        "compliance_id", "compliance_task",
        "document_name", "statutory_provision",
        "compliance_description", "statutory_id",
        "statutory_nature_name"
    ]
    result = convert_to_dict(rows, columns)
    final_result = []
    compliance_ids = []
    for r in result:
        compliance_id = int(r["compliance_id"])
        if compliance_id not in compliance_ids:
            compliance_ids.append(compliance_id)
            final_result.append(r)
    # New compliances to_structure
    if bool(STATUTORY_PARENTS) is False:
        get_statutory_master(db)
    level_1_compliance = {}
    for d in final_result:
        statutory_nature_name = d["statutory_nature_name"]
        statutory_id = int(d["statutory_id"])
        statutory_data = STATUTORY_PARENTS.get(statutory_id)
        s_mapping = statutory_data[1]
        level_1 = statutory_data[2][0]
        if level_1 == 0:
            level_1 = statutory_id
        compliance_applicable_status = bool(1)
        compliance_opted_status = None
        compliance_remarks = None
        compliance_applicable_list = level_1_compliance.get(level_1)
        if compliance_applicable_list is None:
            compliance_applicable_list = []
        provision = "%s - %s" % (s_mapping, d["statutory_provision"])
        document_name = d["document_name"]
        if document_name == "None":
            document_name = None
        if document_name:
            name = "%s - %s" % (document_name, d["compliance_task"])
        else:
            name = "%s" % (d["compliance_task"])
        c_data = core.ComplianceApplicability(
            d["compliance_id"],
            name,
            d["compliance_description"],
            provision,
            statutory_nature_name,
            compliance_applicable_status,
            compliance_opted_status,
            compliance_remarks
        )
        compliance_applicable_list.append(c_data)
        level_1_compliance[level_1] = compliance_applicable_list

    return level_1_compliance


def return_assigned_statutories_by_id(db, data):
    client_statutory_id = data["client_statutory_id"]
    statutories = return_assigned_compliances_by_id(db, client_statutory_id)
    new_compliances = get_unassigned_compliances(
        db, data["country_id"], data["domain_id"],
        data["industry_id"], data["geography_id"],
        data["unit_id"]
    )
    for key, value in new_compliances.iteritems():
        key = int(key)
        key_exists = False
        for item in statutories:
            if key == item.level_1_statutory_id:
                key_exists = True
                break
        if key_exists is False:
            statutory_name = STATUTORY_PARENTS.get(key)[0]
            s_data = core.AssignedStatutory(
                key,
                statutory_name,
                None,
                True,
                None,
                None
            )
            statutories.append(s_data)

    return technotransactions.GetAssignedStatutoriesByIdSuccess(
        data["country_name"],
        data["group_name"],
        data["business_group_name"],
        data["legal_entity_name"],
        data["division_name"],
        data["unit_name"],
        data["geography_name"],
        data["domain_name"],
        statutories,
        new_compliances,
        data["industry_name"]
    )


def get_groups_for_country(db, country_id, user_id):
    def return_result(groups, client_country_map, client_domain_map):
        group_results = []
        for group in groups:
            client_id = int(group["client_id"])
            group_results.append(core.GroupCompany(
                group["client_id"],
                group["group_name"],
                bool(group["is_active"]),
                client_country_map[client_id],
                client_domain_map[client_id]
            ))
        return group_results

    country_domain_condition = " client_id in ( " + \
        " select distinct client_id " + \
        " from tbl_client_countries where country_id = %s)"
    country_domain_condition_val = [country_id]

    country_columns = [
        "Distinct country_id as country_id", "client_id"
    ]
    countries = db.get_data(
        "tbl_client_countries", country_columns,
        country_domain_condition, country_domain_condition_val
    )

    domain_columns = [
        "Distinct domain_id as domain_id", "client_id"
    ]
    domains = db.get_data(
        "tbl_client_domains", domain_columns,
        country_domain_condition, country_domain_condition_val
    )

    client_country_map = {}
    for country in countries:
        client_id = int(country["client_id"])
        if client_id not in client_country_map:
            client_country_map[client_id] = []
        client_country_map[client_id].append(country["country_id"])

    client_domain_map = {}
    for domain in domains:
        client_id = int(domain["client_id"])
        if client_id not in client_domain_map:
            client_domain_map[client_id] = []
        client_domain_map[client_id].append(domain["domain_id"])

    query = "SELECT distinct t1.client_id, t1.group_name," +  \
        " t1.is_active " + \
        " FROM tbl_client_groups t1 " + \
        " INNER JOIN tbl_user_clients t4 " + \
        " ON t1.client_id = t4.client_id " + \
        " AND t1.is_active = 1 " + \
        " AND t4.user_id =  %s " + \
        " AND t1.client_id in (select distinct client_id " + \
        " from tbl_client_countries where country_id = %s)"

    rows = db.select_all(query, [user_id, country_id])
    columns = [
        "client_id", "group_name", "is_active"
    ]
    results = convert_to_dict(rows, columns)
    return return_result(results, client_country_map, client_domain_map)


def get_business_groups_for_country(db, country_id, user_id):
    query = "SELECT distinct t1.client_id, t1.business_group_id, " + \
        " t1.business_group_name FROM tbl_business_groups t1 " + \
        " INNER JOIN tbl_client_countries t2 " + \
        " ON t1.client_id = t2.client_id " + \
        " INNER JOIN tbl_user_clients t3 " + \
        " ON t1.client_id = t3.client_id " + \
        " AND t3.user_id = %s " + \
        " AND t2.country_id = %s "
    rows = db.select_all(
        query, [
            user_id, country_id
        ]
    )
    columns = ["client_id", "business_group_id", "business_group_name"]
    result = convert_to_dict(rows, columns)

    def return_business_groups(business_groups):
        results = []
        for business_group in business_groups:
            results.append(core.BusinessGroup(
                business_group["business_group_id"],
                business_group["business_group_name"],
                business_group["client_id"]
            ))
        return results

    return return_business_groups(result)


def get_legal_entity_for_country(db, country_id, user_id):
    query = "SELECT distinct t1.client_id, t1.legal_entity_id, " + \
        " t1.legal_entity_name, t1.business_group_id " + \
        " FROM tbl_legal_entities t1 " + \
        " INNER JOIN tbl_client_countries t2 " + \
        " ON t1.client_id = t2.client_id " + \
        " INNER JOIN tbl_user_clients t3 " + \
        " ON t1.client_id = t3.client_id " + \
        " AND t3.user_id = %s " + \
        " AND t2.country_id = %s"
    rows = db.select_all(query, [user_id, country_id])
    columns = [
        "client_id", "legal_entity_id", "legal_entity_name",
        "business_group_id"
    ]
    result = convert_to_dict(rows, columns)

    def return_legal_entities(legal_entities):
        results = []
        for legal_entity in legal_entities:
            results.append(core.LegalEntity(
                legal_entity["legal_entity_id"],
                legal_entity["legal_entity_name"],
                legal_entity["business_group_id"],
                legal_entity["client_id"]
            ))
        return results

    return return_legal_entities(result)


def get_divisions_for_country(db, country_id, user_id):
    query = "SELECT distinct t1.client_id, t1.business_group_id, " + \
        " t1.legal_entity_id, t1.division_id, t1.division_name " + \
        " FROM tbl_divisions t1 " + \
        " INNER JOIN tbl_client_countries t2 " + \
        " ON t1.client_id = t2.client_id " + \
        " INNER JOIN tbl_user_clients t3 " + \
        " ON t1.client_id = t3.client_id " + \
        " AND t3.user_id = %s " + \
        " AND t2.country_id=%s"
    rows = db.select_all(query, [user_id, country_id])
    columns = [
        "client_id", "business_group_id", "legal_entity_id",
        "division_id", "division_name"
    ]
    result = convert_to_dict(rows, columns)

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

    return return_divisions(result)


def get_units_for_country(db, country_id, user_id):
    def return_unit_details(units):
        results = []
        for unit in units:
            domain_ids = [
                int(x) for x in unit["domain_ids"].split(',')
            ]
            parent_ids = [
                int(x) for x in unit["parent_ids"][:-1].split(',')
            ]
            parent_ids.append(int(unit["geography_id"]))
            unit_name = "%s - %s" % (unit["unit_code"], unit["unit_name"])
            results.append(technotransactions.UNIT(
                unit["unit_id"],
                unit_name,
                unit["division_id"],
                unit["legal_entity_id"],
                unit["business_group_id"],
                unit["client_id"],
                domain_ids,
                unit["industry_id"],
                parent_ids
            ))
        return results

    query = "SELECT distinct t1.unit_id, t1.unit_code, t1.unit_name, " + \
        " t1.division_id, t1.legal_entity_id, t1.business_group_id," + \
        " t1.client_id, t1.geography_id, t1.industry_id, t1.domain_ids, " + \
        " t3.parent_ids " + \
        " FROM tbl_units t1 " + \
        " INNER JOIN tbl_client_countries t2 " + \
        " ON t2.client_id = t1.client_id " + \
        " INNER JOIN tbl_geographies t3 " + \
        " ON t1.geography_id = t3.geography_id " + \
        " INNER JOIN tbl_user_clients t4 " + \
        " ON t1.client_id = t4.client_id " + \
        " AND t1.is_active = 1 " + \
        " AND t4.user_id = %s " + \
        " AND t2.country_id = %s "
    rows = db.select_all(query, [user_id, country_id])
    columns = [
        "unit_id", "unit_code", "unit_name", "division_id",
        "legal_entity_id", "business_group_id",
        "client_id", "geography_id",
        "industry_id", "domain_ids", "parent_ids"
    ]
    result = convert_to_dict(rows, columns)
    return return_unit_details(result)


def get_assign_statutory_wizard_two(
    db, country_id, geography_id, industry_id,
    domain_id, unit_id, user_id
):
    if unit_id is not None:
        return return_unassign_statutory_wizard_two(
            db, country_id, geography_id, industry_id, domain_id, unit_id
        )

    q = "select parent_ids from tbl_geographies where geography_id = %s"
    row = db.select_one(q, [int(geography_id)])
    if row:
        parent_ids = [int(x) for x in row[0].split(',')[:-1]]
        if len(parent_ids) == 1:
            parent_ids.append(0)
    else:
        parent_ids = []

    query = "SELECT distinct t1.statutory_mapping_id, " + \
        " t1.statutory_nature_id, t2.statutory_nature_name, " + \
        " t5.statutory_id" + \
        " FROM tbl_statutory_mappings t1 " + \
        " INNER JOIN tbl_statutory_natures t2 " + \
        " ON t1.statutory_nature_id = t2.statutory_nature_id" + \
        " INNER JOIN tbl_statutory_industry t3 " + \
        " ON t1.statutory_mapping_id = t3.statutory_mapping_id" + \
        " INNER JOIN tbl_statutory_geographies t4 " + \
        " ON t1.statutory_mapping_id = t4.statutory_mapping_id " + \
        " INNER JOIN tbl_statutory_statutories t5 " + \
        " ON t1.statutory_mapping_id = t5.statutory_mapping_id" + \
        " WHERE t1.is_active = 1 AND t1.approval_status IN (1, 3) " + \
        " AND t1.domain_id = %s " + \
        " AND t1.country_id = %s " + \
        " AND t3.industry_id = %s " + \
        " AND t4.geography_id" + \
        " IN ( " + \
        " SELECT g.geography_id " + \
        " FROM tbl_geographies g " + \
        " WHERE g.geography_id = %s " + \
        " OR g.parent_ids LIKE %s OR t4.geography_id IN %s )"
    rows = db.select_all(query, [
        domain_id, country_id, industry_id, geography_id,
        str("%" + str(geography_id) + ",%"),
        tuple(parent_ids)
    ])
    print rows
    columns = [
        "statutory_mapping_id", "statutory_nature_id",
        "statutory_nature_name", "statutory_id"
    ]
    result = convert_to_dict(rows, columns)
    final_result = []
    mapping_ids = []
    for r in result:
        mapping_id = int(r["statutory_mapping_id"])
        if mapping_id not in mapping_ids:
            mapping_ids.append(mapping_id)
            final_result.append(r)
    return return_assign_statutory_wizard_two(
        db, country_id, domain_id, final_result
    )


def get_compliance_by_mapping_id(db, mapping_id):
    qry = "SELECT distinct t1.compliance_id, t1.statutory_provision, " + \
        " t1.compliance_task, t1.compliance_description, " + \
        " t1.document_name " + \
        " FROM tbl_compliances t1 " + \
        " WHERE t1.is_active = 1 AND t1.statutory_mapping_id = %s"
    rows = db.select_all(qry, [mapping_id])
    columns = [
        "compliance_id", "statutory_provision",
        "compliance_task", "compliance_description",
        "document_name"
    ]
    result = []
    if rows:
        result = convert_to_dict(rows, columns)
    return result


def return_unassign_statutory_wizard_two(
    db, country_id, geography_id, industry_id,
    domain_id, unit_id
):
    new_compliance = get_unassigned_compliances(
        db, country_id, domain_id, industry_id,
        geography_id, unit_id
    )
    print new_compliance
    assigned_statutory_list = []
    print STATUTORY_PARENTS
    for key, value in new_compliance.items():
        print key
        name = STATUTORY_PARENTS.get(int(key))[0]
        compliances = value
        applicable_status = bool(1)
        statutory_opted_status = None
        not_applicable_remarks = None
        assigned_statutory_list.append(
            core.AssignedStatutory(
                key, name, compliances, applicable_status,
                statutory_opted_status,
                not_applicable_remarks
            )
        )
    return technotransactions.GetStatutoryWizardTwoDataSuccess(
        assigned_statutory_list
    )


def return_assign_statutory_wizard_two(db, country_id, domain_id, data):
    if bool(STATUTORY_PARENTS) is False:
        get_statutory_master(db)
    level_1_compliance = {}
    for d in data:
        mapping_id = int(d["statutory_mapping_id"])
        statutory_nature_name = d["statutory_nature_name"]
        statutory_id = int(d["statutory_id"])
        compliance_list = get_compliance_by_mapping_id(db, mapping_id)
        statutory_data = STATUTORY_PARENTS.get(statutory_id)
        s_mapping = statutory_data[1]
        level_map = s_mapping.split(">>")
        if len(level_map) == 1:
            level_map = None
        else:
            level_map = ">>".join(level_map[-1:])
        statutory_parents = statutory_data[2]
        level_1 = statutory_parents[0]
        if level_1 == 0:
            level_1 = statutory_id
        compliance_applicable_status = bool(1)
        compliance_opted_status = None
        compliance_remarks = None
        compliance_applicable_list = level_1_compliance.get(level_1)
        if compliance_applicable_list is None:
            compliance_applicable_list = []
        for c in compliance_list:
            if level_map is not None:
                provision = "%s - %s" % (level_map, c["statutory_provision"])
            else:
                provision = " %s" % (c["statutory_provision"])
            # provision.replace(level_1, "")
            document_name = c["document_name"]
            if document_name == "None":
                document_name = None
            if document_name:
                name = "%s - %s" % (document_name, c["compliance_task"])
            else:
                name = c["compliance_task"]
            c_data = core.ComplianceApplicability(
                c["compliance_id"],
                name,
                c["compliance_description"],
                provision,
                statutory_nature_name,
                compliance_applicable_status,
                compliance_opted_status,
                compliance_remarks
            )
            compliance_applicable_list.append(c_data)
        level_1_compliance[level_1] = compliance_applicable_list

    assigned_dict = {}
    assigned_statutory_list = []
    for key, value in level_1_compliance.iteritems():
        name = STATUTORY_PARENTS.get(int(key))
        name = name[0]
        compliances = value
        applicable_status = bool(1)
        statutory_opted_status = None
        not_applicable_remarks = None
        assigned_dict[name] = core.AssignedStatutory(
            key, name, compliances, applicable_status,
            statutory_opted_status,
            not_applicable_remarks
        )
    for k in sorted(assigned_dict):
        assigned_statutory_list.append(
            assigned_dict[k]
        )

    return technotransactions.GetStatutoryWizardTwoDataSuccess(
        assigned_statutory_list
    )


def save_assigned_statutories(db, data, user_id):
    submission_type = data.submission_type
    client_statutory_id = data.client_statutory_id
    created_on = get_date_time()
    if submission_type == "Save":
        if client_statutory_id is None:
            save_client_statutories(db, data, user_id)
        else:
            assigned_statutories = data.assigned_statutories
            value_list = save_update_client_complainces(
                db, client_statutory_id, assigned_statutories,
                user_id, created_on
            )
            execute_bulk_insert(db, value_list)
    elif submission_type == "Submit":
        assigned_statutories = data.assigned_statutories
        submit_client_statutories_compliances(
            db, client_statutory_id, assigned_statutories, user_id
        )

    return technotransactions.SaveAssignedStatutorySuccess()


def save_client_statutories(db, data, user_id):
    country_id = data.country_id
    client_id = data.client_id
    geography_id = data.geography_id
    unit_ids = data.unit_ids
    domain_id = data.domain_id
    submission_type = 0

    field = [
        "client_id", "geography_id",
        "country_id", "domain_id", "unit_id", "submission_type",
        "created_by", "created_on"
    ]
    value_list = []
    for unit_id in unit_ids:
        # client_statutory_id = db.get_new_id(
        #     "client_statutory_id", tblClientStatutories
        # )
        created_on = get_date_time()
        values = (
            client_id, geography_id, country_id,
            domain_id, int(unit_id), submission_type,
            int(user_id), created_on
        )
        client_statutory_id = db.insert(tblClientStatutories, field, values)
        if (client_statutory_id is not False):
            assigned_statutories = data.assigned_statutories
            value_list.extend(
                save_update_client_complainces(
                    db, client_statutory_id, assigned_statutories,
                    user_id, created_on
                )
            )
        else:
            raise process_error("E060")
    execute_bulk_insert(db, value_list)


def execute_bulk_insert(db, value_list, submitted_on=None):
    table = "tbl_client_compliances"
    column = [
        "client_statutory_id",
        "compliance_id", "statutory_id", "statutory_applicable",
        "not_applicable_remarks",
        "compliance_applicable",
        "created_by",
    ]
    update_column = [
        "client_statutory_id", "compliance_id",
        "statutory_id", "statutory_applicable",
        "not_applicable_remarks",
        "compliance_applicable"
    ]
    if submitted_on is None:
        column.append("created_on")
        update_column.append("created_on")
    else:
        column.append("submitted_on")
        update_column.append("submitted_on")
    db.on_duplicate_key_update(
        table, ",".join(column), value_list, update_column
    )


def save_update_client_complainces(
    db, client_statutory_id,  data, user_id, created_on
):
    value_list = []
    for d in data:
        level_1_id = d.level_1_statutory_id
        applicable_status = int(d.applicable_status)
        not_applicable_remarks = d.not_applicable_remarks
        if not_applicable_remarks is None:
            not_applicable_remarks = ""
        for key, value in d.compliances.iteritems():
            compliance_id = int(key)
            compliance_applicable_status = int(value)
            values = (
                client_statutory_id, compliance_id,
                level_1_id, applicable_status,
                not_applicable_remarks,
                compliance_applicable_status,
                int(user_id), created_on
            )
            value_list.append(values)

    return value_list


def submit_client_statutories_compliances(
    db, client_statutory_id, data, user_id
):
    submitted_on = get_date_time()
    query = "UPDATE tbl_client_statutories SET submission_type = 1, " + \
        " updated_by=%s WHERE client_statutory_id = %s"
    param = [int(user_id), client_statutory_id]
    db.execute(query, param)
    value_list = save_update_client_complainces(
        db, client_statutory_id, data, user_id, submitted_on
    )
    execute_bulk_insert(db, value_list, submitted_on)
