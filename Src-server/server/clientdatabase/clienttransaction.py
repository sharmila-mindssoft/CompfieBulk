import threading
import datetime
import json
from server.emailcontroller import EmailHandler
from server import logger
from server.clientdatabase.tables import *
from protocol import (
    clienttransactions, core
)
from server.common import (
   get_date_time, string_to_datetime, datetime_to_string,
   convert_to_dict, get_date_time_in_date, new_uuid
)
from server.clientdatabase.general import (
    calculate_ageing, get_user_unit_ids, get_admin_id,
    get_user_domains, get_email_id_for_users,
    get_user_name_by_id, convert_base64_to_file,
    set_new_due_date, is_two_levels_of_approval,
    is_admin, calculate_due_date, filter_out_due_dates,
    get_user_email_name,  save_compliance_notification,
    get_user_countries, is_space_available, update_used_space
)
from server.exceptionmessage import client_process_error
from server.clientdatabase.savetoknowledge import *
email = EmailHandler()

__all__ = [
    "get_statutory_settings",
    "update_statutory_settings",
    "return_compliance_for_statutory_settings",
    "get_units_for_assign_compliance",
    "get_units_to_assig",
    "get_users_for_seating_units",
    "get_assign_compliance_statutories_for_units",
    "get_units_for_user_grouped_by_industry",
    "get_level_1_statutories_for_user_with_domain",
    "get_statutory_wise_compliances",
    "validate_before_save",
    "save_past_record",
    "get_compliance_approval_count",
    "get_compliance_approval_list",
    "approve_compliance",
    "reject_compliance_approval",
    "get_assigneewise_compliance_count",
    "get_compliance_for_assignee",
    "reassign_compliance",
    "save_assigned_compliance",
    "reject_compliance_concurrence",
    "concur_compliance"
]

CLIENT_DOCS_DOWNLOAD_URL = "/client/client_documents"


def get_statutory_settings(db, session_user):
    admin_id = get_admin_id(db)
    if session_user == admin_id:
        where_qry = ''
        condition_val = None
    else:
        user_id = int(session_user)
        where_qry = " WHERE t2.is_closed=0 AND t1.unit_id in ( " + \
            " select unit_id from tbl_user_units where user_id LIKE %s) " + \
            " AND t1.domain_id in (select domain_id from tbl_user_domains " + \
            " where user_id LIKE %s)"
        condition_val = [user_id, user_id]
    query = "SELECT distinct  " + \
        " t1.country_id, t1.domain_id, t1.unit_id,t2.unit_name, " + \
        " (select business_group_name from tbl_business_groups " + \
        " where business_group_id = t2.business_group_id " + \
        " ) business_group_name, " + \
        " (select legal_entity_name from tbl_legal_entities " + \
        " where legal_entity_id = t2.legal_entity_id)legal_entity_name, " + \
        " (select division_name from tbl_divisions " + \
        " where division_id = t2.division_id)division_name, " + \
        " t2.address, t2.postal_code, t2.unit_code, " + \
        " (select country_name from tbl_countries " + \
        " where country_id = t1.country_id )country_name, " + \
        " (select domain_name from tbl_domains " + \
        " where domain_id = t1.domain_id)domain_name, " + \
        " t2.is_closed,  " + \
        " (select is_new from tbl_client_statutories " + \
        " where unit_id = t1.unit_id order by is_new limit 1) " + \
        " FROM tbl_client_statutories t1 " + \
        " INNER JOIN tbl_units t2 " + \
        " ON t1.unit_id = t2.unit_id %s " + \
        " ORDER BY t1.unit_id "
    query = query % (where_qry)
    if condition_val is None:
        rows = db.select_all(query)
    else:
        rows = db.select_all(query, condition_val)

    columns = [
        "country_id", "domain_id", "unit_id", "unit_name",
        "business_group_name", "legal_entity_name",
        "division_name", "address", "postal_code", "unit_code",
        "country_name", 'domain_name', 'is_closed', 'is_new'
    ]
    result = convert_to_dict(rows, columns)
    return return_statutory_settings(result)


def return_compliance_for_statutory_settings(
    db, unit_id,  from_count, to_count
):
    query = "SELECT t1.client_compliance_id, " + \
        " t1.client_statutory_id, t1.compliance_id, " + \
        " t1.statutory_applicable, t1.statutory_opted, " + \
        " t1.not_applicable_remarks, " + \
        " t1.compliance_applicable, t1.compliance_opted, " + \
        " t1.compliance_remarks, " + \
        " t2.compliance_task, t2.document_name, t2.statutory_mapping, " + \
        " t2.statutory_provision, t2.compliance_description, " + \
        " (select is_new from tbl_client_statutories " + \
        " where client_statutory_id = t1.client_statutory_id), " + \
        " (select domain_name from tbl_domains " + \
        " where domain_id = t2.domain_id), " + \
        " (select count(tc1.client_compliance_id) " + \
        " from tbl_client_compliances tc1 " + \
        " inner join tbl_client_statutories ts2 " + \
        " ON ts2.client_statutory_id = tc1.client_statutory_id " + \
        " AND ts2.unit_id = %s " + \
        " ) total " + \
        " FROM tbl_client_compliances t1 " + \
        " INNER JOIN tbl_compliances t2 " + \
        " ON t2.compliance_id = t1.compliance_id " + \
        " WHERE " + \
        " t1.client_statutory_id in ( " + \
        " select distinct client_statutory_id from " + \
        " tbl_client_statutories where unit_id = %s) " + \
        " ORDER BY t2.domain_id, t2.statutory_mapping " + \
        " limit %s, %s "
    rows = db.select_all(query, [
            unit_id,
            unit_id,
            from_count,
            to_count
    ])
    columns = [
        "client_compliance_id", "client_statutory_id", "compliance_id",
        "statutory_applicable", "statutory_opted",
        "not_applicable_remarks", "compliance_applicable",
        "compliance_opted", "compliance_remarks",
        "compliance_task", "document_name", "statutory_mapping",
        "statutory_provision", "compliance_description",
        "is_new", "domain", "total"
    ]
    results = convert_to_dict(rows, columns)
    statutory_wise_compliances = []
    total = 0
    for r in results:
        total = r["total"]
        statutory_opted = r["statutory_opted"]
        if statutory_opted is None:
            statutory_opted = bool(r["statutory_applicable"])
        else:
            statutory_opted = bool(statutory_opted)

        compliance_opted = r["compliance_opted"]
        if type(compliance_opted) is int:
            compliance_opted = bool(compliance_opted)
        else:
            compliance_opted = bool(r["compliance_applicable"])

        compliance_remarks = r["compliance_remarks"]
        if compliance_remarks == "":
            compliance_remarks = None
        if r["document_name"] == "":
            r["document_name"] = None

        mappings = r["statutory_mapping"].split('>>')
        statutory_name = mappings[0].strip()
        statutory_name = statutory_name.strip()
        if len(mappings) > 1:
            provision = "%s - %s" % (
                ','.join(mappings[1:]),
                r["statutory_provision"]
            )
        else:
            provision = r["statutory_provision"]

        if r["document_name"] not in [None, "None"]:
            name = "%s - %s" % (
                r["document_name"], r["compliance_task"]
            )

        else:
            name = r["compliance_task"]

        compliance = clienttransactions.ComplianceApplicability(
            statutory_name,
            bool(r["statutory_applicable"]),
            statutory_opted,
            r["not_applicable_remarks"],
            r["client_statutory_id"],
            r["client_compliance_id"],
            r["compliance_id"],
            name,
            r["compliance_description"],
            provision,
            bool(r["compliance_applicable"]),
            bool(compliance_opted),
            compliance_remarks,
            not bool(r["is_new"]),
            r["domain"]
        )

        statutory_wise_compliances.append(compliance)
    return statutory_wise_compliances, total


def return_statutory_settings(data):
    unit_wise_statutories = {}
    for d in data:
        domain_name = d["domain_name"]
        unit_id = d["unit_id"]
        unit_name = "%s - %s" % (d["unit_code"], d["unit_name"])
        address = "%s, %s" % (
            d["address"],
            d["postal_code"]
        )

        unit_statutories = unit_wise_statutories.get(unit_id)
        if unit_statutories is None:
            # statutory_dict = {}
            # statutory_dict[domain_name] = statutory_val
            unit_statutories = clienttransactions.UnitStatutoryCompliances(
                unit_id,
                unit_name,
                address,
                d["country_name"],
                [domain_name],
                d["business_group_name"],
                d["legal_entity_name"],
                d["division_name"],
                bool(d["is_closed"]),
                not bool(d["is_new"])
            )
        else:
            domain_list = unit_statutories.domain_names
            domain_list.append(domain_name)
            domain_list = list(set(domain_list))
            unit_statutories.domain_names = domain_list
            # unit_statutories.statutories = statutory_dict
        unit_wise_statutories[unit_id] = unit_statutories
    lst = []
    for k in sorted(unit_wise_statutories):
        lst.append(unit_wise_statutories.get(k))

    return clienttransactions.GetStatutorySettingsSuccess(
        lst
    )


def update_statutory_settings(db, data, session_user):
    unit_id = data.unit_id
    unit_name = data.unit_name
    statutories = data.statutories
    updated_on = get_date_time()
    value_list = []
    for s in statutories:
        client_compliance_id = s.client_compliance_id
        client_statutory_id = s.client_statutory_id
        statutory_opted_status = int(s.applicable_status)
        not_applicable_remarks = s.not_applicable_remarks
        if not_applicable_remarks is None:
            not_applicable_remarks = ""
        compliance_id = s.compliance_id
        opted_status = int(s.compliance_opted_status)
        remarks = s.compliance_remarks
        if remarks is None:
            remarks = ""
        value = (
            client_compliance_id, client_statutory_id, compliance_id,
            statutory_opted_status, not_applicable_remarks,
            opted_status, remarks,
            int(session_user), str(updated_on)
        )
        value_list.append(value)

    execute_bulk_insert(db, value_list)
    update_new_statutory_settings(db, unit_id)
    action = "Statutory settings updated for unit - %s " % (unit_name)
    db.save_activity(session_user, 6, action)
    SaveOptedStatus(data)

    return clienttransactions.UpdateStatutorySettingsSuccess()


