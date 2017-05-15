import MySQLdb as mysql
import requests
from server.exceptionmessage import process_error, fetch_run_error
from protocol import consoleadmin
from forms import *
from tables import *
from server.common import get_date_time
from server.database.validateEnvironment import ServerValidation, UpdateServerValidation
from server.database.createclientdatabase import ClientGroupDBCreate, ClientLEDBCreate

__all__ = [
    "get_db_server_list",
    "is_duplicate_db_server_name",
    "save_db_server",
    "get_client_server_list",
    "is_duplicate_client_server_name",
    "save_client_server",
    "get_client_database_form_data",
    "save_allocated_db_env",
    "get_file_storage_form_data",
    "save_file_storage",
    "get_auto_deletion_form_data",
    "save_auto_deletion_details",
    "get_file_server_list",
    "file_server_entry_process",
    "is_duplicate_file_server_name",
    "get_ip_settings_form_data",
    "get_group_ip_details_form_data",
    "save_ip_setting_details",
    "delete_ip_setting_details",
    "get_ip_settings_report_filter",
    "ip_setting_report_data",
    "get_allocated_server_form_data"
]


###############################################################################
# To get list of database servers
# parameter : Object of database
# return type : Returns List of object of DBServer
###############################################################################
def get_db_server_list(db):
    #
    #  To get list of all database servers
    #  Parameters : None
    #  Return : Returns all database servers
    #
    data = db.call_proc(
        "sp_databaseserver_list", None
    )
    print "db data"
    print data
    return return_database_servers(data)


###############################################################################
# To convert data fetched from database into a list of Object of DBServer
# parameter : Data fetched from database (Tuple of tuples)
# return type : Returns List of object of DBServer
###############################################################################
def return_database_servers(data):
    fn = consoleadmin.DBServer
    result = []
    for datum in data:
        no_of_clients = 0
        if datum["legal_entity_ids"] is not None and datum["legal_entity_ids"] != "" :
            if datum["legal_entity_ids"].find(",") >= 0:
                no_of_clients = len(datum["legal_entity_ids"].split(","))
            else:
                no_of_clients = 1

        result.append(
            fn(
                db_server_id=datum["database_server_id"], db_server_name=datum["database_server_name"],
                ip=datum["database_ip"], port=datum["database_port"],
                username=datum["database_username"], password=datum["database_password"],
                no_of_clients=no_of_clients
            )
        )
    return result


###############################################################################
# To check whether the db server name already exists or not
# parameter : Object of database, db server name, ip
# return type : Returns True if db server name already exists otherwise returns
#               False
###############################################################################
def is_duplicate_db_server_name(db, db_server_name, db_server_id):
    #
    #  To check whether db server name already exists or not
    #  Parameters : Db server name, ip
    #  Return : returns count of db servers exists with the save name
    #
    result = db.call_proc(
        "sp_databaseserver_is_duplicate", (db_server_name, db_server_id))
    if result[0]["count"] > 0:
        return True
    else:
        return False


###############################################################################
# To save db server
# parameter : Object of database, Save DB server request, session user
# return type : Returns True if db server name already exists otherwise returns
#               False
###############################################################################
def save_db_server(db, request, session_user):
    #
    #  To save database server
    #  Parameters : Db server name, ip, port, username, password
    #  Return : returns last inserted row id
    #
    # try:
        is_valid = validate_database_server_before_save(db, request)
        if is_valid is not True:
            raise fetch_run_error(is_valid)
        db.call_insert_proc(
            "sp_databaseserver_save", (
                request.db_server_id, request.db_server_name, request.ip,
                request.port, request.username, request.password, session_user,
                get_date_time()
            )
        )
        if request.db_server_id is None:
            action = "New Database server %s added" % (request.db_server_name)
        else:
            action = "Database server %s updated" % (request.db_server_name)
        db.save_activity(session_user, frmConfigureDatabaseServer, action)
    # except:
    #     raise process_error("E074")

