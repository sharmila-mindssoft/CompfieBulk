import time
from protocol import login, knowledgetransaction
from generalcontroller import validate_user_session, validate_user_forms
from server import logger
from server.database.general import (
    get_compliance_duration, get_compliance_repeat,
    get_compliance_frequency, get_approval_status
)
from server.database.admin import (
    get_domains_for_user, get_countries_for_user
)
from server.database.knowledgemaster import (
    get_industries, get_statutory_nature,
    get_statutory_levels, get_geograhpy_levels_for_user,
    get_geographies, get_statutory_master
)
from server.database.knowledgetransaction import (
    get_statutory_mappings,
    check_duplicate_compliance_name,
    check_duplicate_statutory_mapping,
    save_statutory_mapping,
    update_statutory_mapping,
    change_statutory_mapping_status,
    change_approval_status
)
__all__ = [
    "process_knowledge_transaction_request"
]

forms = [10, 11]

def process_knowledge_transaction_request(request, db) :
    session_token = request.session_token
    request_frame = request.request
    user_id = validate_user_session(db, session_token)
    if user_id is not None :
        is_valid = validate_user_forms(db, user_id, forms, request_frame)
        if is_valid is not True :
            return login.InvalidSessionToken()

    if user_id is None:
        return login.InvalidSessionToken()

    if type(request_frame) is knowledgetransaction.GetStatutoryMappingsMaster:
        logger.logKnowledgeApi("GetStatutoryMappingsMaster", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_statutory_mapping_master(db, user_id)
        logger.logKnowledgeApi("GetStatutoryMappingsMaster", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is knowledgetransaction.GetStatutoryMappings :
        logger.logKnowledgeApi("GetStatutoryMappings", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_statutory_mappings(db, user_id)
        logger.logKnowledgeApi("GetStatutoryMappings", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is knowledgetransaction.CheckDuplicateStatutoryMapping :
        logger.logKnowledgeApi("CheckDuplicateStatutoryMapping", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_check_statutory_mapping(db, request_frame)
        logger.logKnowledgeApi("CheckDuplicateStatutoryMapping", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is knowledgetransaction.SaveStatutoryMapping :
        logger.logKnowledgeApi("SaveStatutoryMapping", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_save_statutory_mapping(db, request_frame, user_id)
        logger.logKnowledgeApi("SaveStatutoryMapping", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is knowledgetransaction.UpdateStatutoryMapping :
        logger.logKnowledgeApi("UpdateStatutoryMapping", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_update_statutory_mapping(db, request_frame, user_id)
        logger.logKnowledgeApi("UpdateStatutoryMapping", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is knowledgetransaction.ChangeStatutoryMappingStatus :
        logger.logKnowledgeApi("ChangeStatutoryMappingStatus", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_change_statutory_mapping_status(db, request_frame, user_id)
        logger.logKnowledgeApi("ChangeStatutoryMappingStatus", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is knowledgetransaction.GetApproveStatutoryMappings :
        logger.logKnowledgeApi("GetApproveStatutoryMappings", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_approve_statutory_mappings(db, user_id)
        logger.logKnowledgeApi("GetApproveStatutoryMappings", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is knowledgetransaction.ApproveStatutoryMapping :
        logger.logKnowledgeApi("ApproveStatutoryMapping", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_approve_statutory_mapping(db, request_frame, user_id)
        logger.logKnowledgeApi("ApproveStatutoryMapping", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))

    return result

def process_get_statutory_mapping_master(db, user_id):
    countries = get_countries_for_user(db, user_id)
    domains = get_domains_for_user(db, user_id)
    industries = get_industries(db)
    statutory_natures = get_statutory_nature(db)
    statutory_levels = get_statutory_levels(db)
    statutories = get_statutory_master(db)
    geography_levels = get_geograhpy_levels_for_user(db, user_id)
    geographies = get_geographies(db, user_id)
    compliance_frequency = get_compliance_frequency(db)
    compliance_repeat_type = get_compliance_repeat(db)
    compliance_duration_type = get_compliance_duration(db)
    compliance_approval_status = get_approval_status(db)
    return knowledgetransaction.GetStatutoryMappingsMasterSuccess(
        countries, domains, industries, statutory_natures,
        statutory_levels, statutories, geography_levels,
        geographies, compliance_frequency,
        compliance_repeat_type,
        compliance_approval_status, compliance_duration_type
    )

def process_get_statutory_mappings(db, user_id):
    statutory_mappings = get_statutory_mappings(db, user_id, for_approve=False)
    return knowledgetransaction.GetStatutoryMappingsSuccess(
        statutory_mappings
    )

def process_check_statutory_mapping(db, request_frame):
    is_duplicate = check_duplicate_statutory_mapping(db, request_frame)
    if is_duplicate is None :
        is_duplicate = False
    else :
        is_duplicate = True
    return knowledgetransaction.CheckDuplicateStatutoryMappingSuccess(is_duplicate)

def process_save_statutory_mapping(db, request_frame, user_id):
    is_duplicate = check_duplicate_compliance_name(db, request_frame)
    if is_duplicate is False:
        if (save_statutory_mapping(db, request_frame, user_id)) :
            return knowledgetransaction.SaveStatutoryMappingSuccess()
    else :
        return knowledgetransaction.ComplianceNameAlreadyExists(is_duplicate)

def process_update_statutory_mapping(db, request_frame, user_id):
    is_duplicate = check_duplicate_compliance_name(db, request_frame)
    if is_duplicate is False:
        if (update_statutory_mapping(db, request_frame, user_id)):
            return knowledgetransaction.UpdateStatutoryMappingSuccess()
        else :
            return knowledgetransaction.InvalidStatutoryMappingId()
    else :
        return knowledgetransaction.ComplianceNameAlreadyExists(is_duplicate)

def process_change_statutory_mapping_status(db, request_frame, user_id):
    if (change_statutory_mapping_status(db, request_frame, user_id)) :
        return knowledgetransaction.ChangeStatutoryMappingStatusSuccess()
    else :
        return knowledgetransaction.InvalidStatutoryMappingId()

def process_get_approve_statutory_mappings(db, user_id):
    statutory_mappings = get_statutory_mappings(db, user_id, for_approve=True)
    return knowledgetransaction.GetStatutoryMappingsSuccess(
        statutory_mappings
    )

def process_approve_statutory_mapping(db, request_frame, user_id):
    is_approved = False
    message = value = None
    for data in request_frame.statutory_mappings :
        result = change_approval_status(db, data, user_id)
        if result is True:
            is_approved = True
        else :
            message, value = result
            is_approved = False
            break

    if is_approved :
        return knowledgetransaction.ApproveStatutoryMappingSuccess()
    else :
        return knowledgetransaction.TransactionFailed(message, value)