def execute_bulk_insert(db, value_list):
    table = "tbl_client_compliances"
    column = [
        "client_compliance_id", "client_statutory_id",
        "compliance_id",
        "statutory_opted", "not_applicable_remarks",
        "compliance_opted", "compliance_remarks",
        "updated_by", "updated_on"
    ]
    update_column = [
        "client_statutory_id", "compliance_id",
        "statutory_opted", "not_applicable_remarks",
        "compliance_opted", "compliance_remarks",
        "updated_by", "updated_on"
    ]

    db.on_duplicate_key_update(
        table, ",".join(column), value_list, update_column
    )


def update_new_statutory_settings(db, unit_id):
    q = "Update tbl_client_statutories set is_new=1 where unit_id = %s"
    db.execute(q, [unit_id])


def get_units_for_assign_compliance(db, session_user, is_closed=None):
    if is_closed is None:
        is_close = 0
    else:
        is_close = '%'
    if session_user != get_admin_id(db):
        qry = " AND t1.unit_id in (select distinct unit_id " + \
            " from tbl_user_units where user_id = %s)"
    else:
        qry = None
    query = "SELECT distinct t1.unit_id, t1.unit_code, t1.unit_name, " + \
        " t1.division_id, t1.legal_entity_id, t1.business_group_id, " + \
        " t1.address, t1.country_id, domain_ids " + \
        " FROM tbl_units t1 WHERE t1.is_closed like %s "
    condition_val = [is_close]
    if qry is not None:
        query += qry
        condition_val.append(int(session_user))

    rows = db.select_all(query, condition_val)
    columns = [
        "unit_id", "unit_code", "unit_name",
        "division_id", "legal_entity_id",
        "business_group_id", "address", "country_id", "domain_ids"
    ]
    result = convert_to_dict(rows, columns)
    return return_units_for_assign_compliance(result)


def get_units_to_assig(db, session_user):
    if session_user != get_admin_id(db):
        qry = " AND t1.unit_id in (select distinct unit_id " + \
            " from tbl_user_units where user_id = %s) "
    else:
        qry = None
    query = "SELECT distinct t1.unit_id, t1.unit_code, t1.unit_name, " + \
        " t1.division_id, t1.legal_entity_id, t1.business_group_id, " + \
        " t1.address, t1.country_id, domain_ids " + \
        " FROM tbl_units t1 WHERE t1.is_closed = 0 " + \
        " AND (select count(distinct t1.compliance_id) " + \
        " from tbl_client_compliances t1 " + \
        " inner join tbl_client_statutories t2 " + \
        " on t1.client_statutory_id = t2.client_statutory_id " + \
        " left join tbl_assigned_compliances t3 " + \
        " on t3.unit_id = t2.unit_id " + \
        " and t3.compliance_id = t1.compliance_id " + \
        " inner join tbl_compliances t4 on " + \
        " t4.compliance_id = t1.compliance_id and t4.is_active = 1 " + \
        " where t3.compliance_id is null and t1.compliance_opted = 1 " + \
        " and t2.unit_id = t1.unit_id) > 0 "

    if qry is not None:
        query += qry
        condition_val = [int(session_user)]
        rows = db.select_all(query, condition_val)
    else:
        rows = db.select_all(query)

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


def get_users_for_seating_units(db, session_user):
    columns = ["user_id", "domain_id"]
    domains = db.get_data(tblUserDomains, columns, "1")
    user_domain_mapping = {}
    for domain in domains:
        user_id = int(domain["user_id"])
        if user_id not in user_domain_mapping:
            user_domain_mapping[user_id] = []
        user_domain_mapping[user_id].append(domain["domain_id"])

    columns = ["user_id", "unit_id"]
    units = db.get_data(tblUserUnits, columns, "1")
    user_unit_mapping = {}
    for unit in units:
        user_id = int(unit["user_id"])
        if user_id not in user_unit_mapping:
            user_unit_mapping[user_id] = []
        user_unit_mapping[user_id].append(unit["unit_id"])
    where_condition = " AND t1.is_primary_admin = 0 " + \
        " AND t1.is_active = 1 AND t2.unit_id " + \
        " IN " + \
        " (select distinct unit_id from tbl_user_units where user_id = %s)"
    query = "SELECT distinct t1.user_id, t1.service_provider_id, " + \
        "  t1.employee_name, t1.employee_code, " + \
        " t1.seating_unit_id, t1.user_level, " + \
        " t1.is_service_provider, " + \
        " (select service_provider_name " + \
        " from  tbl_service_providers " + \
        " where service_provider_id = t1.service_provider_id) " + \
        " service_provider, " + \
        " (select form_ids from tbl_user_groups " + \
        " where user_group_id = t1.user_group_id)form_ids, " + \
        " (select concat(unit_code,' - ',  unit_name) from tbl_units " + \
        " where t1.seating_unit_id = unit_id ) seating_unit_name" + \
        " FROM tbl_users t1 " + \
        " INNER JOIN tbl_user_units t2 " + \
        " ON t1.user_id = t2.user_id " + \
        " WHERE t1.is_active = 1 "

    if session_user != get_admin_id(db):
        query = query + where_condition
        rows = db.select_all(query, [session_user])
    else:
        rows = db.select_all(query)
    columns = [
        "user_id", "service_provider_id", "employee_name", "employee_code",
        "seating_unit_id", "user_level",
        "is_service_provider", "service_provider",
        "form_ids", "seating_unit_name"
    ]
    result = convert_to_dict(rows, columns)
    user_list = []
    for r in result:
        user_id = int(r["user_id"])
        unit_ids = user_unit_mapping[user_id]
        domain_ids = user_domain_mapping[user_id]
        if int(r["is_service_provider"]) == 0:
            name = "%s - %s" % (r["employee_code"], r["employee_name"])
        else:
            name = "%s - %s" % (r["service_provider"], r["employee_name"])
        unit_id = None
        if r["seating_unit_id"]:
            unit_id = int(r["seating_unit_id"])
            unit_name = r["seating_unit_name"]
        if r["form_ids"] is None:
            is_assignee = is_approver = is_concurrence = True
        else:
            form_ids = [int(x) for x in r["form_ids"].split(',')]
            is_assignee = False
            is_approver = False
            is_concurrence = False

            if 11 in form_ids or 12 in form_ids:
                is_assignee = True
            if 9 in form_ids:
                is_concurrence = True
                is_approver = True

        if is_admin(db, user_id):
            is_assignee = is_concurrence = is_approver = True

        user = clienttransactions.ASSIGN_COMPLIANCE_USER(
            user_id,
            r["service_provider_id"],
            name,
            r["user_level"],
            unit_id,
            unit_ids,
            domain_ids,
            is_assignee,
            is_approver,
            is_concurrence,
            unit_name
        )
        # user_list = seating_unit_users.get(unit_id)
        # if user_list is None:
        #     user_list = []
        # user_list.append(user)
        # seating_unit_users[unit_id] = user_list
        user_list.append(user)

    return user_list


def total_compliance_for_units(db, unit_ids, domain_id):
    q = " select " + \
        " count(distinct t01.compliance_id) " + \
        " From " + \
        " tbl_client_compliances t01 " + \
        " inner join " + \
        " tbl_client_statutories t02 ON " + \
        " t01.client_statutory_id = t02.client_statutory_id " + \
        " inner join " + \
        " tbl_compliances t04 ON t01.compliance_id = t04.compliance_id " + \
        " left join " + \
        " tbl_assigned_compliances t03 ON t02.unit_id = t03.unit_id " + \
        " and t01.compliance_id = t03.compliance_id " + \
        " where " + \
        " t02.unit_id in %s " + \
        " and t02.domain_id = %s " + \
        " and t02.is_new = 1 " + \
        " and t01.compliance_opted = 1 " + \
        " and t04.is_active = 1 " + \
        " and t03.compliance_id IS NULL "
    row = db.select_one(q, [
        tuple(unit_ids), domain_id
    ])
    if row:
        return row[0]
    else:
        return 0


