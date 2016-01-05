import json
from protocol.jsonvalidators import (parse_enum, parse_dictionary, parse_static_list)
from protocol.parse_structure import (
    parse_structure_MapType_SignedIntegerType_8_RecordType_core_Menu,
    parse_structure_CustomTextType_100,
    parse_structure_VectorType_RecordType_core_Domain,
    parse_structure_VariantType_admin_Request,
    parse_structure_CustomTextType_250,
    parse_structure_VectorType_RecordType_core_UserGroup,
    parse_structure_VectorType_SignedIntegerType_8,
    parse_structure_VectorType_RecordType_core_FormCategory,
    parse_structure_SignedIntegerType_8,
    parse_structure_VectorType_RecordType_core_Country,
    parse_structure_Bool,
    parse_structure_VectorType_RecordType_core_UserDetails,
    parse_structure_CustomTextType_20, parse_structure_CustomTextType_50,
    parse_structure_RecordType_admin_UserGroup,
    parse_structure_VectorType_RecordType_admin_UserGroup
)
from protocol.to_structure import (
    to_structure_MapType_SignedIntegerType_8_RecordType_core_Menu,
    to_structure_CustomTextType_100,
    to_structure_VectorType_RecordType_core_Domain,
    to_structure_VariantType_admin_Request,
    to_structure_CustomTextType_250,
    to_structure_VectorType_RecordType_core_UserGroup,
    to_structure_VectorType_SignedIntegerType_8,
    to_structure_VectorType_RecordType_core_FormCategory,
    to_structure_SignedIntegerType_8,
    to_structure_VectorType_RecordType_core_Country, to_structure_Bool,
    to_structure_VectorType_RecordType_core_UserDetails,
    to_structure_CustomTextType_20, to_structure_CustomTextType_50,
    to_structure_RecordType_admin_UserGroup,
    to_structure_VectorType_RecordType_admin_UserGroup
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
        data = parse_dictionary(data, ["user_group_name", "form_category_id", "form_ids"])
        user_group_name = data.get("user_group_name")
        user_group_name = parse_structure_CustomTextType_50(user_group_name)
        form_category_id = data.get("form_category_id")
        form_category_id = parse_structure_SignedIntegerType_8(form_category_id)
        form_ids = data.get("form_ids")
        form_ids = parse_structure_VectorType_SignedIntegerType_8(form_ids)
        return SaveUserGroup(user_group_name, form_category_id, form_ids)

    def to_inner_structure(self):
        return {
            "user_group_name": to_structure_CustomTextType_50(self.user_group_name),
            "form_category_id": to_structure_SignedIntegerType_8(self.form_category_id),
            "form_ids": to_structure_VectorType_SignedIntegerType_8(self.form_ids),
        }

class UpdateUserGroup(Request):
    def __init__(self, user_group_id, user_group_name, form_category_id, form_ids):
        self.user_group_id = user_group_id
        self.user_group_name = user_group_name
        self.form_category_id = form_category_id
        self.form_ids = form_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_group_id", "user_group_name", "form_category_id", "form_ids"])
        user_group_id = data.get("user_group_id")
        user_group_id = parse_structure_SignedIntegerType_8(user_group_id)
        user_group_name = data.get("user_group_name")
        user_group_name = parse_structure_CustomTextType_50(user_group_name)
        form_category_id = data.get("form_category_id")
        form_category_id = parse_structure_SignedIntegerType_8(form_category_id)
        form_ids = data.get("form_ids")
        form_ids = parse_structure_VectorType_SignedIntegerType_8(form_ids)
        return UpdateUserGroup(user_group_id, user_group_name, form_category_id, form_ids)

    def to_inner_structure(self):
        return {
            "user_group_id": to_structure_SignedIntegerType_8(self.user_group_id),
            "user_group_name": to_structure_CustomTextType_50(self.user_group_name),
            "form_category_id": to_structure_SignedIntegerType_8(self.form_category_id),
            "form_ids": to_structure_VectorType_SignedIntegerType_8(self.form_ids),
        }

class ChangeUserGroupStatus(Request):
    def __init__(self, user_group_id, is_active):
        self.user_group_id = user_group_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_group_id", "is_active"])
        user_group_id = data.get("user_group_id")
        user_group_id = parse_structure_SignedIntegerType_8(user_group_id)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return ChangeUserGroupStatus(user_group_id, is_active)

    def to_inner_structure(self):
        return {
            "user_group_id": to_structure_SignedIntegerType_8(self.user_group_id),
            "is_active": to_structure_Bool(self.is_active),
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
    def __init__(self, email_id, user_group_id, employee_name, employee_code, contact_no, address, designation, country_ids, domain_ids):
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
        data = parse_dictionary(data, ["email_id", "user_group_id", "employee_name", "employee_code", "contact_no", "address", "designation", "country_ids", "domain_ids"])
        email_id = data.get("email_id")
        email_id = parse_structure_CustomTextType_100(email_id)
        user_group_id = data.get("user_group_id")
        user_group_id = parse_structure_SignedIntegerType_8(user_group_id)
        employee_name = data.get("employee_name")
        employee_name = parse_structure_CustomTextType_50(employee_name)
        employee_code = data.get("employee_code")
        employee_code = parse_structure_CustomTextType_50(employee_code)
        contact_no = data.get("contact_no")
        contact_no = parse_structure_CustomTextType_20(contact_no)
        address = data.get("address")
        address = parse_structure_CustomTextType_250(address)
        designation = data.get("designation")
        designation = parse_structure_CustomTextType_50(designation)
        country_ids = data.get("country_ids")
        country_ids = parse_structure_VectorType_SignedIntegerType_8(country_ids)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        return SaveUser(email_id, user_group_id, employee_name, employee_code, contact_no, address, designation, country_ids, domain_ids)

    def to_inner_structure(self):
        return {
            "email_id": to_structure_CustomTextType_100(self.email_id),
            "user_group_id": to_structure_SignedIntegerType_8(self.user_group_id),
            "employee_name": to_structure_CustomTextType_50(self.employee_name),
            "employee_code": to_structure_CustomTextType_50(self.employee_code),
            "contact_no": to_structure_CustomTextType_20(self.contact_no),
            "address": to_structure_CustomTextType_250(self.address),
            "designation": to_structure_CustomTextType_50(self.designation),
            "country_ids": to_structure_VectorType_SignedIntegerType_8(self.country_ids),
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
        }

class UpdateUser(Request):
    def __init__(self, user_id, user_group_id, employee_name, employee_code, contact_no, address, designation, country_ids, domain_ids):
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
        data = parse_dictionary(data, ["user_id", "user_group_id", "employee_name", "employee_code", "contact_no", "address", "designation", "country_ids", "domain_ids"])
        user_id = data.get("user_id")
        user_id = parse_structure_SignedIntegerType_8(user_id)
        user_group_id = data.get("user_group_id")
        user_group_id = parse_structure_SignedIntegerType_8(user_group_id)
        employee_name = data.get("employee_name")
        employee_name = parse_structure_CustomTextType_50(employee_name)
        employee_code = data.get("employee_code")
        employee_code = parse_structure_CustomTextType_50(employee_code)
        contact_no = data.get("contact_no")
        contact_no = parse_structure_CustomTextType_20(contact_no)
        address = data.get("address")
        address = parse_structure_CustomTextType_250(address)
        designation = data.get("designation")
        designation = parse_structure_CustomTextType_50(designation)
        country_ids = data.get("country_ids")
        country_ids = parse_structure_VectorType_SignedIntegerType_8(country_ids)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        return UpdateUser(user_id, user_group_id, employee_name, employee_code, contact_no, address, designation, country_ids, domain_ids)

    def to_inner_structure(self):
        return {
            "user_id": to_structure_SignedIntegerType_8(self.user_id),
            "user_group_id": to_structure_SignedIntegerType_8(self.user_group_id),
            "employee_name": to_structure_CustomTextType_50(self.employee_name),
            "employee_code": to_structure_CustomTextType_50(self.employee_code),
            "contact_no": to_structure_CustomTextType_20(self.contact_no),
            "address": to_structure_CustomTextType_250(self.address),
            "designation": to_structure_CustomTextType_50(self.designation),
            "country_ids": to_structure_VectorType_SignedIntegerType_8(self.country_ids),
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
        }

class ChangeUserStatus(Request):
    def __init__(self, user_id, is_active):
        self.user_id = user_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_id", "is_active"])
        user_id = data.get("user_id")
        user_id = parse_structure_SignedIntegerType_8(user_id)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return ChangeUserStatus(user_id, is_active)

    def to_inner_structure(self):
        return {
            "user_id": to_structure_SignedIntegerType_8(self.user_id),
            "is_active": to_structure_Bool(self.is_active),
        }


def _init_Request_class_map():
    classes = [GetUserGroups, SaveUserGroup, UpdateUserGroup, ChangeUserGroupStatus, GetUsers, SaveUser, UpdateUser, ChangeUserStatus]
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

class UserGroup(object):
    def __init__(self, user_group_id, user_group_name, form_category_id, 
        form_ids, is_active):
        self.user_group_id = user_group_id
        self.user_group_name = user_group_name
        self.form_category_id = form_category_id
        self.form_ids = form_ids
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_group_id", "user_group_name", 
            "form_category_id", "form_ids", "is_active"])
        user_group_id = data.get("user_group_id")
        user_group_id = parse_structure_SignedIntegerType_8(user_group_id)
        user_group_name = data.get("user_group_name")
        user_group_name = parse_structure_CustomTextType_50(user_group_name)
        form_category_id = data.get("form_category_id")
        form_category_id = parse_structure_SignedIntegerType_8(form_category_id)
        form_ids = data.get("form_ids")
        form_ids = parse_structure_VectorType_SignedIntegerType_8(form_ids)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return UserGroup(user_group_id, user_group_name, form_category_id,
            form_ids, is_active)

    def to_structure(self):
        return {
            "user_group_id": to_structure_SignedIntegerType_8(self.user_group_id),
            "user_group_name": to_structure_CustomTextType_50(self.user_group_name),
            "form_category_id": to_structure_SignedIntegerType_8(self.form_category_id),
            "form_ids": to_structure_VectorType_SignedIntegerType_8(self.form_ids),
            "is_active": to_structure_Bool(self.is_active),
        }

