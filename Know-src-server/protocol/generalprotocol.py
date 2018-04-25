from protocol.jsonvalidators import (
    parse_dictionary, parse_static_list,
    to_structure_dictionary_values, parse_VariantType,
    to_VariantType
)
from protocol.parse_structure import (
    parse_structure_EnumType_core_DURATION_TYPE,
    parse_structure_EnumType_core_REPEATS_TYPE,
    parse_structure_EnumType_core_COMPLIANCE_FREQUENCY,
    parse_structure_MapType_CustomTextType_50_VectorType_CustomTextType_50,
    parse_structure_EnumType_core_APPROVAL_STATUS

)
from protocol.to_structure import (
    to_structure_EnumType_core_DURATION_TYPE,
    to_structure_EnumType_core_REPEATS_TYPE,
    to_structure_EnumType_core_COMPLIANCE_FREQUENCY,
    to_structure_MapType_CustomTextType_50_VectorType_CustomTextType_50,
    to_structure_EnumType_core_APPROVAL_STATUS
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
        return UpdateStatutoryNotificationStatus(notification_id, user_id, has_read)

    def to_inner_structure(self):
        return {
            "notification_id": self.notification_id,
            "user_id": self.user_id,
            "has_read": self.has_read,
        }

class UpdateMessageStatus(Request):
    def __init__(self, message_id, has_read):
        self.message_id = message_id
        self.has_read = has_read

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["message_id", "has_read"])
        message_id = data.get("message_id")
        has_read = data.get("has_read")
        return UpdateMessageStatus(message_id, has_read)

    def to_inner_structure(self):
        return {
            "message_id": self.message_id,
            "has_read": self.has_read,
        }

class GetAuditTrails(Request):
    def __init__(
        self, from_date, to_date, user_id_search, form_id_search, category_id,
        client_id, legal_entity_id, unit_id, record_count, page_count
    ):
        self.from_date = from_date
        self.to_date = to_date
        self.user_id_search = user_id_search
        self.form_id_search = form_id_search
        self.category_id = category_id
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.unit_id = unit_id
        self.record_count = record_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "from_date", "to_date", "user_id_search", "form_id_search", "category_id",
            "client_id", "legal_entity_id", "unit_id", "record_count", "page_count"
        ])
        from_date = data.get("from_date")
        to_date = data.get("to_date")
        user_id_search = data.get("user_id_search")
        form_id_search = data.get("form_id_search")
        category_id = data.get("category_id")
        client_id = data.get("client_id")
        legal_entity_id = data.get("legal_entity_id")
        unit_id = data.get("unit_id")
        record_count = data.get("record_count")
        page_count = data.get("page_count")
        return GetAuditTrails(
            from_date, to_date,
            user_id_search, form_id_search,
            category_id, client_id, legal_entity_id,
            unit_id, record_count, page_count
        )

    def to_inner_structure(self):
        return {
            "from_date": self.from_date,
            "to_date": self.to_date,
            "user_id_search": self.user_id_search,
            "form_id_search": self.form_id_search,
            "category_id": self.category_id,
            "client_id": self.client_id,
            "legal_entity_id": self.legal_entity_id,
            "unit_id": self.unit_id,
            "record_count": self.record_count,
            "page_count": self.page_count
        }

