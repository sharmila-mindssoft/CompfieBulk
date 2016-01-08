from corecontroller import process_user_forms
from generalcontroller import validate_user_session
from protocol import login, core


__all__ = [
	"process_login_request",
	"process_login", "process_forgot_password",
	"process_reset_token",
	"process_reset_password",
	"process_change_password",
	"process_logout"
]

def process_login_request(request, db) :
	if type(request) is login.Login:
		return process_login(db, request)

	if type(request) is login.ForgotPassword :
		return process_forgot_password(db, request)

	if type(request) is login.ResetTokenValidation :
		return process_reset_token(db, request)

	if type(request) is login.ResetPassword :
		return process_reset_password(db, request)

	if type(request) is login.ChangePassword :
		return process_change_password(db, request)

	if type(request) is login.Logout:
		return process_logout(db, request)
	

def process_login(db, request):
	login_type = request.login_type
	username = request.username
	password = request.password
	encrypt_password = db.encrypt(password)
	response = db.verify_login(username, encrypt_password)
	if response is True:
		return admin_login_response(db)
	else :
		if bool(response):
			return user_login_response(db, response)
		else :
			return login.InvalidCredentials()


def user_login_response(db, data):
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
	menu = process_user_forms(db, form_ids)
	print menu
	return login.UserLoginSuccess(
		int(user_id), session_token, email_id, user_group_name, 
		menu, employee_name, employee_code, contact_no, address, designation
	)

def admin_login_response(db):
	user_id = 0
	email_id = None
	session_type = 1 #web
	session_token = db.add_session(user_id, session_type)
	menu = process_user_forms(db, "1,2,3,4")
	print menu
	employee_name = "Administrator"
	return login.AdminLoginSuccess(user_id, session_token, email_id, menu, employee_name)

def process_forgot_password(db, request):
	self.url = url
	if db.validate_username(request.username):
		send_reset_link()
		return login.ForgotPasswordSuccess()
	else:
	    return login.InvalidUsername()
	

def process_reset_token(db, request):
	return login.ResetSessionTokenValidationSuccess()

def process_reset_password(db, request):
	return login.ResetPasswordSuccess()

def process_change_password(db, request):
	session_user = db.validate_session_token(request.session_token)
	if db.verify_password(request.current_password, session_user):
		db.update_password(request.new_password, session_user)
		return login.ChangePasswordSuccess()
	else :
		return login.InvalidCurrentPassword()
	

def process_logout(db, request):
	return login.LogoutSuccess()


