from protocol.jsonvalidators import (
    parse_dictionary, parse_static_list, to_structure_dictionary_values,
    to_dictionary_values
)
from protocol.parse_structure import (
    parse_structure_VectorType_RecordType_general_Notification,
    parse_structure_CustomTextType_250,
    parse_structure_VectorType_RecordType_core_Domain,
    parse_structure_UnsignedIntegerType_32,
    parse_structure_VariantType_general_Request, parse_structure_Bool,
    parse_structure_CustomTextType_20, parse_structure_CustomTextType_500,
    parse_structure_CustomTextType_50,
    parse_structure_VectorType_RecordType_general_AuditTrail,
    parse_structure_VectorType_RecordType_general_User,
    parse_structure_VectorType_RecordType_general_AuditTrailForm,
    parse_structure_OptionalType_UnsignedIntegerType_32,
    parse_structure_Text,
    parse_structure_VectorType_RecordType_core_FileLst
)
from protocol.to_structure import (
    to_structure_VectorType_RecordType_general_Notification,
    to_structure_CustomTextType_250,
    to_structure_VectorType_RecordType_core_Domain,
    to_structure_SignedIntegerType_8,
    to_structure_VariantType_general_Request, to_structure_Bool,
    to_structure_CustomTextType_20, to_structure_CustomTextType_500,
    to_structure_CustomTextType_50,
    to_structure_VectorType_RecordType_general_AuditTrail,
    to_structure_UnsignedIntegerType_32,
    to_structure_VectorType_RecordType_general_User,
    to_structure_VectorType_RecordType_general_AuditTrailForm,
    to_structure_OptionalType_UnsignedIntegerType_32,
    to_structure_Text,
    to_structure_VectorType_RecordType_core_FileLst
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
    def __init__(self, contact_no, address):
        self.contact_no = contact_no
        self.address = address

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["contact_no", "address"])
        contact_no = data.get("contact_no")
        contact_no = parse_structure_CustomTextType_20(contact_no)
        address = data.get("address")
        address = parse_structure_CustomTextType_250(address)
        return UpdateUserProfile(contact_no, address)

    def to_inner_structure(self):
        return {
            "contact_no": to_structure_CustomTextType_20(self.contact_no),
            "address": to_structure_CustomTextType_250(self.address),
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
    def __init__(self, domain_name):
        self.domain_name = domain_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["d_name"])
        domain_name = data.get('d_name')
        return SaveDomain(domain_name)

    def to_inner_structure(self):
        return {
            "d_name": self.domain_name,
        }

class UpdateDomain(Request):
    def __init__(self, domain_id, domain_name):
        self.domain_id = domain_id
        self.domain_name = domain_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["d_id", "d_name"])
        domain_id = data.get("d_id")
        domain_name = data.get("d_name")
        return UpdateDomain(domain_id, domain_name)

    def to_inner_structure(self):
        return {
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
        notification_type = parse_structure_CustomTextType_20(notification_type)
        return GetNotifications(notification_type)

    def to_inner_structure(self):
        return {
            "notification_type": to_structure_CustomTextType_20(self.notification_type),
        }

class UpdateNotificationStatus(Request):
    def __init__(self, notification_id, has_read):
        self.notification_id = notification_id
        self.has_read = has_read

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["notification_id", "has_read"])
        notification_id = data.get("notification_id")
        notification_id = parse_structure_UnsignedIntegerType_32(notification_id)
        has_read = data.get("has_read")
        has_read = parse_structure_Bool(has_read)
        return UpdateNotificationStatus(notification_id, has_read)

    def to_inner_structure(self):
        return {
            "notification_id": to_structure_UnsignedIntegerType_32(self.notification_id),
            "has_read": to_structure_Bool(self.has_read),
        }

