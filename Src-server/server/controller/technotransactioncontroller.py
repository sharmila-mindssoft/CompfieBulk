import time
from protocol import login, technotransactions
from generalcontroller import (
    validate_user_session, validate_user_forms
)
from server import logger
from server.database.admin import (
    get_domains_for_user
)
from server.database.technomaster import (
    get_clients_by_user, get_business_groups_for_user,
    get_legal_entities_for_user, get_divisions_for_user,
    get_units_for_user
)
from server.database.technotransaction import *


__all__ = [
    "process_techno_transaction_request"
]

forms = [21]


def process_techno_transaction_request(request, db):
    session_token = request.session_token
    request_frame = request.request
    user_id = validate_user_session(db, session_token)
    if user_id is not None:
        is_valid = validate_user_forms(db, user_id, forms, request_frame)
        if is_valid is not True:
            return login.InvalidSessionToken()

    if user_id is None:
        return login.InvalidSessionToken()

    if type(request_frame) is technotransactions.GetAssignedStatutories:
        logger.logKnowledgeApi("GetAssignedStatutoriesList", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_assigned_statutories(db)
        logger.logKnowledgeApi("GetAssignedStatutoriesList", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technotransactions.GetAssignedStatutoriesById:
        logger.logKnowledgeApi("GetAssignedStatutoriesById", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_assigned_statutories_by_id(db, request_frame, user_id)
        logger.logKnowledgeApi("GetAssignedStatutoriesById", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(
        request_frame
    ) is technotransactions.GetAssignedStatutoryWizardOneData:
        logger.logKnowledgeApi(
            "GetAssignedStatutoryWizardOneData", "process begin"
        )
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_assigned_statutory_wizard_one(
            db, user_id
        )
        logger.logKnowledgeApi(
            "GetAssignedStatutoryWizardOneData", "process end"
        )
        logger.logKnowledgeApi("------", str(time.time()))

    elif(
        type(
            request_frame
        ) is technotransactions.GetAssignedStatutoryWizardTwoData
    ):
        logger.logKnowledgeApi(
            "GetAssignedStatutoryWizardTwoData", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_assigned_statutory_wizard_two(
            db, request_frame, user_id
        )
        logger.logKnowledgeApi(
            "GetAssignedStatutoryWizardTwoData", "process end")
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


def process_get_assigned_statutory_wizard_one(db, user_id):
    group_companies = get_clients_by_user(db, user_id)
    business_groups = get_business_groups_for_user(db, user_id)
    legal_entities = get_legal_entities_for_user(db, user_id)
    divisions = get_divisions_for_user(db, user_id)
    categories = get_categories_for_user(db, user_id)
    domains = get_domains_for_user(db, user_id)
    units = get_units_for_user(db, user_id)
    return technotransactions.GetAssignedStatutoryWizardOneDataSuccess(
        group_companies, business_groups, legal_entities, divisions,
        categories, domains, units
    )


def process_get_assigned_statutory_wizard_two(db, request, session_user):
    level_1_statutories, statutories = get_assigned_statutory_wizard_two_data(
        db, request.client_id, request.business_group_id,
        request.legal_entity_id, request.division_id, request.category_id,
        request.domain_id_optional, request.unit_ids
    )
    return technotransactions.GetAssignedStatutoryWizardTwoDataSuccess(
        level_1_statutories_list=level_1_statutories,
        statutories_for_assigning=statutories
    )


def process_save_assigned_statutory(db, request, session_user):
    client_statutory_id = request.client_statutory_id
    client_id = request.client_id
    compliances_list = request.compliances_applicablity_status
    unit_ids = request.unit_ids
    units = request.unit_id_name
    level_1_statutory_compliance = request.level_1_statutory_wise_compliances
    submission_type = request.submission_type
    if client_statutory_id is None:
        save_assigned_statutory(
            db, client_statutory_id, client_id, compliances_list, unit_ids, units,
            level_1_statutory_compliance, submission_type, session_user
        )
    else:
        update_assigned_statutory(
            db, client_statutory_id, client_id, compliances_list, unit_ids, units,
            level_1_statutory_compliance, submission_type, session_user
        )
    return technotransactions.SaveAssignedStatutorySuccess()


def process_get_assigned_statutories(db):
    assigned_statutories = get_assigned_statutories_list(db)
    return technotransactions.GetAssignedStatutoriesSuccess(
        assigned_statutories
    )

def process_get_assigned_statutories_by_id(db, request, session_user):
    client_statutory_id = request.client_statutory_id
    level_1_statutories, assigned_statutories = get_assigned_statutories_by_id(db, client_statutory_id)
    return technotransactions.GetAssignedStatutoriesByIdSuccess(
        level_1_statutories_list=level_1_statutories,
        statutories_for_assigning=assigned_statutories 
    )