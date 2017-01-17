import threading
from server.emailcontroller import EmailHandler
from server import logger
from clientprotocol import (clientcore, general)
from server.common import (
    datetime_to_string, get_date_time,
    string_to_datetime, generate_and_return_password, datetime_to_string_time
)
from clientprotocol import clientmasters

from server.clientdatabase.tables import *
from server.clientdatabase.general import (
    is_primary_admin, is_admin, get_user_unit_ids,
    get_users, get_users_by_id, get_user_countries,
    get_user_domains
)
from server.clientdatabase.savetoknowledge import *
from server.exceptionmessage import client_process_error

email = EmailHandler()
__all__ = [
    "get_service_provider_details_list",
    "is_duplicate_service_provider",
    "save_service_provider",
    "update_service_provider",
    "is_service_provider_in_contract",
    "is_user_exists_under_service_provider",
    "update_service_provider_status",
    "get_forms",
    "get_user_category",
    "is_duplicate_user_privilege",
    "get_user_privilege_details_list",
    "get_user_privileges",
    "save_user_privilege",
    "update_user_privilege",
    "is_user_exists_under_user_group",
    "update_user_privilege_status",
    "get_user_details",
    "get_service_providers",
    "get_no_of_remaining_licence",
    "is_duplicate_user_email",
    "is_duplicate_employee_code",
    "save_user",
    "update_user",
    "update_user_status",
    "update_admin_status",
    "get_units_closure_for_user",
    "close_unit",
    "get_audit_trails",
    "is_duplicate_employee_name",
    "get_unit_closure_legal_entities",
    "get_unit_closure_units_list",
    "save_unit_closure_data",
    "is_invalid_id"
]

############################################################################
# To get the details of all service providers
# Parameter(s) - object of database
# Return Type - returns list of object of ServiceProviderDetails
############################################################################
def get_service_provider_details_list(db):
    columns = [
        "service_provider_id", "service_provider_name", "short_name", "contract_from",
        "contract_to", "contact_person", "contact_no", "email_id", "mobile_no",
        "address", "is_active", "is_blocked", "remarks",
        "ifnull(DATEDIFF(CURRENT_DATE(), blocked_on),0) AS unblock_days"
    ]
    condition = condition_val = None
    order = " ORDER BY service_provider_name"
    rows = db.get_data(
        tblServiceProviders, columns, condition, condition_val, order
    )
    print rows
    return return_service_provider_details(rows)


############################################################################
# To Structure the service provider data fetched from database
# Parameter(s) - service provider details fetched from database in tuple of
#                tuples format
# Return Type - List of ServiceProviderDetails object
############################################################################
def return_service_provider_details(service_providers):
    results = []
    for service_provider in service_providers:
        service_provider_obj = clientcore.ServiceProviderDetails(
            service_provider["service_provider_id"],
            service_provider["service_provider_name"],
            service_provider["short_name"],
            datetime_to_string(service_provider["contract_from"]),
            datetime_to_string(service_provider["contract_to"]),
            service_provider["contact_person"],
            service_provider["contact_no"],
            service_provider["email_id"],
            service_provider["mobile_no"],
            service_provider["address"],
            bool(service_provider["is_active"]),
            bool(service_provider["is_blocked"]),            
            service_provider["unblock_days"],
            service_provider["remarks"])

        results.append(service_provider_obj)
    print results
    return results

############################################################################
# To Check whether the service provider name already exists
# Parameter(s) - Object of database, Service provider Id,
#                Service provider name
# Return Type - Boolean
#             - Returns False if data not exists
#             - Returns True if data exists
############################################################################
def is_duplicate_service_provider(
    db, service_provider_id, service_provider_name
):
    condition = "service_provider_name = %s "
    condition_val = [service_provider_name]
    if service_provider_id is not None:
        condition += " AND service_provider_id != %s"
        condition_val.append(service_provider_id)
    res = db.is_already_exists(tblServiceProviders, condition, condition_val)
    return res


############################################################################
# To saves service provider and saves the activity
# Parameter(s) - Object of database, Object of SaveServiceProvider
# Return Type - int / RuntimeError
#             - Returns service provider id on success
#             - Returns RuntimeError on Failure
############################################################################
def save_service_provider(db, service_provider, session_user):
    current_time_stamp = get_date_time()
    contract_from = string_to_datetime(service_provider.contract_from)
    contract_to = string_to_datetime(service_provider.contract_to)
    columns = [
        "service_provider_name", "short_name", "contract_from", "contract_to",
        "contact_person", "contact_no", "mobile_no", "email_id", "address",
        "created_on", "created_by", "updated_on", "updated_by"        
    ]
    values = [
        service_provider.service_provider_name, service_provider.short_name,
        contract_from, contract_to, service_provider.contact_person,
        service_provider.contact_no, service_provider.mobile_no,
        service_provider.email_id, service_provider.address,
        current_time_stamp, session_user, current_time_stamp, session_user
    ]
    service_provider_id = db.insert(tblServiceProviders, columns, values)
    if service_provider_id is False:
        raise client_process_error("E001")

    action = "Created Service Provider \"%s\"" % (
        service_provider.service_provider_name
    )
    # db.save_activity(session_user, 2, action)
    return service_provider_id


