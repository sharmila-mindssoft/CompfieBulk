import json
from protocol.jsonvalidators import (parse_enum, parse_dictionary, parse_static_list)
from protocol.parse_structure import (
    parse_structure_CustomTextType_100,
    parse_structure_RecordType_core_Menu,
    parse_structure_CustomTextType_250,
    parse_structure_SignedIntegerType_8,
    parse_structure_CustomTextType_20, parse_structure_CustomTextType_50
)
from protocol.to_structure import (
    to_structure_CustomTextType_100,
    to_structure_RecordType_core_Menu, to_structure_CustomTextType_250,
    to_structure_SignedIntegerType_8, to_structure_CustomTextType_20,
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
        print data
        data = parse_static_list(data, 2)
        print data
        name, data = data
        if _Request_class_map.get(name) is None:
            msg = "invalid request: " + name
            raise ValueError(msg)
        return _Request_class_map[name].parse_inner_structure(data)

    @staticmethod
    def parse_inner_structure(data):
        raise NotImplementedError

class Login(Request):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["username", "password"])
        username = data.get("username")
        username = parse_structure_CustomTextType_100(username)
        password = data.get("password")
        password = parse_structure_CustomTextType_20(password)
        return Login(username, password)

    def to_inner_structure(self):
        return {
            "username": to_structure_CustomTextType_100(self.username),
            "password": to_structure_CustomTextType_20(self.password),
        }

class ForgotPassword(Request):
    def __init__(self, username):
        self.username = username

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["username"])
        username = data.get("username")
        username = parse_structure_CustomTextType_100(username)
        return ForgotPassword(username)

    def to_inner_structure(self):
        return {
            "username": to_structure_CustomTextType_100(self.username),
        }

class ResetTokenValidation(Request):
    def __init__(self, reset_token):
        self.reset_token = reset_token

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["reset_token"])
        reset_token = data.get("reset_token")
        reset_token = parse_structure_CustomTextType_50(reset_token)
        return ResetTokenValidation(reset_token)

    def to_inner_structure(self):
        return {
            "reset_token": to_structure_CustomTextType_50(self.reset_token),
        }

class ResetPassword(Request):
    def __init__(self, reset_token, new_password):
        self.reset_token = reset_token
        self.new_password = new_password

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["reset_token", "new_password"])
        reset_token = data.get("reset_token")
        reset_token = parse_structure_CustomTextType_50(reset_token)
        new_password = data.get("new_password")
        new_password = parse_structure_CustomTextType_20(new_password)
        return ResetPassword(reset_token, new_password)

    def to_inner_structure(self):
        return {
            "reset_token": to_structure_CustomTextType_50(self.reset_token),
            "new_password": to_structure_CustomTextType_20(self.new_password),
        }

class ChangePassword(Request):
    def __init__(self, current_password, new_password):
        self.current_password = current_password
        self.new_password = new_password

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["current_password", "new_password"])
        current_password = data.get("current_password")
        current_password = parse_structure_CustomTextType_20(current_password)
        new_password = data.get("new_password")
        new_password = parse_structure_CustomTextType_20(new_password)
        return ChangePassword(current_password, new_password)

    def to_inner_structure(self):
        return {
            "current_password": to_structure_CustomTextType_20(self.current_password),
            "new_password": to_structure_CustomTextType_20(self.new_password),
        }

class Logout(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return Logout()

    def to_inner_structure(self):
        return {
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
    def __init__(self, user_id, client_id, session_token, email_id, user_group_name, menu, employee_name, employee_code, contact_no, address, designation):
        self.user_id = user_id
        self.client_id = client_id
        self.session_token = session_token
        self.email_id = email_id
        self.user_group_name = user_group_name
        self.menu = menu
        self.employee_name = employee_name
        self.employee_code = employee_code
        self.contact_no = contact_no
        self.address = address
        self.designation = designation

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_id", "client_id", "session_token", "email_id", "user_group_name", "menu", "employee_name", "employee_code", "contact_no", "address", "designation"])
        user_id = data.get("user_id")
        user_id = parse_structure_SignedIntegerType_8(user_id)
        client_id = data.get("client_id")
        client_id = parse_structure_SignedIntegerType_8(client_id)
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
        address = parse_structure_CustomTextType_250(address)
        designation = data.get("designation")
        designation = parse_structure_CustomTextType_50(designation)
        return LoginSuccess(user_id, client_id, session_token, email_id, user_group_name, menu, employee_name, employee_code, contact_no, address, designation)

    def to_inner_structure(self):
        return {
            "user_id": to_structure_SignedIntegerType_8(self.user_id),
            "client_id": to_structure_SignedIntegerType_8(self.client_id),
            "session_token": to_structure_CustomTextType_50(self.session_token),
            "email_id": to_structure_CustomTextType_100(self.email_id),
            "user_group_name": to_structure_CustomTextType_50(self.user_group_name),
            "menu": to_structure_RecordType_core_Menu(self.menu),
            "employee_name": to_structure_CustomTextType_50(self.employee_name),
            "employee_code": to_structure_CustomTextType_50(self.employee_code),
            "contact_no": to_structure_CustomTextType_20(self.contact_no),
            "address": to_structure_CustomTextType_250(self.address),
            "designation": to_structure_CustomTextType_50(self.designation),
        }

class AdminLoginSuccess(Response):
    def __init__(self, user_id, session_token, email_id, menu, employee_name):
        self.user_id = user_id
        self.session_token = session_token
        self.email_id = email_id
        self.menu = menu
        self.employee_name = employee_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_id", "session_token", "email_id", "menu", "employee_name"])
        user_id = data.get("user_id")
        user_id = parse_structure_SignedIntegerType_8(user_id)
        session_token = data.get("session_token")
        session_token = parse_structure_CustomTextType_50(session_token)
        email_id = data.get("email_id")
        email_id = parse_structure_CustomTextType_100(email_id)
        menu = data.get("menu")
        menu = parse_structure_RecordType_core_Menu(menu)
        employee_name = data.get("employee_name")
        employee_name = parse_structure_CustomTextType_50(employee_name)
        return LoginSuccess(user_id, session_token, email_id, menu, employee_name)

    def to_inner_structure(self):
        return {
            "user_id": to_structure_SignedIntegerType_8(self.user_id),
            "session_token": to_structure_CustomTextType_50(self.session_token),
            "email_id": to_structure_CustomTextType_100(self.email_id),
            "menu": to_structure_RecordType_core_Menu(self.menu),
            "employee_name": to_structure_CustomTextType_50(self.employee_name),
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

