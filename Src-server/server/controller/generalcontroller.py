from protocol import login, general, core

__all__ = [
	"process_general_request",
	"validate_user_session", "process_save_domain", 
	"process_update_domain",
	"process_change_domain_status", 
	"process_get_domains",
	"procees_update_user_profile",
	"process_save_country", "process_update_country",
	"process_change_country_status", "process_get_countries",
	"process_get_notifications",
	"process_update_notification_status"
]

def process_general_request(request, db) :
	session_token = request.session_token
	request_frame = request.request
	user_id = validate_user_session(db, session_token)
	print request_frame
	if user_id is None:
		return login.InvalidSessionToken()

	if type(request_frame) is general.UpdateUserProfile :
		return procees_update_user_profile(db, request_frame, user_id)
	if type(request_frame) is general.GetDomains :
		return process_get_domains(db, user_id)
	if type(request_frame) is general.SaveDomain :
		return process_save_domain(db, request_frame, user_id)
	if type(request_frame) is general.UpdateDomain :
		return process_update_domain(db, request_frame, user_id)
	if type(request_frame) is general.ChangeDomainStatus :
		return process_change_domain_status(db, request_frame, user_id)
	if type(request_frame) is general.GetCountries :
		return process_get_countries(db, user_id)
	if type(request_frame) is general.SaveCountry :
		return process_save_country(db, request_frame, user_id)
	if type(request_frame) is general.UpdateCountry :
		return process_update_country(db, request_frame, user_id)
	if type(request_frame) is general.ChangeCountryStatus :
		return process_change_country_status(db, request_frame, user_id)
	if type(request_frame) is general.GetAuditTrails :
		return process_get_audit_trails(db, request_frame, user_id)


def validate_user_session(db, session_token):
	return db.validate_session_token(session_token)

def process_save_domain(db, request, user_id):
	domain_name = request.domain_name
	isDuplicate = db.check_duplicate_domain(domain_name, domain_id = None)

	if isDuplicate :
		return general.DomainNameAlreadyExists()

	if (db.save_domain(domain_name, user_id)) :
		return general.SaveDomainSuccess()

def process_update_domain(db, request, user_id):
	domain_name = request.domain_name
	domain_id = request.domain_id
	isDuplicate = db.check_duplicate_domain(domain_name, domain_id)

	if isDuplicate :
		return general.DomainNameAlreadyExists()

	if (db.update_domain(domain_id, domain_name, user_id)) :
		return general.UpdateDomainSuccess()
	else :
		return general.InvalidDomainId()
	
def process_change_domain_status(db, request, user_id):
	is_active = request.is_active
	domain_id = request.domain_id

	if (db.update_domain_status(domain_id, is_active, user_id)) :
		return general.ChangeDomainStatusSuccess()
	else :
		return general.InvalidDomainId()

def process_get_domains(db, user_id):
	results = db.get_domains_for_user(user_id)
	success = general.GetDomainsSuccess(domains=results)
	return success

def procees_update_user_profile(db, request, user_id):
	contact_no = request.contact_no
	address = request.address

	return general.UpdateUserProfileSuccess()

def process_save_country(db, request, user_id):
	country_name = request.country_name
	isDuplicate = db.check_duplicate_country(country_name, country_id = None)

	if isDuplicate :
		return general.CountryNameAlreadyExists()

	if (db.save_country(country_name, user_id)) :
		return general.SaveCountrySuccess()

def process_update_country(db, request, user_id):
	country_name = request.country_name
	country_id = request.country_id
	isDuplicate = db.check_duplicate_country(country_name, country_id)

	if isDuplicate :
		return general.CountryNameAlreadyExists()

	if (db.update_country(country_id, country_name, user_id)) :
		return general.UpdateCountrySuccess()
	else :
		return general.InvalidCountryId()
	
def process_change_country_status(db, request, user_id):
	is_active = request.is_active
	country_id = request.country_id

	if (db.update_country_status(country_id, int(is_active), user_id)) :
		return general.ChangeCountryStatusSuccess()
	else :
		return general.InvalidCountryId()

def process_get_countries(db, user_id):
	results = db.get_countries_for_user(user_id)
	success = general.GetCountriesSuccess(countries=results)
	return success

def process_get_notifications(db, request, user_id):
	notification_type = request.notification_type
	notification_list = []
	notification_id = None
	notification_text = None
	extra_details = None
	has_read = None
	date_and_time = None

	notification_list.append(
		general.Notification(notification_id, notification_text, extra_details, has_read, date_and_time)
	)

	return general.GetNotificationsSuccess(notifications = notification_list)

def process_update_notification_status(db, request, user_id):
	notification_id = request.notification_id
	has_read = request.has_read
	return general.UpdateNotificationStatusSuccess()

def process_get_audit_trails(db, request_frame, user_id):
	audit_trails = db.get_audit_trails(user_id)
	return audit_trails
