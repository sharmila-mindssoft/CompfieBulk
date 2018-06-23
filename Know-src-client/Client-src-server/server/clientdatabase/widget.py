
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
    years = years[-5:]
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
            " where find_in_set(chart_year, %s) and user_id = %s" + \
            " group by chart_year"

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

    u_id = user_id
    if user_category <= 3 :
        u_id = None

    q1 = "select count(distinct t1.client_compliance_id) as not_opt from tbl_client_compliances as t1 " + \
        " left join tbl_user_units as t2 on t1.unit_id = t2.unit_id " + \
        " left join tbl_user_domains as t3 on t2.user_id = t3.user_id and t1.domain_id = t3.domain_id " +  \
        " where t1.compliance_opted_status = 0 and if (%s is not null, t2.user_id = %s, 1) "

    not_opt = db.select_one(q1, [u_id, u_id]).get("not_opt")
    not_opt = 0 if not_opt is None else int(not_opt)

    # not complied and rejected count
    if user_category <= 3 :
        q2 = " SELECT " + \
            " SUM(IF(IF(ifnull(t2.duration_type_id, 0) = 2, t1.due_date  < now(), date(t1.due_date) < CURDATE()) and ifnull(t1.approve_status, 0) not in (1, 3), 1, 0)) as not_complied, " + \
            " SUM(IF(IFNULL(t1.approve_status, 0) = 3, 1, 0)) AS rejected           " + \
            " FROM tbl_compliances AS t2  " + \
            " INNER JOIN tbl_compliance_history AS t1 ON t1.compliance_id = t2.compliance_id  " + \
            " inner join tbl_units as t3 on t1.unit_id = t3.unit_id " + \
            " where 1 =1 "
        param = []

    else :
        q2 = " SELECT " + \
            " SUM(IF(IF(ifnull(t2.duration_type_id, 0) = 2, t1.due_date  < now(), date(t1.due_date) < CURDATE()) and ifnull(t1.approve_status, 0) not in (1, 3), 1, 0)) as not_complied, " + \
            " SUM(IF(IFNULL(t1.approve_status, 0) = 3, 1, 0)) AS rejected           " + \
            " FROM tbl_compliances AS t2  " + \
            " INNER JOIN tbl_compliance_history AS t1 ON t1.compliance_id = t2.compliance_id  " + \
            " inner join tbl_units as t3 on t1.unit_id = t3.unit_id " + \
            " left join tbl_user_units as uu on uu.unit_id = t1.unit_id " + \
            " left join tbl_user_domains as ud on uu.user_id = ud.user_id and ud.domain_id = t2.domain_id " + \
            " where if (%s is not null, uu.user_id = %s, 1) and if (%s is not null, ud.user_id = %s, 1) "

        param = [u_id, u_id, u_id, u_id]

        if user_category > 4 :
            q2 += " AND t1.completed_by = %s "
            param.append(u_id)

    param2 = param

    print q2, param2
    comp_status = db.select_one(q2, param2)
    print comp_status

    reject = comp_status.get("rejected")
    reject = 0 if reject is None else int(reject)
    not_complied = comp_status.get("not_complied")
    not_complied = 0 if not_complied is None else int(not_complied)

    if user_category <= 3 :
        # unnassigned count
        q3 = " SELECT SUM(IF(ifnull(t1.compliance_opted_status, 0) = 1 AND " + \
            " IFNULL(t2.compliance_id, 0) = 0, 1, 0)) AS unassigned      FROM        " + \
            " tbl_client_compliances AS t1  " + \
            " inner join tbl_units as t3 on t1.unit_id = t3.unit_id " + \
            " LEFT JOIN tbl_assign_compliances AS t2 ON t1.compliance_id = t2.compliance_id and t1.domain_id = t2.domain_id   " + \
            " AND t1.unit_id = t2.unit_id  "
        param = []

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
            " where uu.user_id = %s "
        param = [u_id]

    unassinged = db.select_one(q3, param).get("unassigned")
    unassinged = 0 if unassinged is None else int(unassinged)

    return frame_risk_chart(not_opt, reject, not_complied, unassinged)

