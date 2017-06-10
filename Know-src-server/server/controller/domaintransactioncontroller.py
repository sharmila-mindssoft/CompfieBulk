from protocol import domaintransactionprotocol
from server.database.domaintransaction import *
from server.exceptionmessage import process_error

_all__ = ["process_domain_transaction_request"]

def process_domain_transaction_request(request, db, user_id):

    request_frame = request.request

    if type(request_frame) is domaintransactionprotocol.GetAssignedStatutories:
        result = process_get_approve_statutory_list(db, request_frame, user_id)

    elif type(
        request_frame
    ) is domaintransactionprotocol.GetAssignedStatutoryWizardOneData:
        result = process_get_assigned_statutory_wizard_one(
            db, user_id
        )

    elif type(
        request_frame
    ) is domaintransactionprotocol.GetAssignedStatutoryWizardOneUnits:
        result = process_get_statutory_units(
            db, request_frame, user_id
        )

    elif type(
        request_frame
    ) is domaintransactionprotocol.GetAssignedStatutoryWizardTwoCount:

        result = process_get_compliance_count(
            db, request_frame, user_id
        )

    elif type(
        request_frame
    ) is domaintransactionprotocol.GetAssignedStatutoryWizardTwoData:

        result = process_get_compliances_toassign(
            db, request_frame, user_id
        )

    elif type(request_frame) is domaintransactionprotocol.SaveAssignedStatutory :
        result = process_save_assign_satutory(db, request_frame, user_id)

    elif type(request_frame) is domaintransactionprotocol.GetAssignedStatutoriesById :
        result = process_get_assigned_compliance_byid(db, request_frame, user_id)

    elif type(request_frame) is domaintransactionprotocol.GetAssignedStatutoriesForApprove :
        result = process_get_assigned_statutory_approve_list(db, request_frame, user_id)

    elif type(request_frame) is domaintransactionprotocol.ApproveAssignedStatutory :
        result = process_approve_assigned_statutory(db, request_frame, user_id)

    elif type(request_frame) is domaintransactionprotocol.GetAssignedStatutoriesToApprove :
        result = process_get_assigned_statutory_to_approve(db, request_frame, user_id)

    return result

def process_get_approve_statutory_list(db, request, user_id):
    assigned_statutories, r_count = get_assigned_statutories_list(db, request, user_id)
    return domaintransactionprotocol.GetAssignedStatutoriesSuccess(
        assigned_statutories, r_count
    )

def process_get_assigned_statutory_wizard_one(db, user_id):
    return get_assigned_statutories_filters(db, user_id)


def process_get_statutory_units(db, request, user_id):
    return get_statutories_units(db, request, user_id)

def process_get_compliance_count(db, request, user_id):
    unit_total, total_comp = get_complinaces_count_to_assign(db, request, user_id)
    return domaintransactionprotocol.GetAssignedStatutoryWizardTwoCountSuccess(total_comp, unit_total)

def process_get_compliances_toassign(db, request, user_id):
    data = get_compliances_to_assign(db, request, user_id)
    unit_ids = request.unit_ids
    if len(unit_ids) > 1 :
        return domaintransactionprotocol.GetAssignedStatutoryWizardTwoMultipleDataSuccess(data)
    else :
        return domaintransactionprotocol.GetAssignedStatutoryWizardTwoDataSuccess(data, 0)


def process_save_assign_satutory(db, request, user_id):
    data = save_client_statutories(db, request, user_id)
    if data is True :
        return domaintransactionprotocol.SaveAssignedStatutorySuccess()

def process_get_assigned_compliance_byid(db, request, user_id):
    data = get_assigned_compliance_by_id(db, request, user_id)
    return domaintransactionprotocol.GetAssignedStatutoryWizardTwoDataSuccess(data, 0)

def process_get_assigned_statutory_approve_list(db, request, user_id):
    data = get_assigned_statutories_to_approve(db, request, user_id)
    # print data
    return domaintransactionprotocol.GetAssignedStatutoriesApproveSuccess(
        data
    )

def process_approve_assigned_statutory(db, request, user_id):
    data = save_approve_statutories(db, request, user_id)
    if data is True :
        return domaintransactionprotocol.ApproveAssignedStatutorySuccess()
    else :
        raise process_error("E088")

def process_get_assigned_statutory_to_approve(db, request, user_id):
    data, r_count = get_assigne_statu_compliance_to_approve(db, request, user_id)
    return domaintransactionprotocol.GetAssignedStatutoryWizardTwoDataSuccess(
        data, r_count
    )
