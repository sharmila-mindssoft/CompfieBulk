from protocol import (clientadminsettings, login, core)
from server.clientdatabase.clientadminsettings import *

from server.clientdatabase.general import (
    validate_session_token,
    )

__all__ = [
    "process_client_admin_settings_requests"
]

########################################################
# To Redirect the requests to the corresponding
# functions
########################################################
def process_client_admin_settings_requests(request, db) :
    session_token = request.session_token
    client_info = session_token.split("-")

    request = request.request
    client_id = int(client_info[0])
    session_user = validate_session_token(db, client_id, session_token)
    if session_user is None:
        return login.InvalidSessionToken()
    if type(request) is clientadminsettings.GetSettings :
        return process_get_settings(db, request, session_user, client_id)
    elif type(request) is clientadminsettings.UpdateSettings :
        return process_update_settings(db, request, session_user, client_id)

########################################################
# To retrieve the settings and profile of the given
# client
########################################################
def process_get_settings(db, request, session_user, client_id):
    settings = get_settings(db, client_id)
    contract_from = settings[4]
    contract_to = settings[5]
    no_of_user_licence = settings[6]
    total_disk_space = settings[7]
    used_space = settings[8]
    profile_detail = get_profile(db, 
        contract_from, contract_to, no_of_user_licence,
        total_disk_space, used_space, client_id
    )
    return clientadminsettings.GetSettingsSuccess(
        is_two_levels_of_approval=bool(settings[0]),
        assignee_reminder_days=settings[1],
        escalation_reminder_In_advance_days=settings[2],
        escalation_reminder_days=settings[3],
        profile_detail=profile_detail
    )


########################################################
# To update the client settings
########################################################
def process_update_settings(db, request, session_user, client_id):
    is_two_levels_of_approval = request.is_two_levels_of_approval
    assignee_reminder_days = request.assignee_reminder_days
    escalation_reminder_In_advance_days = request.escalation_reminder_In_advance_days
    escalation_reminder_days = request.escalation_reminder_days
    updateSettings(db, is_two_levels_of_approval, assignee_reminder_days,
        escalation_reminder_In_advance_days, escalation_reminder_days, client_id)
    return clientadminsettings.UpdateSettingsSuccess()
