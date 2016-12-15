from protocol import (core, domaintransactionprotocol)
# from server.exceptionmessage import process_error
from server.database.tables import *
# from server.common import (get_date_time)

__all__ = [
    "get_assigned_statutories_list",
    "get_assigned_statutories_filters",
    "get_statutories_units", "get_compliances_to_assign"
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
        print (
            d["country_name"], d["client_id"], d["group_name"],
            d["business_group_name"], d["legal_entity_name"],
            d["division_name"], c_name, d["geography_name"],
            d["unit_id"], d["domain_id"], d["domain_name"], d["category_name"],
            d["is_approved"],
            core.ASSIGN_STATUTORY_APPROVAL_STATUS().value(d["is_approved"])
        )
        data_list.append(fn(
            d["country_name"], d["client_id"], d["group_name"],
            d["business_group_name"], d["legal_entity_name"],
            d["division_name"], c_name, d["geography_name"],
            d["unit_id"], d["domain_id"], d["domain_name"], d["category_name"],
            core.ASSIGN_STATUTORY_APPROVAL_STATUS().value(d["is_approved"]),
            d["is_approved"]
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
            r["address"], r["geography_name"]
        ))

    return domaintransactionprotocol.GetAssignedStatutoryWizardOneUnitsSuccess(
        data_list
    )

def get_compliances_to_assign(db, request, user_id):

    unit_id = request.unit_ids[0]
    domain_id = request.domain_id

    result = db.call_proc_with_multiresult_set("sp_clientstatutories_compliance_new", [unit_id, domain_id], 4)
    statu = result[1]
    organisation = result[2]
    compliance = result[3]

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
                if s["parent_ids"] == 0 :
                    level_1_id = s["statutory_id"]
                    map_text = s["statutory_name"]
                else :
                    names = [x.strip() for x in s["parent_names"].split('>>') if x != '']
                    ids = [int(y) for y in s["parent_ids"].split(',') if y != '']
                    level_1_id = ids[0]
                    map_text = " >> ".join(names[1:])

        return level_1_id, map_text

    data_list = []
    for r in compliance :
        map_id = r["statutory_mapping_id"]
        orgs = organisation_list(map_id)
        level_1, map_text = status_list(map_id)
        print level_1, map_text
        data_list.append(domaintransactionprotocol.AssignStatutoryCompliance(
            level_1, map_text,
            r["statutory_provision"], r["compliance_id"], r["document_name"],
            r["compliance_task"], r["compliance_description"],
            orgs
        ))
    return data_list
