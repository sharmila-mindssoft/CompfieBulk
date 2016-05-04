from server.jsontocsvconverter import ConvertJsonToCSV
from protocol import (core, clientreport, login)
from server import logger
__all__ = [
    "process_client_report_requests"
]

def process_client_report_requests(request, db) :
    session_token = request.session_token
    client_info = request.session_token.split("-")
    request = request.request
    client_id = int(client_info[0])
    session_user = db.validate_session_token(client_id, session_token)
    if session_user is None:
        return login.InvalidSessionToken()

    if type(request) is clientreport.GetClientReportFilters:
        logger.logClientApi("GetClientReportFilters", "process begin")
        result = get_client_report_filters(db, request, session_user)
        logger.logClientApi("GetClientReportFilters", "process end")

    elif type(request) is clientreport.GetUnitwisecomplianceReport:
        logger.logClientApi("GetUnitwisecomplianceReport", "process begin")
        result = get_unitwise_compliance(db, request, session_user)
        logger.logClientApi("GetUnitwisecomplianceReport", "process end")

    elif type(request) is clientreport.GetAssigneewisecomplianceReport:
        logger.logClientApi("GetAssigneewisecomplianceReport", "process begin")
        result = get_assigneewise_compliance(db, request, session_user)
        logger.logClientApi("GetAssigneewisecomplianceReport", "process end")

    elif type(request) is clientreport.GetServiceProviderReportFilters:
        logger.logClientApi("GetServiceProviderReportFilters", "process begin")
        result = get_serviceprovider_report_filters(db, request, session_user)
        logger.logClientApi("GetServiceProviderReportFilters", "process end")

    elif type(request) is clientreport.GetServiceProviderWiseCompliance:
        logger.logClientApi("GetServiceProviderWiseCompliance", "process begin")
        result = get_serviceproviderwise_compliance(db, request, session_user, client_id)
        logger.logClientApi("GetServiceProviderWiseCompliance", "process end")

    elif type(request) is clientreport.GetComplianceDetailsReportFilters:
        logger.logClientApi("GetComplianceDetailsReportFilters", "process begin")
        result = get_compliancedetails_report_filters(db, request, session_user, client_id)
        logger.logClientApi("GetComplianceDetailsReportFilters", "process end")

    elif type(request) is clientreport.GetComplianceDetailsReport:
        logger.logClientApi("GetComplianceDetailsReport", "process begin")
        result = get_compliancedetails_report(db, request, session_user, client_id)
        logger.logClientApi("GetComplianceDetailsReport", "process end")

    elif type(request) is clientreport.GetStatutoryNotificationsListFilters:
        logger.logClientApi("GetStatutoryNotificationsListFilters", "process begin")
        result = get_statutory_notifications_list_filters(db, request, session_user, client_id)
        logger.logClientApi("GetStatutoryNotificationsListFilters", "process end")

    elif type(request) is clientreport.GetStatutoryNotificationsListReport:
        logger.logClientApi("GetStatutoryNotificationsListReport", "process begin")
        result = get_statutory_notifications_list_report(db, request, session_user, client_id)
        logger.logClientApi("GetStatutoryNotificationsListReport", "process end")

    elif type(request) is clientreport.GetRiskReportFilters:
        logger.logClientApi("GetRiskReportFilters", "process begin")
        result = get_risk_report_filters(db, request, session_user, client_id)
        logger.logClientApi("GetRiskReportFilters", "process end")

    elif type(request) is clientreport.GetRiskReport:
        logger.logClientApi("GetRiskReport", "process begin")
        result = get_risk_report(db, request, session_user, client_id)
        logger.logClientApi("GetRiskReport", "process end")

    elif type(request) is clientreport.GetReassignedHistoryReportFilters:
        logger.logClientApi("GetReassignedHistoryReportFilters", "process begin")
        result = get_reassignedhistory_report_filters(db, request, session_user, client_id)
        logger.logClientApi("GetReassignedHistoryReportFilters", "process end")

    elif type(request) is clientreport.GetReassignedHistoryReport:
        logger.logClientApi("GetReassignedHistoryReport", "process begin")
        result = get_reassignedhistory_report(db, request, session_user, client_id)
        logger.logClientApi("GetReassignedHistoryReport", "process end")

    elif type(request) is clientreport.GetLoginTrace:
        logger.logClientApi("GetLoginTrace", "process begin")
        result = get_login_trace(db, request, session_user, client_id)
        logger.logClientApi("GetLoginTrace", "process end")

    elif type(request) is clientreport.GetComplianceActivityReportFilters:
        logger.logClientApi("GetComplianceActivityReportFilters", "process begin")
        result = get_compliance_activity_report_filters(db, request, session_user, client_id)
        logger.logClientApi("GetComplianceActivityReportFilters", "process end")

    elif type(request) is clientreport.GetComplianceActivityReport:
        logger.logClientApi("GetComplianceActivityReport", "process begin")
        result = get_compliance_activity_report(db, request, session_user, client_id)
        logger.logClientApi("GetComplianceActivityReport", "process end")

    elif type(request) is clientreport.GetTaskApplicabilityStatusFilters:
        logger.logClientApi("GetTaskApplicabilityStatusFilters", "process begin")
        result = process_get_task_applicability_status_filters(db, request, session_user)
        logger.logClientApi("GetTaskApplicabilityStatusFilters", "process end")

    elif type(request) is clientreport.GetComplianceTaskApplicabilityStatusReport:
        logger.logClientApi("GetComplianceTaskApplicabilityStatusReport", "process begin")
        result = process_get_task_applicability_report_data(db, request, session_user, client_id)
        logger.logClientApi("GetComplianceTaskApplicabilityStatusReport", "process end")

    elif type(request) is clientreport.GetClientDetailsReportFilters:
        logger.logClientApi("GetClientDetailsReportFilters", "process begin")
        result = get_client_details_report_filters(db, request, session_user, client_id)
        logger.logClientApi("GetClientDetailsReportFilters", "process end")

    elif type(request) is clientreport.GetClientDetailsReportData:
        logger.logClientApi("GetClientDetailsReportData", "process begin")
        result = get_client_details_report_data(db, request, session_user, client_id)
        logger.logClientApi("GetClientDetailsReportData", "process end")

    elif type(request) is clientreport.ExportToCSV:
        logger.logClientApi("ExportToCSV", "process begin")
        result = export_to_csv(db, request, session_user, client_id)
        logger.logClientApi("ExportToCSV", "process end")

    return result


