from protocol import (core, domaintransactionprotocol)
from server.exceptionmessage import process_error
from server.database.tables import *
from server.common import (get_date_time)


__all__ = [
    "get_assigned_statutories_list",
    "get_assigned_statutories_filters",
    "get_statutories_units", "get_compliances_to_assign",
    "save_client_statutories",
    "save_statutory_compliances",
    "get_assigned_compliance_by_id",
    "get_assigned_statutories_to_approve",
    "save_approve_statutories"
]

#
# Domain executive assigne statutory apis
#
def get_assigned_statutories_list(db, user_id):
    result = db.call_proc(
        "sp_clientstatutories_list", [user_id]
    )
    return return_assigned_statutories(result)


def return_assigned_statutories(data):
    fn = domaintransactionprotocol.AssignedStatutories
    data_list = []
    for d in data :
        is_edit = True if d.get("is_edit") > 0 else False
        is_edit = True if d["status"] == 4 else is_edit
        c_name = "%s - %s" % (d["unit_code"], d["unit_name"])
        data_list.append(fn(
            d["country_name"], d["client_id"], d["group_name"],
            d["business_group_name"], d["legal_entity_name"],
            d["division_name"], c_name, d["geography_name"],
            d["unit_id"], d["domain_id"], d["domain_name"], d["category_name"],
            core.ASSIGN_STATUTORY_APPROVAL_STATUS().value(d["status"]),
            d["status"], d["client_statutory_id"], d["legal_entity_id"], d["reason"],
            is_edit
        ))

    return data_list

def get_assigned_statutories_filters(db, user_id):
    result = db.call_proc_with_multiresult_set("sp_clientstatutories_filters", [user_id], 6)
    return return_statutories_filters(result)

def return_statutories_filters(data):
    groups = data[0]
    entitys = data[1]
    bgroups = data[2]
    divs = data[3]
    cats = data[4]
    domains = data[5]

    group_list = [
        core.Client(
            datum["client_id"], datum["group_name"],
            bool(datum["is_active"])
        ) for datum in groups
    ]

    bgroups_list = [
        core.BusinessGroup(
            datum["business_group_id"], datum["business_group_name"],
            datum["client_id"]
        ) for datum in bgroups
    ]

    entity_list = [
        core.AssignUnitLegalEntity(
            datum["legal_entity_id"], datum["legal_entity_name"],
            datum["business_group_id"], datum["client_id"]
        ) for datum in entitys
    ]

    div_list = [
        core.Division(
            datum["division_id"], datum["division_name"],
            datum["legal_entity_id"], datum["business_group_id"],
            datum["client_id"]
        ) for datum in divs
    ]

    cat_list = [
        core.Category(
            datum["category_id"], datum["category_name"],
            datum["division_id"], datum["legal_entity_id"],
            datum["business_group_id"], datum["client_id"]
        ) for datum in cats
    ]

    dom_list = [
        domaintransactionprotocol.LegalentityDomains(
            datum["legal_entity_id"], datum["domain_id"],
            datum["domain_name"]
        ) for datum in domains
    ]

    return domaintransactionprotocol.GetAssignedStatutoryWizardOneDataSuccess(
        group_list, bgroups_list, entity_list, div_list, cat_list, dom_list
    )

def get_statutories_units(db, request, user_id):
    client_id = request.client_id
    legal_entity_id = request.legal_entity_id
    domain_id = request.domain_id
    b_id = request.business_group_id
    if b_id is None :
        b_id = '%'
    div_id = request.division_id
    if div_id is None :
        div_id = '%'
    cat_id = request.category_id
    if cat_id is None :
        cat_id = '%'
    result = db.call_proc('sp_clientstatutories_units', [
        user_id, client_id, b_id, legal_entity_id, div_id, cat_id, domain_id
    ])

    data_list = []
    for r in result :
        data_list.append(domaintransactionprotocol.StatutoryUnits(
            r["unit_id"], r["unit_code"], r["unit_name"],
            r["address"], r["geography_name"], r["client_statutory_id"]
        ))

    return domaintransactionprotocol.GetAssignedStatutoryWizardOneUnitsSuccess(
        data_list
    )