def validate_database_server_before_save(db, request):
        dhost = request.ip
        uname = request.username
        pwd = request.password
        port = request.port
        try :
            connection = mysql.connect(host=dhost, user=uname, passwd=pwd, port=port)
            c = connection.cursor()
            c.close()
            connection.close()
            return True
        except mysql.Error, e :
            print e
            if(e[0] == 1045):
                return "Invalid Database Credentials"
            else:
                return "Database server connection failed"
###############################################################################
# To Get list of client servers
# parameter : Object of database
# return type : Returns list of object of ClientServer
###############################################################################
def get_client_server_list(db):
    #
    #  To get list of client servers
    #  Parameters : None
    #  Return : Returns all client servers
    #
    data = db.call_proc(
        "sp_machines_list", None
    )
    return return_client_servers(data)


###############################################################################
# To convert data fetched from database into list of Object of Client Server
# parameter : Data fetched from database (Tuple of tuples)
# return type : Returns list of object of ClientServer
###############################################################################
def return_client_servers(data):
    fn = consoleadmin.ClientServer
    result = []
    for datum in data:
        no_of_clients = []
        if datum["client_ids"] is not None and datum["client_ids"] != "":
            no_of_clients = datum["client_ids"].split(",")
        result.append(
            fn(
                client_server_id=datum["machine_id"],
                client_server_name=datum["machine_name"], ip=datum["ip"],
                port=datum["port"], no_of_clients=len(no_of_clients)
            )
        )
    return result


###############################################################################
# To check whether the client server name already exists or not
# parameter : Object of database, client server name, client server id
# return type : Returns True if a duplicate cilent server name already exists
#               Otherwise returns False
###############################################################################
def is_duplicate_client_server_name(db, client_server_name, client_server_id):
    #
    #  To check whether the client server name already exists or not
    #  Parameters : Client server name, client server id
    #  Return : Returns count of client server with the same name
    #
    result = db.call_proc(
        "sp_machines_is_duplicate", (client_server_name, client_server_id))
    if result[0]["count"] > 0:
        return True
    else:
        return False


###############################################################################
# To Save Client server
# parameter : Object of database, Save Client server request, session user
# return type : Raises process error if saving client server fails otherwise
#                returns None
###############################################################################
def save_client_server(db, request, session_user):
    #
    #  To save client server
    #  Parameters : Client server id, Client server name, ip, port
    #  Return : returns last inserted id
    #
    # try:
        is_valid = validate_application_server_before_save(request)
        if is_valid is not True:
            raise fetch_run_error(is_valid)
        print "args"
        print request.client_server_id, request.client_server_name, request.ip, request.port
        new_id = db.call_insert_proc(
            "sp_machines_save", (
                request.client_server_id, request.client_server_name,
                request.ip, request.port, session_user, get_date_time()
            )
        )
        print "new_id"
        print new_id
        action = "New %s added" % (request.client_server_name)
        print action
        if request.client_server_id is not None:
            action = "%s updated" % (request.client_server_name)
        db.save_activity(session_user,  frmConfigureApplicationServer, action)
    # except Exception, e:
    #     print e
    #     raise process_error("E075")

def validate_application_server_before_save(request):
    port = request.port
    ip = request.ip
    try :
        r = requests.post("http://%s:%s/api/isalive" % (ip, port))
        print r
        print "-" * 50
        if r.status_code != 200 :
            return "Application server connection failed"
        else :
            return True

    except :
        raise RuntimeError("Application server connection failed")
###############################################################################
# To Get data required for allocating database environment
# parameter : Object of database
# return type : Returns tuple of Lists. List contains client databases,
#               Client groups, Legal entities, Client Servers, DB Servers
###############################################################################
def get_client_database_form_data(db):
    #
    #  To get data required for allocating database environment
    #  Parameters : None
    #  Return : returns list of Client db environments, Client groups,
    #   Legal entities, Client servers and Database servers
    #
    data = db.call_proc_with_multiresult_set(
        "sp_clientdatabase_list", None, 4)
    print data
    client_dbs = data[0]
    machines = data[1]
    db_servers = data[2]
    file_servers = data[3]
    client_dbs_list = return_client_dbs(client_dbs)
    machines_list = return_machines(machines)
    db_servers_list = return_db_servers(db_servers)
    file_servers_list = return_File_servers_List(file_servers)
    return (
        client_dbs_list, machines_list, db_servers_list, file_servers_list
    )


