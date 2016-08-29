import json
import datetime
from dateutil import relativedelta
from protocol import (core, dashboard)
from server.constants import FORMAT_DOWNLOAD_URL
from server.emailcontroller import EmailHandler
from server.clientdatabase.tables import *
from server.clientdatabase.common import (
    get_last_7_years, get_country_domain_timelines,
    calculate_ageing_in_hours, calculate_years
)
from server.common import (
    get_date_time_in_date, convert_to_dict,
    datetime_to_string_time, datetime_to_string
)
from server.clientdatabase.general import (
    get_user_unit_ids, calculate_ageing, get_admin_id,
    get_user_domains, get_group_name, is_primary_admin,
    get_all_users
)
from server.clientdatabase.clienttransaction import (
    get_units_for_assign_compliance
)
from processes.expiry_report_generator import ExpiryReportGenerator as exp

email = EmailHandler()
__all__ = [
    "get_units_for_dashboard_filters",
    "get_compliance_status_chart",
    "get_trend_chart",
    "get_filtered_trend_data",
    "get_trend_chart_drill_down",
    "get_compliances_details_for_status_chart",
    "get_escalation_chart",
    "get_escalation_drill_down_data",
    "get_not_complied_chart",
    "get_not_complied_drill_down",
    "get_compliance_applicability_chart",
    "get_compliance_applicability_drill_down",
    "get_notifications",
    "update_notification_status",
    "get_user_company_details",
    "get_assigneewise_compliances_list",
    "get_assigneewise_yearwise_compliances",
    "get_assigneewise_reassigned_compliances",
    "get_assigneewise_compliances_drilldown_data",
    "get_assigneewise_compliances_drilldown_data_count",
    "get_no_of_days_left_for_contract_expiration",
    "need_to_display_deletion_popup",
    "get_client_compliance_count",
    "get_dashboard_notification_counts"
]


def get_units_for_dashboard_filters(db, session_user, is_closed=True):
    return get_units_for_assign_compliance(db, session_user, is_closed)


def get_status_wise_compliances_count(db, request, session_user):
    user_id = int(session_user)
    from_date = request.from_date
    to_date = request.to_date
    chart_year = request.chart_year

    filter_ids = []

    inprogress_qry = " AND ((IFNULL(T2.duration_type_id, 0) = 2 " + \
        " AND T1.due_date >= now()) " + \
        " or (IFNULL(T2.duration_type_id, 0) != 2 " + \
        " and T1.due_date >= CURDATE())) " + \
        " AND IFNULL(T1.approve_status,0) != 1"

    complied_qry = " AND T1.due_date >= T1.completion_date " + \
        " AND IFNULL(T1.approve_status,0) = 1"

    delayed_qry = " AND T1.due_date < T1.completion_date " + \
        " AND IFNULL(T1.approve_status,0) = 1"

    not_complied_qry = " AND ((IFNULL(T2.duration_type_id, 0) = 2 " + \
        " AND T1.due_date < now()) " + \
        " or (IFNULL(T2.duration_type_id, 0) != 2 " + \
        " and T1.due_date < CURDATE())) " + \
        " AND IFNULL(T1.approve_status,0) != 1"

    filter_ids, inprogress = get_compliance_status(
        db, inprogress_qry, request, user_id
        )
    filter_ids, complied = get_compliance_status(
        db, complied_qry, request, user_id
        )
    filter_ids, delayed = get_compliance_status(
        db, delayed_qry, request, user_id
        )
    filter_ids, not_complied = get_compliance_status(
        db, not_complied_qry, request, user_id
        )
    if from_date is not None and to_date is not None:
        return frame_compliance_status_count(
            db, inprogress, complied, delayed,
            not_complied
        )
    else:
        return frame_compliance_status_yearwise_count(
            db, inprogress, complied, delayed, not_complied,
            filter_ids, chart_year
        )


def get_compliance_status(
    db, status_type_qry,
    request, user_id, chart_type=None
):
    country_ids = request.country_ids

    if len(country_ids) == 1:
        country_ids.append(0)
    domain_ids = request.domain_ids

    if len(domain_ids) == 1:
        domain_ids.append(0)
    filter_type = request.filter_type

    # domain_ids = request.domain_ids
    filter_ids = request.filter_ids
    year_range_qry = ""
    where_qry = ""
    where_qry += status_type_qry
    where_qry_val = []
    if chart_type is None:
        from_date = request.from_date
        if from_date == "":
            from_date = None
        to_date = request.to_date
        if to_date == "":
            to_date = None
        chart_year = request.chart_year
        year_condition = get_client_domain_configuration(db, chart_year)[1]

        for i, y in enumerate(year_condition):
            if i == 0:
                year_range_qry = y
            else:
                year_range_qry += " OR %s " % (y)
        if len(year_condition) > 0:
            year_range_qry = " AND (%s) " % year_range_qry
        else:
            year_range_qry = ""
    else:
        from_date = None
        to_date = None

    where_qry += year_range_qry

    if filter_type == "Group":
        group_by_name = "T3.country_id"
        filter_type_ids = ""
        filter_ids = country_ids

    elif filter_type == "BusinessGroup":
        if len(filter_ids) == 1:
            filter_ids.append(0)
        group_by_name = "T3.business_group_id"
        filter_type_ids = " AND T3.business_group_id in %s "
        where_qry_val.append(tuple(filter_ids))
    elif filter_type == "LegalEntity":
        if len(filter_ids) == 1:
            filter_ids.append(0)
        group_by_name = "T3.legal_entity_id"
        filter_type_ids = " AND T3.legal_entity_id in %s "
        where_qry_val.append(tuple(filter_ids))

    elif filter_type == "Division":
        if len(filter_ids) == 1:
            filter_ids.append(0)
        group_by_name = "T3.division_id"
        filter_type_ids = " AND T3.division_id in %s "
        where_qry_val.append(tuple(filter_ids))

    elif filter_type == "Unit":
        if len(filter_ids) == 1:
            filter_ids.append(0)
        group_by_name = "T3.unit_id"
        filter_type_ids = " AND T3.unit_id in %s "
        where_qry_val.append(tuple(filter_ids))

    elif filter_type == "Consolidated":
        group_by_name = "T3.country_id"
        filter_type_ids = ""
        filter_ids = country_ids

    where_qry += filter_type_ids

    if is_primary_admin(db, user_id):
        user_qry = ""
    else:
        user_qry = " AND (T1.completed_by LIKE %s " + \
            " OR T1.concurred_by LIKE %s " + \
            " OR T1.approved_by LIKE %s) "
        where_qry += user_qry
        where_qry_val.extend([user_id, user_id, user_id])

    date_qry = ""
    if from_date is not None and to_date is not None:
        from_date = string_to_datetime(from_date)
        to_date = string_to_datetime(to_date)
        date_qry = " AND T1.due_date >= %s AND T1.due_date <= %s "
        where_qry += date_qry
        where_qry_val.extend([from_date, to_date])

    query = "SELECT %s, " + \
        " T3.country_id, " + \
        " T2.domain_id, " + \
        " YEAR(T1.due_date) as year, " + \
        " MONTH(T1.due_date) as month, " + \
        " count(1) as compliances " + \
        " FROM tbl_compliance_history T1  " + \
        " INNER JOIN tbl_compliances T2 " + \
        " ON T1.compliance_id = T2.compliance_id " + \
        " INNER JOIN tbl_units T3 " + \
        " ON T1.unit_id = T3.unit_id " + \
        " WHERE "
    query = query % (group_by_name)

    order = "GROUP BY month, year, T2.domain_id, %s " + \
        " ORDER BY month desc, year desc, %s "
    order = order % (group_by_name, group_by_name)

    where_qry1 = " T3.country_id IN %s " + \
        " AND T2.domain_id IN %s  " + where_qry

    param = [tuple(country_ids), tuple(domain_ids)]
    param.extend(where_qry_val)
    # # print query
    q = "%s %s %s" % (query, where_qry1, order)
    rows = db.select_all(q, param)
    columns = [
        "filter_type", "country_id", "domain_id",
        "year", "month", "compliances"
    ]
    return filter_ids, convert_to_dict(rows, columns)


def frame_compliance_status_count(
    db,
    inprogress, complied, delayed,
    not_complied
):
    calculated_data = {}

    def compliance_count(compliances, status):
        for i in compliances:
            filter_type = int(i["filter_type"])
            domain_id = int(i["domain_id"])
            domain_wise = calculated_data.get(filter_type)

            # domain_wise = country.get(domain_id)
            if domain_wise is None:
                domain_wise = {}

            compliance_count_info = domain_wise.get(domain_id)
            if compliance_count_info is None:
                compliance_count_info = {
                    "inprogress_count": 0,
                    "complied_count": 0,
                    "delayed_count": 0,
                    "not_complied_count": 0,
                }

            compliance_count_info[status] += int(i["compliances"])
            compliance_count_info["domain_id"] = i["domain_id"]
            compliance_count_info["country_id"] = i["country_id"]
            domain_wise[domain_id] = compliance_count_info
            calculated_data[filter_type] = domain_wise
        return calculated_data

    calculated_data = compliance_count(inprogress, "inprogress_count")
    calculated_data = compliance_count(complied, "complied_count")
    calculated_data = compliance_count(delayed, "delayed_count")
    calculated_data = compliance_count(not_complied, "not_complied_count")

    current_year = datetime.datetime.now().year
    filter_type_wise = {}
    for key, value in calculated_data.iteritems():
        domain_wise = {}
        compliance_list = []

        for k, v in value.iteritems():
            year = current_year
            inprogress = v["inprogress_count"]
            complied = v["complied_count"]
            delayed = v["delayed_count"]
            not_complied = v["not_complied_count"]
            country_id = v["country_id"]
            domain_id = v["domain_id"]
            if len(compliance_list) == 0:
                compliance_count = core.NumberOfCompliances(
                    domain_id, country_id, str(year), complied,
                    delayed, inprogress, not_complied
                )
                compliance_list.append(compliance_count)
            else:
                compliance_count = compliance_list[0]
                compliance_count.inprogress_compliance_count += v[0]
                compliance_count.complied_count += v[1]
                compliance_count.delayed_compliance_count += v[2]
                compliance_count.not_complied_count += v[3]

            domain_wise[k] = compliance_list
            compliance_list = []
        filter_type_wise[key] = domain_wise

    final_result_list = []
    for k, v in filter_type_wise.items():
        data_list = []
        for i, j in v.items():
            data_list.extend(j)
        chart = dashboard.ChartDataMap(k, data_list)
        final_result_list.append(chart)
    return final_result_list


def frame_compliance_status_yearwise_count(
    db,
    inprogress, complied, delayed,
    not_complied, filter_type_ids, current_year
):
    year_info = get_client_domain_configuration(db, current_year)[0]
    calculated_data = {}
    calculated_data = calculate_year_wise_count(
        db, calculated_data, year_info, inprogress, "inprogress",
        filter_type_ids
    )
    calculated_data = calculate_year_wise_count(
        db, calculated_data, year_info, complied, "complied",
        filter_type_ids
    )
    calculated_data = calculate_year_wise_count(
        db, calculated_data, year_info, delayed, "delayed",
        filter_type_ids
    )
    calculated_data = calculate_year_wise_count(
        db, calculated_data, year_info, not_complied, "not_complied",
        filter_type_ids
    )

    # Sum compliance for filter_type wise
    filter_type_wise = {}

    for filter_type, value in calculated_data.iteritems():
        domain_wise = {}
        for key, val in value.iteritems():
            compliance_list = []
            for k, v in val.iteritems():
                year = k
                inprogress = v["inprogress_count"]
                complied = v["complied_count"]
                delayed = v["delayed_count"]
                not_complied = v["not_complied_count"]
                country_id = v["country_id"]
                domain_id = v["domain_id"]
                compliance_count = core.NumberOfCompliances(
                    domain_id, country_id, str(year), complied,
                    delayed, inprogress, not_complied
                )
                compliance_list.append(compliance_count)
            domain_wise[key] = compliance_list
        filter_type_wise[filter_type] = domain_wise

    final_result_list = []
    for k, v in filter_type_wise.items():
        data_list = []
        for i, j in v.items():
            data_list.extend(j)
        chart = dashboard.ChartDataMap(k, data_list)
        final_result_list.append(chart)
    return final_result_list


