import threading
from server.emailcontroller import EmailHandler
from clientprotocol import (clientcore, general)
from server.common import (
    datetime_to_string, get_date_time,
    string_to_datetime, generate_and_return_password, datetime_to_string_time,
    get_current_date, new_uuid, addHours, encrypt
)
from server.emailcontroller import EmailHandler as email
from clientprotocol import clientmasters

from server.clientdatabase.tables import *
from server.clientdatabase.general import (
    is_primary_admin, is_admin, get_user_unit_ids,
    get_users, get_users_by_id, get_user_countries,
    get_user_domains
)
from server.clientdatabase.savetoknowledge import *
from server.exceptionmessage import client_process_error
from server.constants import REGISTRATION_EXPIRY, KNOWLEDGE_URL, CLIENT_URL


# email = EmailHandler()
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
    "verify_password_user_privilege",
    "update_user_privilege_status",
    "get_user_details",
    "get_service_providers",
    "get_no_of_remaining_licence_Viewonly",
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
    "is_already_assigned_units",
    "get_unit_closure_legal_entities",
    "get_unit_closure_units_list",
    "save_unit_closure_data",
    "is_invalid_id",
    "userManagement_GetUserCategory",
    "userManagement_GetUserGroup",
    "userManagement_GetLegalEntity",
    "userManagement_GetBusinessGroup",
    "userManagement_GetDivision",
    "userManagement_GetGroupCategory",
    "userManagement_GetLegalEntity_Domain",
    "userManagement_GetLegalEntity_Units",
    "userManagement_domains_for_Units",
    "userManagement_legalentity_for_User",
    "userManagement_GetServiceProviders",
    "userManagement_list_GetLegalEntities",
    "userManagement_list_GetUsers",
    "save_user_legal_entities",
    "get_service_providers_list",
    "get_service_providers_user_list",
    "get_service_provider_status",
    "get_service_provider_details_report_data",
    "get_audit_users_list",
    "get_audit_forms_list",
    "get_login_users_list",
    "process_login_trace_report",
    "get_user_info",
    "update_profile",
    "block_service_provider",
    "userManagement_EditView_GetUsers",
    "userManagement_EditView_GetLegalEntities",
    "userManagement_EditView_GetDomains",
    "userManagement_EditView_GetUnits",
    "update_licence_viewonly",
    "update_licence",
    "block_user",
    "resend_registration_email",
    "get_user_Category_by_user_id",
    "get_user_legal_entity_by_user_id",
    "userManagement_legalentity_for_BusinessGroup",
    "get_legal_entity_domains_data"
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
        "greatest((30 - ifnull(DATEDIFF(CURRENT_DATE(), blocked_on),0)),0) AS unblock_days"
    ]
    condition = condition_val = None
    order = " ORDER BY service_provider_name"
    resultRows = db.get_data(
        tblServiceProviders, columns, condition, condition_val, order)

    results = []
    for row in resultRows:
        service_provider_id = row["service_provider_id"]
        service_provider_name = row["service_provider_name"]
        short_name = row["short_name"]
        contract_from = datetime_to_string(row["contract_from"])
        contract_to = datetime_to_string(row["contract_to"])
        contact_person = row["contact_person"]
        contact_no = row["contact_no"]
        email_id = row["email_id"]
        mobile_no = row["mobile_no"]
        address = row["address"]
        is_active = bool(row["is_active"])
        is_blocked = bool(row["is_blocked"])
        unblock_days = row["unblock_days"]
        remarks = row["remarks"]
        sp_users = get_user_service_provider_wise(db, service_provider_id)

        results.append(clientcore.ServiceProviderDetails(
                        service_provider_id, service_provider_name, short_name, contract_from,
                        contract_to, contact_person,contact_no, email_id, mobile_no, address, is_active,
                        is_blocked, unblock_days, remarks, sp_users))

    return results
############################################################################
# To Check whether the service provider name already exists
# Parameter(s) - Object of database, Service provider Id,
#                Service provider name
# Return Type - Boolean
#             - Returns False if data not exists
#             - Returns True if data exists
############################################################################
def is_duplicate_service_provider(db, service_provider_id, service_provider_name,
                                  short_name):
    column = ["short_name", "service_provider_name"]
    condition = "short_name = %s AND service_provider_name = %s "
    condition_val = [short_name, service_provider_name]
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
    # Audit Log Entry
    db.save_activity(session_user, 1, action)
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
    db.save_activity(session_user, 1, action)
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
    condition = " now() between DATE_ADD(contract_from, INTERVAL 0 DAY) " + \
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
    columns = ["is_active", "updated_on", "updated_by", "status_changed_on", "status_changed_by"]
    values = [is_active, get_date_time(), session_user, get_date_time(), session_user, service_provider_id]
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
# To Block service provider
# Parameter(s) - Object of database, Service provider id, block status and
#                session user
# Return Type - Boolean
#             - Returns True on successfull block
#             - Returns RuntimeError on failure block
##############################################################################
def block_service_provider(
    db, service_provider_id, remarks, is_blocked, session_user
):
    columns = ["is_blocked", "updated_on", "updated_by", "blocked_on", "blocked_by", "remarks"]
    values = [is_blocked, get_date_time(), session_user, get_date_time(), session_user, remarks, service_provider_id ]
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
    if is_blocked == 1:
        action = "Blocked Service Provider \"%s\"" % service_provider_name
    else:
        action = "Unblocked Service Provider \"%s\"" % service_provider_name
    db.save_activity(session_user, 2, action)

    return result

##############################################################################
# Get list of users for service providers
##############################################################################
def get_user_service_provider_wise(db, service_provider_id):
    if service_provider_id != None:
        q= " select IFNULL(Concat(T01.user_id, '-', GROUP_CONCAT(T02.legal_entity_id)),0) as user_id from tbl_users as T01 " + \
            " inner join tbl_user_legal_entities as T02 ON T01.user_id = T02.user_id " + \
            " where T01.user_category_id = 6 and T01.service_provider_id = %s "
        row = db.select_all(q, [service_provider_id])
        results = []
        for r in row:
            results.append(r["user_id"])
        return results
##############################################################################
# To Disable User
# Parameter(s) - Object of database, Service provider id, block status and
#                session user
# Return Type - Boolean
#             - Returns True on successfull block
#             - Returns RuntimeError on failure block
##############################################################################
def block_user(
    db, user_id, remarks, is_blocked, session_user
):
    columns = ["is_disable", "updated_on", "updated_by", "disabled_on", "remarks"]
    values = [is_blocked, get_date_time(), session_user, get_date_time(), remarks, user_id ]
    condition = "user_id= %s "
    result = db.update(tblUsers, columns, values, condition)
    if result is False:
        raise client_process_error("E003")

    action_column = "employee_name"
    rows = db.get_data(
        tblUsers, action_column, condition, [user_id]
    )
    employee_name = rows[0]["employee_name"]
    action = None
    if is_blocked == 1:
        action = "Disabled User \"%s\"" % employee_name
    else:
        action = "Enabled User \"%s\"" % employee_name
    db.save_activity(session_user, 2, action)

    return result

