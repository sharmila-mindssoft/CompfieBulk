
import datetime
from clientprotocol import (widgetprotocol)
from server.clientdatabase.common import (get_last_7_years)

def getCurrentYear():
    now = datetime.datetime.now()
    return now.year


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
    yaxis = ["Inprogress", "Complied", "Delayed Compliance", "Not Complied"]
    chartdata = []
    complied_data = []
    delayed_data = []
    not_complied_data = []
    inprogress_data = []
    d = data[0]
    xaxis.append(d["country_name"])
    complied_data.append({"y": int(d["comp_count"]) if d["comp_count"] is not None else 0})
    not_complied_data.append({"y": int(d["over_count"]) if d["over_count"] is not None else 0})
    inprogress_data.append({"y": int(d["inp_count"]) if d["inp_count"] is not None else 0})
    delayed_data.append({"y": int(d["delay_count"]) if d["delay_count"] is not None else 0})

    chartdata.append({
        "name": yaxis[0],
        "data": inprogress_data
    })

    chartdata.append({
        "name": yaxis[1],
        "data": complied_data
    })
    chartdata.append({
        "name": yaxis[2],
        "data": not_complied_data
    })
    chartdata.append({
        "name": yaxis[3],
        "data": delayed_data
    })

    return widgetprotocol.GetComplianceChartSuccess(chart_title, xaxis_name, xaxis, yaxis_name, yaxis, chartdata)

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
    return frame_escalation_count(rows)

def frame_escalation_count(data):
    chart_title = "Escalation"
    xaxis_name = "Years"
    xaxis = []
    yaxis_name = "Total Compliances"
    yaxis = []

    delayed = []
    not_complied = []

    for d in data :
        year = str(d["chart_year"])
        xaxis.append(year)
        yaxis.append(year)
        delayed.append(
            {
                "y": int(d["delay_count"]) if d["delay_count"] is not None else 0,
                "year": d["chart_year"]
            }
        )
        not_complied.append(
            {
                "y": int(d["over_count"]) if d["over_count"] is not None else 0,
                "year": d["chart_year"]
            }
        )

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

    return widgetprotocol.GetEscalationChartSuccess(
        chart_title, xaxis_name, xaxis, yaxis_name, yaxis, chartdata
    )

def get_risk_chart_count(db, le_ids, user_id, user_category):
    q = "select ch.not_complied, ch.rejected, cc.not_opted, cc.unassigned from ( " + \
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
    rows = db.select_all(q, param)
    return rows

def get_trend_chart(db, le_ids, user_id, user_category):
    years = get_last_7_years()
    if user_category <= 3 :
        q = "select chart_year, sum(complied_count) as comp_count, " + \
            " (sum(complied_count)+sum(delayed_count)+sum(inprogress_count)+sum(overdue_count)) as total" + \
            " from tbl_compliance_status_chart_unitwise " + \
            " where find_in_set(chart_year, %s) " + \
            " group by chart_year "
        param = [",".join([str(x) for x in years])]

    else :
        q = ""
        param = []

    rows = db.select_all(q, param)
    return rows

def frame_trend_chart(data):
    return data
