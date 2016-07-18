import os
from protocol import core, login, general, possiblefailure
from server import logger
from server.constants import (
    RECORD_DISPLAY_COUNT, FILE_TYPES,
    FILE_MAX_LIMIT, KNOWLEDGE_FORMAT_PATH,
    CLIENT_DOCS_BASE_PATH
)
from server.common import (save_file_in_path)
from server.database.admin import *
from server.database.general import (
    get_user_form_ids,
    get_notifications
)

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
    "process_update_notification_status",
    "process_uploaded_file"
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
        logger.logKnowledgeApi("UpdateUserProfile", "process begin")
        result = procees_update_user_profile(db, request_frame, user_id)
        logger.logKnowledgeApi("UpdateUserProfile", "process end")

    elif type(request_frame) is general.GetDomains :
        logger.logKnowledgeApi("GetDomains", "process begin")
        result = process_get_domains(db, user_id)
        logger.logKnowledgeApi("GetDomains", "process end")

    elif type(request_frame) is general.SaveDomain :
        logger.logKnowledgeApi("SaveDomain", "process begin")
        result = process_save_domain(db, request_frame, user_id)
        logger.logKnowledgeApi("SaveDomain", "process end")

    elif type(request_frame) is general.UpdateDomain :
        logger.logKnowledgeApi("UpdateDomain", "process begin")
        result = process_update_domain(db, request_frame, user_id)
        logger.logKnowledgeApi("UpdateDomain", "process end")

    elif type(request_frame) is general.ChangeDomainStatus :
        logger.logKnowledgeApi("ChangeDomainStatus", "process begin")
        result = process_change_domain_status(db, request_frame, user_id)
        logger.logKnowledgeApi("ChangeDomainStatus", "process end")

    elif type(request_frame) is general.GetCountriesForUser :
        logger.logKnowledgeApi("GetCountriesForUser", "process begin")
        result = process_get_countries_for_user(db, user_id)
        logger.logKnowledgeApi("GetCountriesForUser", "process end")

    elif type(request_frame) is general.GetCountries :
        logger.logKnowledgeApi("GetCountries", "process begin")
        result = process_get_countries(db, user_id)
        logger.logKnowledgeApi("GetCountries", "process end")

    elif type(request_frame) is general.SaveCountry :
        logger.logKnowledgeApi("SaveCountry", "process begin")
        result = process_save_country(db, request_frame, user_id)
        logger.logKnowledgeApi("SaveCountry", "process end")

    elif type(request_frame) is general.UpdateCountry :
        logger.logKnowledgeApi("UpdateCountry", "process begin")
        result = process_update_country(db, request_frame, user_id)
        logger.logKnowledgeApi("UpdateCountry", "process end")

    elif type(request_frame) is general.ChangeCountryStatus :
        logger.logKnowledgeApi("ChangeCountryStatus", "process begin")
        result = process_change_country_status(db, request_frame, user_id)
        logger.logKnowledgeApi("ChangeCountryStatus", "process end")

    elif type(request_frame) is general.GetAuditTrails :
        logger.logKnowledgeApi("GetAuditTrails", "process begin")
        result = process_get_audit_trails(db, request_frame, user_id)
        logger.logKnowledgeApi("GetAuditTrails", "process end")

    elif type(request_frame) is general.UpdateNotificationStatus :
        logger.logKnowledgeApi("UpdateNotificationStatus", "process begin")
        result = process_update_notification_status(db, request_frame, user_id)
        logger.logKnowledgeApi("UpdateNotificationStatus", "process end")

    elif type(request_frame) is general.GetNotifications :
        logger.logKnowledgeApi("GetNotifications", "process begin")
        result = process_get_notifications(db, request_frame, user_id)
        logger.logKnowledgeApi("GetNotifications", "process end")

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
            alloted_forms = get_user_form_ids(db, user_id)
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
    isDuplicate = check_duplicate_domain(db, domain_name, domain_id=None)

    if isDuplicate :
        return general.DomainNameAlreadyExists()

    if (save_domain(db, domain_name, user_id)) :
        return general.SaveDomainSuccess()

########################################################
# To Handle domain update request
########################################################
def process_update_domain(db, request, user_id):
    domain_name = request.domain_name
    domain_id = request.domain_id
    isDuplicate = check_duplicate_domain(db, domain_name, domain_id)

    if isDuplicate :
        return general.DomainNameAlreadyExists()

    if (update_domain(db, domain_id, domain_name, user_id)) :
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
        if check_domain_id_to_deactivate(db, domain_id) :
            if (update_domain_status(db, domain_id, is_active, user_id)) :
                return general.ChangeDomainStatusSuccess()
            else :
                return general.InvalidDomainId()
        else :
            return general.TransactionExists()
    else :
        if (update_domain_status(db, domain_id, is_active, user_id)) :
            return general.ChangeDomainStatusSuccess()
        else :
            return general.InvalidDomainId()

