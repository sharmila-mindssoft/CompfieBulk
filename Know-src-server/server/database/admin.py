import threading
from protocol import core, admin
from server.database.tables import *
from server.database.forms import *
from server.common import (
    get_date_time, get_current_date,
    addHours, new_uuid
)
from server.emailcontroller import EmailHandler as email
from server.exceptionmessage import process_error
from server.constants import REGISTRATION_EXPIRY, KNOWLEDGE_URL

__all__ = [
    "get_domains_for_user", "save_domain",
    "check_duplicate_domain", "get_domain_by_id",
    "update_domain", "is_transaction_exists_for_domain",
    "update_domain_status",
    "get_countries_for_user", "get_country_by_id",
    "check_duplicate_country", "save_country",
    "update_country", "is_transaction_exists",
    "update_country_status",
    "get_forms", "get_form_categories",
    "is_duplicate_user_group_name",
    "is_user_exists_under_user_group",
    "get_user_groups_from_db",
    "save_user_group", "update_user_group",
    "update_user_group_status",
    "get_detailed_user_list", "is_duplicate_email",
    "is_duplicate_employee_code", "save_user", "update_user",
    "update_user_status", "get_user_group_detailed_list",
    "get_user_countries", "get_user_domains", "get_mapped_countries",
    "get_mapped_domains", "get_validity_dates", "get_country_domain_mappings",
    "save_validity_date_settings", "get_user_mapping_form_data",
    "save_user_mappings", "get_all_user_types", "get_legal_entities_for_user",
    "get_reassign_legal_entity",
    # "get_assigned_legal_entities",
    "get_assigned_units", "get_assigned_clients", "save_registraion_token", "update_disable_status",
    "get_countries_for_user_filter",
    "get_child_users", "get_categories_for_user",
    "get_reassign_user_filters",
    "get_techno_user_data",
    "get_domain_user_data",
    "save_reassign_techno_manager", "save_reassign_techno_executive",
    "save_reassign_domain_manager", "save_reassign_domain_executive",
    "save_user_replacement", "is_user_idle", "get_reassign_client_groups",
    "check_user_mappings", "check_user_replacement"
]


#
# Domain
#
#############################################################################
# To get domains configured under a user
# Parameter(s) : Object of database, user id
# Return Type : List of Object of Domain
#############################################################################
def get_domains_for_user(db, user_id):
    procedure = 'sp_tbl_domains_for_user'
    result = db.call_proc_with_multiresult_set(procedure, (user_id,), 3)
    result.pop(0)
    return return_domains(result)


###############################################################################
# To convert the data fetched from database into List of object of Domain
# Parameter(s) : Data fetched from database
# Return Type : List of Object of Domain
###############################################################################
def return_country_list_of_domain(domain_id, countries):
    c_ids = []
    c_names = []
    for c in countries:
        if int(c["domain_id"]) == domain_id:
            c_ids.append(int(c["country_id"]))
            c_names.append(c["country_name"])

    return c_ids, c_names


def return_domains(data):
    results = []
    for d in data[0]:
        d_id = d["domain_id"]
        c_ids, c_names = return_country_list_of_domain(d_id, data[1])
        results.append(core.Domain(
            c_ids, c_names, d_id, d["domain_name"], bool(d["is_active"])
        ))
    return results


###############################################################################
# To save domain
# Parameter(s) : Object of database, Domain name, session user
# Return Type : Returns True on Successfull save otherwise raises process error
###############################################################################
def save_domain_country(db, c_ids, d_id):
    country_columns = ["country_id", "domain_id"]
    country_values_list = [
       (c_id, d_id) for c_id in c_ids
    ]
    result = db.bulk_insert(
        "tbl_domain_countries", country_columns, country_values_list
    )
    if result is False:
        raise process_error("E034")


def save_domain(db, country_ids, domain_name, user_id):
    domain_id = db.call_insert_proc(
        "sp_domains_save", (None, domain_name, user_id)
    )
    if domain_id is False:
        raise process_error("E024")
    else:
        save_domain_country(db, country_ids, domain_id)
        msg_text = "Domain Name \"" + domain_name + "\" Added"
        print msg_text
        u_cg_id = [3, 5, 7]
        for cg_id in u_cg_id:
            users_id = []
            result = db.call_proc("sp_users_under_user_category", (cg_id,))
            for user in result:
                users_id.append(user["user_id"])
            if len(users_id) > 0:
                db.save_toast_messages(cg_id, "Domain Created", msg_text, None, users_id, user_id)
    action = "Add Domain - \"%s\"" % domain_name
    db.save_activity(user_id, frmDomain, action)
    return True


###############################################################################
# To Check whether the domain name already exists or not
# Parameter(s) : Object of database, Domain name, domain id
# Return Type : Returns True - if duplicate exists, False - If duplicate
#               doesn't exists
###############################################################################
def check_duplicate_domain(db, domain_name, domain_id):
    isDuplicate = False
    result = db.call_proc(
        "sp_domains_is_duplicate", (domain_name, domain_id)
    )
    if (result[0]["count"]) > 0:
        isDuplicate = True
    return isDuplicate


###############################################################################
# To Get the domain name  by it's id
# Parameter(s) : Object of database, domain id
# Return Type : Domain name (String)
###############################################################################
def get_domain_by_id(db, domain_id):
    result = db.call_proc("sp_domains_by_id", (domain_id,))
    if result:
        domain_name = result[0]["domain_name"]
    return domain_name


###############################################################################
# To Update domain
# Parameter(s) : Object of database, domain id, domain name, session user
# Return Type : Returns - True on Successfull update, Raises Process error
#               When update fails
###############################################################################
def update_domain(db, c_ids, domain_id, domain_name, updated_by):
    oldData = get_domain_by_id(db, domain_id)
    if oldData is None:
        return False
    else:
        sdomain_id = db.call_update_proc(
            "sp_domains_save", (domain_id, domain_name, updated_by)
        )
        if sdomain_id:
            db.call_update_proc("sp_domaincountries_delete", (domain_id,))
            save_domain_country(db, c_ids, domain_id)
            u_cg_id = [3, 4, 5, 6, 7, 8]
            msg_text = "Domain Name \"" + oldData + "\" Updated as \"" + domain_name + "\""
            print msg_text
            for cg_id in u_cg_id:
                users_id = []
                result = db.call_proc("sp_domain_users_under_usercategory", (cg_id, domain_id))
                for user in result:
                    users_id.append(user["user_id"])
                if len(users_id) > 0:
                    db.save_toast_messages(cg_id, "Domain Updated", msg_text, None, users_id, updated_by)
            action = "Edit Domain - \"%s\"" % domain_name
            db.save_activity(updated_by, frmDomain, action)
            return True
        else:
            raise process_error("E025")


###############################################################################
# To Check whether transactions exists under a domain or not
# Parameter(s) : Object of database, domain id
# Return Type : Returns - True if transaction exists otherwise return False
###############################################################################
def is_transaction_exists_for_domain(db, domain_id):
    result = db.call_proc_with_multiresult_set(
        "sp_domains_is_transaction_exists", (domain_id,), 2
    )
    statutory_mapped = int(result[0][0]["count"])
    client_mapped = int(result[1][0]["count"])
    if(statutory_mapped > 0 or client_mapped > 0):
        return False
    else:
        return True


