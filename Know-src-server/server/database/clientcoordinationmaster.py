from tables import tblUnits, tblClientGroups
from server.common import get_date_time
from forms import frmClientUnitApproval, frmApproveClientGroup
from protocol import clientcoordinationmaster
from server.exceptionmessage import process_error, return_Knowledge_message
from server.common import datetime_to_string

__all__ = [
    "get_unit_approval_list",
    "get_entity_units_list",
    "approve_unit", "approve_client_group",
    "get_client_groups_approval_list", "get_legal_entity_info"
]


###############################################################################
# To get List of Legal entities which has un approved units
# Parameters : Object of database
# Return Type : List of Object of Unit Approval
###############################################################################
def get_unit_approval_list(db, session_user):
    #
    # sp_units_approval_list
    # Arguments : None
    # Results : List of legal entities with no of units to be approved
    #
    data = db.call_proc(
        "sp_units_approval_list", [session_user]
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
                    unit_id]["organisation_name"]
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
        if "organisation_name" not in unit_wise_industry_domain_map[unit_id]:
            unit_wise_industry_domain_map[unit_id]["organisation_name"] = []
        unit_wise_industry_domain_map[
            unit_id]["domain_names"].append(data["domain_name"])
        unit_wise_industry_domain_map[
            unit_id]["organisation_name"].append(data["organisation_name"])
    return unit_wise_industry_domain_map


###############################################################################
# To Approve/ Reject a multiple Units
# Parameters : Objct of database, request, session user
# Return Type : True if approve succeeds otherwise raises process error
###############################################################################
def approve_unit(db, request, session_user):
    unit_approval_details = request.unit_approval_details
    legal_entity_name = None
    current_time_stamp = get_date_time()
    columns = ["is_approved", "approved_by", "approved_on", "remarks", "updated_by", "updated_on"]
    values = []
    conditions = []
    for detail in unit_approval_details:
        legal_entity_name = detail.legal_entity_name
        unit_id = detail.unit_id
        approval_status = detail.approval_status
        reason = detail.reason
        value_tuple = (
           1 if approval_status is True else 2, session_user, current_time_stamp,
           reason, session_user, current_time_stamp
        )
        values.append(value_tuple)
        condition = "unit_id=%s" % (unit_id)
        conditions.append(condition)
    result = db.bulk_update(
        tblUnits, columns, values, conditions
    )
    db.call_insert_proc("sp_client_unit_apprival_messages_save", (
        session_user, "/knowledge/client-unit-approval", legal_entity_name, current_time_stamp
        ))
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
    data = db.call_proc_with_multiresult_set(
        "sp_client_groups_approval_list", [session_user], 3
    )
    print data
    group = return_client_groups(data[0], data[1])
    le_info = return_client_groups_approval_list(data[2])
    return group, le_info

def return_client_groups(data, c_info):
    groups = []
    for d in data :
        c_ids = []
        for c in c_info :
            if d["client_id"] == c["client_id"] :
                c_ids.append(c["country_id"])

        groups.append(clientcoordinationmaster.GroupInfo(
            d["client_id"], d["group_name"], d["short_name"],
            c_ids
        ))
    return groups
def return_client_groups_approval_list(groups):
    fn = clientcoordinationmaster.ClientGroupApproval
    result = [
        fn(
            group["client_id"], group["group_name"],
            group["short_name"], group["email_id"],
            group["legal_entity_name"], group["legal_entity_id"],
            group["country_name"]
        ) for group in groups
    ]
    return result

def get_legal_entity_info(db, entity_id):
    data = db.call_proc_with_multiresult_set("sp_client_groups_legal_entity_info", (entity_id,), 2)
    org_list = []
    result = None
    for d in data[1] :
        org_list.append(
            clientcoordinationmaster.LegalEntityOrganisation(
                d["legal_entity_id"], d["domain_id"],
                d["domain_name"], d["organisation_id"],
                d["organisation_name"], d["count"]
            )
        )
    for d1 in data[0]:
        result = clientcoordinationmaster.GetLegalEntityInfoSuccess(
            d1["legal_entity_id"], d1["bg_name"], datetime_to_string(d1["contract_from"]),
            datetime_to_string(d1["contract_to"]), int(d1["file_space_limit"]),
            d1["total_licence"], d1["total_view_licence"],
            org_list
        )

    return result

def approve_client_group(db, request, session_user):
    client_group_approval_details = request.client_group_approval_details
    current_time_stamp = get_date_time()
    columns = ["is_approved", "reason", "approved_by", "approved_on"]
    values = []
    conditions = []
    client_ids = []
    approval_status = False
    for detail in client_group_approval_details:
        client_ids.append(detail.client_id)
        entity_id = detail.entity_id
        entity_name = detail.entity_name
        approval_status = detail.approval_status
        reason = detail.reason
        value_tuple = (
           1 if approval_status is True else 2,
           reason, session_user, current_time_stamp
        )
        values.append(value_tuple)
        condition = "legal_entity_id=%s" % (entity_id)
        conditions.append(condition)
    result = db.bulk_update(
        "tbl_legal_entities", columns, values, conditions
    )

    text = entity_name + " Legal entity has been approved " if(approval_status is True) else "Legal entity has been rejected"

    db.call_insert_proc("sp_client_group_approve_message", [2, "Approve Client Group", text, session_user])

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
                text,
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