def get_client_report_filters(db, request, session_user):
    user_company_info = db.get_user_company_details(session_user)
    unit_ids = user_company_info[0]
    division_ids = user_company_info[1]
    legal_entity_ids = user_company_info[2]
    business_group_ids = user_company_info[3]
    country_list = db.get_countries_for_user(session_user)
    domain_list = db.get_domains_for_user(session_user)
    business_group_list = db.get_business_groups_for_user(business_group_ids)
    legal_entity_list = db.get_legal_entities_for_user(legal_entity_ids)
    division_list = db.get_divisions_for_user(division_ids)
    unit_list = db.get_units_for_user(unit_ids)
    users_list = db.get_client_users()
    return clientreport.GetClientReportFiltersSuccess(
        countries=country_list,
        domains=domain_list,
        business_groups=business_group_list,
        legal_entities=legal_entity_list,
        divisions=division_list,
        units=unit_list,
        users=users_list
    )

def get_unitwise_compliance(db, request, session_user):
    country_id = request.country_id
    domain_id = request.domain_id
    business_group_id = request.business_group_id
    legal_entity_id = request.legal_entity_id
    division_id = request.division_id
    unit_id = request.unit_id
    user_id = request.user_id
    from_count = request.record_count
    to_count = 500

    data, total = db.report_unitwise_compliance(
        country_id, domain_id, business_group_id,
        legal_entity_id, division_id, unit_id, user_id, session_user,
        from_count, to_count
    )
    unit_wise_compliances_list = db.return_unitwise_report(data)
    return clientreport.GetUnitwisecomplianceReportSuccess(unit_wise_compliances_list, total)