###############################################################################
# Convert data fetched from database into List of object of ClientDatabase
# parameter : Data fetched from database (Tuple of tuples)
# return type : Returns List of object of ClientDatabase
###############################################################################
def return_client_dbs(data):
    fn = consoleadmin.ClientDatabase
    client_dbs = [
        fn(
            client_database_id=datum["client_database_id"],
            client_id=datum["client_id"],
            group_name=datum["group_name"],
            legal_entity_id=datum["legal_entity_id"],
            legal_entity_name=datum["legal_entity_name"],
            machine_id=datum["machine_id"],
            machine_name=datum["machine_name"],
            client_db_server_id=datum["client_database_server_id"],
            client_db_server_name=datum["client_database_server_name"],
            db_server_id=datum["database_server_id"],
            db_server_name=datum["database_server_name"],
            file_server_id=datum["file_server_id"],
            file_server_name=datum["file_server_name"],
            is_created=bool(datum["is_created"])
        ) for datum in data
    ]
    return client_dbs


###############################################################################
# Convert data fetched from database into List of object of ClientGroup
# parameter : Data fetched from database (Tuple of tuples)
# return type : Returns List of object of ClientGroup
###############################################################################
def return_client_groups(data):
    fn = consoleadmin.ClientGroup
    client_groups = [
        fn(
            client_id=datum["client_id"],
            group_name=datum["group_name"]
        ) for datum in data
    ]
    return client_groups


###############################################################################
# Convert data fetched from database into List of object of LegalEntity
# parameter : Data fetched from database (Tuple of tuples)
# return type : Returns List of object of LegalEntity
###############################################################################
def return_legal_entites(data):
    fn = consoleadmin.LegalEntity
    legal_entites = [
        fn(
            legal_entity_id=datum["legal_entity_id"],
            legal_entity_name=datum["legal_entity_name"],
            client_id=datum["client_id"]
        ) for datum in data
    ]
    return legal_entites


###############################################################################
# Convert data fetched from database into List of object of Machines
# parameter : Data fetched from database (Tuple of tuples)
# return type : Returns List of object of ClientServerNameAndID
###############################################################################
def return_machines(data):
    fn = consoleadmin.ClientServerNameAndID
    client_server_name_and_id = [
        fn(
            machine_id=datum["machine_id"],
            machine_name=datum["machine_name"],
            ip=datum["ip"],
            port=datum["port"],
            console_cl_ids=datum["client_ids"]
        ) for datum in data
    ]
    return client_server_name_and_id


###############################################################################
# Convert data fetched from database into List of object of DBServerNameAndID
# parameter : Data fetched from database (Tuple of tuples)
# return type : Returns List of object of DBServerNameAndID
###############################################################################
def return_db_servers(data):
    fn = consoleadmin.DBServerNameAndID
    db_servers_name_and_id = [
        fn(
           db_server_id=datum["database_server_id"], db_server_name=datum["database_server_name"],
           database_server_ip=datum["database_ip"], port=datum["database_port"],
           console_le_ids=datum["legal_entity_ids"]
        ) for datum in data
    ]
    return db_servers_name_and_id


###############################################################################
# Convert data fetched from database into List of object of FileServerNameAndID
# parameter : Data fetched from database (Tuple of tuples)
# return type : Returns List of object of FileServerNameAndID
###############################################################################
def return_File_servers_List(data):
    fn = consoleadmin.AllocateFileServerList
    file_servers_name_and_id = [
        fn(
           file_server_id=datum["file_server_id"], file_server_name=datum["file_server_name"],
           ip=datum["ip"], port=datum["port"], console_le_ids=datum["legal_entity_ids"]
        ) for datum in data
    ]
    return file_servers_name_and_id


