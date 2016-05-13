from protocol import (dashboard, login, general)
from server import logger

__all__ = [
    "process_client_dashboard_requests"
]


########################################################
# To Redirect the requests to the corresponding
# functions
########################################################
def process_client_dashboard_requests(request, db) :
    session_token = request.session_token
    client_info = session_token.split("-")

    request = request.request
    client_id = int(client_info[0])
    session_user = db.validate_session_token(client_id, session_token)

    if session_user is None:
        return login.InvalidSessionToken()

    if db.get_client_compliance_count() == 0:
        logger.logClientApi("CheckMasterDataDashboard", "process begin")
        result = general.MasterDataNotAvailableForClient()
        logger.logClientApi("CheckMasterDataDashboard", "process end")

    elif type(request) is dashboard.GetChartFilters :
        logger.logClientApi("GetChartFilters", "process begin")
        result = process_get_chart_filters(db, session_user, client_id)
        logger.logClientApi("GetChartFilters", "process end")

    elif type(request) is dashboard.GetComplianceStatusChart :
        logger.logClientApi("GetComplianceStatusChart", "process begin")
        result = process_compliance_status_chart(db, request, session_user, client_id)
        logger.logClientApi("GetComplianceStatusChart", "process end")

    elif type(request) is dashboard.GetComplianceStatusDrillDownData:
        logger.logClientApi("GetComplianceStatusDrillDownData", "process begin")
        result = process_compliance_status_chart_drilldown(db, request, session_user, client_id)
        logger.logClientApi("GetComplianceStatusDrillDownData", "process end")

    elif type(request) is dashboard.GetEscalationsChart :
        logger.logClientApi("GetEscalationsChart", "process begin")
        result = process_escalation_chart(db, request, session_user, client_id)
        logger.logClientApi("GetEscalationsChart", "process end")

    elif type(request) is dashboard.GetEscalationsDrillDownData :
        logger.logClientApi("GetEscalationsDrillDownData", "process begin")
        result = process_escalation_chart_drilldown(db, request, session_user, client_id)
        logger.logClientApi("GetEscalationsDrillDownData", "process end")

    elif type(request) is dashboard.GetNotCompliedChart :
        logger.logClientApi("GetNotCompliedChart", "process begin")
        result = process_not_complied_chart(db, request, session_user, client_id)
        logger.logClientApi("GetNotCompliedChart", "process end")

    elif type(request) is dashboard.GetNotCompliedDrillDown :
        logger.logClientApi("GetNotCompliedDrillDown", "process begin")
        result = process_not_complied_drill_down(db, request, session_user, client_id)
        logger.logClientApi("GetNotCompliedDrillDown", "process end")

    elif type(request) is dashboard.GetTrendChart :
        logger.logClientApi("GetTrendChart", "process begin")
        result = process_trend_chart(db, request, session_user, client_id)
        logger.logClientApi("GetTrendChart", "process end")

    elif type(request) is dashboard.GetTrendChartDrillDownData :
        logger.logClientApi("GetTrendChartDrillDownData", "process begin")
        result = process_get_trend_chart_drilldown(db, request, session_user, client_id)
        logger.logClientApi("GetTrendChartDrillDownData", "process end")

    elif type(request) is dashboard.GetComplianceApplicabilityStatusChart :
        logger.logClientApi("GetComplianceApplicabilityStatusChart", "process begin")
        result = process_compliance_applicability_chat(db, request, session_user, client_id)
        logger.logClientApi("GetComplianceApplicabilityStatusChart", "process end")

    elif type(request) is dashboard.GetComplianceApplicabilityStatusDrillDown :
        logger.logClientApi("GetComplianceApplicabilityStatusDrillDown", "process begin")
        result = process_compliance_applicability_drill_down(db, request, session_user, client_id)
        logger.logClientApi("GetComplianceApplicabilityStatusDrillDown", "process end")

    elif type(request) is dashboard.GetNotifications :
        logger.logClientApi("GetNotifications", "process begin")
        result = process_get_notifications(db, request, session_user, client_id)
        logger.logClientApi("GetNotifications", "process end")

    elif type(request) is dashboard.UpdateNotificationStatus :
        logger.logClientApi("UpdateNotificationStatus", "process begin")
        result = process_update_notification_status(db, request, session_user, client_id)
        logger.logClientApi("UpdateNotificationStatus", "process end")

    elif type(request) is dashboard.GetAssigneewiseComplianesFilters :
        logger.logClientApi("GetAssigneewiseComplianesFilters", "process begin")
        result = process_assigneewise_compliances_filters(db, request, session_user, client_id)
        logger.logClientApi("GetAssigneewiseComplianesFilters", "process end")

    elif type(request) is dashboard.GetAssigneeWiseCompliancesChart :
        logger.logClientApi("GetAssigneeWiseCompliancesChart", "process begin")
        result = process_assigneewise_compliances(db, request, session_user, client_id)
        logger.logClientApi("GetAssigneeWiseCompliancesChart", "process end")

    elif type(request) is dashboard.GetAssigneewiseYearwiseCompliances:
        logger.logClientApi("GetAssigneewiseYearwiseCompliances", "process begin")
        result = process_assigneewise_yearwise_compliances(db, request, session_user, client_id)
        logger.logClientApi("GetAssigneewiseYearwiseCompliances", "process end")

    elif type(request) is dashboard.GetAssigneewiseReassignedComplianes:
        logger.logClientApi("GetAssigneewiseReassignedComplianes", "process begin")
        result = process_get_assigneewise_reassigned_compliances(db, request, session_user, client_id)
        logger.logClientApi("GetAssigneewiseReassignedComplianes", "process end")

    elif type(request) is dashboard.GetAssigneeWiseComplianceDrillDown :
        logger.logClientApi("GetAssigneeWiseComplianceDrillDown", "process begin")
        result = process_assigneewise_compliances_drilldown(db, request, session_user, client_id)
        logger.logClientApi("GetAssigneeWiseComplianceDrillDown", "process end")

    elif type(request) is dashboard.CheckContractExpiration:
        logger.logClientApi("CheckContractExpiration", "process begin")
        result = check_contract_expiration(db, request, session_user, client_id)
        logger.logClientApi("CheckContractExpiration", "process end")

    return result

