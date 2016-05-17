from protocol import login, core, technomasters
from generalcontroller import validate_user_session, validate_user_forms
from technomastercontroller import (
    get_client_groups,
    save_client_group,
    update_client_group,
    change_client_group_status,
    save_client,
    update_client,
    get_clients,
    change_client_status,
    reactivate_unit,
    get_client_profile,
    create_new_admin,
    get_next_unit_code
)
from server import logger
__all__=[
    "process_techno_request",
]

forms = [18, 19, 20]

def process_techno_request(request, db) :
    session_token = request.session_token
    request_frame = request.request
    session_user = validate_user_session(db, session_token)
    if session_user is not None :
        is_valid = validate_user_forms(db, session_user, forms, request_frame)
        if is_valid is not True :
            return login.InvalidSessionToken()

    if session_user is None:
        return login.InvalidSessionToken()

    if type(request_frame) is technomasters.GetClientGroups:
        logger.logKnowledgeApi("GetClientGroups", "process begin")
        result = get_client_groups(db, request_frame, session_user)
        logger.logKnowledgeApi("GetClientGroups", "process end")

    if type(request_frame) is technomasters.SaveClientGroup:
        logger.logKnowledgeApi("SaveClientGroup", "process begin")
        result = save_client_group(db, request_frame, session_user)
        logger.logKnowledgeApi("SaveClientGroup", "process end")

    if type(request_frame) is technomasters.UpdateClientGroup:
        logger.logKnowledgeApi("UpdateCleintGroup", "process begin")
        result = update_client_group(db, request_frame, session_user)
        logger.logKnowledgeApi("UpdateClientGroup", "process end")

    if type(request_frame) is technomasters.ChangeClientGroupStatus:
        logger.logKnowledgeApi("ChangeClientGroupStatus", "process begin")
        result = change_client_group_status(db, request_frame, session_user)
        logger.logKnowledgeApi("ChangeClientGroupStatus", "process end")

    if type(request_frame) is technomasters.GetClients:
        logger.logKnowledgeApi("GetClients", "process begin")
        result = get_clients(db, request_frame, session_user)
        logger.logKnowledgeApi("GetClients", "process end")

    if type(request_frame) is technomasters.SaveClient:
        logger.logKnowledgeApi("SaveClient", "process begin")
        result = save_client(db, request_frame, session_user)
        logger.logKnowledgeApi("SaveCient", "process end")

    if type(request_frame) is technomasters.UpdateClient:
        logger.logKnowledgeApi("UpdateClient", "process begin")
        result = update_client(db, request_frame, session_user)
        logger.logKnowledgeApi("UpdateClient", "process end")

    if type(request_frame) is technomasters.ChangeClientStatus:
        logger.logKnowledgeApi("ChangeClientStatus", "process begin")
        result = change_client_status(db, request_frame, session_user)
        logger.logKnowledgeApi("ChangeClientStatus", "process end")

    if type(request_frame) is technomasters.ReactivateUnit:
        logger.logKnowledgeApi("ReactivateUnit", "process begin")
        result = reactivate_unit(db, request_frame, session_user)
        logger.logKnowledgeApi("ReactivateUnit", "process end")

    if type(request_frame) is technomasters.GetClientProfile:
        logger.logKnowledgeApi("GetClientProfile", "process begin")
        result = get_client_profile(db, request_frame, session_user)
        logger.logKnowledgeApi("GetClientProfile", "process end")

    if type(request_frame) is technomasters.CreateNewAdmin:
        logger.logKnowledgeApi("GetclientProfile", "process begin")
        result = create_new_admin(db, request_frame, session_user)
        logger.logKnowledgeApi("GetClientProfile", "process end")

    if type(request_frame) is technomasters.GetNextUnitCode:
        logger.logKnowledgeApi("GetNextUnitCode", "process begin")
        result = get_next_unit_code(db, request_frame, session_user)
        logger.logKnowledgeApi("GetNextUnitCode", "process end")

    return result