###############################################################################
# To Update the status of domain
# Parameter(s) : Object of database, domain id, stauts, session user
# Return Type : Returns - True on Successfull update, otherwise raises
#               process error
###############################################################################
def update_domain_status(db, domain_id, is_active, updated_by):
    updated_on = get_date_time()
    oldData = get_domain_by_id(db, domain_id)
    if oldData is None:
        return False
    else:
        result = db.call_update_proc(
            "sp_domains_change_status",
            (domain_id, is_active, updated_by, updated_on)
        )
        if is_active == 0:
            msg_text = "Domain Name \"" + oldData + "\" Deactivated "
        else:
            msg_text = "Domain Name \"" + oldData + "\" Activated "
        if result:
            u_cg_id = [3, 4, 5, 6, 7, 8]
            for cg_id in u_cg_id:
                users_id = []
                result = db.call_proc("sp_domain_users_under_usercategory", (cg_id, domain_id))
                for user in result:
                    users_id.append(user["user_id"])
                if len(users_id) > 0:
                    db.save_toast_messages(cg_id, "Domain Status Updated", msg_text, None, users_id, updated_by)
            action = "Domain %s status  - %s" % (
                oldData, "deactivated" if is_active == 0 else "activated"
            )
            db.save_activity(updated_by, frmDomain, action)
            return True
        else:
            raise process_error("E026")


#
# Country
#
#############################################################################
# To get country ids configured under a user
# Parameter(s) : Object of database, user id
# Return Type : List of country ids (List of Integer)
#############################################################################
def get_user_countries(db, user_id):
    rows = db.call_proc("sp_usercountries_by_userid", (user_id,))
    country_ids = []
    for r in rows:
        country_ids.append(int(r["country_id"]))
    return country_ids


#############################################################################
# To get domain ids configured under a user
# Parameter(s) : Object of database, user id
# Return Type : List of domain ids (List of Integer)
#############################################################################
def get_user_domains(db, user_id):
    rows = db.call_proc("sp_userdomains_by_userid", (user_id,))
    domain_ids = []
    for r in rows:
        domain_ids.append(int(r["domain_id"]))
    return domain_ids

#
# Level One Statutory
#
#############################################################################
# To get level one statutory list
# Parameter(s) : Object of database
# Return Type : List of level one statutoriesdetails
#############################################################################
def get_level_1_statutories(db):
    results = []
    rows = db.call_proc("sp_levelone_statutories", ())
    for row in rows:
        results.append(core.Level1StatutoryList(
            row["statutory_id"], row["statutory_name"], row["country_id"], row["domain_id"])
        )
    return results


#############################################################################
# To get countries configured under a user
# Parameter(s) : Object of database, user id
# Return Type : List of Object of Countries
#############################################################################
def get_countries_for_user(db, user_id):
    result = db.call_proc_with_multiresult_set("sp_countries_for_user", [user_id], 2)
    if len(result) > 1:
        result = result[1]
    return return_countries(result)


###############################################################################
# To convert the data fetched from database into List of object of Country
# Parameter(s) : Data fetched from database
# Return Type : List of Object of Country
###############################################################################
def return_countries(data):
    results = []
    for d in data:
        results.append(core.Country(
            d["country_id"], d["country_name"], bool(d["is_active"])
        ))
    return results


#############################################################################
# To get countries configured under a user for report filters
# Parameter(s) : Object of database, user id
# Return Type : List of Object of Countries
#############################################################################
def get_countries_for_user_filter(db, user_id):
    result = db.call_proc_with_multiresult_set("sp_countries_for_user_filter", (user_id,), 2)
    return return_countries_filter(result)


###############################################################################
# To convert the data fetched from database into List of object of Country
# Parameter(s) : Data fetched from database
# Return Type : List of Object of Country
###############################################################################
def return_countries_filter(data):
    results = []
    for d in data[1]:
        results.append(core.Country(
            d["country_id"], d["country_name"], bool(d["is_active"])
        ))
    return results

###############################################################################
# To Get the country name  by it's id
# Parameter(s) : Object of database, country id
# Return Type : Country name (String)
###############################################################################
def get_country_by_id(db, country_id):
    result = db.call_proc("sp_countries_by_id", (country_id,))
    country_name = result[0]["country_name"]
    return country_name


###############################################################################
# To Check whether the country name already exists or not
# Parameter(s) : Object of database, Country name, country id
# Return Type : Returns True - if duplicate exists, False - If duplicate
#               doesn't exists
###############################################################################
def check_duplicate_country(db, country_name, country_id):
    isDuplicate = False
    result = db.call_proc(
        "sp_countries_is_dupliacte", (country_name, country_id)
    )
    count = result[0]["count"]
    if count > 0:
        isDuplicate = True
    return isDuplicate


###############################################################################
# To save Country
# Parameter(s) : Object of database, Country name, session user id
# Return Type : Returns True on Successfull save otherwise raises process error
###############################################################################
def save_country(db, country_name, created_by):
    created_on = get_date_time()
    country_id = db.call_insert_proc(
        "sp_countries_save", (None, country_name, created_by, created_on)
    )
    msg_text = "Country Name \"" + country_name + "\" Added "
    if country_id:
        u_cg_id = [3, 5, 7]
        for cg_id in u_cg_id:
            users_id = []
            result = db.call_proc("sp_users_under_user_category", (cg_id,))
            for user in result:
                users_id.append(user["user_id"])
            if len(users_id) > 0:
                db.save_toast_messages(cg_id, "Country Created", msg_text, None, users_id, created_by)
        action = "Add Country - \"%s\"" % country_name
        db.save_activity(created_by, frmCountry, action)
        return True
    else:
        raise process_error("E027")


###############################################################################
# To Update country
# Parameter(s) : Object of database, country id, country name, session user id
# Return Type : Returns - True on Successfull update, Raises Process error
#               When update fails
###############################################################################
def update_country(db, country_id, country_name, updated_by):
    updated_on = get_date_time()
    oldData = get_country_by_id(db, country_id)
    if oldData is None:
        return False
    else:
        result = db.call_update_proc(
            "sp_countries_save",
            (country_id, country_name, updated_by, updated_on)
        )
        msg_text = "Country Name \"" + oldData + "\" Updated as \"" + country_name + "\""
        if result:
            u_cg_id = [3, 4, 5, 6, 7, 8]
            for cg_id in u_cg_id:
                users_id = []
                result = db.call_proc("sp_country_users_under_usercategory", (cg_id, country_id))
                for user in result:
                    users_id.append(user["user_id"])
                if len(users_id) > 0:
                    db.save_toast_messages(cg_id, "Country Updated", msg_text, None, users_id, updated_by)
            action = "Edit Country - \"%s\"" % country_name
            db.save_activity(updated_by, frmCountry, action)
            return True
        else:
            raise process_error("E028")


###############################################################################
# To Check whether transactions exists under a country or not
# Parameter(s) : Object of database, country id
# Return Type : Returns - True if transaction exists otherwise return False
###############################################################################
def is_transaction_exists(db, country_id):
    result = db.call_proc_with_multiresult_set(
        "sp_countries_is_transaction_exists", (country_id,), 2
    )
    statutory_mapped = int(result[0][0]["count"])
    client_mapped = int(result[1][0]["count"])
    if(statutory_mapped > 0 or client_mapped > 0):
        return False
    else:
        return True


