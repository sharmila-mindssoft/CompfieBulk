from basics.types import VectorType, RecordType, VariantType, MapType, Field
from common import (USERNAME, PASSWORD, RESET_TOKEN, USER_ID, CLIENT_ID, SESSION_TOKEN,
	EMAIL_ID, USER_GROUP_NAME, EMPLOYEE_NAME, EMPLOYEE_CODE, CONTACT_NUMBER, ADDRESS, DESIGNATION, SESSION_TOKEN)
from core import Menu

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
	Field("new_password", PASSWORD),
	Field("session_token", SESSION_TOKEN)
])

Logout = RecordType("Logout", [
	Field("session_token", SESSION_TOKEN)	
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

UserLoginSuccess = RecordType("UserLoginSuccess", [
	Field("user_id", USER_ID),
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

AdminLoginSuccess = RecordType("AdminLoginSuccess", [
	Field("user_id", USER_ID),
	Field("session_token", SESSION_TOKEN),
	Field("email_id", EMAIL_ID),
	Field("menu", Menu),
	Field("employee_name", EMPLOYEE_NAME)
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
	UserLoginSuccess, AdminLoginSuccess, InvalidCredentials,
	ForgotPasswordSuccess, InvalidUserName,
	ResetSessionTokenValidationSuccess, InvalidResetToken,
	ResetPasswordSuccess,
	ChangePasswordSuccess, InvalidCurrentPassword,
	LogoutSuccess, InvalidSessionToken
])