from protocol import (
    core, technomasters
)
from server.exceptionmessage import process_error
from server.constants import (CLIENT_LOGO_PATH)
from server.common import (
    datetime_to_string, get_date_time,
    string_to_datetime, remove_uploaded_file,
    convert_base64_to_file, new_uuid
)
from server.database.tables import *
from server.database.validateclientuserrecord import ClientAdmin


#
# Client Group List
#
##########################################################################
#  To get countries assigned to the session user
#  Parameters : Object of database and  session user id (int)
#  Return Type : List of object of Country
##########################################################################
def get_user_countries(db, session_user):
    countries = db.call_proc(
        "sp_countries_for_user", (session_user,)
    )
    return return_countries(countries)


##########################################################################
#  To convert the data fetched from database to list of object of country
#  Parameters : Data fetched from database (Tuple of tuples)
#  Return Type : List of object of Country
##########################################################################
def return_countries(data):
    fn = core.Country
    results = [
        fn(
           d["country_id"], d["country_name"], bool(d["is_active"])
        ) for d in data
    ]
    return results


##########################################################################
#  To Get business groups under a client
#  Parameters : Object of database and client id
#  Return Type : List of object of BusinessGroup
##########################################################################
def get_client_business_groups(db, client_id):
    business_groups = db.call_proc(
        "sp_business_groups_list", (client_id,)
    )
    return return_business_groups(business_groups)


##########################################################################
#  To convert the data fetched from database to list of
#  Object of Business group
#  Parameters : Data fetched from database (tuple of tuples)
#  Return Type List of object of BusinessGroup
##########################################################################
def return_business_groups(business_groups):
    results = []
    for business_group in business_groups:
        results.append(core.BusinessGroup(
            business_group["business_group_id"],
            business_group["business_group_name"],
            business_group["client_id"]
        ))
    return results


##########################################################################
#  To get domains assigned to the session user
#  Parameters : Object of database and  session user id (int)
#  Return Type : List of object of Domain
##########################################################################
def get_user_domains(db, session_user):
    domains = db.call_proc(
        "sp_domains_for_user", (session_user,)
    )
    return return_domains(domains)


##########################################################################
#  To convert data fetched from database into list of Object of Domain
#  Parameters : Data fetched from database (Tuple of tuples)
#  Return Type : List of object of Domain
##########################################################################
def return_domains(data):
    fn = core.Domain
    results = [
        fn(
            d["domain_id"], d["domain_name"], bool(d["is_active"])
        ) for d in data
    ]
    return results


##########################################################################
#  To get all active industries
#  Parameters : Object of database
#  Return Type : List of object of Industry
##########################################################################
def get_active_industries(db):
    domains = db.call_proc(
        "sp_industries_active_list", None
    )
    return return_industries(domains)


##########################################################################
#  To convert data fetched from database into list of object of Industry
#  Parameters : Data fetched from database
#  Return Type List of object of Industry
##########################################################################
def return_industries(data):
    fn = core.Industries
    results = [
        fn(
            d["industry_id"], d["industry_name"], bool(d["is_active"])
        ) for d in data
    ]
    return results


#
# Client Group Save/ Update
#
##########################################################################
#  To Save client group (name and group admin)
#  Parameters : Object of database, group name and group admin username
#  Return Type : client id  (Int)
##########################################################################
def save_client_group(
    db, group_name, username, short_name, no_of_view_licence, session_user
):
    client_id = db.call_insert_proc(
        "sp_client_group_save",
        (group_name, username, short_name, no_of_view_licence, session_user)
    )
    return client_id


##########################################################################
#  To Update client group (group name)
#  Parameters : Object of database, group name and client id
#  Return Type : None
##########################################################################
def update_client_group(db, group_name, client_id):
    db.call_update_proc(
        "sp_client_group_update", (group_name, client_id)
    )


##########################################################################
#  To Save group admin as a client user under the client
#  Parameters : Object of database, client id, group admin username
#  Return Type : Raises Process error if insertion fails / returns True
##########################################################################
def save_client_user(db, client_id, username):
    current_time_stamp = get_date_time()
    r = db.call_insert_proc(
        "sp_client_user_save_admin",
        (client_id, username, current_time_stamp)
    )
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
        "client_id", "country_id", "business_group_id",
        "legal_entity_name", "contract_from", "contract_to", "logo",
        "file_space_limit", "total_licence",
        'is_active', "created_by", "created_on", 'updated_by', "updated_on"
    ]
    values = []
    current_time_stamp = get_date_time()
    legal_entity_names = []
    for entity in request.legal_entity_details:
        if is_logo_in_image_format(entity.logo):
            file_name = save_client_logo(entity.logo)
        else:
            raise process_error("E067")
        business_group_id = return_business_group_id(
            db, entity, group_id, session_user, current_time_stamp
        )
        if is_duplicate_legal_entity(
            db, None, entity.legal_entity_name, group_id
        ):
            raise process_error("E068")
        legal_entity_names.append(entity.legal_entity_name)
        value_tuple = (
            group_id, entity.country_id, business_group_id,
            entity.legal_entity_name,
            string_to_datetime(entity.contract_from),
            string_to_datetime(entity.contract_to),
            file_name, entity.file_space, entity.no_of_licence,
            1, session_user, current_time_stamp,
            session_user, current_time_stamp
        )
        values.append(value_tuple)
    db.bulk_insert(
        tblLegalEntities, columns, values
    )
    return legal_entity_names


