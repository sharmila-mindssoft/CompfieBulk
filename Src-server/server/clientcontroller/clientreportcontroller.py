from protocol import (clientmasters, core)
from server.controller.corecontroller import process_user_menus

__all__ = [
	"process_client_report_requests"
]

def process_client_report_requests(request, db) :
	client_info = request.session_token.split("-")
	request = request.request
	client_id = int(client_info[0])
	session_token = client_info[1]
	session_user = db.validate_session_token(client_id, session_token)
	if session_user is None:
		return login.InvalidSessionToken()

	if type(request) is clientmasters.GetServiceProviders:
		return get_service_providers(db, request, session_user, client_id)