############################################################################
# To get Service provider contract status
# Parameter(s) - Object of database, Service provider id
# Return Type - Boolean
#             - Returns True if service provider is in contract
#             - Returns False if contract of service provider expired
############################################################################
def get_contract_status(
    db, service_provider_id
):
    column = ["count(service_provider_id) as services"]
    condition = "now() between contract_from and contract_to " + \
        " AND service_provider_id = %s "
    condition_val = [service_provider_id]
    rows = db.get_data(tblServiceProviders, column, condition, condition_val)
    if int(rows[0]["services"]) > 0:
        contract_status = True
    else:
        contract_status = False
    return contract_status


############################################################################
# To Update service provider and save update activity
# Parameter(s) - Object of database, Object of UpdateServiceProvider and
#                session user
# Return Type - Boolean
#             - Returns True on Successful update
#             - Returns Runtime Error on Update failure
############################################################################
def update_service_provider(db, service_provider, session_user):
    contract_status_before_update = get_contract_status(
        db, service_provider.service_provider_id
    )
    current_time_stamp = get_date_time()
    contract_from = string_to_datetime(service_provider.contract_from)
    contract_to = string_to_datetime(service_provider.contract_to)
    columns_list = [
        "service_provider_id", "service_provider_name", "short_name", "contract_from", "contract_to",
        "contact_person", "contact_no", "mobile_no", "email_id", "address",
        "updated_on", "updated_by"
    ]    
    values_list = [
        service_provider.service_provider_id, service_provider.service_provider_name, service_provider.short_name,
        contract_from, contract_to, service_provider.contact_person,
        service_provider.contact_no, service_provider.mobile_no,
        service_provider.email_id, service_provider.address,
        current_time_stamp, session_user
    ]
    condition = "service_provider_id= %s"
    values_list.append(service_provider.service_provider_id)
    result = db.update(
        tblServiceProviders, columns_list, values_list, condition
    )
    contract_status_after_update = get_contract_status(
        db, service_provider.service_provider_id
    )
    if result is False:
        raise client_process_error("E002")

    if(
        (contract_status_before_update is False) and
        (contract_status_after_update is True)
    ):
        update_service_provider_status(
            db, service_provider.service_provider_id,
            1, session_user
        )
    elif(
        (contract_status_before_update is True) and
        (contract_status_after_update is False)
    ):
        update_service_provider_status(
            db, service_provider.service_provider_id,
            0, session_user
        )

    action = "Updated Service Provider \"%s\"" % (
        service_provider.service_provider_name
    )
    # db.save_activity(session_user, 2, action)
    return result


############################################################################
# To check whether a service provider is in contract or not
# Parameter(s) - Object of database, Service provider id
# Return Type - Boolean
#             - Returns True if service provider is in contract
#             - Returns False if contract of service provider expired
############################################################################
def is_service_provider_in_contract(db, service_provider_id):
    column = ["count(service_provider_id) as services"]
    condition = " now() between DATE_ADD(contract_from, INTERVAL 1 DAY) " + \
        " and DATE_ADD(contract_to, INTERVAL 1 DAY) " + \
        " and service_provider_id = %s "
    condition_val = [service_provider_id]
    rows = db.get_data(tblServiceProviders, column, condition, condition_val)
    if int(rows[0]["services"]) > 0:
        return True
    else:
        return False


##############################################################################
# To check whether users exists under a service provider
# Parameter(s) - Object of database, Service provider id
# Return Type - Boolean
#             - Returns True if users exists under given service provider
#             - Returns False if users not exists under given servie provider
##############################################################################
def is_user_exists_under_service_provider(db, service_provider_id):
    columns = ["count(user_id) as users"]
    condition = "service_provider_id = %s "
    rows = db.get_data(
        tblUsers, columns, condition, [service_provider_id]
    )
    if len(rows) > 0:
        if int(rows[0]["users"]) > 0:
            return True
        else:
            return False
    else:
        return False


##############################################################################
# To Activate or Inactivate service provider
# Parameter(s) - Object of database, Service provider id, active status and
#                session user
# Return Type - Boolean
#             - Returns True on successfull updation of status
#             - Returns RuntimeError on failure of updation status
##############################################################################
def update_service_provider_status(
    db, service_provider_id,  is_active, session_user
):
    columns = ["is_active", "updated_on", "updated_by"]
    values = [is_active, get_date_time(), session_user, service_provider_id]
    condition = "service_provider_id= %s "
    result = db.update(tblServiceProviders, columns, values, condition)
    if result is False:
        raise client_process_error("E003")

    action_column = "service_provider_name"
    rows = db.get_data(
        tblServiceProviders, action_column, condition, [service_provider_id]
    )
    service_provider_name = rows[0]["service_provider_name"]
    action = None
    if is_active == 1:
        action = "Activated Service Provider \"%s\"" % service_provider_name
    else:
        action = "Deactivated Service Provider \"%s\"" % service_provider_name
    db.save_activity(session_user, 2, action)

    return result

##############################################################################
# To Get list of all forms
# Parameter(s) - Object of database
# Return Type - Tuple of form detail tuples
##############################################################################
def get_forms(db, cat_id):
    q = "SELECT  t1.form_id, t1.form_type_id, t1.form_name, t1.form_url, " + \
        " t1.form_order, t2.form_type, t1.parent_menu FROM tbl_forms as t1 " + \
        " INNER JOIN  tbl_form_type as t2 ON t2.form_type_id = t1.form_type_id" + \
        " INNER JOIN tbl_form_category as t3 ON t1.form_id = t3.form_id " + \
        " WHERE t3.user_category_id = %s"
    row = db.select_all(q, [cat_id])
    return row