###############################################################################
# To Update the status of country
# Parameter(s) : Object of database, country id, stauts, session user
# Return Type : Returns - True on Successfull update, otherwise raises
#               process error
###############################################################################
def update_country_status(db, country_id, is_active, updated_by):
    updated_on = get_date_time()
    oldData = get_country_by_id(db, country_id)
    if oldData is None:
        return False
    else:
        result = db.call_update_proc(
            "sp_countries_change_status",
            (country_id, is_active, updated_by, updated_on)
        )
        if is_active == 0:
            msg_text = "Country Name \"" + oldData + "\" Deactivated "
        else:
            msg_text = "Country Name \"" + oldData + "\" Activated "

        if result:
            u_cg_id = [3, 4, 5, 6, 7, 8]
            for cg_id in u_cg_id:
                users_id = []
                result = db.call_proc("sp_country_users_under_usercategory", (cg_id, country_id))
                for user in result:
                    users_id.append(user["user_id"])
                if len(users_id) > 0:
                    db.save_toast_messages(cg_id, "Country Status Updated", msg_text, None, users_id, updated_by)
            action = "Country %s status  - %s" % (
                oldData, "deactivated" if is_active == 0 else "activated"
            )
            db.save_activity(updated_by, frmCountry, action)
            return True
        else:
            raise process_error("E029")


#
#   Forms
#
###############################################################################
# To get all Forms
# Parameter(s) : Object of database
# Return Type : Returns data fetched from database (Tuplse)
###############################################################################
def get_forms(db):
    # Category wise forms list result set
    return db.call_proc_with_multiresult_set("sp_categorywise_forms_list", None, 6)


###############################################################################
# To get all Form categories
# Parameter(s) : Object of database
# Return Type : Returns data fetched from database (Tuplse)
###############################################################################
def get_form_categories(db):
    return db.call_proc("sp_usercategory_list", None)


#
#   Admin User Group
#
###############################################################################
# To Check whether the user group name already exists or not
# Parameter(s) : Object of database, user group name, user group id
# Return Type : Returns True - if duplicate exists, False - If duplicate
#               doesn't exists
###############################################################################
def is_duplicate_user_group_name(db, user_group_name, user_group_id=None):
    result = db.call_proc(
        "sp_usergroup_is_duplicate", (user_group_id, user_group_name)
    )
    if result[0]["count"] > 0:
        return True
    else:
        return False


###############################################################################
# To Check whether users where created under the user group or not
# Parameter(s) : Object of database, user group id
# Return Type : Returns True - if users exists, False - If users doesn't exists
###############################################################################
def is_user_exists_under_user_group(db, user_group_id):
    rows = db.call_proc(
        "sp_usergroup_is_transaction_exists", (user_group_id, )
    )
    if rows[0]["count"] > 0:
        return True
    else:
        return False


###############################################################################
# To get List of all user groups with all details
# Parameter(s) : Object of database
# Return Type : Returns data fetched from database (Tuple)
###############################################################################
def get_user_group_detailed_list(db):
    return db.call_proc_with_multiresult_set("sp_usergroup_detailed_list", None, 2)


###############################################################################
# To get List of all user groups (only id, name and status)
# Parameter(s) : Object of database
# Return Type : Returns data fetched from database (Tuple)
###############################################################################
def get_user_groups_from_db(db):
    return db.call_proc_with_multiresult_set("sp_usergroup_list", None, 2)


###############################################################################
# To save User group
# Parameter(s) : Object of database, user group name (String),
# form category id (INT), List of form ids (List of integer), session user id
# Return Type : Returns True on Successfull save otherwise raises process error
###############################################################################
def user_group_forms(db, user_group_id, form_ids):
    table = "tbl_user_group_forms"
    db.delete(table, "user_group_id = %s", [user_group_id])
    column = ["user_group_id", "form_id"]
    value_list = []
    for f in form_ids:
        value_list.append((user_group_id, f))
    return db.bulk_insert(table, column, value_list)


def save_user_group(
    db, user_group_name, user_category_id, form_ids, session_user
):
    ug_id = db.call_insert_proc(
        "sp_usergroup_save",
        (
            None, user_category_id, user_group_name, session_user
        )
    )
    if ug_id:
        if user_group_forms(db, ug_id, form_ids) is True :
            action = "Created User Group \"%s\"" % user_group_name
            db.save_activity(session_user, frmUserGroup, action)
            return True
        else:
            return False
    else:
        raise process_error("E030")


###############################################################################
# To update User group
# Parameter(s) : Object of database, user group id, user group name (String),
# form category id (INT), List of form ids (List of integer), session user id
# Return Type : Returns True on Successfull update otherwise raises
#   process error
###############################################################################
def update_user_group(
    db, user_group_id, user_group_name, user_category_id, form_ids,
    session_user
):
    result = db.call_update_proc(
        "sp_usergroup_save",
        (
            user_group_id, user_category_id, user_group_name,
            session_user
        )
    )
    if result:
        if user_group_forms(db, user_group_id, form_ids) is True :
            action = "Updated User Group \"%s\"" % user_group_name
            db.save_activity(session_user, frmUserGroup, action)
            return True
        else:
            return False
    else:
        raise process_error("E031")


###############################################################################
# To update the status of user group
# Parameter(s) : Object of database, user group id, is_active, session user id
# Return Type : True on Successfull update otherwise raises process error
###############################################################################
def update_user_group_status(db, user_group_id, ug_name, is_active, session_user):
    result = db.call_update_proc(
        "sp_usergroup_change_status",
        (
            user_group_id, is_active, session_user
        )
    )
    if result is False:
        raise process_error("E032")

    action = "%s User Group \"%s\"" % (
        "Deactivated" if is_active == 0 else "Activated",
        ug_name
    )
    db.save_activity(session_user, frmUserGroup, action)
    return result


#
# Admin User
#
###############################################################################
# To get List of all users with all details
# Parameter(s) : Object of database
# Return Type : Returns data fetched from database (Tuple)
###############################################################################
def get_detailed_user_list(db):
    return db.call_proc_with_multiresult_set("sp_user_detailed_list", None, 3)


###############################################################################
# To Check whether the email id already exists or not
# Parameter(s) : Object of database, email id, session user id
# Return Type : Returns True - if duplicate exists, False - If duplicate
#               doesn't exists
###############################################################################
def is_duplicate_email(db, email_id, user_id=None):
    rows = db.call_proc("sp_user_is_duplicate_email", (email_id, user_id))
    if rows[0]["count"] > 0:
        return True
    else:
        return False


###############################################################################
# To Check whether the employee code already exists or not
# Parameter(s) : Object of database, employee code, session user id
# Return Type : Returns True - if duplicate exists, False - If duplicate
#               doesn't exists
###############################################################################
def is_duplicate_employee_code(db, employee_code, user_id=None):
    rows = db.call_proc(
        "sp_user_is_duplicate_employeecode", (employee_code, user_id))
    if rows[0]["count"] > 0:
        return True
    else:
        return False

def save_registraion_token(db, user_id, emp_name, email_id):
    def _del_olddata():
        condition = "user_id = %s and verification_type_id = %s"
        condition_val = [user_id, 1]
        db.delete(tblEmailVerification, condition, condition_val)
        return True

    current_time_stamp = get_current_date()
    registration_token = new_uuid()
    expiry_date = addHours(int(REGISTRATION_EXPIRY), current_time_stamp)

    link = "%s/userregistration/%s" % (
        KNOWLEDGE_URL, registration_token
    )

    notify_user_thread = threading.Thread(
        target=notify_user, args=[
            email_id, emp_name, link
        ]
    )
    notify_user_thread.start()

    if (_del_olddata()):
        db.call_insert_proc(
            "sp_tbl_email_verification_save",
            (user_id, registration_token, 1, expiry_date)
        )
        return True
    else:
        return False


