import threading
from protocol import core, technotransactions
from server.exceptionmessage import process_error
from server.database.tables import *
from server.common import (
    get_date_time, get_current_date,
    addHours, new_uuid, string_to_datetime,
    datetime_to_string
)

from server.database.general import get_short_name
from server.database.saveclientdata import *
from server.constants import REGISTRATION_EXPIRY, CLIENT_URL
from server.emailcontroller import EmailHandler as email

__all__ = [
    "get_categories_for_user",
    "get_assigned_statutory_wizard_two_data", "save_assigned_statutory",
    "get_assigned_statutories_by_id",
    "update_assigned_statutory", "get_groupadmin_registration_grouplist",
    "get_groupadmin_registration_unitlist", "send_groupadmin_registration_mail",
    "resave_registraion_token", "get_LegalEntityClosureReportData", "save_legalentity_closure_data"
]

def get_categories_for_user(db, user_id):
    result = db.call_proc("sp_categories_by_user", (user_id,))
    return return_categories(result)


def return_categories(data):
    fn = core.Category
    result = [
        fn(
            category_id=datum["category_id"],
            category_name=datum["category_name"],
            division_id=datum["division_id"],
            legal_entity_id=datum["legal_entity_id"],
            business_group_id=datum["business_group_id"],
            client_id=datum["client_id"]
        ) for datum in data
    ]
    return result

def get_assigned_statutory_wizard_two_data(
    db, client_id, busienss_group_id, legal_entity_id,
    division_id, category_id, domain_id, unit_ids
):
    (
        unit_loc_details, unit_org_details
    ) = db.call_proc_with_multiresult_set(
        "sp_unit_unit_organiation_details",
        (",".join(str(x) for x in unit_ids),), 2
    )
    country_count_map = {}
    domain_count_map = {}
    geo_count_map = {}
    org_count_map = {}

    unit_count = len(unit_ids)  # Unit count

    # To separate country wise units and geo wise units
    for unit in unit_loc_details:
        country_id = unit["country_id"]
        geography_id = unit["geography_id"]
        if country_id not in country_count_map:
            country_count_map[country_id] = []
        if geography_id not in geo_count_map:
            geo_count_map[geography_id] = []
        country_count_map[country_id].append(unit["unit_id"])
        geo_count_map[geography_id].append(unit["unit_id"])

    # To separate domain wise and org wise units
    for unit in unit_org_details:
        domain_id = unit["domain_id"]
        org_id = unit["organisation_id"]
        unit_id = unit["unit_id"]
        if domain_id not in domain_count_map:
            domain_count_map[domain_id] = []
        if org_id not in org_count_map:
            org_count_map[org_id] = []
        domain_count_map[domain_id].append(unit_id)
        org_count_map[org_id].append(unit_id)

    common_countries = []
    common_geographies = []
    common_domains = []
    common_orgs = []
    for country_id in country_count_map:
        unit_ids = country_count_map[country_id]
        if len(unit_ids) >= unit_count:
            common_countries.append(country_id)

    for geography_id in geo_count_map:
        unit_ids = geo_count_map[geography_id]
        if len(unit_ids) >= unit_count:
            common_geographies.append(geography_id)

    for domain_id in domain_count_map:
        unit_ids = domain_count_map[domain_id]
        if len(unit_ids) >= unit_count:
            common_domains.append(domain_id)

    for org_id in org_count_map:
        unit_ids = org_count_map[org_id]
        if len(unit_ids) >= unit_count:
            common_orgs.append(org_id)

    if(len(common_countries) <= 0):
        raise process_error("EO83")
    elif(len(common_geographies) <= 0):
        raise process_error("E084")
    elif(len(common_domains) <= 0):
        raise process_error("E085")
    elif(len(common_orgs) <= 0):
        raise process_error("E086")

    (
        statutories, level_1_statutories,
        mapping_orgs, mapping_locations
    ) = db.call_proc_with_multiresult_set(
        "sp_compliances_by_unit_details", (
            ",".join(str(x) for x in common_domains),
            ",".join(str(x) for x in common_countries),
            ",".join(str(x) for x in common_geographies),
            ",".join(str(x) for x in common_orgs),
        ), 4
    )
    return return_wizard_two_data(
        statutories, level_1_statutories, mapping_orgs, mapping_locations
    )


