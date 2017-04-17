import os
from server.jsontocsvconverter import ConvertJsonToCSV
from protocol import core, generalprotocol, possiblefailure
from server.constants import (
    FILE_TYPES,
    FILE_MAX_LIMIT, KNOWLEDGE_FORMAT_PATH,
    CLIENT_DOCS_BASE_PATH
)
from server.common import (save_file_in_path, encrypt)
from server.database.admin import *
from server.database.general import (
    # get_user_form_ids,
    get_notifications, get_audit_trails,
    update_profile,
    verify_password,
    get_messages,
    get_statutory_notifications,
    update_statutory_notification_status,
    get_audit_trail_filters
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
    "process_uploaded_file",
    "process_verify_password",
    "process_update_statutory_notification_status"
]


def process_general_request(request, db, user_id):

    request_frame = request.request
    print request_frame
    if type(request_frame) is generalprotocol.UpdateUserProfile:
        result = procees_update_user_profile(db, request_frame, user_id)

    elif type(request_frame) is generalprotocol.GetDomains:
        result = process_get_domains(db, user_id)

    elif type(request_frame) is generalprotocol.SaveDomain:
        result = process_save_domain(db, request_frame, user_id)

    elif type(request_frame) is generalprotocol.UpdateDomain:
        result = process_update_domain(db, request_frame, user_id)

    elif type(request_frame) is generalprotocol.ChangeDomainStatus:
        result = process_change_domain_status(db, request_frame, user_id)

    elif type(request_frame) is generalprotocol.GetCountriesForUser:
        result = process_get_countries_for_user(db, user_id)

    elif type(request_frame) is generalprotocol.GetCountries:
        result = process_get_countries(db, user_id)

    elif type(request_frame) is generalprotocol.SaveCountry:
        result = process_save_country(db, request_frame, user_id)

    elif type(request_frame) is generalprotocol.UpdateCountry:
        result = process_update_country(db, request_frame, user_id)

    elif type(request_frame) is generalprotocol.ChangeCountryStatus:
        result = process_change_country_status(db, request_frame, user_id)

    elif type(request_frame) is generalprotocol.GetAuditTrails:
        result = process_get_audit_trails(db, request_frame, user_id)

    elif type(request_frame) is generalprotocol.ExportAuditTrails:
        result = process_export_audit_trails(db, request_frame, user_id)

    elif type(request_frame) is generalprotocol.GetAuditTrailsFilter:
        result = process_get_audit_trails_filter(db, request_frame, user_id)

    elif type(request_frame) is generalprotocol.UpdateNotificationStatus:
        result = process_update_notification_status(db, request_frame, user_id)

    elif type(request_frame) is generalprotocol.GetNotifications:
        result = process_get_notifications(db, request_frame, user_id)

    elif type(request_frame) is generalprotocol.VerifyPassword:
        result = process_verify_password(db, request_frame, user_id)

    elif type(request_frame) is generalprotocol.GetMessages:
        result = process_get_messages(db, request_frame, user_id)

    elif type(request_frame) is generalprotocol.GetStatutoryNotifications:
        result = process_get_statutory_notifications(db, request_frame, user_id)

    elif type(request_frame) is generalprotocol.UpdateStatutoryNotificationStatus:
        result = process_update_statutory_notification_status(db, request_frame, user_id)

    return result


def validate_user_session(db, session_token, client_id=None):
    return db.validate_session_token(session_token)


########################################################
# To Handle save domain request
########################################################
def process_save_domain(db, request, user_id):
    domain_name = request.domain_name
    c_ids = request.country_ids
    isDuplicate = check_duplicate_domain(db, domain_name, domain_id=None)
    if isDuplicate:
        return generalprotocol.DomainNameAlreadyExists()
    if (save_domain(db, c_ids, domain_name, user_id)):
        return generalprotocol.SaveDomainSuccess()