def get_assign_compliance_statutories_for_units(
    db, unit_ids, domain_id, session_user, from_count, to_count
):
    if len(unit_ids) == 1:
        unit_ids.append(0)
    if session_user == get_admin_id(db):
        session_user = '%'

    qry_applicable = " SELECT distinct A.compliance_id, " + \
        " B.unit_id units FROM " + \
        " tbl_client_compliances A " + \
        " INNER JOIN tbl_client_statutories B " + \
        " ON A.client_statutory_id = B.client_statutory_id " + \
        " INNER JOIN tbl_compliances C " + \
        " ON A.compliance_id = C.compliance_id " +\
        " LEFT JOIN tbl_assigned_compliances AC " + \
        " ON B.unit_id = AC.unit_id " + \
        " AND A.compliance_id = AC.compliance_id " + \
        " WHERE " + \
        " B.unit_id in %s " + \
        " AND B.domain_id = %s " + \
        " AND A.compliance_opted = 1 " + \
        " AND C.is_active = 1 " + \
        " AND B.is_new = 1 " + \
        " AND AC.compliance_id is null " + \
        " ORDER BY SUBSTRING_INDEX( " + \
        " SUBSTRING_INDEX(C.statutory_mapping, '>>', 1), " + \
        " '>>',  - 1) , A.compliance_id  "

    qry_applicable_val = [
        tuple(unit_ids), domain_id
    ]
    query = " SELECT distinct " + \
        " t2.compliance_id, " + \
        " t1.domain_id, " + \
        " t3.compliance_task, " + \
        " t3.document_name, " + \
        " t3.compliance_description, " + \
        " t3.statutory_mapping, " + \
        " t3.statutory_provision, " + \
        " t3.statutory_dates, " + \
        " (select frequency from tbl_compliance_frequency " + \
        " where frequency_id = t3.frequency_id) frequency, " + \
        " t3.frequency_id, " + \
        " (select duration_type from tbl_compliance_duration_type " + \
        " where duration_type_id = t3.duration_type_id) duration_type, " + \
        " t3.duration, " + \
        " (select repeat_type from tbl_compliance_repeat_type " + \
        " where repeat_type_id = t3.repeats_type_id) repeat_type, " + \
        " t3.repeats_every, " + \
        " t3.repeats_type_id " + \
        " FROM " + \
        " tbl_client_compliances t2  " + \
        " INNER JOIN  " + \
        " tbl_client_statutories t1 " + \
        " ON t2.client_statutory_id = t1.client_statutory_id " + \
        " INNER JOIN " + \
        " tbl_compliances t3 ON t2.compliance_id = t3.compliance_id " + \
        " LEFT JOIN tbl_assigned_compliances AC " + \
        " ON t2.compliance_id = AC.compliance_id " + \
        " and t1.unit_id = AC.unit_id " + \
        " WHERE t1.unit_id IN %s " + \
        " AND t1.domain_id = %s " + \
        " AND t1.is_new = 1 " + \
        " AND t2.compliance_opted = 1 " + \
        " AND t3.is_active = 1 " + \
        " AND AC.compliance_id IS NULL " + \
        " ORDER BY SUBSTRING_INDEX( " + \
        " SUBSTRING_INDEX(t3.statutory_mapping, '>>', 1), " + \
        " '>>', - 1) , t2.compliance_id " + \
        " limit %s, %s "
    db.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ;")
    total = total_compliance_for_units(db, unit_ids, domain_id)
    c_rows = db.select_all(qry_applicable, qry_applicable_val)
    rows = db.select_all(query, [
        tuple(unit_ids),
        domain_id,
        from_count,
        to_count
    ])
    db.execute("SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ ;")

    temp = convert_to_dict(c_rows, ["compliance_id", "units"])
    applicable_units = {}
    for r in temp:
        c_id = int(r["compliance_id"])
        if applicable_units.get(c_id) is None:
            applicable_units[c_id] = [int(r["units"])]
        else:
            applicable_units[c_id].append(int(r["units"]))

    columns = [
        "compliance_id", "domain_id",
        "compliance_task",
        "document_name", "compliance_description",
        "statutory_mapping", "statutory_provision",
        "statutory_dates", "frequency", "frequency_id",
        "duration_type", "duration",
        "repeat_type", "repeats_every", "repeats_type_id"
    ]
    result = convert_to_dict(rows, columns)
    return return_assign_compliance_data(result, applicable_units, total)


def return_assign_compliance_data(result, applicable_units, total):
    level_1_wise = {}
    level_1_name = []
    for r in result:
        c_id = int(r["compliance_id"])
        maipping = r["statutory_mapping"].split(">>")
        level_1 = maipping[0].strip()
        c_units = applicable_units.get(c_id)
        if c_units is None:
            continue
        unit_ids = c_units
        # unit_ids = [
        #     int(x) for x in c_units.split(',')
        # ]
        compliance_list = level_1_wise.get(level_1)
        if compliance_list is None:
            compliance_list = []
        if r["document_name"] not in ("", "None", None):
            name = "%s - %s" % (r["document_name"], r["compliance_task"])
        else:
            name = r["compliance_task"]
        statutory_dates = r["statutory_dates"]
        statutory_dates = json.loads(statutory_dates)

        repeats_evey = repeats_by = None
        if r["frequency_id"] in (2, 3):
            summary = "Repeats every %s - %s" % (
                r["repeats_every"], r["repeat_type"]
            )
            repeats_evey = int(r["repeats_every"])
            repeats_by = r["repeats_type_id"]

        elif r["frequency_id"] == 4:
            summary = "To complete within %s - %s" % (
                r["duration"], r["duration_type"]
            )
        else:
            summary = None

        due_date, due_date_list, date_list = set_new_due_date(
            statutory_dates, r["repeats_type_id"], c_id
        )

        compliance = clienttransactions.UNIT_WISE_STATUTORIES(
            c_id,
            name,
            r["compliance_description"],
            core.COMPLIANCE_FREQUENCY(r["frequency"]),
            date_list,
            due_date_list,
            unit_ids,
            summary,
            repeats_evey,
            repeats_by
        )
        compliance_list.append(compliance)
        level_1_wise[level_1] = compliance_list
    level_1_name = sorted(level_1_wise.keys())
    return level_1_name, level_1_wise, total


def save_assigned_compliance(db, request, session_user):
    new_unit_settings = request.new_units
    current_date = get_date_time()
    created_on = str(current_date)
    country_id = int(request.country_id)
    assignee = int(request.assignee)
    concurrence = request.concurrence_person
    approval = int(request.approval_person)
    compliances = request.compliances

    compliance_names = []
    columns = [
        "country_id", "unit_id", "compliance_id",
        "statutory_dates", "assignee",
        "approval_person", "trigger_before_days",
        "due_date", "validity_date", "created_by",
        "created_on"
    ]
    value_list = []
    update_column = [
        "statutory_dates", "assignee",
        "approval_person", "trigger_before_days",
        "due_date", "validity_date", "created_by",
        "created_on"
    ]

    if concurrence is not None:
        columns.append("concurrence_person")
        update_column.append("concurrence_person")

    for c in compliances:
        compliance_id = int(c.compliance_id)
        statutory_dates = c.statutory_dates
        if statutory_dates is not None:
            date_list = []
            for dates in statutory_dates:
                date_list.append(dates.to_structure())
            date_list = json.dumps(date_list)
        else:
            date_list = []

        unit_ids = c.unit_ids
        if c.trigger_before is not None:
            trigger_before = int(c.trigger_before)
        else:
            trigger_before = "0"
        if c.due_date is not None:
            due_date = datetime.datetime.strptime(c.due_date, "%d-%b-%Y")
            a_due_date = due_date
        else:
            due_date = "0000-00-00"
            a_due_date = "Nil"

        compliance_names.append(
            "Complaince Name:" +
            c.compliance_name +
            "- Due Date:" + str(a_due_date)
        )
        validity_date = c.validity_date
        if validity_date is not None:
            validity_date = datetime.datetime.strptime(
                validity_date, "%d-%b-%Y"
            )
            if due_date > validity_date:
                due_date = validity_date
            elif (validity_date - datetime.timedelta(days=90)) > due_date:
                due_date = validity_date
        else:
            validity_date = "0000-00-00"

        for unit_id in unit_ids:
            value = [
                country_id, unit_id, compliance_id,
                str(date_list), assignee,
                approval, trigger_before, str(due_date),
                str(validity_date), int(session_user), created_on
            ]
            if concurrence is not None:
                value.append(concurrence)
            value_list.append(tuple(value))

    # db.bulk_insert("tbl_assigned_compliances", columns, value_list)
    db.on_duplicate_key_update(
        "tbl_assigned_compliances", ",".join(columns),
        value_list, update_column
    )
    if new_unit_settings is not None:
        update_user_settings(db, new_unit_settings)

    compliance_names = " <br> ".join(compliance_names)
    if request.concurrence_person_name is None:
        action = " Following compliances has assigned to  " + \
            " assignee - %s and approval-person - %s <br> %s" % (
                request.assignee_name,
                request.approval_person_name,
                compliance_names
            )
        cc = [get_email_id_for_users(db, approval)[1]]
    else:
        action = " Following compliances has assigned to " + \
            " assignee - %s concurrence-person - %s " + \
            " approval-person - %s <br> %s"
        action = action % (
                request.assignee_name,
                request.concurrence_person_name,
                request.approval_person_name,
                compliance_names
            )
        cc = [
            get_email_id_for_users(db, concurrence)[1],
            get_email_id_for_users(db, approval)[1]
        ]
    activity_text = action.replace("<br>", " ")
    db.save_activity(session_user, 7, json.dumps(activity_text))
    receiver = get_email_id_for_users(db, assignee)[1]

    notify_assign_compliance = threading.Thread(
        target=email.notify_assign_compliance,
        args=[
            receiver, request.assignee_name, action, cc
        ]
    )
    notify_assign_compliance.start()

    # bg_task_start = threading.Thread(
    #     target=self.start_new_task,
    #     args=[
    #         current_date.date(), country_id
    #     ]
    # )
    # # print "bg_task_start begin"
    # bg_task_start.start()
    # self.start_new_task(current_date.date(), country_id)

    return clienttransactions.SaveAssignedComplianceSuccess()


def get_units_for_user_grouped_by_industry(db, unit_ids):
    condition = "1"
    condition_val = None

    if unit_ids is not None:
        condition, condition_val = db.generate_tuple_condition(
            "unit_id", [int(x) for x in unit_ids.split(",")]
        )
        condition_val = [condition_val]
    industry_column = "industry_name"
    industry_condition = condition + " group by industry_name"
    industry_rows = db.get_data(
        tblUnits, industry_column, industry_condition, condition_val
    )

    columns = [
        "unit_id", "concat(unit_code,'-',unit_name) as u_name",
        "address", "division_id",
        "legal_entity_id", "business_group_id", "country_id", "domain_ids"
    ]
    industry_wise_units = []
    for industry in industry_rows:
        industry_name = industry["industry_name"]
        units = []
        ad_condition = " and industry_name = %s and is_active = 1"
        ad_condition_val = condition_val
        ad_condition_val.append(industry_name)
        rows = db.get_data(
            tblUnits, columns, condition+ad_condition, ad_condition_val
        )
        for unit in rows:
            domain_ids_list = [int(x) for x in unit["domain_ids"].split(",")]
            division_id = None
            b_group_id = None
            if unit["division_id"] > 0:
                division_id = unit["division_id"]
            if unit["business_group_id"] > 0:
                b_group_id = unit["business_group_id"]
            units.append(
                clienttransactions.PastRecordUnits(
                    unit["unit_id"], unit["u_name"],
                    unit["address"], division_id, unit["legal_entity_id"],
                    b_group_id, unit["country_id"], domain_ids_list
                )
            )
        industry_wise_units.append(
            clienttransactions.IndustryWiseUnits(industry_name, units)
        )
    return industry_wise_units