class GetAuditTrails(Request):
    def __init__(self, from_date, to_date, user_id, form_id, record_count, page_count):
        self.from_date = from_date
        self.to_date = to_date
        self.user_id = user_id
        self.form_id = form_id
        self.record_count = record_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["from_date", "to_date", "user_id", "form_id", "record_count", "page_count"])
        from_date = data.get("from_date")
        from_date = parse_structure_CustomTextType_20(from_date)
        to_date = data.get("to_date")
        to_date = parse_structure_CustomTextType_20(to_date)
        user_id = data.get("user_id")
        user_id = parse_structure_OptionalType_UnsignedIntegerType_32(user_id)
        form_id = data.get("form_id")
        form_id = parse_structure_OptionalType_UnsignedIntegerType_32(form_id)
        record_count = data.get("record_count")
        record_count = parse_structure_UnsignedIntegerType_32(record_count)
        page_count = data.get("page_count")
        page_count = parse_structure_UnsignedIntegerType_32(page_count)
        return GetAuditTrails(
            from_date, to_date,
            user_id, form_id,
            record_count, page_count
        )

    def to_inner_structure(self):
        return {
            "from_date": to_structure_CustomTextType_20(self.from_date),
            "to_date": to_structure_CustomTextType_20(self.to_date),
            "user_id": to_structure_OptionalType_UnsignedIntegerType_32(self.user_id),
            "form_id": to_structure_OptionalType_UnsignedIntegerType_32(self.form_id),
            "record_count": to_structure_UnsignedIntegerType_32(self.record_count),
            "page_count": to_structure_UnsignedIntegerType_32(self.page_count)
        }

