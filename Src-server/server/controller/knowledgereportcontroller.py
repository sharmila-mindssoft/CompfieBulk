from protocol import login, knowledgereport
from generalcontroller import (
    validate_user_session, validate_user_forms,
    process_get_domains, process_get_countries
)

__all__ = [
    "process_knowledge_report_request"
]

forms = [12, 13, 14, 15, 16, 17]


def process_knowledge_report_request(request, db) :
    session_token = request.session_token
    request_frame = request.request
    user_id = validate_user_session(db, session_token)
    if user_id is not None :
        is_valid = validate_user_forms(db, user_id, forms, request_frame)
        if is_valid is not True :
            return login.InvalidSessionToken()
    if user_id is None:
        return login.InvalidSessionToken()

    if type(request_frame) is knowledgereport.GetStatutoryMappingReportFilters :
        return process_get_statutory_mapping_filters(db, request_frame, user_id)

    elif type(request_frame) is knowledgereport.GetStatutoryMappingReportData :
        return process_get_statutory_mapping_report_data(db, request_frame, user_id)

    elif type(request_frame) is knowledgereport.GetGeographyReport:
        return process_get_geography_report(db, request_frame, user_id)

    elif type(request_frame) is knowledgereport.GetDomainsReport:
        return process_get_domain_report(db, user_id)

    elif type(request_frame) is knowledgereport.GetCountriesReport:
        return process_get_country_report(db, user_id)

def process_get_statutory_mapping_filters(db, request_frame, user_id):
    countries = db.get_countries_for_user(user_id)
    domains = db.get_domains_for_user(user_id)
    industries = db.get_industries()
    statutory_nature = db.get_statutory_nature()
    geographies = db.get_geographies()
    level_1_statutories = db.get_country_wise_level_1_statutoy()
    compliance_frequency = db.get_compliance_frequency()
    return knowledgereport.GetStatutoryMappingReportFiltersSuccess(
        countries, domains, industries, statutory_nature,
        geographies, level_1_statutories, compliance_frequency
    )

def process_get_statutory_mapping_report_data(db, request_frame, user_id):
    country_id = request_frame.country_id
    domain_id = request_frame.domain_id
    industry_id = request_frame.industry_id
    nature_id = request_frame.statutory_nature_id
    geography_id = request_frame.geography_id
    level_1_id = request_frame.level_1_statutory_id

    report_data = db.get_statutory_mapping_report(
        country_id, domain_id, industry_id,
        nature_id, geography_id, level_1_id, user_id
    )
    # statutory_mappings = {
    # if level_1_id is None:
    #     statutory_mappings = report_data
    # else :
    #     statutory_mappings[level_1_id] = report_data[level_1_id]

    return knowledgereport.GetStatutoryMappingReportDataSuccess(
        country_id, domain_id, report_data
    )

def process_get_geography_report(db, request_frame, user_id):
    countries = db.get_countries_for_user(user_id)
    geography_data = db.get_geography_report()

    return knowledgereport.GetGeographyReportSuccess(
        countries, geography_data
    )

def process_get_country_report(db, user_id):
    return process_get_countries(db, user_id)

def process_get_domain_report(db, user_id):
    return process_get_domains(db, user_id)