def return_wizard_two_data(
    statutories, level_1_statutories, mapping_orgs, mapping_locations
):
    mapping_wise_level_1_statutory = {}
    for level_1_statutory in level_1_statutories:
        statutory_mapping_id = level_1_statutory["statutory_mapping_id"]
        mapping_wise_level_1_statutory[
            statutory_mapping_id] = level_1_statutory["statutory_name"]

    mapping_wise_orgs = {}
    for org in mapping_orgs:
        statutory_mapping_id = org["statutory_mapping_id"]
        organisation_name = org["org_name"]
        if statutory_mapping_id not in mapping_wise_orgs:
            mapping_wise_orgs[statutory_mapping_id] = []
        mapping_wise_orgs[statutory_mapping_id].append(
            organisation_name
        )

    mapping_wise_locations = {}
    for location in mapping_locations:
        statutory_mapping_id = location["statutory_mapping_id"]
        geography_name = location["geography_name"]
        if statutory_mapping_id not in mapping_wise_locations:
            mapping_wise_locations[statutory_mapping_id] = []
        mapping_wise_locations[statutory_mapping_id].append(
            geography_name
        )

    level_1_statutories = []
    compliances = []
    fn = technotransactions.AssignStatutoryCompliance
    for statutory in statutories:
        statutory_mapping_id = int(statutory["statutory_mapping_id"])
        level_1_statutories.append(
            mapping_wise_level_1_statutory[statutory_mapping_id]
        )
        compliances.append(
            fn(
                level_1_statutory_index=len(level_1_statutories) - 1,
                statutory_provision=statutory["statutory_provision"],
                compliance_id=statutory["compliance_id"],
                document_name=statutory["document_name"],
                compliance_name=statutory["compliance_task"],
                description=statutory["compliance_description"],
                organizations=mapping_wise_orgs[statutory_mapping_id],
                locations=mapping_wise_locations[statutory_mapping_id]
            )
        )
    return level_1_statutories, compliances


def update_assigned_statutory(
    db, client_statutory_id, client_id, compliances_list, unit_ids, units, level_1_statutory_compliance,
    submission_type, session_user
):
    if(submission_type == "save"):
        columns = [
            "statutory_applicable_status", "compliance_applicable_status", "is_saved",
            "saved_by", "saved_on"
        ]
    else:
        columns = [
            "statutory_applicable_status", "compliance_applicable_status",
            "is_submitted", "submitted_by", "submitted_on"
        ]
    value_list = []
    conditions = []
    for compliances in compliances_list:
        for unit_id in unit_ids:
            compliance_id = compliances.compliance_id
            compliance_applicable_status = compliances.compliance_applicability_status
            statutory_applicable_status = compliances.statutory_applicability_status
            value_list.append(
                (
                    statutory_applicable_status, compliance_applicable_status,
                    1, session_user, get_date_time()
                )
            )
            conditions.append(
                "client_statutory_id=%s and compliance_id=%s" % (client_statutory_id, compliance_id)
            )
    db.bulk_update(
        tblClientCompliances, columns, value_list, conditions
    )


