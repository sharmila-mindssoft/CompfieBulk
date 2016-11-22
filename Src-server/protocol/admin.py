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
    def __init__(self, user_group_id, user_group_name, is_active):
        self.user_group_id = user_group_id
        self.user_group_name = user_group_name
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["ug_id", "ug_name", "active"])
        user_group_id = data.get("ug_id")
        user_group_name = data.get("ug_name")
        is_active = data.get("active")
        return ChangeUserGroupStatus(user_group_id, user_group_name, is_active)

    def to_inner_structure(self):
        return {
            "ug_id": self.user_group_id,
            "ug_name": self.user_group_name,
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


class SendRegistraion(Request):
    def __init__(self, user_id, username, email_id):
        self.user_id = user_id
        self.email_id = email_id
        self.username = username

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_id", "username", "email_id"])
        user_id = data.get("user_id")
        username = data.get("username")
        email_id = data.get("email_id")
        return SendRegistraion(user_id, username, email_id)

    def to_inner_structure(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email_id": self.email_id
        }


class SaveUser(Request):
    def __init__(
        self, user_category_id, employee_name,
        employee_code, email_id, contact_no, mobile_no,
        user_group_id, address, designation,
        country_ids, domain_ids
    ):
        self.user_category_id = user_category_id
        self.employee_name = employee_name
        self.employee_code = employee_code
        self.email_id = email_id
        self.contact_no = contact_no
        self.mobile_no = mobile_no
        self.user_group_id = user_group_id
        self.address = address
        self.designation = designation
        self.country_ids = country_ids
        self.domain_ids = domain_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "u_cat_id",  "employee_name", "employee_code",
            "email_id", "contact_no", "mobile_no",
            "ug_id", "address", "designation", "country_ids",
            "domain_ids"])
        user_category_id = data.get("u_cat_id")
        employee_name = data.get("employee_name")
        employee_code = data.get("employee_code")
        email_id = data.get("email_id")
        contact_no = data.get("contact_no")
        mobile_no = data.get("mobile_no")
        user_group_id = data.get("ug_id")
        address = data.get("address")
        designation = data.get("designation")
        country_ids = data.get("country_ids")
        domain_ids = data.get("domain_ids")
        return SaveUser(
            user_category_id, employee_name, employee_code, email_id,
            contact_no, mobile_no, user_group_id, address,
            designation, country_ids, domain_ids
        )

    def to_inner_structure(self):
        return {
            "u_cat_id": self.user_category_id,
            "employee_name": self.employee_name,
            "employee_code": self.employee_code,
            "email_id": self.email_id,
            "contact_no": self.contact_no,
            "mobile_no": self.mobile_no,
            "ug_id": self.user_group_id,
            "address": self.address,
            "designation": self.designation,
            "country_ids": self.country_ids,
            "domain_ids": self.domain_ids
        }


