from protocol import core

__all__ = [
	"process_user_forms", "process_user_menus", 
	"generate_menu_from_forms"
]

def process_user_forms(db, form_ids):
	forms = db.get_user_forms(form_ids)
	form_list = []
	for f in forms :
		print f
		form_id = int(f["form_id"])
		form_name = f["form_name"]
		form_url = f["form_url"]
		form_type = f["form_type"]
		parent_menu = f["parent_menu"]
		form = core.Form(form_id, form_name, form_url, parent_menu, form_type)
		form_list.append(form)
	return process_user_menus(form_list)

def process_user_menus(form_list):
	menus = {}

	for form in form_list:
		form_type = form.form_type
		_forms = menus.get(form_type)
		if _forms is None :
			_forms = []
		_forms.append(form)
		menus[form_type] = _forms
	print menus
	return core.Menu(menus)