##############################################################################
# To Get list of all Menus
# Parameter(s) - Object of database
# Return Type - Tuple of form detail tuples
##############################################################################
def get_user_category(db):
    q = "SELECT user_category_id, user_category_name FROM tbl_user_category"
    row = db.select_all(q, None)
    return row


##############################################################################
# To check whether the user privilege already exists or not
# Parameter(s) - Object of database, user privilege id, user privilege name
# Return Type - Boolean
#             - Returns True if an userprivilege with same name already exists
#             - Returns False if a duplicate doen't exists
##############################################################################
def is_duplicate_user_privilege(
    db, user_category_id, user_privilege_name
):
    condition = "user_group_name = %s "
    condition_val = [user_privilege_name]
    if user_category_id is not None:
        condition += " AND user_category_id != %s "
        condition_val.append(user_category_id)
    return db.is_already_exists(tblUserGroups, condition, condition_val)


##############################################################################
# To Get All user privilege details
# Parameter(s) - Object of database
# Return Type - Tuple of user privilege detail tuples
##############################################################################
def get_user_privilege_details_list(db):
    q = "SELECT t1.user_group_id, t1.user_category_id, " + \
        " group_concat(t3.form_id) form_ids, t1.user_group_name, " + \
        " t2.user_category_name, t1.is_active " + \
        " FROM tbl_user_groups as t1 " + \
        " INNER JOIN tbl_user_category AS t2 ON t2.user_category_id = t1.user_category_id " + \
        " INNER JOIN tbl_user_group_forms AS t3 ON t3.user_group_id = t1.user_group_id" + \
        " group by t1.user_group_id"

    # q = "SELECT t1.user_group_id, t1.user_category_id, t1.user_group_name, " + \
    #    " t2.user_category_name, t1.is_active FROM tbl_user_groups as t1 " + \
    #    " INNER JOIN tbl_user_category AS t2 ON t2.user_category_id = t1.user_category_id"
    groups = db.select_all(q, None)

    # columns = ["user_group_id", "user_category_id", "user_group_name", "user_category_name", "is_active"]
    # groups = db.get_data(
    #     "tbl_user_groups", columns, "1 ORDER BY user_group_name"
    # )

    columns = ["user_group_id", "form_id"]
    group_forms = db.get_data(
        "tbl_user_group_forms", columns, "1 ORDER BY user_group_id"
    )
    #print groups, group_forms
    # return groups, group_forms
    return return_user_privilage_list(groups, group_forms)



def return_user_privilage_list(groups, group_forms):
    user_group_list = []
    for row in groups:
        user_group_id = int(row["user_group_id"])
        user_group_name = row["user_group_name"]
        user_category_id = row["user_category_id"]
        user_category_name = row["user_category_name"]
        category_form_ids = row["form_ids"]
        is_active = bool(row["is_active"])
        user_group_list.append(
            clientcore.ClientUserGroup(
                user_group_id, user_group_name, user_category_id, user_category_name, [int(x) for x in category_form_ids.split(",")],  is_active
            )
        )
    return user_group_list


##############################################################################
# To Get id, name and status of user privileges
# Parameter(s) - Object of database
# Return Type - List of object of UserGroup
##############################################################################
def get_user_privileges(db):
    columns = ["user_group_id", "user_group_name", "is_active"]
    rows = db.get_data(
        tblUserGroups, columns, "1 ORDER BY user_group_name"
    )
    return return_user_privileges(rows)


##############################################################################
# To convert tuple of user privileges to List of UserGroup Objects
# Parameter(s) - Tuple of user privilege tuples
# Return Type - List of object of UserGroup
##############################################################################
def return_user_privileges(user_privileges):
    results = []
    for user_privilege in user_privileges:
        results.append(clientcore.UserGroup(
            user_privilege["user_group_id"],
            user_privilege["user_group_name"],
            bool(user_privilege["is_active"])
        ))
    return results


##############################################################################
# To Save user Privilege
# Parameter(s) - Object of database, Object of User Privilege and session user
# Return Type - Boolean
#             - Returns True on Saving the user privilege successfully
#             - Returns RuntimeError on Save failure
##############################################################################
def save_user_privilege(
    db, user_privilege, session_user
):
    columns = [
        "user_category_id", "user_group_name", "is_active",
        "created_on", "created_by", "updated_on", "updated_by"
    ]
    values_list = [
        user_privilege.user_category_id,
        user_privilege.user_group_name, 1, get_date_time(),
        session_user, get_date_time(), session_user
    ]
    result = db.insert(tblUserGroups, columns, values_list)
    if result is False:
        raise client_process_error("E004")
    if result:
        for x in user_privilege.form_ids:
            columns1 = ["user_group_id", "form_id"]
            values1 = [result, x]
            db.insert(tblUserGroupForms, columns1, values1)

    action = "Created User Group \"%s\"" % user_privilege.user_group_name
    db.save_activity(session_user, 3, action)
    return result


