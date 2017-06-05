from protocol import ( core, technomasters, admin, generalprotocol )
from server.database.forms import *
from server.exceptionmessage import process_error, process_error_with_msg
from server.constants import (CLIENT_LOGO_PATH)
from server.common import ( datetime_to_string, get_date_time, string_to_datetime, get_system_date,
                            remove_uploaded_file, convert_base64_to_file, new_uuid )
from server.database.tables import *
from server.database.validateclientuserrecord import ClientAdmin
import datetime

##########################################################################
#  To get countries assigned to the session user
#  Parameters : Object of database and  session user id (int)
#  Return Type : List of object of Country
##########################################################################
def get_user_countries(db, session_user):
    result = db.call_proc_with_multiresult_set("sp_countries_for_user", (session_user,), 2)
    if len(result) > 1:
        result = result[1]
    return return_countries(result)

##########################################################################
#  To convert the data fetched from database to list of object of country
#  Parameters : Data fetched from database (Tuple of tuples)
#  Return Type : List of object of Country
##########################################################################
def return_countries(data):
    fn = core.Country
    results = [ fn( d["country_id"], d["country_name"], bool(d["is_active"]) ) for d in data]
    return results

##########################################################################
#  To Get business groups under a client
#  Parameters : Object of database and client id
#  Return Type : List of object of BusinessGroup
##########################################################################
def get_client_business_groups(db, client_id):
    business_groups = db.call_proc("sp_business_groups_list", (client_id,) )
    results = []
    for business_group in business_groups:
        results.append(core.ClientBusinessGroupCountry(business_group["business_group_id"],
            business_group["business_group_name"], business_group["client_id"], business_group["country_id"]))
    return results

##########################################################################
#  To convert the data fetched from database to list of
#  Object of Business group
#  Parameters : Data fetched from database (tuple of tuples)
#  Return Type List of object of BusinessGroup
##########################################################################
def return_business_groups(business_groups):
    results = []
    for business_group in business_groups:
        results.append(core.BusinessGroup( business_group["business_group_id"],
        business_group["business_group_name"], business_group["client_id"] ))
    return results

##########################################################################
#  To get domains assigned to the session user
#  Parameters : Object of database and  session user id (int)
#  Return Type : List of object of Domain
##########################################################################
def get_user_domains(db, session_user):
    result = db.call_proc_with_multiresult_set('sp_tbl_domains_for_user', (session_user,), 3)
    result.pop(0)
    return return_domains(result)

##########################################################################
#  To get all active industries
#  Parameters : Object of database
#  Return Type : List of object of Industry
##########################################################################
def get_active_industries(db):
    domains = db.call_proc( "sp_industries_active_list", None)
    return return_industries(domains)

##########################################################################
#  To convert data fetched from database into list of object of Industry
#  Parameters : Data fetched from database
#  Return Type List of object of Industry
##########################################################################
def return_industries(data):
    fn = core.Industries
    results = [fn( d["organisation_id"], d["organisation_name"], bool(d["is_active"]) ) for d in data]
    return results

##########################################################################
#  To Save client group (name and group admin)
#  Parameters : Object of database, group name and group admin username
#  Return Type : client id  (Int)
##########################################################################
def save_client_group( db, group_name, username, short_name, no_of_view_licence, session_user ):
    client_id = db.call_insert_proc(
        "sp_client_group_save",
        (group_name, username, short_name, no_of_view_licence, session_user))
    message_text = 'New Client %s has been Created.' % group_name
    db.save_activity(session_user, frmClientGroup, message_text)
    u_cg_id = [1]
    for cg_id in u_cg_id:
        users_id = []
        result = db.call_proc("sp_users_under_user_category", (cg_id,))
        for user in result:
            users_id.append(user["user_id"])
        if len(users_id) > 0:
            db.save_toast_messages(1, "Client Group", message_text, None, users_id, session_user)
    # data = db.call_proc("sp_get_userid_from_admin", ())
    # db.save_messages_users(msg_id, data[0]["userids"])
    return client_id

##########################################################################
#  To Update client group (group name)
#  Parameters : Object of database, group name and client id
#  Return Type : None
##########################################################################
def update_client_group(db, client_id, email_id, no_of_licence, remarks, session_user):
    db.call_update_proc(
        "sp_client_group_update", (client_id, email_id, no_of_licence, remarks))
    data = db.call_proc("sp_group_name_by_id", (client_id, ))
    message_text = '%s has been Updated.' % data[0]["group_name"]
    db.save_activity(session_user, frmClientGroup, message_text)

    u_cg_id = [1, 5, 6, 7]
    for cg_id in u_cg_id:
        users_id = []
        result = db.call_proc("sp_users_under_user_category", (cg_id,))
        for user in result:
            users_id.append(user["user_id"])
        if len(users_id) > 0:
            db.save_toast_messages(1, "Client Group", message_text, None, users_id, session_user)
    # db.save_messages_users(msg_id, [1])

##########################################################################
#  To Save group admin as a client user under the client
#  Parameters : Object of database, client id, group admin username
#  Return Type : Raises Process error if insertion fails / returns True
##########################################################################
def save_client_user(db, client_id, username):
    current_time_stamp = get_date_time()
    r = db.call_insert_proc(
        "sp_client_user_save_admin",
        (client_id, username, current_time_stamp))
    if r is False:
        raise process_error("E044")
    return r

##########################################################################
#  To Save List of legal entites under a Client
#  Parameters : Object of database, Request, client id, session user id
#  Return Type : List of legal entity names
##########################################################################
def save_legal_entities(db, request, group_id, session_user):
    columns = [
        "client_id", "country_id", "business_group_id", "legal_entity_name",
        "contract_from", "contract_to", "logo", "file_space_limit", "total_licence",
        'is_closed', "created_by", "created_on", 'updated_by', "updated_on", "logo_size"
    ]
    current_time_stamp = get_date_time()
    legal_entity_ids = []
    for entity in request.legal_entity_details:
        if entity.logo is None:
            file_name = None
            file_size = 0
        else:
            if is_logo_in_image_format(entity.logo):
                file_name = save_client_logo(entity.logo)
                file_size = entity.logo.file_size
            else:
                raise process_error("E067")
        business_group_id = return_business_group_id(
            db, entity, group_id, session_user, current_time_stamp)
        if is_duplicate_legal_entity(
            db, None, entity.legal_entity_name, group_id, entity.country_id
        ):
            raise process_error("E068")
        value_tuple = (
            group_id, entity.country_id, business_group_id,
            entity.legal_entity_name,
            string_to_datetime(entity.contract_from),
            string_to_datetime(entity.contract_to),
            file_name, entity.file_space*1024*1024*1024, entity.no_of_licence,
            0, session_user, current_time_stamp,
            session_user, current_time_stamp, file_size
        )
        result = db.insert(tblLegalEntities, columns, value_tuple)
        legal_entity_ids.append(result)
    return legal_entity_ids


##########################################################################
#  To Update List of legal entites under a Client
#  Parameters : Object of database, Request, client id, session user id
#  Return Type : List of legal entity names
##########################################################################
def update_legal_entities(db, request, group_id, session_user):
    columns = ["country_id", "business_group_id", "legal_entity_name", "contract_from", "contract_to",
            "logo", "file_space_limit", "total_licence", 'updated_by', "updated_on", "is_approved"]
    insert_columns = ["client_id", "country_id", "business_group_id", "legal_entity_name",
        "contract_from", "contract_to", "logo", "file_space_limit", "total_licence",
        'is_closed', "created_by", "created_on", 'updated_by', "updated_on"]
    values = []
    insert_values = []
    conditions = []
    current_time_stamp = get_date_time()
    legal_entity_ids = []
    for entity in request.legal_entities:
        if(entity.new_logo is not None):
            if "logo_size" in insert_columns:
                insert_columns.remove("logo_size")
            if is_logo_in_image_format(entity.new_logo):
                file_name = save_client_logo(entity.new_logo)
                file_size = entity.new_logo.file_size
                insert_columns.append("logo_size")
            else:
                raise process_error("E067")
        else:
            file_name = entity.old_logo

        business_group_id = return_business_group_id(db, entity, group_id, session_user, current_time_stamp)
        if is_duplicate_legal_entity(
            db, entity.legal_entity_id, entity.legal_entity_name, group_id, entity.country_id
        ):
            raise process_error("E068")
        elif validate_total_disk_space(db, entity.file_space, group_id, entity.legal_entity_id):
            raise process_error("E070")
        elif validate_no_of_user_licence(db, entity.no_of_licence, group_id, entity.legal_entity_id):
            raise process_error_with_msg("E069", entity.legal_entity_name)
        if entity.legal_entity_id is not None:
            value_list = [entity.country_id, business_group_id, entity.legal_entity_name,
                string_to_datetime(entity.contract_from), string_to_datetime(entity.contract_to),
                file_name, entity.file_space * 1024 * 1024 * 1024, entity.no_of_licence,
                session_user, current_time_stamp, 0]
            values.append(tuple(value_list))
            condition = "client_id=%s and legal_entity_id=%s" % (group_id, entity.legal_entity_id)
            result_update = db.update(tblLegalEntities, columns, tuple(value_list), condition)
            legal_entity_ids.append(entity.legal_entity_id)
            if result_update is False:
                raise process_error("E052")
        else:
            insert_value_list = [ group_id, entity.country_id, business_group_id,
                entity.legal_entity_name, string_to_datetime(entity.contract_from),
                string_to_datetime(entity.contract_to),
                file_name, entity.file_space * 1024 * 1024 * 1024, entity.no_of_licence,
                0, session_user, current_time_stamp, session_user, current_time_stamp ]
            if(entity.new_logo is not None):
                insert_value_list.append(file_size)
            result = db.insert(tblLegalEntities, insert_columns, insert_value_list)
            legal_entity_ids.append(result)
            if result is False:
                raise process_error("E052")
    return legal_entity_ids

##########################################################################
#  To Save / Update Business group
#  Parameters : Object of database, Request, client id, session user id,
#  current time stamp
#  Return Type : Business group id (Int)
##########################################################################
def return_business_group_id( db, request, group_id, session_user, current_time_stamp ):
    if request.business_group is None:
        return None
    elif request.business_group.business_group_id is not 0:
        business_group_name = request.business_group.business_group_name
        business_group_id = request.business_group.business_group_id
        db.call_insert_proc( "sp_business_group_update", ( business_group_id, business_group_name ) )
        return business_group_id
    else:
        business_group_name = request.business_group.business_group_name
        if is_duplicate_business_group( db, None, business_group_name, group_id ):
            raise process_error("E066")
        else:
            business_group_id = db.call_insert_proc( "sp_business_group_save", (
                    business_group_name, group_id, request.country_id,
                    session_user, current_time_stamp ) )
            return business_group_id

