from clientprotocol.jsonvalidators_client import (
    parse_dictionary, parse_static_list, to_structure_dictionary_values
)

#
# Request
#


class Request(object):
    def to_structure(self):
        name = type(self).__name__
        inner = self.to_inner_structure()
        if type(inner) is dict:
            inner = to_structure_dictionary_values(inner)
        return [name, inner]

    def to_inner_structure(self):
        raise NotImplementedError

    @staticmethod
    def parse_structure(data):
        data = parse_static_list(data, 2)
        name, data = data
        if _Request_class_map.get(name) is None:
            msg = "invalid request: " + name
            raise ValueError(msg)
        return _Request_class_map[name].parse_inner_structure(data)

    @staticmethod
    def parse_inner_structure(data):
        raise NotImplementedError


class UpdateUserProfile(Request):
    def __init__(self, contact_no, address, mobile_no, email_id):
        self.contact_no = contact_no
        self.address = address
        self.mobile_no = mobile_no
        self.email_id = email_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["contact_no", "address", "mobile_no", "email_id"])
        contact_no = data.get("contact_no")
        address = data.get("address")
        mobile_no = data.get("mobile_no")
        email_id = data.get("email_id")
        return UpdateUserProfile(contact_no, address, mobile_no, email_id)

    def to_inner_structure(self):
        return {
            "contact_no": self.contact_no,
            "address": self.address,
            "mobile_no": self.mobile_no,
            "email_id": self.email_id
        }


class GetDomains(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetDomains()

    def to_inner_structure(self):
        return {
        }


class SaveDomain(Request):
    def __init__(self, country_ids, domain_name):
        self.country_ids = country_ids
        self.domain_name = domain_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_ids", "d_name"])
        domain_name = data.get("d_name")
        country_ids = data.get("c_ids")
        return SaveDomain(country_ids, domain_name)

    def to_inner_structure(self):
        return {
            "c_ids": self.country_ids,
            "d_name": self.domain_name,
        }


class UpdateDomain(Request):
    def __init__(self, country_ids, domain_id, domain_name):
        self.country_ids = country_ids
        self.domain_id = domain_id
        self.domain_name = domain_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_ids", "d_id", "d_name"])
        country_ids = data.get("c_ids")
        domain_id = data.get("d_id")
        domain_name = data.get("d_name")
        return UpdateDomain(country_ids, domain_id, domain_name)

    def to_inner_structure(self):
        return {
            "c_ids": self.country_ids,
            "d_id": self.domain_id,
            "d_name": self.domain_name,
        }


class ChangeDomainStatus(Request):
    def __init__(self, domain_id, is_active):
        self.domain_id = domain_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["d_id", "is_active"])
        domain_id = data.get("d_id")
        is_active = data.get("is_active")
        return ChangeDomainStatus(domain_id, is_active)

    def to_inner_structure(self):
        return {
            "d_id": self.domain_id,
            "is_active": self.is_active,
        }


class GetCountriesForUser(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetCountriesForUser()

    def to_inner_structure(self):
        return {
        }


class GetCountries(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetCountries()

    def to_inner_structure(self):
        return {
        }


class SaveCountry(Request):
    def __init__(self, country_name):
        self.country_name = country_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_name"])
        country_name = data.get("c_name")
        return SaveCountry(country_name)

    def to_inner_structure(self):
        return {
            "c_name": self.country_name,
        }


class UpdateCountry(Request):
    def __init__(self, country_id, country_name):
        self.country_id = country_id
        self.country_name = country_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_id", "c_name"])
        country_id = data.get("c_id")
        country_name = data.get("c_name")
        return UpdateCountry(country_id, country_name)

    def to_inner_structure(self):
        return {
            "c_id": self.country_id,
            "c_name": self.country_name,
        }


class ChangeCountryStatus(Request):
    def __init__(self, country_id, is_active):
        self.country_id = country_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_id", "is_active"])
        country_id = data.get("c_id")
        is_active = data.get("is_active")
        return ChangeCountryStatus(country_id, is_active)

    def to_inner_structure(self):
        return {
            "c_id": self.country_id,
            "is_active": self.is_active,
        }


class GetNotifications(Request):
    def __init__(self, notification_type):
        self.notification_type = notification_type

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["notification_type"])
        notification_type = data.get("notification_type")
        return GetNotifications(notification_type)

    def to_inner_structure(self):
        return {
            "notification_type": self.notification_type,
        }

class UpdateNotificationStatus(Request):
    def __init__(self, notification_id, has_read):
        self.notification_id = notification_id
        self.has_read = has_read

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["notification_id", "has_read"])
        notification_id = data.get("notification_id")
        has_read = data.get("has_read")
        return UpdateNotificationStatus(notification_id, has_read)

    def to_inner_structure(self):
        return {
            "notification_id": self.notification_id,
            "has_read": self.has_read,
        }

