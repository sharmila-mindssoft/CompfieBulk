from protocol import (clienttransactions, core)

__all__ = [
	"process_client_transaction_requests"
]

def process_client_transaction_requests(request, db) :
	client_info = request.session_token.split("-")
	request = request.request
	client_id = int(client_info[0])
	session_token = client_info[1]
	session_user = db.validate_session_token(client_id, session_token)
	if session_user is None:
		return login.InvalidSessionToken()

	if type(request) is clienttransactions.GetStatutorySettings :
		return process_get_statutory_settings(db, session_user, client_id)

	elif type(request) is clienttransactions.UpdateStatutorySettings :
		return process_update_statutory_settings(db, request, session_user, client_id)

	elif type(request) is clienttransactions.GetAssignCompliancesFormData:
		pass

	elif type(request) is clienttransactions.SaveAssignedCompliance :
		pass

	elif type(request) is clienttransactions.GetUserwiseCompliances :
		pass

	elif type(request) is clienttransactions.ReassignCompliance :
		pass

def process_get_statutory_settings(db, session_user, client_id):
	return db.get_statutory_settings(session_user, client_id)

def process_update_statutory_settings(db, request, session_user, client_id):
	return db.update_statutory_settings(request, session_user, client_id)
	 