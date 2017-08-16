from clientprotocol import (clientuser, clientcore)
from server.constants import (
    RECORD_DISPLAY_COUNT, FILE_MAX_LIMIT
)
from server.clientdatabase.clientuser import *

from server.common import (
    datetime_to_string_time,
    get_date_time_in_date, datetime_to_string
)

from server.clientdatabase.general import (
    get_user_domains, get_user_unit_ids, is_space_available, get_units_for_user
    )
__all__ = [
    "process_client_user_request"
]


########################################################
# To Redirect the requests to the corresponding
# functions
########################################################
def process_client_user_request(request, db, session_user):
    request = request.request

    if type(request) is clientuser.GetCurrentComplianceDetail:
        result = process_get_current_compliance_detail(
            db, request, session_user
        )

    if type(request) is clientuser.GetUpcomingComplianceDetail:
        result = process_get_upcoming_compliance_detail(
            db, request, session_user
        )

    if type(request) is clientuser.UpdateComplianceDetail:
        result = process_update_compliance_detail(
            db, request, session_user
        )

    elif type(request) is clientuser.GetOnOccurrenceCompliances:
        result = process_get_on_occurrence_compliances(
            db, request, session_user
        )

    elif type(request) is clientuser.StartOnOccurrenceCompliance:
        result = process_start_on_occurrence_compliance(
            db, request, session_user
        )

    elif type(request) is clientuser.ComplianceFilters:
        result = process_compliance_filters(
            db, request, session_user
        )
    elif type(request) is clientuser.OnOccurrenceLastTransaction:
        result = process_onoccurrence_last_transaction(
            db, request, session_user
        )
    elif type(request) is clientuser.GetCalendarView :
        result = get_calendar_view(db, request, session_user)

    elif type(request) is clientuser.GetSettingsFormDetails:
        result = process_settings_form_data(db, request, session_user)

    elif type(request) is clientuser.SaveSettingsFormDetails:
        result = process_save_settings_form_data(db, request, session_user)

    return result


########################################################
# To get the ongoing and upcoming compliances of the
# given user
########################################################
def process_get_current_compliance_detail(
    db, request, session_user
):
    unit_id = request.unit_id
    current_start_count = request.current_start_count
    cal_view = request.cal_view
    cal_date = request.cal_date

    to_count = RECORD_DISPLAY_COUNT

    current_compliances_list = get_current_compliances_list(
        db, unit_id, current_start_count, to_count, session_user, cal_view, cal_date
    )

    current_date_time = get_date_time_in_date()
    str_current_date_time = datetime_to_string_time(current_date_time)
    inprogress_count = get_inprogress_count(db, session_user, unit_id, cal_view, cal_date)
    overdue_count = get_overdue_count(db, session_user, unit_id, cal_view, cal_date)
    return clientuser.GetCurrentComplianceDetailSuccess(
        current_compliances=current_compliances_list,
        current_date=str_current_date_time,
        overdue_count=overdue_count,
        inprogress_count=inprogress_count
    )
#############################################################
# Get Upcoming Compliances List
#############################################################
def process_get_upcoming_compliance_detail(
    db, request, session_user
):
    unit_id = request.unit_id
    upcoming_start_count = request.upcoming_start_count
    cal_view = request.cal_view
    cal_date = request.cal_date
    print "cal_view>>>", cal_view
    print "cal_date>>", cal_date

    to_count = RECORD_DISPLAY_COUNT
    upcoming_compliances_list = get_upcoming_compliances_list(
        db, unit_id, upcoming_start_count, to_count, session_user, cal_view, cal_date
    )
    total_count = get_upcoming_count(db, unit_id, session_user)
    return clientuser.GetUpcomingComplianceDetailSuccess(
        upcoming_compliances=upcoming_compliances_list,
        total_count=total_count
    )

########################################################
# To validate and update the compliance details
########################################################
def is_unsupported_file(documents):
    if documents is None:
        return False
    for doc in documents:
        file_name_parts = doc.file_name.split('.')
        if len(file_name_parts) > 1:
            exten = file_name_parts[1]
            if exten in ["exe", "htm", "html", "xhtml"]:
                return True
            else:
                continue


def validate_file_size(db, documents):
    if documents is None:
        return False
    for doc in documents:
        file_size = doc.file_size
        if(
            file_size > FILE_MAX_LIMIT or
            not is_space_available(db, file_size)
        ):
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
########################################################
# Update Compliances - Submit Compliances
########################################################
def process_update_compliance_detail(db, request, session_user):
    if validate_documents(request.documents):
        return clientuser.UnSupportedFile()
    elif validate_file_size(db, request.documents):
        return clientuser.FileSizeExceedsLimit()
    else:
        result = update_compliances(
            db, request.compliance_history_id, request.documents,
            request.uploaded_documents,
            request.completion_date, request.validity_date,
            request.next_due_date, request.remarks,
            session_user
        )
    if result:
        return clientuser.UpdateComplianceDetailSuccess()
    elif result == "InvalidUser":
        return clientuser.InvalidUser()
    else:
        return result


