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
    create_new_admin
)

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
        return get_client_groups(db, request_frame, session_user)

    if type(request_frame) is technomasters.SaveClientGroup:
        return save_client_group(db, request_frame, session_user)

    if type(request_frame) is technomasters.UpdateClientGroup:
        return update_client_group(db, request_frame, session_user)

    if type(request_frame) is technomasters.ChangeClientGroupStatus:
        return change_client_group_status(db, request_frame, session_user)

    if type(request_frame) is technomasters.GetClients:
        return get_clients(db, request_frame, session_user)

    if type(request_frame) is technomasters.SaveClient:
        return save_client(db, request_frame, session_user)

    if type(request_frame) is technomasters.UpdateClient:
        return update_client(db, request_frame, session_user)

    if type(request_frame) is technomasters.ChangeClientStatus:
        return change_client_status(db, request_frame, session_user)

    if type(request_frame) is technomasters.ReactivateUnit:
        return reactivate_unit(db, request_frame, session_user)

    if type(request_frame) is technomasters.GetClientProfile:
        return get_client_profile(db, request_frame, session_user)

    if type(request_frame) is technomasters.CreateNewAdmin:
        return create_new_admin(db, request_frame, session_user)