##############################################################################
# To Update user Privilege
# Parameter(s) - Object of database, Object of User Privilege and session user
# Return Type - Boolean
#             - Returns True on successful updation
#             - Returns RuntimeError on updation failure
##############################################################################
def update_user_privilege(db, user_privilege, session_user):
    columns = ["user_category_id", "user_group_name", "updated_on", "updated_by"]
    values = [
        user_privilege.user_category_id,
        user_privilege.user_group_name,
        get_date_time(), session_user, user_privilege.user_group_id
    ]
    condition = "user_group_id=%s"
    result = db.update(tblUserGroups, columns, values, condition)
    if result is False:
        raise client_process_error("E005")
    if result:
        condition2 = "user_group_id=%s" % user_privilege.user_group_id
        db.delete(tblUserGroupForms, condition2, user_privilege.user_group_id)
        #db.execute("DELETE FROM ", condition_val)
        for x in user_privilege.form_ids:
            columns1 = ["user_group_id", "form_id"]
            values1 = [user_privilege.user_group_id, x]
            db.insert(tblUserGroupForms, columns1, values1)
    action = "Updated User Group \"%s\"" % user_privilege.user_group_name
    db.save_activity(session_user, 3, action)
    return result

##############################################################################
# To check whether users exists under a user group
# Parameter(s) - Object of database, User group id
# Return Type - Boolean
#             - Returns True if users exists under given user group
#             - Returns False if users not exists under given user group
##############################################################################
def is_user_exists_under_user_group(db, user_group_id):
    columns = "count(*) as users"
    condition = "user_group_id = %s and is_active = 1"
    condition_val = [user_group_id]
    rows = db.get_data(
        tblUsers, columns, condition, condition_val
    )
    if rows[0]["users"] > 0:
        return True
    else:
        return False


##############################################################################
# To Activate or Inactivate user privilege
# Parameter(s) - Object of database, User group id, active status and
#                session user
# Return Type - Boolean
#             - Returns True on successfull updation of status
#             - Returns RuntimeError on failure of updation status
##############################################################################
def update_user_privilege_status(
    db, user_group_id, is_active, session_user
):
    is_active = 0 if is_active is not True else 1
    columns = ["is_active", "updated_by", "updated_on"]
    values = [is_active, session_user, get_date_time(), user_group_id]
    condition = "user_group_id=%s"
    result = db.update(tblUserGroups, columns, values, condition)
    if result is False:
        raise client_process_error("E006")

    action_column = "user_group_name"
    rows = db.get_data(
        tblUserGroups, action_column, condition, [user_group_id]
    )
    user_group_name = rows[0]["user_group_name"]
    action = None
    if is_active == 0:
        action = "Deactivated user group \"%s\"" % user_group_name
    else:
        action = "Activated user group \"%s\"" % user_group_name
    db.save_activity(session_user, 3, action)
    return result


############################################################################
# To get the details of all users
# Parameter(s) - object of database
# Return Type - returns list of object of ClientUser
############################################################################
def get_user_details(db):
    user_country_columns = ["user_id", "country_id"]
    countries = db.get_data(
        tblUserCountries, user_country_columns, "1"
    )
    user_country_mapping = {}
    for country in countries:
        user_id = int(country["user_id"])
        if user_id not in user_country_mapping:
            user_country_mapping[user_id] = []
        user_country_mapping[user_id].append(
            country["country_id"]
        )
    user_domain_columns = ["user_id", "domain_id"]
    domains = db.get_data(
        tblUserDomains, user_domain_columns, "1"
    )
    user_domain_mapping = {}
    for domain in domains:
        user_id = int(domain["user_id"])
        if user_id not in user_domain_mapping:
            user_domain_mapping[user_id] = []
        user_domain_mapping[user_id].append(
            domain["domain_id"]
        )

    user_unit_columns = ["user_id", "unit_id"]
    units = db.get_data(
        tblUserUnits, user_unit_columns, "1"
    )
    user_unit_mapping = {}
    for unit in units:
        user_id = int(unit["user_id"])
        if user_id not in user_unit_mapping:
            user_unit_mapping[user_id] = []
        user_unit_mapping[user_id].append(
            unit["unit_id"]
        )

    columns = [
        "user_id", "email_id", "user_group_id", "employee_name",
        "employee_code", "contact_no", "seating_unit_id", "user_level",
        "is_admin", "is_service_provider", "service_provider_id",
        "is_active", "is_primary_admin"
    ]
    condition = "1 ORDER BY employee_name"
    rows = db.get_data(
        tblUsers + " tu", columns, condition
    )
    return return_user_details(
        db, rows, user_country_mapping,
        user_domain_mapping, user_unit_mapping
    )


############################################################################
# To convert the data from tuple type to Object of ClientUser
# Parameter(s) - object of database, Tuple of user detail tuples,
#                Dict (key: user id, value : country id),
#                Dict (key : user id, value : domain id),
#                Dict (key : user id, value : unit id)
# Return Type - returns list of object of ClientUser
############################################################################
def return_user_details(
    db, users, user_country_mapping,
    user_domain_mapping, user_unit_mapping
):
    results = []
    for user in users:
        user_id = user["user_id"]
        if is_primary_admin(db, user_id) is True:
            user_country_mapping[user_id] = get_user_countries(db, user_id)
            user_domain_mapping[user_id] = get_user_domains(db, user_id)
            user_unit_mapping[user_id] = get_user_unit_ids(db, user_id)
        results.append(
            clientcore.ClientUser(
                user["user_id"], user["email_id"],
                user["user_group_id"], user["employee_name"],
                user["employee_code"], user["contact_no"],
                user["seating_unit_id"], user["user_level"],
                user_country_mapping[user_id],
                user_domain_mapping[user_id],
                user_unit_mapping[user_id],
                bool(user["is_admin"]), bool(user["is_service_provider"]),
                user["service_provider_id"], bool(user["is_active"]),
                bool(user["is_primary_admin"])
            )
        )
    return results