def save_assigned_statutory(
    db, client_statutory_id, client_id, compliances_list, unit_ids, units, level_1_statutory_compliance,
    submission_type, session_user
):
    ### Inserting in client statutories
    column = ["client_id", "unit_id"]
    value_list = []
    for unit_id in unit_ids:
        value_list.append((client_id, unit_id))
    db.bulk_insert(tblClientStatutories, column, value_list)

    compliance_ids_list = []
    for level_1 in level_1_statutory_compliance:
        compliance_ids_list = compliance_ids_list + level_1_statutory_compliance[level_1]

    compliance_domains, client_statutory_ids = db.call_proc_with_multiresult_set(
        "sp_clientstatutories_by_client_unit",
        (
            client_id, ",".join(str(x) for x in unit_ids),
            ",".join(str(x) for x in compliance_ids_list),
        ), 2
    )

    compliance_domain_maps = {}
    client_domain_statutories = {}
    unit_id_map = {}

    ### To pick domain id with compliance id
    for c in compliance_domains:
        compliance_domain_maps[c["compliance_id"]] = c["domain_id"]

    ### To pick client stautory id with client id and unit id
    for s in client_statutory_ids:
        client_id = s["client_id"]
        unit_id = s["unit_id"]
        if client_id not in client_domain_statutories:
            client_domain_statutories[client_id] = {}
        if unit_id not in client_domain_statutories[client_id]:
            client_domain_statutories[client_id][unit_id] = s["client_statutory_id"]

    ### To pick unit values with unit id
    for u in units:
        unit_id_map[u.unit_id] = u

    ### Inserting in client compliances table
    if(submission_type == "save"):
        compliance_columns = [
            "client_statutory_id", "client_id", "legal_entity_id", "unit_id", "domain_id",
            "statutory_id", "statutory_applicable_status", "compliance_id",
            "compliance_applicable_status", "is_saved", "saved_by", "saved_on"
        ]
    else:
        compliance_columns = [
            "client_statutory_id", "client_id", "legal_entity_id", "unit_id", "domain_id",
            "statutory_id", "statutory_applicable_status", "compliance_id",
            "compliance_applicable_status", "is_submitted", "submitted_by", "submitted_on"
        ]
    compliance_values_list = []
    for compliances in compliances_list:
        for unit_id in unit_ids:
            client_statutory_id = client_domain_statutories[client_id][unit_id]
            compliance_id = compliances.compliance_id
            compliance_applicable_status = compliances.compliance_applicability_status
            statutory_applicable_status = compliances.statutory_applicability_status
            level_1_statutory_id = None
            for level_1 in level_1_statutory_compliance:
                if compliance_id in level_1_statutory_compliance[level_1]:
                    level_1_statutory_id = level_1
                    break
            compliance_values_list.append(
                (
                    client_statutory_id, client_id, unit_id_map[unit_id].legal_entity_id,
                    unit_id, compliance_domain_maps[compliance_id], level_1_statutory_id,
                    statutory_applicable_status, compliance_id, compliance_applicable_status,
                    1, session_user, get_date_time()
                )
            )
    db.bulk_insert(tblClientCompliances, compliance_columns, compliance_values_list)

def get_assigned_statutories_by_id(db, client_statutory_id):
    client_statutories  = db.call_proc(
        "sp_clientstatutories_by_id", (client_statutory_id,), 2
    )
    return return_assigned_statutories_by_id(client_statutories)


def return_assigned_statutories_by_id(statutories):
    level_1_statutories = []
    compliances = []
    fn = technotransactions.AssignStatutoryCompliance
    for statutory in statutories:
        statutory_mapping_id = int(statutory["statutory_mapping_id"])
        if statutory["statutory_name"] not in level_1_statutories:
            level_1_statutories.append(
                statutory["statutory_name"]
            )
        level_1_statutory_index = level_1_statutories.index(statutory["statutory_name"])
        compliances.append(
            fn(
                level_1_statutory_index=level_1_statutory_index,
                statutory_provision=statutory["statutory_provision"],
                compliance_id=statutory["compliance_id"],
                document_name=statutory["document_name"],
                compliance_name=statutory["compliance_task"],
                description=statutory["compliance_description"],
                organizations=[str(x) for x in statutory["organisation_name"].split(",")],
                locations=[str(x) for x in statutory["geography_name"].split(",")]
            )
        )
    return level_1_statutories, compliances

######################################################################################
# To get group admin registered email groups list
# Parameter(s) : Object of the database, user id
# Return Type : Return list of group admin registered email list
######################################################################################
def get_groupadmin_registration_grouplist(db, user_id):
    groupadmin_grouplist = db.call_proc_with_multiresult_set("sp_groupadmin_registration_email_groupslist", (user_id,), 2)
    return return_groupadmin_registration_grouplist(groupadmin_grouplist)