def get_assigneewise_compliance(db, request, session_user):
    country_id = request.country_id
    domain_id = request.domain_id
    business_group_id = request.business_group_id
    legal_entity_id = request.legal_entity_id
    division_id = request.division_id
    unit_id = request.unit_id
    user_id = request.user_id
    from_count = request.record_count
    to_count = 500

    data, total_count = db.report_assigneewise_compliance(
        country_id, domain_id, business_group_id,
        legal_entity_id, division_id, unit_id, user_id, session_user,
        from_count, to_count
    )
    print total_count
    assignee_wise_compliances_list = db.return_assignee_report_data(data)
    return clientreport.GetAssigneewisecomplianceReportSuccess(assignee_wise_compliances_list, total_count)

def get_serviceprovider_report_filters(db, request, session_user):
    user_company_info = db.get_user_company_details(session_user)
    unit_ids = user_company_info[0]
    country_list = db.get_countries_for_user(session_user)
    domain_list = db.get_domains_for_user(session_user)
    unit_list = db.get_units_for_user(unit_ids)
    level_1_statutories_list = db.get_client_level_1_statutoy(session_user)
    service_providers_list = db.get_service_providers()

    return clientreport.GetServiceProviderReportFiltersSuccess(
        countries=country_list,
        domains=domain_list,
        level_1_statutories=level_1_statutories_list,
        units=unit_list,
        service_providers=service_providers_list
    )

def get_serviceproviderwise_compliance(db, request, session_user, client_id):
    if request.csv:
        converter = ConvertJsonToCSV(db, request, session_user, client_id, "ServiceProviderWise")
        return clientreport.ExportToCSVSuccess(link=converter.FILE_DOWNLOAD_PATH)
    else:
        country_id = request.country_id
        domain_id = request.domain_id
        statutory_id = request.statutory_id
        unit_id = request.unit_id
        service_provider_id = request.service_provider_id

        if service_provider_id is None :
            service_provider_id = '%'

        serviceprovider_wise_compliances_list = db.get_serviceproviderwise_compliance_report(
            country_id, domain_id, statutory_id, unit_id, service_provider_id, client_id, session_user
        )
        return clientreport.GetServiceProviderWiseComplianceSuccess(serviceprovider_wise_compliances_list)

def get_compliancedetails_report_filters(db, request, session_user, client_id):
    user_company_info = db.get_user_company_details(session_user)
    unit_ids = user_company_info[0]
    country_list = db.get_countries_for_user(session_user)
    domain_list = db.get_domains_for_user(session_user)
    unit_list = db.get_units_for_user(unit_ids)
    level_1_statutories_list = db.get_client_level_1_statutoy(session_user)
    compliances_list = db.get_client_compliances(session_user)
    users_list = db.get_client_users()
    return clientreport.GetComplianceDetailsReportFiltersSuccess(
        countries=country_list,
        domains=domain_list,
        level_1_statutories=level_1_statutories_list,
        units=unit_list,
        Compliances=compliances_list,
        users=users_list
    )

