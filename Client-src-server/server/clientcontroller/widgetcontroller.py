from clientprotocol import (widgetprotocol)
from server.clientdatabase.widget import *

__all__ = [
    "process_client_widget_requests",
    "merge_compliance_chart_widget",
    "merge_escalation_chart_widget",
    "merge_user_scorecard",
    "merge_domain_scorecard",
    "merge_risk_chart_widget",
    "merge_calendar_view"

]

def process_client_widget_requests(request, db, session_user, session_category):
    request = request.request
    le_ids = request.legal_entity_ids
    if type(request) is widgetprotocol.GetComplianceChart :
        result = get_compliance_status_count(db, le_ids, session_user, session_category)

    elif type(request) is widgetprotocol.GetEscalationChart :
        result = get_escalation_count(db, le_ids, session_user, session_category)

    elif type(request) is widgetprotocol.GetNotCompliedChart :
        result = get_not_complied_count(db, session_user, session_category)

    elif type(request) is widgetprotocol.GetRiskChart :
        result = get_risk_chart_count(db, session_user, session_category)

    elif type(request) is widgetprotocol.GetTrendChart :
        result = get_trend_chart(db, session_user, session_category)

    elif type(request) is widgetprotocol.GetUserScoreCard :
        result = get_userwise_score_card(db, session_user, session_category)

    elif type(request) is widgetprotocol.GetDomainScoreCard :
        result = get_domain_score_card(db, session_user, session_category)

    elif type(request) is widgetprotocol.GetCalendarView :
        result = get_calendar_view(db, session_user)

    return result

def merge_compliance_chart_widget(data, new_data):
    xnames = data.xaxis
    xdata = data.chart_data
    newdata = new_data.chart_data
    if len(new_data.xaxis) > 0 :
        if new_data.xaxis[0] in xnames :
            for i, k in enumerate(xnames):
                if k == new_data.xaxis[0] :
                    xdata[0]["data"][i]["y"] += newdata[0]["data"][0]["y"]
                    xdata[1]["data"][i]["y"] += newdata[1]["data"][0]["y"]
                    xdata[2]["data"][i]["y"] += newdata[2]["data"][0]["y"]
                    xdata[3]["data"][i]["y"] += newdata[3]["data"][0]["y"]
                    data.chart_data = xdata
        else :
            data.xaxis.append(new_data.xaxis[0])
            xdata[0]["data"].extend(newdata[0]["data"])
            xdata[1]["data"].extend(newdata[1]["data"])
            xdata[2]["data"].extend(newdata[2]["data"])
            xdata[3]["data"].extend(newdata[3]["data"])
            data.chart_data = xdata
    return data

def merge_escalation_chart_widget(data, new_data):
    xnames = data.xaxis
    old_delayed = data.chart_data[0]["data"]
    old_notcomplied = data.chart_data[1]["data"]

    new_delayed = new_data.chart_data[0]["data"]
    new_notcomplied = new_data.chart_data[1]["data"]

    for delay in new_delayed :
        idx = xnames.index(delay["year"])
        old_delayed[idx]["y"] += delay["y"]

    for not_comp in new_notcomplied :
        idx = xnames.index(not_comp["year"])
        old_notcomplied[idx]["y"] += not_comp["y"]

    data.chart_data[0]["data"] = old_delayed
    data.chart_data[1]["data"] = old_notcomplied
    return data

def merge_risk_chart_widget(data, new_data):

    reject = data.chart_data[0]
    not_complied = data.chart_data[1]
    unassign = data.chart_data[2]
    notopt = data.chart_data[3]

    new_reject = new_data.chart_data[0]
    new_notcomplied = new_data.chart_data[1]
    new_unassign = new_data.chart_data[2]
    new_notopt = new_data.chart_data[3]

    reject["y"] += new_reject["y"]
    reject["visible"] = False if reject["y"] == 0 else True

    not_complied["y"] += new_notcomplied["y"]
    not_complied["visible"] = False if not_complied["y"] == 0 else True

    unassign["y"] += new_unassign["y"]
    unassign["visible"] = False if unassign["y"] == 0 else True

    notopt["y"] += new_notopt["y"]
    notopt["visible"] = False if notopt["y"] == 0 else True

    data.chart_data = [reject, not_complied, unassign, notopt]
    return data


def merge_user_scorecard(data, new_data):
    def merge_data(idx, x, y) :
        x = x[idx]
        x["Assingee"] += int(y[idx]["Assingee"])
        x["Concur"] += int(y[idx]["Concur"])
        x["Approver"] += int(y[idx]["Approver"])
        return x

    completed = merge_data(0, data.chart_data, new_data.chart_data)
    inprogress = merge_data(1, data.chart_data, new_data.chart_data)
    overdue = merge_data(2, data.chart_data, new_data.chart_data)

    data.chart_data = [completed, inprogress, overdue]
    return data

def merge_domain_scorecard(data, new_data):
    new_xaxis = new_data.xaxis
    old_xaxis = data.xaxis

    for idx, val in enumerate(new_xaxis) :
        if val in old_xaxis :
            old = old_xaxis.index(val)
            old_data = data.chart_data[old]
            new = new_data.chart_data[idx]
            old_data["assigned"] += new["assigned"]
            old_data["unassinged"] += new["unassinged"]
            old_data["notopted"] += new["notopted"]
            data.chart_data[old] = old_data
        else :
            data.chart_data.append(new_data.chart_data[idx])
    return data

def merge_calendar_view(data, new_data):
    new_xaxis = new_data.xaxis
    old_xaxis = data.xaxis
    for idx, val in enumerate(new_xaxis) :
        if val in old_xaxis :
            old = old_xaxis.index(val)
            old_data = data.chart_data[0]["data"][old]
            new = new_data.chart_data[0]["data"][idx]
            old_data["overdue"] += new["overdue"]
            old_data["upcoming"] += new["upcoming"]
            old_data["inprogress"] += new["inprogress"]
            old_data["duedate"] += new["duedate"]
            data.chart_data[0]["data"][old] = old_data
        else :
            data.chart_data[0]["data"].append(new_data.chart_data[0]["data"][idx])

    final_data = sorted(data.chart_data[0]["data"], key=lambda k: k['date'])

    data.chart_data[0]["data"] = final_data
    return data
