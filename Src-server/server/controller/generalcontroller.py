from protocol import login, general, core
from server import logger

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

forms = [1, 2]

def process_general_request(request, db) :
    session_token = request.session_token
    request_frame = request.request
    user_id = validate_user_session(db, session_token)
    if user_id is not None :
        is_valid = validate_user_forms(db, user_id, forms, request_frame)
        if is_valid is not True :
            return login.InvalidSessionToken()
    if user_id is None:
        return login.InvalidSessionToken()

    if type(request_frame) is general.UpdateUserProfile :
        logger.logClientApi("UpdateUserProfile", "process begin")
        result = procees_update_user_profile(db, request_frame, user_id)
        logger.logClientApi("UpdateUserProfile", "process end")

    elif type(request_frame) is general.GetDomains :
        logger.logClientApi("GetDomains", "process begin")
        result = process_get_domains(db, user_id)
        logger.logClientApi("GetDomains", "process end")

    elif type(request_frame) is general.SaveDomain :
        logger.logClientApi("SaveDomain", "process begin")
        result = process_save_domain(db, request_frame, user_id)
        logger.logClientApi("SaveDomain", "process end")

    elif type(request_frame) is general.UpdateDomain :
        logger.logClientApi("UpdateDomain", "process begin")
        result = process_update_domain(db, request_frame, user_id)
        logger.logClientApi("UpdateDomain", "process end")

    elif type(request_frame) is general.ChangeDomainStatus :
        logger.logClientApi("ChangeDomainStatus", "process begin")
        result = process_change_domain_status(db, request_frame, user_id)
        logger.logClientApi("ChangeDomainStatus", "process end")

    elif type(request_frame) is general.GetCountriesForUser :
        logger.logClientApi("GetCountriesForUser", "process begin")
        result = process_get_countries_for_user(db, user_id)
        logger.logClientApi("GetCountriesForUser", "process end")

    elif type(request_frame) is general.GetCountries :
        logger.logClientApi("GetCountries", "process begin")
        result = process_get_countries(db, user_id)
        logger.logClientApi("GetCountries", "process end")

    elif type(request_frame) is general.SaveCountry :
        logger.logClientApi("SaveCountry", "process begin")
        result = process_save_country(db, request_frame, user_id)
        logger.logClientApi("SaveCountry", "process end")

    elif type(request_frame) is general.UpdateCountry :
        logger.logClientApi("UpdateCountry", "process begin")
        result = process_update_country(db, request_frame, user_id)
        logger.logClientApi("UpdateCountry", "process end")

    elif type(request_frame) is general.ChangeCountryStatus :
        logger.logClientApi("ChangeCountryStatus", "process begin")
        result = process_change_country_status(db, request_frame, user_id)
        logger.logClientApi("ChangeCountryStatus", "process end")

    elif type(request_frame) is general.GetAuditTrails :
        logger.logClientApi("GetAuditTrails", "process begin")
        result = process_get_audit_trails(db, request_frame, user_id)
        logger.logClientApi("GetAuditTrails", "process end")

    elif type(request_frame) is general.UpdateNotificationStatus :
        logger.logClientApi("UpdateNotificationStatus", "process begin")
        result = process_update_notification_status(db, request_frame, user_id)
        logger.logClientApi("UpdateNotificationStatus", "process end")

    elif type(request_frame) is general.GetNotifications :
        logger.logClientApi("GetNotifications", "process begin")
        result = process_get_notifications(db, request_frame, user_id)
        logger.logClientApi("GetNotifications", "process end")

    return result

def validate_user_session(db, session_token, client_id=None):
    if client_id:
        return db.validate_session_token(client_id, session_token)
    else:
        return db.validate_session_token(session_token)

