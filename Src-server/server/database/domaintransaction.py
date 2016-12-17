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
    "get_assigned_compliance_by_id"
]

def get_assigned_statutories_list(db, user_id):
    result = db.call_proc(
        "sp_clientstatutories_list", [user_id]
    )
    print result
    return return_assigned_statutories(result)


def return_assigned_statutories(data):
    fn = domaintransactionprotocol.AssignedStatutories
    data_list = []
    for d in data :
        c_name = "%s - %s" % (d["unit_code"], d["unit_name"])
        data_list.append(fn(
            d["country_name"], d["client_id"], d["group_name"],
            d["business_group_name"], d["legal_entity_name"],
            d["division_name"], c_name, d["geography_name"],
            d["unit_id"], d["domain_id"], d["domain_name"], d["category_name"],
            core.ASSIGN_STATUTORY_APPROVAL_STATUS().value(d["is_approved"]),
            d["is_approved"], d["client_statutory_id"], d["legal_entity_id"]
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
        core.UnitLegalEntity(
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
    results = []
    for u in unit_ids :
        data = get_compliances_to_assign_byid(db, u, domain_id, user_id)
        results.extend(data)

    results.sort(key=lambda x : (x.level_one_id, x.compliance_id))
    return results

def get_compliances_to_assign_byid(db, unit_id, domain_id, user_id):

    result = db.call_proc_with_multiresult_set("sp_clientstatutories_compliance_new", [unit_id, domain_id], 5)
    statu = result[1]
    organisation = result[2]
    new_compliance = result[3]
    assigned_compliance = result[4]

    def organisation_list(map_id) :
        org_list = []
        for o in organisation :
            print o
            if o.get("statutory_mapping_id") == map_id :
                org_list.append(o["organisation_name"])
        return org_list

    def status_list(map_id):
        level_1_id = None
        map_text = None
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
                        map_text = " >> ".join(names[1:])
                        map_text += " >> %s" % (s["statutory_name"])
                    else :
                        map_text = s["statutory_name"]

        return level_1_id, level_1_s_name, map_text

    data_list = []
    for r in new_compliance :
        map_id = r["statutory_mapping_id"]
        orgs = organisation_list(map_id)
        level_1, level_1_name, map_text = status_list(map_id)
        print level_1, map_text
        # before save rest of the field will be null before save in assignstatutorycompliance
        data_list.append(domaintransactionprotocol.AssignStatutoryCompliance(
            level_1, level_1_name, map_text,
            r["statutory_provision"], r["compliance_id"], r["document_name"],
            r["compliance_task"], r["compliance_description"], orgs,
            None, None, None, None, unit_id

        ))

    for r in assigned_compliance :
        map_id = r["statutory_mapping_id"]
        orgs = organisation_list(map_id)
        level_1, level_1_name, map_text = status_list(map_id)
        print level_1, map_text
        # before save rest of the field will be null before save in assignstatutorycompliance
        data_list.append(domaintransactionprotocol.AssignStatutoryCompliance(
            level_1, level_1_name, map_text,
            r["statutory_provision"], r["compliance_id"], r["document_name"],
            r["compliance_task"], r["compliance_description"], orgs,
            r["statutory_applicable_status"], r["remarks"], r["compliance_applicable_status"], r["is_approved"],
            unit_id

        ))

    data_list.sort(key=lambda x : (x.level_one_id, x.compliance_id))
    return data_list

def save_client_statutories(db, request, user_id):
    status = request.submission_type
    comps = request.compliances_applicablity_status
    q = "INSERT INTO tbl_client_statutories(client_id, unit_id, status)" + \
        " values (%s, %s, %s)"

    saved_unit = None
    for c in comps :
        if saved_unit == c.unit_id :
            continue
        if c.client_statutory_id is None :
            csid = db.execute_insert(q, [c.client_id, c.unit_id, status])
            if csid is False :
                raise process_error("E088")
        else :
            csid = c.client_statutory_id

        saved_unit = c.unit_id

        save_statutory_compliances(
            db, comps,
            c.unit_id, status, user_id, csid
        )

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
    # is_saved = 0 , is_submmitted = 1, is_rejected = 2, is_assigned = 3, is_new = 4
    unit_id = request.unit_id
    domain_id = request.domain_id

    result = db.call_proc_with_multiresult_set("sp_clientstatutories_compliance_edit", [unit_id, domain_id], 5)
    statu = result[1]
    organisation = result[2]
    assigned_compliance = result[3]
    new_compliance = result[4]

    def organisation_list(map_id) :
        org_list = []
        for o in organisation :
            print o
            if o.get("statutory_mapping_id") == map_id :
                org_list.append(o["organisation_name"])
        return org_list

    def status_list(map_id):
        level_1_id = None
        map_text = None
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
                        map_text = " >> ".join(names[1:])
                        map_text += " >> %s" % (s["statutory_name"])
                    else :
                        map_text = s["statutory_name"]

        return level_1_id, level_1_s_name, map_text

    data_list = []
    for r in assigned_compliance :
        map_id = r["statutory_mapping_id"]
        orgs = organisation_list(map_id)

        level_1, level_1_s_name, map_text = status_list(map_id)
        print level_1, map_text
        # before save rest of the field will be null before save in assignstatutorycompliance
        data_list.append(domaintransactionprotocol.AssignStatutoryCompliance(
            level_1, level_1_s_name, map_text,
            r["statutory_provision"], r["compliance_id"], r["document_name"],
            r["compliance_task"], r["compliance_description"], orgs,
            r["statutory_applicable_status"], r["remarks"],
            r["compliance_applicable_status"], r["is_approved"], unit_id
        ))

    for r in new_compliance :
        map_id = r["statutory_mapping_id"]
        orgs = organisation_list(map_id)

        level_1, level_1_s_name, map_text = status_list(map_id)
        print level_1, map_text
        # before save rest of the field will be null before save in assignstatutorycompliance
        data_list.append(domaintransactionprotocol.AssignStatutoryCompliance(
            level_1, level_1_s_name, map_text,
            r["statutory_provision"], r["compliance_id"], r["document_name"],
            r["compliance_task"], r["compliance_description"], orgs,
            None, None, None, None, unit_id
        ))

    data_list.sort(key=lambda x : (x.level_one_id, x.compliance_id))
    return data_list
