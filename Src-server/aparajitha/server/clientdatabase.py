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
		elif form == "UserPrivilege":
			tblName = self._db.tblClientUserGroups
			column = "user_group_id"
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
		elif form == "UserPrivilege":		
			tblName = self._db.tblClientUserGroups
			if field == "name":
				condition = "user_group_name ='%s' AND user_group_id != '%d'" %(value, idValue)
		elif form == "User":		
			tblName = self._db.tblClientUserDetails
			if field == "employeeCode":
				condition = "employee_code ='%s' AND user_id != '%d'" %(value, idValue)
			elif field == "contactNo":
				condition = "contact_no ='%s' AND user_id != '%d'" %(value, idValue)
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
		elif form == "UserPrivilege":
			tblName = self._db.tblClientUserGroups
			condition = "user_group_id = '%d'" % idValue
		elif form == "User":
			tblName = self._db.tblClientUserDetails
			condition = "user_id = '%d'" % idValue
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
		        	"contract_from, contract_to, contact_person,"+\
		        	" contact_no,created_on,created_by, updated_on, updated_by"
		valuesList = [(serviceProvider.serviceProviderId,serviceProvider.serviceProviderName,serviceProvider.address, serviceProvider.contractFrom, serviceProvider.contractTo,serviceProvider.contactPerson, serviceProvider.contactNo, currentTimeStamp,sessionUser, currentTimeStamp, sessionUser)]
		updateColumnsList = ["service_provider_name", "address", "contract_from",
		 					"contract_to", "contact_person", "contact_no", 
		 					"updated_on", "updated_by"]
		return self._db.onDuplicateKeyUpdate(self._db.tblServiceProviders, columns, valuesList, updateColumnsList)

	def changeServiceProviderStatus(self, serviceProviderId, isActive,
		sessionUser):
		currentTimeStamp = currentTimestamp()
		columns = ["is_active", "updated_on" , "updated_by"]
		values = [isActive, currentTimeStamp, sessionUser]
		condition = "service_provider_id='%d'" % serviceProviderId
		return self._db.update(self._db.tblServiceProviders, 
        	columns, values, condition)

#
# User Groups
#
	def getUserGroupDetails(self):
		columns = "user_group_id, user_group_name,form_type, "+\
                    "form_ids, is_active"
		condition = "1"
		rows = self._db.getData(self._db.tblClientUserGroups, columns, condition)
		return rows

	def getUserGroups(self):
		columns = "user_group_id, user_group_name, is_active"
		condition = "1"
		rows = self._db.getData(self._db.tblClientUserGroups, columns, condition)
		return rows

	def saveUserPrivilege(self, userPrivilege, sessionUser):
		currentTimeStamp = currentTimestamp()
		columns = "user_group_id, user_group_name,form_type, form_ids, "+\
		"is_active, created_on, created_by, updated_on, updated_by"
		formIds = ",".join(str(x) for x in userPrivilege.formIds)
		valuesList =  [(userPrivilege.userGroupId, userPrivilege.userGroupName, userPrivilege.formType,
		 formIds, userPrivilege.isActive, currentTimeStamp,sessionUser,currentTimeStamp, sessionUser)]
		updateColumnsList = ["user_group_name","form_type", "form_ids", "updated_on", "updated_by"]
		return self._db.onDuplicateKeyUpdate(self._db.tblClientUserGroups, columns, valuesList, updateColumnsList)

	def changeUserPrivilegeStatus(self, userGroupId, isActive, sessionUser):
		currentTimeStamp = currentTimestamp()
		columns = ["is_active", "updated_on" , "updated_by"]
		values = [isActive, currentTimeStamp, sessionUser]
		condition = "user_group_id='%d'" % userGroupId
		return self._db.update(self._db.tblClientUserGroups, columns, values, condition)

