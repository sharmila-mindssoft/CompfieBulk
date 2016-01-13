from protocol import (clienttransactions, core)

__all__ = [
	"process_client_master_requests"
]

def process_client_master_requests(request, db) :
	client_info = request.session_token.split("-")
	request = request.request
	client_id = int(client_info[0])
	session_token = client_info[1]
	session_user = db.validate_session_token(client_id, session_token)
	if session_user is None:
		return login.InvalidSessionToken()

	if type(request) is clienttransactions.GetStatutorySettings :
		pass

	elif type(request) is clienttransactions.UpdateStatutorySettings :
		pass

	elif type(request) is clienttransactions.GetAssignCompliancesFormData:
		pass

	elif type(request) is clienttransactions.SaveAssignedCompliance :
		pass

	elif type(request) is clienttransactions.GetUserwiseCompliances :
		pass

	elif type(request) is clienttransactions.ReassignCompliance :
		pass
	