class ExportAuditTrails(Request):
    def __init__(
        self, from_date, to_date, user_id_search, form_id_search, category_id,
        client_id, legal_entity_id, unit_id, csv
    ):
        self.from_date = from_date
        self.to_date = to_date
        self.user_id_search = user_id_search
        self.form_id_search = form_id_search
        self.category_id = category_id
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.unit_id = unit_id
        self.csv = csv

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "from_date", "to_date", "user_id_search", "form_id_search", "category_id",
            "client_id", "legal_entity_id", "unit_id", "csv"
        ])
        from_date = data.get("from_date")
        to_date = data.get("to_date")
        user_id_search = data.get("user_id_search")
        form_id_search = data.get("form_id_search")
        category_id = data.get("category_id")
        client_id = data.get("client_id")
        legal_entity_id = data.get("legal_entity_id")
        unit_id = data.get("unit_id")
        csv = data.get("csv")
        return ExportAuditTrails(
            from_date, to_date,
            user_id_search, form_id_search,
            category_id, client_id, legal_entity_id,
            unit_id, csv
        )

    def to_inner_structure(self):
        return {
            "from_date": self.from_date,
            "to_date": self.to_date,
            "user_id_search": self.user_id_search,
            "form_id_search": self.form_id_search,
            "category_id": self.category_id,
            "client_id": self.client_id,
            "legal_entity_id": self.legal_entity_id,
            "unit_id": self.unit_id,
            "csv": self.csv
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

class GetClientAuditTrailsFilter(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetClientAuditTrailsFilter()

    def to_inner_structure(self):
        return {
        }

class GetClientAuditTrails(Request):
    def __init__(
        self, from_date, to_date, user_id_search, form_id_search,
        client_id, legal_entity_id, record_count, page_count
    ):
        self.from_date = from_date
        self.to_date = to_date
        self.user_id_search = user_id_search
        self.form_id_search = form_id_search
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.record_count = record_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "from_date", "to_date", "user_id_search", "form_id_search",
            "client_id", "legal_entity_id", "record_count", "page_count"
        ])
        from_date = data.get("from_date")
        to_date = data.get("to_date")
        user_id_search = data.get("user_id_search")
        form_id_search = data.get("form_id_search")
        client_id = data.get("client_id")
        legal_entity_id = data.get("legal_entity_id")
        record_count = data.get("record_count")
        page_count = data.get("page_count")
        return GetClientAuditTrails(
            from_date, to_date,
            user_id_search, form_id_search,
            client_id, legal_entity_id,
            record_count, page_count
        )

    def to_inner_structure(self):
        return {
            "from_date": self.from_date,
            "to_date": self.to_date,
            "user_id_search": self.user_id_search,
            "form_id_search": self.form_id_search,
            "client_id": self.client_id,
            "legal_entity_id": self.legal_entity_id,
            "record_count": self.record_count,
            "page_count": self.page_count
        }

class ExportClientAuditTrails(Request):
    def __init__(
        self, from_date, to_date, user_id_search, form_id_search,
        client_id, legal_entity_id, csv
    ):
        self.from_date = from_date
        self.to_date = to_date
        self.user_id_search = user_id_search
        self.form_id_search = form_id_search
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.csv = csv

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "from_date", "to_date", "user_id_search", "form_id_search",
            "client_id", "legal_entity_id", "csv"
        ])
        from_date = data.get("from_date")
        to_date = data.get("to_date")
        user_id_search = data.get("user_id_search")
        form_id_search = data.get("form_id_search")
        client_id = data.get("client_id")
        legal_entity_id = data.get("legal_entity_id")
        csv = data.get("csv")
        return ExportClientAuditTrails(
            from_date, to_date,
            user_id_search, form_id_search,
            client_id, legal_entity_id,
            csv
        )

    def to_inner_structure(self):
        return {
            "from_date": self.from_date,
            "to_date": self.to_date,
            "user_id_search": self.user_id_search,
            "form_id_search": self.form_id_search,
            "client_id": self.client_id,
            "legal_entity_id": self.legal_entity_id,
            "csv": self.csv
        }

class GetClientLoginTraceFilter(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetClientLoginTraceFilter()

    def to_inner_structure(self):
        return {
        }

class GetClientLoginTrace(Request):
    def __init__(
        self, from_date, to_date, user_id_search,
        client_id, record_count, page_count
    ):
        self.from_date = from_date
        self.to_date = to_date
        self.user_id_search = user_id_search
        self.client_id = client_id
        self.record_count = record_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "from_date", "to_date", "user_id_search",
            "client_id", "record_count", "page_count"
        ])
        from_date = data.get("from_date")
        to_date = data.get("to_date")
        user_id_search = data.get("user_id_search")
        client_id = data.get("client_id")
        record_count = data.get("record_count")
        page_count = data.get("page_count")
        return GetClientLoginTrace(
            from_date, to_date,
            user_id_search, client_id,
            record_count, page_count
        )

    def to_inner_structure(self):
        return {
            "from_date": self.from_date,
            "to_date": self.to_date,
            "user_id_search": self.user_id_search,
            "client_id": self.client_id,
            "record_count": self.record_count,
            "page_count": self.page_count
        }

class ExportClientLoginTrace(Request):
    def __init__(
        self, from_date, to_date, user_id_search,
        client_id, csv
    ):
        self.from_date = from_date
        self.to_date = to_date
        self.user_id_search = user_id_search
        self.client_id = client_id
        self.csv = csv

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "from_date", "to_date", "user_id_search", "client_id", "csv"
        ])
        from_date = data.get("from_date")
        to_date = data.get("to_date")
        user_id_search = data.get("user_id_search")
        client_id = data.get("client_id")
        csv = data.get("csv")
        return ExportClientLoginTrace(
            from_date, to_date,
            user_id_search, client_id,
            csv
        )

    def to_inner_structure(self):
        return {
            "from_date": self.from_date,
            "to_date": self.to_date,
            "user_id_search": self.user_id_search,
            "client_id": self.client_id,
            "csv": self.csv
        }

