import os
import io
import datetime
import json
from dateutil import relativedelta
from server.clientdatabase.tables import *
from server.constants import (CLIENT_DOCS_BASE_PATH)
from clientprotocol import (clientcore, dashboard)
from server.common import (
    encrypt, convert_to_dict, get_date_time, get_date_time_in_date,
    remove_uploaded_file, convert_to_key_dict, datetime_to_string
)
from server.exceptionmessage import client_process_error
from savetoknowledge import UpdateFileSpace
CLIENT_LOGO_PATH = "/clientlogo"

__all__ = [
    "get_client_user_forms",
    "get_countries_for_user",
    "get_domains_for_user",
    "get_business_groups_for_user",
    "get_legal_entities_for_user",
    "get_divisions_for_user",
    "get_categories_for_user",
    "get_divisions",
    "get_categories",
    "get_group_name",
    "get_country_wise_domain_month_range",
    "get_units_for_user",
    "get_client_users",
    "get_user_domains",
    "get_user_countries",
    "verify_username",
    "verify_password",
    "get_countries",
    "get_domains",
    "is_primary_admin",
    "have_compliances",
    "is_seating_unit",
    "is_admin",
    "get_user_unit_ids",
    "is_two_levels_of_approval",
    "get_user_company_details",
    "get_client_level_1_statutoy",
    "get_service_providers",
    "get_client_compliances",
    "get_client_settings",
    "get_admin_info",
    "validate_compliance_due_date",
    "get_compliance_frequency",
    "get_users",
    "get_users_by_id",
    "get_users_by_unit_and_domain",
    "get_compliance_name_by_id",
    "is_space_available",
    "update_used_space",
    "save_compliance_activity",
    "save_compliance_notification",
    "get_email_id_for_users",
    "get_user_email_name",
    "calculate_due_date",
    "filter_out_due_dates",
    "convert_base64_to_file",
    "get_user_name_by_id",
    "get_form_ids_for_admin",
    "get_report_form_ids",
    "get_client_id_from_short_name",
    "validate_reset_token",
    "remove_session",
    "update_profile",
    "is_service_proivder_user",
    "convert_datetime_to_date",
    "is_old_primary_admin",
    "get_domains_info",
    "get_user_based_units",
    "get_user_widget_settings",
    "save_user_widget_settings",
    "get_themes",
    "get_themes_for_user",
    "save_themes_for_user",
    "update_themes_for_user",
    "legal_entity_logo_url",
    "verify_username_forgotpassword",
    "update_task_status_in_chart",
    "get_reassign_client_users"
    ]


def get_client_user_forms(db, user_id):
    # columns = "tf.form_id, tf.form_type_id, tft.form_type, tf.form_name, "
    # columns += "tf.form_url, tf.form_order, tf.parent_menu "

    # tables = [tblForms, tblFormType]
    # aliases = ["tf",  "tft"]
    # joinConditions = ["tf.form_type_id = tft.form_type_id"]
    # whereCondition, whereConditionVal = db.generate_tuple_condition(
    #     "form_id", [int(x) for x in form_ids.split(",")]
    # )
    # order = " order by tf.form_order "
    # joinType = "left join"
    # rows = db.get_data_from_multiple_tables(
    #     columns, tables, aliases, joinType,
    #     joinConditions, whereCondition + order, [whereConditionVal]
    # )
    return rows


def get_admin_id(db):
    columns = "user_id"
    condition = " is_active = 1 and user_category_id = 1"  # and is_primary_admin = 1
    rows = db.get_data(tblUsers, columns, condition)
    return rows[0]["user_id"]

def get_countries_for_user(db, user_id):
    query = "SELECT t4.country_id, t4.country_name, t4.is_active FROM tbl_users AS t1 " + \
        " INNER JOIN tbl_user_units AS t2 ON t2.user_id = t1.user_id " + \
        " INNER JOIN tbl_legal_entities AS t3 ON t3.legal_entity_id = t2.legal_entity_id " + \
        " INNER JOIN tbl_countries AS t4 ON t4.country_id = t3.country_id " + \
        " WHERE t1.user_id = %s GROUP BY t4.country_id "
    rows = db.select_all(query, [user_id])

    return return_countries(rows)

def return_countries(data):
    results = []
    for d in data:
        results.append(clientcore.Country(
            d["country_id"], d["country_name"], bool(d["is_active"])
        ))
    return results


# def get_domains_for_user(db, user_id):
#     admin_id = get_admin_id(db)
#     query = "SELECT distinct t1.domain_id, t1.domain_name, " + \
#         " t1.is_active FROM tbl_domains t1 "
#     if user_id != admin_id:
#         query = query + " INNER JOIN tbl_user_domains t2 ON " + \
#             " t1.domain_id = t2.domain_id WHERE t2.user_id = %s"
#         rows = db.select_all(query, [user_id])
#     else:
#         rows = db.select_all(query)
#     columns = ["domain_id", "domain_name", "is_active"]
#     result = convert_to_dict(rows, columns)
#     return return_domains(result)

def get_domains_for_user(db, user_id, user_category):
    if user_category > 3 :
        query = "SELECT distinct t1.domain_id, t1.legal_entity_id, t2.domain_name, " + \
            "t2.is_active FROM tbl_user_domains AS t1 " + \
            "INNER JOIN tbl_domains AS t2 ON t2.domain_id = t1.domain_id " + \
            "where t1.user_id = %s "

        rows = db.select_all(query, [user_id])
    else:
        query = "SELECT distinct t1.domain_id, t1.legal_entity_id, t2.domain_name, " + \
            "t2.is_active FROM tbl_legal_entity_domains AS t1 " + \
            "INNER JOIN tbl_domains AS t2 ON t2.domain_id = t1.domain_id "
        rows = db.select_all(query)
    return return_domains(rows)


def get_domains_info(db, user_id, user_category, le_ids=None):

    if user_category > 3 :
        query = "SELECT distinct t1.domain_id, t2.domain_name, " + \
            "t2.is_active FROM tbl_user_domains AS t1 " + \
            "INNER JOIN tbl_domains AS t2 ON t2.domain_id = t1.domain_id " + \
            "where t1.user_id = %s "
        param = [user_id]
        if le_ids is not None :
            query += " and find_in_set(t1.legal_entity_id, %s) "
            param.append(",".join([str(x) for x in le_ids]))

        rows = db.select_all(query, param)
    elif user_category == 1 :
        query = "SELECT distinct t1.domain_id, t2.domain_name, " + \
            "t2.is_active FROM tbl_legal_entity_domains AS t1 " + \
            "INNER JOIN tbl_domains AS t2 ON t2.domain_id = t1.domain_id  "
        param = []
        if le_ids is not None :
            query += " where find_in_set(t1.legal_entity_id, %s) "
            param.append(",".join([str(x) for x in le_ids]))

        rows = db.select_all(query, param)
    else :
        query = "SELECT distinct t2.domain_id, t2.domain_name, " + \
            "t2.is_active FROM tbl_domains AS t2 " + \
            " INNER JOIN tbl_legal_entity_domains as t3 on t2.domain_id = t3.domain_id " + \
            "INNER JOIN tbl_user_legal_entities AS t4 ON t4.legal_entity_id = t3.legal_entity_id " + \
            "where t4.user_id = %s "
        param = [user_id]
        if le_ids is not None :
            query += " and find_in_set(t3.legal_entity_id, %s) "
            param.append(",".join([str(x) for x in le_ids]))

        rows = db.select_all(query, param)

    results = []
    for d in rows:
        results.append(clientcore.DomainInfo(
            d["domain_id"], d["domain_name"], bool(d["is_active"])
        ))
    return results


def return_domains(data):
    results = []
    for d in data:
        results.append(clientcore.Domain(
            d["domain_id"], d["domain_name"], d["legal_entity_id"], bool(d["is_active"])
        ))
    return results

def get_business_groups_for_user(db, business_group_ids):
    columns = "business_group_id, business_group_name"
    condition = "1 "
    condition_val = None
    if business_group_ids is not None:
        condition = " find_in_set (business_group_id, %s) "
        condition_val = [business_group_ids]
    order = " ORDER BY business_group_name "
    rows = db.get_data(
        tblBusinessGroups, columns, condition, condition_val, order
    )
    return return_business_groups(rows)


def return_business_groups(business_groups):
    results = []
    for business_group in business_groups:
        results.append(clientcore.ClientBusinessGroup(
            business_group["business_group_id"],
            business_group["business_group_name"]
        ))
    return results


def get_legal_entities_for_user(db, legal_entity_ids):
    columns = "legal_entity_id, legal_entity_name, business_group_id"
    condition = "1 "
    condition_val = None
    if legal_entity_ids is not None:
        condition = " find_in_set(legal_entity_id, %s) "
        condition_val = [legal_entity_ids]
    order = "ORDER BY legal_entity_name "
    rows = db.get_data(
        tblLegalEntities, columns, condition, condition_val, order
    )
    return return_legal_entities(rows)

def get_legal_entities(db, user_id):
    query = "SELECT t4.country_id, t4.country_name, t4.is_active FROM tbl_users AS t1 " + \
        " INNER JOIN tbl_user_units AS t2 ON t2.user_id = t1.user_id " + \
        " INNER JOIN tbl_legal_entities AS t3 ON t3.legal_entity_id = t2.legal_entity_id " + \
        " INNER JOIN tbl_countries AS t4 ON t4.country_id = t3.country_id " + \
        " WHERE t1.user_id = %s GROUP BY t4.country_id "
    rows = db.select_all(query, [user_id])
    return return_countries(rows)


def return_legal_entities(legal_entities):
    results = []
    for legal_entity in legal_entities:
        b_group_id = None
        if legal_entity["business_group_id"] > 0:
            b_group_id = int(legal_entity["business_group_id"])
        results.append(clientcore.ClientLegalEntity(
            legal_entity["legal_entity_id"],
            legal_entity["legal_entity_name"],
            b_group_id
        ))
    return results

def get_divisions_for_user(db, division_ids):
    columns = "division_id, division_name, legal_entity_id, business_group_id"
    condition = "1"
    condition_val = None
    if division_ids is not None:
        condition = " find_in_set(division_id, %s) "
        condition_val = [division_ids]
    order = " ORDER BY division_name"
    rows = db.get_data(
        tblDivisions, columns, condition, condition_val, order
    )
    return return_divisions(rows)

def get_divisions(db):
    columns = "division_id, division_name, legal_entity_id, business_group_id"
    condition = "1"
    condition_val = None
    rows = db.get_data(
        tblDivisions, columns, condition, condition_val
    )
    return return_divisions(rows)

def return_divisions(divisions):
    results = []
    for division in divisions:
        division_obj = clientcore.ClientDivision(
            division["division_id"], division["division_name"],
            division["legal_entity_id"], division["business_group_id"]
        )
        results.append(division_obj)
    return results