def frame_risk_chart(not_opt, reject, not_complied, unassinged):
    chart_title = "Risk Chart"
    xaxis_name = "Years"
    xaxis = []
    yaxis_name = "Total Compliances"
    yaxis = []
    chartData = []
    chartData.append({
        "name": "Rejected",
        "y": reject,
        "visible": False if reject == 0 else True
    })
    chartData.append({
        "name": "Not Complied",
        "y": not_complied,
        "visible": False if not_complied == 0 else True
    })
    chartData.append({
        "name": "Unassigned",
        "y": unassinged,
        "visible": False if unassinged == 0 else True
    })
    chartData.append({
        "name": "Not Opted",
        "y": not_opt,
        "visible": False if not_opt == 0 else True
    })

    return widgetprotocol.ChartSuccess(chart_title, xaxis_name, xaxis, yaxis_name, yaxis, chartData)

# Trend chart groupwise count
def get_trend_chart(db, user_id, user_category):
    years = get_last_7_years()
    years = years[-5:]
    print "years---", years
    if user_category <= 3 :
        q = "select chart_year, t1.country_id, c.country_name, ifnull(sum(complied_count), 0) as comp_count, " + \
            " (sum(complied_count)+sum(delayed_count)+sum(inprogress_count)+sum(overdue_count)) as total" + \
            " from tbl_compliance_status_chart_unitwise as t1 " + \
            " inner join tbl_countries as c on c.country_id = t1.country_id " +\
            " where complied_count > 0 and find_in_set(chart_year, %s) " + \
            " group by chart_year "
        param = [",".join([str(x) for x in years])]

    else :
        q = "select chart_year, t1.country_id, c.country_name, ifnull(sum(complied_count), 0) as comp_count, " + \
            " (sum(complied_count)+sum(delayed_count)+sum(inprogress_count)+sum(overdue_count)) as total" + \
            " from tbl_compliance_status_chart_userwise as t1 " + \
            " inner join tbl_countries as c on c.country_id = t1.country_id " +\
            " where complied_count > 0 and find_in_set(chart_year, %s) and user_id = %s " + \
            " group by chart_year "
        param = [",".join([str(x) for x in years]), user_id]

    rows = db.select_all(q, param)
    return frame_trend_chart(years, rows)

def frame_trend_chart(years, data):
    print years
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

    for y in years :
        if str(y) not in xaxis :
            xaxis.append(str(y))
            trend_data.append({
                "y": 0,
                "t": 0,
                "year": y
            })

    trend_data.sort(key=lambda x: x["year"])
    xaxis.sort();
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