class GetKExecutiveDetails(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetKExecutiveDetails()

    def to_inner_structure(self):
        return {
        }

class GetTechnoUserDetails(Request):
    def __init__(self, user_type):
        self.user_type = user_type

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_type"])
        user_type = data.get("user_type")
        return GetTechnoUserDetails(user_type)

    def to_inner_structure(self):
        return {
            "user_type": self.user_type
        }


def _init_Request_class_map():
    classes = [
        UpdateUserProfile, GetDomains, SaveDomain, UpdateDomain,
        ChangeDomainStatus, GetCountriesForUser, GetCountries, SaveCountry, UpdateCountry,
        ChangeCountryStatus, GetNotifications, UpdateNotificationStatus,
        GetAuditTrails, VerifyPassword, GetMessages, GetStatutoryNotifications, UpdateStatutoryNotificationStatus,
        GetAuditTrailsFilter, ExportAuditTrails, UpdateMessageStatus, GetClientAuditTrailsFilter,
        GetClientAuditTrails, GetClientLoginTraceFilter, GetClientLoginTrace, ExportClientLoginTrace,
        ExportClientAuditTrails, GetKExecutiveDetails, GetTechnoUserDetails
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
    def __init__(self, m_count, s_count):
        self.m_count = m_count
        self.s_count = s_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["m_count", "s_count"])
        m_count = data.get("m_count")
        s_count = data.get("s_count")
        return UpdateStatutoryNotificationStatusSuccess(m_count, s_count)

    def to_inner_structure(self):
        return {
            "m_count": self.m_count,
            "s_count": self.s_count
        }

class UpdateMessageStatusSuccess(Response):
    def __init__(self, m_count, s_count):
        self.m_count = m_count
        self.s_count = s_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["m_count", "s_count"])
        m_count = data.get("m_count")
        s_count = data.get("s_count")
        return UpdateMessageStatusSuccess(m_count, s_count)

    def to_inner_structure(self):
        return {
            "m_count": self.m_count,
            "s_count": self.s_count
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
    def __init__(
        self, user_categories, audit_trail_countries, forms_list, users,
        audit_trail_details
    ):
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

        return GetAuditTrailFilterSuccess(
            user_categories, audit_trail_countries, forms_list, users, audit_trail_details
        )

    def to_inner_structure(self):
        data = {
            "user_categories": self.user_categories,
            "audit_trail_countries": self.audit_trail_countries,
            "forms_list": self.forms_list,
            "users": self.users,
            "audit_trail_details": self.audit_trail_details,
        }
        return data

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

class ExportToCSVSuccess(Response):
    def __init__(self, link):
        self.link = link

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["link"])
        link = data.get("link")
        return ExportToCSVSuccess(link)

    def to_inner_structure(self):
        return {
            "link" : self.link
        }

class GetClientAuditTrailFilterSuccess(Response):
    def __init__(
        self, clients, unit_legal_entity, audit_client_users, client_audit_details,
    ):
        self.clients = clients
        self.unit_legal_entity = unit_legal_entity
        self.audit_client_users = audit_client_users
        self.client_audit_details = client_audit_details

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
                "clients", "unit_legal_entity", "audit_client_users", "client_audit_details"
            ])
        clients = data.get("clients")
        unit_legal_entity = data.get("unit_legal_entity")
        audit_client_users = data.get("audit_client_users")
        client_audit_details = data.get("client_audit_details")

        return GetClientAuditTrailFilterSuccess(
            clients, unit_legal_entity, audit_client_users, client_audit_details
        )

    def to_inner_structure(self):
        data = {
            "clients": self.clients,
            "unit_legal_entity": self.unit_legal_entity,
            "audit_client_users": self.audit_client_users,
            "client_audit_details": self.client_audit_details,
        }
        return data