###############################################################################
# To save User
# Parameter(s) : Object of database, email id, user group id, employee name,
#                employee code, contact number, address, designation,
#               list of country ids, list of domain ids, session user id
# Return Type : Returns True on Successfull save otherwise raises process error
###############################################################################
def save_user(
    db, user_category_id, email_id, user_group_id, employee_name,
    employee_code, contact_no, mobile_no,
    address, designation, country_ids, domain_ids,
    session_user
):
    # current_time_stamp = get_date_time()
    # encrypted_password, password = generate_and_return_password()
    user_id = db.call_insert_proc(
        "sp_users_save", (
            user_category_id, None, email_id, user_group_id,
            employee_name, employee_code, contact_no, mobile_no,
            address, designation, session_user)
    )
    if user_id is False:
        raise process_error("E033")
    save_user_countries(db, country_ids, user_id, session_user)
    save_user_domains(db, domain_ids, user_id, session_user)
    action = "Created User \"%s - %s\"" % (employee_code, employee_name)
    db.save_activity(session_user, frmUserManagement, action)
    name = "%s - %s" % (employee_code, employee_name)
    save_registraion_token(db, user_id, name, email_id)

    return True


###############################################################################
# To Send the credentials to the user
# Parameter(s) : email id, password, employee name, employee code
# Return Type : if the email fails raises exception
###############################################################################
def notify_user(
    email_id, emp_name, link
):
    try:
        email().send_registraion_link(email_id, emp_name, link)
    except Exception, e:
        print "Error while sending email"
        print e


###############################################################################
# To Save Countries configured for the user
# Parameter(s) : Object of database, list of country ids, user id
# Return Type : Returns None on Successfull save otherwise raises process error
###############################################################################
def save_user_countries(
    db, country_ids, user_id, session_user
):
    current_time_stamp = get_date_time()
    country_columns = ["user_id", "country_id", "assigned_by", "assigned_on"]
    country_values_list = [
       (user_id, int(country_id), session_user, current_time_stamp) for country_id in country_ids
    ]
    result = db.bulk_insert(
        tblUserCountries, country_columns, country_values_list
    )
    if result is False:
        raise process_error("E034")


###############################################################################
# To Save Domains configured for the user
# Parameter(s) : Object of database, list of domain ids, user id
# Return Type : Returns None on Successfull save otherwise raises process error
###############################################################################
def save_user_domains(
    db, domain_ids, user_id, session_user
):
    current_time_stamp = get_date_time()
    domain_columns = ["user_id", "domain_id", "country_id", "assigned_by", "assigned_on"]
    domain_values_list = [
        (user_id, int(d.domain_id), int(d.country_id), session_user, current_time_stamp) for d in domain_ids
    ]
    result = db.bulk_insert(
        tblUserDomains, domain_columns, domain_values_list
    )
    if result is False:
        raise process_error("E035")


###############################################################################
# To update User
# Parameter(s) : Object of database, user id, user group id, employee name,
# employee code, contact no, address, designation, List of country ids,
# List of domain ids, session user id
# Return Type : Returns True on Successfull update otherwise raises
#   process error
###############################################################################
def update_user(
    db, user_id, user_category_id, email_id, user_group_id, employee_name,
    employee_code, contact_no, mobile_no,
    address, designation, country_ids, domain_ids,
    session_user
):
    result = db.call_update_proc(
        "sp_users_save", (
            user_category_id, user_id, email_id, user_group_id,
            employee_name, employee_code, contact_no, mobile_no,
            address, designation, session_user)
    )
    if result is False:
        raise process_error("E036")
    db.call_update_proc("sp_usercountries_delete", (user_id,))
    db.call_update_proc("sp_userdomains_delete", (user_id,))
    save_user_countries(db, country_ids, user_id, session_user)
    save_user_domains(db, domain_ids, user_id, session_user)
    action = "Updated User \"%s - %s\"" % (employee_code, employee_name)
    db.save_activity(session_user, frmUserManagement, action)
    return True


###############################################################################
# To Check whether the user group of user is active or not
# Parameter(s) : Object of database, user id
# Return Type : If the user group is inactive raises process error
###############################################################################
def check_user_group_active_status(db, user_id):
    row = db.call_proc("sp_user_usergroup_status", (user_id,))
    if int(row[0]["group_count"]) == 0:
        raise process_error("E065")


###############################################################################
# To Update the status of user
# Parameter(s) : Object of database, user id, active status
# Return Type : Returns True on Successfull update, Other wise raises process
#               error
###############################################################################
def update_user_status(db, user_id, is_active, session_user):
    check_user_group_active_status(db, user_id)
    result = db.call_update_proc(
        "sp_users_change_status",
        (user_id, is_active, session_user, get_date_time())
    )
    if result is False:
        raise process_error("E039")

    rows = db.call_proc("sp_empname_by_id", (user_id, ))
    employee_name = rows[0]["empname"]
    action = ""
    if is_active == 1:
        action = "Activated User \"%s\"" % employee_name
    else:
        action = "Dectivated User \"%s\"" % employee_name
    db.save_activity(session_user, frmUserManagement, action)
    return result


###############################################################################
# To Update the status of user
# Parameter(s) : Object of database, user id, active status
# Return Type : Returns True on Successfull update, Other wise raises process
#               error
###############################################################################
def update_disable_status(db, user_id, is_disable, remarks, session_user):
    result = db.call_update_proc(
        "sp_users_disable_status",
        (user_id, is_disable, session_user, get_date_time(), remarks)
    )
    if result is False:
        raise process_error("E039")

    rows = db.call_proc("sp_empname_by_id", (user_id, ))
    employee_name = rows[0]["empname"]
    action = ""
    if is_disable == 1:
        action = "Disabled User \"%s\"" % employee_name
    else:
        action = "Enabled User \"%s\"" % employee_name
    db.save_activity(session_user, frmUserManagement, action)
    return result


def is_user_idle(db, user_id):
    rows = db.call_proc("sp_get_user_mapped_data", [user_id], 1)
    if rows:
        print "user_id>>", user_id
        print "rows[0].get(cnt)>>", rows[0].get('cnt')
        if rows[0].get('cnt') > 0:
            return False
    else:
        return True


#####################################################################
# To Fetch Countries which are mapped to Domains
# Parameter(s) : Object of database
# Return Type : List of Object of Country
#####################################################################
def get_mapped_countries(db):
    result = db.call_proc(
        "sp_country_mapped_list", None
    )
    return return_countries(result)


#####################################################################
# To Fetch Domains which are mapped to Country
# Parameter(s) : Object of database
# Return Type : List of Object of Domain
#####################################################################
def get_mapped_domains(db):
    result = db.call_proc_with_multiresult_set(
        "sp_domain_mapped_list", None, 2
    )
    return return_domains(result)


#####################################################################
# To Fetch Validity Dates from Table
# Parameter(s) : Object of database
# Return Type : List of Object of ValidityDates
#####################################################################
def get_validity_dates(db):
    result = db.call_proc(
        "sp_validitydays_settings_list", None
    )
    return return_validity_days(result)