def get_userwise_score_card(db, user_id, user_category):
    q = "select " + \
        " sum(IF(ifnull(ch.current_status,0) = 1 and ch.completed_by = %s,1,0)) as c_assignee, " + \
        " sum(IF(ifnull(ch.current_status,0) = 2 and ifnull(ch.concurred_by,0) = %s OR (ifnull(ch.current_status,0) = 0 and ifnull(ch.concurrence_status,0) = 2) ,1,0)) as c_concur, " + \
        " sum(IF(ifnull(ch.approved_by,0) = %s and ifnull(ch.current_status,0) = 3 OR (ifnull(ch.current_status,0) = 0 and ifnull(ch.approve_status,0) = 2 and ifnull(ch.approved_by,0) = %s) ,1,0)) as c_approver, " + \
        " sum(IF(ifnull(com.duration_type_id,0) = 2,IF(ch.due_date >= now() and ifnull(ch.current_status, 0) = 0 and ch.completed_by = %s,1,0), " + \
        " IF(date(ch.due_date) >= curdate() and ifnull(ch.current_status,0) = 0 and ch.completed_by = %s,1,0))) as in_assignee, " + \
        " sum(IF(ifnull(com.duration_type_id,0) = 2,IF(ch.due_date >= now() and ifnull(ch.current_status, 0) = 1 and ifnull(ch.concurred_by,0) = %s,1,0), " + \
        " IF(date(ch.due_date) >= curdate() and ifnull(ch.current_status,0) = 1 and ifnull(ch.concurred_by,0) = %s,1,0))) as in_concur, " + \
        " sum(IF(ifnull(com.duration_type_id,0) = 2,IF(ch.due_date >= now() and ifnull(ch.current_status, 0) = 2 and ch.approved_by = %s,1,0), " + \
        " IF(date(ch.due_date) >= curdate() and ifnull(ch.current_status,0) = 2 and ch.approved_by = %s,1,0))) as in_approver, " + \
        " sum(IF(ifnull(com.duration_type_id,0) = 2,IF(ch.due_date < now() and ifnull(ch.current_status, 0) = 0 and ch.completed_by = %s,1,0), " + \
        " IF(date(ch.due_date) < curdate() and ifnull(ch.current_status,0) = 0 and ch.completed_by = %s,1,0))) as ov_assignee, " + \
        " sum(IF(ifnull(com.duration_type_id,0) = 2,IF(ch.due_date < now() and ifnull(ch.current_status, 0) = 1 and ifnull(ch.concurred_by,0) = %s,1,0), " + \
        " IF(date(ch.due_date) < curdate() and ifnull(ch.current_status,0) = 1 and ifnull(ch.concurred_by,0) = %s,1,0))) as ov_concur, " + \
        " sum(IF(ifnull(com.duration_type_id,0) = 2,IF(ch.due_date < now() and ifnull(ch.current_status, 0) = 2 and ch.approved_by = %s,1,0), " + \
        " IF(date(ch.due_date) < curdate() and ifnull(ch.current_status,0) = 2 and ch.approved_by = %s,1,0))) as ov_approver " + \
        " from tbl_compliance_history as ch " + \
        " inner join tbl_compliances as com on ch.compliance_id = com.compliance_id; "

    rows = db.select_all(q, [
        user_id, user_id, user_id, user_id, user_id, user_id, user_id, user_id,
        user_id, user_id, user_id, user_id, user_id, user_id, user_id, user_id
    ])

    print q % (
        user_id, user_id, user_id, user_id, user_id, user_id, user_id, user_id,
        user_id, user_id, user_id, user_id, user_id, user_id, user_id, user_id
    )
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

    param = []
    if user_category_id > 3 :
        q = "select distinct t1.domain_id, " + \
            " (select domain_name from tbl_domains where domain_id = t1.domain_id) as d_name, " + \
            " sum(IF(t1.compliance_opted_status = 0, 1, 0)) as not_opted, " + \
            " sum(IF(ifnull(t1.compliance_opted_status, 0) = 1, 1, 0)) as opted, " + \
            " sum(IF(ifnull(t1.compliance_opted_status, 0) = 1 and ifnull(t2.compliance_id, 0) = 0, 1, 0)) as unassigned, " + \
            " (IFNULL(csu.complied_count, 0) + IFNULL(csu.delayed_count, 0) + " + \
            " IFNULL(csu.inprogress_count, 0) + IFNULL(csu.overdue_count, 0)) as assigned_count " + \
            " from tbl_client_compliances as t1   " + \
            " left join tbl_assign_compliances as t2 " + \
            " on t1.compliance_id = t2.compliance_id and t1.unit_id = t2.unit_id and t1.domain_id = t2.domain_id " + \
            " inner join tbl_user_domains as t3 on t1.domain_id = t3.domain_id and t1.legal_entity_id = t3.legal_entity_id " + \
            " inner join tbl_user_units as t4 on t4.unit_id = t1.unit_id and t4.legal_entity_id =  t3.legal_entity_id " + \
            " left join (select sum(inprogress_count) as inprogress_count,sum(overdue_count) as overdue_count, " + \
            " sum(delayed_count) as delayed_count,sum(complied_count) as complied_count,domain_id,legal_entity_id, " + \
            " date(concat_ws('-',chart_year,month_from,1)) as from_date,last_day(date(concat_ws('-',chart_year,month_to,1))) as to_date " + \
            " From tbl_compliance_status_chart_unitwise " + \
            " where utc_date() >= date(concat_ws('-',chart_year,month_from,1)) " + \
            " and utc_date() <= (if(month_from > 1,last_day(date(concat_ws('-',(chart_year+1),month_to,1))), " + \
            " last_day(date(concat_ws('-',chart_year,month_to,1))))) " + \
            " group by domain_id " + \
            " ) as csu on t2.legal_entity_id = csu.legal_entity_id and t2.domain_id = csu.domain_id " + \
            " where t3.user_id = %s and t4.user_id = %s"
        param = [user_id, user_id]
    else :
        q = "select distinct t1.domain_id, " + \
            " (select domain_name from tbl_domains where domain_id = t1.domain_id) as d_name, " + \
            " sum(IF(t1.compliance_opted_status = 0, 1, 0)) as not_opted, " + \
            " sum(IF(ifnull(t1.compliance_opted_status, 0) = 1, 1, 0)) as opted, " + \
            " sum(IF(ifnull(t1.compliance_opted_status, 0) = 1 and ifnull(t2.compliance_id, 0) = 0, 1, 0)) as unassigned, " + \
            " (IFNULL(csu.complied_count, 0) + IFNULL(csu.delayed_count, 0) + " + \
            " IFNULL(csu.inprogress_count, 0) + IFNULL(csu.overdue_count, 0)) as assigned_count " + \
            " from tbl_client_compliances as t1   " + \
            " left join tbl_assign_compliances as t2 " + \
            " on t1.compliance_id = t2.compliance_id and t1.unit_id = t2.unit_id and t1.domain_id = t2.domain_id " + \
            " left join (select sum(inprogress_count) as inprogress_count,sum(overdue_count) as overdue_count, " + \
            " sum(delayed_count) as delayed_count,sum(complied_count) as complied_count,domain_id,legal_entity_id, " + \
            " date(concat_ws('-',chart_year,month_from,1)) as from_date,last_day(date(concat_ws('-',chart_year,month_to,1))) as to_date " + \
            " From tbl_compliance_status_chart_unitwise " + \
            " where utc_date() >= date(concat_ws('-',chart_year,month_from,1)) " + \
            " and utc_date() <= (if(month_from > 1,last_day(date(concat_ws('-',(chart_year+1),month_to,1))), " + \
            " last_day(date(concat_ws('-',chart_year,month_to,1))))) " + \
            " group by domain_id " + \
            " ) as csu on t2.legal_entity_id = csu.legal_entity_id and t2.domain_id = csu.domain_id "

    q += " group by t1.domain_id"

    print q % tuple(param)
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
        # assigned = opted - unassign
        assigned = d["assigned_count"]
        assigned = 0 if assigned is None else int(assigned)
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
        " from tbl_calendar_view where user_id = %s and year = %s and month = %s " + \
        " and date >= day(now())"

    rows = db.select_all(q, [user_id, year, month])
    return frame_calendar_view(db, rows, user_id)

def get_current_inprogess_overdue(db, user_id):
    q = "select " + \
        " sum(IF(IF(ifnull(com.duration_type_id,0) = 2, ch.due_date >= now(), date(ch.due_date) >= curdate()) and ifnull(ch.approve_status, 0) <> 1  " + \
        " and ifnull(ch.approve_status,0) <> 3, 1, 0)) as inprogress_count, " + \
        " sum(IF((IF(ifnull(com.duration_type_id,0) = 2, ch.due_date < now(), ch.due_date < curdate())  " + \
        " and ifnull(ch.approve_status,0) <> 1) or ifnull(ch.approve_status,0) = 3, 1, 0)) as overdue_count " + \
        " from tbl_compliance_history as ch " + \
        " inner join tbl_compliances as com on ch.compliance_id = com.compliance_id  " + \
        " inner join tbl_client_compliances as cc on ch.unit_id = cc.unit_id and cc.domain_id = com.domain_id " + \
        " and cc.compliance_id = com.compliance_id " + \
        " inner join tbl_user_units as un on un.unit_id = ch.unit_id and un.user_id = ch.completed_by " + \
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

        if d["date"] == currentDay() :
            upcoming = 0

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