def get_compliance_status_chart(db, request, session_user, client_id):
    result = get_status_wise_compliances_count(db, request, session_user)
    final = []
    filter_types = []
    for r in result:
        data = r.data
        for d in data:
            if (
                d.inprogress_compliance_count == 0 and
                d.not_complied_count == 0 and
                d.delayed_compliance_count == 0 and
                d.complied_count == 0
            ):
                pass
            else:
                if r.filter_type_id not in filter_types:
                    filter_types.append(r.filter_type_id)
                    final.append(r)

    return dashboard.GetComplianceStatusChartSuccess(final)


def get_trend_chart(db, country_ids, domain_ids, client_id):
    # import from common.py
    years = get_last_7_years()
    # import from common.py
    country_domain_timelines = get_country_domain_timelines(
        db, country_ids, domain_ids, years, client_id)
    chart_data = []
    count_flag = 0
    for country_wise_timeline in country_domain_timelines:
        country_id = country_wise_timeline[0]
        domain_wise_timelines = country_wise_timeline[1]
        year_wise_count = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        for domain_wise_timeline in domain_wise_timelines:
            domain_id = domain_wise_timeline[0]
            start_end_dates = domain_wise_timeline[1]
            (
                compliance_history_ids, client_statutory_ids, unit_ids
            ) = get_compliance_history_ids_for_trend_chart(
                db, country_id, domain_id, client_id
            )
            if compliance_history_ids not in [None, "None", ""]:
                for index, dates in enumerate(start_end_dates):
                    columns = "count(*) as total, sum(case " + \
                        " when approve_status = 1 then 1 " + \
                        "else 0 end) as complied"
                    condition = "due_date between '%s' and '%s' "
                    condition = condition % (
                        dates["start_date"], dates["end_date"]
                    )
                    condition += " and compliance_history_id in (%s)"
                    condition_val = [compliance_history_ids]
                    rows = db.get_data(
                        tblComplianceHistory, columns, condition, condition_val
                    )
                    if len(rows) > 0:
                        row = rows[0]
                        total_compliances = row["total"]
                        complied_compliances = row["complied"] if (
                            row["complied"] != None
                        ) else 0
                        year_wise_count[index][0] += int(total_compliances) if(
                            total_compliances is not None
                        ) else 0
                        year_wise_count[index][1] += int(
                                complied_compliances
                            ) if(
                                complied_compliances is not None
                            ) else 0
        compliance_chart_data = []
        for index, count_of_year in enumerate(year_wise_count):
            count_flag += int(count_of_year[0])
            compliance_chart_data.append(
                dashboard.CompliedMap(
                    year=years[index],
                    total_compliances=int(count_of_year[0]),
                    complied_compliances_count=int(count_of_year[1])
                ))
        chart_data.append(dashboard.TrendData(
            filter_id=country_id,
            complied_compliance=compliance_chart_data
        ))
    return years, chart_data, count_flag


def get_filtered_trend_data(
    db, country_ids, domain_ids, filter_type, filter_ids, client_id
):
    print "inside get_filtered_trend_data"
    # import from common.py
    years = get_last_7_years()
    # import from common.py
    country_domain_timelines = get_country_domain_timelines(
        db, country_ids, domain_ids, years, client_id)
    chart_data = []
    count_flag = 0
    for filter_id in filter_ids:
        year_wise_count = [
            [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]
        ]
        for country_wise_timeline in country_domain_timelines:
            country_id = country_wise_timeline[0]
            domain_wise_timelines = country_wise_timeline[1]
            for domain_wise_timeline in domain_wise_timelines:
                domain_id = domain_wise_timeline[0]
                start_end_dates = domain_wise_timeline[1]
                for index, dates in enumerate(start_end_dates):
                    columns = "count(*) as total, " + \
                        " sum(case when approve_status is null then 1 " + \
                        " else 0 end) as complied"
                    condition = "due_date between '{}' and '{}'".format(
                        dates["start_date"], dates["end_date"]
                    )
                    fn = get_compliance_history_ids_for_trend_chart
                    compliance_history_ids = fn(
                        db, country_id, domain_id, client_id,
                        filter_id, filter_type
                    )

                    if(
                        compliance_history_ids[0] is not None and
                        compliance_history_ids[2] is not None
                    ):
                        condition += " and compliance_history_id in (%s)"
                        condition += " and unit_id in (%s)"
                        condition_val = [
                            compliance_history_ids[0],
                            compliance_history_ids[2]
                        ]
                        rows = db.get_data(
                            tblComplianceHistory, columns,
                            condition, condition_val
                        )
                        if len(rows) > 0:
                            row = rows[0]
                            total_compliances = int(row[0])
                            complied_comp = int(row[1]) if (
                                row[1] != None) else 0
                            year_wise_count[index][0] += total_compliances if(
                                total_compliances is not None) else 0
                            year_wise_count[index][1] += complied_comp if(
                                complied_comp is not None) else 0
        compliance_chart_data = []
        for index, count_of_year in enumerate(year_wise_count):
            count_flag += int(count_of_year[0])
            compliance_chart_data.append(
                dashboard.CompliedMap(
                    year=years[index],
                    total_compliances=int(count_of_year[0]),
                    complied_compliances_count=int(count_of_year[1])
                ))
        chart_data.append(dashboard.TrendData(
            filter_id=filter_id,
            complied_compliance=compliance_chart_data
        ))
    return years, chart_data, count_flag


def get_trend_chart_drill_down(
    db, country_ids, domain_ids, filter_ids,
    filter_type, year, client_id
):
    # Getting Unit ids
    rows = None
    country_ids = ",".join(str(x) for x in country_ids)
    domain_ids = ",".join(str(x) for x in domain_ids)

    if filter_type == "Group":
        columns = ["DISTINCT unit_id as unit_id"]
        condition = "country_id in (%s) and domain_id in (%s)"
        condition_val = [
            country_ids, domain_ids
        ]
        rows = db.get_data(
            tblClientStatutories, columns, condition, condition_val
        )
    else:
        columns = "DISTINCT tcs.unit_id as unit_id"
        tables = [tblClientStatutories, tblUnits]
        aliases = ["tcs", "tu"]
        join_type = "left join "
        join_conditions = ["tcs.unit_id = tu.unit_id"]
        where_condition = "tu.country_id in (%s) and domain_id in (%s)" % (
            country_ids, domain_ids)
        if filter_type == "BusinessGroup":
            where_condition += " and business_group_id in(%s)" % filter_ids
        elif filter_type == "LegalEntity":
            where_condition += " and legal_entity_id in (%s)" % filter_ids
        elif filter_type == "Division":
            where_condition += " and  division_id in (%s) " % filter_ids
        elif filter_type == "Unit":
            where_condition += " and  tcs.unit_id in (%s) " % filter_ids
        rows = db.get_data_from_multiple_tables(
            columns, tables, aliases,
            join_type, join_conditions,
            where_condition
        )
    unit_ids = [
        int(row["unit_id"]) for row in rows
    ]
    drill_down_data = []
    for unit_id in unit_ids:
        # Getting Unit details
        unit_detail_columns = "tu.country_id, domain_ids, " + \
            " business_group_id, legal_entity_id, division_id, " + \
            " unit_code, unit_name, address"
        unit_detail_condition = "tu.unit_id = %s"
        unit_detail_condition_val = [unit_id]
        tables = "%s tu" % (
            tblUnits
        )
        unit_rows = db.get_data(
            tables, unit_detail_columns,
            unit_detail_condition, unit_detail_condition_val
        )
        unit_detail = unit_rows[0]
        business_group_id = unit_detail["business_group_id"]
        legal_entity_id = unit_detail["legal_entity_id"]
        division_id = unit_detail["division_id"]
        unit_name = "%s-%s" % (
            unit_detail["unit_code"], unit_detail["unit_name"]
        )
        address = unit_detail["address"]

        # Getting complied compliances for the given year
        years = [year]
        country_ids = [unit_detail["country_id"]]
        domain_ids = unit_detail["domain_ids"].split(",")
        # import from common.py
        timelines = get_country_domain_timelines(
            db, country_ids, domain_ids, years, client_id
        )
        domain_wise_timelines = timelines[0][1] if len(timelines) > 0 else []
        for domain_wise_timeline in domain_wise_timelines:
            domain_id = domain_wise_timeline[0]
            start_end_dates = domain_wise_timeline[1][0]
            start_date = start_end_dates["start_date"]
            end_date = start_end_dates["end_date"]

            # Getting compliances relevent to unit, country, domain
            compliance_columns = ["distinct compliance_id as comp_id"]
            compliance_condition = "compliance_opted = 1"
            compliance_condition += " and client_statutory_id in ( " + \
                " select client_statutory_id from %s "
            compliance_condition = compliance_condition % tblClientStatutories
            compliance_condition += " where unit_id = %s and domain_id = %s)"
            compliance_condition_val = [
                int(unit_id), int(domain_id)
            ]
            compliance_rows = db.get_data(
                tblClientCompliances, compliance_columns,
                compliance_condition, compliance_condition_val
            )
            compliance_ids_list = [
                int(row["comp_id"]) for row in compliance_rows
            ]
            compliance_ids = ",".join(str(x) for x in compliance_ids_list)
            if compliance_ids is not None:
                history_columns = "tch.compliance_id, tu.employee_code, "
                history_columns += "tu.employee_name, tc.compliance_task,"
                history_columns += " tc.compliance_description, "
                history_columns += " tc.document_name,"
                history_columns += "tc.compliance_description, "
                history_columns += "tc.statutory_mapping"
                history_condition = "due_date between '%s' and '%s'" % (
                    start_date, end_date
                )
                history_condition += " and tch.compliance_id in (%s)" % (
                    compliance_ids
                )
                history_condition += " and tch.unit_id = %s" % (
                    unit_id
                )
                tables = [
                    tblComplianceHistory,
                    tblUsers, tblCompliances
                ]
                aliases = ["tch", "tu", "tc"]
                join_type = "left join"
                join_condition = [
                    "tch.completed_by = tu.user_id",
                    "tch.compliance_id = tc.compliance_id"
                ]
                history_rows = db.get_data_from_multiple_tables(
                    history_columns, tables, aliases,
                    join_type, join_condition,
                    history_condition,
                )
                level_1_statutory_wise_compliances = {}
                for history_row in history_rows:
                    assignee_name = "%s-%s" % (history_row[1], history_row[2])
                    compliance_name = "%s-%s" % (
                        history_row[5], history_row[3]
                    )
                    description = history_row[4]
                    statutories = history_row[7].split(">>")
                    level_1_statutory = statutories[0]
                    if(
                        level_1_statutory not in
                        level_1_statutory_wise_compliances
                    ):
                        level_1_statutory_wise_compliances[
                            level_1_statutory
                        ] = []
                    level_1_statutory_wise_compliances[
                        level_1_statutory
                    ].append(dashboard.TrendCompliance(
                        compliance_name, description, assignee_name
                        )
                    )
        if len(level_1_statutory_wise_compliances) > 0:
            business_group_name = None
            legal_entity_name = None
            division_name = None
            if business_group_id is not None:
                rows = db.get_data(
                    tblBusinessGroups, "business_group_name",
                    "business_group_id=%s", [business_group_id]
                )
                if rows:
                    business_group_name = rows[0][0]
            if division_id is not None:
                rows = db.get_data(
                    tblDivisions, "division_name",
                    "division_id=%s", [division_id]
                )
                if rows:
                    division_name = rows[0][0]
            rows = db.get_data(
                tblLegalEntities, "legal_entity_name",
                "legal_entity_id=%s", [legal_entity_id]
            )
            if rows:
                legal_entity_name = rows[0][0]

            drill_down_data.append(
                dashboard.TrendDrillDownData(
                        business_group_name,
                        legal_entity_name, division_name,
                        unit_name, address,
                        level_1_statutory_wise_compliances
                    )
                )
    return drill_down_data