##############################################################################
# To Disable User
# Parameter(s) - Object of database, Service provider id, block status and
#                session user
# Return Type - Boolean
#             - Returns True on successfull block
#             - Returns RuntimeError on failure block
##############################################################################
def resend_registration_email(
    db, user_id, session_user, client_id
):
    query = "select employee_name, email_id from tbl_users where client_id=%s AND user_id = %s"
    result = db.select_all(query, [client_id, user_id])
    for row in result:
        emp_name = row["employee_name"]
        email_id = row["email_id"]

    short_name = get_short_name(db)
    save_registration_token(db, short_name, user_id, emp_name, email_id)

    return True

##############################################################################
# User Management Add - Category Prerequisite
##############################################################################
def userManagement_GetUserCategory(db, session_category):
    if session_category == 1: #Group Admin
        condition = " WHERE user_category_id NOT IN (1)"
    elif session_category == 3: #Legal Entity Admin
        condition = " WHERE user_category_id NOT IN (1,2,3)"
    elif session_category == 4: #Domain Admin
        condition = " WHERE user_category_id NOT IN (1,2,3,4)"

    q = "SELECT user_category_id, user_category_name From tbl_user_category " + condition
    row = db.select_all(q, None)
    return row

##############################################################################
# User Management Add - User Group Prerequisite
##############################################################################
def userManagement_GetUserGroup(db):
    q = "SELECT user_group_id, user_group_name, user_category_id from tbl_user_groups " + \
        " WHERE is_active = '1'"
    row = db.select_all(q, None)
    return row

##############################################################################
# User Management Add - Business Group Prerequisite
##############################################################################
def userManagement_GetBusinessGroup(db):
    q = "SELECT business_group_id, business_group_name from tbl_business_groups "
    row = db.select_all(q, None)
    return row

##############################################################################
# User Management Add - Legal Entity Prerequisite
##############################################################################
def userManagement_GetLegalEntity(db):
    # q = "SELECT legal_entity_id, business_group_id, legal_entity_name From tbl_legal_entities " + \
    #     " WHERE is_closed ='0' order by legal_entity_name, business_group_id"
    q = " SELECT T01.legal_entity_id, T01.business_group_id, T01.legal_entity_name, " + \
        " T04.user_id AS le_admin, T04.user_category_id From tbl_legal_entities AS T01 " + \
        " LEFT JOIN (SELECT T03.legal_entity_id,T02.user_id, T02.user_category_id " + \
        " FROM tbl_user_legal_entities AS T03 INNER JOIN  tbl_users AS T02 " + \
        " ON T02.user_id = T03.user_id WHERE   T02.user_category_id = 3) as T04 " + \
        " ON T01.legal_entity_id = T04.legal_entity_id WHERE T01.is_closed ='0' " + \
        " order by T01.legal_entity_name, T01.business_group_id "
    row = db.select_all(q, None)
    return row
##############################################################################
# User Management Add - Division Prerequisite
##############################################################################
def userManagement_GetDivision(db):
    q = "SELECT division_id, division_name, legal_entity_id, business_group_id From tbl_divisions " + \
        " order by division_name, legal_entity_id "
    row = db.select_all(q, None)
    return row
##############################################################################
# User Management Add - Category Prerequisite
##############################################################################
def userManagement_GetGroupCategory(db):
    q = "SELECT category_id, category_name, legal_entity_id, "+ \
        " business_group_id, division_id From tbl_categories " + \
        " order by category_name, legal_entity_id "
    row = db.select_all(q, None)
    return row
##############################################################################
# User Management Add - Legal Entity Domains Prerequisite
##############################################################################
def userManagement_GetLegalEntity_Domain(db, session_user, session_category):
    q = "SELECT  Distinct T01.domain_id, T01.legal_entity_id, T02.domain_name " + \
        " From tbl_legal_entity_domains AS T01 INNER JOIN tbl_domains as T02" + \
        " ON T01.domain_id = T02.domain_id WHERE T02.is_active=1 "

    if session_category == 4: #Domain Admin
        condition = " AND T01.domain_id IN (SELECT distinct domain_id From tbl_user_domains where user_id =%s)"
        q = q + condition + " order by domain_name, legal_entity_id "        
        row = db.select_all(q, [session_user])
    else:
        q = q + " order by domain_name, legal_entity_id "
        row = db.select_all(q, None)
    
    return row
##############################################################################
# User Management Add - Units
##############################################################################
def userManagement_GetLegalEntity_Units(db):
    q = "SELECT unit_id, business_group_id, legal_entity_id, division_id, " + \
        " category_id, unit_code, unit_name, address, postal_code " + \
        " From tbl_units where is_closed = '0' "
    row = db.select_all(q, None)
    return row
##############################################################################
# User Management Add - Units
##############################################################################
def userManagement_domains_for_Units(db, unit_id):
    q = "select distinct t1.domain_id from tbl_domains as t1 " + \
        "inner join tbl_units_organizations as t2 on t2.domain_id = t1.domain_id " + \
        "inner join tbl_units as t3 on t3.unit_id = t2.unit_id AND is_closed = 0 AND t3.unit_id = %s "
    row = db.select_all(q, [unit_id])
    results = []
    for r in row:
        results.append(r["domain_id"])
    return results
##############################################################################
# User Management Add - Units
##############################################################################
def userManagement_legalentity_for_User(db, user_id):
    q = "select distinct legal_entity_id from tbl_user_legal_entities where user_id = %s "
    row = db.select_all(q, [user_id])
    results = []
    for r in row:
        results.append(r["legal_entity_id"])
    return results

##############################################################################
# User Management Get Legal Entities
##############################################################################
def userManagement_legalentity_for_BusinessGroup(db, bg_id):
    if bg_id != None:
        q = "select distinct legal_entity_id from tbl_legal_entities where business_group_id = %s "
        row = db.select_all(q, [bg_id])
        results = []
        for r in row:
            results.append(r["legal_entity_id"])
        return results
##############################################################################
# User Management Add - Service Providers
##############################################################################
def userManagement_GetServiceProviders(db):
    q = "SELECT service_provider_id, service_provider_name, short_name " + \
        " From tbl_service_providers where is_active = '1' and is_blocked = '0' " + \
        " and now() between DATE_ADD(contract_from, INTERVAL 0 DAY) " + \
        " and DATE_ADD(contract_to, INTERVAL 1 DAY) "
    row = db.select_all(q, None)
    return row
##############################################################################
# User Management List - Get Legal Entity Details
##############################################################################
def userManagement_list_GetLegalEntities(db):
    le_ids = "%"
    q = " SELECT Distinct T01.legal_entity_id, T01.legal_entity_name, T01.country_id, " + \
        " T02.country_name, T01.business_group_id, T03.business_group_name, " + \
        " T01.contract_from, T01.contract_to, T01.total_licence, T01.used_licence " + \
        " From tbl_legal_entities AS T01 INNER JOIN tbl_countries AS T02 " + \
        " ON T01.country_id = T02.country_id LEFT JOIN tbl_business_groups AS T03 " + \
        " ON T01.business_group_id = T03.business_group_id  " + \
        " INNER JOIN tbl_user_legal_entities AS T04 ON T01.legal_entity_id = T04.legal_entity_id" + \
        " Where T01.legal_entity_id like '%' "
    # " FIND_IN_SET(T01.legal_entity_id, %s) "
    # row = db.select_all(q, [le_ids])
    row = db.select_all(q, None)
    return row