##########################################################################
#  To Save date configurations of a client
#  Parameters : Object of database, client id, date configurations,
#  session user id
#  Return Type : List of country ids under the client
##########################################################################
def save_date_configurations( db, client_id, date_configurations, session_user ):
    values_list = []
    current_time_stamp = get_date_time()
    # db.call_update_proc("sp_client_configurations_delete", (client_id, ) )
    for configuration in date_configurations:
        value_tuple = (client_id, configuration.country_id, configuration.domain_id,
            configuration.month_from, configuration.month_to,
            session_user, current_time_stamp)
        res = db.call_insert_proc( "sp_client_group_date_config_save", value_tuple)
    #     value_tuple = (client_id, configuration.country_id, configuration.domain_id,
    #         configuration.month_from, configuration.month_to,
    #         session_user, current_time_stamp)
    #     values_list.append(value_tuple)
    # res = db.bulk_insert(tblClientConfiguration, columns, values_list)
    if res is False:
        raise process_error("E047")
    return res

##########################################################################
#  To Create a dict with legal entity name as key and legal entity id as
#  value
#  Parameters : Object of database, List of legal entity names
#  Return Type : Dictionary
##########################################################################
def get_legal_entity_ids_by_name(db, legal_entity_names):
    legal_entity_name_id_map = {}
    result = db.call_proc( "sp_legal_entity_id_by_name", (",".join(legal_entity_names),) )
    for row in result:
        le_name = row["legal_entity_name"]
        if le_name not in legal_entity_name_id_map:
            legal_entity_name_id_map[le_name] = row["legal_entity_id"]
    return legal_entity_name_id_map

##########################################################################
#  To Save client domains
#  Parameters : Object of database, client id, Request, Dictionary
#  Return Type : Boolean - Raises Process exception if insertion fails /
#   returns True
##########################################################################
def save_client_domains(db, client_id, request, legal_entity_name_id_map):
    db.call_update_proc( "sp_client_domains_delete", (client_id, ) )
    values_list = []
    columns = ["client_id", "legal_entity_id", "domain_id"]
    if hasattr(request, "legal_entity_details"):
        entity_details = request.legal_entity_details
    else:
        entity_details = request.legal_entities
    for entity in entity_details:
        for domain in entity.domain_details:
            value_tuple = ( client_id, legal_entity_name_id_map[
                    entity.legal_entity_name ], domain.domain_id)
            values_list.append(value_tuple)
    r = db.bulk_insert(tblClientDomains, columns, values_list)
    if r is False:
        raise process_error("E042")
    return r

##########################################################################
#  To Save incharge persons
#  Parameters : Object of database, client id, Request, Dictionary
#  Return Type : Boolean - Raises Process exception if insertion fails /
#   returns True
##########################################################################
def save_incharge_persons(db, client_id, request, user_id):
    r = db.call_insert_proc("sp_user_clients_save", (user_id, client_id))
    if r is False:
        raise process_error("E043")
    return r

##########################################################################
#  To Save  organizations under a domain
#  Parameters : Object of database, client id, Request, Dictionary,
#   session user id
#  Return Type : Boolean - Raises Process exception if insertion fails /
#   returns True
##########################################################################
def save_organization(db, group_id, request, legal_entity_name_id_map, session_user):
    current_time_stamp = get_date_time()
    columns = [
        "legal_entity_id", "domain_id", "organisation_id",
        "activation_date", "count", "created_by", "created_on"
    ]
    values_list = []
    if hasattr(request, "legal_entity_details"):
        entity_details = request.legal_entity_details
    else:
        entity_details = request.legal_entities
    new_domains = {}
    count = 0
    for entity in entity_details:
        # get ole_domain_list
        le_id = legal_entity_name_id_map[count]
        new_domains[le_id] = []
        old_rows = db.select_all("select domain_id from tbl_legal_entity_domains  where legal_entity_id = %s ", [le_id])
        old_domains = []
        for r in old_rows :
            old_domains.append(int(r["domain_id"]))

        domain_details = entity.domain_details
        db.call_update_proc("sp_le_domain_industry_delete", [legal_entity_name_id_map[count]])
        for domain in domain_details:
            domain_id = int(domain.domain_id)
            organization = domain.organization
            activation_date = string_to_datetime(domain.activation_date)
            for org in organization:
                orgval = organization[org].split('-')[0]
                value_tuple = (
                    legal_entity_name_id_map[count], domain_id, org, activation_date,
                    orgval, session_user, current_time_stamp
                )
                values_list.append(value_tuple)
            if len(old_domains) > 0 :
                if domain_id not in old_domains :
                    new_domains[le_id].append(domain_id)

        count += 1
    r = db.bulk_insert(tblLegalEntityDomains, columns, values_list)
    if r is False:
        raise process_error("E071")
    else :
        for k, v in new_domains.iteritems() :
            if len(v) > 0 :
                d_ids = ",".join([str(x) for x in v])
                q = "INSERT INTO tbl_client_replication_status (client_id, is_new_domain, domain_id, is_group) " + \
                    " values(%s, 1, %s, 0) " + \
                    " on duplicate key update is_new_domain = 1, domain_id = %s "
                db.execute(q, [k, d_ids, d_ids])

    return r

##########################################################################
#  To Check whether the group name already exists
#  Parameters : Object of database, group name, client id (Optional)
#  Return Type : Boolean - Returns true if group name already exists
#   returns False if there is no duplicates
##########################################################################
def is_duplicate_group_name(db, group_name, client_id=None):
    count_rows = db.call_proc( "sp_client_group_is_duplicate_groupname", (group_name, client_id))
    if count_rows[0]["count"] > 0:
        return True
    else:
        return False

##########################################################################
#  To Check whether created maximum licence users
#  Parameters : Object of database, client id, no_of_licence
#  Return Type : Boolean - Returns true if group name already exists
#   returns False if there is no maximum exists
##########################################################################
def check_licence_created(db, group_id, no_of_licence):
    count_rows = db.call_proc( "sp_client_group_licence_count", (client_id, no_of_licence))
    if count_rows[0]["count"] > 0:
        return True
    else:
        return False

##########################################################################
#  To Check whether the group name already exists
#  Parameters : Object of database, group name, client id (Optional)
#  Return Type : Boolean - Returns true if group name already exists
#   returns False if there is no duplicates
##########################################################################
def is_duplicate_group_short_name(db, group_short_name, client_id=None):
    count_rows = db.call_proc( "sp_client_group_is_duplicate_groupshortname", (group_short_name, client_id))
    if count_rows[0]["count"] > 0:
        return True
    else:
        return False

##########################################################################
#  To Check whether the busienss group name already exists
#  Parameters : Object of database, business group id, business group name,
#   client id
#  Return Type : Boolean - Returns true if business group name already exists
#   returns False if there is no duplicates
##########################################################################
def is_duplicate_business_group( db, business_group_id, business_group_name, client_id ):
    count_rows = db.call_proc( "sp_businessgroup_is_duplicate_businessgroupname",
        (business_group_name, business_group_id, client_id))
    if count_rows[0]["count"] > 0:
        return True
    else:
        return False

##########################################################################
#  To Check whether the legal entity name already exists
#  Parameters : Object of database, legal entity id, legal entity name,
#   client id
#  Return Type : Boolean - Returns true if legal entity name already exists
#   returns False if there is no duplicates
##########################################################################
def is_duplicate_legal_entity( db, legal_entity_id, legal_entity_name, client_id, country_id ):
    count_rows = db.call_proc( "sp_legalentity_is_duplicate_legalentityname",
        (legal_entity_name, legal_entity_id, client_id, country_id))
    if count_rows[0]["count"] > 0:
        return True
    else:
        return False

##########################################################################
#  To Check whether the uploaded logo is an image or not
#  Parameters : uploaded logo
#  Return Type : Boolean - Returns true if legal entity name already exists
#   returns False if there is no duplicates
##########################################################################
def is_logo_in_image_format(logo):
    exten = logo.file_name.split('.')[1]
    if exten in ["png", "jpg", "jpeg", "gif", "bmp"]:
        return True
    else:
        return False

##########################################################################
#  To Save the client logo
#  Parameters : uploaded logo
#  Return Type : Returns File name (String) - if upload succeeds and
#   returns None if upload fails
##########################################################################
def save_client_logo(logo):
    name = logo.file_name.split('.')[0]
    exten = logo.file_name.split('.')[1]
    auto_code = new_uuid()
    file_name = "%s-%s.%s" % (name, auto_code, exten)
    try:
        convert_base64_to_file(file_name, logo.file_content, CLIENT_LOGO_PATH)
        return file_name
    except Exception, e:
        print e
        return None

##########################################################################
#  To get details of a client by id
#  Parameters : Object of database, client id
#  Return Type : Tuple with group name, username, legal entities and
#  date configurations
##########################################################################
def get_client_details(db, client_id):
    client_details = db.call_proc("sp_client_groups_details_by_id", (client_id,))
    legal_entities = db.call_proc("sp_legal_entity_details_by_group_id", (client_id,))
    date_configurations = db.call_proc("sp_client_configuration_by_group_id", (client_id,))
    organizations = db.call_proc("sp_le_d_industry_by_group_id", (client_id,))
    group_name = client_details[0]["group_name"]
    user_name = client_details[0]["email_id"]
    short_name = client_details[0]["short_name"]
    total_view_licence = client_details[0]["total_view_licence"]
    domain_map = return_organization_by_legalentity_domain(db, organizations, client_id)
    print "domain_map", (domain_map)
    legal_entities = return_legal_entities(legal_entities, domain_map)
    date_configuration_list = return_date_configurations(date_configurations)
    return (group_name, user_name, short_name, total_view_licence, legal_entities, date_configuration_list)

##########################################################################
#  To convert the data fetched from database into Legal entity object
#  Parameters : Legal entity tuple, incharge person tuple, domain tuple
#  Return Type : List of object of Legal entities
##########################################################################
def return_legal_entities(legal_entities, domains):
    results = []
    for legal_entity in legal_entities:
        if legal_entity["business_group_id"] is None:
            business_group = None
        else:
            business_group = core.ClientBusinessGroup(business_group_id=legal_entity["business_group_id"],
                business_group_name=legal_entity["business_group_name"])
        results.append( core.LegalEntityList( country_id=legal_entity["country_id"],
                business_group=business_group, legal_entity_id=legal_entity["legal_entity_id"],
                legal_entity_name=legal_entity["legal_entity_name"], old_logo=legal_entity["logo"],
                new_logo=None, no_of_licence=legal_entity["total_licence"],
                file_space=int(round(legal_entity["file_space_limit"]/(1024*1024*1024))),
                contract_from=datetime_to_string(legal_entity["contract_from"]),
                contract_to=datetime_to_string(legal_entity["contract_to"]),
                domain_details=domains[legal_entity["legal_entity_id"]],
                is_closed=bool(legal_entity["is_closed"]),
                is_approved=int(legal_entity["is_approved"]) ) )
    return results

