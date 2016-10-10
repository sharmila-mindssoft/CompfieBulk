from protocol.jsonvalidators import (
    parse_dictionary, parse_static_list, parse_VariantType,
    to_VariantType, to_structure_dictionary_values
)
from protocol.parse_structure import (
    parse_structure_MapType_UnsignedInteger_32_VectorType_UnsignedInteger_32
)
from protocol.to_structure import (
    to_structure_MapType_UnsignedInteger_32_VectorType_UnsignedInteger_32
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


class GetUserGroups(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetUserGroups()

    def to_inner_structure(self):
        return {
        }


class SaveUserGroup(Request):
    def __init__(self, user_group_name, form_category_id, form_ids):
        self.user_group_name = user_group_name
        self.form_category_id = form_category_id
        self.form_ids = form_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["ug_name", "fc_id", "f_ids"])
        user_group_name = data.get("ug_name")
        form_category_id = data.get("fc_id")
        form_ids = data.get("f_ids")
        return SaveUserGroup(user_group_name, form_category_id, form_ids)

    def to_inner_structure(self):
        return {
            "ug_name": self.user_group_name,
            "fc_id": self.form_category_id,
            "f_ids": self.form_ids
        }


class UpdateUserGroup(Request):
    def __init__(
        self, user_group_id, user_group_name, form_category_id, form_ids
    ):
        self.user_group_id = user_group_id
        self.user_group_name = user_group_name
        self.form_category_id = form_category_id
        self.form_ids = form_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["ug_id", "ug_name", "fc_id", "f_ids"])
        user_group_id = data.get("ug_id")
        user_group_name = data.get("ug_name")
        form_category_id = data.get("fc_id")
        form_ids = data.get("f_ids")
        return UpdateUserGroup(
            user_group_id, user_group_name, form_category_id, form_ids)

    def to_inner_structure(self):
        return {
            "ug_id": self.user_group_id,
            "ug_name": self.user_group_name,
            "fc_id": self.form_category_id,
            "f_ids": self.form_ids
        }


class ChangeUserGroupStatus(Request):
    def __init__(self, user_group_id, is_active):
        self.user_group_id = user_group_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["ug_id", "active"])
        user_group_id = data.get("ug_id")
        is_active = data.get("active")
        return ChangeUserGroupStatus(user_group_id, is_active)

    def to_inner_structure(self):
        return {
            "ug_id": self.user_group_id,
            "active": self.is_active
        }


class GetUsers(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetUsers()

    def to_inner_structure(self):
        return {
        }


class SaveUser(Request):
    def __init__(
        self, email_id, user_group_id, employee_name,
        employee_code, contact_no, address, designation,
        country_ids, domain_ids
    ):
        self.email_id = email_id
        self.user_group_id = user_group_id
        self.employee_name = employee_name
        self.employee_code = employee_code
        self.contact_no = contact_no
        self.address = address
        self.designation = designation
        self.country_ids = country_ids
        self.domain_ids = domain_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "email_id", "ug_id", "employee_name", "employee_code",
            "contact_no", "address", "designation", "country_ids",
            "domain_ids"])
        email_id = data.get("email_id")
        user_group_id = data.get("ug_id")
        employee_name = data.get("employee_name")
        employee_code = data.get("employee_code")
        contact_no = data.get("contact_no")
        address = data.get("address")
        designation = data.get("designation")
        country_ids = data.get("country_ids")
        domain_ids = data.get("domain_ids")
        return SaveUser(
            email_id, user_group_id, employee_name, employee_code, contact_no,
            address, designation, country_ids, domain_ids
        )

    def to_inner_structure(self):
        return {
            "email_id": self.email_id,
            "ug_id": self.user_group_id,
            "employee_name": self.employee_name,
            "employee_code": self.employee_code,
            "contact_no": self.contact_no,
            "address": self.address,
            "designation": self.designation,
            "country_ids": self.country_ids,
            "domain_ids": self.domain_ids
        }


