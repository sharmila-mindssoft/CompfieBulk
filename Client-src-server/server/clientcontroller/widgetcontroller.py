from clientprotocol import (widgetprotocol)
from server.clientdatabase.widget import *

__all__ = [
    "process_client_widget_requests",
    "merge_compliance_chart_widget"
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
    print data.to_structure()
    print new_data.to_structure()
    xnames = data.xaxis
    print xnames
    xdata = data.chart_data
    newdata = new_data.chart_data
    # if new_data.xaxis[0] in xnames :
    #     pass
    # else :
    data.xaxis.append(new_data.xaxis[0])
    xdata[0]["data"].extend(newdata[0]["data"])
    xdata[1]["data"].extend(newdata[1]["data"])
    xdata[2]["data"].extend(newdata[2]["data"])
    xdata[3]["data"].extend(newdata[3]["data"])
    data.chart_data = xdata
    return data
