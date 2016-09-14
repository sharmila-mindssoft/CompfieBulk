from protocol.jsonvalidators import (parse_dictionary, parse_static_list)
from protocol.parse_structure import (
    parse_structure_MapType_SignedIntegerType_8_RecordType_core_Menu,
    parse_structure_CustomTextType_100,
    parse_structure_VectorType_RecordType_core_Domain,
    parse_structure_VariantType_admin_Request,
    parse_structure_VectorType_RecordType_core_UserGroup,
    parse_structure_VectorType_SignedIntegerType_8,
    parse_structure_VectorType_RecordType_core_FormCategory,
    parse_structure_UnsignedIntegerType_32,
    parse_structure_VectorType_RecordType_core_Country,
    parse_structure_Bool,
    parse_structure_VectorType_RecordType_core_UserDetails,
    parse_structure_CustomTextType_20, parse_structure_CustomTextType_50,
    parse_structure_VectorType_RecordType_admin_UserGroup,
    parse_structure_OptionalType_CustomTextType_250,
    parse_structure_OptionalType_CustomTextType_50
)
from protocol.to_structure import (
    to_structure_MapType_SignedIntegerType_8_RecordType_core_Menu,
    to_structure_CustomTextType_100,
    to_structure_VectorType_RecordType_core_Domain,
    to_structure_VariantType_admin_Request,
    to_structure_VectorType_RecordType_core_UserGroup,
    to_structure_VectorType_SignedIntegerType_8,
    to_structure_VectorType_RecordType_core_FormCategory,
    to_structure_SignedIntegerType_8,
    to_structure_VectorType_RecordType_core_Country, to_structure_Bool,
    to_structure_VectorType_RecordType_core_UserDetails,
    to_structure_CustomTextType_20, to_structure_CustomTextType_50,
    to_structure_VectorType_RecordType_admin_UserGroup,
    to_structure_UnsignedIntegerType_32,
    to_structure_OptionalType_CustomTextType_250,
    to_structure_OptionalType_CustomTextType_50
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
        data = parse_dictionary(data, ["ug_name", "fc_id", "f_ids"])
        user_group_name = data.get("ug_name")
        user_group_name = parse_structure_CustomTextType_50(user_group_name)
        form_category_id = data.get("fc_id")
        form_category_id = parse_structure_UnsignedIntegerType_32(form_category_id)
        form_ids = data.get("f_ids")
        form_ids = parse_structure_VectorType_SignedIntegerType_8(form_ids)
        return SaveUserGroup(user_group_name, form_category_id, form_ids)

    def to_inner_structure(self):
        return {
            "ug_name": to_structure_CustomTextType_50(self.user_group_name),
            "fc_id": to_structure_SignedIntegerType_8(self.form_category_id),
            "f_ids": to_structure_VectorType_SignedIntegerType_8(self.form_ids),
        }

class UpdateUserGroup(Request):
    def __init__(self, user_group_id, user_group_name, form_category_id, form_ids):
        self.user_group_id = user_group_id
        self.user_group_name = user_group_name
        self.form_category_id = form_category_id
        self.form_ids = form_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["ug_id", "ug_name", "fc_id", "f_ids"])
        user_group_id = data.get("ug_id")
        user_group_id = parse_structure_UnsignedIntegerType_32(user_group_id)
        user_group_name = data.get("ug_name")
        user_group_name = parse_structure_CustomTextType_50(user_group_name)
        form_category_id = data.get("fc_id")
        form_category_id = parse_structure_UnsignedIntegerType_32(form_category_id)
        form_ids = data.get("f_ids")
        form_ids = parse_structure_VectorType_SignedIntegerType_8(form_ids)
        return UpdateUserGroup(user_group_id, user_group_name, form_category_id, form_ids)

    def to_inner_structure(self):
        return {
            "ug_id": to_structure_SignedIntegerType_8(self.user_group_id),
            "ug_name": to_structure_CustomTextType_50(self.user_group_name),
            "fc_id": to_structure_SignedIntegerType_8(self.form_category_id),
            "f_ids": to_structure_VectorType_SignedIntegerType_8(self.form_ids),
        }

