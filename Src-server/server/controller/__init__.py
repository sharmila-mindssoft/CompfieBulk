from knowledgecontroller import process_save_country
from protocol import admin

class Controller:
	def processAdminRequest(self, request):
		if type(request) is admin.GetUserGroups:
			print "got user group request"
			return admin.GetUserGroupsSuccess()
		else:
			print "invalid request"