def process_get_chart_filters(db, session_user, client_id):
    countries = db.get_countries_for_user(session_user, client_id)
    domains = db.get_domains_for_user(session_user, client_id)
    business_group_ids = None
    business_groups = db.get_business_groups_for_user(business_group_ids)
    legal_entity_ids = None
    legal_entities = db.get_legal_entities_for_user(legal_entity_ids)
    division_ids = None
    divisions = db.get_divisions_for_user(division_ids)
    units = db.get_units_for_dashboard_filters(session_user)
    domain_info = db.get_country_wise_domain_month_range()
    group_name = db.get_group_name()
    return dashboard.GetChartFiltersSuccess(
        countries, domains, business_groups,
        legal_entities, divisions, units,
        domain_info, group_name
    )

def process_compliance_status_chart(db, request, session_user, client_id):
    return db.get_compliance_status_chart(request, session_user, client_id)

def process_trend_chart(db, request, session_user, client_id):
    trend_chart_info = None
    if request.filter_type == "Group":
        trend_chart_info = db.get_trend_chart(
            request.country_ids, request.domain_ids,
            client_id
        )
    else:
        trend_chart_info = db.get_filtered_trend_data(
            request.country_ids, request.domain_ids,
            request.filter_type, request.filter_ids, client_id
        )
    years = trend_chart_info[0]
    data = trend_chart_info[1]
    count_flag = trend_chart_info[2]
    if count_flag == 0:
        data = []
    return dashboard.GetTrendChartSuccess(
        years=years,
        data=data
    )

def process_get_trend_chart_drilldown(db, request, session_user, client_id):
    drill_down_info = None
    filter_ids = None if request.filter_ids is None else ",".join(str(x) for x in request.filter_ids)
    drill_down_info = db.get_trend_chart_drill_down(
        request.country_ids,
        request.domain_ids, filter_ids,
        request.filter_type, request.year,
        client_id
    )
    return dashboard.GetTrendChartDrillDownDataSuccess(
        drill_down_data=drill_down_info
    )

def process_compliance_status_chart_drilldown(db, request, session_user, client_id):
    from_count = request.record_count
    to_count = 500
    unit_wise_data = db.get_compliances_details_for_status_chart(
        request, session_user, client_id,
        from_count, to_count
    )
    return dashboard.GetComplianceStatusDrillDownDataSuccess(
        unit_wise_data.values()
    )

def process_escalation_chart(db, request, session_user, client_id):
    return db.get_escalation_chart(request, session_user, client_id)

def process_escalation_chart_drilldown(db, request, session_user, client_id) :
    from_count = request.record_count
    to_count = 500
    result_list = db.get_escalation_drill_down_data(
        request, session_user, client_id,
        from_count, to_count
    )
    return dashboard.GetEscalationsDrillDownDataSuccess(
        result_list[0],
        result_list[1]
    )

def process_not_complied_chart(db, request, session_user, client_id):
    return db.get_not_complied_chart(request, session_user, client_id)

def  process_not_complied_drill_down(db, request, session_user, client_id):
    from_count = request.record_count
    to_count = 500
    result_list = db.get_not_complied_drill_down(
        request, session_user, client_id,
        from_count, to_count
    )
    return dashboard.GetNotCompliedDrillDownSuccess(result_list.values())

def process_compliance_applicability_chat(db, request, session_user, client_id):
    return db.get_compliance_applicability_chart(request, session_user, client_id)

def process_compliance_applicability_drill_down(db, request, session_user, client_id) :
    from_count = request.record_count
    to_count = 500
    result_list = db.get_compliance_applicability_drill_down(
        request, session_user, client_id,
        from_count, to_count
    )
    return dashboard.GetComplianceApplicabilityStatusDrillDownSuccess(result_list)