##########################################################################
#  To Update List of legal entites under a Client
#  Parameters : Object of database, Request, client id, session user id
#  Return Type : List of legal entity names
##########################################################################
def update_legal_entities(db, request, group_id, session_user):
    columns = [
        "country_id", "business_group_id",
        "legal_entity_name", "contract_from", "contract_to", "logo",
        "file_space_limit", "total_licence", 'updated_by', "updated_on"
    ]
    insert_columns = [
        "client_id", "country_id", "business_group_id",
        "legal_entity_name", "contract_from", "contract_to", "logo",
        "file_space_limit", "total_licence",
        'is_active', "created_by", "created_on", 'updated_by', "updated_on"
    ]
    values = []
    insert_values = []
    conditions = []
    current_time_stamp = get_date_time()
    legal_entity_names = []
    for entity in request.legal_entities:
        if(entity.new_logo is not None):
            if is_logo_in_image_format(entity.new_logo):
                file_name = save_client_logo(entity.new_logo)
            else:
                raise process_error("E067")
        else:
            file_name = entity.old_logo
        business_group_id = return_business_group_id(
            db, entity, group_id, session_user, current_time_stamp
        )
        if is_duplicate_legal_entity(
            db, entity.legal_entity_id, entity.legal_entity_name, group_id
        ):
            raise process_error("E068")
        elif validate_total_disk_space(
            db, entity.file_space, group_id, entity.legal_entity_id
        ):
            raise process_error("E069")
        elif validate_no_of_user_licence(
            db, entity.no_of_licence, group_id, entity.legal_entity_id
        ):
            raise process_error("E070")
        legal_entity_names.append(entity.legal_entity_name)
        if entity.legal_entity_id is not None:
            value_tuple = (
                entity.country_id, business_group_id,
                entity.legal_entity_name,
                string_to_datetime(entity.contract_from),
                string_to_datetime(entity.contract_to),
                file_name, entity.file_space, entity.no_of_licence, 1,
                session_user, current_time_stamp
            )
            values.append(value_tuple)
            condition = "client_id=%s and legal_entity_id=%s" % (
                group_id, entity.legal_entity_id)
            conditions.append(condition)
        else:
            insert_value_tuple = (
                group_id, entity.country_id, business_group_id,
                entity.legal_entity_name,
                string_to_datetime(entity.contract_from),
                string_to_datetime(entity.contract_to),
                file_name, entity.file_space, entity.no_of_licence,
                1, session_user, current_time_stamp,
                session_user, current_time_stamp
            )
            insert_values.append(insert_value_tuple)
    if db.bulk_insert(
        tblLegalEntities, insert_columns, insert_values
    ) is False:
        raise process_error("E052")
    if db.bulk_update(
        tblLegalEntities, columns, values, conditions
    ) is True:
        return legal_entity_names
    else:
        raise process_error("E052")


##########################################################################
#  To Save / Update Business group
#  Parameters : Object of database, Request, client id, session user id,
#  current time stamp
#  Return Type : Business group id (Int)
##########################################################################
def return_business_group_id(
    db, request, group_id, session_user, current_time_stamp
):
    if request.business_group is None:
        return None
    elif request.business_group.business_group_id is not None:
        return request.business_group.business_group_id
    else:
        business_group_name = request.business_group.business_group_name
        if is_duplicate_business_group(
            db, None, business_group_name, group_id
        ):
            raise process_error("E066")
        else:
            business_group_id = db.call_insert_proc(
                "sp_business_group_save", (
                    business_group_name, group_id, request.country_id,
                    session_user, current_time_stamp
                )
            )
            return business_group_id