def get_compliances_details_for_status_chart(
    db, request, session_user, client_id, from_count, to_count
):
    year = request.year
    compliance_status = request.compliance_status
    chart_type = "compliance_status"

    result = compliance_details_query(
        db, request, chart_type, compliance_status,
        from_count, to_count, session_user, year
    )
    year_info = get_client_domain_configuration(db, int(year))[0]
    return return_compliance_details_drill_down(
        year_info, compliance_status, request.year, result, client_id
    )


def frame_compliance_details_query(
    db, chart_type, compliance_status, request,
    from_count, to_count, user_id, chart_year=None
):
    domain_ids = request.domain_ids
    filter_type = request.filter_type
    if chart_type == "compliance_status":
        from_date = request.from_date
        to_date = request.to_date
        filter_id = request.filter_id
    else:
        filter_id = request.filter_ids
        from_date = None
        to_date = None

    if len(domain_ids) == 1:
        domain_ids.append(0)

    if chart_year is not None :
        year_condition = get_client_domain_configuration(db, chart_year)[1]

        for i, y in enumerate(year_condition):
            if i == 0:
                year_range_qry = y
            else:
                year_range_qry += " OR %s " % (y)
        if len(year_condition) > 0:
            year_range_qry = " AND (%s) " % year_range_qry
        else :
            year_range_qry = ""
    else:
        year_range_qry = ""

    where_qry = ""
    where_qry_val = []
    if compliance_status == "Inprogress":
        where_qry = " AND ((IFNULL(T2.duration_type_id,0) = 2 " + \
            " AND T1.due_date >= now()) " + \
            " or (IFNULL(T2.duration_type_id, 0) != 2  " + \
            " AND T1.due_date >= CURDATE())) " + \
            " AND IFNULL(T1.approve_status, 0) != 1"

    elif compliance_status == "Complied":
        where_qry = " AND T1.due_date >= T1.completion_date " + \
            " AND T1.approve_status = 1"

    elif compliance_status == "Delayed Compliance":
        where_qry = " AND T1.due_date < T1.completion_date " + \
            " AND T1.approve_status = 1"

    elif compliance_status == "Not Complied":
        where_qry = " AND ((IFNULL(T2.duration_type_id,0) =2 " + \
            " AND T1.due_date < now()) " + \
            " or (IFNULL(T2.duration_type_id,0) != 2 " + \
            " AND T1.due_date < CURDATE())) " + \
            " AND IFNULL(T1.approve_status, 0) != 1 "

    if filter_type == "Group":
        where_qry += " AND T3.country_id "

    elif filter_type == "BusinessGroup":
        where_qry += " AND T3.business_group_id "

    elif filter_type == "LegalEntity":
        where_qry += " AND T3.legal_entity_id "

    elif filter_type == "Division":
        where_qry += " AND T3.division_id "

    elif filter_type == "Unit":
        where_qry += " AND T3.unit_id "

    if chart_type != "compliance_status":
        if len(filter_id) == 1:
            filter_id.append(0)
        where_qry += " IN %s "
        where_qry_val.append(tuple(filter_id))
    else:
        where_qry += " = %s "
        where_qry_val.append(filter_id)

    if chart_type == "not_complied":
        not_complied_type = request.not_complied_type

        if not_complied_type == "Below 30":
            where_qry += " AND abs(datediff(date(now()), " + \
                " date(T1.due_date))) <= 30 "
        elif not_complied_type == "Below 60":
            where_qry += " AND abs(datediff(date(now()), " + \
                " date(T1.due_date))) BETWEEN 30 and 60 "
        elif not_complied_type == "Below 90":
            if ageing > 60 and ageing <= 90:
                where_qry += " AND abs(datediff(date(now())," + \
                    " date(T1.due_date))) BETWEEN 60 and 90 "
        else:
            where_qry += " AND abs(datediff(date(now()), " + \
                " date(T1.due_date))) > 90 "

    if from_date is not None and to_date is not None:
        from_date = string_to_datetime(from_date)
        to_date = string_to_datetime(to_date)
        where_qry += " AND T1.due_date >= %s AND T1.due_date <= %s "
        where_qry_val.extend([from_date, to_date])

    if is_primary_admin(db, user_id) is False:
        where_qry += " AND (T1.completed_by LIKE %s " + \
            " OR T1.concurred_by LIKE %s " + \
            " OR T1.approved_by LIKE %s)"
        where_qry_val.extend([user_id, user_id, user_id])

    where_qry += year_range_qry

    query = "SELECT " + \
        " T1.compliance_history_id, T1.unit_id, " + \
        " T1.compliance_id, T1.start_date, " + \
        " T1.due_date, T1.completion_date, " + \
        " T1.completed_by, " + \
        " T2.compliance_task, T2.document_name, " + \
        " T2.compliance_description, T2.statutory_mapping, " + \
        " T2.frequency_id, T2.duration_type_id, " + \
        " unit_name, " + \
        " (select division_name from tbl_divisions " + \
        " where division_id = T3.division_id)division_name, " + \
        " (select legal_entity_name from tbl_legal_entities " + \
        " where legal_entity_id = T3.legal_entity_id)legal_entity_name, " + \
        " (select business_group_name from tbl_business_groups " + \
        " where business_group_id = T3.business_group_id) " + \
        " business_group_name, " + \
        " (select country_name from tbl_countries " + \
        " where country_id = T3.country_id)country_name, " + \
        " (select employee_name from tbl_users " + \
        " where user_id = T1.completed_by) employee_name, " + \
        " T3.unit_code, T3.address, T3.geography, T3.postal_code, " + \
        " T3.industry_name, T3.country_id, " + \
        " T2.domain_id, " + \
        " YEAR(T1.due_date) as year, " + \
        " MONTH(T1.due_date) as month " + \
        " FROM tbl_compliance_history T1 " + \
        " INNER JOIN tbl_compliances T2 " + \
        " ON T1.compliance_id = T2.compliance_id " + \
        " INNER JOIN tbl_units T3 ON T1.unit_id = T3.unit_id " + \
        " WHERE " + \
        " T2.domain_id IN %s "

    order = " ORDER BY  T1.unit_id, " + \
            " SUBSTRING_INDEX(SUBSTRING_INDEX( " + \
            " T2.statutory_mapping, '>>', 1), '>>', -1), " + \
            " T1.due_date " + \
            " limit %s, %s "

    where_qry_val.extend([from_count, to_count])
    q = "%s %s %s " % (query, where_qry, order)
    param = [tuple(domain_ids)]
    param.extend(where_qry_val)
    rows = db.select_all(q, param)
    return rows


def compliance_details_query(
    db, data, chart_type, compliance_status, from_count, to_count, user_id, chart_year
):
    rows = frame_compliance_details_query(
        db, chart_type, compliance_status, data, from_count, to_count, user_id, chart_year
    )
    columns = [
        "compliance_history_id", "unit_id",
        "compliance_id", "start_date", "due_date",
        "completion_date", "assignee", "compliance_task",
        "document_name", "compliance_description",
        "statutory_mapping", "frequency_id", "duration_type_id",
        "unit_name", "division_name",
        "legal_entity_name", "business_group_name",
        "country_name", "employee_name",
        "unit_code", "address", "geography",
        "postal_code", "industry_name",
        "country_id", "domain_id",
        "year", "month"
    ]
    result = convert_to_dict(rows, columns)
    return result


def get_client_domain_configuration(
    db, current_year=None
):
    query = "SELECT country_id, domain_id, " + \
        " period_from, period_to " + \
        " FROM  tbl_client_configurations "

    rows = db.select_all(query)
    columns = ["country_id", "domain_id", "period_from", "period_to"]
    data = convert_to_dict(rows, columns)
    years_range = []
    year_condition = []
    cond = "(T3.country_id = %s " + \
        "  AND T2.domain_id = %s " + \
        " AND YEAR(T1.due_date) IN %s)"
    for d in data:
        info = {}
        country_id = int(d["country_id"])
        domain_id = int(d["domain_id"])
        info["country_id"] = country_id
        info["domain_id"] = domain_id
        year_list = calculate_years(int(d["period_from"]), int(d["period_to"]))
        years_list = []
        if current_year is None:
            years_list = year_list
        else:
            for y in year_list:
                if current_year == y[0]:
                    years_list.append(y)
                    if len(y) == 1:
                        y.append(0)
                    year_condition.append(
                        cond % (country_id, domain_id, str(tuple(y)))
                    )
        if len(years_list) == 0:
            info["years"] = []
        else:
            info["years"] = years_list
        info["period_from"] = int(d["period_from"])
        info["period_to"] = int(d["period_to"])
        years_range.append(info)
    return (years_range, year_condition)


def return_compliance_details_drill_down(
    year_info, compliance_status, request_year, result, client_id
):
    current_date = datetime.datetime.today()
    unit_wise_data = {}
    for r in result:
        country_id = int(r["country_id"])
        domain_id = int(r["domain_id"])
        saved_year = int(r["year"])
        saved_month = int(r["month"])

        years_list = []
        month_from = 0
        month_to = 0
        for y in year_info:
            if(
                country_id == int(y["country_id"]) and
                domain_id == int(y["domain_id"])
            ):
                years = y["years"]
                month_from = int(y["period_from"])
                month_to = int(y["period_to"])
                for i in years:
                    # year = 0
                    if type(i) is int and i == int(request_year):
                        years_list = [i]
                    elif type(i) is list:
                        if i[0] == int(request_year):
                            years_list = i
                break

        if saved_year not in years_list:
            continue
        else:
            if len(years_list) == 2:
                if (
                    saved_year == years_list[0] and
                    saved_month not in [x for x in range(month_from, 12+1)]
                ):
                    continue
                elif (
                    saved_year == years_list[1] and
                    saved_month not in [x for x in range(1, month_to+1)]
                ):
                    continue

        unit_id = int(r["unit_id"])
        statutories = r["statutory_mapping"].split('>>')
        level_1 = statutories[0].strip()
        ageing = 0
        due_date = r["due_date"]
        completion_date = r["completion_date"]

        if compliance_status == "Inprogress":
            if r["frequency_id"] != 4:
                ageing = abs((due_date.date() - current_date.date()).days) + 1
            else:
                diff = (due_date - current_date)
                if r["duration_type_id"] == 2:
                    ageing = calculate_ageing_in_hours(diff)
                else:
                    ageing = diff.days
        elif compliance_status == "Complied":
            ageing = 0
        elif compliance_status == "Not Complied":
            if r["frequency_id"] != 4:
                ageing = abs((current_date.date() - due_date.date()).days) + 1
            else:
                diff = (current_date - due_date)
                if r["duration_type_id"] == 2:
                    ageing = calculate_ageing_in_hours(diff)
                else:
                    ageing = diff.days
        elif compliance_status == "Delayed Compliance":
            ageing = abs((completion_date - due_date).days) + 1
            if r["frequency_id"] != 4:
                ageing = abs((completion_date - due_date).days) + 1
            else:
                diff = (completion_date - due_date)
                if r["duration_type_id"] == 2:
                    ageing = calculate_ageing_in_hours(diff)
                else:
                    ageing = diff.days

        if type(ageing) is int:
            ageing = " %s Day(s)" % ageing

        status = core.COMPLIANCE_STATUS(compliance_status)
        if r["document_name"] not in ("", "None", None):
            name = "%s-%s" % (r["document_name"], r["compliance_task"])
        else:
            name = r["compliance_task"]
        if r["employee_name"] is None:
            employee_name = "Administrator"
        else:
            employee_name = r["employee_name"]
        compliance = dashboard.Level1Compliance(
            name, r["compliance_description"], employee_name,
            str(r["start_date"]), str(due_date),
            str(completion_date), status,
            str(ageing)
        )

        drill_down_data = unit_wise_data.get(unit_id)
        if drill_down_data is None:
            level_compliance = {}
            level_compliance[level_1] = [compliance]
            unit_name = "%s-%s" % (r["unit_code"], r["unit_name"])
            geography = r["geography"].split(">>")
            geography.reverse()
            geography = ','.join(geography)
            address = "%s, %s, %s" % (
                r["address"], geography, r["postal_code"]
            )
            drill_down_data = dashboard.DrillDownData(
                r["business_group_name"], r["legal_entity_name"],
                r["division_name"], unit_name, address,
                r["industry_name"],
                level_compliance
            )

        else:
            level_compliance = drill_down_data.compliances
            compliance_list = level_compliance.get(level_1)
            if compliance_list is None:
                compliance_list = []
            compliance_list.append(compliance)

            level_compliance[level_1] = compliance_list
            drill_down_data.compliances = level_compliance

        unit_wise_data[unit_id] = drill_down_data

    return unit_wise_data


