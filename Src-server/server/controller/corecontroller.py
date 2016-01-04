from protocol import core

__all__ = [
	"process_user_forms", "process_user_menus", 
	"generate_menu_from_forms"
]

def process_user_forms(db, form_ids):
	forms = db.get_user_forms(form_ids)
	form_list = []
	for f in forms :
		form_id = f[0]
		form_name = f[6]
		form_url = f[7]
		category_id = f[2]
		form_type_id = f[4]
		parent_menu = f[9]
		form_list.append(
			core.KnowledgeForm(form_id, form_name, form_url, category_id, form_type_id, parent_menu)
		)
	return process_user_menus(form_list)

def process_user_menus(form_list):
	menus = {}

	for form in form_list:
		form_type = form.form_type_id
		if menus.get(form_type) is None :
			menus[form_type] = [form]
		else:
			menus[form_type].append(form)

	return core.Menu(menus)