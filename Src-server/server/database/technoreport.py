import json
from protocol import (technoreports, core, knowledgereport)
from server.database.tables import *
from server.constants import (
    KNOWLEDGE_FORMAT_DOWNLOAD_URL
)
from server.common import (
    convert_to_dict, string_to_datetime, datetime_to_string
)
from server.database.knowledgemaster import (
    GEOGRAPHY_PARENTS,
    get_geographies
)
from server.database.technotransaction import (
    return_assigned_compliances_by_id
)


def get_assigned_statutories_report(db, request_data, user_id):
    country_id = request_data.country_id
    domain_id = request_data.domain_id
    group_id = request_data.group_id
    qry = ""
    param_list = [country_id, domain_id]

    is_user_has_client = False
    if group_id is not None:
        qry += " AND t1.client_id = %s "
        param_list.append(group_id)
        is_user_has_client = True
    else:
        user_client_columns = ["client_id"]
        user_client_condition = "user_id = %s"
        user_client_condition_params = [user_id]
        user_client_rows = db.get_data(
                tblUserClients, user_client_columns,
                user_client_condition,
                user_client_condition_params
            )
        client_ids = []
        for client in user_client_rows:
            client_ids.append(client["client_id"])
        if len(client_ids) <= 0:
            is_user_has_client = False
        elif len(client_ids) == 1:
            qry += " AND t1.client_id = %s "
            param_list.append(client_ids[0])
            is_user_has_client = True
        else:
            qry += " AND t1.client_id in %s "
            param_list.append(tuple(client_ids))
            is_user_has_client = True

    if is_user_has_client:
        business_group_id = request_data.business_group_id
        if business_group_id is not None:
            qry += " AND t3.business_group_id = %s "
            param_list.append(business_group_id)

        legal_entity_id = request_data.legal_entity_id
        if legal_entity_id is not None:
            qry += " AND t3.legal_entity_id = %s "
            param_list.append(legal_entity_id)

        division_id = request_data.division_id
        if division_id is not None:
            qry += " AND t3.division_id =%s "
            param_list.append(division_id)

        unit_id = request_data.unit_id
        if unit_id is not None:
            qry += " AND t3.unit_id = %s "
            param_list.append(unit_id)

        level_1_statutory_id = request_data.level_1_statutory_id
        if level_1_statutory_id is not None:
            qry += " AND t4.statutory_id = %s "
            param_list.append(level_1_statutory_id)

        applicable_status = request_data.applicability_status
        if applicable_status is not None:
            applicable_status = int(applicable_status)
            qry += " AND t4.compliance_applicable = %s "
            param_list.append(applicable_status)

        query = "SELECT distinct t1.client_statutory_id, t1.client_id, " + \
            " t1.geography_id, t1.country_id, t1.domain_id, t1.unit_id, " + \
            " t1.submission_type, t2.group_name, t3.unit_name, " + \
            " (select business_group_name from tbl_business_groups " + \
            "  where business_group_id " + \
            " = t3.business_group_id ) business_group_name," + \
            " (select legal_entity_name from tbl_legal_entities " + \
            " where legal_entity_id = t3.legal_entity_id) " + \
            " legal_entity_name, " + \
            " (select division_name from tbl_divisions " + \
            " where division_id = t3.division_id)division_name, " + \
            " t3.address, t3.postal_code, t3.unit_code " + \
            " FROM tbl_client_statutories t1 " + \
            " INNER JOIN tbl_client_groups t2 " + \
            " ON t1.client_id = t2.client_id " + \
            " INNER JOIN tbl_units t3 " + \
            " ON t1.unit_id = t3.unit_id " + \
            " INNER JOIN tbl_client_compliances t4 " + \
            " ON t1.client_statutory_id = t4.client_statutory_id " + \
            " WHERE t1.submission_type =1 " + \
            " AND t1.country_id = %s " + \
            " AND t1.domain_id = %s "

        query = query + qry
        rows = db.select_all(query, param_list)
        columns = [
            "client_statutory_id", "client_id", "geography_id",
            "country_id", "domain_id", "unit_id", "submission_type",
            "group_name", "unit_name",
            "business_group_name", "legal_entity_name",
            "division_name", "address", "postal_code", "unit_code"
        ]
        result = convert_to_dict(rows, columns)
        return return_assigned_statutory_report(
            db, result, level_1_statutory_id, applicable_status
        )
    else:
        return technoreports.GetAssignedStatutoryReportSuccess(
            []
        )