##########################################################################
#  To Save date configurations of a client
#  Parameters : Object of database, client id, date configurations,
#  session user id
#  Return Type : List of country ids under the client
##########################################################################
def save_date_configurations(
    db, client_id, date_configurations, session_user
):
    values_list = []
    current_time_stamp = get_date_time()
    db.call_update_proc(
        "sp_client_configurations_delete", (client_id, )
    )
    columns = [
        "client_id", "country_id", "domain_id", "period_from",
        "period_to", "updated_by", "updated_on"
    ]
    for configuration in date_configurations:
        value_tuple = (
            client_id, configuration.country_id, configuration.domain_id,
            configuration.period_from, configuration.period_to,
            session_user, current_time_stamp
        )
        values_list.append(value_tuple)
    res = db.bulk_insert(
        tblClientConfigurations, columns, values_list
    )
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
    result = db.call_proc(
        "sp_legal_entity_id_by_name", (",".join(legal_entity_names),)
    )
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
    db.call_update_proc(
        "sp_client_domains_delete", (client_id, )
    )
    values_list = []
    columns = ["client_id", "legal_entity_id", "domain_id"]

    if hasattr(request, "legal_entity_details"):
        entity_details = request.legal_entity_details
    else:
        entity_details = request.legal_entities
    for entity in entity_details:
        for domain in entity.domain_details:
            value_tuple = (
                client_id, legal_entity_name_id_map[
                    entity.legal_entity_name
                ], domain.domain_id
            )
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
def save_incharge_persons(db, client_id, request, legal_entity_id_name_map):
    db.call_update_proc(
        "sp_user_clients_delete", (client_id, )
    )
    values_list = []
    columns = ["client_id", "legal_entity_id", "user_id"]
    for entity in request.legal_entities:
        for incharge_person in entity.incharge_persons:
            values_tuple = (
                client_id, legal_entity_id_name_map[entity.legal_entity_name],
                incharge_person
            )
            values_list.append(values_tuple)
    r = db.bulk_insert(tblUserClients, columns, values_list)
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
def save_organization(
    db, group_id, request, legal_entity_name_id_map, session_user
):
    current_time_stamp = get_date_time()
    db.call_update_proc(
        "sp_le_domain_industry_delete", (group_id, )
    )
    columns = [
        "legal_entity_id", "domain_id", "organization_id",
        "activation_date", "count", "created_by", "created_on"
    ]
    values_list = []
    if hasattr(request, "legal_entity_details"):
        entity_details = request.legal_entity_details
    else:
        entity_details = request.legal_entities
    for entity in entity_details:
        legal_entity_name = entity.legal_entity_name
        domain_details = entity.domain_details
        for domain in domain_details:
            domain_id = domain.domain_id
            organization = domain.organization
            for org in organization:
                value_tuple = (
                    legal_entity_name_id_map[legal_entity_name],
                    domain_id, org, current_time_stamp,
                    organization[org], session_user,
                    current_time_stamp
                )
                values_list.append(value_tuple)
    r = db.bulk_insert(tblLegalEntityDomains, columns, values_list)
    if r is False:
        raise process_error("E071")
    return r


##########################################################################
#  To Check whether the group name already exists
#  Parameters : Object of database, group name, client id (Optional)
#  Return Type : Boolean - Returns true if group name already exists
#   returns False if there is no duplicates
##########################################################################
def is_duplicate_group_name(db, group_name, client_id=None):
    count_rows = db.call_proc(
        "sp_client_group_is_duplicate_groupname",
        (group_name, client_id)
    )
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
def is_duplicate_business_group(
    db, business_group_id, business_group_name, client_id
):
    count_rows = db.call_proc(
        "sp_businessgroup_is_duplicate_businessgroupname",
        (business_group_name, business_group_id, client_id)
    )
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
def is_duplicate_legal_entity(
    db, legal_entity_id, legal_entity_name, client_id
):
    count_rows = db.call_proc(
        "sp_legalentity_is_duplicate_legalentityname",
        (legal_entity_name, legal_entity_id, client_id)
    )
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
    if exten in ["png", "jpg", "jpeg"]:
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


#
#   Getting data for Editing Client Group
#
##########################################################################
#  To get details of a client by id
#  Parameters : Object of database, client id
#  Return Type : Tuple with group name, username, legal entities and
#  date configurations
##########################################################################
def get_client_details(db, client_id):
    client_details = db.call_proc(
        "sp_client_groups_details_by_id", (client_id,)
    )
    legal_entities = db.call_proc(
        "sp_legal_entity_details_by_group_id", (client_id,)
    )
    date_configurations = db.call_proc(
        "sp_client_configuration_by_group_id", (client_id,)
    )
    organizations = db.call_proc(
        "sp_le_d_industry_by_group_id", (client_id,)
    )
    group_name = client_details[0]["group_name"]
    user_name = client_details[0]["email_id"]
    short_name = client_details[0]["short_name"]
    total_view_licence = client_details[0]["total_view_licence"]
    domain_map = return_organization_by_legalentity_domain(
        organizations
    )
    legal_entities = return_legal_entities(
        legal_entities, domain_map
    )
    date_configuration_list = return_date_configurations(
        date_configurations
    )
    return (
        group_name, user_name, short_name, total_view_licence,
        legal_entities, date_configuration_list
    )


##########################################################################
#  To convert the data fetched from database into Legal entity object
#  Parameters : Legal entity tuple, incharge person tuple, domain tuple
#  Return Type : List of object of Legal entities
##########################################################################
def return_legal_entities(legal_entities, domains):
    results = []
    print "domains : %s" % domains
    for legal_entity in legal_entities:
        if legal_entity["business_group_id"] is None:
            business_group = None
        else:
            business_group = core.ClientBusinessGroup(
                business_group_id=legal_entity["business_group_id"],
                business_group_name=legal_entity["business_group_name"]
            )
        results.append(
            core.LegalEntity(
                country_id=legal_entity["country_id"],
                business_group=business_group,
                legal_entity_id=legal_entity["legal_entity_id"],
                legal_entity_name=legal_entity["legal_entity_name"],
                old_logo=legal_entity["logo"],
                new_logo=None,
                no_of_licence=legal_entity["total_licence"],
                file_space=int(legal_entity["file_space_limit"]),
                contract_from=datetime_to_string(
                    legal_entity["contract_from"]),
                contract_to=datetime_to_string(legal_entity["contract_to"]),
                domain_details=domains[legal_entity["legal_entity_id"]]
            )
        )
    return results