def get_categories_for_user(db, category_ids):
    columns = "category_id, category_name, division_id, legal_entity_id, business_group_id"
    condition = "1"
    condition_val = None
    if category_ids is not None:
        condition = " find_in_set(category_id, %s) "
        condition_val = [category_ids]
    order = " ORDER BY category_name"
    rows = db.get_data(
        tblCategories, columns, condition, condition_val, order
    )
    return return_categories(rows)

def get_categories(db):
    q = "SELECT category_id, category_name, division_id, legal_entity_id, business_group_id from tbl_categories"
    rows = db.select_all(q)
    return return_categories(rows)

def return_categories(categories):
    results = []
    for category in categories:
        category_obj = clientcore.ClientCategory(
            category["category_id"], category["category_name"], category["legal_entity_id"],
            category["business_group_id"], category["division_id"]
        )
        results.append(category_obj)
    return results


def get_group_name(db):
    query = "SELECT group_name from %s " % tblClientGroups
    row = db.select_one(query)
    if row:
        return row["group_name"]
    return "group_name"


def get_country_wise_domain_month_range(db):
    q = " SELECT t1.country_id, " + \
        " (select country_name " + \
        " from tbl_countries " + \
        " where country_id = t1.country_id) country_name, " + \
        " t1.domain_id," + \
        " (select domain_name from tbl_domains " + \
        " where domain_id = t1.domain_id)domain_name, " + \
        " t1.month_from, t1.month_to " + \
        " from tbl_client_configuration t1 INNER JOIN " + \
        " tbl_countries TC ON TC.country_id = t1.country_id  " + \
        " INNER JOIN tbl_domains TD ON TD.domain_id = t1.domain_id"
    rows = db.select_all(q)

    country_wise = {}
    domain_info = []
    for r in rows:
        country_name = r["country_name"].strip()
        domain_name = r["domain_name"]
        info = dashboard.DomainWiseYearConfiguration(
            country_name,
            domain_name,
            db.string_full_months.get(int(r["month_from"])),
            db.string_full_months.get(int(r["month_to"]))
        )
        domain_info = country_wise.get(country_name)
        if domain_info is None:
            domain_info = []

        domain_info.append(info)
        country_wise[country_name] = domain_info
    return country_wise


# def get_units_for_user(db, unit_ids):
#     columns = [
#         "unit_id", "unit_code", "unit_name", "address", "division_id",
#         "domain_ids", "country_id", "legal_entity_id", "business_group_id",
#         "is_active", "is_closed"
#     ]
#     condition = "is_closed = 0"
#     condition_val = None
#     if unit_ids is not None:
#         condition = " find_in_set(unit_id, %s) "
#         condition_val = [unit_ids]
#     order = "ORDER BY unit_name"
#     rows = db.get_data(
#         tblUnits, columns, condition, condition_val, order
#     )
#     return return_units(rows)

def get_user_based_units(db, user_id, user_category) :
    if user_category > 3 :
        query = "SELECT t2.unit_id, t2.legal_entity_id, t2.division_id, " + \
                "t2.category_id, t2.unit_code, t2.unit_name, t2.is_closed, " + \
                "t2.address, (select GROUP_CONCAT(distinct domain_id) from tbl_units_organizations where unit_id = t1.unit_id) as domain_ids, " + \
                " t2.country_id, t2.business_group_id " + \
                "FROM tbl_user_units AS t1 " + \
                "INNER JOIN tbl_units AS t2 ON t2.unit_id = t1.unit_id  " + \
                "WHERE t1.user_id = %s AND t2.is_closed = 0 ORDER BY unit_name"
        rows = db.select_all(query, [user_id])
    else:
        query = "SELECT t2.unit_id, t2.legal_entity_id, t2.division_id, " + \
                "t2.category_id, t2.unit_code, t2.unit_name, t2.is_closed, " + \
                "t2.address, (select GROUP_CONCAT(distinct domain_id) from tbl_units_organizations where unit_id = t2.unit_id) as domain_ids, " + \
                " t2.country_id, t2.business_group_id " + \
                "FROM tbl_units AS t2   " + \
                "WHERE t2.is_closed = 0 Group by t2.unit_id ORDER BY unit_name"
        rows = db.select_all(query)
    return return_units(rows)


def get_units_for_user(db, user_id):
    #admin_id = get_admin_id(db)
    user_category_id = get_user_category(db, user_id)
    if user_category_id > 3:
        query = "SELECT t2.unit_id, t2.legal_entity_id, t2.division_id, " + \
                "t2.category_id, t2.unit_code, t2.unit_name, t2.is_closed, " + \
                "t2.address, GROUP_CONCAT(t3.domain_id) as domain_ids, t2.country_id, t2.business_group_id " + \
                "FROM tbl_user_units AS t1 " + \
                "INNER JOIN tbl_units AS t2 ON t2.unit_id = t1.unit_id  " + \
                "INNER JOIN tbl_units_organizations AS t3 ON t3.unit_id = t2.unit_id " + \
                "WHERE t1.user_id = %s AND t2.is_closed = 0 group by t2.unit_id ORDER BY t2.unit_name"
        rows = db.select_all(query, [user_id])
    else:
        query = "SELECT t2.unit_id, t2.legal_entity_id, t2.division_id, " + \
                "t2.category_id, t2.unit_code, t2.unit_name, t2.is_closed, " + \
                "t2.address, GROUP_CONCAT(t3.domain_id) as domain_ids, t2.country_id, t2.business_group_id " + \
                "FROM tbl_user_units AS t1 " + \
                "INNER JOIN tbl_units AS t2 ON t2.unit_id = t1.unit_id  " + \
                "INNER JOIN tbl_units_organizations AS t3 ON t3.unit_id = t2.unit_id " + \
                "WHERE t2.is_closed = 0 group by t2.unit_id ORDER BY t2.unit_name"
        rows = db.select_all(query)
    return return_units(rows)

def return_units(units):
        results = []
        for unit in units:
            division_id = None
            category_id = None
            b_group_id = None
            if unit["division_id"] > 0:
                division_id = unit["division_id"]
            if unit["category_id"] > 0:
                category_id = unit["category_id"]
            if unit["business_group_id"] > 0:
                b_group_id = unit["business_group_id"]
            results.append(clientcore.ClientUnit(
                unit["unit_id"], division_id, category_id, unit["legal_entity_id"],
                b_group_id, unit["unit_code"],
                unit["unit_name"], unit["address"],
                [int(x) for x in unit["domain_ids"].split(",")],
                unit["country_id"],
                bool(unit["is_closed"])
            ))
        return results

# get_acts_for_user(db, user_id):
#     admin_id = get_admin_id(db)
#     if user_id != admin_id:
#         query = "SELECT t2.unit_id, t2.legal_entity_id, t2.division_id, " + \
#         "t2.category_id, t2.unit_code, t2.unit_name, t2.is_closed, " + \
#         "t2.address, t2.domain_ids, t2.country_id, t2.business_group_id " + \
#         "FROM tbl_user_units AS t1 " + \
#         "INNER JOIN tbl_units AS t2 ON t2.unit_id = t1.unit_id  " + \
#         "WHERE t1.user_id = %s AND t2.is_closed = 0 ORDER BY unit_name"
#         rows = db.select_all(query, [user_id])
#     else:
#         query = "SELECT t2.unit_id, t2.legal_entity_id, t2.division_id, " + \
#         "t2.category_id, t2.unit_code, t2.unit_name, t2.is_closed, " + \
#         "t2.address, t2.domain_ids, t2.country_id, t2.business_group_id " + \
#         "FROM tbl_user_units AS t1 " + \
#         "INNER JOIN tbl_units AS t2 ON t2.unit_id = t1.unit_id " +\
#         "WHERE t2.is_closed = 0 ORDER BY unit_name"
#         rows = db.select_all(query)
#     return return_units(rows)


def get_acts_for_user(db, user_id):
    admin_id = get_admin_id(db)
    if user_id != admin_id:
        query = "SELECT distinct t1.domain_id, SUBSTRING_INDEX(substring(substring(t3.statutory_mapping,3),1, char_length(t3.statutory_mapping) -4), '>>', 1) as act " + \
            "FROM tbl_user_domains AS t1 " + \
            "INNER JOIN tbl_domains AS t2 ON t2.domain_id = t1.domain_id " + \
            "INNER JOIN tbl_compliances AS t3 ON t3.domain_id = t1.domain_id " + \
            "where t1.user_id = %s "
        rows = db.select_all(query, [user_id])
    else:
        query = "SELECT distinct t1.domain_id, SUBSTRING_INDEX(substring(substring(t3.statutory_mapping,3),1, char_length(t3.statutory_mapping) -4), '>>', 1) as act " + \
            "FROM tbl_user_domains AS t1 " + \
            "INNER JOIN tbl_domains AS t2 ON t2.domain_id = t1.domain_id " + \
            "INNER JOIN tbl_compliances AS t3 ON t3.domain_id = t1.domain_id "
        rows = db.select_all(query)
    return return_acts(rows)

def return_acts(acts):
        results = []
        for act in acts:
            results.append(clientcore.ClientAct(
                act["domain_id"], act["act"].strip()
            ))
        return results

def get_units_for_user_assign(db, unit_ids):
    columns = [
        "unit_id", "unit_code", "unit_name", "address", "division_id",
        "domain_ids", "country_id", "legal_entity_id", "business_group_id",
        "is_active", "is_closed"
    ]
    condition = "is_closed = 0"
    condition_val = None
    if unit_ids is not None:
        condition = " find_in_set(unit_id, %s) "
        condition_val = [unit_ids]
    order = "ORDER BY unit_name"
    rows = db.get_data(
        tblUnits, columns, condition, condition_val, order
    )
    return return_units(rows)


def return_units_assign(units):
        results = []
        for unit in units:
            division_id = None
            b_group_id = None
            if unit["division_id"] > 0:
                division_id = unit["division_id"]
            if unit["business_group_id"] > 0:
                b_group_id = unit["business_group_id"]
            results.append(clientcore.ClientUnit(
                unit["unit_id"], division_id, unit["legal_entity_id"],
                b_group_id, unit["unit_code"],
                unit["unit_name"], unit["address"], bool(unit["is_active"]),
                [int(x) for x in unit["domain_ids"].split(",")],
                unit["country_id"],
                bool(unit["is_closed"])
            ))
        return results

# def get_client_users(db, unit_ids=None):
#     columns = "user_id, employee_name, employee_code, is_active"
#     condition = "1"
#     conditon_val = None
#     if unit_ids is not None:
#         condition += " and seating_unit_id in (%s)"
#         conditon_val = [unit_ids]
#     rows = db.get_data(
#         tblUsers, columns, condition, conditon_val
#     )
#     return return_client_users(rows)


