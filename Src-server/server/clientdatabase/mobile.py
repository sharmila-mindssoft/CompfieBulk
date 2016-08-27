import datetime
from protocol import (
    core, clienttransactions, mobile
)
from server.clientdatabase.tables import *
from server.common import (
    convert_to_dict
)
from server.clientdatabase.general import (
    get_admin_id
)

__all__ = [
    "get_version", "get_admin_id",
    "get_users_for_mobile", "get_countries_for_user",
    "get_domains_for_user", "get_business_groups_for_mobile",
    "get_legal_entities_for_mobile", "get_divisions_for_mobile",
    "get_units_for_assign_compliance",
    "get_compliance_applicability_for_mobile",
    "get_trend_chart_for_mobile", "get_compliance_history_for_mobile",
    "get_check_disk_space_for_mobile", "save_registration_key"
]


def get_version(db):
    q = "SELECT unit_details_version, user_details_version, " + \
        " compliance_applicability_version, compliance_history_version, " + \
        " reassign_history_version FROM tbl_mobile_sync_versions"
    rows = db.select_one(q)
    column = [
        "unit_details", "user_details",
        "compliance_applicability",
        "compliance_history",
        "reassign_history"
    ]
    result = convert_to_dict(rows, column)
    return result


def get_users_for_mobile(db, session_user):
    where_condition = " WHERE t2.unit_id IN " + \
        " (select distinct unit_id " + \
        " from tbl_user_units where user_id = %s)"
    where_qry_val = None
    query = "SELECT distinct t1.user_id, t1.employee_name, " + \
        " t1.employee_code, t1.is_service_provider, " + \
        " (select service_provider_name " + \
        " from  tbl_service_providers " + \
        " where service_provider_id = t1.service_provider_id) " + \
        " service_provider " + \
        " FROM tbl_users t1 " + \
        " INNER JOIN tbl_user_units t2 " + \
        " ON t1.user_id = t2.user_id AND t1.is_active = 1 "
    if(
        session_user > 0 and
        session_user != get_admin_id(db)
    ):
        query = query + where_condition
        where_qry_val = [session_user]
    rows = db.select_all(query, where_qry_val)
    columns = [
        "user_id", "employee_name", "employee_code",
        "is_service_provider", "service_provider"
    ]
    result = convert_to_dict(rows, columns)
    user_list = []
    for r in result:
        if int(r["is_service_provider"]) == 0:
            name = "%s - %s" % (r["employee_code"], r["employee_name"])
        else:
            name = "%s - %s" % (r["service_provider"], r["employee_name"])

        user_id = r["user_id"]
        user_list.append(mobile.GetUsersList(user_id, name))
    return user_list


def get_countries_for_user(db, user_id, client_id=None):
    admin_id = get_admin_id(db)
    query = "SELECT distinct t1.country_id, t1.country_name, " + \
        " t1.is_active FROM tbl_countries t1 "
    where_qry_val = None
    if user_id > 0 and user_id != admin_id:
        query = query + " INNER JOIN tbl_user_countries t2 " + \
            " ON t1.country_id = t2.country_id " + \
            " WHERE t2.user_id = %s"
        where_qry_val = [user_id]
    rows = db.select_all(query, where_qry_val)
    columns = ["country_id", "country_name", "is_active"]
    result = convert_to_dict(rows, columns)
    return return_countries(result)


def return_countries(data):
    results = []
    for d in data:
        results.append(core.Country(
            d["country_id"], d["country_name"], bool(d["is_active"])
        ))
    return results


def get_domains_for_user(db, user_id, client_id=None):
        admin_id = get_admin_id(db)
        query = "SELECT distinct t1.domain_id, t1.domain_name, " + \
            " t1.is_active FROM tbl_domains t1 "
        where_qry_val = None
        if user_id > 0 and user_id != admin_id:
            query = query + " INNER JOIN tbl_user_domains t2 ON " + \
                " t1.domain_id = t2.domain_id " + \
                " WHERE t2.user_id = %s"
            where_qry_val = [user_id]
        rows = db.select_all(query, where_qry_val)
        columns = ["domain_id", "domain_name", "is_active"]
        result = convert_to_dict(rows, columns)
        return return_domains(result)


