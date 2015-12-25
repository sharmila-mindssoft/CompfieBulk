from protocol.common import *
from protocol.core import Menu

__all__=  [
	"Request", "Response"
]


# 
# Request
#

Login = RecordType("Login", [
	Field("username", USERNAME),
	Field("password", PASSWORD)
])

ForgotPassword = RecordType("ForgotPassword", [
	Field("username", USERNAME)
])

ResetTokenValidation = RecordType("ResetTokenValidation", [
	Field("reset_token", RESET_TOKEN)
])

ResetPassword = RecordType("ResetPassword", [
	Field("reset_token", RESET_TOKEN),
	Field("new_password", PASSWORD)
])

ChangePassword = RecordType("ChangePassword", [
	Field("current_password", PASSWORD),
	Field("new_password", PASSWORD)
])

Logout = RecordType("Logout", [
])

Request = VariantType("Request", [
	Login, 
	ForgotPassword, 
	ResetTokenValidation, 
	ResetPassword,
	ChangePassword,
	Logout
])


#
# Response
#

LoginSuccess = RecordType("LoginSuccess", [
	Field("user_id", USER_ID),
	Field("client_id", CLIENT_ID),
	Field("session_token", SESSION_TOKEN),
	Field("email_id", EMAIL_ID),
	Field("user_group_name", USER_GROUP_NAME),
	Field("menu", Menu),
	Field("employee_name", EMPLOYEE_NAME),
    Field("employee_code", EMPLOYEE_CODE),
    Field("contact_no", CONTACT_NUMBER),
    Field("address", ADDRESS),
    Field("designation", DESIGNATION)
])

InvalidCredentials = RecordType("InvalidCredentials", [	
])

ForgotPasswordSuccess = RecordType("ForgotPasswordSuccess", [])

InvalidUserName = RecordType("InvalidUserName", [])

ResetSessionTokenValidationSuccess = RecordType("ResetSessionTokenValidationSuccess", [])

InvalidResetToken = RecordType("InvalidResetToken", [])

ResetPasswordSuccess = RecordType("ResetPasswordSuccess", [])

ChangePasswordSuccess = RecordType("ChangePasswordSuccess", [])

InvalidCurrentPassword = RecordType("InvalidCurrentPassword", [])

LogoutSuccess = RecordType("LogoutSuccess", [])

InvalidSessionToken = RecordType("InvalidSessionToken", [	
])

Response = VariantType("Response", [
	LoginSuccess, InvalidCredentials,
	ForgotPasswordSuccess, InvalidUserName,
	ResetSessionTokenValidationSuccess, InvalidResetToken,
	ResetPasswordSuccess,
	ChangePasswordSuccess, InvalidCurrentPassword,
	LogoutSuccess, InvalidSessionToken
])