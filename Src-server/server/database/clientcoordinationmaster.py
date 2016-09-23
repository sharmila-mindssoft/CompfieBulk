from protocol import (
    clientcoordinationmaster
)

__all__ = [
    "get_unit_approval_list"
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