def return_domains(data):
    results = []
    for d in data:
        results.append(core.Domain(
            d["domain_id"], d["domain_name"], bool(d["is_active"])
        ))
    return results


def get_business_groups_for_mobile(db):
        q = "select business_group_id, business_group_name " + \
            " from tbl_business_groups order by business_group_name"
        rows = db.select_all(q)
        result = convert_to_dict(
            rows, ["business_group_id", "business_group_name"])
        business_group_list = []
        for r in result:
            business_group_list.append(
                core.ClientBusinessGroup(
                    r["business_group_id"],
                    r["business_group_name"]
                )
            )
        return business_group_list


def get_legal_entities_for_mobile(db):
    columns = "legal_entity_id, legal_entity_name, business_group_id"
    condition = " 1 ORDER BY legal_entity_name"
    rows = db.get_data(
        tblLegalEntities, columns, condition
    )
    result = convert_to_dict(
        rows, ["legal_entity_id", "legal_entity_name", "business_group_id"]
    )
    legal_entity_list = []
    for r in result:
        legal_entity_list.append(
            core.ClientLegalEntity(
                r["legal_entity_id"],
                r["legal_entity_name"],
                r["business_group_id"]
            )
        )
    return legal_entity_list


def get_divisions_for_mobile(db):
    columns = "division_id, division_name, legal_entity_id, business_group_id"
    condition = " 1 ORDER BY division_name"
    rows = db.get_data(
        tblDivisions, columns, condition
    )
    columns = [
        "division_id", "division_name", "legal_entity_id",
        "business_group_id"
    ]
    result = convert_to_dict(rows, columns)
    division_list = []
    for r in result:
        division_list.append(core.ClientDivision(
            r["division_id"],
            r["division_name"],
            r["legal_entity_id"],
            r["business_group_id"]
        ))
    return division_list


def get_units_for_assign_compliance(db, session_user, is_closed=None):
    if is_closed is None:
        is_close = 0
    else:
        is_close = '%'
    if session_user > 0 and session_user != get_admin_id(db):
        qry = " AND t1.unit_id in (select distinct unit_id " + \
            " from tbl_user_units where user_id = %s)"
        qry_val = [int(session_user)]
    else:
        qry = ""
        qry_val = None
    query = "SELECT distinct t1.unit_id, t1.unit_code, t1.unit_name, " + \
        " t1.division_id, t1.legal_entity_id, t1.business_group_id, " + \
        " t1.address, t1.country_id, domain_ids " + \
        " FROM tbl_units t1 WHERE t1.is_closed like %s"
    param = [is_close]
    query += qry
    if qry_val is not None:
        param.extend(qry_val)

    rows = db.select_all(query, param)
    columns = [
        "unit_id", "unit_code", "unit_name",
        "division_id", "legal_entity_id",
        "business_group_id", "address", "country_id", "domain_ids"
    ]
    result = convert_to_dict(rows, columns)
    return return_units_for_assign_compliance(result)


def return_units_for_assign_compliance(result):
    unit_list = []
    for r in result:
        name = "%s - %s" % (r["unit_code"], r["unit_name"])
        division_id = None
        b_group_id = None
        if r["division_id"] > 0:
            division_id = r["division_id"]
        if r["business_group_id"] > 0:
            b_group_id = r["business_group_id"]

        domain_ids = [int(x) for x in r["domain_ids"].split(',')]
        unit_list.append(
            clienttransactions.ASSIGN_COMPLIANCE_UNITS(
                r["unit_id"], name,
                r["address"],
                division_id,
                r["legal_entity_id"],
                b_group_id,
                r["country_id"],
                domain_ids
            )
        )
    return unit_list