def get_client_users(db):
    query = "SELECT distinct t1.user_id, t1.employee_name, " + \
        "t1.employee_code, t1.is_active, t3.legal_entity_id, t1.user_category_id from tbl_users as t1 " + \
        " inner join tbl_user_legal_entities t3 on t1.user_id = t3.user_id  " + \
        "left join tbl_user_domains as t2 ON t2.user_id = t1.user_id where t1.user_category_id != 2"

    rows = db.select_all(query)
    return return_client_users(rows)


def get_assignees(db, unit_ids=None):
    q = "select t1.user_id, t1.employee_code, t1.employee_name, t1.is_active, t2.legal_entity_id, t1.user_category_id " + \
        " from tbl_users t1  " + \
        " inner join tbl_user_legal_entities t2 on t1.user_id = t2.user_id  " + \
        " where t1.is_active = 1 and t1.user_category_id in (5,6)"

    rows = db.select_all(q)
    return return_client_users(rows)

def get_reassign_client_users(db):
    query = "SELECT distinct t1.user_id, t1.employee_name, " + \
        "t1.employee_code, t1.is_active, t3.legal_entity_id, t1.user_category_id from tbl_users as t1 " + \
        " inner join tbl_user_legal_entities t3 on (t1.user_id = t3.user_id  or t1.user_category_id = 1)" + \
        "left join tbl_user_domains as t2 ON t2.user_id = t1.user_id " + \
        "where t1.user_category_id != 2"

    rows = db.select_all(query)
    return return_client_users(rows)

def return_client_users(users):
    results = []
    for user in users:
        if user["employee_code"] is not None :
            employee_name = user["employee_code"] + ' - ' + user["employee_name"]
        else:
            employee_name = user["employee_name"]

        results.append(clientcore.LegalEntityUser(
            user["user_id"], user["employee_code"], employee_name, bool(user["is_active"]),
            user["legal_entity_id"], user["user_category_id"]
        ))
    return results

def get_user_domains(db, user_id, user_category_id=None):
    condition = ""
    print user_category_id
    param = []
    if user_category_id is not None :
        if user_category_id <= 3 :
            q = "select domain_id from tbl_domains"

        else :
            q = "select domain_id from tbl_user_domains"
            condition = " WHERE user_id = %s"
            param.append(user_id)

    else :
        q = "select domain_id from tbl_user_domains"
        condition = " WHERE user_id = %s"
        param.append(user_id)

    print q
    rows = db.select_all(q + condition, param)
    print rows
    d_ids = []
    for r in rows:
        d_ids.append(int(r["domain_id"]))

    return d_ids


def is_service_provider_in_contract(db, service_provider_id):
    column = "count(1) as live"
    condition = "now() between contract_from " + \
        " and DATE_ADD(contract_to, INTERVAL 1 DAY) " + \
        " and service_provider_id = %s and is_active = 1"
    condition_val = [service_provider_id]
    rows = db.get_data(tblServiceProviders, column, condition, condition_val)
    if rows[0]["live"] > 0:
        return True
    else:
        return False


def is_in_contract(db):
    columns = "count(1) as live"
    condition = "now() between contract_from and " + \
        " DATE_ADD(contract_to, INTERVAL 1 DAY)"
    rows = db.get_data(
        tblClientGroups, columns, condition
    )
    if rows[0]["live"] <= 0:
        return False
    else:
        return True


def verify_username(db, username):
    columns = "count(0) as result, user_id"
    condition = "username=%s and is_active = 1"
    condition_val = [username]
    rows = db.get_data(
        tblUserLoginDetails, columns, condition, condition_val
    )
    count = rows[0]["result"]
    if count == 1:
        return rows[0]["user_id"]
    else:
        return None

def get_forms_by_category(db, category_id):
    q = "SELECT t1.form_id, t1.form_type_id, t1.form_name, t1.form_url, t1.form_order, t1.parent_menu, " + \
        "t2.user_category_id , t3.form_type " + \
        "FROM tbl_forms as t1 " + \
        "inner join tbl_form_category as t2 on t1.form_id = t2.form_id " + \
        "inner join tbl_form_type as t3 on t1.form_type_id = t3.form_type_id " + \
        "where user_category_id = %s order by t1.form_order"
    rows = db.select_all(q, [category_id])
    return rows

def get_user_forms(db, user_id, category_id):
    q = "SELECT t1.form_id, t1.form_type_id, t1.form_name, t1.form_url, t1.form_order, t1.parent_menu, tf.form_type " + \
        "FROM tbl_forms as t1 " + \
        "INNER JOIN tbl_form_type tf on t1.form_type_id = tf.form_type_id " + \
        "INNER JOIN tbl_user_group_forms as t2 on t1.form_id = t2.form_id " + \
        "INNER JOIN tbl_users as t3 on t2.user_group_id = t3.user_group_id " + \
        "WHERE t3.user_id = %s and t3.is_active = 1 and t3.is_disable = 0 " + \
        "UNION ALL " + \
        "SELECT t1.form_id, t1.form_type_id, t1.form_name, t1.form_url, t1.form_order, t1.parent_menu, tf.form_type " + \
        "FROM tbl_forms as t1 " + \
        "INNER JOIN tbl_form_type tf on t1.form_type_id = tf.form_type_id " + \
        "WHERE t1.form_type_id = 4 AND IF(%s = 2, t1.form_id != 32,1) AND IF(%s = 4, t1.form_id != 32,1) " + \
        "AND IF(%s = 5, t1.form_id != 32,1) AND IF(%s = 6, t1.form_id != 32,1) " + \
        "AND IF(%s = 5, t1.form_id NOT IN (37),1) " + \
        "AND IF(%s = 6, t1.form_id NOT IN (36,37,38),1) " + \
        "AND IF(%s = 2, t1.form_id NOT IN (36,37,38,39),1) " + \
        "ORDER BY form_order, form_type_id"
    # print q, user_id, category_id
    rows = db.select_all(q, [user_id,category_id,category_id,category_id,category_id,category_id,category_id,category_id])
    return rows

def get_country_info(db, user_id, user_category_id):
    if user_category_id == 1 :
        q = "SELECT t4.country_id, t4.country_name, t4.is_active FROM tbl_users AS t1 " + \
            "INNER JOIN tbl_user_units AS t2 ON t2.user_id = t1.user_id " + \
            "INNER JOIN tbl_legal_entities AS t3 ON t3.legal_entity_id = t2.legal_entity_id " + \
            "INNER JOIN tbl_countries AS t4 ON t4.country_id = t3.country_id " + \
            "GROUP BY t4.country_id"
        rows = db.select_all(q)
    else :
        q = "SELECT t4.country_id, t4.country_name, t4.is_active FROM tbl_users AS t1 " + \
            "INNER JOIN tbl_user_units AS t2 ON t2.user_id = t1.user_id " + \
            "INNER JOIN tbl_legal_entities AS t3 ON t3.legal_entity_id = t2.legal_entity_id " + \
            "INNER JOIN tbl_countries AS t4 ON t4.country_id = t3.country_id " + \
            "WHERE t1.user_id = %s GROUP BY t4.country_id"
        rows = db.select_all(q, [user_id])

    c_list = []
    for r in rows :
        c_list.append(clientcore.Country(
            r["country_id"], r["country_name"], bool(r["is_active"])
        ))
    return c_list

def get_legal_entity_info(db, user_id, user_category_id):
    if user_category_id == 1 :
        q = "SELECT t1.legal_entity_id, t1.legal_entity_name, " + \
            "t1.business_group_id, t1.country_id, t2.country_name, " + \
            "(select business_group_name from tbl_business_groups where ifnull(business_group_id,0) = t1.business_group_id) as business_group_name " + \
            "FROM tbl_legal_entities as t1 " + \
            "inner join tbl_countries t2 on t1.country_id = t2.country_id " + \
            "WHERE contract_from <= CURDATE() and contract_to >= CURDATE() and is_closed = 0 order by t2.country_name, t1.legal_entity_name"
        rows = db.select_all(q)
        # print "------------------ Admin ---------------"
    else :
        q = "SELECT distinct t1.legal_entity_id, t1.legal_entity_name, " + \
            "t1.business_group_id, t1.country_id, t3.country_name, " + \
            " (select business_group_name from tbl_business_groups where ifnull(business_group_id,0) = t1.business_group_id) as business_group_name " + \
            "from tbl_legal_entities as t1 " + \
            "inner join tbl_user_legal_entities as t2 on " + \
            "t1.legal_entity_id = t2.legal_entity_id " + \
            "inner join tbl_countries t3 on t1.country_id = t3.country_id " + \
            "where contract_from <= CURDATE() and contract_to >= CURDATE() and is_closed = 0 and t2.user_id= %s"

        rows = db.select_all(q, [user_id])
        # print "------------------ User ---------------"
    le_list = []
    for r in rows :
        le_list.append(clientcore.LegalEntityInfo(
            r["legal_entity_id"], r["legal_entity_name"], r["country_id"],
            r["business_group_id"], r["business_group_name"], r["country_name"]
        ))
    return le_list


def verify_password(db, password, user_id):
    columns = "count(0) as result"
    encrypted_password = encrypt(password)
    condition = "1"
    rows = None
    condition = "password=%s and user_id=%s"
    condition_val = [encrypted_password, user_id]
    rows = db.get_data(
        tblUserLoginDetails, columns, condition, condition_val
    )

    if(int(rows[0]["result"]) <= 0):
        return False
    else:
        return True


def get_countries(db):
    query = "SELECT distinct t1.country_id, t1.country_name, " + \
        " t1.is_active FROM tbl_countries t1 "
    rows = db.select_all(query)
    columns = ["country_id", "country_name", "is_active"]
    result = convert_to_dict(rows, columns)
    return return_countries(result)


def get_domains(db):
    query = "SELECT distinct t1.domain_id " + \
        " FROM tbl_domains t1 "

    rows = db.select_all(query)
    d_id = []
    for r in rows :
        d_id.append(r.get("domain_id"))
    return d_id


def get_le_domains(db):
    query = "SELECT distinct t1.domain_id" + \
        "  FROM tbl_legal_entity_domains t1 "
    rows = db.select_all(query)
    return rows

def is_primary_admin(db, user_id):
    column = "count(1) as result"
    condition = "user_id = %s and user_category_id in (1,2,3) and is_active = 1"
    condition_val = [user_id]
    rows = db.get_data(tblUsers, column, condition, condition_val)
    if rows[0]["result"] > 0 or user_id == 1:
        return True
    else:
        return False


def is_old_primary_admin(db, user_id):
    column = "count(1) as result"
    condition = "user_id = %s and is_primary_admin = 1 and is_active = 0"
    condition_val = [user_id]
    rows = db.get_data(tblUsers, column, condition, condition_val)
    if rows[0]["result"] > 0:
        return True
    else:
        return False


