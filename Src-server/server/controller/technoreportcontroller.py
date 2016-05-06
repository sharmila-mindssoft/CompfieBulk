from protocol import login, technoreports, knowledgereport
from generalcontroller import validate_user_session, validate_user_forms
from server import logger
__all__ = [
    "process_techno_report_request"
]

forms = [22, 23, 24, 25]

def process_techno_report_request(request, db):
    session_token = request.session_token
    request_frame = request.request
    user_id = validate_user_session(db, session_token)
    if user_id is not None :
        is_valid = validate_user_forms(db, user_id, forms, request_frame)
        if is_valid is not True :
            return login.InvalidSessionToken()
    if user_id is None:
        return login.InvalidSessionToken()

    if type(request_frame) is technoreports.GetAssignedStatutoryReportFilters:
        logger.logKnowledgeApi("GetAssignedStatutoryReportFilters", "process begin")
        result = process_get_assigned_statutory_report_filters(db, user_id)
        logger.logKnowledgeApi("GetAssignedStatutoryReportFilters", "process end")

    elif type(request_frame) is technoreports.GetAssignedStatutoryReport:
        logger.logKnowledgeApi("GetAssignedStatutoryReport", "process begin")
        result = process_get_assigned_statutory_report_data(db, request_frame, user_id)
        logger.logKnowledgeApi("GetAssignedStatutoryReport", "process end")

    elif type(request_frame) is technoreports.GetClientDetailsReportFilters:
        logger.logKnowledgeApi("GetClientDetailsReportFilters", "process begin")
        result = process_get_client_details_report_filters(db, request_frame, user_id)
        logger.logKnowledgeApi("GetClientDetailsReportFilters", "process end")

    elif type(request_frame) is technoreports.GetClientDetailsReportData:
        logger.logKnowledgeApi("GetClientDetailsReportData", "process begin")
        result = process_get_client_details_report_data(db, request_frame, user_id)
        logger.logKnowledgeApi("GetClientDetailsReportData", "process end")

    elif type(request_frame) is technoreports.GetStatutoryNotificationsFilters:
        logger.logKnowledgeApi("GetStatutoryNotificationsFilters", "process begin")
        result = process_get_statutory_notifications_filters(db, request_frame, user_id)
        logger.logKnowledgeApi("GetStatutoryNotificationsFilters", "process end")

    elif type(request_frame) is technoreports.GetStatutoryNotificationsReportData:
        logger.logKnowledgeApi("GetStatutoryNotificationsReportData", "process begin")
        result = process_get_statutory_notifications_report_data(db, request_frame, user_id)
        logger.logKnowledgeApi("GetStatutoryNotificationsReportData", "process end")

    elif type(request_frame) is technoreports.GetComplianceTaskFilter :
        logger.logKnowledgeApi("GetComplianceTaskFilter", "process begin")
        result = process_get_compliance_task_filter(db, request_frame, user_id)
        logger.logKnowledgeApi("GetComplianceTaskFilter", "process end")

    elif type(request_frame) is technoreports.GetComplianceTaskReport :
        logger.logKnowledgeApi("GetComplianceTaskReport", "process begin")
        result = process_get_compliance_task_report(db, request_frame, user_id)
        logger.logKnowledgeApi("GetComplianceTaskFilter", "process end")

    return result

def process_get_assigned_statutory_report_filters(db, user_id):
    countries = db.get_countries_for_user(user_id)
    domains = db.get_domains_for_user(user_id)
    group_companies = db.get_group_companies_for_user(user_id)
    business_groups = db.get_business_groups_for_user(user_id)
    legal_entities = db.get_legal_entities_for_user(user_id)
    divisions = db.get_divisions_for_user(user_id)
    units = db.get_units_for_user(user_id)
    level_1_statutories = db.get_country_wise_level_1_statutoy()
    return technoreports.GetAssignedStatutoryReportFiltersSuccess(
        countries, domains, group_companies,
        business_groups, legal_entities, divisions, units,
        level_1_statutories
    )

def process_get_assigned_statutory_report_data(db, request_frame, user_id):
    return db.get_assigned_statutories_report(request_frame, user_id)

def process_get_statutory_notifications_filters(db, request_frame, user_id):
    countries = db.get_countries_for_user(user_id)
    domains = db.get_domains_for_user(user_id)
    level_1_statutories = db.get_country_wise_level_1_statutoy()
    return technoreports.GetStatutoryNotificationsFiltersSuccess(
        countries=countries,
        domains=domains,
        level_1_statutories=level_1_statutories
    )

def process_get_statutory_notifications_report_data(db, request, user_id):
    countries = db.get_countries_for_user(user_id)
    domains = db.get_domains_for_user(user_id)
    level_1_statutories = db.get_country_wise_level_1_statutoy()
    print "level_!_statatatat: {} ".format(level_1_statutories)
    print "inside process_get_statutory_notifications_report_data: {}".format(request)
    result = db.get_statutory_notifications_report_data(request)
    return technoreports.GetStatutoryNotificationsReportDataSuccess(countries, domains, level_1_statutories, result)

def process_get_client_details_report_filters(db, request_frame, session_user):
    countries = db.get_countries_for_user(session_user)
    domains = db.get_domains_for_user(session_user)
    group_companies = db.get_group_companies_for_user(session_user)
    business_groups = db.get_business_groups_for_user(session_user)
    legal_entities = db.get_legal_entities_for_user(session_user)
    divisions = db.get_divisions_for_user(session_user)
    units = db.get_units_for_user(session_user)
    return technoreports.GetClientDetailsReportFiltersSuccess(
        countries=countries,
        domains=domains,
        group_companies=group_companies,
        business_groups=business_groups,
        legal_entities=legal_entities,
        divisions=divisions, units=units
    )

def process_get_client_details_report_data(db, request, session_user):
    units = db.get_client_details_report(
        request.country_id, request.group_id, request.business_group_id,
        request.legal_entity_id, request.division_id,
        request.unit_id, request.domain_ids
    )
    return technoreports.GetClientDetailsReportDataSuccess(units=units)

def process_get_compliance_task_filter(db, request, session_user):
    countries = db.get_countries_for_user(session_user)
    domains = db.get_domains_for_user(session_user)
    industries = db.get_industries()
    statutory_nature = db.get_statutory_nature()
    geographies = db.get_geographies()
    level_1_statutories = db.get_country_wise_level_1_statutoy()
    compliance_frequency = db.get_compliance_frequency()
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
    from_count = request_frame.record_count
    to_count = 500
    report_data, total_count = db.get_compliance_list_report_techno(
        country_id, domain_id, industry_id,
        nature_id, geography_id, level_1_id, user_id,
        from_count, to_count
    )

    return knowledgereport.GetStatutoryMappingReportDataSuccess(
        country_id, domain_id, report_data, total_count
    )
