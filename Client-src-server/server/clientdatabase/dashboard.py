import json
import datetime
from dateutil import relativedelta
from clientprotocol import (clientcore, dashboard)
from server.constants import FORMAT_DOWNLOAD_URL
from server.emailcontroller import EmailHandler
from server.clientdatabase.tables import *
from server.clientdatabase.common import (
    get_last_7_years, get_country_domain_timelines,
    calculate_ageing_in_hours, calculate_years,
)
from server.common import (
    get_date_time_in_date,
    datetime_to_string,
    make_summary,
    string_to_datetime
)
from server.clientdatabase.general import (
    get_user_unit_ids, get_admin_id,
    get_user_domains, get_group_name,
    convert_datetime_to_date
)

# from processes.expiry_report_generator import ExpiryReportGenerator as exp

email = EmailHandler()
__all__ = [
    "get_compliance_status_chart", "get_trend_chart", "get_not_complied_count",
    "get_risk_chart_count", "get_escalation_chart",
    "get_trend_chart_drill_down", "get_compliances_details_for_status_chart",
    "get_escalation_drill_down_data", "get_not_complied_drill_down", "get_compliance_applicability_drill_down",
    "get_notification_counts", "get_reminders", "get_escalations", "get_messages", "get_statutory",
    "update_notification_status", "update_statutory_notification_status", "statutory_notification_detail",
    "notification_detail", "get_user_company_details", "get_assigneewise_compliances_list",
    "get_assigneewise_yearwise_compliances", "get_assigneewise_reassigned_compliances",
    "get_assigneewise_compliances_drilldown_data", "get_assigneewise_compliances_drilldown_data_count",
    "get_no_of_days_left_for_contract_expiration", "need_to_display_deletion_popup",
]


def getCurrentYear():
    now = datetime.datetime.now()
    return now.year

# Compliance Status chart Begin


def get_compliances_details_for_status_chart(
    db, request, session_user, session_category, from_count, to_count
):
    d_ids = request.domain_ids
    year = request.year
    compliance_status = request.compliance_status
    chart_type = "compliance_status"

    result = compliance_details_query(
        db, request, chart_type, compliance_status,
        from_count, to_count, session_user, session_category, year
    )
    year_info = get_client_domain_configuration(db, d_ids, int(year))[0]
    return return_compliance_details_drill_down(
        year_info, compliance_status, request.year, result
    )

def get_compliance_status_count(db, request, user_id, user_category):
    chart_year = request.chart_year
    country_ids = request.country_ids
    domain_ids = request.domain_ids
    filter_type = request.filter_type
    filter_ids = request.filter_ids
    print filter_ids

    # where_qry_val.append(",".join([str(x) for x in filter_ids]))

    if filter_type == "Group":
        group_by_name = "t3.country_id"
        filter_type_ids = None
        filter_ids = country_ids

    elif filter_type == "BusinessGroup":
        group_by_name = "t3.business_group_id"
        filter_type_ids = " AND find_in_set(t3.business_group_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    elif filter_type == "LegalEntity":

        group_by_name = "t3.legal_entity_id"
        filter_type_ids = " AND find_in_set(t3.legal_entity_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    elif filter_type == "Division":
        group_by_name = "t3.division_id"
        filter_type_ids = " AND find_in_set(t3.division_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    elif filter_type == "Category" :
        group_by_name = "t3.category_id"
        filter_type_ids = " AND find_in_set(t3.category_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    elif filter_type == "Unit":
        group_by_name = "t3.unit_id"
        filter_type_ids = " AND find_in_set(t3.unit_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    elif filter_type == "Consolidated":
        group_by_name = "t3.country_id"
        filter_type_ids = None
        filter_ids = country_ids

    # where_qry += filter_type_ids

    if user_category <= 3 :
        q = "select " + group_by_name + " as filter_name, t1.country_id, t1.domain_id, " + \
            " sum(ifnull(complied_count, 0)) as comp_count, " + \
            " sum(ifnull(delayed_count, 0)) as delay_count, " + \
            " sum(ifnull(inprogress_count, 0)) as inp_count, sum(ifnull(overdue_count, 0)) as over_count, " + \
            " chart_year " + \
            " from tbl_compliance_status_chart_unitwise as t1  " + \
            " inner join tbl_units as t3 on t1.unit_id = t3.unit_id " + \
            " where chart_year = %s and find_in_set(t1.domain_id, %s) and find_in_set(t1.country_id, %s)"
        param = [
            chart_year,
            ",".join([str(x) for x in domain_ids]),
            ",".join([str(x) for x in country_ids])
        ]
    else :
        q = "select " + group_by_name + " as filter_name, t1.country_id, t1.domain_id, " + \
            " sum(ifnull(complied_count, 0)) as comp_count, sum(ifnull(delayed_count,0)) as delay_count, " + \
            " sum(ifnull(inprogress_count,0)) as inp_count, sum(ifnull(overdue_count,0)) as over_count, " + \
            " chart_year " + \
            " from tbl_compliance_status_chart_userwise as t1  " + \
            " inner join tbl_units as t3 on t1.unit_id = t3.unit_id " + \
            " where chart_year = %s and user_id = %s " + \
            " and find_in_set(t1.domain_id, %s) and find_in_set(t1.country_id, %s)"
        param = [
            chart_year, user_id,
            ",".join([str(x) for x in domain_ids]),
            ",".join([str(x) for x in country_ids])
        ]
    if filter_type_ids is not None :
        q += filter_type_ids
        param.append(filter_ids)

    q += " group by " + group_by_name

    rows = db.select_all(q, param)

    return frame_compliance_status(rows)

def frame_compliance_status(data):
    filter_wise_data = {}
    for d in data :
        filter_name = d["filter_name"]
        c = clientcore.NumberOfCompliances(
            d["domain_id"], d["country_id"], str(d["chart_year"]),
            0 if d["comp_count"] is None else int(d["comp_count"]),
            0 if d["delay_count"] is None else int(d["delay_count"]),
            0 if d["inp_count"] is None else int(d["inp_count"]),
            0 if d["over_count"] is None else int(d["over_count"])
        )
        if filter_wise_data.get(filter_name) is None :
            filter_wise_data[filter_name] = [c]
        else :
            lst = filter_wise_data.get(filter_name)
            lst.append(c)
            filter_wise_data[filter_name] = lst
    chart_data = []
    for k, v in filter_wise_data.iteritems() :
        chart_data.append(dashboard.ChartDataMap(k, v))
    return chart_data

def get_compliance_status_chart_date_wise(db, request, user_id, user_category):
    country_ids = request.country_ids
    domain_ids = request.domain_ids
    filter_type = request.filter_type
    from_date = request.from_date
    to_date = request.to_date
    from_date = string_to_datetime(from_date).date()
    to_date = string_to_datetime(to_date).date()

    if filter_type == "Group":
        group_by_name = "t3.country_id"
        filter_type_ids = None
        filter_ids = country_ids

    elif filter_type == "BusinessGroup":
        group_by_name = "t3.business_group_id"
        filter_type_ids = " AND find_in_set(t3.business_group_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    elif filter_type == "LegalEntity":

        group_by_name = "t3.legal_entity_id"
        filter_type_ids = " AND find_in_set(t3.legal_entity_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    elif filter_type == "Division":
        group_by_name = "t3.division_id"
        filter_type_ids = " AND find_in_set(t3.division_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    elif filter_type == "Category" :
        group_by_name = "t3.category_id"
        filter_type_ids = " AND find_in_set(t3.category_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    elif filter_type == "Unit":
        group_by_name = "t3.unit_id"
        filter_type_ids = " AND find_in_set(t3.unit_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    elif filter_type == "Consolidated":
        group_by_name = "t3.country_id"
        filter_type_ids = None
        filter_ids = country_ids

    q = "select " + group_by_name + " as filter_name , t3.country_id, cc.domain_id, ch.unit_id, ch.completed_by, " + \
        " ch.due_date, " + \
        " sum(IF(ifnull(com.duration_type_id,0) = 2,IF(ch.due_date >= ch.completion_date and ifnull(ch.approve_status,0) = 1,1,0),  " + \
        " IF(date(ch.due_date) >= date(ch.completion_date) and ifnull(ch.approve_status,0) = 1,1,0))) as comp_count,  " + \
        " sum(IF(ifnull(com.duration_type_id,0) = 2,IF(ch.due_date < ch.completion_date and ifnull(ch.approve_status,0) = 1,1,0),  " + \
        " IF(date(ch.due_date) < date(ch.completion_date) and ifnull(ch.approve_status,0) = 1,1,0))) as delay_count,  " + \
        " sum(IF(ifnull(com.duration_type_id,0) = 2,IF(ch.due_date >= now() and ifnull(ch.approve_status,0) <> 1 ,1,0),  " + \
        " IF(date(ch.due_date) >= curdate() and ifnull(ch.approve_status,0) <> 1 ,1,0))) as inp_count,  " + \
        " sum(IF(ifnull(com.duration_type_id,0) = 2,IF(ch.due_date < now() and ifnull(ch.approve_status,0) <> 1 ,1,0),  " + \
        " IF(date(ch.due_date) < curdate() and ifnull(ch.approve_status,0) <> 1 ,1,0))) as over_count,  " + \
        " Null as chart_year " + \
        " from tbl_units as t3  " + \
        " inner join tbl_client_compliances as cc on t3.unit_id = cc.unit_id  " + \
        " inner join tbl_compliances as com on cc.compliance_id = com.compliance_id  " + \
        " left join tbl_compliance_history as ch on ch.unit_id = cc.unit_id and ch.compliance_id = cc.compliance_id  "

    if user_category > 3 :
        q += " inner join tbl_users as usr on usr.user_id = ch.completed_by OR usr.user_id = ch.concurred_by OR usr.user_id = ch.approved_by  " + \
            " where find_in_set(cc.domain_id, %s) " + \
            " and date(ch.due_date) >= %s and date(ch.due_date) <= %s " + \
            " and usr.user_id = %s "
        param = [",".join([str(x) for x in domain_ids]), from_date, to_date, user_id]
    else :
        q += " where find_in_set(cc.domain_id, %s) " + \
            " and date(ch.due_date) >= %s and date(ch.due_date) <= %s "
        param = [",".join([str(x) for x in domain_ids]), from_date, to_date]

    q += " group by " + group_by_name

    if filter_type_ids is not None :
        q += filter_type_ids
        param.append(filter_ids)

    print q % tuple(param)

    rows = db.select_all(q, param)
    print rows
    return frame_compliance_status(rows)

def get_compliance_status_chart(db, request, user_id, user_category):
    from_date = request.from_date
    to_date = request.to_date
    if from_date is not None and to_date is not None:
        result = get_compliance_status_chart_date_wise(db, request, user_id, user_category)
    else:
        result = get_compliance_status_count(db, request, user_id, user_category)

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

# Compliancce Status chart End


