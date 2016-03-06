import json
from protocol.jsonvalidators import (parse_enum, parse_dictionary, parse_static_list, parse_bool)
from protocol.parse_structure import (
    parse_structure_CustomTextType_100,
    parse_structure_RecordType_core_Menu,
    parse_structure_CustomTextType_250,
    parse_structure_UnsignedIntegerType_32,
    parse_structure_EnumType_core_SESSION_TYPE,
    parse_structure_CustomTextType_20, 
    parse_structure_CustomTextType_50,
    parse_structure_OptionalType_CustomTextType_50,
    parse_structure_OptionalType_CustomTextType_100,
    parse_structure_OptionalType_CustomTextType_20,
    parse_structure_OptionalType_UnsignedIntegerType_32
)
from protocol.to_structure import (
    to_structure_CustomTextType_100,
    to_structure_RecordType_core_Menu, to_structure_CustomTextType_250,
    to_structure_SignedIntegerType_8,
    to_structure_EnumType_core_SESSION_TYPE,
    to_structure_OptionalType_CustomTextType_50,
    to_structure_CustomTextType_20, to_structure_CustomTextType_50,
    to_structure_OptionalType_CustomTextType_100,
    to_structure_OptionalType_CustomTextType_20,
    to_structure_OptionalType_UnsignedIntegerType_32,
    to_structure_OptionalType_CustomTextType_500,
    to_structure_Bool
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

class Login(Request):
    def __init__(self, login_type, username, password, short_name):
        self.login_type = login_type
        self.username = username
        self.password = password
        self.short_name = short_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["login_type", "username", "password"])
        login_type = data.get("login_type")
        login_type = parse_structure_EnumType_core_SESSION_TYPE(login_type)
        username = data.get("username")
        username = parse_structure_CustomTextType_100(username)
        password = data.get("password")
        password = parse_structure_CustomTextType_20(password)
        short_name = data.get("short_name")
        short_name = parse_structure_OptionalType_CustomTextType_20(short_name)
        return Login(login_type, username, password, short_name)

    def to_inner_structure(self):
        return {
            "login_type": to_structure_EnumType_core_SESSION_TYPE(self.login_type),
            "username": to_structure_CustomTextType_100(self.username),
            "password": to_structure_CustomTextType_20(self.password),
            "short_name": to_structure_OptionalType_CustomTextType_20(self.short_name),
        }

class ForgotPassword(Request):
    def __init__(self, username, short_name):
        self.username = username
        self.short_name = short_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["username", "short_name"])
        username = data.get("username")
        username = parse_structure_CustomTextType_100(username)
        short_name = data.get("short_name")
        short_name = parse_structure_OptionalType_CustomTextType_100(short_name)
        return ForgotPassword(username, short_name)

    def to_inner_structure(self):
        return {
            "username": to_structure_CustomTextType_100(self.username),
            "short_name" : to_structure_OptionalType_CustomTextType_100(self.short_name)
        }

class ResetTokenValidation(Request):
    def __init__(self, reset_token, short_name):
        self.reset_token = reset_token
        self.short_name = short_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["reset_token", "short_name"])
        reset_token = data.get("reset_token")
        reset_token = parse_structure_CustomTextType_50(reset_token)
        short_name = data.get("short_name")
        short_name = parse_structure_OptionalType_CustomTextType_50(short_name)
        return ResetTokenValidation(reset_token, short_name)

    def to_inner_structure(self):
        return {
            "reset_token": to_structure_CustomTextType_50(self.reset_token),
            "short_name":to_structure_OptionalType_CustomTextType_50(self.short_name)
        }