##############################################################################
# User Management List - Get Users
##############################################################################
def userManagement_list_GetUsers(db, session_category):
    if session_category == 1: #Group Admin
        condition = " AND T01.user_category_id like '%' "
    elif session_category == 3: #Legal Entity Admin
        condition = " AND T01.user_category_id NOT IN (1,2,3)"
    elif session_category == 4: #Domain Admin
        condition = " AND T01.user_category_id NOT IN (1,2,3,4)"
    le_ids = "%"
    q = " SELECT T01.user_id, T01.user_category_id, T01.employee_code, T01.employee_name, " + \
        " T02.username, T01.email_id, T01.mobile_no,T03.legal_entity_id, T01.is_active, T01.is_disable, " + \
        " greatest((30 - ifnull(DATEDIFF(CURRENT_DATE(), T01.disabled_on),0)),0) AS unblock_days, " + \
        " (Select CONCAT('Seating Unit: ', unit_code, ' - ' , unit_name , ' - ' , address , ', ' , postal_code) " + \
        " From tbl_units where unit_id = T01.seating_unit_id) as seating_unit " + \
        " FROM tbl_users AS T01 INNER JOIN tbl_user_legal_entities AS T03 " + \
        " ON T01.user_id = T03.user_id LEFT JOIN tbl_user_login_details AS T02 " + \
        " ON T01.user_id = T02.user_id Where T03.legal_entity_id like '%' " + condition
    # row = db.select_all(q, [le_ids])
    row = db.select_all(q, None)
    return row

##############################################################################
# User Management - Edit View Get User Details
##############################################################################
def userManagement_EditView_GetUsers(db, userID):
    q = " SELECT  T01.user_id, T01.user_category_id, T01. seating_unit_id, T01.service_provider_id, " + \
        " T01.user_level, T01.user_group_id, T01.email_id, T01.employee_name, T01.employee_code, " + \
        " T01.contact_no, T01.mobile_no, T01.address, T01.is_service_provider, T01.is_active, " + \
        " T01.is_disable FROM tbl_users AS T01 Where T01.user_id = %s"

    row = db.select_all(q, [userID])
    return row

##############################################################################
# User Management - Edit View Get Users - Legal Entities
##############################################################################
def userManagement_EditView_GetLegalEntities(db, userID):
    q = "SELECT T01.user_id, T01.legal_entity_id, T02.business_group_id " + \
        " FROM tbl_user_legal_entities As T01 INNER JOIN tbl_legal_entities As T02 " + \
        " ON T01.legal_entity_id = T02.legal_entity_id WHERE user_id = %s"

    row = db.select_all(q, [userID])
    return row

##############################################################################
# User Management - Edit View Get Users - Domains
##############################################################################
def userManagement_EditView_GetDomains(db, userID):
    q = " SELECT user_id, legal_entity_id, domain_id from tbl_user_domains where user_id = %s "

    row = db.select_all(q, [userID])
    return row

##############################################################################
# User Management - Edit View Get Users - Units
##############################################################################
def userManagement_EditView_GetUnits(db, userID):
    q = " SELECT T01.user_id, T01.legal_entity_id, T01.unit_id, T02.business_group_id, " + \
        " T02.division_id, T02.category_id FROM tbl_user_units As T01 " + \
        " INNER JOIN tbl_units AS T02 ON T01.unit_id = T02.unit_id where user_id = %s "
    row = db.select_all(q, [userID])
    return row

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
        " WHERE t3.user_category_id = %s Order by t1.form_type_id DESC"
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
    db, user_category_id, user_privilege_name, user_group_id=None
):
    condition = "user_group_name = %s "
    condition_val = [user_privilege_name]
    # if user_category_id is not None:
    #     condition += " AND user_category_id != %s "
    #     condition_val.append(user_category_id)
    if user_group_id is not None:
        condition += " AND user_group_id != %s "
        condition_val.append(user_group_id)
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
    groups = db.select_all(q, None)
    columns = ["user_group_id", "form_id"]
    group_forms = db.get_data(
        "tbl_user_group_forms", columns, "1 ORDER BY user_group_id"
    )
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
    print ""
    print result
    if result is False:
        raise client_process_error("E004")
    if result:
        for x in user_privilege.form_ids:
            columns1 = ["user_group_id", "form_id"]
            values1 = [result, x]
            db.insert(tblUserGroupForms, columns1, values1)

    action = "Created User Group \"%s\"" % user_privilege.user_group_name
    db.save_activity(session_user, 2, action)
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
    db.save_activity(session_user, 2, action)
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

def verify_password_user_privilege(db, user_id, password):
    ec_password = encrypt(password)
    q = "SELECT username from tbl_user_login_details where user_id = %s and password = %s"
    #print q
    data_list = db.select_one(q, [user_id, ec_password])
    if data_list is None:
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
    print "+++++++++++++++++++++++++"
    print is_active
    is_active = 0 if is_active is not True else 1
    print is_active
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
    db.save_activity(session_user, 2, action)
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
def get_no_of_remaining_licence_Viewonly(db):
    q = " SELECT (total_view_licence - ifnull(licence_used,0)) As remaining_licence from tbl_client_groups "
    row = db.select_one(q, None)
    return row["remaining_licence"]

############################################################################
# Returns Remaining number of  licence
# Parameter(s) - Object of database
# Return Type - int
############################################################################
def get_no_of_remaining_licence(db, legal_entity_ids):
    q = " SELECT legal_entity_id, (total_licence - ifnull(used_licence,0)) As remaining_licence " + \
        " FROM tbl_legal_entities Where find_in_set(legal_entity_id, %s)"
    legalEntityList = ",".join([str(x) for x in legal_entity_ids])
    row = db.select_all(q, [legalEntityList])
    return row

############################################################################
# Returns User Category ID
# Parameter(s) - Object of database
# Return Type - int
############################################################################
def get_user_Category_by_user_id(db, user_id):
    q = " select user_category_id from tbl_users where user_id = %s "
    row = db.select_one(q, [user_id])
    return row["user_category_id"]

############################################################################
# Returns User Legal Entities
# Parameter(s) - Object of database
# Return Type - int
############################################################################
def get_user_legal_entity_by_user_id(db, user_id):
    q = " select user_id, legal_entity_id From tbl_user_legal_entities where user_id = %s "
    row = db.select_all(q, [user_id])
    return row

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
# To check Units are already assinged
# Parameter(s) - Object of database, employee code, userid
# Return Type - Boolean
#             - Returns Records if units are already assigned
############################################################################
def is_already_assigned_units(db, unit_ids, domain_ids):
    #  q = "SELECT T01.domain_id,T01.unit_id,T05.legal_entity_id,T05.user_id,T05.unit_id,T05.domain_id " + \
    q = " SELECT Count(T01.unit_id) as unit_count " + \
        " FROM tbl_units_organizations AS T01 " + \
        " LEFT JOIN (SELECT T02.legal_entity_id,T02.user_id,T02.unit_id,T03.domain_id " +\
        " FROM tbl_user_units AS T02 " + \
        " INNER JOIN tbl_user_domains AS T03 ON T02.user_id = T03.user_id " + \
        " INNER JOIN tbl_users AS T04 ON T02.user_id = T04.user_id AND T04.user_category_id = 5) AS T05 " +\
        " ON T01.unit_id = T05.unit_id AND T01.domain_id = T05.domain_id " + \
        " WHERE find_in_set(T05.unit_id, %s) AND find_in_set(T05.domain_id, %s) "

    unitList = ",".join(str(uid.unit_id) for uid in unit_ids)
    domainList = ",".join(str(uid.domain_id) for uid in domain_ids)

    row = db.select_one(q, [unitList, domainList])

    if int(row["unit_count"]) > 0:
        return True
    else :
        return False

