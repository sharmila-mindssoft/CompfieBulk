import json
from protocol import (technoreports, core, knowledgereport)
from server.database.tables import *
from server.constants import (
    KNOWLEDGE_FORMAT_DOWNLOAD_URL
)
from server.common import (
    convert_to_dict, string_to_datetime, datetime_to_string
)
from server.database.knowledgemaster import (
    GEOGRAPHY_PARENTS,
    get_geographies
)
from server.database.technotransaction import (
    return_assigned_compliances_by_id
)


def get_group_companies_for_statutorysetting_report(db, user_id):
    result = []
    print "inside group company"
    print user_id
    result = db.call_proc_with_multiresult_set(
        "sp_statutory_setting_report_clientdetails", (user_id,), 2)
    print result[1]
    return return_group_companies(db, result[1])


def return_group_companies(db, client_groups):
    results = []
    for client in client_groups:
        results.append(
            technoreports.ClientGroup(
                client["country_id"], client["client_id"], client["short_name"],
                bool(client["is_active"])
            )
        )
    return results

def get_business_groups_for_statutorysetting_report(db, user_id):
    result = []
    result = db.call_proc_with_multiresult_set(
        "sp_statutory_setting_report_businessgroupdetails", (user_id,), 2)
    return return_business_groups(db, result[1])

def return_business_groups(db, business_group):
    results = []
    for bg_grp in business_group:
        results.append(
            technoreports.ClientBusinessGroup(
                bg_grp["client_id"], bg_grp["legal_entity_id"], bg_grp["legal_entity_name"],
                bg_grp["business_group_id"], bg_grp["business_group_name"]
            )
        )
    return results

def get_units_for_statutorysetting_report(db, user_id):
    result = []
    result = db.call_proc_with_multiresult_set(
        "sp_statutory_setting_report_unitdetails", (user_id,), 2)
    return return_compliance_units(db, result[1])

def return_compliance_units(db, units_list):
    results = []
    for unit in units_list:
        results.append(
            technoreports.ComplianceUnits(
                unit["client_id"], unit["legal_entity_id"], unit["unit_id"],
                unit["unit_code"], unit["unit_name"]
            )
        )
    return results

def get_compliance_statutoy_for_statutorysetting_report(db, user_id):
    result = []
    result = db.call_proc_with_multiresult_set(
        "sp_statutory_setting_report_domains_compliances", (user_id,), 2)
    return return_compliance_statutory(db, result[1])

def return_compliance_statutory(db, stat_compl_list):
    results = []
    for st_cmp in stat_compl_list:
        results.append(
            technoreports.ComplianceStatutory(
                st_cmp["client_id"], st_cmp["legal_entity_id"], st_cmp["unit_id"],
                st_cmp["domain_id"], st_cmp["statutory_id"], st_cmp["compliance_id"],
                st_cmp["c_task"], st_cmp["document_name"], st_cmp["statutory_name"]
            )
        )
    return results

######################################################################################
# To Get client units under user
# Parameter(s) : Object of database, user id
# Return Type : Return list of client units
######################################################################################
def get_units_for_clientdetails_report(db, session_user):
    result = db.call_proc_with_multiresult_set("sp_client_details_report_unitlist", (int(session_user),), 3)
    return return_unit_details(result)

######################################################################################
# To convert db data to list
# Parameter(s) : result set from db
# Return Type : Return list of client units as list
######################################################################################
def return_unit_details(result):
    unitdetails = []
    print "inside unit details"
    print result
    for r in result[1]:
        print r
        country_id = int(r.get("country_id"))
        client_id = int(r.get("client_id"))
        legal_entity_id = int(r.get("legal_entity_id"))
        business_group_id = r.get("business_group_id")
        unit_id = int(r.get("unit_id"))
        unit_code = r.get("unit_code")
        unit_name = r.get("unit_name")
        address = r.get("address")
        postal_code = r.get("postal_code")
        is_active = bool(r.get("is_active"))
        closed_on = r.get("closed_on")
        check_date = r.get("check_date")
        emp_code_name = r.get("emp_code_name")
        created_on = r.get("created_on")
        division_name = r.get("division_name")
        category_name = r.get("category_name")
        d_ids = []
        i_ids = []
        for domain in result[2]:
            if unit_id == domain.get("unit_id"):
                d_ids.append(int(domain.get("domain_id")))
                i_ids.append(int(domain.get("organisation_id")))
        unitdetails.append(technoreports.ClientUnitDetailsReport(
            country_id, client_id, legal_entity_id, business_group_id,
            unit_id, unit_code, unit_name, address, postal_code, is_active,
            closed_on, check_date, emp_code_name, created_on, division_name,
            category_name, d_ids, i_ids
        ))
    print "unitdetails"
    print unitdetails
    return unitdetails

######################################################################################
# To Get assigned statutories
# Parameter(s) : Object of database, user id, requests
# Return Type : Return list of assigned statutories for report
######################################################################################
def get_assigned_statutories_report_data(db, request_data, user_id):
    country_id = request_data.country_id
    group_id = request_data.group_id
    business_group_id = request_data.business_group_id
    legal_entity_id = request_data.legal_entity_id
    unit_id = request_data.unit_id
    domain_id = request_data.domain_id_optional
    statutory_id = request_data.statutory_id
    compliance_id = request_data.compliance_id
    param_list = [country_id, domain_id, business_group_id, legal_entity_id, unit_id, group_id, statutory_id, compliance_id]
    result = db.call_proc_with_multiresult_set("sp_statutory_setting_report_recordset", param_list, 3)
    return return_assigned_statutories_report_data(db, result)