#
# Escalation chart
#
def get_escalation_chart(db, request, session_user, client_id):
    user_id = int(session_user)

    filter_type = request.filter_type

    delayed_qry = " AND T1.due_date < T1.completion_date " + \
        " AND T1.approve_status = 1 "

    not_complied_qry = " AND ((IFNULL(T2.duration_type_id, 0) =2 " + \
        " AND T1.due_date < now()) " + \
        " or (IFNULL(T2.duration_type_id, 0) != 2 " + \
        " and T1.due_date < CURDATE())) " + \
        " AND IFNULL(T1.approve_status,0) <> 1 "

    chart_type = "Escalation"
    filter_ids, delayed = get_compliance_status(
        db, delayed_qry, request, user_id, chart_type
    )
    filter_ids, not_complied = get_compliance_status(
        db, not_complied_qry, request, user_id, chart_type
    )

    year_info = get_client_domain_configuration(db)[0]
    calculated_data = {}
    calculated_data = calculate_year_wise_count(
        db, calculated_data, year_info, delayed,
        "delayed", filter_ids
    )
    calculated_data = calculate_year_wise_count(
        db, calculated_data, year_info, not_complied,
        "not_complied", filter_ids
    )

    # Sum compliance for filter_type wise
    escalation_years = {}

    filter_ids = request.filter_ids

    for filter_type, value in calculated_data.iteritems():
        if filter_type not in filter_ids:
            continue
        for key, val in value.iteritems():
            for k, v in val.iteritems():
                year = k
                delayed = v["delayed_count"]
                not_complied = v["not_complied_count"]

                count_det = escalation_years.get(year)
                if count_det is None:
                    count_det = dashboard.EscalationData(
                        year,
                        delayed,
                        not_complied
                    )

                else:
                    count_det.delayed_compliance_count += int(delayed)
                    count_det.not_complied_count += int(not_complied)

                escalation_years[year] = count_det

    years = escalation_years.keys()
    years.sort()
    chart_data = []
    for y in years:
        chart_data.append(
            escalation_years.get(y)
        )
    return dashboard.GetEscalationsChartSuccess(
        years, chart_data
    )


def get_user_business_group_ids(db, user_id):
    columns = "distinct business_group_id as b_id"
    table = tblUnits
    rows = db.get_data(table, columns, "1")
    result = [
        int(row["b_id"]) for row in rows
    ]
    return ",".join(str(x) for x in result)


def get_user_legal_entity_ids(db, user_id):
    columns = "distinct legal_entity_id as l_id"
    table = tblUnits
    rows = db.get_data(
        table, columns, "1"
    )
    result = [
        int(row["l_id"]) for row in rows
    ]
    return ",".join(str(x) for x in result)


def get_user_division_ids(db, user_id):
    columns = "distinct division_id as d_id"
    table = tblUnits
    rows = db.get_data(
        table, columns, "1"
    )
    result = [
        int(row["d_id"]) for row in rows
    ]
    return ",".join(str(x) for x in result)


def calculate_year_wise_count(
    db,
    calculated_data, years_info, compliances,
    status, filter_ids
):
    for f in filter_ids:
        if f == 0:
            continue
        filter_type = int(f)
        for y in years_info:

            country_id = y["country_id"]

            domain_id = y["domain_id"]

            country = calculated_data.get(filter_type)
            if country is None:
                country = {}

            years_range = y["years"]

            year_wise = country.get(domain_id)

            if year_wise is None:
                year_wise = {}

            period_from = int(y["period_from"])
            period_to = int(y["period_to"])
            for index, i in enumerate(years_range):
                compliance_count_info = year_wise.get(i[0])
                if compliance_count_info is None:
                    compliance_count_info = {
                        "inprogress_count": 0,
                        "complied_count": 0,
                        "delayed_count": 0,
                        "not_complied_count": 0,
                        "country_id": country_id,
                        "domain_id": domain_id
                    }
                compliance_count = 0
                for c in compliances:
                    if int(c["year"]) not in (i):
                        continue
                    if (
                        filter_type == int(c["filter_type"]) and
                        country_id == int(c["country_id"]) and
                        domain_id == int(c["domain_id"])
                    ):
                        month = int(c["month"])

                        if len(i) == 2:
                            if (
                                c["year"] == i[0] and
                                month in [
                                    int(x) for x in range(period_from, 12+1)
                                ]
                            ):
                                compliance_count += int(c["compliances"])

                            elif (
                                c["year"] == i[1] and
                                month in [
                                    int(y) for y in range(1, period_to+1)
                                ]
                            ):
                                compliance_count += int(c["compliances"])

                        else:
                            if (
                                int(c["year"]) == i[0] and
                                month in [
                                    int(x) for x in range(
                                        period_from, period_to + 1
                                    )
                                ]
                            ):
                                compliance_count += int(c["compliances"])

                        compliance_count_info["domain_id"] = c["domain_id"]
                        compliance_count_info["country_id"] = c["country_id"]

                if status == "inprogress":
                    compliance_count_info[
                        "inprogress_count"
                    ] += compliance_count
                elif status == "complied":
                    compliance_count_info["complied_count"] += compliance_count
                elif status == "delayed":
                    compliance_count_info["delayed_count"] += compliance_count
                elif status == "not_complied":
                    compliance_count_info[
                        "not_complied_count"
                    ] += compliance_count

                year_wise[i[0]] = compliance_count_info

            country[domain_id] = year_wise
            calculated_data[filter_type] = country

    return calculated_data


def get_escalation_drill_down_data(
    db, request, session_user, client_id, from_count, to_count
):
    year = request.year
    year_info = get_client_domain_configuration(db)[0]

    chart_type = "excalation"
    compliance_status = "Delayed Compliance"
    delayed_details = compliance_details_query(
        db, request, chart_type, compliance_status,
        from_count, to_count, session_user, year
    )

    delayed_details_list = return_compliance_details_drill_down(
        year_info, compliance_status, year,
        delayed_details, client_id
    )

    compliance_status = "Not Complied"
    not_complied_details = compliance_details_query(
        db, request, chart_type, compliance_status,
        from_count, to_count, session_user, year
    )

    not_complied_details_list = return_compliance_details_drill_down(
        year_info, compliance_status, year,
        not_complied_details, client_id
    )

    return [delayed_details_list.values(), not_complied_details_list.values()]


#
# Not Complied chart
#
def get_not_complied_chart(db, request, session_user, client_id):
    user_id = int(session_user)
    country_ids = request.country_ids
    if len(country_ids) == 1:
        country_ids.append(0)
    domain_ids = request.domain_ids
    if len(domain_ids) == 1:
        domain_ids.append(0)
    filter_type = request.filter_type
    _filter_ids = request.filter_ids
    if len(_filter_ids) == 1:
        _filter_ids.append(0)

    filter_type_ids = ""
    where_qry_val = []
    if filter_type == "Group":
        pass

    elif filter_type == "BusinessGroup":
        filter_type_ids = "AND T4.business_group_id IN %s"
        where_qry_val.append(tuple(_filter_ids))

    elif filter_type == "LegalEntity":
        filter_type_ids = "AND T4.legal_entity_id IN %s"
        where_qry_val.append(tuple(_filter_ids))

    elif filter_type == "Division":
        filter_type_ids = "AND T4.division_id IN %s"
        where_qry_val.append(tuple(_filter_ids))

    elif filter_type == "Unit":
        filter_type_ids = "AND T4.unit_id IN %s"
        where_qry_val.append(tuple(_filter_ids))

    query = "SELECT T1.compliance_history_id, T1.unit_id, " + \
        " T1.compliance_id, T1.start_date, T1.due_date, " + \
        " T4.business_group_id, T4.legal_entity_id, T4.division_id " + \
        " FROM tbl_compliance_history T1 " + \
        " INNER JOIN tbl_client_compliances T2 " + \
        " ON T1.compliance_id = T2.compliance_id " + \
        " INNER JOIN tbl_client_statutories T3 " + \
        " ON T2.client_statutory_id = T3.client_statutory_id " + \
        " AND T1.unit_id = T3.unit_id " + \
        " INNER JOIN tbl_units T4 " + \
        " ON T1.unit_id = T4.unit_id " + \
        " WHERE T3.country_id IN %s " + \
        " AND T3.domain_id IN %s " + \
        " AND T1.due_date < CURDATE() " + \
        " AND IFNULL(T1.approve_status, 0) != 1 "
    query += filter_type_ids
    param = [tuple(country_ids), tuple(domain_ids)]

    if is_primary_admin(db, user_id) is True:
        query += ""
    else:
        query += " AND (T1.completed_by LIKE %s " + \
            " OR T1.concurred_by LIKE %s " + \
            " OR T1.approved_by LIKE %s) "
        where_qry_val.extend([user_id, user_id, user_id])

    param.extend(where_qry_val)

    order = "ORDER BY T1.due_date "
    rows = db.select_all("%s %s" % (query, order), param)
    columns = [
        "compliance_history_id", "unit_id", "compliance_id",
        "start_date", "due_date", "business_group_id",
        "legal_entity_id", "division_id"
    ]
    not_complied = convert_to_dict(rows, columns)
    current_date = datetime.datetime.today()
    below_30 = 0
    below_60 = 0
    below_90 = 0
    above_90 = 0

    for i in not_complied:
        if filter_type == "BusinessGroup":
            if i["business_group_id"] == 0:
                continue
            if i["business_group_id"] not in request.filter_ids:
                continue
        elif filter_type == "LegalEntity":
            if i["legal_entity_id"] == 0:
                continue
            if i["legal_entity_id"] not in request.filter_ids:
                continue
        elif filter_type == "Division":
            if i["division_id"] == 0:
                continue
            if i["division_id"] not in request.filter_ids:
                continue
        elif filter_type == "Unit":
            if i["unit_id"] == 0:
                continue
            if i["unit_id"] not in request.filter_ids:
                continue

        due_date = i["due_date"]
        if due_date is None:
            continue
        ageing = abs((current_date - due_date).days)
        if ageing <= 30:
            below_30 += 1
        elif ageing > 30 and ageing <= 60:
            below_60 += 1
        elif ageing > 60 and ageing <= 90:
            below_90 += 1
        else:
            above_90 += 1

    return dashboard.GetNotCompliedChartSuccess(
        below_30, below_60,
        below_90, above_90
    )