def get_level_1_statutories_for_user_with_domain(
    db, session_user, domain_id=None
):
    if not is_admin(db, session_user):
        condition = " tac.assignee = %s "
        condition_val = [session_user]
    else:
        condition = "1"
        condition_val = None

    query = " SELECT domain_id, statutory_mapping " + \
        " FROM tbl_compliances tc WHERE compliance_id in ( " + \
        " SELECT distinct compliance_id FROM tbl_assigned_compliances tac " + \
        " WHERE %s)"
    query = query % condition
    rows = db.select_all(query, condition_val)
    columns = ["domain_id", "statutory_mapping"]
    result = convert_to_dict(rows, columns)

    level_1_statutory = {}
    for row in result:
        domain_id = str(row["domain_id"])
        statutory_mapping = row["statutory_mapping"]
        if domain_id not in level_1_statutory:
            level_1_statutory[domain_id] = []
        statutories = statutory_mapping.split(">>")
        if statutories[0].strip() not in level_1_statutory[domain_id]:
            level_1_statutory[domain_id].append(statutories[0].strip())
    return level_1_statutory


def get_statutory_wise_compliances(
    db, unit_id, domain_id, level_1_statutory_name, frequency_name,
    country_id, session_user, start_count, to_count
):
    condition = ""
    condition_val = []
    if frequency_name is not None:
        condition += "AND c.frequency_id = (SELECT frequency_id " + \
            " FROM tbl_compliance_frequency WHERE " + \
            " frequency = %s)"
        condition_val.append(frequency_name)
    else:
        condition += "AND c.frequency_id in (2,3)"

    if level_1_statutory_name is not None:
        condition += " AND statutory_mapping like %s"
        condition_val.append(str(level_1_statutory_name + "%"))

    query = "SELECT ac.compliance_id, ac.statutory_dates, ac.due_date, " + \
        " assignee, employee_code, employee_name, statutory_mapping, " + \
        " document_name, compliance_task, compliance_description, " + \
        " c.repeats_type_id, repeat_type, repeats_every, frequency, " + \
        " c.frequency_id FROM tbl_assigned_compliances ac " + \
        " INNER JOIN tbl_users u ON (ac.assignee = u.user_id) " + \
        " INNER JOIN tbl_compliances c ON " + \
        " (ac.compliance_id = c.compliance_id) " + \
        " INNER JOIN tbl_compliance_frequency f " + \
        " ON (c.frequency_id = f.frequency_id) " + \
        " INNER JOIN tbl_compliance_repeat_type rt " + \
        " ON (c.repeats_type_id = rt.repeat_type_id) " + \
        " WHERE ac.is_active = 1 " + \
        " AND c.domain_id = %s AND ac.unit_id = %s "
    param = [
        domain_id, unit_id
    ]
    if condition != "":
        query += condition
        param.extend(condition_val)

    rows = db.select_all(query, param)
    columns = [
        "compliance_id", "statutory_dates", "due_date", "assignee",
        "employee_code", "employee_name", "statutory_mapping",
        "document_name", "compliance_task", "compliance_description",
        "repeats_type_id",  "repeat_type", "repeat_every", "frequency",
        "frequency_id"
    ]
    client_compliance_rows = convert_to_dict(rows, columns)
    level_1_statutory_wise_compliances = {}
    total_count = 0
    compliance_count = 0
    for compliance in client_compliance_rows:
        statutories = compliance["statutory_mapping"].split(">>")
        if level_1_statutory_name is None:

            level_1 = statutories[0]
        else:
            level_1 = level_1_statutory_name
        if level_1 not in level_1_statutory_wise_compliances:
            level_1_statutory_wise_compliances[level_1] = []
        compliance_name = compliance["compliance_task"]
        if compliance["document_name"] not in (None, "None", ""):
            compliance_name = "%s - %s" % (
                compliance["document_name"], compliance_name
            )
        employee_code = compliance["employee_code"]
        if employee_code is None:
            employee_code = "Administrator"
        assingee_name = "%s - %s" % (
            employee_code, compliance["employee_name"]
        )
        due_dates = []
        # statutory_dates_list = []
        summary = ""
        if compliance["repeats_type_id"] == 1:  # Days
            due_dates, summary = calculate_due_date(
                db,
                repeat_by=1,
                repeat_every=compliance["repeat_every"],
                due_date=compliance["due_date"],
                domain_id=domain_id,
                country_id=country_id
            )
        elif compliance["repeats_type_id"] == 2:  # Months
            due_dates, summary = calculate_due_date(
                db,
                statutory_dates=compliance["statutory_dates"],
                repeat_by=2,
                repeat_every=compliance["repeat_every"],
                due_date=compliance["due_date"],
                domain_id=domain_id,
                country_id=country_id
            )
        elif compliance["repeats_type_id"] == 3:  # years
            due_dates, summary = calculate_due_date(
                db,
                repeat_by=3,
                statutory_dates=compliance["statutory_dates"],
                repeat_every=compliance["repeat_every"],
                due_date=compliance["due_date"],
                domain_id=domain_id,
                country_id=country_id
            )
        final_due_dates = filter_out_due_dates(
            db, unit_id, compliance["compliance_id"], due_dates
        )
        total_count += len(final_due_dates)
        for due_date in final_due_dates:
            if (
                int(start_count) <= compliance_count and
                compliance_count < (int(start_count)+to_count)
            ):
                due_date_parts = due_date.replace("'", "").split("-")
                year = due_date_parts[0]
                month = due_date_parts[1]
                day = due_date_parts[2]
                due_date = datetime.date(int(year), int(month), int(day))
                level_1_statutory_wise_compliances[
                    statutories[0].strip()
                ].append(
                    clienttransactions.UNIT_WISE_STATUTORIES_FOR_PAST_RECORDS(
                        compliance["compliance_id"], compliance_name,
                        compliance["compliance_description"],
                        core.COMPLIANCE_FREQUENCY(compliance["frequency"]),
                        summary, datetime_to_string(due_date),
                        assingee_name, compliance["assignee"]
                    )
                )
                compliance_count += 1
            elif compliance_count > (int(start_count)+to_count):
                break
            else:
                compliance_count += 1
                continue

    statutory_wise_compliances = []
    for (
        level_1_statutory_name, compliances
    ) in level_1_statutory_wise_compliances.iteritems():
        if len(compliances) > 0:
            statutory_wise_compliances.append(
                clienttransactions.STATUTORY_WISE_COMPLIANCES(
                    level_1_statutory_name, compliances
                )
            )
    return statutory_wise_compliances, total_count


def is_already_completed_compliance(
    db, due_date, compliance_id, unit_id, due_dates_list=None
):
    # Checking same due date already exists
    columns = "count(*) as history"
    condition = "unit_id = %s and due_date = %s and compliance_id = %s "
    condition_val = [unit_id, due_date, compliance_id]
    rows = db.get_data(tblComplianceHistory, columns, condition, condition_val)
    is_compliance_with_same_due_date_exists = True if (
        rows[0]["history"] > 0) else False
    if is_compliance_with_same_due_date_exists:
        return is_compliance_with_same_due_date_exists
    else:
        # Checking validity of previous compliance
        # exceeds the current compliance
        if due_dates_list is not None:
            next_due_date = None
            current_due_date_index = due_dates_list.index(due_date)
            if len(due_dates_list) < current_due_date_index + 1:
                return False
            else:
                if current_due_date_index == len(due_dates_list)-1:
                    next_due_date = due_dates_list[current_due_date_index]
                else:
                    next_due_date = due_dates_list[current_due_date_index+1]

                columns = "count(*) as history"
                condition = "unit_id = %s AND due_date < %s " + \
                    " AND compliance_id = %s AND " + \
                    " approve_status = 1 and validity_date > %s " + \
                    " and validity_date > %s "
                condition_val = [
                    unit_id, due_date, compliance_id, due_date, next_due_date
                ]
                rows = db.get_data(
                    tblComplianceHistory, columns, condition, condition_val
                )
                if rows[0]["history"] > 0:
                    return True
                else:
                    return False


def validate_before_save(
    db, unit_id, compliance_id, due_date, completion_date, documents,
    validity_date, completed_by
):
    # Checking whether compliance already completed
    if is_already_completed_compliance(
        db, string_to_datetime(due_date),
        compliance_id, unit_id,
        [string_to_datetime(due_date)]
    ):
        return False
    else:
        return True


def save_past_record(
        db, unit_id, compliance_id, due_date, completion_date, documents,
        validity_date, completed_by, client_id
):
    is_uploading_file = False

    # Checking whether compliance already completed
    if is_already_completed_compliance(
        db, string_to_datetime(due_date),
        compliance_id, unit_id,
        [string_to_datetime(due_date)]
    ):
        return False

    # Hanling upload
    document_names = []
    file_size = 0
    if len(documents) > 0:
        for doc in documents:
            file_size += doc.file_size

        if is_space_available(db, file_size):
            is_uploading_file = True
            for doc in documents:
                file_name_parts = doc.file_name.split('.')
                name = None
                exten = None
                for index, file_name_part in enumerate(file_name_parts):
                    if index == len(file_name_parts) - 1:
                        exten = file_name_part
                    else:
                        if name is None:
                            name = file_name_part
                        else:
                            name += file_name_part
                auto_code = new_uuid()
                file_name = "%s-%s.%s" % (name, auto_code, exten)
                document_names.append(file_name)
                convert_base64_to_file(file_name, doc.file_content, client_id)
            update_used_space(db, file_size)
        else:
            return clienttransactions.NotEnoughSpaceAvailable()

    # Checking Settings for two levels of approval
    is_two_level = is_two_levels_of_approval(db)
    # compliance_history_id = db.get_new_id(
    #     "compliance_history_id", tblComplianceHistory
    # )
    completion_date = string_to_datetime(completion_date).date()
    # next_due_date = None
    # if validity_date:
    #   next_due_date = string_to_datetime(validity_date).date()

    # Getting Approval and Concurrence Persons
    concur_approve_columns = "approval_person"
    if is_two_level:
        concur_approve_columns += ", concurrence_person"
    condition = "compliance_id = %s and unit_id = %s "
    rows = db.get_data(
        tblAssignedCompliances,
        concur_approve_columns,
        condition, [compliance_id, unit_id]
    )
    concurred_by = 0
    approved_by = 0
    if rows:
        approved_by = rows[0]["approval_person"]
        if is_two_level:
            concurred_by = rows[0]["concurrence_person"]
    columns = [
        "unit_id", "compliance_id",
        "due_date", "completion_date",
        "completed_by", "completed_on",
        "approve_status", "approved_by", "approved_on"
    ]
    values = [
        unit_id, compliance_id,
        string_to_datetime(due_date).date(),
        completion_date,
        completed_by, completion_date, 1, approved_by, completion_date
    ]
    if validity_date is not None and validity_date != "":
        validity_date = string_to_datetime(validity_date).date()
        columns.append("validity_date")
        values.append(validity_date)

    if is_two_level:
        columns.append("concurrence_status")
        columns.append("concurred_by")
        columns.append("concurred_on")
        values.append(1)
        values.append(concurred_by)
        values.append(completion_date)

    if is_uploading_file:
        columns.append("documents")
        columns.append("document_size")
        values.append(",".join(document_names))
        values.append(file_size)

    result = db.insert(
        tblComplianceHistory, columns, values
    )
    if result is False:
        raise client_process_error("E015")
    return result