###############################################################################
# To Save allocated databse environment
# parameter : Object of database, Save Allocated database environment request
# return type : Raises process error if save fails otherwise returns None
###############################################################################
def validated_env_before_save(db, request):
    client_db_id = request.client_database_id
    db_server_id = request.db_server_id
    le_db_server_id = request.le_db_server_id
    machine_id = request.machine_id
    file_server_id = request.file_server_id
    legal_entity_id = request.legal_entity_id
    client_id = request.client_id
    if client_db_id is None:
        vobj = ServerValidation(db, machine_id, db_server_id, file_server_id)
        is_valid = vobj.perform_validation()
        print is_valid
        if is_valid[0] is not True :
            return is_valid[0]
        elif is_valid[1] is not True :
            return is_valid[1]
        elif is_valid[2] is not True :
            return is_valid[2]
        else :
            return True
    else:
        vobj = UpdateServerValidation(db, client_db_id, legal_entity_id, client_id, machine_id, db_server_id, le_db_server_id, file_server_id)
        is_valid = vobj.perform_update_validation()
        if is_valid[0] is not True :
            return is_valid[0]
        elif is_valid[1] is not True :
            return is_valid[1]
        elif is_valid[2] is not True :
            return is_valid[2]
        elif is_valid[3] is not True :
            return is_valid[3]
        else :
            return True

def create_db_process(db, client_database_id, client_id, legal_entity_id, db_server_id, le_db_server_id):

    def save_db_name(db_name, db_user, db_password, is_group):
        dbowner = client_id
        if is_group is False :
            dbowner = legal_entity_id
        db.call_insert_proc("sp_clientdatabase_dbname_info_save", [client_database_id, db_user, db_password, dbowner, db_name, int(is_group)])

    def _create_db(_db_info, short_name, email_id, is_group):
        if is_group :
            create_db = ClientGroupDBCreate(
                db, client_id, short_name, email_id,
                _db_info.get("database_ip"),
                _db_info.get("database_port"),
                _db_info.get("database_username"),
                _db_info.get("database_password")
            )
            is_db_created = create_db.begin_process()
            if is_db_created[0] is True :
                create_db._save_master_info()
                save_db_name(is_db_created[1], is_db_created[2], is_db_created[3], True)
        else :
            create_db = ClientLEDBCreate(
                db, client_id, short_name, email_id,
                _db_info.get("database_ip"),
                _db_info.get("database_port"),
                _db_info.get("database_username"),
                _db_info.get("database_password"),
                legal_entity_id
            )
            is_db_created = create_db.begin_process()
            if is_db_created[0] is True :
                print "save process"
                create_db._save_master_info()
                save_db_name(is_db_created[1], is_db_created[2], is_db_created[3], False)

    # db information for both client and legal entity
    client_db_info = db.call_proc_with_multiresult_set("sp_tbl_client_groups_createdb_info", [client_id, db_server_id, le_db_server_id], 2)
    c_info = client_db_info[0][0]
    db_info = client_db_info[1]
    print client_db_info
    print [client_id, db_server_id, le_db_server_id]
    print c_info
    count = c_info.get("cnt")

    _db_group_info = None
    _db_le_info = None

    for r in db_info :
        if r["database_server_id"] == db_server_id :
            _db_group_info = r
        if r["database_server_id"] == le_db_server_id :
            _db_le_info = r

    # create group db
    print count
    if count == 1 :
        if _db_group_info :
            is_done = _create_db(_db_group_info, c_info.get("short_name"), c_info.get("email_id"), True)
            print is_done

    # create le db

    if _db_le_info :
        is_done = _create_db(_db_le_info, c_info.get("short_name"), c_info.get("email_id"), False)
        print is_done

    return is_done

