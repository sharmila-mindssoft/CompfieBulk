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

class CheckRegistrationToken(Request):
    def __init__(self, reset_token):
        self.reset_token = reset_token

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["reset_token"])
        reset_token = data.get("reset_token")
        return CheckRegistrationToken(reset_token)

    def to_inner_structure(self):
        return {
            "reset_token": self.reset_token,
        }

class SaveRegistraion(Request):
    def __init__(self, token, username, password, captcha):
        self.token = token
        self.username = username
        self.password = password
        self.captcha = captcha

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["token", "uname", "pword", "captcha"])
        token = data.get("token")
        username = data.get("uname")
        pword = data.get("pword")
        captcha = data.get("captcha")
        return SaveRegistraion(token, username, pword, captcha)

    def to_inner_structure(self):
        return {
            "token": self.token,
            "uname": self.username,
            "pword": self.password,
            "captcha": self.captcha
        }

class CheckUsername(Request):
    def __init__(self, username):
        self.username = username

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["uname"])
        username = data.get("uname")
        return CheckUsername(username)

    def to_inner_structure(self):
        return {
            "uname": self.username,
        }

def _init_Request_class_map():
    classes = [
        Login, ForgotPassword, ResetTokenValidation, ResetPassword,
        ChangePassword, Logout, UpdateUserProfile, CheckRegistrationToken,
        SaveRegistraion, CheckUsername
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

class UserLoginSuccess(Response):
    def __init__(
        self, user_id, session_token, email_id, user_group_name, menu,
        employee_name, employee_code, contact_no, address, designation, client_id,
        is_admin, username, mobile_no, m_count, s_count
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
        self.username = username
        self.mobile_no = mobile_no
        self.m_count = m_count
        self.s_count = s_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "user_id", "session_token", "email_id",
            "user_group_name", "menu", "employee_name", "employee_code",
            "contact_no", "address", "designation", "user_client_id", "is_admin", "username", "mobile_no",
            "m_count", "s_count"])
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
        client_id = data.get("user_client_id")
        is_admin = data.get("is_admin")
        username = data.get("username")
        mobile_no = data.get("mobile_no")
        return UserLoginSuccess(
            user_id, session_token, email_id, user_group_name, menu,
            employee_name, employee_code, contact_no, address,
            designation, client_id, is_admin, username, mobile_no)

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
            "user_client_id": self.client_id,
            "is_admin": self.is_admin,
            "username": self.username,
            "mobile_no": self.mobile_no,
            "m_count": self.m_count,
            "s_count": self.s_count
        }

class AdminLoginSuccess(Response):
    def __init__(
        self, user_id, session_token, email_id,
        menu, employee_name, client_id, m_count, s_count
    ):
        self.user_id = user_id
        self.session_token = session_token
        self.email_id = email_id
        self.menu = menu
        self.employee_name = employee_name
        self.client_id = client_id
        self.m_count = m_count
        self.s_count = s_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "user_id", "session_token", "email_id", "menu",
                "employee_name", "user_client_id", "m_count", "s_count"
            ])
        user_id = data.get("user_id")
        session_token = data.get("session_token")
        email_id = data.get("email_id")
        menu = data.get("menu")
        employee_name = data.get("employee_name")
        client_id = data.get("user_client_id")
        m_count = data.get("m_count")
        s_count = data.get("s_count")
        return AdminLoginSuccess(
            user_id, session_token, email_id, menu, employee_name, client_id, m_count, s_count)

    def to_inner_structure(self):

        return {
            "user_id": self.user_id,
            "session_token": self.session_token,
            "email_id": self.email_id,
            "menu": self.menu,
            "employee_name": self.employee_name,
            "user_client_id": self.client_id,
            "m_count": self.m_count,
            "s_count": self.s_count
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


class DisabledUser(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return DisabledUser()

    def to_inner_structure(self):
        return {}


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

class CurrentandNewPasswordSame(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CurrentandNewPasswordSame()

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

class CheckRegistrationTokenSuccess(Response):
    def __init__(self, captcha, is_register):
        self.captcha = captcha
        self.is_register = is_register

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["captcha", "is_register"])
        captcha = data.get("captcha")
        is_register = data.get("is_register")
        return CheckRegistrationTokenSuccess(captcha, is_register)

    def to_inner_structure(self):
        return {
            "captcha": self.captcha,
            "is_register": self.is_register
        }


class SaveRegistraionSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveRegistraionSuccess()

    def to_inner_structure(self):
        return {
        }

class InvalidCaptcha(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidCaptcha()

    def to_inner_structure(self):
        return {
        }

class CheckUsernameSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CheckUsernameSuccess()

    def to_inner_structure(self):
        return {
        }

class UsernameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UsernameAlreadyExists()

    def to_inner_structure(self):
        return {
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


def _init_Response_class_map():
    classes = [
        DisabledUser,
        UserLoginSuccess, AdminLoginSuccess, InvalidCredentials,
        ForgotPasswordSuccess, InvalidUserName, ResetSessionTokenValidationSuccess,
        InvalidResetToken, ResetPasswordSuccess, ChangePasswordSuccess,
        InvalidCurrentPassword, LogoutSuccess, InvalidSessionToken,
        ClientDatabaseNotExists, ContractExpired, EnterDifferentPassword,
        NotConfigured, ContractNotYetStarted, UpdateUserProfileSuccess,
        CheckRegistrationTokenSuccess, InvalidCaptcha,
        SaveRegistraionSuccess, CheckUsernameSuccess, UsernameAlreadyExists,
        CurrentandNewPasswordSame,
        InvalidPassword
    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()
