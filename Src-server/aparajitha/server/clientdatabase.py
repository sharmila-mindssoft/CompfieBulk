from aparajitha.server.database import Database 
from aparajitha.server.clientmodels import *
from aparajitha.misc.dates import *

class ClientDatabase(object) :
	def __init__(self, db) :
		self._db = Database(db)

	def test(self) :
		query = "SHOW TABLES;"
		print self._db.executeAndReturn(query)
		return True

#
# 	Common
#
	def generateNewId(self, form):
		tblName = None
		column = None
		if form == "ServiceProvider":
			tblName = self._db.tblServiceProviders
			column = "service_provider_id"
		else:
			print "Error : Cannot generate new id for form %s" % form

		return self._db.generateNewId(tblName, column)

	def isDuplicate(self, form, field, value, idValue):
		tblName = None
		condition = None
		if form == "ServiceProvider":
			tblName = self._db.tblServiceProviders
			if field == "name":
				condition = "service_provider_name ='%s' AND service_provider_id != '%d'" %(
           value, idValue)
			elif field == "contactNo":
				condition = "contact_no ='%s' AND service_provider_id != '%d'" % (
					value, idValue)		
		else:
			print "Error : Duplicate Validation for form %s not exists" % form
			return False

		if tblName == None and condition == None:
			print "Error : Duplicate Validation for field %s in form %s not exists" %(
					field, form)
			return False
		else:
			return self._db.isAlreadyExists(tblName, condition)

	def isIdInvalid(self, form, idValue):
		tblName = None
		condition = None
		if form == "ServiceProvider":
			tblName = self._db.tblServiceProviders
			condition = "service_provider_id = '%d'" % idValue
		else:
			print "Error: Id Validation not exists for form %s" % form

		return not self._db.isAlreadyExists(tblName, condition)
#
# Service Provider
#
	def getServiceProviders(self):
		columns = "service_provider_id, service_provider_name, address, contract_from,"+\
                "contract_to, contact_person, contact_no, is_active"
		condition = "1"
		rows = self._db.getData(self._db.tblServiceProviders, columns, condition)
		return rows

	def saveServiceProvider(self, serviceProvider, sessionUser):
		currentTimeStamp = currentTimestamp()
		columns = "service_provider_id, service_provider_name, address, "+\
		        	"contract_from, contract_to, contact_person, contact_no, "+\
		        	"created_on,created_by, updated_on, updated_by"
		valuesList = [(serviceProvider.serviceProviderId,serviceProvider.serviceProviderName,
				        serviceProvider.address, serviceProvider.contractFrom, serviceProvider.contractTo,
					    serviceProvider.contactPerson, serviceProvider.contactNo, currentTimeStamp,
					    sessionUser, currentTimeStamp, sessionUser)]
		updateColumnsList = ["service_provider_name", "address", "contract_from",
		 					"contract_to", "contact_person", "contact_no", 
		 					"updated_on", "updated_by"]
		return self._db.onDuplicateKeyUpdate(self._db.tblServiceProviders, columns, 
											valuesList, updateColumnsList)

	def changeServiceProviderStatus(self, serviceProviderId, isActive,
		sessionUser):
		currentTimeStamp = currentTimestamp()
		columns = ["is_active", "updated_on" , "updated_by"]
		values = [isActive, currentTimeStamp, sessionUser]
		condition = "service_provider_id='%d'" % serviceProviderId
		return self._db.update(self._db.tblServiceProviders, 
        	columns, values, condition)