import os
from aparajitha.server.knowledgedatabase import KnowledgeDatabase
from aparajitha.model.common import validate_data
from aparajitha.model import protocol
from aparajitha.server.knowledgemodels import *
from aparajitha.server.clientmodels import *
import json
import uuid

class APIHandler(object):
	def __init__(self):
		self._request_map = {
			"Login": self._login,
			"Logout": self._logout,
			"GetDomains": self._get_domain_list,
			"SaveDomain": self._save_domain,
			"UpdateDomain": self._update_domain,
			"ChangeDomainStatus": self._change_domain_status,
			"GetCountries": self._get_country_list,
			"SaveCountry": self._save_country,
			"UpdateCountry": self._update_country,
			"ChangeCountryStatus": self._change_country_status,
			"GetIndustries": self._get_industry_list,
			"SaveIndustry": self._save_industry,
			"UpdateIndustry": self._update_industry,
			"ChangeIndustryStatus": self._change_industry_status,
			"GetStatutoryNatures": self._get_statutory_nature_list,
			"SaveStatutoryNature": self._save_statutory_nature,
			"UpdateStatutoryNature": self._update_statutory_nature,
			"ChangeStatutoryNatureStatus": self._change_statutory_nature_status,
			"GetStatutoryLevels": self._get_statutory_levels_list,
			"SaveStatutoryLevels": self._save_statutory_levels,
			"GetGeographyLevels": self._get_geography_levels_list,
			"SaveGeographyLevels": self._save_geography_levels,
			"GetGeographies": self._get_geographies,
			"SaveGeography": self._save_geography,
			"UpdateGeography": self._update_geography,
			"ChangeGeographyStatus": self._change_geography_status,
			"GeographyReport": self._get_geography_report,
			"SaveStatutory": self._save_statutories,
			"UpdateStatutory": self._update_statutories,
			"GetStatutoryMappings": self._get_statutory_mappings,
			"SaveStatutoryMapping": self._save_statutory_mappings,
			"UpdateStatutoryMapping": self._update_statutory_mappings,
			"ChangeStatutoryMappingStatus": self._change_statutory_mappings_status,
			"ApproveStatutoryMapping": self._change_approval_status
			"GetUserGroups": self._get_user_groups,
			"SaveUserGroup": self._save_user_group,
			"UpdateUserGroup": self._update_user_group,
			"ChangeUserGroupStatus": self._change_user_group_status,
			"GetUsers": self._get_users,
			"SaveUser": self._save_user,
			"UpdateUser": self._update_user,
			"ChangeUserStatus": self._change_admin_user_status,
			"ChangePassword": self._change_password,
			"ForgotPassword": self._forgot_password,
			"ResetTokenValidation": self._validate_reset_token,
			"ResetPassword": self._reset_password,
			"SaveClientGroup": self._save_client_group,
			"UpdateClientGroup": self._update_client_group,
			"ChangeClientGroupStatus": self._change_client_group_status,
			"GetClientGroups": self._get_client_groups
		}

	def _success_response(self, response, response_option, data) :
		response = getattr(protocol, response)
		return {"protocol": response, "data": [response_option, data]}

	def _failure_response(self, response, option) :
		response = getattr(protocol, response)
		return {"protocol": response, "data": [option, {}]}

	def _is_protocol_without_session(self, option) :
		protocols = [
			"Login"
		]
		if option in protocols :
			return True
		return False

	def process(self, db, session_id, request) :
		request_option = request[0]
		request_data = request[1]
		handler = self._request_map[request_option]
		if self._is_protocol_without_session(request_option) :
			return handler(db, request_data)
		user_id = db.get_session_user_id(session_id)
		if user_id is None :
			return self._failure_response(
				request_option + "Response", "InvalidSession"
			)
		if request_option == u"Logout" :
			return handler(db, session_id, request_data)
		user = db.get_user(user_id)
		return handler(db, user, request_data)


	#
	# Login, Logout
	#

	def _login(self, db, request) :
		email, password = request["username"], request["password"]
		email = email.lower()
		user_id = db.get_user_id(email)
		if user_id is None :
			return self._failure_response("LoginResponse", "LoginFailed")
		user = db.match_password(user_id, password)
		if user is None :
			return self._failure_response("LoginResponse", "LoginFailed")
		user = user[0]
		user_details = db.get_user_details(user_id, user["client_id"])
		if user_details is None :
			return self._failure_response("LoginResponse", "LoginFailed")
		session_id = db.add_session(user_id)
		response_data = {
			"session_token": session_id,
			"user": {
				"user_id": user_id,
				"client_id": int(user["client_id"]),
				"email_id": str(email),
				"category": user_details["category"],
				"user_group_name": user_details["user_group_name"],
				"employee_name": user_details["employee_name"],
				"employee_code": user_details["employee_code"],
				"contact_no": user_details["contact_no"],
				"address": user_details["address"],
				"designation": user_details["designation"]
			},
			"menu": user_details["menu"]
		}
		return self._success_response(
			"LoginResponse", "LoginSuccess", response_data
		)

	def _logout(self, db, session_id, request) :
		db.remove_session(session_id)
		return self._success_response(
			"LogoutResponse", "LogoutSuccess", {}
		)

	#
	# Domain
	#
	def _get_domains(self, db) :
		domain_list = []
		_domains = db.get_domains()
		for row in _domains :
			domain = Domain(int(row[0]), row[1], row[2])
			domain_list.append(domain.toStructure())
		return domain_list

	def _get_domain_list(self, db, user, request) :
		domain_list = self._get_domains(db)     
		return self._success_response( "GetDomainsResponse", "GetDomainsSuccess",
			{"domains": domain_list}
		)

	def _save_domain(self, db, user, request) :
		domain_name = request["domain_name"]
		is_duplicate = db.check_duplicate_domain(domain_name, None)
		if is_duplicate :
			return self._failure_response("SaveDomainResponse", "DomainNameAlreadyExists")
		else :
			db.add_domain(domain_name, user["user_id"])
			return self._success_response("SaveDomainResponse", "SaveDomainSuccess", {})

	def _update_domain(self, db, user, request) :
		domain_id = request["domain_id"]
		domain_name = request["domain_name"]
		is_duplicate = db.check_duplicate_domain(domain_name, domain_id)
		if is_duplicate :
			return self._failure_response("UpdateDomainResponse", "DomainNameAlreadyExists")
		else :
			if (db.update_domain(domain_id, domain_name, user["user_id"])):
				return self._success_response("UpdateDomainResponse", "UpdateDomainSuccess", {})
			else :
				return self._failure_response("UpdateDomainResponse", "InvalidDomainId")

	def _change_domain_status(self, db, user, request) :
		domain_id = request["domain_id"]
		is_active = request["is_active"]
		if (db.update_domain_status(domain_id, is_active, user["user_id"])) :
			return self._success_response("ChangeDomainStatusResponse", "ChangeDomainStatusSuccess", {})
		else :
			return self._failure_response("ChangeDomainStatusResponse", "InvalidDomainId")

	def _get_countries(self, db) :
		country_list = []
		_countries = db.get_countries()
		for row in _countries :
			country = Country(int(row[0]), row[1], row[2])
			country_list.append(country.toStructure())
		return country_list

	def _get_country_list(self, db, user, request) :
		country_list = self.get_countries(db)
		return self._success_response( "GetCountriesResponse", "GetCountriesSuccess",
			{"countries": country_list}
		)

	def _save_country(self, db, user, request) :
		country_name = request["country_name"]
		is_duplicate = db.check_duplicate_country(country_name, None)
		if is_duplicate :
			return self._failure_response("SaveCountryResponse", "CountryNameAlreadyExists")
		else :
			db.add_country(country_name, user["user_id"])
			return self._success_response("SaveCountryResponse", "SaveCountrySuccess", {})

	def _update_country(self, db, user, request) :
		country_id = request["country_id"]
		country_name = request["country_name"]
		is_duplicate = db.check_duplicate_country(country_name, country_id)
		if is_duplicate :
			return self._failure_response("UpdateCountryResponse", "CountryNameAlreadyExists")
		else :
			if (db.update_country(country_id, country_name, user["user_id"])):
				return self._success_response("UpdateCountryResponse", "UpdateCountrySuccess", {})
			else :
				return self._failure_response("UpdateCountryResponse", "InvalidCountryId")

	def _change_country_status(self, db, user, request) :
		country_id = request["country_id"]
		is_active = request["is_active"]
		if (db.update_country_status(country_id, is_active, user["user_id"])) :
			return self._success_response("ChangeCountryStatusResponse", "ChangeCountryStatusSuccess", {})
		else :
			return self._failure_response("ChangeCountryStatusResponse", "InvalidCountryId")

	def _get_industries(self, db) :
		industry_list = []
		_industries = db.get_industries()
		for row in _industries :
			industry = Industry(int(row[0]), row[1], row[2])
			industry_list.append(industry.toStructure())
		return industry_list

	def _get_industry_list(self, db, user, request) :
		industry_list = self._get_industries(db)
		return self._success_response( "GetIndustriesResponse", "GetIndustriesSuccess",
			{"industries": industry_list}
		)

	def _save_industry(self, db, user, request) :
		industry_name = request["industry_name"]
		is_duplicate = db.check_duplicate_industry(industry_name, None)
		if is_duplicate :
			return self._failure_response("SaveIndustryResponse", "IndustryNameAlreadyExists")
		else :
			db.add_industry(industry_name, user["user_id"])
			return self._success_response("SaveIndustryResponse", "SaveIndustrySuccess", {})

	def _update_industry(self, db, user, request) :
		industry_id = request["industry_id"]
		industry_name = request["industry_name"]
		is_duplicate = db.check_duplicate_industry(industry_name, industry_id)
		if is_duplicate :
			return self._failure_response("UpdateIndustryResponse", "IndustryNameAlreadyExists")
		else :
			if (db.update_industry(industry_id, industry_name, user["user_id"])):
				return self._success_response("UpdateIndustryResponse", "UpdateIndustrySuccess", {})
			else :
				return self._failure_response("UpdateIndustryResponse", "InvalidIndustryId")

	def _change_industry_status(self, db, user, request) :
		industry_id = request["industry_id"]
		is_active = request["is_active"]
		if (db.update_industry_status(industry_id, is_active, user["user_id"])) :
			return self._success_response("ChangeIndustryStatusResponse", "ChangeIndustryStatusSuccess", {})
		else :
			return self._failure_response("ChangeIndustryStatusResponse", "InvalidIndustryId")

	def _get_statutory_natures(self, db) :
		nature_list = []
		_natures = db.get_statutory_natures()
		for row in _natures :
			nature = StatutoryNature(int(row[0]), row[1], row[2])
			nature_list.append(nature.toStructure())
		return nature_list

	def _get_statutory_nature_list(self, db, user, request) :
		nature_list = self._get_statutory_natures(db)
		return self._success_response( "GetStatutoryNaturesResponse", "GetStatutoryNaturesSuccess",
			{"statutory_natures": nature_list}
		)

	def _save_statutory_nature(self, db, user, request) :
		statutory_nature_name = request["statutory_nature_name"]
		is_duplicate = db.check_duplicate_statutory_nature(statutory_nature_name, None)
		if is_duplicate :
			return self._failure_response("SaveStatutoryNatureResponse", 
				"StatutoryNatureNameAlreadyExists")
		else :
			db.add_statutory_nature(statutory_nature_name, user["user_id"])
			return self._success_response("SaveStatutoryNatureResponse", 
				"SaveStatutoryNatureSuccess", {})

	def _update_statutory_nature(self, db, user, request) :
		statutory_nature_id = request["statutory_nature_id"]
		statutory_nature_name = request["statutory_nature_name"]
		is_duplicate = db.check_duplicate_statutory_nature(statutory_nature_name, statutory_nature_id)
		if is_duplicate :
			return self._failure_response("UpdateStatutoryNatureResponse", 
				"StatutoryNatureNameAlreadyExists")
		else :
			if (db.update_statutory_nature(statutory_nature_id, statutory_nature_name, user["user_id"])):
				return self._success_response("UpdateStatutoryNatureResponse", 
					"UpdateStatutoryNatureSuccess", {})
			else :
				return self._failure_response("UpdateStatutoryNatureResponse", 
					"InvalidStatutoryNatureId")

	def _change_statutory_nature_status(self, db, user, request) :
		statutory_nature_id = request["statutory_nature_id"]
		is_active = request["is_active"]
		if (db.update_statutory_nature_status(statutory_nature_id, is_active, user["user_id"])) :
			return self._success_response("ChangeStatutoryNatureStatusResponse", 
				"ChangeStatutoryNatureStatusSuccess", {})
		else :
			return self._failure_response("ChangeStatutoryNatureStatusResponse", 
				"InvalidStatutoryNatureId")

	def _get_statutory_levels(self, db) :
		statutory_levels = {}
		_statutory_levels = db.get_statutory_levels()
		for row in _statutory_levels :
			statutoryLevel = Level(int(row[0]), int(row[1]), row[2])
			countryId = int(row[3])
			domainId = int(row[4])
			_list = []
			countryWise = {}
			countryWise = statutory_levels.get(countryId)
			if countryWise is None :
				countryWise = {}
			else :
				_list = countryWise.get(domainId)
				if _list is None :
					_list = []
			_list.append(statutoryLevel.toStructure())
			countryWise[domainId] = _list
			statutory_levels[countryId] = countryWise
			print statutory_levels
		return statutory_levels

	def _get_statutory_levels_list(self, db, user, request) :
		country_list = self._get_countries(db)
		domain_list = self._get_domains(db)
		statutory_levels = self._get_statutory_levels(db)
		return self._success_response("GetStatutoryLevelsResponse", "GetStatutoryLevelsSuccess", 
			{
				"countries": country_list,
				"domains": domain_list,
				"statutory_levels": statutory_levels
			}
		)

	def _save_statutory_levels(self, db, user, request) :
		failure_response = None
		country_id = request["country_id"]
		domain_id = request["domain_id"]
		levels = request["levels"]
		savedNames = [row[2] for row in db.get_statutory_levels_by_id(country_id, domain_id)]
		levelNames = []
		levelPositions = []

		for level in levels :
			levelId = level["level_id"]
			name = level["level_name"]
			position = level["level_position"]
			if levelId is None :
				if (savedNames.count(name) > 0) :
					failure_response = "LevelIdCannotNullFor '%s'" % name
					break
			levelNames.append(name)
			levelPositions.append(position)

		duplicateNames = [x for i, x in enumerate(levelNames) if levelNames.count(x) > 1]
		duplicatePositions = [x for i, x in enumerate(levelPositions) if levelPositions.count(x) > 1]

		if len(duplicateNames) > 0 :
			failure_response = "DuplicateStatutoryLevelNamesExists"
		elif len(duplicatePositions) > 0 :
			failure_response = "DuplicateStatutoryLevelPositionsExists"

		if failure_response is None :
			for level in levels :
				levelId = level["level_id"]
				name = level["level_name"]
				position = level["level_position"]

				db.save_statutory_level(
					country_id, domain_id, levelId, name, position, user["user_id"]
				)
			return self._success_response("SaveStatutoryLevelsResponse", "SaveStatutoryLevelsSuccess", {})
					
		else :
			return self._failure_response("SaveStatutoryLevelsResponse", failure_response)

	def _get_geography_levels(self, db):
		geography_levels = {}
		_geographyLevels = db.get_geography_levels()
		for row in _geographyLevels :
			geographyLevel = Level(int(row[0]), int(row[1]), row[2])
			countryId = int(row[3])
			_list = geography_levels.get(countryId)
			if _list is None :
				_list = []
			_list.append(geographyLevel.toStructure())
			geography_levels[countryId] = _list

		return geography_levels

	def _get_geography_levels_list(self, db, user, request) :
		country_list = self._get_countries(db)
		geography_levels = self._get_geography_levels(db)
		return self._success_response("GetGeographyLevelsResponse", "GetStatutoryLevelsSuccess", 
			{
				"countries": country_list,
				"geography_levels": geography_levels
			}
		)

	def _save_geography_levels(self, db, user, request) :
		failure_response = None
		country_id = request["country_id"]
		levels = request["levels"]
		savedNames = [row[2] for row in db.get_geography_levels_by_country(country_id)]
		levelNames = []
		levelPositions = []

		for level in levels :
			level_id = level["level_id"]
			name = level["level_name"]
			levelNames.append(name)
			levelPositions.append(level["level_position"])
			if levelId is None :
				if (savedNames.count(name) > 0) :
					failure_response = "LevelIdCannotNullFor '%s'" % name
					break

		duplicateNames = [x for i, x in enumerate(levelNames) if levelNames.count(x) > 1]
		duplicatePositions = [x for i, x in enumerate(levelPositions) if levelPositions.count(x) > 1]
		if len(duplicateNames) > 0 :
			failure_response = "DuplicateGeographyLevelNamesExists"
		elif len(duplicatePositions) > 0 :
			failure_response = "DuplicateGeographyLevelPositionsExists"

		if failure_response is None :
			for level in levels :
				level_id = level["level_id"]
				name = level["level_name"]
				position = level["level_position"]

				db.save_geography_level(country_id, level_id, name, position, user["user_id"])

			return self._success_response("SaveGeographyLevelsResponse", "SaveGeographyLevelsSuccess", {})
		else :
			return self._failure_response("SaveGeographyLevelsResponse", failure_response)

	def _get_geographies_list(self, db) :
		geographies = {}
		_geographyList = db.get_geographies()
		for row in _geographyList :
			parent_ids = [int(x) for x in row[3][:-1].split(',')]
			geography = Geography(int(row[0]), row[1], int(row[2]), parentIds[-1], int(row[4]))
			country_id = int(row[5])
			_list = geographies.get(country_id)
			if _list is None :
				_list = []
			_list.append(geography.toStructure())
			geographies[country_id] = _list

		return geographies

	def _get_geographies(self, db, user, request) :
		countries_list = self._get_countries(db)
		geography_levels = self._get_geography_levels(db)
		geographies = self._get_geographies_list(db)
		return self._success_response("GetGeographiesResponse", "GetGeographiesSuccess", 
			{
				"countries": countries_list,
				"geography_levels": geography_levels,
				"geographies": geographies
			}
		)

	def _save_geography(self, db, user, request) :
		levelId = request["geography_level_id"]
		geographyName = request["geography_name"]
		parentIdsList = request["parent_ids"]
		parentIds = ','.join(str(x) for x in parentIdsList) + ","
		geographyNames = [row[1].lower() for row in db.get_duplicate_geographies(parentIds, None)]
		if geographyNames.count(geographyName.lower()) > 0:
			self._failure_response("SaveGeographyResponse", "GeographyNameAlreadyExists",)
		else :
			db.save_geographies(geographyName, levelId, parentIds, user["user_id"])
			return self._success_response("SaveGeographyResponse", "SaveGeographySuccess", {})

	def _update_geography(self, db, user, request) :
		geographyId =  request["geography_id"]
		levelId = request["geography_level_id"]
		geographyName = request["geography_name"]
		parentIdsList = request["parent_ids"]
		parentIds = ','.join(str(x) for x in parentIdsList) + ","
		geographyNames = [row[1].lower() for row in db.get_duplicate_geographies(parentIds, geographyId)]
		if geographyNames.count(geographyName.lower()) > 0:
			return self._failure_response("UpdateGeographyResponse", "GeographyNameAlreadyExists")
		else :
			db.update_geographies(geographyId, geographyName, parentIds, user["user_id"])
			return self._success_response("UpdateGeographyResponse", "UpdateGeographySuccess")

	def _change_geography_status(self, db, user, request) :
		geographyId =  request["geography_id"]
		isActive = request["is_active"]
		if (db.change_geography_status(geographyId, isActive, user["user_id"])) :
			return self._success_response("ChangeGeographyStatusResponse", "ChangeGeographyStatusSuccess", {})
		else :
			return self._failure_response("ChangeGeographyStatusResponse", "InvalidGeographyId", {})

	def _get_geography_report(self, db, user, request) :
		countries = self._get_countries(db)
		_geographyList = self._get_geographies(db)
		geoMappingList = []
		geoMappingDict = {}
		geographyData = {}

		for row in _geographyList :
			geographyData[int(row[0])] = row[1]
		for geo in _geographyList :
			countryId = int(row[5])
			parentIds = [int(x) for x in geo[3][:-1].split(',')]
			names = []
			names.append(geo[6])
			for id in parentIds :
				if id > 0 :
					names.append(geographyData.get(id))
				names.append(geo[1])

			geographies = '>>'.join(str(x) for x in names)
			isActive = int(geo[4])
			geoMappingList.append(
				{
					"geography": geographies,
					"is_active": isActive
				}
			)
			geoMappingDict[countryId] = geoMappingList
		return self._success_response("GeographyReportResponse", "GeographyReportSuccess", 
				{
					"countries": countries,
					"geographies": geoMappingDict
				}
			)

	def _get_statutories(self, db, user, request) :
		statutories = {}
		_statutoryList = db.get_statutories()
		for row in _statutoryList :
			parentIds = [int(x) for x in row[3][:-1].split(',')]
			statutory = Statutory(int(row[0]), row[1], int(row[2]), parentIds)
			countryId = int(row[4])
			domainId = int(row[6])
			_list = []
			_countryWise = statutories.get(countryId)
			if _countryWise is None :
				_countryWise = {}
			else :
				_list = _countryWise.get(domainId)
				if _list is None :
					_list = []
			_list.append(statutory.toStructure())
			_countryWise[domainId] = _list
			statutories[countryId] = _countryWise

		return statutories

	def _save_statutories(self, db, user, request) :
		statutoryName = request["statutory_name"]
		levelId = request["statutory_level_id"]
		parentIdsList = request["parent_ids"]
		parentIds = ','.join(str(x) for x in parentIdsList) + ","
		statutoryNames = [row[1].lower() for row in db.get_duplicate_statutories(parentIds, None)]
		if statutoryNames.count(statutoryName.lower()) > 0:
			return self._failure_response("SaveStatutoryResponse", "StatutoryNameAlreadyExists")
		else :
			db.save_statutories(statutoryName, levelId, parentIds, user["user_id"])
			return self._success_response("SaveStatutoryResponse", "SaveStatutorySuccess")

	def _update_statutories(self, db, user, request) :
		statutoryId = request["statutory_id"]
		statutoryName = request["statutory_name"]
		levelId = request["statutory_level_id"]
		parentIdsList = request["parent_ids"]
		parentIds = ','.join(str(x) for x in parentIdsList) + ","
		statutoryNames = [row[1].lower() for row in db.get_duplicate_statutories(parentIds, statutoryId)]
		if statutoryNames.count(statutoryName.lower()) > 0:
			return self._failure_response("UpdateStatutoryResponse", "StatutoryNameAlreadyExists")
		else :
			db.update_statutories(statutoryId, statutoryName, parentIds, user["user_id"])
			return self._success_response("UpdateStatutoryResponse", "StatutoryNameAlreadyExists")
			
	def _get_statutory_mappings(self, db, user, request) :
		statutory_mappings = {}
		_staturoyMapList = db.get_stautory_mappings()
		_statutoryMappings = db.allStatutories
		for row in _staturoyMapList :
			mappingId = int(row[0])
			countryId = int(row[1])
			countryName = row[2]
			domainId = int(row[3])
			domainName = row[4]
			industryIds = [int(x) for x in row[5][:-1].split(',')]
			statutoryNatureId = int(row[6])
			statutoryNatureName = row[7]
			statutoryIds = [int(x) for x in row[8][:-1].split(',')]
			statutoryMappings = [_statutoryMappings.get(x)[1] for x in statutoryIds ]
			complianceIds = [int(x) for x in row[9][:-1].split(',')]
			geographyIds = [int(x) for x in row[10][:-1].split(',')]
			approvalStatus = row[11]
			isActive = row[12]
			mapping = StatutoryMapping (
				countryId, countryName, domainId, domainName, 
				industryIds, statutoryNatureId, statutoryNatureName, 
				statutoryIds, statutoryMappings, complianceIds, 
				geographyIds, approvalStatus, isActive
			)
			statutory_mappings[mappingId] = mapping.toStructure()
		return self._success_response("GetStatutoryMappingsResponse", "GetStatutoryMappingsSuccess", 
			{
				"countries" : self._get_countries(db),
				"domains": self._get_domains(db),
				"industries": self._get_industries(db),
				"statutory_natures": self._get_statutory_natures(db),
				"statutory_levels": self._get_statutory_levels(db),
				"statutories": self._get_statutories(db),
				"geography_levels": self._get_geography_levels(db),
				"geographies": self._get_geographies_list(db),
				"statutory_mappings": statutory_mappings
			}
		)

	def _save_statutory_mappings(self, db, user, request) :
		if (db.save_statutory_mapping(request, user["user_id"])) :
			return self._success_response("SaveStatutoryMappingResponse", "SaveStatutoryMappingSuccess", {})
		else :
			return self._failure_response("SaveStatutoryMappingResponse", "SaveStatutoryMappingFailed")

	def _update_statutory_mappings(self, db, user, request) :
		if (db.update_statutory_mapping(request, user["user_id"])) :
			return self._success_response("UpdateStatutoryMappingResponse", "UpdateStatutoryMappingSuccess", {})
		else :
			return self._failure_response("UpdateStatutoryMappingResponse", "InvalidStatutoryMappingId")

	def _change_statutory_mappings_status(self, db, user, request) :
		if (db.change_statutory_mapping_status(request, user["user_id"])) :
			return self._success_response("ChangeStatutoryMappingStatusResponse", "ChangeStatutoryMappingStatusSuccess", {})
		else :
			return self._failure_response("ChangeStatutoryMappingStatusResponse", "InvalidStatutoryMappingId")

	def _change_approval_status(self, db, user, request) :
			if (db.change_approval_status(request, user["user_id"])) :
				return self._success_response("ApproveStatutoryMappingResponse", "ApproveStatutoryMappingSuccess", {})
			else :
				return self._failure_response("ApproveStatutoryMappingResponse", "InvalidStatutoryMappingId")

		

	def _get_user_groups(self, db, user, request):
		knowledge_forms = Form.get_forms("knowledge", db)
		techno_forms = Form.get_forms("techno", db)
		forms = {}
		forms["knowledge"] = Menu.get_menu(knowledge_forms)
		forms["techno"] = Menu.get_menu(techno_forms)
		user_group_list = UserGroup.get_detailed_list(db)
		response_data = {}
		response_data["forms"] = forms
		response_data["user_groups"] = user_group_list
		return self._success_response(
			"GetUserGroupsResponse", 
			"GetUserGroupsSuccess", 
			response_data
		)

	def _save_user_group(self, db, user, request):
		form = "UserGroupMaster"
		session_user = int(user["user_id"])
		response = "SaveUserGroupResponse"
		response_data = None
		user_group_id = db.generate_new_id(form)
		user_group = UserGroup.initialize_with_request( request, user_group_id)
		if db.is_duplicate(form, "name", user_group.user_group_name,user_group_id):
			response_data = self._failure_response(response, "GroupNameAlreadyExists")
		elif db.save_user_group(user_group, session_user):
			action_type = "save"
			db.save_activity(form, user_group.user_group_name, 
				action_type, session_user)
			response_data =  self._success_response(
				response, 
				"SaveUserGroupSuccess", 
				{}
			)
		return response_data
        

	def _update_user_group(self, db, user, request):
		form = "UserGroupMaster"
		session_user = int(user["user_id"])
		response = "UpdateUserGroupResponse"
		response_data = None
		user_group_id = request["user_group_id"]
		user_group = UserGroup.initialize_with_request(request, user_group_id)
		if db.is_id_invalid(form, user_group_id):
			response_data = self._failure_response(response, "InvalidUserGroupId")
		elif db.is_duplicate(form, "name", user_group.user_group_name,
			user_group.user_group_id):
			response_data = self._failure_response(response,"GroupNameAlreadyExists")
		elif db.save_user_group(user_group, session_user):
			action_type = "update"
			db.save_activity(form, user_group.user_group_name, 
				action_type, session_user)
			response_data =  self._success_response(response, "UpdateUserGroupSuccess",{})
		return response_data

	def _change_user_group_status(self, db, user, request):
		form = "UserGroupMaster"
		session_user = int(user["user_id"])
		response = "ChangeUserGroupStatusResponse"
		response_data = None
		user_group_id = request["user_group_id"]
		is_active = request["is_active"]
		if db.is_id_invalid(form, user_group_id):
			response_data = self._failure_response(
				response, "InvalidUserGroupId")
		elif db.change_user_group_status(user_group_id, is_active,
				session_user):
			action_type = "status_change"
			db.save_activity(form, user_group_id, 
				action_type, session_user)
			response_data = self._success_response(
				response, "ChangeUserGroupStatusSuccess",{})
		return response_data

	def _get_users(self, db, user, request):
		domain_list = Domain.get_list(db)
		country_list = Country.get_list(db)
		user_group_list = UserGroup.get_list(db)
		user_list = AdminUser.get_detailed_list(db)
		response_data = {}
		response_data["domains"] = domain_list
		response_data["countries"] = country_list
		response_data["user_groups"] = user_group_list
		response_data["users"] = user_list
		return self._success_response(
				"GetUsersResponse", 
				"GetUsersSuccess",
				response_data)
        
	def _save_user(self, db, user, request):
		form = "UserMaster"
		session_user = int(user["user_id"])
		response = "SaveUserResponse"
		response_data = None
		user_id = db.generate_new_id(form)
		user = AdminUser.initialize_with_request( request, user_id)
		if db.is_duplicate(form, "email", user.email_id,user_id):
			response_data = self._failure_response(
				response, "EmailIdAlreadyExists")
		elif db.is_duplicate(form, "employee_code", user.employee_code,user_id):
			response_data = self._failure_response(
				response, "EmployeeCodeAlreadyExists")
		elif db.is_duplicate(form, "contact_no", user.contact_no,user_id):
			response_data = self._failure_response(
				response, "ContactNumberAlreadyExists")
		elif (db.save_user(user, session_user) and db.save_user_details(
					user, session_user)):
			action_type = "save"
			db.save_activity(form, user.employee_code+"-"+user.employee_name, 
				action_type, session_user)
			response_data = self._success_response(response, "SaveUserSuccess",
				{})
		return response_data

	def _update_user(self, db, user, request):
		form = "UserMaster"
		session_user = int(user["user_id"])
		response = "UpdateUserResponse"
		response_data = None
		user_id = request["user_id"]
		user = AdminUser.initialize_with_request( request, user_id)
		if db.is_id_invalid(form, user_id):
			response_data = self._failure_response(
				response, "InvalidUserId")
		elif db.is_duplicate(form, "email", user.email_id,user_id):
			response_data = self._failure_response(
				response, "EmailIdAlreadyExists")
		elif db.is_duplicate(form, "employee_code", user.employee_code,user_id):
			response_data = self._failure_response(
				response, "EmployeeCodeAlreadyExists")
		elif db.is_duplicate(form, "contact_no", user.contact_no,user_id):
			response_data = self._failure_response(
				response, "ContactNumberAlreadyExists")
		elif db.save_user_details(user, session_user):
			action_type = "update"
			db.save_activity(form, user.employee_code+"-"+user.employee_name, 
				action_type, session_user)
			response_data = self._success_response(response, "UpdateUserSuccess",
				{})
		return response_data

	def _change_admin_user_status(self, db, user, request):
		form = "UserMaster"
		session_user = int(user["user_id"])
		response = "ChangeUserStatusResponse"
		response_data = None
		user_id = request["user_id"]
		is_active = request["is_active"]
		if db.is_id_invalid(form, user_id):
			response_data = self._failure_response(
				response, "InvalidUserId")
		elif db.change_user_status(user_id, is_active,
				session_user):
			action_type = "status_change"
			db.save_activity(form, user_id, 
				action_type, session_user)
			response_data = self._success_response(
				response, "ChangeUserStatusSuccess",{})
		return response_data

	def _change_password(self, db, user, request):
		session_user = user["user_id"]
		current_password = request["current_password"]
		new_password = request["new_password"]
		client_id = db.get_client_id(session_user)        
		response = "ChangePasswordResponse"
		response_data = None
		if not db.verify_password(current_password, session_user, client_id):
			response_data = self._failure_response(response, "InvalidCurrentPassword")
		elif db.update_password(new_password, session_user):
			response_data = self._success_response(
				response, "ChangePasswordSuccess",{})
		return response_data
        
	def _forgot_password(self, db, user, request):
		username = request["username"]
		response = "ForgotPasswordResponse"
		response_data = None
		user_id = db.validate_username(username)
		if user_id == None :
			response_data = self._failure_response(response,
			 "InvalidUsername")
		else:
			self._send_reset_link(db, user_id)
			response_data = self._success_response(response,
				"ForgotPasswordSuccess",{})
		return response_data

	def _send_reset_link(self, db, user_id):
		resetToken = uuid.uuid4()
		print "http://localhost:8080/ForgotPassword?reset_token=%d" % resetToken
		if db.save_reset_token(resetToken, user_id):
			print "send email"
			# send_email()
			return True

	def _validate_reset_token(self, db, user, request):
		response = "ResetTokenValidationResponse"
		response_data = None
		reset_token = request["reset_token"]
		if db.validate_reset_token(reset_token):
			response_data = self._success_response(response,
            	"ResetTokenValidationSuccess",{})
		else:
			response_data = self._failure_response(response, "InvalidResetToken")
		return response_data

	def _reset_password(self, db, user, request):		
		reset_token = request["reset_token"]
		newPassword = request["new_password"]
		user_id = None
		response = "ResetPasswordResponse"
		response_data = None
		if db.validate_reset_token(reset_token):
			user_id = db.get_user_id_by_verification_code(reset_token)
			if (db.update_password(newPassword, user_id) and 
        		db.delete_user_verfication_code(reset_token)):
				response_data = self._success_response(response,
            	"ResetPasswordSuccess",{})
			else:
				print "Error: Reset Password Failed"
		else:
			response_data = self._failure_response(response, "InvalidResetToken")			
		return response_data

	def _save_client_group(self, db, user, request):
		print "inside save client"

	def _update_client_group(self, db, user, request):
		print "inside update client"
	
	def _change_client_group_status(self, db, user, request):
		print "inside change client status"
	
	def _get_client_groups(self, db, user, request):
		response_data = {}
		domain_list = Domain.get_list(db)
		country_list = Country.get_list(db)
		user_list = AdminUser.get_list(db)
		client_list = GroupCompany.get_detailed_list(db)
		response_data["domains"] = domain_list
		response_data["countries"] = country_list
		response_data["users"] = user_list
		response_data["client_list"] = client_list
		print response_data
		return self._success_response("GetClientGroupsResponse",
	        	"GetClientGroupsSuccess",
	        	response_data)
                
                