##########################################################################
#  To convert the data fetched from database into a dict
#  Parameters : Organization details fetched from database (Tuple of
#  tuples )
#  Return Type : Dictionary
##########################################################################
def return_organization_by_legalentity_domain(organizations):
    organization_map = {}
    domain_map = {}
    for row in organizations:
        legal_entity_id = row["legal_entity_id"]
        domain_id = row["domain_id"]
        industry_id = row["organization_id"]
        no_of_units = row["count"]
        activation_date = row["activation_date"]
        if legal_entity_id not in domain_map:
            domain_map[legal_entity_id] = []
        if legal_entity_id not in organization_map:
            organization_map[legal_entity_id] = {}
        if domain_id not in organization_map[legal_entity_id]:
            organization_map[legal_entity_id][domain_id] = {}
        if industry_id not in organization_map[legal_entity_id][domain_id]:
            organization_map[
                legal_entity_id][domain_id][str(industry_id)] = no_of_units
        organization_map[
            legal_entity_id][domain_id][str(industry_id)] = no_of_units
        domain_map[legal_entity_id].append(
            core.EntityDomainDetails(
                domain_id=domain_id,
                activation_date=datetime_to_string(activation_date),
                organization=organization_map[
                    int(legal_entity_id)][int(domain_id)]
            )
        )
    return domain_map


##########################################################################
#  To convert data configuration details fetched from database into
#  list of object of ClientConfiguration
#  Parameters : Data fetched from database (Tuple of tuples)
#  Return Type : List of object of ClientConfiguration
##########################################################################
def return_date_configurations(date_configurations):
    results = [
        core.ClientConfiguration(
            country_id=config["country_id"],
            domain_id=config["domain_id"],
            period_from=config["period_from"],
            period_to=config["period_to"]
        ) for config in date_configurations
    ]
    return results


#
#   To Update Client
#
##########################################################################
#  To check whether the client id is valid or not
#  Parameters : Object of database, client id
#  Return Type : Boolean - True if client id is valid, False if invalid
##########################################################################
def is_invalid_group_id(db, client_id):
    count_rows = db.call_proc(
        "sp_client_groups_is_valid_group_id", (client_id,)
    )
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
    rows = db.call_proc(
        "sp_client_countries_by_group_id", (client_id,)
    )
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
            domain["domain_id"]
        )
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
    results = [
        fn(
            int(user["user_id"]), user["e_name"],
            bool(user["is_active"]),
            user_country_map[int(user["user_id"])],
            user_domain_map[int(user["user_id"])]
        ) for user in users
    ]
    return results


##########################################################################
#  To get list of groups
#  Parameters : Object of database
#  Return Type : Returns List of object of ClientGroup
##########################################################################
def get_groups(db):
    groups = db.call_proc(
        "sp_client_groups_list", None
    )
    return return_group(groups)


##########################################################################
#  To get list of groups
#  Parameters : Object of database
#  Return Type : Returns List of object of ClientGroup
##########################################################################
def return_group(groups):
    fn = core.ClientGroup
    client_list = [
        fn(
            group["client_id"], group["group_name"],
            group["country_names"], group["no_of_legal_entities"],
            True if group["is_active"] > 0 else False,
            int(group["is_approved"]), group["remarks"]
        ) for group in groups
    ]
    return client_list


##########################################################################
#  To check Wheteher the entered no of licence is less than already
#  existing number of users
#  Parameters : Object of database, New no of user licence entered,
#   client id, legal entitiy id
#  Return Type : Returns true if entered no of licence is less than already
#  existing number of users otherwise returns false
##########################################################################
def validate_no_of_user_licence(
    db, no_of_user_licence, client_id, legal_entity_id
):
    rows = db.call_proc(
        "sp_client_users_count", (client_id, legal_entity_id)
    )
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
def validate_total_disk_space(
    db, file_space, client_id, legal_entity_id
):
    if legal_entity_id is None:
        return False
    rows = db.call_proc(
        "sp_legal_entities_space_used", (legal_entity_id,),
    )
    used_space = int(rows[0]["used_space"])
    if file_space < used_space:
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
    rows = db.get_data(
        tblUserClients, columns, condition
    )
    client_ids = []
    if rows:
        client_ids.append(str(rows[0]["client_id"]))
    return client_ids


def get_client_domains(db, client_id):
    columns = "domain_id"
    condition = "client_id = %s "
    condition_val = [client_id]
    rows = db.get_data(tblClientDomains, columns, condition, condition_val)
    domain_ids = [
        int(r["domain_id"]) for r in rows
    ]
    return domain_ids


def get_user_client_domains(db, session_user):
    result = db.call_proc("sp_tbl_unit_getclientdomains", (session_user,0))
    if result:
        return return_domains(result)
    else:
        result = db.call_proc("sp_tbl_unit_getclientdomains", (session_user,1))
        return return_domains(result)


