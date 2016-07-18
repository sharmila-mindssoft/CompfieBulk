import time
from protocol import login, technotransactions
from generalcontroller import validate_user_session, validate_user_forms, process_get_countries_for_user
from server import logger
from server.database.admin import (
    get_domains_for_user
)
from server.database.knowledgemaster import (
    get_industries,
    get_geographies,
    get_geograhpy_levels_for_user

)
from server.database.technotransaction import (
    get_groups_for_country,
    get_business_groups_for_country,
    get_legal_entity_for_country,
    get_divisions_for_country,
    get_units_for_country,
    get_assign_statutory_wizard_two,
    save_assigned_statutories,
    get_assigned_statutories_list,
    get_assigned_statutories_by_id
)

__all__ = [
    "process_techno_transaction_request"
]

forms = [21]

def process_techno_transaction_request(request, db):
    session_token = request.session_token
    request_frame = request.request
    user_id = validate_user_session(db, session_token)
    if user_id is not None :
        is_valid = validate_user_forms(db, user_id, forms, request_frame)
        if is_valid is not True :
            return login.InvalidSessionToken()

    if user_id is None:
        return login.InvalidSessionToken()

    if type(request_frame) is technotransactions.GetAssignedStatutoriesList:
        logger.logKnowledgeApi("GetAssignedStatutoriesList", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_assigned_statutories(db, user_id)
        logger.logKnowledgeApi("GetAssignedStatutoriesList", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technotransactions.GetAssignedStatutoriesById:
        logger.logKnowledgeApi("GetAssignedStatutoriesById", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_assigned_statutories_by_id(db, request_frame)
        logger.logKnowledgeApi("GetAssignedStatutoriesById", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technotransactions.GetAssignedStatutoryWizardOneData:
        logger.logKnowledgeApi("GetAssignedStatutoryWizardOneData", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_assigned_statutory_wizard_one(db, request_frame, user_id)
        logger.logKnowledgeApi("GetAssignedStatutoryWizardOneData", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technotransactions.GetStatutoryWizardTwoData:
        logger.logKnowledgeApi("GetStatutoryWizardTwoData", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_assigned_statutory_wizard_two(db, request_frame, user_id)
        logger.logKnowledgeApi("GetStatutoryWizardTwoData", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technotransactions.SaveAssignedStatutory:
        logger.logKnowledgeApi("SaveAssignedStatutory", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_save_assigned_statutory(db, request_frame, user_id)
        logger.logKnowledgeApi("SaveAssignedStatutory", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technotransactions.GetCountriesForGroup:
        logger.logKnowledgeApi("GetCountriesForGroup", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_countries_for_groups(db, user_id)
        logger.logKnowledgeApi("GetCountriesForGroup", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    return result

def process_get_assigned_statutories(db, user_id):
    return get_assigned_statutories_list(db, user_id)

def process_get_assigned_statutories_by_id(db, request_frame):
    client_statutory_id = request_frame.client_statutory_id
    return get_assigned_statutories_by_id(db, client_statutory_id)

def process_get_assigned_statutory_wizard_one(db, request_frame, user_id):
    country_id = request_frame.country_id
    domains = get_domains_for_user(db, user_id)
    industries = get_industries(db)
    geography_levels = get_geograhpy_levels_for_user(db, user_id)
    geographies = get_geographies(db, user_id, country_id)
    group_companies = get_groups_for_country(db, country_id, user_id)
    business_groups = get_business_groups_for_country(db, country_id, user_id)
    legal_entities = get_legal_entity_for_country(db, country_id, user_id)
    divisions = get_divisions_for_country(db, country_id, user_id)
    units = get_units_for_country(db, country_id, user_id)
    return technotransactions.GetAssignedStatutoryWizardOneDataSuccess(
        domains, industries, geography_levels,
        geographies, group_companies, business_groups,
        legal_entities, divisions, units
    )

def process_get_assigned_statutory_wizard_two(db, request_frame, user_id):
    geography_id = request_frame.geography_id
    industry_id = request_frame.industry_id
    domain_id = request_frame.domain_id
    country_id = request_frame.country_id
    unit_id = request_frame.unit_id
    print unit_id
    return get_assign_statutory_wizard_two(
        db, country_id, geography_id, industry_id,
        domain_id, unit_id, user_id
    )

def process_save_assigned_statutory(db, request_frame, user_id):
    return save_assigned_statutories(db, request_frame, user_id)

def process_get_countries_for_groups(db, user_id):
    return process_get_countries_for_user(db, user_id)