def save_allocated_db_env(db, request, session_user):
    is_valid = validated_env_before_save(db, request)
    if is_valid is not True:
        raise fetch_run_error(is_valid)

    client_id = request.client_id
    legal_entity_id = request.legal_entity_id
    client_db_id = request.client_database_id
    print client_db_id
    db_server_id = request.db_server_id
    machine_id = request.machine_id
    le_db_server_id = request.le_db_server_id
    file_server_id = request.file_server_id
    client_ids = request.console_cl_ids
    legal_entity_ids = request.console_le_ids
    f_legal_entity_ids = request.console_f_le_ids
    le_legal_entity_ids = request.console_le_le_ids
    print "new"
    print request.new_le_le_ids
    #
    #  To save allocated database environment
    #  Parameters : client id, legal entity id, database ip, client server id
    #  Return : List of allocated database environment details
    #
    # try:
    if client_db_id is None:
        try :
            client_db_id = db.call_insert_proc(
                "sp_clientdatabase_save",
                (client_id, legal_entity_id, machine_id, db_server_id, le_db_server_id, file_server_id,
                    client_ids, legal_entity_ids, session_user, get_date_time())
            )
            create_db_process(db, client_db_id, client_id, legal_entity_id, db_server_id, le_db_server_id)

        except Exception, e :
            print e
            raise Exception(e)

    else:
        db.call_insert_proc(
            "sp_clientdatabase_update",
            (client_db_id, client_id, legal_entity_id, machine_id, db_server_id, le_db_server_id, file_server_id,
                client_ids, legal_entity_ids, request.old_grp_app_id, request.old_grp_db_s_id, request.old_le_db_s_id,
                request.old_le_f_s_id, request.new_cl_ids, request.new_grp_le_ids, request.new_le_le_ids,
                request.new_le_f_s_ids, session_user, get_date_time(), f_legal_entity_ids, le_legal_entity_ids)
        )
    #
    #  To get legal entity name by it's id to save activity
    #  Parameters : legal entity id
    #  Return : Returns legal entity name
    #
    print "legal_entity_id : %s" % legal_entity_id
    data = db.call_proc("sp_legal_entity_name_by_id", (legal_entity_id,))
    print "data: %s" % data
    action = "Allocated database environment for %s " % (
        data[0]["legal_entity_name"])
    db.save_activity(session_user, frmAllocateDatabaseEnvironment, action)

    # Notification Message
    current_time_stamp = str(get_date_time())
    if client_db_id is None:
        db.call_insert_proc("sp_allocate_server_message_save", (session_user, "Save", client_id, current_time_stamp))
        return True
    else:
        db.call_insert_proc("sp_allocate_server_message_save", (session_user, "Update", client_id, current_time_stamp))
        return True

    # perform db creation

    # except Exception, e:
    #     print e
    #     raise process_error("E076")


###############################################################################
# To Get data required for Configuring file storage
# parameter : Object of database
# return type : Tuple of Lists. List contains File Storage details list,
#  Client Group list, Legal entities list and Client servers list
###############################################################################
def get_file_storage_form_data(db):
    #
    #  To get list of form data for configuring file storage
    #  Parameters : None
    #  Return : Returns file storage details, Client group details,
    #   Legal entity details, Client server details
    #
    data = db.call_proc_with_multiresult_set(
        "sp_clientfilestorage_list", None, 4)
    file_storages = data[0]
    groups = data[1]
    les = data[2]
    machines = data[3]
    file_storages_list = return_file_storages(file_storages)
    groups_list = return_client_groups(groups)
    les_list = return_legal_entites(les)
    machines_list = return_machines(machines)
    return (
        file_storages_list, groups_list, les_list,
        machines_list
    )


###############################################################################
# To convert data fetched from database into List of object of FileStorage
# parameter : Data fetched from database (Tuple of tuples)
# return type : Returns List of object of FileStorage
###############################################################################
def return_file_storages(data):
    fn = consoleadmin.FileStorage
    file_storages = [
        fn(
            client_id=datum["client_id"],
            legal_entity_id=datum["legal_entity_id"],
            machine_id=datum["machine_id"]
        ) for datum in data
    ]
    return file_storages


###############################################################################
# To Save File storage configuration
# parameter : Object of database, Save file storage request
# return type : Returns List of object of FileStorage
###############################################################################
def save_file_storage(db, request, session_user):
    client_id = request.client_id
    legal_entity_id = request.legal_entity_id
    machine_id = request.machine_id
    #
    #  To save file storage configuration
    #  Parameters : Client id, Legal entity id, Clietn server id
    #  Return : Returns last inserted id
    #
    result = db.call_update_proc(
        "sp_clientfilestorage_save",
        (client_id, legal_entity_id, machine_id)
    )
    if result:
        #
        #  To get legal entity name by it's id to save activity
        #  Parameters : legal entity id
        #  Return : Returns legal entity name
        #
        data = db.call_proc("sp_legal_entity_name_by_id", (legal_entity_id,))
        action = "Configured file storage for %s " % (
            data[0]["legal_entity_name"])
        db.save_activity(session_user, frmConfigureFileStorage, action)
    else:
        raise process_error("E077")


