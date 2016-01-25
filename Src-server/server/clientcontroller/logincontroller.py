from server.controller.corecontroller import process_user_forms
from server.controller.generalcontroller import validate_user_session
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
	short_name = request.short_name
	encrypt_password = db.encrypt(password)
	client_id = db.get_client_id_from_short_name(short_name)
	response = db.verify_login(username, encrypt_password, int(client_id))
	if response is True:
		return admin_login_response(db, client_id)
	else :
		if bool(response):
			return user_login_response(db, response, client_id)
		else :
			return login.InvalidCredentials()


def user_login_response(db, data, client_id):
	user_id = data["user_id"]
	email_id = data["email_id"]
	session_type = 1 #web
	session_token = db.add_session(user_id, session_type, client_id)
	employee_name = data["employee_name"]
	employee_code = data["employee_code"]
	contact_no = data["contact_no"]
	user_group_name = data["user_group_name"]
	form_ids = data["form_ids"]
	menu = process_user_forms(db, form_ids, client_id, 0)
	return login.UserLoginSuccess(
		user_id, session_token, email_id, user_group_name, 
		menu, employee_name, employee_code, contact_no, None, None,
		client_id
	)

def admin_login_response(db, client_id):
	user_id = 0
	email_id = None
	session_type = 1 #web
	session_token = db.add_session(user_id, session_type, client_id)
	menu = process_user_forms(db, "1,2,3,4", client_id, 1)
	employee_name = "Administrator"
	return login.AdminLoginSuccess(user_id, session_token, email_id, menu, employee_name, client_id)

def process_forgot_password(db, request):
	client_id = db.get_client_id_from_short_name(request.short_name)
	user_id = db.verify_username(request.username, client_id)
	if user_id != None:
		send_reset_link(db, user_id, client_id)
		return login.ForgotPasswordSuccess()
	else:
	    return login.InvalidUserName()
	
def send_reset_link(db, user_id, client_id):
	reset_token = db.new_uuid()
	print "http://localhost:8080/ForgotPassword?reset_token=%s" % reset_token
	columns = ["user_id", "verification_code"]
	values_list = [user_id, reset_token]
	if db.insert(db.tblEmailVerification, columns, values_list, client_id):
	    if send_email():
	        return True
	    else:
	        print "Send email failed"
	else:
	    print "Saving reset token failed"

def send_email():
	return True

def process_reset_token(db, request):
	client_id = db.get_client_id_from_short_name(request.short_name)
	user_id = db.validate_reset_token(request.reset_token, client_id)
	if user_id != None:
	    return login.ResetSessionTokenValidationSuccess()
	else:
	    return login.InvalidResetToken()
	

def process_reset_password(db, request):
	client_id = db.get_client_id_from_short_name(request.short_name)
	user_id = db.validate_reset_token(request.reset_token, client_id)
	if user_id != None:
		db.update_password(request.new_password, user_id, client_id)
		db.delete_used_token(request.reset_token, client_id)
		return login.ResetPasswordSuccess()
	else:
		return login.InvalidResetToken()

def process_change_password(db, request):
	client_info = request.session_token.split("-")
	session_token = client_info[1]
	client_id = int(client_info[0])
	session_user = db.validate_session_token(client_id, session_token)
	if db.verify_password(request.current_password, session_user, client_id):
		db.update_password(request.new_password, session_user, client_id)
		return login.ChangePasswordSuccess()
	else :
		return login.InvalidCurrentPassword()
	

def process_logout(db, request):
	return login.LogoutSuccess()


