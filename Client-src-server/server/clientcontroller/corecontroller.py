import base64
import collections

from clientprotocol import clientcore


# from server.clientdatabase.general import get_client_user_forms

__all__ = [
    "process_user_forms", "process_user_menus", "process_admin_forms"
]


# temporarly places here have to rewrite to avoid redundant code

def get_user_forms(db, form_ids):
    columns = "tf.form_id, tf.form_category_id, tfc.form_category," + \
        " tf.form_type_id, tft.form_type, " + \
        " tf.form_name, tf.form_url, tf.form_order, tf.parent_menu"
    tables = ["tbl_forms", "tbl_form_category", "tbl_form_type"]
    aliases = ["tf", "tfc", "tft"]
    join_conditions = [
        "tf.form_category_id = tfc.form_category_id",
        "tf.form_type_id = tft.form_type_id"
    ]
    form_ids_list = [int(x) for x in form_ids.split(",")]
    where_condition, where_condition_val = db.generate_tuple_condition(
        "tf.form_id", form_ids_list
    )
    where_condition += " order by tf.form_order "
    join_type = "left join"
    rows = db.get_data_from_multiple_tables(
        columns, tables,
        aliases, join_type,
        join_conditions, where_condition,
        [where_condition_val]
    )
    return rows

def process_user_forms(
    db, forms, short_name
):
    # print "===============>", forms
    form_list = []
    for f in forms:
        form_id = int(f["form_id"])
        form_name = f["form_name"]
        form_type = f["form_type"]
        form_url = f["form_url"]
        if form_type == "Transaction" :
            form_url += "/" + base64.b64encode(short_name)
        parent_menu = f["parent_menu"]
        form = clientcore.Form(form_id, form_name, form_url, parent_menu, form_type)
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
        # print "form_name: %s" % form_name
        form = clientcore.Form(form_id, form_name, form_url, parent_menu, form_type)
        form_list.append(form)
    return process_user_menus(form_list)


def process_user_menus(form_list):
    menus = {}
    for form in form_list:
        form_type = form.form_type
        # print "form_name: %s, form_type: %s" % (form.form_name, form.form_type)
        _forms = menus.get(form_type)
        if _forms is None:
            _forms = []
        _forms.append(form)
        menus[form_type] = _forms
    menus = reorder_menu(menus)
    return menus
    # return clientcore.Menu(menus)


def reorder_menu(menus):
    new_menu = collections.OrderedDict()
    if "Home" in menus:
        new_menu["Home"] = menus["Home"]
    if "Dashboard" in menus:
        new_menu["Dashboard"] = menus["Dashboard"]
    if "Master" in menus:
        new_menu["Master"] = menus["Master"]
    if "Transaction" in menus:
        new_menu["Transaction"] = menus["Transaction"]
    if "Report" in menus:
        new_menu["Report"] = menus["Report"]
    if "Settings" in menus:
        new_menu["Settings"] = menus["Settings"]
    if "My Accounts" in menus:
        new_menu["My Accounts"] = menus["My Accounts"]
    return new_menu