##########################################################################
#  To convert the data fetched from database into a dict
#  Parameters : Organization details fetched from database (Tuple of
#  tuples )
#  Return Type : Dictionary
##########################################################################
def return_organization_by_legalentity_domain(db, organizations, client_id):
    organization_map = {}
    domain_map = {}
    for row in organizations:
        legal_entity_id = row["legal_entity_id"]
        domain_id = row["domain_id"]
        industry_id = row["organisation_id"]
        no_of_units = row["count"]
        activation_date = row["activation_date"]

        org_count_rows = db.call_proc("sp_legal_entity_domain_transaction_check", (client_id, legal_entity_id, domain_id, industry_id,))
        if org_count_rows[0]["count"] <= 0:
            org_is_delete = org_count_rows[0]["count"]
        else:
            org_is_delete = org_count_rows[0]["count"]

        if legal_entity_id not in domain_map:
            domain_map[legal_entity_id] = []
        if legal_entity_id not in organization_map:
            organization_map[legal_entity_id] = {}
        if domain_id not in organization_map[legal_entity_id]:
            organization_map[legal_entity_id][domain_id] = {}
        if industry_id not in organization_map[legal_entity_id][domain_id]:
            org_concat = "%s-%s" % (no_of_units, org_is_delete)
            organization_map[legal_entity_id][domain_id][str(industry_id)] = org_concat

        org_concat = "%s-%s" % (no_of_units, org_is_delete)
        organization_map[legal_entity_id][domain_id][str(industry_id)] = org_concat

        if domain_id in [x.domain_id for x in domain_map[legal_entity_id]]:
            continue
        domain_count_rows = db.call_proc("sp_legal_entity_domain_transaction_check", (client_id, legal_entity_id, domain_id, None,))
        if domain_count_rows[0]["count"] <= 0:
            domain_is_delete = 0
        else:
            domain_is_delete = 1
        domain_map[legal_entity_id].append(generalprotocol.EntityDomainDetails(
                domain_id=domain_id, activation_date=datetime_to_string(activation_date),
                organization=organization_map[int(legal_entity_id)][int(domain_id)], is_delete=domain_is_delete))
    return domain_map


##########################################################################
#  To convert data configuration details fetched from database into
#  list of object of ClientConfiguration
#  Parameters : Data fetched from database (Tuple of tuples)
#  Return Type : List of object of ClientConfiguration
##########################################################################
def return_date_configurations(date_configurations):
    results = [core.ClientConfiguration(country_id=config["country_id"],
            domain_id=config["domain_id"], month_from=config["month_from"],
            month_to=config["month_to"]) for config in date_configurations]
    return results

##########################################################################
#  To check whether the client id is valid or not
#  Parameters : Object of database, client id
#  Return Type : Boolean - True if client id is valid, False if invalid
##########################################################################
def is_invalid_group_id(db, client_id):
    count_rows = db.call_proc("sp_client_groups_is_valid_group_id", (client_id,))
    if count_rows[0]["count"] <= 0:
        return True
    else:
        return False

##########################################################################
#  To check whether a domain with units is deactivated
#  Parameters : Object of database, client id, List of domain ids
#  Return Type : Boolean - True if deactivated a domain with active units,
#   Otherwise returns false
##########################################################################
def is_deactivated_existing_domain(db, client_id, domain_ids):
    existing_domain_ids = get_client_domains(db, client_id)
    current_domains = [int(x) for x in domain_ids]
    for domain in existing_domain_ids:
        if domain not in current_domains:
            if is_unit_exists_under_domain(db, domain, client_id):
                return True
            else:
                continue
        else:
            continue
    return False

##########################################################################
#  To get countries of  a client
#  Parameters : Object of database, client id,
#  Return Type : List of country ids (List of Int)
##########################################################################
def get_client_countries(db, client_id):
    rows = db.call_proc("sp_client_countries_by_group_id", (client_id,))
    country_ids = [int(r["country_id"]) for r in rows]
    return country_ids

##########################################################################
#  To get list of techno users
#  Parameters : Object of database
#  Return Type : List of Object of ClientInchargePersons
##########################################################################
def get_techno_users(db):
    countries = db.call_proc("sp_user_countries_techno", None)
    domains = db.call_proc("sp_user_domains_techno", None)
    users = db.call_proc("sp_users_techno", None)
    user_country_map = {}
    for country in countries:
        user_id = int(country["user_id"])
        if user_id not in user_country_map:
            user_country_map[user_id] = []
        user_country_map[user_id].append(country["country_id"])

    user_domain_map = {}
    for domain in domains:
        user_id = int(domain["user_id"])
        if user_id not in user_domain_map:
            user_domain_map[user_id] = []
        user_domain_map[user_id].append(
            domain["domain_id"])
    return return_techno_users(users, user_country_map, user_domain_map)

##########################################################################
#  To convert Data fetched from database into list of Object of
#   ClientInchargePersons
#  Parameters : Data fetched from database,
#   dict (Key: user, value: Country), dict (key: user, value: domain)
#  Return Type : List of Object of ClientInchargePersons
##########################################################################
def return_techno_users(users, user_country_map, user_domain_map):
    fn = core.ClientInchargePersons
    results = [fn( int(user["user_id"]), user["e_name"], bool(user["is_active"]),
            user_country_map[int(user["user_id"])], user_domain_map[int(user["user_id"])]
        ) for user in users]
    return results

##########################################################################
#  To get list of groups
#  Parameters : Object of database
#  Return Type : Returns List of object of ClientGroup
##########################################################################
def get_groups(db, session_user):
    groups = db.call_proc_with_multiresult_set("sp_client_groups_list", (session_user,), 2)
    return return_group(groups[1])

##########################################################################
#  To get list of groups
#  Parameters : Object of database
#  Return Type : Returns List of object of ClientGroup
##########################################################################
def return_group(groups):
    fn = core.ClientGroup
    client_list = []
    for group in groups:
        if group["client_id"] is not None:
            if group["is_closed"] > 0:
                if ((datetime.datetime.now() - group["closed_on"]).days > 90) is True:
                    is_closed_cg = 2
                else:
                    is_closed_cg = 1
            else:
                is_closed_cg = 0

            client_list.append(
                fn( group["client_id"], group["group_name"], group["country_name"],
                    group["legal_entity_name"], int(is_closed_cg),
                    int(group["is_approved"]), group["reason"] )
            )
    return client_list

##########################################################################
#  To get list of groups
#  Parameters : Object of database
#  Return Type : Returns List of object of ClientGroup
##########################################################################
def get_client_groups_for_user(db, user_id):
    groups = db.call_proc_with_multiresult_set("sp_client_groups_for_user", (user_id,), 3)
    return return_client_groups_for_user(groups)

##########################################################################
#  To get list of groups
#  Parameters : Object of database
#  Return Type : Returns List of object of ClientGroup
##########################################################################
def return_country_list_of_client_group(client_id, countries):
    c_ids = []
    for c in countries:
        if int(c["client_id"]) == client_id:
            c_ids.append(int(c["country_id"]))
    return c_ids

def return_client_groups_for_user(data):
    results = []
    for d in data[1]:
        c_id = d["client_id"]
        c_ids = return_country_list_of_client_group(c_id, data[2])
        results.append(core.ClientGroupMaster(
            c_ids, c_id, d["group_name"], bool(d["is_active"]), int(d["is_approved"]) ))
    return results

###############################################################################
# To convert the data fetched from database into List of object of Domain
# Parameter(s) : Data fetched from database
# Return Type : List of Object of Domain
###############################################################################
def return_country_list_of_domain(domain_id, countries):
    c_ids = []
    c_names = []
    for c in countries:
        if int(c["domain_id"]) == domain_id:
            c_ids.append(int(c["country_id"]))
            c_names.append(c["country_name"])
    return c_ids, c_names

def return_domains(data):
    results = []
    for d in data[0]:
        d_id = d["domain_id"]
        c_ids, c_names = return_country_list_of_domain(d_id, data[1])
        results.append(core.Domain(
            c_ids, c_names, d_id, d["domain_name"], bool(d["is_active"])
        ))
    return results

##########################################################################
#  To check Wheteher the entered no of licence is less than already
#  existing number of users
#  Parameters : Object of database, New no of user licence entered,
#   client id, legal entitiy id
#  Return Type : Returns true if entered no of licence is less than already
#  existing number of users otherwise returns false
##########################################################################
def validate_no_of_user_licence( db, no_of_user_licence, client_id, legal_entity_id ):
    rows = db.call_proc("sp_client_users_count", (client_id, legal_entity_id))
    current_no_of_users = int(rows[0]["count"])
    if no_of_user_licence < current_no_of_users:
        return True
    else:
        return False

##########################################################################
#  To check Wheteher the entered file space is less than already
#  used file space
#  Parameters : Object of database, entered file space, client id,
# legal entity id
#  Return Type : Returns true if entered file space is less than already
#  used file space
##########################################################################
def validate_total_disk_space(db, file_space, client_id, legal_entity_id):
    if legal_entity_id is None:
        return False
    rows = db.call_proc("sp_legal_entities_space_used", (legal_entity_id,),)
    used_space = int(rows[0]["used_file_space"])
    if (file_space * 1024 * 1024 * 1024) < used_space:
        return True
    else:
        return False

def is_unit_exists_under_domain(db, domain, client_id):
    columns = "count(*) as units"
    condition = " FIND_IN_SET(%s, domain_ids) and client_id = %s "
    condition_val = [domain, client_id]
    rows = db.get_data_data(tblUnits, columns, condition, condition_val)
    if rows[0]["units"] > 0:
        return True
    else:
        return False

def get_client_ids(db):
    columns = "client_id"
    condition = "1"
    rows = db.get_data(tblUserClients, columns, condition)
    client_ids = []
    if rows:
        client_ids.append(str(rows[0]["client_id"]))
    return client_ids

def get_client_domains(db, client_id):
    columns = "domain_id"
    condition = "client_id = %s "
    condition_val = [client_id]
    rows = db.get_data(tblClientDomains, columns, condition, condition_val)
    domain_ids = [int(r["domain_id"]) for r in rows]
    return domain_ids

def get_user_client_domains(db, session_user):
    result = db.call_proc("sp_tbl_unit_getclientdomains", (session_user, 0))
    if result:
        return return_domains(result)
    else:
        result = db.call_proc("sp_tbl_unit_getclientdomains", (session_user, 1))
        return return_domains(result)

def get_date_configurations(db, client_id):
    columns = "country_id, domain_id, month_from, month_to"
    condition = "client_id=%s"
    condition_val = [client_id]
    result = db.get_data(
        tblClientConfiguration, columns, condition,
        condition_val)
    return return_client_configuration(result)


def return_client_configuration(configurations):
    fn = core.ClientConfiguration
    results = [ fn( configuration["country_id"], configuration["domain_id"],
            configuration["month_from"], configuration["month_to"]
        ) for configuration in configurations ]
    return results