def get_compliances_to_assign(db, request, user_id):
    unit_ids = request.unit_ids
    domain_id = request.domain_id
    rcount = request.rcount
    show_count = 50
    results = []
    totals = []
    for u in unit_ids :
        data, total = get_compliances_to_assign_byid(db, u, domain_id, user_id, rcount, show_count)
        results.extend(data)
        totals.append(total)

    results.sort(key=lambda x : (x.level_one_name, x.compliance_id))

    if len(unit_ids) > 1 :
        final = []
        app_units = []
        comp_id = None
        for r in results :

            if comp_id == r.compliance_id or comp_id is None :
                app_units.append(domaintransactionprotocol.ApplicableUnit(
                        r.unit_id, r.compliance_status, r.is_saved
                    ))
            else :
                if r.compliance_id != comp_id and comp_id is not None:
                    final.append(domaintransactionprotocol.AssignStatutoryComplianceMultiple(
                        r.level_one_id, r.level_one_name, r.mapping_text, r.statutory_provision,
                        r.compliance_id, r.document_name, r.compliance_name, r.description, r.organizations,
                        r.level_one_status, r.level_one_remarks, app_units
                    ))
                    app_units = []

                    app_units.append(domaintransactionprotocol.ApplicableUnit(
                        r.unit_id, r.compliance_status, r.is_saved
                    ))

            comp_id = r.compliance_id

    else :
        final = results

    return final, max(totals)

def get_compliances_to_assign_byid(db, unit_id, domain_id, user_id, from_count, show_count):
    result = db.call_proc_with_multiresult_set("sp_clientstatutories_compliance_new", [unit_id, domain_id, from_count, show_count], 5)
    statu = result[1]
    organisation = result[2]
    assigned_new_compliance = result[3]
    total_comp_list = result[4]

    def organisation_list(map_id) :
        org_list = []
        for o in organisation :
            if o.get("statutory_mapping_id") == map_id :
                org_list.append(o["organisation_name"])
        return org_list

    def status_list(map_id):
        level_1_id = None
        map_text = None
        level_1_s_name = None
        for s in statu :
            if s["statutory_mapping_id"] == map_id :
                if s["parent_ids"] == '' or s["parent_ids"] == 0 or s["parent_ids"] == '0,':
                    level_1_id = s["statutory_id"]
                    map_text = s["statutory_name"]
                    level_1_s_name = map_text
                else :
                    names = [x.strip() for x in s["parent_names"].split('>>') if x != '']
                    ids = [int(y) for y in s["parent_ids"].split(',') if y != '']
                    level_1_id = ids[0]
                    level_1_s_name = names[0]
                    if len(names) > 1 :
                        map_text = names[1]
                    else :
                        map_text = ''

        return level_1_id, level_1_s_name, map_text

    data_list = []
    for r in assigned_new_compliance :

        map_id = r["statutory_mapping_id"]
        orgs = organisation_list(map_id)
        level_1, level_1_name, map_text = status_list(map_id)
        if map_text == level_1_name :
            map_text = ""
        if r["assigned_compid"] is None :
            # before save rest of the field will be null before save in assignstatutorycompliance
            data_list.append(domaintransactionprotocol.AssignStatutoryCompliance(
                level_1, level_1_name, map_text,
                r["statutory_provision"], r["compliance_id"], r["document_name"],
                r["compliance_task"], r["compliance_description"], orgs,
                None, None, None, 0, unit_id

            ))
        else :
            # print r["is_approved"]
            # if r["is_approved"] == 5 :
            #     continue
            data_list.append(domaintransactionprotocol.AssignStatutoryCompliance(
                level_1, level_1_name, map_text,
                r["statutory_provision"], r["compliance_id"], r["document_name"],
                r["compliance_task"], r["compliance_description"], orgs,
                r["statutory_applicable_status"], r["remarks"], r["compliance_applicable_status"], r["is_approved"],
                unit_id
            ))

    data_list.sort(key=lambda x : (x.mapping_text, x.compliance_id))

    total_comp = 0
    for t in total_comp_list :
        total_comp = t["total"]

    return data_list, total_comp

