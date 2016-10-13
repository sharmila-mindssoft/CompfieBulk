from tables import tblUnits, tblClientGroups
from server.common import get_date_time
from forms import frmClientUnitApproval, frmApproveClientGroup
from protocol import clientcoordinationmaster
from server.exceptionmessage import process_error, return_Knowledge_message


__all__ = [
    "get_unit_approval_list",
    "get_entity_units_list",
    "approve_unit", "approve_client_group",
    "get_client_groups_approval_list"
]


###############################################################################
# To get List of Legal entities which has un approved units
# Parameters : Object of database
# Return Type : List of Object of Unit Approval
###############################################################################
def get_unit_approval_list(db):
    #
    # sp_units_approval_list
    # Arguments : None
    # Results : List of legal entities with no of units to be approved
    #
    data = db.call_proc(
        "sp_units_approval_list", None
    )
    return return_unit_approval_list(data)


###############################################################################
# To convert Data fetched from database into list of object of Unit Approval
# Parameters : Legal entity list fetched from database
# Return Type : List of Object of Unit Approval
###############################################################################
def return_unit_approval_list(data):
    fn = clientcoordinationmaster.UnitApproval
    result = [
        fn(
            legal_entity_id=datum["legal_entity_id"],
            legal_entity_name=datum["legal_entity_name"],
            country_name=datum["country_name"],
            business_group_name=datum["business_group_name"],
            group_name=datum["group_name"],
            unit_count=datum["unit_count"]
        ) for datum in data
    ]
    return result


###############################################################################
# To get list of un approved units under a legal entity
# Parameters : Object of database, legal entity id
# Return Type : List of Object of EntityUnitApproval
###############################################################################
def get_entity_units_list(db, legal_entity_id):
    #
    # sp_units_approval_list_by_entity_id
    # Arguments : legal_entity_id
    # Results : List of units to be approved under the legal entity
    #
    data = db.call_proc_with_multiresult_set(
        "sp_units_approval_list_by_entity_id", (legal_entity_id,), 2
    )
    units = data[0]
    industry_domain_data = data[1]
    industry_domain_unitwise_map = return_unit_wise_industry_domain_map(
        industry_domain_data
    )
    return return_approval_units_under_entity(
        units, industry_domain_unitwise_map
    )


###############################################################################
# To Convert data fetched from database into list of Object
# of EntityUnitApproval
# Parameters : Unit Data fetched from database, dictionary
# Return Type : List of Object of EntityUnitApproval
###############################################################################
def return_approval_units_under_entity(units, industry_domain_unitwise_map):
    fn = clientcoordinationmaster.EntityUnitApproval
    result = []
    for row in units:
        unit_id = int(row["unit_id"])
        result.append(
            fn(
                unit_id=int(row["unit_id"]),
                division_name=row["division_name"],
                category_name=row["category_name"],
                unit_code=row["unit_code"],
                unit_name=row["unit_name"],
                address=row["address"],
                postal_code=row["postal_code"],
                geography_name=row["geography_name"],
                domain_names=industry_domain_unitwise_map[
                    unit_id]["domain_names"],
                org_names=industry_domain_unitwise_map[
                    unit_id]["industry_names"]
            )
        )
    return result


###############################################################################
# To create a dictionary (key: unit_id,
# value: dictionary (key: string, value:list))
# Parameters : Data fetched from database
# Return Type : Dictionary
###############################################################################
def return_unit_wise_industry_domain_map(industry_domain_data):
    unit_wise_industry_domain_map = {}
    for data in industry_domain_data:
        unit_id = int(data["unit_id"])
        if unit_id not in unit_wise_industry_domain_map:
            unit_wise_industry_domain_map[unit_id] = {}
        if "domain_names" not in unit_wise_industry_domain_map[unit_id]:
            unit_wise_industry_domain_map[unit_id]["domain_names"] = []
        if "industry_names" not in unit_wise_industry_domain_map[unit_id]:
            unit_wise_industry_domain_map[unit_id]["industry_names"] = []
        unit_wise_industry_domain_map[
            unit_id]["domain_names"].append(data["domain_name"])
        unit_wise_industry_domain_map[
            unit_id]["industry_names"].append(data["industry_name"])
    return unit_wise_industry_domain_map


###############################################################################
# To Approve/ Reject a multiple Units
# Parameters : Objct of database, request, session user
# Return Type : True if approve succeeds otherwise raises process error
###############################################################################
def approve_unit(db, request, session_user):
    unit_approval_details = request.unit_approval_details
    current_time_stamp = get_date_time()
    columns = ["approve_status", "remarks", "updated_by", "updated_on"]
    values = []
    conditions = []
    for detail in unit_approval_details:
        unit_id = detail.unit_id
        approval_status = detail.approval_status
        reason = detail.reason
        value_tuple = (
           1 if approval_status is True else 0,
           reason, session_user, current_time_stamp
        )
        values.append(value_tuple)
        condition = "unit_id=%s" % (unit_id)
        conditions.append(condition)
    result = db.bulk_update(
        tblUnits, columns, values, conditions
    )
    #
    # sp_activity_log_save
    # Arguments : user id, form id, action, time of action
    # Results : Returns activity log id
    #
    if result:
        db.call_insert_proc(
            "sp_activity_log_save",
            (
                session_user, frmClientUnitApproval,
                "Approved Unit" if(
                    approval_status is True) else "Rejected Unit",
                current_time_stamp
            )
        )
        return result
    else:
        db.call_insert_proc(
            "sp_activity_log_save",
            (
                session_user, frmClientUnitApproval,
                return_Knowledge_message("E072"), current_time_stamp
            )
        )
        raise process_error("E072")


def get_client_groups_approval_list(db, session_user):
    #
    # sp_client_groups_approval_list
    # Arguments : None
    # Results : List of Client groups with no of legal entities
    #
    data = db.call_proc(
        "sp_client_groups_approval_list", (session_user,)
    )
    return return_client_groups_approval_list(data)


def return_client_groups_approval_list(groups):
    fn = clientcoordinationmaster.ClientGroupApproval
    result = [
        fn(
            client_id=group["client_id"], group_name=group["group_name"],
            username=group["email_id"], le_count=group["count"],
            is_active=True if(group["count"] > 0) else False,
            country_ids=[
                int(x) for x in group["client_countries"].split(",")
            ]
        ) for group in groups
    ]
    return result


def approve_client_group(db, request, session_user):
    client_group_approval_details = request.client_group_approval_details
    current_time_stamp = get_date_time()
    columns = ["is_approved", "remarks", "approved_by", "approved_on"]
    values = []
    conditions = []
    approval_status = False
    for detail in client_group_approval_details:
        client_id = detail.client_id
        approval_status = detail.approval_status
        reason = detail.reason
        value_tuple = (
           1 if approval_status is True else 0,
           reason, session_user, current_time_stamp
        )
        values.append(value_tuple)
        condition = "client_id=%s" % (client_id)
        conditions.append(condition)
    result = db.bulk_update(
        tblClientGroups, columns, values, conditions
    )
    #
    # sp_activity_log_save
    # Arguments : user id, form id, action, time of action
    # Results : Returns activity log id
    #
    if result:
        db.call_insert_proc(
            "sp_activity_log_save",
            (
                session_user, frmApproveClientGroup,
                "Approved Client Group" if(
                    approval_status is True) else "Rejected Client Group",
                current_time_stamp
            )
        )
        return result
    else:
        db.call_insert_proc(
            "sp_activity_log_save",
            (
                session_user, frmApproveClientGroup,
                return_Knowledge_message("E072"), current_time_stamp
            )
        )
        raise process_error("E072")