######################################################################################
# To convert DB recordset to list
# Parameter(s) : DB Resultset
# Return Type : Return list of assigned statutories
######################################################################################
def return_assigned_statutories_report_data(db, result):
    unit_grp = []
    act_grp = []
    stat_compl_list = []
    for r in result[0]:
        unit_grp.append(technoreports.StatutorySettingUnitGroup(
            int(r.get("unit_id")), r.get("unit_code"), r.get("unit_name"),
            r.get("address")
        ))
    for r in result[1]:
        act_grp.append(technoreports.StatutorySettingActGroup(
            int(r.get("unit_id")), int(r.get("statutory_id")), r.get("statutory_name")
        ))
    for r in result[2]:
        stat_compl_list.append(technoreports.StatutorySettingCompliances(
            int(r.get("unit_id")), int(r.get("statutory_id")), r.get("statutory_provision"),
            r.get("c_task"), r.get("document_name"), r.get("remarks"),
            r.get("statutory_applicability_status"), r.get("statutory_opted_status"),
            r.get("compfie_admin"), r.get("admin_update"), r.get("client_admin"),
            r.get("client_update"), r.get("statutory_nature_name")
        ))
    print "inside grouping"
    print unit_grp
    return (unit_grp, act_grp, stat_compl_list)





# old code starts for statutory setting report--------------------------------------------

def get_assigned_statutories_report(db, request_data, user_id):
    country_id = request_data.country_id
    domain_id = request_data.domain_id
    group_id = request_data.group_id
    qry = ""
    param_list = [country_id, domain_id]

    is_user_has_client = False
    if group_id is not None:
        qry += " AND t1.client_id = %s "
        param_list.append(group_id)
        is_user_has_client = True
    else:
        user_client_columns = ["client_id"]
        user_client_condition = "user_id = %s"
        user_client_condition_params = [user_id]
        user_client_rows = db.get_data(
                tblUserClients, user_client_columns,
                user_client_condition,
                user_client_condition_params
            )
        client_ids = []
        for client in user_client_rows:
            client_ids.append(client["client_id"])
        if len(client_ids) <= 0:
            is_user_has_client = False
        elif len(client_ids) == 1:
            qry += " AND t1.client_id = %s "
            param_list.append(client_ids[0])
            is_user_has_client = True
        else:
            qry += " AND t1.client_id in %s "
            param_list.append(tuple(client_ids))
            is_user_has_client = True

    if is_user_has_client:


        if business_group_id is not None:
            qry += " AND t3.business_group_id = %s "
            param_list.append(business_group_id)

        legal_entity_id = request_data.legal_entity_id
        if legal_entity_id is not None:
            qry += " AND t3.legal_entity_id = %s "
            param_list.append(legal_entity_id)

        division_id = request_data.division_id
        if division_id is not None:
            qry += " AND t3.division_id =%s "
            param_list.append(division_id)

        unit_id = request_data.unit_id
        if unit_id is not None:
            qry += " AND t3.unit_id = %s "
            param_list.append(unit_id)

        level_1_statutory_id = request_data.level_1_statutory_id
        if level_1_statutory_id is not None:
            qry += " AND t4.statutory_id = %s "
            param_list.append(level_1_statutory_id)

        applicable_status = request_data.applicability_status
        if applicable_status is not None:
            applicable_status = int(applicable_status)
            qry += " AND t4.compliance_applicable = %s "
            param_list.append(applicable_status)

        query = "SELECT distinct t1.client_statutory_id, t1.client_id, " + \
            " t1.geography_id, t1.country_id, t1.domain_id, t1.unit_id, " + \
            " t1.submission_type, t2.group_name, t3.unit_name, " + \
            " (select business_group_name from tbl_business_groups " + \
            "  where business_group_id " + \
            " = t3.business_group_id ) business_group_name," + \
            " (select legal_entity_name from tbl_legal_entities " + \
            " where legal_entity_id = t3.legal_entity_id) " + \
            " legal_entity_name, " + \
            " (select division_name from tbl_divisions " + \
            " where division_id = t3.division_id)division_name, " + \
            " t3.address, t3.postal_code, t3.unit_code " + \
            " FROM tbl_client_statutories t1 " + \
            " INNER JOIN tbl_client_groups t2 " + \
            " ON t1.client_id = t2.client_id " + \
            " INNER JOIN tbl_units t3 " + \
            " ON t1.unit_id = t3.unit_id " + \
            " INNER JOIN tbl_client_compliances t4 " + \
            " ON t1.client_statutory_id = t4.client_statutory_id " + \
            " WHERE t1.submission_type =1 " + \
            " AND t1.country_id = %s " + \
            " AND t1.domain_id = %s "

        query = query + qry
        rows = db.select_all(query, param_list)
        columns = [
            "client_statutory_id", "client_id", "geography_id",
            "country_id", "domain_id", "unit_id", "submission_type",
            "group_name", "unit_name",
            "business_group_name", "legal_entity_name",
            "division_name", "address", "postal_code", "unit_code"
        ]
        result = convert_to_dict(rows, columns)
        return return_assigned_statutory_report(
            db, result, level_1_statutory_id, applicable_status
        )
    else:
        return technoreports.GetAssignedStatutoryReportSuccess(
            []
        )


