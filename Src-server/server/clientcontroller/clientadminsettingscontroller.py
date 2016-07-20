from protocol import (clientadminsettings, login, core)
from server.clientdatabase.clientadminsettings import *

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
    session_user = db.validate_session_token(session_token)
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
    contract_from = settings["contract_from"]
    contract_to = settings["contract_to"]
    no_of_user_licence = settings["no_of_user_licence"]
    total_disk_space = settings["total_disk_space"]
    used_space = settings["total_disk_space_used"]
    profile_detail = get_profile(
        db, contract_from, contract_to, no_of_user_licence,
        total_disk_space, used_space, client_id
    )
    return clientadminsettings.GetSettingsSuccess(
        is_two_levels_of_approval=bool(settings["two_levels_of_approval"]),
        assignee_reminder_days=settings["assignee_reminder"],
        escalation_reminder_In_advance_days=settings["escalation_reminder_in_advance"],
        escalation_reminder_days=settings["escalation_reminder"],
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