#####################################################################
# To Structure the tuple of data into List of ValidityDates object
# Parameter(s) : Data to be converted
# Return Type : List of Object of ValidityDates
#####################################################################
def return_validity_days(data):
    fn = core.ValidityDates
    validity_date_list = [
        fn(
            datum["validity_date_id"],
            datum["country_id"], datum["domain_id"],
            datum["days"]
        ) for datum in data
    ]
    return validity_date_list


#####################################################################
# To Fetch country domain mappings from statutory levels table
# Parameter(s) : Object of database
# Return Type : Dict (key: country id, value: list of domain ids)
#####################################################################
def get_country_domain_mappings(db):
    result = db.call_proc(
        "sp_statutorylevels_mappings", None
    )
    return return_country_domain_mappings(result)


#####################################################################
# To convert tuple of data into dictionary
# Parameter(s) : Data to be converted
# Return Type : Dict (key: country id, value: list of domain ids)
#####################################################################
def return_country_domain_mappings(data):
    country_domain_map = {}
    for datum in data:
        country_id = datum["country_id"]
        domain_id = datum["domain_id"]
        if country_id not in country_domain_map:
            country_domain_map[country_id] = []
        if domain_id not in country_domain_map[country_id]:
            country_domain_map[country_id].append(domain_id)
    return country_domain_map


#####################################################################
# To save validity date settings
# Parameter(s) : Object of database, data to be saved, session user
# Return Type : None
#####################################################################
def save_validity_date_settings(db, data, session_user):
    current_time_stamp = get_date_time()
    country_id = None
    domain_id = None
    for datum in data:
        if (datum.validity_days < 0 or datum.validity_days > 366):
            country_id = datum.country_id
            domain_id = datum.domain_id
            break
        else:
            continue
        return admin.SaveValidityDateSettingsFailure(domain_id, country_id)

    for datum in data:
        if (datum.validity_days >= 0 and datum.validity_days <= 366):
            validity_days_id = datum.validity_days_id
            country_id = datum.country_id
            domain_id = datum.domain_id
            validity_days = datum.validity_days
            db.call_insert_proc(
                "sp_validitydays_settings_save", (
                    validity_days_id, country_id, domain_id, validity_days,
                    session_user, current_time_stamp, session_user,
                    current_time_stamp
                )
            )
            query = "select country_name from tbl_countries where country_id = %s"
            c_rows = db.select_one(query, (country_id,))

            query = "select domain_name from tbl_domains where domain_id = %s"
            d_rows = db.select_one(query, (domain_id,))

            action = "Validity days updated for \"%s\" under \"%s\"" % (
                d_rows["domain_name"], c_rows["country_name"]
            )
            db.save_activity(session_user, frmValidityDateSettings, action)
    return admin.SaveValidityDateSettingsSuccess()


def get_user_mappings(db):
    data = db.call_proc("sp_usermappings_list", None)
    return return_user_mapping_users(data)


def return_user_mapping_users(data):
    result = []
    for datum in data:
        fn = admin.UserMapping
        mapping = fn(
                user_mapping_id=datum["user_mapping_id"],
                parent_user_id=datum["parent_user_id"],
                child_user_id=datum["child_user_id"],
                country_id=datum["country_id"],
                domain_id=datum["domain_id"],
            )
        result.append(mapping)

    return result


def return_users(data, country_map, domain_map):
    fn = admin.User
    result = []
    for datum in data:
        user_id = int(datum["user_id"])
        user = fn(
            user_id=user_id, employee_name=datum["employee_name"],
            is_active=bool(datum["is_active"]),
            country_ids=country_map[user_id],
            domain_ids=domain_map[user_id]
        )
        result.append(user)
    return result


def generate_country_map(countries):
    country_map = {}
    for country in countries:
        user_id = country["user_id"]
        if user_id not in country_map:
            country_map[user_id] = []
        country_map[user_id].append(
            int(country["country_id"])
        )
    return country_map


def generate_domain_map(domains):
    domain_map = {}
    for domain in domains:
        user_id = domain["user_id"]
        if user_id not in domain_map:
            domain_map[user_id] = []
        domain_map[user_id].append(
            int(domain["domain_id"])
        )
    return domain_map


def get_all_user_types(db):
    result = db.call_proc_with_multiresult_set("sp_users_type_wise", None, 8)
    user_countries = result[6]
    user_domains = result[7]
    user_countries_map = generate_country_map(user_countries)
    user_domains_map = generate_domain_map(user_domains)

    knowledge_managers_result = result[0]
    knowledge_users_result = result[1]
    techno_managers_result = result[2]
    techno_users_result = result[3]
    domain_managers_result = result[4]
    domain_users_result = result[5]
    knowledge_managers = return_users(
        knowledge_managers_result, user_countries_map, user_domains_map)
    knowledge_users = return_users(
        knowledge_users_result, user_countries_map, user_domains_map)
    techno_managers = return_users(
        techno_managers_result, user_countries_map, user_domains_map)
    techno_users = return_users(
        techno_users_result, user_countries_map, user_domains_map)
    domain_managers = return_users(
        domain_managers_result, user_countries_map, user_domains_map)
    domain_users = return_users(
        domain_users_result, user_countries_map, user_domains_map)
    return (
        knowledge_managers, knowledge_users, techno_managers, techno_users,
        domain_managers, domain_users)


def get_user_mapping_form_data(db, session_user):
    countries = get_countries_for_user(db, session_user)
    domains = get_domains_for_user(db, session_user)
    (
        knowledge_managers, knowledge_users, techno_managers, techno_users,
        domain_managers, domain_users
    ) = get_all_user_types(db)
    user_mappings = get_user_mappings(db)
    return (
        countries, domains, knowledge_managers, knowledge_users,
        techno_managers, techno_users, domain_managers, domain_users,
        user_mappings
    )

def check_user_mappings(db, request, session_user):
    country_id = request.country_id
    domain_id = request.domain_id
    parent_user_id = request.parent_user_id
    child_user_id = request.child_user_id
    user_cat_id = request.user_category_id

    rows = db.call_proc("sp_check_user_mapping", [country_id, domain_id, parent_user_id, child_user_id, user_cat_id], 1)
    if rows :
        if rows[0].get('cnt') > 0 :
            return False
    else :
        return True

def save_user_mappings(db, request, session_user):
    current_time_stamp = get_date_time()
    country_id = request.country_id
    domain_id = request.domain_id
    parent_user_id = request.parent_user_id
    child_users = request.child_users
    user_cat_id = request.user_category_id
    new_child_users = request.new_child_users
    new_child_user_names = request.new_child_user_names

    country_name = get_country_by_id(db, country_id)
    domain_name = get_domain_by_id(db, domain_id)

    insert_columns = [
        "user_category_id", "country_id", "domain_id", "parent_user_id",
        "child_user_id", "created_by", "created_on"
    ]
    cat_rows = db.call_proc("sp_users_category_by_id", (parent_user_id,))
    user_category_id = cat_rows[0]["user_category_id"]
    insert_values = [
        (
            user_category_id, country_id, domain_id, parent_user_id,
            child_user_id, session_user, current_time_stamp
        ) for child_user_id in child_users
    ]
    db.call_update_proc("sp_usermapping_delete", (parent_user_id, country_id, domain_id))
    result = db.bulk_insert(
        tblUserMapping, insert_columns, insert_values
    )
    if result:
        name_rows = db.call_proc("sp_empname_by_id", (parent_user_id,))
        action = "Users mapped for - \"%s\"" % name_rows[0]["empname"]
        db.save_activity(session_user, frmUserMapping, action)

        if len(new_child_users) > 0:
            child_users_name = ','.join(new_child_user_names);
            parent_user_ids = []
            parent_user_ids.append(parent_user_id)

            message_text = '\"%s\" has been mapped with \"%s\" in %s, %s Domain' % (name_rows[0]["empname"], child_users_name, country_name, domain_name)
            db.save_toast_messages(user_category_id, "User Mapping", message_text, None, parent_user_ids, session_user)

            child_message_text = 'User has been mapped under \"%s\" in %s, %s Domain' % (name_rows[0]["empname"], country_name, domain_name)
            db.save_toast_messages(user_cat_id, "User Mapping", child_message_text, None, new_child_users, session_user)

    else:
        raise process_error("E079")