class GetClientAuditTrailSuccess(Response):
    def __init__(self, client_audit_trail_details, total_records):
        self.client_audit_trail_details = client_audit_trail_details
        self.total_records = total_records

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
                "client_audit_trail_details", "total_records"
            ])
        client_audit_trail_details = data.get("client_audit_trail_details")
        total_records = data.get("total_records")
        return GetClientAuditTrailSuccess(client_audit_trail_details, total_records)

    def to_inner_structure(self):
        return {
            "client_audit_trail_details": self.client_audit_trail_details,
            "total_records": self.total_records,
        }

class GetClientLoginTraceFilterSuccess(Response):
    def __init__(
        self, clients, audit_client_users
    ):
        self.clients = clients
        self.audit_client_users = audit_client_users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
                "clients", "audit_client_users"
            ])
        clients = data.get("clients")
        audit_client_users = data.get("audit_client_users")

        return GetClientLoginTraceFilterSuccess(
            clients, audit_client_users
        )

    def to_inner_structure(self):
        data = {
            "clients": self.clients,
            "audit_client_users": self.audit_client_users,
        }
        return data

class GetClientLoginTraceSuccess(Response):
    def __init__(self, client_login_trace_details, total_records):
        self.client_login_trace_details = client_login_trace_details
        self.total_records = total_records

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
                "client_login_trace_details", "total_records"
            ])
        client_login_trace_details = data.get("client_login_trace_details")
        total_records = data.get("total_records")
        return GetClientLoginTraceSuccess(client_login_trace_details, total_records)

    def to_inner_structure(self):
        return {
            "client_login_trace_details": self.client_login_trace_details,
            "total_records": self.total_records,
        }

class DatabaseConnectionFailure(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return DatabaseConnectionFailure()

    def to_inner_structure(self):
        return {
        }


class GetKExecutiveDetailsSuccess(Response):
    def __init__(self, k_executive_info):
        self.k_executive_info = k_executive_info

    @staticmethod
    def parse_inner_strucure(data):
        data = parse_dictionary(data, ["k_executive_info"])
        return GetKExecutiveDetailsSuccess(
            data.get("k_executive_info")
        )

    def to_inner_structure(self):
        return {
            "k_executive_info": self.k_executive_info
        }

class GetTechnoDetailsSuccess(Response):
    def __init__(self, techno_info):
        self.techno_info = techno_info

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["techno_info"])
        return GetTechnoDetailsSuccess(
            data.get("techno_info")
        )

    def to_inner_structure(self):
        return {
            "techno_info": self.techno_info
        }


def _init_Response_class_map():
    classes = [
        UpdateUserProfileSuccess,
        GetDomainsSuccess, SaveDomainSuccess, DomainNameAlreadyExists,
        UpdateDomainSuccess, InvalidDomainId, ChangeDomainStatusSuccess,
        GetNotificationsSuccess, UpdateNotificationStatusSuccess, GetAuditTrailSuccess,
        FileUploadSuccess, VerifyPasswordSuccess, InvalidPassword, GetMessagesSuccess,
        GetStatutoryNotificationsSuccess, UpdateStatutoryNotificationStatusSuccess,
        ExportToCSVSuccess, UpdateMessageStatusSuccess, GetClientAuditTrailSuccess,
        GetClientLoginTraceFilterSuccess, GetClientLoginTraceSuccess,
        DatabaseConnectionFailure,
        GetKExecutiveDetailsSuccess, GetTechnoDetailsSuccess
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


#
# Audit Trail -  Countries
#
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
# ComplianceFrequency
#

class ComplianceFrequency(object):
    def __init__(self, frequency_id, frequency):
        self.frequency_id = frequency_id
        self.frequency = frequency

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["frequency_id", "frequency"])
        frequency_id = data.get("frequency_id")
        frequency = data.get("frequency")
        frequency = parse_structure_EnumType_core_COMPLIANCE_FREQUENCY(frequency)
        return ComplianceFrequency(frequency_id, frequency)

    def to_structure(self):
        data = {
            "frequency_id": self.frequency_id,
            "frequency": to_structure_EnumType_core_COMPLIANCE_FREQUENCY(self.frequency),
        }
        return to_structure_dictionary_values(data)

#
# ComplianceRepeatType
#

class ComplianceRepeatType(object):
    def __init__(self, repeat_type_id, repeat_type):
        self.repeat_type_id = repeat_type_id
        self.repeat_type = repeat_type

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["repeat_type_id", "repeat_type"])
        repeat_type = data.get("repeat_type")
        repeat_type = parse_structure_EnumType_core_REPEATS_TYPE(repeat_type)
        return ComplianceRepeatType(data.get("repeat_type_id"), repeat_type)

    def to_structure(self):
        return {
            "repeat_type_id": self.repeat_type_id,
            "repeat_type": to_structure_EnumType_core_REPEATS_TYPE(self.repeat_type),
        }

