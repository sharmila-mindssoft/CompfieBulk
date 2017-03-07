
import datetime
from clientprotocol import (widgetprotocol)
from server.clientdatabase.common import (get_last_7_years)

def getCurrentYear():
    now = datetime.datetime.now()
    return now.year

def getCurrentMonth():
    now = datetime.datetime.now()
    return now.month

def getDayName(date):
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    dayNumber = date.weekday()
    return days[dayNumber]

def getFirstDate():
    now = datetime.date.today().replace(day=1)
    return now

def totalDays():
    thismonth = getFirstDate()
    nextmonth = thismonth.replace(month=getCurrentMonth()+1)
    return (nextmonth - thismonth).days

def currentDay():
    return datetime.datetime.now().day

# Compliance Status chart groupwise count

def get_compliance_status_count(db, le_ids, user_id, user_category):
    if user_category <= 3 :
        q = "select t1.country_id, t2.country_name, sum(ifnull(complied_count, 0)) as comp_count, " + \
            " sum(ifnull(delayed_count, 0)) as delay_count, " + \
            " sum(ifnull(inprogress_count, 0)) as inp_count, sum(ifnull(overdue_count, 0)) as over_count" + \
            " from tbl_compliance_status_chart_unitwise as t1  " + \
            " inner join tbl_countries as t2 on t1.country_id = t2.country_id " + \
            " where chart_year = %s"
        param = [getCurrentYear()]
    else :
        q = "select t1.country_id, t2.country_name, sum(ifnull(complied_count, 0)) as comp_count, sum(ifnull(delayed_count,0)) as delay_count, " + \
            " sum(ifnull(inprogress_count,0)) as inp_count, sum(ifnull(overdue_count,0)) as over_count" + \
            " from tbl_compliance_status_chart_userwise as t1  " + \
            " inner join tbl_countries as t2 on t1.country_id = t2.country_id " + \
            " where chart_year = %s and user_id = %s"
        param = [getCurrentYear(), user_id]

    rows = db.select_all(q, param)
    return frame_compliance_status(rows)

def frame_compliance_status(data) :
    chart_title = "Compliance Status"
    xaxis_name = "Countries"
    yaxis_name = "Total Compliances"
    xaxis = []
    yaxis = ["Complied", "Delayed Compliance ", "Inprogress", "Not Complied"]
    chartdata = []
    complied_data = []
    delayed_data = []
    not_complied_data = []
    inprogress_data = []
    d = data[0]
    if d["country_id"] is not None :
        xaxis.append(d["country_name"])
        complied_data.append({"y": int(d["comp_count"]) if d["comp_count"] is not None else 0})
        not_complied_data.append({"y": int(d["over_count"]) if d["over_count"] is not None else 0})
        inprogress_data.append({"y": int(d["inp_count"]) if d["inp_count"] is not None else 0})
        delayed_data.append({"y": int(d["delay_count"]) if d["delay_count"] is not None else 0})

    chartdata.append({
        "name": yaxis[0],
        "data": complied_data
    })
    chartdata.append({
        "name": yaxis[1],
        "data": delayed_data
    })
    chartdata.append({
        "name": yaxis[2],
        "data": inprogress_data
    })
    chartdata.append({
        "name": yaxis[3],
        "data": not_complied_data
    })

    return widgetprotocol.ChartSuccess(chart_title, xaxis_name, xaxis, yaxis_name, yaxis, chartdata)

# Escalation chart groupwise count
def get_escalation_count(db, le_ids, user_id, user_category):
    years = get_last_7_years()
    years.append(getCurrentYear())

    if user_category <= 3 :
        q = "select chart_year, " + \
            " sum(ifnull(delayed_count, 0)) as delay_count, " + \
            " sum(ifnull(overdue_count, 0)) as over_count" + \
            " from tbl_compliance_status_chart_unitwise as t1  " + \
            " where find_in_set(chart_year, %s)" + \
            " group by chart_year"

        param = [",".join([str(x) for x in years])]
    else :
        q = "select chart_year, sum(ifnull(delayed_count,0)) as delay_count, " + \
            " sum(ifnull(overdue_count,0)) as over_count" + \
            " from tbl_compliance_status_chart_userwise as t1  " + \
            " where find_in_set(chart_year, %s) and user_id = %s"

        param = [",".join([str(x) for x in years]), user_id]

    rows = db.select_all(q, param)
    return frame_escalation_count(rows, years)