def save_client_statutories(db, request, user_id):
    status = request.submission_type
    comps = request.compliances_applicablity_status
    q = "INSERT INTO tbl_client_statutories(client_id, unit_id, status)" + \
        " values (%s, %s, %s)"

    saved_unit = []

    for c in comps :

        if c.unit_id in saved_unit :
            continue

        if c.client_statutory_id is None :
            csid = db.execute_insert(q, [c.client_id, c.unit_id, status])
            if csid is False :
                raise process_error("E088")
        else :
            q1 = "UPDATE tbl_client_statutories set status = %s where client_statutory_id = %s"
            db.execute(q1, [status, c.client_statutory_id])
            csid = c.client_statutory_id

        saved_unit.append(c.unit_id)
        save_statutory_compliances(
            db, comps,
            c.unit_id, status, user_id, csid
        )
        unit_name = c.unit_name
        domain_name = c.domain_name

        msg = "Statutories has been assigned for following unit(s) %s in %s domain " % (
            unit_name, domain_name
        )
        save_messages(db, cat_domain_manager, "Assign Statutory", msg, "", user_id, c.unit_id)

    return True


def save_statutory_compliances(db, data, unit_id, status, user_id, csid):
    value_list = []
    for r in data :
        if r.unit_id == unit_id :
            remarks = r.remarks
            if remarks is None :
                remarks = ''
            value_list.append(
                (
                    csid, r.client_id, r.legal_entity_id, unit_id, r.domain_id,
                    r.level_1_id, r.status, str(remarks),
                    r.compliance_id, r.compliance_status, status,
                    user_id, get_date_time(), status
                )
            )

    table = "tbl_client_compliances"
    column = [
        "client_statutory_id",
        "client_id", "legal_entity_id", "unit_id",
        "domain_id", "statutory_id", "statutory_applicable_status",
        "remarks", "compliance_id",
        "compliance_applicable_status", "is_saved",
        "saved_by", "saved_on", "is_approved"
    ]
    update_column = [
        "statutory_id", "statutory_applicable_status", "remarks",
        "compliance_id", "compliance_applicable_status", "is_saved",
        "saved_by", "saved_on", "is_approved"
    ]

    result = db.on_duplicate_key_update(
        table, ",".join(column), value_list, update_column
    )
    if result is False :
        raise process_error("E088")


def get_assigned_compliance_by_id(db, request, user_id):
    # is_new = 0 is_saved = 1 , is_submmitted = 2, is_approved = 3, is_rejected = 4,  is_assigned = 5
    unit_id = request.unit_id
    domain_id = request.domain_id
    rcount = request.rcount
    show_count = 10

    result = db.call_proc_with_multiresult_set("sp_clientstatutories_compliance_new", [unit_id, domain_id, rcount, show_count], 5)
    statu = result[1]
    organisation = result[2]
    assigned_new_compliance = result[3]
    total_comp_list = result[4]

    def organisation_list(map_id) :
        org_list = []
        for o in organisation :
            if o.get("statutory_mapping_id") == map_id :
                org_list.append(o["organisation_name"])
        return org_list

    def status_list(map_id):
        level_1_id = None
        map_text = None
        level_1_s_name = None
        for s in statu :
            if s["statutory_mapping_id"] == map_id :
                if s["parent_ids"] == '' or s["parent_ids"] == 0 or s["parent_ids"] == '0,':
                    level_1_id = s["statutory_id"]
                    map_text = s["statutory_name"]
                    level_1_s_name = map_text
                else :
                    names = [x.strip() for x in s["parent_names"].split('>>') if x != '']
                    ids = [int(y) for y in s["parent_ids"].split(',') if y != '']
                    level_1_id = ids[0]
                    level_1_s_name = names[0]
                    if len(names) > 1 :
                        map_text = names[1]
                    else :
                        map_text = ''

        return level_1_id, level_1_s_name, map_text

    data_list = []
    for r in assigned_new_compliance :
        map_id = r["statutory_mapping_id"]
        orgs = organisation_list(map_id)

        level_1, level_1_s_name, map_text = status_list(map_id)
        if map_text == level_1_s_name :
            map_text = ""
        if r["assigned_compid"] is None :
                data_list.append(domaintransactionprotocol.AssignStatutoryCompliance(
                    level_1, level_1_s_name, map_text,
                    r["statutory_provision"], r["compliance_id"], r["document_name"],
                    r["compliance_task"], r["compliance_description"], orgs,
                    None, None, None, 0, unit_id
                ))
        else :
            # print r["is_approved"]
            # if r["is_approved"] == 5 :
            #     continue
            # before save rest of the field will be null before save in assignstatutorycompliance
            data_list.append(domaintransactionprotocol.AssignStatutoryCompliance(
                level_1, level_1_s_name, map_text,
                r["statutory_provision"], r["compliance_id"], r["document_name"],
                r["compliance_task"], r["compliance_description"], orgs,
                r["statutory_applicable_status"], r["remarks"],
                r["compliance_applicable_status"], r["is_approved"], unit_id
            ))

    data_list.sort(key=lambda x : (x.mapping_text, x.compliance_id))

    total_comp = 0
    for t in total_comp_list :
        total_comp = t["total"]

    return data_list, total_comp


