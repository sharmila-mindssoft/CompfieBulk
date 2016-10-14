from protocol.jsonvalidators import (
    parse_dictionary, parse_static_list, to_structure_dictionary_values)


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


class Login(Request):
    def __init__(self, login_type, username, password, short_name, ip):
        self.login_type = login_type
        self.username = username
        self.password = password
        self.short_name = short_name
        self.ip = ip

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, ["login_type", "username", "password", "ip"])
        login_type = data.get("login_type")
        username = data.get("username")
        password = data.get("password")
        short_name = data.get("short_name")
        ip = data.get("ip")
        return Login(login_type, username, password, short_name, ip)

    def to_inner_structure(self):
        return {
            "login_type": self.login_type,
            "username": self.username,
            "password": self.password,
            "short_name": self.short_name,
            "ip": self.ip
        }


class ForgotPassword(Request):
    def __init__(self, username, short_name, login_type):
        self.username = username
        self.short_name = short_name
        self.login_type = login_type

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["username", "short_name", "login_type"])
        username = data.get("username")
        short_name = data.get("short_name")
        login_type = data.get("login_type")
        return ForgotPassword(username, short_name, login_type)

    def to_inner_structure(self):
        return {
            "username": self.username,
            "short_name" : self.short_name,
            "login_type": self.login_type
        }

class ResetTokenValidation(Request):
    def __init__(self, reset_token, short_name):
        self.reset_token = reset_token
        self.short_name = short_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["reset_token", "short_name"])
        reset_token = data.get("reset_token")
        short_name = data.get("short_name")
        return ResetTokenValidation(reset_token, short_name)

    def to_inner_structure(self):
        return {
            "reset_token": self.reset_token,
            "short_name": self.short_name
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
        new_password = data.get("new_password")
        short_name = data.get("short_name")
        return ResetPassword(reset_token, new_password, short_name)

    def to_inner_structure(self):
        return {
            "reset_token": self.reset_token,
            "new_password": self.new_password,
            "short_name": self.short_name
        }

class UpdateUserProfile(Request):
    def __init__(self, contact_no, address, session_token):
        self.contact_no = contact_no
        self.address = address
        self.session_token = session_token

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["contact_no", "address", "session_token"])
        contact_no = data.get("contact_no")
        address = data.get("address")
        session_token = data.get("session_token")
        return UpdateUserProfile(contact_no, address, session_token)

    def to_inner_structure(self):
        return {
            "contact_no": self.contact_no,
            "address": self.address,
            "session_token": self.session_token
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
        new_password = data.get("new_password")
        session_token = data.get("session_token")
        return ChangePassword(current_password, new_password, session_token)

    def to_inner_structure(self):
        return {
            "current_password": self.current_password,
            "new_password": self.new_password,
            "session_token": self.session_token,
        }

class Logout(Request):
    def __init__(self, session_token):
        self.session_token = session_token

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["session_token"])
        session_token = data.get("session_token")
        return Logout(session_token)

    def to_inner_structure(self):
        return {
            "session_token": self.session_token,
        }


def _init_Request_class_map():
    classes = [
        Login, ForgotPassword, ResetTokenValidation, ResetPassword,
        ChangePassword, Logout, UpdateUserProfile
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
        print "inner before: %s " % inner
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

class UserLoginSuccess(Response):
    def __init__(
        self, user_id, session_token, email_id, user_group_name, menu,
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
        data = parse_dictionary(data, [
            "user_id", "session_token", "email_id",
            "user_group_name", "menu", "employee_name", "employee_code",
            "contact_no", "address", "designation", "client_id", "is_admin"])
        user_id = data.get("user_id")
        session_token = data.get("session_token")
        email_id = data.get("email_id")
        user_group_name = data.get("user_group_name")
        menu = data.get("menu")
        employee_name = data.get("employee_name")
        employee_code = data.get("employee_code")
        contact_no = data.get("contact_no")
        address = data.get("address")
        designation = data.get("designation")
        client_id = data.get("client_id")
        is_admin = data.get("is_admin")
        return UserLoginSuccess(
            user_id, session_token, email_id, user_group_name, menu,
            employee_name, employee_code, contact_no, address,
            designation, client_id, is_admin)

    def to_inner_structure(self):
        return {
            "user_id": self.user_id,
            "session_token": self.session_token,
            "email_id": self.email_id,
            "user_group_name": self.user_group_name,
            "menu": self.menu,
            "employee_name": self.employee_name,
            "employee_code": self.employee_code,
            "contact_no": self.contact_no,
            "address": self.address,
            "designation": self.designation,
            "client_id": self.client_id,
            "is_admin": self.is_admin
        }


class AdminLoginSuccess(Response):
    def __init__(
        self, user_id, session_token, email_id,
        menu, employee_name, client_id
    ):
        self.user_id = user_id
        self.session_token = session_token
        self.email_id = email_id
        self.menu = menu
        self.employee_name = employee_name
        self.client_id = client_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "user_id", "session_token", "email_id", "menu",
                "employee_name", "user_client_id"
            ])
        user_id = data.get("user_id")
        session_token = data.get("session_token")
        email_id = data.get("email_id")
        menu = data.get("menu")
        employee_name = data.get("employee_name")
        client_id = data.get("user_client_id")
        return AdminLoginSuccess(
            user_id, session_token, email_id, menu, employee_name, client_id)

    def to_inner_structure(self):
        print {
            "user_id": self.user_id,
            "session_token": self.session_token,
            "email_id": self.email_id,
            "menu": self.menu,
            "employee_name": self.employee_name,
            "user_client_id": self.client_id
        }
        return {
            "user_id": self.user_id,
            "session_token": self.session_token,
            "email_id": self.email_id,
            "menu": self.menu,
            "employee_name": self.employee_name,
            "user_client_id": self.client_id
        }


class InvalidCredentials(Response):
    def __init__(self, captcha_text):
        self.captcha_text = captcha_text

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["captcha_text"])
        captcha_text = data.get("captcha_text")
        return InvalidCredentials(captcha_text)

    def to_inner_structure(self):
        return {
            "captcha_text": self.captcha_text
        }

class InvalidMobileCredentials(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidMobileCredentials()

    def to_inner_structure(self):
        return {}

class ClientDatabaseNotExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ClientDatabaseNotExists()

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

class ContractExpired(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ContractExpired()

    def to_inner_structure(self):
        return {
        }

class ContractNotYetStarted(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ContractNotYetStarted()

    def to_inner_structure(self):
        return {
        }

class NotConfigured(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return NotConfigured()

    def to_inner_structure(self):
        return {
        }

class EnterDifferentPassword(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return EnterDifferentPassword()

    def to_inner_structure(self):
        return {
        }

class UpdateUserProfileSuccess(Response):
    def __init__(self, contact_no, address):
        self.contact_no = contact_no
        self.address = address

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["contact_no", "address"])
        contact_no = data.get("contact_no")
        address = data.get("address")
        return UpdateUserProfile(contact_no, address)

    def to_inner_structure(self):
        return {
            "contact_no": self.contact_no,
            "address": self.address
        }

def _init_Response_class_map():
    classes = [
        UserLoginSuccess, AdminLoginSuccess, InvalidCredentials,
        ForgotPasswordSuccess, InvalidUserName, ResetSessionTokenValidationSuccess,
        InvalidResetToken, ResetPasswordSuccess, ChangePasswordSuccess,
        InvalidCurrentPassword, LogoutSuccess, InvalidSessionToken,
        ClientDatabaseNotExists, ContractExpired, EnterDifferentPassword,
        NotConfigured, ContractNotYetStarted, UpdateUserProfileSuccess
    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()