def return_assigned_statutory_report(
    db, report_data, level_1_statutory_id, applicable_status
):
    if bool(GEOGRAPHY_PARENTS) is False:
        get_geographies(db)

    unit_wise_statutories_dict = {}
    for data in report_data:
        client_statutory_id = data["client_statutory_id"]
        unit_id = int(data["unit_id"])
        unit_statutories = unit_wise_statutories_dict.get(unit_id)
        if unit_statutories is None:
            geography_id = int(data["geography_id"])
            geography_parents = GEOGRAPHY_PARENTS.get(geography_id)
            temp_parents = geography_parents[0].split(">>")
            ordered = temp_parents[::-1]
            unit_name = "%s - %s" % (data["unit_code"], data["unit_name"])
            unit_address = "%s, %s, %s" % (
                data["address"], ', '.join(ordered), data["postal_code"]
            )
            statutories = return_assigned_compliances_by_id(
                db, client_statutory_id, level_1_statutory_id,
                applicable_status
            )
            print '*' * 50
            unit_statutories = technoreports.UNIT_WISE_ASSIGNED_STATUTORIES(
                data["unit_id"],
                unit_name,
                data["group_name"],
                data["business_group_name"],
                data["legal_entity_name"],
                data["division_name"],
                unit_address,
                statutories
            )
        else:
            statutories = unit_statutories.assigned_statutories
            new_stautory = return_assigned_compliances_by_id(
                db, client_statutory_id, None, applicable_status
            )
            print '*' * 50
            for new_s in new_stautory:
                new_id = new_s.level_1_statutory_id
                is_exists = False
                for x in statutories:
                    if x.level_1_statutory_id == new_id:
                        x.compliances.extend(new_s.compliances)
                        is_exists = True
                        break
                if is_exists is False:
                    statutories.append(new_s)
            unit_statutories.assigned_statutories = statutories

        unit_wise_statutories_dict[unit_id] = unit_statutories

    final_unit_wise_statutories_list = []
    for key, value in unit_wise_statutories_dict.iteritems():
        final_unit_wise_statutories_list.append(value)

    return technoreports.GetAssignedStatutoryReportSuccess(
        final_unit_wise_statutories_list
    )
# old code ends for statutory setting report--------------------------------------------

def get_domainwise_agreement_report(db, country_id, client_id, business_group_id,
    legal_entity_id, domain_id, contract_from, contract_to,
    from_count, page_count, session_user):

    if contract_from is not None:
        contract_from = string_to_datetime(contract_from).date()
    if contract_to is not None:
        contract_to = string_to_datetime(contract_to).date()

    domainwise_agreement_list = db.call_proc(
        "sp_domainwise_agreement_details", (country_id, client_id, business_group_id,
    legal_entity_id, domain_id, contract_from, contract_to, from_count, page_count, session_user)
    )

    domainwise_agreement_list = return_domainwise_agreement_report(
        domainwise_agreement_list
    )

    return (
        domainwise_agreement_list
    )

def return_domainwise_agreement_report(domainwise_agreement_list):
    results = []
    for client_agreement in domainwise_agreement_list:
        le_admin_contactno = 'Not Available'
        if client_agreement["le_admin_contactno"] is not None:
            le_admin_contactno = client_agreement["le_admin_contactno"]

        le_admin_email = 'Not Available'
        if client_agreement["le_admin_email"] is not None:
            le_admin_email = client_agreement["le_admin_email"]
        results.append(
            technoreports.DomainwiseAgreementList(
                legal_entity_id = int(client_agreement["legal_entity_id"]),
                domain_id = int(client_agreement["domain_id"]),
                legal_entity_name = client_agreement["legal_entity_name"],
                contract_from = datetime_to_string(client_agreement["contract_from"]),
                contract_to = datetime_to_string(client_agreement["contract_to"]),
                group_name=client_agreement["group_name"],
                group_admin_email=client_agreement["groupadmin_email"],
                domain_total_unit=int(client_agreement["domain_total_unit"]),
                activation_date=datetime_to_string(client_agreement["activation_date"]),
                domain_used_unit=int(client_agreement["domain_used_unit"]),
                legal_entity_admin_contactno = le_admin_contactno,
                legal_entity_admin_email = le_admin_email,
                business_group_name=client_agreement["business_group_name"]
            )
        )
    return results

def get_statutory_notifications_report_data(db, request_data):
    country_id = request_data.country_id
    domain_id = request_data.domain_id
    level_1_statutory_id = request_data.statutory_id_optional
    from_date = request_data.from_date_optional
    to_date = request_data.to_date_optional
    from_count = request_data.from_count
    page_count = request_data.page_count

    if from_date is not None:
        from_date = string_to_datetime(from_date).date()
    if to_date is not None:
        to_date = string_to_datetime(to_date).date()

    statutory_notifictions_list = db.call_proc(
        "sp_statutory_notification_details", (country_id, domain_id,
            level_1_statutory_id, from_date, to_date, from_count, page_count)
    )

    statutory_notifictions_list = return_statutory_notifications(
        statutory_notifictions_list
    )

    return (
        statutory_notifictions_list
    )

def return_statutory_notifications(
    statutory_notifications
):
    notifications = []
    for notification in statutory_notifications:
        notifications.append(
            technoreports.StatutoryNotificationList(
                statutory_name=notification["statutory_name"],
                compliance_task=notification["compliance_task"],
                description=notification["description"],
                notification_text=notification["notification_text"],
                date=datetime_to_string(notification["created_on"])
            )
        )

    return notifications

def get_statutory_notifications_report_count(
    db, request_data
):
    country_id = request_data.country_id
    domain_id = request_data.domain_id
    level_1_statutory_id = request_data.statutory_id_optional
    from_date = request_data.from_date_optional
    to_date = request_data.to_date_optional

    if from_date is not None:
        from_date = string_to_datetime(from_date).date()
    if to_date is not None:
        to_date = string_to_datetime(to_date).date()

    statutory_notifictions_list_count = db.call_proc(
        "sp_statutory_notification_details_count", (
            country_id, domain_id, level_1_statutory_id, from_date, to_date
        )
    )

    return statutory_notifictions_list_count[0]["total_record"]

