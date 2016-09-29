import threading
from protocol import core
from server.database.tables import *
from server.common import (
    get_date_time,
    generate_and_return_password
)
from server.emailcontroller import EmailHandler as email
from server.exceptionmessage import process_error

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
    "save_validity_date_settings"
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
    result = db.call_proc(procedure, (user_id,))
    return return_domains(result)


###############################################################################
# To convert the data fetched from database into List of object of Domain
# Parameter(s) : Data fetched from database
# Return Type : List of Object of Domain
###############################################################################
def return_domains(data):
    results = []
    for d in data:
        results.append(core.Domain(
            d["domain_id"], d["domain_name"], bool(d["is_active"])
        ))
    return results


###############################################################################
# To save domain
# Parameter(s) : Object of database, Domain name, session user
# Return Type : Returns True on Successfull save otherwise raises process error
###############################################################################
def save_domain(db, domain_name, user_id):
    created_on = get_date_time()
    domain_id = db.call_insert_proc(
        "sp_domains_save", (None, domain_name, user_id, created_on)
    )
    if domain_id is False:
        raise process_error("E024")
    action = "Add Domain - \"%s\"" % domain_name
    db.save_activity(user_id, 2, action)
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
def update_domain(db, domain_id, domain_name, updated_by):
    updated_on = get_date_time()
    oldData = get_domain_by_id(db, domain_id)
    if oldData is None:
        return False
    else:
        domain_id = db.call_update_proc(
            "sp_domains_save", (domain_id, domain_name, updated_by, updated_on)
        )
        if domain_id:
            action = "Edit Domain - \"%s\"" % domain_name
            db.save_activity(updated_by, 2, action)
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
        if result:
            action = "Domain %s status  - %s" % (
                oldData, "deactivated" if is_active == 0 else "activated"
            )
            db.save_activity(updated_by, 1, action)
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


#############################################################################
# To get countries configured under a user
# Parameter(s) : Object of database, user id
# Return Type : List of Object of Countries
#############################################################################
def get_countries_for_user(db, user_id):
    result = db.call_proc("sp_countries_for_user", (user_id,))
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
    if country_id:
        action = "Add Country - \"%s\"" % country_name
        db.save_activity(created_by, 1, action)
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
        if result:
            action = "Edit Country - \"%s\"" % country_name
            db.save_activity(updated_by, 1, action)
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
        if result:
            action = "Country %s status  - %s" % (
                oldData, "deactivated" if is_active == 0 else "activated"
            )
            db.save_activity(updated_by, 1, action)
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
    return db.call_proc("sp_forms_list", None)


###############################################################################
# To get all Form categories
# Parameter(s) : Object of database
# Return Type : Returns data fetched from database (Tuplse)
###############################################################################
def get_form_categories(db):
    return db.call_proc("sp_formcategory_list", None)


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
    return db.call_proc("sp_usergroup_detailed_list", None)


###############################################################################
# To get List of all user groups (only id, name and status)
# Parameter(s) : Object of database
# Return Type : Returns data fetched from database (Tuple)
###############################################################################
def get_user_groups_from_db(db):
    return db.call_proc("sp_usergroup_list", None)


###############################################################################
# To save User group
# Parameter(s) : Object of database, user group name (String),
# form category id (INT), List of form ids (List of integer), session user id
# Return Type : Returns True on Successfull save otherwise raises process error
###############################################################################
def save_user_group(
    db, user_group_name, form_category_id, form_ids, session_user
):
    time_stamp = str(get_date_time())
    ug_id = db.call_insert_proc(
        "sp_usergroup_save",
        (
            None, user_group_name, form_category_id,
            form_ids, session_user, time_stamp
        )
    )
    if ug_id:
        action = "Created User Group \"%s\"" % user_group_name
        db.save_activity(0, 3, action)
        return True
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
    db, user_group_id, user_group_name, form_category_id, form_ids,
    session_user
):
    time_stamp = get_date_time()
    result = db.call_update_proc(
        "sp_usergroup_save",
        (
            user_group_id, user_group_name, form_category_id,
            form_ids, session_user, time_stamp
        )
    )
    if result:
        action = "Updated User Group \"%s\"" % user_group_name
        db.save_activity(0, 3, action)
        return True
    else:
        raise process_error("E031")


