from protocol import (clientuser, login)
from server import logger

__all__ = [
    "process_client_user_request"
]

########################################################
# To Redirect the requests to the corresponding
# functions
########################################################
def process_client_user_request(request, db) :
    session_token = request.session_token
    client_info = session_token.split("-")
    request = request.request
    client_id = int(client_info[0])
    session_user = db.validate_session_token(client_id, session_token)
    if session_user is None:
        return login.InvalidSessionToken()

    if type(request) is clientuser.GetCurrentComplianceDetail:
        logger.logClientApi("GetCurrentComplianceDetail", "process begin")
        result = process_get_current_compliance_detail(db, request, session_user, client_id)
        logger.logClientApi("GetCurrentComplianceDetail", "process end")

    if type(request) is clientuser.GetUpcomingComplianceDetail:
        logger.logClientApi("GetUpcomingComplianceDetail", "process begin")
        result = process_get_upcoming_compliance_detail(db, request, session_user, client_id)
        logger.logClientApi("GetUpcomingComplianceDetail", "process end")

    if type(request) is clientuser.UpdateComplianceDetail:
        logger.logClientApi("UpdateComplianceDetail", "process begin")
        result = process_update_compliance_detail(db, request, session_user, client_id)
        logger.logClientApi("UpdateComplianceDetail", "process end")

    elif type(request) is clientuser.GetOnOccurrenceCompliances:
        logger.logClientApi("GetOnOccurrenceCompliances", "process begin")
        result = process_get_on_occurrence_compliances(
            db, request, session_user, client_id
        )
        logger.logClientApi("GetOnOccurrenceCompliances", "process end")

    elif type(request) is clientuser.StartOnOccurrenceCompliance:
        logger.logClientApi("StartOnOccurrenceCompliance", "process begin")
        result = process_start_on_occurrence_compliance(
            db, request, session_user, client_id
        )
        logger.logClientApi("StartOnOccurrenceCompliance", "process end")

    return result


########################################################
# To get the ongoing and upcoming compliances of the
# given user
########################################################
def process_get_current_compliance_detail(db, request, session_user, client_id):
    current_start_count = request.current_start_count
    to_count = 500
    current_compliances_list = db.get_current_compliances_list(
        current_start_count, to_count, session_user, client_id
    )
    current_date_time = db.get_date_time()
    str_current_date_time = db.datetime_to_string_time(current_date_time)
    inprogress_count =db.get_inprogress_count(session_user)
    overdue_count =db.get_overdue_count(session_user)
    return clientuser.GetCurrentComplianceDetailSuccess(
        current_compliances=current_compliances_list,
        current_date=str_current_date_time,
        overdue_count=overdue_count,
        inprogress_count=inprogress_count
    )

def process_get_upcoming_compliance_detail(db, request, session_user, client_id):
    upcoming_start_count = request.upcoming_start_count
    to_count = 500
    upcoming_compliances_list = db.get_upcoming_compliances_list(
        upcoming_start_count, to_count, session_user, client_id
    )
    total_count = db.get_upcoming_count(session_user)
    return clientuser.GetUpcomingComplianceDetailSuccess(
        upcoming_compliances=upcoming_compliances_list,
        total_count=total_count
    )

########################################################
# To validate and update the compliance details
########################################################
def process_update_compliance_detail(db, request, session_user, client_id):
    result = db.update_compliances(
        request.compliance_history_id, request.documents,
        request.completion_date, request.validity_date, request.next_due_date,
        request.remarks, client_id, session_user
    )
    if result is True:
        return clientuser.UpdateComplianceDetailSuccess()
    elif result == "InvalidUser":
        return clientuser.InvalidUser()
    else:
        return clientuser.NextDueDateMustBeWithIn90DaysBeforeValidityDate()

########################################################
# To get the list of all on occurrence compliances
# under the given user
########################################################
def process_get_on_occurrence_compliances(
    db, request, session_user, client_id
):
    to_count = 500
    user_domain_ids = db.get_user_domains(session_user)
    user_unit_ids = db.get_user_unit_ids(session_user)
    compliances = db.get_on_occurrence_compliances_for_user(
        session_user, user_domain_ids, user_unit_ids, 
        request.start_count, to_count
    )
    total_count = db.get_on_occurrence_compliance_count(
        session_user, user_domain_ids, user_unit_ids
    )
    return clientuser.GetOnOccurrenceCompliancesSuccess(
        compliances=compliances,
        total_count=total_count
    )

########################################################
# To start an on occurrence compliance
########################################################
def process_start_on_occurrence_compliance(
    db, request, session_user, client_id
):
    compliance_id = request.compliance_id
    start_date = request.start_date
    unit_id = request.unit_id
    duration = request.duration
    db.start_on_occurrence_task(
        compliance_id, start_date, unit_id, duration, session_user, client_id
    )
    return clientuser.StartOnOccurrenceComplianceSuccess()
