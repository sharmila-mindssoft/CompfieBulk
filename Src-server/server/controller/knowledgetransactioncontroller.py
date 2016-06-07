import time
from protocol import login, knowledgetransaction
from generalcontroller import validate_user_session, validate_user_forms
from server import logger
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
    countries = db.get_countries_for_user(user_id)
    domains = db.get_domains_for_user(user_id)
    industries = db.get_industries()
    statutory_natures = db.get_statutory_nature()
    statutory_levels = db.get_statutory_levels()
    statutories = db.get_statutory_master()
    geography_levels = db.get_geograhpy_levels_for_user(user_id)
    geographies = db.get_geographies(user_id)
    compliance_frequency = db.get_compliance_frequency()
    compliance_repeat_type = db.get_compliance_repeat()
    compliance_duration_type = db.get_compliance_duration()
    compliance_approval_status = db.get_approval_status()
    return knowledgetransaction.GetStatutoryMappingsMasterSuccess(
        countries, domains, industries, statutory_natures,
        statutory_levels, statutories, geography_levels,
        geographies, compliance_frequency,
        compliance_repeat_type,
        compliance_approval_status, compliance_duration_type
    )

def process_get_statutory_mappings(db, user_id):
    statutory_mappings = db.get_statutory_mappings(user_id, for_approve=False)
    return knowledgetransaction.GetStatutoryMappingsSuccess(
        statutory_mappings
    )

def process_check_statutory_mapping(db, request_frame):
    is_duplicate = db.check_duplicate_statutory_mapping(request_frame)
    if is_duplicate is None :
        is_duplicate = False
    else :
        is_duplicate = True
    return knowledgetransaction.CheckDuplicateStatutoryMappingSuccess(is_duplicate)

def process_save_statutory_mapping(db, request_frame, user_id):
    is_duplicate = db.check_duplicate_compliance_name(request_frame)
    if is_duplicate is False:
        if (db.save_statutory_mapping(request_frame, user_id)) :
            return knowledgetransaction.SaveStatutoryMappingSuccess()
    else :
        return knowledgetransaction.ComplianceNameAlreadyExists(is_duplicate)


def process_update_statutory_mapping(db, request_frame, user_id):
    is_duplicate = db.check_duplicate_compliance_name(request_frame)
    if is_duplicate is False:
        if (db.update_statutory_mapping(request_frame, user_id)):
            return knowledgetransaction.UpdateStatutoryMappingSuccess()
        else :
            return knowledgetransaction.InvalidStatutoryMappingId()
    else :
        return knowledgetransaction.ComplianceNameAlreadyExists(is_duplicate)

def process_change_statutory_mapping_status(db, request_frame, user_id):
    if (db.change_statutory_mapping_status(request_frame, user_id)) :
        return knowledgetransaction.ChangeStatutoryMappingStatusSuccess()
    else :
        return knowledgetransaction.InvalidStatutoryMappingId()

def process_get_approve_statutory_mappings(db, user_id):
    statutory_mappings = db.get_statutory_mappings(user_id, for_approve=True)
    return knowledgetransaction.GetStatutoryMappingsSuccess(
        statutory_mappings
    )

def process_approve_statutory_mapping(db, request_frame, user_id):
    is_approved = False
    for data in request_frame.statutory_mappings :
        if (db.change_approval_status(data, user_id)):
            is_approved = True
        else :
            is_approved = False
            break

    if is_approved :
        return knowledgetransaction.ApproveStatutoryMappingSuccess()
    else :
        return knowledgetransaction.InvalidStatutoryMappingId()
