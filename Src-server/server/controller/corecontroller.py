import collections

from protocol import core

from server.database.general import get_user_forms
from server.clientdatabase.general import get_client_user_forms

__all__ = [
    "process_user_forms", "process_user_menus", "process_admin_forms"
]


def process_user_forms(
    db, form_ids, client_id=None, is_admin=None
):
    forms = None
    if client_id is not None:
        forms = get_client_user_forms(db, form_ids, is_admin)
    else:
        if type(form_ids) is list:
            form_ids = ', '.join(form_ids)
        forms = get_user_forms(db, form_ids)
    form_list = []
    for f in forms:
        form_id = int(f["form_id"])
        form_name = f["form_name"]
        form_url = f["form_url"]
        form_type = f["form_type"]
        parent_menu = f["parent_menu"]
        form = core.Form(form_id, form_name, form_url, parent_menu, form_type)
        form_list.append(form)
    return process_user_menus(form_list)


def process_admin_forms(data):
    form_list = []
    for f in data:
        form_id = int(f["form_id"])
        form_name = f["form_name"]
        form_url = f["form_url"]
        form_type = f["form_type"]
        parent_menu = f["parent_menu"]
        print "form_name: %s" % form_name
        form = core.Form(form_id, form_name, form_url, parent_menu, form_type)
        form_list.append(form)
    return process_user_menus(form_list)


def process_user_menus(form_list):
    menus = {}
    for form in form_list:
        form_type = form.form_type
        print "form_name: %s, form_type: %s" % (form.form_name, form.form_type)
        _forms = menus.get(form_type)
        if _forms is None:
            _forms = []
        _forms.append(form)
        menus[form_type] = _forms
    menus = reorder_menu(menus)
    return core.Menu(menus)


def reorder_menu(menus):
    new_menu = collections.OrderedDict()
    if "Home" in menus:
        new_menu["Home"] = menus["Home"]
    if "Master" in menus:
        new_menu["Master"] = menus["Master"]
    if "Transaction" in menus:
        new_menu["Transaction"] = menus["Transaction"]
    if "Report" in menus:
        new_menu["Report"] = menus["Report"]
    if "Settings" in menus:
        new_menu["Settings"] = menus["Settings"]
    return new_menu
