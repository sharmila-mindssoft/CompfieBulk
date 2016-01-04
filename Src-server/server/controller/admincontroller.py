from protocol import (admin, core)
from corecontroller import process_user_menus

__all__ = [
	"process_admin_request", "get_user_groups"
]

def process_admin_request(request, db) :
	print "inside admin request"
	session_token = request.session_token
	request_frame = request.request
	session_user = db.validate_session_token(session_token)
	if session_user is None:
		return login.InvalidSessionToken()

	if type(request_frame) is admin.GetUserGroups:
		return get_user_groups(db, request_frame, session_user)

	if type(request_frame) is admin.SaveUserGroup:
		return save_user_group(db, request_frame, session_user)

	if type(request_frame) is admin.UpdateUserGroup:
		return update_user_group(db, request_frame, session_user)

	if type(request_frame) is admin.ChangeUserGroupStatus:
		return change_user_group_status(db, request_frame, session_user)

	if type(request_frame) is admin.GetUsers:
		return get_users(db, request_frame, session_user)

	if type(request_frame) is admin.SaveUser:
		return save_user(db, request_frame, session_user)

	if type(request_frame) is admin.UpdateUser:
		return update_user(db, request_frame, session_user)

	if type(request_frame) is admin.ChangeUserStatus:
		return change_user_status(db, request_frame, session_user)

def get_forms(db) :
	result_rows = db.get_forms()
	knowledge_forms = []
	techno_forms = []
	for row in result_rows:
		parent_menu = "" if row[8] == None else row[8]
		if int(row[1]) == 2:
			form = core.KnowledgeForm(form_id = row[0], form_name = row[5], form_url = row[6], 
				parent_menu = parent_menu, form_category_id = row[1], form_type_id = row[3])
			knowledge_forms.append(form)
		elif int(row[1]) == 3: 
			form = core.KnowledgeForm(form_id = row[0], form_name = row[5], form_url = row[6], 
				parent_menu = parent_menu, form_category_id = row[1], form_type_id = row[3])
			techno_forms.append(form)
	result = {}
	result[2] = process_user_menus(knowledge_forms)
	result[3] = process_user_menus(techno_forms)
	return result

def get_user_group_detailed_list(db):
	user_group_list = []
	rows = db.get_user_group_detailed_list()
	for row in rows:
		user_group_id = int(row[0])
		user_group_name = row[1]
		form_category_id = row[2]
		form_ids = [int(x) for x in row[3].split(",")]
		is_active = False if row[4] == 0 else True
		user_group_list.append(admin.UserGroup(user_group_id, user_group_name, 
			form_category_id, form_ids, is_active))
	return user_group_list

def get_form_categories(db):
	formCategoryList = []
	rows = db.get_form_categories()
	for row in rows:
		formCategoryList.append(core.FormCategory(row[0], row[1]))
	return formCategoryList

def get_user_groups(db, request_frame, session_user):
	forms = get_forms(db)
  	form_categories = get_form_categories(db)
	user_group_list = get_user_group_detailed_list(db)
	result = admin.GetUserGroupsSuccess(form_categories=form_categories, 
		forms=forms, user_groups=user_group_list)
	return result

def save_user_group(db, request, session_user):
	user_group_name = request.user_group_name
	form_category_id = request.form_category_id
	form_ids =  request.form_ids
	user_group_id = db.generate_new_user_group_id()
	if db.is_duplicate_user_group_name(user_group_id, user_group_name) :
		return admin.GroupNameAlreadyExists()
	elif db.save_user_group(user_group_id, user_group_name,
			form_category_id, form_ids) :
		return admin.SaveUserGroupSuccess()

def update_user_group(db, request, session_user):
	user_group_id= request.user_group_id
	user_group_name= request.user_group_name
	form_category_id= request.form_category_id
	form_ids=  request.form_ids
	if db.is_invalid_id(db.tblUserGroups, "user_group_id", user_group_id) :
	    return admin.InvalidUserGroupId()
	elif db.is_duplicate_user_group_name(user_group_id, user_group_name) :
	    return admin.GroupNameAlreadyExists()
	elif db.update_user_group(user_group_id, user_group_name,
			form_category_id, form_ids) :
		return admin.UpdateUserGroupSuccess()