def have_compliances(db, user_id):
        column = "count(compliance_id) as compliances"
        condition = "assignee = %s and is_active = 1"
        condition_val = [user_id]
        rows = db.get_data(
            tblAssignedCompliances, column, condition, condition_val
        )
        no_of_compliances = rows[0]["compliances"]
        if no_of_compliances > 0:
            return True
        else:
            return False


def is_seating_unit(db, unit_id):
    column = "count(*) as units"
    condition = "seating_unit_id =%s"
    condition_val = [unit_id]
    rows = db.get_data(tblUsers, column, condition, condition_val)
    user_count = rows[0]["units"]
    if user_count > 0:
        return True
    else:
        return False

def get_user_category(db, user_id):
    q = "select user_category_id from tbl_users where user_id = %s"
    row = db.select_one(q, [user_id])
    if row :
        return row["user_category_id"]
    else :
        return None

def is_admin(db, user_id):
    if user_id == 0:
        return True
    else:
        columns = "count(user_id) as admin"
        condition = "(is_admin = 1 or is_primary_admin = 1) " + \
            " and user_id = %s"
        condition_val = [user_id]
        rows = db.get_data(tblUsers, columns, condition, condition_val)
        if rows[0]["admin"] > 0:
            return True
        else:
            return False


def get_user_unit_ids(db, user_id, user_category_id=None):
    if user_category_id is None:
        q = "select distinct t1.unit_id from tbl_units as t1 " + \
            "left join tbl_user_units as t2 on t1.unit_id = t2.unit_id " + \
            " where t2.user_id = %s "
        param = [user_id]
    else :
        if user_category_id > 3 :
            q = "select distinct t1.unit_id from tbl_units as t1 " + \
                "left join tbl_user_units as t2 on t1.unit_id = t2.unit_id " + \
                " where t2.user_id = %s "
            param = [user_id]
        else :
            q = "select unit_id from tbl_units "
            param = []

    rows = db.select_all(q, param)
    u_ids = []
    for r in rows:
        u_ids.append(int(r["unit_id"]))
    return u_ids


def is_two_levels_of_approval(db):
    columns = "two_levels_of_approval"
    # rows = db.get_data(tblClientGroups, columns, condition=None)
    rows = db.get_data(tblReminderSettings, columns, condition=None)
    return bool(rows[0]["two_levels_of_approval"])


def get_user_company_details(db, user_id):
    if is_primary_admin(db, user_id):
        condition = " 1 "
        condition_val = None
    else:
        condition = "  unit_id in ( " + \
            " SELECT unit_id FROM  tbl_user_units " + \
            " WHERE user_id = %s )"
        condition_val = [user_id]
    columns = [
        "unit_id", "division_id", "legal_entity_id", "business_group_id", "category_id"
    ]
    rows = db.get_data(tblUnits, columns, condition, condition_val)

    unit_ids = []
    division_ids = []
    legal_entity_ids = []
    business_group_ids = []
    category_ids =[]
    for row in rows:
        unit_ids.append(
            int(row["unit_id"])
        )
        if row["division_id"] is not None:
            if int(row["division_id"]) not in division_ids:
                division_ids.append(int(row["division_id"]))
        if int(row["legal_entity_id"]) not in legal_entity_ids:
            legal_entity_ids.append(int(row["legal_entity_id"]))
        if row["business_group_id"] is not None:
            if int(row["business_group_id"]) not in business_group_ids:
                business_group_ids.append(int(row["business_group_id"]))
        if row["category_id"] is not None:
            if int(row["category_id"]) not in category_ids:
                category_ids.append(int(row["category_id"]))
    return (
        ",".join(str(x) for x in unit_ids),
        ",".join(str(x) for x in division_ids),
        ",".join(str(x) for x in legal_entity_ids),
        ",".join(str(x) for x in business_group_ids),
        ",".join(str(x) for x in category_ids),
    )


def get_client_level_1_statutoy(db, user_id):
    query = "SELECT (case when (LEFT( " + \
            " statutory_mapping,INSTR(statutory_mapping,'>>')-1) = '') " + \
            " THEN " + \
            " statutory_mapping " + \
            " ELSE " + \
            " LEFT (statutory_mapping,INSTR(statutory_mapping,'>>')-1) " + \
            " END ) as statutory " + \
            " FROM tbl_compliances GROUP BY statutory"
    rows = db.select_all(query)
    columns = ["statutory"]
    result = convert_to_dict(rows, columns)
    return return_client_level_1_statutories(result)


def return_client_level_1_statutories(data):
    results = []
    for d in data:
        results.append(
            d["statutory"]
        )
    return results


def get_service_providers(db):
    columns = "service_provider_id, service_provider_name, is_active"
    condition = "1"
    rows = db.get_data(
        tblServiceProviders, columns, condition
    )
    return return_service_providers(rows)


def return_service_providers(service_providers):
    results = []
    for service_provider in service_providers:
        service_provider_obj = clientcore.ServiceProvider(
            service_provider["service_provider_id"],
            service_provider["service_provider_name"],
            bool(service_provider["is_active"]))
        results.append(service_provider_obj)
    return results


# def get_client_compliances(db, user_id):
#     query = " SELECT compliance_id, document_name ,compliance_task " + \
#             " FROM tbl_compliances"
#     rows = db.select_all(query)
#     columns = ["compliance_id", "document_name", "compliance_name"]
#     result = convert_to_dict(rows, columns)
#     return return_client_compliances(result)


# def return_client_compliances(data):
#     results = []
#     for d in data:
#         compliance_name = d["compliance_name"]
#         if d["document_name"] not in ["None", None, ""]:
#             compliance_name = "%s - %s" % (d["document_name"], compliance_name)
#         results.append(clientcore.ComplianceFilter(
#             d["compliance_id"], compliance_name
#         ))
#     return results

def get_client_compliances(db, user_id):
    admin_id = get_admin_id(db)
    if user_id != admin_id:
        query = "SELECT distinct t1.domain_id, t3.compliance_id, t3.compliance_task " + \
            "FROM tbl_user_domains AS t1 " + \
            "INNER JOIN tbl_domains AS t2 ON t2.domain_id = t1.domain_id " + \
            "INNER JOIN tbl_compliances AS t3 ON t3.domain_id = t1.domain_id " + \
            "where t1.user_id = %s "
        rows = db.select_all(query, [user_id])
    else:
        query = "SELECT distinct t1.domain_id, t3.compliance_id, t3.compliance_task " + \
            "FROM tbl_user_domains AS t1 " + \
            "INNER JOIN tbl_domains AS t2 ON t2.domain_id = t1.domain_id " + \
            "INNER JOIN tbl_compliances AS t3 ON t3.domain_id = t1.domain_id "
        rows = db.select_all(query)
    return return_client_compliances(rows)


def return_client_compliances(data):
    results = []
    for d in data:
        results.append(clientcore.ComplianceFilter(
            d["domain_id"], d["compliance_id"], d["compliance_task"]
        ))
    return results

def set_new_due_date(statutory_dates, repeats_type_id, compliance_id):
    due_date = None
    due_date_list = []
    date_list = []
    now = datetime.datetime.now()
    current_year = now.year
    current_month = now.month
    for date in statutory_dates:
            s_date = clientcore.StatutoryDate(
                date["statutory_date"],
                date["statutory_month"],
                date["trigger_before_days"],
                date.get("repeat_by")
            )
            date_list.append(s_date)

            s_month = date["statutory_month"]
            s_day = date["statutory_date"]
            current_date = n_date = datetime.date.today()

            if s_date.statutory_date is not None:
                try:
                    n_date = n_date.replace(day=int(s_day))
                except ValueError:
                    if n_date.month == 12:
                        days = 31
                    else:
                        days = (n_date.replace(
                                    month=n_date.month+1, day=1
                                ) - datetime.timedelta(
                                    days=1)
                                ).day
                    n_date = n_date.replace(day=days)

            if s_date.statutory_month is not None:
                if s_date.statutory_date is not None:
                    n_date = n_date.replace(day=s_day, month=int(s_month))
                else:
                    try:
                        n_date = n_date.replace(month=int(s_month))
                    except ValueError:
                        if n_date.month == 12:
                            days = 31
                        else:
                            days = (
                                n_date.replace(
                                    day=1, month=s_month+1
                                ) - datetime.timedelta(days=1)).day
                        n_date = n_date.replace(day=days, month=int(s_month))
            if current_date > n_date:
                if repeats_type_id == 2 and len(statutory_dates) == 1:
                    try:
                        n_date = n_date.replace(month=current_month+1)
                    except ValueError:
                        if n_date.month == 12:
                            days = 31
                        else:
                            days = (
                                n_date.replace(
                                    day=1, month=current_month+1,
                                    year=current_year+1
                                ) - datetime.timedelta(days=1)).day
                        try:
                            n_date = n_date.replace(
                                day=days, month=current_month+1
                            )
                        except ValueError:
                            logger.logclient(
                                "error", "set_new_due_date", n_date
                            )
                            logger.logclient("error", "set_new_due_date", days)
                            logger.logclient(
                                "error", "set_new_due_date", current_month+1
                            )

                else:
                    try:
                        n_date = n_date.replace(year=current_year+1)
                    except ValueError:
                        if n_date.month == 12:
                            days = 31
                        else:
                            days = (
                                n_date.replace(
                                    day=1, month=n_date.month+1,
                                    year=current_year+1
                                ) - datetime.timedelta(days=1)).day

                        n_date = n_date.replace(day=days, year=current_year+1)
            if s_day is None and s_month is None:
                due_date = ""
            else:
                due_date = n_date.strftime("%d-%b-%Y")
            due_date_list.append(due_date)
    return due_date, due_date_list, date_list


def convert_datetime_to_date(val):
    if type(val) == datetime.datetime:
        return val.date()
    else:
        return val


def create_datetime_summary_text(r, diff, only_hours=False, ext=None):
    summary_text = ""
    if(only_hours):
        # if(abs(r.hours) > 0 or abs(r.months) or abs(r.years) > 0):
        if(abs(r.hours) > 0):
            hours = abs(r.hours)
            if abs(r.months) > 0 or abs(r.years) > 0:
                hours = (diff.days * 24) + hours
            elif abs(r.days) > 0:
                hours = (abs(r.days) * 24) + hours
            summary_text += " %s.%s hour(s) " % (hours, abs(r.minutes))
        elif abs(r.minutes) > 0:
            summary_text += " %s minute(s) " % abs(r.minutes)

    else:
        if abs(r.years) > 0 or abs(r.months) > 0:
            days = abs(diff.days)
            if ext == "left":
                days += 1
            summary_text += " %s day(s) " % days
        elif abs(r.days) >= 0:
            days = abs(diff.days)
            if ext == "left":
                days += 1
            summary_text += " %s day(s) " % days
    return summary_text