#
#   Get Details Report
#
def get_client_details_report_condition(
    country_id, client_id, business_group_id,
    legal_entity_id, division_id, unit_id, domain_ids
):
    condition = "tu.country_id = %s AND tu.client_id = %s "
    param = [country_id, client_id]
    if business_group_id is not None:
        condition += " AND tu.business_group_id = %s "
        param.append(business_group_id)

    if legal_entity_id is not None:
        condition += " AND tu.legal_entity_id = %s "
        param.append(legal_entity_id)

    if division_id is not None:
        condition += " AND tu.division_id = %s "
        param.append(division_id)

    if unit_id is not None:
        condition += " AND tu.unit_id = %s "
        param.append(unit_id)

    if domain_ids is not None:
        for i, domain_id in enumerate(domain_ids):
            if i == 0:
                condition += "  AND (FIND_IN_SET(%s, tu.domain_ids)"
                param.append(domain_id)
            elif i == len(domain_ids) - 1:
                condition += " OR FIND_IN_SET(%s, tu.domain_ids) )"
                param.append(domain_id)
            else:
                condition += " OR FIND_IN_SET(%s, tu.domain_ids)"
                param.append(domain_id)
        if len(domain_ids) == 1:
            condition += " )"
    return condition, param


def get_client_details_report_count(
    db, country_id, client_id, business_group_id,
    legal_entity_id, division_id, unit_id, domain_ids
):
    condition, param = get_client_details_report_condition(
        country_id, client_id, business_group_id,
        legal_entity_id, division_id, unit_id, domain_ids
    )
    query = "SELECT count(*) " +\
        " FROM %s tu " + \
        " WHERE %s "
    query = query % (tblUnits, condition)
    rows = db.select_all(query, param)
    result = convert_to_dict(rows, ["count"])
    return result[0]["count"]


def get_client_details_report(
    db, country_id, client_id, business_group_id,
    legal_entity_id, division_id, unit_id, domain_ids,
    start_count, to_count
):
    condition, params = get_client_details_report_condition(
        country_id, client_id, business_group_id,
        legal_entity_id, division_id, unit_id, domain_ids
    )
    columns = " unit_id, unit_code, unit_name, geography_name, " + \
        " address, domain_ids, postal_code, " + \
        " business_group_name, legal_entity_name, " + \
        " division_name "
    query = " SELECT %s FROM %s tu " + \
        " INNER JOIN %s tg ON (tu.geography_id = tg.geography_id) " + \
        " LEFT JOIN %s tb ON (tb.business_group_id " + \
        " = tu.business_group_id) " + \
        " INNER JOIN %s tl ON " + \
        " (tl.legal_entity_id = tu.legal_entity_id) " + \
        " LEFT JOIN %s td ON (td.division_id = tu.division_id) " + \
        " WHERE %s "
    query = query % (
            columns, tblUnits, tblGeographies, tblBusinessGroups,
            tblLegalEntities, tblDivisions, condition
        )
    query += " ORDER BY tu.business_group_id, " + \
        " tu.legal_entity_id, tu.division_id, " + \
        " tu.unit_id ASC LIMIT %s, %s"
    params.extend([int(start_count), int(to_count)])
    rows = db.select_all(query, params)
    columns_list = columns.replace(" ", "").split(",")
    unit_rows = convert_to_dict(rows, columns_list)
    grouped_units = {}
    for unit in unit_rows:
        business_group_name = unit["business_group_name"]
        legal_entity_name = unit["legal_entity_name"]
        division_name = unit["division_name"]
        if business_group_name in ["None", None, ""]:
            business_group_name = "null"
        if division_name in ["None", None, ""]:
            division_name = "null"
        if business_group_name not in grouped_units:
            grouped_units[business_group_name] = {}
        if legal_entity_name not in grouped_units[business_group_name]:
            grouped_units[business_group_name][legal_entity_name] = {}
        if (
            division_name not in grouped_units[
                business_group_name][legal_entity_name]
        ):
            grouped_units[
                business_group_name][legal_entity_name][division_name] = []
        grouped_units[
            business_group_name][legal_entity_name][division_name].append(
            technoreports.UnitDetails(
                unit["unit_id"], unit["geography_name"], unit["unit_code"],
                unit["unit_name"], unit["address"], unit["postal_code"],
                [int(x) for x in unit["domain_ids"].split(",")]
            )
        )
    GroupedUnits = []
    for business_group in grouped_units:
        for legal_entity_name in grouped_units[business_group]:
            for division in grouped_units[business_group][legal_entity_name]:
                if business_group == "null":
                    business_group_name = None
                else:
                    business_group_name = business_group
                if division == "null":
                    division_name = None
                else:
                    division_name = division
                GroupedUnits.append(
                    technoreports.GroupedUnits(
                        division_name, legal_entity_name, business_group_name,
                        grouped_units[
                            business_group][legal_entity_name][division]
                    )
                )
    return GroupedUnits