def get_server_details(db):
    columns = ["ip", "server_username", "server_password", "port"]
    condition = "server_full = 0 "
    _order = "ORDER BY length ASC limit 1"
    rows = db.get_data( tblDatabaseServer, columns, condition, condition_val=None, order=_order )
    return rows

def is_unit_exists_under_country(db, country, client_id):
    columns = "count(*) as units"
    condition = "country_id = %s and client_id = %s "
    condition_val = [country, client_id]
    rows = db.get_data(tblUnits, columns, condition, condition_val)
    if rows[0]["units"] > 0:
        return True
    else:
        return False

##########################################################################
#  To Update client logo
#  Parameters : Object of database, logo, client id
#  Return Type : to save client logo
##########################################################################
def update_client_logo(db, logo, client_id):
    column = "logo_url"
    condition = "client_id = %s "
    condition_val = [client_id]
    rows = db.get_data( tblClientGroups, column, condition, condition_val )
    old_file_name = rows[0]["logo_url"]
    old_file_path = "%s/%s" % (CLIENT_LOGO_PATH, old_file_name)
    remove_uploaded_file(old_file_path)
    return save_client_logo(logo)

##########################################################################
#  To Update client group
#  Parameters : Object of database, client group details,
#  session user id
#  Return Type : return true
##########################################################################
def update_client_group_record(db, client_group, session_user):
    current_time_stamp = get_date_time()
    contract_from = string_to_datetime(client_group.contract_from)
    contract_to = string_to_datetime(client_group.contract_to)
    is_sms_subscribed = 0 if client_group.is_sms_subscribed is False else 1
    columns = ["group_name", "contract_from", "contract_to", "no_of_user_licence",
        "total_disk_space", "is_sms_subscribed", "incharge_persons", "updated_by", "updated_on"]
    values = [client_group.group_name, contract_from, contract_to, client_group.no_of_user_licence,
        client_group.file_space * (1024 * 1024 * 1024), is_sms_subscribed,
        ','.join(str(x) for x in client_group.incharge_persons), session_user, current_time_stamp]
    if client_group.logo is not None:
        columns.append("logo_url")
        columns.append("logo_size")
        file_name = update_client_logo(db, client_group.logo, client_group.client_id)
        values.append(file_name)
        values.append(client_group.logo.file_size)
    condition = "client_id = %s"
    values.append(client_group.client_id)
    if db.update(tblClientGroups, columns, values, condition):
        action = "Updated Client \"%s\"" % client_group.group_name
        db.save_activity(session_user, frmClientGroup, action)
        return True
    else:
        raise process_error("E046")

def is_unit_exists_under_client(db, client_id):
    column = "count(*) as units"
    condition = "client_id = %s and is_active = 1"
    condition_val = [client_id]
    rows = db.get_data(tblUnits, column, condition, condition_val)
    if rows[0]["units"] > 0:
        return True
    else:
        return False

def update_client_group_status(db, client_id, is_active, session_user):
    r = db.call_proc( "sp_client_groups_change_status", (client_id, is_active), ["group_name"] )
    if r is False:
        raise process_error("E049")
    else:
        group_name = r[0]["group_name"]
        if is_active == 1:
            action = "Activated Client \"%s\"" % group_name
        else:
            action = "Deactivated Client \"%s\"" % group_name
        db.save_activity(session_user, frmClientGroup, action)

def is_duplicate_division(db, division_id, division_name, client_id):
    condition = "division_name = %s  AND client_id = %s "
    condition_val = [division_name, client_id]
    if division_id is not None:
        condition += " AND division_id != %s "
        condition_val.append(division_id)
    return db.is_already_exists(tblDivisions, condition, condition_val)

def update_division(db, client_id, division_id, division_name, session_user):
    current_time_stamp = get_date_time()
    columns = ["division_name", "updated_by", "updated_on"]
    values = [division_name, session_user, current_time_stamp]
    condition = "division_id = %s and client_id = %s"
    values.extend([division_id, client_id])
    result = db.update(tblDivisions, columns, values, condition)
    if result:
        action = "Updated Division \"%s\"" % division_name
        db.save_activity(session_user, frmClientUnit, action)
        return result
    else:
        raise process_error("E055")

######################################################################################
# To check duplication of unit code
# Parameter(s) : Object of database, unit code, unit id, client id
# Return Type : Return count of unit code
######################################################################################
def is_duplicate_unit_code(db, unit_id, unit_code, client_id):
    params = [unit_id, unit_code, None, client_id]
    rows = db.call_proc("sp_tbl_units_checkduplication", params)
    for d in rows:
        if(int(d["unit_code_cnt"]) > 0):
            return True
        else:
            return False

######################################################################################
# To check duplicate unit name
# Parameter(s) : Object of database, unit id, unit name, client id
# Return Type : Return count if unit name
######################################################################################
def is_duplicate_unit_name(db, unit_id, unit_name, client_id):
    params = [unit_id, None, unit_name, client_id]
    rows = db.call_proc("sp_tbl_units_checkduplication", params)
    for d in rows:
        if(int(d["unit_name_cnt"]) > 0):
            return True
        else:
            return False
######################################################################################
# To check invalid id
# Parameter(s) : Object of database, mode of table/ column, column value
# Return Type : Return count of the column
######################################################################################
def is_invalid_id(db, check_mode, val):
    if check_mode == "unit_id":
        params = [val,]
        rows = db.call_proc("sp_tbl_units_check_unitId", params)
        for d in rows:
            if(int(d["unit_id_cnt"]) > 0):
                return True
            else:
                return False
    else:
        params = [check_mode, val]
        rows = db.call_proc("sp_tbl_units_check_unitgroupid", params)
        for r in rows:
            if check_mode == "client_id":
                if(int(r["client_cnt"]) > 0):
                    return True
                else:
                    return False
            if check_mode == "bg_id":
                if(int(r["bg_cnt"]) > 0):
                    return True
                else:
                    return False
            if check_mode == "legal_entity_id":
                if(int(r["le_cnt"]) > 0):
                    return True
                else:
                    return False
            if check_mode == "division_id":
                if(int(r["divi_cnt"]) > 0):
                    return True
                else:
                    return False

######################################################################################
# To check invalid name
# Parameter(s) : Object of database, column value
# Return Type : Return count of the column
######################################################################################
def is_invalid_name(db, check_mode, val):
    params = [check_mode, val]
    rows = db.call_proc("sp_tbl_units_check_unitgroupname", params)
    for r in rows:
        if check_mode == "div_name":
            if(int(r["div_name_cnt"]) > 0):
                return True
            else:
                return False
        if check_mode == "catg_name":
            if(int(r["catg_cnt"]) > 0):
                return True
            else:
                return False

######################################################################################
# To save division
# Parameter(s) : Object of database, client id, business group id, legal entity id, user id
# Return Type : Return value of the saved division
######################################################################################
def is_duplicate_division(db, division_id, division_name, client_id):
    condition = "division_name = %s  AND client_id = %s "
    condition_val = [division_name, client_id]
    if division_id is not None:
        condition += " AND division_id != %s "
        condition_val.append(division_id)
    return db.is_already_exists(tblDivisions, condition, condition_val)

def save_division( db, client_id, div_name, business_group_id, legal_entity_id, session_user):
    div_id = -1
    current_time_stamp = str(get_date_time())
    values = [ client_id, business_group_id, legal_entity_id, div_name,
        session_user, current_time_stamp]
    if is_duplicate_division(db, None, div_name, client_id) == False:
        print "no dupl div"
        div_id = db.call_insert_proc("sp_tbl_units_save_division", values)
        action = "Added Division \"%s\"" % div_name
        db.save_activity(session_user, frmClientUnit, action)
        if div_id > 0:
            return div_id
        else:
            raise process_error("E055")
    else:
        return div_id

######################################################################################
# To update division
# Parameter(s) : Object of database, client id, business group id, legal entity id, user id
# Return Type : Return value of the updated division
######################################################################################
def update_division( db, client_id, div_id, div_name, business_group_id, legal_entity_id, session_user ):
    current_time_stamp = str(get_date_time())
    values = [client_id, business_group_id, legal_entity_id, div_name, div_id,
        session_user, current_time_stamp]
    if is_duplicate_division(db, div_id, div_name, client_id) == False:
        div_id = db.call_update_proc("sp_tbl_units_update_division", values)
        action = "Updated Division \"%s\"" % div_name
        db.save_activity(session_user, frmClientUnit, action)
        if div_id > 0:
            return True
        else:
            raise process_error("E055")
    else:
        return False

##########################################################################################################
# To save category
# Parameter(s) : Object of database, client id, business group id, legal entity id, category name, user id
# Return Type : Return list of statutory nature
##########################################################################################################
def is_duplicate_category(db, catg_id, catg_name, client_id):
    condition = "category_name = %s  AND client_id = %s "
    condition_val = [catg_name, client_id]
    if catg_id is not None:
        condition += " AND category_id != %s "
        condition_val.append(catg_id)
    return db.is_already_exists(tblCategories, condition, condition_val)

def save_category(
        db, client_id, div_id, business_group_id, legal_entity_id,
        category_name, session_user):
    catg_id = -1
    current_time_stamp = str(get_date_time())
    values = [
        client_id, business_group_id, legal_entity_id, div_id,
        category_name, session_user, current_time_stamp]
    if is_duplicate_category(db, None, category_name, client_id) == False:
        print "no dupli categ"
        catg_id = db.call_insert_proc("sp_tbl_units_save_category", values)
        action = "Added Category \"%s\"" % category_name
        db.save_activity(session_user, frmClientUnit, action)
        if catg_id > 0:
            return catg_id
        else:
            raise process_error("E055")
    else:
        print "dupliacte categ"
        return catg_id

def update_category(db, client_id, div_id, categ_id, business_group_id, legal_entity_id,
    category_name, session_user):
    current_time_stamp = str(get_date_time())
    values = [client_id, business_group_id, legal_entity_id, div_id, categ_id,
        category_name, session_user, current_time_stamp]
    if is_duplicate_category(db, categ_id, category_name, client_id) == False:
        catg_id = db.call_update_proc("sp_tbl_units_update_category", values)
        action = "Updated Category \"%s\"" % category_name
        db.save_activity(session_user, frmClientUnit, action)
        if catg_id > 0:
            return True
        else:
            raise process_error("E055")
    else:
        return False