def get_compliance_approval_count(db, session_user):
    columns = "count(compliance_history_id) as count"
    condition = "IFNULL(completed_on, 0) != 0 "

    approval_condition = " %s AND IFNULL(approve_status, 0) != 1 "
    approval_condition = approval_condition % condition

    concur_count = 0
    approval_count = 0
    if (is_two_levels_of_approval(db)):
        concur_condition = " %s AND IFNULL(concurrence_status, 0) != 1 "
        concur_condition = concur_condition % approval_condition
        concur_count_condition = concur_condition + "  AND concurred_by = %s "
        concur_count_condition_val = [session_user]
        concur_count = db.get_data(
            tblComplianceHistory, columns,
            concur_count_condition, concur_count_condition_val
        )[0]["count"]
        concurrence_condition = " AND  " + \
            " IF(IFNULL(concurred_by, 0) = 0,  1, concurrence_status = 1)"
        approval_condition = (
            approval_condition + concurrence_condition
        )

    approval_count_condition = approval_condition + " AND " + \
        " approved_by = %s"
    approval_count_condition_val = [session_user]
    approval_count = db.get_data(
        tblComplianceHistory, columns, approval_count_condition,
        approval_count_condition_val
    )[0]["count"]
    return concur_count + approval_count


def get_compliance_approval_list(
    db, start_count, to_count, session_user, client_id
):
    is_two_levels = is_two_levels_of_approval(db)

    query = "SELECT " + \
        " compliance_history_id, tch.compliance_id, start_date, " + \
        " tch.due_date as due_date, documents, completion_date, " + \
        " completed_on, next_due_date, " + \
        " ifnull(concurred_by, -1), remarks, " + \
        " datediff(tch.due_date, completion_date ), " + \
        " compliance_task, compliance_description, tc.frequency_id, " + \
        " (SELECT frequency FROM tbl_compliance_frequency tcf " + \
        " WHERE tcf.frequency_id = tc.frequency_id ), " + \
        " document_name, ifnull(concurrence_status,false), " + \
        " (select statutory_dates from " + \
        " tbl_assigned_compliances tac " + \
        " where tac.compliance_id = tch.compliance_id " + \
        " limit 1), tch.validity_date, ifnull(approved_by, -1), " + \
        " (SELECT concat(unit_code, '-', tu.unit_name) " + \
        " FROM tbl_units tu " + \
        " where tch.unit_id = tu.unit_id), " + \
        " completed_by, " + \
        " (SELECT concat(IFNULL(employee_code, ''),'-',employee_name) " + \
        " FROM tbl_users tu " + \
        " WHERE tu.user_id = tch.completed_by), " + \
        " (SELECT domain_name from tbl_domains td " + \
        " WHERE td.domain_id = tc.domain_id ), duration_type_id " + \
        " FROM tbl_compliance_history tch " + \
        " INNER JOIN tbl_compliances tc " + \
        " ON (tch.compliance_id = tc.compliance_id) " + \
        " WHERE IFNULL(completion_date, 0) != 0  " + \
        " AND IFNULL(completed_on, 0) != 0  "
    order = " ORDER BY completed_by, due_date ASC " + \
        " LIMIT %s, %s "

    param = []
    if is_two_levels:
        condition = " AND ( IFNULL(approve_status, 0) = 0 " + \
            " OR (IFNULL(concurrence_status, 0) = 0 AND " + \
            " IFNULL(approve_status, 0) != 1)) AND " + \
            " (concurred_by = %s OR approved_by = %s)"
        param.append(int(session_user))
        param.append(int(session_user))
    else:
        condition = " AND IFNULL(approve_status, 0) = 0 " + \
            " AND approved_by = %s "
        param.append(int(session_user))
    param.extend([start_count, to_count])
    rows = db.select_all(query + condition + order, param)
    columns = [
        "compliance_history_id", "compliance_id", "start_date",
        "due_date", "documents", "completion_date",
        "completed_on", "next_due_date", "concurred_by", "remarks",
        "ageing", "compliance_task", "compliance_description",
        "frequency_id", "frequency", "document_name",
        "concurrence_status", "statutory_dates", "validity_date",
        "approved_by", "unit_name", "completed_by", "employee_name",
        "domain_name", "duration_type_id"
    ]
    result = convert_to_dict(rows, columns)
    assignee_wise_compliances = {}
    assignee_id_name_map = {}
    count = 0
    for row in result:
        no_of_days, ageing = calculate_ageing(
            due_date=row["due_date"],
            frequency_type=row["frequency_id"],
            duration_type=row["duration_type_id"]
        )
        download_urls = []
        file_name = []
        if row["documents"] is not None and len(row["documents"]) > 0:
            for document in row["documents"].split(","):
                if document is not None and document.strip(',') != '':
                    dl_url = "%s/%s/%s" % (
                        CLIENT_DOCS_DOWNLOAD_URL, str(client_id), document
                    )
                    download_urls.append(dl_url)
                    file_name_part = document.split("-")[0]
                    file_extn_parts = document.split(".")
                    file_extn_part = None
                    if len(file_extn_parts) > 1:
                        file_extn_part = file_extn_parts[
                            len(file_extn_parts)-1
                        ]
                    if file_extn_part is not None:
                        name = "%s.%s" % (
                            file_name_part, file_extn_part
                        )
                        file_name.append(name)
                    else:
                        file_name.append(file_name_part)
        concurred_by_id = None if(
            int(row["concurred_by"]) == -1
        ) else int(row["concurred_by"])
        approved_by_id = None if(
            int(row["approved_by"]) == -1
        ) else int(row["approved_by"])
        compliance_history_id = row["compliance_history_id"]
        start_date = datetime_to_string(row["start_date"])
        due_date = datetime_to_string(row["due_date"])
        documents = download_urls if len(download_urls) > 0 else None
        file_names = file_name if len(file_name) > 0 else None
        completion_date = None if(
                row["completion_date"] is None
            ) else datetime_to_string(row["completion_date"])
        completed_on = None if(
            row["completed_on"] is None
        ) else datetime_to_string(row["completed_on"])
        next_due_date = None if(
            row["next_due_date"] is None
        ) else datetime_to_string(row["next_due_date"])
        concurred_by = None if (
            concurred_by_id is None
            ) else get_user_name_by_id(
                db, concurred_by_id
            )
        remarks = row["remarks"]
        compliance_name = row["compliance_task"]
        if row["document_name"] not in (None, "None", ""):
            compliance_name = "%s - %s" % (
                row["document_name"], compliance_name
            )
        frequency = core.COMPLIANCE_FREQUENCY(row["frequency"])
        description = row["compliance_description"]
        concurrence_status = None if (
                row["concurrence_status"] in [None, "None", ""]
            ) else bool(int(row["concurrence_status"]))
        statutory_dates = [] if (
            row["statutory_dates"] is [None, "None", ""]
        ) else json.loads(row["statutory_dates"])
        validity_date = None if (
            row["validity_date"] is [None, "None", ""]
        ) else datetime_to_string(row["validity_date"])
        unit_name = row["unit_name"]
        date_list = []
        for date in statutory_dates:
            s_date = core.StatutoryDate(
                date["statutory_date"],
                date["statutory_month"],
                date["trigger_before_days"],
                date.get("repeat_by")
            )
            date_list.append(s_date)

        domain_name = row["domain_name"]
        action = None
        if is_two_levels:
            if(
                concurred_by_id == session_user and
                concurrence_status in [False, None]
            ):
                action = "Concur"
            elif(
                concurrence_status is True and
                int(session_user) == approved_by_id
            ):
                action = "Approve"
            elif concurred_by_id is None and session_user == approved_by_id:
                action = "Approve"
            else:
                continue
        elif(
            concurred_by_id != session_user and
            session_user == approved_by_id
        ):
            action = "Approve"
        else:
            continue
        assignee = row["employee_name"]

        if assignee not in assignee_id_name_map:
            assignee_id_name_map[assignee] = row["completed_by"]
        if assignee not in assignee_wise_compliances:
            assignee_wise_compliances[assignee] = []
        count += 1
        assignee_wise_compliances[assignee].append(
            clienttransactions.APPROVALCOMPLIANCE(
                compliance_history_id, compliance_name,
                description, domain_name,
                start_date, due_date, ageing, frequency, documents,
                file_names, completed_on, completion_date, next_due_date,
                concurred_by, remarks, action, date_list,
                validity_date, unit_name
            )
        )
    approval_compliances = []
    for assignee in assignee_wise_compliances:
        if len(assignee_wise_compliances[assignee]) > 0:
            approval_compliances.append(
                clienttransactions.APPORVALCOMPLIANCELIST(
                    assignee_id_name_map[assignee], assignee,
                    assignee_wise_compliances[assignee]
                )
            )
        else:
            continue
    return approval_compliances, count