#
# domain manager approve assign statutory apis
#

def get_assigned_statutories_to_approve(db, request, user_id):
    result = db.call_proc(
        "sp_clientstatutories_approvelist", [user_id]
    )
    return return_assigned_statutories(result)

def save_approve_statutories(db, request, user_id):
    unit_id = request.unit_id
    domain_id = request.domain_id
    client_statutory_id = request.client_statutory_id
    compliance_ids = request.compliance_ids
    s_s = request.submission_type
    reason = request.remarks
    unit_name = request.unit_name
    domain_name = request.domain_name
    # 3 : approve 4: reject
    if s_s not in (3, 4) :
        raise process_edrror("E089")

    if reason is None :
        reason = ''

    q = "update tbl_client_statutories set reason = %s, status = %s where unit_id = %s and client_statutory_id = %s"
    params = [reason, s_s, unit_id, client_statutory_id]
    db.execute(q, params)

    if s_s == 4 :

        for c in compliance_ids :
            # reject selected compliances
            q1 = "UPDATE tbl_client_compliances set is_approved=%s, approved_by=%s, approved_on=%s" + \
                " where unit_id = %s and domain_id = %s and compliance_id = %s"
            db.execute(q1, [4, user_id, get_date_time(), unit_id, domain_id, c])

        msg = "Assgined statutories has been rejected for unit %s in %s domain with following reason %s" % (
            unit_name, domain_name, reason
        )

    else :
        # is_approve = 5 when the compliance is applicable or not applicable
        q1 = "UPDATE tbl_client_compliances set is_approved=%s where compliance_applicable_status != 3 and client_statutory_id = %s"
        db.execute(q1, [5, client_statutory_id])

        # is_approve = 3 when the compliance is not at all applicable because it has to reshow domain users
        q1 = "UPDATE tbl_client_compliances set is_approved=%s where compliance_applicable_status = 3 and client_statutory_id = %s"
        db.execute(q1, [3, client_statutory_id])

        msg = "Assgined statutories has been approved for unit %s in %s domain " % (
            unit_name, domain_name
        )

    save_messages(db, cat_domain_executive, "Approved Assign Statutory", msg, "", user_id, unit_id)
    return True

def save_messages(db, user_cat_id, message_head, message_text, link, created_by, unit_id):
    msg_id = db.save_toast_messages(user_cat_id, message_head, message_text, link, created_by, get_date_time())
    msg_user_id = []
    q = "select user_id from tbl_user_units where user_category_id = %s and unit_id = %s"
    # if user_cat_id == cat_domain_executive :
    #     row = db.select_one(q, [cat_domain_manager, unit_id])

    # elif user_cat_id == cat_domain_manager :
    #     row = db.select_one(q, [cat_domain_executive, unit_id])
    row = db.select_one(q, [user_cat_id, unit_id])
    if row :
        msg_user_id.append(row["user_id"])

    if msg_user_id is not None :
        db.save_messages_users(msg_id, msg_user_id)