def calculate_ageing(
    due_date, frequency_type=None, completion_date=None, duration_type=None
):
    current_time_stamp = get_date_time_in_date()
    compliance_status = "-"
    if frequency_type == "On Occurrence" or frequency_type in [5, "5"]:
        if completion_date is not None:  # Completed compliances
            r = relativedelta.relativedelta(
                convert_datetime_to_date(due_date),
                convert_datetime_to_date(completion_date)
            )
            diff = abs(due_date-completion_date)
            if r.days < 0 and r.hours < 0 and r.minutes < 0:
                compliance_status = "On Time"
            else:
                summary_text = "Delayed by "
                if duration_type in ["2", 2]:
                    r = relativedelta.relativedelta(
                        due_date, completion_date
                    )
                    compliance_status = (
                            summary_text + create_datetime_summary_text(
                                r, diff, only_hours=True, ext=summary_text
                            )
                        )
                else:
                    compliance_status = (
                        summary_text + create_datetime_summary_text(
                            r, diff, only_hours=False, ext=summary_text
                        )
                    )
                return r.days, compliance_status
        else:
            diff = abs(due_date-current_time_stamp)
            summary_text = ""
            if duration_type in ["2", 2]:
                r = relativedelta.relativedelta(
                    due_date, current_time_stamp
                )

                if r.days >= 0 and r.hours >= 0 and r.minutes >= 0:
                    compliance_status = " %s left" % (
                        create_datetime_summary_text(
                            r, diff, only_hours=True, ext="left"
                        )
                    )
                else:
                    # if overdue is below 24 hours, then time is shown
                    if r.days == 0:
                        compliance_status = " Overdue by %s" % (
                            create_datetime_summary_text(
                                r, diff, only_hours=True, ext="Overdue by"))

                    elif r.days == 0 and r.hours == 0 and r.minutes < 0:
                        compliance_status = " Overdue by %s" % (
                            create_datetime_summary_text(
                                r, diff, only_hours=True, ext="Overdue by"))

                    else:
                        compliance_status = " Overdue by %s" % (
                            create_datetime_summary_text(
                                r, diff, only_hours=False, ext="Overdue by"))

            else:
                r = relativedelta.relativedelta(
                    convert_datetime_to_date(due_date),
                    convert_datetime_to_date(current_time_stamp)
                )
                if r.days >= 0 and r.hours >= 0 and r.minutes >= 0 and r.years >=0:
                    compliance_status = " %s left" % (
                        create_datetime_summary_text(
                            r, diff, only_hours=False, ext="left"
                        )
                    )
                else:
                    compliance_status = " Overdue by %s " % (
                        create_datetime_summary_text(
                            r, diff, only_hours=False, ext="Overdue by"
                        )
                    )
            return r.days, compliance_status
    else:
        if completion_date is not None:  # Completed compliances
            compliance_status = "On Time"
            due_date = convert_datetime_to_date(due_date)
            completion_date = convert_datetime_to_date(completion_date)
            if due_date not in [None, "None", 0]:
                r = relativedelta.relativedelta(
                    due_date, completion_date
                )
                diff = abs(due_date-completion_date)
                compliance_status = (
                    "Delayed by " + create_datetime_summary_text(
                        r, diff, only_hours=False, ext="Delayed by")
                )
                return r.days, compliance_status
        else:
            if due_date not in [None, "None", 0]:
                due_date = convert_datetime_to_date(due_date)
                current_time_stamp = convert_datetime_to_date(
                    current_time_stamp)
                r = relativedelta.relativedelta(due_date, current_time_stamp)
                diff = abs(due_date-current_time_stamp)
                # compliance_status = create_datetime_summary_text(
                #     r, diff, only_hours=False, ext="left"
                # )
                if r.days < 0 or r.months < 0 or r.years < 0:
                    compliance_status = "Overdue by %s " % (
                        create_datetime_summary_text(
                            r, diff, only_hours=False, ext="Overdue by"
                        )
                    )
                else:
                    compliance_status = " %s left" % (
                        create_datetime_summary_text(
                            r, diff, only_hours=False, ext="left"
                        )
                    )
                return r.days, compliance_status
    return 0, compliance_status


def get_client_settings(db):
    query = "SELECT two_levels_of_approval " + \
        " FROM tbl_client_groups"
    row = db.select_one(query)
    if row:
        return bool(int(row[0]))


def get_admin_info(db):
    query = "SELECT email_id from tbl_users"
    row = db.select_one(query)
    return int(row[0])


def validate_compliance_due_date(db, request):
    c_ids = []
    d_id = request.domain_id
    u_ids = request.unit_ids
    for u in u_ids:
        u_id = u

    for c in request.compliances:
        c_ids.append(c.compliance_id)
        q = "SELECT compliance_id, compliance_task, " + \
            " statutory_dates, repeats_type_id from tbl_compliances " + \
            " where compliance_id = %s"
        param = [int(c.compliance_id)]
        row = db.select_one(q, param)
        if row:
            comp_id = row["compliance_id"]
            task = row["compliance_task"]

            q1 = "select t1.compliance_id, t1.unit_id, t1.domain_id, t1.statutory_date, t1.repeats_every, t1.repeats_type_id, " + \
                " (select repeat_type from tbl_compliance_repeat_type " + \
                " where repeat_type_id = t1.repeats_type_id) as repeat_type " + \
                " FROM tbl_compliance_dates as t1 WHERE t1.unit_id = %s and t1.domain_id = %s and t1.compliance_id = %s"

            if (c.frequency == 'Review' or c.frequency == 'Flexi Review') :
                nrows = db.select_all(q1, [u_id, d_id, int(c.compliance_id)])
            else :
                nrows = []

            for n in nrows :
                row["statutory_dates"] = n["statutory_date"]
                row["repeats_type_id"] = n["repeats_type_id"]

            s_dates = json.loads(row["statutory_dates"])
            repeats_type_id = row["repeats_type_id"]
            due_date, due_date_list, date_list = set_new_due_date(
                s_dates, repeats_type_id, comp_id
            )
            if c.due_date not in [None, ""] and due_date not in [None, ""]:
                t_due_date = datetime.datetime.strptime(c.due_date, "%d-%b-%Y")
                n_due_date = datetime.datetime.strptime(due_date, "%d-%b-%Y")            
                if c.validity_date is None :
                    if (n_due_date < t_due_date):
                        # Due date should be lessthen statutory date
                        return False, task
                else :
                    v_due_date = datetime.datetime.strptime(c.validity_date, "%d-%b-%Y")
                    if (t_due_date > v_due_date):
                        return False, task
    return True, None


def get_compliance_frequency(db, condition="1"):
    columns = "frequency_id, frequency"
    rows = db.get_data(
        tblComplianceFrequency, columns, condition
    )
    compliance_frequency = []
    for row in rows:
        compliance_frequency.append(
            clientcore.ComplianceFrequency(
                row["frequency_id"], row["frequency"]
                #clientcore.COMPLIANCE_FREQUENCY(row["frequency"])
                )
            )
    return compliance_frequency


def get_user_ids_by_unit_and_domain(
    db, unit_id, domain_id
):
    unit_user_rows = db.get_data(
        tblUserUnits, "user_id",
        "unit_id = %s", [unit_id]
    )
    unit_users = [
        int(unit_user["user_id"]) for unit_user in unit_user_rows
    ]

    domain_user_rows = db.get_data(
        tblUserDomains, "user_id",
        "domain_id = %s", [domain_id]
    )
    domain_users = [
        int(domain_user["user_id"]) for domain_user in domain_user_rows
    ]

    users = list(set(unit_users).intersection(domain_users))
    if len(users) > 0:
        user_ids = ",".join(str(x) for x in users)
    else:
        user_ids = None
    return user_ids
########################################################
# To get the compliances under the selected filters
# Used in - Completed Task - Current Year (Past Data)
########################################################
def get_users_by_unit_and_domain(
    db, unit_id, domain_id
):
    rows = []
    user_ids = get_user_ids_by_unit_and_domain(
        db, unit_id, domain_id
    )
    if user_ids is not None:
        columns = "user_id, employee_name, employee_code, is_active, user_category_id"
        condition = " is_active = 1 and user_id in (%s)"
        condtion_val = [user_ids]
        rows = db.get_data(
            tblUsers, columns, condition, condtion_val
        )
    return return_users(rows)


def get_all_users(db):
    columns = [
        "user_id", "employee_code", "employee_name",
        "contact_no", "email_id"
    ]
    q = "select user_id, IFNULL(employee_code, '-'), employee_name, " + \
        " IFNULL(contact_no, '--'), email_id from tbl_users"
    data = db.select_all(q)
    rows = convert_to_key_dict(data, columns)
    return rows


def get_users(db):
    columns = "user_id, employee_name, employee_code, is_active"
    condition = "1"
    rows = db.get_data(
        tblUsers, columns, condition
    )
    return return_users(rows)


def get_users_by_id(db, user_ids):
    columns = "user_id, employee_name, employee_code, is_active"
    condition = " user_id in (%s)"
    condition_val = [user_ids]
    rows = db.get_data(
        tblUsers, columns, condition, condition_val
    )
    return return_users(rows)


def return_users(users):
    results = []
    for user in users:
        if user["employee_code"] is not None:
            employee_name = "%s - %s" % (
                user["employee_code"], user["employee_name"]
            )
        else:
            employee_name = "Administrator"
        results.append(clientcore.User(
            user["user_id"], user["user_category_id"], employee_name, bool(user["is_active"])
        ))
    return results


def get_compliance_name_by_id(db, compliance_id):
    column = "document_name, compliance_task"
    condition = "compliance_id = %s"
    condition_val = [compliance_id]
    rows = db.get_data(
        tblCompliances, column, condition, condition_val
    )
    compliance_name = ""
    if rows[0]["document_name"] is not None:
        if str(rows[0]["document_name"]) == "None":
            compliance_name = rows[0]["compliance_task"]
        else:
            compliance_name += rows[0][
                    "document_name"
                ]+" - "+rows[0]["compliance_task"]
    else:
        compliance_name = rows[0]["compliance_task"]
    return compliance_name


def is_space_available(db, upload_size):
    columns = "(file_space_limit - used_file_space) as space"
    # GB to Bytes
    # columns = "((file_space_limit*1073741824) - used_file_space) as space"
    rows = db.get_data(tblLegalEntities, columns, "1")
    remaining_space = rows[0]["space"]
    if upload_size < remaining_space:
        return True
    else:
        return False

def update_used_space(db, file_size):
    columns = ["used_file_space"]
    condition = "1"
    print "file_size>>", file_size
    db.increment(
        tblLegalEntities, columns, condition, value=file_size
    )

    total_used_space = 0
    rows = db.get_data(
        tblLegalEntities, "used_file_space, legal_entity_id", "1"
    )
    legal_entity_id = rows[0]["legal_entity_id"]
    if rows[0]["used_file_space"] is not None:
        total_used_space = int(rows[0]["used_file_space"])

    # Update Knowledge Data
    UpdateFileSpace(total_used_space, legal_entity_id)