def process_get_notifications(db, request, session_user, client_id):
    notifications = None
    to_count = 500
    notifications = db.get_notifications(
        request.notification_type,
        request.start_count, to_count,
        session_user, client_id
    )
    return dashboard.GetNotificationsSuccess(notifications = notifications)

def process_update_notification_status(db, request, session_user, client_id):
    notifications = None
    db.update_notification_status(request.notification_id, request.has_read,
        session_user, client_id)
    return dashboard.UpdateNotificationStatusSuccess()


########################################################
# To get data to populate in assignee wise compliance
# chart filters
########################################################
def process_assigneewise_compliances_filters(db, request, session_user, client_id):
    user_company_info = db.get_user_company_details( session_user, client_id)
    unit_ids = user_company_info[0]
    division_ids = user_company_info[1]
    legal_entity_ids = user_company_info[2]
    business_group_ids = user_company_info[3]
    country_list = db.get_countries_for_user(session_user, client_id)
    domain_list = db.get_domains_for_user(session_user, client_id)
    business_group_list = db.get_business_groups_for_user(business_group_ids)
    legal_entity_list = db.get_legal_entities_for_user(legal_entity_ids)
    division_list =  db.get_divisions_for_user(division_ids)
    unit_list = db.get_units_for_user(unit_ids, client_id)
    users_list = db.get_client_users(client_id, unit_ids);
    return dashboard.GetAssigneewiseComplianesFiltersSuccess(
        countries=country_list, business_groups=business_group_list,
        legal_entities=legal_entity_list, divisions=division_list,
        units=unit_list, users=users_list, domains=domain_list
    )


########################################################
# To retrieve data for assignee wise compliances chart
# based on the received filters
########################################################
def process_assigneewise_compliances(db, request, session_user, client_id):
    country_id = request.country_id
    business_group_id = request.business_group_id
    legal_entity_id = request.legal_entity_id
    division_id = request.division_id
    unit_id = request.unit_id
    user_id = request.user_id
    chart_data = db.get_assigneewise_compliances_list(
        country_id, business_group_id, legal_entity_id, division_id, unit_id,
        session_user, client_id, user_id
    )
    return dashboard.GetAssigneeWiseCompliancesChartSuccess(
        chart_data=chart_data
    )

def process_assigneewise_yearwise_compliances(db, request, session_user, client_id):
    country_id = request.country_id
    unit_id = request.unit_id
    user_id = request.user_id
    chart_data = db.get_assigneewise_yearwise_compliances(
        country_id, unit_id, user_id, client_id
    )
    return dashboard.GetAssigneewiseYearwiseCompliancesSuccess(
        chart_data=chart_data
    )

def process_get_assigneewise_reassigned_compliances(db, request, session_user, client_id):
    country_id = request.country_id
    unit_id = request.unit_id
    user_id = request.user_id
    domain_id = request.domain_id
    chart_data = db.get_assigneewise_reassigned_compliances(
        country_id, unit_id, user_id, domain_id, client_id
    )
    return dashboard.GetAssigneewiseReassignedComplianesSuccess(
        chart_data=chart_data
    )


########################################################
# To get the detailed info of the selected domain in the
# assignee wise compliances chart
########################################################
def process_assigneewise_compliances_drilldown(
    db, request, session_user, client_id
):
    country_id = request.country_id
    assignee_id = request.assignee_id
    domain_id = request.domain_id
    year = request.year
    unit_id = request.unit_id
    start_count = request.start_count
    to_count = 500

    drill_down_data = {}
    complied, delayed, inprogress, not_complied = db.get_assigneewise_compliances_drilldown_data(
        country_id, assignee_id, domain_id, client_id, year, unit_id, start_count,
        to_count, session_user
    )
    total_count = db.get_assigneewise_compliances_drilldown_data_count(
        country_id, assignee_id, domain_id, client_id, year, unit_id, session_user
    )
    
    drill_down_data = dashboard.AssigneeWiseCompliance(
        complied=complied,
        delayed=delayed,
        inprogress=inprogress,
        not_complied=not_complied
    )
    return dashboard.GetAssigneeWiseComplianceDrillDownSuccess(
        drill_down_data=drill_down_data,
        total_count=total_count
    )

########################################################
# To check whether the contract of the given client
# expired or not and to get the notification, reminder
# and escalation count
########################################################
def check_contract_expiration(
    db, request, session_user, client_id
):
    no_of_days_left = db.get_no_of_days_left_for_contract_expiration()
    if no_of_days_left < 0:
        no_of_days_left = 0
    notification_count, reminder_count, escalation_count = db.get_dashboard_notification_counts(
        session_user
    )
    show_popup, notification_text = db.need_to_display_deletion_popup()
    return dashboard.CheckContractExpirationSuccesss(
        no_of_days_left=no_of_days_left,
        notification_count=notification_count,
        reminder_count=reminder_count,
        escalation_count=escalation_count,
        show_popup=show_popup,
        notification_text=notification_text
    )