def get_legal_entities_for_user(db, user_id):
    result = db.call_proc(
        "sp_tbl_unit_getclientlegalentity", [user_id])
    return return_legal_entities_for_unit(result)

def get_reassign_legal_entity(db, user_id):
    result = db.call_proc_with_multiresult_set(
        "sp_get_reassign_legalentity", [user_id], 2)
    return return_legal_entities_for_unit(result)

def return_legal_entities_for_unit(legal_entities):
    results = []
    for legal_entity in legal_entities[0]:
        d_ids = []
        for d in legal_entities[1]:
            if d["legal_entity_id"] == legal_entity["legal_entity_id"] :
                d_ids.append(d["domain_id"])
        legal_entity_obj = admin.LegalEntity(
            legal_entity_id=legal_entity["legal_entity_id"],
            legal_entity_name=legal_entity["legal_entity_name"],
            business_group_id=legal_entity["business_group_id"],
            client_id=legal_entity["client_id"],
            country_id=legal_entity["country_id"],
            domain_ids=d_ids
        )
        results.append(legal_entity_obj)
    return results


# def save_reassigned_user_account_history(db, request, session_user):
#     try:
#         old_user_id = request.old_user_id
#         new_user_id = request.new_user_id
#         assigned_ids = request.assigned_ids
#         remarks = request.remarks
#         user_type = request.user_type
#         current_time_stamp = get_date_time()
#         data = db.call_proc(
#             "sp_names_by_id",
#             (",".join(str(x) for x in assigned_ids), user_type),
#         )
#         names = ''
#         for datum in data:
#             names += datum["name"]

#         if user_type == 5:
#             reassigned_data = "Following groups were reassigned :- %s " % (
#                 names)
#         elif user_type == 6:
#             reassigned_data = "Following legal entities were " + \
#                 " reassigned :- %s" % (
#                     names)
#         else:
#             reassigned_data = "Following units were reassigned :- %s" % (names)
#         db.call_insert_proc(
#             "sp_reassignaccounthistory_save", (
#                 old_user_id, new_user_id,  reassigned_data, remarks,
#                 session_user, current_time_stamp
#             )
#         )
#     except Exception, e:
#         print e
#         raise process_error("E081")


# def save_reassigned_user_account(db, request, session_user):
#     save_reassigned_user_account_history(db, request, session_user)
#     try:
#         user_type = request.user_type
#         current_time_stamp = get_date_time()
#         columns = ["user_id", "assigned_by", "assigned_on"]
#         value_list = []
#         conditions = []
#         table = None
#         for assigned_id in request.assigned_ids:
#             value_list.append(
#                 (request.new_user_id, session_user, current_time_stamp)
#             )
#             if user_type == 5:
#                 condition = "client_id=%s" % (assigned_id)
#                 table = tblUserClients
#             elif user_type == 6:
#                 condition = "legal_entity_id=%s" % (assigned_id)
#                 table = tblUserLegalEntity
#             else:
#                 condition = "unit_id = %s" % (assigned_id)
#                 table = tblUserUnits
#             conditions.append(condition)
#         db.bulk_update(
#             table, columns, value_list, conditions
#         )
#     except Exception, e:
#         print e
#         raise process_error("E082")


def get_assigned_legal_entities(db):
    result = db.call_proc("sp_userlegalentities_assigned_list", None)
    return return_assigned_legal_entities(result)


def return_assigned_legal_entities(data):
    fn = admin.AssignedLegalEntities
    result = [
        fn(
            user_id=datum["user_id"],
            legal_entity_id=datum["legal_entity_id"]
        ) for datum in data
    ]
    return result


def get_assigned_units(db):
    result = db.call_proc("sp_userunits_reassign_list", None)
    return return_assigned_units(result)


def return_assigned_units(data):
    fn = admin.AssignedUnits
    result = [
        fn(
            user_id=datum["user_id"],
            unit_id=datum["unit_id"],
            domain_id=datum["domain_id"]
        )for datum in data
    ]
    return result


def get_assigned_clients(db):
    result = db.call_proc("sp_userclients_reassign_list", None)
    return return_assigned_clients(result)


def return_assigned_clients(data):
    fn = admin.AssignedClient
    result = [
        fn(
            user_id=datum["user_id"],
            client_id=datum["client_id"]
        )for datum in data
    ]
    return result


def get_child_users(db, user_id):
    result = db.call_proc("sp_user_knowledge_executives", [user_id])
    data = []
    for r in result:
        data.append(core.ChildUsers(r["child_user_id"], r["emp_name"]))

    return data


def get_categories_for_user(db, user_id):
    result = db.call_proc_with_multiresult_set("sp_get_user_categories_for_user", (user_id,), 2)
    data = []
    for r in result[1]:
        data.append(core.UserCategory(r["user_category_id"], r["user_category_name"]))

    return data

def get_reassign_client_groups(db, user_id):
    result = db.call_proc("sp_reassign_client_groups_list", [user_id])
    groups = []
    for r in result :
        groups.append(core.ReassignClientGroup(
            r["client_id"], r["group_name"]
        ))
    return groups

