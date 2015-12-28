import json
from protocol.jsonvalidators import (parse_enum, parse_dictionary, parse_static_list)
from protocol.parse_structure import (
    parse_structure_Float,
    parse_structure_VectorType_RecordType_general_Notification,
    parse_structure_CustomTextType_250,
    parse_structure_VectorType_RecordType_core_Domain,
    parse_structure_SignedIntegerType_8, parse_structure_Bool,
    parse_structure_CustomTextType_20, parse_structure_CustomTextType_500,
    parse_structure_CustomTextType_50
)
from protocol.to_structure import (
    to_structure_Float,
    to_structure_VectorType_RecordType_general_Notification,
    to_structure_CustomTextType_250,
    to_structure_VectorType_RecordType_core_Domain,
    to_structure_SignedIntegerType_8, to_structure_Bool,
    to_structure_CustomTextType_20, to_structure_CustomTextType_500,
    to_structure_CustomTextType_50
)

#
# Request
#

class Request(object):
    def to_structure(self):
        name = type(self).__name__
        inner = self.to_inner_structure()
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
        data = parse_dictionary(data, ["domain_name"])
        domain_name = data.get("domain_name")
        domain_name = parse_structure_CustomTextType_50(domain_name)
        return SaveDomain(domain_name)

    def to_inner_structure(self):
        return {
            "domain_name": to_structure_CustomTextType_50(self.domain_name),
        }

class UpdateDomain(Request):
    def __init__(self, domain_id, domain_name):
        self.domain_id = domain_id
        self.domain_name = domain_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domain_id", "domain_name"])
        domain_id = data.get("domain_id")
        domain_id = parse_structure_SignedIntegerType_8(domain_id)
        domain_name = data.get("domain_name")
        domain_name = parse_structure_CustomTextType_50(domain_name)
        return UpdateDomain(domain_id, domain_name)

    def to_inner_structure(self):
        return {
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "domain_name": to_structure_CustomTextType_50(self.domain_name),
        }

class ChangeDomainStatus(Request):
    def __init__(self, domain_id, is_active):
        self.domain_id = domain_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domain_id", "is_active"])
        domain_id = data.get("domain_id")
        domain_id = parse_structure_SignedIntegerType_8(domain_id)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return ChangeDomainStatus(domain_id, is_active)

    def to_inner_structure(self):
        return {
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "is_active": to_structure_Bool(self.is_active),
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
        data = parse_dictionary(data, ["country_name"])
        country_name = data.get("country_name")
        country_name = parse_structure_CustomTextType_50(country_name)
        return SaveCountry(country_name)

    def to_inner_structure(self):
        return {
            "country_name": to_structure_CustomTextType_50(self.country_name),
        }

class UpdateCountry(Request):
    def __init__(self, country_id, country_name):
        self.country_id = country_id
        self.country_name = country_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "country_name"])
        country_id = data.get("country_id")
        country_id = parse_structure_SignedIntegerType_8(country_id)
        country_name = data.get("country_name")
        country_name = parse_structure_CustomTextType_50(country_name)
        return UpdateCountry(country_id, country_name)

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "country_name": to_structure_CustomTextType_50(self.country_name),
        }

class ChangeCountryStatus(Request):
    def __init__(self, country_id, is_active):
        self.country_id = country_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "is_active"])
        country_id = data.get("country_id")
        country_id = parse_structure_SignedIntegerType_8(country_id)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return ChangeCountryStatus(country_id, is_active)

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "is_active": to_structure_Bool(self.is_active),
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
        notification_id = parse_structure_SignedIntegerType_8(notification_id)
        has_read = data.get("has_read")
        has_read = parse_structure_Bool(has_read)
        return UpdateNotificationStatus(notification_id, has_read)

    def to_inner_structure(self):
        return {
            "notification_id": to_structure_SignedIntegerType_8(self.notification_id),
            "has_read": to_structure_Bool(self.has_read),
        }


def _init_Request_class_map():
    classes = [UpdateUserProfile, GetDomains, SaveDomain, UpdateDomain, ChangeDomainStatus, GetCountries, SaveCountry, UpdateCountry, ChangeCountryStatus, GetNotifications, UpdateNotificationStatus]
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
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateUserProfileSuccess()

    def to_inner_structure(self):
        return {
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


def _init_Response_class_map():
    classes = [UpdateUserProfileSuccess, ContactNumberAlreadyExists, GetDomainsSuccess, SaveDomainSuccess, DomainNameAlreadyExists, UpdateDomainSuccess, InvalidDomainId, ChangeDomainStatusSuccess, GetNotificationsSuccess, UpdateNotificationStatusSuccess]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()

#
# Notification
#

class Notification(object):
    def __init__(self, notification_id, notification_text, extra_details, has_read, date_and_time):
        self.notification_id = notification_id
        self.notification_text = notification_text
        self.extra_details = extra_details
        self.has_read = has_read
        self.date_and_time = date_and_time

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["notification_id", "notification_text", "extra_details", "has_read", "date_and_time"])
        notification_id = data.get("notification_id")
        notification_id = parse_structure_SignedIntegerType_8(notification_id)
        notification_text = data.get("notification_text")
        notification_text = parse_structure_CustomTextType_500(notification_text)
        extra_details = data.get("extra_details")
        extra_details = parse_structure_CustomTextType_500(extra_details)
        has_read = data.get("has_read")
        has_read = parse_structure_Bool(has_read)
        date_and_time = data.get("date_and_time")
        date_and_time = parse_structure_Float(date_and_time)
        return Notification(notification_id, notification_text, extra_details, has_read, date_and_time)

    def to_structure(self):
        return {
            "notification_id": to_structure_SignedIntegerType_8(self.notification_id),
            "notification_text": to_structure_CustomTextType_500(self.notification_text),
            "extra_details": to_structure_CustomTextType_500(self.extra_details),
            "has_read": to_structure_Bool(self.has_read),
            "date_and_time": to_structure_Float(self.date_and_time),
        }