########################################################
# To Handle domain update request
########################################################
def process_update_domain(db, request, user_id):
    domain_name = request.domain_name
    domain_id = request.domain_id
    c_ids = request.country_ids
    isDuplicate = check_duplicate_domain(db, domain_name, domain_id)

    if isDuplicate:
        return generalprotocol.DomainNameAlreadyExists()
    if (update_domain(db, c_ids, domain_id, domain_name, user_id)):
        return generalprotocol.UpdateDomainSuccess()
    else:
        return generalprotocol.InvalidDomainId()


########################################################
# To get list of all domains
########################################################
def process_change_domain_status(db, request, user_id):
    is_active = request.is_active
    domain_id = int(request.domain_id)
    if is_active is False:
        # if is_transaction_exists_for_domain(db, domain_id):
        if (update_domain_status(db, domain_id, is_active, user_id)):
            return generalprotocol.ChangeDomainStatusSuccess()
        else:
            return generalprotocol.InvalidDomainId()
        # else:
        #     return generalprotocol.TransactionExists()
    else:
        if (update_domain_status(db, domain_id, is_active, user_id)):
            return generalprotocol.ChangeDomainStatusSuccess()
        else:
            return generalprotocol.InvalidDomainId()


########################################################
# To get list of all domains
########################################################
def process_get_domains(db, user_id):
    domains = get_domains_for_user(db, 0)
    countries = get_countries_for_user(db, user_id)
    success = generalprotocol.GetDomainsSuccess(domains, countries)
    return success


########################################################
# To update the profile of the given user
########################################################
def procees_update_user_profile(db, request, session_user):
    update_profile(db, request.contact_no, request.address, request.mobile_no, request.email_id, session_user)
    return generalprotocol.UpdateUserProfileSuccess(
        request.contact_no, request.address, request.mobile_no, request.email_id
    )


########################################################
# To Handle the save country request
########################################################
def process_save_country(db, request, user_id):
    country_name = request.country_name
    isDuplicate = check_duplicate_country(db, country_name, country_id=None)
    if isDuplicate:
        return generalprotocol.CountryNameAlreadyExists()
    if (save_country(db, country_name, user_id)):
        return generalprotocol.SaveCountrySuccess()


########################################################
# To Handle the country update request
########################################################
def process_update_country(db, request, user_id):
    country_name = request.country_name
    country_id = request.country_id
    isDuplicate = check_duplicate_country(db, country_name, country_id)
    if isDuplicate:
        return generalprotocol.CountryNameAlreadyExists()
    if (update_country(db, country_id, country_name, user_id)):
        return generalprotocol.UpdateCountrySuccess()
    else:
        return generalprotocol.InvalidCountryId()


########################################################
# To change the status of the country received in the
# request as given in the request
########################################################
def process_change_country_status(db, request, user_id):
    is_active = request.is_active
    country_id = int(request.country_id)
    if (
        update_country_status(
            db, country_id, int(is_active), user_id
        )
    ):
        return generalprotocol.ChangeCountryStatusSuccess()
    else:
        return generalprotocol.InvalidCountryId()


########################################################
# To get the list of countries under the given user
########################################################
def process_get_countries_for_user(db, user_id):
    results = get_countries_for_user(db, user_id)
    success = generalprotocol.GetCountriesSuccess(countries=results)
    return success


########################################################
# To get the list of all countries
########################################################
def process_get_countries(db, user_id):
    results = get_countries_for_user(db, 0)
    success = generalprotocol.GetCountriesSuccess(countries=results)
    return success


########################################################
# To retrieve all the audit trails of the given User
########################################################
def process_get_audit_trails(db, request, session_user):
    from_count = request.record_count
    to_count = request.page_count
    from_date = request.from_date
    to_date = request.to_date
    user_id = request.user_id_search
    form_id = request.form_id_search
    category_id = request.category_id
    audit_trails = get_audit_trails(
        db,
        session_user, from_count, to_count,
        from_date, to_date, user_id, form_id,
        category_id, request.client_id, request.legal_entity_id,
        request.unit_id
    )
    return audit_trails