def get_compliance_list_report_techno(
    db, country_id, domain_id, industry_id,
    statutory_nature_id, geography_id,
    level_1_statutory_id, frequency_id, user_id, from_count, to_count
):
    q_count = "SELECT  count(distinct t2.compliance_id) " + \
        " FROM tbl_statutory_mappings t1 " + \
        " INNER JOIN tbl_compliances t2 " + \
        " ON t2.statutory_mapping_id = t1.statutory_mapping_id " + \
        " INNER JOIN tbl_mapped_industries t3 " + \
        " ON t3.statutory_mapping_id = t1.statutory_mapping_id " + \
        " INNER JOIN tbl_statutory_geographies t4 " + \
        " ON t4.statutory_mapping_id = t1.statutory_mapping_id " + \
        " INNER JOIN tbl_user_domains t5 " + \
        " ON t5.domain_id = t1.domain_id " + \
        " and t5.user_id = %s " + \
        " INNER JOIN tbl_user_countries t6 " + \
        " ON t6.country_id = t1.country_id " + \
        " and t6.user_id = %s " + \
        " WHERE t1.approval_status in (1, 3) AND t2.is_active = 1 AND " + \
        " t1.country_id = %s " + \
        " and t1.domain_id = %s "
    q_order = "ORDER BY SUBSTRING_INDEX( " + \
        " SUBSTRING_INDEX(t1.statutory_mapping, '>>', 1), '>>', -1), " + \
        " t2.frequency_id "
    param_list = [
        int(user_id), int(user_id), country_id, domain_id
    ]

    qry_where = ""
    if industry_id is not None:
        qry_where += "AND t3.industry_id = %s "
        param_list.append(industry_id)

    if geography_id is not None:
        qry_where += "AND t4.geography_id = %s "
        param_list.append(geography_id)

    if statutory_nature_id is not None:
        qry_where += "AND t1.statutory_nature_id = %s "
        param_list.append(statutory_nature_id)

    if level_1_statutory_id is not None:
        qry_where += " AND t1.statutory_mapping LIKE ( " + \
            " select concat(statutory_name, %s) " + \
            " from tbl_statutories where statutory_id = %s)"
        param_list.extend([str("%"), level_1_statutory_id])

    if frequency_id is not None:
        qry_where += "AND t2.frequency_id = %s "
        param_list.append(frequency_id)

    query = q_count + qry_where + q_order
    row = db.select_one(query, param_list)
    if row:
        r_count = row[0]
    else:
        r_count = 0

    industry_qry = "select organisation_name, statutory_mapping_id " + \
        " from tbl_mapped_industries si " + \
        " INNER JOIN tbl_organisation i on " + \
        " i.industry_id = si.industry_id "
    industry_rows = db.select_all(industry_qry)
    industry_result = convert_to_dict(
        industry_rows, ["organisation_name", "statutory_mapping_id"]
    )
    industry_statutory_mapping = {}
    for row in industry_result:
        statu_mapping_id = int(row["statutory_mapping_id"])
        if statu_mapping_id not in industry_statutory_mapping:
            industry_statutory_mapping[statu_mapping_id] = []
        industry_statutory_mapping[statu_mapping_id].append(
            row["organisation_name"]
        )

    q = " SELECT distinct t1.statutory_mapping_id, t1.country_id, " + \
        " (select country_name from tbl_countries " + \
        " where country_id = t1.country_id) country_name, " + \
        " t1.domain_id, " + \
        " (select domain_name from tbl_domains " + \
        " where domain_id = t1.domain_id) domain_name, " + \
        " t1.industry_ids, t1.statutory_nature_id, " + \
        " (select statutory_nature_name from tbl_statutory_natures " + \
        " where statutory_nature_id = t1.statutory_nature_id) " + \
        " statutory_nature_name, " + \
        " t1.statutory_ids, " + \
        " t1.geography_ids, " + \
        " t1.approval_status, t1.is_active, t1.statutory_mapping, " + \
        " t2.compliance_id, t2.statutory_provision, " + \
        " t2.compliance_task, t2.compliance_description, " + \
        " t2.document_name, t2.format_file, t2.format_file_size, " +\
        " t2.penal_consequences, t2.frequency_id, " + \
        " t2.statutory_dates, t2.repeats_every, " + \
        " t2.repeats_type_id, " + \
        " t2.duration, t2.duration_type_id " + \
        " FROM tbl_statutory_mappings t1 " + \
        " INNER JOIN tbl_compliances t2 " + \
        " ON t2.statutory_mapping_id = t1.statutory_mapping_id " + \
        " INNER JOIN tbl_mapped_industries t3 " + \
        " ON t3.statutory_mapping_id = t1.statutory_mapping_id " + \
        " INNER JOIN tbl_statutory_geographies t4 " + \
        " ON t4.statutory_mapping_id = t1.statutory_mapping_id " + \
        " INNER JOIN tbl_user_domains t5 " + \
        " ON t5.domain_id = t1.domain_id " + \
        " and t5.user_id = %s " + \
        " INNER JOIN tbl_user_countries t6 " + \
        " ON t6.country_id = t1.country_id " + \
        " and t6.user_id = %s " + \
        " WHERE t1.approval_status in (1, 3) AND t2.is_active = 1 AND " + \
        " t1.country_id = %s " + \
        " and t1.domain_id = %s "

    q_order = "ORDER BY SUBSTRING_INDEX(SUBSTRING_INDEX( " + \
        " t1.statutory_mapping, '>>', 1), '>>', -1), " + \
        " t2.frequency_id " + \
        " limit %s, %s"
    param_list.extend([from_count, to_count])
    q += qry_where + q_order

    rows = db.select_all(q, param_list)
    columns = [
        "statutory_mapping_id", "country_id",
        "country_name", "domain_id", "domain_name", "industry_ids",
        "statutory_nature_id", "statutory_nature_name",
        "statutory_ids", "geography_ids",
        "approval_status", "is_active", "statutory_mapping",
        "compliance_id", "statutory_provision",
        "compliance_task", "compliance_description",
        "document_name", "format_file",
        "format_file_size", "penal_consequences",
        "frequency_id", "statutory_dates", "repeats_every",
        "repeats_type_id", "duration", "duration_type_id"
    ]
    report_data = []
    if rows:
        report_data = convert_to_dict(rows, columns)

    return return_knowledge_report(
        db, report_data, industry_statutory_mapping, r_count
    )


