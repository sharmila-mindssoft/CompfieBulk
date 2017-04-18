from protocol import knowledgereport
from generalcontroller import (
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


def process_knowledge_report_request(request, db, user_id):

    request_frame = request.request

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

##############################################################################
# To get geography report and countries list under user id
# Returns the list of countries and geographies
##############################################################################
def process_get_geography_report(db, request_frame, user_id):
    countries = get_countries_for_user(db, user_id)
    geography_report = get_geography_report(db)

    return knowledgereport.GetGeographyReportSuccess(
        countries, geography_report
    )

##############################################################################
# To generate country master report under user id
# Returns countries list
##############################################################################
def process_get_country_report(db, user_id):
    return process_get_countries(db, user_id)

##############################################################################
# To generate domain master report under report
# Returns domains list
##############################################################################
def process_get_domain_report(db, user_id):
    return process_get_domains(db, user_id)
