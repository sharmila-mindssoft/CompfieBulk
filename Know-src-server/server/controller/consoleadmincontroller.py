###############################################################################
# This Controller will handle Console admin related requests
#
# In this module "db" is an object of "KnowledgeDatabase"
###############################################################################
from protocol import consoleadmin
from server.jsontocsvconverter import ConvertJsonToCSV
from server.database.consoleadmin import *


__all__ = [
    "process_console_admin_request"
]


###############################################################################
# process_client_coordination_master_request will process
# below mentioned request.
# parameter : request type is object of request class from clientcoordination
#   master protocol, db is database connection object.
# return :
#   return type is object of response class from
#   clientcoordination master protocol.
###############################################################################
def process_console_admin_request(request, db, session_user):
    request_frame = request.request

    if(type(request_frame) is consoleadmin.GetDatabaseServerList):
        result = process_get_db_server_list(db)

    elif(type(request_frame) is consoleadmin.SaveDBServer):
        result = process_save_db_server(db, request_frame, session_user)

    elif(
        type(request_frame) is consoleadmin.GetClientServerList
    ):
        result = process_get_client_server_list(db)

    elif(type(request_frame) is consoleadmin.SaveClientServer):
        result = process_save_client_server(db, request_frame, session_user)

    elif(
        type(request_frame) is consoleadmin.GetFileServerList
    ):
        result = process_get_file_server_list(db)

    elif(
        type(request_frame) is consoleadmin.SaveFileServer
    ):
        result = process_file_server_entry(db, request_frame, session_user)

    elif(type(request_frame) is consoleadmin.GetAllocatedDBEnv):
        result = process_get_allocated_db_env(db)

    elif(type(request_frame) is consoleadmin.SaveAllocatedDBEnv):
        result = process_save_allocated_db_env(db, request_frame, session_user)

    elif(type(request_frame) is consoleadmin.GetFileStorage):
        result = process_get_file_storage(db)

    elif(type(request_frame) is consoleadmin.SaveFileStorage):
        result = process_save_file_storage(db, request_frame, session_user)

    elif(type(request_frame) is consoleadmin.GetAutoDeletionList):
        result = process_get_auto_deletion_list(
            db, request_frame, session_user)

    elif(type(request_frame) is consoleadmin.SaveAutoDeletion):
        result = process_save_auto_deletion(
            db, request_frame, session_user)

    elif(type(request_frame) is consoleadmin.GetIPSettingsList):
        result = process_get_ip_settings_list(
            db, request_frame, session_user)

    elif(type(request_frame) is consoleadmin.GetGroupIPDetails):
        result = process_get_group_ip_details(
            db, request_frame, session_user)

    elif(type(request_frame) is consoleadmin.SaveIPSettings):
        result = process_save_ip_settings(
            db, request_frame, session_user)

    elif(type(request_frame) is consoleadmin.DeleteIPSettings):
        result = process_delete_ip_settings(
            db, request_frame, session_user)

    elif(type(request_frame) is consoleadmin.GetIPSettingsReportFilter):
        result = process_ip_setting_report_filter(
            db, request_frame, session_user)

    elif(type(request_frame) is consoleadmin.GetIPSettingsReport):
        result = process_ip_setting_report(
            db, request_frame, session_user)

    elif(type(request_frame) is consoleadmin.GetAllocateServerReportData):
        result = process_allocate_server_report_data(
            db, request_frame, session_user)

    elif(type(request_frame) is consoleadmin.ExportAllocateServerReportData):
        result = export_allocate_server_report_data(
            db, request_frame, session_user)

    return result


###############################################################################
# To get Database servers List
# parameter : Object of database
# return type : Returns Success response
###############################################################################
def process_get_db_server_list(db):
    db_servers = get_db_server_list(db)
    return consoleadmin.GetDbServerListSuccess(
        db_servers
    )


###############################################################################
# To save a database server
# parameter : Object of database, SaveDBServer Request, session user
# return type : Raises process error if save fails otherwise returns success
#               response
###############################################################################
def process_save_db_server(db, request, session_user):
    if is_duplicate_db_server_name(db, request.db_server_name, request.db_server_id):
        return consoleadmin.DBServerNameAlreadyExists()
    else:
        save_db_server(db, request, session_user)
        return consoleadmin.SaveDBServerSuccess()


###############################################################################
# To get client servers list
# parameter : Object of database
# return type : Returns success response
###############################################################################
def process_get_client_server_list(db):
    client_servers = get_client_server_list(db)
    return consoleadmin.GetClientServerListSuccess(
        client_servers
    )


###############################################################################
# To save client servers
# parameter : Object of database, Save Client server request
# return type : Raises process error if save fails otherwise returns success
#               response
###############################################################################
def process_save_client_server(db, request, session_user):
    if is_duplicate_client_server_name(
            db, request.client_server_name, request.client_server_id):
        return consoleadmin.ClientServerNameAlreadyExists()
    else:
        save_client_server(db, request, session_user)
        return consoleadmin.SaveClientServerSuccess()


###############################################################################
# To get list of all allocated database environments
# parameter : Object of database
# return type : Returns success response
###############################################################################
def process_get_allocated_db_env(db):
    (
        client_dbs_list, machines_list, db_servers_list, file_server_list
    ) = get_client_database_form_data(db)
    return consoleadmin.GetAllocatedDBEnvSuccess(
        client_dbs=client_dbs_list,
        client_server_name_and_id=machines_list,
        db_server_name_and_id=db_servers_list,
        file_server_list=file_server_list
    )