def save_compliance_activity(
    db, unit_id, compliance_id, activity_status, compliance_status,
    remarks
):
    # compliance_activity_id = db.get_new_id(
    #     "compliance_activity_id", self.tblComplianceActivityLog,
    # )
    date = get_date_time()
    columns = [
        "unit_id", "compliance_id",
        "activity_date", "activity_status", "compliance_status",
        "updated_on"
    ]
    values = [
        unit_id, compliance_id, date, activity_status,
        compliance_status,  date
    ]
    if remarks:
        columns.append("remarks")
        values.append(remarks)
    compliance_activity_id = db.insert(
        tblComplianceActivityLog, columns, values
    )
    if compliance_activity_id is False:
        raise client_process_error("E020")


def approve_compliance(
    db, compliance_history_id, remarks, next_due_date,
    validity_date
):
    # Updating approval in compliance history
    columns = ["approve_status", "approved_on"]

    values = [1, get_date_time()]
    if remarks is not None:
        columns.append("remarks")
        values.append(remarks)
    if next_due_date is not None:
        columns.append("next_due_date")
        values.append(string_to_datetime(next_due_date))
    condition = "compliance_history_id = %s "
    values.append(compliance_history_id)
    db.update(tblComplianceHistory, columns, values, condition)

    # Getting compliance details from compliance history
    query = " SELECT tch.unit_id, tch.compliance_id, " + \
        " (SELECT frequency_id FROM tbl_compliances tc " + \
        " WHERE tch.compliance_id = tc.compliance_id ), " + \
        " due_date, completion_date, " + \
        " (select duration_type_id FROM tbl_compliances tc " + \
        " where tch.compliance_id=tc.compliance_id) " + \
        " FROM tbl_compliance_history tch " + \
        " WHERE compliance_history_id = %s "
    rows = db.select_all(query, [compliance_history_id])
    columns = [
        "unit_id", "compliance_id", "frequency_id",
        "due_date", "completion_date", "duration_type_id"
    ]
    rows = convert_to_dict(rows, columns)

    unit_id = rows[0]["unit_id"]
    compliance_id = rows[0]["compliance_id"]
    due_date = rows[0]["due_date"]
    completion_date = rows[0]["completion_date"]
    frequency_id = rows[0]["frequency_id"]
    duration_type_id = rows[0]["duration_type_id"]

    # Updating next due date validity dates in assign compliance table
    as_columns = []
    as_values = []

    if next_due_date is not None:
        as_columns.append("due_date")
        as_values.append(string_to_datetime(next_due_date))
    if validity_date is not None:
        as_columns.append("validity_date")
        as_values.append(string_to_datetime(validity_date))
    if frequency_id in (1, "1"):
        as_columns.append("is_active")
        as_values.append(0)
    if(
        len(as_columns) > 0 and
        len(as_values) > 0 and
        len(as_columns) == len(as_values)
    ):
        as_condition = " unit_id = %s and compliance_id = %s "
        as_values.extend([unit_id, compliance_id])
        db.update(
            tblAssignedCompliances, as_columns, as_values, as_condition
        )
    status = "Complied"
    if due_date < completion_date:
        status = "Delayed Compliance"

    # Saving in compliance activity
    ageing, remarks = calculate_ageing(
        due_date, frequency_type=frequency_id,
        completion_date=completion_date,
        duration_type=duration_type_id
    )
    save_compliance_activity(
        db, unit_id, compliance_id, "Approved", status,
        remarks
    )
    notify_compliance_approved(db, compliance_history_id, "Approved")
    return True


def get_compliance_history_details(db, compliance_history_id):
    compliance_task_column = "(select compliance_task " + \
        " from tbl_compliances c " + \
        " where c.compliance_id = ch.compliance_id ) as compliance_name "
    document_name_column = "(select document_name " + \
        " from tbl_compliances c " + \
        " where c.compliance_id = ch.compliance_id ) as doc_name"
    columns = [
        "completed_by", "ifnull(concurred_by, -1) as concurred_by",
        "approved_by", compliance_task_column, document_name_column, "due_date"
    ]
    condition = "compliance_history_id = %s "
    rows = db.get_data(
        tblComplianceHistory + " ch", columns,
        condition, [compliance_history_id]
    )
    if rows:
        return rows[0]
    else:
        return {}


def notify_compliance_approved(
    db, compliance_history_id, approval_status
):
    history = get_compliance_history_details(db, compliance_history_id)
    assignee_id = history.get("completed_by")
    concurrence_id = history.get("concurred_by")
    approver_id = history.get("approved_by")
    compliance_name = history.get("compliance_name")
    document_name = history.get("doc_name")

    if(
        document_name is not None and
        document_name != '' and
        document_name != 'None'
    ):
        compliance_name = "%s - %s" % (document_name, compliance_name)

    assignee_email, assignee_name = get_user_email_name(db, str(assignee_id))
    approver_email, approver_name = get_user_email_name(db, str(approver_id))
    concurrence_email, concurrence_name = (None, None)
    if concurrence_id != -1 and is_two_levels_of_approval(db) is True:
        (
            concurrence_email, concurrence_name
        ) = get_user_email_name(db, str(concurrence_id))
        if approval_status == "Approved":
            notification_text = "Compliance %s, " + \
                " completed by %s and concurred by you " + \
                " has approved by %s"
            notification_text = notification_text % (
                    compliance_name, assignee_name, approver_name
                )
            save_compliance_notification(
                db, compliance_history_id, notification_text,
                "Compliance Approved", "ApprovedToConcur"
            )
        else:
            notification_text = "Compliance %s,has completed by %s " + \
                " and concurred by %s " + \
                " Review and approve"
            notification_text = notification_text % (
                    compliance_name, assignee_name, concurrence_name
                )
            save_compliance_notification(
                db, compliance_history_id, notification_text,
                "Compliance Concurred", "Approve"
            )
    who_approved = approver_name if (
            approval_status == "Approved"
        ) else concurrence_name
    category = "Compliance Approved" if (
        approval_status == "Approved"
    ) else "Compliance Concurred"
    notification_text = "Compliance %s has %s by %s" % (
        compliance_name, approval_status, who_approved
    )
    save_compliance_notification(
        db, compliance_history_id, notification_text, category,
        "ApprovedToAssignee"
    )

    try:
        notify_compliance_approved = threading.Thread(
            target=email.notify_task_approved, args=[
                approval_status, assignee_name, assignee_email,
                concurrence_name, concurrence_email, approver_name,
                approver_email, compliance_name, is_two_levels_of_approval(db)
            ]
        )
        notify_compliance_approved.start()
        return True
    except Exception, e:
        logger.logClient(
            "error", "clientdatabase.py-notifycomplianceapproved", e
        )
        print "Error while sending email: %s" % e


def reject_compliance_approval(
    db, compliance_history_id, remarks, next_due_date
):
    query = " SELECT unit_id, ch.compliance_id, due_date, " + \
        "completion_date, completed_by, concurred_by, approved_by, " + \
        "(SELECT concat( " + \
        " IFNULL(document_name+'-',''),compliance_task) " + \
        " FROM tbl_compliances tc " + \
        " WHERE tc.compliance_id = ch.compliance_id) as compliance_name, " + \
        " (SELECT duration_type_id FROM tbl_compliances tc WHERE " + \
        " tc.compliance_id = ch.compliance_id ) " + \
        " FROM tbl_compliance_history ch WHERE compliance_history_id = %s "
    result = db.select_all(query, [compliance_history_id])
    history_columns = [
        "unit_id", "compliance_id", "due_date", "completion_date",
        "assignee_id", "concurrence_id", "approval_id", "compliance_name",
        "duration_type_id"
    ]
    rows = convert_to_dict(result, history_columns)
    unit_id = rows[0]["unit_id"]
    compliance_id = rows[0]["compliance_id"]
    due_date = rows[0]["due_date"]
    completion_date = rows[0]["completion_date"]
    duration_type_id = rows[0]["duration_type_id"]
    status = "Inprogress"

    if due_date is not None:
        if due_date < completion_date:
            status = "Not Complied"

    ageing, ageing_remarks = calculate_ageing(
        due_date, frequency_type=None,
        completion_date=completion_date,
        duration_type=duration_type_id
    )
    save_compliance_activity(
        db, unit_id, compliance_id, "Rejected", status,
        ageing_remarks
    )

    update_columns = [
        "approve_status", "remarks", "completion_date", "completed_on",
        "concurred_on", "concurrence_status"
    ]
    update_condition = "compliance_history_id = %s "
    values = [0, remarks, None, None, None, None, compliance_history_id]
    db.update(
        tblComplianceHistory, update_columns, values, update_condition
    )
    notify_compliance_rejected(
        db, compliance_history_id, remarks,
        "RejectApproval", rows[0]["assignee_id"],
        rows[0]["concurrence_id"], rows[0]["approval_id"],
        rows[0]["compliance_name"], due_date
    )
    return True


def notify_compliance_rejected(
    db,  compliance_history_id, remarks, reject_status, assignee_id,
    concurrence_id,  approver_id, compliance_name, due_date
):
    assignee_email, assignee_name = get_user_email_name(db, str(assignee_id))
    approver_email, approver_name = get_user_email_name(db, str(approver_id))
    concurrence_email, concurrence_name = (None, None)
    if(
        concurrence_id not in [None, "None", "", "null", "Null", 0] and
        is_two_levels_of_approval(db)
    ):
        concurrence_email, concurrence_name = get_user_email_name(
            db, str(concurrence_id)
        )
        if reject_status == "RejectApproval":
            notification_text = "Compliance %s, completed by %s " + \
                " and concurred by you " + \
                " has rejected by %s"
            notification_text = notification_text % (
                compliance_name, assignee_name, approver_name
            )
            save_compliance_notification(
                db, compliance_history_id, notification_text,
                "Compliance Approved", "ApproveRejectedToConcur"
            )

    who_rejected = approver_name if(
        reject_status == "RejectApproval"
    ) else concurrence_name
    category = "Compliance Approval Rejected" if(
        reject_status == "RejectApproval"
    ) else "Compliance Concurrence Rejected"
    notification_text = "Compliance %s has rejected by %s. " + \
        " the reason is %s"
    notification_text = notification_text % (
        compliance_name, who_rejected, remarks
    )
    action = "ApproveRejectedToAssignee" if(
        reject_status == "RejectApproval"
    ) else "ConcurRejected"
    save_compliance_notification(
        db, compliance_history_id, notification_text, category,
        action
    )
    try:
        notify_compliance_rejected_thread = threading.Thread(
            target=email.notify_task_rejected, args=[
                compliance_history_id, remarks, reject_status,
                assignee_name, assignee_email, concurrence_email,
                concurrence_name, compliance_name
            ]
        )
        notify_compliance_rejected_thread.start()
        return True
    except Exception, e:
        logger.logClient("error", "clientdatabase.py-notify-compliance", e)
        print "Error while sending email: %s" % e