#
# ComplianceDurationType
#

class ComplianceDurationType(object):
    def __init__(self, duration_type_id, duration_type):
        self.duration_type_id = duration_type_id
        self.duration_type = duration_type

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["duration_type_id", "duration_type"])
        duration_type = data.get("duration_type")
        duration_type = parse_structure_EnumType_core_DURATION_TYPE(duration_type)
        return ComplianceDurationType(data.get("duration_type_id"), duration_type)

    def to_structure(self):
        return {
            "duration_type_id": self.duration_type_id,
            "duration_type": to_structure_EnumType_core_DURATION_TYPE(self.duration_type),
        }


#
# Entity Domain Details
#
class EntityDomainDetails(object):
    def __init__(
        self, domain_id, organization, activation_date, is_delete
    ):
        self.domain_id = domain_id
        self.organization = organization
        self.activation_date = activation_date
        self.is_delete = is_delete

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["d_id", "org", "activation_date", "is_delete"])
        organization = data.get("org")
        organization = parse_structure_MapType_CustomTextType_50_VectorType_CustomTextType_50(organization)
        return EntityDomainDetails(
            data.get("d_id"), organization, data.get("activation_date"), data.get("is_delete")
        )

    def to_structure(self):
        return {
            "d_id": self.domain_id,
            "org": to_structure_MapType_CustomTextType_50_VectorType_CustomTextType_50(
                    self.organization
                ),
            "activation_date": self.activation_date,
            "is_delete": self.is_delete
        }

class AssignLegalEntity(object):
    def __init__(
        self, client_id, country_name,
        group_name, no_of_legal_entities, no_of_assigned_legal_entities
    ):
        self.client_id = client_id
        self.country_name = country_name
        self.group_name = group_name
        self.no_of_legal_entities = no_of_legal_entities
        self.no_of_assigned_legal_entities = no_of_assigned_legal_entities

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "client_id", "country_names", "group_name"
                "no_of_legal_entities", "no_of_assigned_legal_entities"
            ]
        )
        return AssignLegalEntity(
            data.get("client_id"), data.get("country_names"), data.get("group_name"),
            data.get("no_of_legal_entities"), data.get("no_of_assigned_legal_entities")
        )

    def to_structure(self):
        return {
            "client_id": self.client_id,
            "country_names": self.country_name,
            "group_name": self.group_name,
            "no_of_legal_entities": self.no_of_legal_entities,
            "no_of_assigned_legal_entities": self.no_of_assigned_legal_entities
        }


class UnAssignLegalEntity(object):
    def __init__(
        self, legal_entity_id, legal_entity_name,
        business_group_name, c_name, c_id, domain_ids
    ):
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.business_group_name = business_group_name
        self.c_name = c_name
        self.c_id = c_id
        self.domain_ids = domain_ids

    @staticmethod
    def parse_structure(data):
        d = parse_dictionary(
            data, [
                "legal_entity_id", "legal_entity_name", "business_group_name",
                "c_name", "c_id", "domain_ids"
            ]
        )
        return UnAssignLegalEntity(
            d.get("legal_entity_id"), d.get("legal_entity_name"), d.get("business_group_name"),
            d.get("c_name"), d.get("c_id"), d.get("domain_ids")
        )

    def to_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id, "legal_entity_name": self.legal_entity_name,
            "business_group_name": self.business_group_name, "c_name": self.c_name,
            "c_id": self.c_id, "domain_ids": self.domain_ids
        }


class AssignedLegalEntity(object):
    def __init__(
        self, legal_entity_id, legal_entity_name,
        business_group_name, c_name, c_id, employee_name
    ):
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.business_group_name = business_group_name
        self.c_name = c_name
        self.c_id = c_id
        self.employee_name = employee_name

    @staticmethod
    def parse_structure(data):
        d = parse_dictionary(
            data, [
                "legal_entity_id", "legal_entity_name", "business_group_name",
                "c_name", "c_id", "employee_name"
            ]
        )
        return UnAssignLegalEntity(
            d.get("legal_entity_id"), d.get("legal_entity_name"), d.get("business_group_name"),
            d.get("c_name"), d.get("c_id"), d.get("employee_name")
        )

    def to_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id, "legal_entity_name": self.legal_entity_name,
            "business_group_name": self.business_group_name, "c_name": self.c_name,
            "c_id": self.c_id, "employee_name": self.employee_name
        }