######################################################################################
# To convert databse result to list
# Parameter(s) : DB Recordset
# Return Type : Return list of group admin registered email groups list
######################################################################################
def return_groupadmin_registration_grouplist(groupslist):
    groupadmin_grouplist = []
    for groups in groupslist[0]:
        if groups.get("replication_status") == 1 :
            continue
        client_id = groups.get("client_id")
        group_name = groups.get("group_name")
        no_of_legal_entities = groups.get("no_of_legal_entities")
        ug_name = groups.get("ug_name")
        email_id = groups.get("email_id")
        user_id_search = groups.get("user_id")
        emp_code_name = groups.get("emp_code_name")
        registration_email_date = groups.get("registration_email_date")
        c_names = []
        occur = -1
        for countries in groupslist[1]:
            if client_id == countries.get("client_id"):
                if len(c_names) > 0:
                    for c_n in c_names:
                        if(c_n.find(countries.get("country_name")) >= 0):
                            occur = 1
                if occur < 0:
                        c_names.append(countries.get("country_name"))

        groupadmin_grouplist.append(technotransactions.GroupAdmin_GroupList(
                client_id, group_name, no_of_legal_entities,
                c_names, ug_name, email_id, user_id_search, emp_code_name,
                registration_email_date
            ))
    return groupadmin_grouplist
######################################################################################
# To get group admin registered email units list
# Parameter(s) : Object of the database, user id
# Return Type : Return list of group admin registered email unit list
######################################################################################
def get_groupadmin_registration_unitlist(db, user_id):
    groupadmin_unitlist = db.call_proc_with_multiresult_set("sp_groupadmin_registration_email_unitslist", (user_id,), 2)
    result = []
    result = groupadmin_unitlist[1]
    return return_groupadmin_registration_unitlist(result)
######################################################################################
# To convert database records to list
# Parameter(s) : Database recordset
# Return Type : Return list of group admin registered email units list
######################################################################################
def return_groupadmin_registration_unitlist(unitslist):
    groupadmin_unitlist = []
    for units in unitslist:
        unit_creation_informed = 0
        statutory_assigned_informed = 0
        if units["unit_creation_informed"] is not None:
            unit_creation_informed = units["unit_creation_informed"]
        if units["statutory_assigned_informed"] is not None:
            statutory_assigned_informed = units["statutory_assigned_informed"]
        groupadmin_unitlist.append(technotransactions.GroupAdmin_UnitList(
                units["client_id"], units["legal_entity_id"], units["legal_entity_name"],
                units["country_name"], units["unit_count"],
                unit_creation_informed, statutory_assigned_informed, units["email_id"],
                units["user_id"], units["emp_code_name"], units["statutory_count"]
            ))
    return groupadmin_unitlist
######################################################################################
# To resend the user registration for group admin registered email list
# Parameter(s) : Object of the database, user id
# Return Type : Return list of group admin registered email list
######################################################################################
def resave_registraion_token(db, client_id, email_id, save_mode, user_id):

    # def _del_olddata():
    #     condition = "client_id = %s and verification_type_id = %s"
    #     condition_val = [client_id, 1]
    #     db.delete(tblClientEmailVerification, condition, condition_val)
    #     return True

    short_name = get_short_name(db, client_id)
    current_time_stamp = get_current_date()
    registration_token = new_uuid()
    expiry_date = addHours(int(REGISTRATION_EXPIRY), current_time_stamp)

    link = "%suserregistration/%s/%s" % (
        CLIENT_URL, short_name, registration_token
    )
    print link

    notify_user_thread = threading.Thread(
        target=notify_user, args=[
            email_id, link
        ]
    )
    notify_user_thread.start()
    if short_name:
        SaveRegistrationData(db, registration_token, expiry_date, email_id, client_id, current_time_stamp, user_id)
        if save_mode == "send":
            q = "insert into tbl_group_admin_email_notification(client_id, group_admin_email_id, " + \
                " registration_sent_by, registration_sent_on ) values(%s, %s, %s, %s)"
            db.execute(q, [client_id, email_id, user_id, current_time_stamp])
            message_text = 'Registartion Email has been sent successfully under the group - %s' % short_name
            db.save_activity(user_id, frmGroupAdminRegistraionEmail, message_text)
            return True
        elif save_mode == "resend":
            q = "insert into tbl_group_admin_email_notification(client_id, group_admin_email_id, " + \
                " registration_resend_by, registration_resend_on ) values(%s, %s, %s, %s)"
            db.execute(q, [client_id, email_id, user_id, current_time_stamp])
            message_text = 'Registartion Email has been resend successfully under the group - %s' % short_name
            db.save_activity(user_id, frmGroupAdminRegistraionEmail, message_text)
            return True
    else :
        return False