def _init_Request_class_map():
    classes = [
        UpdateUserProfile, GetDomains, SaveDomain, UpdateDomain,
        ChangeDomainStatus, GetCountriesForUser, GetCountries, SaveCountry, UpdateCountry,
        ChangeCountryStatus, GetNotifications, UpdateNotificationStatus,
        GetAuditTrails
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
    def __init__(self, contact_no, address):
        self.contact_no = contact_no
        self.address = address

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["contact_no", "address"])
        contact_no = data.get("contact_no")
        contact_no = parse_structure_CustomTextType_20(contact_no)
        address = data.get("address")
        address = parse_structure_CustomTextType_250(address)
        return UpdateUserProfile(contact_no, address)

    def to_inner_structure(self):
        return {
            "contact_no": to_structure_CustomTextType_20(self.contact_no),
            "address": to_structure_CustomTextType_250(self.address),
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
    def __init__(self, domains):
        self.domains = domains

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domains"])
        domains = data.get("domains")
        domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        return GetDomainsSuccess(domains)

    def to_inner_structure(self):
        return {
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
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
    def parse_structure(data):
        data = parse_dictionary(data, ["countries"])
        countries = data.get("countries")
        return GetCountriesSuccess(countries)

    def to_structure(self):
        data = {
            "countries": self.countries
        }
        return to_dictionary_values(data, "GetCountriesSuccess")


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
        notifications = parse_structure_VectorType_RecordType_general_Notification(notifications)
        return GetNotificationsSuccess(notifications)

    def to_inner_structure(self):
        return {
            "notifications": to_structure_VectorType_RecordType_general_Notification(self.notifications),
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

class GetAuditTrailSuccess(Response):
    def __init__(self, audit_trails, users, forms, total_records):
        self.audit_trails = audit_trails
        self.users = users
        self.forms = forms
        self.total_records = total_records

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["audit_trails", "users", "forms", "total_records"])
        audit_trails = data.get("audit_trails")
        audit_trails = parse_structure_VectorType_RecordType_general_AuditTrail(audit_trails)
        users = data.get("users")
        users = parse_structure_VectorType_RecordType_general_User(users)
        forms = data.get("forms")
        forms = parse_structure_VectorType_RecordType_general_AuditTrailForm(forms)
        total_records = data.get("total_records")
        total_records = parse_structure_UnsignedIntegerType_32(total_records)
        return GetAuditTrailSuccess(audit_trails, users, forms, total_records)

    def to_inner_structure(self):
        return {
            "audit_trail_details": to_structure_VectorType_RecordType_general_AuditTrail(self.audit_trails),
            "users": to_structure_VectorType_RecordType_general_User(self.users),
            "forms": to_structure_VectorType_RecordType_general_AuditTrailForm(self.forms),
            "total_records": to_structure_UnsignedIntegerType_32(self.total_records)
        }

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
        job_id = parse_structure_UnsignedIntegerType_32(job_id)
        return TransactionJobId(job_id)

    def to_inner_structure(self):
        return {
            "job_id": to_structure_UnsignedIntegerType_32(self.job_id)
        }

class FileUploadSuccess(Response):
    def __init__(self, file_list):
        self.file_list = file_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["file_list"])
        file_list = data.get("file_list")
        file_list = parse_structure_VectorType_RecordType_core_FileLst(file_list)
        return FileUploadSuccess(file_list)

    def to_inner_structure(self):
        return {
            "file_list": to_structure_VectorType_RecordType_core_FileLst(self.file_list)
        }

def _init_Response_class_map():
    classes = [
        UpdateUserProfileSuccess, ContactNumberAlreadyExists,
        GetDomainsSuccess, SaveDomainSuccess, DomainNameAlreadyExists,
        UpdateDomainSuccess, InvalidDomainId, ChangeDomainStatusSuccess,
        GetNotificationsSuccess, UpdateNotificationStatusSuccess, GetAuditTrailSuccess,
        MasterDataNotAvailableForClient, TransactionExists, TransactionJobId,
        FileUploadSuccess
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
        notification_id = parse_structure_UnsignedIntegerType_32(notification_id)
        notification_text = data.get("notification_text")
        notification_text = parse_structure_Text(notification_text)
        link = data.get("link")
        link = parse_structure_CustomTextType_500(link)
        has_read = data.get("has_read")
        has_read = parse_structure_Bool(has_read)
        date_and_time = data.get("date_and_time")
        date_and_time = parse_structure_CustomTextType_20(date_and_time)
        return Notification(notification_id, notification_text, link, has_read, date_and_time)

    def to_structure(self):
        return {
            "notification_id": to_structure_UnsignedIntegerType_32(self.notification_id),
            "notification_text": to_structure_Text(self.notification_text),
            "link": to_structure_CustomTextType_500(self.link),
            "has_read": to_structure_Bool(self.has_read),
            "date_and_time": to_structure_CustomTextType_20(self.date_and_time),
        }

#
# Audit Trail
#
class AuditTrail(object):
    def __init__(self, user_id, form_id, action, date):
        self.user_id = user_id
        self.form_id = form_id
        self.action = action
        self.date = date

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "form_id", "action", "date"])
        user_id = data.get("user_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        form_id = data.get("form_id")
        form_id = parse_structure_UnsignedIntegerType_32(form_id)
        action = data.get("action")
        action = parse_structure_CustomTextType_500(action)
        date = data.get("date")
        date = parse_structure_CustomTextType_20(date)
        return AuditTrail(user_id, form_id, action, date)

    def to_structure(self):
        return {
            "user_id": to_structure_UnsignedIntegerType_32(self.user_id),
            "form_id": to_structure_UnsignedIntegerType_32(self.form_id),
            "action": to_structure_CustomTextType_500(self.action),
            "date": to_structure_CustomTextType_20(self.date)
        }

class AuditTrailForm(object):
    def __init__(self, form_id, form_name):

        self.form_id = form_id
        self.form_name = form_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["form_id", "form_name"])
        form_id = data.get("form_id")
        form_id = parse_structure_UnsignedIntegerType_32(form_id)
        form_name = data.get("form_name")
        form_name = parse_structure_CustomTextType_50(form_name)
        return AuditTrailForm(form_id, form_name)

    def to_structure(self):
        return {
            "form_id": to_structure_SignedIntegerType_8(self.form_id),
            "form_name": to_structure_CustomTextType_50(self.form_name)
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
        session_token = parse_structure_CustomTextType_50(session_token)
        request = data.get("request")
        request = parse_structure_VariantType_general_Request(request)
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": to_structure_CustomTextType_50(self.session_token),
            "request": to_structure_VariantType_general_Request(self.request),
        }