def return_assigned_statutory_report(
    db, report_data, level_1_statutory_id, applicable_status
):
    if bool(GEOGRAPHY_PARENTS) is False:
        get_geographies(db)

    unit_wise_statutories_dict = {}
    for data in report_data:
        client_statutory_id = data["client_statutory_id"]
        unit_id = int(data["unit_id"])
        unit_statutories = unit_wise_statutories_dict.get(unit_id)
        if unit_statutories is None:
            geography_id = int(data["geography_id"])
            geography_parents = GEOGRAPHY_PARENTS.get(geography_id)
            temp_parents = geography_parents[0].split(">>")
            ordered = temp_parents[::-1]
            unit_name = "%s - %s" % (data["unit_code"], data["unit_name"])
            unit_address = "%s, %s, %s" % (
                data["address"], ', '.join(ordered), data["postal_code"]
            )
            statutories = return_assigned_compliances_by_id(
                db, client_statutory_id, level_1_statutory_id,
                applicable_status
            )
            print '*' * 50
            unit_statutories = technoreports.UNIT_WISE_ASSIGNED_STATUTORIES(
                data["unit_id"],
                unit_name,
                data["group_name"],
                data["business_group_name"],
                data["legal_entity_name"],
                data["division_name"],
                unit_address,
                statutories
            )
        else:
            statutories = unit_statutories.assigned_statutories
            new_stautory = return_assigned_compliances_by_id(
                db, client_statutory_id, None, applicable_status
            )
            print '*' * 50
            for new_s in new_stautory:
                new_id = new_s.level_1_statutory_id
                is_exists = False
                for x in statutories:
                    if x.level_1_statutory_id == new_id:
                        x.compliances.extend(new_s.compliances)
                        is_exists = True
                        break
                if is_exists is False:
                    statutories.append(new_s)
            unit_statutories.assigned_statutories = statutories

        unit_wise_statutories_dict[unit_id] = unit_statutories

    final_unit_wise_statutories_list = []
    for key, value in unit_wise_statutories_dict.iteritems():
        final_unit_wise_statutories_list.append(value)

    return technoreports.GetAssignedStatutoryReportSuccess(
        final_unit_wise_statutories_list
    )


def get_statutory_notifications_report_data(db, request_data):
    country_id = request_data.country_id
    domain_id = request_data.domain_id
    level_1_statutory_id = request_data.level_1_statutory_id
    from_date = request_data.from_date
    to_date = request_data.to_date
    where_qry = ""
    where_qry_val = [country_id, domain_id]
    if level_1_statutory_id is not None:
        where_qry += " AND tss.statutory_id IN " + \
            " (select statutory_id from tbl_statutories " + \
            " where FIND_IN_SET(%s, parent_ids)) "
        where_qry_val.append(level_1_statutory_id)

    if from_date is not None and to_date is not None:
        from_date = string_to_datetime(from_date).date()
        to_date = string_to_datetime(to_date).date()
        where_qry += " AND date(tsnl.updated_on) between %s " + \
            " AND %s"
        where_qry_val.extend([from_date, to_date])
    query = "SELECT  ts.statutory_name, tsnl.statutory_provision, " + \
        " tsnl.notification_text, tsnl.updated_on " + \
        " from `tbl_statutory_notifications_log` tsnl " + \
        " INNER JOIN `tbl_statutory_statutories` tss ON " + \
        " tsnl.statutory_mapping_id = tss.statutory_mapping_id " + \
        " INNER JOIN `tbl_statutory_mappings` tsm ON " + \
        " tsm.statutory_mapping_id = tsnl.statutory_mapping_id " + \
        " INNER JOIN  `tbl_statutories` ts ON " + \
        " tss.statutory_id = ts.statutory_id " + \
        " WHERE  " + \
        " tsm.country_id = %s and " + \
        " tsm.domain_id = %s "
    query += where_qry
    notifications_rows = db.select_all(query, where_qry_val)
    notification_columns = [
        "statutory_name", "statutory_provision",
        "notification_text", "updated_on"
    ]
    statutory_notifications = convert_to_dict(
        notifications_rows, notification_columns
    )
    return return_statutory_notifications(
        statutory_notifications, country_id, domain_id
    )


def return_statutory_notifications(
    statutory_notifications, country_id, domain_id
):
    notifications = []
    for notification in statutory_notifications:
        notifications.append(
            technoreports.NOTIFICATIONS(
                statutory_provision=notification["statutory_provision"],
                notification_text=notification["notification_text"],
                date_and_time=datetime_to_string(notification["updated_on"])
            )
        )
    final_result = []
    if len(notifications) > 0:
        final_result.append(
            technoreports.COUNTRY_WISE_NOTIFICATIONS(
                country_id=country_id,
                domain_id=domain_id,
                notifications=notifications
            )
        )
    return final_result