class UpdateUser(Request):
    def __init__(
        self, user_id, user_category_id, employee_name,
        employee_code, email_id, contact_no, mobile_no,
        user_group_id, address, designation,
        country_ids, domain_ids
    ):
        self.user_id = user_id
        self.user_category_id = user_category_id
        self.employee_name = employee_name
        self.employee_code = employee_code
        self.email_id = email_id
        self.contact_no = contact_no
        self.mobile_no = mobile_no
        self.user_group_id = user_group_id
        self.address = address
        self.designation = designation
        self.country_ids = country_ids
        self.domain_ids = domain_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "user_id", "u_cat_id",  "employee_name", "employee_code",
            "email_id", "contact_no", "mobile_no",
            "ug_id", "address", "designation", "country_ids",
            "domain_ids"])
        user_id = data.get("user_id")
        user_category_id = data.get("u_cat_id")
        employee_name = data.get("employee_name")
        employee_code = data.get("employee_code")
        email_id = data.get("email_id")
        contact_no = data.get("contact_no")
        mobile_no = data.get("mobile_no")
        user_group_id = data.get("ug_id")
        address = data.get("address")
        designation = data.get("designation")
        country_ids = data.get("country_ids")
        domain_ids = data.get("domain_ids")
        return UpdateUser(
            user_id, user_category_id, employee_name, employee_code, email_id,
            contact_no, mobile_no, user_group_id, address,
            designation, country_ids, domain_ids
        )

    def to_inner_structure(self):
        return {
            "user_id": self.user_id,
            "u_cat_id": self.user_category_id,
            "employee_name": self.employee_name,
            "employee_code": self.employee_code,
            "email_id": self.email_id,
            "contact_no": self.contact_no,
            "mobile_no": self.mobile_no,
            "ug_id": self.user_group_id,
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

class ChangeDisableStatus(Request):
    def __init__(self, user_id, is_active):
        self.user_id = user_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_id", "is_disable"])
        user_id = data.get("user_id")
        is_active = data.get("is_disable")
        return ChangeDisableStatus(user_id, is_active)

    def to_inner_structure(self):
        return {
            "user_id": self.user_id,
            "is_disable": self.is_active,
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
    def __init__(self, country_id, domain_id, parent_user_id, child_users):
        self.country_id = country_id
        self.domain_id = domain_id
        self.parent_user_id = parent_user_id
        self.child_users = child_users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "country_id", "domain_id", "parent_user_id", "child_users"
            ])
        country_id = data.get("country_id")
        domain_id = data.get("domain_id")
        parent_user_id = data.get("parent_user_id")
        child_users = data.get("child_users")
        return SaveUserMappings(
            country_id, domain_id, parent_user_id, child_users
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "domain_id": self.domain_id,
            "parent_user_id": self.parent_user_id,
            "child_users": self.child_users
        }


class GetReassignUserAccountFormdata(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetReassignUserAccountFormdata()

    def to_inner_structure(self):
        return {
        }


class SaveReassignUserAccount(Request):
    def __init__(
        self, user_type, old_user_id, new_user_id, assigned_ids, remarks
    ):
        self.user_type = user_type
        self.old_user_id = old_user_id
        self.new_user_id = new_user_id
        self.assigned_ids = assigned_ids
        self.remarks = remarks

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "user_type", "old_user_id", "new_user_id", "assigned_ids",
            "remarks"
        ])
        user_type = data.get("user_type")
        old_user_id = data.get("old_user_id")
        new_user_id = data.get("new_user_id")
        assigned_ids = data.get("assigned_ids")
        remarks = data.get("remarks")
        return SaveReassignUserAccount(
            user_type, old_user_id, new_user_id, assigned_ids, remarks)

    def to_inner_structure(self):
        return {
            "user_type": self.user_type,
            "old_user_id": self.old_user_id,
            "new_user_id": self.new_user_id,
            "assigned_ids": self.assigned_ids,
            "remarks": self.remarks
        }


def _init_Request_class_map():
    classes = [
        GetUserGroups, SaveUserGroup, UpdateUserGroup,
        ChangeUserGroupStatus, GetUsers, SaveUser, UpdateUser,
        ChangeUserStatus, GetValidityDateList, SaveValidityDateSettings,
        GetUserMappings, SaveUserMappings, GetReassignUserAccountFormdata,
        SaveReassignUserAccount, SendRegistraion, ChangeDisableStatus
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
        self, user_group_id, user_group_name, user_category_id,
        form_ids, is_active, no_of_users
    ):
        self.user_group_id = user_group_id
        self.user_group_name = user_group_name
        self.user_category_id = user_category_id
        self.form_ids = form_ids
        self.is_active = is_active
        self.no_of_users = no_of_users

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "user_group_id", "user_group_name",
                "user_category_id", "form_ids", "is_active", "no_of_users"
            ])
        user_group_id = data.get("user_group_id")
        user_group_name = data.get("user_group_name")
        user_category_id = data.get("user_category_id")
        form_ids = data.get("form_ids")
        is_active = data.get("is_active")
        no_of_users = data.get("no_of_users")
        return UserGroup(
            user_group_id, user_group_name, user_category_id,
            form_ids, is_active, no_of_users)

    def to_structure(self):
        return {
            "user_group_id": self.user_group_id,
            "user_group_name": self.user_group_name,
            "user_category_id": self.user_category_id,
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
    def __init__(self, user_groups, domains, countries, user_categories, users):
        self.user_groups = user_groups
        self.domains = domains
        self.countries = countries
        self.user_categories = user_categories
        self.users = users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, ["user_groups", "domains", "countries", "user-categories", "user_details"])
        user_groups = data.get("user_groups")
        domains = data.get("domains")
        countries = data.get("countries")
        user_categories = data.get("user_categories")
        users = data.get("user_details")
        return GetUsersSuccess(user_groups, domains, countries, user_categories, users)

    def to_inner_structure(self):
        return {
            "user_groups": self.user_groups,
            "domains": self.domains,
            "countries": self.countries,
            "user_categories": self.user_categories,
            "user_details": self.users
        }

class SendRegistraionSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SendRegistraionSuccess()

    def to_inner_structure(self):
        return {
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
        self, user_mapping_id, parent_user_id, child_user_id
    ):
        self.user_mapping_id = user_mapping_id
        self.parent_user_id = parent_user_id
        self.child_user_id = child_user_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "user_mapping_id", "parent_user_id", "child_user_id"
            ])
        user_mapping_id = data.get("user_mapping_id")
        parent_user_id = data.get("parent_user_id")
        child_user_id = data.get("child_user_id")
        return UserMapping(
            user_mapping_id, parent_user_id, child_user_id
        )

    def to_structure(self):
        return {
            "user_mapping_id": self.user_mapping_id,
            "parent_user_id": self.parent_user_id,
            "child_user_id": self.child_user_id
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
        self, countries, domains, knowledge_managers, knowledge_users,
        techno_managers, techno_users, domain_managers, domain_users,
        user_mappings
    ):
        self.countries = countries
        self.domains = domains
        self.knowledge_managers = knowledge_managers
        self.knowledge_users = knowledge_users
        self.techno_managers = techno_managers
        self.techno_users = techno_users
        self.domain_managers = domain_managers
        self.domain_users = domain_users
        self.user_mappings = user_mappings

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "countries", "domains", "knowledge_managers",
                "knowledge_users", "techno_managers", "techno_users",
                "domain_managers", "domain_users", "user_mappings"
            ])
        countries = data.get("countries")
        domains = data.get("domains")
        knowledge_managers = data.get("knowledge_managers")
        knowledge_users = data.get("knowledge_users")
        techno_managers = data.get("techno_managers")
        techno_users = data.get("techno_users")
        domain_managers = data.get("domain_managers")
        domain_users = data.get("domain_users")
        user_mappings = data.get("user_mappings")
        return GetUserMappingsSuccess(
            countries, domains, knowledge_managers, knowledge_users,
            techno_managers, techno_users, domain_managers, domain_users,
            user_mappings
        )

    def to_inner_structure(self):
        return {
            "countries": self.countries,
            "domains": self.domains,
            "knowledge_managers": self.knowledge_managers,
            "knowledge_users": self.knowledge_users,
            "techno_managers": self.techno_managers,
            "techno_users": self.techno_users,
            "domain_managers": self.domain_managers,
            "domain_users": self.domain_users,
            "user_mappings": self.user_mappings
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


class LegalEntity(object):
    def __init__(
        self, legal_entity_id, legal_entity_name, business_group_id,
        client_id, country_id
    ):
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.business_group_id = business_group_id
        self.client_id = client_id
        self.country_id = country_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "legal_entity_id", "legal_entity_name", "business_group_id",
                "client_id", "country_id"
            ]
        )
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_name = data.get("legal_entity_name")
        business_group_id = data.get("business_group_id")
        client_id = data.get("client_id")
        country_id = data.get("country_id")
        return LegalEntity(
            legal_entity_id, legal_entity_name, business_group_id, client_id,
            country_id
        )

    def to_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id,
            "legal_entity_name": self.legal_entity_name,
            "business_group_id": self.business_group_id,
            "client_id": self.client_id,
            "country_id": self.country_id
        }