def get_compliance_applicability_for_mobile(db, session_user):
    user_id = session_user
    if session_user == 0 or session_user == get_admin_id(db):
        user_id = "%"
    q = "SELECT t1.country_id, t1.domain_id, t1.unit_id, " + \
        " t2.compliance_id, t2.compliance_applicable, " +  \
        " t2.compliance_opted, t3.compliance_task, " + \
        " t3.document_name, " + \
        " (select frequency from tbl_compliance_frequency where " + \
        " frequency_id = t3.frequency_id) frequency " + \
        " FROM tbl_client_statutories t1 " + \
        " INNER JOIN " + \
        " tbl_client_compliances t2 on " + \
        " t1.client_statutory_id = t2.client_statutory_id " + \
        " INNER JOIN " + \
        " tbl_compliances t3 ON t2.compliance_id = t3.compliance_id " + \
        " WHERE t1.is_new = 1 AND t1.unit_id in " + \
        " (select unit_id from tbl_user_units where " + \
        " user_id LIKE %s)"

    rows = db.select_all(q, [user_id])
    result = convert_to_dict(rows, [
        "country_id", "domain_id", "unit_id",
        "compliance_id", "compliance_applicable",
        "compliance_opted", "compliance_task",
        "document_name", "frequency"
    ])
    applicability = []
    for r in result:
        if r["document_name"] not in ("None", "", None):
            name = "%s - %s" % (r["document_name"], r["compliance_task"])
        else:
            name = r["compliance_task"]
        applicability.append(mobile.ComplianceApplicability(
            r["country_id"],
            r["domain_id"],
            r["unit_id"],
            r["compliance_id"],
            name,
            r["frequency"],
            bool(r["compliance_applicable"]),
            bool(r["compliance_opted"])
        ))
    return applicability


def get_last_7_years(db):
        seven_years_list = []
        end_year = datetime.datetime.now().year - 1
        start_year = end_year - 5
        iter_value = start_year
        while iter_value <= end_year:
            seven_years_list.append(iter_value)
            iter_value += 1
        return seven_years_list


def get_user_unit_ids(db, user_id, client_id=None):
        columns = "unit_id"
        table = tblUnits
        result = None
        condition = ""
        condition_val = None
        if user_id > 0:
            table = tblUserUnits
            condition = " user_id = %s"
            condition_val = [user_id]
        rows = db.get_data(
            table, columns, condition, condition_val
        )
        result = ",".join(str(row[0]) for row in rows)
        return result


def get_trend_chart_for_mobile(db, session_user):
    years = get_last_7_years(db)
    unit_ids = get_user_unit_ids(db, session_user)
    unit_wise_details = []
    if unit_ids not in [None, "None", ""]:
        for unit_id in [int(x) for x in unit_ids.split(",")]:
            unit_details_column = "country_id, domain_ids"
            unit_details_condition = "unit_id = %s"
            unit_details_condition_val = [unit_id]
            rows = db.get_data(
                tblUnits, unit_details_column,
                unit_details_condition,
                unit_details_condition_val
            )
            country_id = rows[0][0]
            domain_ids = rows[0][1]
            country_ids_list = [country_id]
            domain_ids_list = [int(x) for x in domain_ids.split(",")]
            country_domain_timelines = db.get_country_domain_timelines(
                country_ids_list, domain_ids_list, years
            )
            for country_wise_timeline in country_domain_timelines:
                country_id = country_wise_timeline[0]
                domain_wise_timelines = country_wise_timeline[1]
                domain_wise_details = []
                for domain_wise_timeline in domain_wise_timelines:
                    year_wise_count = [
                        [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]
                    ]
                    domain_id = domain_wise_timeline[0]
                    start_end_dates = domain_wise_timeline[1]

                    history_columns = "compliance_history_id"
                    history_condition = " compliance_id in " + \
                        " ( SELECT compliance_id " + \
                        " FROM tbl_compliances WHERE domain_id = %s) " + \
                        " AND unit_id = %s "
                    history_condition_val = [domain_id, unit_id]
                    history_rows = db.get_data(
                        tblComplianceHistory, history_columns,
                        history_condition, history_condition_val
                    )
                    compliance_history_ids = [
                        int(row[0]) for row in history_rows
                    ]

                    if compliance_history_ids not in [None, '', "None"]:
                        for index, dates in enumerate(start_end_dates):
                            columns = "count(*) as total, " + \
                                " sum(case when approve_status = 1 then 1 " + \
                                "else 0 end) as complied "
                            condition = " due_date  between %s and %s and"
                            hist_cond, his_cond_val = db.generate_tuple_condition(
                                "compliance_history_id", compliance_history_ids
                            )
                            condition = condition + hist_cond
                            condition_val = [
                                dates["start_date"], dates["end_date"],
                                his_cond_val
                            ]
                            rows = db.get_data(
                                tblComplianceHistory,
                                columns, condition, condition_val
                            )
                            if len(rows) > 0:
                                row = rows[0]
                                total_compliances = row[0]
                                complied_compliances = row[1] if(
                                    row[1] != None) else 0
                                year_wise_count[
                                    index][0] += int(total_compliances) if(
                                        total_compliances is not None) else 0
                                year_wise_count[index][1] += int(
                                    complied_compliances) if(
                                    complied_compliances is not None) else 0

                    for index, count_of_year in enumerate(year_wise_count):
                        domain_wise_details.append(
                            mobile.DomainWiseCount(
                                domain_id=domain_id,
                                year=years[index],
                                total_compliances=int(count_of_year[0]),
                                complied_compliances_count=int(
                                    count_of_year[1])
                            ))
        unit_wise_details.append(mobile.UnitWiseCount(
            unit_id=unit_id,
            domain_wise_count=domain_wise_details
        ))
    return unit_wise_details