class GetUserGroupsSuccess(Response):
    def __init__(self, form_categories, forms, user_groups):
        print "inside get user groups success constructor"
        self.form_categories = form_categories
        print "crossed form_categories assignment"
        self.forms = forms
        print "crossed forms assignment"
        self.user_groups = user_groups
        print "crossed user groups assignment"

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["form_categories", "forms", "user_groups"])
        form_categories = data.get("form_categories")
        form_categories = parse_structure_VectorType_RecordType_core_FormCategory(form_categories)
        forms = data.get("forms")
        forms = parse_structure_MapType_SignedIntegerType_8_RecordType_core_Menu(forms)
        user_groups = data.get("user_groups")
        user_groups = parse_structure_VectorType_RecordType_admin_UserGroup(user_groups)
        return GetUserGroupsSuccess(form_categories, forms, user_groups)

    def to_inner_structure(self):
        print "form_categories : {}".format(to_structure_VectorType_RecordType_core_FormCategory(self.form_categories))
        print "forms : {}".format(to_structure_MapType_SignedIntegerType_8_RecordType_core_Menu(self.forms))
        print "user_groups : {}".format(to_structure_VectorType_RecordType_admin_UserGroup(self.user_groups))
        return {
            "form_categories": to_structure_VectorType_RecordType_core_FormCategory(self.form_categories),
            "forms": to_structure_MapType_SignedIntegerType_8_RecordType_core_Menu(self.forms),
            "user_groups": to_structure_VectorType_RecordType_admin_UserGroup(self.user_groups),
        }

