from clientprotocol import (widgetprotocol)
from server.clientdatabase.widget import *

__all__ = [
    "process_client_widget_requests",
    "merge_compliance_chart_widget",
    "merge_escalation_chart_widget"
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

    return result

def merge_compliance_chart_widget(data, new_data):
    xnames = data.xaxis
    xdata = data.chart_data
    newdata = new_data.chart_data
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