def frame_escalation_count(data, years):
    chart_title = "Escalation"
    xaxis_name = "Years"
    xaxis = []
    yaxis_name = "Total Compliances"
    yaxis = []

    delayed = []
    not_complied = []

    for y in years :
        xaxis.append(str(y))
        delayed.append(
            {
                "y": 0,
                "year": str(y)
            }
        )
        not_complied.append(
            {
                "y": 0,
                "year": str(y)
            }
        )

    for d in data :
        y = str(d["chart_year"])
        yaxis.append(y)
        for idx, y1 in enumerate(years) :
            if str(y) == str(y1) :
                delayed[idx]["y"] += int(d["delay_count"]) if d["delay_count"] is not None else 0
                not_complied[idx]["y"] += int(d["over_count"]) if d["over_count"] is not None else 0

    chartdata = []
    chartdata.append(
        {
            "name": "Delayed Compliances",
            "data": delayed
        }
    )
    chartdata.append(
        {
            "name": "Not Complied",
            "data": not_complied
        }
    )

    return widgetprotocol.ChartSuccess(
        chart_title, xaxis_name, xaxis, yaxis_name, yaxis, chartdata
    )

# Risk chart groupwise count

def get_risk_chart_count(db, user_id, user_category):
    q = "select ifnull(ch.not_complied,0) as not_comp, ifnull(ch.rejected,0) as reject, ifnull(cc.not_opted,0) as not_opt, ifnull(cc.unassigned,0) as unassign from ( " + \
        " (select " + \
        " sum(IF(t2.frequency_id = 5,IF(t1.due_date < now() and ifnull(t1.approve_status,0) <> 1 ,1,0), " + \
        " IF(date(t1.due_date) < curdate() and ifnull(t1.approve_status,0) <> 1 ,1,0))) as not_complied, " + \
        " sum(if(ifnull(t1.approve_status, 0) = 3, 1, 0)) as rejected " + \
        " from tbl_compliance_history as t1 " + \
        " inner join tbl_compliances as t2 on t1.compliance_id = t2.compliance_id) as ch, " + \
        " (select sum(IF(ifnull(t1.compliance_opted_status, 0) = 0 , 1, 0)) as not_opted, " + \
        " sum(IF(ifnull(t1.compliance_opted_status, 0) and t2.compliance_id is null = 1, 1, 0)) as unassigned " + \
        " from tbl_client_compliances as t1  " + \
        " left join tbl_assign_compliances as t2 " + \
        " on t1.compliance_id = t2.compliance_id ) as cc)"
    param = []

    if user_category > 3 :
        q = "select ifnull(ch.not_complied,0) as not_comp, ifnull(ch.rejected,0) as reject, ifnull(cc.not_opted,0) as not_opt, ifnull(cc.unassigned,0) as unassign from ( " + \
            " (select " + \
            " sum(IF(t2.frequency_id = 5,IF(t1.due_date < now() and ifnull(t1.approve_status,0) <> 1 ,1,0), " + \
            " IF(date(t1.due_date) < curdate() and ifnull(t1.approve_status,0) <> 1 ,1,0))) as not_complied, " + \
            " sum(if(ifnull(t1.approve_status, 0) = 3, 1, 0)) as rejected " + \
            " from tbl_compliance_history as t1 " + \
            " inner join tbl_compliances as t2 on t1.compliance_id = t2.compliance_id " + \
            " inner join tbl_user_units as t3 on t1.unit_id = t3.unit_id " + \
            " inner join tbl_user_domains as t4 on t3.user_id = t4.user_id where t4.user_id = %s " + \
            " ) as ch, " + \
            " (select sum(IF(ifnull(t1.compliance_opted_status, 0) = 0 , 1, 0)) as not_opted, " + \
            " sum(IF(ifnull(t1.compliance_opted_status, 0) and t2.compliance_id is null = 1, 1, 0)) as unassigned " + \
            " from tbl_client_compliances as t1  " + \
            " left join tbl_assign_compliances as t2 " + \
            " on t1.compliance_id = t2.compliance_id  " + \
            " inner join tbl_user_units as t3 on t1.unit_id = t3.unit_id " + \
            " inner join tbl_user_domains as t4 on t3.user_id = t4.user_id where t4.user_id = %s " + \
            " ) as cc)"
        param = [user_id, user_id]
    rows = db.select_one(q, param)
    return frame_risk_chart(rows)