def get_not_complied_drill_down(
    db, request, session_user, client_id, from_count, to_count
):
    chart_type = "not_complied"
    compliance_status = "Not Complied"
    not_complied_details_filtered = compliance_details_query(
        db, request, chart_type, compliance_status,
        from_count, to_count, session_user , year=None
    )
    current_date = datetime.datetime.today()
    unit_wise_data = {}
    for r in not_complied_details_filtered:

        unit_id = int(r["unit_id"])
        statutories = r["statutory_mapping"].split('>>')
        level_1 = statutories[0].strip()
        ageing = 0
        due_date = r["due_date"]
        completion_date = r["completion_date"]

        if r["frequency_id"] != 4:
                ageing = abs((current_date - due_date).days) + 1
        else:
            diff = (current_date - due_date)
            if r["duration_type_id"] == 2:
                ageing = calculate_ageing_in_hours(diff)
            else:
                ageing = diff.days

        if type(ageing) is int:
            ageing = " %s Day(s)" % ageing

        status = core.COMPLIANCE_STATUS("Not Complied")
        name = "%s-%s" % (r["document_name"], r["compliance_task"])
        compliance = dashboard.Level1Compliance(
            name, r["compliance_description"], r["employee_name"],
            str(r["start_date"]), str(due_date),
            str(completion_date), status,
            str(ageing)
        )

        drill_down_data = unit_wise_data.get(unit_id)
        if drill_down_data is None:
            level_compliance = {}
            level_compliance[level_1] = [compliance]
            unit_name = "%s-%s" % (r["unit_code"], r["unit_name"])
            geography = r["geography"].split(">>")
            geography.reverse()
            geography = ','.join(geography)
            address = "%s, %s, %s" % (
                r["address"], geography, r["postal_code"]
            )
            drill_down_data = dashboard.DrillDownData(
                r["business_group_name"], r["legal_entity_name"],
                r["division_name"], unit_name, address,
                r["industry_name"],
                level_compliance
            )

        else:
            level_compliance = drill_down_data.compliances
            compliance_list = level_compliance.get(level_1)
            if compliance_list is None:
                compliance_list = []
            compliance_list.append(compliance)

            level_compliance[level_1] = compliance_list
            drill_down_data.compliances = level_compliance

        unit_wise_data[unit_id] = drill_down_data

    return unit_wise_data


#
# Compliance Applicability Chart
#
def get_compliance_applicability_chart(
    db, request, session_user, client_id
):
    query = "SELECT T1.compliance_id, " + \
        " T1.statutory_applicable, T1.statutory_opted, " + \
        " T1.not_applicable_remarks, " + \
        " T1.compliance_applicable, T1.compliance_opted, " + \
        " T1.compliance_remarks " + \
        " FROM tbl_client_compliances T1 " + \
        " INNER JOIN tbl_client_statutories T2 " + \
        " ON T1.client_statutory_id = T2.client_statutory_id " + \
        " INNER JOIN tbl_units T3 " + \
        " ON T2.unit_id = T3.unit_id " + \
        " WHERE T2.country_id IN %s " + \
        " AND T2.domain_id IN %s "

    country_ids = request.country_ids
    if len(country_ids) == 1:
        country_ids.append(0)
    domain_ids = request.domain_ids
    if len(domain_ids) == 1:
        domain_ids.append(0)
    filter_type = request.filter_type
    filter_id = request.filter_ids
    if len(filter_id) == 1:
        filter_id.append(0)

    param = [
        tuple(country_ids), tuple(domain_ids),
    ]
    filter_type_qry = ""
    if filter_type == "Group":
        # filter_type_qry = "AND T3.country_id
        # IN %s" % (str(tuple(filter_ids)))
        pass

    elif filter_type == "BusinessGroup":
        filter_type_qry = "AND T3.business_group_id IN %s"
        param.append(tuple(filter_id))

    elif filter_type == "LegalEntity":
        filter_type_qry = "AND T3.legal_entity_id IN %s"
        param.append(tuple(filter_id))

    elif filter_type == "Division":
        filter_type_qry = "AND T3.division_id IN %s"
        param.append(tuple(filter_id))

    elif filter_type == "Unit":
        filter_type_qry = "AND T3.unit_id IN %s"
        param.append(tuple(filter_id))

    query1 = query + filter_type_qry

    rows = db.select_all(query1, param)

    columns = [
        "compliance_id", "statutory_applicable",
        "statutory_opted", "not_applicable_remarks",
        "compliance_applicable", "compliance_opted",
        "compliance_remarks"
    ]
    result = convert_to_dict(rows, columns)

    applicable_count = 0
    not_applicable_count = 0
    not_opted_count = 0

    for r in result:
        if r["compliance_opted"] == 1:
            applicable_count += 1
        elif r["compliance_opted"] == 0:
            if r["compliance_applicable"] == 0:
                not_applicable_count += 1
            else:
                not_opted_count += 1

    return dashboard.GetComplianceApplicabilityStatusChartSuccess(
        applicable_count, not_applicable_count, not_opted_count
    )


def get_compliance_applicability_drill_down(
    db, request, session_user, client_id, from_count, to_count
):
    query = "SELECT T1.compliance_id, T2.unit_id, T4.frequency_id, " + \
        " (select frequency from tbl_compliance_frequency " + \
        " where frequency_id = T4.frequency_id) frequency, " + \
        " (select repeat_type from tbl_compliance_repeat_type " + \
        " where repeat_type_id = T4.repeats_type_id) repeats_type, " + \
        " (select duration_type from tbl_compliance_duration_type " + \
        " where duration_type_id = T4.duration_type_id)duration_type, " + \
        " T4.statutory_mapping, T4.statutory_provision, " + \
        " T4.compliance_task, T4.compliance_description, " + \
        " T4.document_name, T4.format_file, T4.format_file_size, " + \
        " T4.penal_consequences, T4.statutory_dates, " + \
        " T4.repeats_every, T4.duration, T4.is_active, " + \
        " (select concat(unit_code, ' - ', unit_name) " + \
        " from tbl_units where unit_id =  T3.unit_id) " + \
        " FROM tbl_client_compliances T1 " + \
        " INNER JOIN tbl_client_statutories T2 " + \
        " ON T2.client_statutory_id = T1.client_statutory_id " + \
        " INNER JOIN tbl_units T3 " + \
        " ON T3.unit_id = T2.unit_id " + \
        " INNER JOIN tbl_compliances T4 " + \
        " ON T4.compliance_id = T1.compliance_id " + \
        " WHERE T2.country_id IN %s " + \
        " AND T2.domain_id IN %s "
    limit = " limit %s, %s "
    country_ids = request.country_ids
    if len(country_ids) == 1:
        country_ids.append(0)
    domain_ids = request.domain_ids
    if len(domain_ids) == 1:
        domain_ids.append(0)
    param = [
        tuple(country_ids), tuple(domain_ids),
    ]
    filter_type = request.filter_type
    filter_id = request.filter_ids
    if len(filter_id) == 1:
        filter_id.append(0)
    applicability = request.applicability_status

    if filter_type == "Group":
        # filter_type_qry = "AND T3.country_id
        # IN %s" % (str(tuple(filter_ids)))
        where_type_qry = ""

    elif filter_type == "BusinessGroup":
        where_type_qry = "AND T3.business_group_id IN %s "
        param.append(tuple(filter_id))

    elif filter_type == "LegalEntity":
        where_type_qry = "AND T3.legal_entity_id IN %s "
        param.append(tuple(filter_id))

    elif filter_type == "Division":
        where_type_qry = "AND T3.division_id IN %s "
        param.append(tuple(filter_id))

    elif filter_type == "Unit":
        where_type_qry = "AND T3.unit_id IN %s "
        param.append(tuple(filter_id))

    if applicability == "Applicable":
        where_type_qry += " AND T1.compliance_opted = 1"
    elif applicability == "Not Applicable":
        where_type_qry += " AND T1.compliance_opted = 0 " + \
            " AND T1.compliance_applicable = 0"
    elif applicability == "Not Opted":
        where_type_qry += " AND T1.compliance_applicable = 1 " + \
            " AND T1.compliance_opted = 0"

    query1 = query + where_type_qry + limit
    param.extend([from_count, to_count])
    rows = db.select_all(query1, param)
    columns = [
        "compliance_id", "unit_id", "frequency_id",
        "frequency", "repeats_type", "duration_type",
        "statutory_mapping", "statutory_provision", "compliance_task",
        "compliance_description", "document_name", "format_file",
        "format_file_size", "penal_consequences", "statutory_dates",
        "repeats_every", "duration", "is_active", "unit_name"
    ]
    result = convert_to_dict(rows, columns)

    level_1_wise_compliance = {}

    for r in result:
        unit_name = r["unit_name"]
        mappings = r["statutory_mapping"].split(">>")
        if len(mappings) >= 1:
            level_1 = mappings[0]
        else:
            level_1 = mappings

        level_1 = level_1.strip()

        statutory_dates = json.loads(r["statutory_dates"])
        date_list = []
        for s in statutory_dates:
            s_date = core.StatutoryDate(
                s["statutory_date"], s["statutory_month"],
                s["trigger_before_days"],
                s.get("repeat_by")
            )
            date_list.append(s_date)

        format_file = r["format_file"]
        format_file_size = r["format_file_size"]
        file_list = None
        download_file_list = None
        if format_file is not None and format_file_size is not None:
            if len(format_file) != 0:
                file_list = []
                download_file_list = []
                file_info = core.FileList(
                    int(format_file_size), format_file, None
                )
                file_list.append(file_info)
                # file_name = format_file.split('-')[0]
                file_download = "%s/%s" % (
                    FORMAT_DOWNLOAD_URL, format_file
                )
                download_file_list.append(
                        file_download
                    )

        if int(r["frequency_id"]) == 1:
            summary = None
        elif int(r["frequency_id"]) in (2, 3):
            summary = "Repeats every %s %s " % (
                r["repeats_every"], r["repeats_type"]
            )
        else:
            summary = "To complete with in %s %s " % (
                r["duration"], r["duration_type"]
            )

        compliance = dashboard.Compliance(
            int(r["compliance_id"]), r["statutory_provision"],
            r["compliance_task"], r["compliance_description"],
            r["document_name"], file_list, r["penal_consequences"],
            r["frequency"], date_list, bool(r["is_active"]),
            download_file_list, summary
        )
        level_1_wise_data = level_1_wise_compliance.get(level_1)
        if level_1_wise_data is None:
            compliance_dict = {}
            compliance_list = [compliance]
            compliance_dict[unit_name] = compliance_list
            level_1_wise_data = dashboard.ApplicableDrillDown(
                level_1, compliance_dict
            )
        else:
            compliance_dict = level_1_wise_data.compliances
            compliance_list = compliance_dict.get(unit_name)
            if compliance_list is None:
                compliance_list = []
            compliance_list.append(compliance)

            compliance_dict[unit_name] = compliance_list
            level_1_wise_data.compliances = compliance_dict

        level_1_wise_compliance[level_1] = level_1_wise_data

    return level_1_wise_compliance.values()