########################################################################################################
# To Save client Unit
# Parameter(s) : Object of database, client id, business group id, legal entity id, country id, user id
# Return Type : Return value of the saved units
########################################################################################################
def save_unit(
    db, client_id, units, business_group_id, legal_entity_id,
    country_id, session_user
):
    params = ["le_closed", legal_entity_id]
    rows = db.call_proc("sp_tbl_units_check_unitgroupid", params)
    print rows
    print len(rows)
    for r in rows:
        print "le close"
        print r["is_closed"]
        if(r["is_closed"] == 0):
            current_time_stamp = str(get_date_time())
            columns = ["client_id", "geography_id", "unit_code", "unit_name",
                "address", "postal_code", "country_id", "created_by", "created_on",
                "is_approved", "division_id", "category_id"]
            if business_group_id is not None:
                columns.append("business_group_id")
            if legal_entity_id is not None:
                columns.append("legal_entity_id")
            values_list = []
            unit_names = []
            msg_units = []
            int_i = 0
            while int_i < len(units):
                vals = [client_id, units[int_i].geography_id, units[int_i].unit_code.upper(), units[int_i].unit_name,
                    units[int_i].unit_address, units[int_i].postal_code, country_id,
                    session_user, current_time_stamp, units[int_i].is_approved]
                unit_names.append("\"%s - %s\"" % (str(units[int_i].unit_code).upper(), units[int_i].unit_name))
                msg_units.append("\"%s - %s\"" % (units[int_i].geography_id, str(units[int_i].unit_code).upper()))
                int_i = int_i + 1
                if units[int_i].get("div_id") is not None:
                    vals.append(units[int_i].get("div_id"))
                else:
                    vals.append(None)
                int_i = int_i + 1
                if units[int_i].get("catg_id") is not None:
                    vals.append(units[int_i].get("catg_id"))
                else:
                    vals.append(None)
                int_i = int_i + 1
                if business_group_id is not None:
                    vals.append(business_group_id)
                if legal_entity_id is not None:
                    vals.append(legal_entity_id)
                values_list.append(vals)
            result = db.bulk_insert(tblUnits, columns, values_list)
            if result is False:
                raise process_error("E056")
            for msg in msg_units:
                geo_id = int(str(msg).split("-")[0][1:2])
                u_code = str(msg).split("-")[1][:-1]
                db.call_insert_proc("sp_client_unit_messages_save",
                    (session_user, None, client_id, legal_entity_id, geo_id, u_code, current_time_stamp))
            action = "Created following Units %s" % (",".join(unit_names))
            db.save_activity(session_user, frmClientUnit, action)
            max_unit_id = None
            rows = db.call_proc("sp_tbl_units_max_unitid", ())
            for id in rows:
                if(int(id["max_id"]) > 0):
                    max_unit_id = int(id["max_id"])
            columns = ["unit_id", "domain_id", "organisation_id"]
            if len(units) > 3:
                unit_id_start = int(len(units))/3
            else:
                unit_id_start = 1
            values_list = []
            unit_id = None
            i = 1
            j = 0
            while j < len(units):
                d_i_id = units[j].industry_ids
                j = j + 3
                if unit_id_start == 1:
                    unit_id = max_unit_id
                else:
                    unit_id = (max_unit_id - unit_id_start) + i
                    i = i + 1
                for c in d_i_id:
                    delete_res = db.call_proc("sp_tbl_units_delete_unitorganizations", (unit_id,))
                    vals = [unit_id, c.domain_id, c.industry_id]
                    values_list.append(vals)
            result_1 = db.bulk_insert(tblUnitIndustries, columns, values_list)
            if result is True and result_1 is True:
                return True
            else:
                return False
        else:
            print "a"
            return False

######################################################################################
# To update client unit
# Parameter(s) : Object of database, client id, units list, user id
# Return Type : Return value of the updated units
######################################################################################
def update_unit(db, client_id, legal_entity_id, units, session_user):
    params = ["le_closed", legal_entity_id]
    rows = db.call_proc("sp_tbl_units_check_unitgroupid", params)
    for r in rows:
        if(r["is_closed"] == 0):
            current_time_stamp = str(get_date_time())
            columns = ["geography_id", "unit_code", "unit_name", "address", "postal_code",
                "updated_by", "updated_on", "is_approved", "division_id", "category_id"]
            values_list = []
            unit_names = []
            unit_ids = []
            conditions = []
            int_i = 0
            while int_i < len(units):
                vals = [units[int_i].geography_id, units[int_i].unit_code.upper(), units[int_i].unit_name,
                    units[int_i].unit_address, units[int_i].postal_code,
                    session_user, current_time_stamp, units[int_i].is_approved]
                condition = "client_id=%s and unit_id=%s" % (client_id, units[int_i].unit_id)
                conditions.append(condition)
                unit_names.append("\"%s - %s\"" % (str(units[int_i].unit_code).upper(), units[int_i].unit_name))
                unit_ids.append(units[int_i].unit_id)
                int_i = int_i + 1
                if units[int_i].get("div_id") is not None:
                    vals.append(units[int_i].get("div_id"))
                else:
                    vals.append(None)
                int_i = int_i + 1
                if units[int_i].get("catg_id") is not None:
                    vals.append(units[int_i].get("catg_id"))
                else:
                    vals.append(None)
                int_i = int_i + 1
                values_list.append(vals)
            result = db.bulk_update(tblUnits, columns, values_list, conditions)
            if result is False:
                raise process_error("E057")
            for u_id in unit_ids:
                db.call_insert_proc("sp_client_unit_messages_update", (session_user, None, client_id, legal_entity_id, u_id, current_time_stamp))
            action = "Updated following Units %s" % (",".join(unit_names))
            db.save_activity(session_user, frmClientUnit, action)
            if result is True:
                for i in unit_ids:
                    delete_res = db.call_proc("sp_tbl_units_delete_unitorganizations", (i,))
                columns = ["unit_id", "domain_id", "organisation_id"]
                values_list = []
                j = 0
                if len(units) == 3:
                    d_i_id = units[j].industry_ids
                    for c in d_i_id:
                        vals = [units[j].unit_id, c.domain_id, c.industry_id]
                        values_list.append(vals)
                else:
                    while j < len(units):
                        d_i_id = units[j].industry_ids
                        for c in d_i_id:
                            vals = [units[j].unit_id, c.domain_id, c.industry_id]
                            values_list.append(vals)
                        j = j + 3
                result_1 = db.bulk_insert(tblUnitIndustries, columns, values_list)
            if result_1 is True:
                return True
            else:
                return False
        else:
            print "a"
            return False

def update_unit_old(db, client_id,  units, session_user):
    current_time_stamp = str(get_date_time())
    columns = ["country_id", "geography_id", "industry_id", "domain_ids", "unit_code",
            "unit_name", "address", "postal_code", "updated_by", "updated_on"]
    for unit in units:
        domain_ids = ",".join(str(x) for x in unit.domain_ids)
        values = [unit.country_id, unit.geography_id, unit.industry_id, domain_ids,
            str(unit.unit_code), str(unit.unit_name), str(unit.unit_address),
            str(unit.postal_code), session_user, current_time_stamp]
        condition = "client_id= %s and unit_id = %s"
        values.extend([client_id, unit.unit_id])
        res = db.update(tblUnits, columns, values, condition)
        if res:
            action = "Unit details updated for \"%s - %s\"" % (unit.unit_code, unit.unit_name)
            db.save_activity(session_user, frmClientUnit, action)
        else:
            raise process_error("E057")
    return True

######################################################################################
# To Get client ids under user
# Parameter(s) : Object of database, user id
# Return Type : Return list of client ids
######################################################################################
def get_user_clients(db, user_id):
    rows = db.call_proc("sp_tbl_unit_getuserclients", [int(user_id)])
    client_ids = [int(r["client_id"]) for r in rows]
    return client_ids

######################################################################################
# To Get clients under user
# Parameter(s) : Object of database, user id
# Return Type : Return list of client list
######################################################################################
def get_clients_by_user(db, user_id):
    data = db.call_proc("sp_tbl_unit_getuserclients", [int(user_id)])
    fn = core.Client
    result = [fn(client_id=datum["client_id"], group_name=datum["group_name"],
            is_active=bool(datum["is_active"]) ) for datum in data]
    return result

######################################################################################
# To Get countries under user
# Parameter(s) : Object of database, user id
# Return Type : Return list of countries under legal entity
######################################################################################
def get_countries_for_unit(db, user_id):
    rows = db.call_proc("sp_countries_for_unit", (user_id,))
    fn = core.UnitCountries
    results = [fn(d["client_id"], d["business_group_id"], d["country_id"], d["country_name"]) for d in rows]
    return results

######################################################################################
# To Get domain and organization
# Parameter(s) : Object of database, user id
# Return Type : Return list of domains and organization list
######################################################################################
def get_domains_for_unit(db, user_id):
    rows = db.call_proc("sp_domains_for_user", (user_id,))
    fn = core.UnitDomainOrganisation
    results = [fn(d["legal_entity_id"], d["domain_id"], d["domain_name"], d["industry_id"],
           d["industry_name"], d["unit_count"]) for d in rows]
    return results

######################################################################################
# To Get business groups under user
# Parameter(s) : Object of database, user id
# Return Type : Return list of business groups
######################################################################################
def get_business_groups_for_user(db, user_id):
    result = db.call_proc("sp_tbl_unit_getclientbusinessgroup", (user_id,))
    return return_business_groups(result)

######################################################################################
# To Get legal entities under user
# Parameter(s) : Object of database, user id
# Return Type : Return list of legal entities
######################################################################################
def get_legal_entities_for_user(db, user_id):
    result = db.call_proc("sp_tbl_unit_getclientlegalentity", (user_id,))
    return return_legal_entities_for_unit(result)

def return_legal_entities_for_unit(legal_entities):
    results = []
    for legal_entity in legal_entities:
        legal_entity_obj = core.UnitLegalEntity(
            legal_entity_id=legal_entity["legal_entity_id"], legal_entity_name=legal_entity["legal_entity_name"],
            business_group_id=legal_entity["business_group_id"], client_id=legal_entity["client_id"],
            country_id=legal_entity["country_id"], le_expiry_days=str(legal_entity["contract_days"]),
            is_approved=int(legal_entity["is_approved"]))
        results.append(legal_entity_obj)
    return results

######################################################################################
# To Get divisions under user
# Parameter(s) : Object of database, user id
# Return Type : Return list of divisions
######################################################################################
def get_divisions_for_user(db, user_id):
    result = db.call_proc("sp_tbl_unit_getclientdivision", (user_id,))
    return return_divisions(result)

def return_divisions(divisions):
    results = []
    for division in divisions:
        division_obj = core.Division( division["division_id"], division["division_name"],
            division["legal_entity_id"], division["business_group_id"], division["client_id"])
        results.append(division_obj)
    return results

def return_unit_geography_levels(data):
    geography_levels = []
    for d in data:
        level = core.UnitGeographyLevel(d["level_id"], d["level_position"], d["level_name"], d["country_id"])
        geography_levels.append(level)
    return geography_levels

######################################################################################
# To Get geography levels under user
# Parameter(s) : Object of database, user id
# Return Type : Return list of geography levels
######################################################################################
def get_unit_geograhpy_levels_for_user(db, user_id):
    assert user_id is not None
    condition_val = [user_id]
    result = db.call_proc("sp_tbl_unit_getgeographylevels", condition_val)
    return return_unit_geography_levels(result)