def frame_risk_chart(data):
    chart_title = "Risk Chart"
    xaxis_name = "Years"
    xaxis = []
    yaxis_name = "Total Compliances"
    yaxis = []
    chartData = []
    if data :
        chartData.append({
            "name": "Not Complied",
            "y": int(data["not_comp"])
        })
        chartData.append({
            "name": "Rejected",
            "y": int(data["reject"])
        })
        chartData.append({
            "name": "Unassigned",
            "y": int(data["unassign"])
        })
        chartData.append({
            "name": "Not Opted",
            "y": int(data["not_opt"])
        })

    return widgetprotocol.ChartSuccess(chart_title, xaxis_name, xaxis, yaxis_name, yaxis, chartData)

# Trend chart groupwise count
def get_trend_chart(db, user_id, user_category):
    years = get_last_7_years()
    if user_category <= 3 :
        q = "select chart_year, t1.country_id, c.country_name, ifnull(sum(complied_count), 0) as comp_count, " + \
            " (sum(complied_count)+sum(delayed_count)+sum(inprogress_count)+sum(overdue_count)) as total" + \
            " from tbl_compliance_status_chart_unitwise as t1 " + \
            " inner join tbl_countries as c on c.country_id = t1.country_id " +\
            " where find_in_set(chart_year, %s) " + \
            " group by chart_year "
        param = [",".join([str(x) for x in years])]

    else :
        q = "select chart_year, t1.country_id, c.country_name, ifnull(sum(complied_count), 0) as comp_count, " + \
            " (sum(complied_count)+sum(delayed_count)+sum(inprogress_count)+sum(overdue_count)) as total" + \
            " from tbl_compliance_status_chart_userwise as t1 " + \
            " inner join tbl_countries as c on c.country_id = t1.country_id " +\
            " where find_in_set(chart_year, %s) and user_id = %s " + \
            " group by chart_year "
        param = [",".join([str(x) for x in years]), user_id]

    rows = db.select_all(q, param)
    return frame_trend_chart(rows)

def frame_trend_chart(data):
    chart_title = "Trend Chart"
    xaxis_name = "Years"
    xaxis = []
    yaxis_name = "Total Compliances"
    yaxis = []
    chartData = []
    trend_data = []
    total_count = []
    for d in data :
        xaxis.append(str(d["chart_year"]))
        total_count.append(int(d["total"]))
        trend_data.append({
            "y": int(d["comp_count"]),
            "t": int(d["total"]),
            "year": d["chart_year"]
        })

    if data :
        chartData.append({
            "name": data[0]["country_name"],
            "data": trend_data,
            "total": total_count
        })
    return widgetprotocol.ChartSuccess(chart_title, xaxis_name, xaxis, yaxis_name, yaxis, chartData)

