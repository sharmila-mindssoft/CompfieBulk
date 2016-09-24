from protocol import (
    clientcoordinationmaster
)

__all__ = [
    "get_unit_approval_list",
    "get_entity_units_list"
]


def get_unit_approval_list(db):
    data = db.call_proc(
        "sp_units_approval_list", None
    )
    return return_unit_approval_list(data)


def return_unit_approval_list(data):
    fn = clientcoordinationmaster.UnitApproval
    result = [
        fn(
            legal_entity_id=datum["legal_entity_id"],
            legal_entity_name=datum["legal_entity_name"],
            country_name=datum["country_name"],
            business_group_name=datum["business_group_name"],
            group_name=datum["group_name"], unit_count=datum["unit_count"]
        ) for datum in data
    ]
    return result


def get_entity_units_list(db, legal_entity_id):
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