class SaveUserGroupSuccess(Response):
    def __init__(self):
        print "inside save user group success"
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveUserGroupSuccess()

    def to_inner_structure(self):
        print "inside save user group inner structure"
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
        data = parse_dictionary(data, ["user_groups", "domains", "countries", "users"])
        user_groups = data.get("user_groups")
        user_groups = parse_structure_VectorType_RecordType_core_UserGroup(user_groups)
        domains = data.get("domains")
        domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        users = data.get("users")
        users = parse_structure_VectorType_RecordType_core_UserDetails(users)
        return GetUsersSuccess(user_groups, domains, countries, users)

    def to_inner_structure(self):
        return {
            "user_groups": to_structure_VectorType_RecordType_core_UserGroup(self.user_groups),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "users": to_structure_VectorType_RecordType_core_UserDetails(self.users),
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


def _init_Response_class_map():
    classes = [GetUserGroupsSuccess, SaveUserGroupSuccess, GroupNameAlreadyExists, UpdateUserGroupSuccess, InvalidUserGroupId, ChangeUserGroupStatusSuccess, GetUsersSuccess, SaveUserSuccess, EmailIDAlreadyExists, ContactNumberAlreadyExists, EmployeeCodeAlreadyExists, InvalidUserId, UpdateUserSuccess, ChangeUserStatusSuccess]
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
        session_token = parse_structure_CustomTextType_50(session_token)
        request = data.get("request")
        request = parse_structure_VariantType_admin_Request(request)
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": to_structure_CustomTextType_50(self.session_token),
            "request": to_structure_VariantType_admin_Request(self.request),
        }