#
# FormCategory
#

class FormCategory(object):
    def __init__(self, form_category_id, form_category):
        self.form_category_id = form_category_id
        self.form_category = form_category

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["form_category_id", "form_category"])
        return FormCategory(
            data.get("form_category_id"), data.get("form_category")
        )

    def to_structure(self):
        return {
            "form_category_id": self.form_category_id,
            "form_category": self.form_category,
        }
#
#  Form
#
class Form(object):
    def __init__(self, form_id, form_name, form_url, parent_menu, form_type):

        self.form_id = form_id
        self.form_name = form_name
        self.form_url = form_url
        self.parent_menu = parent_menu
        self.form_type = form_type

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "form_id", "form_name", "form_url", "parent_menu", "form_type"
        ])
        return Form(
            data.get("form_id"), data.get("form_name"), data.get("form_url"),
            data.get("parent_menu"), data.get("form_type")
        )

    def to_structure(self):
        data = {
            "form_id": self.form_id, "form_name": self.form_name, "form_url": self.form_url,
            "parent_menu": self.parent_menu, "form_type": self.form_type
        }
        return to_structure_dictionary_values(data)
#
# Menu
#
class Menu(object):
    def __init__(self, menus):
        self.menus = menus

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["menus"])
        menus = data.get("menus")
        return Menu(menus)

    def to_structure(self):
        return {
            "menus": self.menus,
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
        request = parse_VariantType(
            request, "generalprotocol", "Request"
        )
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": to_VariantType(
                self.request, "geleralprotocol", "Response"
            )
        }

#
# StatutoryApprovalAtatus
#
class StatutoryApprovalStatus(object):
    def __init__(self, approval_status_id, approval_status):
        self.approval_status_id = approval_status_id
        self.approval_status = approval_status

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["approval_status_id", "comp_approval_status"])
        approval_status_id = data.get("approval_status_id")
        approval_status = parse_structure_EnumType_core_APPROVAL_STATUS(data.get("comp_approval_status"))
        return StatutoryApprovalStatus(approval_status_id, approval_status)

    def to_structure(self):
        return {
            "approval_status_id": self.approval_status_id,
            "comp_approval_status": to_structure_EnumType_core_APPROVAL_STATUS(self.approval_status),
        }

#
# Client Audit Trail Forms
#

class ClientAuditTrail(object):
    def __init__(self, user_id, form_id, action, created_on, user_category_name, user_name):
        self.user_id = user_id
        self.form_id = form_id
        self.action = action
        self.created_on = created_on
        self.user_category_name = user_category_name
        self.user_name = user_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id", "form_id", "action," "created_on", "user_category_name", "user_name",
        ])
        user_id = data.get("user_id")
        form_id = data.get("form_id")
        action = data.get("action")
        created_on = data.get("created_on")
        user_category_name = data.get("user_category_name")
        user_name = data.get("user_name")

        return ClientAuditTrail(user_id, form_id, action, created_on, user_category_name, user_name)

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "form_id": self.form_id,
            "action": self.action,
            "created_on": self.created_on,
            "user_category_name": self.user_category_name,
            "user_name": self.user_name,
        }

class KExecutiveInfo(object):
    def __init__(self, c_ids, d_ids, emp_code_name, user_id):
        self.c_ids = c_ids
        self.d_ids = d_ids
        self.emp_code_name = emp_code_name
        self.user_id = user_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "c_ids", "d_ids", "emp_code_name",
            "user_id"
        ])
        return KExecutiveInfo(
            data.get("c_ids"), data.get("d_ids"),
            data.get("emp_code_name"),
            data.get("user_id")
        )

    def to_structure(self):
        return {
            "c_ids": self.c_ids,
            "d_ids": self.d_ids,
            "emp_code_name": self.emp_code_name,
            "user_id": self.user_id
        }

class TechnoInfo(object):
    def __init__(self, group_id, user_id, emp_code_name):
        self.group_id = group_id
        self.user_id = user_id
        self.emp_code_name = emp_code_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data , [
            "group_id", "user_id", "emp_code_name"
        ])
        return TechnoInfo(
            data.get("group_id"), data.get("user_id"),
            data.get("emp_code_name")
        )

    def to_structure(self):
        return {
            "group_id": self.group_id,
            "user_id": self.user_id,
            "emp_code_name": self.emp_code_name
        }
