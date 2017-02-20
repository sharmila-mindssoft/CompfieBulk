import time
from server.jsontocsvconverter import ConvertJsonToCSV
from clientprotocol import (clientcore, clientreport)
from server import logger
from server.constants import RECORD_DISPLAY_COUNT

from server.clientdatabase.clientreport import *

from server.clientdatabase.general import (
    get_user_company_details,
    get_countries_for_user, get_domains_for_user,
    get_business_groups_for_user, get_legal_entities_for_user,
    get_divisions_for_user, get_units_for_user, get_acts_for_user, 
    get_client_users, get_client_level_1_statutoy, 
    get_service_providers, get_client_compliances,
    get_compliance_frequency, get_divisions,
    get_categories
)

__all__ = [
    "process_client_report_requests"
]

def process_client_report_requests(request, db, session_user, session_category):
    # session_token = request.session_token
    # client_info = request.session_token.split("-")
    request = request.request
    # client_id = int(client_info[0])
    # session_user = db.validate_session_token(session_token)
    # if session_user is None:
    # return clientlogin.InvalidSessionToken()

    if type(request) is clientreport.GetClientReportFilters:
        logger.logClientApi(
            "GetClientReportFilters  - " + str(session_user), "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_client_report_filters(db, request, session_user)
        logger.logClientApi("GetClientReportFilters", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetUnitwisecomplianceReport:
        logger.logClientApi(
            "GetUnitwisecomplianceReport  - " + str(session_user), "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_unitwise_compliance(db, request, session_user)
        logger.logClientApi("GetUnitwisecomplianceReport", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetAssigneewisecomplianceReport:
        logger.logClientApi(
            "GetAssigneewisecomplianceReport  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_assigneewise_compliance(db, request, session_user)
        logger.logClientApi("GetAssigneewisecomplianceReport", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetServiceProviderReportFilters:
        logger.logClientApi(
            "GetServiceProviderReportFilters  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_serviceprovider_report_filters(db, request, session_user)
        logger.logClientApi("GetServiceProviderReportFilters", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetServiceProviderWiseCompliance:
        logger.logClientApi(
            "GetServiceProviderWiseCompliance  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_serviceproviderwise_compliance(db, request, session_user)
        logger.logClientApi("GetServiceProviderWiseCompliance", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetComplianceDetailsReportFilters:
        logger.logClientApi(
            "GetComplianceDetailsReportFilters  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_compliancedetails_report_filters(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetComplianceDetailsReportFilters", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetComplianceDetailsReport:
        logger.logClientApi(
            "GetComplianceDetailsReport  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_compliancedetails_report(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetComplianceDetailsReport", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetStatutoryNotificationsListFilters:
        logger.logClientApi(
            "GetStatutoryNotificationsListFilters  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_statutory_notifications_list_filters(
            db, request, session_user, session_category
        )
        logger.logClientApi(
            "GetStatutoryNotificationsListFilters", "process end"
        )
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetStatutoryNotificationsListReport:
        logger.logClientApi(
            "GetStatutoryNotificationsListReport  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_statutory_notifications_list_report(
            db, request, session_user, session_category
        )
        logger.logClientApi(
            "GetStatutoryNotificationsListReport", "process end"
        )
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetRiskReportFilters:
        logger.logClientApi(
            "GetRiskReportFilters  - " + str(session_user), "process begin")
        logger.logClientApi("------", str(time.time()))
        result = get_risk_report_filters(db, request, session_user, session_category)
        logger.logClientApi("GetRiskReportFilters", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetRiskReport:
        logger.logClientApi(
            "GetRiskReport  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_risk_report(db, request, session_user, session_category)
        logger.logClientApi("GetRiskReport", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetReassignedHistoryReportFilters:
        logger.logClientApi(
            "GetReassignedHistoryReportFilters  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_reassignedhistory_report_filters(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetReassignedHistoryReportFilters", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetReassignedHistoryReport:
        logger.logClientApi(
            "GetReassignedHistoryReport  - " + str(session_user), "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_reassignedhistory_report(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetReassignedHistoryReport", "process end")
        logger.logClientApi("------", str(time.time()))
    elif type(request) is clientreport.GetStatusReportConsolidatedFilters:

        logger.logClientApi(
            "GetStatusReportConsolidatedFilters  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_status_report_consolidated_filters(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetStatusReportConsolidatedFilters", "process end")
        logger.logClientApi("------", str(time.time()))
    elif type(request) is clientreport.GetStatusReportConsolidated:
        logger.logClientApi(
            "GetStatusReportConsolidated  - " + str(session_user), "process begin"
        ) 
        logger.logClientApi("------", str(time.time()))
        result = get_status_report_consolidated(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetStatusReportConsolidated", "process end")
        logger.logClientApi("------", str(time.time()))
    elif type(request) is clientreport.GetStatutorySettingsUnitWiseFilters:

        logger.logClientApi(
            "GetStatutorySettingsUnitWiseFilters  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_statutory_settings_unit_Wise_filters(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetStatutorySettingsUnitWiseFilters", "process end")
        logger.logClientApi("------", str(time.time()))
    elif type(request) is clientreport.GetStatutorySettingsUnitWise:
        logger.logClientApi(
            "GetStatutorySettingsUnitWise  - " + str(session_user), "process begin"
        ) 
        logger.logClientApi("------", str(time.time()))
        result = get_statutory_settings_unit_Wise(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetStatutorySettingsUnitWise", "process end")
        logger.logClientApi("------", str(time.time()))
    elif type(request) is clientreport.GetDomainScoreCardFilters:

        logger.logClientApi(
            "GetDomainScoreCardFilters  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_domain_score_card_filters(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetDomainScoreCardFilters", "process end")
        logger.logClientApi("------", str(time.time()))
    elif type(request) is clientreport.GetDomainScoreCard:
        logger.logClientApi(
            "GetDomainScoreCard  - " + str(session_user), "process begin"
        ) 
        logger.logClientApi("------", str(time.time()))
        result = get_domain_score_card(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetDomainScoreCard", "process end")
        logger.logClientApi("------", str(time.time()))
    elif type(request) is clientreport.GetLEWiseScoreCardFilters:

        logger.logClientApi(
            "GetLEWiseScoreCardFilters  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_le_wise_score_card_filters(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetLEWiseScoreCardFilters", "process end")
        logger.logClientApi("------", str(time.time()))
    elif type(request) is clientreport.GetLEWiseScoreCard:
        logger.logClientApi(
            "GetLEWiseScoreCard  - " + str(session_user), "process begin"
        ) 
        logger.logClientApi("------", str(time.time()))
        result = get_le_wise_score_card(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetLEWiseScoreCard", "process end")
        logger.logClientApi("------", str(time.time()))
    elif type(request) is clientreport.GetLoginTrace:
        logger.logClientApi(
            "GetLoginTrace  - " + str(session_user), "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_login_trace_report(db, request, session_user, session_category)
        logger.logClientApi("GetLoginTrace", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetComplianceActivityReportFilters:
        logger.logClientApi(
            "GetComplianceActivityReportFilters  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = process_get_compliance_activity_report_filters(
            db, request, session_user, session_category
        )
        logger.logClientApi(
            "GetComplianceActivityReportFilters",
            "process end"
        )
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetComplianceActivityReport:
        logger.logClientApi(
            "GetComplianceActivityReport  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = process_get_compliance_activity_report(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetComplianceActivityReport", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetTaskApplicabilityStatusFilters:
        logger.logClientApi(
            "GetTaskApplicabilityStatusFilters  - " + str(session_user),
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
            "GetComplianceTaskApplicabilityStatusReport  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = process_get_task_applicability_report_data(
            db, request, session_user, session_category
        )
        logger.logClientApi(
            "GetComplianceTaskApplicabilityStatusReport", "process end"
        )
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetClientDetailsReportFilters:
        logger.logClientApi(
            "GetClientDetailsReportFilters  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_client_details_report_filters(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetClientDetailsReportFilters", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetClientDetailsReportData:
        logger.logClientApi(
            "GetClientDetailsReportData  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_client_details_report_data(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetClientDetailsReportData", "process end")
        logger.logClientApi("------", str(time.time()))

    # elif type(request) is clientreport.ExportToCSV:
    #     logger.logClientApi(
    #         "ExportToCSV  - " + str(session_user), "process begin"
    #     )
    #     logger.logClientApi("------", str(time.time()))
    #     result = export_to_csv(db, request, session_user, session_category)
    #     logger.logClientApi("ExportToCSV", "process end")
    #     logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetLegalEntityWiseReportFilters:
        logger.logClientApi(
            "GetLegalEntityWiseReportFilters  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_legal_entity_wise_report_filters(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetLegalEntityWiseReportFilters", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetLegalEntityWiseReport:
        logger.logClientApi(
            "GetLegalEntityWiseReport  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_legal_entity_wise_report(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetLegalEntityWiseReport", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetDomainWiseReportFilters:
        logger.logClientApi(
            "GetDomainWiseReportFilters  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_domain_wise_report_filters(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetDomainWiseReportFilters", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetDomainWiseReport:
        logger.logClientApi(
            "GetDomainWiseReport  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_domain_wise_report(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetDomainWiseReport", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetUnitWiseReportFilters:
        logger.logClientApi(
            "GetUnitWiseReportFilters  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_unit_wise_report_filters(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetUnitWiseReportFilters", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetUnitWiseReport:
        logger.logClientApi(
            "GetUnitWiseReport  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_unit_wise_report(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetUnitWiseReport", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetServiceProviderWiseReportFilters:
        logger.logClientApi(
            "GetServiceProviderWiseReportFilters  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_service_provider_wise_report_filters(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetServiceProviderWiseReportFilters", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetServiceProviderWiseReport:
        logger.logClientApi(
            "GetServiceProviderWiseReport  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_service_provider_wise_report(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetServiceProviderWiseReport", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetUserWiseReportFilters:
        logger.logClientApi(
            "GetUserWiseReportFilters  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_user_wise_report_filters(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetUserWiseReportFilters", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetUserWiseReport:
        logger.logClientApi(
            "GetUserWiseReport  - " + str(session_user),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_user_wise_report(
            db, request, session_user, session_category
        )
        logger.logClientApi("GetUserWiseReport", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetUnitListReportFilters:
        logger.logClientApi(
            "GetUnitListReportFilters  - " + str(client_id),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_unit_list_report_filters(
            db, request, session_user, client_id
        )
        logger.logClientApi("GetUnitListReportFilters", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetUnitListReport:
        logger.logClientApi(
            "GetUnitListReport  - " + str(client_id),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_unit_list_report(
            db, request, session_user, client_id
        )
        logger.logClientApi("GetUnitListReport", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetStatutoryNotificationsListReportFilters:
        logger.logClientApi(
            "GetStatutoryNotificationsListReportFilters  - " + str(client_id),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_statutory_notifications_list_report_filters(
            db, request, session_user, client_id
        )
        logger.logClientApi("GetStatutoryNotificationsListReportFilters", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetStatutoryNotificationsListReportData:
        logger.logClientApi(
            "GetStatutoryNotificationsListReportData  - " + str(client_id),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_statutory_notification_list_report(
            db, request, session_user, client_id
        )
        logger.logClientApi("GetStatutoryNotificationsListReportData", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientreport.GetAuditTrailReportData:
        logger.logClientApi(
            "GetAuditTrailReportData  - " + str(client_id),
            "process begin"
        )
        logger.logClientApi("------", str(time.time()))
        result = get_audit_trail_report_data(
            db, request, session_user, client_id
        )
        logger.logClientApi("GetAuditTrailReportData", "process end")
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


def get_compliancedetails_report_filters(db, request, session_user, session_category):
    user_company_info = get_user_company_details(db, session_user)
    unit_ids = user_company_info[0]
    country_list = get_countries_for_user(db, session_user)
    domain_list = get_domains_for_user(db, session_user, session_category)
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
    db, request, session_user, session_category
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
    db, request, session_user, session_category
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


def get_compliancedetails_report(db, request, session_user, session_category):
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
            db, country_id, domain_id, statutory_id, unit_id, compliance_id,
            assignee_id, from_date, to_date, compliance_status, session_user,
            from_count, page_count
        )
        return clientreport.GetComplianceDetailsReportSuccess(
            compliance_details_list, total
        )


def get_risk_report_filters(db, request, session_user, session_category):
    user_company_info = get_user_company_details(db, session_user)
    unit_ids = user_company_info[0]
    division_ids = user_company_info[1]
    legal_entity_ids = user_company_info[2]
    business_group_ids = user_company_info[3]
    country_list = get_countries_for_user(db, session_user)
    domain_list = get_domains_for_user(db, session_user, session_category)
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

# Reassigned History Report Start
def get_reassignedhistory_report_filters(db, request, session_user, session_category):
    domain_list = get_domains_for_user(db, session_user, session_category)
    unit_list = get_units_for_user(db, session_user)
    acts_list = get_acts_for_user(db, session_user)
    compliances_list = get_client_compliances(db, session_user)
    users_list = get_client_users(db)

    return clientreport.GetReassignedHistoryReportFiltersSuccess(
        domains=domain_list,
        units=unit_list,
        acts=acts_list,
        compliances=compliances_list,
        legal_entity_users=users_list
    )

def get_reassignedhistory_report(db, request, session_user, session_category):
    if not request.csv:
        country_id = request.c_id
        legal_entity_id = request.legal_entity_id
        domain_id = request.d_id
        unit_id = request.unit_id
        act = request.act
        compliance_id = request.compliance_id
        usr_id = request.usr_id
        from_date = request.from_date
        to_date = request.to_date
        csv = request.csv
        f_count = request.f_count
        t_count = request.t_count

        reassigned_history_list = report_reassigned_history(
            db, country_id, legal_entity_id, domain_id, unit_id, 
            act, compliance_id, usr_id, from_date, to_date, session_user, f_count, t_count
        )
        total_count = report_reassigned_history_total(
            db, country_id, legal_entity_id, domain_id, unit_id, 
            act, compliance_id, usr_id, from_date, to_date, session_user
        )
        return clientreport.GetReassignedHistoryReportSuccess(
            reassigned_history_list, total_count
        )
    else:
        converter = ConvertJsonToCSV(
            db, request, session_user, "Reassign"
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
# Reassigned History Report End

# Status Report Consolidated Report Start
def get_status_report_consolidated_filters(db, request, session_user, session_category):
    domain_list = get_domains_for_user(db, session_user, session_category)
    unit_list = get_units_for_user(db, session_user)
    acts_list = get_acts_for_user(db, session_user)
    compliances_list = get_client_compliances(db, session_user)
    compliance_frequency_list = get_compliance_frequency(db)
    users_list = get_client_users(db)

    return clientreport.GetStatusReportConsolidatedFiltersSuccess(
        domains=domain_list,
        units=unit_list,
        acts=acts_list,
        compliances=compliances_list,
        compliance_frequency = compliance_frequency_list,
        legal_entity_users=users_list
    )

def get_status_report_consolidated(db, request, session_user, session_category):
    if not request.csv:
        country_id = request.c_id
        legal_entity_id = request.legal_entity_id
        domain_id = request.d_id
        unit_id = request.unit_id
        act = request.act
        compliance_id = request.compliance_id
        frequency_id = request.frequency_id
        user_type_id = request.user_type_id
        status_name = request.status_name
        usr_id = request.usr_id
        from_date = request.from_date
        to_date = request.to_date
        csv = request.csv
        f_count = request.f_count
        t_count = request.t_count

        status_report_consolidated_list = report_status_report_consolidated(
            db, country_id, legal_entity_id, domain_id, unit_id, 
            act, compliance_id, frequency_id, user_type_id, status_name, usr_id, from_date, to_date, session_user, f_count, t_count
        )
        total_count = report_status_report_consolidated_total(
            db, country_id, legal_entity_id, domain_id, unit_id, 
            act, compliance_id, frequency_id, user_type_id, status_name, usr_id, from_date, to_date, session_user
        )
        return clientreport.GetStatusReportConsolidatedSuccess(
            status_report_consolidated_list, total_count
        )
    else:
        converter = ConvertJsonToCSV(
            db, request, session_user, "Reassign"
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
# Status Report Consolidated Report End

# Statutory Settings Unit Wise Start
def get_statutory_settings_unit_Wise_filters(db, request, session_user, session_category):
    domain_list = get_domains_for_user(db, session_user, session_category)
    unit_list = get_units_for_user(db, session_user)
    acts_list = get_acts_for_user(db, session_user)
    compliances_list = get_client_compliances(db, session_user)
    compliance_frequency_list = get_compliance_frequency(db)
    divisions_list = get_divisions(db)
    categories_list = get_categories(db)

    return clientreport.GetStatutorySettingsUnitWiseFiltersSuccess(
        domains=domain_list,
        units=unit_list,
        acts=acts_list,
        compliances=compliances_list,
        compliance_frequency = compliance_frequency_list,
        divisions=divisions_list,
        categories=categories_list
    )

def get_statutory_settings_unit_Wise(db, request, session_user, session_category):
    if not request.csv:
        country_id = request.c_id
        bg_id = request.bg_id
        legal_entity_id = request.legal_entity_id
        domain_id = request.d_id
        unit_id = request.unit_id
        div_id = request.div_id
        cat_id = request.cat_id
        act = request.act
        compliance_id = request.compliance_id
        frequency_id = request.frequency_id
        status_name = request.status_name
        csv = request.csv
        f_count = request.f_count
        t_count = request.t_count

        statutory_settings_unit_Wise_list = report_statutory_settings_unit_Wise(
            db, country_id, bg_id, legal_entity_id, domain_id, unit_id, 
            div_id, cat_id, act, compliance_id, frequency_id, status_name, session_user, f_count, t_count
        )
        total_count = report_statutory_settings_unit_Wise_total(
            db, country_id, bg_id, legal_entity_id, domain_id, unit_id, div_id, cat_id, 
            act, compliance_id, frequency_id, status_name, session_user
        )
        return clientreport.GetStatutorySettingsUnitWiseSuccess(
            statutory_settings_unit_Wise_list, total_count
        )
    else:
        converter = ConvertJsonToCSV(
            db, request, session_user, "Reassign"
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
# Statutory Settings Unit Wise End

# Domain Score Card Start
def get_domain_score_card_filters(db, request, session_user, session_category):
    domain_list = get_domains_for_user(db, session_user, session_category)
    divisions_list = get_divisions(db)
    categories_list = get_categories(db)

    return clientreport.GetDomainScoreCardFiltersSuccess(
        domains=domain_list,
        divisions=divisions_list,
        categories=categories_list
    )

def get_domain_score_card(db, request, session_user, session_category):
    if not request.csv:
        country_id = request.c_id
        bg_id = request.bg_id
        legal_entity_id = request.legal_entity_id
        domain_id = request.d_id
        div_id = request.div_id
        cat_id = request.cat_id

        domain_score_card_list = report_domain_score_card(
            db, country_id, bg_id, legal_entity_id, domain_id, div_id, cat_id, session_user
        )
        return clientreport.GetDomainScoreCardSuccess(domain_score_card_list)
    else:
        converter = ConvertJsonToCSV(
            db, request, session_user, "Reassign"
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
# Domain Score Card End


# Legal Entity Wise Score Card Start
def get_le_wise_score_card_filters(db, request, session_user, session_category):
    domain_list = get_domains_for_user(db, session_user, session_category)

    return clientreport.GetLEWiseScoreCardFiltersSuccess(
        domains=domain_list
    )

def get_le_wise_score_card(db, request, session_user, session_category):
    if not request.csv:
        country_id = request.c_id
        legal_entity_id = request.legal_entity_id
        domain_id = request.d_id

        le_wise_score_card_list = report_le_wise_score_card(
            db, country_id, legal_entity_id, domain_id, session_user
        )
        return clientreport.GetLEWiseScoreCardSuccess(le_wise_score_card_list)
    else:
        converter = ConvertJsonToCSV(
            db, request, session_user, "Reassign"
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
# Legal Entity Wise Score Card End

def get_risk_report(db, request, session_user, session_category):
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


def get_login_trace_report(db, request, session_user, session_category):
    users_list = get_client_users(db)
    from_count = request.record_count
    user_id = request.user_id
    to_count = RECORD_DISPLAY_COUNT
    from_date = request.from_date
    to_date = request.to_date
    logintracelist = get_login_trace(
        db, session_user, from_count, to_count, user_id,
        from_date, to_date
    )
    return clientreport.GetLoginTraceSuccess(
        users=users_list,
        login_trace=logintracelist
    )


def process_get_compliance_activity_report_filters(
    db, request, session_user, session_category
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
    db, request, session_user, session_category
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
            from_date, to_date, session_user
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
    db, request, session_user, session_category
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


def get_client_details_report_filters(db, request, session_user, session_category):
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


def get_client_details_report_data(db, request, session_user, session_category):
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


def export_to_csv(db, request, session_user, session_category):
    converter = ConvertJsonToCSV(db, request, session_user)
    return clientreport.ExportToCSVSuccess(link=converter.FILE_DOWNLOAD_PATH)


###############################################################################################
# Objective: To get the filters data under selected legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains domain list, compliances, units
###############################################################################################

def get_legal_entity_wise_report_filters(db, request, session_user, session_category):
    country_id = request.country_id
    legal_entity_id = request.legal_entity_id
    domains_list = get_domains_for_le(db, legal_entity_id)
    unit_list = get_units_for_le_domain(db, country_id, legal_entity_id)
    act_list = get_acts_for_le_domain(db, legal_entity_id, country_id)
    task_list = get_task_for_le_domain(db, legal_entity_id)
    frequency_list = get_frequency_list(db)
    compliance_user_type = get_compliance_user_type(db)
    compliance_status = get_compiance_status(db)
    compliance_user_list = get_compliance_user_list(db, country_id, legal_entity_id)
    return clientreport.GetLegalEntityWiseReportFiltersSuccess(
        domains=domains_list, unit_legal_entity=unit_list, act_legal_entity=act_list,
        compliance_task_list=task_list, compliance_frequency_list=frequency_list,
        compliance_user_type=compliance_user_type, compliance_task_status=compliance_status,
        compliance_users=compliance_user_list
    )

###############################################################################################
# Objective: To get legal entity wise compliances data under selected legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains compliance list with the status
###############################################################################################
def get_legal_entity_wise_report(db, request, session_user, session_category):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "LegalEntityWiseReport"
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
    else:
        result = process_legal_entity_wise_report(db, request)
        return clientreport.GetLegalEntityWiseReportSuccess(legal_entities_compliances=result)

###############################################################################################
# Objective: To get the filters data under selected legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains domain list, compliances, units
###############################################################################################

def get_domain_wise_report_filters(db, request, session_user, session_category):
    country_id = request.country_id
    legal_entity_id = request.legal_entity_id
    domains_list = get_domains_for_le(db, legal_entity_id)
    unit_list = get_units_for_le_domain(db, country_id, legal_entity_id)
    act_list = get_acts_for_le_domain(db, legal_entity_id, country_id)
    task_list = get_task_for_le_domain(db, legal_entity_id)
    frequency_list = get_frequency_list(db)
    compliance_user_type = get_compliance_user_type(db)
    compliance_status = get_compiance_status(db)
    compliance_user_list = get_compliance_user_list(db, country_id, legal_entity_id)
    return clientreport.GetDomainWiseReportFiltersSuccess(
        domains=domains_list, unit_legal_entity=unit_list, act_legal_entity=act_list,
        compliance_task_list=task_list, compliance_frequency_list=frequency_list,
        compliance_user_type=compliance_user_type, compliance_task_status=compliance_status,
        compliance_users=compliance_user_list
    )

###############################################################################################
# Objective: To get legal entity wise compliances data under selected legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains compliance list with the status
###############################################################################################
def get_domain_wise_report(db, request, session_user, session_category):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "DomainWiseReport"
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
    else:
        result = process_domain_wise_report(db, request)
        return clientreport.GetDomainWiseReportSuccess(legal_entities_compliances=result)


###############################################################################################
# Objective: To get the filters data under selected legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains domain list, compliances, units
###############################################################################################

def get_unit_wise_report_filters(db, request, session_user, session_category):
    country_id = request.country_id
    legal_entity_id = request.legal_entity_id
    domains_list = get_domains_for_le(db, legal_entity_id)
    unit_list = get_units_for_le_domain(db, country_id, legal_entity_id)
    act_list = get_acts_for_le_domain(db, legal_entity_id, country_id)
    task_list = get_task_for_le_domain(db, legal_entity_id)
    frequency_list = get_frequency_list(db)
    compliance_user_type = get_compliance_user_type(db)
    compliance_status = get_compiance_status(db)
    compliance_user_list = get_compliance_user_list(db, country_id, legal_entity_id)
    return clientreport.GetUnitWiseReportFiltersSuccess(
        domains=domains_list, unit_legal_entity=unit_list, act_legal_entity=act_list,
        compliance_task_list=task_list, compliance_frequency_list=frequency_list,
        compliance_user_type=compliance_user_type, compliance_task_status=compliance_status,
        compliance_users=compliance_user_list
    )

###############################################################################################
# Objective: To get unit wise compliances data under selected legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains compliance list with the status
###############################################################################################
def get_unit_wise_report(db, request, session_user, session_category):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "UnitWiseReport"
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
    else:
        result = process_unit_wise_report(db, request)
        return clientreport.GetUnitWiseReportSuccess(unit_compliances=result)


###############################################################################################
# Objective: To get the filters data under selected legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains service provider list, domain list, compliances.
###############################################################################################
def get_service_provider_wise_report_filters(db, request, session_user, session_category):
    country_id = request.country_id
    legal_entity_id = request.legal_entity_id
    sp_list = get_service_providers_list(db)
    sp_domains_list = get_domains_for_sp_users(db, legal_entity_id)
    sp_unit_list = get_units_for_sp_users(db, country_id, legal_entity_id)
    sp_act_task_list = get_acts_for_sp_users(db, legal_entity_id, country_id)
    compliance_status = get_compiance_status(db)
    sp_user_list = get_service_provider_user_list(db, country_id, legal_entity_id)
    return clientreport.GetServiceProviderWiseReportFiltersSuccess(
        sp_domains_list=sp_domains_list, sp_unit_list=sp_unit_list,
        sp_act_task_list=sp_act_task_list, sp_list=sp_list,
        compliance_task_status=compliance_status, sp_users_list=sp_user_list
    )

###############################################################################################
# Objective: To get unit wise compliances data under selected legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains compliance list with the status
###############################################################################################
def get_service_provider_wise_report(db, request, session_user, session_category):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "ServiceProviderWiseReport"
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
    else:
        result = process_service_provider_wise_report(db, request)
        return clientreport.GetServiceProviderWiseReportSuccess(sp_compliances=result)


###############################################################################################
# Objective: To get the filters data under selected legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains users lits, domain list, compliances, units
###############################################################################################

def get_user_wise_report_filters(db, request, session_user, session_category):
    country_id = request.country_id
    legal_entity_id = request.legal_entity_id
    le_users_list = get_le_users_list(db)
    user_domains_list = get_domains_for_le_users(db, legal_entity_id)
    users_units_list = get_units_for_le_users(db, country_id, legal_entity_id)
    user_act_task_list = get_acts_for_le_users(db, legal_entity_id, country_id)
    frequency_list = get_frequency_list(db)
    compliance_user_type = get_compliance_user_type(db)
    compliance_status = get_compiance_status(db)
    return clientreport.GetUserWiseReportFiltersSuccess(
        le_users_list=le_users_list, user_domains_list=user_domains_list,
        users_units_list=users_units_list,
        user_act_task_list=user_act_task_list,
        compliance_frequency_list=frequency_list,
        compliance_user_type=compliance_user_type, compliance_task_status=compliance_status
    )

###############################################################################################
# Objective: To get unit wise compliances data under selected legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains compliance list with the status
###############################################################################################
def get_user_wise_report(db, request, session_user, session_category):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "UserWiseReport"
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
    else:
        result = process_user_wise_report(db, request)
        return clientreport.GetUserWiseReportSuccess(user_compliances=result)


###############################################################################################
# Objective: To get the filters data under selected legal entity, country and business group
# Parameter: request object and the client id
# Result: list of record sets which contains division, category, unit, domain and organization
###############################################################################################
def get_unit_list_report_filters(db, request, session_user, client_id):
    country_id = request.country_id
    business_group_id = request.business_group_id
    legal_entity_id = request.legal_entity_id
    divsions_list = get_divisions_for_unit_list(db, business_group_id, legal_entity_id)
    categories_list = get_categories_for_unit_list(db, business_group_id, legal_entity_id)
    units_list = get_units_list(db, country_id, business_group_id, legal_entity_id)
    domains_organisation_list = get_domains_organization_for_le(db, legal_entity_id)
    unit_status_list = get_units_status(db)
    return clientreport.GetUnitListReportFiltersSuccess(
        divisions=divsions_list, categories=categories_list, units_list=units_list,
        domains_organisations_list=domains_organisation_list, unit_status_list=unit_status_list
    )

###############################################################################################
# Objective: To get unit details under selected legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains units and its status
###############################################################################################
def get_unit_list_report(db, request, session_user, client_id):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "UnitListReport"
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
    else:
        result = process_unit_list_report(db, request)
        return clientreport.GetunitListReportSuccess(unit_list_report=result)

###############################################################################################
# Objective: To get domains and acts under legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains domains and acts
###############################################################################################
def get_statutory_notifications_list_report_filters(db, request, session_user, client_id):
    country_id = request.country_id
    legal_entity_id = request.legal_entity_id
    domain_list = get_domains_for_le(db, legal_entity_id)
    act_list = get_acts_for_le_domain(db, legal_entity_id, country_id)
    return clientreport.GetStatutoryNotificationsListReportFilterSuccess(
        domains=domain_list, act_legal_entity=act_list
    )


###############################################################################################
# Objective: To get statutory notification list under domain and legal entity
# Parameter: request object and the client id
# Result: list of record sets which contains act and compliance tasks
###############################################################################################
def get_statutory_notification_list_report(db, request, session_user, client_id):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "StatutoryNotificationListReport"
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
    else:
        result = process_statutory_notification_list_report(db, request)
        return clientreport.GetStatutoryNotificationReportDataSuccess(stat_notf_list_report=result)

###############################################################################################
# Objective: To get activity log under user and form
# Parameter: request object and the client id
# Result: list of record sets which contains activity log of forms
###############################################################################################
def get_audit_trail_report_data(db, request, session_user, client_id):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "AuditTrailReport"
        )
        return clientreport.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
    else:
        result = process_audit_trail_report(db, request)
        return clientreport.GetAuditTrailReportDataSuccess(audit_activities=result)