############################################################################
# To Save User Domains
# Parameter(s) - Object of database, domain ids, user id
# Return Type - None / RunTimeError
#             - Returns RuntimeError if insertion fails
############################################################################
def save_user_domains(db, domain_ids, user_id):
    for domain_id in domain_ids:
        db.delete(tblUserDomains, "user_id = %s", [user_id])
    domain_columns = ["user_id", "legal_entity_id", "domain_id"]
    domain_values_list = [
        (user_id, int(uid.legal_entity_id), int(uid.domain_id)) for uid in domain_ids
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
    unit_columns = ["user_id", "legal_entity_id", "unit_id"]
    unit_values_list = [
        (user_id, int(uid.legal_entity_id), int(uid.unit_id)) for uid in unit_ids
    ]
    res = db.bulk_insert(tblUserUnits, unit_columns, unit_values_list)
    if res is False:
        raise client_process_error("E010")
############################################################################
# To Save User Legal Entities
# Parameter(s) - Object of database, unit ids, user id
# Return Type - None / RunTimeError
#             - Returns RuntimeError if insertion fails
############################################################################
def save_user_legal_entities(db, entity_ids, user_id):
    db.delete(tbluserlegalentities, "user_id = %s", [user_id])
    entity_columns = ["user_id", "legal_entity_id"]
    entity_values_list = [(user_id, int(le_id)) for le_id in entity_ids]
    # print "entity_columns>>>", entity_columns
    # print "entity_values_list>>", entity_values_list
    res = db.bulk_insert(tbluserlegalentities, entity_columns, entity_values_list)
    if res is False:
        raise client_process_error("E010")

############################################################################
# To Save Registration Token
# Parameter(s) - Object of database, unit ids, user id
# Return Type - None / RunTimeError
#             - Returns RuntimeError if insertion fails
############################################################################
def save_registration_token(db, short_name, user_id, emp_name, email_id):
    def _del_olddata():
        condition = "user_id = %s and verification_type_id = %s"
        condition_val = [user_id, 1]
        db.delete(tblEmailVerification, condition, condition_val)
        return True

    current_time_stamp = get_current_date()
    registration_token = new_uuid()
    expiry_date = addHours(int(REGISTRATION_EXPIRY), current_time_stamp)

    link = "%suserregistration/%s/%s" % (
        CLIENT_URL,short_name, registration_token
    )

    notify_user_thread = threading.Thread(
        target=notify_user, args=[
            short_name, email_id, emp_name, link
        ]
    )
    notify_user_thread.start()

    if _del_olddata():
        q = " INSERT INTO tbl_email_verification(user_id, verification_code, " + \
            " verification_type_id, expiry_date) VALUES (%s, %s, %s, %s)"
        row = db.execute(q, [user_id, registration_token, 1, expiry_date])
        return True
    else:
        return False
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
        "client_id", "user_category_id", "user_group_id", "email_id", "employee_name",
        "employee_code", "contact_no", "mobile_no", "user_level",
        "is_service_provider", "created_by", "created_on",
        "updated_by", "updated_on"
    ]

    values = [
        client_id, user.user_category, user.user_group_id, user.email_id,
        user.employee_name, user.employee_code.replace(" ", ""),
        user.contact_no, user.mobile_no, user.user_level,
        user.is_service_provider, session_user, current_time_stamp,
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

    short_name = get_short_name(db)

    save_user_domains(db, user.user_domain_ids, user_id)
    save_user_units(db, user.user_unit_ids, user_id)
    save_user_legal_entities(db, user.user_entity_ids, user_id)

    save_registration_token(db, short_name, user_id, user.employee_name, user.email_id)

    action = "Created user \"%s - %s\"" % (
        user.employee_code, user.employee_name)
    # Audit Log Entry
    db.save_activity(session_user, 4, action)

    # notify_user_thread = threading.Thread(
    #     target=notify_user, args=[
    #         short_name, user.email_id, password,
    #         user.employee_name, user.employee_code
    #     ]
    # )
    # notify_user_thread.start()
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
    current_time_stamp = get_date_time()
    user_id = user.user_id
    current_time_stamp = get_date_time()
    user.is_service_provider = 0 if user.is_service_provider is False else 1
    # columns = [
    #     "user_group_id", "employee_name", "employee_code",
    #     "contact_no", "seating_unit_id", "user_level",
    #     "is_service_provider", "updated_on", "updated_by"
    # ]
    columns = [
        "user_group_id", "email_id", "employee_name",
        "employee_code", "contact_no", "mobile_no", "user_level",
        "is_service_provider",
        "updated_by", "updated_on"
    ]
    # values = [
    #     user.user_group_id, user.employee_name,
    #     user.employee_code.replace(" ", ""),
    #     user.contact_no, user.seating_unit_id, user.user_level,
    #     user.is_service_provider, current_time_stamp,
    #     session_user
    # ]
    values = [
        user.user_group_id, user.email_id,
        user.employee_name, user.employee_code.replace(" ", ""),
        user.contact_no, user.mobile_no, user.user_level,
        user.is_service_provider,
        session_user, current_time_stamp
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

    # save_user_domains(db, user.domain_ids, user_id)
    # save_user_units(db, user.unit_ids, user_id)
    save_user_domains(db, user.user_domain_ids, user_id)
    save_user_units(db, user.user_unit_ids, user_id)
    save_user_legal_entities(db, user.user_entity_ids, user_id)

    UpdateUsers(user, client_id)

    action = "Updated user \"%s - %s\"" % (
        user.employee_code, user.employee_name
    )
    db.save_activity(session_user, 4, action)

    return True

############################################################################
# To Update licence viewonly
# Parameter(s) - Object of database
# Return Type - True / RunTimeError
#             - Returns True on successfull updation
#             - Returns RuntimeError if Updation fails
############################################################################
def update_licence_viewonly(db, mode):
    q = " Update tbl_client_groups SET licence_used = (ifnull(licence_used,0) + %s)"

    if mode== "ADD":
        result1 = db.execute(q, [1])
    elif mode== "LESS":
        result1 = db.execute(q, [-1])

    if result1 is False:
        raise client_process_error("E011")

    return True
############################################################################
# To Update licence viewonly
# Parameter(s) - Object of database
# Return Type - True / RunTimeError
#             - Returns True on successfull updation
#             - Returns RuntimeError if Updation fails
############################################################################
def update_licence(db, legal_entity_id, mode):
    q = " Update tbl_legal_entities SET used_licence = (used_licence + %s) Where legal_entity_id = %s"

    if mode== "ADD":
        result1 = db.execute(q, [1, legal_entity_id])
    elif mode== "LESS":
        result1 = db.execute(q, [-1, legal_entity_id])

    if result1 is False:
        raise client_process_error("E011")

    return True

############################################################################
# To Check the active status of user group of given user
# Parameter(s) - Object of database, user id
# Return Type - None / RunTimeError
#             - Returns RuntimeError if user group of the given user is
#             inactive
############################################################################
def check_user_group_active_status(db, user_id):
    q = "select count(ug.user_group_id) count from tbl_user_groups ug " + \
        " inner join tbl_users u on  ug.user_group_id = u.user_group_id " + \
        " where u.user_id = %s and ug.is_active = 1 "
    row = db.select_one(q, [user_id])
    if int(row["count"]) == 0:
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
        "is_active", "updated_on", "updated_by", "status_changed_on"
    ]
    is_active = 1 if is_active is not False else 0
    condition = "user_id = %s "
    values = [
        is_active, get_date_time(), session_user, get_date_time(), user_id
    ]
    result = db.update(tblUsers, columns, values, condition)
    if result is False:
        raise client_process_error("E012")

    # Updating the Status to Knowledge Database
    # UpdateUserStatus(is_active, user_id, client_id)

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
    columns = "short_name"
    rows = db.get_data(
        tblClientGroups, columns, "1"
    )
    return rows[0]["short_name"]

###############################################################################
# To Send the credentials to the user
# Parameter(s) : email id, password, employee name, employee code
# Return Type : if the email fails raises exception
###############################################################################
def notify_user(
    short_name, email_id, emp_name, link
):
    try:
        email().send_registraion_link(email_id, emp_name, link)
    except Exception, e:
        print "Error while sending email"
        print e


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

    query = "select t1.unit_id, t1.unit_code, t1.unit_name, t1.address, t1.postal_code, " + \
            "(select business_group_name from tbl_business_groups where " + \
            "business_group_id = t1.business_group_id) as business_group_name, " + \
            "(select legal_entity_name from tbl_legal_entities where " + \
            "legal_entity_id = t1.legal_entity_id) as legal_entity_name, " + \
            "(select division_name from tbl_divisions where " + \
            "division_id = t1.division_id) as division_name, " + \
            "(select category_name from tbl_categories where " + \
            "category_id = t1.category_id) as category_name, " + \
            "t1.is_closed as is_active, t1.closed_on, " + \
            "(case when t1.closed_on is not null then " + \
            "abs(DATEDIFF(NOW(), t1.closed_on)) else 0 end) as validity_days, " + \
            "t1.legal_entity_id from tbl_units as t1 where t1.legal_entity_id = %s " + \
            "order by t1.unit_name; "
    result = db.select_all(query, [le_id])

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
        q = "select count(*) as unit_id_cnt from tbl_units where unit_id = %s "
        rows = db.select_all(q, params)
        print rows
        for d in rows:
            if(d["unit_id_cnt"] > 0):
                return True
            else:
                return False


def save_unit_closure_data(db, user_id, unit_id, remarks, action_mode):
    current_time_stamp = get_date_time()
    print action_mode
    msg_text = None
    columns = ["is_closed", "closed_on", "closed_by", "closed_remarks"]
    values = []
    is_closed = 1
    if action_mode == "close":
        print "save"
        values = [is_closed, current_time_stamp, user_id, remarks]
        condition_val = "unit_id= %s"
        values.append(unit_id)
        result = db.update(tblUnits, columns, values, condition_val)
        if result is False:
            raise client_process_error("E010")

        condition_val = []
        qry = "select concat(unit_code,'-',unit_name) as unit_name from tbl_units where unit_id = %s"
        condition_val.append(unit_id)
        u_name = db.select_one(qry, condition_val)

        action = "Closed Unit \"%s\" with the following remarks \"%s\"" % (
            u_name["unit_name"], remarks
        )
        # Audit Log Entry
        db.save_activity(user_id, 4, action)
        # Notification icon -messages
        msg_text = "Unit has been \"" + u_name["unit_name"] + "\" Closed  with the following remarks \"" + remarks + "\""

    elif action_mode == "reactive":
        is_closed = 0
        values = [is_closed, current_time_stamp, user_id, remarks]
        condition_val = "unit_id= %s"
        values.append(unit_id)
        result = db.update(tblUnits, columns, values, condition_val)
        if result is False:
            raise client_process_error("E010")

        condition_val = []
        qry = "select concat(unit_code,'-',unit_name) as unit_name from tbl_units where unit_id = %s"
        condition_val.append(unit_id)
        u_name = db.select_one(qry, condition_val)

        action = "Reactivated Unit \"%s\" with the following remarks \"%s\"" % (
            u_name["unit_name"], remarks
        )
        # Audit Log Entry
        db.save_activity(user_id, 4, action)

        # Notification icon - messages
        msg_text = "Unit has been \"" + u_name["unit_name"] + "\" activated with the following remarks \"" + remarks + "\""

    UnitClose(unit_id, is_closed, current_time_stamp, user_id, remarks, msg_text)
    print "result"
    print result
    return result


###############################################################################################
# Objective: To get the service provider details from master
# Parameter: request object
# Result: list of service providers
###############################################################################################
def get_service_providers_list(db):
    query = "select concat(short_name,' - ',service_provider_name) as sp_name, " + \
            "service_provider_id as sp_id from tbl_service_providers"
    result = db.select_all(query, None)
    print "sp list"
    print result
    sp_details = []

    for row in result:
        sp_details.append(clientmasters.ServiceProviders(
            row["sp_id"], row["sp_name"]
        ))
    return sp_details

###############################################################################################
# Objective: To get the users list with its service providers
# Parameter: request object
# Result: list of users under service providers
###############################################################################################
def get_service_providers_user_list(db):
    query = "select service_provider_id, user_id, concat(employee_code,' - ',employee_name) as " + \
        "user_name from tbl_users where service_provider_id is not null order by employee_name;"

    result = db.select_all(query, None)
    sp_user_details = []

    for row in result:
        sp_id_optional = row["service_provider_id"]
        sp_user_details.append(clientmasters.ServiceProviderUsers(
            sp_id_optional, row["user_id"], row["user_name"]
        ))
    return sp_user_details

###############################################################################################
# Objective: To get the service provider status
# Parameter: request object
# Result: list of service provider status
###############################################################################################
def get_service_provider_status(db):
    status = ("Active", "Inactive", "Blocked")
    sp_status = []
    i = 0
    for sts in status:
        s_p_status = clientmasters.ServiceProvidersStatus(
            i, sts
        )
        sp_status.append(s_p_status)
        i = i + 1
    return sp_status

###############################################################################################
# Objective: To get the service providerand the user details
# Parameter: request object
# Result: list of service provider and user details
###############################################################################################
def get_service_provider_details_report_data(db, request):
    where_clause = None
    condition_val = []
    select_qry = None
    sp_id = request.sp_id
    user_id = request.user_id
    s_p_status = request.s_p_status
    total_count = 0
    print user_id
    select_qry = "select t1.service_provider_id, t1.short_name, t1.service_provider_name, " + \
        "t1.contact_no, t1.email_id, t1.address, t1.contract_from, t1.contract_to, t1.is_active, " + \
        "t1.status_changed_on, t1.is_blocked, t1.blocked_on from tbl_service_providers as t1 "
    where_1 = None
    where_2 = None
    if (int(sp_id) > 0 or s_p_status != "All"):
        where_clause = "where "
        if int(sp_id) > 0:
            where_1 = "t1.service_provider_id = %s "
            condition_val.append(sp_id)

        if s_p_status == "Active":
            where_2 = "t1.is_active = %s and t1.is_blocked = %s "
            condition_val.extend([1, 0])
        elif s_p_status == "Inactive":
            where_2 = "t1.is_active = %s and t1.is_blocked = %s "
            condition_val.extend([0, 0])
        elif s_p_status == "Blocked":
            where_2 = "t1.is_blocked = %s "
            condition_val.append(1)

        if where_1 is not None and where_2 is not None:
            where_clause = where_clause + str(where_1)+" and "+str(where_2)
        elif where_1 is not None:
            where_clause = where_clause + str(where_1)
        elif where_2 is not None:
            where_clause = where_clause + str(where_2)

    if where_clause is None:
        where_clause = "order by t1.service_provider_name ASC limit %s, %s;"
        condition_val.extend([int(request.from_count), int(request.page_count)])
    else:
        where_clause = where_clause + "order by t1.service_provider_name ASC limit %s, %s;"
        condition_val.extend([int(request.from_count), int(request.page_count)])
    query = select_qry + where_clause
    print "qry"
    print query
    result_sp = db.select_all(query, condition_val)

    where_clause = None
    where_1 = None
    where_2 = None
    condition_val = []
    select_qry = None
    select_qry = "select t1.service_provider_id, t1.user_id, t1.employee_name, t1.address, " + \
        "t1.contact_no, t1.email_id, t1.is_active, (select group_concat(unit_id) from " + \
        "tbl_user_units where user_id = t1.user_id) as unit_id, t1.status_changed_on from tbl_users as t1 "

    if (int(sp_id) > 0 or int(user_id) > 0):
        where_clause = "where "
        if int(sp_id) > 0:
            where_1 = "t1.service_provider_id = %s "
            condition_val.append(sp_id)

        if int(user_id) > 0:
            where_2 = "t1.user_id = %s "
            condition_val.append(user_id)

        if where_1 is not None and where_2 is not None:
            where_clause = where_clause + str(where_1)+" and "+str(where_2)
        elif where_1 is not None:
            where_clause = where_clause + str(where_1)
        elif where_2 is not None:
            where_clause = where_clause + str(where_2)

    if where_clause is None:
        where_clause = "order by t1.employee_name ASC;"
    else:
        where_clause = where_clause + "order by t1.employee_name ASC;"

    query = select_qry + where_clause
    print "qry user"
    print query
    result_users = db.select_all(query, condition_val)
    print result_users
    sp_details = []

    if(int(sp_id) == 0 and int(user_id) == 0):
        print "a"
        for row in result_sp:
            sp_id = row["service_provider_id"]
            sp_name = row["short_name"]+' - '+row["service_provider_name"]
            con_no = row["contact_no"]
            email_id = row["email_id"]
            address = row["address"]
            contract_period = datetime_to_string(row["contract_from"])+" to "+datetime_to_string(row["contract_to"])
            if (row["is_active"] == 1 or row["is_active"] == 0) and row["is_blocked"] == 1:
                s_p_status = "Blocked"
                sp_status_date = datetime_to_string(row["blocked_on"])
            elif row["is_active"] == 1 and row["is_blocked"] == 0:
                s_p_status = "Active"
                sp_status_date = datetime_to_string(row["status_changed_on"])
            elif row["is_active"] == 0 and row["is_blocked"] == 0:
                s_p_status = "Inactive"
                sp_status_date = datetime_to_string(row["status_changed_on"])
            unit_count = 0
            for row_1 in result_users:
                if sp_id == row_1["service_provider_id"]:
                    unit_count = getSPUnitsCount(sp_id, result_users)

            sp_details.append(clientmasters.ServiceProvidersDetailsList(
                sp_id, sp_name, con_no, email_id, address, contract_period,
                s_p_status, sp_status_date, unit_count
            ))
            total_count = total_count + 1
            print "3",total_count

            for row_1 in result_users:
                if sp_id == row_1["service_provider_id"]:
                    employee_name = row_1["employee_name"]
                    address = row_1["address"]
                    mob_no = row_1["contact_no"]
                    user_email_id = row_1["email_id"]
                    if row_1["is_active"] == 1:
                        user_status = "Active"
                        user_status_date = datetime_to_string(row_1["status_changed_on"])
                    elif row_1["is_active"] == 0:
                        user_status = "Inactive"
                        user_status_date = datetime_to_string(row_1["status_changed_on"])
                    sp_details.append(clientmasters.ServiceProvidersDetailsList(
                        sp_id, employee_name, mob_no, user_email_id, address, None,
                        user_status, user_status_date, unit_count
                    ))
                    print total_count

    elif (int(sp_id) > 0 or int(user_id) == 0):
        print "b"
        for row in result_sp:
            if (sp_id == row["service_provider_id"]):
                # sp_id = row["service_provider_id"]
                sp_name = row["short_name"]+' - '+row["service_provider_name"]
                con_no = row["contact_no"]
                email_id = row["email_id"]
                address = row["address"]
                contract_period = datetime_to_string(row["contract_from"])+" to "+datetime_to_string(row["contract_to"])
                if (row["is_active"] == 1 or row["is_active"] == 0) and row["is_blocked"] == 1:
                    s_p_status = "Blocked"
                    sp_status_date = datetime_to_string(row["blocked_on"])
                elif row["is_active"] == 1 and row["is_blocked"] == 0:
                    s_p_status = "Active"
                    sp_status_date = datetime_to_string(row["status_changed_on"])
                elif row["is_active"] == 0 and row["is_blocked"] == 0:
                    s_p_status = "Inactive"
                    sp_status_date = datetime_to_string(row["status_changed_on"])
                unit_count = 0
                for row_1 in result_users:
                    if sp_id == row_1["service_provider_id"]:
                        unit_count = getSPUnitsCount(sp_id, result_users)
                sp_details.append(clientmasters.ServiceProvidersDetailsList(
                    sp_id, sp_name, con_no, email_id, address, contract_period,
                    s_p_status, sp_status_date, unit_count
                ))
                total_count = total_count + 1

                for row_1 in result_users:
                    if sp_id == row_1["service_provider_id"]:
                        employee_name = row_1["employee_name"]
                        address = row_1["address"]
                        mob_no = row_1["contact_no"]
                        user_email_id = row_1["email_id"]
                        if row_1["is_active"] == 1:
                            user_status = "Active"
                            user_status_date = datetime_to_string(row_1["status_changed_on"])
                        elif row_1["is_active"] == 0:
                            user_status = "Inactive"
                            user_status_date = datetime_to_string(row_1["status_changed_on"])
                        sp_details.append(clientmasters.ServiceProvidersDetailsList(
                            sp_id, employee_name, mob_no, user_email_id, address, None,
                            user_status, user_status_date, unit_count
                        ))
    elif(int(sp_id) == 0 or int(user_id) > 0):
        print "c"
        for row_1 in result_users:
            if (user_id == row_1["user_id"]):
                sp_id = row_1["service_provider_id"]
                for row in result_sp:
                    if (sp_id == row["service_provider_id"]):
                        print row["service_provider_name"]
                        # sp_id = row["service_provider_id"]
                        sp_name = row["short_name"]+' - '+row["service_provider_name"]
                        con_no = row["contact_no"]
                        email_id = row["email_id"]
                        address = row["address"]
                        contract_period = datetime_to_string(row["contract_from"])+" to "+datetime_to_string(row["contract_to"])
                        if (row["is_active"] == 1 or row["is_active"] == 0) and row["is_blocked"] == 1:
                            s_p_status = "Blocked"
                            sp_status_date = datetime_to_string(row["blocked_on"])
                        elif row["is_active"] == 1 and row["is_blocked"] == 0:
                            s_p_status = "Active"
                            sp_status_date = datetime_to_string(row["status_changed_on"])
                        elif row["is_active"] == 0 and row["is_blocked"] == 0:
                            s_p_status = "Inactive"
                            sp_status_date = datetime_to_string(row["status_changed_on"])
                        unit_count = 0
                        if sp_id == row_1["service_provider_id"]:
                            unit_count = getSPUnitsCount(sp_id, result_users)

                        sp_details.append(clientmasters.ServiceProvidersDetailsList(
                            sp_id, sp_name, con_no, email_id, address, contract_period,
                            s_p_status, sp_status_date, unit_count
                        ))
                        total_count = total_count + 1

                        if sp_id == row_1["service_provider_id"] and user_id == row_1["user_id"]:
                            print row_1["employee_name"]
                            employee_name = row_1["employee_name"]
                            address = row_1["address"]
                            mob_no = row_1["contact_no"]
                            user_email_id = row_1["email_id"]
                            if row_1["is_active"] == 1:
                                user_status = "Active"
                                user_status_date = datetime_to_string(row_1["status_changed_on"])
                            elif row_1["is_active"] == 0:
                                user_status = "Inactive"
                                user_status_date = datetime_to_string(row_1["status_changed_on"])
                            sp_details.append(clientmasters.ServiceProvidersDetailsList(
                                sp_id, employee_name, mob_no, user_email_id, address, None,
                                user_status, user_status_date, unit_count
                            ))
    elif(int(sp_id) > 0 and int(user_id) > 0):
        print "d"
        if (sp_id == row["service_provider_id"]):
            # sp_id = row["service_provider_id"]
            sp_name = row["short_name"]+' - '+row["service_provider_name"]
            con_no = row["contact_no"]
            email_id = row["email_id"]
            address = row["address"]
            contract_period = datetime_to_string(row["contract_from"])+" to "+datetime_to_string(row["contract_to"])
            if (row["is_active"] == 1 or row["is_active"] == 0) and row["is_blocked"] == 1:
                s_p_status = "Blocked"
                sp_status_date = datetime_to_string(row["blocked_on"])
            elif row["is_active"] == 1 and row["is_blocked"] == 0:
                s_p_status = "Active"
                sp_status_date = datetime_to_string(row["status_changed_on"])
            elif row["is_active"] == 0 and row["is_blocked"] == 0:
                s_p_status = "Inactive"
                sp_status_date = datetime_to_string(row["status_changed_on"])
            unit_count = 0
            for row_1 in result_users:
                if sp_id == row_1["service_provider_id"]:
                    unit_count = getSPUnitsCount(sp_id, result_users)
            sp_details.append(clientmasters.ServiceProvidersDetailsList(
                sp_id, sp_name, con_no, email_id, address, contract_period,
                s_p_status, sp_status_date, unit_count
            ))
            total_count = total_count + 1

            for row_1 in result_users:
                if sp_id == row_1["service_provider_id"] and user_id == row_1["user_id"]:
                    employee_name = row_1["employee_name"]
                    address = row_1["address"]
                    mob_no = row_1["contact_no"]
                    user_email_id = row_1["email_id"]
                    if row_1["is_active"] == 1:
                        user_status = "Active"
                        user_status_date = datetime_to_string(row_1["status_changed_on"])
                    elif row_1["is_active"] == 0:
                        user_status = "Inactive"
                        user_status_date = datetime_to_string(row_1["status_changed_on"])
                    sp_details.append(clientmasters.ServiceProvidersDetailsList(
                        sp_id, employee_name, mob_no, user_email_id, address, None,
                        user_status, user_status_date, unit_count
                    ))
    print len(sp_details)
    return sp_details, total_count

def getSPUnitsCount(sp_id, data):
    last = object()
    unit_count = []
    for d in data:
        if last != d["service_provider_id"]:
            last = d["service_provider_id"]
            if d["unit_id"] is not None:
                u_id = d["unit_id"].split(",")
                last_1 = object()
                for u in u_id:
                    if last_1 != u:
                        last_1 = u
                        unit_count.append(u)
    return len(unit_count)


###############################################################################################
# Objective: To get the list of users under legal entity
# Parameter: request object
# Result: list of users
###############################################################################################
def get_audit_users_list(db, legal_entity_id):
    query = "select distinct(t2.user_id), t2.employee_code,t2.employee_name, " + \
        "t2.user_category_id, t2.user_group_id from tbl_user_legal_entities as t1 inner join tbl_users as t2 " + \
        "on t2.user_id = t1.user_id or t2.user_category_id=1 where t1.legal_entity_id=%s " + \
        "order by employee_name asc;"
    result = db.select_all(query, [legal_entity_id])
    audit_users_list = []
    for row in result:
        u_g_id = row["user_group_id"]
        if row["employee_code"] is None:
            user_name = row["employee_name"]
        else:
            user_name = row["employee_code"]+' - '+row["employee_name"]
        audit_users_list.append(clientmasters.AuditTrailUsers(
            row["user_id"], user_name, row["user_category_id"], u_g_id
        ))
    return audit_users_list

###############################################################################################
# Objective: To get the list of forms under legal entity
# Parameter: request object
# Result: list of forms
###############################################################################################
def get_audit_forms_list(db):
    query = "select t1.user_group_id as u_g_id, t1.form_id, t2.form_name from tbl_user_group_forms " + \
        "as t1 inner join tbl_forms as t2 on t2.form_id = t1.form_id and t2.form_type_id in ('1','2');"
    result = db.select_all(query, None)
    audit_forms_list = []
    for row in result:
        audit_forms_list.append(clientmasters.AuditTrailForms(
            row["u_g_id"], row["form_id"], row["form_name"]
        ))
    return audit_forms_list

###############################################################################################
# Objective: To get the list of users
# Parameter: request object
# Result: list of users
###############################################################################################
def get_login_users_list(db):
    query = "select user_id, employee_code,employee_name, " + \
        "user_category_id, user_group_id from tbl_users order by employee_name asc;"
    result = db.select_all(query, None)
    login_users_list = []
    for row in result:
        u_g_id = row["user_group_id"]
        if row["employee_code"] is None or row["employee_code"] == "":
            user_name = row["employee_name"]
        else:
            user_name = row["employee_code"]+' - '+row["employee_name"]
        login_users_list.append(clientmasters.AuditTrailUsers(
            row["user_id"], user_name, row["user_category_id"], u_g_id
        ))
    return login_users_list


###############################################################################################
# Objective: To get the list of activities
# Parameter: request object
# Result: list of activities
###############################################################################################
def process_login_trace_report(db, request, client_id):
    where_clause = None
    condition_val = []
    select_qry = None
    user_id = request.user_id
    due_from = request.due_from_date
    due_to = request.due_to_date

    print user_id

    select_qry = "select t1.form_id, t1.action, t1.created_on, (select  " + \
        "concat(employee_code,' - ',employee_name) from tbl_users where user_id " + \
        "= t1.user_id) as user_name from tbl_activity_log as t1 where "
    where_clause = "t1.form_id = 0 "

    if int(user_id) > 0:
        where_clause = where_clause + "and t1.user_id = %s "
        condition_val.append(user_id)
    if due_from is not None and due_to is not None:
        due_from = string_to_datetime(due_from).date()
        due_to = string_to_datetime(due_to).date()
        where_clause = where_clause + " and t1.created_on >= " + \
            " date(%s)  and t1.created_on <= " + \
            " DATE_ADD(%s, INTERVAL 1 DAY)  "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        due_from = string_to_datetime(due_from).date()
        where_clause = where_clause + " and t1.created_on >= " + \
            " date(%s)  and t1.created_on <= " + \
            " DATE_ADD(date(curdate()), INTERVAL 1 DAY) "
        condition_val.append(due_from)
    elif due_from is None and due_to is not None:
        due_to = string_to_datetime(due_to).date()
        where_clause = where_clause + " and t1.created_on < " + \
            " DATE_ADD(%s, INTERVAL 1 DAY) "
        condition_val.append(due_to)

    where_clause = where_clause + "order by t1.created_on desc limit %s, %s;"
    condition_val.extend([int(request.from_count), int(request.page_count)])
    query = select_qry + where_clause
    print "qry"
    print query
    result = db.select_all(query, condition_val)

    where_clause = None
    condition_val = []
    if request.from_count == 0:
        select_qry = "select t1.form_id, t1.action, t1.created_on, (select  " + \
            "concat(employee_code,' - ',employee_name) from tbl_users where user_id " + \
            "= t1.user_id) as user_name from tbl_activity_log as t1 where "
        where_clause = "t1.form_id = 0 "

        if int(user_id) > 0:
            where_clause = where_clause + "and t1.user_id = %s "
            condition_val.append(user_id)
        if due_from is not None and due_to is not None:
            where_clause = where_clause + " and t1.created_on >= " + \
                " date(%s)  and t1.created_on <= " + \
                " DATE_ADD(%s, INTERVAL 1 DAY)  "
            condition_val.extend([due_from, due_to])
        elif due_from is not None and due_to is None:
            where_clause = where_clause + " and t1.created_on >= " + \
                " date(%s)  and t1.created_on <= " + \
                " DATE_ADD(date(curdate()), INTERVAL 1 DAY) "
            condition_val.append(due_from)
        elif due_from is None and due_to is not None:
            where_clause = where_clause + " and t1.created_on < " + \
                " DATE_ADD(%s, INTERVAL 1 DAY) "
            condition_val.append(due_to)

        where_clause = where_clause + "order by t1.created_on desc;"
        query = select_qry + where_clause
        count = db.select_all(query, condition_val)
        print len(count)


    activity_list = []
    for row in result:
        if row["action"].find("Login") >= 0:
            activity_list.append(clientmasters.LoginTraceActivities(
                row["form_id"], "Login",
                row["action"], datetime_to_string_time(row["created_on"])
            ))
        elif row["action"].find("Logout") >= 0:
            activity_list.append(clientmasters.LoginTraceActivities(
                row["form_id"], "Logout",
                row["action"], datetime_to_string_time(row["created_on"])
            ))
    if request.from_count == 0:
        return activity_list, len(count)
    else:
        return activity_list, 0


###############################################################################################
# Objective: To get the user details under client
# Parameter: request object
# Result: user information
###############################################################################################
def get_user_info(db, session_user, client_id):
    user_id = session_user
    query = "select t1.employee_name, (select short_name from tbl_client_groups where client_id = %s) as " + \
        "short_name, t1.email_id, t1.contact_no, t1.mobile_no, t1.employee_code, (select username from " + \
        "tbl_user_login_details where user_id = t1.user_id) as user_name, (select user_group_name from " + \
        "tbl_user_groups where user_category_id = t1.user_category_id and user_group_id = t1.user_group_id) " + \
        "as u_g_name, t1.address from tbl_users as t1 where t1.user_id = %s"
    result = db.select_all(query, [client_id, user_id])
    user_profile = []
    for row in result:
        user_name = row["user_name"]
        emp_code = row["employee_code"]
        emp_name = row["employee_name"]
        short_name = row["short_name"]
        email_id = row["email_id"]
        con_no = row["contact_no"]
        mob_no = row["mobile_no"]
        u_g_name = row["u_g_name"]
        address = row["address"]
        user_profile.append(clientmasters.UserProfile(
            user_id, user_name, emp_code, emp_name, short_name, email_id,
            con_no, mob_no, u_g_name, address
        ))
    return user_profile

###############################################################################################
# Objective: To update user details
# Parameter: request object and the client id
# Result: updates user details
###############################################################################################
def update_profile(db, session_user, request):
    user_id = request.user_id
    email_id = request.email_id
    con_no = request.con_no
    mob_no = request.mob_no
    address = request.address
    current_time_stamp = get_date_time()
    columns = [
        "email_id", "contact_no", "mobile_no", "address", "updated_on", "updated_by"
    ]
    values = [
        email_id, con_no, mob_no, address, current_time_stamp, session_user
    ]
    condition = "user_id= %s "

    values.append(user_id)
    result1 = db.update(tblUsers, columns, values, condition)
    if result1 is False:
        raise client_process_error("E011")

    action = "Updated user \"%s - %s\"" % (
        request.emp_code, request.emp_name
    )
    db.save_activity(session_user, 4, action)

    return True

###############################################################################################
# Objective: To get legal entity domains and organizations
# Parameter: request object and the client id, legal entity id
# Result: return list of legal entities domains and organization
###############################################################################################
def get_legal_entity_domains_data(db, request):
    le_id = request.legal_entity_id
    # legal entity domains
    query = "select t1.activation_date, t1.count as org_count, (select domain_name from tbl_domains where " + \
        "domain_id = t1.domain_id) as domain_name, (select organisation_name from tbl_organisation " + \
        "where organisation_id = t1.organisation_id) as organisation_name from tbl_legal_entity_domains as t1 " + \
        "where t1.legal_entity_id = %s"
    result = db.select_all(query, [le_id])
    le_domains_info = []
    for row in result:
        # if (row["domain_name"] is not None or row["organisation_name"] is not None):
        le_domains_info.append(clientmasters.LegalEntityDomains(
            row["domain_name"], row["organisation_name"], row["org_count"],
            activity_date=datetime_to_string(row["activation_date"])
        ))
    return le_domains_info