#
#   Get Details Report
#
def get_client_details_report_condition(
    country_id, client_id, business_group_id,
    legal_entity_id, division_id, unit_id, domain_ids
):
    condition = "tu.country_id = %s AND tu.client_id = %s "
    param = [country_id, client_id]
    if business_group_id is not None:
        condition += " AND tu.business_group_id = %s "
        param.append(business_group_id)

    if legal_entity_id is not None:
        condition += " AND tu.legal_entity_id = %s "
        param.append(legal_entity_id)

    if division_id is not None:
        condition += " AND tu.division_id = %s "
        param.append(division_id)

    if unit_id is not None:
        condition += " AND tu.unit_id = %s "
        param.append(unit_id)

    if domain_ids is not None:
        for i, domain_id in enumerate(domain_ids):
            if i == 0:
                condition += "  AND (FIND_IN_SET(%s, tu.domain_ids)"
                param.append(domain_id)
            elif i == len(domain_ids) - 1:
                condition += " OR FIND_IN_SET(%s, tu.domain_ids) )"
                param.append(domain_id)
            else:
                condition += " OR FIND_IN_SET(%s, tu.domain_ids)"
                param.append(domain_id)
        if len(domain_ids) == 1:
            condition += " )"
    return condition, param


def get_client_details_report_count(
    db, country_id, client_id, business_group_id,
    legal_entity_id, division_id, unit_id, domain_ids
):
    condition, param = get_client_details_report_condition(
        country_id, client_id, business_group_id,
        legal_entity_id, division_id, unit_id, domain_ids
    )
    query = "SELECT count(*) " +\
        " FROM %s tu " + \
        " WHERE %s "
    query = query % (tblUnits, condition)
    rows = db.select_all(query, param)
    result = convert_to_dict(rows, ["count"])
    return result[0]["count"]


def get_client_details_report(
    db, country_id, client_id, business_group_id,
    legal_entity_id, division_id, unit_id, domain_ids,
    start_count, to_count
):
    condition, params = get_client_details_report_condition(
        country_id, client_id, business_group_id,
        legal_entity_id, division_id, unit_id, domain_ids
    )
    columns = " unit_id, unit_code, unit_name, geography_name, " + \
        " address, domain_ids, postal_code, " + \
        " business_group_name, legal_entity_name, " + \
        " division_name "
    query = " SELECT %s FROM %s tu " + \
        " INNER JOIN %s tg ON (tu.geography_id = tg.geography_id) " + \
        " LEFT JOIN %s tb ON (tb.business_group_id " + \
        " = tu.business_group_id) " + \
        " INNER JOIN %s tl ON " + \
        " (tl.legal_entity_id = tu.legal_entity_id) " + \
        " LEFT JOIN %s td ON (td.division_id = tu.division_id) " + \
        " WHERE %s "
    query = query % (
            columns, tblUnits, tblGeographies, tblBusinessGroups,
            tblLegalEntities, tblDivisions, condition
        )
    query += " ORDER BY tu.business_group_id, " + \
        " tu.legal_entity_id, tu.division_id, " + \
        " tu.unit_id ASC LIMIT %s, %s"
    params.extend([int(start_count), int(to_count)])
    rows = db.select_all(query, params)
    print rows
    columns_list = columns.replace(" ", "").split(",")
    unit_rows = convert_to_dict(rows, columns_list)
    grouped_units = {}
    for unit in unit_rows:
        business_group_name = unit["business_group_name"]
        legal_entity_name = unit["legal_entity_name"]
        division_name = unit["division_name"]
        if business_group_name in ["None", None, ""]:
            business_group_name = "null"
        if division_name in ["None", None, ""]:
            division_name = "null"
        if business_group_name not in grouped_units:
            grouped_units[business_group_name] = {}
        if legal_entity_name not in grouped_units[business_group_name]:
            grouped_units[business_group_name][legal_entity_name] = {}
        if (
            division_name not in grouped_units[
                business_group_name][legal_entity_name]
        ):
            grouped_units[
                business_group_name][legal_entity_name][division_name] = []
        grouped_units[
            business_group_name][legal_entity_name][division_name].append(
            technoreports.UnitDetails(
                unit["unit_id"], unit["geography_name"], unit["unit_code"],
                unit["unit_name"], unit["address"], unit["postal_code"],
                [int(x) for x in unit["domain_ids"].split(",")]
            )
        )
    GroupedUnits = []
    for business_group in grouped_units:
        for legal_entity_name in grouped_units[business_group]:
            for division in grouped_units[business_group][legal_entity_name]:
                if business_group == "null":
                    business_group_name = None
                else:
                    business_group_name = business_group
                if division == "null":
                    division_name = None
                else:
                    division_name = division
                GroupedUnits.append(
                    technoreports.GroupedUnits(
                        division_name, legal_entity_name, business_group_name,
                        grouped_units[
                            business_group][legal_entity_name][division]
                    )
                )
    return GroupedUnits