############################################################################
# To get id, name and active status of Service providers
# Parameter(s) - object of database
# Return Type - returns list of object of ServiceProvider
############################################################################
def get_service_providers(db):
    columns = ["service_provider_id", "service_provider_name", "is_active"]
    condition = " now() between DATE_SUB(contract_from, INTERVAL 1 DAY) " + \
        " and DATE_ADD(contract_to, INTERVAL 1 DAY)"
    rows = db.get_data(
        tblServiceProviders, columns, condition
    )
    return return_service_providers(rows)


############################################################################
# To convert the Tuple of service provider tuples into list of object of
# Service providers
# Parameter(s) - Tuple of service provider tuples
# Return Type - returns list of object of ServiceProvider
############################################################################
def return_service_providers(service_providers):
    results = []
    for service_provider in service_providers:
        service_provider_obj = clientcore.ServiceProvider(
            service_provider["service_provider_id"],
            service_provider["service_provider_name"],
            bool(service_provider["is_active"]))
        results.append(service_provider_obj)
    return results


############################################################################
# Returns Remaining number of  licences
# Parameter(s) - Object of database
# Return Type - int
############################################################################
def get_no_of_remaining_licence(db):
    columns = ["count(0) as licence"]
    condition = "1"
    rows = db.get_data(tblUsers, columns, condition)
    no_of_licence_holders = rows[0]["licence"]

    columns = ["no_of_user_licence"]
    rows = db.get_data(tblClientGroups, columns, condition)
    no_of_licence = rows[0]["no_of_user_licence"]

    remaining_licence = int(no_of_licence) - int(no_of_licence_holders)
    return remaining_licence


############################################################################
# To check whether another user exists with the given email id
# Parameter(s) - Object of database, email id, userid
# Return Type - Boolean
#             - Returns True if another user exists with the same email id
#             - Returns False if duplicate email id doesn't exists
############################################################################
def is_duplicate_user_email(db, email_id, user_id=None):
    condition = "email_id = %s "
    condition_val = [email_id]
    if user_id is not None:
        condition += " AND user_id != %s"
        condition_val.append(user_id)
    flag2 = db.is_already_exists(tblUsers, condition, condition_val)
    return flag2


############################################################################
# To check whether another user exists with the given employee code
# Parameter(s) - Object of database, employee code, userid
# Return Type - Boolean
#             - Returns True if duplicate employee code exists
#             - Returns False if duplicate employee code doesn't exists
############################################################################
def is_duplicate_employee_code(db, employee_code, user_id=None):
    condition = "employee_code = %s "
    condition_val = [employee_code]
    if user_id is not None:
        condition += " AND user_id != %s"
        condition_val.append(user_id)
    return db.is_already_exists(tblUsers, condition, condition_val)


############################################################################
# To check whether another user exists with the given employee name
# Parameter(s) - Object of database, employee name, userid
# Return Type - Boolean
#             - Returns True if duplicate employee name exists
#             - Returns False if duplicate employee name doesn't exists
############################################################################
def is_duplicate_employee_name(db, employee_name, user_id=None):
    condition = "employee_name = %s "
    condition_val = [employee_name]
    if user_id is not None:
        condition += " AND user_id != %s"
        condition_val.append(user_id)
    return db.is_already_exists(tblUsers, condition, condition_val)


############################################################################
# To Save User countries
# Parameter(s) - Object of database, country ids, user id
# Return Type - None / RunTimeError
#             - Returns RuntimeError if insertion fails
############################################################################
def save_user_countries(db, country_ids, user_id):
    db.delete(tblUserCountries, "user_id = %s", [user_id])
    country_columns = ["user_id", "country_id"]
    country_values_list = [
        (user_id, c_id) for c_id in country_ids
    ]
    res = db.bulk_insert(
        tblUserCountries, country_columns, country_values_list
    )
    if res is False:
        raise client_process_error("E008")


############################################################################
# To Save User Domains
# Parameter(s) - Object of database, domain ids, user id
# Return Type - None / RunTimeError
#             - Returns RuntimeError if insertion fails
############################################################################
def save_user_domains(db, domain_ids, user_id):
    db.delete(tblUserDomains, "user_id = %s", [user_id])
    domain_columns = ["user_id", "domain_id"]
    domain_values_list = [
        (user_id, int(domain_id)) for domain_id in domain_ids
    ]
    res = db.bulk_insert(tblUserDomains, domain_columns, domain_values_list)
    if res is False:
        raise client_process_error("E009")


############################################################################
# To Save User Units
# Parameter(s) - Object of database, unit ids, user id
# Return Type - None / RunTimeError
#             - Returns RuntimeError if insertion fails
############################################################################
def save_user_units(db, unit_ids, user_id):
    db.delete(tblUserUnits, "user_id = %s", [user_id])
    unit_columns = ["user_id", "unit_id"]
    unit_values_list = [
        (user_id, int(unit_id)) for unit_id in unit_ids
    ]
    res = db.bulk_insert(tblUserUnits, unit_columns, unit_values_list)
    if res is False:
        raise client_process_error("E010")