########################################################
# To retrieve all the audit trails of the given User
########################################################
def process_export_audit_trails(db, request, session_user):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "AuditTraiReport"
        )
        return generalprotocol.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )

########################################################
# To retrieve all the audit trails filter data - user, categories
########################################################
def process_get_audit_trails_filter(db, request, session_user):
    audit_trail_filters = get_audit_trail_filters(db)
    return audit_trail_filters

########################################################
# To get the last 30 notifications of the current user
########################################################
def process_get_notifications(db, request, session_user):
    notifications = None
    notifications = get_notifications(
        db, request.notification_type, session_user
    )
    return generalprotocol.GetNotificationsSuccess(
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
    return generalprotocol.UpdateNotificationStatusSuccess()


def process_uploaded_file(info, f_type, client_id=None):
    info_keys = info.keys()
    is_valid = True
    # Validate
    res = None
    for k in info_keys:
        try:
            file_info = info[k]
            file_name = file_info.filename
            file_content = file_info.read()
            f_name = file_name.split('.')
            if len(f_name) == 1:
                res = possiblefailure.InvalidFile()
                is_valid = False
            else:
                file_type = str(f_name[1].lower())
                if file_type in FILE_TYPES:
                    res = possiblefailure.InvalidFile()
                    is_valid = False
                elif len(file_content) == 0:
                    res = possiblefailure.FileIsEmpty()
                    is_valid = False
                elif len(file_content) > FILE_MAX_LIMIT:
                    res = possiblefailure.FileMaxLimitExceed()
                    is_valid = False

            if is_valid :
                lst = []
                if f_type == "knowledge":
                    file_path = "%s/%s" % (KNOWLEDGE_FORMAT_PATH, file_name)
                else:
                    client_dir = "%s/%s" % (CLIENT_DOCS_BASE_PATH, client_id)
                    file_path = "%s/%s" % (client_dir, file_name)
                    if not os.path.exists(client_dir):
                        os.makedirs(client_dir)
                if save_file_in_path(file_path, file_content, file_name):
                    file_response = core.FileList(
                        len(file_content),
                        file_name,
                        None
                    )
                    lst.append(file_response)
                res = generalprotocol.FileUploadSuccess(lst)

        except Exception, e:
            print e

    return res

########################################################
# To Handle the verify password request
########################################################
def process_verify_password(db, request, user_id):
    password = request.password
    encrypt_password = encrypt(password)
    response = verify_password(db, user_id, encrypt_password)
    if response == 0:
        return generalprotocol.InvalidPassword()
    else:
        return generalprotocol.VerifyPasswordSuccess()

########################################################################
# To get the list of messages of the current user unread orderwise
########################################################################
def process_get_messages(db, request, session_user):
    messages = None
    messages = get_messages(
        db, request.from_count, request.page_count, session_user
    )
    return generalprotocol.GetMessagesSuccess(
        messages=messages
    )

##################################################################################
# To get the list of statutory notifications of the current user unread orderwise
##################################################################################
def process_get_statutory_notifications(db, request, session_user):
    statutory_notifications = None
    statutory_notifications = get_statutory_notifications(
        db, request.from_count, request.page_count, session_user
    )
    return generalprotocol.GetStatutoryNotificationsSuccess(
        statutory_notifications=statutory_notifications
    )

########################################################
# To mark the statutory notification as 'Read' once the user read
# a notification
########################################################
def process_update_statutory_notification_status(db, request, session_user):
    result = update_statutory_notification_status(
        db, request.notification_id, request.user_id, request.has_read,
        session_user)

    if result:
        return generalprotocol.UpdateStatutoryNotificationStatusSuccess()
    else:
        raise process_error("E029")
