from protocol import (clientuser, core, login)
from server.controller.corecontroller import process_user_menus

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

	if type(request) is clientuser.GetComplianceDetail:
		return process_get_compliance_detail(db, request, session_user, client_id)
	if type(request) is clientuser.UpdateComplianceDetail:
		return process_update_compliance_detail(db, request, session_user, client_id)
	elif type(request) is clientuser.GetOnOccurrenceCompliances:
		return process_get_on_occurrence_compliances(
		    db, request, session_user, client_id
		)
	elif type(request) is clientuser.StartOnOccurrenceCompliance:
		return process_start_on_occurrence_compliance(
		    db, request, session_user, client_id
		)

########################################################
# To get the ongoing and upcoming compliances of the 
# given user
########################################################
def process_get_compliance_detail(db, request, session_user, client_id):
	current_compliances_list = db.get_current_compliances_list(session_user, client_id)
	upcoming_compliances_list = db.get_upcoming_compliances_list(session_user, client_id)
	current_date_time = db.get_date_time()
	str_current_date_time = db.datetime_to_string_time(current_date_time)
	compliance_details = clientuser.ComplianceDetail(
		current_date=str_current_date_time,
		current_compliances = current_compliances_list,
		upcoming_compliances = upcoming_compliances_list
	)
	return clientuser.GetComplianceDetailSuccess(compliance_details)

########################################################
# To validate and update the compliance details
########################################################
def process_update_compliance_detail(db, request, session_user, client_id):
	result = db.update_compliances(request.compliance_history_id, request.documents,
		request.completion_date, request.validity_date, request.next_due_date,
		request.remarks, client_id, session_user)
	if result == True:
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
	compliances = db.get_on_occurrence_compliances_for_user(session_user)
	return clientuser.GetOnOccurrenceCompliancesSuccess(
		compliances=compliances
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