###############################################################################
# To save allocated database environment
# parameter : Object of database, Save Request, session user
# return type : Returns success response
###############################################################################
def process_save_allocated_db_env(db, request, session_user):
    save_allocated_db_env(db, request, session_user)
    return consoleadmin.SaveAllocatedDBEnvSuccess()


###############################################################################
# To get all file storage details
# parameter : Object of database
# return type : Returns success response
###############################################################################
def process_get_file_storage(db):
    (
        client_dbs_list, groups_list, les_list,
        machines_list
    ) = get_file_storage_form_data(db)
    return consoleadmin.GetFileStorageSuccess(
        file_storages=client_dbs_list, client_groups=groups_list,
        client_legal_entities=les_list,
        client_server_name_and_id=machines_list,
    )


###############################################################################
# To save file storage details
# parameter : Object of database, Save Request, session user
# return type : Returns success response
###############################################################################
def process_save_file_storage(db, request, session_user):
    save_file_storage(db, request, session_user)
    return consoleadmin.SaveFileStorageSuccess()


###############################################################################
# To get auto deletion details
# parameter : Object of database, Save Request, session user
# return type : Returns success response
###############################################################################
def process_get_auto_deletion_list(db, request, session_user):
    (
        groups_list, les_list, units_list
    ) = get_auto_deletion_form_data(db)
    return consoleadmin.GetAutoDeletionListSuccess(
        client_groups=groups_list, auto_deletion_entities=les_list,
        auto_deletion_units=units_list
    )


###############################################################################
# To save auto deletion details
# parameter : Object of database, Save Request, session user
# return type : Returns success response
###############################################################################
def process_save_auto_deletion(db, request, session_user):
    save_auto_deletion_details(db, request, session_user)
    return consoleadmin.SaveAutoDeletionSuccess()


###############################################################################
# To GET configure file server details
# parameter : Object of database, Get Request, session user
# return type : Returns file server records
###############################################################################
def process_get_file_server_list(db):
    file_server_list = get_file_server_list(db)
    return consoleadmin.GetFileServerListSuccess(file_server_list)


###############################################################################
# To save configure file server details
# parameter : Object of database, Save Request, session user
# return type : Returns success response
###############################################################################
def process_file_server_entry(db, request, session_user):
    if is_duplicate_file_server_name(
            db, request.file_server_name, request.file_server_id):
        return consoleadmin.FileServerNameAlreadyExists()
    else:
        file_server_entry_process(db, request, session_user)
        return consoleadmin.SaveFileServerSuccess()


###############################################################################
# To get ip setting details
# parameter : Object of database, Save Request, session user
# return type : Returns success response
###############################################################################
def process_get_ip_settings_list(db, request, session_user):
    (
        groups_list, forms_list, ips_list
    ) = get_ip_settings_form_data(db)
    return consoleadmin.GetIPSettingsListSuccess(
        client_groups=groups_list, ip_setting_forms=forms_list, ips_list=ips_list)


###############################################################################
# To get group ip details
# parameter : Object of database, Save Request, session user
# return type : Returns success response
###############################################################################
def process_get_group_ip_details(db, request, session_user):
    (
        group_ips_list
    ) = get_group_ip_details_form_data(db, request)
    return consoleadmin.GetGroupIPDetailsSuccess(
        group_ips_list=group_ips_list)

###############################################################################
# To save ip settings details
# parameter : Object of database, Save Request, session user
# return type : Returns success response
###############################################################################
def process_save_ip_settings(db, request, session_user):
    save_ip_setting_details(db, request, session_user)
    return consoleadmin.SaveIPSettingsSuccess()

###############################################################################
# To delete ip settings details
# parameter : Object of database, Save Request, session user
# return type : Returns success response
###############################################################################
def process_delete_ip_settings(db, request, session_user):
    delete_ip_setting_details(db, request, session_user)
    return consoleadmin.DeleteIPSettingsSuccess()

###############################################################################
# To get ip setting details report filter
# parameter : Object of database, Save Request, session user
# return type : Returns success response
###############################################################################
def process_ip_setting_report_filter(db, request, session_user):
    (
        groups_list, forms_list
    ) = get_ip_settings_report_filter(db)
    return consoleadmin.GetIPSettingsReportFilterSuccess(
        client_groups=groups_list, ip_setting_forms=forms_list
        )
###############################################################################
# To get ip settings report details
# parameter : Object of database, Get Request, session user
# return type : Returns success response
###############################################################################
def process_ip_setting_report(db, request, session_user):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "IPSettingReport"
        )
        return consoleadmin.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
    else:
        (
            total_records, group_ips_list
        ) = ip_setting_report_data(db, request, session_user)
        return consoleadmin.GetIPSettingsReportSuccess(
            total_records=total_records, group_ips_list=group_ips_list)


###############################################################################
# To get allocated server group, legal entity
# parameter : Object of database, session user
# return type : Returns success response
###############################################################################
def process_allocate_server_report_data(db, request, session_user):
    allocate_server_list = get_allocated_server_form_data(db)
    return consoleadmin.GetAllocatedDBListSuccess(allocate_server_list)

###############################################################################
# To xport allocated server group, legal entity
# parameter : Object of database, session user
# return type : Returns success response
###############################################################################
def export_allocate_server_report_data(db, request, session_user):
    print request.csv
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "AllocateServerReport"
        )
        return consoleadmin.ExportToCSVSuccess(
            link=converter.FILE_DOWNLOAD_PATH
        )