#
#   Notifications
#
def get_notifications(
    db, notification_type, start_count, to_count,
    session_user, client_id
):
    users = get_all_users(db)

    def get_user_info_str(user_id):
        u_info = users.get(user_id)
        if u_info is None:
            return None
        data = "%s - %s, %s - %s " % (
            u_info.get("employee_code"),
            u_info.get("employee_name"),
            u_info.get("contact_no"),
            u_info.get("email_id")
        )
        return data

    notification_type_id = None
    if notification_type == "Notification":
        notification_type_id = 1
    elif notification_type == "Reminder":
        notification_type_id = 2
    elif notification_type == "Escalation":
        notification_type_id = 3
    user_ids = [session_user]
    if is_primary_admin(db, session_user) is True:
        user_ids.append(0)
    query = " SELECT nul.notification_id as notification_id, " + \
            " notification_text, created_on, extra_details, " + \
            " statutory_provision, assignee, " + \
            " IFNULL(concurrence_person, -1), " + \
            " approval_person, nl.compliance_id, compliance_task, " + \
            " document_name, compliance_description, penal_consequences,  " + \
            " read_status, due_date, completion_date, approve_status, " + \
            " (select concat(unit_code, '-', unit_name, ',', address) " + \
            " from tbl_units where " + \
            " unit_id = nl.unit_id) " + \
            " FROM tbl_notification_user_log nul " + \
            " LEFT JOIN tbl_notifications_log nl " + \
            " ON (nul.notification_id = nl.notification_id) " + \
            " LEFT JOIN tbl_compliances tc " + \
            " ON (tc.compliance_id = nl.compliance_id) " + \
            " LEFT JOIN tbl_compliance_history tch " + \
            " ON (tch.compliance_id = nl.compliance_id AND " + \
            " tch.unit_id = nl.unit_id) " + \
            " WHERE notification_type_id = %s " + \
            " AND user_id in (%s) " + \
            " AND (compliance_history_id is null " + \
            " OR  compliance_history_id = CAST(REPLACE( " + \
            " SUBSTRING_INDEX(extra_details, '-', 1), " + \
            " ' ','') AS UNSIGNED)) " + \
            " ORDER BY read_status ASC, nul.notification_id DESC " + \
            " limit %s, %s"
    rows = db.select_all(query, [
        notification_type_id,
        ",".join(str(x) for x in user_ids),
        start_count, to_count
    ])
    columns_list = [
        "notification_id", "notification_text", "created_on",
        "extra_details", "statutory_provision",
        "assignee", "concurrence_person", "approval_person",
        "compliance_id", "compliance_task", "document_name",
        "compliance_description", "penal_consequences", "read_status",
        "due_date", "completion_date", "approve_status", "unit_details"
    ]

    notifications = convert_to_dict(rows, columns_list)
    notifications_list = []
    for notification in notifications:
        notification_id = notification["notification_id"]
        read_status = bool(int(notification["read_status"]))
        extra_details_with_history_id = notification[
            "extra_details"].split("-")
        compliance_history_id = int(extra_details_with_history_id[0])
        extra_details = extra_details_with_history_id[1]
        if compliance_history_id not in [0, "0", None, "None", ""]:
            due_date_as_date = notification["due_date"]
            due_date = datetime_to_string_time(due_date_as_date)
            completion_date = notification["completion_date"]
            approve_status = notification["approve_status"]
            delayed_days = "-"
            if completion_date is None or approve_status == 0:
                no_of_days, delayed_days = calculate_ageing(due_date_as_date)
            else:
                r = relativedelta.relativedelta(
                    due_date_as_date, completion_date
                )
                delayed_days = "-"
                if r.days < 0 and r.hours < 0 and r.minutes < 0:
                    delayed_days = "Overdue by %s days" % abs(r.days)
            if "Overdue" not in delayed_days:
                delayed_days = "-"
            # diff = get_date_time() - due_date_as_datetime
            statutory_provision = notification[
                "statutory_provision"].split(">>")
            level_1_statutory = statutory_provision[0]

            notification_text = notification["notification_text"]
            updated_on = datetime_to_string(notification["created_on"])
            unit_details = notification["unit_details"].split(",")
            unit_name = unit_details[0]
            unit_address = unit_details[1]
            assignee = get_user_info_str(notification["assignee"])
            concurrence_person = get_user_info_str(
                notification["concurrence_person"]
            )
            approval_person = get_user_info_str(
                notification["approval_person"]
            )
            compliance_name = notification["compliance_task"]
            if(
                notification["document_name"] is not None and
                notification["document_name"].replace(" ", "") != "None"
            ):
                compliance_name = "%s - %s" % (
                    notification["document_name"],
                    notification["compliance_task"]
                )
            compliance_description = notification["compliance_description"]
            penal_consequences = notification["penal_consequences"]
            due_date = datetime_to_string_time(notification["due_date"])
        else:
            penal_consequences = None
            delayed_days = None
            due_date = None
            compliance_description = None
            approval_person = None
            compliance_name = None
            concurrence_person = None
            assignee = None
            unit_name = None
            unit_address = None
            level_1_statutory = None
            extra_details = notification["extra_details"].split("-")[1]
            read_status = bool(0)
            updated_on = datetime_to_string(get_date_time_in_date())
            notification_text = notification["notification_text"]
        notifications_list.append(
            dashboard.Notification(
                notification_id, read_status, notification_text, extra_details,
                updated_on, level_1_statutory, unit_name, unit_address,
                assignee, concurrence_person, approval_person, compliance_name,
                compliance_description, due_date, delayed_days,
                penal_consequences
            )
        )
    return notifications_list


def update_notification_status(
    db, notification_id, has_read, session_user, client_id
):
    user_ids = [session_user]
    if is_primary_admin(db, session_user) is True:
        user_ids.append(0)
    columns = ["read_status"]
    values = [1 if has_read is True else 0]
    condition = " notification_id = %s AND "
    user_condition, user_condition_val = db.generate_tuple_condition(
        "user_id", user_ids)
    condition = condition + user_condition
    values.extend([notification_id, user_condition_val])
    db.update(
        tblNotificationUserLog, columns, values, condition
    )


def get_user_company_details(db, user_id, client_id=None):
    admin_id = get_admin_id(db)
    columns = [
        "unit_id", "business_group_id", "legal_entity_id", "division_id"
    ]
    condition = " 1 "
    condition_val = None
    if user_id != admin_id:
        columns = ["unit_id"]
        condition = "  user_id = %s"
        condition_val = [user_id]
        rows = db.get_data(
            tblUserUnits, columns, condition, condition_val
        )
        unit_ids = [
            int(row["unit_id"]) for row in rows
        ]
        condition = " unit_id in (%s)"
        condition_val = [
            ",".join(str(x) for x in unit_ids)
        ]
    rows = db.get_data(
        tblUnits, columns, condition, condition_val
    )
    unit_ids = []
    division_ids = []
    legal_entity_ids = []
    business_group_ids = []
    for row in rows:
        unit_ids.append(
            int(row["unit_id"])
        )
        if row["division_id"] is not None:
            if int(row["division_id"]) not in division_ids:
                division_ids.append(int(row["division_id"]))
        if int(row["legal_entity_id"]) not in legal_entity_ids:
            legal_entity_ids.append(int(row["legal_entity_id"]))
        if row["business_group_id"] is not None:
            if int(row["business_group_id"]) not in business_group_ids:
                business_group_ids.append(int(row["business_group_id"]))
    return (
        ",".join(str(x) for x in unit_ids),
        ",".join(str(x) for x in division_ids),
        ",".join(str(x) for x in legal_entity_ids),
        ",".join(str(x) for x in business_group_ids)
    )


#
#   Assigee wise compliance chart
#
def get_assigneewise_compliances_list(
    db, country_id, business_group_id, legal_entity_id, division_id,
    unit_id, session_user, client_id, assignee_id
):
    condition = "tu.country_id =  %s" % country_id
    if business_group_id is not None:
        condition += " AND tu.business_group_id = %s" % (business_group_id)
    if legal_entity_id is not None:
        condition += " AND tu.legal_entity_id = %s" % (legal_entity_id)
    if division_id is not None:
        condition += " AND tu.division_id = %s" % (division_id)
    if unit_id is not None:
        condition += " AND tu.unit_id = %s" % (unit_id)
    else:
        units = get_user_unit_ids(db, session_user)
        if len(units) == 1:
            units.append(0)
        condition += " AND tu.unit_id in (%s) " % (
            ",".join(str(x) for x in units)
        )
    if assignee_id is not None:
        condition += " AND tch.completed_by = %s" % (assignee_id)
    domain_ids_list = get_user_domains(db, session_user)
    current_date = get_date_time_in_date()
    result = {}
    for domain_id in domain_ids_list:
        timelines = get_country_domain_timelines(
            db, [country_id], [domain_id], [current_date.year], client_id
        )
        from_date = timelines[0][1][0][1][0]["start_date"].date()
        to_date = timelines[0][1][0][1][0]["end_date"].date()
        query = " SELECT " + \
            " concat(IFNULL(employee_code, " + \
            " 'Administrator'), '-', employee_name) " + \
            " as Assignee, tch.completed_by, tch.unit_id, " + \
            " concat(unit_code, '-', unit_name) as Unit, " + \
            " address, tc.domain_id, " + \
            " (SELECT domain_name FROM tbl_domains td " + \
            " WHERE tc.domain_id = td.domain_id) as Domain, " + \
            " sum(case when (approve_status = 1 " + \
            " and (tch.due_date > completion_date or " + \
            " tch.due_date = completion_date)) then 1 else 0 end) " + \
            " as complied, " + \
            " sum(case when ((approve_status = 0 " + \
            " or approve_status is null) and " + \
            " tch.due_date > now()) then 1 else 0 end) as Inprogress, " + \
            " sum(case when ((approve_status = 0 " + \
            " or approve_status is null) and " + \
            " tch.due_date < now()) then 1 else 0 end) as NotComplied, " + \
            " sum(case when (approve_status = 1 " + \
            " and completion_date > tch.due_date and " + \
            " (is_reassigned = 0 or is_reassigned is null) ) " + \
            " then 1 else 0 end) as DelayedCompliance , " + \
            " sum(case when (approve_status = 1 " + \
            " and completion_date > tch.due_date and (is_reassigned = 1)) " + \
            " then 1 else 0 end) as DelayedReassignedCompliance " + \
            " FROM tbl_compliance_history tch " + \
            " INNER JOIN tbl_assigned_compliances tac ON ( " + \
            " tch.compliance_id = tac.compliance_id " + \
            " AND tch.unit_id = tac.unit_id) " + \
            " INNER JOIN tbl_units tu ON (tac.unit_id = tu.unit_id) " + \
            " INNER JOIN tbl_users tus ON (tus.user_id = tac.assignee) " + \
            " INNER JOIN tbl_compliances tc " + \
            " ON (tac.compliance_id = tc.compliance_id) " + \
            " WHERE %s AND domain_id = %s "
        query = query % (condition, domain_id)
        date_condition = " AND tch.due_date " + \
            " BETWEEN '%s' AND '%s' " + \
            " group by completed_by, tch.unit_id; "
        date_condition = date_condition % (from_date, to_date)
        query = query + date_condition
        rows = db.select_all(query)
        columns = [
            "assignee", "completed_by", "unit_id", "unit_name",
            "address", "domain_id", "domain_name", "complied",
            "inprogress", "not_complied", "delayed", "delayed_reassigned"
        ]
        assignee_wise_compliances = convert_to_dict(rows, columns)

        for compliance in assignee_wise_compliances:
            unit_name = compliance["unit_name"]
            assignee = compliance["assignee"]
            if unit_name not in result:
                result[unit_name] = {
                    "unit_id": compliance["unit_id"],
                    "address": compliance["address"],
                    "assignee_wise": {}
                }
            if assignee not in result[unit_name]["assignee_wise"]:
                result[unit_name]["assignee_wise"][assignee] = {
                    "user_id": compliance["completed_by"],
                    "domain_wise": []
                }
            total_compliances = int(
                compliance["complied"]) + int(compliance["inprogress"])
            total_compliances += int(
                compliance["delayed"]) + int(compliance["delayed_reassigned"])
            total_compliances += int(compliance["not_complied"])
            result[unit_name]["assignee_wise"][assignee]["domain_wise"].append(
                dashboard.DomainWise(
                    domain_id=domain_id,
                    domain_name=compliance["domain_name"],
                    total_compliances=total_compliances,
                    complied_count=int(compliance["complied"]),
                    assigned_count=int(compliance["delayed"]),
                    reassigned_count=int(compliance["delayed_reassigned"]),
                    inprogress_compliance_count=int(compliance["inprogress"]),
                    not_complied_count=int(compliance["not_complied"])
                )
            )
    chart_data = []
    for unit_name in result:
        assignee_wise_compliances_count = []
        for assignee in result[unit_name]["assignee_wise"]:
            result[unit_name]["assignee_wise"][assignee]["domain_wise"]
            assignee_wise_compliances_count.append(
                dashboard.AssigneeWiseDetails(
                    user_id=result[
                        unit_name]["assignee_wise"][assignee]["user_id"],
                    assignee_name=assignee,
                    domain_wise_details=result[
                        unit_name]["assignee_wise"][assignee]["domain_wise"]
                )
            )
        if len(assignee_wise_compliances_count) > 0:
            chart_data.append(
                dashboard.AssigneeChartData(
                    unit_name=unit_name,
                    unit_id=result[unit_name]["unit_id"],
                    address=result[unit_name]["address"],
                    assignee_wise_details=assignee_wise_compliances_count
                )
            )
    return chart_data


