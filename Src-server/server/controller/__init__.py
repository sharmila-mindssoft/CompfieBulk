from knowledgemastercontroller import *
from logincontroller import *
from generalcontroller import *

from protocol import admin

class Controller:
	def processAdminRequest(self, request):
		if type(request) is admin.GetUserGroups:
			print "got user group request"
			return admin.GetUserGroupsSuccess()
		else:
			print "invalid request"

