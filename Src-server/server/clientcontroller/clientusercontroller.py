from protocol import (clientuser, core)
from server.controller.corecontroller import process_user_menus

__all__ = [
	"process_client_user_request"
]

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

def process_get_compliance_detail(db, request, session_user, client_id):
	current_compliances_list = db.get_current_compliances_list(session_user, client_id)
	upcoming_compliances_list = db.get_upcoming_compliances_list(session_user, client_id)
	compliance_details = clientuser.ComplianceDetail(
		current_compliances = current_compliances_list,
		upcoming_compliances = upcoming_compliances_list
	)
	return clientuser.GetComplianceDetailSuccess(compliance_details)