class UpdateUser(Request):
    def __init__(
        self, user_id, user_group_id, employee_name,
        employee_code, contact_no, address, designation,
        country_ids, domain_ids
    ):
        self.user_id = user_id
        self.user_group_id = user_group_id
        self.employee_name = employee_name
        self.employee_code = employee_code
        self.contact_no = contact_no
        self.address = address
        self.designation = designation
        self.country_ids = country_ids
        self.domain_ids = domain_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "user_id", "ug_id", "employee_name", "employee_code", "contact_no",
            "address", "designation", "country_ids", "domain_ids"
        ])
        user_id = data.get("user_id")
        user_group_id = data.get("ug_id")
        employee_name = data.get("employee_name")
        employee_code = data.get("employee_code")
        contact_no = data.get("contact_no")
        address = data.get("address")
        designation = data.get("designation")
        country_ids = data.get("country_ids")
        domain_ids = data.get("domain_ids")
        return UpdateUser(
            user_id, user_group_id, employee_name, employee_code, contact_no,
            address, designation, country_ids, domain_ids
        )

    def to_inner_structure(self):
        return {
            "user_id": self.user_id,
            "ug_id": self.user_group_id,
            "employee_name": self.employee_name,
            "employee_code": self.employee_code,
            "contact_no": self.contact_no,
            "address": self.address,
            "designation": self.designation,
            "country_ids": self.country_ids,
            "domain_ids": self.domain_ids
        }


class ChangeUserStatus(Request):
    def __init__(self, user_id, is_active):
        self.user_id = user_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_id", "is_active"])
        user_id = data.get("user_id")
        is_active = data.get("is_active")
        return ChangeUserStatus(user_id, is_active)

    def to_inner_structure(self):
        return {
            "user_id": self.user_id,
            "is_active": self.is_active,
        }


class GetValidityDateList(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetValidityDateList()

    def to_inner_structure(self):
        return {
        }


class SaveValidityDateSettings(Request):
    def __init__(self, validity_date_settings):
        self.validity_date_settings = validity_date_settings

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["validity_date_settings"])
        validity_date_settings = data.get("validity_date_settings")
        return SaveValidityDateSettings(validity_date_settings)

    def to_inner_structure(self):
        return {
            "validity_date_settings": self.validity_date_settings
        }


class GetUserMappings(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetUserMappings()

    def to_inner_structure(self):
        return {
        }


class SaveUserMappings(Request):
    def __init__(self, user_id, cc_user_ids, techno_manager_ids):
        self.user_id = user_id
        self.cc_user_ids = cc_user_ids
        self.techno_manager_ids = techno_manager_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, ["user_id", "cc_user_ids", "techno_manager_ids"])
        user_id = data.get("user_id")
        cc_user_ids = data.get("cc_user_ids")
        techno_manager_ids = data.get("techno_manager_ids")
        return SaveUserMappings(user_id, cc_user_ids, techno_manager_ids)

    def to_inner_structure(self):
        return {
            "user_id": self.user_id,
            "cc_user_ids": self.cc_user_ids,
            "techno_manager_ids": self.techno_manager_ids
        }


def _init_Request_class_map():
    classes = [
        GetUserGroups, SaveUserGroup, UpdateUserGroup,
        ChangeUserGroupStatus, GetUsers, SaveUser, UpdateUser,
        ChangeUserStatus, GetValidityDateList, SaveValidityDateSettings,
        GetUserMappings, SaveUserMappings
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


class UserGroup(object):
    def __init__(
        self, user_group_id, user_group_name, form_category_id,
        form_ids, is_active, no_of_users
    ):
        self.user_group_id = user_group_id
        self.user_group_name = user_group_name
        self.form_category_id = form_category_id
        self.form_ids = form_ids
        self.is_active = is_active
        self.no_of_users = no_of_users

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "user_group_id", "user_group_name",
                "form_category_id", "form_ids", "is_active", "no_of_users"
            ])
        user_group_id = data.get("user_group_id")
        user_group_name = data.get("user_group_name")
        form_category_id = data.get("form_category_id")
        form_ids = data.get("form_ids")
        is_active = data.get("is_active")
        no_of_users = data.get("no_of_users")
        return UserGroup(
            user_group_id, user_group_name, form_category_id,
            form_ids, is_active, no_of_users)

    def to_structure(self):
        return {
            "user_group_id": self.user_group_id,
            "user_group_name": self.user_group_name,
            "form_category_id": self.form_category_id,
            "form_ids": self.form_ids,
            "is_active": self.is_active,
            "no_of_users": self.no_of_users
        }