def get_date_configurations(db, client_id):
    columns = "country_id, domain_id, period_from, period_to"
    condition = "client_id=%s"
    condition_val = [client_id]
    result = db.get_data(
        tblClientConfigurations, columns, condition,
        condition_val
    )
    return return_client_configuration(result)


def return_client_configuration(configurations):
    fn = core.ClientConfiguration
    results = [
        fn(
            configuration["country_id"], configuration["domain_id"],
            configuration["period_from"], configuration["period_to"]
        ) for configuration in configurations
    ]
    return results


def get_server_details(db):
    columns = ["ip", "server_username", "server_password", "port"]
    condition = "server_full = 0 "
    _order = "ORDER BY length ASC limit 1"
    rows = db.get_data(
        tblDatabaseServer, columns, condition,
        condition_val=None, order=_order
    )
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



def update_client_logo(db, logo, client_id):
    column = "logo_url"
    condition = "client_id = %s "
    condition_val = [client_id]
    rows = db.get_data(
        tblClientGroups, column, condition, condition_val
    )
    old_file_name = rows[0]["logo_url"]
    old_file_path = "%s/%s" % (CLIENT_LOGO_PATH, old_file_name)
    remove_uploaded_file(old_file_path)
    return save_client_logo(logo)


def update_client_group_record(db, client_group, session_user):
    current_time_stamp = get_date_time()
    contract_from = string_to_datetime(client_group.contract_from)
    contract_to = string_to_datetime(client_group.contract_to)
    is_sms_subscribed = 0 if client_group.is_sms_subscribed is False else 1
    columns = [
        "group_name", "contract_from", "contract_to", "no_of_user_licence",
        "total_disk_space", "is_sms_subscribed", "incharge_persons",
        "updated_by", "updated_on"
    ]
    values = [
        client_group.group_name, contract_from, contract_to,
        client_group.no_of_user_licence, client_group.file_space * (1024 * 1024 * 1024),
        is_sms_subscribed,
        ','.join(str(x) for x in client_group.incharge_persons), session_user,
        current_time_stamp
    ]
    if client_group.logo is not None:
        columns.append("logo_url")
        columns.append("logo_size")
        file_name = update_client_logo(
            db, client_group.logo, client_group.client_id
        )
        values.append(file_name)
        values.append(client_group.logo.file_size)

    condition = "client_id = %s"
    values.append(client_group.client_id)
    if db.update(tblClientGroups, columns, values, condition):
        action = "Updated Client \"%s\"" % client_group.group_name
        db.save_activity(session_user, 18, action)
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
    r = db.call_proc(
        "sp_client_groups_change_status",
        (client_id, is_active), ["group_name"]
    )
    if r is False:
        raise process_error("E049")
    else:
        group_name = r[0]["group_name"]
        if is_active == 1:
            action = "Activated Client \"%s\"" % group_name
        else:
            action = "Deactivated Client \"%s\"" % group_name
        db.save_activity(session_user, 18, action)

##########################################################################
##########################################################################


def is_duplicate_division(db, division_id, division_name, client_id):
    condition = "division_name = %s  AND client_id = %s "
    condition_val = [division_name, client_id]
    if division_id is not None:
        condition += " AND division_id != %s "
        condition_val.append(division_id)
    return db.is_already_exists(tblDivisions, condition, condition_val)


def save_division(
    db, client_id, division_name, business_group_id,
    legal_entity_id, session_user
):
    current_time_stamp = get_date_time()
    columns = [
        "client_id", "division_name",
        "legal_entity_id", "created_by", "created_on",
        "updated_by", "updated_on"
    ]
    values = [
        client_id, division_name, legal_entity_id,
        session_user, current_time_stamp, session_user,
        current_time_stamp
    ]

    if business_group_id is not None:
        columns.append("business_group_id")
        values.append(business_group_id)

    new_id = db.insert(tblDivisions, columns, values)
    if new_id is False:
        raise process_error("E054")
    else:
        action = "Created Division \"%s\"" % division_name
        db.save_activity(session_user, 19, action)

        return int(new_id)


def update_division(db, client_id, division_id, division_name, session_user):
    current_time_stamp = get_date_time()
    columns = ["division_name", "updated_by", "updated_on"]
    values = [division_name, session_user, current_time_stamp]
    condition = "division_id = %s and client_id = %s"
    values.extend([division_id, client_id])
    result = db.update(tblDivisions, columns, values, condition)
    if result:
        action = "Updated Division \"%s\"" % division_name
        db.save_activity(session_user, 19, action)
        return result
    else:
        raise process_error("E055")


def is_duplicate_unit_code(db, unit_id, unit_code, client_id):
    params =[unit_id, unit_code, None, client_id]
    rows = db.call_proc("sp_tbl_units_checkduplication", params)
    for d in rows:
        if(int(d["unit_code_cnt"]) > 0):
            return True
        else:
            return False


def is_duplicate_unit_name(db, unit_id, unit_name, client_id):
    params =[unit_id, None, unit_name, client_id]
    rows = db.call_proc("sp_tbl_units_checkduplication", params)
    for d in rows:
        if(int(d["unit_name_cnt"]) > 0):
            return True
        else:
            return False

