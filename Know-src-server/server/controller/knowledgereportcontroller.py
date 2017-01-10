from protocol import login, knowledgereport
from generalcontroller import (
    validate_user_session, validate_user_forms,
    process_get_domains, process_get_countries
)
from server.constants import RECORD_DISPLAY_COUNT
from server.database.admin import (
    get_countries_for_user, get_domains_for_user
)
from server.database.general import (
    get_compliance_frequency
)
from server.database.knowledgemaster import (
    get_industries, get_statutory_nature,
    get_geographies
)
from server.database.admin import (
    get_level_1_statutories
)
from server.database.knowledgereport import *

__all__ = [
    "process_knowledge_report_request"
]

forms = [12, 13, 14, 15, 16, 17]


def process_knowledge_report_request(request, db):
    session_token = request.session_token
    request_frame = request.request
    user_id = validate_user_session(db, session_token)
    if user_id is not None:
        is_valid = validate_user_forms(db, user_id, forms, request_frame)
        if is_valid is not True:
            return login.InvalidSessionToken()
    if user_id is None:
        return login.InvalidSessionToken()

    if type(request_frame) is knowledgereport.GetStatutoryMappingReportFilters:
        result = process_get_statutory_mapping_filters(
            db, request_frame, user_id
        )

    elif type(request_frame) is knowledgereport.GetStatutoryMappingReportData:
        result = process_get_statutory_mapping_report_data(
            db, request_frame, user_id
        )

    elif type(request_frame) is knowledgereport.GetGeographyReport:
        result = process_get_geography_report(db, request_frame, user_id)

    elif type(request_frame) is knowledgereport.GetDomainsReport:
        result = process_get_domain_report(db, user_id)

    elif type(request_frame) is knowledgereport.GetCountriesReport:
        result = process_get_country_report(db, user_id)

    return result


def process_get_statutory_mapping_filters(db, request_frame, user_id):
    countries = get_countries_for_user(db, user_id)
    domains = get_domains_for_user(db, user_id)
    industries = get_industries(db)
    statutory_nature = get_statutory_nature(db)
    geographies = get_geographies(db)
    #level_1_statutories = get_country_wise_level_1_statutoy(db, user_id)
    level_1_statutories = get_level_1_statutories(db)
    compliance_frequency = get_compliance_frequency(db)
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
    frequency_id = request_frame.frequency_id
    from_count = request_frame.record_count
    to_count = request_frame.page_count
    report_data, total_record = get_statutory_mapping_report(
        db, country_id, domain_id, industry_id,
        nature_id, geography_id, level_1_id, frequency_id, user_id,
        from_count, to_count
    )
    return knowledgereport.GetStatutoryMappingReportDataSuccess(
        country_id, domain_id, report_data, total_record
    )


def process_get_geography_report(db, request_frame, user_id):
    countries = get_countries_for_user(db, user_id)
    geography_report = get_geography_report(db)
    print "geography_data"
    print geography_report

    return knowledgereport.GetGeographyReportSuccess(
        countries, geography_report
    )


def process_get_country_report(db, user_id):
    return process_get_countries(db, user_id)


def process_get_domain_report(db, user_id):
    return process_get_domains(db, user_id)
