from protocol import clientcoordinationmaster
from server.database.clientcoordinationmaster import *

__all__ = [
    "process_client_coordination_master_request"
]


def process_client_coordination_master_request(request, db):
    unit_approval_list = get_unit_approval_list(db)
    return clientcoordinationmaster.GetClientUnitApprovalListSuccess(
        unit_approval_list)