def get_statutory_notifications_list_filters(db, request, session_user, client_id):
    user_company_info = db.get_user_company_details(session_user)
    unit_ids = user_company_info[0]
    division_ids = user_company_info[1]
    legal_entity_ids = user_company_info[2]
    business_group_ids = user_company_info[3]
    country_list = db.get_countries_for_user(session_user)
    domain_list = db.get_domains_for_user(session_user)
    business_group_list = db.get_business_groups_for_user(business_group_ids)
    legal_entity_list = db.get_legal_entities_for_user(legal_entity_ids)
    division_list = db.get_divisions_for_user(division_ids)
    unit_list = db.get_units_for_user(unit_ids)
    level_1_statutories_list = db.get_client_level_1_statutoy(session_user)
    users_list = db.get_client_users()

    return clientreport.GetStatutoryNotificationsListFiltersSuccess(
        countries=country_list,
        domains=domain_list,
        business_groups=business_group_list,
        legal_entities=legal_entity_list,
        divisions=division_list,
        units=unit_list,
        level_1_statutories=level_1_statutories_list,
        users=users_list
    )

def get_statutory_notifications_list_report(db, request, session_user, client_id):
    if request.csv:
        converter = ConvertJsonToCSV(db, request, session_user, client_id, "StatutoryNotification")
        return clientreport.ExportToCSVSuccess(link=converter.FILE_DOWNLOAD_PATH)
    else:
        result = db.get_statutory_notifications_list_report(request, client_id)
        return clientreport.GetStatutoryNotificationsListReportSuccess(result)

def get_compliancedetails_report(db, request, session_user, client_id):
    if request.csv:
        converter = ConvertJsonToCSV(db, request, session_user, client_id, "ComplianceDetails")
        return clientreport.ExportToCSVSuccess(link=converter.FILE_DOWNLOAD_PATH)
    else:
        country_id = request.country_id
        domain_id = request.domain_id
        statutory_id = request.statutory_id
        unit_id = request.unit_id
        compliance_id = request.compliance_id
        assignee_id = request.assignee_id
        from_date = request.from_date
        to_date = request.to_date
        compliance_status = request.compliance_status
        from_count = request.record_count
        to_count = 500

        compliance_details_list, total = db.report_compliance_details(
            country_id, domain_id, statutory_id, unit_id, compliance_id,
            assignee_id, from_date, to_date, compliance_status, session_user,
            from_count, to_count
        )
        return clientreport.GetComplianceDetailsReportSuccess(
            compliance_details_list, total
        )

def get_risk_report_filters(db, request, session_user, client_id):
    user_company_info = db.get_user_company_details(session_user)
    unit_ids = user_company_info[0]
    division_ids = user_company_info[1]
    legal_entity_ids = user_company_info[2]
    business_group_ids = user_company_info[3]
    country_list = db.get_countries_for_user(session_user)
    domain_list = db.get_domains_for_user(session_user)
    business_group_list = db.get_business_groups_for_user(business_group_ids)
    legal_entity_list = db.get_legal_entities_for_user(legal_entity_ids)
    division_list = db.get_divisions_for_user(division_ids)
    unit_list = db.get_units_for_user(unit_ids)
    level_1_statutories_list = db.get_client_level_1_statutoy(session_user)
    return clientreport.GetRiskReportFiltersSuccess(
        countries=country_list,
        domains=domain_list,
        business_groups=business_group_list,
        legal_entities=legal_entity_list,
        divisions=division_list,
        units=unit_list,
        level1_statutories=level_1_statutories_list
    )

def get_reassignedhistory_report_filters(db, request, session_user, client_id):
    user_company_info = db.get_user_company_details(session_user)
    unit_ids = user_company_info[0]
    country_list = db.get_countries_for_user(session_user)
    domain_list = db.get_domains_for_user(session_user)
    unit_list = db.get_units_for_user(unit_ids)
    level_1_statutories_list = db.get_client_level_1_statutoy(session_user)
    compliances_list = db.get_client_compliances(session_user)
    users_list = db.get_client_users()

    return clientreport.GetReassignedHistoryReportFiltersSuccess(
        countries=country_list,
        domains=domain_list,
        units=unit_list,
        level_1_statutories=level_1_statutories_list,
        compliances=compliances_list,
        users=users_list
    )


