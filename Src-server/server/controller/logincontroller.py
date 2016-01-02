from corecontroller import process_user_forms
from protocol import login, core

__all__ = [
	"process_login", "process_forgot_password",
	"process_reset_token",
	"process_reset_password",
	"process_change_password",
	"process_logout"
]

def process_login(db, request):
	username = request.username
	password = request.password
	print username, password
	response = db.verify_login(username, password)
	if response is True:
		return admin_login_response()
	else :
		if bool(response):
			return user_login_response(response)
		else :
			return login.InvalidCredentials()


def user_login_response(data):
	user_id = data["user_id"]
	email_id = data["email_id"]
    session_type = 1 #web
    session_token = db.add_session(user_id, session_type)
   	employee_name = data["employee_name"]
   	employee_code = data["employee_code"]
   	contact_no = data["contact_no"]
   	address = data["address"]
   	designation = data["designation"]
   	user_group_name = data["user_group_name"]
   	form_ids = data["form_ids"]
   	menu = process_user_forms(form_ids)

   	return login.UserLoginSuccess(
   		user_id, session_token, email_id, user_group_name, 
   		menu, employee_name, employee_code, contact_no, address, designation
   	)

def admin_login_response():
	user_id = 0
	email_id = None
    session_type = 1 #web
    session_token = db.add_session(user_id, session_type)
    menu = process_user_forms("1,2,3,4")
   	employee_name = "Administrator"
   	return login.AdminLoginSuccess(user_id, session_token, email_id, menu, employee_name)

def process_forgot_password(db, request):
	return login.ForgotPasswordSuccess()

def process_reset_token(db, request):
	return login.ResetSessionTokenValidationSuccess()

def process_reset_password(db, request):
	return login.ResetPasswordSuccess()

def process_change_password(db, request):
	return login.ChangePasswordSuccess()

def process_logout(db, request):
	return login.LogoutSuccess()