class GetMessages(Request):
    def __init__(self, from_count, page_count):
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["from_count", "page_count"])
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        return GetMessages(from_count, page_count)

    def to_inner_structure(self):
        return {
            "from_count": self.from_count,
            "page_count": self.page_count,
        }

class GetStatutoryNotifications(Request):
    def __init__(self, from_count, page_count):
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["from_count", "page_count"])
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        return GetStatutoryNotifications(from_count, page_count)

    def to_inner_structure(self):
        return {
            "from_count": self.from_count,
            "page_count": self.page_count,
        }

class UpdateStatutoryNotificationStatus(Request):
    def __init__(self, notification_id, user_id, has_read):
        self.notification_id = notification_id
        self.user_id = user_id
        self.has_read = has_read

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["notification_id", "user_id", "has_read"])
        notification_id = data.get("notification_id")
        user_id = data.get("user_id")
        has_read = data.get("has_read")
        return UpdateNotificationStatus(notification_id, has_read)

    def to_inner_structure(self):
        return {
            "notification_id": self.notification_id,
            "user_id": self.user_id,
            "has_read": self.has_read,
        }

class GetAuditTrails(Request):
    def __init__(self, from_date, to_date, user_id_search, form_id_search, country_id, category_id, record_count, page_count):
        self.from_date = from_date
        self.to_date = to_date
        self.user_id_search = user_id_search
        self.form_id_search = form_id_search
        self.country_id = country_id
        self.category_id = category_id
        self.record_count = record_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["from_date", "to_date", "user_id_search", "form_id_search", "country_id", "category_id", "record_count", "page_count"])
        from_date = data.get("from_date")
        to_date = data.get("to_date")
        user_id_search = data.get("user_id_search")
        form_id_search = data.get("form_id_search")
        country_id = data.get("country_id")
        category_id = data.get("category_id")
        record_count = data.get("record_count")
        page_count = data.get("page_count")
        return GetAuditTrails(
            from_date, to_date,
            user_id_search, form_id_search,
            country_id, category_id,
            record_count, page_count
        )

    def to_inner_structure(self):
        return {
            "from_date": self.from_date,
            "to_date": self.to_date,
            "user_id_search": self.user_id_search,
            "form_id_search": self.form_id_search,
            "country_id": self.country_id,
            "category_id": self.category_id,
            "record_count": self.record_count,
            "page_count": self.page_count
        }

class GetAuditTrailsFilter(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetAuditTrailsFilter()

    def to_inner_structure(self):
        return {
        }

class VerifyPassword(Request):
    def __init__(self, password):
        self.password = password

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["password"])
        password = data.get("password")
        return VerifyPassword(password)

    def to_inner_structure(self):
        return {
            "password": self.password,
        }