def validate_user_forms(db, user_id, form_ids, requet):
    if user_id == 0 and type(requet) in [
        general.UpdateNotificationStatus,
        general.UpdateUserProfile,
        general.GetAuditTrails
    ] :
        return False

    if type(requet) not in [
        general.GetNotifications,
        general.UpdateNotificationStatus,
        general.UpdateUserProfile,
        general.GetAuditTrails
    ] :
        valid = 0
        if user_id is not None :
            alloted_forms = db.get_user_form_ids(user_id)
            alloted_forms = [int(x) for x in alloted_forms.split(",")]
            for i in alloted_forms :
                if i in form_ids :
                    valid += 1
            if valid > 0 :
                return True
        return False

    else :
        return True

########################################################
# To Handle save domain request
########################################################
def process_save_domain(db, request, user_id):
    domain_name = request.domain_name
    isDuplicate = db.check_duplicate_domain(domain_name, domain_id=None)

    if isDuplicate :
        return general.DomainNameAlreadyExists()

    if (db.save_domain(domain_name, user_id)) :
        return general.SaveDomainSuccess()

########################################################
# To Handle domain update request
########################################################
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

########################################################
# To get list of all domains
########################################################
def process_change_domain_status(db, request, user_id):
    is_active = request.is_active
    domain_id = int(request.domain_id)
    if is_active is False :
        if db.check_domain_id_to_deactivate(domain_id) :
            if (db.update_domain_status(domain_id, is_active, user_id)) :
                return general.ChangeDomainStatusSuccess()
            else :
                return general.InvalidDomainId()
        else :
            return general.TransactionExists()
    else :
        if (db.update_domain_status(domain_id, is_active, user_id)) :
            return general.ChangeDomainStatusSuccess()
        else :
            return general.InvalidDomainId()

########################################################
# To get list of all domains
########################################################
def process_get_domains(db, user_id):
    results = db.get_domains_for_user(0)
    success = general.GetDomainsSuccess(domains=results)
    return success

########################################################
# To update the profile of the given user
########################################################
def procees_update_user_profile(db, request, session_user):
    db.update_profile(request.contact_no, request.address, session_user)
    return general.UpdateUserProfileSuccess(request.contact_no, request.address)

########################################################
# To Handle the save country request
########################################################
def process_save_country(db, request, user_id):
    country_name = request.country_name
    isDuplicate = db.check_duplicate_country(country_name, country_id = None)

    if isDuplicate :
        return general.CountryNameAlreadyExists()

    if (db.save_country(country_name, user_id)) :
        return general.SaveCountrySuccess()

########################################################
# To Handle the country update request
########################################################
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

########################################################
# To change the status of the country received in the
# request as given in the request
########################################################
def process_change_country_status(db, request, user_id):
    is_active = request.is_active
    country_id = int(request.country_id)
    if is_active is False :
        if db.check_country_id_to_deactivate(country_id) :
            if (db.update_country_status(country_id, int(is_active), user_id)) :
                return general.ChangeCountryStatusSuccess()
            else :
                return general.InvalidCountryId()
        else :
            return general.TransactionExists()
    else :
        if (db.update_country_status(country_id, int(is_active), user_id)) :
            return general.ChangeCountryStatusSuccess()
        else :
            return general.InvalidCountryId()

########################################################
# To get the list of countries under the given user
########################################################
def process_get_countries_for_user(db, user_id):
    results = db.get_countries_for_user(user_id)
    success = general.GetCountriesSuccess(countries=results)
    return success

########################################################
# To get the list of all countries
########################################################
def process_get_countries(db, user_id):
    results = db.get_countries_for_user(0)
    success = general.GetCountriesSuccess(countries=results)
    return success

########################################################
# To retrieve all the audit trails of the given User
########################################################
def process_get_audit_trails(db, request_frame, user_id):
    audit_trails = db.get_audit_trails(user_id)
    return audit_trails

########################################################
# To get the last 30 notifications of the current user
########################################################
def process_get_notifications(db, request, session_user):
    notifications = None
    notifications = db.get_notifications(request.notification_type, session_user)
    return general.GetNotificationsSuccess(notifications = notifications)


########################################################
# To mark the notification as 'Read' once the user read
# a notification
########################################################
def process_update_notification_status(db, request, session_user):
    notifications = None
    db.update_notification_status(request.notification_id, request.has_read,
        session_user)
    return general.UpdateNotificationStatusSuccess()