def concur_compliance(
    db, compliance_history_id, remarks,
    next_due_date, validity_date
):
    columns = ["concurrence_status", "concurred_on"]

    values = [1, get_date_time()]
    if validity_date is not None:
        columns.append("validity_date")
        values.append(string_to_datetime(validity_date))
    if next_due_date is not None:
        columns.append("next_due_date")
        values.append(string_to_datetime(next_due_date))
    if remarks is not None:
        columns.append("remarks")
        values.append(remarks)
    condition = "compliance_history_id = %s "
    values.append(compliance_history_id)
    db.update(tblComplianceHistory, columns, values, condition)

    columns = "unit_id, compliance_id, due_date, completion_date, " + \
        " (select duration_type_id from tbl_compliances tc where  " + \
        " tc.compliance_id = tch.compliance_id ) as duration_type_id"
    condition = "compliance_history_id = %s "
    rows = db.get_data(
        tblComplianceHistory+ " tch", columns, condition,
        [compliance_history_id]
    )
    unit_id = rows[0]["unit_id"]
    compliance_id = rows[0]["compliance_id"]
    due_date = rows[0]["due_date"]
    completion_date = rows[0]["completion_date"]
    duration_type_id = rows[0]["duration_type_id"]

    columns = []
    values = []
    if validity_date is not None:
        columns.append("validity_date")
        values.append(string_to_datetime(validity_date))
    if next_due_date is not None:
        columns.append("due_date")
        values.append(string_to_datetime(next_due_date))
    if len(columns) > 0:
        condition = "compliance_id = %s AND unit_id = %s "
        values.extend([compliance_id, unit_id])
        db.update(tblAssignedCompliances, columns, values, condition)

    status = "Inprogress"
    # due_date = datetime.datetime(
    #     int(due_date_parts[0]),
    # int(due_date_parts[1]), int(due_date_parts[2])
    # )
    if due_date < completion_date:
        status = "Not Complied"
    ageing, remarks = calculate_ageing(
        due_date, frequency_type=None,
        completion_date=completion_date,
        duration_type=duration_type_id
    )
    save_compliance_activity(
        db, unit_id, compliance_id, "Concurred", status,
        remarks
    )
    notify_compliance_approved(db, compliance_history_id, "Concurred")
    return True


def reject_compliance_concurrence(
    db, compliance_history_id, remarks, next_due_date
):
    compliance_name_column = " (SELECT concat( " + \
        " IFNULL(document_name,''), '-', compliance_task " + \
        " ) " + \
        " FROM tbl_compliances tc " + \
        " WHERE tc.compliance_id = ch.compliance_id) as compliance_task"
    duration_column = "(select duration_type_id  " + \
        " from tbl_compliances tc  " + \
        " where tc.compliance_id=ch.compliance_id) as duration_type_id"
    columns = [
        "unit_id", "ch.compliance_id as compliance_id",
        "due_date", "completion_date",
        "completed_by", "concurred_by", "approved_by",
        compliance_name_column, duration_column
    ]
    condition = "compliance_history_id = %s "

    rows = db.get_data(
        tblComplianceHistory + " ch", columns,
        condition, [compliance_history_id]
    )
    unit_id = rows[0]["unit_id"]
    compliance_id = rows[0]["compliance_id"]
    due_date = rows[0]["due_date"]
    completion_date = rows[0]["completion_date"]
    duration_type_id = rows[0]["duration_type_id"]
    status = "Inprogress"
    if due_date < completion_date:
        status = "Not Complied"
    ageing, ageing_remarks = calculate_ageing(
        due_date, frequency_type=None,
        completion_date=completion_date,
        duration_type=duration_type_id
    )
    save_compliance_activity(
        db, unit_id, compliance_id, "Rejected", status,
        ageing_remarks
    )
    columns = [
        "concurrence_status", "remarks", "completion_date", "completed_on"
    ]

    values = [0,  remarks, None, None]
    condition = "compliance_history_id = %s "
    values.append(compliance_history_id)
    db.update(tblComplianceHistory, columns, values, condition)
    notify_compliance_rejected(
        db, compliance_history_id, remarks, "RejectConcurrence",
        rows[0]["completed_by"], rows[0]["concurred_by"],
        rows[0]["approved_by"], rows[0]["compliance_task"],
        due_date
    )
    return True


def get_assigneewise_compliance_count(db, session_user):
    admin_id = get_admin_id(db)

    q = "SELECT t01.assignee, count( t01.compliance_id ) AS cnt " + \
        " FROM tbl_assigned_compliances t01 " + \
        " INNER JOIN tbl_compliances t02 " + \
        " ON t01.compliance_id = t02.compliance_id " + \
        " LEFT JOIN tbl_compliance_history t03 " + \
        " ON t01.assignee = t03.completed_by " + \
        " AND t01.unit_id = t03.unit_id " + \
        " AND t01.compliance_id = t03.compliance_id " + \
        " AND IFNULL( t03.approve_status, 0 ) !=1 " + \
        " INNER JOIN tbl_client_statutories t04 " + \
        " ON t01.unit_id = t04.unit_id " + \
        " INNER JOIN tbl_client_compliances t05 " + \
        " ON t04.client_statutory_id = t05.client_statutory_id " + \
        " AND t01.compliance_id = t05.compliance_id " + \
        " AND IFNULL(t05.compliance_opted, 0) = 1 " + \
        " WHERE " + \
        " t02.is_active = %s and t01.is_active = %s "
    param = [1, 1]
    order = "GROUP BY t01.assignee "

    if session_user != admin_id:
        user_qry = " AND t01.unit_id in (select distinct unit_id " + \
            " from tbl_user_units where user_id like %s)"
        user_qry += " AND t02.domain_id in (select distinct domain_id " + \
            " from tbl_user_domains where user_id like %s)"
        param.extend([session_user, session_user])
        q += user_qry
    print '-----------------'
    print q
    print param

    db.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ;")
    rows = db.select_all(q + order, param)
    db.execute("SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ ;")
    result = convert_to_dict(rows, columns=["assignee", "count"])
    data = {}
    for r in result:
        data[int(r["assignee"])] = int(r["count"])
    return data


def get_compliance_for_assignee(
    db, session_user, assignee, from_count, to_count
):
    admin_id = get_admin_id(db)
    result = []
    user_qry = ""
    if session_user != admin_id:
        user_qry = " AND t1.unit_id in (select distinct unit_id " + \
            " from tbl_user_units where user_id like %s)"
        user_qry += " AND t2.domain_id in (select distinct domain_id " + \
            " from tbl_user_domains where user_id like %s)"

    columns = [
        "compliance_id", "unit_id", "statutory_dates",
        "assignee", "due_date", "validity_date",
        "compliance_task", "document_name",
        "compliance_description", "statutory_mapping",
        "unit_name", "unit_code", "address", "postal_code",
        "frequency", "frequency_id", "duration_type", "duration",
        "duration_type_id", "repeat_type", "repeats_every",
        "compliance_history_id", "current_due_date",
        "domain_id", "trigger_before_days", "approve_status"
    ]
    q = " SELECT distinct t1.compliance_id, t1.unit_id, " + \
        " t1.statutory_dates, t1.assignee, t1.due_date, " + \
        " t1.validity_date, t2.compliance_task, t2.document_name, " + \
        " t2.compliance_description, t2.statutory_mapping, t3.unit_name, " + \
        " t3.unit_code, t3.address, t3.postal_code, " + \
        " (select frequency from tbl_compliance_frequency " + \
        " where frequency_id = t2.frequency_id) frequency, " + \
        " t2.frequency_id, " + \
        " (select duration_type from tbl_compliance_duration_type " + \
        " where duration_type_id = t2.duration_type_id) duration_type, " + \
        " t2.duration, t2.duration_type_id, " + \
        " (select repeat_type from tbl_compliance_repeat_type " + \
        " where repeat_type_id = t2.repeats_type_id) repeat_type, " + \
        " t2.repeats_every, " + \
        " t4.compliance_history_id, " + \
        " t4.due_date, t2.domain_id, t1.trigger_before_days, " + \
        " IFNULL(t4.approve_status, 0) " + \
        " FROM  tbl_assigned_compliances t1 " + \
        " INNER JOIN  tbl_compliances t2 " + \
        " ON t1.compliance_id = t2.compliance_id " + \
        " AND t1.is_active = 1 " + \
        " INNER JOIN  tbl_units t3 ON t1.unit_id = t3.unit_id " + \
        " LEFT JOIN tbl_compliance_history t4 on " + \
        " t4.unit_id = t1.unit_id " + \
        " and t4.compliance_id = t1.compliance_id " + \
        " and t4.completed_by = t1.assignee " + \
        " and IFNULL(t4.approve_status, 0) != 1 " + \
        " INNER JOIN tbl_client_statutories t5 ON t1.unit_id = t5.unit_id " + \
        " INNER JOIN tbl_client_compliances t6 " + \
        " ON t5.client_statutory_id = t6.client_statutory_id " + \
        " AND t1.compliance_id = t6.compliance_id " + \
        " AND IFNULL(t6.compliance_opted, 0) = 1 " + \
        " WHERE t1.assignee = %s " + \
        " and t1.is_active = 1  "

    order = " ORDER BY t3.unit_id , t2.statutory_mapping," + \
            " t2.frequency_id, t4.due_date " + \
            " limit %s, %s "
    param = [assignee]

    if user_qry != "":
        q += user_qry
        param.extend([session_user, session_user])
    param.extend([from_count, to_count])

    db.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ;")
    rows = db.select_all(q + order, param)
    db.execute("SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ ;")
    result.extend(convert_to_dict(rows, columns))
    return return_compliance_to_reassign(result)


