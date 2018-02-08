from protocol import technomasters
from technomastercontroller import (
    get_client_groups, process_save_client_group, process_update_client_group,
    change_client_group_status, save_client, update_client, get_clients, get_clients_edit,
    reactivate_unit, get_client_profile,
    get_next_unit_code, get_client_group_form_data,
    get_edit_client_group_form_data, get_assign_legal_entity_list,
    get_unassigned_units, get_assigned_units, get_assigned_unit_details,
    get_assign_unit_form_data, process_save_assigned_units_request,
    get_edit_assign_legal_entity, process_save_assign_legal_entity,
    view_assign_legal_entity, save_division_category, check_assigned_units_under_domain,
    get_client_groups_for_client_unit_bulk_upload
)

__all__ = [
    "process_techno_request",
]


def process_techno_request(request, db, session_user):
    request_frame = request.request

    if type(request_frame) is technomasters.GetClientGroups:
        result = get_client_groups(db, request_frame, session_user)

    elif type(request_frame) is technomasters.SaveClientGroup:
        result = process_save_client_group(db, request_frame, session_user)

    elif type(request_frame) is technomasters.UpdateClientGroup:
        result = process_update_client_group(db, request_frame, session_user)

    # elif type(request_frame) is technomasters.ChangeClientGroupStatus:
    #     result = change_client_group_status(db, request_frame, session_user)

    elif type(request_frame) is technomasters.GetClients:
        result = get_clients(db, request_frame, session_user)

    elif type(request_frame) is technomasters.GetClientsEdit:
        result = get_clients_edit(db, request_frame, session_user)

    elif type(request_frame) is technomasters.SaveClient:
        result = save_client(db, request_frame, session_user)

    elif type(request_frame) is technomasters.SaveDivisionCategory:
        result = save_division_category(db, request_frame, session_user)

    elif type(request_frame) is technomasters.UpdateClient:
        result = update_client(db, request_frame, session_user)

    elif type(request_frame) is technomasters.GetClientGroupFormData:
        result = get_client_group_form_data(
            db, request_frame, session_user
        )

    elif type(request_frame) is technomasters.GetEditClientGroupFormData:
        result = get_edit_client_group_form_data(
            db, request_frame, session_user
        )

    elif type(request_frame) is technomasters.GetNextUnitCode:
        result = get_next_unit_code(db, request_frame, session_user)

    elif type(request_frame) is technomasters.GetAssignLegalEntityList:
        result = get_assign_legal_entity_list(
            db, request_frame, session_user)

    elif type(request_frame) is technomasters.GetUnassignedUnits:
        result = get_unassigned_units(db, session_user)

    elif type(request_frame) is technomasters.GetAssignedUnits:
        result = get_assigned_units(db, request_frame, session_user)

    elif type(request_frame) is technomasters.GetAssignedUnitDetails:
        result = get_assigned_unit_details(db, request_frame)

    elif type(request_frame) is technomasters.GetAssignUnitFormData:
        result = get_assign_unit_form_data(db, request_frame, session_user)

    elif type(request_frame) is technomasters.SaveAsssignedUnits:
        result = process_save_assigned_units_request(
            db, request_frame, session_user)

    elif type(request_frame) is technomasters.GetEditAssignLegalEntity:
        result = get_edit_assign_legal_entity(
            db, request_frame, session_user
        )

    elif type(request_frame) is technomasters.SaveAssignLegalEntity:
        result = process_save_assign_legal_entity(
            db, request_frame, session_user
        )

    elif type(request_frame) is technomasters.ViewAssignLegalEntity:
        result = view_assign_legal_entity(
            db, request_frame, session_user
        )

    elif type(request_frame) is technomasters.CheckAssignedDomainUnits:
        result = check_assigned_units_under_domain(
            db, request_frame, session_user
        )

    # client unit - bulk upload - request functions - starts

    elif type(request_frame) is technomasters.GetClientGroupsList:
        result = get_client_groups_for_client_unit_bulk_upload(
            db, request_frame, session_user
        )

    # client unit - bulk upload - request functions - ends

    return result
