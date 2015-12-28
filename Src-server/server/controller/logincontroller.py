from server.database import DatabaseHandler as db
from protocol import login
__all__ = [
	"process_login"
]

def process_login(request):
	username = request.username
	password = request.password
	print username, password
	return login.ResetPasswordSuccess()
	# result = db.verify_login(username, password)
	# print result
	# if result is True:

