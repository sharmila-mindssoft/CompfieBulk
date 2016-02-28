import threading
import re

from protocol import core, technomasters

__all__ = [
	"get_client_groups",
	"save_client_group",
	"update_client_group",
	"change_client_group_status",
	"save_client",
	"update_client",
	"get_clients",
	"change_client_status",
	"reactivate_unit",
	"get_client_profile"
]

#
# Client Group Master
#

def get_client_groups(db, request, session_user):
	domain_list = db.get_domains_for_user(session_user)
	country_list = db.get_countries_for_user(session_user)
	user_list = []
	client_list = []

	user_rows = db.get_techno_users()
	for user_row in user_rows:
		employee_name = None
		if user_row[2] == None:
			employee_name = user_row[1]
		else:
			employee_name = "%s-%s" % (user_row[2], user_row[1])
		user_id = user_row[0]
		is_active = True if user_row[3]==1 else False
		user_list.append(core.User(user_id, employee_name, is_active))
	client_list = db.get_group_company_details()
	return technomasters.GetClientGroupsSuccess(countries = country_list, 
		domains = domain_list, users = user_list, client_list = client_list)

def create_database(
	host, username, password, database_name, db_username,
	db_password, email_id, client_id, short_name, db
):
	try:
		db._create_database(
			host, username, password, database_name, db_username,
			db_password, email_id, client_id, short_name
		)
	except Exception, x:
		print x

def save_client_group(db, request, session_user):
	session_user = int(session_user)
	client_id = db.generate_new_client_id()
	if db.is_duplicate_group_name(request.group_name, client_id):
		return technomasters.GroupNameAlreadyExists()
	elif db.is_duplicate_short_name(request.short_name, client_id):
		return technomasters.ShortNameAlreadyExists()
	else:
		group_name = re.sub('[^a-zA-Z0-9 \n\.]', '', request.group_name)
		group_name = group_name.replace(" ", "")
		database_name = "mirror_%s_%d" % (group_name.lower(), client_id)
		row = db._get_server_details()
		host = row[0]
		username = row[1]
		password = row[2]
		db_username = db.generate_random()
		db_password = db.generate_random()
		create_database_thread = threading.Thread(
			target=create_database, args=[
				host, username, password, database_name, db_username,
				db_password, request.email_id, client_id, request.short_name, db
			]
		)
		create_database_thread.start()
		try:
			db.save_client_group(client_id, request, session_user)
			db.save_date_configurations(client_id, request.date_configurations, 
				session_user)
			db.save_client_countries(client_id, request.country_ids)
			db.save_client_domains(client_id, request.domain_ids)
			db.save_incharge_persons(request, client_id)
			db.save_client_user(request, session_user, client_id)
			db.update_client_db_details(host, client_id, db_username,
	            db_password, request.short_names, database_name)
		except Exception, e:
			print e
			db.rollback()
			db.delete_database(host, database_name, db_username, db_password)
		return technomasters.SaveClientGroupSuccess()

def update_client_group(db, request, session_user):
	session_user = int(session_user)
	if db.is_invalid_id(db.tblClientGroups, "client_id", request.client_id) :
		return technomasters.InvalidClientId()
	elif db.is_duplicate_group_name(request.group_name, request.client_id):
		return technomasters.GroupNameAlreadyExists()
	else:
		db.update_client_group(request, session_user)
		db.save_date_configurations(request.client_id, request.date_configurations,
		 session_user)
		db.save_client_countries(request.client_id, request.country_ids)
		db.save_client_domains(request.client_id, request.domain_ids)
		db.save_incharge_persons(request, request.client_id)
		return technomasters.UpdateClientSuccess()

def change_client_group_status(db, request, session_user):
	session_user = int(session_user)
	client_id = request.client_id
	is_active = request.is_active
	if db.is_invalid_id(db.tblClientGroups, "client_id", client_id) :
		return technomasters.InvalidClientId()
	else:
		db.update_client_group_status(client_id, is_active, session_user)
		return technomasters.ChangeClientStatusSuccess()

#
# Client Unit Creation
# 

def save_client(db, request, session_user):
	session_user = int(session_user)
	client_id = request.client_id
	business_group = request.business_group
	legal_entity = request.legal_entity
	division = request.division
	country_wise_units = request.country_wise_units
	business_group_id = None
	business_group_name = None
	division_id = None
	division_name = None
	optional_business_group = False
	optional_division = False
	result1 = False
	result2 = False
	result3 = False
	result4 = False
	existing_business_group = False
	existing_entity = False
	existing_division = False

	if db.is_invalid_id(db.tblClientGroups, "client_id", client_id) :
		return technomasters.InvalidClientId()

	if business_group == None:
	    optional_business_group = True
	    result1 = True
	else:
	    business_group_id = business_group.business_group_id
	    business_group_name = business_group.business_group_name
	    if business_group_id == None:
	        business_group_id = db.generate_new_business_group_id()
	    else:
	        existing_business_group = True
	    if db.is_duplicate_business_group(business_group_id, business_group_name, client_id):
	        return technomasters.BusinessGroupNameAlreadyExists()

	legal_entity_id = legal_entity.legal_entity_id
	legal_entity_name = legal_entity.legal_entity_name
	if legal_entity_id == None:
	    legal_entity_id = db.generate_new_legal_entity_id()
	else:
	    existing_entity = True
	if db.is_duplicate_legal_entity(legal_entity_id, legal_entity_name, client_id):
	    return technomasters.LegalEntityNameAlreadyExists()

	if division == None:
	    optional_division = True
	    result3 = True
	else:
	    division_id = division.division_id
	    division_name = division.division_name 
	    if division_id == None:
	        division_id = db.generate_new_division_id()
	    else:
	        existing_division = True
	    if db.is_duplicate_division(division_id, division_name, client_id):
	        return technomasters.DivisionNameAlreadyExists()

	units_list = []
	unit_id = None
	for country in country_wise_units:
	    country_id = country.country_id
	    units = country.units
	    for unit in units:
	        unit_id = (unit_id+1) if unit_id != None else db.generate_new_unit_id()
	        domain_ids = ",".join(str(x) for x in unit.domain_ids)
	        if db.is_duplicate_unit_name(unit_id, unit.unit_name, client_id):
	            return technomasters.UnitNameAlreadyExists()
	        elif db.is_duplicate_unit_code(unit_id, unit.unit_code, client_id):
	            return technomasters.UnitCodeAlreadyExists()
	        else:
				unit.unit_id = unit_id
				unit.country_id = country_id
				units_list.append(unit)
	if not optional_business_group:
	    if not existing_business_group:
	        result1 = db.save_business_group(client_id, business_group_id, business_group_name, session_user)
	    else:
	        result1 = True
	if not existing_entity:
	    result2 = db.save_legal_entity(client_id, legal_entity_id, legal_entity_name, business_group_id, session_user)
	else:
	    result2 = True
	if not optional_division:
	    if not existing_division:
	        result3 = db.save_division(client_id, division_id, division_name, business_group_id, legal_entity_id, session_user)
	    else:
	        result3 = True
	result4 = db.save_unit(client_id, units_list, business_group_id, legal_entity_id, division_id, session_user)
	if result1 and result2 and result3 and result4:
	    return technomasters.SaveClientSuccess()

def update_client(db, request, session_user):
	session_user = int(session_user)
	client_id = request.client_id
	business_group = request.business_group
	legal_entity = request.legal_entity
	division = request.division
	country_wise_units = request.country_wise_units

	business_group_id = None
	business_group_name = None
	division_id = None
	division_name = None
	optional_business_group = False
	optional_division = False
	result1 = False
	result2 = False
	result3 = False
	result4 = False
	result5 = False

	if db.is_invalid_id(db.tblClientGroups, "client_id", client_id) :
		return technomasters.InvalidClientId()

	if business_group == None:
	    optional_business_group = True
	    result1 = True
	else:
	    business_group_id = business_group.business_group_id
	    business_group_name = business_group.business_group_name
	    if db.is_invalid_id(db.tblBusinessGroups, "business_group_id", business_group_id):
	        return technomasters.InvalidBusinessGroupId()
	    elif db.is_duplicate_business_group(business_group_id, 
	    	business_group_name, client_id):
	        return technomasters.BusinessGroupNameAlreadyExists()

	legal_entity_id = legal_entity.legal_entity_id
	legal_entity_name = legal_entity.legal_entity_name
	if db.is_invalid_id( db.tblLegalEntities, "legal_entity_id", legal_entity_id):
	    return technomasters.InvalidLegalEntityId()
	elif db.is_duplicate_legal_entity(legal_entity_id, legal_entity_name, client_id):
	    return technomasters.LegalEntityNameAlreadyExists()

	if division == None:
	    optional_division = True
	    result3 = True
	else:
	    division_id = division.division_id
	    division_name = division.division_name 
	    if db.is_invalid_id(db.tblDivisions, "division_id", division_id):
	        return technomasters.InvalidDivisionId()
	    elif db.is_duplicate_division(division_id, division_name, client_id):
	        return technomasters.DivisionNameAlreadyExists()

	new_units_list = []
	existing_units_list = []
	unit_id = None
	for country in country_wise_units:
	    country_id = country.country_id
	    units = country.units
	    for unit in units:
	        domain_ids = ",".join(str(x) for x in unit.domain_ids)
	        if unit.unit_id == None:
	            unit_id = (unit_id+1) if unit_id != None else db.generate_new_unit_id()
	            if db.is_duplicate_unit_name(unit_id, unit.unit_name, client_id):
	                return technomasters.UnitNameAlreadyExists()
	            elif db.is_duplicate_unit_code(unit_id, unit.unit_code, client_id):
	                return technomasters.UnitCodeAlreadyExists()
	            else:
	                unit.unit_id = unit_id
	                unit.country_id = country_id
	                new_units_list.append(unit)
	        else:
	            if db.is_invalid_id(db.tblUnits, "unit_id", unit.unit_id):
	                return technomasters.InvalidUnitId()
	            elif db.is_duplicate_unit_name(unit.unit_id, unit.unit_name, client_id):
	                return technomasters.UnitNameAlreadyExists()
	            elif db.is_duplicate_unit_code(unit.unit_id, unit.unit_code, client_id):
	                return technomasters.UnitCodeAlreadyExists()
	            else:
	                unit.country_id = country_id
	                existing_units_list.append(unit)

	if not optional_business_group:
	    result1 = db.update_business_group(client_id, business_group_id, business_group_name, session_user)
	result2 = db.update_legal_entity(client_id, legal_entity_id, legal_entity_name, business_group_id, session_user)
	if not optional_division:
	    result3 = db.update_division(client_id, division_id, division_name, business_group_id, legal_entity_id, session_user)
	if len(new_units_list) > 0:
	    result4 = db.save_unit(client_id, new_units_list, business_group_id, legal_entity_id, division_id, session_user)
	else:
	    result4 = True
	result5 = db.update_unit(client_id, existing_units_list, business_group_id, legal_entity_id, division_id, session_user)
	if result1 and result2 and result3 and result4 and result5:
	    return technomasters.UpdateClientSuccess()


def get_clients(db, request, session_user):
	group_company_list = db.get_group_companies_for_user(session_user)
	if len(group_company_list) > 0:
		country_list = db.get_countries_for_user(session_user)
		domain_list = db.get_domains_for_user(session_user)
		business_group_list = db.get_business_groups_for_user(session_user)
		legal_entity_list = db.get_legal_entities_for_user(session_user)
		division_list = db.get_divisions_for_user(session_user)
		unit_list = db.get_unit_details_for_user(session_user)
		geography_levels = db.get_geograhpy_levels_for_user(session_user)
		geographies = db.get_geographies_for_user_with_mapping(session_user)
		industries = db.get_industries()
		return technomasters.GetClientsSuccess(countries=country_list, 
			domains = domain_list, group_companies = group_company_list, 
			business_groups = business_group_list, legal_entities = legal_entity_list, 
			divisions = division_list, units = unit_list, geography_levels = geography_levels,
			geographies = geographies, industries = industries)
	else:
		return technomasters.UserIsNotResponsibleForAnyClient()

def change_client_status(db, request, session_user):
	session_user = int(session_user)

	client_id = request.client_id
	legal_entity_id = request.legal_entity_id
	is_active = request.is_active
	division_id = request.division_id

	is_active = 1 if is_active == True else 0

	if db.is_invalid_id(db.tblClientGroups, "client_id", client_id):
		return technomasters.InvalidClientId()
	elif db.is_invalid_id(db.tblLegalEntities, "legal_entity_id", legal_entity_id):
		return technomasters.InvalidLegalEntityId()
	elif division_id != None:
		if db.is_invalid_id(db.tblDivisions, "division_id", division_id):
			return technomasters.InvalidDivisionId()
		elif db.change_client_status(client_id, legal_entity_id, division_id, 
			is_active, session_user):
			return technomasters.ChangeClientStatusSuccess()	
	elif db.change_client_status(client_id, legal_entity_id, division_id, 
	    is_active, session_user):
	    return technomasters.ChangeClientStatusSuccess()
    

def reactivate_unit(db, request, session_user):
	session_user = int(session_user)
	client_id = request.client_id
	unit_id = request.unit_id
	password = request.password
	if db.is_invalid_id(db.tblClientGroups, "client_id", client_id):
		return technomasters.InvalidClientId()
	elif db.is_invalid_id(db.tblUnits, "unit_id", unit_id):
		return technomasters.InvalidUnitId()
	else:
		if db.verify_password(password, session_user):
		    if db.reactivate_unit(client_id, unit_id, session_user):
		        return technomasters.ReactivateUnitSuccess()
		else:
		    return technomasters.InvalidPassword()

def get_client_profile(db, request, session_user):
	client_ids = db.get_user_clients(session_user)

	if client_ids ==  None:
		return technomasters.UserIsNotResponsibleForAnyClient()
	else:
		profiles = db.get_profiles(client_ids)
		group_companies = db.get_group_companies_for_user(session_user)
		return technomasters.GetClientProfileSuccess(
			group_companies = group_companies,
			profiles = profiles)