def get_compliance_list_report_techno(
    db, country_id, domain_id, industry_id,
    statutory_nature_id, geography_id,
    level_1_statutory_id, frequency_id, user_id, from_count, to_count
):
    q_count = "SELECT  count(distinct t2.compliance_id) " + \
        " FROM tbl_statutory_mappings t1 " + \
        " INNER JOIN tbl_compliances t2 " + \
        " ON t2.statutory_mapping_id = t1.statutory_mapping_id " + \
        " INNER JOIN tbl_statutory_industry t3 " + \
        " ON t3.statutory_mapping_id = t1.statutory_mapping_id " + \
        " INNER JOIN tbl_statutory_geographies t4 " + \
        " ON t4.statutory_mapping_id = t1.statutory_mapping_id " + \
        " INNER JOIN tbl_user_domains t5 " + \
        " ON t5.domain_id = t1.domain_id " + \
        " and t5.user_id = %s " + \
        " INNER JOIN tbl_user_countries t6 " + \
        " ON t6.country_id = t1.country_id " + \
        " and t6.user_id = %s " + \
        " WHERE t1.approval_status in (1, 3) AND t2.is_active = 1 AND " + \
        " t1.country_id = %s " + \
        " and t1.domain_id = %s "
    q_order = "ORDER BY SUBSTRING_INDEX( " + \
        " SUBSTRING_INDEX(t1.statutory_mapping, '>>', 1), '>>', -1), " + \
        " t2.frequency_id "
    param_list = [
        int(user_id), int(user_id), country_id, domain_id
    ]

    qry_where = ""
    if industry_id is not None:
        qry_where += "AND t3.industry_id = %s "
        param_list.append(industry_id)

    if geography_id is not None:
        qry_where += "AND t4.geography_id = %s "
        param_list.append(geography_id)

    if statutory_nature_id is not None:
        qry_where += "AND t1.statutory_nature_id = %s "
        param_list.append(statutory_nature_id)

    if level_1_statutory_id is not None:
        qry_where += " AND t1.statutory_mapping LIKE ( " + \
            " select concat(statutory_name, %s) " + \
            " from tbl_statutories where statutory_id = %s)"
        param_list.extend([str("%"), level_1_statutory_id])

    if frequency_id is not None:
        qry_where += "AND t2.frequency_id = %s "
        param_list.append(frequency_id)

    query = q_count + qry_where + q_order
    row = db.select_one(query, param_list)
    if row:
        r_count = row[0]
    else:
        r_count = 0

    industry_qry = "select industry_name, statutory_mapping_id " + \
        " from tbl_statutory_industry si " + \
        " INNER JOIN tbl_industries i on " + \
        " i.industry_id = si.industry_id "
    industry_rows = db.select_all(industry_qry)
    industry_result = convert_to_dict(
        industry_rows, ["industry_name", "statutory_mapping_id"]
    )
    industry_statutory_mapping = {}
    for row in industry_result:
        statu_mapping_id = int(row["statutory_mapping_id"])
        if statu_mapping_id not in industry_statutory_mapping:
            industry_statutory_mapping[statu_mapping_id] = []
        industry_statutory_mapping[statu_mapping_id].append(
            row["industry_name"]
        )

    q = " SELECT distinct t1.statutory_mapping_id, t1.country_id, " + \
        " (select country_name from tbl_countries " + \
        " where country_id = t1.country_id) country_name, " + \
        " t1.domain_id, " + \
        " (select domain_name from tbl_domains " + \
        " where domain_id = t1.domain_id) domain_name, " + \
        " t1.industry_ids, t1.statutory_nature_id, " + \
        " (select statutory_nature_name from tbl_statutory_natures " + \
        " where statutory_nature_id = t1.statutory_nature_id) " + \
        " statutory_nature_name, " + \
        " t1.statutory_ids, " + \
        " t1.geography_ids, " + \
        " t1.approval_status, t1.is_active, t1.statutory_mapping, " + \
        " t2.compliance_id, t2.statutory_provision, " + \
        " t2.compliance_task, t2.compliance_description, " + \
        " t2.document_name, t2.format_file, t2.format_file_size, " +\
        " t2.penal_consequences, t2.frequency_id, " + \
        " t2.statutory_dates, t2.repeats_every, " + \
        " t2.repeats_type_id, " + \
        " t2.duration, t2.duration_type_id " + \
        " FROM tbl_statutory_mappings t1 " + \
        " INNER JOIN tbl_compliances t2 " + \
        " ON t2.statutory_mapping_id = t1.statutory_mapping_id " + \
        " INNER JOIN tbl_statutory_industry t3 " + \
        " ON t3.statutory_mapping_id = t1.statutory_mapping_id " + \
        " INNER JOIN tbl_statutory_geographies t4 " + \
        " ON t4.statutory_mapping_id = t1.statutory_mapping_id " + \
        " INNER JOIN tbl_user_domains t5 " + \
        " ON t5.domain_id = t1.domain_id " + \
        " and t5.user_id = %s " + \
        " INNER JOIN tbl_user_countries t6 " + \
        " ON t6.country_id = t1.country_id " + \
        " and t6.user_id = %s " + \
        " WHERE t1.approval_status in (1, 3) AND t2.is_active = 1 AND " + \
        " t1.country_id = %s " + \
        " and t1.domain_id = %s "

    q_order = "ORDER BY SUBSTRING_INDEX(SUBSTRING_INDEX( " + \
        " t1.statutory_mapping, '>>', 1), '>>', -1), " + \
        " t2.frequency_id " + \
        " limit %s, %s"
    param_list.extend([from_count, to_count])
    q += qry_where + q_order

    rows = db.select_all(q, param_list)
    columns = [
        "statutory_mapping_id", "country_id",
        "country_name", "domain_id", "domain_name", "industry_ids",
        "statutory_nature_id", "statutory_nature_name",
        "statutory_ids", "geography_ids",
        "approval_status", "is_active", "statutory_mapping",
        "compliance_id", "statutory_provision",
        "compliance_task", "compliance_description",
        "document_name", "format_file",
        "format_file_size", "penal_consequences",
        "frequency_id", "statutory_dates", "repeats_every",
        "repeats_type_id", "duration", "duration_type_id"
    ]
    print rows
    report_data = []
    if rows:
        report_data = convert_to_dict(rows, columns)

    return return_knowledge_report(
        db, report_data, industry_statutory_mapping, r_count
    )