def is_invalid_id(db, check_mode, val):
    print "inside valid checking"
    print check_mode

    if check_mode == "unit_id":
        params =[val,]
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

def save_unit (
    db, client_id,  units, business_group_id, legal_entity_id,
    country_id, division_id, category_name, session_user
):
    current_time_stamp = str(get_date_time())
    columns = [
        "client_id", "category_name", "geography_id", "unit_code", "unit_name",
        "address", "postal_code", "country_id", "is_active", "created_by", "created_on",
    ]
    if business_group_id is not None:
        columns.append("business_group_id")
    if legal_entity_id is not None:
        columns.append("legal_entity_id")
    if division_id is not None:
        columns.append("division_id")
    values_list = []
    unit_names = []
    for unit in units:
        domain_ids = ",".join(str(x) for x in unit.domain_ids)
        industry_ids = ",".join(str(x) for x in unit.industry_ids)
        vals = [
            client_id, category_name,
            unit.geography_id, unit.unit_code.upper(), unit.unit_name,
            unit.unit_address, unit.postal_code, country_id,
            1, session_user, current_time_stamp,
        ]
        if business_group_id is not None:
            vals.append(business_group_id)
        if legal_entity_id is not None:
            vals.append(legal_entity_id)
        if division_id is not None:
            vals.append(division_id)
        values_list.append(vals)
        unit_names.append("\"%s - %s\"" % (
            str(unit.unit_code).upper(), unit.unit_name)
        )

    result = db.bulk_insert(tblUnits, columns, values_list)
    if result is False:
        raise process_error("E056")

    action = "Created following Units %s" % (",".join(unit_names))
    db.save_activity(session_user, 19, action)

    max_unit_id = None
    rows = db.call_proc("sp_tbl_units_max_unitid",())
    for id in rows:
        if(int(id["max_id"]) > 0):
            max_unit_id = int(id["max_id"])
    columns = ["unit_id", "domain_id", "industry_id"]
    unit_id_start = len(units)
    print "unit length"
    print unit_id_start
    print max_unit_id
    values_list = []
    unit_id = None
    i = 1
    for unit in units:
        domain_ids = ",".join(str(x) for x in unit.domain_ids)
        industry_ids = ",".join(str(x) for x in unit.industry_ids)
        if unit_id_start == 1:
            unit_id = max_unit_id
        else :
            unit_id = (max_unit_id - unit_id_start) + i
            i = i +1
        print"unit_id"
        print unit_id
        vals = [unit_id, domain_ids, industry_ids]
        values_list.append(vals)

    result_1 = db.bulk_insert(tblUnitIndustries, columns, values_list)
    if result == True and result_1 == True:
        return True


def update_unit(db, client_id,  units, session_user):
    current_time_stamp = str(get_date_time())
    columns = [
        "country_id", "geography_id", "industry_id", "domain_ids",
        "unit_code", "unit_name", "address", "postal_code",
        "updated_by", "updated_on"
    ]
    for unit in units:
        domain_ids = ",".join(str(x) for x in unit.domain_ids)
        values = [
            unit.country_id, unit.geography_id, unit.industry_id, domain_ids,
            str(unit.unit_code), str(unit.unit_name), str(unit.unit_address),
            str(unit.postal_code), session_user, current_time_stamp
        ]
        condition = "client_id= %s and unit_id = %s"
        values.extend([client_id, unit.unit_id])
        res = db.update(tblUnits, columns, values, condition)
        if res:
            action = "Unit details updated for \"%s - %s\"" % (
                unit.unit_code, unit.unit_name
            )
            db.save_activity(session_user, 19, action)
        else:
            raise process_error("E057")

    return True


#
# get_clients
#
def get_user_clients(db, user_id):
    rows = db.call_proc("sp_tbl_unit_getuserclients", [int(user_id)])
    client_ids = [
        int(r["client_id"]) for r in rows
    ]
    return client_ids

def get_countries_for_unit(db, user_id):
    rows = db.call_proc("sp_countries_for_unit", (user_id,))

    fn = core.Country
    results = [
        fn(
           d["country_id"], d["country_name"], bool(d["is_active"])
        ) for d in rows
    ]
    return results


def get_business_groups_for_user(db, user_id):
    result = db.call_proc("sp_tbl_unit_getclientbusinessgroup", (user_id,))
    return return_business_groups(result)


def get_legal_entities_for_user(db, user_id):
    result = db.call_proc("sp_tbl_unit_getclientlegalentity",(user_id,))
    return return_legal_entities_for_unit(result)


def return_legal_entities_for_unit(legal_entities):
    results = []
    print "inside get lagal entity"
    print legal_entities

    for legal_entity in legal_entities:
        legal_entity_obj = core.UnitLegalEntity(
            legal_entity_id = legal_entity["legal_entity_id"],
            legal_entity_name = legal_entity["legal_entity_name"],
            business_group_id = legal_entity["business_group_id"],
            client_id = legal_entity["client_id"]
        )
        results.append(legal_entity_obj)
    return results