def return_knowledge_report(
    db, report_data, industry_statutory_mapping, total_count=None
):
    if bool(GEOGRAPHY_PARENTS) is False:
        get_geographies(db)

    report_list = []
    for r in report_data:
        mapping = r["statutory_mapping"].split(">>")
        act_name = mapping[0].strip()
        statutory_provision = " >>".join(mapping[1:])
        statutory_provision += " " + r["statutory_provision"]
        compliance_task = r["compliance_task"]
        document_name = r["document_name"]
        if document_name == "None":
            document_name = None
        if document_name:
            name = "%s - %s" % (
                document_name, compliance_task
            )
        else:
            name = compliance_task

        format_file = r["format_file"]
        format_file_size = r["format_file_size"]
        if format_file_size is not None:
            format_file_size = int(format_file_size)
        if format_file:
            url = "%s/%s" % (
                KNOWLEDGE_FORMAT_DOWNLOAD_URL, format_file
            )
        else:
            url = None
        industry_names = ",".join(
            industry_statutory_mapping[r["statutory_mapping_id"]]
        )
        geography_ids = [
            int(x) for x in r["geography_ids"][:-1].split(',')
        ]
        geography_mapping_list = []
        for g_id in geography_ids:
            map_data = GEOGRAPHY_PARENTS.get(int(g_id))
            if map_data is not None:
                map_data = map_data[0]
            geography_mapping_list.append(map_data)

        statutory_dates = r["statutory_dates"]
        statutory_dates = json.loads(statutory_dates)
        date_list = []
        for date in statutory_dates:
            s_date = core.StatutoryDate(
                date["statutory_date"],
                date["statutory_month"],
                date["trigger_before_days"],
                date.get("repeat_by")
            )
            date_list.append(s_date)

        info = knowledgereport.StatutoryMappingReport(
            r["country_name"],
            r["domain_name"],
            industry_names,
            r["statutory_nature_name"],
            geography_mapping_list,
            r["approval_status"],
            bool(r["is_active"]),
            act_name,
            r["compliance_id"],
            statutory_provision,
            name,
            r["compliance_description"],
            r["penal_consequences"],
            r["frequency_id"],
            date_list,
            r["repeats_type_id"],
            r["repeats_every"],
            r["duration_type_id"],
            r["duration"],
            url
        )
        report_list.append(info)
    return report_list, total_count

def get_client_agreement_report(db, country_id, client_id, business_group_id,
    legal_entity_id, domain_id, contract_from, contract_to,
    from_count, page_count, session_user):

    if contract_from is not None:
        contract_from = string_to_datetime(contract_from).date()
    if contract_to is not None:
        contract_to = string_to_datetime(contract_to).date()

    client_agreement_list = db.call_proc(
        "sp_client_agreement_details", (country_id, client_id, business_group_id,
    legal_entity_id, domain_id, contract_from, contract_to, from_count, page_count, session_user)
    )

    client_agreement_list = return_client_agreement_report(
        client_agreement_list
    )

    return (
        client_agreement_list
    )

def return_client_agreement_report(client_agreement_list):
    results = []
    for client_agreement in client_agreement_list:
        le_admin_contactno = 'Not Available'
        if client_agreement["le_admin_contactno"] is not None:
            le_admin_contactno = client_agreement["le_admin_contactno"]

        le_admin_email = 'Not Available'
        if client_agreement["le_admin_email"] is not None:
            le_admin_email = client_agreement["le_admin_email"]
        results.append(
            technoreports.ClientAgreementList(
                legal_entity_id = int(client_agreement["legal_entity_id"]),
                domain_id = int(client_agreement["domain_id"]),
                legal_entity_name = client_agreement["legal_entity_name"],
                total_licence = int(client_agreement["total_licence"]),
                used_licence = int(client_agreement["used_licence"]),
                file_space = int(client_agreement["file_space_limit"]),
                used_file_space = int(client_agreement["used_file_space"]),
                contract_from = datetime_to_string(client_agreement["contract_from"]),
                contract_to = datetime_to_string(client_agreement["contract_to"]),
                group_name=client_agreement["group_name"],
                group_admin_email=client_agreement["groupadmin_email"],
                is_closed=bool(client_agreement["is_closed"]),
                domain_count=int(client_agreement["domaincount"]),
                d_name=client_agreement["domain_name"],
                domain_total_unit=int(client_agreement["domain_total_unit"]),
                activation_date=datetime_to_string(client_agreement["activation_date"]),
                domain_used_unit=int(client_agreement["domain_used_unit"]),
                legal_entity_admin_contactno = le_admin_contactno,
                legal_entity_admin_email = le_admin_email,
                business_group_name=client_agreement["business_group_name"],
            )
        )
    return results

def get_client_agreement_report_count(
    db, country_id, client_id, business_group_id,
    legal_entity_id, domain_id, contract_from, contract_to, session_user
):
    if contract_from is not None:
        contract_from = string_to_datetime(contract_from).date()
    if contract_to is not None:
        contract_to = string_to_datetime(contract_to).date()

    client_agreement_list_count = db.call_proc(
        "sp_client_agreement_details_count", (country_id, client_id, business_group_id,
    legal_entity_id, domain_id, contract_from, contract_to, session_user)
    )
    return client_agreement_list_count[0]["total_record"]

def get_domainwise_agreement_report(db, country_id, client_id, business_group_id,
    legal_entity_id, domain_id, contract_from, contract_to,
    from_count, page_count, session_user):

    if contract_from is not None:
        contract_from = string_to_datetime(contract_from).date()
    if contract_to is not None:
        contract_to = string_to_datetime(contract_to).date()

    domainwise_agreement_list = db.call_proc(
        "sp_domainwise_agreement_details", (country_id, client_id, business_group_id,
    legal_entity_id, domain_id, contract_from, contract_to, from_count, page_count, session_user)
    )

    domainwise_agreement_list = return_domainwise_agreement_report(
        domainwise_agreement_list
    )

    return (
        domainwise_agreement_list
    )