# Not complied Chart
def get_not_complied_count(db, user_id, user_category):
    q = "select ch.legal_entity_id, " + \
        " sum(IF(com.frequency_id = 5,IF(ch.due_date < now() and ifnull(ch.approve_status,0) <> 1 ,1,0), " + \
        " IF(date(ch.due_date) < curdate() and ifnull(ch.approve_status,0) <> 1 ,1,0))) as overdue_count, " + \
        " sum(IF(com.frequency_id = 5,IF(datediff(now(),ch.due_date) <= 30 and ch.due_date < now() and ifnull(ch.approve_status,0) <> 1 ,1,0), " + \
        " IF(datediff(now(),ch.due_date) <= 30 and date(ch.due_date) < curdate() and ifnull(ch.approve_status,0) <> 1 ,1,0))) as 'below_30_days', " + \
        " sum(IF(com.frequency_id = 5,IF(datediff(now(),ch.due_date) >= 31 and datediff(now(),ch.due_date) <= 60 and ch.due_date < now() and ifnull(ch.approve_status,0) <> 1 ,1,0), " + \
        " IF(datediff(now(),ch.due_date) >= 31 and datediff(now(),ch.due_date) <= 60 and date(ch.due_date) < curdate() and ifnull(ch.approve_status,0) <> 1 ,1,0))) as '31_60_days', " + \
        " sum(IF(com.frequency_id = 5,IF(datediff(now(),ch.due_date) >= 31 and datediff(now(),ch.due_date) <= 60 and ch.due_date < now() and ifnull(ch.approve_status,0) <> 1 ,1,0), " + \
        " IF(datediff(now(),ch.due_date) >= 61 and datediff(now(),ch.due_date) <= 90 and date(ch.due_date) < curdate() and ifnull(ch.approve_status,0) <> 1 ,1,0))) as '61_90_days', " + \
        " sum(IF(com.frequency_id = 5,IF(datediff(ch.due_date,now()) >= 31 and datediff(ch.due_date,now()) <= 60 and ch.due_date < now() and ifnull(ch.approve_status,0) <> 1 ,1,0), " + \
        " IF(datediff(ch.due_date,now()) >= 91 and date(ch.due_date) < curdate() and ifnull(ch.approve_status,0) <> 1 ,1,0))) as 'above_90_days' " + \
        " from tbl_compliance_history as ch " + \
        " inner join tbl_compliances as com on ch.compliance_id = com.compliance_id "
    param = []
    if user_category > 3 :
        q += " inner join tbl_users as usr on usr.user_id = ch.completed_by " + \
            " OR usr.user_id = ch.concurred_by OR usr.user_id = ch.approved_by " + \
            " where usr.user_id = %s "
        param = [user_id]

    q += " group by ch.legal_entity_id"

    rows = db.select_one(q, param)
    return frame_not_complied_chart(rows)

def frame_not_complied_chart(data):
    chart_title = "Over due Compliances"
    xaxis_name = "Ageings"
    xaxis = []
    yaxis_name = "Total Compliances"
    yaxis = []
    chartData = []
    if data :
        below_30_days = data["below_30_days"]
        below_30_days = int(below_30_days) if below_30_days is not None else 0
        b_31_60_days = data["31_60_days"]
        b_31_60_days = int(b_31_60_days) if b_31_60_days is not None else 0
        b_61_90_days = data["61_90_days"]
        b_61_90_days = int(b_61_90_days) if b_61_90_days is not None else 0
        above_90_days = data["above_90_days"]
        above_90_days = int(above_90_days) if above_90_days is not None else 0

        chartData.append({
            "name": "0 - 30 days",
            "y": below_30_days
        })
        chartData.append({
            "name": "31 - 60 days",
            "y": b_31_60_days
        })
        chartData.append({
            "name": "61 - 90 days",
            "y": b_61_90_days
        })
        chartData.append({
            "name": "Above 90 days",
            "y": above_90_days
        })
    return widgetprotocol.ChartSuccess(chart_title, xaxis_name, xaxis, yaxis_name, yaxis, chartData)