def get_divisions_for_user(db, user_id):
    result = db.call_proc("sp_tbl_unit_getclientdivision", (user_id,))
    return return_divisions(result)


def return_divisions(divisions):
    results = []
    for division in divisions:
        division_obj = core.Division(
            division["division_id"], division["division_name"],
            division["legal_entity_id"], division["business_group_id"],
            division["client_id"]
        )
        results.append(division_obj)
    return results


def get_client_industries(db, user_id,):
    columns = [
        "country_id", "country_name",
        "domain_id", "domain_name",
        "industry_id", "industry_name",
        "is_active"
    ]
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
        results.append(core.UnitIndustries(
            industry_id, industry_name, country_id,  domain_id, client_id, unit_count, legal_entity_id, is_active
        ))
    return results



def get_units_for_user(db, user_id):
    client_ids = None
    result = {}
    if user_id is not None:
        client_ids = get_user_clients(db, (user_id,))
    columns = [
        "unit_id", "unit_code", "unit_name",
        "address", "division_id",
        "legal_entity_id", "business_group_id",
        "client_id", "is_active", "geography_id",
        "industry_id", "domain_ids"
    ]
    condition, condition_val = db.generate_tuple_condition(
        "client_id", client_ids
    )
    order = " order by unit_name ASC "
    result = db.get_data(tblUnits, columns, condition, [condition_val], order)
    return return_units(result)


def return_units(units):
    results = []
    for unit in units:
        results.append(core.Unit(
            unit["unit_id"], unit["division_id"], unit["legal_entity_id"],
            unit["business_group_id"], unit["client_id"], unit["unit_code"],
            unit["unit_name"], unit["address"], bool(unit["is_active"])
        ))
    return results


def get_unit_details_for_user(db, user_id):
    where_condition_val = [user_id,]
    result = db.call_proc("sp_tbl_unit_getunitdetailsforuser", (where_condition_val,))
    return return_unit_details(result)


def return_unit_details(result):
    unitdetails = []

    for r in result:
        unitdetails.append(core.Unit(
                int(r["unit_id"]), int(r["client_id"]),
                int(r["business_group_id"]), int(r["legal_entity_id"]),
                int(r["country_id"]), int(r["division_id"]),
                r["category_name"], int(r["geography_id"]),
                r["unit_code"], r["unit_name"],
                r["address"], r["postal_code"],
                [int(x) for x in r["domain_ids"].split(",")],
                [int(y) for y in r["i_ids"].split(",")],
                bool(r["is_active"]),
                bool(r["approve_status"])
            ))
    return unitdetails

def get_group_companies_for_user_with_max_unit_count(db, user_id):
    print "inside max unit count"
    print user_id
    result = db.call_proc("sp_tbl_unit_getuserclients", (user_id,))
    return return_group_companies_with_max_unit_count(db, result)


def return_group_companies_with_max_unit_count(db, group_companies):
    results = []
    for group_company in group_companies:
        countries = get_client_countries(db, group_company["client_id"])
        domain_result = db.call_proc("sp_client_domains_by_group_id", (group_company["client_id"],))
        domain_ids = [int(r["domain_id"]) for r in domain_result]
        next_auto_gen_no = get_next_auto_gen_number(
            db, group_company["group_name"], group_company["client_id"]
        )
        results.append(core.GroupCompanyForUnitCreation(
            group_company["client_id"], group_company["group_name"],
            countries, domain_ids, next_auto_gen_no
        ))
    return results


def get_next_auto_gen_number(db, group_name=None, client_id=None):
    if group_name is None:
        condition_val = [client_id]
        rows = db.call_proc("sp_client_groups_details_by_id", (condition_val,))
        if rows:
            group_name = rows[0]["group_name"]

    condition_val = [client_id]
    rows = db.call_proc("sp_tbl_unit_getunitcount", (condition_val,))
    for r in rows:
        no_of_units = r["units"]
    group_name = group_name.replace(" ", "")
    unit_code_start_letters = group_name[:2].upper()

    unit_code_start_letters = "%s%s" % (unit_code_start_letters, "%")
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
    action_column = [
        "business_group_id", "legal_entity_id", "division_id",
        "country_id", "geography_id", "industry_id",
        "unit_code", "unit_name", "address",
        "postal_code", "domain_ids"
    ]
    condition = "unit_id = %s "
    condition_val = [unit_id]
    result = db.get_data(tblUnits, action_column, condition, condition_val)
    result = result[0]
    action = "Reactivated Unit \"%s-%s\"" % (
        result["unit_code"], result["unit_name"]
    )
    db.save_activity(session_user, 19, action)

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
    unit_columns = [
        "client_id", "is_active", "legal_entity_id",
        "country_id", "geography_id", "industry_id", "unit_code", "unit_name",
        "address", "postal_code", "domain_ids"
    ]
    values = [
        client_id, 1, result["legal_entity_id"],
        result["country_id"], result["geography_id"],
        result["industry_id"], unit_code, result["unit_name"],
        result["address"], result["postal_code"], result["domain_ids"]
    ]
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
                employee_name = "%s - %s" % (
                    row["employee_code"], row["employee_name"]
                )
            address = row["address"]
            is_service_provider = False
            if unit_name == "-":
                if (is_primary_admin == 1 or is_admin == 1):
                    is_service_provider = False
                else:
                    is_service_provider = True

            used_val = round((used_space/ONE_GB), 2)

            licence_holders.append(
                technomasters.LICENCE_HOLDER_DETAILS(
                    user_id, employee_name, email_id, contact_no,
                    unit_name, address,
                    file_space/ONE_GB, used_val,
                    bool(is_active), bool(is_primary_admin),
                    is_service_provider
                )
            )

        remaining_licence = (no_of_user_licence) - len(licence_holder_rows)
        total_free_space = round(file_space/ONE_GB, 2)
        total_used_space = round(used_space/ONE_GB, 2)
        profile_detail = technomasters.PROFILE_DETAIL(
            str(contract_from),
            str(contract_to), no_of_user_licence, remaining_licence,
            total_free_space, total_used_space, licence_holders
        )
        profiles.append(technomasters.PROFILES(client_id, profile_detail))
    return profiles