def get_reassignedhistory_report(db, request, session_user, client_id):
    if not request.csv:
        country_id = request.country_id
        domain_id = request.domain_id
        level_1_statutory_id = request.level_1_statutory_id
        unit_id = request.unit_id
        compliance_id = request.compliance_id
        user_id = request.user_id
        from_date = request.from_date
        to_date = request.to_date
        from_count = request.record_count
        to_count = 5
        reassigned_history_list, total = db.report_reassigned_history(
            country_id, domain_id, level_1_statutory_id,
            unit_id, compliance_id, user_id, from_date, to_date, session_user,
            from_count, to_count
        )
        return clientreport.GetReassignedHistoryReportSuccess(reassigned_history_list, total)
    else:
        converter = ConvertJsonToCSV(db, request, session_user, client_id, "Reassign")
        return clientreport.ExportToCSVSuccess(link=converter.FILE_DOWNLOAD_PATH)


def get_risk_report(db, request, session_user, client_id):
    country_id = request.country_id
    domain_id = request.domain_id
    business_group_id = request.business_group_id
    legal_entity_id = request.division_id
    division_id = request.division_id
    unit_id = request.unit_id
    level_1_statutory_name = request.level_1_statutory_name
    statutory_status = request.statutory_status
    delayed_compliance = [] #1
    not_complied = [] # 2
    not_opted = [] # 3
    unassigned = [] # 4
    if request.csv == False:
        if statutory_status in [1, None, "None", "", 0]:# Delayed compliance
            delayed_compliance = db.get_risk_report(
                country_id, domain_id, business_group_id,
                legal_entity_id, division_id, unit_id, level_1_statutory_name, 1,
                client_id, session_user
            )
        if statutory_status in [2, None, "None", "", 0]: # Not complied
            not_complied = db.get_risk_report(
                country_id, domain_id, business_group_id,
                legal_entity_id, division_id, unit_id, level_1_statutory_name, 2,
                client_id, session_user
            )
        if statutory_status in [3, None, "None", "", 0]: # Not opted
            not_opted = db.get_risk_report(
                country_id, domain_id, business_group_id,
                legal_entity_id, division_id, unit_id, level_1_statutory_name, 3,
                client_id, session_user
            )
        if statutory_status in [4, None, "None", "", 0]: # Unassigned
            unassigned = db.get_risk_report(
                country_id, domain_id, business_group_id,
                legal_entity_id, division_id, unit_id, level_1_statutory_name, 4,
                client_id, session_user
            )

        return clientreport.GetRiskReportSuccess(
            delayed_compliance = delayed_compliance,
            not_complied = not_complied,
            not_opted = not_opted,
            unassigned_compliance = unassigned
        )
    else:
        converter = ConvertJsonToCSV(db, request, session_user, client_id, "RiskReport")
        return clientreport.ExportToCSVSuccess(link=converter.FILE_DOWNLOAD_PATH)

def get_login_trace(db, request, session_user, client_id):
    users_list = db.get_client_users()
    logintracelist = db.get_login_trace(client_id, session_user)
    return clientreport.GetLoginTraceSuccess(
        users=users_list,
        login_trace=logintracelist
    )

def get_compliance_activity_report_filters(db, request, session_user, client_id):
    user_company_info = db.get_user_company_details(session_user)
    unit_ids = user_company_info[0]
    domain_list = db.get_domains_for_user(session_user)
    unit_list = db.get_units_for_user(unit_ids)
    level_1_statutories_list = db.get_client_level_1_statutoy(session_user)
    compliances_list = db.get_client_compliances(session_user)
    country_list = db.get_countries_for_user(session_user)
    users_list = db.get_client_users()
    return clientreport.GetComplianceActivityReportFiltersSuccess(
        users=users_list,
        domains=domain_list,
        level_1_statutories=level_1_statutories_list,
        units=unit_list,
        compliances=compliances_list,
        countries=country_list
    )