class GetUserGroupsSuccess(Response):
    def __init__(self, form_categories, forms, user_groups):
        self.form_categories = form_categories
        self.forms = forms
        self.user_groups = user_groups

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, ["form_categories", "forms", "user_group_details"])
        form_categories = data.get("form_categories")
        forms = data.get("forms")
        user_groups = data.get("user_group_details")
        return GetUserGroupsSuccess(form_categories, forms, user_groups)

    def to_inner_structure(self):
        return {
            "form_categories": self.form_categories,
            "forms": self.forms,
            "user_group_details": self.user_groups
        }


class SaveUserGroupSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveUserGroupSuccess()

    def to_inner_structure(self):
        return {
        }


class GroupNameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GroupNameAlreadyExists()

    def to_inner_structure(self):
        return {
        }


class UpdateUserGroupSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateUserGroupSuccess()

    def to_inner_structure(self):
        return {
        }


class InvalidUserGroupId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidUserGroupId()

    def to_inner_structure(self):
        return {
        }


class ChangeUserGroupStatusSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ChangeUserGroupStatusSuccess()

    def to_inner_structure(self):
        return {
        }


class GetUsersSuccess(Response):
    def __init__(self, user_groups, domains, countries, users):
        self.user_groups = user_groups
        self.domains = domains
        self.countries = countries
        self.users = users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, ["user_groups", "domains", "countries", "user_details"])
        user_groups = data.get("user_groups")
        domains = data.get("domains")
        countries = data.get("countries")
        users = data.get("user_details")
        return GetUsersSuccess(user_groups, domains, countries, users)

    def to_inner_structure(self):
        return {
            "user_groups": self.user_groups,
            "domains": self.domains,
            "countries": self.countries,
            "user_details": self.users
        }


class SaveUserSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveUserSuccess()

    def to_inner_structure(self):
        return {
        }


class EmailIDAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return EmailIDAlreadyExists()

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


class EmployeeCodeAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return EmployeeCodeAlreadyExists()

    def to_inner_structure(self):
        return {
        }


class InvalidUserId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidUserId()

    def to_inner_structure(self):
        return {
        }


class CannotDeactivateUserExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CannotDeactivateUserExists()

    def to_inner_structure(self):
        return {
        }


class UpdateUserSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateUserSuccess()

    def to_inner_structure(self):
        return {
        }


class ChangeUserStatusSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ChangeUserStatusSuccess()

    def to_inner_structure(self):
        return {
        }


class SaveValidityDateSettingsSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveValidityDateSettingsSuccess()

    def to_inner_structure(self):
        return {
        }


class GetValidityDateListSuccess(Response):
    def __init__(
        self, countries, domains, validity_dates, country_domain_mappings
    ):
        self.countries = countries
        self.domains = domains
        self.validity_dates = validity_dates
        self.country_domain_mappings = country_domain_mappings

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "countries", "domains", "validity_date_settings",
                "country_domain_mappings"
            ])
        countries = data.get("countries")
        domains = data.get("domains")
        validity_dates = data.get("validity_date_settings")
        country_domain_mappings = data.get("country_domain_mappings")
        country_domain_mappings = parse_structure_MapType_UnsignedInteger_32_VectorType_UnsignedInteger_32(country_domain_mappings)
        return GetValidityDateListSuccess(
            countries, domains, validity_dates, country_domain_mappings
        )

    def to_inner_structure(self):
        return {
            "countries": self.countries,
            "domains": self.domains,
            "validity_date_settings": self.validity_dates,
            "country_domain_mappings": to_structure_MapType_UnsignedInteger_32_VectorType_UnsignedInteger_32(
                self.country_domain_mappings)
        }