###############################################################################
# To get data required for Auto deletion form
# parameter : Object of database
# return type : Returns Tuple of lists. List contains Client Groups list,
#  Legal entities list, Units List
###############################################################################
def get_auto_deletion_form_data(db):
    #
    #  To get data required for auto deletion form
    #  Parameters : None
    #  Return : Returns Client group details, Legal entity details and
    #   Unit details
    #
    data = db.call_proc_with_multiresult_set(
        "sp_unit_autodeletion_list", None, 4)
    groups = data[0]
    les = data[1]
    units = data[2]
    groups_list = return_client_groups(groups)
    les_list = return_auto_deletion_legal_entites(les)
    units_list = return_units(units)
    return (
        groups_list, les_list, units_list
    )


###############################################################################
# To convert data fetched from database into List of object of
# EntitiesWithAutoDeletion
# parameter : Data fetched from database (Tuple of tuples)
# return type : Returns List of object of EntitiesWithAutoDeletion
###############################################################################
def return_auto_deletion_legal_entites(data):
    fn = consoleadmin.EntitiesWithAutoDeletion
    result = [
        fn(
            legal_entity_id=datum["legal_entity_id"],
            legal_entity_name=datum["legal_entity_name"],
            client_id=datum["client_id"],
            unit_count=datum["unit_count"],
            deletion_period=datum["deletion_period"],
            is_closed=bool(datum["is_closed"])
        ) for datum in data
    ]
    return result


###############################################################################
# To convert data fetched from database into List of object of Unit
# parameter : Data fetched from database (Tuple of tuples)
# return type : Returns List of object of Unit
###############################################################################
def return_units(data):
    fn = consoleadmin.Unit
    result = [
        fn(
            unit_id=datum["unit_id"], client_id=datum["client_id"],
            legal_entity_id=datum["legal_entity_id"],
            unit_code=datum["unit_code"], address=datum["address"],
            unit_name=datum["unit_name"], deletion_period=datum["deletion_period"]
        ) for datum in data
    ]
    return result


###############################################################################
# To save auto deletion details
# parameter : Object of databse, Save Auto deletion request, session user
# return type : Returns True on success full save. Otherwise raises
#   process error
###############################################################################
def save_auto_deletion_details(db, request, session_user):
    auto_deletion_details = request.auto_deletion_details
    unit_ids = []
    insert_columns = [
        "client_id", "legal_entity_id", "unit_id", "deletion_period"
    ]
    insert_values = []
    legal_entity_id = None
    for detail in auto_deletion_details:
        unit_ids.append(detail.unit_id)
        legal_entity_id = detail.legal_entity_id
        insert_values.append(
            (
                detail.client_id, detail.legal_entity_id,
                detail.unit_id, detail.deletion_period
            )
        )
    #
    #  To delete all auto deletion details under the legal entity
    #  Parameters : Legal entity id
    #  Return : True on successfull deletion otherwise returns False
    #
    db.call_update_proc("sp_unitautodeletion_delete", (legal_entity_id,))
    result = db.bulk_insert(
        tblAutoDeletion, insert_columns, insert_values
    )
    if result:
        #
        #  To get legal entity name by it's id to save activity
        #  Parameters : legal entity id
        #  Return : Returns legal entity name
        #
        data = db.call_proc("sp_legal_entity_name_by_id", (legal_entity_id,))
        action = "Configured auto deletion for %s " % (
            data[0]["legal_entity_name"])
        db.save_activity(session_user, frmAutoDeletion, action)
    else:
        raise process_error("E078")


###############################################################################
# To Get list of file servers
# parameter : Object of database
# return type : Returns list of object of FileServer
###############################################################################
def get_file_server_list(db):
    #
    #  To get list of file servers
    #  Parameters : None
    #  Return : Returns all file servers
    #
    data = db.call_proc(
        "sp_file_server_list", None
    )
    return return_file_servers(data)