def get_assigneewise_yearwise_compliances(
    db, country_id, unit_id, user_id, client_id
):
    current_year = get_date_time_in_date().year
    domain_ids_list = get_user_domains(db, user_id)
    start_year = current_year - 5
    iter_year = start_year
    year_wise_compliance_count = []
    while iter_year <= current_year:
        domainwise_complied = 0
        domainwise_inprogress = 0
        domainwise_notcomplied = 0
        domainwise_total = 0
        domainwise_delayed = 0
        for domain_id in domain_ids_list:
            result = get_country_domain_timelines(
                db, [country_id], [domain_id], [iter_year], client_id
            )
            from_date = result[0][1][0][1][0]["start_date"].date()
            to_date = result[0][1][0][1][0]["end_date"].date()
            query = " SELECT tc.domain_id, " + \
                " sum(case when (approve_status = 1 " + \
                " and (tch.due_date > completion_date or " + \
                " tch.due_date = completion_date)) " + \
                " then 1 else 0 end) as complied, " + \
                " sum(case when ((approve_status = 0 " + \
                " or approve_status is null) and " + \
                " tch.due_date > now()) then 1 else 0 end) as Inprogress, " + \
                " sum(case when ((approve_status = 0 or " + \
                " approve_status is null) and " + \
                " tch.due_date < now()) then 1 else 0 end) " + \
                " as NotComplied, " + \
                " sum(case when (approve_status = 1 " + \
                " and completion_date > tch.due_date and " + \
                " (is_reassigned = 0 or is_reassigned is null) ) " + \
                " then 1 else 0 end) as DelayedCompliance, " + \
                " sum(case when (approve_status = 1 and " + \
                " completion_date > tch.due_date and (is_reassigned = 1)) " + \
                " then 1 else 0 end) as DelayedReassignedCompliance " + \
                " FROM tbl_compliance_history tch " + \
                " INNER JOIN tbl_assigned_compliances tac ON ( " + \
                " tch.compliance_id = tac.compliance_id " + \
                " AND tch.unit_id = tac.unit_id " + \
                " AND tch.completed_by = %s) " + \
                " INNER JOIN tbl_units tu ON (tac.unit_id = tu.unit_id) " + \
                " INNER JOIN tbl_users tus " + \
                " ON (tus.user_id = tac.assignee) " + \
                " INNER JOIN tbl_compliances tc " + \
                " ON (tac.compliance_id = tc.compliance_id) " + \
                " INNER JOIN tbl_domains td " + \
                " ON (td.domain_id = tc.domain_id) " + \
                " WHERE tch.unit_id =%s " + \
                " AND tc.domain_id = %s "
            date_condition = " AND tch.due_date between '%s' AND '%s';"
            date_condition = date_condition % (from_date, to_date)
            query = query + date_condition
            rows = db.select_all(query, [
                user_id, unit_id, int(domain_id)
            ])
            if rows:
                convert_columns = [
                    "domain_id", "complied", "inprogress", "not_complied",
                    "delayed", "delayed_reassigned"
                ]
                count_rows = convert_to_dict(rows, convert_columns)
                for row in count_rows:
                    domainwise_complied += 0 if(
                        row["complied"] is None) else int(row["complied"])
                    domainwise_inprogress += 0 if(
                        row["inprogress"] is None) else int(row["inprogress"])
                    domainwise_notcomplied += 0 if(
                        row["not_complied"] is None
                    ) else int(row["not_complied"])
                    domainwise_delayed += 0 if(
                        row["delayed"] is None) else int(row["delayed"])
                    domainwise_delayed += 0 if(
                            row["delayed_reassigned"] is None
                        ) else int(row["delayed_reassigned"])
        domainwise_total += (
            domainwise_complied + domainwise_inprogress)
        domainwise_total += (
            domainwise_notcomplied + domainwise_delayed)
        year_wise_compliance_count.append(
            dashboard.YearWise(
                year=str(iter_year),
                total_compliances=domainwise_total,
                complied_count=domainwise_complied,
                delayed_compliance=domainwise_delayed,
                inprogress_compliance_count=domainwise_inprogress,
                not_complied_count=domainwise_notcomplied
            )
        )
        iter_year += 1
    return year_wise_compliance_count


def get_assigneewise_reassigned_compliances(
    db, country_id, unit_id, user_id, domain_id, client_id
):
    current_year = get_date_time_in_date().year
    result = get_country_domain_timelines(
        db, [country_id], [domain_id], [current_year], client_id
    )
    from_date = result[0][1][0][1][0]["start_date"].date()
    to_date = result[0][1][0][1][0]["end_date"].date()
    query = " SELECT reassigned_date, concat( " + \
        " IFNULL(employee_code, 'Administrator'), '-', " + \
        " employee_name) as previous_assignee,  " + \
        " document_name, compliance_task, " + \
        " tch.due_date, DATE_SUB(tch.due_date, " + \
        " INTERVAL trigger_before_days DAY) as start_date, " + \
        " completion_date FROM tbl_reassigned_compliances_history trch " + \
        " INNER JOIN " + \
        " tbl_compliance_history tch ON ( " + \
        " trch.compliance_id = tch.compliance_id " + \
        " AND assignee= %s AND trch.unit_id = tch.unit_id) " + \
        " INNER JOIN tbl_assigned_compliances tac ON ( " + \
        " tch.compliance_id = tac.compliance_id  " + \
        " AND tch.unit_id = tac.unit_id " + \
        " AND tch.completed_by = %s) " + \
        " INNER JOIN tbl_units tu ON (tac.unit_id = tu.unit_id) " + \
        " INNER JOIN tbl_users tus ON (tus.user_id = tac.assignee) " + \
        " INNER JOIN tbl_compliances tc " + \
        " ON (tac.compliance_id = tc.compliance_id) " + \
        " INNER JOIN tbl_domains td ON (td.domain_id = tc.domain_id) " + \
        " WHERE tch.unit_id = %s AND tc.domain_id = %s " + \
        " AND approve_status = 1 AND completed_by = %s " + \
        " AND reassigned_date between CAST(tch.start_date AS DATE) " + \
        " and CAST(completion_date AS DATE) " + \
        " AND completion_date > tch.due_date AND is_reassigned = 1 "

    date_condition = " AND tch.due_date between '%s' AND '%s' "
    date_condition = date_condition % (from_date, to_date)
    query += date_condition
    rows = db.select_all(query, [
        user_id, user_id, unit_id, int(domain_id), user_id
    ])
    columns = [
        "reassigned_date", "reassigned_from", "document_name",
        "compliance_name", "due_date", "start_date", "completion_date"
    ]
    results = convert_to_dict(rows, columns)
    reassigned_compliances = []
    for compliance in results:
        compliance_name = compliance["compliance_name"]
        if compliance["document_name"] is not None:
            compliance_name = "%s - %s" % (
                compliance["document_name"], compliance_name
            )
        reassigned_compliances.append(
            dashboard.RessignedCompliance(
                compliance_name=compliance_name,
                reassigned_from=compliance["reassigned_from"],
                start_date=datetime_to_string(compliance["start_date"]),
                due_date=datetime_to_string(compliance["due_date"]),
                reassigned_date=datetime_to_string(
                    compliance["reassigned_date"]
                ),
                completed_date=datetime_to_string(
                    compliance["completion_date"]
                )
            )
        )
    return reassigned_compliances


def get_assigneewise_compliances_drilldown_data_count(
    db, country_id, assignee_id, domain_id, client_id, year, unit_id,
    session_user
):
    domain_id_list = []
    if domain_id is None:
        domain_id_list = get_user_domains(db, session_user)
    else:
        domain_id_list = [domain_id]

    if year is None:
        current_year = get_date_time_in_date().year
    else:
        current_year = year
    result = get_country_domain_timelines(
        db, [country_id], [domain_id], [current_year], client_id
    )
    from_date = datetime.datetime(current_year, 1, 1)
    to_date = datetime.datetime(current_year, 12, 31)
    domain_condition = ",".join(str(x) for x in domain_id_list)
    if len(domain_id_list) == 1:
        result = get_country_domain_timelines(
            db, [country_id], domain_id_list, [current_year], client_id
        )
        from_date = result[0][1][0][1][0]["start_date"]
        to_date = result[0][1][0][1][0]["end_date"]
        domain_condition = str(domain_id_list[0])
    query = " SELECT count(*) " + \
        " FROM tbl_compliance_history tch " + \
        " INNER JOIN tbl_compliances tc ON " + \
        " (tch.compliance_id = tc.compliance_id) " + \
        " INNER JOIN tbl_users tu ON (tch.completed_by = tu.user_id) " + \
        " WHERE completed_by = %s AND unit_id = %s " + \
        " AND due_date BETWEEN %s AND %s " + \
        " AND domain_id in (%s) "
    rows = db.select_all(query, [
        assignee_id, unit_id, from_date, to_date, domain_condition
    ])
    return rows[0][0]