###############################################################################
# To update the status of user group
# Parameter(s) : Object of database, user group id, is_active, session user id
# Return Type : True on Successfull update otherwise raises process error
###############################################################################
def update_user_group_status(db, user_group_id, is_active, session_user):
    time_stamp = get_date_time()
    result = db.call_update_proc(
        "sp_usergroup_change_status",
        (
            user_group_id, is_active, session_user,
            time_stamp
        )
    )
    if result is False:
        raise process_error("E032")

    result = db.call_proc("sp_usergroup_by_id", (user_group_id,))
    user_group_name = result[0]["user_group_name"]
    action = "%s User Group \"%s\"" % (
        "Deactivated" if is_active == 0 else "Activated",
        user_group_name
    )
    db.save_activity(0, 3, action)
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
    return db.call_proc("sp_user_detailed_list", None)


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


###############################################################################
# To save User
# Parameter(s) : Object of database, email id, user group id, employee name,
#                employee code, contact number, address, designation,
#               list of country ids, list of domain ids, session user id
# Return Type : Returns True on Successfull save otherwise raises process error
###############################################################################
def save_user(
    db, email_id, user_group_id, employee_name, employee_code, contact_no,
    address, designation, country_ids, domain_ids, session_user
):
    current_time_stamp = get_date_time()
    encrypted_password, password = generate_and_return_password()
    user_id = db.call_insert_proc(
        "sp_users_save", (
            None, email_id, user_group_id, encrypted_password,
            employee_name, employee_code, contact_no, address,
            designation, session_user, current_time_stamp)
    )
    if user_id is False:
        raise process_error("E033")
    save_user_countries(db, country_ids, user_id)
    save_user_domains(db, domain_ids, user_id)
    action = "Created User \"%s - %s\"" % (employee_code, employee_name)
    db.save_activity(0, 4, action)
    notify_user_thread = threading.Thread(
        target=notify_user, args=[
            email_id, password, employee_name, employee_code
        ]
    )
    notify_user_thread.start()
    return True


###############################################################################
# To Send the credentials to the user
# Parameter(s) : email id, password, employee name, employee code
# Return Type : if the email fails raises exception
###############################################################################
def notify_user(
    email_id, password, employee_name, employee_code
):
    try:
        email().send_knowledge_user_credentials(
            email_id, password, employee_name, employee_code
        )
    except Exception, e:
        print "Error while sending email"
        print e


###############################################################################
# To Save Countries configured for the user
# Parameter(s) : Object of database, list of country ids, user id
# Return Type : Returns None on Successfull save otherwise raises process error
###############################################################################
def save_user_countries(
    db, country_ids, user_id
):
    country_columns = ["user_id", "country_id"]
    country_values_list = [
       (user_id, int(country_id)) for country_id in country_ids
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
    db, domain_ids, user_id
):
    domain_columns = ["user_id", "domain_id"]
    domain_values_list = [
        (user_id, int(domain_id)) for domain_id in domain_ids
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
    db, user_id, user_group_id, employee_name, employee_code, contact_no,
    address, designation, country_ids, domain_ids, session_user
):
    current_time_stamp = get_date_time()
    result = db.call_update_proc(
        "sp_users_save", (
            user_id, None, user_group_id, None,
            employee_name, employee_code, contact_no, address,
            designation, session_user, current_time_stamp)
    )
    if result is False:
        raise process_error("E036")
    db.call_update_proc("sp_usercountries_delete", (user_id,))
    db.call_update_proc("sp_userdomains_delete", (user_id,))
    save_user_countries(db, country_ids, user_id)
    save_user_domains(db, domain_ids, user_id)
    action = "Updated User \"%s - %s\"" % (employee_code, employee_name)
    db.save_activity(0, 4, action)
    return True


###############################################################################
# To Check whether the user group of user is active or not
# Parameter(s) : Object of database, user id
# Return Type : If the user group is inactive raises process error
###############################################################################
def check_user_group_active_status(db, user_id):
    row = db.call_proc("sp_user_usergroup_status", (user_id,))
    if int(row[0]) == 0:
        raise process_error("E065")


###############################################################################
# To Update the status of user
# Parameter(s) : Object of database, user id, active status
# Return Type : Returns True on Successfull update, Other wise raises process
#               error
###############################################################################
def update_user_status(db, user_id, is_active):
    check_user_group_active_status(db, user_id)
    result = db.call_update_proc(
        "sp_users_change_status",
        (user_id, is_active, session_user, get_date_time())
    )
    if result is False:
        raise process_error("E039")
    rows = db.call_proc("sp_users_change_status", (user_id, ))
    employee_name = rows[0]["empname"]
    action = ""
    if is_active == 1:
        action = "Activated User \"%s\"" % employee_name
    else:
        action = "Dectivated User \"%s\"" % employee_name
    db.save_activity(0, 4, action)
    return result


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
    result = db.call_proc(
        "sp_domain_mapped_list", None
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
            datum["validity_days_id"],
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
    for datum in data:
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
