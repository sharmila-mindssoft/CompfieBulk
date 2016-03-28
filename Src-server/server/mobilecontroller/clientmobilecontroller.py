from protocol import mobile, login
from generalcontroller import validate_user_session

__all__ = [
    "process_client_mobile_request"
]

def process_client_mobile_request(request, db):
    session_token = request.session_token
    request_frame = request.request
    session_user = validate_user_session(db, session_token)
    if session_user is None:
        return login.InvalidSessionToken()

    elif type(request_frame) is mobile.GetVersions :
        return process_get_version(db, request)

    elif type(request_frame) is mobile.GetUsers :
        return process_get_users(db, request)

    elif type(request_frame) is mobile.GetUnitDatails :
        return process_get_unit_details()

    elif type(request_frame) is mobile.GetComplianceApplicabilityStatus :
        return process_get_compliance_applicability()

def process_get_version(db, request):
    data = db.get_version()
    return mobile.GetVersionsSuccess(
        int(data["unit_details"]),
        int(data["user_details"]),
        int(data["compliance_applicability"]),
        int(data["compliance_history"]),
        int(data["reassign_history"])
    )

def process_get_users(db):
    pass

def process_get_unit_details():
    pass

def process_get_compliance_applicability():
    pass