class ResetPassword(Request):
    def __init__(self, reset_token, new_password, short_name):
        self.reset_token = reset_token
        self.new_password = new_password
        self.short_name = short_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["reset_token", "new_password", "short_name"])
        reset_token = data.get("reset_token")
        reset_token = parse_structure_CustomTextType_50(reset_token)
        new_password = data.get("new_password")
        new_password = parse_structure_CustomTextType_20(new_password)
        short_name = data.get("short_name")
        short_name = parse_structure_OptionalType_CustomTextType_50(short_name)
        return ResetPassword(reset_token, new_password, short_name)

    def to_inner_structure(self):
        return {
            "reset_token": to_structure_CustomTextType_50(self.reset_token),
            "new_password": to_structure_CustomTextType_20(self.new_password),
            "short_name": to_structure_OptionalType_CustomTextType_50(self.short_name)
        }

class ChangePassword(Request):
    def __init__(self, current_password, new_password, session_token):
        self.current_password = current_password
        self.new_password = new_password
        self.session_token = session_token

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["current_password", "new_password", "session_token"])
        current_password = data.get("current_password")
        current_password = parse_structure_CustomTextType_20(current_password)
        new_password = data.get("new_password")
        new_password = parse_structure_CustomTextType_20(new_password)
        session_token = data.get("session_token")
        session_token = parse_structure_CustomTextType_50(session_token)
        return ChangePassword(current_password, new_password, session_token)

    def to_inner_structure(self):
        return {
            "current_password": to_structure_CustomTextType_20(self.current_password),
            "new_password": to_structure_CustomTextType_20(self.new_password),
            "session_token": to_structure_CustomTextType_50(self.session_token),
        }

class Logout(Request):
    def __init__(self, session_token):
        self.session_token = session_token

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["session_token"])
        session_token = data.get("session_token")
        session_token = parse_structure_CustomTextType_50(session_token)
        return Logout(session_token)

    def to_inner_structure(self):
        return {
            "session_token": to_structure_CustomTextType_50(self.session_token),
        }

def _init_Request_class_map():
    classes = [Login, ForgotPassword, ResetTokenValidation, ResetPassword, ChangePassword, Logout]
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