def get_compliance_activity_report(db, request, session_user, client_id):
    country_id = request.country_id
    domain_id = request.domain_id
    unit_id = request.unit_id
    user_id = request.user_id
    user_type = request.user_type
    from_date = request.from_date
    to_date = request.to_date
    compliance_id = request.compliance_id
    level_1_statutory_name = request.level_1_statutory_name
    if request.csv is False:
        print "inside if in get_compliance_activity_report controller"
        activities = db.get_compliance_activity_report(
            country_id, domain_id, user_type, user_id, unit_id, compliance_id, level_1_statutory_name,
            from_date, to_date, session_user, client_id
        )
        return clientreport.GetComplianceActivityReportSuccess(
            activities=activities
        )
    else:
        converter = ConvertJsonToCSV(db, request, session_user, client_id, "ActivityReport")
        return clientreport.ExportToCSVSuccess(link=converter.FILE_DOWNLOAD_PATH)


def process_get_task_applicability_status_filters(db, request, session_user):
    user_company_info = db.get_user_company_details(session_user)
    unit_ids = user_company_info[0]
    division_ids = user_company_info[1]
    legal_entity_ids = user_company_info[2]
    business_group_ids = user_company_info[3]

    countries = db.get_countries_for_user(session_user)
    domains = db.get_domains_for_user(session_user)
    business_groups = db.get_business_groups_for_user(business_group_ids)
    legal_entities = db.get_legal_entities_for_user(legal_entity_ids)
    divisions = db.get_divisions_for_user(division_ids)
    units = db.get_units_for_user(unit_ids)
    level1_statutories = db.get_client_level_1_statutoy(session_user)
    applicable_status = core.APPLICABILITY_STATUS.values()
    return clientreport.GetTaskApplicabilityStatusFiltersSuccess(
        countries, domains, business_groups, legal_entities,
        divisions, units, level1_statutories, applicable_status
    )

def process_get_task_applicability_report_data(db, request, session_user, client_id):
    if request.csv:
        converter = ConvertJsonToCSV(db, request, session_user, client_id, "TaskApplicability")
        return clientreport.ExportToCSVSuccess(link=converter.FILE_DOWNLOAD_PATH)
    else:
        result = db.get_compliance_task_applicability(request, session_user)
        print result
        return result

def get_client_details_report_filters(db, request, session_user, client_id):
    countries = db.get_countries_for_user(session_user, client_id)
    domains = db.get_domains_for_user(session_user, client_id)
    user_company_info = db.get_user_company_details(session_user)
    unit_ids = user_company_info[0]
    division_ids = user_company_info[1]
    legal_entity_ids = user_company_info[2]
    business_group_ids = user_company_info[3]

    business_groups = db.get_business_groups_for_user(business_group_ids)
    legal_entities = db.get_legal_entities_for_user(legal_entity_ids)
    divisions = db.get_divisions_for_user(division_ids)
    units = db.get_units_for_user(unit_ids)
    return clientreport.GetClientDetailsReportFiltersSuccess(
        countries=countries,
        domains=domains,
        business_groups=business_groups,
        legal_entities=legal_entities,
        divisions=divisions,
        units=units
    )

def get_client_details_report_data(db, request, session_user, client_id):
    if request.csv:
        converter = ConvertJsonToCSV(db, request, session_user, client_id, "ClientDetails")
        return clientreport.ExportToCSVSuccess(link=converter.FILE_DOWNLOAD_PATH)
    else:
        units = db.get_client_details_report(
            request.country_id, request.business_group_id,
            request.legal_entity_id, request.division_id, request.unit_id,
            request.domain_ids, session_user
        )
        return clientreport.GetClientDetailsReportDataSuccess(units=units)

def export_to_csv(db, request, session_user, client_id):
    converter = ConvertJsonToCSV(db, request, session_user)
    return clientreport.ExportToCSVSuccess(link=converter.FILE_DOWNLOAD_PATH)