class ChangeUserGroupStatus(Request):
    def __init__(self, user_group_id, is_active):
        self.user_group_id = user_group_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["ug_id", "active"])
        user_group_id = data.get("ug_id")
        user_group_id = parse_structure_UnsignedIntegerType_32(user_group_id)
        is_active = data.get("active")
        is_active = parse_structure_Bool(is_active)
        return ChangeUserGroupStatus(user_group_id, is_active)

    def to_inner_structure(self):
        return {
            "ug_id": to_structure_SignedIntegerType_8(self.user_group_id),
            "active": to_structure_Bool(self.is_active),
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
        data = parse_dictionary(data, [
            "email", "ug_id", "emp_n", "emp_c", "c_n", "add", "desig", "c_ids", "d_ids"])
        email_id = data.get("email")
        email_id = parse_structure_CustomTextType_100(email_id)
        user_group_id = data.get("ug_id")
        user_group_id = parse_structure_UnsignedIntegerType_32(user_group_id)
        employee_name = data.get("emp_n")
        employee_name = parse_structure_CustomTextType_50(employee_name)
        employee_code = data.get("emp_c")
        employee_code = parse_structure_CustomTextType_50(employee_code)
        contact_no = data.get("c_n")
        contact_no = parse_structure_CustomTextType_20(contact_no)
        address = data.get("add")
        address = parse_structure_OptionalType_CustomTextType_250(address)
        designation = data.get("desig")
        designation = parse_structure_OptionalType_CustomTextType_50(designation)
        country_ids = data.get("c_ids")
        country_ids = parse_structure_VectorType_SignedIntegerType_8(country_ids)
        domain_ids = data.get("d_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        return SaveUser(
            email_id, user_group_id, employee_name, employee_code, contact_no,
            address, designation, country_ids, domain_ids
        )

    def to_inner_structure(self):
        return {
            "email": to_structure_CustomTextType_100(self.email_id),
            "ug_id": to_structure_SignedIntegerType_8(self.user_group_id),
            "emp_n": to_structure_CustomTextType_50(self.employee_name),
            "emp_c": to_structure_CustomTextType_50(self.employee_code),
            "c_n": to_structure_CustomTextType_20(self.contact_no),
            "add": to_structure_OptionalType_CustomTextType_250(self.address),
            "desig": to_structure_OptionalType_CustomTextType_50(self.designation),
            "c_ids": to_structure_VectorType_SignedIntegerType_8(self.country_ids),
            "d_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
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
        data = parse_dictionary(data, [
            "u_id", "ug_id", "emp_n", "emp_c", "c_n",
            "add", "desig", "c_ids", "d_ids"
        ])
        user_id = data.get("u_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        user_group_id = data.get("ug_id")
        user_group_id = parse_structure_UnsignedIntegerType_32(user_group_id)
        employee_name = data.get("emp_n")
        employee_name = parse_structure_CustomTextType_50(employee_name)
        employee_code = data.get("emp_c")
        employee_code = parse_structure_CustomTextType_50(employee_code)
        contact_no = data.get("c_n")
        contact_no = parse_structure_CustomTextType_20(contact_no)
        address = data.get("add")
        address = parse_structure_OptionalType_CustomTextType_250(address)
        designation = data.get("desig")
        designation = parse_structure_OptionalType_CustomTextType_50(designation)
        country_ids = data.get("c_ids")
        country_ids = parse_structure_VectorType_SignedIntegerType_8(country_ids)
        domain_ids = data.get("d_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        return UpdateUser(
            user_id, user_group_id, employee_name, employee_code, contact_no,
            address, designation, country_ids, domain_ids
        )

    def to_inner_structure(self):
        return {
            "u_id": to_structure_SignedIntegerType_8(self.user_id),
            "ug_id": to_structure_SignedIntegerType_8(self.user_group_id),
            "emp_n": to_structure_CustomTextType_50(self.employee_name),
            "emp_c": to_structure_CustomTextType_50(self.employee_code),
            "c_n": to_structure_CustomTextType_20(self.contact_no),
            "add": to_structure_OptionalType_CustomTextType_250(self.address),
            "desig": to_structure_OptionalType_CustomTextType_50(self.designation),
            "c_ids": to_structure_VectorType_SignedIntegerType_8(self.country_ids),
            "d_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
        }

class ChangeUserStatus(Request):
    def __init__(self, user_id, is_active):
        self.user_id = user_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["u_id", "active"])
        user_id = data.get("u_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        is_active = data.get("active")
        is_active = parse_structure_Bool(is_active)
        return ChangeUserStatus(user_id, is_active)

    def to_inner_structure(self):
        return {
            "u_id": to_structure_SignedIntegerType_8(self.user_id),
            "active": to_structure_Bool(self.is_active),
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
        form_ids, is_active, no_of_users):
        self.user_group_id = user_group_id
        self.user_group_name = user_group_name
        self.form_category_id = form_category_id
        self.form_ids = form_ids
        self.is_active = is_active
        self.no_of_users = no_of_users

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_group_id", "user_group_name",
            "form_category_id", "form_ids", "is_active", "no_of_users"])
        user_group_id = data.get("user_group_id")
        user_group_id = parse_structure_UnsignedIntegerType_32(user_group_id)
        user_group_name = data.get("user_group_name")
        user_group_name = parse_structure_CustomTextType_50(user_group_name)
        form_category_id = data.get("form_category_id")
        form_category_id = parse_structure_UnsignedIntegerType_32(form_category_id)
        form_ids = data.get("form_ids")
        form_ids = parse_structure_VectorType_SignedIntegerType_8(form_ids)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        no_of_users = data.get("no_of_users")
        no_of_users = parse_structure_UnsignedIntegerType_32(no_of_users)
        return UserGroup(user_group_id, user_group_name, form_category_id,
            form_ids, is_active, no_of_users)

    def to_structure(self):
        return {
            "user_group_id": to_structure_UnsignedIntegerType_32(self.user_group_id),
            "user_group_name": to_structure_CustomTextType_50(self.user_group_name),
            "form_category_id": to_structure_SignedIntegerType_8(self.form_category_id),
            "form_ids": to_structure_VectorType_SignedIntegerType_8(self.form_ids),
            "is_active": to_structure_Bool(self.is_active),
            "no_of_users" : to_structure_UnsignedIntegerType_32(self.no_of_users)
        }

class GetUserGroupsSuccess(Response):
    def __init__(self, form_categories, forms, user_groups):
        self.form_categories = form_categories
        self.forms = forms
        self.user_groups = user_groups

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
        return {
            "form_categories": to_structure_VectorType_RecordType_core_FormCategory(self.form_categories),
            "forms": to_structure_MapType_SignedIntegerType_8_RecordType_core_Menu(self.forms),
            "user_groups": to_structure_VectorType_RecordType_admin_UserGroup(self.user_groups),
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


def _init_Response_class_map():
    classes = [GetUserGroupsSuccess, SaveUserGroupSuccess,
    GroupNameAlreadyExists, UpdateUserGroupSuccess, InvalidUserGroupId,
    ChangeUserGroupStatusSuccess, GetUsersSuccess, SaveUserSuccess,
    EmailIDAlreadyExists, ContactNumberAlreadyExists, EmployeeCodeAlreadyExists,
    InvalidUserId, UpdateUserSuccess, ChangeUserStatusSuccess, CannotDeactivateUserExists]
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