###############################################################################
# Convert data fetched from database into List of object of File Servers
# parameter : Data fetched from database (Tuple of tuples)
# return type : Returns List of object of File server name and id
###############################################################################
def return_file_servers(data):
    file_server_list = []
    for datum in data:
        no_of_clients = 0
        if(datum["legal_entity_ids"] is not None and datum["legal_entity_ids"] != ""):
            no_of_clients = len(datum["legal_entity_ids"].split(","))

        file_server_list.append(consoleadmin.FileServerList(
            datum["file_server_id"], datum["file_server_name"],
            datum["ip"], datum["port"], no_of_clients
        ))
    return file_server_list


###############################################################################
# To check whether the file server name already exists or not
# parameter : Object of database, file server name, file server id
# return type : Returns True if a duplicate file server name already exists
#               Otherwise returns False
###############################################################################
def is_duplicate_file_server_name(db, file_server_name, file_server_id):
    #
    #  To check whether the client server name already exists or not
    #  Parameters : Client server name, client server id
    #  Return : Returns count of client server with the same name
    #
    result = db.call_proc(
        "sp_file_server_is_duplicate", (file_server_name, file_server_id))
    if result[0]["count"] > 0:
        return True
    else:
        return False

###############################################################################
# To save file server details
# parameter : Object of databse, Save file server request, session user
# return type : Returns True on success full save. Otherwise raises
#   process error
###############################################################################
def file_server_entry_process(db, request, user_id):
    #
    #  To save client server
    #  Parameters : Client server id, Client server name, ip, port
    #  Return : returns last inserted id
    #
    # try:
        is_valid = validate_file_server_before_save(request)
        if is_valid is not True:
            raise fetch_run_error(is_valid)
        print "args"
        print request.file_server_id, request.file_server_name, request.ip, request.port
        new_id = db.call_insert_proc(
            "sp_file_server_entry", (
                request.file_server_id, request.file_server_name,
                request.ip, request.port, user_id, get_date_time()
            )
        )
        print "new_id"
        print new_id
        action = "New File Server %s added" % (request.file_server_name)
        print action
        if request.file_server_id is not None:
            action = "File Server %s updated" % (request.file_server_name)
        db.save_activity(user_id,  frmConfigureFileServer, action)
    # except Exception, e:
    #     print e
    #     raise process_error("E078")


def validate_file_server_before_save(request):
    port = request.port
    ip = request.ip
    try :
        r = requests.post("http://%s:%s/api/isfilealive" % (ip, port))
        print r
        print "-" * 50
        if r.status_code != 200 :
            return "File server connection failed"
        else :
            return True

    except :
        raise RuntimeError("File server connection failed")


def get_ip_settings_form_data(db):
    #
    #  To get data required for ip settings form
    #  Parameters : None
    #  Return : Returns Client group details and
    #   form details
    #
    data = db.call_proc_with_multiresult_set(
        "sp_ip_settings_list", None, 3)
    groups = data[0]
    forms = data[1]
    ipslist = data[2]
    groups_list = return_client_groups(groups)
    forms_list = return_forms(forms)
    ips_list = return_ipslist(ipslist)
    return (
        groups_list, forms_list, ips_list
    )

###############################################################################
# To convert data fetched from database into List of object of Unit
# parameter : Data fetched from database (Tuple of tuples)
# return type : Returns List of object of Form List
###############################################################################
def return_forms(data):
    fn = consoleadmin.Form
    result = [
        fn(
            form_id=datum["form_id"], form_name=datum["form_name"]
        ) for datum in data
    ]
    return result

def return_ipslist(data):
    fn = consoleadmin.IPSettingsList
    result = [
        fn(
            client_id=datum["client_id"], form_id=datum["form_id"], group_name=datum["group_name"]
        ) for datum in data
    ]
    return result

def get_group_ip_details_form_data(db, request):
    #
    #  To get data required for group ip details
    #  Parameters : None
    #  Return : Returns Client groupis IP details
    #
    data = db.call_proc(
        "sp_group_ip_details", [request.client_id]
    )
    group_ips_list = return_group_ipslist(data)
    return (
        group_ips_list
    )