def get_compliance_history_for_mobile(db, user_id, request):
    compliance_history_id = request.compliance_history_id
    if user_id == 0:
        user_qry = '1'
    else:
        user_qry = "(t1.completed_by LIKE %s " + \
            " OR t1.concurred_by LIKE %s " +  \
            " OR t1.approved_by LIKE %s)"

    q = "SELECT t1.compliance_history_id, t1.unit_id, " + \
        " t1.compliance_id, t1.start_date, t1.due_date, " + \
        " t1.completion_date, t1.documents, IFNULL(t1.document_size, 0), " + \
        " t1.validity_date, t1.next_due_date, t1.remarks, " + \
        " t1.completed_by, t1.completed_on, " + \
        " IFNULL(t1.concurrence_status, 0), " + \
        " t1.concurred_by, t1.concurred_on, IFNULL(t1.approve_status, 0), " + \
        " t1.approved_by, t1.approved_on " + \
        " FROM tbl_compliance_history t1 " + \
        " WHERE t1.compliance_history_id > %s AND "
    q = q + user_qry
    param = [compliance_history_id, user_id, user_id, user_id]
    rows = db.select_all(q, param)
    column = [
        "compliance_history_id", "unit_id", "compliance_id",
        "start_date", "due_date", "completion_date",
        "documents", "document_size", "validity_date",
        "next_due_date", "remarks", "completed_by",
        "completed_on", "concurrence_status",
        "concurred_by", "concurred_on", "approve_status",
        "approved_by", "approved_on"
    ]
    result = convert_to_dict(rows, column)
    history_list = []
    for r in result:
        document_list = None
        if r["documents"] is not None:
            documents = r["documents"].strip().split(',')
            if len(documents) > 0:
                document_list = []
                for d in documents:
                    document_list.append(
                        core.FileList(
                            r["document_size"],
                            d,
                            None
                        )
                    )

        history_list.append(mobile.ComplianceHistory(
            r["compliance_history_id"],
            r["unit_id"],
            r["compliance_id"],
            str(r["start_date"]),
            str(r["due_date"]),
            str(r["completion_date"]),
            document_list,
            str(r["validity_date"]),
            str(r["next_due_date"]),
            r["remarks"],
            r["completed_by"],
            str(r["completed_on"]),
            bool(r["concurrence_status"]),
            r["concurred_by"],
            str(r["concurred_on"]),
            bool(r["approve_status"]),
            r["approved_by"],
            str(r["approved_on"])
        ))

    return history_list


def get_check_disk_space_for_mobile(db):
    q = "SELECT total_disk_space, IFNULL(total_disk_space_used, 0) " + \
        " FROM  tbl_client_groups"
    row = db.select_one(q)
    result = convert_to_dict(
        row, ["total_disk_space", "total_disk_space_used"])
    return result


def save_registration_key(db, session_user, request):
    columns = ["registration_key", "device_type_id", "user_id"]
    if request.session_type.lower() is "android":
        device = 2
    elif request.session_type.lower() is "ios":
        device = 3
    elif request.session_type.lower() is "blackberry":
        device = 4

    value_list = [
        request.reg_key, device, session_user
    ]
    db.insert(tblMobileRegistration, columns, value_list)