######################################################################################
# To Get geographies under user
# Parameter(s) : Object of database, user id
# Return Type : Return list of geographies
######################################################################################
def get_geographies_for_unit(db, user_id):
    where_condition_val = [user_id]
    result = db.call_proc("sp_get_geographies_for_users_mapping", where_condition_val)
    geographies = []
    if result:
        for d in result:
            parent_ids = [int(x) for x in d["parent_ids"].split(',') if x != '']
            parent_names = [str(y) for y in d["parent_names"].split(',') if y != '']
            geography = core.UnitGeographyMapping( d["geography_id"], d["geography_name"],
                d["level_id"], parent_names, parent_ids, d["country_id"], bool(d["is_active"]))
            geographies.append(geography)
    return geographies

######################################################################################
# To Get domains, organization under user
# Parameter(s) : Object of database, user id
# Return Type : Return list of domains, organizations
######################################################################################
def get_client_industries(db, user_id,):
    columns = [ "country_id", "country_name", "domain_id", "domain_name",
        "industry_id", "industry_name", "is_active"]
    result = db.call_proc("sp_tbl_units_getindustries_for_legalentity", (user_id,))
    return return_unit_industry(result)

def return_unit_industry(data):
    results = []
    for d in data:
        industry_id = d["industry_id"]
        industry_name = d["industry_name"]
        country_id = d["country_id"]
        domain_id = d["domain_id"]
        client_id = d["client_id"]
        unit_count = d["no_of_units"]
        legal_entity_id = d["legal_entity_id"]
        is_active = bool(d["is_active"])
        results.append(core.UnitIndustries(industry_id, industry_name, country_id,  domain_id,
            client_id, unit_count, legal_entity_id, is_active))
    return results

def get_units(db):
    result = db.call_proc("sp_units_name_and_id", None)
    return return_units(result)

def get_units_for_user(db, user_id):
    result = db.call_proc("sp_units_by_user", (user_id,))
    return return_units(result)

def return_units(units):
    results = []
    for unit in units:
        domain_ids = [int(x) for x in unit["domain_ids"].split(',') if x != '']
        results.append(core.Unit(unit["unit_id"], unit["division_id"], unit["legal_entity_id"],
            unit["business_group_id"], unit["client_id"], unit["unit_code"],
            unit["unit_name"], unit["address"], bool(unit["is_active"]), domain_ids))
    return results

def get_units_for_user_assign(db, user_id):
    result = db.call_proc("sp_units_by_user_assign", (user_id,))
    return return_units(result)

def return_units_assign(units):
    results = []
    for unit in units:
        domain_ids = [int(x) for x in unit["domain_ids"].split(',') if x != '']
        results.append(core.Unit( unit["unit_id"], unit["division_id"], unit["legal_entity_id"],
            unit["business_group_id"], unit["client_id"], unit["unit_code"],
            unit["unit_name"], unit["address"], bool(unit["is_active"]), domain_ids))
    return results

######################################################################################
# To Get units under user
# Parameter(s) : Object of database, user id, request
# Return Type : Return list of units
######################################################################################
def get_unit_details_for_user(db, user_id, request):
    where_condition_val = [user_id]
    result = db.call_proc_with_multiresult_set("sp_tbl_unit_getunitdetailsforuser", where_condition_val, 2)
    return return_client_unit_list(result)

def return_client_unit_list(result):
    unitlist = []
    for r in result[0]:
        client_id = int(r.get("client_id"))
        business_group_id = r.get("business_group_id")
        legal_entity_id = int(r.get("legal_entity_id"))
        country_id = int(r.get("country_id"))
        country_name = r.get("country_name")
        client_name = r.get("group_name")
        business_group_name = r.get("b_group")
        legal_entity_name = r.get("l_entity")
        is_approved = int(r.get("is_approved"))
        unitlist.append(core.UnitList(client_id, business_group_id, legal_entity_id, country_id,
            country_name, client_name, business_group_name, legal_entity_name, is_approved))
    return unitlist

######################################################################################
# To Get units under user
# Parameter(s) : Object of database, user id, request
# Return Type : Return list of units
######################################################################################
def get_unit_details_for_user_edit(db, user_id, request):
    from_count = request.from_count
    if from_count > 0:
        from_count = from_count * request.page_count
    if(request.business_group_id is None or request.business_group_id == 0):
        where_condition_val = [request.client_id, '%', request.legal_entity_id, request.country_id, user_id, from_count, request.page_count]
    else:
        where_condition_val = [request.client_id, str(request.business_group_id), request.legal_entity_id, request.country_id, user_id, from_count, request.page_count]
    result = db.call_proc_with_multiresult_set("sp_tbl_unit_getunitdetailsforuser_edit", where_condition_val, 2)
    return return_unit_details(result)

def return_unit_details(result):
    unitdetails = []
    for r in result[0]:
        unit_id = int(r.get("unit_id"))
        client_id = int(r.get("client_id"))
        business_group_id = r.get("business_group_id")
        legal_entity_id = int(r.get("legal_entity_id"))
        country_id = int(r.get("country_id"))
        division_id = int(r.get("division_id"))
        category_name = r.get("category_name")
        geography_id = int(r.get("geography_id"))
        unit_code = r.get("unit_code")
        unit_name = r.get("unit_name")
        address = r.get("address")
        postal_code = r.get("postal_code")
        is_active = bool(r.get("is_active"))
        is_approved = int(r.get("is_approved"))
        category_id = int(r.get("category_id"))
        remarks = r.get("remarks")
        d_ids = []
        i_ids = []
        assign_count = []
        for domain in result[1]:
            if unit_id == domain.get("unit_id"):
                d_ids.append(int(domain.get("domain_id")))
                i_ids.append(int(domain.get("organisation_id")))
                assign_count.append(int(domain.get("assigned_count")))
        unitdetails.append(core.UnitDetails(
            unit_id, client_id, business_group_id, legal_entity_id, country_id, division_id,
            category_name, geography_id, unit_code, unit_name, address, postal_code,
            d_ids, i_ids, assign_count, is_active, is_approved, category_id, remarks ))
    return unitdetails

######################################################################################
# To Get groups list under user
# Parameter(s) : Object of database, user id
# Return Type : Return list of groups
######################################################################################
def get_group_companies_for_user_with_max_unit_count(db, user_id):
    result = db.call_proc("sp_tbl_unit_getuserclients", (user_id,))
    return return_group_companies_with_max_unit_count(db, result, user_id)

######################################################################################
# To return groups under user
# Parameter(s) : Object of database, user id, client list
# Return Type : Return clients list
######################################################################################
def return_group_companies_with_max_unit_count(db, group_companies, user_id):
    results = []
    for group_company in group_companies:
        countries = get_client_countries_for_unit(db, group_company["client_id"], user_id)
        domain_result = db.call_proc("sp_client_domains_by_group_id", (group_company["client_id"], user_id))
        domain_ids = [int(r["domain_id"]) for r in domain_result]
        next_auto_gen_no = get_next_auto_gen_number( db, group_company["short_name"], group_company["client_id"] )
        results.append(core.GroupCompanyForUnitCreation( group_company["client_id"], group_company["short_name"],
            countries, domain_ids, next_auto_gen_no ))
    return results

######################################################################################
# To Get countries under user and client
# Parameter(s) : Object of database, user id, client id
# Return Type : Return list of countries
######################################################################################
def get_client_countries_for_unit(db, client_id, user_id):
    rows = db.call_proc( "sp_tbl_units_getCountries", (client_id, user_id) )
    country_ids = [int(r["country_id"]) for r in rows]
    return country_ids

######################################################################################
# To Get next auto generated no. for unit under client
# Parameter(s) : Object of database, group name, client id
# Return Type : Return auttogenerated value
######################################################################################
def get_next_auto_gen_number(db, group_name=None, client_id=None):
    if group_name is None:
        condition_val = [client_id]
        rows = db.call_proc("sp_client_groups_details_by_id", condition_val)
        if rows:
            group_name = rows[0]["group_name"]
    condition_val = [client_id]
    rows = db.call_proc("sp_tbl_unit_getunitcount", condition_val)
    for r in rows:
        no_of_units = r["units"]
    group_name = group_name.replace(" ", "")
    unit_code_start_letters = group_name[:2].upper()
    condition_val = [unit_code_start_letters, client_id]
    rows = db.call_proc("sp_tbl_unit_getunitcode", condition_val)
    auto_generated_unit_codes = []
    for row in rows:
        try:
            auto_generated_unit_codes.append(int(row["code"]))
        except Exception, ex:
            print ex
            continue
    next_auto_gen_no = 1
    if len(auto_generated_unit_codes) > 0:
        existing_max_unit_code = max(auto_generated_unit_codes)
        if existing_max_unit_code == no_of_units:
            next_auto_gen_no = no_of_units + 1
        else:
            next_auto_gen_no = existing_max_unit_code + 1
    return next_auto_gen_no


def reactivate_unit_data(db, client_id, unit_id, session_user):
    action_column = [ "business_group_id", "legal_entity_id", "division_id",
        "country_id", "geography_id", "industry_id", "unit_code", "unit_name",
        "address", "postal_code", "domain_ids"]
    condition = "unit_id = %s "
    condition_val = [unit_id]
    result = db.get_data(tblUnits, action_column, condition, condition_val)
    result = result[0]
    action = "Reactivated Unit \"%s-%s\"" % (result["unit_code"], result["unit_name"])
    db.save_activity(session_user, frmClientUnit, action)
    next_auto_gen_no = get_next_auto_gen_number(db, client_id=client_id)
    unit_code = group_name[:2].upper()
    if len(str(next_auto_gen_no)) == 1:
        unit_code += "0000"
    elif len(str(next_auto_gen_no)) == 2:
        unit_code += "000"
    elif len(str(next_auto_gen_no)) == 3:
        unit_code += "00"
    elif len(str(next_auto_gen_no)) == 4:
        unit_code += "0"
    unit_code += "%s" % (next_auto_gen_no)
    unit_columns = ["client_id", "is_active", "legal_entity_id",
        "country_id", "geography_id", "industry_id", "unit_code", "unit_name",
        "address", "postal_code", "domain_ids"]
    values = [client_id, 1, result["legal_entity_id"],result["country_id"],
        result["geography_id"], result["industry_id"], unit_code, result["unit_name"],
        result["address"], result["postal_code"], result["domain_ids"]]
    if result["business_group_id"] not in ["Null", "None", None, ""]:
        unit_columns.append("business_group_id")
        values.append(result["business_group_id"])
    if result["division_id"] not in ["Null", "None", None, ""]:
        unit_columns.append("division_id")
        values.append(result["division_id"])
    if db.insert(tblUnits, unit_columns, values):
        return unit_code, result["unit_name"]
    else:
        raise process_error("E058")