def return_compliance_to_reassign(data):
    assignee_compliance_count = {}
    assignee_wise_compliances = {}
    for d in data:
        assignee = d["assignee"]
        unit_id = d["unit_id"]
        mappings = d["statutory_mapping"].split('>>')
        level_1 = mappings[0].strip()
        unit_name = "%s - %s " % (
            d["unit_code"], d["unit_name"]
        )
        address = "%s- %s " % (
            d["address"], d["postal_code"]
        )
        frequency = core.COMPLIANCE_FREQUENCY(d["frequency"])
        compliance_history_id = d["compliance_history_id"]
        if compliance_history_id is not None and d["approve_status"] == "0":
            compliance_history_id = int(compliance_history_id)
            due_date = d["current_due_date"]
        else:
            compliance_history_id = None
            due_date = d["due_date"]
        if due_date is not None:
            due_date = due_date.strftime("%d-%b-%Y")
        else:
            due_date = ''
        validity_date = d["validity_date"]
        if validity_date is not None:
            validity_date = validity_date.strftime("%d-%b-%Y")
        else:
            validity_date = ''
        statutory_dates = json.loads(d["statutory_dates"])
        date_list = []
        for date in statutory_dates:
            s_date = core.StatutoryDate(
                date["statutory_date"],
                date["statutory_month"],
                date["trigger_before_days"],
                date.get("repeat_by")
            )
            date_list.append(s_date)
        if d["document_name"] not in (None, "None", ""):
            compliance_name = "%s - %s" % (
                d["document_name"], d["compliance_task"]
            )
        else:
            compliance_name = d["compliance_task"]
        if d["frequency_id"] in (2, 3):
            summary = "Repeats every %s - %s" % (
                d["repeats_every"], d["repeat_type"]
            )
        elif d["frequency_id"] == 4:
            summary = "To complete within %s - %s" % (
                d["duration"], d["duration_type"]
            )
            if d["duration_type_id"] == 2:
                due_date = d["due_date"]
                if due_date is not None:
                    due_date = due_date.strftime("%d-%b-%Y %H:%M")
                else:
                    due_date = ''
        else:
            summary = None

        compliance = clienttransactions.STATUTORYWISECOMPLIANCE(
            compliance_history_id, d["compliance_id"],
            compliance_name,
            d["compliance_description"], frequency,
            date_list, due_date, validity_date,
            summary, int(d["domain_id"]), d["trigger_before_days"]
        )
        assignee_data = assignee_wise_compliances.get(assignee)
        if assignee_data is None:
            assignee_data = {}
            # unit_wise_compliances = {}
            statutories = {}
            statutories[level_1] = [compliance]
            unit_data = clienttransactions.USER_WISE_UNITS(
                unit_id, unit_name, address, statutories
            )
            count = assignee_compliance_count.get(assignee)
            if count is None:
                count = 1
            else:
                count += 1
            assignee_compliance_count[assignee] = count
            assignee_data[unit_id] = unit_data
        else:
            unit_data = assignee_data.get(unit_id)
            if unit_data is None:
                statutories = {}
                statutories[level_1] = [compliance]
                unit_data = clienttransactions.USER_WISE_UNITS(
                    unit_id, unit_name, address, statutories
                )
                count = assignee_compliance_count.get(assignee)
                if count is None:
                    count = 1
                else:
                    count += 1
                assignee_compliance_count[assignee] = count
            else:
                statutories = unit_data.statutories
                compliance_list = statutories.get(level_1)
                if compliance_list is None:
                    compliance_list = []
                compliance_list.append(compliance)
                statutories[level_1] = compliance_list

                unit_data.statutories = statutories
                count = assignee_compliance_count.get(assignee)
                if count is None:
                    count = 1
                else:
                    count += 1
                assignee_compliance_count[assignee] = count
            assignee_data[unit_id] = unit_data

        assignee_wise_compliances[assignee] = assignee_data
    return (
            assignee_wise_compliances, assignee_compliance_count
        )


def reassign_compliance(db, request, session_user):
    reassigned_from = request.reassigned_from
    assignee = request.assignee
    concurrence = request.concurrence_person
    approval = request.approval_person
    compliances = request.compliances
    reassigned_reason = request.reassigned_reason
    created_on = get_date_time_in_date()
    reassigned_date = created_on.strftime("%Y-%m-%d")
    created_by = int(session_user)
    new_unit_settings = request.new_units
    compliance_names = []
    compliance_ids = []
    reassing_columns = [
        "unit_id", "compliance_id", "assignee",
        "reassigned_from", "reassigned_date", "remarks",
        "created_by", "created_on"
    ]
    for c in compliances:
        unit_id = c.unit_id
        compliance_id = c.compliance_id
        compliance_ids.append(compliance_id)
        compliance_names.append(c.compliance_name)
        due_date = c.due_date
        if due_date is not None:
            due_date = datetime.datetime.strptime(due_date, "%d-%b-%Y").date()

        history_id = c.compliance_history_id
        values = [
            unit_id, compliance_id, assignee, reassigned_from,
            reassigned_date, reassigned_reason, created_by,
            created_on
        ]
        result = db.insert(
            tblReassignedCompliancesHistory, reassing_columns, values
        )
        if result is False:
            raise client_process_error("E016")

        update_assign_column = [
            "assignee", "is_reassigned", "approval_person",
        ]
        update_assign_val = [
            assignee, 1, approval,
        ]
        if due_date is not None:
            update_assign_column.append("due_date")
            update_assign_val.append(due_date)

        if concurrence not in [None, "None", 0, "null", "NULL"]:
            update_assign_column.append("concurrence_person")
            update_assign_val.append(concurrence)

        where_qry = " unit_id = %s AND compliance_id = %s "
        update_assign_val.extend([unit_id, compliance_id])
        db.update(
            tblAssignedCompliances, update_assign_column,
            update_assign_val, where_qry
        )

        if history_id is not None:
            update_history = "UPDATE tbl_compliance_history SET  " + \
                " completed_by = %s, approved_by = %s"
            if concurrence not in [None, "None", "null", "Null", 0]:
                update_history += " ,concurred_by = %s " % (concurrence)
            where_qry = " WHERE IFNULL(approve_status, 0) != 1 " + \
                " and compliance_id = %s  and unit_id = %s "

            qry = update_history + where_qry
            update_qry_val = [assignee, approval, compliance_id, unit_id]
            db.execute(qry, update_qry_val)

    if new_unit_settings is not None:
        update_user_settings(db, new_unit_settings)

    compliance_names = " <br> ".join(compliance_names)
    if is_admin(db, assignee):
        action = " Following compliances has reassigned to %s <br> %s" % (
            request.assignee_name,
            compliance_names
        )

        cc = None

        if concurrence is None:
            action = " Following compliances has reassigned to " + \
                " assignee - %s and approval-person - %s <br> %s" % (
                    request.assignee_name,
                    get_user_name_by_id(db, request.approval_person),
                    compliance_names
                )
            cc = [
                get_email_id_for_users(db, request.approval_person)[1],
            ]
        else:
            action = " Following compliances has reassigned " + \
                " to assignee - %s concurrence-person - %s " + \
                " approval-person - %s <br> %s"
            action = action % (
                    request.assignee_name,
                    get_user_name_by_id(db, request.concurrence_person),
                    get_user_name_by_id(db, request.approval_person),
                    compliance_names
                )
            cc = [
                get_email_id_for_users(db, request.concurrence_person)[1],
                get_email_id_for_users(db, request.approval_person)[1]
            ]
    activity_text = action.replace("<br>", " ")
    db.save_activity(session_user, 8, json.dumps(activity_text))
    receiver = get_email_id_for_users(db, assignee)[1]
    notify_reassing_compliance = threading.Thread(
        target=email.notify_assign_compliance,
        args=[
            receiver, request.assignee_name, action, cc
        ]
    )
    notify_reassing_compliance.start()
    return clienttransactions.ReassignComplianceSuccess()


def update_user_settings(db, new_units):
    for n in new_units:
        user_id = n.user_id
        unit_ids = n.unit_ids
        domain_ids = n.domain_id
        country_ids = n.country_id

        user_units = get_user_unit_ids(db, user_id)
        new_unit = []
        if unit_ids is not None:
            for u_id in unit_ids:
                if u_id not in user_units:
                    new_unit.append(u_id)

        if len(new_unit) > 0:
            unit_values_list = []
            unit_columns = ["user_id", "unit_id"]
            for unit_id in new_unit:
                unit_value_tuple = (int(user_id), int(unit_id))
                unit_values_list.append(unit_value_tuple)
            db.bulk_insert(tblUserUnits, unit_columns, unit_values_list)
            # action = "New units %s added for user %s
            # while assign compliance " % (
            # new_units, user_id)
            # self.save_activity(user_id, 7, action)

        user_domain_ids = get_user_domains(db, user_id)
        new_domains = []
        if domain_ids is not None:
            for d_id in domain_ids:
                if d_id not in user_domain_ids:
                    new_domains.append(d_id)

        if len(new_domains) > 0:
            domain_values_list = []
            domain_columns = ["user_id", "domain_id"]
            for domain_id in new_domains:
                domain_value_tuple = (int(user_id), int(domain_id))
                domain_values_list.append(domain_value_tuple)
            db.bulk_insert(tblUserDomains, domain_columns, domain_values_list)

        user_countries = get_user_countries(db, user_id)
        new_countries = []
        if country_ids is not None:
            for c_id in country_ids:
                if c_id not in user_countries:
                    new_countries.append(c_id)

        if len(new_countries) > 0:
            country_values_list = []
            country_columns = ["user_id", "country_id"]
            for country_id in new_countries:
                country_value_tuple = (int(user_id), int(country_id))
                country_values_list.append(country_value_tuple)
            db.bulk_insert(
                tblUserCountries, country_columns, country_values_list
            )