# Trend Chart begin
def get_trend_chart(
    db, request, user_id, user_category
):
    domain_ids = request.domain_ids
    # country_ids = request.country_ids
    filter_type = request.filter_type
    filter_ids = request.filter_ids
    where_qry_val = []

    if filter_type == "BusinessGroup":
        group_by_name = "T3.business_group_id"
        filter_type_ids = " AND find_in_set(T3.business_group_id, %s) "
        where_qry_val.append(",".join([str(x) for x in filter_ids]))

    elif filter_type == "LegalEntity":

        group_by_name = "T3.legal_entity_id"
        filter_type_ids = " AND find_in_set(T3.legal_entity_id, %s) "
        where_qry_val.append(",".join([str(x) for x in filter_ids]))

    elif filter_type == "Division":
        group_by_name = "T3.division_id"
        filter_type_ids = " AND find_in_set(T3.division_id, %s) "
        where_qry_val.append(",".join([str(x) for x in filter_ids]))

    elif filter_type == "Category" :
        group_by_name = "T3.category_id"
        filter_type_ids = " AND find_in_set(T3.category_id, %s) "
        where_qry_val.append(",".join([str(x) for x in filter_ids]))

    elif filter_type == "Unit":
        group_by_name = "T3.unit_id"
        filter_type_ids = " AND find_in_set(T3.unit_id, %s) "
        where_qry_val.append(",".join([str(x) for x in filter_ids]))

    else :
        group_by_name = "T3.country_id"
        filter_type_ids = ""

    # import from common.py
    years = get_last_7_years()
    years = years[-5:]
    print years
    # import from common.py

    if user_category <= 3 :
        tbl_name = "tbl_compliance_status_chart_unitwise"
    else :
        tbl_name = "tbl_compliance_status_chart_userwise"

    q = "select " + group_by_name + " as filter_id, t1.chart_year, sum(t1.complied_count) as comp_count, " + \
        " (sum(t1.complied_count)+sum(t1.delayed_count)+sum(t1.inprogress_count)+sum(t1.overdue_count)) as total" + \
        " from " + tbl_name + " as t1" + \
        " inner join tbl_units as T3 on t1.unit_id = T3.unit_id " + \
        " where complied_count > 0 and find_in_set(t1.chart_year, %s) and " + \
        " find_in_set(t1.domain_id, %s) " + filter_type_ids

    param = [
        ",".join([str(x) for x in years]),
        ",".join([str(x) for x in domain_ids]),
    ]
    param.extend(where_qry_val)

    if user_category > 3 :
        q += " and t1.user_id = %s"
        param.append(user_id)

    q += " group by t1.chart_year, %s "

    param.append(group_by_name)

    rows = db.select_all(q, param)
    chart_years = []
    chart_data = []

    t_filter_id = None
    for d in rows :
        t_filter_id = d["filter_id"]
        chart_years.append(d["chart_year"])
        chart_data.append(dashboard.TrendCompliedMap(
            d["filter_id"], d["chart_year"],
            int(d["total"]), int(d["comp_count"])
        ))

    if t_filter_id is not None :
        for y in years :
            if y not in chart_years :
                chart_years.append(y)
                chart_data.append(dashboard.TrendCompliedMap(t_filter_id, y, 0, 0))

    chart_data.sort(key=lambda x: x.year)
    return years, chart_data

# Trend Chart End

# Escalation Chart Begin
def get_escalation_chart(db, request, user_id, user_category):
    country_ids = request.country_ids
    domain_ids = request.domain_ids
    filter_type = request.filter_type
    years = get_last_7_years()
    years.append(getCurrentYear())
    print years
    years = years[-5:]
    years_7 = ",".join([str(x) for x in years])
    filter_ids = request.filter_ids

    if filter_type == "Group":
        filter_type_ids = None
        filter_ids = country_ids

    elif filter_type == "BusinessGroup":
        filter_type_ids = " AND find_in_set(t3.business_group_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    elif filter_type == "LegalEntity":
        filter_type_ids = " AND find_in_set(t3.legal_entity_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    elif filter_type == "Division":
        filter_type_ids = " AND find_in_set(t3.division_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    elif filter_type == "Category" :
        filter_type_ids = " AND find_in_set(t3.category_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    elif filter_type == "Unit":
        filter_type_ids = " AND find_in_set(t3.unit_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    if user_category <= 3 :
        q = "select t1.country_id, t1.domain_id, " + \
            " sum(ifnull(delayed_count, 0)) as delay_count, " + \
            " sum(ifnull(overdue_count, 0)) as over_count, " + \
            " chart_year " + \
            " from tbl_compliance_status_chart_unitwise as t1  " + \
            " inner join tbl_units as t3 on t1.unit_id = t3.unit_id " + \
            " where find_in_set(chart_year, %s) and find_in_set(t1.domain_id, %s) and find_in_set(t1.country_id, %s)"
        param = [
            years_7,
            ",".join([str(x) for x in domain_ids]),
            ",".join([str(x) for x in country_ids]),
        ]
    else :
        q = "select t1.country_id, t1.domain_id, " + \
            " sum(ifnull(delayed_count,0)) as delay_count, " + \
            " sum(ifnull(overdue_count,0)) as over_count, " + \
            " chart_year " + \
            " from tbl_compliance_status_chart_userwise as t1  " + \
            " inner join tbl_units as t3 on t1.unit_id = t3.unit_id " + \
            " where find_in_set(chart_year, %s) and user_id = %s " + \
            " and find_in_set(t1.domain_id, %s) and find_in_set(t1.country_id, %s)"
        param = [
            years_7, user_id,
            ",".join([str(x) for x in domain_ids]),
            ",".join([str(x) for x in country_ids]),
        ]
    if filter_type_ids is not None :
        q += filter_type_ids
        param.append(filter_ids)

    q += " group by chart_year"
    rows = db.select_all(q, param)

    return frame_escalation_status(rows, years)

def frame_escalation_status(data, last_years):
    years = {}
    for d in data :
        years[d["chart_year"]] = dashboard.EscalationData(
            d["chart_year"],
            0 if d["delay_count"] is None else int(d["delay_count"]),
            0 if d["over_count"] is None else int(d["over_count"])
        )

    for y in last_years :
        print y
        if years.get(y) is None :
            years[y] = dashboard.EscalationData(y, 0, 0)

    f_years = years.keys()
    f_years.sort()
    f_values = []
    for y in f_years :
        f_values.append(years.get(y))

    return dashboard.GetEscalationsChartSuccess(
        f_years, f_values
    )

# Escalation chart End

# Not Complied chart begin

def get_not_complied_count(db, request, user_id, user_category):
    country_ids = request.country_ids
    domain_ids = request.domain_ids
    d_ids = ",".join([str(x) for x in domain_ids])
    filter_type = request.filter_type
    filter_ids = request.filter_ids

    if filter_type == "Group":
        filter_type_ids = None
        filter_ids = country_ids

    elif filter_type == "BusinessGroup":
        filter_type_ids = " AND find_in_set(t3.business_group_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    elif filter_type == "LegalEntity":
        filter_type_ids = " AND find_in_set(t3.legal_entity_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    elif filter_type == "Division":
        filter_type_ids = " AND find_in_set(t3.division_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    elif filter_type == "Category" :
        filter_type_ids = " AND find_in_set(t3.category_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    elif filter_type == "Unit":
        filter_type_ids = " AND find_in_set(t3.unit_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    q = "select ch.legal_entity_id, " + \
        " sum(IF(ifnull(com.duration_type_id,0) = 2,IF(ch.due_date < now() and ifnull(ch.approve_status,0) <> 1 ,1,0), " + \
        " IF(date(ch.due_date) < curdate() and ifnull(ch.approve_status,0) <> 1 ,1,0))) as overdue_count, " + \
        " sum(IF(ifnull(com.duration_type_id,0) = 2,IF(datediff(now(),ch.due_date) <= 30 and ch.due_date < now() and ifnull(ch.approve_status,0) <> 1 ,1,0), " + \
        " IF(datediff(curdate(),ch.due_date) <= 30 and date(ch.due_date) < curdate() and ifnull(ch.approve_status,0) <> 1 ,1,0))) as 'below_30_days', " + \
        " sum(IF(ifnull(com.duration_type_id,0) = 2,IF(datediff(now(),ch.due_date) >= 31 and datediff(now(),ch.due_date) <= 60 and ch.due_date < now() and ifnull(ch.approve_status,0) <> 1 ,1,0), " + \
        " IF(datediff(curdate(),ch.due_date) >= 31 and datediff(curdate(),ch.due_date) <= 60 and date(ch.due_date) < curdate() and ifnull(ch.approve_status,0) <> 1 ,1,0))) as '31_60_days', " + \
        " sum(IF(ifnull(com.duration_type_id,0) = 2,IF(datediff(now(),ch.due_date) >= 61 and datediff(now(),ch.due_date) <= 90 and ch.due_date < now() and ifnull(ch.approve_status,0) <> 1 ,1,0), " + \
        " IF(datediff(curdate(),ch.due_date) >= 61 and datediff(curdate(),ch.due_date) <= 90 and date(ch.due_date) < curdate() and ifnull(ch.approve_status,0) <> 1 ,1,0))) as '61_90_days', " + \
        " sum(IF(ifnull(com.duration_type_id,0) = 2,IF(datediff(now(), ch.due_date) >= 91 and ch.due_date < now() and ifnull(ch.approve_status,0) <> 1 ,1,0), " + \
        " IF(datediff(curdate(), ch.due_date) >= 91 and date(ch.due_date) < curdate() and ifnull(ch.approve_status,0) <> 1 ,1,0))) as 'above_90_days' " + \
        " from tbl_compliance_history as ch " + \
        " inner join tbl_units as t3 on ch.unit_id = t3.unit_id " + \
        " inner join tbl_compliances as com on ch.compliance_id = com.compliance_id "

    if user_category > 3 :
        q += " inner join tbl_users as usr on usr.user_id = ch.completed_by " + \
            " OR usr.user_id = ch.concurred_by OR usr.user_id = ch.approved_by " + \
            " where usr.user_id = %s and find_in_set(com.domain_id, %s)"
        param = [user_id, d_ids]
    else :
        q += " where find_in_set(com.domain_id, %s)"
        param = [d_ids]

    if filter_type_ids is not None :
        q += filter_type_ids
        param.append(filter_ids)

    q += " group by ch.legal_entity_id"

    rows = db.select_one(q, param)
    print rows
    print "23232322222222222222222222222222222222222222"
    below_30 = 0
    below_60 = 0
    below_90 = 0
    above_90 = 0
    if rows :
        below_30 = 0 if rows["below_30_days"] is None else int(rows["below_30_days"])
        below_60 = 0 if rows["31_60_days"] is None else int(rows["31_60_days"])
        below_90 = 0 if rows["61_90_days"] is None else int(rows["61_90_days"])
        above_90 = 0 if rows["above_90_days"] is None else int(rows["above_90_days"])

    return dashboard.GetNotCompliedChartSuccess(
        below_30, below_60,
        below_90, above_90
    )

# Not Complied cahrt end

# Risk chart begin