def get_reassign_user_filters(db):
    techno_manag = db.call_proc_with_multiresult_set("sp_tbl_users_techno_managers", None, 2)
    techno_execut = db.call_proc_with_multiresult_set("sp_tbl_users_techno_executive", None, 2)
    domain_manag = db.call_proc_with_multiresult_set("sp_tbl_users_domain_managers", None, 4)
    domain_execut = db.call_proc_with_multiresult_set("sp_tbl_users_domain_executive", None, 3)

    techno_manag_users = []
    for t in techno_manag[1] :
        e_name = "%s - %s" % (t["employee_code"], t["employee_name"])
        user_id = t["user_id"]
        c_d_list = []
        for x in techno_manag[0] :
            if x["user_id"] == user_id :
                p_ids = []
                c_d_list.append(admin.CountryWiseDomainParent(x["country_id"], x["domain_id"], p_ids))
        techno_manag_users.append(
            admin.UserInfo(
                t["user_id"], e_name, c_d_list, t["user_category_id"],
                None, None
            )
        )

    techno_exec_users = []
    for t in techno_execut[1] :
        user_id = t["user_id"]
        e_name = "%s - %s" % (t["employee_code"], t["employee_name"])
        c_d_list = []
        for x in techno_execut[0] :
            if x["user_id"] == user_id :
                p_ids = []
                if x["parent_user_ids"] is not None:
                    p_ids = [int(i) for i in x["parent_user_ids"].split(',') if i.strip()!= '']

                c_d_list.append(admin.CountryWiseDomainParent(x["country_id"], x["domain_id"], p_ids))

        techno_exec_users.append(admin.UserInfo(
            user_id, e_name, c_d_list,
            t["user_category_id"], None, None
        ))

    domain_exec_users = []
    for t in domain_execut[1] :
        le_ids = []
        grp_ids = []
        user_id = t["user_id"]
        e_name = "%s - %s" % (t["employee_code"], t["employee_name"])
        c_d_list = []
        for x in domain_execut[0] :
            if x["user_id"] == user_id :
                p_ids = []
                if x["parent_user_ids"] is not None:
                    p_ids = [int(i) for i in x["parent_user_ids"].split(',') if i.strip()!= '']

                c_d_list.append(admin.CountryWiseDomainParent(x["country_id"], x["domain_id"], p_ids))

        for z in domain_execut[2] :
            if z["user_id"] == user_id and z["legal_entity_id"] is not None :
                le_ids.append(z["legal_entity_id"])
                grp_ids.append(z["client_id"])

        grp_ids = set(grp_ids)
        grp_ids = list(grp_ids)
        le_ids = set(le_ids)
        le_ids = list(le_ids)

        domain_exec_users.append(admin.UserInfo(
            user_id, e_name, c_d_list,
            t["user_category_id"], grp_ids, le_ids
        ))

    domain_manag_users = []
    for t in domain_manag[1] :
        user_id = t["user_id"]
        e_name = "%s - %s" % (t["employee_code"], t["employee_name"])
        c_d_list = []
        le_ids = []
        grp_ids = []
        for x in domain_manag[0] :
            if x["user_id"] == user_id :
                p_ids = []
                if x["parent_user_ids"] is not None:
                    p_ids = [int(i) for i in x["parent_user_ids"].split(',') if i.strip()!= '']

                c_d_list.append(admin.CountryWiseDomainParent(x["country_id"], x["domain_id"], p_ids))

        for z in domain_manag[2] :
            if z["user_id"] == user_id and z["legal_entity_id"] is not None :
                le_ids.append(z["legal_entity_id"])
                grp_ids.append(z["client_id"])

        grp_ids = set(grp_ids)
        grp_ids = list(grp_ids)
        le_ids = set(le_ids)
        le_ids = list(le_ids)

        if len(le_ids) == 0 :
            le_ids = None
        if len(grp_ids) == 0 :
            grp_ids = None
        if len(p_ids) == 0 :
            p_ids = None

        domain_manag_users.append(admin.UserInfo(
            user_id, e_name, c_d_list,
            t["user_category_id"], grp_ids, le_ids
        ))

    return (techno_manag_users, techno_exec_users, domain_manag_users, domain_exec_users)

def get_techno_user_data(db, techno_user):
    techno_data = db.call_proc_with_multiresult_set("sp_tbl_users_techno_user_info", [techno_user], 3)

    data_list = []
    for r in techno_data[1] :
        d_ids = []
        d_names = []
        for x in techno_data[2] :
            if x["legal_entity_id"] == r["legal_entity_id"]:
                d_ids.append(x["domain_id"])
                d_names.append(x["domain_name"])

        data_list.append(admin.TechnoEntity(
            r["client_id"], r["group_name"], r["country_id"], r["country_name"],
            d_ids, d_names,
            r["legal_entity_id"], r["legal_entity_name"], r["bg_name"],
            r["user_id"]
        ))

    return data_list

def get_domain_user_data(db, domain_user, group_id, legal_entity_id, domain_id):
    domain_data = db.call_proc("sp_tbl_users_domain_user_info", [group_id, legal_entity_id, domain_id, domain_user])
    data_list = []
    for r in domain_data :

        data_list.append(admin.DomainUnit(
            r["unit_id"], r["unit_code"], r["unit_name"], r["address"],
            r["location"], r["legal_entity_id"], r["legal_entity_name"],
            r["child_user"]
        ))

    return data_list

def save_reassign_techno_manager(db, user_from, data, remarks, session_user):

    reassign_history = "INSERT INTO tbl_user_account_reassign_history (user_category_id, " + \
        "reassigned_from, reassigned_to, reassigned_data, remarks, assigned_by, " + \
        " assigned_on ) values (%s, %s, %s, %s, %s, %s, %s)"

    # Notify  reassign message to new and old techno manager

    name_rows = db.call_proc("sp_empname_by_id", [user_from])
    uname_from = name_rows[0]["empname"]

    save_client = []
    for d in data :
        if d.client_id not in save_client :
            # new techno manager update.
            q = "UPDATE tbl_user_clients SET user_id = %s, " + \
                " assigned_by = %s, assigned_on = %s " + \
                " WHERE client_id = %s and user_id = %s"
            db.execute(q, [d.reassign_to, session_user, get_date_time(), d.client_id, user_from])
            save_client.append(d.client_id)

            # domain manager under client which is not mapped with new techno manager
            qs = "SELECT distinct t1.user_id, t1.domain_id, t2.country_id FROM tbl_user_units as t1 " + \
                "INNER JOIN tbl_legal_entities as t2 " + \
                "ON t1.legal_entity_id = t2.legal_entity_id " + \
                "INNER JOIN tbl_user_mapping as t3 " + \
                " ON t1.user_id = t3.child_user_id and t1.domain_id = t3.domain_id and t3.parent_user_id != %s " + \
                "WHERE t1.user_category_id = 7 and t1.client_id = %s"

            rows = db.select_all(qs, [d.reassign_to, d.client_id])
            # map domain manager to new techno manager
            for r in rows:
                q = "INSERT INTO tbl_user_mapping(user_category_id, country_id, domain_id, parent_user_id, child_user_id, created_by, created_on)" + \
                    "values (%s, %s, %s, %s, %s, %s, %s)"
                db.execute(q, [
                    7, r["country_id"], r["domain_id"], d.reassign_to, r["user_id"],
                    session_user, get_date_time()
                ])

            # reassign history record for techno manager
            db.execute(reassign_history, [
                5, user_from, d.reassign_to, d.client_id, remarks, session_user, get_date_time()
            ])

            # client group reassign message
            gp_name_rows = db.call_proc("sp_groupname_by_id", [d.client_id])
            gp_name = gp_name_rows[0]["group_name"]
            name_rows = db.call_proc("sp_empname_by_id", [d.reassign_to])
            uname_to = name_rows[0]["empname"]

            text = "Client group  %s has been reassigned to techno manager: %s from %s " % (gp_name, uname_to, uname_from)
            db.save_toast_messages(5, "Reassign User Account", text, None, [d.reassign_to, user_from], session_user)

        # techno executive update
        q1 = "UPDATE tbl_user_legalentity SET user_id = %s, " + \
            " assigned_by = %s, assigned_on = %s " + \
            " WHERE client_id = %s and legal_entity_id = %s"

        db.execute(q1, [d.techno_executive, session_user, get_date_time(), d.client_id, d.entity_id])

        # reassign history record for techno executive
        db.execute(reassign_history, [
            6, d.old_techno_executive, d.techno_executive, d.entity_id, remarks, session_user, get_date_time()
        ])

        # Legal entity reassign message
        old_te_rows = db.call_proc("sp_empname_by_id", [d.old_techno_executive])
        old_te = old_te_rows[0]["empname"]

        le_name_rows = db.call_proc("sp_legalentityname_by_id", [d.entity_id])
        le_name = le_name_rows[0]["legal_entity_name"]
        new_te_rows = db.call_proc("sp_empname_by_id", [d.techno_executive])
        new_te = new_te_rows[0]["empname"]

        text = "Legal entity  %s has been reassigned to techno executive: %s from %s " % (le_name, new_te, old_te)
        db.save_toast_messages(6, "Reassign User Account", text, None, [d.old_techno_executive, d.techno_executive], session_user)

        db.save_activity(session_user, frmReassignUserAccount, text)

    return True

