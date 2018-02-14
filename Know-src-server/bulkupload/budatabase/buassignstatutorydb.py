from ..buapiprotocol import buassignstatutoryprotocol as bu_as

__all__ = [
    "get_client_list"
]
########################################################
# Return the uploaded statutory mapping csv list
# :param db : database class object
# :type db  : Object
# :param session_user : user id who currently logged in
# :type session_user : String
# :returns : upload_mmore : flag which defines user upload rights
# :returns : csv_data: list of uploaded csv_data
# rtypes: Boolean, lsit of Object
########################################################
def get_client_list(db, session_user):
    clients_data = []
    entitys_data = []
    units_data = []

    result = db.call_proc_with_multiresult_set("sp_client_info", [session_user], 3)


    clients = result[0]
    entitys = result[1]
    units = result[2]

    for c in clients :
        clients_data.append(bu_as.Clients(
            c["client_id"], c["group_name"]
        ))

    for e in entitys :
        entitys_data.append(bu_as.LegalEntites(
            e["client_id"], e["legal_entity_id"], e["legal_entity_name"]
        ))

    for u in units :
        units_data.append(bu_as.Units(
            u["legal_entity_id"], u["legal_entity_id"], u["domain_id"], u["domain_name"]
        ))

    return clients_data, entitys_data, units_data