def get_profiles(db, client_ids_list):
    ONE_GB = 1024 * 1024 * 1024
    profiles = []
    for client_id in client_ids_list:
        settings_rows = get_settings(db, client_id)
        contract_from = datetime_to_string(settings_rows[0]["contract_from"])
        contract_to = datetime_to_string(settings_rows[0]["contract_to"])
        no_of_user_licence = settings_rows[0]["no_of_user_licence"]
        file_space = settings_rows[0]["total_disk_space"]
        used_space = settings_rows[0]["total_disk_space_used"]
        licence_holder_rows = get_licence_holder_details(db, client_id)
        licence_holders = []
        for row in licence_holder_rows:
            employee_name = None
            unit_name = None
            if row["unit_name"] == None:
                unit_name = "-"
            else:
                unit_name = "%s - %s" % (row["unit_code"], row["unit_name"])
            user_id = row["user_id"]
            email_id = row["email_id"]
            contact_no = None if row["contact_no"] is "" else row["contact_no"]
            is_primary_admin = row["is_primary_admin"]
            is_active = row["is_active"]
            is_admin = row["is_admin"]
            if(row["employee_code"] == None):
                employee_name = row["employee_name"]
            elif (is_primary_admin == 1 and is_active == 1):
                employee_name = "Administrator"
            elif (is_primary_admin == 1 and is_active == 0):
                employee_name = "Old Administrator"
            else:
                employee_name = "%s - %s" % (row["employee_code"], row["employee_name"])
            address = row["address"]
            is_service_provider = False
            if unit_name == "-":
                if (is_primary_admin == 1 or is_admin == 1):
                    is_service_provider = False
                else:
                    is_service_provider = True
            used_val = round((used_space/ONE_GB), 2)
            licence_holders.append( technomasters.LICENCE_HOLDER_DETAILS(
                    user_id, employee_name, email_id, contact_no, unit_name, address,
                    file_space/ONE_GB, used_val, bool(is_active), bool(is_primary_admin),
                    is_service_provider))
        remaining_licence = (no_of_user_licence) - len(licence_holder_rows)
        total_free_space = round(file_space/ONE_GB, 2)
        total_used_space = round(used_space/ONE_GB, 2)
        profile_detail = technomasters.PROFILE_DETAIL(str(contract_from),
            str(contract_to), no_of_user_licence, remaining_licence,
            total_free_space, total_used_space, licence_holders)
        profiles.append(technomasters.PROFILES(client_id, profile_detail))
    return profiles

def get_settings(db, client_id):
    settings_columns = ["contract_from", "contract_to", "no_of_user_licence",
        "total_disk_space", "total_disk_space_used"]
    condition = "client_id = %s"
    condition_val = [client_id]
    return db.get_data(tblClientGroups, settings_columns, condition, condition_val)

def get_licence_holder_details(db, client_id):
    columns = ["tcu.user_id", "tcu.email_id", "tcu.employee_name", "tcu.employee_code",
        "tcu.contact_no", "tcu.is_primary_admin", "tu.unit_code", "tu.unit_name",
        "tu.address", "tcu.is_active", "tcu.is_admin"]
    tables = [tblClientUsers, tblUnits]
    aliases = ["tcu", "tu"]
    join_type = "left join"
    join_conditions = ["tcu.seating_unit_id = tu.unit_id"]
    where_condition = "tcu.client_id = %s"
    where_condition_val = [client_id]
    return db.get_data_from_multiple_tables( columns, tables, aliases, join_type,
        join_conditions, where_condition, where_condition_val)

def get_group_companies_for_user(db, user_id):
    result = {}
    client_ids = None
    if user_id is not None:
        client_ids = get_user_clients(db, user_id)
    columns = ["client_id", "group_name", "is_active"]
    condition, condition_val = db.generate_tuple_condition("client_id", client_ids)
    condition += " AND is_active = 1"
    order = " order by group_name ASC "
    result = db.get_data(tblClientGroups, columns, condition, [condition_val], order)
    return return_group_companies(db, result)

def return_group_companies(db, group_companies):
    results = []
    for group_company in group_companies:
        countries = get_client_countries(db, group_company["client_id"])
        domains = get_client_domains(db, group_company["client_id"])
        results.append(
            core.GroupCompany(group_company["client_id"], group_company["group_name"],
                bool(group_company["is_active"]), countries, domains)
        )
    return results

def get_user_client_countries(db, session_user):
    client_ids_list = get_client_ids(db)
    if len(client_ids_list) > 0:
        country_ids = []
        for client_id in client_ids_list:
            country_ids.extend(get_client_countries(db, int(client_id)))
        columns = "DISTINCT country_id as country_id, country_name, is_active"
        condition = "country_id in (%s) and is_active = 1 "
        condition_val = [",".join(str(x) for x in country_ids)]
        order = " ORDER BY country_name "
        result = db.get_data(tblCountries, columns, condition, condition_val, order)
        if result:
            return return_countries(result)
    else:
        return get_user_countries(db, session_user)

##########################################################################
#  To get list of legal entities with no of unassigned units
#  Parameters : Object of database
#  Return Type : Returns List of object of LegalEntities
##########################################################################
def get_assign_legalentities(db, session_user):
    legalentities = db.call_proc("sp_assign_legal_entities_list", [session_user])
    return return_assign_legalentities(legalentities)

##########################################################################
#  To get list of groups
#  Parameters : Object of database
#  Return Type : Returns List of object of LegalEntities
##########################################################################
def return_assign_legalentities(assign_legalentities_list):
    fn = generalprotocol.AssignLegalEntity
    assign_legalentities_list = [
        fn(legalentity["client_id"], legalentity["country_names"],
            legalentity["group_name"], legalentity["no_of_legal_entities"],
            legalentity["no_of_assigned_legal_entities"]
        ) for legalentity in assign_legalentities_list]
    return assign_legalentities_list

##########################################################################
#  To get Unassigned units list
#  Parameters : Object of database
#  Return Type : Returns List of object of UnassignedUnit
##########################################################################
def get_unassigned_units_list(db, session_user):
    units = db.call_proc_with_multiresult_set("sp_userunits_list", [session_user], 2)
    return return_unassigned_units(units[1])

###############################################################################
#  To convert data fetched from database into List of object of UnassignedUnit
#  Parameters : Object fetched from database
#  Return Type : Returns List of object of UnassignedUnit
###############################################################################
def return_unassigned_units(data):
    assigned_total = 0
    result = []
    for datum in data:
        assigned_total = "%s / %s" % (datum["total_units"] - datum["assigned_units"], datum["total_units"])
        result.append(technomasters.UnassignedUnit( domain_name=datum["domain_name"],
            group_name=datum["client_name"], legal_entity_name=datum["legal_entity_name"],
            business_group_name=datum["business_group_name"], unassigned_units=assigned_total,
            domain_id=datum["domain_id"], client_id=datum["client_id"],
            legal_entity_id=datum["legal_entity_id"] ))
    return result

###############################################################################
#  To get list of assigned units
#  Parameters : Object of database, Received request
#  Return Type : Returns List of object of AssignedUnit
###############################################################################
def get_assigned_units_list(db, request, user_id):
    domain_id = request.domain_id
    client_id = request.client_id
    legal_entity_id = request.legal_entity_id
    units = db.call_proc_with_multiresult_set(
        "sp_userunits_assigned_list", (client_id, domain_id, legal_entity_id, user_id), 2 )
    return return_assigned_units(units[1])

###############################################################################
#  To convert data fetched from database into list of object of Assigned unit
#  Parameters : Data fetched from database (Tuple of tuples)
#  Return Type : Returns List of object of AssignedUnit
###############################################################################
def return_assigned_units(data):
    fn = technomasters.AssignedUnit
    result = [fn (
                user_id=datum["user_id"], employee_name=datum["employee_name"],
                business_group_name=datum["business_group_name"],
                legal_entity_id=datum["legal_entity_id"], legal_entity_name=datum["legal_entity_name"],
                unit_count=datum["no_of_units"], user_category_id=datum["user_category_id"],
                client_id=datum["client_id"], domain_id=datum["domain_id"]
            ) for datum in data
    ]
    return result

###############################################################################
#  To get details of assigned units
#  Parameters : Object of database, Received request
#  Return Type : Returns List of object of AssignedUnitDetails
###############################################################################
def get_assigned_unit_details_list(db, request):
    legal_entity_id = request.legal_entity_id
    user_id = request.user_id
    client_id = request.client_id
    domain_id = request.domain_id
    units, industry_details = db.call_proc_with_multiresult_set(
        "sp_userunits_assigned_details_list", (user_id, legal_entity_id, client_id, domain_id), 2 )
    unit_industry_name_map = generate_unit_domain_industry_map(industry_details)
    return return_assigned_unit_details(units, unit_industry_name_map)

###############################################################################
#  To convert data fetched from database into list of object of
#  AssignedUnitDetails
#  Parameters : Unit data, Unit - industry name map (Dict)
#  Return Type : Returns List of object of AssignedUnitDetails
###############################################################################
def return_assigned_unit_details(units, unit_industry_name_map):
    fn = technomasters.AssignedUnitDetails
    result = [ fn( unit_id=unit["unit_id"], legal_entity_name=unit["legal_entity_name"],
            division_name=unit["division_name"], category_name=unit["category_name"],
            unit_code=unit["unit_code"], unit_name=unit["unit_name"], address=unit["address"],
            domain_names=unit_industry_name_map[unit["unit_id"]].keys(),
            org_names_list=unit_industry_name_map[unit["unit_id"]].values(),
            geography_name=unit["geography_name"] ) for unit in units ]
    return result

###############################################################################
#  To convert data fetched from database into list of object of
#  AssignedUnitDetails
#  Parameters : Unit data, Unit - industry name map (Dict)
#  Return Type : Returns List of object of AssignedUnitDetails
###############################################################################
def get_data_for_assign_unit(db, request, session_user):
    business_groups = get_business_groups_for_client(db, request.client_id)
    legal_entities = get_legal_entities_for_client(db, request.client_id)
    units = get_units_of_client(db, request.client_id, request.domain_id, request.legal_entity_id, session_user)
    domain_managers, mapped_domain_users = get_domain_managers_for_user(db, request.client_id, request.domain_id, session_user)
    return business_groups, legal_entities, units, domain_managers, mapped_domain_users

###############################################################################
#  To get business groups under a client
#  Parameters : Object of database, client id
#  Return Type : Returns List of object of BusinessGroup
###############################################################################
def get_business_groups_for_client(db, client_id):
    data = db.call_proc("sp_business_groups_by_client", (client_id,))
    return return_business_groups(data)

###############################################################################
#  To get Legal entities under a client
#  Parameters : Object of database, client id
#  Return Type : Returns List of object of Legal Entity
###############################################################################
def get_legal_entities_for_client(db, client_id):
    data = db.call_proc("sp_legal_entities_by_client", (client_id,))
    return return_legal_entities_for_unit(data)

