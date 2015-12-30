from protocol import login
__all__ = [
	"process_login", "process_forgot_password",
	"process_reset_token",
	"process_reset_password",
	"process_change_password",
	"process_logout"
]

def process_login(db, request):
	pass
	username = request.username
	password = request.password
	print username, password
	return login.InvalidCredentials()
	# return login.ResetPasswordSuccess()
	# result = db.verify_login(username, password)
	# print result
	
	# if result is True:

def user_login_response(request):
	pass

def admin_login_response(request):
	pass

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


