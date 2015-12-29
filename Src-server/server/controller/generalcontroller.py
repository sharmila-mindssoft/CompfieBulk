from server.database import DatabaseHandler
from protocol import general, core

__all__ = [
	"validate_session_token", "process_save_domain", "process_update_domain",
	"process_change_domain_status", "process_get_domains"
]

db = DatabaseHandler.instance()
def validate_session_token(session_token):
	return db.validate_session_token(session_token)

def process_save_domain(request, user_id):
	domain_name = request.domain_name
	isDuplicate = db.check_duplicate_domain(domain_name, domain_id = None)

	if isDuplicate :
		return general.DomainNameAlreadyExists()

	if (db.save_domain(domain_name, user_id)) :
		return general.SaveDomainSuccess()

def process_update_domain(request, user_id):
	domain_name = request.domain_name
	domain_id = request.domain_id
	isDuplicate = db.check_duplicate_domain(domain_name, domain_id)

	if isDuplicate :
		return general.DomainNameAlreadyExists()

	if (db.update_domain(domain_id, domain_name, user_id)) :
		return general.UpdateDomainSuccess()
	else :
		return general.InvalidDomainId()
	
def process_change_domain_status(request, user_id):
	is_active = request.is_active
	domain_id = request.domain_id

	if (db.update_domain_status(domain_id, is_active, user_id)) :
		return general.ChangeDomainStatusSuccess()
	else :
		return general.InvalidDomainId()

def process_get_domains(user_id):
	data = db.get_domains_for_user(user_id)
	results = []

	for d in data :
		domain_id = d[0]
		domain_name = d[1]
		is_active = bool(d[2])
		results.append(core.Domain(domain_id, domain_name, is_active))

	success = general.GetDomainsSuccess(domains=results)
	return success