def change_user_group_status(db, request, session_user):
	user_group_id = request.user_group_id
	is_active =  0 if request.is_active == False else 1
	if db.is_invalid_id(db.tblUserGroups, "user_group_id", user_group_id):
		return admin.InvalidUserGroupId()
	elif db.update_user_group_status(user_group_id, is_active):
		return admin.ChangeUserGroupStatusSuccess()

def get_users(db, request_frame, session_user):
	domain_list = []
	country_list = []
	user_group_list = []
	user_list = []

	domain_rows = db.get_domains()
	for domain_row in domain_rows:
		domain_id = domain_row[0]
		domain_name = domain_row[1]
		is_active = True if domain_row[2] == 1 else False
		domain_list.append(core.Domain(domain_id, domain_name, is_active))

	country_rows = db.get_countries()
	for country_row in country_rows:
		country_id = country_row[0]
		country_name = country_row[1]
		is_active = True if country_row[2] == 1 else False
		country_list.append(core.Country(country_id, country_name, is_active))

	user_group_rows = db.get_user_groups()
	for user_group_row in user_group_rows:
		user_group_id = user_group_row[0]
		user_group_name = user_group_row[1]
		is_active = True if user_group_row[2] == 1 else False
		user_group_list.append(core.UserGroup(user_group_id, user_group_name, is_active))	

	user_rows = db.get_detailed_user_list()
	columns = "user_id, email_id, user_group_id, employee_name, employee_code,"+\
	            "contact_no, address, designation, is_active"
	for user_row in user_rows:
		user_id = user_row[0]
		email_id = user_row[1]
		user_group_id = user_row[2]
		employee_name = user_row[3]
		employee_code = user_row[4]
		contact_no = user_row[5]
		address = user_row[6]
		designation = user_row[7]
		is_active = True if user_row[8] == 1 else False
		country_ids = [int(x) for x in db.get_user_countries(user_id).split(",")]
		domain_ids = [int(x) for x in db.get_user_domains(user_id).split(",")]
		user_list.append(core.UserDetails(user_id, email_id, user_group_id, 
			employee_name, employee_code, contact_no, address, designation, 
			country_ids, domain_ids, is_active))		
		
	return admin.GetUsersSuccess(user_groups = user_group_list,
		countries = country_list, domains=domain_list, users=user_list)

def save_user(db, request, session_user):
	user_id = db.generate_new_user_id()
	email_id = request.email_id
	user_group_id = request.user_group_id
	employee_name = request.employee_name
	employee_code = request.employee_code
	contact_no = request.contact_no
	address =  request.address
	designation =  request.designation
	country_ids = request.country_ids
	domain_ids = request.domain_ids
	if db.is_duplicate_email(email_id, user_id) :
	    return admin.EmailIDAlreadyExists()
	elif db.is_duplicate_employee_code(employee_code, user_id) :
	    return admin.EmployeeCodeAlreadyExists()
	elif db.is_duplicate_contact_no(contact_no, user_id) :
	    return admin.ContactNumberAlreadyExists()
	elif db.save_user(user_id, email_id, user_group_id, employee_name,
     employee_code, contact_no, address, designation, country_ids, domain_ids) :
	    return admin.SaveUserSuccess()


def update_user(db, request, session_user):
	user_id = request.user_id
	user_group_id = request.user_group_id
	employee_name = request.employee_name
	employee_code = request.employee_code
	contact_no = request.contact_no
	address =  request.address
	designation =  request.designation
	country_ids = request.country_ids
	domain_ids = request.domain_ids
	if db.is_invalid_id(db.tblUsers, "user_id", user_id):
		return admin.InvalidUserId()
	elif db.is_duplicate_employee_code(employee_code, user_id) :
		return admin.EmployeeCodeAlreadyExists()
	elif db.is_duplicate_contact_no(contact_no, user_id) :
		return admin.ContactNumberAlreadyExists()
	elif db.update_user(user_id, user_group_id, employee_name, employee_code, 
		contact_no, address, designation, country_ids, domain_ids) :
		return admin.UpdateUserSuccess()

def change_user_status(db, request, session_user):
	user_id = request.user_id
	is_active = 0 if request.is_active == False else 1
	if db.is_invalid_id(db.tblUsers, "user_id", user_id):
	    return admin.InvalidUserId()
	elif db.update_user_status(user_id, is_active):
	    return admin.ChangeUserStatusSuccess()