class UserLoginSuccess(Response):
    def __init__(self, user_id, session_token, email_id, user_group_name, menu, 
        employee_name, employee_code, contact_no, address, designation, client_id,
        is_admin
    ):
        self.user_id = user_id
        self.session_token = session_token
        self.email_id = email_id
        self.user_group_name = user_group_name
        self.menu = menu
        self.employee_name = employee_name
        self.employee_code = employee_code
        self.contact_no = contact_no
        self.address = address
        self.designation = designation
        self.client_id = client_id
        self.is_admin = is_admin

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_id", "session_token", "email_id", 
            "user_group_name", "menu", "employee_name", "employee_code", 
            "contact_no", "address", "designation", "client_id", "is_admin"])
        user_id = data.get("user_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        session_token = data.get("session_token")
        session_token = parse_structure_CustomTextType_50(session_token)
        email_id = data.get("email_id")
        email_id = parse_structure_CustomTextType_100(email_id)
        user_group_name = data.get("user_group_name")
        user_group_name = parse_structure_CustomTextType_50(user_group_name)
        menu = data.get("menu")
        menu = parse_structure_RecordType_core_Menu(menu)
        employee_name = data.get("employee_name")
        employee_name = parse_structure_CustomTextType_50(employee_name)
        employee_code = data.get("employee_code")
        employee_code = parse_structure_CustomTextType_50(employee_code)
        contact_no = data.get("contact_no")
        contact_no = parse_structure_CustomTextType_20(contact_no)
        address = data.get("address")
        address = parse_structure_OptionalType_CustomTextType_250(address)
        designation = data.get("designation")
        designation = parse_structure_OptionalType_CustomTextType_50(designation)
        client_id = data.get("client_id")
        client_id = parse_structure_OptionalType_UnsignedIntegerType_32(client_id)
        is_admin = data.get("is_admin")
        is_admin = parse_bool(is_admin)
        return UserLoginSuccess(
            user_id, session_token, email_id, user_group_name, menu, employee_name,
            employee_code, contact_no, address, designation, client_id, is_admin)

    def to_inner_structure(self):
        return {
            "user_id": to_structure_SignedIntegerType_8(self.user_id),
            "session_token": to_structure_CustomTextType_50(self.session_token),
            "email_id": to_structure_CustomTextType_100(self.email_id),
            "user_group_name": to_structure_CustomTextType_50(self.user_group_name),
            "menu": to_structure_RecordType_core_Menu(self.menu),
            "employee_name": to_structure_CustomTextType_50(self.employee_name),
            "employee_code": to_structure_CustomTextType_50(self.employee_code),
            "contact_no": to_structure_CustomTextType_20(self.contact_no),
            "address": to_structure_OptionalType_CustomTextType_500(self.address),
            "designation": to_structure_OptionalType_CustomTextType_50(self.designation),
            "client_id": to_structure_OptionalType_UnsignedIntegerType_32(self.client_id),
            "is_admin": to_structure_Bool(self.is_admin)
        }

class AdminLoginSuccess(Response):
    def __init__(self, user_id, session_token, email_id, menu, employee_name, client_id):
        self.user_id = user_id
        self.session_token = session_token
        self.email_id = email_id
        self.menu = menu
        self.employee_name = employee_name
        self.client_id = client_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_id", "session_token", "email_id", "menu", "employee_name"])
        user_id = data.get("user_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        session_token = data.get("session_token")
        session_token = parse_structure_CustomTextType_50(session_token)
        email_id = data.get("email_id")
        email_id = parse_structure_OptionalType_CustomTextType_100(email_id)
        menu = data.get("menu")
        menu = parse_structure_RecordType_core_Menu(menu)
        employee_name = data.get("employee_name")
        employee_name = parse_structure_CustomTextType_50(employee_name)
        client_id = data.get("client_id")
        client_id = parse_structure_OptionalType_UnsignedIntegerType_32(client_id)
        return AdminLoginSuccess(user_id, session_token, email_id, menu, employee_name)

    def to_inner_structure(self):
        return {
            "user_id": to_structure_SignedIntegerType_8(self.user_id),
            "session_token": to_structure_CustomTextType_50(self.session_token),
            "email_id": to_structure_OptionalType_CustomTextType_100(self.email_id),
            "menu": to_structure_RecordType_core_Menu(self.menu),
            "employee_name": to_structure_CustomTextType_50(self.employee_name),
            "client_id": to_structure_OptionalType_UnsignedIntegerType_32(self.client_id)
        }

class InvalidCredentials(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidCredentials()

    def to_inner_structure(self):
        return {
        }

class ForgotPasswordSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ForgotPasswordSuccess()

    def to_inner_structure(self):
        return {
        }

class InvalidUserName(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidUserName()

    def to_inner_structure(self):
        return {
        }

class ResetSessionTokenValidationSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ResetSessionTokenValidationSuccess()

    def to_inner_structure(self):
        return {
        }

class InvalidResetToken(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidResetToken()

    def to_inner_structure(self):
        return {
        }

class ResetPasswordSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ResetPasswordSuccess()

    def to_inner_structure(self):
        return {
        }

class ChangePasswordSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ChangePasswordSuccess()

    def to_inner_structure(self):
        return {
        }

class InvalidCurrentPassword(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidCurrentPassword()

    def to_inner_structure(self):
        return {
        }

class LogoutSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return LogoutSuccess()

    def to_inner_structure(self):
        return {
        }

class InvalidSessionToken(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidSessionToken()

    def to_inner_structure(self):
        return {
        }


def _init_Response_class_map():
    classes = [UserLoginSuccess, AdminLoginSuccess, InvalidCredentials, ForgotPasswordSuccess, InvalidUserName, ResetSessionTokenValidationSuccess, InvalidResetToken, ResetPasswordSuccess, ChangePasswordSuccess, InvalidCurrentPassword, LogoutSuccess, InvalidSessionToken]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()