def return_knowledge_report(
    db, report_data, industry_statutory_mapping, total_count=None
):
    if bool(GEOGRAPHY_PARENTS) is False:
        get_geographies(db)

    report_list = []
    for r in report_data:
        print
        print r
        print
        mapping = r["statutory_mapping"].split(">>")
        act_name = mapping[0].strip()
        statutory_provision = " >>".join(mapping[1:])
        statutory_provision += " " + r["statutory_provision"]
        compliance_task = r["compliance_task"]
        document_name = r["document_name"]
        if document_name == "None":
            document_name = None
        if document_name:
            name = "%s - %s" % (
                document_name, compliance_task
            )
        else:
            name = compliance_task

        format_file = r["format_file"]
        format_file_size = r["format_file_size"]
        if format_file_size is not None:
            format_file_size = int(format_file_size)
        if format_file:
            url = "%s/%s" % (
                KNOWLEDGE_FORMAT_DOWNLOAD_URL, format_file
            )
        else:
            url = None
        industry_names = ",".join(
            industry_statutory_mapping[r["statutory_mapping_id"]]
        )
        geography_ids = [
            int(x) for x in r["geography_ids"][:-1].split(',')
        ]
        geography_mapping_list = []
        for g_id in geography_ids:
            map_data = GEOGRAPHY_PARENTS.get(int(g_id))
            if map_data is not None:
                map_data = map_data[0]
            geography_mapping_list.append(map_data)

        statutory_dates = r["statutory_dates"]
        statutory_dates = json.loads(statutory_dates)
        date_list = []
        for date in statutory_dates:
            s_date = core.StatutoryDate(
                date["statutory_date"],
                date["statutory_month"],
                date["trigger_before_days"],
                date.get("repeat_by")
            )
            date_list.append(s_date)

        info = knowledgereport.StatutoryMappingReport(
            r["country_name"],
            r["domain_name"],
            industry_names,
            r["statutory_nature_name"],
            geography_mapping_list,
            r["approval_status"],
            bool(r["is_active"]),
            act_name,
            r["compliance_id"],
            statutory_provision,
            name,
            r["compliance_description"],
            r["penal_consequences"],
            r["frequency_id"],
            date_list,
            r["repeats_type_id"],
            r["repeats_every"],
            r["duration_type_id"],
            r["duration"],
            url
        )
        report_list.append(info)
    return report_list, total_count