def save_reassign_techno_executive(db, user_from, user_to, data, remarks, session_user):
    reassign_history = "INSERT INTO tbl_user_account_reassign_history (user_category_id, " + \
        "reassigned_from, reassigned_to, reassigned_data, remarks, assigned_by, " + \
        " assigned_on ) values (%s, %s, %s, %s, %s, %s, %s)"

    old_te_rows = db.call_proc("sp_empname_by_id", [user_from])
    old_te = old_te_rows[0]["empname"]

    new_te_rows = db.call_proc("sp_empname_by_id", [user_to])
    new_te = new_te_rows[0]["empname"]

    for d in data :
        q1 = " UPDATE tbl_user_legalentity SET user_id = %s, assigned_by = %s, " + \
            " assigned_on = %s where client_id = %s and legal_entity_id = %s"
        db.execute(q1, [user_to, session_user, get_date_time(), d.client_id, d.entity_id])

        db.execute(reassign_history, [
            6, user_from, user_to, d.entity_id, remarks,
            session_user, get_date_time()
        ])
        # Legal entity reassign message

        le_name_rows = db.call_proc("sp_legalentityname_by_id", [d.entity_id])
        le_name = le_name_rows[0]["legal_entity_name"]

        text = "Legal entity  %s has been reassigned to techno executive: %s from %s " % (le_name, new_te, old_te)
        db.save_toast_messages(6, "Reassign User Account", text, None, [user_to, user_from], session_user)
        db.save_activity(session_user, frmReassignUserAccount, text)

    return True

def save_reassign_domain_manager(db, user_from, user_to, domain_id, data, remarks, session_user):
    reassign_history = "INSERT INTO tbl_user_account_reassign_history (user_category_id, " + \
        "reassigned_from, reassigned_to, reassigned_data, domain_id, remarks, assigned_by, " + \
        " assigned_on ) values (%s, %s, %s, %s, %s, %s, %s, %s)"

    new_dm_rows = db.call_proc("sp_empname_by_id", [user_to])
    new_dm = new_dm_rows[0]["empname"]
    old_dm_rows = db.call_proc("sp_empname_by_id", [user_from])
    old_dm = old_dm_rows[0]["empname"]

    for d in data :
        # updating domain manager for units
        q = " UPDATE tbl_user_units set user_id = %s, assigned_by = %s, assigned_on = %s " + \
            " WHERE domain_id = %s and unit_id = %s and user_category_id = 7"
        db.execute(q, [user_to, session_user, get_date_time(), domain_id, d.unit_id])

        db.execute(reassign_history, [
            7, user_from, user_to, d.unit_id, domain_id, remarks, session_user, get_date_time()
        ])

        u_name_rows = db.call_proc("sp_unitname_by_id", [d.unit_id])
        text = "Unit %s has been reassigned to domain manager: %s from %s " % (u_name_rows[0]["unit_name"], new_dm, old_dm)
        db.save_toast_messages(7, "Reassign User Account", text, None, [user_to, user_from], session_user)
        db.save_activity(session_user, frmReassignUserAccount, text)

        # updating domain executive for units
        q = " UPDATE tbl_user_units set user_id = %s, assigned_by = %s, assigned_on = %s " + \
            " WHERE domain_id = %s and unit_id = %s and user_category_id = 8"
        db.execute(q, [d.domain_executive, session_user, get_date_time(), domain_id, d.unit_id])

        db.execute(reassign_history, [
            8, d.old_domain_executive, d.domain_executive, d.unit_id, domain_id, remarks, session_user, get_date_time()
        ])

        new_de_rows = db.call_proc("sp_empname_by_id", [d.domain_executive])
        new_de = new_dm_rows[0]["empname"]
        old_de_rows = db.call_proc("sp_empname_by_id", [d.old_domain_executive])
        old_de = old_dm_rows[0]["empname"]
        text = "Unit %s has been reassigned to domain executive: %s from %s " % (u_name_rows[0]["unit_name"], new_de, old_de)
        db.save_toast_messages(7, "Reassign User Account", text, None, [d.domain_executive, d.old_domain_executive], session_user)
        db.save_activity(session_user, frmReassignUserAccount, text)

    return True

def save_reassign_domain_executive(db, user_from, user_to, domain_id, unit_ids, remarks, session_user):
    reassign_history = "INSERT INTO tbl_user_account_reassign_history (user_category_id, " + \
        "reassigned_from, reassigned_to, reassigned_data, domain_id, remarks, assigned_by, " + \
        " assigned_on ) values (%s, %s, %s, %s, %s, %s, %s, %s)"

    old_de_rows = db.call_proc("sp_empname_by_id", [user_from])
    old_de = old_de_rows[0]["empname"]

    new_de_rows = db.call_proc("sp_empname_by_id", [user_to])
    new_de = new_de_rows[0]["empname"]

    u_name = ''
    for unit_id in unit_ids :
        q = " UPDATE tbl_user_units set user_id = %s, assigned_by = %s, assigned_on = %s " + \
            " WHERE domain_id = %s and unit_id = %s and user_category_id = 8"
        db.execute(q, [user_to, session_user, get_date_time(), domain_id, unit_id])

        db.execute(reassign_history, [
            8, user_from, user_to, unit_id, domain_id, remarks, session_user, get_date_time()
        ])

        u_name_rows = db.call_proc("sp_unitname_by_id", [unit_id])
        u_name = u_name + u_name_rows[0]["unit_name"]
        u_names = [str(i) for i in u_name.split(',') if i.strip()!= '']

    text = "Client unit(s)  %s has been reassigned to domain executive: %s from %s " % (str(u_names), new_de, old_de)
    db.save_toast_messages(8, "Reassign User Account", text, None, [user_to, user_from], session_user)
    db.save_activity(session_user, frmReassignUserAccount, text)
    return True

def save_user_replacement(db, user_type, user_from, user_to, remarks, session_user):
    print [user_type, user_from, user_to, remarks, session_user]
    db.call_update_proc("sp_tbl_users_replacement", [
        user_type, user_from, user_to, remarks, session_user
    ])

    rows = db.call_proc("sp_empname_by_id", (user_from, ))
    old_user = rows[0]["empname"]

    rows1 = db.call_proc("sp_empname_by_id", (user_to, ))
    new_user = rows1[0]["empname"]

    admin_users_id = []
    res = db.call_proc("sp_users_under_user_category", (1,))
    for user in res:
        admin_users_id.append(user["user_id"])

    text = "User %s has been replaced by %s" % (old_user, new_user)
    db.save_toast_messages(user_type, "Reassign User Account", text, None, [user_to, user_from], session_user)
    db.save_activity(session_user, frmReassignUserAccount, text)

    if len(admin_users_id) > 0:
        db.save_toast_messages(1, "Reassign User Account", text, None, admin_users_id, session_user)

    return True

def check_user_replacement(db, request, session_user):
    user_type = request.user_type
    user_from = request.user_from

    rows = db.call_proc("sp_check_user_replacement", [user_type, user_from], 1)
    if rows[0].get('cnt') > 0 :
        return True
    else :
        return False