class UserMapping(object):
    def __init__(
        self, usermapping_id, cc_manager_id, is_active
    ):
        self.usermapping_id = usermapping_id
        self.cc_manager_id = cc_manager_id
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "usermapping_id", "cc_manager_id", "is_active"
            ])
        usermapping_id = data.get("usermapping_id")
        cc_manager_id = data.get("cc_manager_id")
        is_active = data.get("is_active")
        return UserMapping(
            usermapping_id, cc_manager_id, is_active
        )

    def to_structure(self):
        return {
            "usermapping_id": self.usermapping_id,
            "cc_manager_id": self.cc_manager_id,
            "is_active": self.is_active
        }


class UserMappingUsers(object):
    def __init__(
        self, usermapping_id, user_id, form_category_id
    ):
        self.usermapping_id = usermapping_id
        self.user_id = user_id
        self.form_category_id = form_category_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "usermapping_id", "user_id", "form_category_id"
            ])
        usermapping_id = data.get("usermapping_id")
        user_id = data.get("user_id")
        form_category_id = data.get("form_category_id")
        return UserMappingUsers(
            usermapping_id, user_id, form_category_id
        )

    def to_structure(self):
        return {
            "usermapping_id": self.usermapping_id,
            "user_id": self.user_id,
            "form_category_id": self.form_category_id
        }


class User(object):
    def __init__(
        self, user_id, employee_name, is_active, country_ids, domain_ids
    ):
        self.user_id = user_id
        self.employee_name = employee_name
        self.is_active = is_active
        self.country_ids = country_ids
        self.domain_ids = domain_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "user_id", "employee_name", "is_active",
                "country_ids", "domain_ids"
            ]
        )
        user_id = data.get("user_id")
        employee_name = data.get("employee_name")
        is_active = data.get("is_active")
        country_ids = data.get("country_ids")
        domain_ids = data.get("domain_ids")
        return User(user_id, employee_name, is_active, country_ids, domain_ids)

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "employee_name": self.employee_name,
            "is_active": self.is_active,
            "country_ids": self.country_ids,
            "domain_ids": self.domain_ids
        }


class GetUserMappingsSuccess(Response):
    def __init__(
        self, countries, domains, cc_managers, cc_users, techno_managers,
        user_mappings, user_mapping_users
    ):
        self.countries = countries
        self.domains = domains
        self.cc_managers = cc_managers
        self.cc_users = cc_users
        self.techno_managers = techno_managers
        self.user_mappings = user_mappings
        self.user_mapping_users = user_mapping_users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "countries", "domains", "cc_managers", "cc_users",
                "techno_managers", "user_mappings", "user_mapping_users"
            ])
        countries = data.get("countries")
        domains = data.get("domains")
        cc_managers = data.get("cc_managers")
        cc_users = data.get("cc_users")
        techno_managers = data.get("techno_managers")
        user_mappings = data.get("user_mappings")
        user_mapping_users = data.get("user_mapping_users")
        return GetUserMappingsSuccess(
            countries, domains, cc_managers, cc_users, techno_managers,
            user_mappings, user_mapping_users
        )

    def to_inner_structure(self):
        return {
            "countries": self.countries,
            "domains": self.domains,
            "cc_managers": self.cc_managers,
            "cc_users": self.cc_users,
            "techno_managers": self.techno_managers,
            "user_mappings": self.user_mappings,
            "user_mapping_users": self.user_mapping_users
        }


class SaveUserMappingsSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveUserMappingsSuccess()

    def to_inner_structure(self):
        return {
        }


def _init_Response_class_map():
    classes = [
        GetUserGroupsSuccess, SaveUserGroupSuccess,
        GroupNameAlreadyExists, UpdateUserGroupSuccess, InvalidUserGroupId,
        ChangeUserGroupStatusSuccess, GetUsersSuccess, SaveUserSuccess,
        EmailIDAlreadyExists, ContactNumberAlreadyExists,
        EmployeeCodeAlreadyExists, InvalidUserId, UpdateUserSuccess,
        ChangeUserStatusSuccess, CannotDeactivateUserExists,
        GetValidityDateListSuccess, SaveValidityDateSettingsSuccess,
        GetUserMappingsSuccess, GetUserMappingsSuccess,
        SaveUserMappingsSuccess
    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()


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
            request, "admin", "Request"
        )
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": to_VariantType(
                self.request, "admin", "Response"
            )
        }