#		
# db_request
#

def db_request(f) :
	def wrapper(self, request_handler) :
		self._handle_db_request(f, request_handler)
	return wrapper


#
# KnowledgeController
#

class KnowledgeController(object):
	def __init__(self):
		self._db = KnowledgeDatabase()
		self._api_handler = APIHandler()

	def _handle_db_request(self, unbound_method, request_handler) :
		request_handler.set_header("Access-Control-Allow-Origin", "*")
		unbound_method(self, self._db, request_handler)

	def _send_error(self, request_handler, status, msg) :
		request_handler.set_status(status)
		request_handler.write(msg)

	def _parse_request(self, request_handler, protocol2) :
		try:
			data = json.loads(request_handler.request.body)
			data = data["data"]
			if validate_data(protocol2, data) :
				return data
			else :
				return None
		except Exception, e:
			print e
			raise

	def _send_response(self, request_handler, protocol, data) :
		if not validate_data(protocol, data) :
			self._send_error(request_handler, 500, "")
			return
		structure = {"data": data}
		response_data = json.dumps(structure)
		request_handler.set_header("Content-Type", "application/json")
		request_handler.write(response_data)

	@db_request
	def handle_api_knowledge(self, db, request_handler) :
		db.test()
		request_frame = self._parse_request(request_handler, protocol.RequestFrame)
		if request_frame is None :
			request_handler.set_status(500)
			request_handler.write("")
			return
		session_id = request_frame["session_token"]
		request_obj = request_frame["request"]
		response_obj = self._api_handler.process(db, session_id, request_obj)
		self._send_response(request_handler, response_obj["protocol"], response_obj["data"])