def save_compliance_activity(
    db, unit_id, compliance_id, compliance_history_id, activity_by, activity_on, action,
    remarks
):
    date = get_date_time()
    columns = [
        "unit_id", "compliance_id", "compliance_history_id", "activity_by",
        "activity_on", "action"
    ]
    values = [
        unit_id, compliance_id, compliance_history_id, activity_by,
        activity_on,  action
    ]

    if remarks:
        columns.append("remarks")
        values.append(remarks)
    result = db.insert(
       tblComplianceActivityLog, columns, values
    )
    if result is False:
        raise client_process_error("E018")


def save_compliance_notification(
    db, compliance_history_id, notification_text, category, action, notification_type_id
):
    current_time_stamp = get_date_time_in_date()

    # Get history details from compliance history id
    history_columns = [
        "unit_id", "compliance_id", "completed_by",
        "concurred_by", "approved_by"
    ]
    history_condition = "compliance_history_id = %s"
    history_condition_val = [compliance_history_id]
    print compliance_history_id
    history_rows = db.get_data(
        tblComplianceHistory, history_columns,
        history_condition, history_condition_val
    )
    print history_rows
    history = history_rows[0]
    unit_id = history["unit_id"]
    compliance_id = history["compliance_id"]

    # Getting Unit details from unit_id
    unit_columns = [
        "country_id", "business_group_id", "legal_entity_id", "division_id"
    ]
    unit_condition = "unit_id = %s"
    unit_condition_val = [int(unit_id)]
    unit_rows = db.get_data(
        tblUnits, unit_columns, unit_condition, unit_condition_val
    )
    # unit_columns_list = [
    #     "country_id", "business_group_id", "legal_entity_id", "division_id"
    # ]
    unit = unit_rows[0]  # convert_to_dict(unit_rows[0], unit_columns_list)

    # Getting compliance_details from compliance_id
    compliance_columns = "domain_id"
    compliance_condition = "compliance_id = %s "
    compliance_condition_val = [compliance_id]
    compliance_rows = db.get_data(
        tblCompliances, compliance_columns,
        compliance_condition, compliance_condition_val
    )
    domain_id = compliance_rows[0]["domain_id"]

    # Saving notification
    columns = [
        "country_id", "domain_id", "business_group_id",
        "legal_entity_id", "division_id", "unit_id", "compliance_id",
        "assignee", "concurrence_person", "approval_person",
        "notification_type_id", "notification_text", "extra_details",
        "created_on"
    ]
    extra_details = "%s-%s" % (compliance_history_id, category)
    # values = [
    #     unit["country_id"], domain_id, unit["business_group_id"],
    #     unit["legal_entity_id"], unit["division_id"], unit_id, compliance_id,
    #     history["completed_by"], history["concurred_by"],
    #     history["approved_by"], 1, notification_text, extra_details,
    #     current_time_stamp
    # ]
    values = [
        unit["country_id"], domain_id, unit["business_group_id"],
        unit["legal_entity_id"], unit["division_id"], unit_id, compliance_id,
        history["completed_by"], history["concurred_by"],
        history["approved_by"], notification_type_id, notification_text, extra_details,
        current_time_stamp
    ]
    notification_id = db.insert(tblNotificationsLog, columns, values)
    if notification_id is False:
        raise client_process_error("E019")

    # Saving in user log
    print history
    columns = ["notification_id", "read_status", "updated_on", "user_id"]
    values = [notification_id, 0, current_time_stamp]
    {u'concurred_by': 3, u'approved_by': 2, u'unit_id': 182, u'compliance_id': 216, u'completed_by': 4}

    if action.lower() == "concur":
        values.append(int(history["concurred_by"]))
    elif action.lower() == "approve":
        values.append(int(history["approved_by"]))
    elif action.lower() == "concurred":
        values.append(int(history["completed_by"]))
    elif action.lower() == "approvedtoassignee":
        values.append(int(history["completed_by"]))
    elif action.lower() == "approvedtoconcur":
        values.append(int(history["concurred_by"]))
    elif action.lower() == "concurrejected":
        values.append(int(history["completed_by"]))
    elif action.lower() == "approverejectedtoassignee":
        values.append(int(history["completed_by"]))
    elif action.lower() == "approverejectedtoconcur":
        values.append(int(history["concurred_by"]))
    elif action.lower() == "started":
        values.append(int(history["completed_by"]))
    print values
    if action.lower() == "started" :
        r1 = db.insert(
            tblNotificationUserLog, columns,
            [notification_id, 0, current_time_stamp, history["completed_by"]])
        r1 = db.insert(
            tblNotificationUserLog, columns,
            [notification_id, 0, current_time_stamp, history["concurred_by"]])
        r1 = db.insert(
            tblNotificationUserLog, columns,
            [notification_id, 0, current_time_stamp, history["approved_by"]])

    else :
        r1 = db.insert(tblNotificationUserLog, columns, values)

    if r1 is False:
        raise client_process_error("E019")
    return r1


def get_user_countries(db, user_id):
    q = "select country_id from tbl_countries"
    param = None
    condition = ""
    if is_primary_admin(db, user_id) is not True:
        q = "select country_id from tbl_user_countries"
        condition = " WHERE user_id = %s"
        param = [user_id]
    rows = db.select_all(q + condition, param)
    c_ids = []
    for r in rows:
        c_ids.append(int(r[0]))
    return c_ids


def get_email_id_for_users(db, user_id):
    q = "SELECT employee_name, email_id from tbl_users where user_id = %s"
    row = db.select_one(q, [user_id])
    if row:
        return row["employee_name"], row["email_id"]
    else:
        return None, None


def get_user_email_name(db, user_ids):
    index = None
    column = "email_id, employee_name"
    condition = "user_id in (%s)"
    condition_val = [",".join(str(x) for x in user_ids)]
    rows = db.get_data(
        tblUsers, column, condition, condition_val
    )
    email_ids = ""
    employee_name = ""
    for index, row in enumerate(rows):
        if index == 0:
            if row["employee_name"] is not None:
                employee_name += "%s" % row["employee_name"]
            email_ids += "%s" % row["email_id"]
        else:
            if row["employee_name"] is not None:
                employee_name += ", %s" % row["employee_name"]
            email_ids += ", %s" % row["email_id"]
    # if admin_email is not None:
    #     employee_name += "Administrator"
    #     email_ids += admin_email

    return email_ids, employee_name

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)


def calculate_from_and_to_date_for_domain(db, domain_id):
    # country_id
    columns = "contract_from, contract_to"
    # rows = db.get_data(tblClientGroups, columns, "1")
    rows = db.get_data(tblLegalEntities, columns, "1")
    if rows:
        contract_from = rows[0]["contract_from"]
    else:
        contract_from = None
    # contract_to = rows[0][1]

    # columns = "period_from, period_to"
    columns = "month_from, month_to"
    # condition = "country_id = %s and domain_id = %s"
    # condition_val = [country_id, domain_id]
    condition = " domain_id = %s"
    condition_val = [domain_id]
    rows = db.get_data(
        tblClientConfigurations, columns, condition, condition_val
    )
    period_from = rows[0]["month_from"]

    to_date = contract_from
    current_year = to_date.year
    previous_year = current_year-1
    from_date = datetime.date(previous_year, period_from, 1)
    r = relativedelta.relativedelta(
        convert_datetime_to_date(to_date),
        convert_datetime_to_date(from_date)
    )
    no_of_years = r.years
    no_of_months = r.months
    if no_of_years is not 0 or no_of_months >= 12:
        from_date = datetime.date(current_year, period_from, 1)
    return from_date, to_date

def get_from_and_to_date_for_domain(db, country_id, domain_id):
    from_date = None
    to_date = None
    columns = "month_from, month_to"
    condition = " country_id = %s and domain_id = %s"
    condition_val = [country_id, domain_id]
    rows = db.get_data(
        tblClientConfigurations, columns, condition, condition_val
    )
    month_from = rows[0]["month_from"]
    month_to = rows[0]["month_to"]
    now = datetime.datetime.now()
    current_year = now.year
    from_date = str(current_year) + "-" + str(month_from) + "-1"
    if month_from == 1:
        to_date = last_day_of_month(datetime.date(current_year, month_to, 1))
    else:
        to_date = last_day_of_month(datetime.date(current_year + 1, month_to, 1))
    return from_date, to_date


def calculate_due_date(
    db, domain_id, statutory_dates=None, repeat_by=None,
    repeat_every=None, due_date=None
):
    def is_future_date(test_date):
        result = False
        current_date = datetime.date.today()
        if type(test_date) == datetime.datetime:
            test_date = test_date.date()
        if ((current_date - test_date).days < 0):
            result = True
        return result
    from_date, to_date = calculate_from_and_to_date_for_domain(
        db, domain_id
    )

    # country_id
    due_dates = []
    due_dates_test = []
    summary = ""
    # For Monthly Recurring compliances
    if statutory_dates and len(json.loads(statutory_dates)) > 1:
        summary += "Every %s month(s) (" % (repeat_every)
        for statutory_date in json.loads(statutory_dates):
            date = statutory_date["statutory_date"]
            month = statutory_date["statutory_month"]
            summary += "%s %s " % (db.string_months[month], date)
            current_date = datetime.datetime.today().date()
            due_date_guess = datetime.date(current_date.year, month, date)
            real_due_date = None
            if is_future_date(due_date_guess):
                real_due_date = datetime.date(current_date.year - 1, month, date)
            else:
                real_due_date = due_date_guess
            if from_date <= real_due_date <= to_date:
                real_due_date_str = str(real_due_date)
                due_dates.append(real_due_date_str)
            else:
                continue
        summary += ")"
    elif repeat_by:
        date_details = ""
        if statutory_dates not in ["None", None, ""]:
            statutory_date_json = json.loads(statutory_dates)
            if len(statutory_date_json) > 0:
                date_details += "(%s)" % (
                    statutory_date_json[0]["statutory_date"]
                )

        # For Compliances Recurring in days
        if repeat_by == 1:  # Days
            summary = "Every %s day(s)" % (repeat_every)
            previous_year_due_date = datetime.date(
                due_date.year - 1, due_date.month, due_date.day
            )
            if from_date <= previous_year_due_date <= to_date:
                previous_year_due_date_str = str(previous_year_due_date)
                due_dates.append(previous_year_due_date_str)
            iter_due_date = previous_year_due_date
            while not is_future_date(iter_due_date):
                iter_due_date = iter_due_date + datetime.timedelta(
                    days=repeat_every
                )
                if from_date <= iter_due_date <= to_date:
                    date_str = str(iter_due_date)
                    due_dates.append(date_str)
        elif repeat_by == 2:   # Months
            summary = "Every %s month(s) %s " % (repeat_every, date_details)
            iter_due_date = due_date
            while iter_due_date > from_date:
                iter_due_date = iter_due_date + relativedelta.relativedelta(
                    months=-repeat_every
                )
                if from_date <= iter_due_date <= to_date:
                    date_str = str(iter_due_date)
                    due_dates.append(date_str)
        elif repeat_by == 3:   # Years
            summary = "Every %s year(s) %s" % (repeat_every, date_details)
            year = from_date.year
            while year <= to_date.year:
                due_date = datetime.date(
                    year, due_date.month, due_date.day
                )
                if from_date <= due_date <= to_date:
                    date_str = str(due_date)
                    due_dates.append(date_str)
                year += 1
    if len(due_dates) >= 2:
        if due_dates[0] > due_dates[1]:
            due_dates.reverse()
    return due_dates, summary