############################################################################
# To Save User
# Parameter(s) - Object of database, Object of user, session user
# and client id
# Return Type - True / RunTimeError
#             - Returns True on saved Successfully
#             - Returns RuntimeError if Save fails
############################################################################
def save_user(db, user, session_user, client_id):
    current_time_stamp = get_date_time()
    user.is_service_provider = 0 if user.is_service_provider is False else 1
    columns = [
        "user_group_id", "email_id", "password", "employee_name",
        "employee_code", "contact_no", "user_level",
        "is_admin", "is_service_provider", "created_by", "created_on",
        "updated_by", "updated_on"
    ]
    encrypted_password, password = generate_and_return_password()
    values = [
        user.user_group_id, user.email_id,
        encrypted_password, user.employee_name,
        user.employee_code.replace(" ", ""), user.contact_no, user.user_level,
        0, user.is_service_provider, session_user, current_time_stamp,
        session_user, current_time_stamp
    ]
    if user.is_service_provider == 1:
        columns.append("service_provider_id")
        values.append(user.service_provider_id)
    else:
        columns.append("seating_unit_id")
        values.append(user.seating_unit_id)

    user_id = db.insert(tblUsers, columns, values)
    if user_id is False:
        raise client_process_error("E007")

    save_user_countries(db, user.country_ids, user_id)
    save_user_domains(db, user.domain_ids, user_id)
    save_user_units(db, user.unit_ids, user_id)
    # Save user into  knowledge db
    SaveUsers(user, user_id, client_id)
    action = "Created user \"%s - %s\"" % (
        user.employee_code, user.employee_name
    )
    db.save_activity(session_user, 4, action)
    short_name = get_short_name(db)
    notify_user_thread = threading.Thread(
        target=notify_user, args=[
            short_name, user.email_id, password,
            user.employee_name, user.employee_code
        ]
    )
    notify_user_thread.start()
    return True


############################################################################
# To Update User
# Parameter(s) - Object of database, Object of user, session user
# and client id
# Return Type - True / RunTimeError
#             - Returns True on successfull updation
#             - Returns RuntimeError if Updation fails
############################################################################
def update_user(db, user, session_user, client_id):
    user_id = user.user_id
    current_time_stamp = get_date_time()
    user.is_service_provider = 0 if user.is_service_provider is False else 1
    columns = [
        "user_group_id", "employee_name", "employee_code",
        "contact_no", "seating_unit_id", "user_level",
        "is_service_provider", "updated_on", "updated_by"
    ]
    values = [
        user.user_group_id, user.employee_name,
        user.employee_code.replace(" ", ""),
        user.contact_no, user.seating_unit_id, user.user_level,
        user.is_service_provider, current_time_stamp,
        session_user
    ]
    condition = "user_id= %s "

    if user.is_service_provider == 1:
        columns.append("service_provider_id")
        values.append(user.service_provider_id)
    else:
        columns.append("seating_unit_id")
        values.append(user.seating_unit_id)
    values.append(user_id)
    result1 = db.update(tblUsers, columns, values, condition)
    if result1 is False:
        raise client_process_error("E011")

    save_user_countries(db, user.country_ids, user_id)
    save_user_domains(db, user.domain_ids, user_id)
    save_user_units(db, user.unit_ids, user_id)
    UpdateUsers(user, user.user_id, client_id)

    action = "Updated user \"%s - %s\"" % (
        user.employee_code, user.employee_name
    )
    db.save_activity(session_user, 4, action)

    return True


############################################################################
# To Check the active status of user group of given user
# Parameter(s) - Object of database, user id
# Return Type - None / RunTimeError
#             - Returns RuntimeError if user group of the given user is
#             inactive
############################################################################
def check_user_group_active_status(db, user_id):
    q = "select count(ug.user_group_id) from tbl_user_groups ug " + \
        " inner join tbl_users u on  ug.user_group_id = u.user_group_id " + \
        " where u.user_id = %s and ug.is_active = 1 "
    row = db.select_one(q, [user_id])
    if int(row[0]) == 0:
        raise client_process_error("E030")


##############################################################################
# To Activate or Inactivate user and save the activity
# Parameter(s) - Object of database, User id, active status, employee name
#                session user and client id
# Return Type - Boolean
#             - Returns True on successfull updation of status
#             - Returns RuntimeError on failure of updation status
##############################################################################
def update_user_status(
    db, user_id, is_active, emp_name, session_user, client_id
):
    check_user_group_active_status(db, user_id)

    columns = [
        "is_active", "updated_on", "updated_by"
    ]
    is_active = 1 if is_active is not False else 0
    condition = "user_id = %s "
    values = [
        is_active, get_date_time(), session_user, user_id
    ]
    result = db.update(tblUsers, columns, values, condition)
    if result is False:
        raise client_process_error("E012")

    UpdateUserStatus(is_active, user_id, client_id)

    if is_active == 1:
        action = "Activated user %s" % (emp_name)
    else:
        action = "Dectivated user %s" % (emp_name)
    db.save_activity(session_user, 4, action)

    return result