def _init_Request_class_map():
    classes = [
        UpdateUserProfile, GetDomains, SaveDomain, UpdateDomain,
        ChangeDomainStatus, GetCountriesForUser, GetCountries, SaveCountry, UpdateCountry,
        ChangeCountryStatus, GetNotifications, UpdateNotificationStatus,
        GetAuditTrails, VerifyPassword, GetMessages, GetStatutoryNotifications, UpdateStatutoryNotificationStatus,
        GetAuditTrailsFilter
    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Request_class_map = _init_Request_class_map()


#
# Response
#
class Response(object):
    def to_structure(self):
        name = type(self).__name__
        inner = self.to_inner_structure()
        if type(inner) is dict:
            inner = to_structure_dictionary_values(inner)
        return [name, inner]

    def to_inner_structure(self):
        raise NotImplementedError

    @staticmethod
    def parse_structure(data):
        data = parse_static_list(data, 2)
        name, data = data
        if _Response_class_map.get(name) is None:
            msg = "invalid request: " + name
            raise ValueError(msg)
        return _Response_class_map[name].parse_inner_structure(data)

    @staticmethod
    def parse_inner_structure(data):
        raise NotImplementedError


class UpdateUserProfileSuccess(Response):
    def __init__(self, contact_no, address, mobile_no, email_id):
        self.contact_no = contact_no
        self.address = address
        self.mobile_no = mobile_no
        self.email_id = email_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["contact_no", "address", "mobile_no", "email_id"])
        contact_no = data.get("contact_no")
        address = data.get("address")
        mobile_no = data.get("mobile_no")
        email_id = data.get("email_id")
        return UpdateUserProfile(contact_no, address, mobile_no, email_id)

    def to_inner_structure(self):
        return {
            "contact_no": self.contact_no,
            "address": self.address,
            "mobile_no": self.mobile_no,
            "email_id": self.email_id
        }


class ContactNumberAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ContactNumberAlreadyExists()

    def to_inner_structure(self):
        return {
        }


class GetDomainsSuccess(Response):
    def __init__(self, domains, countries):
        self.domains = domains
        self.countries = countries

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domains", "countries"])
        domains = data.get("domains")
        countries = data.get("countries")
        return GetDomainsSuccess(domains, countries)

    def to_inner_structure(self):
        return {
            "domains": self.domains,
            "countries": self.countries
        }


class SaveDomainSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveDomainSuccess()

    def to_inner_structure(self):
        return {
        }


class DomainNameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return DomainNameAlreadyExists()

    def to_inner_structure(self):
        return {
        }

class UpdateDomainSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateDomainSuccess()

    def to_inner_structure(self):
        return {
        }

class InvalidDomainId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidDomainId()

    def to_inner_structure(self):
        return {
        }


class ChangeDomainStatusSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ChangeDomainStatusSuccess()

    def to_inner_structure(self):
        return {
        }


class GetCountriesSuccess(Response):
    def __init__(self, countries):
        self.countries = countries

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries"])
        countries = data.get("countries")
        return GetCountriesSuccess(countries)

    def to_inner_structure(self):

        data = {
            "countries": self.countries
        }
        return data


class SaveCountrySuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveCountrySuccess()

    def to_inner_structure(self):
        return {
        }


class CountryNameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CountryNameAlreadyExists()

    def to_inner_structure(self):
        return {
        }


class UpdateCountrySuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateCountrySuccess()

    def to_inner_structure(self):
        return {
        }


class InvalidCountryId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidCountryId()

    def to_inner_structure(self):
        return {
        }


class ChangeCountryStatusSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ChangeCountryStatusSuccess()

    def to_inner_structure(self):
        return {
        }


class GetNotificationsSuccess(Response):
    def __init__(self, notifications):
        self.notifications = notifications

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["notifications"])
        notifications = data.get("notifications")
        return GetNotificationsSuccess(notifications)

    def to_inner_structure(self):
        return {
            "notifications": self.notifications
        }


class UpdateNotificationStatusSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateNotificationStatusSuccess()

    def to_inner_structure(self):
        return {
        }


class GetMessagesSuccess(Response):
    def __init__(self, messages):
        self.messages = messages

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["messages"])
        messages = data.get("messages")
        return GetMessagesSuccess(messages)

    def to_inner_structure(self):
        return {
            "messages": self.messages
        }

class GetStatutoryNotificationsSuccess(Response):
    def __init__(self, statutory_notifications):
        self.statutory_notifications = statutory_notifications

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutory_notifications"])
        statutory_notifications = data.get("statutory_notifications")
        return GetStatutoryNotificationsSuccess(statutory_notifications)

    def to_inner_structure(self):
        return {
            "statutory_notifications": self.statutory_notifications
        }

class UpdateStatutoryNotificationStatusSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateStatutoryNotificationStatusSuccess()

    def to_inner_structure(self):
        return {
        }

class GetAuditTrailSuccess(Response):
    def __init__(self, audit_trails, total_records):
        self.audit_trails = audit_trails
        self.total_records = total_records

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
                "audit_trails", "total_records"
            ])
        audit_trails = data.get("audit_trails")
        total_records = data.get("total_records")
        return GetAuditTrailSuccess(audit_trails, total_records)

    def to_inner_structure(self):
        return {
            "audit_trail_details": self.audit_trails,
            "total_records": self.total_records,
        }

class GetAuditTrailFilterSuccess(Response):
    def __init__(self, user_categories, audit_trail_countries, forms_list, users, audit_trail_details):
        self.user_categories = user_categories
        self.audit_trail_countries = audit_trail_countries
        self.forms_list = forms_list
        self.users = users
        self.audit_trail_details = audit_trail_details

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
                "user_categories", "audit_trail_countries", "forms_list", "users",
                "audit_trail_details"
            ])
        user_categories = data.get("user_categories")
        audit_trail_countries = data.get("audit_trail_countries")
        forms_list = data.get("forms_list")
        users = data.get("users")
        audit_trail_details = data.get("audit_trail_details")

        return GetAuditTrailFilterSuccess(user_categories, audit_trail_countries, forms_list, users, audit_trail_details)

    def to_inner_structure(self):
        data = {
            "user_categories": self.user_categories,
            "audit_trail_countries": self.audit_trail_countries,
            "forms_list": self.forms_list,
            "users": self.users,
            "audit_trail_details": self.audit_trail_details,
        }
        return data

class MasterDataNotAvailableForClient(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return MasterDataNotAvailableForClient()

    def to_inner_structure(self):
        return {
        }

class TransactionExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return TransactionExists()

    def to_inner_structure(self):
        return {
        }

class TransactionJobId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["job_id"])
        job_id = data.get("job_id")
        return TransactionJobId(job_id)

    def to_inner_structure(self):
        return {
            "job_id": self.job_id
        }

class FileUploadSuccess(Response):
    def __init__(self, file_list):
        self.file_list = file_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["file_list"])
        file_list = data.get("file_list")
        return FileUploadSuccess(file_list)

    def to_inner_structure(self):
        return {
            "file_list": self.file_list
        }

class InvalidPassword(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidPassword()

    def to_inner_structure(self):
        return {
        }

class VerifyPasswordSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return VerifyPasswordSuccess()

    def to_inner_structure(self):
        return {
        }

def _init_Response_class_map():
    classes = [
        UpdateUserProfileSuccess, ContactNumberAlreadyExists,
        GetDomainsSuccess, SaveDomainSuccess, DomainNameAlreadyExists,
        UpdateDomainSuccess, InvalidDomainId, ChangeDomainStatusSuccess,
        GetNotificationsSuccess, UpdateNotificationStatusSuccess, GetAuditTrailSuccess,
        MasterDataNotAvailableForClient, TransactionExists, TransactionJobId,
        FileUploadSuccess, VerifyPasswordSuccess, InvalidPassword, GetMessagesSuccess,
        GetStatutoryNotificationsSuccess, UpdateStatutoryNotificationStatusSuccess
    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()

#
# Notification
#

class Notification(object):
    def __init__(self, notification_id, notification_text, link, has_read, date_and_time):
        self.notification_id = notification_id
        self.notification_text = notification_text
        self.link = link
        self.has_read = has_read
        self.date_and_time = date_and_time

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["notification_id", "notification_text", "link", "has_read", "date_and_time"])
        notification_id = data.get("notification_id")
        notification_text = data.get("notification_text")
        link = data.get("link")
        has_read = data.get("has_read")
        date_and_time = data.get("date_and_time")
        return Notification(notification_id, notification_text, link, has_read, date_and_time)

    def to_structure(self):
        return {
            "notification_id": self.notification_id,
            "notification_text": self.notification_text,
            "link": self.link,
            "has_read": self.has_read,
            "date_and_time": self.date_and_time,
        }

#
# Audit Trail
#
class AuditTrail(object):
    def __init__(self, user_id, user_category_id, form_id, action, date):
        self.user_id = user_id
        self.user_category_id = user_category_id
        self.form_id = form_id
        self.action = action
        self.date = date

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "user_category_id", "form_id", "action", "date"])
        user_id = data.get("user_id")
        user_category_id = data.get("user_category_id")
        form_id = data.get("form_id")
        action = data.get("action")
        date = data.get("date")
        return AuditTrail(user_id, user_category_id, form_id, action, date)

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "user_category_id": self.user_category_id,
            "form_id": self.form_id,
            "action": self.action,
            "date": self.date
        }