########################################################
# To get list of all domains
########################################################
def process_get_domains(db, user_id):
    results = get_domains_for_user(db, 0)
    success = general.GetDomainsSuccess(domains=results)
    return success

########################################################
# To update the profile of the given user
########################################################
def procees_update_user_profile(db, request, session_user):
    update_profile(db, request.contact_no, request.address, session_user)
    return general.UpdateUserProfileSuccess(request.contact_no, request.address)

########################################################
# To Handle the save country request
########################################################
def process_save_country(db, request, user_id):
    country_name = request.country_name
    isDuplicate = check_duplicate_country(db, country_name, country_id=None)

    if isDuplicate :
        return general.CountryNameAlreadyExists()

    if (save_country(db, country_name, user_id)) :
        return general.SaveCountrySuccess()

########################################################
# To Handle the country update request
########################################################
def process_update_country(db, request, user_id):
    country_name = request.country_name
    country_id = request.country_id
    isDuplicate = check_duplicate_country(db, country_name, country_id)

    if isDuplicate :
        return general.CountryNameAlreadyExists()

    if (update_country(db, country_id, country_name, user_id)) :
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
        if check_country_id_to_deactivate(db, country_id) :
            if (update_country_status(db, country_id, int(is_active), user_id)) :
                return general.ChangeCountryStatusSuccess()
            else :
                return general.InvalidCountryId()
        else :
            return general.TransactionExists()
    else :
        if (update_country_status(db, country_id, int(is_active), user_id)) :
            return general.ChangeCountryStatusSuccess()
        else :
            return general.InvalidCountryId()

########################################################
# To get the list of countries under the given user
########################################################
def process_get_countries_for_user(db, user_id):
    results = get_countries_for_user(db, user_id)
    success = general.GetCountriesSuccess(countries=results)
    return success

########################################################
# To get the list of all countries
########################################################
def process_get_countries(db, user_id):
    results = get_countries_for_user(db, 0)
    success = general.GetCountriesSuccess(countries=results)
    return success

########################################################
# To retrieve all the audit trails of the given User
########################################################
def process_get_audit_trails(db, request, session_user):
    from_count = request.record_count
    to_count = RECORD_DISPLAY_COUNT
    from_date = request.from_date
    to_date = request.to_date
    user_id = request.user_id
    form_id = request.form_id
    audit_trails = get_audit_trails(
        db,
        session_user, from_count, to_count,
        from_date, to_date, user_id, form_id
    )
    return audit_trails

########################################################
# To get the last 30 notifications of the current user
########################################################
def process_get_notifications(db, request, session_user):
    notifications = None
    notifications = get_notifications(db, request.notification_type, session_user)
    return general.GetNotificationsSuccess(
        notifications=notifications
    )


########################################################
# To mark the notification as 'Read' once the user read
# a notification
########################################################
def process_update_notification_status(db, request, session_user):
    update_notification_status(
        db, request.notification_id, request.has_read,
        session_user)
    return general.UpdateNotificationStatusSuccess()

def process_uploaded_file(info, f_type, client_id=None):
    info_keys = info.keys()
    is_valid = True
    # Validate
    res = None
    for k in info_keys :
        try :
            file_info = info[k][0]
            file_name = file_info.file_name()
            file_content = file_info.body()
            f_name = file_name.split('.')
            if len(f_name) == 1 :
                res = possiblefailure.InvalidFile()
                is_valid = False
            else :
                file_type = str(f_name[1].lower())
                if file_type in FILE_TYPES :
                    res = possiblefailure.InvalidFile()
                    is_valid = False
                elif len(file_content) == 0 :
                    res = possiblefailure.FileIsEmpty()
                    is_valid = False
                elif len(file_content) > FILE_MAX_LIMIT :
                    res = possiblefailure.FileMaxLimitExceed()
                    is_valid = False

        except Exception, e :
            print e
    if is_valid :
        lst = []
        for k in info_keys :
            try :
                file_info = info[k][0]
                file_name = file_info.file_name()
                file_content = file_info.body()
                if f_type == "knowledge" :
                    file_path = "%s/%s" % (KNOWLEDGE_FORMAT_PATH, file_name)
                else :
                    client_dir = "%s/%s" % (CLIENT_DOCS_BASE_PATH, client_id)
                    file_path = "%s/%s" % (client_dir, file_name)
                    if not os.path.exists(client_dir):
                        os.makedirs(client_dir)
                if save_file_in_path(file_path, file_content, file_name) :
                    file_response = core.FileList(
                        len(file_content),
                        file_name,
                        None
                    )
                    lst.append(file_response)
            except Exception, e :
                print e
        res = general.FileUploadSuccess(lst)
    else :
        print "is_valid ", is_valid
    return res