def filter_out_due_dates(db, unit_id, compliance_id, due_dates_list):
    # Checking same due date already exists
    if due_dates_list is not None and len(due_dates_list) > 0:
        formated_date_list = []
        for x in due_dates_list:
            x = str(x)
            x.replace(" ", "")
            formated_date_list.append("%s" % (x))

        query = " SELECT is_ok FROM " + \
            " (SELECT (CASE WHEN (unit_id = %s " + \
            " AND find_in_set(DATE(due_date), %s) " + \
            " AND compliance_id = %s) THEN DATE(due_date) " + \
            " ELSE 'NotExists' END ) as " + \
            " is_ok FROM tbl_compliance_history ) a WHERE is_ok != 'NotExists'"
        rows = db.select_all(
            query, [unit_id,
                ",".join([x for x in due_dates_list]),
                compliance_id
            ]
        )
        rows_copy = []
        if len(rows) > 0:
            for row in rows:
                rows_copy.append("%s" % (x))

            filtered_list = [x for x in formated_date_list if x not in set(rows_copy)]
            formated_date_list = filtered_list

        result_due_date = []
        for current_due_date_index, due_date in enumerate(formated_date_list):
            next_due_date = None

            if len(due_dates_list) < current_due_date_index + 1:
                continue
            else:
                if current_due_date_index == len(formated_date_list)-1:
                    next_due_date = due_dates_list[current_due_date_index]
                else:
                    next_due_date = due_dates_list[current_due_date_index+1]

                columns = "count(*) as compliance"
                condition = "unit_id = %s AND due_date <= %s " + \
                    " AND compliance_id = %s AND " + \
                    " approve_status = 1 and validity_date >= %s "

                condition_val = [
                    unit_id, due_date, compliance_id, next_due_date
                ]
                rows = db.get_data(
                    tblComplianceHistory, columns, condition, condition_val
                )
                if rows[0]["compliance"] > 0:
                    continue
                else:
                    result_due_date.append(due_date)
        return result_due_date
    else:
        return []


def convert_base64_to_file(file_name, file_content, client_id):
    client_directory = "%s/%s" % (CLIENT_DOCS_BASE_PATH, client_id)
    file_path = "%s/%s" % (client_directory, file_name)
    if not os.path.exists(client_directory):
        os.makedirs(client_directory)
    remove_uploaded_file(file_path)
    if file_content is not None:
        with io.FileIO(file_path, "wb") as fn:
            fn.write(file_content.decode('base64'))


def get_user_name_by_id(db, user_id):
    employee_name = None
    if user_id is None:
        return ""
    if user_id is not None and user_id != 0:
        columns = "employee_code, employee_name"
        condition = "user_id = %s "
        condition_val = [user_id]
        rows = db.get_data(
            tblUsers, columns, condition, condition_val
        )
        if len(rows) > 0:
            emp_code = ""
            if(rows[0]["employee_code"] is not None):
                emp_code = rows[0]["employee_code"] + " - "
            employee_name = "%s %s" % (
                emp_code, rows[0]["employee_name"]
            )
        if user_id == is_primary_admin(db, user_id):
            employee_name += " (Client Admin)"
    else:
        employee_name = "Administrator"
    return employee_name


def get_form_ids_for_admin(db):
    columns = ["form_id"]
    condition = " is_admin = 1 OR form_type_id in (4,5) " + \
        " OR form_id in (1, 9,11,10,12)"
    rows = db.get_data(
        tblForms, columns, condition
    )
    form_ids = [
        row["form_id"] for row in rows
    ]
    return ",".join(str(x) for x in form_ids)


def get_report_form_ids(db):
    columns = ["form_id"]
    condition = " form_type_id = 3"
    rows = db.get_data(
        tblForms, columns, condition
    )
    form_ids = [
        row["form_id"] for row in rows
    ]
    return ",".join(str(x) for x in form_ids)


def get_client_id_from_short_name(db, short_name):
    columns = "client_id"
    condition = "url_short_name = %s"
    condition_val = [short_name]
    rows = db.get_data(
        "tbl_client_groups", columns, condition, condition_val
    )
    return rows[0]["client_id"]


def validate_reset_token(db, reset_token):
    q = "select t1.user_id from tbl_email_verification t1 inner join tbl_users t2 on t1.user_id = t2.user_id " + \
        "where t2.is_active = 1 and t1.verification_code = %s "
    rows = db.select_all(q, [reset_token])
    if rows :
        return int(rows[0]["user_id"])
    else :
        return None

def update_password(db, password, user_id):
    columns = ["password"]
    values = [encrypt(password)]
    condition = "1"
    result = False
    condition = " user_id=%s"
    values.append(user_id)
    result = db.update(
        tblUserLoginDetails, columns, values, condition
    )
    columns = "employee_code, employee_name"
    condition = "user_id = %s"
    condition_val = [user_id]
    rows = db.get_data(tblUsers, columns, condition, condition_val)
    employee_name = rows[0]["employee_name"]
    if rows[0]["employee_code"] is not None:
        employee_name = "%s - %s" % (
            rows[0]["employee_code"], rows[0]["employee_name"]
        )
    else:
        employee_name = rows[0]["employee_name"]

    action = "\"%s\" has updated his/her password" % (employee_name)
    db.save_activity(user_id, 31, action)

    if result:
        return True
    else:
        return False


def delete_used_token(db, reset_token):
    condition = " verification_code=%s"
    condition_val = [reset_token]
    if db.delete(tblEmailVerification, condition, condition_val):
        return True
    else:
        return False


def remove_session(db, session_token, ip):
    condition = "session_token = %s"
    condition_val = [session_token]
    q = "select t1.user_id, t1.employee_code, employee_name from tbl_users as t1 " + \
        " inner join tbl_user_sessions as t2 on t1.user_id = t2.user_id where t2.session_token = %s"
    row = db.select_one(q, [session_token])
    if row :
        user_id = row.get("user_id")
        ecode = row.get("employee_code")
        ename = row.get("employee_name")
        if ecode is not None :
            ename = "%s - %s" % (ecode, ename)
        if ename is not None :
            action = "Logout by - \"%s\" from \"%s\"" % (ename, ip)
            db.save_activity(user_id, 0, action)

    if db.delete(tblUserSessions, condition, condition_val):
        return True
    else:
        return False


def update_profile(db, contact_no, address, session_user):
    columns = ["contact_no", "address"]
    values = [contact_no, address, session_user]
    condition = "user_id= %s"
    db.update(tblUsers, columns, values, condition)


def is_service_proivder_user(db, user_id):
    column = "count(1) as result"
    condition = "user_id = %s and is_service_provider = 1"
    condition_val = [user_id]
    rows = db.get_data(tblUsers, column, condition, condition_val)
    if rows[0]["result"] > 0:
        return True
    else:
        return False


def get_trail_id(db, types=None):
    if types is None:
        query = "select IFNULL(audit_trail_id, 0) as audit_trail_id " + \
            " from tbl_audit_log;"
    else:
        query = "select IFNULL(domain_trail_id, 0) as audit_trail_id " + \
            " from tbl_audit_log;"
    row = db.select_one(query)
    print row

    trail_id = row.get("audit_trail_id")
    return trail_id


def update_traild_id(db, audit_trail_id, get_type=None):
    if get_type is None:
        query = "UPDATE tbl_audit_log SET audit_trail_id=%s;" % (
            audit_trail_id
        )
    else:
        query = "UPDATE tbl_audit_log SET domain_trail_id=%s;" % (
            audit_trail_id
        )
    db.execute(query)


def reset_domain_trail_id(db):
    q = "update tbl_audit_log set domain_trail_id=0"
    db.execute(q)

def get_users_forms(db, user_id, user_category):
    if user_category == 1 :
        q = "select form_id from tbl_form_category where user_category_id = 1"
        param = []
    else :
        q = "select t1.form_id from tbl_user_group_forms as t1 " + \
            " inner join tbl_users as t2  " + \
            " on t1.user_group_id = t2.user_group_id " + \
            " where t2.user_id = %s"
        param = [user_id]

    rows = db.select_all(q, param)
    f_ids = []
    for r in rows :
        f_ids.append(int(r["form_id"]))
    return f_ids

def get_widget_rights(db, user_id, user_category):
    forms = get_users_forms(db, user_id, user_category)
    print forms
    showDashboard = False
    showCalendar = False
    showUserScore = False
    showDomainScore = False
    if 34 in forms :
        showDashboard = True

    if 35 in forms :
        showCalendar = True

    if 18 in forms :
        showDomainScore = True

    if 20 in forms :
        showUserScore = True

    return showDashboard, showCalendar, showUserScore, showDomainScore

def get_user_widget_settings(db, user_id, user_category):
    q = "select form_id, form_name from tbl_widget_forms order by form_id"
    rows = db.select_all(q, [])
    print rows
    showDashboard, showCalendar, showUserScore, showDomainScore = get_widget_rights(db, user_id, user_category)

    widget_list = []
    for r in rows :
        if showDashboard is True and int(r["form_id"]) in [1, 2, 3, 4, 5] :
            widget_list.append(r)
        elif showUserScore is True and int(r["form_id"]) == 6 :
            widget_list.append(r)
        elif showDomainScore is True and int(r["form_id"]) == 7 :
            widget_list.append(r)
        elif showCalendar is True and int(r["form_id"]) == 8 :
            widget_list.append(r)

    q = "select user_id, widget_data from tbl_widget_settings where user_id = %s"
    rows = db.select_one(q, [user_id])
    if rows :
        rows = json.loads(rows["widget_data"])
    else :
        rows = []

    data = rows
    rm_index = []
    if len(rows) > 0 :

        for i, d in enumerate(rows) :
            w_id = int(d["w_id"])
            if showDashboard is False and w_id in [1, 2, 3, 4, 5]:
                rm_index.append(i)

            elif showUserScore is False and w_id == 6 :
                rm_index.append(i)

            elif showCalendar is False and w_id == 8 :
                rm_index.append(i)

            elif showDomainScore is False and w_id == 7 :
                rm_index.append(i)

    for r in reversed(rm_index) :
        data.pop(r)

    return widget_list, data


