from clientprotocol import clientmobile, clientlogin
from server.clientdatabase.mobile import *

__all__ = [
    "process_client_mobile_request"
]


def process_client_mobile_request(request, db):
    # client_info = request.session_token.split("-")
    session_token = request.session_token
    request_frame = request.request
    # client_id = int(client_info[0])
    session_user = db.validate_session_token(session_token)

    if session_user is None:
        return clientlogin.InvalidSessionToken()

    elif type(request_frame) is clientmobile.GetVersions:
        return process_get_version(db, request)

    elif type(request_frame) is clientmobile.GetUsers:
        return process_get_users(db, session_user)

    elif type(request_frame) is clientmobile.GetUnitDetails:
        return process_get_unit_details(db, session_user)
    elif type(request_frame) is clientmobile.GetComplianceApplicabilityStatus:
        return process_get_compliance_applicability(db, session_user)
    elif type(request_frame) is clientmobile.GetComplianceHistory:
        return process_get_compliance_history(db, session_user, request_frame)
    elif type(request_frame) is clientmobile.CheckDiskSpace:
        return process_check_disk_space(db)
    elif type(request_frame) is clientmobile.GetTrendChartData:
        return process_get_trend_chart(db, session_user)
    elif type(request_frame) is clientmobile.SaveRegistrationKey:
        return


def process_get_version(db, request):
    data = get_version(db)
    return clientmobile.GetVersionsSuccess(
        int(data["unit_details"]),
        int(data["user_details"]),
        int(data["compliance_applicability"]),
        int(data["compliance_history"]),
        int(data["reassign_history"])
    )


def process_get_users(db, session_user):
    users = get_users_for_mobile(db, session_user)
    return clientmobile.GetUsersSuccess(users)


def process_get_unit_details(db, session_user):
    countries = get_countries_for_user(db, session_user)
    domains = get_domains_for_user(db, session_user)
    business_groups = get_business_groups_for_mobile(db)
    legal_entity = get_legal_entities_for_mobile(db)
    division = get_divisions_for_mobile(db)
    units = get_units_for_assign_compliance(db, session_user)
    return clientmobile.GetUnitDetailsSuccess(
        countries, domains,
        business_groups, legal_entity,
        division, units
    )


def process_get_compliance_applicability(db, session_user):
    data = get_compliance_applicability_for_mobile(db, session_user)
    return clientmobile.GetComplianceApplicabilityStatusSuccess(data)


def process_get_trend_chart(db, session_user):
    data = get_trend_chart_for_mobile(db, session_user)
    return clientmobile.GetTrendChartDataSuccess(data)


def process_get_compliance_history(db, session_user, request):
    data = get_compliance_history_for_mobile(db, session_user, request)
    return clientmobile.GetComplianceHistorySuccess(data)


def process_check_disk_space(db):
    data = get_check_disk_space_for_mobile(db)
    return clientmobile.CheckDiskSpaceSuccess(
        int(data["total_disk_space"]),
        int(data["total_disk_space_used"])
    )


def process_save_registration_key(db, session_user, request):
    save_registration_key(db, session_user, request)
    return clientmobile.SaveRegistrationKeySuccess()
    # return clientmobile.InvalidRegistrationKey()
