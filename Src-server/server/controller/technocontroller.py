import time
from protocol import login, technomasters
from generalcontroller import validate_user_session, validate_user_forms
from technomastercontroller import (
    get_client_groups, process_save_client_group, process_update_client_group,
    change_client_group_status, save_client, update_client, get_clients,
    reactivate_unit, get_client_profile, create_new_admin_for_client,
    get_next_unit_code, get_client_group_form_data,
    get_edit_client_group_form_data, get_assign_legal_entity_list,
    get_unassigned_units, get_assigned_units, get_assigned_unit_details,
    get_assign_unit_form_data, process_save_assigned_units_request,
    get_edit_assign_legal_entity, process_save_assign_legal_entity,
    view_assign_legal_entity
)
from server import logger

__all__ = [
    "process_techno_request",
]

forms = [18, 19, 20, 21, 44]


def process_techno_request(request, db):
    session_token = request.session_token
    request_frame = request.request
    session_user = validate_user_session(db, session_token)
    if session_user is not None:
        is_valid = validate_user_forms(db, session_user, forms, request_frame)
        if is_valid is not True:
            return login.InvalidSessionToken()

    if session_user is None:
        return login.InvalidSessionToken()

    if type(request_frame) is technomasters.GetClientGroups:
        logger.logKnowledgeApi("GetClientGroups", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = get_client_groups(db, request_frame, session_user)
        logger.logKnowledgeApi("GetClientGroups", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technomasters.SaveClientGroup:
        logger.logKnowledgeApi("SaveClientGroup", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_save_client_group(db, request_frame, session_user)
        logger.logKnowledgeApi("SaveClientGroup", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technomasters.UpdateClientGroup:
        logger.logKnowledgeApi("UpdateCleintGroup", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_update_client_group(db, request_frame, session_user)
        logger.logKnowledgeApi("UpdateClientGroup", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technomasters.ChangeClientGroupStatus:
        logger.logKnowledgeApi("ChangeClientGroupStatus", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = change_client_group_status(db, request_frame, session_user)
        logger.logKnowledgeApi("ChangeClientGroupStatus", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technomasters.GetClients:
        logger.logKnowledgeApi("GetClients", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = get_clients(db, request_frame, session_user)
        logger.logKnowledgeApi("GetClients", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technomasters.SaveClient:
        logger.logKnowledgeApi("SaveClient", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = save_client(db, request_frame, session_user)
        logger.logKnowledgeApi("SaveCient", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technomasters.UpdateClient:
        logger.logKnowledgeApi("UpdateClient", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = update_client(db, request_frame, session_user)
        logger.logKnowledgeApi("UpdateClient", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technomasters.GetClientGroupFormData:
        logger.logKnowledgeApi("GetClientGroupFormData", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = get_client_group_form_data(
            db, request_frame, session_user
        )
        logger.logKnowledgeApi("GetClientGroupFormData", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technomasters.GetEditClientGroupFormData:
        logger.logKnowledgeApi("GetClientGroupFormData", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = get_edit_client_group_form_data(
            db, request_frame, session_user
        )
        logger.logKnowledgeApi("GetClientGroupFormData", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technomasters.ReactivateUnit:
        logger.logKnowledgeApi("ReactivateUnit", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = reactivate_unit(db, request_frame, session_user)
        logger.logKnowledgeApi("ReactivateUnit", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technomasters.GetClientProfile:
        logger.logKnowledgeApi("GetClientProfile", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = get_client_profile(db, request_frame, session_user)
        logger.logKnowledgeApi("GetClientProfile", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technomasters.CreateNewAdmin:
        logger.logKnowledgeApi("GetclientProfile", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = create_new_admin_for_client(db, request_frame, session_user)
        logger.logKnowledgeApi("GetClientProfile", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technomasters.GetNextUnitCode:
        logger.logKnowledgeApi("GetNextUnitCode", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = get_next_unit_code(db, request_frame, session_user)
        logger.logKnowledgeApi("GetNextUnitCode", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technomasters.GetAssignLegalEntityList:
        logger.logKnowledgeApi("GetAssignLegalEntityList", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = get_assign_legal_entity_list(
            db, request_frame, session_user)
        logger.logKnowledgeApi("GetAssignLegalEntityList", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technomasters.GetUnassignedUnits:
        logger.logKnowledgeApi("GetUnassignedUnits", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = get_unassigned_units(db, session_user)
        logger.logKnowledgeApi("GetUnassignedUnits", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technomasters.GetAssignedUnits:
        logger.logKnowledgeApi("GetAssignedUnits", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = get_assigned_units(db, request_frame)
        logger.logKnowledgeApi("GetAssignedUnits", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technomasters.GetAssignedUnitDetails:
        logger.logKnowledgeApi("GetAssignedUnitDetails", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = get_assigned_unit_details(db, request_frame)
        logger.logKnowledgeApi("GetAssignedUnitDetails", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technomasters.GetAssignUnitFormData:
        logger.logKnowledgeApi("GetAssignUnitFormData", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = get_assign_unit_form_data(db, request_frame, session_user)
        logger.logKnowledgeApi("GetAssignUnitFormData", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technomasters.SaveAsssignedUnits:
        logger.logKnowledgeApi("SaveAsssignedUnits", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_save_assigned_units_request(
            db, request_frame, session_user)
        logger.logKnowledgeApi("SaveAsssignedUnits", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technomasters.GetEditAssignLegalEntity:
        logger.logKnowledgeApi("GetEditAssignLegalEntity", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = get_edit_assign_legal_entity(
            db, request_frame, session_user
        )
        logger.logKnowledgeApi("GetEditAssignLegalEntity", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technomasters.SaveAssignLegalEntity:
        logger.logKnowledgeApi("SaveAssignLegalEntity", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_save_assign_legal_entity(
            db, request_frame, session_user
        )
        logger.logKnowledgeApi("SaveAssignLegalEntity", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technomasters.ViewAssignLegalEntity:
        logger.logKnowledgeApi("ViewAssignLegalEntity", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = view_assign_legal_entity(
            db, request_frame, session_user
        )
        logger.logKnowledgeApi("ViewAssignLegalEntity", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    return result