def return_domainwise_agreement_report(domainwise_agreement_list):
    results = []
    for client_agreement in domainwise_agreement_list:
        le_admin_contactno = 'Not Available'
        if client_agreement["le_admin_contactno"] is not None:
            le_admin_contactno = client_agreement["le_admin_contactno"]

        le_admin_email = 'Not Available'
        if client_agreement["le_admin_email"] is not None:
            le_admin_email = client_agreement["le_admin_email"]
        results.append(
            technoreports.DomainwiseAgreementList(
                legal_entity_id = int(client_agreement["legal_entity_id"]),
                domain_id = int(client_agreement["domain_id"]),
                legal_entity_name = client_agreement["legal_entity_name"],
                contract_from = datetime_to_string(client_agreement["contract_from"]),
                contract_to = datetime_to_string(client_agreement["contract_to"]),
                group_name=client_agreement["group_name"],
                group_admin_email=client_agreement["groupadmin_email"],
                domain_total_unit=int(client_agreement["domain_total_unit"]),
                activation_date=datetime_to_string(client_agreement["activation_date"]),
                domain_used_unit=int(client_agreement["domain_used_unit"]),
                legal_entity_admin_contactno = le_admin_contactno,
                legal_entity_admin_email = le_admin_email,
                business_group_name=client_agreement["business_group_name"]
            )
        )
    return results

def get_domainwise_agreement_report_count(
    db, country_id, client_id, business_group_id,
    legal_entity_id, domain_id, contract_from, contract_to, session_user
):
    if contract_from is not None:
        contract_from = string_to_datetime(contract_from).date()
    if contract_to is not None:
        contract_to = string_to_datetime(contract_to).date()

    domainwise_agreement_list_count = db.call_proc(
        "sp_domainwise_agreement_details_count", (country_id, client_id, business_group_id,
    legal_entity_id, domain_id, contract_from, contract_to, session_user)
    )
    return domainwise_agreement_list_count[0]["total_record"]

def get_organizationwise_unit_count(db, legal_entity_id, domain_id):
    organizationwise_unit_count_list = db.call_proc(
        "sp_organizationwise_unit_count", (legal_entity_id, domain_id)
    )

    results = []
    for organizationwise_unit_count in organizationwise_unit_count_list:
        results.append(
            technoreports.OrganizationwiseUnitCountList(
                domain_name = organizationwise_unit_count["domain_name"],
                organization_name = organizationwise_unit_count["organization_name"],
                domain_total_unit=int(organizationwise_unit_count["domain_total_unit"]),
                domain_used_unit=int(organizationwise_unit_count["domain_used_unit"])
            )
        )
    return results

def get_user_category_details(db, session_user):
    result = db.call_proc("sp_get_user_category_details", (int(session_user),))
    return result

######################################################################################
# To get countries list for user mapping report
# Parameter(s) : Object of database, user category id, user id
# Return Type : Return list of countries
######################################################################################
def get_countries_for_usermapping_report_filter(db, user_category_id, user_id):

    result = db.call_proc("sp_countries_for_usermapping_report", (user_category_id, user_id))
    print "countries"
    print result
    results = []
    for d in result:
        results.append(core.Country(
            d["country_id"], d["country_name"], bool(d["is_active"])
        ))
    return results

######################################################################################
# To get group details for user mapping report
# Parameter(s) : Object of the database, user category id, user id
# Return Type : Return list of client groups
######################################################################################
def get_group_details_for_usermapping_report_filter(db, user_category_id, user_id):
    result = db.call_proc("sp_usermapping_report_group_details", (user_category_id, user_id))
    results = []
    for d in result:
        results.append(core.UserMappingGroupDetails(
            d["client_id"], d["client_name"], d["legal_entity_id"], d["country_id"], d["business_group_id"]
        ))
    return results

######################################################################################
# To get business groups for user mapping report
# Parameter(s) : Object of Database
# Return Type : Return list of business groups
######################################################################################
def get_business_groups_for_usermapping_report(db):
    result = db.call_proc("sp_usermapping_report_business_groups", ())
    results = []
    for d in result:
        results.append(core.ClientBusinessGroup(
            d["business_group_id"], d["business_group_name"]
        ))
    return results
######################################################################################
# To get legal entity list
# Parameter(s) : Object of database
# Return Type : Return list of legal entities
######################################################################################
def get_legal_entities_for_usermapping_report(db):
    result = db.call_proc("sp_usermapping_report_legal_entity", ())
    results = []
    for d in result:
        results.append(core.ClientLegalEntity(
            d["legal_entity_id"], d["legal_entity_name"], d["business_group_id"]
        ))
    return results
######################################################################################
# To get units list for user mapping report
# Parameter(s) : Object of datanase, user category id, user id
# Return Type : Return list of units
######################################################################################
def get_unit_details_for_usermapping_report(db, user_category_id, user_id):
    result = db.call_proc("sp_usermapping_report_unit_details", (user_category_id, user_id))
    results = []
    for d in result:
        results.append(core.UserMappingUnitDetails(
            d["unit_id"], d["unit_name"], d["client_id"], d["business_group_id"],
            d["legal_entity_id"], d["country_id"], d["division_id"], d["division_name"],
            d["category_id"], d["category_name"]
        ))
    return results