########################################################
# To get the list of all on occurrence compliances
# under the given user
########################################################
def process_get_on_occurrence_compliances(db, request, session_user):
    unit_id = request.unit_id
    to_count = RECORD_DISPLAY_COUNT
    user_domain_ids = get_user_domains(db, session_user)
    user_unit_ids = get_user_unit_ids(db, session_user)
    compliances = get_on_occurrence_compliances_for_user(
        db, session_user, user_domain_ids, user_unit_ids, unit_id,
        request.start_count, to_count
    )

    total_count = get_on_occurrence_compliance_count(
        db, session_user, user_domain_ids, user_unit_ids, unit_id
    )
    current_date_time = get_date_time_in_date()
    str_current_date_time = datetime_to_string_time(current_date_time)
    return clientuser.GetOnOccurrenceCompliancesSuccess(
        compliances=compliances,
        current_date=str_current_date_time,
        total_count=total_count
    )

########################################################
# To start an on occurrence compliance
########################################################
def process_start_on_occurrence_compliance(
    db, request, session_user
):
    compliance_id = request.compliance_id
    start_date = request.start_date
    unit_id = request.unit_id
    duration = request.duration
    legal_entity_id = request.legal_entity_id
    remarks = request.remarks

    if start_on_occurrence_task(
        db, legal_entity_id, compliance_id, start_date,
        unit_id, duration, remarks, session_user
    ):
        return clientuser.StartOnOccurrenceComplianceSuccess()
########################################################
# Compliance Filters
########################################################
def process_compliance_filters(
    db, request, session_user
):
    user_units = get_units_for_user(db, session_user)

    return clientuser.ComplianceFiltersSuccess(user_units=user_units)

########################################################
# OnOccurrence Last Transactions
########################################################
def process_onoccurrence_last_transaction(
    db, request, session_user
):
    onOccurrenceTransactions = {}

    onOccurrenceTransactions = process_onoccurrence_transaction_list(db, request, session_user)

    return clientuser.OnOccurrenceLastTransactionSuccess(onoccurrence_transactions=onOccurrenceTransactions)
########################################################
# OnOccurrence Last Transactions
########################################################
def process_onoccurrence_transaction_list(db, request, session_user):

    compliance_id = request.compliance_id
    unit_id = request.unit_id

    resultRows = getLastTransaction_Onoccurrence(db, compliance_id, unit_id)
    transactionList = []

    for row in resultRows:
        compliance_hisory_id = int(row["compliance_history_id"])
        compliance_id = int(row["compliance_id"])
        compliance_task = row["compliance_task"]
        on_statutory = row["statutory"]
        on_unit = row["unit"]
        compliance_description = row["compliance_description"]
        start_date = datetime_to_string(row["start_date"])
        assignee_name = row["assignee"]
        completion_date = datetime_to_string_time(row["completion_date"])
        concurrer_name = row["concurr"]
        concurred_on = datetime_to_string_time(row["concurred_on"])
        approver_name = row["approver"]
        approver_on = datetime_to_string_time(row["approved_on"])
        on_compliance_status = row["compliance_status"]

        transactionList.append(
            clientcore.GetOnoccurrencce_Last_Transaction(compliance_hisory_id, compliance_id, compliance_task, on_statutory, on_unit, compliance_description, start_date, assignee_name, completion_date, concurrer_name, concurred_on, approver_name, approver_on, on_compliance_status)
        )

    return transactionList

###############################################################################################
# Objective: To get reminder settings details
# Parameter: request object and the client id, legal entity id
# Result: return list of legal entity details, domains and organization
###############################################################################################
def process_settings_form_data(db, request, session_user):
    settings_details, settings_users = get_settings_form_data(db, request)
    return clientuser.GetSettingsFormDetailsSuccess(
        settings_details=settings_details,
        settings_users=settings_users
    )

###############################################################################################
# Objective: To save/update reminder settings details
# Parameter: request object and the client id, legal entity id
# Result: return success of the transaction
###############################################################################################
def process_save_settings_form_data(db, request, session_user):
    result = save_settings_form_data(db, request, session_user)
    if result is True:
        return clientuser.SaveSettingsFormDetailsSuccess()