######################################################################################
# To send group admin registered email and save the notification to the user
# Parameter(s) : Object of the database, user id, request set
# Return Type : Return the value of the notofication saved
######################################################################################
def send_groupadmin_registration_mail(db, request, user_id):
    group_mode = request.grp_mode
    email_id = request.email_id
    emp_name = request.username
    group_name = request.group_name
    current_time_stamp = get_date_time()
    legal_entity_name = request.legal_entity_name
    insert_result = False
    try:
        notify_grp_admin_thread = threading.Thread(
            target=notify_grp_admin_mail, args=[
                group_mode, email_id, group_name, legal_entity_name
            ]
        )
        notify_grp_admin_thread.start()
        result = db.call_insert_proc(
                        "sp_tbl_groupadmin_email_notification_insert", (
                            group_mode, int(request.client_id), int(request.legal_entity_id),
                            email_id, 1, current_time_stamp, int(user_id))
                        )
        if result > 0 :
            insert_result = True
            if group_mode == "unit":
                message_text = 'Registartion Email for unit has been sent successfully under the group - %s' % group_name
                db.save_activity(user_id, frmGroupAdminRegistraionEmail, message_text)
            else:
                message_text = 'Registartion Email for assigned statutory has been sent successfully under the group - %s' % group_name
                db.save_activity(user_id, frmGroupAdminRegistraionEmail, message_text)
    except Exception, e:
        print "Error with group admin registration"
        print e
    return insert_result
######################################################################################
# To send email to registration link
# Parameter(s) : Email Id, Link
# Return Type : Return email success/failure value
######################################################################################
def notify_user(email_id, link):
    try:
        email().resend_registraion_link(email_id, link)
    except Exception, e:
        print "Error while sending email"
        print e

######################################################################################
# To send notification email of the units and statutories
# Parameter(s) : email id, group name, legal entity name
# Return Type : Return success/failure value of the email
######################################################################################
def notify_grp_admin_mail(mode, email_id, group_name, legal_entity_name):
    try:
        if mode == "unit" :
            email().send_notification_groupadmin_unit(email_id, group_name, legal_entity_name)
        elif mode == "statutory" :
            email().send_notification_groupadmin_statutory(email_id, group_name, legal_entity_name)
    except Exception, e:
            print "Error while sending email"
            print e

#
# To get the legal entity list under the techno manager for closure prrocess
#
######################################################################################
# To get legal entity closure report data
# Parameter(s) : Object of the database, user id
# Return Type : Return list of legal closed list with its status
######################################################################################
def get_LegalEntityClosureReportData(db, user_id):
    result = db.call_proc("sp_legalenity_closure_list", (user_id,))
    le_closure = []

    for r in result:
        le_closure.append(technotransactions.LegalEntityClosure(
            int(r["client_id"]), r["group_name"], int(r["legal_entity_id"]), r["legal_entity_name"],
            r["business_group_name"], r["country_name"], bool(r["is_active"]), str(r["closed_on"]),
            int(r["validity_days"])
        ))
    return le_closure

######################################################################################
# To save legal entity closure data
# Parameter(s) : Object of the database, user id, password, legal entity id, remarks
# Return Type : Return the value of the save process
######################################################################################
def save_legalentity_closure_data(db, user_id, password, legal_entity_id, remarks, action_mode):
    current_time_stamp = get_current_date()
    return_result = None
    if action_mode == "close":
        return_result = "Unable to Close the Legal Entity"
        result = db.call_update_proc("sp_legalentity_closure_save", (
            user_id, legal_entity_id, 1, current_time_stamp, remarks
        ))
    elif action_mode == "reactive":
        return_result = "Unable to Reactivate the Legal Entity"
        result = db.call_update_proc("sp_legalentity_closure_save", (
            user_id, legal_entity_id, 0, current_time_stamp, remarks
        ))

    if result:
        return_result = None

    if(return_result is None):
        return result
    else:
        return return_result
