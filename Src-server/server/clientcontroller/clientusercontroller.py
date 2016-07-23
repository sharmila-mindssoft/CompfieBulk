import time
from protocol import (clientuser, login)
from server import logger
from server.constants import RECORD_DISPLAY_COUNT
from server.clientdatabase.clientuser import *

from server.common import (
    datetime_to_string_time,
    get_date_time_in_date
)

from server.clientdatabase.general import (
    get_user_domains, get_user_unit_ids
    )
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
    session_user = db.validate_session_token(session_token)
    if session_user is None:
        return login.InvalidSessionToken()

    if type(request) is clientuser.GetCurrentComplianceDetail:
        logger.logClientApi("GetCurrentComplianceDetail", "process begin")
        logger.logClientApi("------", str(time.time()))
        result = process_get_current_compliance_detail(db, request, session_user, client_id)
        logger.logClientApi("GetCurrentComplianceDetail", "process end")
        logger.logClientApi("------", str(time.time()))

    if type(request) is clientuser.GetUpcomingComplianceDetail:
        logger.logClientApi("GetUpcomingComplianceDetail", "process begin")
        logger.logClientApi("------", str(time.time()))
        result = process_get_upcoming_compliance_detail(db, request, session_user, client_id)
        logger.logClientApi("GetUpcomingComplianceDetail", "process end")
        logger.logClientApi("------", str(time.time()))

    if type(request) is clientuser.UpdateComplianceDetail:
        logger.logClientApi("UpdateComplianceDetail", "process begin")
        logger.logClientApi("------", str(time.time()))
        result = process_update_compliance_detail(db, request, session_user, client_id)
        logger.logClientApi("UpdateComplianceDetail", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientuser.GetOnOccurrenceCompliances:
        logger.logClientApi("GetOnOccurrenceCompliances", "process begin")
        logger.logClientApi("------", str(time.time()))
        result = process_get_on_occurrence_compliances(
            db, request, session_user, client_id
        )
        logger.logClientApi("GetOnOccurrenceCompliances", "process end")
        logger.logClientApi("------", str(time.time()))

    elif type(request) is clientuser.StartOnOccurrenceCompliance:
        logger.logClientApi("StartOnOccurrenceCompliance", "process begin")
        logger.logClientApi("------", str(time.time()))
        result = process_start_on_occurrence_compliance(
            db, request, session_user, client_id
        )
        logger.logClientApi("StartOnOccurrenceCompliance", "process end")
        logger.logClientApi("------", str(time.time()))

    return result


########################################################
# To get the ongoing and upcoming compliances of the
# given user
########################################################
def process_get_current_compliance_detail(db, request, session_user, client_id):
    current_start_count = request.current_start_count
    to_count = RECORD_DISPLAY_COUNT
    current_compliances_list = get_current_compliances_list(
        db, current_start_count, to_count, session_user, client_id
    )
    current_date_time = get_date_time_in_date()
    str_current_date_time = datetime_to_string_time(current_date_time)
    inprogress_count = get_inprogress_count(db, session_user)
    overdue_count = get_overdue_count(db, session_user)
    return clientuser.GetCurrentComplianceDetailSuccess(
        current_compliances=current_compliances_list,
        current_date=str_current_date_time,
        overdue_count=overdue_count,
        inprogress_count=inprogress_count
    )

def process_get_upcoming_compliance_detail(db, request, session_user, client_id):
    upcoming_start_count = request.upcoming_start_count
    to_count = RECORD_DISPLAY_COUNT
    upcoming_compliances_list = get_upcoming_compliances_list(
        db, upcoming_start_count, to_count, session_user, client_id
    )
    total_count = get_upcoming_count(db, session_user)
    return clientuser.GetUpcomingComplianceDetailSuccess(
        upcoming_compliances=upcoming_compliances_list,
        total_count=total_count
    )

########################################################
# To validate and update the compliance details
########################################################
def is_unsupported_file(documents):
    for doc in documents:
        file_name_parts = doc.file_name.split('.')
        name = doc.file_name.split('.')[0]
        exten = doc.file_name.split('.')[1]
        if exten in ["exe", "htm", "html", "xhtml"]:
            return True
        else:
            continue

def validate_documents(documents):
    if documents is not None:
        if is_unsupported_file(documents):
            return True
        else:
            return False
    else:
        return False

def process_update_compliance_detail(db, request, session_user, client_id):
    if validate_documents(request.documents):
        return clientuser.UnSupportedFile()
    else:
        result = update_compliances(db,
            request.compliance_history_id, request.documents,
            request.completion_date, request.validity_date, request.next_due_date,
            request.remarks, client_id, session_user
        )
        if result is True:
            return clientuser.UpdateComplianceDetailSuccess()
        elif result == "InvalidUser":
            return clientuser.InvalidUser()
        else:
            return result

########################################################
# To get the list of all on occurrence compliances
# under the given user
########################################################
def process_get_on_occurrence_compliances(
    db, request, session_user, client_id
):
    to_count = RECORD_DISPLAY_COUNT
    #import from general.py
    user_domain_ids = get_user_domains(db, session_user)
    user_unit_ids = get_user_unit_ids(db, session_user)
    #import from clientuser.py
    compliances = get_on_occurrence_compliances_for_user(
        db, session_user, user_domain_ids, user_unit_ids,
        request.start_count, to_count
    )
    total_count = get_on_occurrence_compliance_count(
        db, session_user, user_domain_ids, user_unit_ids
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
    start_on_occurrence_task(
        db, compliance_id, start_date, unit_id, duration, session_user, client_id
    )
    return clientuser.StartOnOccurrenceComplianceSuccess()