####################################################################################################
# To get the user mapping report data
# Parameter(s) : Object of the database, user id, client id, legal entity id, country id,
#                   business group id, division id, category id, unit id
# Return Type : Return list of user mapped data
####################################################################################################
def get_usermapping_report_dataset(
        db, user_id, client_id, legal_entity_id, country_id, bgrp_id,
        division_id, category_id, unit_id, from_count, page_count
):
    args = [user_id, client_id, legal_entity_id, country_id, bgrp_id, division_id, category_id, unit_id, from_count, page_count]
    expected_result = 4
    result = db.call_proc_with_multiresult_set(
       "sp_usermapping_report_details", args, expected_result
    )
    print "result"
    print result
    techno_details = unit_domains = domains = {}

    if(len(result) > 0):
        if(len(result[1]) > 0):
            print "result 1"
            print result[1]
            techno_details = result[1]
            '''for techno in result[1]:
                techno_details.append(core.UserMappingReportTechno(
                    techno["unit_id"], techno["techno_manager"], techno["techno_user"]
                ))'''
        if(len(result[2]) > 0):
            unit_domains = result[2]
            '''for assign_domain in result[2]:
                unit_domains.append(core.UserMappingReportDomain(
                    assign_domain["unit_id"], assign_domain["employee_name"], assign_domain["user_category_name"], assign_domain["domain_id"]
                ))'''

        if(len(result[3]) > 0):
            domains = result[3]
            '''for domain in result[3]:
                domains.append(core.Domain(
                    domain["domain_id"], domain["domain_name"], domain["is_active"]
                ))'''
    return (techno_details, unit_domains, domains)
######################################################################################
# To get group admin email registration report data
# Parameter(s) : Object of database, user id
# Return Type : Return list of group admin registered email data
######################################################################################
def get_GroupAdminReportData(db, user_id):
    result = db.call_proc_with_multiresult_set("sp_group_admin_registration_email_report_data", (user_id,), 3)
    return result
######################################################################################
# To get reassigned user group user category and filter data
# Parameter(s) : Object of the database, user id
# Return Type : Return list of reassigned user report filter data
######################################################################################
def get_AssignedUserClientGroupsDetails(db, user_id):
    result = db.call_proc_with_multiresult_set("sp_reassignuser_report_usercategories", (), 5)
    print len(result)
    client_categories = []
    for categories in result[1]:
        user_id = int(categories.get("user_id"))
        user_category_id = int(categories.get("user_category_id"))
        emp_code_name = categories.get("emp_code_name")
        client_ids = []
        for user_clients in result[2]:
            if user_id == user_clients.get("user_id"):
                client_ids.append(int(user_clients.get("client_id")))
        client_categories.append([
            user_id, user_category_id, emp_code_name, client_ids
        ])
    print "user clients"
    print client_categories
    return (result[0], client_categories, result[3], result[4])
######################################################################################
# To get reassigned user group data
# Parameter(s) : Object of the database, user id, user category id, group id
# Return Type : Return list of reassigned user report data
######################################################################################
def get_ReassignUserReportData(db, user_category_id, user_id, group_id):
    c_names = []

    if group_id is None or group_id == 0:
        args = [user_id, user_category_id, '%']
    else:
        args = [user_id, user_category_id, group_id]
    print "inside args"
    print args
    result = db.call_proc_with_multiresult_set("sp_reassign_user_report_getdata", args, 2)
    reassign_group_list = []
    print len(result)
    print len(result[1])
    print result[1]
    if len(result[0]) > 0:
        for cl in result[0]:
            c_names = []
            print "inside 1 loop"
            client_id = int(cl.get("client_id"))
            print client_id
            group_name = cl.get("group_name")
            print group_name
            assigned_on = cl.get("assigned_on")
            emp_code_name = cl.get("emp_code_name")
            remarks = cl.get("remarks")
            le_count = int(cl.get("le_count"))
            for country in result[1]:

                print "inside 2 loop"
                print client_id
                if client_id == country.get("client_id"):
                    print "inside cl"
                    print country.get("client_id")
                    if len(c_names) == 0:
                        c_names.append(country.get("country_name"))
                    else:
                        for c_n in c_names:
                            if c_n.find(country.get("country_name")) == -1:
                                c_names.append(country.get("country_name"))

            reassign_group_list.append(technoreports.ReassignedUserList(
                client_id, group_name, le_count, c_names, assigned_on, emp_code_name, remarks
            ))
    print "inside database"
    print reassign_group_list
    return reassign_group_list
######################################################################################
# To get reassigned user group domain data
# Parameter(s) : Object of the database, request
# Return Type : Return list of reassigned user report data for domain user
######################################################################################
def get_ReassignUserDomainReportData(db, request_data):
    user_category_id = request_data.user_category_id
    user_id = request_data.user_id
    group_id = request_data.group_id_none
    bg_id = request_data.bg_id
    le_id = request_data.le_id
    d_id = request_data.d_id
    if bg_id is None:
        bg_id = '%'
        args = [user_id, user_category_id, group_id, bg_id, le_id, d_id]
    else:
        args = [user_id, user_category_id, group_id, bg_id, le_id, d_id]
    print "inside args"
    print args
    result = db.call_proc("sp_reassign_user_report_domain_user_getdata", args)
    reassign_group_list = []
    for d in result:
        reassign_group_list.append(technoreports.ReassignedDomainUserList(
            int(d["unit_id"]), d["unit_code"], d["unit_name"], d["address"], d["postal_code"],
            d["geography_name"], d["unit_email_date"], d["emp_code_name"], d["remarks"]
        ))
    print "after append"
    print reassign_group_list
    return reassign_group_list

def get_assigned_statutories_list(db, user_id):
    assigned_statutories = []
    result = db.call_proc_with_multiresult_set("sp_approve_assigned_statutories_list", (user_id,), 2)
    for row in result[1]:
        assigned_statutories.append(technoreports.ApproveAssignedStatutories(
            row["country_name"], row["group_name"], row["legal_entity_name"],
            row["business_group_name"], row["division_name"], row["category_name"],
            row["unit_id"], row["unit_name"], row["domain_name"], row["statutory_id"],
            row["domain_id"]
        ))
    print "approved list"
    print assigned_statutories
    return assigned_statutories

def get_ComplianceStatutoriesList(db, unit_id, domain_id, user_id):
    compliance_statutories = []
    args = [unit_id, domain_id]
    result = db.call_proc_with_multiresult_set("sp_approve_assigned_statutories_compliance_list", args, 3)