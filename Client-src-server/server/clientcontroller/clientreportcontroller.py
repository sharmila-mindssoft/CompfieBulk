import time
from server.jsontocsvconverter import ConvertJsonToCSV
from clientprotocol import (clientcore, clientreport, clientlogin)
from server import logger
from server.constants import RECORD_DISPLAY_COUNT

from server.clientdatabase.clientreport import *

from server.clientdatabase.general import (
    get_user_company_details,
    get_countries_for_user, get_domains_for_user,
    get_business_groups_for_user, get_legal_entities_for_user,
    get_divisions_for_user, get_units_for_user,
    get_client_users, get_client_level_1_statutoy,
    get_service_providers, get_client_compliances
    )

__all__ = [
    "process_client_report_requests"
]


def process_client_report_requests(request, db):
    session_token = request.session_token
    client_info = request.session_token.split("-")
    request = request.request
    client_id = int(client_info[0])
    session_user = db.validate_session_token(session_token)
    if session_user is None:
        return clientlogin.InvalidSessionToken()

    if type(request) is clientreport.GetClientReportFilters:
        logger.logClientApi(
            "GetClientReportFilters  - " + str(client_id), "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_client_report_filters(db, request, session_user)
        logger.logClientApi("GetClientReportFilters", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetUnitwisecomplianceReport:
        logger.logClientApi(
            "GetUnitwisecomplianceReport  - " + str(client_id), "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_unitwise_compliance(db, request, session_user)
        logger.logClientApi("GetUnitwisecomplianceReport", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetAssigneewisecomplianceReport:
        logger.logClientApi(
            "GetAssigneewisecomplianceReport  - " + str(client_id),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_assigneewise_compliance(db, request, session_user)
        logger.logClientApi("GetAssigneewisecomplianceReport", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetServiceProviderReportFilters:
        logger.logClientApi(
            "GetServiceProviderReportFilters  - " + str(client_id),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_serviceprovider_report_filters(db, request, session_user)
        logger.logClientApi("GetServiceProviderReportFilters", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetServiceProviderWiseCompliance:
        logger.logClientApi(
            "GetServiceProviderWiseCompliance  - " + str(client_id),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_serviceproviderwise_compliance(db, request, session_user)
        logger.logClientApi("GetServiceProviderWiseCompliance", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetComplianceDetailsReportFilters:
        logger.logClientApi(
            "GetComplianceDetailsReportFilters  - " + str(client_id),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_compliancedetails_report_filters(
            db, request, session_user, client_id
        )
        logger.logClientApi("GetComplianceDetailsReportFilters", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetComplianceDetailsReport:
        logger.logClientApi(
            "GetComplianceDetailsReport  - " + str(client_id),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_compliancedetails_report(
            db, request, session_user, client_id
        )
        logger.logClientApi("GetComplianceDetailsReport", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetStatutoryNotificationsListFilters:
        logger.logClientApi(
            "GetStatutoryNotificationsListFilters  - " + str(client_id),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_statutory_notifications_list_filters(
            db, request, session_user, client_id
        )
        logger.logClientApi(
            "GetStatutoryNotificationsListFilters", "process end"
        )
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetStatutoryNotificationsListReport:
        logger.logClientApi(
            "GetStatutoryNotificationsListReport  - " + str(client_id),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_statutory_notifications_list_report(
            db, request, session_user, client_id
        )
        logger.logClientApi(
            "GetStatutoryNotificationsListReport", "process end"
        )
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetRiskReportFilters:
        logger.logClientApi(
            "GetRiskReportFilters  - " + str(client_id), "process begin")
        logger.logClientApi("------", str(time.time()))
        result = get_risk_report_filters(db, request, session_user, client_id)
        logger.logClientApi("GetRiskReportFilters", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetRiskReport:
        logger.logClientApi(
            "GetRiskReport  - " + str(client_id),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_risk_report(db, request, session_user, client_id)
        logger.logClientApi("GetRiskReport", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetReassignedHistoryReportFilters:
        logger.logClientApi(
            "GetReassignedHistoryReportFilters  - " + str(client_id),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_reassignedhistory_report_filters(
            db, request, session_user, client_id, le_id
        )
        logger.logClientApi("GetReassignedHistoryReportFilters", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetReassignedHistoryReport:
        logger.logClientApi(
            "GetReassignedHistoryReport  - " + str(client_id), "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_reassignedhistory_report(
            db, request, session_user, client_id
        )
        logger.logClientApi("GetReassignedHistoryReport", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetLoginTrace:
        logger.logClientApi(
            "GetLoginTrace  - " + str(client_id), "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_login_trace_report(db, request, session_user, client_id)
        logger.logClientApi("GetLoginTrace", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetComplianceActivityReportFilters:
        logger.logClientApi(
            "GetComplianceActivityReportFilters  - " + str(client_id),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = process_get_compliance_activity_report_filters(
            db, request, session_user, client_id
        )
        logger.logClientApi(
            "GetComplianceActivityReportFilters",
            "process end"
        )
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetComplianceActivityReport:
        logger.logClientApi(
            "GetComplianceActivityReport  - " + str(client_id),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = process_get_compliance_activity_report(
            db, request, session_user, client_id
        )
        logger.logClientApi("GetComplianceActivityReport", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetTaskApplicabilityStatusFilters:
        logger.logClientApi(
            "GetTaskApplicabilityStatusFilters  - " + str(client_id),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = process_get_task_applicability_status_filters(
            db, request, session_user
        )
        logger.logClientApi("GetTaskApplicabilityStatusFilters", "process end")
        logger.logClientApi("------", str(time.time()))

    elif(
            type(request) is
            clientreport.GetComplianceTaskApplicabilityStatusReport
    ):
        logger.logClientApi(
            "GetComplianceTaskApplicabilityStatusReport  - " + str(client_id),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = process_get_task_applicability_report_data(
            db, request, session_user, client_id
        )
        logger.logClientApi(
            "GetComplianceTaskApplicabilityStatusReport", "process end"
        )
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetClientDetailsReportFilters:
        logger.logClientApi(
            "GetClientDetailsReportFilters  - " + str(client_id),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_client_details_report_filters(
            db, request, session_user, client_id
        )
        logger.logClientApi("GetClientDetailsReportFilters", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetClientDetailsReportData:
        logger.logClientApi(
            "GetClientDetailsReportData  - " + str(client_id),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_client_details_report_data(
            db, request, session_user, client_id
        )
        logger.logClientApi("GetClientDetailsReportData", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.ExportToCSV:
        logger.logClientApi(
            "ExportToCSV  - " + str(client_id), "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = export_to_csv(db, request, session_user, client_id)
        logger.logClientApi("ExportToCSV", "process end")
        logger.logClientApi("------", str(time.time()))

    return result


def get_client_report_filters(db, request, session_user):
    user_company_info = get_user_company_details(db, session_user)
    unit_ids = user_company_info[0]
    division_ids = user_company_info[1]
    legal_entity_ids = user_company_info[2]
    business_group_ids = user_company_info[3]
    country_list = get_countries_for_user(db, session_user)
    domain_list = get_domains_for_user(db, session_user)
    business_group_list = get_business_groups_for_user(db, business_group_ids)
    legal_entity_list = get_legal_entities_for_user(db, legal_entity_ids)
    division_list = get_divisions_for_user(db, division_ids)
    unit_list = get_units_for_user(db, unit_ids)
    users_list = get_client_users(db)
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
    from_count = request.from_count
    page_count = request.page_count

    data, total = report_unitwise_compliance(
        db, country_id, domain_id, business_group_id,
        legal_entity_id, division_id, unit_id, user_id, session_user,
        from_count, page_count
    )
    unit_wise_compliances_list = return_unitwise_report(data)
    return clientreport.GetUnitwisecomplianceReportSuccess(
        unit_wise_compliances_list, total
    )


def get_assigneewise_compliance(db, request, session_user):
    country_id = request.country_id
    domain_id = request.domain_id
    business_group_id = request.business_group_id
    legal_entity_id = request.legal_entity_id
    division_id = request.division_id
    unit_id = request.unit_id
    user_id = request.user_id
    from_count = request.from_count
    page_count = request.page_count

    data, total_count = report_assigneewise_compliance(
        db, country_id, domain_id, business_group_id,
        legal_entity_id, division_id, unit_id, user_id, session_user,
        from_count, page_count
    )
    assignee_wise_compliances_list = return_assignee_report_data(data)
    return clientreport.GetAssigneewisecomplianceReportSuccess(
        assignee_wise_compliances_list, total_count
    )


def get_serviceprovider_report_filters(db, request, session_user):
    user_company_info = get_user_company_details(db, session_user)
    unit_ids = user_company_info[0]
    country_list = get_countries_for_user(db, session_user)
    domain_list = get_domains_for_user(db, session_user)
    unit_list = get_units_for_user(db, unit_ids)
    level_1_statutories_list = get_client_level_1_statutoy(db, session_user)
    service_providers_list = get_service_providers(db)

    return clientreport.GetServiceProviderReportFiltersSuccess(
        countries=country_list,
        domains=domain_list,
        level_1_statutories=level_1_statutories_list,
        units=unit_list,
        service_providers=service_providers_list
    )


def get_serviceproviderwise_compliance(db, request, session_user):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "ServiceProviderWise"
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
    else:
        country_id = request.country_id
        domain_id = request.domain_id
        statutory_id = request.statutory_id
        unit_id = request.unit_id
        service_provider_id = request.service_provider_id
        from_count = request.from_count
        page_count = request.page_count

        data, total_count = report_serviceproviderwise_compliance(
            db, country_id, domain_id, statutory_id,
            unit_id, service_provider_id, session_user,
            from_count, page_count
        )
        sp_wise_compliances_list = return_serviceprovider_report_data(data)
        return clientreport.GetServiceProviderWiseComplianceSuccess(
            sp_wise_compliances_list, total_count
        )


def get_compliancedetails_report_filters(db, request, session_user, client_id):
    user_company_info = get_user_company_details(db, session_user)
    unit_ids = user_company_info[0]
    country_list = get_countries_for_user(db, session_user)
    domain_list = get_domains_for_user(db, session_user)
    unit_list = get_units_for_user(db, unit_ids)
    level_1_statutories_list = get_client_level_1_statutoy(db, session_user)
    compliances_list = get_client_compliances(db, session_user)
    users_list = get_client_users(db)
    return clientreport.GetComplianceDetailsReportFiltersSuccess(
        countries=country_list,
        domains=domain_list,
        level_1_statutories=level_1_statutories_list,
        units=unit_list,
        Compliances=compliances_list,
        users=users_list
    )


def get_statutory_notifications_list_filters(
    db, request, session_user, client_id
):
    user_company_info = get_user_company_details(db, session_user)
    unit_ids = user_company_info[0]
    division_ids = user_company_info[1]
    legal_entity_ids = user_company_info[2]
    business_group_ids = user_company_info[3]
    country_list = get_countries_for_user(db, session_user)
    domain_list = get_domains_for_user(db, session_user)
    business_group_list = get_business_groups_for_user(db, business_group_ids)
    legal_entity_list = get_legal_entities_for_user(db, legal_entity_ids)
    division_list = get_divisions_for_user(db, division_ids)
    unit_list = get_units_for_user(db, unit_ids)
    level_1_statutories_list = get_client_level_1_statutoy(db, session_user)
    users_list = get_client_users(db)

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


def get_statutory_notifications_list_report(
    db, request, session_user, client_id
):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "StatutoryNotification"
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
    else:
        result = report_statutory_notifications_list(db, request)
        return clientreport.GetStatutoryNotificationsListReportSuccess(result)


def get_compliancedetails_report(db, request, session_user, client_id):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "ComplianceDetails"
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
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
        from_count = request.from_count
        page_count = request.page_count

        compliance_details_list, total = report_compliance_details(
            db, client_id,
            country_id, domain_id, statutory_id, unit_id, compliance_id,
            assignee_id, from_date, to_date, compliance_status, session_user,
            from_count, page_count
        )
        return clientreport.GetComplianceDetailsReportSuccess(
            compliance_details_list, total
        )


def get_risk_report_filters(db, request, session_user, client_id):
    user_company_info = get_user_company_details(db, session_user)
    unit_ids = user_company_info[0]
    division_ids = user_company_info[1]
    legal_entity_ids = user_company_info[2]
    business_group_ids = user_company_info[3]
    country_list = get_countries_for_user(db, session_user)
    domain_list = get_domains_for_user(db, session_user)
    business_group_list = get_business_groups_for_user(db, business_group_ids)
    legal_entity_list = get_legal_entities_for_user(db, legal_entity_ids)
    division_list = get_divisions_for_user(db, division_ids)
    unit_list = get_units_for_user(db, unit_ids)
    level_1_statutories_list = get_client_level_1_statutoy(db, session_user)
    return clientreport.GetRiskReportFiltersSuccess(
        countries=country_list,
        domains=domain_list,
        business_groups=business_group_list,
        legal_entities=legal_entity_list,
        divisions=division_list,
        units=unit_list,
        level1_statutories=level_1_statutories_list
    )


def get_reassignedhistory_report_filters(db, request, session_user, client_id, le_id):
    #user_company_info = get_user_company_details(db, session_user)
    #unit_ids = user_company_info[0]
    country_list = get_countries_for_user(db, session_user)
    #domain_list = get_domains_for_user(db, session_user)
    #unit_list = get_units_for_user(db, unit_ids)
    #level_1_statutories_list = get_client_level_1_statutoy(db, session_user)
    #compliances_list = get_client_compliances(db, session_user)
    #users_list = get_client_users(db)

    return clientreport.GetReassignedHistoryReportFiltersSuccess(
        countries=country_list,
        #domains=domain_list,
        #units=unit_list,
        #level_1_statutories=level_1_statutories_list,
        #compliances=compliances_list,
        #users=users_list
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
        to_count = 200
        reassigned_history_list, total = report_reassigned_history(
            db, country_id, domain_id, level_1_statutory_id,
            unit_id, compliance_id, user_id, from_date, to_date, session_user,
            from_count, to_count
        )
        return clientreport.GetReassignedHistoryReportSuccess(
            reassigned_history_list, total
        )
    else:
        converter = ConvertJsonToCSV(
            db, request, session_user, "Reassign"
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )


def get_risk_report(db, request, session_user, client_id):
    country_id = request.country_id
    domain_id = request.domain_id
    business_group_id = request.business_group_id
    legal_entity_id = request.legal_entity_id
    division_id = request.division_id
    unit_id = request.unit_id
    level_1_statutory_name = request.level_1_statutory_name
    statutory_status = request.statutory_status
    from_count = request.from_count
    page_count = request.page_count
    compliance_list = []
    if request.csv is False:
        if statutory_status == 1:  # Delayed compliance
            total, compliance_list = get_delayed_compliances_with_count(
                db, country_id, domain_id, business_group_id,
                legal_entity_id, division_id, unit_id, level_1_statutory_name,
                session_user, from_count, page_count
            )
        if statutory_status == 2:  # Not complied
            total, compliance_list = get_not_complied_compliances_with_count(
                db, country_id, domain_id, business_group_id,
                legal_entity_id, division_id, unit_id, level_1_statutory_name,
                session_user, from_count, page_count
            )
        if statutory_status == 3:  # Not opted
            total, compliance_list = get_not_opted_compliances_with_count(
                db, country_id, domain_id, business_group_id,
                legal_entity_id, division_id, unit_id, level_1_statutory_name,
                session_user, from_count, page_count
            )
        if statutory_status == 4:  # Unassigned
            total, compliance_list = get_unassigned_compliances_with_count(
                db, country_id, domain_id, business_group_id,
                legal_entity_id, division_id, unit_id,
                level_1_statutory_name,
                session_user, from_count, page_count
            )
        return clientreport.GetRiskReportSuccess(
            total, compliance_list

        )
    else:
        converter = ConvertJsonToCSV(
            db, request, session_user, "RiskReport"
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )


def get_login_trace_report(db, request, session_user, client_id):
    users_list = get_client_users(db)
    from_count = request.record_count
    user_id = request.user_id
    to_count = RECORD_DISPLAY_COUNT
    from_date = request.from_date
    to_date = request.to_date
    logintracelist = get_login_trace(
        db, client_id, session_user, from_count, to_count, user_id,
        from_date, to_date
    )
    return clientreport.GetLoginTraceSuccess(
        users=users_list,
        login_trace=logintracelist
    )


def process_get_compliance_activity_report_filters(
    db, request, session_user, client_id
):
    user_company_info = get_user_company_details(db, session_user)
    unit_ids = user_company_info[0]
    domain_list = get_domains_for_user(db, session_user)
    unit_list = get_units_for_user(db, unit_ids)
    level_1_statutories_list = get_client_level_1_statutoy(db, session_user)
    compliances_list = get_client_compliances(db, session_user)
    country_list = get_countries_for_user(db, session_user)
    users_list = get_client_users(db)
    return clientreport.GetComplianceActivityReportFiltersSuccess(
        users=users_list,
        domains=domain_list,
        level_1_statutories=level_1_statutories_list,
        units=unit_list,
        compliances=compliances_list,
        countries=country_list
    )


def process_get_compliance_activity_report(
    db, request, session_user, client_id
):
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
        activities = return_compliance_activity_report(
            db, country_id, domain_id, user_type, user_id,
            unit_id, compliance_id, level_1_statutory_name,
            from_date, to_date, session_user, client_id
        )
        return clientreport.GetComplianceActivityReportSuccess(
            activities=activities
        )
    else:
        converter = ConvertJsonToCSV(
            db, request, session_user, "ActivityReport"
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )


def process_get_task_applicability_status_filters(db, request, session_user):
    user_company_info = get_user_company_details(db, session_user)
    unit_ids = user_company_info[0]
    division_ids = user_company_info[1]
    legal_entity_ids = user_company_info[2]
    business_group_ids = user_company_info[3]

    countries = get_countries_for_user(db, session_user)
    domains = get_domains_for_user(db, session_user)
    business_groups = get_business_groups_for_user(db, business_group_ids)
    legal_entities = get_legal_entities_for_user(db, legal_entity_ids)
    divisions = get_divisions_for_user(db, division_ids)
    units = get_units_for_user(db, unit_ids)
    level1_statutories = get_client_level_1_statutoy(db, session_user)
    applicable_status = clientcore.APPLICABILITY_STATUS.values()
    return clientreport.GetTaskApplicabilityStatusFiltersSuccess(
        countries, domains, business_groups, legal_entities,
        divisions, units, level1_statutories, applicable_status
    )


def process_get_task_applicability_report_data(
    db, request, session_user, client_id
):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "TaskApplicability"
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
    else:
        result = get_compliance_task_applicability(db, request, session_user)
        return result


def get_client_details_report_filters(db, request, session_user, client_id):
    countries = get_countries_for_user(db, session_user)
    domains = get_domains_for_user(db, session_user)
    user_company_info = get_user_company_details(db, session_user)
    unit_ids = user_company_info[0]
    division_ids = user_company_info[1]
    legal_entity_ids = user_company_info[2]
    business_group_ids = user_company_info[3]

    business_groups = get_business_groups_for_user(db, business_group_ids)
    legal_entities = get_legal_entities_for_user(db, legal_entity_ids)
    divisions = get_divisions_for_user(db, division_ids)
    units = get_units_for_user(db, unit_ids)
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
        converter = ConvertJsonToCSV(
            db, request, session_user, "ClientDetails"
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
    else:
        units = get_client_details_report(
            db, request.country_id, request.business_group_id,
            request.legal_entity_id, request.division_id, request.unit_id,
            request.domain_ids, session_user, request.from_count, request.page_count
        )
        total_count = get_client_details_count(
            db, request.country_id, request.business_group_id,
            request.legal_entity_id, request.division_id, request.unit_id,
            request.domain_ids, session_user
        )
        return clientreport.GetClientDetailsReportDataSuccess(
            units=units, total_count=total_count
        )


def export_to_csv(db, request, session_user, client_id):
    converter = ConvertJsonToCSV(db, request, session_user)
    return clientreport.ExportToCSVSuccess(link=converter.FILE_DOWNLOAD_PATH)