def get_userwise_score_card(db, user_id):
    q = "select " + \
        " sum(IF(ifnull(ch.current_status,0) = 1 and ch.completed_by = %s,1,0)) as c_assignee, " + \
        " sum(IF(ifnull(ch.current_status,0) = 2 OR (ifnull(ch.current_status,0) = 0 and ifnull(ch.concurrence_status,0) = 2) and ch.concurred_by = %s,1,0)) as c_concur, " + \
        " sum(IF(ifnull(ch.current_status,0) = 3 OR (ifnull(ch.current_status,0) = 0 and ifnull(ch.approve_status,0) = 2) and ch.approved_by = %s,1,0)) as c_approver, " + \
        " sum(IF(com.frequency_id = 5,IF(ch.due_date >= now() and ifnull(ch.current_status, 0) = 0 and ch.completed_by = %s,1,0), " + \
        " IF(date(ch.due_date) >= curdate() and ifnull(ch.current_status,0) = 0 and ch.completed_by = %s,1,0))) as in_assignee, " + \
        " sum(IF(com.frequency_id = 5,IF(ch.due_date >= now() and ifnull(ch.current_status, 0) = 1 and ch.concurred_by = %s,1,0), " + \
        " IF(date(ch.due_date) >= curdate() and ifnull(ch.current_status,0) = 1 and ch.concurred_by = %s,1,0))) as in_concur, " + \
        " sum(IF(com.frequency_id = 5,IF(ch.due_date >= now() and ifnull(ch.current_status, 0) = 2 and ch.approved_by = %s,1,0), " + \
        " IF(date(ch.due_date) >= curdate() and ifnull(ch.current_status,0) = 2 and ch.approved_by = %s,1,0))) as in_approver, " + \
        " sum(IF(com.frequency_id = 5,IF(ch.due_date < now() and ifnull(ch.current_status, 0) = 0 and ch.completed_by = %s,1,0), " + \
        " IF(date(ch.due_date) < curdate() and ifnull(ch.current_status,0) = 0 and ch.completed_by = %s,1,0))) as ov_assignee, " + \
        " sum(IF(com.frequency_id = 5,IF(ch.due_date < now() and ifnull(ch.current_status, 0) = 1 and ch.concurred_by = %s,1,0), " + \
        " IF(date(ch.due_date) < curdate() and ifnull(ch.current_status,0) = 1 and ch.concurred_by = %s,1,0))) as ov_concur, " + \
        " sum(IF(com.frequency_id = 5,IF(ch.due_date < now() and ifnull(ch.current_status, 0) = 2 and ch.approved_by = %s,1,0), " + \
        " IF(date(ch.due_date) < curdate() and ifnull(ch.current_status,0) = 2 and ch.approved_by = %s,1,0))) as ov_approver " + \
        " from tbl_compliance_history as ch " + \
        " inner join tbl_compliances as com on ch.compliance_id = com.compliance_id; "

    rows = db.select_all(q, [
        user_id, user_id, user_id, user_id, user_id, user_id, user_id,
        user_id, user_id, user_id, user_id, user_id, user_id, user_id, user_id
    ])

    return frame_user_score_card(rows)

def frame_user_score_card(data):
    chart_title = "User Scorecard"
    xaxis_name = "Total Compliances"
    xaxis = []
    yaxis_name = "Total Compliances"
    yaxis = []
    chartData = []
    if data :
        d = data[0]
        chartData.append({
            "Role": "Completed",
            "Assingee": 0 if d["c_assignee"] is None else int(d["c_assignee"]),
            "Concur":  0 if d["c_concur"] is None else int(d["c_concur"]),
            "Approver":  0 if d["c_approver"] is None else int(d["c_approver"])
        })
        chartData.append({
            "Role": "In progress within due date",
            "Assingee":  0 if d["in_assignee"] is None else int(d["in_assignee"]),
            "Concur":  0 if d["in_concur"] is None else int(d["in_concur"]),
            "Approver":  0 if d["in_approver"] is None else int(d["in_approver"])
        })
        chartData.append({
            "Role": "In progress over due",
            "Assingee":  0 if d["ov_assignee"] is None else int(d["ov_assignee"]),
            "Concur":  0 if d["ov_concur"] is None else int(d["ov_concur"]),
            "Approver":  0 if d["ov_approver"] is None else int(d["ov_approver"])
        })

    return widgetprotocol.ChartSuccess(chart_title, xaxis_name, xaxis, yaxis_name, yaxis, chartData)

def get_domain_score_card(db, user_id, user_category_id):
    q = "select t1.domain_id, " + \
        " (select domain_name from tbl_domains where domain_id = t1.domain_id) as d_name, " + \
        "sum(IF(ifnull(t1.compliance_opted_status, 0) = 0 , 1, 0)) as not_opted, " + \
        " sum(IF(ifnull(t1.compliance_opted_status, 0) = 1, 1, 0)) as opted, " + \
        " sum(IF(ifnull(t1.compliance_opted_status, 0) = 1 and t2.compliance_id is null, 1, 0)) as unassigned " + \
        " from tbl_client_compliances as t1   " + \
        " left join tbl_assign_compliances as t2 " + \
        " on t1.compliance_id = t2.compliance_id "

    param = []
    if user_category_id > 3 :
        q += " inner join tbl_user_units as t3 on t1.unit_id = t3.unit_id " + \
            " where t3.user_id = %s"
        param = [user_id]

    rows = db.select_all(q, param)
    return frame_domain_scorecard(rows)