##############################################################################
# To Promote or Demote from Admin status
# Parameter(s) - Object of database, User id, admin status, employee name
#                session user
# Return Type - Boolean
#             - Returns True on successfull updation of admin status
#             - Returns RuntimeError on failure of updation
##############################################################################
def update_admin_status(
    db, user_id, is_admin, employee_name, session_user
):
    columns = ["is_admin", "updated_on", "updated_by"]
    is_admin = 1 if is_admin is not False else 0
    condition = "user_id = %s"
    values = [is_admin, get_date_time(), session_user, user_id]
    result = db.update(tblUsers, columns, values, condition)
    if result is False:
        raise client_process_error("E013")

    UpdateUserStatus(is_admin, user_id, "admin")

    action = None
    if is_admin == 0:
        action = "User %s  was demoted from admin status" % (employee_name)
    else:
        action = "User %s was promoted to admin status" % (employee_name)
    db.save_activity(session_user, 4, action)

    return result


##############################################################################
# To Get List of Units
# Parameter(s) - Object of database, Unit ids
# Return Type - List of Object of Client Unit
##############################################################################
def get_units_closure_for_user(db, unit_ids):
    columns = [
        "unit_id", "unit_code", "unit_name", "address",
        "division_id", "domain_ids", "country_id",
        "legal_entity_id", "business_group_id",
        "is_active", "is_closed"
    ]
    if unit_ids not in [None, ""]:
        condition, condition_val = db.generate_tuple_condition(
            "unit_id", [int(x) for x in unit_ids.split(",")]
        )
        condition_val = [condition_val]
    else:
        condition = "1"
        condition_val = None
    order = " ORDER BY unit_id ASC "
    rows = db.get_data(
        tblUnits, columns, condition, condition_val, order
    )
    return return_units(rows)


##############################################################################
# To Convert tuple of unit tuples into List of object of client unit
# Parameter(s) - Tuple of unit tuples
# Return Type - List of Object of Client Unit
##############################################################################
def return_units(units):
    results = []
    for unit in units:
        division_id = None
        b_group_id = None
        if unit["division_id"] > 0:
            division_id = unit["division_id"]
        if unit["business_group_id"] > 0:
            b_group_id = unit["business_group_id"]
        results.append(
            clientcore.ClientUnit(
                unit["unit_id"], division_id, unit["legal_entity_id"],
                b_group_id, unit["unit_code"],
                unit["unit_name"], unit["address"], bool(unit["is_active"]),
                [int(x) for x in unit["domain_ids"].split(",")],
                unit["country_id"],
                bool(unit["is_closed"])
            )
        )
    return results


##############################################################################
# To Close a Unit
# Parameter(s) - Object of database, Unit id, Unit name, Sesssion User
# Return Type - None / RuntimeError
#             - Returns Runtime Error if close unit process fails
##############################################################################
def close_unit(db, unit_id, unit_name, session_user):
    condition = "unit_id = %s "
    columns = ["is_closed", "is_active"]
    values = [1, 0, unit_id]
    result = db.update(
        tblUnits, columns, values, condition
    )
    if result is False:
        raise client_process_error("E014")
    columns = ["is_active"]
    values = [0, unit_id]
    result = db.update(
        tblAssignedCompliances, columns, values, condition
    )
    if result is False:
        raise client_process_error("E014")

    UnitClose(unit_id)

    action = "Closed Unit %s" % (unit_name)
    db.save_activity(session_user, 5, action)


def get_users_related_to_session_user(
    db, session_user
):
    if (
        not is_primary_admin(db, session_user) and not
        is_admin(db, session_user)
    ):
        query = " SELECT user_id, employee_name, employee_code, is_active " + \
                " FROM tbl_users WHERE user_id in (SELECT DISTINCT user_id" + \
                " FROM tbl_user_units " + \
                " WHERE unit_id in ( " + \
                " SELECT unit_id FROM tbl_user_units " + \
                " WHERE user_id = %s ) )"
        rows = db.select_all(query, [session_user])
        user_ids_list = [
            int(row[0]) for row in rows
        ]
        users = get_users_by_id(
            db, ",".join(str(user_id) for user_id in user_ids_list)
        )
    else:
        users = get_users(db)
    return users


def get_audit_trails(
    db, session_user, from_count, to_count,
    from_date, to_date, user_id, form_id
):
    form_ids = None
    form_column = "form_id"
    form_condition = "form_type_id != 4"
    rows = db.get_data(
        tblForms, form_column, form_condition
    )
    form_ids = [
        int(row["form_id"]) for row in rows
    ]
    forms = return_forms(
        db, ",".join(str(f) for f in form_ids)
    )

    users = get_users_related_to_session_user(db, session_user)

    from_date = string_to_datetime(from_date).date()
    to_date = string_to_datetime(to_date).date()
    where_qry = "1"
    where_qry_val = []
    if from_date is not None and to_date is not None:
        where_qry += " AND  date(created_on) between %s AND %s "
        where_qry_val.extend([from_date, to_date])
    if user_id is not None:
        where_qry += " AND user_id = %s"
        where_qry_val.append(user_id)
    if form_id is not None:
        where_qry += " AND form_id = %s"
        where_qry_val.append(form_id)
    columns = [
        "user_id", "form_id", "action", "created_on"
    ]
    where_qry += " AND action not like %s " + \
        " ORDER BY activity_log_id DESC limit %s, %s "

    action_condition = "%sLog In by%s" % ("%", "%")
    where_qry_val.extend(
        [
            action_condition, from_count, to_count
        ]
    )
    rows = db.get_data(
        tblActivityLog, columns, where_qry, where_qry_val
    )

    c_rows = db.get_data(tblActivityLog, "count(0) as total", where_qry, where_qry_val)
    c_total = 0
    for c in c_rows :
        c_total = c["total"]

    audit_trail_details = []
    for row in rows:
        user_id = row["user_id"]
        form_id = row["form_id"]
        action = row["action"]
        date = datetime_to_string_time(row["created_on"])
        audit_trail_details.append(
            general.AuditTrail(user_id, form_id, action, date)
        )
    return general.GetAuditTrailSuccess(audit_trail_details, users, forms, c_total)