def get_settings(db, client_id):
    settings_columns = [
        "contract_from", "contract_to", "no_of_user_licence",
        "total_disk_space", "total_disk_space_used"
    ]
    condition = "client_id = %s"
    condition_val = [client_id]
    return db.get_data(
        tblClientGroups, settings_columns, condition, condition_val
    )


def get_licence_holder_details(db, client_id):
    columns = [
        "tcu.user_id", "tcu.email_id", "tcu.employee_name",
        "tcu.employee_code", "tcu.contact_no",
        "tcu.is_primary_admin", "tu.unit_code", "tu.unit_name",
        "tu.address", "tcu.is_active", "tcu.is_admin"
    ]
    tables = [tblClientUsers, tblUnits]
    aliases = ["tcu", "tu"]
    join_type = "left join"
    join_conditions = ["tcu.seating_unit_id = tu.unit_id"]
    where_condition = "tcu.client_id = %s"
    where_condition_val = [client_id]
    return db.get_data_from_multiple_tables(
        columns, tables, aliases, join_type, join_conditions,
        where_condition, where_condition_val
    )


def get_group_companies_for_user(db, user_id):
    result = {}
    client_ids = None
    if user_id is not None:
        client_ids = get_user_clients(db, user_id)
    columns = ["client_id", "group_name", "is_active"]
    condition, condition_val = db.generate_tuple_condition(
        "client_id", client_ids
    )
    condition += " AND is_active = 1"
    order = " order by group_name ASC "
    result = db.get_data(
        tblClientGroups, columns, condition, [condition_val], order
    )
    return return_group_companies(db, result)


def return_group_companies(db, group_companies):
    results = []
    for group_company in group_companies:
        countries = get_client_countries(db, group_company["client_id"])
        domains = get_client_domains(db, group_company["client_id"])
        results.append(
            core.GroupCompany(
                group_company["client_id"], group_company["group_name"],
                bool(group_company["is_active"]), countries, domains
            )
        )
    return results


def create_new_admin(
    db, new_admin_id, old_admin_id, old_admin_name,
    client_id, session_user
):
    t_obj = ClientAdmin(db, new_admin_id, old_admin_id, client_id)
    result = t_obj.perform_promote_admin()
    if result is True:
        # Promoting to new admin in Knowledge db
        query = "update tbl_client_users set is_primary_admin = 1 " + \
            " where user_id = %s and client_id = %s"
        db.execute(query, [new_admin_id, client_id])

        # Deactivating old admin in Knowledge db
        query = "update tbl_client_users set is_active = 0 " + \
            " where user_id = %s and client_id = %s"
        db.execute(query, [old_admin_id, client_id])

        query = "update tbl_client_groups t1, " + \
            " (select email_id from tbl_client_users where user_id = %s " + \
            " and client_id = %s) t2 " + \
            " set t1.email_id = t2.email_id  where client_id = %s"
        db.execute(query, [
            old_admin_id, client_id, client_id
        ])
        action = None
        action = "User \"%s\" is promoted as Client Admin" % (old_admin_name)
        db.save_activity(session_user, 20, action)
        return True
    return result


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
        result = db.get_data(
            tblCountries, columns, condition, condition_val, order
        )
        if result:
            return return_countries(result)
    else:
        return get_user_countries(db, session_user)


##########################################################################
#  To get list of legal entities
#  Parameters : Object of database
#  Return Type : Returns List of object of LegalEntities
##########################################################################
def get_assign_legalentities(db):
    legalentities = db.call_proc(
        "sp_assign_legal_entities_list", None
    )
    return return_assign_legalentities(legalentities)

##########################################################################
#  To get list of groups
#  Parameters : Object of database
#  Return Type : Returns List of object of LegalEntities
##########################################################################
def return_assign_legalentities(assign_legalentities_list):
    fn = core.AssignLegalEntity
    assign_legalentities_list = [
        fn(
            legalentity["client_id"], legalentity["group_name"],
            legalentity["country_names"], legalentity["no_of_legal_entities"]
            
        ) for legalentity in assign_legalentities_list
    ]
    return assign_legalentities_list
