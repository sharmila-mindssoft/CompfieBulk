from protocol import (
    clientadminsettings, login
)
from server.clientdatabase.clientadminsettings import *

__all__ = [
    "process_client_admin_settings_requests"
]


###############################################################
# To Redirect the requests to the corresponding functions
# Parameters - Object of request, object of database
# Return Type - Varies depends on the request
###############################################################
def process_client_admin_settings_requests(request, db):
    session_token = request.session_token
    request = request.request
    session_user = db.validate_session_token(session_token)
    if session_user is None:
        return login.InvalidSessionToken()
    if type(request) is clientadminsettings.GetSettings:
        return process_get_settings(db, request)
    elif type(request) is clientadminsettings.UpdateSettings:
        return process_update_settings(db, request)


################################################################
# To retrieve the settings and profile of the given client
# Parameters - object of database, Object of request
# Return Type - GetSettingsSuccess
################################################################
def process_get_settings(db, request):
    settings = get_settings(db)
    contract_from = settings["contract_from"]
    contract_to = settings["contract_to"]
    no_of_user_licence = settings["no_of_user_licence"]
    total_disk_space = settings["total_disk_space"]
    used_space = settings["total_disk_space_used"]
    profile_detail = get_profile(
        db, contract_from, contract_to, no_of_user_licence,
        total_disk_space, used_space
    )
    return clientadminsettings.GetSettingsSuccess(
        is_two_levels_of_approval=bool(settings["two_levels_of_approval"]),
        assignee_reminder_days=settings["assignee_reminder"],
        escalation_reminder_In_advance_days=settings[
            "escalation_reminder_in_advance"
        ],
        escalation_reminder_days=settings["escalation_reminder"],
        profile_detail=profile_detail
    )


###############################################################
# To Process Update settings request
# Parameters - object of database, Object of request
# Return type - UpdateSettingsSuccess
###############################################################
def process_update_settings(db, request):
    is_two_levels_of_approval = request.is_two_levels_of_approval
    assignee_reminder_days = request.assignee_reminder_days
    rem_in_advance = request.escalation_reminder_In_advance_days
    escalation_reminder_days = request.escalation_reminder_days
    updateSettings(
        db, is_two_levels_of_approval, assignee_reminder_days,
        rem_in_advance, escalation_reminder_days
    )
    return clientadminsettings.UpdateSettingsSuccess()