def get_risk_chart_count(db, request, user_id, user_category):
    country_ids = request.country_ids
    domain_ids = request.domain_ids
    d_ids = ",".join([str(x) for x in domain_ids])
    filter_type = request.filter_type
    filter_ids = request.filter_ids

    if filter_type == "Group":
        filter_type_ids = None
        filter_ids = country_ids

    elif filter_type == "BusinessGroup":
        filter_type_ids = " AND find_in_set(t3.business_group_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    elif filter_type == "LegalEntity":
        filter_type_ids = " AND find_in_set(t3.legal_entity_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    elif filter_type == "Division":
        filter_type_ids = " AND find_in_set(t3.division_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    elif filter_type == "Category" :
        filter_type_ids = " AND find_in_set(t3.category_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    elif filter_type == "Unit":
        filter_type_ids = " AND find_in_set(t3.unit_id, %s) "
        filter_ids = ",".join([str(x) for x in filter_ids])

    u_id = user_id
    if user_category < 3 :
        u_id = None

    param = [u_id, u_id, d_ids]
    # Not opteed count
    q1 = "select count(distinct t1.client_compliance_id) as not_opt from tbl_client_compliances as t1 " + \
        " inner join tbl_units as t3 on t1.unit_id = t3.unit_id " + \
        " inner join tbl_legal_entities as le on le.legal_entity_id = t3.legal_entity_id" + \
        " left join tbl_user_units as uu on t1.unit_id = uu.unit_id " + \
        " left join tbl_user_domains as ud on ud.legal_entity_id = le.legal_entity_id and " + \
        " uu.user_id = ud.user_id and t1.domain_id = ud.domain_id " +  \
        " where t1.compliance_opted_status = 0 and if (%s is not null, uu.user_id = %s, 1) " + \
        " and find_in_set(t1.domain_id, %s) "

    param1 = param
    if filter_type_ids is not None :
        q1 += filter_type_ids
        param1.append(filter_ids)

    not_opt = db.select_one(q1, param1).get("not_opt")
    not_opt = 0 if not_opt is None else int(not_opt)
    # not complied and rejected count
    if user_category < 3 :
        q2 = " SELECT " + \
            " SUM(IF(IF(ifnull(t2.duration_type_id, 0) = 2, t1.due_date  < now(), date(t1.due_date) < CURDATE()) and ifnull(t1.approve_status, 0) not in (1, 3), 1, 0)) as not_complied, " + \
            " SUM(IF(IFNULL(t1.approve_status, 0) = 3, 1, 0)) AS rejected           " + \
            " FROM tbl_compliances AS t2  " + \
            " INNER JOIN tbl_compliance_history AS t1 ON t1.compliance_id = t2.compliance_id  " + \
            " inner join tbl_units as t3 on t1.unit_id = t3.unit_id " + \
            " where find_in_set(t2.domain_id, %s) "
        param = [d_ids]

    else :
        q2 = " SELECT " + \
            " SUM(IF(IF(ifnull(t2.duration_type_id, 0) = 2, t1.due_date  < now(), date(t1.due_date) < CURDATE()) and ifnull(t1.approve_status, 0) not in (1, 3), 1, 0)) as not_complied, " + \
            " SUM(IF(IFNULL(t1.approve_status, 0) = 3, 1, 0)) AS rejected           " + \
            " FROM tbl_compliances AS t2  " + \
            " INNER JOIN tbl_compliance_history AS t1 ON t1.compliance_id = t2.compliance_id  " + \
            " inner join tbl_units as t3 on t1.unit_id = t3.unit_id " + \
            " left join tbl_user_units as uu on uu.unit_id = t1.unit_id " + \
            " left join tbl_user_domains as ud on uu.user_id = ud.user_id and ud.domain_id = t2.domain_id " + \
            " where if (%s is not null, uu.user_id = %s, 1) and if (%s is not null, ud.user_id = %s, 1) " + \
            " and find_in_set(t2.domain_id, %s) "
        param = [u_id, u_id, u_id, u_id, d_ids]

        if user_category > 4 :
            q2 += " AND t1.completed_by = %s "
            param.append(u_id)

    param2 = param
    if filter_type_ids is not None :
        q2 += filter_type_ids
        param2.append(filter_ids)

    print q2, param2
    comp_status = db.select_one(q2, param2)
    print comp_status
    reject = comp_status.get("rejected")
    reject = 0 if reject is None else int(reject)
    not_complied = comp_status.get("not_complied")
    not_complied = 0 if not_complied is None else int(not_complied)

    if user_category == 1 :
        # unnassigned count
        q3 = " SELECT SUM(IF(ifnull(t1.compliance_opted_status, 0) = 1 AND " + \
            " IFNULL(t2.compliance_id, 0) = 0, 1, 0)) AS unassigned      FROM        " + \
            " tbl_client_compliances AS t1  " + \
            " inner join tbl_units as t3 on t1.unit_id = t3.unit_id " + \
            " LEFT JOIN tbl_assign_compliances AS t2 ON t1.compliance_id = t2.compliance_id and t1.domain_id = t2.domain_id   " + \
            " AND t1.unit_id = t2.unit_id  " + \
            " where find_in_set(t1.domain_id, %s) "
        param = [d_ids]
    elif user_category in (2, 3) :
        # unnassigned count
        q3 = " SELECT SUM(IF(ifnull(t1.compliance_opted_status, 0) = 1 AND " + \
            " IFNULL(t2.compliance_id, 0) = 0, 1, 0)) AS unassigned      FROM        " + \
            " tbl_client_compliances AS t1  " + \
            " inner join tbl_units as t3 on t1.unit_id = t3.unit_id " + \
            " LEFT JOIN tbl_assign_compliances AS t2 ON t1.compliance_id = t2.compliance_id and t1.domain_id = t2.domain_id   " + \
            " AND t1.unit_id = t2.unit_id  " + \
            " inner join tbl_user_domains as ud on t1.legal_entity_id = ud.legal_entity_id and ud.domain_id = t1.domain_id" + \
            " where ud.user_id = %s and find_in_set(t1.domain_id, %s) "
        param = [u_id, d_ids]
    elif user_category > 3 :
        # unnassigned count
        q3 = " SELECT SUM(IF(ifnull(t1.compliance_opted_status, 0) = 1 AND " + \
            " IFNULL(t2.compliance_id, 0) = 0, 1, 0)) AS unassigned      FROM        " + \
            " tbl_client_compliances AS t1  " + \
            " inner join tbl_units as t3 on t1.unit_id = t3.unit_id " + \
            " LEFT JOIN tbl_assign_compliances AS t2 ON t1.compliance_id = t2.compliance_id and t1.domain_id = t2.domain_id   " + \
            " AND t1.unit_id = t2.unit_id  " + \
            " inner join tbl_user_units as uu on uu.unit_id = t1.unit_id" + \
            " inner join tbl_user_domains as ud on uu.user_id = ud.user_id and ud.domain_id = t1.domain_id" + \
            " where uu.user_id = %s and find_in_set(t1.domain_id, %s) "
        param = [u_id, d_ids]

    param3 = param
    if filter_type_ids is not None :
        q3 += filter_type_ids
        param3.append(filter_ids)

    unassinged = db.select_one(q3, param3).get("unassigned")
    unassinged = 0 if unassinged is None else int(unassinged)

    return frame_risk_chart(not_opt, reject, not_complied, unassinged)

def frame_risk_chart(not_opt, reject, not_complied, unassinged):
    return dashboard.GetComplianceApplicabilityStatusChartSuccess(
        unassinged, not_opt, reject, not_complied
    )

# Risk  chart end


def get_trend_chart_drill_down(
    db, country_ids, domain_ids, filter_ids,
    filter_type, year
):

    where_qry_val = []
    if filter_type == "BusinessGroup":
        filter_type_ids = " AND find_in_set(u.business_group_id, %s) "
        where_qry_val.append(",".join([str(x) for x in filter_ids]))

    elif filter_type == "LegalEntity":
        filter_type_ids = " AND find_in_set(u.legal_entity_id, %s) "
        where_qry_val.append(",".join([str(x) for x in filter_ids]))

    elif filter_type == "Division":
        filter_type_ids = " AND find_in_set(u.division_id, %s) "
        where_qry_val.append(",".join([str(x) for x in filter_ids]))

    elif filter_type == "Category" :
        filter_type_ids = " AND find_in_set(u.category_id, %s) "
        where_qry_val.append(",".join([str(x) for x in filter_ids]))

    elif filter_type == "Unit":
        filter_type_ids = " AND find_in_set(u.unit_id, %s) "
        where_qry_val.append(",".join([str(x) for x in filter_ids]))

    else :
        filter_type_ids = ""

    query = " SELECT " + \
        " tch.compliance_id, tu.employee_code, tu.employee_name, " + \
        " tc.compliance_task, tc.compliance_description, " + \
        " tc.document_name, tc.statutory_mapping, tch.due_date, tcc.domain_id, " + \
        " u.country_id, " + \
        " (SELECT business_group_name FROM tbl_business_groups " + \
        " where business_group_id = u.business_group_id ) as business_group_name, " + \
        " (SELECT legal_entity_name FROM tbl_legal_entities " + \
        " where legal_entity_id = u.legal_entity_id ) as legal_entity_name, " + \
        " (SELECT division_name FROM tbl_divisions " + \
        " where division_id = u.division_id ) as division_name, " + \
        " (SELECT category_name FROM tbl_categories " + \
        " where category_id = u.category_id ) as category_name, " + \
        " concat(unit_code, '-', unit_name) as unit_name," + \
        " address, u.unit_id " + \
        " FROM tbl_compliance_history tch " + \
        " inner join tbl_client_compliances as tcc on tch.compliance_id = tcc.compliance_id and tch.unit_id = tcc.unit_id " + \
        "  inner join tbl_units u ON tch.unit_id = u.unit_id  INNER JOIN " + \
        " tbl_compliances tc ON tch.compliance_id = tc.compliance_id " + \
        "  inner join tbl_client_configuration as ccf on tcc.domain_id = ccf.domain_id and u.country_id = ccf.country_id " + \
        " INNER JOIN  tbl_users tu ON tch.completed_by = tu.user_id  " + \
        " WHERE " + \
        " approve_status = 1 AND " + \
        " tch.due_date >= tch.completion_date AND " + \
        " tch.due_date >= date(concat_ws('-',%s,ccf.month_from,1)) " + \
        " AND  tch.due_date <= last_day(date(concat_ws('-',if(ccf.month_to = 12, %s, %s +1),ccf.month_to,1))) " + \
        " AND find_in_set(tcc.domain_id, %s) " + filter_type_ids
    param = [
        year, year, year, ",".join([str(x) for x in domain_ids]),
    ]
    param.extend(where_qry_val)

    history_rows = db.select_all(query, param)

    trend_comp = {}
    for d in history_rows:
        unit_id = d["unit_id"]

        business_group_name = d["business_group_name"]
        legal_entity_name = d["legal_entity_name"]
        division_name = d["division_name"]
        category_name = d["category_name"]
        unit_name = d["unit_name"]
        address = d["address"]
        assignee_name = d["employee_name"]
        if d["employee_code"] is not None:
            assignee_name = "%s-%s" % (
                d["employee_code"],
                d["employee_name"]
            )
        compliance_name = d["compliance_task"]
        if d["document_name"] is not None:
            compliance_name = "%s-%s" % (
                d["document_name"],
                d["compliance_task"]
            )
        description = d["compliance_description"]
        maps = json.loads(d["statutory_mapping"])
        statutories = maps[0].split(">>")
        level_1_statutory = statutories[0]
        comp_info = dashboard.TrendCompliance(compliance_name, description, assignee_name)

        saved_trend = trend_comp.get(unit_id)
        if saved_trend is None :
            level_one = {}
            level_one[level_1_statutory] = [comp_info]
            trend_comp[unit_id] = dashboard.TrendDrillDownData(
                business_group_name, legal_entity_name, division_name, category_name,
                unit_name, address, level_one
            )
            # print trend_comp[unit_id].to_structure()
        else :
            compliances = saved_trend.compliances
            comp_map_info = compliances.get(level_1_statutory)

            if comp_map_info is None :
                compliances[level_1_statutory] = [comp_info]
            else :
                comp_map_info.append(comp_info)
                compliances[level_1_statutory] = comp_map_info

            saved_trend.compliances = compliances
            trend_comp[unit_id] = saved_trend

    return trend_comp.values()