class AuditTrailCountries(object):
    def __init__(self, user_id, user_category_id, country_id, country_name):
        self.user_id = user_id
        self.user_category_id = user_category_id
        self.country_id = country_id
        self.country_name = country_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "user_category_id", "country_id", "country_name"])
        user_id = data.get("user_id")
        user_category_id = data.get("user_category_id")
        country_id = data.get("country_id")
        country_name = data.get("country_name")
        return AuditTrailCountries(user_id, user_category_id, country_id, country_name)

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "user_category_id": self.user_category_id,
            "country_id": self.country_id,
            "country_name": self.country_name
        }

class AuditTrailForm(object):
    def __init__(self, form_id, form_name):

        self.form_id = form_id
        self.form_name = form_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["form_id", "form_name"])
        form_id = data.get("form_id")
        form_name = data.get("form_name")
        return AuditTrailForm(form_id, form_name)

    def to_structure(self):
        return {
            "form_id": self.form_id,
            "form_name": self.form_name
        }


#
# Message
#

class Message(object):
    def __init__(self, message_id, message_heading, message_text, link, created_by, created_on):
        self.message_id = message_id
        self.message_heading = message_heading
        self.message_text = message_text
        self.link = link
        self.created_by = created_by
        self.created_on = created_on

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["message_id", "message_heading", "message_text", "link", "created_by", "created_on"])
        message_id = data.get("message_id")
        message_heading = data.get("message_heading")
        message_text = data.get("message_text")
        link = data.get("link")
        created_by = data.get("created_by")
        created_on = data.get("created_on")
        return Message(message_id, message_heading, message_text, link, created_by, created_on)

    def to_structure(self):
        return {
            "message_id": self.message_id,
            "message_heading": self.message_heading,
            "message_text": self.message_text,
            "link": self.link,
            "created_by": self.created_by,
            "created_on": self.created_on,
        }

#
# StatutoryNotiification
#

class StatutoryNotification(object):
    def __init__(self, notification_id, user_id, compliance_id, notification_text, created_by, created_on, has_read):
        self.notification_id = notification_id
        self.user_id = user_id
        self.compliance_id = compliance_id
        self.notification_text = notification_text
        self.created_by = created_by
        self.created_on = created_on
        self.has_read = has_read

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["notification_id", "user_id", "compliance_id", "notification_text", "created_by", "created_on", "has_read"])
        notification_id = data.get("notification_id")
        user_id = data.get("user_id")
        compliance_id = data.get("compliance_id")
        notification_text = data.get("notification_text")
        created_by = data.get("created_by")
        created_on = data.get("created_on")
        has_read = data.get("has_read")
        return notification(notification_id, user_id, compliance_id, notification_text, created_by, created_on, has_read)

    def to_structure(self):
        return {
            "notification_id": self.notification_id,
            "user_id": self.user_id,
            "compliance_id": self.compliance_id,
            "notification_text": self.notification_text,
            "created_by": self.created_by,
            "created_on": self.created_on,
            "has_read": self.has_read
        }

#
# RequestFormat
#

class RequestFormat(object):
    def __init__(self, session_token, request):
        self.session_token = session_token
        self.request = request

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["session_token", "request"])
        session_token = data.get("session_token")
        request = data.get("request")
        request = Request.parse_structure(request)
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": Request.to_structure(self.request)
        }