class AssignedLegalEntities(object):
    def __init__(
        self, user_id, legal_entity_id
    ):
        self.user_id = user_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id", "legal_entity_id"
        ])
        user_id = data.get("user_id")
        legal_entity_id = data.get("legal_entity_id")
        return AssignedLegalEntities(user_id, legal_entity_id)

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "legal_entity_id": self.legal_entity_id
        }


class AssignedUnits(object):
    def __init__(
        self, user_id, unit_id, domain_id
    ):
        self.user_id = user_id
        self.unit_id = unit_id
        self.domain_id = domain_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id", "unit_id", "domain_id"
        ])
        user_id = data.get("user_id")
        unit_id = data.get("unit_id")
        domain_id = data.get("domain_id")
        return AssignedUnits(user_id, unit_id, domain_id)

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "unit_id": self.unit_id,
            "domain_id": self.domain_id
        }


class AssignedClient(object):
    def __init__(
        self, user_id, client_id
    ):
        self.user_id = user_id
        self.client_id = client_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id", "client_id"
        ])
        user_id = data.get("user_id")
        client_id = data.get("client_id")
        return AssignedUnits(user_id, client_id)

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "client_id": self.client_id
        }


class GetReassignUserAccountFormdataSuccess(Request):
    def __init__(
        self, techno_managers, techno_users, domain_managers,
        domain_users, groups, business_groups, admin_legal_entity,
        domains, countries, unit_id_name, assigned_legal_entities,
        assigned_units, assigned_clients
    ):
        self.techno_managers = techno_managers
        self.techno_users = techno_users
        self.domain_managers = domain_managers
        self.domain_users = domain_users
        self.groups = groups
        self.business_groups = business_groups
        self.admin_legal_entity = admin_legal_entity
        self.domains = domains
        self.countries = countries
        self.unit_id_name = unit_id_name
        self.assigned_legal_entities = assigned_legal_entities
        self.assigned_units = assigned_units
        self.assigned_clients = assigned_clients

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "techno_managers", "techno_users", "domain_managers",
            "domain_users", "groups", "business_groups", "admin_legal_entity",
            "domains", "countries", "unit_id_name", "assigned_legal_entities",
            "assigned_units", "assigned_clients"
        ])
        techno_managers = data.get("techno_managers")
        techno_users = data.get("techno_users")
        domain_managers = data.get("domain_managers")
        domain_users = data.get("domain_users")
        groups = data.get("groups")
        business_groups = data.get("business_groups")
        admin_legal_entity = data.get("admin_legal_entity")
        domains = data.get("domains")
        countries = data.get("countries")
        unit_id_name = data.get("unit_id_name")
        assigned_legal_entities = data.get("assigned_legal_entities")
        assigned_units = data.get("assigned_units")
        assigned_clients = data.get("assigned_clients")
        return GetReassignUserAccountFormdataSuccess(
            techno_managers, techno_users, domain_managers,
            domain_users, groups, business_groups, admin_legal_entity,
            domains, countries, unit_id_name, assigned_legal_entities,
            assigned_units, assigned_clients
        )

    def to_inner_structure(self):
        return {
            "techno_managers": self.techno_managers,
            "techno_users": self.techno_users,
            "domain_managers": self.domain_managers,
            "domain_users": self.domain_users,
            "groups": self.groups,
            "business_groups": self.business_groups,
            "admin_legal_entity": self.admin_legal_entity,
            "domains": self.domains,
            "countries": self.countries,
            "unit_id_name": self.unit_id_name,
            "assigned_legal_entities": self.assigned_legal_entities,
            "assigned_units": self.assigned_units,
            "assigned_clients": self.assigned_clients
        }


class SaveReassignUserAccountSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveReassignUserAccountSuccess()

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
        SaveUserMappingsSuccess, SaveReassignUserAccountSuccess,
        SendRegistraionSuccess
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