def save_user_widget_settings(db, user_id, widget_data):
    q = "insert into tbl_widget_settings(user_id, widget_data) values (%s, %s) on duplicate key update widget_data = values(widget_data)"
    db.execute(q, [user_id, widget_data])

def get_themes(db, user_id):
    q = "select theme_name from tbl_themes where user_id = %s"
    rows = db.select_one(q, [user_id])
    if not rows:
        return None
    else:
        return rows['theme_name']

def get_themes_for_user(db, user_id):
    q = "select theme_id from tbl_themes where user_id = %s"
    rows = db.select_one(q, [user_id])
    if not rows:
        return None
    else:
        return rows['theme_id']

def save_themes_for_user(db, session_user, theme_name):
    current_time_stamp = get_date_time_in_date()
    columns = ["theme_name", "user_id", "created_on"]
    values = [theme_name, session_user, current_time_stamp]
    db.insert(tblThemes, columns, values)
    return theme_name
    # q = "insert into tbl_widget_settings(user_id, widget_data) values (%s, %s) on duplicate key update widget_data = values(widget_data)"
    # db.execute(q, [user_id, widget_data])

def update_themes_for_user(db, session_user, theme_id, theme_name):
    current_time_stamp = get_date_time_in_date()
    columns = ["theme_name", "updated_on"]
    values = [theme_name, current_time_stamp]
    condition = " user_id = %s " % session_user
    db.update(tblThemes, columns, values, condition)
    return theme_name

def legal_entity_logo_url(db, legal_entity_id):
    q = "select logo from tbl_legal_entities where legal_entity_id = %s"
    rows = db.select_one(q, [legal_entity_id])
    if rows['logo']:
        logo_url = "%s/%s" % (CLIENT_LOGO_PATH, rows['logo'])
    else:
        logo_url = None
    return logo_url

def verify_username_forgotpassword(db, username):
    # columns = "user_id, email_id, "
    # condition = "username=%s and is_active = 1"
    # condition_val = [username]
    # rows = db.get_data(
    #     tblUserLoginDetails, columns, condition, condition_val
    # )
    # count = rows[0]["result"]
    # if count == 1:
    #     return rows[0]["user_id"]
    # else:
    #     return None

    #     u.user_id, u.email_id, us.employee_name
    q = "select u.user_id, u.username, us.email_id, us.employee_name " + \
        "FROM tbl_user_login_details u " + \
        "inner join  tbl_users us on u.user_id = us.user_id " + \
        "where u.username = %s "
    rows = db.select_one(q, [username])
    if rows:
        return rows
    else:
        return None

def update_task_status_in_chart(db, country_id, domain_id, unit_id, due_date, users):
    year = due_date.year
    q1 = "select month_from, month_to from tbl_client_configuration where country_id = %s and domain_id = %s"
    dat_conf = db.select_all(q1, [country_id, domain_id])

    q = "insert into tbl_compliance_status_chart_unitwise( " + \
        "     legal_entity_id, country_id, domain_id, unit_id,  " + \
        "     month_from, month_to, chart_year, complied_count, delayed_count, inprogress_count, overdue_count " + \
        " ) " + \
        " select unt.legal_entity_id, ccf.country_id,ccf.domain_id, " + \
        " ch.unit_id,ccf.month_from,ccf.month_to, %s, " + \
        " sum(IF(IF(ifnull(com.duration_type_id,0) = 2, ch.due_date >= ch.completion_date, date(ch.due_date) >= date(ch.completion_date)) " + \
        " and ifnull(ch.approve_status,0) = 1, 1, 0)) as complied_count, " + \
        " sum(IF(IF(ifnull(com.duration_type_id,0) = 2, ch.due_date < ch.completion_date, date(ch.due_date) < date(ch.completion_date)) and " + \
        " ifnull(ch.approve_status,0) = 1, 1, 0)) as delayed_count, " + \
        " sum(IF(IF(ifnull(com.duration_type_id,0) = 2, ch.due_date >= now(), date(ch.due_date) >= curdate()) and ifnull(ch.approve_status, 0) <> 1  " + \
        " and ifnull(ch.approve_status,0) <> 3, 1, 0)) as inprogress_count, " + \
        " sum(IF((IF(ifnull(com.duration_type_id,0) = 2, ch.due_date < now(), ch.due_date < curdate())  " + \
        " and ifnull(ch.approve_status,0) <> 1) or ifnull(ch.approve_status,0) = 3, 1, 0)) as overdue_count " + \
        " from tbl_client_configuration as ccf " + \
        " inner join tbl_units as unt on ccf.country_id = unt.country_id and ccf.client_id = unt.client_id and unt.is_closed = 0 " + \
        " inner join tbl_client_compliances as cc on unt.unit_id = cc.unit_id and ccf.domain_id = cc.domain_id  " + \
        " inner join tbl_compliances as com on cc.compliance_id = com.compliance_id and ccf.domain_id = com.domain_id " + \
        " left join tbl_compliance_history as ch on ch.unit_id = cc.unit_id and ch.compliance_id = cc.compliance_id " + \
        " where ch.due_date >= date(concat_ws('-',%s,ccf.month_from,1))  " + \
        " and ch.due_date <= last_day(date(concat_ws('-',%s,ccf.month_to,1))) " + \
        " and ccf.country_id = %s and ccf.domain_id = %s and unt.unit_id = %s " + \
        " group by ccf.country_id,ccf.domain_id,ccf.month_from,ccf.month_to,ch.unit_id " + \
        " on duplicate key update complied_count = values(complied_count), " + \
        " delayed_count = values(delayed_count), inprogress_count = values(inprogress_count), " + \
        " overdue_count = values(overdue_count) "

    q1 = "insert into tbl_compliance_status_chart_userwise( " + \
        "     legal_entity_id, country_id, domain_id, unit_id, user_id, " + \
        "     month_from, month_to, chart_year, complied_count, delayed_count, inprogress_count, overdue_count " + \
        " ) " + \
        " select unt.legal_entity_id, ccf.country_id,ccf.domain_id, ch.unit_id, usr.user_id, " + \
        " ccf.month_from,ccf.month_to,%s, " + \
        " sum(IF(IF(ifnull(com.duration_type_id,0) = 2, ch.due_date >= ch.completion_date, date(ch.due_date) >= date(ch.completion_date)) " + \
        " and ifnull(ch.approve_status,0) = 1, 1, 0)) as complied_count, " + \
        " sum(IF(IF(ifnull(com.duration_type_id,0) = 2, ch.due_date < ch.completion_date, date(ch.due_date) < date(ch.completion_date)) and " + \
        " ifnull(ch.approve_status,0) = 1, 1, 0)) as delayed_count, " + \
        " sum(IF(IF(ifnull(com.duration_type_id,0) = 2, ch.due_date >= now(), date(ch.due_date) >= curdate()) and ifnull(ch.approve_status, 0) <> 1  " + \
        " and ifnull(ch.approve_status,0) <> 3, 1, 0)) as inprogress_count, " + \
        " sum(IF((IF(ifnull(com.duration_type_id,0) = 2, ch.due_date < now(), ch.due_date < curdate())  " + \
        " and ifnull(ch.approve_status,0) <> 1) or ifnull(ch.approve_status,0) = 3, 1, 0)) as overdue_count " + \
        " from tbl_client_configuration as ccf " + \
        " inner join tbl_units as unt on ccf.country_id = unt.country_id and ccf.client_id = unt.client_id and unt.is_closed = 0 " + \
        " inner join tbl_client_compliances as cc on unt.unit_id = cc.unit_id and ccf.domain_id = cc.domain_id " + \
        " inner join tbl_compliances as com on cc.compliance_id = com.compliance_id " + \
        " left join tbl_compliance_history as ch on ch.unit_id = cc.unit_id and ch.compliance_id = cc.compliance_id " + \
        " inner join tbl_users as usr on usr.user_id = ch.completed_by OR usr.user_id = ch.concurred_by OR usr.user_id = ch.approved_by " + \
        " where ch.due_date >= date(concat_ws('-',%s,ccf.month_from,1))  " + \
        " and ch.due_date <= last_day(date(concat_ws('-',%s,ccf.month_to,1))) " + \
        " and ccf.country_id = %s and ccf.domain_id = %s and unt.unit_id = %s " + \
        " and find_in_set(usr.user_id, %s) " + \
        " group by ccf.country_id,ccf.domain_id, ch.unit_id, ccf.month_from,ccf.month_to,usr.user_id " + \
        " on duplicate key update complied_count = values(complied_count), " + \
        " delayed_count = values(delayed_count), inprogress_count = values(inprogress_count), " + \
        " overdue_count = values(overdue_count) "

    for d in dat_conf :
        from_year = year
        if d["month_from"] == 1 and d["month_to"] == 12 :
            to_year = year
        else :
            to_year = year+1
        db.execute(q, [year, from_year, to_year, country_id, domain_id, unit_id])
        db.execute(q1, [year, from_year, to_year, country_id, domain_id, unit_id, ",".join([str(x) for x in users])])

def get_unit_name_by_id(db, unit_id):
    unit_name = None
    columns = "unit_code, unit_name"
    condition = "unit_id = %s "
    condition_val = [unit_id]
    rows = db.get_data(
        tblUnits, columns, condition, condition_val
    )
    if len(rows) > 0:
        unit_code = ""
        if(rows[0]["unit_code"] is not None):
            unit_code = rows[0]["unit_code"]
        unit_name = "%s - %s" % (
            unit_code, rows[0]["unit_name"]
        )
    return unit_name

def get_legalentity_admin_ids(db, legal_entity_id):
    q = "select t1.user_id from tbl_user_legal_entities as t1 inner join " + \
        "tbl_users as t2 on t2.user_id = t1.user_id and t2.is_active = 1 and t2.user_category_id = 3 where " + \
        "t1.legal_entity_id = %s"
    rows = db.select_all(q, [legal_entity_id])
    u_ids = []
    for r in rows :
        u_ids.append(int(r["user_id"]))
    return u_ids

def get_domain_admin_ids(db, legal_entity_id, domain_id):
    q = "select t1.user_id from tbl_user_domains as t1 inner join " + \
        "tbl_users as t2 on t2.user_id = t1.user_id and t2.is_active = 1 and t2.user_category_id = 4 where " + \
        "t1.legal_entity_id = %s and t1.domain_id = %s"
    rows = db.select_all(q, [legal_entity_id, domain_id])
    u_ids = []
    for r in rows :
        u_ids.append(int(r["user_id"]))
    return u_ids
