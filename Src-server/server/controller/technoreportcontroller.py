import time
from protocol import login, technoreports, knowledgereport
from generalcontroller import validate_user_session, validate_user_forms
from server import logger
from server.constants import RECORD_DISPLAY_COUNT
from server.database.admin import (
    get_countries_for_user, get_domains_for_user
)
from server.database.general import (
    get_compliance_frequency
)
from server.database.technomaster import (
    get_group_companies_for_user,
    get_business_groups_for_user,
    get_legal_entities_for_user,
    get_divisions_for_user,
    get_units_for_user,
)
from server.database.knowledgemaster import (
    get_country_wise_level_1_statutoy,
    get_industries, get_statutory_nature,
    get_geographies,
)
from server.database.technoreport import (
    get_assigned_statutories_report,
    get_statutory_notifications_report_data,
    get_client_details_report,
    get_client_details_report_count,
    get_compliance_list_report_techno
)

__all__ = [
    "process_techno_report_request"
]

forms = [22, 23, 24, 25]


def process_techno_report_request(request, db):
    session_token = request.session_token
    request_frame = request.request
    user_id = validate_user_session(db, session_token)
    if user_id is not None:
        is_valid = validate_user_forms(db, user_id, forms, request_frame)
        if is_valid is not True:
            return login.InvalidSessionToken()
    if user_id is None:
        return login.InvalidSessionToken()

    if type(request_frame) is technoreports.GetAssignedStatutoryReportFilters:
        logger.logKnowledgeApi(
            "GetAssignedStatutoryReportFilters", "process begin"
        )
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_assigned_statutory_report_filters(db, user_id)
        logger.logKnowledgeApi(
            "GetAssignedStatutoryReportFilters", "process end"
        )
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technoreports.GetAssignedStatutoryReport:
        logger.logKnowledgeApi("GetAssignedStatutoryReport", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_assigned_statutory_report_data(
            db, request_frame, user_id
        )
        logger.logKnowledgeApi("GetAssignedStatutoryReport", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technoreports.GetClientDetailsReportFilters:
        logger.logKnowledgeApi(
            "GetClientDetailsReportFilters", "process begin"
        )
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_client_details_report_filters(
            db, request_frame, user_id
        )
        logger.logKnowledgeApi("GetClientDetailsReportFilters", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technoreports.GetClientDetailsReportData:
        logger.logKnowledgeApi("GetClientDetailsReportData", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_client_details_report_data(
            db, request_frame, user_id
        )
        logger.logKnowledgeApi("GetClientDetailsReportData", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technoreports.GetStatutoryNotificationsFilters:
        logger.logKnowledgeApi(
            "GetStatutoryNotificationsFilters", "process begin"
        )
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_statutory_notifications_filters(
            db, request_frame, user_id
        )
        logger.logKnowledgeApi(
            "GetStatutoryNotificationsFilters", "process end"
        )
        logger.logKnowledgeApi("------", str(time.time()))

    elif (
        type(
            request_frame
        ) is technoreports.GetStatutoryNotificationsReportData
    ):
        logger.logKnowledgeApi(
            "GetStatutoryNotificationsReportData", "process begin"
        )
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_statutory_notifications_report_data(
            db, request_frame, user_id
        )
        logger.logKnowledgeApi(
            "GetStatutoryNotificationsReportData", "process end"
        )
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technoreports.GetComplianceTaskFilter:
        logger.logKnowledgeApi("GetComplianceTaskFilter", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_compliance_task_filter(db, request_frame, user_id)
        logger.logKnowledgeApi("GetComplianceTaskFilter", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technoreports.GetComplianceTaskReport:
        logger.logKnowledgeApi("GetComplianceTaskReport", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_compliance_task_report(db, request_frame, user_id)
        logger.logKnowledgeApi("GetComplianceTaskFilter", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    return result


def process_get_assigned_statutory_report_filters(db, user_id):
    countries = get_countries_for_user(db, user_id)
    domains = get_domains_for_user(db, user_id)
    group_companies = get_group_companies_for_user(db, user_id)
    business_groups = get_business_groups_for_user(db, user_id)
    legal_entities = get_legal_entities_for_user(db, user_id)
    divisions = get_divisions_for_user(db, user_id)
    units = get_units_for_user(db, user_id)
    level_1_statutories = get_country_wise_level_1_statutoy(db)
    return technoreports.GetAssignedStatutoryReportFiltersSuccess(
        countries, domains, group_companies,
        business_groups, legal_entities, divisions, units,
        level_1_statutories
    )


def process_get_assigned_statutory_report_data(db, request_frame, user_id):
    return get_assigned_statutories_report(db, request_frame, user_id)


def process_get_statutory_notifications_filters(db, request_frame, user_id):
    countries = get_countries_for_user(db, user_id)
    domains = get_domains_for_user(db, user_id)
    level_1_statutories = get_country_wise_level_1_statutoy(db)
    return technoreports.GetStatutoryNotificationsFiltersSuccess(
        countries=countries,
        domains=domains,
        level_1_statutories=level_1_statutories
    )


def process_get_statutory_notifications_report_data(db, request, user_id):
    countries = get_countries_for_user(db, user_id)
    domains = get_domains_for_user(db, user_id)
    level_1_statutories = get_country_wise_level_1_statutoy(db)
    result = get_statutory_notifications_report_data(db, request)
    return technoreports.GetStatutoryNotificationsReportDataSuccess(
        countries, domains, level_1_statutories, result
    )


def process_get_client_details_report_filters(db, request_frame, session_user):
    countries = get_countries_for_user(db, session_user)
    domains = get_domains_for_user(db, session_user)
    group_companies = get_group_companies_for_user(db, session_user)
    business_groups = get_business_groups_for_user(db, session_user)
    legal_entities = get_legal_entities_for_user(db, session_user)
    divisions = get_divisions_for_user(db, session_user)
    units = get_units_for_user(db, session_user)
    return technoreports.GetClientDetailsReportFiltersSuccess(
        countries=countries,
        domains=domains,
        group_companies=group_companies,
        business_groups=business_groups,
        legal_entities=legal_entities,
        divisions=divisions, units=units
    )


def process_get_client_details_report_data(db, request, session_user):
    to_count = RECORD_DISPLAY_COUNT
    units = get_client_details_report(
        db, request.country_id, request.group_id, request.business_group_id,
        request.legal_entity_id, request.division_id,
        request.unit_id, request.domain_ids, request.start_count, to_count
    )
    total_count = get_client_details_report_count(
        db, request.country_id, request.group_id, request.business_group_id,
        request.legal_entity_id, request.division_id,
        request.unit_id, request.domain_ids
    )
    return technoreports.GetClientDetailsReportDataSuccess(
        units=units, total_count=total_count
    )


def process_get_compliance_task_filter(db, request, session_user):
    countries = get_countries_for_user(db, session_user)
    domains = get_domains_for_user(db, session_user)
    industries = get_industries(db)
    statutory_nature = get_statutory_nature(db)
    geographies = get_geographies(db)
    level_1_statutories = get_country_wise_level_1_statutoy(db)
    compliance_frequency = get_compliance_frequency(db)
    return knowledgereport.GetStatutoryMappingReportFiltersSuccess(
        countries, domains, industries, statutory_nature,
        geographies, level_1_statutories, compliance_frequency
    )


def process_get_compliance_task_report(db, request_frame, user_id):
    country_id = request_frame.country_id
    domain_id = request_frame.domain_id
    industry_id = request_frame.industry_id
    nature_id = request_frame.statutory_nature_id
    geography_id = request_frame.geography_id
    level_1_id = request_frame.level_1_statutory_id
    frequency_id = request_frame.frequency_id
    from_count = request_frame.record_count
    to_count = RECORD_DISPLAY_COUNT
    report_data, total_count = get_compliance_list_report_techno(
        db, country_id, domain_id, industry_id,
        nature_id, geography_id, level_1_id, frequency_id, user_id,
        from_count, to_count
    )

    return knowledgereport.GetStatutoryMappingReportDataSuccess(
        country_id, domain_id, report_data, total_count
    )
