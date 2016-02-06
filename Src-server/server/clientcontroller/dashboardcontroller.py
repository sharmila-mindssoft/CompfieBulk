from protocol import (dashboard, login, core)

__all__ = [
    "process_client_dashboard_requests"
]

def process_client_dashboard_requests(request, db) :
    session_token = request.session_token
    client_info = session_token.split("-")

    request = request.request
    client_id = int(client_info[0])
    session_user = db.validate_session_token(client_id, session_token)

    if session_user is None:
        return login.InvalidSessionToken()
    if type(request) is dashboard.GetChartFilters :
        return process_get_chart_filters(db, session_user, client_id)

    elif type(request) is dashboard.GetComplianceStatusChart :
        return process_compliance_status_chart(db, request, session_user, client_id)
    elif type(request) is dashboard.GetComplianceStatusDrillDownData:
        return process_compliance_status_chart_drilldown(db, request, session_user, client_id)

    elif type(request) is dashboard.GetEscalationsChart :
        return process_escalation_chart(db, request, session_user, client_id)
    elif type(request) is dashboard.GetEscalationsDrillDownData :
        return process_escalation_chart_drilldown(db, request, session_user, client_id)   

    elif type(request) is dashboard.GetNotCompliedChart :
        return process_not_complied_chart(db, request, session_user, client_id)
    elif type(request) is dashboard.GetNotCompliedDrillDown :
        return process_not_complied_drill_down(db, request, session_user, client_id)

    elif type(request) is dashboard.GetTrendChart :
        return process_trend_chart(db, request, session_user, client_id)
    elif type(request) is dashboard.GetTrendChartDrillDownData :
        return process_get_trend_chart_drilldown(db, request, session_user, client_id)

    elif type(request) is dashboard.GetComplianceApplicabilityStatusChart :
        return process_compliance_applicability_chat(db, request, session_user, client_id)
    elif type(request) is dashboard.GetComplianceApplicabilityStatusDrillDown :
        return process_compliance_applicability_drill_down(db, request, session_user, client_id)

    elif type(request) is dashboard.GetNotifications :
        return process_get_notifications(db, request, session_user, client_id)
    elif type(request) is dashboard.UpdateNotificationStatus :
        return process_update_notification_status(db, request, session_user, client_id)

def process_get_chart_filters(db, session_user, client_id):
    countries = db.get_countries_for_user(session_user, client_id)
    domains = db.get_domains_for_user(session_user, client_id)
    business_group_ids = None
    business_groups = db.get_business_groups_for_user(business_group_ids, client_id)
    legal_entity_ids = None
    legal_entities = db.get_legal_entities_for_user(legal_entity_ids, client_id)
    division_ids = None
    divisions = db.get_divisions_for_user(division_ids, client_id)
    units = db.get_units_for_assign_compliance(session_user, client_id)
    return dashboard.GetChartFiltersSuccess(
        countries, domains, business_groups,
        legal_entities, divisions, units
    )

def process_compliance_status_chart(db, request, session_user, client_id):
    return db.get_compliance_status_chart(request, session_user, client_id)

def process_trend_chart(db, request, session_user, client_id):
    trend_chart_info = None
    if request.filter_type == "Group":
        trend_chart_info = db.get_trend_chart(request.country_ids, request.domain_ids,
            client_id)
    else:
        trend_chart_info = db.get_filtered_trend_data(request.country_ids, request.domain_ids,
            request.filter_type, request.filter_ids, client_id)
    years = trend_chart_info[0]
    data = trend_chart_info[1]
    return dashboard.GetTrendChartSuccess(years = years, data = data)

def process_get_trend_chart_drilldown(db, request, session_user, client_id):
    drill_down_info = None
    filter_ids = None if request.filter_ids == None else ",".join(str(x) for x in request.filter_ids)
    drill_down_info = db.get_trend_chart_drill_down(request.country_ids, 
        request.domain_ids, filter_ids, request.filter_type, request.year, 
        client_id)
    return dashboard.GetTrendChartDrillDownDataSuccess(
        drill_down_data = drill_down_info)

def process_compliance_status_chart_drilldown(db, request, session_user, client_id):
    unit_wise_data = db.get_compliances_details_for_status_chart(request, session_user, client_id)
    return dashboard.GetComplianceStatusDrillDownDataSuccess(
        unit_wise_data.values()
    )

def process_escalation_chart(db, request, session_user, client_id):
    return db.get_escalation_chart(request, session_user, client_id)

def process_escalation_chart_drilldown(db, request, session_user, client_id) :
    result_list = db.get_escalation_drill_down_data(request, session_user, client_id)
    return dashboard.GetEscalationsDrillDownDataSuccess(
        result_list[0],
        result_list[1]
    )

def process_not_complied_chart(db, request, session_user, client_id):
    return db.get_not_complied_chart(request, session_user, client_id)

def  process_not_complied_drill_down(db, request, session_user, client_id):
    result_list = db.get_not_complied_drill_down(request, session_user, client_id)
    return dashboard.GetNotCompliedDrillDownSuccess(result_list.values())

def process_compliance_applicability_chat(db, request, session_user, client_id):
    return db.get_compliance_applicability_chart(request, session_user, client_id)

def process_compliance_applicability_drill_down(db, request, session_user, client_id) :
    result_list = db.get_compliance_applicability_drill_down(request, session_user, client_id)
    return dashboard.GetComplianceApplicabilityStatusDrillDownSuccess(result_list)

def process_get_notifications(db, request, session_user, client_id):
    notifications = None
    notifications = db.get_notifications(request.notification_type, session_user, client_id)
    return dashboard.GetNotificationsSuccess(notifications = notifications)

def process_update_notification_status(db, request, session_user, client_id):
    notifications = None
    db.update_notification_status(request.notification_id, request.has_read, 
        session_user, client_id)
    return dashboard.UpdateNotificationStatusSuccess()