###############################################################################
#  To get Legal entities under a client
#  Parameters : Object of database, client id
#  Return Type : Returns List of object of Legal Entity
###############################################################################
def get_domain_managers_for_user(db, client_id, domain_id, session_user):
    users = db.call_proc_with_multiresult_set("sp_users_domain_managers", [session_user, domain_id, client_id], 3)
    return return_domain_managers(users)

def return_domain_managers(data):
    fn = core.User
    result = [ fn( user_id=datum["user_id"], user_category_id=datum["user_category_id"],
            employee_name=datum["employee_name"], is_active=bool(datum["is_active"]) ) for datum in data[1] ]
    fn = core.DomainUser
    domain_user_list = [ fn( user_id=datum["user_id"], legal_entity_id=datum["legal_entity_id"]
        ) for datum in data[2] ]
    return result, domain_user_list

######################################################################################
# To Get units under user,client, domain and legal entity
# Parameter(s) : Object of database, user id, client id, domain id, legal entity id
# Return Type : Return list of units
######################################################################################
def get_units_of_client(db, client_id, domain_id, legal_entity_id, session_user):
    result = db.call_proc_with_multiresult_set(
        "sp_units_list", (client_id, domain_id, legal_entity_id, session_user), 3)
    units = result[1]
    industry_details = result[2]
    domain_industry_map = generate_unit_domain_industry_map(industry_details)
    return return_assigned_unit_details(units, domain_industry_map)

def generate_unit_domain_industry_map(industry_details):
    detail_map = {}
    for detail in industry_details:
        unit_id = detail["unit_id"]
        domain_name = detail["domain_name"]
        industry_name = detail["organisation_name"]
        if unit_id not in detail_map:
            detail_map[unit_id] = {}
        if domain_name not in detail_map[unit_id]:
            detail_map[unit_id][domain_name] = []
        detail_map[unit_id][domain_name].append(industry_name)
    return detail_map

######################################################################################
# To Get user category id by user id
# Parameter(s) : Object of database, user id
# Return Type : Return user category id
######################################################################################
def get_user_category_id(db, session_user):
    result = db.call_proc("sp_get_user_category_id_by_userid", (int(session_user),))
    return result[0]["user_category_id"]

######################################################################################
# To save assigned units
# Parameter(s) : Object of database, user id, requests
# Return Type : Return value of the assigned units
######################################################################################
def save_assigned_units(db, request, session_user):
    domain_manager_id = request.user_id
    client_id = request.client_id
    active_units = request.active_units
    values_list = []
    unit_names = []
    current_time_stamp = get_date_time()
    domains = get_user_domains(db, session_user)
    user_category_id = get_user_category_id(db, domain_manager_id)
    domain_name_id_map = {}
    for domain in domains:
        domain_name_id_map[domain.domain_name] = domain.domain_id
    columns = [
        "user_id", "user_category_id", "client_id", "legal_entity_id",
        "unit_id", "domain_id", "assigned_by", "assigned_on"
        ]
    for unit in active_units:
        value_tuple = (
            domain_manager_id, user_category_id, client_id,  unit.legal_entity_id,
            unit.unit_id, domain_name_id_map[unit.domain_name], session_user, current_time_stamp)
        values_list.append(value_tuple)
        print "a"
        print value_tuple
        db.call_insert_proc(
            "sp_assign_client_unit_save", (
                domain_manager_id, unit.unit_id,
                domain_name_id_map[unit.domain_name], None, session_user, current_time_stamp
            )
        )
        unit_name = db.call_proc("sp_unitname_by_id", (unit.unit_id,))
        for r in unit_name:
            unit_names.append(r["unit_name"])
    res = db.bulk_insert(tblUserUnits, columns, values_list)
    action = "Assigned following Units %s" % (",".join(unit_names))
    db.save_activity(session_user, 19, action)
    if res is False:
        raise process_error("E080")
    return res

def get_user_domain(user_id, data):
    domain_ids = []
    for r in data:
        if int(r["user_id"]) == user_id:
            domain_ids.append(admin.CountryWiseDomain(int(r["country_id"]), int(r["domain_id"])))
    return domain_ids

def return_users(data, country_map, domain_map, mapped_country_domains):
    fn = admin.MappedUser
    result = []
    for datum in data:
        user_id = int(datum["user_id"])
        e_name = datum["employee_name"]
        user = fn(
            user_id=user_id, employee_name=e_name,
            is_active=bool(datum["is_active"]),
            country_ids=country_map[user_id],
            domain_ids=domain_map[user_id],
            mapped_country_domains = get_user_domain(user_id, mapped_country_domains))
        result.append(user)
    return result

def generate_country_map(countries):
    country_map = {}
    for country in countries:
        user_id = country["user_id"]
        if user_id not in country_map:
            country_map[user_id] = []
        country_map[user_id].append(
            int(country["country_id"]))
    return country_map

def generate_domain_map(domains):
    domain_map = {}
    for domain in domains:
        user_id = domain["user_id"]
        if user_id not in domain_map:
            domain_map[user_id] = []
        domain_map[user_id].append(
            int(domain["domain_id"]))
    return domain_map

##########################################################################
#  To get details of a client by id
#  Parameters : Object of database, client id
#  Return Type : Tuple with group name, username, legal entities and
#  date configurations
##########################################################################
def get_unassigned_legal_entity(db, client_id):
    legal_entities = db.call_proc_with_multiresult_set(
        "sp_unassigned_legal_entity_details_by_group_id", (client_id,), 2)
    legal_entities = return_unassigned_legal_entities(
        legal_entities[0], legal_entities[1])
    return (legal_entities)

def get_techno_users_list(db, session_user):
    result = db.call_proc_with_multiresult_set("sp_users_technouser_list", (session_user,), 3)
    user_countries = result[1]
    user_domains = result[2]
    techno_users_result = result[0]
    mapped_country_domains = result[3]
    user_countries_map = generate_country_map(user_countries)
    user_domains_map = generate_domain_map(user_domains)
    techno_users = return_users(
        techno_users_result, user_countries_map, user_domains_map, mapped_country_domains)
    return (techno_users)

def get_le_domains(legl_entity_id, data):
        domain_ids = []
        for r in data:
            if int(r["legal_entity_id"]) == legl_entity_id:
                domain_ids.append(int(r["domain_id"]))
        return domain_ids

##########################################################################
#  To convert the data fetched from database into Legal entity object
#  Parameters : Legal entity tuple, incharge person tuple, domain tuple
#  Return Type : List of object of Legal entities
##########################################################################
def return_unassigned_legal_entities(legal_entities, domain_ids):
    results = []
    for legal_entity in legal_entities:
        results.append(generalprotocol.UnAssignLegalEntity(
                legal_entity_id=legal_entity["legal_entity_id"],
                legal_entity_name=legal_entity["legal_entity_name"],
                business_group_name=legal_entity["business_group_name"],
                c_name=legal_entity["country_name"], c_id=legal_entity["country_id"],
                domain_ids=get_le_domains(legal_entity["legal_entity_id"], domain_ids) ))
    return results

##########################################################################
#  To Save Assign Legal Entity
##########################################################################
def save_assign_legal_entity(db, client_id, legal_entity_ids, user_ids, session_user):
    values_list = []
    current_time_stamp = get_date_time()
    group_name = get_group_by_id(db, client_id)
    legal_entity_names = ''

    admin_users_id = []
    res = db.call_proc("sp_users_under_user_category", (1,))
    for user in res:
        admin_users_id.append(user["user_id"])
    columns = ["user_id", "client_id", "legal_entity_id", "assigned_by", "assigned_on"]
    for user_id in user_ids:
        name_rows = db.call_proc("sp_empname_by_id", (user_id,))
        user_name = name_rows[0]["empname"]
        for legal_entity_id in legal_entity_ids:
            legal_entity_name = get_legal_entity_by_id(db, legal_entity_id)
            if legal_entity_names == '':
                legal_entity_names = legal_entity_name
            else:
                legal_entity_names = legal_entity_names + ', ' +legal_entity_name
            values_tuple = ( user_id, client_id, legal_entity_id, session_user, current_time_stamp)
            values_list.append(values_tuple)
    res = db.bulk_insert(tblUserLegalEntity, columns, values_list)
    message_text = '%s for the Group \"%s\" has been assigned to %s' % (legal_entity_names, group_name, user_name)
    db.save_toast_messages(6, "Assign Legal Entity", message_text, None, user_ids, session_user)
    db.save_toast_messages(1, "Assign Legal Entity", message_text, None, admin_users_id, session_user)
    action = "New Legal entity assigned for %s" % (user_name)
    db.save_activity(session_user, 18, action)
    if res is False:
        raise process_error("E041")
    return res

def get_assigned_legal_entity(db, client_id):
    legal_entities = db.call_proc( "sp_assigned_legal_entity_details_by_group_id", (client_id,))
    legal_entities = return_assigned_legal_entities(legal_entities)
    return (legal_entities)

def return_assigned_legal_entities(legal_entities):
    results = []
    for legal_entity in legal_entities:
        results.append(generalprotocol.AssignedLegalEntity(
                legal_entity_id=legal_entity["legal_entity_id"],
                legal_entity_name=legal_entity["legal_entity_name"],
                business_group_name=legal_entity["business_group_name"],
                c_name=legal_entity["country_name"], c_id=legal_entity["country_id"],
                employee_name=legal_entity["employee_name"] ) )
    return results

def unassignDomainUnits(db, unit_id, domain_ids, session_user):
    result = db.call_proc("sp_userunits_delete", (unit_id, domain_ids))
    unit_name = db.call_proc("sp_unitname_by_id", (unit_id,))
    for r in unit_name:
        u_name = r["unit_name"]
    domains = get_user_domains(db, session_user)
    name_rows = db.call_proc("sp_empname_by_id", (session_user,))
    user_name = name_rows[0]["empname"]
    for domain in domains:
        if domain.domain_id == domain_ids:
            domainName = domain.domain_name
    action = "%s under %s has been unassigned for %s" % (u_name, domainName, user_name)
    db.save_activity(session_user, 22, action)
    return result

###############################################################################
# To Get the group name  by it's id
# Parameter(s) : Object of database, client id
# Return Type : Group name (String)
###############################################################################
def get_group_by_id(db, group_id):
    result = db.call_proc("sp_group_by_id", (group_id,))
    group_name = result[0]["group_name"]
    return group_name

###############################################################################
# To Get the legal entity name  by it's id
# Parameter(s) : Object of database, legal entity id
# Return Type : Legal Entity name (String)
###############################################################################
def get_legal_entity_by_id(db, le_id):
    result = db.call_proc("sp_legal_entity_by_id", (le_id,))
    legal_entity_name = result[0]["legal_entity_name"]
    return legal_entity_name