def get_assigneewise_compliances_drilldown_data(
    db, country_id, assignee_id, domain_id, client_id, year, unit_id,
    start_count, to_count, session_user
):
    domain_id_list = []
    if domain_id is None:
        domain_id_list = get_user_domains(db, session_user)
    else:
        domain_id_list = [domain_id]

    if year is None:
        current_year = get_date_time_in_date().year
    else:
        current_year = year
    from_date = datetime.datetime(current_year, 1, 1)
    to_date = datetime.datetime(current_year, 12, 31)
    domain_condition = ",".join(str(x) for x in domain_id_list)
    if len(domain_id_list) == 1:
        result = get_country_domain_timelines(
            db, [country_id], domain_id_list, [current_year], client_id
        )
        from_date = result[0][1][0][1][0]["start_date"]
        to_date = result[0][1][0][1][0]["end_date"]
        domain_condition = str(domain_id_list[0])
    columns = " tch.compliance_id as compliance_id, start_date, " + \
        " due_date, completion_date, " + \
        " document_name, compliance_task, " + \
        " compliance_description, " + \
        " statutory_mapping, concat( " + \
        " IFNULL(employee_code, 'Administrator'), " + \
        " '-', employee_name) as employee_name"
    subquery_columns = "IF( " + \
        " (approve_status = 1 " + \
        " and completion_date <= due_date), " + \
        " 'Complied', " + \
        " ( " + \
        "    IF( " + \
        "        (approve_status = 1 and completion_date > due_date), " + \
        "        'Delayed', " + \
        "        ( " + \
        "            IF ( " + \
        "                 ((approve_status = 0 " + \
        "                 or approve_status is null) and " + \
        "                due_date > now()), " + \
        "                'Inprogress', " + \
        "                'NotComplied' " + \
        "            ) " + \
        "        ) " + \
        "    ) " + \
        ") " + \
        ") as compliance_status"
    query = " SELECT " + \
        " compliance_id, start_date, due_date, completion_date, " + \
        " document_name, compliance_task, compliance_description, " + \
        " statutory_mapping, employee_name, compliance_status FROM ( " + \
        " SELECT %s, %s " + \
        " FROM tbl_compliance_history tch " + \
        " INNER JOIN tbl_compliances tc " + \
        " ON (tch.compliance_id = tc.compliance_id) " + \
        " INNER JOIN tbl_users tu ON (tch.completed_by = tu.user_id) "
    query = query % (columns, subquery_columns)
    date_condition = " AND due_date BETWEEN '%s' AND '%s' " % (
        from_date, to_date
    )
    where_condition = " WHERE completed_by = %s AND unit_id = %s " + \
        " %s  AND domain_id in (%s) " + \
        " LIMIT %s, %s) a " + \
        " ORDER BY compliance_status "
    where_condition = where_condition % (
            assignee_id, unit_id, date_condition, domain_condition,
            int(start_count), to_count
        )
    query = query + where_condition
    rows = db.select_all(query)
    columns_list = [
        "compliance_id", "start_date", "due_date", "completion_date",
        "document_name", "compliance_name", "compliance_description",
        "statutory_mapping", "assignee", "compliance_status"
    ]
    result = convert_to_dict(rows, columns_list)

    complied_compliances = {}
    inprogress_compliances = {}
    delayed_compliances = {}
    not_complied_compliances = {}

    for compliance in result:
        compliance_name = compliance["compliance_name"]
        compliance_status = compliance["compliance_status"]
        if compliance["document_name"] is not None:
            compliance_name = "%s - %s" % (
                compliance["document_name"], compliance_name
            )
        level_1_statutory = compliance["statutory_mapping"].split(">>")[0]

        current_list = not_complied_compliances
        if compliance_status == "Complied":
            current_list = complied_compliances
        elif compliance_status == "Delayed":
            current_list = delayed_compliances
        elif compliance_status == "Inprogress":
            current_list = inprogress_compliances

        if level_1_statutory not in current_list:
            current_list[level_1_statutory] = []

        current_list[level_1_statutory].append(
            dashboard.AssigneeWiseLevel1Compliance(
                compliance_name=compliance_name,
                description=compliance["compliance_description"],
                assignee_name=compliance["assignee"],
                assigned_date=None if(
                    compliance["start_date"] is None
                    ) else datetime_to_string(compliance["start_date"]),
                due_date=datetime_to_string(compliance["due_date"]),
                completion_date=None if(
                    compliance["completion_date"] is None
                ) else datetime_to_string(compliance["completion_date"])
            )
        )
    return (
        complied_compliances, delayed_compliances, inprogress_compliances,
        not_complied_compliances
    )


def is_already_notified(db):
    query = " select count(*) from tbl_notifications_log " + \
        " where notification_text like " + \
        " '%sYour contract with Compfie for%s' " + \
        " AND created_on > DATE_SUB(now(), INTERVAL 30 DAY); "
    query = query % ('%', '%')
    rows = db.select_all(query)
    if rows:
        count = rows[0][0]
        if count > 0:
            return True
        else:
            return False
    else:
        return False


def notify_expiration(db, client_id):
    download_link = exp(client_id, db).generate_report()
    group_name = get_group_name(db)

    notification_text = " Your contract with Compfie for the " + \
        " group \"%s\" is about to expire. " + \
        " Kindly renew your contract to avail the " + \
        " services continuously. " + \
        " Before contract expiration " + \
        " You can download documents <a href='%s'>here </a> "
    notification_text = notification_text % (group_name, download_link)
    extra_details = "0 - Reminder: Contract Expiration"
    # notification_id = db.get_new_id("notification_id", tblNotificationsLog)
    created_on = datetime.datetime.now()
    columns = [
        "notification_type_id", "notification_text",
        "extra_details", "created_on"
    ]
    values = [2, notification_text, extra_details, created_on]
    notification_id = db.insert(tblNotificationsLog, columns, values)

    columns = ["notification_id", "user_id"]
    values = [notification_id, 0]
    db.insert(tblNotificationUserLog, columns, values)
    q = "SELECT email_id from tbl_users " + \
        " where is_active = 1 and is_primary_admin = 1"
    rows = db.select_all(q)
    admin_mail_id = rows[0][0]
    email.notify_contract_expiration(
        admin_mail_id, notification_text
    )


def get_no_of_days_left_for_contract_expiration(db, client_id):
    column = "contract_to"
    condition = "1"
    rows = db.get_data(tblClientGroups, column, condition)
    contract_to_str = str(rows[0]["contract_to"])
    contract_to_parts = [int(x) for x in contract_to_str.split("-")]
    contract_to = datetime.date(
        contract_to_parts[0], contract_to_parts[1], contract_to_parts[2]
    )
    delta = contract_to - get_date_time_in_date().date()
    if delta.days < 30:
        if not is_already_notified(db):
            notify_expiration(db, client_id)
    return delta.days


def need_to_display_deletion_popup(db):
    current_date = get_date_time_in_date()
    column = "notification_id, created_on, notification_text"
    condition = "extra_details like %s%s%s AND " + \
        " created_on > DATE_SUB(now(), INTERVAL 30 DAY )"
    condition_val = ["%", "Auto Deletion", "%"]
    notification_rows = db.get_data(
        tblNotificationsLog, column, condition, condition_val
    )
    if len(notification_rows) > 0:
        notification_id = notification_rows[0]["notification_id"]
        created_on = notification_rows[0]["created_on"]
        r = relativedelta.relativedelta(current_date.date(), created_on)
        if (
            (abs(r.days) % 6) == 0 and
            r.years == 0 and
            r.months == 0 and r.days != 0
        ):
            columns = "updated_on"
            condition = "notification_id = %s and " + \
                " date(updated_on) !=  CURDATE()"
            condition_val = [notification_id]
            rows = db.get_data(
                tblNotificationUserLog, columns, condition, condition_val
            )
            if len(rows) > 0:
                columns = ["updated_on"]
                values = [current_date]
                condition = "notification_id = %s" % notification_id
                db.update(tblNotificationUserLog, columns, values, condition)
                return True, notification_rows[0]["notification_text"]
            else:
                return False, ""
        else:
            return False, ""
    else:
        return False, ""


def get_compliance_history_ids_for_trend_chart(
    db,
    country_id, domain_id, client_id,
    filter_id=None, filter_type=None
):
    # Units related to the selected country and domain
    unit_columns = "unit_id"
    unit_condition = "country_id = %s " % (country_id)
    unit_condition += " AND  find_in_set( " + \
        " %s, domain_ids) " % (
            domain_id
        )
    unit_condition_val = [country_id]
    if filter_type is not None:
        if filter_type == "BusinessGroup":
            unit_condition += " AND business_group_id =%s "
        elif filter_type == "LegalEntity":
            unit_condition += " AND legal_entity_id =%s "
        elif filter_type == "Division":
            unit_condition += " AND division_id =%s"
        elif filter_type == "Unit":
            unit_condition += " AND unit_id =%s "
        unit_condition_val.append(filter_id)
    unit_result_rows = db.get_data(
        tblUnits, unit_columns, unit_condition
    )
    unit_rows = []
    for row in unit_result_rows:
        unit_rows.append(row["unit_id"])
    unit_ids = None
    if len(unit_rows) > 0:
        unit_ids = ",".join(str(int(x)) for x in unit_rows)

    # Compliances related to the domain
    compliance_columns = "compliance_id"
    compliance_condition = "domain_id = %s"
    compliance_condition_val = [domain_id]
    compliance_result_rows = db.get_data(
        tblCompliances, compliance_columns, compliance_condition,
        compliance_condition_val
    )
    compliance_rows = []
    for row in compliance_result_rows:
        compliance_rows.append(row["compliance_id"])
    compliance_ids = None
    if len(compliance_rows) > 0:
        compliance_ids = ",".join(str(int(x)) for x in compliance_rows)

    result = get_client_statutory_ids_and_unit_ids_for_trend_chart(
        db, country_id, domain_id, client_id, filter_id, filter_type
    )
    client_statutory_ids = result[0]

    # Getting compliance history ids for selected country, domain
    compliance_history_ids = None
    if compliance_ids is not None and unit_ids is not None:
        columns = "compliance_history_id"
        condition = "compliance_id in (%s) and unit_id in (%s)"
        condition_val = [compliance_ids, unit_ids]
        rows = db.get_data(
            tblComplianceHistory, columns, condition, condition_val
        )
        result = []
        for row in rows:
            result.append(row["compliance_history_id"])
        compliance_history_ids = ",".join(str(x) for x in result)
    return compliance_history_ids, client_statutory_ids, unit_ids


def get_client_statutory_ids_and_unit_ids_for_trend_chart(
    db, country_id, domain_id, client_id, filter_id=None, filter_type=None
):
    columns = ["client_statutory_id", "unit_id"]
    condition = "country_id= %s and domain_id = %s"
    condition += " and unit_id in (select unit_id from  tbl_units where "
    condition_val = [
        country_id, domain_id
    ]
    if filter_type is not None:
        if filter_type == "BusinessGroup":
            condition += " business_group_id =%s and country_id =%s)"
        elif filter_type == "LegalEntity":
            condition += " legal_entity_id =%s and country_id =%s)"
        elif filter_type == "Division":
            condition += " division_id =%s and country_id =%s)"
        elif filter_type == "Unit":
            condition += " unit_id =%s and country_id =%s)"
        condition_val.append(filter_id)
    else:
        condition += " country_id = %s )"
    condition_val.append(country_id)
    rows = db.get_data(
        tblClientStatutories, columns, condition, condition_val
    )
    client_statutories = []
    unit_ids = []
    for row in rows:
        statu_id = int(row["client_statutory_id"])
        unit_id = int(row["unit_id"])
        if statu_id not in client_statutories:
            client_statutories.append(statu_id)
        if unit_id not in unit_ids:
            unit_ids.append(unit_id)
    return (
        ",".join(str(x) for x in client_statutories),
        ",".join(str(x) for x in unit_ids)
    )


def get_client_compliance_count(db):
    q = "select count(*) from tbl_compliances"
    row = db.select_one(q)
    return row[0]


def get_dashboard_notification_counts(
    db, session_user
):
    query = " SELECT tnl.notification_id FROM %s tnl " + \
        " INNER JOIN %s tnul ON " + \
        " tnl.notification_id = tnul.notification_id " + \
        " WHERE user_id = %s AND read_status = 0 "
    query = query % (
        tblNotificationsLog, tblNotificationUserLog, session_user
    )
    notification_condition = " AND notification_type_id = 1"
    escalation_condition = " AND notification_type_id = 3"
    reminder_condition = " AND notification_type_id = 2"

    notification_query = "%s %s" % (query, notification_condition)
    reminder_query = "%s %s" % (query, reminder_condition)
    escalation_query = "%s %s" % (query, escalation_condition)

    notification_rows = db.select_all(notification_query)
    reminder_rows = db.select_all(reminder_query)
    escalation_rows = db.select_all(escalation_query)

    notification_count = len(notification_rows)
    reminder_count = len(reminder_rows)
    escalation_count = len(escalation_rows)

    # statutory_column = "count(*) as result"
    # statutory_condition = "user_id = %s and read_status = 0 ORDER BY " + \
    #     " statutory_notification_id DESC"
    # statutory_condition_val = [session_user]
    # statutory_notification_rows = db.get_data(
    #     tblStatutoryNotificationStatus, statutory_column,
    #     statutory_condition, statutory_condition_val
    # )
    # statutory_notification_count = statutory_notification_rows[0]["result"]
    # notification_count += statutory_notification_count

    return notification_count, reminder_count, escalation_count