#
#	Users
#

	def getClientUserDetailsList(self):
		columns = "user_id, email_id, user_group_id, employee_name, employee_code,"+\
		" contact_no, seating_unit_id, user_level, country_ids,"+\
		" domain_ids, unit_ids, is_admin, is_service_provider, is_active"
		condition = "1"
		rows = self._db.getData(self._db.tblClientUserDetails, columns, condition)
		return rows

	def getClientUserList(self):
		columns = "user_id, employee_name, employee_code, is_active"
		condition = "1"
		rows = self._db.getData(self._db.tblClientUserDetails, columns, condition)
		return rows

	def saveUserDetail(self, user, sessionUser):
		currentTimeStamp = currentTimestamp()
		columns = "user_id, email_id, user_group_id, employee_name, employee_code,"+\
                    " contact_no, seating_unit_id, user_level, country_ids,"+\
                    " domain_ids, unit_ids, is_admin, is_service_provider, "+\
                    " created_by, created_on, updated_by,updated_on"
		valuesList = [ (user.userId, user.emailId, user.userGroupId, user.employeeName,
                       	user.employeeCode, user.contactNo, user.seatingUnitId, 
                        user.userLevel, ",".join(str(x) for x in user.countryIds), 
                        ",".join(str(x) for x in user.domainIds), 
                        ",".join(str(x) for x in user.unitIds), user.isAdmin,
                        user.isServiceProvider, sessionUser,currentTimeStamp,
                        sessionUser, currentTimeStamp)]
		updateColumnsList = [ "user_group_id", "employee_name", "employee_code",
                            "contact_no", "seating_unit_id", "user_level", "country_ids",
                            "domain_ids", "unit_ids", "is_admin", "is_service_provider",
                            "updated_on", "updated_by"]
		return self._db.onDuplicateKeyUpdate(self._db.tblClientUserDetails, columns, 
        	valuesList, updateColumnsList)

	def updateUserDetail(self, user,sessionUser):
		currentTimeStamp = currentTimestamp()
		columns = ["user_group_id", "employee_name", "employee_code",
		"contact_no", "seating_unit_id", "user_level", "country_ids",
		"domain_ids", "unit_ids", "is_admin", "is_service_provider",
		"updated_by", "updated_on"]
		valuesList = [ user.userGroupId, user.employeeName, user.employeeCode,
						user.contactNo, user.seatingUnitId, user.userLevel,
						",".join(str(x) for x in user.countryIds), 
                        ",".join(str(x) for x in user.domainIds), 
                        ",".join(str(x) for x in user.unitIds), user.isAdmin,
                        user.isServiceProvider, sessionUser, currentTimeStamp]
		condition = "user_id='%d'" % user.userId
		return self._db.update(self._db.tblClientUserDetails, columns, valuesList,
			condition)

	def changeUserDetailStatus(self, userId, isActive, sessionUser):
		columns = ["is_active", "updated_on" , "updated_by"]
		values = [isActive, currentTimestamp(), sessionUser]
		condition = "user_id='%d'" % userId
		return self._db.update(self._db.tblClientUserDetails, columns, values,
			condition) 

	def changeAdminStatus(self, userId, isAdmin, sessionUser):
		columns = ["is_admin", "updated_on" , "updated_by"]
		values = [isAdmin, currentTimestamp(), sessionUser]
		condition = "user_id='%d'" % userId
		return self._db.update(self._db.tblClientUserDetails, columns, values,
			condition)
#
#	Country
#
	def getCountries(self):
		columns = "country_id, country_name, is_active"
		condition = " is_active = '1' "
		rows = self._db.getData(self._db.tblCoutries,columns, 
			condition)
		return rows		

#
#	Domain
#
	def getDomains(self):
		columns = "domain_id, domain_name, is_active"
		condition = " is_active = '1' "
		rows = self._db.getData(self._db.tblDomains,columns, 
			condition)
		return rows	

#
#	Business Group
#

	def getBusinessGroups(self):
		columns = "business_group_id, business_group_name"
		condition = "1"
		rows = self._db.getData(self._db.tblBusinessGroup,columns, 
			condition)
		return rows

#
#	Legal Entity
#
	def getLegalEntities(self):
		columns = "legal_entity_id, legal_entity_name, business_group_id"
		condition = "1"
		rows = self._db.getData(self._db.tblLegalEntity,columns, condition)
		return rows
#
# 	Divisions
#

	def getDivisions(self):
		columns = "division_id, division_name, legal_entity_id, business_group_id"
		condition = "1"
		rows = self._db.getData(self._db.tblDivision,columns, condition)
		return rows

#
#	Units
#
	def getUnits(self):
		columns = "unit_id, division_id, legal_entity_id, "+\
                   "business_group_id, unit_code, unit_name,"+\
                   " country_id, address, domain_ids"
		condition = " is_active = '1' "                 
		rows = self._db.getData(self._db.tblUnit, columns, condition)
		return rows