def frame_domain_scorecard(data):
    chart_title = "Domain Scorecard"
    xaxis_name = "Total Compliances"
    xaxis = []
    yaxis_name = "Total Compliances"
    yaxis = []
    chartData = []
    for d in data :
        if d["d_name"] is None :
            continue
        xaxis.append(d["d_name"])
        not_opted = d["not_opted"]
        not_opted = 0 if not_opted is None else int(not_opted)
        unassign = d["unassigned"]
        unassign = 0 if unassign is None else int(unassign)
        opted = d["opted"]
        opted = 0 if opted is None else int(opted)
        assigned = opted - unassign
        chartData.append({
            "d_name": d["d_name"],
            "assigned": assigned,
            "unassinged": unassign,
            "notopted": not_opted
        })

    return widgetprotocol.ChartSuccess(chart_title, xaxis_name, xaxis, yaxis_name, yaxis, chartData)

def get_calendar_view(db, user_id):
    year = getCurrentYear()
    month = getCurrentMonth()
    q = "select year, month, date, due_date_count, upcoming_count " + \
        " from tbl_calendar_view where user_id = %s and year = %s and month = %s"

    rows = db.select_all(q, [user_id, year, month])
    return frame_calendar_view(db, rows, user_id)

def get_current_inprogess_overdue(db, user_id):
    q = "select " + \
        " sum(IF(com.frequency_id = 5,IF(ch.due_date >= now() and ifnull(ch.approve_status,0) <> 1 ,1,0), " + \
        " IF(date(ch.due_date) >= curdate() and ifnull(ch.approve_status,0) <> 1 ,1,0))) as inprogress_count, " + \
        " sum(IF(com.frequency_id = 5,IF(ch.due_date < now() and ifnull(ch.approve_status,0) <> 1 ,1,0), " + \
        " IF(date(ch.due_date) < curdate() and ifnull(ch.approve_status,0) <> 1 ,1,0))) as overdue_count " + \
        " from tbl_compliance_history as ch " + \
        " inner join tbl_compliances as com on ch.compliance_id = com.compliance_id  " + \
        " inner join tbl_client_compliances as cc on ch.unit_id = cc.unit_id and cc.domain_id = com.domain_id " + \
        " and cc.compliance_id = com.compliance_id " + \
        " inner join tbl_user_units as un on un.unit_id = ch.unit_id " + \
        " where un.user_id = %s "
    rows = db.select_one(q, [user_id])
    overdue = inprogress = 0
    if rows :
        overdue = int(rows["overdue_count"]) if rows["overdue_count"] is not None else 0
        inprogress = int(rows["inprogress_count"]) if rows["inprogress_count"] is not None else 0
    return overdue, inprogress

def frame_calendar_view(db, data, user_id):
    chart_title = "Calendar View"
    xaxis_name = "Total Compliances"
    xaxis = []
    yaxis_name = "Total Compliances"
    yaxis = []
    chartData = []
    cdata = []

    for i in range(totalDays()) :
        overdue = 0
        inprogress = 0
        if i+1 == currentDay() :
            overdue, inprogress = get_current_inprogess_overdue(db, user_id)

        xaxis.append(str(i+1))
        cdata.append({
            "date": i+1,
            "overdue": overdue,
            "upcoming": 0,
            "inprogress": inprogress,
            "duedate": 0
        })
    for d in data :
        idx = xaxis.index(str(d["date"]))
        c = cdata[idx]

        duedate = d["due_date_count"]
        duedate = 0 if duedate is None else int(duedate)
        upcoming = d["upcoming_count"]
        upcoming = 0 if upcoming is None else int(upcoming)

        c["overdue"] += overdue
        c["upcoming"] += upcoming
        c["inprogress"] += inprogress
        c["duedate"] += duedate

        cdata[idx] = c

    chartData.append({
        "CurrentMonth": str(getFirstDate()),
        "StartDay": getDayName(getFirstDate()),
        "data": cdata
    })
    return widgetprotocol.ChartSuccess(chart_title, xaxis_name, xaxis, yaxis_name, yaxis, chartData)