def frame_compliance_details_query(
    db, chart_type, compliance_status, request,
    from_count, to_count, user_id, user_category, chart_year=None
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

    print chart_year
    if chart_year is not None:
        year_condition = get_client_domain_configuration(db, domain_ids, chart_year)[1]
        print year_condition
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
        year_range_qry = ""
    print year_range_qry

    where_qry = ""
    where_qry_val = []
    if compliance_status == "Inprogress":
        where_qry = " AND (IF(ifnull(T2.duration_type_id, 0) = 2, T1.due_date >= now(), T1.due_date >= curdate())) " + \
            " AND ifnull(T1.current_status, 0) < 3 "

    elif compliance_status == "Complied":
        where_qry = " AND T1.due_date >= T1.completion_date " + \
            " AND IFNULL(T1.approve_status, 0) = 1"

    elif compliance_status == "Delayed Compliance":
        where_qry = " AND T1.due_date < T1.completion_date " + \
            " AND IFNULL(T1.approve_status, 0) = 1"

    elif compliance_status == "Not Complied":
        where_qry = " AND (IF(ifnull(T2.duration_type_id, 0) = 2, T1.due_date < now(), T1.due_date < curdate())) " + \
            " AND (ifnull(T1.approve_status, 0) <> 1)"

    if filter_type == "Group":
        where_qry += " AND find_in_set(T3.country_id, %s) "

    elif filter_type == "BusinessGroup":
        where_qry += " AND find_in_set(T3.business_group_id, %s) "

    elif filter_type == "LegalEntity":
        where_qry += " AND find_in_set(T3.legal_entity_id, %s) "

    elif filter_type == "Division":
        where_qry += " AND find_in_set(T3.division_id, %s) "

    elif filter_type == "Category" :
        where_qry += " AND find_in_set(T3.category_id, %s) "

    elif filter_type == "Unit":
        where_qry += " AND find_in_set(T3.unit_id, %s) "
    if type(filter_id) is int :
        filter_id = [filter_id]

    where_qry_val.append(",".join([str(x) for x in filter_id]))

    # if chart_type != "compliance_status":

    #     where_qry += " IN %s "
    #     where_qry_val.append(tuple(filter_id))
    # else:
    #     where_qry += " = %s "
    #     where_qry_val.append(filter_id)

    if chart_type == "not_complied":
        not_complied_type = request.not_complied_type

        if not_complied_type == "Below 30":
            where_qry += " AND abs(datediff(date(now()), " + \
                " date(T1.due_date))) <= 30 "
        elif not_complied_type == "Below 60":
            where_qry += " AND abs(datediff(date(now()), " + \
                " date(T1.due_date))) BETWEEN 30 and 60 "
        elif not_complied_type == "Below 90":
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

    # if user_category > 3 :
    #     where_qry += " AND (T1.completed_by = %s " + \
    #         " OR T1.concurred_by = %s " + \
    #         " OR T1.approved_by = %s)"
    #     where_qry_val.extend([user_id, user_id, user_id])

    if user_category in (5, 6) :
        where_qry += " AND T1.completed_by = %s "
        where_qry_val.extend([user_id])

    where_qry += year_range_qry

    query = "SELECT " + \
        " T1.compliance_history_id, ifnull(T1.approve_status,0) as approval_status, T1.unit_id, " + \
        " T1.compliance_id, T1.start_date, " + \
        " T1.due_date, T1.completion_date, " + \
        " T1.completed_by as assignee, " + \
        " T2.compliance_task, T2.document_name, " + \
        " T2.compliance_description, T2.statutory_mapping, " + \
        " T2.frequency_id, T2.duration_type_id, " + \
        " unit_name, " + \
        " (select division_name from tbl_divisions " + \
        " where division_id = T3.division_id)division_name, " + \
        " (select category_name from tbl_categories " + \
        " where category_id = T3.category_id)category_name, " + \
        " (select legal_entity_name from tbl_legal_entities " + \
        " where legal_entity_id = T3.legal_entity_id)legal_entity_name, " + \
        " (select business_group_name from tbl_business_groups " + \
        " where business_group_id = T3.business_group_id) " + \
        " business_group_name, " + \
        " (select country_name from tbl_countries " + \
        " where country_id = T3.country_id)country_name, " + \
        " (select employee_name from tbl_users " + \
        " where user_id = T1.completed_by) employee_name, " + \
        " T3.unit_code, T3.address, T3.geography_name, T3.postal_code, " + \
        " T3.country_id, " + \
        " (select group_concat(distinct t1.organisation_name SEPARATOR ', ') from tbl_organisation as t1 " + \
        " inner join tbl_units_organizations as t2 on t1.organisation_id = t2.organisation_id " + \
        " where t2.unit_id = T3.unit_id) as industry_name, " + \
        " T2.domain_id, " + \
        " YEAR(T1.due_date) as year, " + \
        " MONTH(T1.due_date) as month " + \
        " FROM tbl_compliance_history T1 " + \
        " INNER JOIN tbl_compliances T2 " + \
        " ON T1.compliance_id = T2.compliance_id " + \
        " INNER JOIN tbl_units T3 ON T1.unit_id = T3.unit_id " + \
        " WHERE " + \
        " find_in_set(T2.domain_id, %s) "

    order = " ORDER BY  T1.unit_id, " + \
            " SUBSTRING_INDEX(SUBSTRING_INDEX( " + \
            " T2.statutory_mapping, '>>', 1), '>>', -1), " + \
            " T1.due_date " + \
            " limit %s, %s "

    where_qry_val.extend([from_count, 1000])
    q = "%s %s %s " % (query, where_qry, order)

    param = [",".join([str(x) for x in domain_ids])]
    param.extend(where_qry_val)

    rows = db.select_all(q, param)
    print q % tuple(param)
    # print rows
    return rows


def compliance_details_query(
    db, data, chart_type, compliance_status, from_count, to_count, user_id, user_category, chart_year=None
):
    rows = frame_compliance_details_query(
        db, chart_type, compliance_status, data, from_count, to_count, user_id, user_category, chart_year
    )

    return rows


def get_client_domain_configuration(
    db, domain_ids, current_year=None
):

    query = "SELECT distinct t1.country_id, t1.domain_id, t1.month_from, t1.month_to " + \
        " FROM  tbl_client_configuration as t1 " + \
        " inner join tbl_legal_entities as t2 on t1.country_id = t2.country_id " + \
        " WHERE find_in_set(domain_id, %s)"
    param = [",".join([str(y) for y in domain_ids])]
    rows = db.select_all(query, param)

    years_range = []
    year_condition = []
    cond = "(T3.country_id = %s " + \
        " AND T2.domain_id = %s " + \
        " AND T1.due_date >= date(concat_ws('-',%s,%s,1)) " + \
        " AND T1.due_date <= last_day(date(concat_ws('-',%s,%s,1))) )"
    for d in rows:
        info = {}
        country_id = int(d["country_id"])
        domain_id = int(d["domain_id"])
        m_from = int(d["month_from"])
        m_to = int(d["month_to"])
        info["country_id"] = country_id
        info["domain_id"] = domain_id
        year_list = calculate_years(m_from, m_to)
        years_list = []
        if current_year is None:
            years_list = year_list
        else:
            for y in year_list:
                print "years_list--", y
                if current_year == y[0]:
                    years_list.append(y)

                    if type(y) is list:
                        if len(y) == 2 :
                            y1 = y[0]
                            y2 = y[1]
                        else :
                            y1 = y[0]
                            y2 = y[0]

                    year_condition.append(
                        cond % (country_id, domain_id, y1, m_from, y2, m_to)
                    )
        if len(years_list) == 0:
            info["years"] = []
        else:
            info["years"] = years_list
        info["month_from"] = int(d["month_from"])
        info["month_to"] = int(d["month_to"])
        years_range.append(info)

    return (years_range, year_condition)


def return_compliance_details_drill_down(
    year_info, compliance_status, request_year, result
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
                month_from = int(y["month_from"])
                month_to = int(y["month_to"])
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
        mappings = json.loads(r["statutory_mapping"])
        statutories = mappings[0].split('>>')
        level_1 = statutories[0].strip()
        ageing = 0
        due_date = r["due_date"]
        completion_date = r["completion_date"]
        if due_date is None :
            continue
        if compliance_status == "Inprogress":
            if r["frequency_id"] != 5:
                ageing = abs((due_date.date() - current_date.date()).days) + 1
            else:

                if r["duration_type_id"] == 2:
                    diff = (due_date - current_date)
                    ageing = calculate_ageing_in_hours(diff)
                else:
                    diff = (due_date.date() - current_date.date())
                    ageing = diff.days
        elif compliance_status == "Complied":
            ageing = 0
        elif compliance_status == "Not Complied":
            if r["frequency_id"] != 5:
                ageing = abs((current_date.date() - due_date.date()).days) + 1
            else:
                diff = (current_date - due_date)
                if r["duration_type_id"] == 2:
                    ageing = calculate_ageing_in_hours(diff)
                else:
                    ageing = diff.days
        elif compliance_status == "Delayed Compliance":
            if completion_date is None :
                continue
            ageing = abs((completion_date - due_date).days) + 1
            if r["frequency_id"] != 5:
                ageing = abs((completion_date - due_date).days) + 1
            else:
                diff = (completion_date - due_date)
                if r["duration_type_id"] == 2:
                    ageing = calculate_ageing_in_hours(diff)
                else:
                    ageing = diff.days

        if type(ageing) is int:
            ageing = " %s Day(s)" % ageing

        status = clientcore.COMPLIANCE_STATUS(compliance_status)
        if r["document_name"] not in ("", "None", None):
            name = "%s-%s" % (r["document_name"], r["compliance_task"])
        else:
            name = r["compliance_task"]
        if r["employee_name"] is None:
            employee_name = "Administrator"
        else:
            employee_name = r["employee_name"]

        print r["approval_status"]

        if r["approval_status"] == 3 :
            ageing = "Rejected"

        compliance = dashboard.Level1Compliance(
            name, r["compliance_description"], employee_name,
            str(r["start_date"]), str(due_date),
            str(completion_date), status,
            str(ageing)
        )
        print compliance.to_structure()

        drill_down_data = unit_wise_data.get(unit_id)
        if drill_down_data is None:
            level_compliance = {}
            level_compliance[level_1] = [compliance]
            unit_name = "%s-%s" % (r["unit_code"], r["unit_name"])
            geography = r["geography_name"].split(">>")
            geography.reverse()
            geography = ','.join(geography)
            address = "%s, %s, %s" % (
                r["address"], geography, r["postal_code"]
            )
            drill_down_data = dashboard.DrillDownData(
                r["business_group_name"], r["legal_entity_name"],
                r["division_name"], r["category_name"],
                unit_name, address,
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


def get_escalation_drill_down_data(
    db, request, session_user, session_category, from_count, to_count
):
    d_ids = request.domain_ids
    year = request.year
    year_info = get_client_domain_configuration(db, d_ids)[0]

    chart_type = "excalation"
    compliance_status = "Delayed Compliance"
    delayed_details = compliance_details_query(
        db, request, chart_type, compliance_status,
        from_count, to_count, session_user, session_category, year
    )

    delayed_details_list = return_compliance_details_drill_down(
        year_info, compliance_status, year,
        delayed_details
    )

    compliance_status = "Not Complied"
    not_complied_details = compliance_details_query(
        db, request, chart_type, compliance_status,
        from_count, to_count, session_user, session_category, year
    )

    not_complied_details_list = return_compliance_details_drill_down(
        year_info, compliance_status, year,
        not_complied_details
    )

    return [delayed_details_list.values(), not_complied_details_list.values()]


def get_not_complied_drill_down(
    db, request, session_user, session_category, from_count, to_count
):
    chart_type = "not_complied"
    compliance_status = "Not Complied"
    not_complied_details_filtered = compliance_details_query(
        db, request, chart_type, compliance_status,
        from_count, to_count, session_user, session_category
    )
    current_date = datetime.datetime.today()
    unit_wise_data = {}
    for r in not_complied_details_filtered:

        unit_id = int(r["unit_id"])
        mappings = json.loads(r["statutory_mapping"])
        statutories = mappings[0].split('>>')
        level_1 = statutories[0].strip()
        ageing = 0
        due_date = r["due_date"]
        completion_date = r["completion_date"]

        if r["frequency_id"] != 5:
                ageing = abs((current_date - due_date).days) + 1
        else:
            diff = (current_date - due_date)
            if r["duration_type_id"] == 2:
                ageing = calculate_ageing_in_hours(diff)
            else:
                ageing = diff.days

        if type(ageing) is int:
            ageing = " %s Day(s)" % ageing

        status = clientcore.COMPLIANCE_STATUS("Not Complied")
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
            geography = r["geography_name"].split(">>")
            geography.reverse()
            geography = ','.join(geography)
            address = "%s, %s, %s" % (
                r["address"], geography, r["postal_code"]
            )
            drill_down_data = dashboard.DrillDownData(
                r["business_group_name"], r["legal_entity_name"],
                r["division_name"], r["category_name"], unit_name, address,
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


def make_not_opted_drill_down_query():
    q_not_opted = "select T1.compliance_id, T1.unit_id, T3.frequency_id,  " + \
        " (select frequency from tbl_compliance_frequency " + \
        " where frequency_id = T3.frequency_id) frequency, " + \
        " (select repeat_type from tbl_compliance_repeat_type " + \
        " where repeat_type_id = T3.repeats_type_id) repeats_type, " + \
        " (select duration_type from tbl_compliance_duration_type " + \
        " where duration_type_id = T3.duration_type_id)duration_type, " + \
        " T3.statutory_mapping, T3.statutory_provision, " + \
        " T3.compliance_task, T3.compliance_description, " + \
        " T3.document_name, T3.format_file, T3.format_file_size, " + \
        " T3.penal_consequences, T3.statutory_dates, " + \
        " T3.repeats_every, T3.duration, T3.is_active, " + \
        " concat(T2.unit_code, ' - ', T2.unit_name) as unit_name " + \
        " from tbl_client_compliances as T1 " + \
        " inner join tbl_units as T2 on T1.unit_id = T2.unit_id" + \
        " inner join tbl_compliances as T3 on T1.compliance_id = T3.compliance_id and" + \
        " T3.domain_id = T1.domain_id " + \
        " where T1.compliance_opted_status = 0 " + \
        " AND find_in_set(T2.country_id, %s) " + \
        " AND find_in_set(T1.domain_id, %s) "
    return q_not_opted

def make_unassigned_drill_down_query():
    q_unassigned = "select T1.compliance_id, T1.unit_id, T3.frequency_id, " + \
        " (select frequency from tbl_compliance_frequency " + \
        " where frequency_id = T3.frequency_id) frequency, " + \
        " (select repeat_type from tbl_compliance_repeat_type " + \
        " where repeat_type_id = T3.repeats_type_id) repeats_type, " + \
        " (select duration_type from tbl_compliance_duration_type " + \
        " where duration_type_id = T3.duration_type_id)duration_type, " + \
        " T3.statutory_mapping, T3.statutory_provision, " + \
        " T3.compliance_task, T3.compliance_description, " + \
        " T3.document_name, T3.format_file, T3.format_file_size, " + \
        " T3.penal_consequences, T3.statutory_dates, " + \
        " T3.repeats_every, T3.duration, T3.is_active, " + \
        " concat(T2.unit_code, ' - ', T2.unit_name) as unit_name " + \
        " from tbl_client_compliances as T1 " + \
        " left join tbl_assign_compliances as tac on T1.compliance_id = tac.compliance_id and " + \
        " T1.unit_id = tac.unit_id and T1.domain_id = tac.domain_id  " + \
        " and T1.domain_id = tac.domain_id  " + \
        " INNER JOIN tbl_units as T2 on T1.unit_id = T2.unit_id " + \
        " INNER JOIN tbl_compliances as T3 on T1.compliance_id = T3.compliance_id " + \
        " WHERE tac.compliance_id is null and find_in_set(T2.country_id, %s) " + \
        " AND find_in_set(T1.domain_id, %s) "
    return q_unassigned

def make_not_complied_drill_down_query():
    q_not_complied = "select T1.compliance_id, T1.unit_id, T3.frequency_id,  " + \
        " (select frequency from tbl_compliance_frequency " + \
        " where frequency_id = T3.frequency_id) frequency, " + \
        " (select repeat_type from tbl_compliance_repeat_type " + \
        " where repeat_type_id = T3.repeats_type_id) repeats_type, " + \
        " (select duration_type from tbl_compliance_duration_type " + \
        " where duration_type_id = T3.duration_type_id)duration_type, " + \
        " T3.statutory_mapping, T3.statutory_provision, " + \
        " T3.compliance_task, T3.compliance_description, " + \
        " T3.document_name, T3.format_file, T3.format_file_size, " + \
        " T3.penal_consequences, T3.statutory_dates, " + \
        " T3.repeats_every, T3.duration, T3.is_active, " + \
        " concat(T2.unit_code, ' - ', T2.unit_name) as unit_name " + \
        " from tbl_compliance_history as T1 " +\
        " INNER JOIN tbl_units as T2 on T1.unit_id = T2.unit_id " + \
        " INNER JOIN tbl_compliances as T3 on " + \
        " T3.compliance_id = T1.compliance_id " + \
        " where ifnull(T1.approve_status,0) != 1 and date(T1.due_date) < date(now())" + \
        " AND find_in_set(T2.country_id, %s) " + \
        " AND find_in_set(T3.domain_id, %s) "

    return q_not_complied

def make_rejected_drill_down_query():
    q_rejected = "select T1.compliance_id, T1.unit_id, T3.frequency_id,  " + \
        " (select frequency from tbl_compliance_frequency " + \
        " where frequency_id = T3.frequency_id) frequency, " + \
        " (select repeat_type from tbl_compliance_repeat_type " + \
        " where repeat_type_id = T3.repeats_type_id) repeats_type, " + \
        " (select duration_type from tbl_compliance_duration_type " + \
        " where duration_type_id = T3.duration_type_id)duration_type, " + \
        " T3.statutory_mapping, T3.statutory_provision, " + \
        " T3.compliance_task, T3.compliance_description, " + \
        " T3.document_name, T3.format_file, T3.format_file_size, " + \
        " T3.penal_consequences, T3.statutory_dates, " + \
        " T3.repeats_every, T3.duration, T3.is_active, " + \
        " concat(T2.unit_code, ' - ', T2.unit_name) as unit_name " + \
        " from tbl_compliance_history as T1 " + \
        " inner join tbl_units as T2 on T1.unit_id = T2.unit_id " + \
        " INNER JOIN tbl_compliances as T3 on " + \
        " T3.compliance_id = T1.compliance_id " + \
        " where ifnull(T1.approve_status, 0) = 3 " + \
        " AND find_in_set(T2.country_id, %s) " + \
        " AND find_in_set(T3.domain_id, %s) "

    return q_rejected


def get_compliance_applicability_drill_down(
    db, request, session_user, from_count, to_count
):

    limit = " limit %s, %s "
    country_ids = ",".join([str(x) for x in request.country_ids])
    domain_ids = ",".join([str(x) for x in request.domain_ids])

    param = [
        country_ids, domain_ids
    ]
    filter_type = request.filter_type
    filter_id = request.filter_ids

    applicability = request.applicability_status

    if filter_type == "Group":
        # filter_type_qry = "AND T3.country_id
        # IN %s" % (str(tuple(filter_ids)))
        where_type_qry = ""

    elif filter_type == "BusinessGroup":
        where_type_qry = "AND fid_in_set(T3.business_group_id, %s) "
        param.append(",".join([str(x) for x in filter_id]))

    elif filter_type == "LegalEntity":
        where_type_qry = "AND find_in_set(T3.legal_entity_id, %s) "
        param.append(",".join([str(x) for x in filter_id]))

    elif filter_type == "Division":
        where_type_qry = "AND find_in_set(T3.division_id, %s) "
        param.append(",".join([str(x) for x in filter_id]))

    elif filter_type == "Category":
        where_type_qry = "AND find_in_set(T3.category_id, %s) "
        param.append(",".join([str(x) for x in filter_id]))

    elif filter_type == "Unit":
        where_type_qry = "AND find_in_set(T3.unit_id, %s )"
        param.append(",".join([str(x) for x in filter_id]))

    query = ""
    if applicability == "Not Complied" :
        query = make_not_complied_drill_down_query()
    elif applicability == "Rejected" :
        query = make_rejected_drill_down_query()
    elif applicability == "Unassigned" :
        query = make_unassigned_drill_down_query()
    elif applicability == "Not Opted" :
        query = make_not_opted_drill_down_query()

    query1 = query + where_type_qry + limit

    param.extend([from_count, to_count])

    rows = db.select_all(query1, param)
    level_1_wise_compliance = {}

    for r in rows:
        unit_name = r["unit_name"]
        mappings = json.loads(r["statutory_mapping"])
        mappings = mappings[0].split(">>")
        if len(mappings) >= 1:
            level_1 = mappings[0]
        else:
            level_1 = mappings

        level_1 = level_1.strip()

        statutory_dates = json.loads(r["statutory_dates"])
        date_list = []
        for s in statutory_dates:
            s_date = clientcore.StatutoryDate(
                s["statutory_date"], s["statutory_month"],
                s["trigger_before_days"],
                s.get("repeat_by")
            )
            date_list.append(s_date)

        format_file = r["format_file"]
        format_file_size = r["format_file_size"]
        file_list = []
        download_file_list = None
        if format_file is not None and format_file_size is not None:
            if len(format_file) != 0:
                file_list = []
                download_file_list = []
                file_info = clientcore.FileList(
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
        elif int(r["frequency_id"]) in (2, 3, 4):
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

def get_notification_counts(db, session_user, session_category, le_ids):
    statutory = 0
    reminder = 0
    escalation = 0
    messages = 0
    le_ids_str = ','.join(str(v) for v in le_ids)

    statutory_query = "SELECT count(distinct s.notification_id) as statutory_count from tbl_statutory_notifications s " + \
                    "INNER JOIN tbl_statutory_notifications_users su ON su.notification_id = s.notification_id AND su.user_id = %s " + \
                    "AND su.is_read = 0 " + \
                    "INNER JOIN tbl_users u ON u.user_id = su.user_id " + \
                    "LEFT JOIN tbl_user_legal_entities ul ON ul.user_id = su.user_id AND find_in_set(ul.legal_entity_id , %s) "
    row = db.select_one(statutory_query, [session_user, le_ids_str])
    if row['statutory_count'] > 0:
        statutory = int(row['statutory_count'])

    reminder_query ="SELECT SUM(reminder_count) as reminder_count FROM ( " + \
                    "select sum(IF(contract_to - INTERVAL 30 DAY <= date(NOW()) and contract_to > date(now()),1,0)) as reminder_count  " + \
                    "from tbl_legal_entities as le  " + \
                    "inner join tbl_user_legal_entities as ule on ule.legal_entity_id = le.legal_entity_id  " + \
                    "where %s = 1 OR %s = 2 AND ule.user_id = %s " + \
                    "UNION ALL  " + \
                    "Select count(*) as reminder_count from tbl_notifications_log as nl  " + \
                    "inner join tbl_notifications_user_log as nlu on nl.notification_id = nlu.notification_id AND nl.notification_type_id = 2  " + \
                    "Where nlu.user_id = %s and nlu.read_status = 0 " + \
                    ") x "

    row = db.select_one(reminder_query, [session_category, session_category, session_user, session_user])
    if row['reminder_count'] > 0:
        reminder = int(row['reminder_count'])

    escalation_query =  "Select count(*) as escalation_count from tbl_notifications_log as nl " + \
                        "inner join tbl_notifications_user_log as nlu on nl.notification_id = nlu.notification_id AND nl.notification_type_id = 3 " + \
                        "Where nlu.user_id = %s and nlu.read_status = 0"
    row = db.select_one(escalation_query, [session_user])
    if row['escalation_count'] > 0:
        escalation = row['escalation_count']

    messages_query ="Select count(*) as messages_count from tbl_notifications_log as nl " + \
                    "inner join tbl_notifications_user_log as nlu on nl.notification_id = nlu.notification_id AND nl.notification_type_id = 4 " + \
                    "Where nlu.user_id = %s and nlu.read_status = 0"
    row = db.select_one(messages_query, [session_user])
    if row['messages_count'] > 0:
        messages = row['messages_count']
    notification_count = []
    notification = dashboard.NotificationsCountSuccess(statutory, reminder, escalation, messages)
    notification_count.append(notification)
    return notification_count

def get_reminders(
    db, notification_type, start_count, to_count, session_user, session_category
):

    qry = "select count(distinct le.legal_entity_id) as expire_count " + \
            "from tbl_legal_entities as le " + \
            "LEFT join tbl_user_legal_entities as ule on ule.legal_entity_id = le.legal_entity_id " + \
            "where (%s = 1 OR %s = 2) AND %s = 2 AND ule.user_id = %s " + \
            "and contract_to - INTERVAL 30 DAY <= date(NOW()) and contract_to > date(now()) "

    row = db.select_one(qry, [session_category, session_category, notification_type, session_user])

    if row["expire_count"] > 0:
        query = "(Select Distinct lg.legal_entity_id, '0' as rank,'0' as notification_id, " + \
                "concat('Your contract with Compfie for the legal entity ', legal_entity_name,' is about to expire. Kindly renew your contract to avail the services continuously.  " + \
                "Before contract expiration') as notification_text, " + \
                "nl.extra_details, " + \
                "date(contract_to - INTERVAL 30 DAY) as created_on from tbl_legal_entities as lg " + \
                "LEFT join tbl_user_legal_entities as ule on ule.legal_entity_id = lg.legal_entity_id " + \
                "INNER JOIN tbl_notifications_log as nl on nl.legal_entity_id = ule.legal_entity_id  " + \
                "AND nl.notification_type_id = %s AND nl.extra_details LIKE %s " + \
                "Where (%s = 1 OR %s = 2) AND %s = 2 AND ule.user_id = %s  " + \
                "AND contract_to - INTERVAL 30 DAY <= date(NOW()) and contract_to > date(now())) " + \
                "UNION ALL " + \
                "(Select * from (SELECT @rownum := @rownum + 1 AS rank,t1.* FROM (select nl.legal_entity_id, nl.notification_id, nl.notification_text, nl.extra_details, date(nl.created_on) as created_on " + \
                "from tbl_notifications_log as nl " + \
                "inner join tbl_notifications_user_log as nlu on nl.notification_id = nlu.notification_id and nl.notification_type_id = 2 " + \
                "Where nlu.user_id = %s AND nl.notification_type_id = %s and nlu.read_status = 0 " + \
                "order by nl.notification_id desc) as t1, (SELECT @rownum := 0) r) as t " + \
                "where t.rank >= %s and t.rank <= %s) "

        rows = db.select_all(query, [notification_type, '%closure%', session_category, session_category, notification_type, session_user, session_user,
            notification_type, start_count, to_count])
    else:
        query = "Select * from (SELECT @rownum := @rownum + 1 AS rank,t1.* FROM (select nl.legal_entity_id, nl.notification_id, nl.extra_details, nl.notification_text,date(nl.created_on) as created_on " + \
                "from tbl_notifications_log as nl " + \
                "inner join tbl_notifications_user_log as nlu on nl.notification_id = nlu.notification_id and nl.notification_type_id = 2 " + \
                "Where nlu.user_id = %s AND nl.notification_type_id = %s and nlu.read_status = 0 " + \
                "order by nl.notification_id desc) as t1, (SELECT @rownum := 0) r) as t " + \
                "where t.rank >= %s and t.rank <= %s "
        rows = db.select_all(query, [session_user, notification_type, start_count, to_count])

    notifications = []
    for r in rows :
        legal_entity_id = int(r["legal_entity_id"])
        notification_id = int(r["notification_id"])
        notification_text = r["notification_text"]
        extra_details = r["extra_details"]
        created_on = datetime_to_string(r["created_on"])
        notification = dashboard.RemindersSuccess(legal_entity_id, notification_id, notification_text, extra_details, created_on)
        notifications.append(notification)
    return notifications

def get_escalations(
    db, notification_type, start_count, to_count, session_user, session_category
):
    query = "Select * from (SELECT @rownum := @rownum + 1 AS rank,t1.* FROM (select nl.legal_entity_id, nl.notification_id, nl.notification_text, nl.extra_details, date(nl.created_on) as created_on " + \
            "from tbl_notifications_log as nl " + \
            "inner join tbl_notifications_user_log as nlu on nl.notification_id = nlu.notification_id AND nl.notification_type_id = 3 " + \
            "Where nlu.user_id = %s " + \
            "AND nl.notification_type_id = %s and nlu.read_status = 0 " + \
            "order by nl.notification_id desc) as t1, " + \
            "(SELECT @rownum := 0) r) as t " + \
            "where t.rank >= %s and t.rank <= %s "
    rows = db.select_all(query, [session_user, notification_type, start_count, to_count])
    #print rows
    notifications = []
    for r in rows :
        legal_entity_id = int(r["legal_entity_id"])
        notification_id = int(r["notification_id"])
        notification_text = r["notification_text"]
        extra_details = r["extra_details"]
        created_on = datetime_to_string(r["created_on"])
        notification = dashboard.EscalationsSuccess(legal_entity_id, notification_id, notification_text, extra_details, created_on )
        notifications.append(notification)
    return notifications

def get_messages(
    db, notification_type, start_count, to_count, session_user, session_category
):
    query = "Select * from (SELECT @rownum := @rownum + 1 AS rank,t1.* FROM (select nl.legal_entity_id, nl.notification_id, nl.notification_text, nl.extra_details, date(nl.created_on) as created_on " + \
            "from tbl_notifications_log as nl " + \
            "inner join tbl_notifications_user_log as nlu on nl.notification_id = nlu.notification_id AND nl.notification_type_id IN (3,4) " + \
            "Where nlu.user_id = %s " + \
            "AND nl.notification_type_id = %s and nlu.read_status = 0 " + \
            "order by nl.notification_id desc) as t1, " + \
            "(SELECT @rownum := 0) r) as t " + \
            "where t.rank >= %s and t.rank <= %s"
    rows = db.select_all(query, [session_user, notification_type, start_count, to_count])
    #print rows
    notifications = []
    for r in rows :
        legal_entity_id = int(r["legal_entity_id"])
        notification_id = int(r["notification_id"])
        notification_text = r["notification_text"]
        extra_details = r["extra_details"]
        created_on = datetime_to_string(r["created_on"])
        notification = dashboard.MessagesSuccess(legal_entity_id, notification_id, notification_text, extra_details, created_on)
        notifications.append(notification)
    return notifications

def update_notification_status(
    db, notification_id, session_user
):
    columns = ["read_status"]
    values = [1]
    condition = " notification_id = %s " % notification_id + " AND user_id = %s " % session_user
    db.update(
        tblNotificationUserLog, columns, values, condition
    )

def notification_detail(
    db, notification_id, session_user
):
    query = "select nl.notification_id, SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1,char_length(com.statutory_mapping) - 4),'>>',1) as act_name, " + \
            "(select concat(unit_code,' - ',unit_name) from tbl_units where unit_id = nl.unit_id) as unit, " + \
            "concat(com.document_name,' - ',com.compliance_task) as compliance_name,date(ch.due_date) as duedate, " + \
            "IF(ch.due_date < now() and ch.approve_status <> 1,concat(abs(datediff(now(),ch.due_date)),' Days'),'-') as delayed_by, " + \
            "(select concat(employee_code,'-',employee_name,' ',email_id,',',ifnull(mobile_no,'-')) from tbl_users where user_id = nl.assignee) as assignee_name, " + \
            "(select concat(employee_code,'-',employee_name,' ',email_id,',',ifnull(mobile_no,'-')) from tbl_users where user_id = nl.concurrence_person) as concur_name, " + \
            "(select concat(ifnull(employee_code, ''),'-',employee_name,' ',email_id,',',ifnull(mobile_no,'-')) from tbl_users where user_id = nl.approval_person) as approver_name " + \
            "from tbl_notifications_log as nl " + \
            "inner join tbl_compliances as com on nl.compliance_id = com.compliance_id " + \
            "inner join tbl_compliance_history as ch on nl.compliance_id = ch.compliance_id and nl.unit_id = ch.unit_id and ch.compliance_history_id = substring_index(nl.extra_details,'-',1) " + \
            "inner join tbl_notifications_user_log as nlu on nl.notification_id = nlu.notification_id " + \
            "Where nlu.user_id = %s AND nl.notification_id = %s "
    rows = db.select_all(query, [session_user, notification_id])
    notifications = []
    for r in rows :
        notification_id = int(r["notification_id"])
        act_name = r["act_name"]
        unit = r["unit"]
        compliance_name = r["compliance_name"]
        due_date = datetime_to_string(r["duedate"])
        delayed_by = r["delayed_by"]
        assignee_name = r["assignee_name"]
        concurrer_name = r["concur_name"]
        approver_name = r["approver_name"]
        notification = dashboard.NotificationDetailsSuccess(notification_id, act_name, unit, compliance_name, due_date, delayed_by,
            assignee_name, concurrer_name, approver_name)
        notifications.append(notification)
    return notifications


def get_statutory(
    db, start_count, to_count, session_user, session_category, le_ids
):
    le_ids_str = ','.join(str(v) for v in le_ids)
    query = "SELECT s.notification_id, s.compliance_id, s.notification_text, s.created_on, " + \
            "su.user_id, CONCAT(ifnull(u.employee_code,''), '', u.employee_name) as user_name " + \
            "from tbl_statutory_notifications s " + \
            "INNER JOIN tbl_statutory_notifications_users su ON su.notification_id = s.notification_id AND su.user_id = %s " + \
            "AND su.is_read = 0 " + \
            "INNER JOIN tbl_users u ON u.user_id = su.user_id " + \
            "LEFT JOIN tbl_user_legal_entities ul ON ul.user_id = su.user_id AND find_in_set(ul.legal_entity_id , %s) " + \
            "order by s.created_on DESC Limit %s, %s "

    rows = db.select_all(query, [session_user, le_ids_str, start_count, to_count])
    #print rows
    notifications = []
    for r in rows :
        notification_id = int(r["notification_id"])
        compliance_id = int(r["compliance_id"])
        notification_text = r["notification_text"]
        user_name = r["user_name"]
        created_on = datetime_to_string(r["created_on"])
        notification = dashboard.StatutorySuccess(notification_id, compliance_id, notification_text, user_name, created_on)
        notifications.append(notification)
    return notifications

def update_statutory_notification_status(db, notification_id, session_user):
    columns = ["is_read"]
    values = [1]
    condition = " notification_id = %s " % notification_id + " AND user_id = %s " % session_user
    db.update(
        tblStatutoryNotificationsUsers, columns, values, condition
    )

def statutory_notification_detail(
    db, notification_id, session_user
):
    query = "SELECT t1.compliance_id, t1.statutory_mapping_id, t1.country_id, " + \
            "t1.domain_id, t1.statutory_provision, t1.compliance_task, t1.document_name, " + \
            "t1.compliance_description, t1.penal_consequences, t1.reference_link, t1.frequency_id, " + \
            "t1.statutory_dates, t1.repeats_type_id, t1.repeats_every, t1.duration_type_id, " + \
            "t1.duration, t1.is_active, " + \
            "(select frequency from tbl_compliance_frequency where frequency_id = t1.frequency_id) as freq_name, " + \
            "(select repeat_type from tbl_compliance_repeat_type where repeat_type_id = t1.repeats_type_id) as repeat_type, " + \
            "(select duration_type from tbl_compliance_duration_type where duration_type_id = t1.duration_type_id) as duration_type " + \
            "FROM tbl_compliances as t1  " + \
            "inner join tbl_statutory_notifications as t2 on t2.compliance_id = t1.compliance_id " + \
            "where t2.notification_id = %s "
    rows = db.select_all(query, [notification_id])

    notifications = []
    for r in rows :
        if r["document_name"] is None or r["document_name"] == '':
            c_name = r["compliance_task"]
        else :
            c_name = r["document_name"] + " - " + r["compliance_task"]

        date_list = []

        statutory_dates = r["statutory_dates"]

        if statutory_dates is not None and statutory_dates != "":
            statutory_dates = json.loads(statutory_dates)

            for date in statutory_dates:
                s_date = clientcore.StatutoryDate(
                    date["statutory_date"],
                    date["statutory_month"],
                    date["trigger_before_days"],
                    date.get("repeat_by")
                )
                date_list.append(s_date)

        summary, dates, trigger = make_summary(date_list, r["frequency_id"], r)
        if summary != "" and dates is not None and dates != "" :
            summary += ' on (%s)' % (dates)

        notification = dashboard.StatutoryNotificationDetailsSuccess(
            r["compliance_id"], r["statutory_provision"], c_name, r["compliance_description"],
            r["penal_consequences"], r["freq_name"], summary, r["reference_link"])
        notifications.append(notification)
    return notifications


def get_user_company_details(db, user_id=None):
    admin_id = get_admin_id(db)
    columns = [
        "unit_id", "business_group_id", "legal_entity_id", "division_id"
    ]
    condition = " 1 "
    condition_val = None
    if user_id != admin_id:
        user_units_columns = [
            "unit_id"
        ]
        user_units_condition = "  user_id = %s"
        user_units_condition_val = [user_id]
        rows = db.get_data(
            tblUserUnits, user_units_columns,
            user_units_condition, user_units_condition_val
        )
        unit_ids = [
            int(row["unit_id"]) for row in rows
        ]
        condition, condition_val = db.generate_tuple_condition(
            "unit_id", unit_ids
        )
        condition_val = [condition_val]
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
    unit_id, session_user, assignee_id, session_category
):
    condition = "unt.country_id =  %s"
    condition_val = [country_id]
    if business_group_id is not None:
        condition += " AND unt.business_group_id = %s"
        condition_val.append(business_group_id)
    if legal_entity_id is not None:
        condition += " AND unt.legal_entity_id = %s"
        condition_val.append(legal_entity_id)
    if division_id is not None:
        condition += " AND unt.division_id = %s"
        condition_val.append(division_id)

    if unit_id is not None:
        condition += " AND unt.unit_id = %s"
        condition_val.append(unit_id)

    if assignee_id is not None:
        condition += " AND ch.completed_by = %s"
        condition_val.append(assignee_id)
    domain_ids_list = get_user_domains(db, session_user, session_category)
    current_date = get_date_time_in_date()
    result = {}

    for domain_id in domain_ids_list:
        timelines = get_country_domain_timelines(
            db, [country_id], [domain_id], [current_date.year]
        )

        if len(timelines[0][1]) == 0:
            continue
        from_date = timelines[0][1][0][1][0]["start_date"].date()
        to_date = timelines[0][1][0][1][0]["end_date"].date()

        query = "select " + \
            "     ch.completed_by, ch.unit_id,  " + \
            "     CONCAT(IFNULL(employee_code, 'Administrator'),'-',employee_name) AS assignee, " + \
            "     unit_code, unit_name, address, com.domain_id, " + \
            "     (select domain_name from tbl_domains where domain_id = com.domain_id) as domain_name, " + \
            "     sum(IF(ifnull(com.duration_type_id,0) = 2,IF(ch.due_date >= ch.completion_date and ifnull(ch.approve_status,0) = 1,1,0), " + \
            "     IF(date(ch.due_date) >= date(ch.completion_date) and ifnull(ch.approve_status,0) = 1,1,0))) as complied_count, " + \
            "     sum(IF(ifnull(com.duration_type_id,0) = 2,IF(ch.due_date < ch.completion_date and ifnull(ch.approve_status,0) = 1,1,0),  " + \
            "     IF(date(ch.due_date) < date(ch.completion_date) and ifnull(ch.approve_status,0) = 1,1,0))) as delayed_count,  " + \
            "     sum(IF(IF(ifnull(com.duration_type_id,0) = 2, ch.due_date >= now(), date(ch.due_date) >= curdate()) and ch.current_status < 3, 1, 0)) " + \
            " as inprogress_count,  " + \
            "     sum(IF(ifnull(com.duration_type_id,0) = 2,IF(ch.due_date < now() and ifnull(ch.approve_status,0) <> 1 and ifnull(ch.approve_status,0) <> 3 ,1,0),  " + \
            "     IF(date(ch.due_date) < curdate() and ifnull(ch.approve_status,0) <> 1 and ifnull(ch.approve_status,0) <> 3 ,1,0))) as overdue_count, " + \
            "     sum(iF(ch.current_status = 3 and ch.completion_date > ch.due_date and ifnull(ac.is_reassigned, 0) = 1, 1, 0)) as reassigned, " + \
            "     sum(iF(ch.current_status = 3 and ifnull(ch.approve_status, 0) = 3, 1, 0)) as rejected " + \
            " from tbl_compliance_history as ch " + \
            " inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
            " inner join tbl_assign_compliances as ac on ch.compliance_id = ac.compliance_id and " + \
            " ch.unit_id = ac.unit_id " + \
            " inner join tbl_users as usr on ch.completed_by = usr.user_id " + \
            " inner join tbl_units as unt on ch.unit_id = unt.unit_id "

        param = [domain_id, from_date, to_date]

        if unit_id is None and session_category > 3 :
            query += " inner join tbl_user_units as uu on uu.unit_id = ch.unit_id and uu.user_id = %s "
            parameter_list = [session_user] + condition_val + param
        else :
            parameter_list = condition_val + param

        query += " where " + condition + " and com.domain_id = %s and ch.due_date >= %s AND ch.due_date <= %s "

        if unit_id is not None :
            parameter_list = condition_val + param

        if session_category > 4 :
            query += " AND ch.completed_by = %s"
            parameter_list.append(session_user)

        query += " group by ch.completed_by, ch.unit_id, com.domain_id "
        rows = db.select_all(query, parameter_list)
        print "*" * 20
        print rows
        assignee_wise_compliances = rows
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

            total_compliances = (
                compliance["complied_count"] + compliance["delayed_count"] +
                compliance["inprogress_count"] + compliance["overdue_count"] + compliance["reassigned"] +
                compliance["rejected"]
            )
            delay = int(compliance["delayed_count"]) - int(compliance["reassigned"])
            if delay < 0 :
                delay = 0
            result[unit_name]["assignee_wise"][assignee]["domain_wise"].append(
                dashboard.DomainWise(
                    domain_id=domain_id,
                    domain_name=compliance["domain_name"],
                    total_compliances=int(total_compliances),
                    complied_count=int(compliance["complied_count"]),
                    assigned_count=int(delay),
                    reassigned_count=int(compliance["reassigned"]),
                    inprogress_compliance_count=int(compliance["inprogress_count"]),
                    not_complied_count=int(compliance["overdue_count"]),
                    rejected_count=int(compliance["rejected"])
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
    db, country_id, unit_id, user_id, domain_ids
):
    current_year = get_date_time_in_date().year

    # domain_ids_list = get_user_domains(db, user_id)
    domain_ids_list = domain_ids

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
                db, [country_id], [domain_id], [iter_year]
            )
            if len(result[0][1]) == 0:
                continue
            from_date = result[0][1][0][1][0]["start_date"].date()
            to_date = result[0][1][0][1][0]["end_date"].date()
            query = " SELECT tc.domain_id, " + \
                " sum(IF(IF(ifnull(tc.duration_type_id, 0) = 2, tch.due_date >= tch.completion_date, date(tch.due_date) >= date(tch.completion_date)) " + \
                " and ifnull(tch.approve_status,0) = 1, 1, 0)) as complied, " + \
                " sum(IF(IF(ifnull(tc.duration_type_id, 0) = 2, tch.due_date < tch.completion_date, date(tch.due_date) < date(tch.completion_date)) and " + \
                " ifnull(tch.approve_status,0) = 1, 1, 0)) as delayed_comp, " + \
                " sum(IF(IF(ifnull(tc.duration_type_id, 0) = 2, tch.due_date >= now(), date(tch.due_date) >= curdate()) and ifnull(tch.approve_status, 0) <> 1  " + \
                " and ifnull(tch.approve_status,0) <> 3, 1, 0)) as inprogress, " + \
                " sum(IF((IF(ifnull(tc.duration_type_id, 0) = 2, tch.due_date < now(), tch.due_date < curdate())  " + \
                " and ifnull(tch.approve_status,0) <> 1) or ifnull(tch.approve_status,0) = 3, 1, 0)) as not_complied, " + \
                " sum(case when (approve_status = 1 and " + \
                " completion_date > tch.due_date and (is_reassigned = 1)) " + \
                " then 1 else 0 end) as delayed_reassigned " + \
                " FROM tbl_compliance_history tch " + \
                " INNER JOIN tbl_assign_compliances tac ON ( " + \
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

            for row in rows:
                domainwise_complied += 0 if(
                    row["complied"] is None) else int(row["complied"])
                domainwise_inprogress += 0 if(
                    row["inprogress"] is None) else int(row["inprogress"])
                domainwise_notcomplied += 0 if(
                    row["not_complied"] is None
                ) else int(row["not_complied"])
                domainwise_delayed += 0 if(
                    row["delayed_comp"] is None) else int(row["delayed_comp"])
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
    year_wise_compliance_count = sorted(year_wise_compliance_count, key=lambda k: k.year, reverse=True)
    return year_wise_compliance_count


def get_assigneewise_reassigned_compliances(
    db, country_id, unit_id, user_id, domain_id
):
    results = fetch_assigneewise_reassigned_compliances(
        db, country_id, unit_id, user_id, domain_id
    )
    return return_reassigned_details(results)


def fetch_assigneewise_reassigned_compliances(
    db, country_id, unit_id, user_id, domain_id
):
    print country_id, unit_id, user_id, domain_id
    current_year = get_date_time_in_date().year
    result = get_country_domain_timelines(
        db, [country_id], [domain_id], [current_year]
    )
    from_date = result[0][1][0][1][0]["start_date"].date()
    to_date = result[0][1][0][1][0]["end_date"].date()
    query = " SELECT distinct trch.assigned_on as reassigned_date, concat( " + \
        " IFNULL(employee_code, 'Administrator'), '-', " + \
        " employee_name) as reassigned_from,  " + \
        " document_name, compliance_task, " + \
        " tch.due_date, DATE_SUB(tch.due_date, " + \
        " INTERVAL trigger_before_days DAY) as start_date, " + \
        " completion_date FROM tbl_reassigned_compliances_history trch " + \
        " INNER JOIN " + \
        " tbl_compliance_history tch ON ( " + \
        " trch.compliance_id = tch.compliance_id " + \
        " AND assignee= %s AND trch.unit_id = tch.unit_id) " + \
        " INNER JOIN tbl_assign_compliances tac ON ( " + \
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
        " AND completion_date >= tch.due_date AND is_reassigned = 1 "
        # " AND trch.assigned_on between CAST(tch.start_date AS DATE) " + \
        # " and CAST(completion_date AS DATE) " + \


    date_condition = " AND tch.due_date between '%s' AND '%s' "
    date_condition = date_condition % (from_date, to_date)
    query += date_condition
    print query % (user_id, user_id, unit_id, int(domain_id), user_id)
    rows = db.select_all(query, [
        user_id, user_id, unit_id, int(domain_id), user_id
    ])
    print rows
    return rows


def return_reassigned_details(results):
    reassigned_compliances = []
    for compliance in results:
        compliance_name = compliance["compliance_task"]
        if compliance["document_name"]:
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
    db, country_id, assignee_id, domain_ids, year, unit_id,
    session_user, session_category
):
    # domain_id_list = []
    # if domain_id is None:
    #     domain_id_list = get_user_domains(db, session_user)
    # else:
    #     domain_id_list = [domain_id]

    domain_id_list = domain_ids

    if year is None:
        current_year = get_date_time_in_date().year
    else:
        current_year = year
    result = get_country_domain_timelines(
        db, [country_id], domain_id_list, [current_year]
    )
    from_date = datetime.datetime(current_year, 1, 1).date()
    to_date = datetime.datetime(current_year, 12, 31).date()
    domain_condition = ",".join(str(x) for x in domain_id_list)
    if len(domain_id_list) == 1:
        result = get_country_domain_timelines(
            db, [country_id], domain_id_list, [current_year]
        )
        if len(result[0][1]) == 0 :
            return 0
        from_date = str(result[0][1][0][1][0]["start_date"])
        to_date = str(result[0][1][0][1][0]["end_date"])
        domain_condition = str(domain_id_list[0])
    query = " SELECT count(*) as cnt " + \
        " FROM tbl_compliance_history tch " + \
        " INNER JOIN tbl_compliances tc ON " + \
        " tch.compliance_id = tc.compliance_id " + \
        " INNER JOIN tbl_users tu ON tch.completed_by = tu.user_id " + \
        " WHERE completed_by = %s AND unit_id = %s " + \
        " AND due_date >= %s AND due_date <= %s " + \
        " AND find_in_set(domain_id, %s) "
    rows = db.select_one(query, [
        assignee_id, unit_id, from_date, to_date, domain_condition
    ])

    return rows["cnt"]


def get_assigneewise_compliances_drilldown_data(
    db, country_id, assignee_id, domain_ids, year, unit_id,
    start_count, to_count, session_user, session_category
):
    result = fetch_assigneewise_compliances_drilldown_data(
        db, country_id, assignee_id, domain_ids, year, unit_id,
        start_count, to_count, session_user, session_category
    )
    return return_assignee_wise_compliance_drill_down_data(result)


def fetch_assigneewise_compliances_drilldown_data(
    db, country_id, assignee_id, domain_ids, year, unit_id,
    start_count, to_count, session_user, session_category
):
    domain_id_list = domain_ids
    # if domain_id is None:
    #     domain_id_list = get_user_domains(db, session_user, session_category)
    # else:
    #     domain_id_list = [domain_id]

    if year is None:
        current_year = get_date_time_in_date().year
    else:
        current_year = year
    from_date = datetime.datetime(current_year, 1, 1)
    to_date = datetime.datetime(current_year, 12, 31)
    domain_condition = ",".join(str(x) for x in domain_id_list)
    if len(domain_id_list) == 1:
        result = get_country_domain_timelines(
            db, [country_id], domain_id_list, [current_year]
        )
        if len(result[0][1]) == 0 :
            return []
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
        "                due_date >= now() and frequency_id=5 and " + \
        "                 duration_type_id=2), " + \
        "                'On_occurrence_Inprogress', " + \
        "                ( " + \
        "                  IF( " + \
        "                       ((approve_status = 0 " + \
        "                       or approve_status is null) and " + \
        "                       due_date >= current_date and " + \
        "                        (frequency_id!=5 or (frequency_id=5 " + \
        "                          and duration_type_id!=2)))," + \
        "                       'Inprogress'," + \
        "                       ( " + \
        "                           IF( " + \
        "                               ((approve_status = 0 " + \
        "                               or approve_status is null) and " + \
        "                               due_date < now() and frequency_id=5 and " + \
        "                               duration_type_id=2)," + \
        "                               'On_occurrence_NotComplied'," + \
        "                               'NotComplied' " + \
        "                           )" + \
        "                       )" + \
        "                   )" + \
        "                )" + \
        "            ) " + \
        "        ) " + \
        "    ) " + \
        ") " + \
        ") as compliance_status"
    query = " SELECT " + \
        " compliance_id, start_date, due_date, completion_date, " + \
        " document_name, compliance_task, compliance_description, " + \
        " statutory_mapping, employee_name as assignee, compliance_status FROM ( " + \
        " SELECT %s, %s " + \
        " FROM tbl_compliance_history tch " + \
        " INNER JOIN tbl_compliances tc " + \
        " ON (tch.compliance_id = tc.compliance_id) " + \
        " INNER JOIN tbl_users tu ON (tch.completed_by = tu.user_id) "
    query = query % (columns, subquery_columns)
    where_condition = " WHERE completed_by = %s AND unit_id = %s " + \
        "  AND due_date BETWEEN %s AND %s AND domain_id in (%s) " + \
        " LIMIT %s, %s) a " + \
        " ORDER BY compliance_status "
    where_condition_val = [
        assignee_id, unit_id, from_date, to_date, domain_condition,
        int(start_count), to_count
    ]
    query = query + where_condition
    # print query % tuple(where_condition_val)
    rows = db.select_all(query, where_condition_val)
    return rows


def return_assignee_wise_compliance_drill_down_data(result):
    complied_compliances = {}
    inprogress_compliances = {}
    delayed_compliances = {}
    not_complied_compliances = {}

    for compliance in result:
        compliance_name = compliance["compliance_task"]
        compliance_status = compliance["compliance_status"]
        print "-----------------------------", compliance["document_name"]
        if compliance["document_name"]:
            compliance_name = "%s - %s" % (
                compliance["document_name"], compliance_name
            )
        maps = json.loads(compliance["statutory_mapping"])
        level_1_statutory = maps[0].split(">>")[0]

        if compliance_status == "Complied":
            current_list = complied_compliances
        elif compliance_status == "Delayed":
            current_list = delayed_compliances
        elif compliance_status in ["Inprogress", "On_occurrence_Inprogress"]:
            current_list = inprogress_compliances
        elif compliance_status in ["NotComplied", "On_occurrence_NotComplied"]:
            current_list = not_complied_compliances
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


def notify_expiration(db):
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


def get_no_of_days_left_for_contract_expiration(db):
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
            notify_expiration(db)
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
        r = relativedelta.relativedelta(
            convert_datetime_to_date(current_date),
            convert_datetime_to_date(created_on)
        )
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