def return_group_ipslist(data):
    fn = consoleadmin.GroupIPDetails
    result = [
        fn(
            form_id=datum["form_id"], ip=datum["ips"], client_id=datum["client_id"]
        ) for datum in data
    ]
    return result

###############################################################################
# To save ip setting details
# parameter : Object of databse, Save Auto deletion request, session user
# return type : Returns True on success full save. Otherwise raises
#   process error
###############################################################################
def save_ip_setting_details(db, request, session_user):
    ip_setting_details = request.group_ips_list
    insert_columns = [
        "client_id", "form_id", "ips"
    ]
    insert_values = []
    client_id = None
    for detail in ip_setting_details:
        #unit_ids.append(detail.unit_id)
        client_id = detail.client_id
        insert_values.append(
            (
                detail.client_id, detail.form_id,
                detail.ip
            )
        )
    #
    #  To delete all ip setting details under the legal entity
    #  Parameters : client id
    #  Return : True on successfull deletion otherwise returns False
    #
    db.call_update_proc("sp_ip_settings_delete", (client_id,))
    result = db.bulk_insert(
        tblIPSettings, insert_columns, insert_values
    )
    if result:
        #
        #  To get legal entity name by it's id to save activity
        #  Parameters : legal entity id
        #  Return : Returns legal entity name
        #
        data = db.call_proc("sp_group_name_by_id", (client_id,))
        action = "Configured ip settings for %s " % (
            data[0]["group_name"])
        db.save_activity(session_user, frmIPSettings, action)

        admin_users_id = []
        res = db.call_proc("sp_users_under_user_category", (1,))
        for user in res:
            admin_users_id.append(user["user_id"])

        if len(admin_users_id) > 0:
            db.save_toast_messages(1, "Form Authorization-IP Setting", "IP level restrictions has been enabled for \""+ data[0]["group_name"] + "\" ", None, admin_users_id, session_user)
            
    else:
        raise process_error("E078")

###############################################################################
# To delete ip setting details
# parameter : Object of databse, Save Auto deletion request, session user
# return type : Returns True on success full save. Otherwise raises
#   process error
###############################################################################
def delete_ip_setting_details(db, request, session_user):
    client_id = request.client_id
    db.call_update_proc("sp_ip_settings_delete", (client_id,))


###############################################################################
# To get ip setting report details
# parameter : Object of databse, report request, session user
# return type : Returns report data.
###############################################################################
def ip_setting_report_data(db, request, session_user):
    client_id = request.client_id
    ip = request.ip
    f_count = request.from_count
    t_count = request.page_count

    data = db.call_proc_with_multiresult_set(
        "sp_ip_setting_details_report", (client_id, ip, f_count, t_count), 2)

    total_records = data[0][0]["total_record"]
    ips_list = return_group_ipslist(data[1])
    return (
        total_records, ips_list
    )

def get_ip_settings_report_filter(db):
    #
    #  To get data required for ip settings form
    #  Parameters : None
    #  Return : Returns Client group details and
    #   form details
    #
    data = db.call_proc_with_multiresult_set(
        "sp_ip_settings_report_filter", None, 2)
    groups = data[0]
    forms = data[1]
    groups_list = return_client_groups(groups)
    forms_list = return_forms(forms)
    return (
        groups_list, forms_list
    )


###############################################################################
# To get allocated server details
# parameter : Object of databse
# return type : Returns records of allocated server lost
#   process error
###############################################################################
def get_allocated_server_form_data(db):
    result = db.call_proc("sp_allocate_db_environment_report_getdata", None)
    allocate_db_report = []
    if(result is not None):
        for row in result:
            allocate_db_report.append(consoleadmin.AllocateDBList(
                    client_id=row["client_id"], group_name=row["group_name"],
                    legal_entity_id=row["legal_entity_id"],
                    legal_entity_name=row["legal_entity_name"],
                    machine_id=row["machine_id"], machine_name=row["machine_name"],
                    client_db_server_id=row["client_database_server_id"],
                    client_db_server_name=row["client_db_server_name"],
                    db_server_id=row["database_server_id"], db_server_name=row["db_server_name"],
                    file_server_id=row["file_server_id"],
                    file_server_name=row["file_server_name"]
                )
            )
        return allocate_db_report
