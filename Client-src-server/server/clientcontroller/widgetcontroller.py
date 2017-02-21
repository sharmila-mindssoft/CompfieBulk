from clientprotocol import (widgetprotocol)
from server.clientdatabase.widget import *

__all__ = [
    "process_client_widget_requests"
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