def return_forms(db, form_ids=None):
    columns = "form_id, form_name"
    condition = "form_id != 24"
    condition_val = None
    if form_ids is not None:
        form_condition, form_condition_val = db.generate_tuple_condition(
            "form_id", [int(x) for x in form_ids.split(",")]
        )
        condition_val = [form_condition_val]
        condition += " AND %s " % form_condition
    forms = db.get_data(
        tblForms, columns, condition, condition_val
    )
    results = []
    for form in forms:
        results.append(
            general.AuditTrailForm(form["form_id"], form["form_name"])
        )
    return results


def get_short_name(db):
    columns = "url_short_name"
    rows = db.get_data(
        tblClientGroups, columns, "1"
    )
    return rows[0]["url_short_name"]


def notify_user(
    short_name, email_id, password, employee_name, employee_code
):
    try:
        email.send_user_credentials(
            short_name, email_id, password, employee_name, employee_code
        )
    except Exception, e:
        logger.logClient("error", "clientdatabase.py-notify-user", e)
        print "Error while sending email: %s" % e


############################################################################
# parameters: db object, requests, user id passed - to get legal entity list
############################################################################
def get_unit_closure_legal_entities(db, user_id):
    le_list = []
    columns = "user_category_id, client_id"
    condition = "user_id = %s"
    condition_val = [user_id]
    l_id = None
    recordSet = None
    user_category = db.get_data(tblUsers, columns, condition, condition_val)
    for row in user_category:
        print row["user_category_id"]
        if row["user_category_id"] == 1:
            print "jfhdsjk"
            columns = "legal_entity_id, legal_entity_name"
            condition = "DATEDIFF(contract_to, NOW()) > 0 and is_closed = 0 and client_id = %s"
            condition_val = [row["client_id"]]
            order = " ORDER BY legal_entity_name"
            recordSet = db.get_data(tblLegalEntities, columns, condition, condition_val, order)
        else:
            if row["user_category_id"] == 3:
                columns = "distinct(legal_entity_id)"
                condition = "user_id = %s"
                condition_val = [user_id]
                le_ids = db.get_data(tblUserDomains, columns, condition, condition_val)
                if le_ids is not None:
                    for le_id in le_ids:
                        if l_id is None:
                            l_id = str(le_id["legal_entity_id"])
                        else:

                            l_id = l_id + "," + str(le_id["legal_entity_id"])

                print l_id
                columns = "legal_entity_id, legal_entity_name"
                le_condition, c_val = db.generate_tuple_condition(
                        "legal_entity_id", [int(x) for x in l_id.split(",")]
                    )
                print le_condition
                condition = "DATEDIFF(contract_to, NOW()) > 0 and is_closed = 0 and %s" % le_condition
                condition_val = [c_val]
                order = "ORDER BY legal_entity_name"
                recordSet = db.get_data(tblLegalEntities, columns, condition, condition_val, order)
    print recordSet
    for row in recordSet:
        le_list.append(clientcore.UnitClosureLegalEntity(
            legal_entity_id=row["legal_entity_id"],
            legal_entity_name=row["legal_entity_name"]
            )
        )
    return le_list

############################################################################
# parameters: db object, requests, user id passed - to get units
# list under legal entity id
############################################################################
def get_unit_closure_units_list(db, request):
    le_id = request.legal_entity_id
    result = db.call_proc("sp_unit_closure_units_list_by_le_id", (le_id,))
    units_list = []
    for row in result:
        units_list.append(clientcore.UnitClosure_Units(
            row["unit_id"], row["unit_code"], row["unit_name"], row["address"],
            row["postal_code"], row["legal_entity_id"], row["legal_entity_name"],
            row["business_group_name"], row["division_name"], row["category_name"],
            bool(row["is_active"]), str(row["closed_on"]), row["validity_days"]
            )
        )
    return units_list

def is_invalid_id(db, check_mode, val):
    print "inside valid checking"
    print check_mode

    if check_mode == "unit_id":
        params = [val, ]
        rows = db.call_proc("sp_tbl_units_check_unitId", params)
        for d in rows:
            if(int(d["unit_id_cnt"]) > 0):
                return True
            else:
                return False


def save_unit_closure_data(db, user_id, password, unit_id, remarks, action_mode):
    current_time_stamp = get_date_time()
    print action_mode
    if action_mode == "close":
        print "save"
        result = db.call_update_proc("sp_unit_closure_save", (
            user_id, unit_id, 0, current_time_stamp, remarks
        ))
    elif action_mode == "reactive":
        result = db.call_update_proc("sp_unit_closure_save", (
            user_id, unit_id, 1, current_time_stamp, remarks
        ))

    print result
    return result
