########################################################
# This Controller will handle Client and Client Unit
# related requests
#
# In this module "db" is an object of "KnowledgeDatabase"
########################################################
import threading
import re
from protocol import technomasters
from server.emailcontroller import EmailHandler as email
from server import logger

from server.database.admin import (
    get_domains_for_user,
    get_countries_for_user
)
from server.database.createclientdatabase import ClientDBCreate

from server.database.technomaster import  *

__all__ = [
    "get_client_groups",
    "save_client_group",
    "update_client_group",
    "change_client_group_status",
    "save_client",
    "update_client",
    "get_clients",
    "change_client_status",
    "reactivate_unit",
    "get_client_profile",
    "create_new_admin"
]

#
# Client Group Master
#

########################################################
# To Get list of all clients with details
########################################################
def get_client_groups(db, request, session_user):
    domain_list = get_domains_for_user(db, session_user)
    country_list = get_countries_for_user(db, session_user)
    user_client_countries = get_user_client_countries(db, session_user)
    user_client_domains = get_user_client_domains(db, session_user)
    users = get_techno_users(db)
    client_list = get_group_company_details(db)
    return technomasters.GetClientGroupsSuccess(
        countries=country_list,
        domains=domain_list, users=users, client_list=client_list,
        client_countries=user_client_countries,
        client_domains=user_client_domains
    )

########################################################
# To Create the database of the client
########################################################
# def create_database(
#     host, username, password, database_name, db_username,
#     db_password, email_id, client_id, short_name, db,
#     country_ids, domain_ids
# ):
#     try:
#         password = db._create_database(
#             host, username, password, database_name, db_username,
#             db_password, email_id, client_id, short_name, country_ids,
#             domain_ids
#         )
#         print "database created"
#         return True, password
#     except Exception, ex:
#         print "Error :{}".format(ex)
#         logger.logKnowledge("error", "technomastercontroller.py-create_database", ex)
#         return False, None


########################################################
# To send the credentials of the created client to
# the same
########################################################
def send_client_credentials(
    short_name, email_id, password
):
    try:
        email().send_client_credentials(short_name, email_id, password)
    except Exception, e:
        print "Error while sending email : {}".format(e)
        logger.logKnowledge("error", "technomastercontroller.py-send_client_credentials", e)
    return True

########################################################
# To Check whether uploaded logo is in image formats
########################################################
# def is_logo_in_image_format(logo):
#     name = logo.file_name.split('.')[0]
#     exten = logo.file_name.split('.')[1]
#     if exten in ["png", "jpg", "jpeg",]:
#         return True
#     else:
#         return False

########################################################
# To Validate and Save Client Group
########################################################
# def save_client_group(db, request, session_user):
#     session_user = int(session_user)
#     client_id = db.generate_new_client_id()
#     if db.is_duplicate_group_name(request.group_name, client_id):
#         return technomasters.GroupNameAlreadyExists()
#     elif db.is_duplicate_short_name(request.short_name, client_id):
#         return technomasters.ShortNameAlreadyExists()
#     elif not is_logo_in_image_format(request.logo):
#         return technomasters.NotAnImageFile()
#     else:
#         country_ids = ",".join(str(x) for x in request.country_ids)
#         domain_ids = ",".join(str(x) for x in request.domain_ids)
#         short_name = re.sub('[^a-zA-Z0-9 \n\.]', '', request.short_name)
#         short_name = short_name.replace(" ", "")
#         create_db = ClientDBCreate(
#             db, client_id, short_name, email_id,
#             country_ids, domain_ids
#         )
#         database_name = "compfie_%s_%d" % (short_name.lower(), client_id)
#         row = db._get_server_details()
#         if len(row) <= 0:
#             return technomasters.ServerIsFull()
#         host = row[0][0]
#         username = row[0][1]
#         password = row[0][2]
#         db_username = db.generate_random()
#         db_password = db.generate_random()
#         db_port = row[0][3]
#         country_ids = ",".join(str(x) for x in request.country_ids)
#         domain_ids = ",".join(str(x) for x in request.domain_ids)
#         try:
#             create_database_thread = None

#             def enthread():
#                 q = Queue.Queue()

#                 def wrapper():
#                     q.put(
#                         create_database(
#                             host, username, password, database_name, db_username,
#                             db_password, request.email_id, client_id, request.short_name, db,
#                             country_ids, domain_ids
#                         )
#                     )
#                     print "database create thread"
#                 create_database_thread = threading.Thread(
#                     target=wrapper
#                 )
#                 create_database_thread.start()
#                 return q
#             result_q = enthread()
#             result = result_q.get()

#             db.save_client_group(client_id, request, session_user)
#             print "client group saved"
#             db.save_date_configurations(
#                 client_id, request.date_configurations,
#                 session_user
#             )
#             print "client date_configurations"
#             db.save_client_countries(client_id, request.country_ids)
#             db.save_client_domains(client_id, request.domain_ids)
#             db.save_incharge_persons(request, client_id)
#             db.save_client_user(request, session_user, client_id)
#             db.update_client_db_details(
#                 host, client_id, db_username,
#                 db_password, request.short_name, database_name, db_port
#             )
#             db.notify_incharge_persons(request)
#             # while create_database_thread.isAlive():
#             #     continue
#             if result[0] :
#                 send_client_credentials_thread = threading.Thread(
#                     target=send_client_credentials, args=[
#                         request.short_name, request.email_id, result[1]
#                     ]
#                 )
#                 send_client_credentials_thread.start()
#                 return technomasters.SaveClientGroupSuccess()
#             else:
#                 logger.logKnowledge("error", "technomastercontroller.py-save_client_group", "error in creating database")
#                 raise Exception('Error in Creating database')
#         except Exception, e:
#             logger.logKnowledge("error", "technomastercontroller.py-save_client_group", e)

#             print "Error in save client group: {}".format(e)
#             try:
#                 db.delete_database(host, database_name, username, password)
#             except Exception, ex:
#                 print "Error in deleting database : {}".format(ex)
#                 logger.logKnowledge("error", "technomastercontroller.py-save_client_group", ex)
#             return technomasters.ClientCreationFailed(error="Failed to create client")

def save_client_group(db, request, session_user):
    session_user = int(session_user)
    client_id = generate_new_client_id(db)
    if db.is_duplicate_group_name(request.group_name, client_id):
        return technomasters.GroupNameAlreadyExists()
    elif db.is_duplicate_short_name(request.short_name, client_id):
        return technomasters.ShortNameAlreadyExists()
    elif not is_logo_in_image_format(request.logo):
        return technomasters.NotAnImageFile()
    else:
        country_ids = ",".join(str(x) for x in request.country_ids)
        domain_ids = ",".join(str(x) for x in request.domain_ids)
        short_name = re.sub('[^a-zA-Z0-9 \n\.]', '', request.short_name)
        short_name = short_name.replace(" ", "")
        create_db = ClientDBCreate(
            db, client_id, short_name, request.email_id,
            country_ids, domain_ids
        )
        try:
            is_db_created = create_db.begin_process()
            save_client_countries(db, client_id, request.country_ids)
            save_client_domains(db, client_id, request.domain_ids)
            save_incharge_persons(db, request, client_id)
            save_client_user(db, request, session_user, client_id)
            create_db.update_client_db_details()
            notify_incharge_persons(db, request)
            if is_db_created :
                send_client_credentials_thread = threading.Thread(
                    target=send_client_credentials, args=[
                        request.short_name, request.email_id, result[1]
                    ]
                )
                send_client_credentials_thread.start()
                return technomasters.SaveClientGroupSuccess()
            else :
                raise Exception("Error in creating database")
        except Exception:
            create_db.delete_database()


########################################################
# To Validate and Update Client Group
########################################################
def update_client_group(db, request, session_user):
    session_user = int(session_user)
    if db.is_invalid_id(db.tblClientGroups, "client_id", request.client_id) :
        return technomasters.InvalidClientId()
    elif is_duplicate_group_name(db, request.group_name, request.client_id):
        return technomasters.GroupNameAlreadyExists()
    elif is_deactivated_existing_country(db, request.client_id, request.country_ids):
        return technomasters.CannotDeactivateCountry()
    elif is_deactivated_existing_domain(db, request.client_id, request.domain_ids):
        return technomasters.CannotDeactivateDomain()
    elif validate_no_of_user_licence(db, request.no_of_user_licence, request.client_id):
        return technomasters.InvalidNoOfLicence()
    elif validate_total_disk_space(
        db, request.file_space * 1000000000, request.client_id
    ):
        return technomasters.InvalidFileSpace()
    else:
        update_client_group_record(db, request, session_user)
        save_client_countries(db, request.client_id, request.country_ids)
        save_client_domains(db, request.client_id, request.domain_ids)
        save_incharge_persons(db, request, request.client_id)
        replicate_client_countries_and_domains(
            db, request.client_id, request.country_ids, request.domain_ids
        )
        save_date_configurations(
            db, request.client_id, request.date_configurations,
            session_user
        )
        return technomasters.UpdateClientSuccess()

########################################################
# To Validate and Change the Client status
########################################################
def change_client_group_status(db, request, session_user):
    session_user = int(session_user)
    client_id = request.client_id
    is_active = request.is_active
    if db.is_invalid_id(tblClientGroups, "client_id", client_id) :
        return technomasters.InvalidClientId()
    elif is_unit_exists_under_client(db, client_id):
        return technomasters.CannotDeactivateClient()
    else:
        update_client_group_status(db, client_id, is_active, session_user)
        return technomasters.ChangeClientStatusSuccess()

#
# Client Unit Creation
#

########################################################
# To Validate and Save Business group, Legal Entity,
# Division and Units received in the request
########################################################
def validate_duplicate_data(db, request, session_user):
    session_user = int(session_user)
    client_id = request.client_id
    business_group = request.business_group
    legal_entity = request.legal_entity
    division = request.division
    country_wise_units = request.country_wise_units

    if db.is_invalid_id(tblClientGroups, "client_id", client_id) :
        return technomasters.InvalidClientId()

    if business_group is not None :
        b_group_id = business_group.business_group_id
        b_group_name = business_group.business_group_name
        if db.is_duplicate_business_group(b_group_id, b_group_name, client_id) :
            return technomasters.BusinessGroupNameAlreadyExists()
        if b_group_id is not None :
            if db.is_invalid_id(tblBusinessGroups, "business_group_id", b_group_id) :
                return technomasters.InvalidBusinessGroupId()

    if division is not None :
        div_id = division.division_id
        div_name = division.division_name
        if db.is_duplicate_division(div_id, div_name, client_id) :
            return technomasters.DivisionNameAlreadyExists()
        if div_id is not None :
            if db.is_invalid_id(tblDivisions, "division_id", div_id) :
                return technomasters.InvalidDivisionId()

    leg_id = legal_entity.legal_entity_id
    leg_name = legal_entity.legal_entity_name
    if db.is_duplicate_legal_entity(leg_id, leg_name, client_id) :
        return technomasters.LegalEntityNameAlreadyExists()
    if leg_id is not None :
        if db.is_invalid_id(tblLegalEntities, "legal_entity_id", leg_id) :
            return technomasters.InvalidLegalEntityId()

    new_unit_list = []
    old_unit_list = []
    for country in country_wise_units :
        units = country.units
        for unit in units :
            unit_id = unit.unit_id
            unit_name = unit.unit_name
            if db.is_duplicate_unit_code(unit_id, unit.unit_code, client_id) :
                return technomasters.UnitCodeAlreadyExists(
                    db.get_next_auto_gen_number(client_id)
                )

            elif db.is_duplicate_unit_name(unit_id, unit_name, client_id):
                return technomasters.UnitNameAlreadyExists()
            else :
                pass

            if unit_id is not None :
                if db.is_invalid_id(tblUnits, "unit_id", unit_id) :
                    return technomasters.InvalidUnitId()
                old_unit_list.append(unit)
            else :
                new_unit_list.append(unit)

    return [True, new_unit_list, old_unit_list]

def save_client(db, request, session_user):
    client_id = request.client_id
    business_group = request.business_group
    legal_entity = request.legal_entity
    division = request.division
    is_valid = validate_duplicate_data(db, request, session_user)
    if type(is_valid) is not list :
        return is_valid
    else :
        if is_valid[0] is True :
            units = is_valid[1]

        b_group_id = None
        leg_id = None
        div_id = None
        if business_group is not None :
            b_group_name = business_group.business_group_name
            b_group_id = db.save_business_group(
                db, client_id, b_group_name, session_user
            )
            if b_group_id is False :
                return False

        if legal_entity is not None :
            leg_name = legal_entity.legal_entity_name
            leg_id = db.save_legal_entity(
                db, client_id, leg_name, b_group_name, session_user
            )
            if leg_id is False :
                return False

        if division is not None :
            div_name = division.division_name
            div_id = db.save_division(
                db, client_id, div_name, b_group_id, leg_id, session_user
            )
            if div_id is False :
                return False

        res = db.save_unit(
            client_id, units, b_group_id, leg_id, div_id, session_user
        )
        if res :
            return technomasters.SaveClientSuccess()

# def save_client(db, request, session_user):
#     session_user = int(session_user)
#     client_id = request.client_id
#     business_group = request.business_group
#     legal_entity = request.legal_entity
#     division = request.division
#     country_wise_units = request.country_wise_units
#     business_group_id = None
#     business_group_name = None
#     division_id = None
#     division_name = None
#     optional_business_group = False
#     optional_division = False
#     result1 = False
#     result2 = False
#     result3 = False
#     result4 = False
#     existing_business_group = False
#     existing_entity = False
#     existing_division = False

#     if db.is_invalid_id(db.tblClientGroups, "client_id", client_id) :
#         return technomasters.InvalidClientId()

#     if business_group is None:
#         optional_business_group = True
#         result1 = True
#     else:
#         business_group_id = business_group.business_group_id
#         business_group_name = business_group.business_group_name
#         if business_group_id is None:
#             business_group_id = db.generate_new_business_group_id()
#         else:
#             existing_business_group = True
#         if db.is_duplicate_business_group(business_group_id, business_group_name, client_id):
#             return technomasters.BusinessGroupNameAlreadyExists()

#     legal_entity_id = legal_entity.legal_entity_id
#     legal_entity_name = legal_entity.legal_entity_name
#     if legal_entity_id is None:
#         legal_entity_id = db.generate_new_legal_entity_id()
#     else:
#         existing_entity = True
#     if db.is_duplicate_legal_entity(legal_entity_id, legal_entity_name, client_id):
#         return technomasters.LegalEntityNameAlreadyExists()

#     if division is None:
#         optional_division = True
#         result3 = True
#     else:
#         division_id = division.division_id
#         division_name = division.division_name
#         if division_id is None:
#             division_id = db.generate_new_division_id()
#         else:
#             existing_division = True
#         if db.is_duplicate_division(division_id, division_name, client_id):
#             return technomasters.DivisionNameAlreadyExists()

#     units_list = []
#     unit_id = None
#     for country in country_wise_units:
#         country_id = country.country_id
#         units = country.units
#         for unit in units:
#             unit_id = unit.unit_id
#             # unit_id = (unit_id+1) if unit_id != None else db.generate_new_unit_id()
#             # domain_ids = ",".join(str(x) for x in unit.domain_ids)
#             if db.is_duplicate_unit_code(unit_id, unit.unit_code, client_id):
#                 next_unit_code = db.get_next_auto_gen_number(client_id=client_id)
#                 return technomasters.UnitCodeAlreadyExists(
#                     next_unit_code=next_unit_code
#                 )
#             else:
#                 # unit.unit_id = 0
#                 unit.country_id = country_id
#                 units_list.append(unit)
#     if not optional_business_group:
#         if not existing_business_group:
#             result1 = db.save_business_group(client_id, business_group_id, business_group_name, session_user)
#         else:
#             result1 = True
#     if not existing_entity:
#         result2 = db.save_legal_entity(client_id, legal_entity_id, legal_entity_name, business_group_id, session_user)
#     else:
#         result2 = True
#     if not optional_division:
#         if not existing_division:
#             result3 = db.save_division(client_id, division_id, division_name, business_group_id, legal_entity_id, session_user)
#         else:
#             result3 = True
#     result4 = db.save_unit(client_id, units_list, business_group_id, legal_entity_id, division_id, session_user)
#     if result1 and result2 and result3 and result4:
#         return technomasters.SaveClientSuccess()

########################################################
# To Validate and Update Business group, Legal Entity,
# Division and Units received in the request
########################################################
def update_client(db, request, session_user):
    session_user = int(session_user)
    client_id = request.client_id
    business_group = request.business_group
    legal_entity = request.legal_entity
    division = request.division
    is_valid = validate_duplicate_data(db, request, session_user)
    if type(is_valid) is not list :
        return is_valid
    else :
        if is_valid[0] is True :
            new_units = is_valid[1]
            old_units = is_valid[2]
            b_group_id = None
            leg_id = None
            div_id = None

            if business_group is not None :
                b_group_name = business_group.business_group_name
                b_group_id = business_group.business_group_id
                db.update_business_group(client_id, b_group_id, b_group_name, session_user)

            if legal_entity is not None :
                leg_id = legal_entity.legal_entity_id
                leg_name = legal_entity.legal_entity_name
                db.update_legal_entity(client_id, leg_id, leg_name, session_user)

            if division is not None :
                div_name = division.division_name
                div_id = division.division_id
                db.update_division(client_id, div_id, div_name, session_user)

            if len(new_units) > 0 :
                is_new_saved = db.save_unit(
                    client_id, new_units, b_group_id, leg_id, div_id, session_user
                )
                if is_new_saved is False:
                    return False

            if len(old_units) > 0 :
                is_old_saved = db.update_unit(
                    client_id, old_units, session_user
                )
                if is_old_saved is False :
                    return False
        return technomasters.UpdateClientSuccess()

########################################################
# To Get List of Business groups, Legal Entities,
# Divisions and Units with details of all clients
########################################################
def get_clients(db, request, session_user):
    group_company_list = db.get_group_companies_for_user_with_max_unit_count(session_user)
    if len(group_company_list) > 0:
        country_list = get_countries_for_user(db, session_user)
        domain_list = get_domains_for_user(db, session_user)
        business_group_list = db.get_business_groups_for_user(session_user)
        legal_entity_list = db.get_legal_entities_for_user(session_user)
        division_list = db.get_divisions_for_user(session_user)
        unit_list = db.get_unit_details_for_user(session_user)
        geography_levels = db.get_geograhpy_levels_for_user(session_user)
        geographies = db.get_geographies_for_user_with_mapping(session_user)
        industries = db.get_active_industries()
        client_domains = db.get_user_client_domains(session_user)
        return technomasters.GetClientsSuccess(countries=country_list,
            domains=domain_list, group_companies=group_company_list,
            business_groups=business_group_list, legal_entities=legal_entity_list,
            divisions=division_list, units=unit_list, geography_levels=geography_levels,
            geographies=geographies, industries=industries, client_domains=client_domains
        )
    else:
        return technomasters.UserIsNotResponsibleForAnyClient()

########################################################
# To Change the status of Units under a particular
# division or Legal entity
########################################################
def change_client_status(db, request, session_user):
    session_user = int(session_user)

    client_id = request.client_id
    legal_entity_id = request.legal_entity_id
    is_active = request.is_active
    division_id = request.division_id

    is_active = 1 if is_active == True else 0

    if db.is_invalid_id(db.tblClientGroups, "client_id", client_id):
        return technomasters.InvalidClientId()
    elif db.is_invalid_id(db.tblLegalEntities, "legal_entity_id", legal_entity_id):
        return technomasters.InvalidLegalEntityId()
    elif division_id != None:
        if db.is_invalid_id(db.tblDivisions, "division_id", division_id):
            return technomasters.InvalidDivisionId()
        elif db.change_client_status(client_id, legal_entity_id, division_id,
            is_active, session_user):
            return technomasters.ChangeClientStatusSuccess()
    elif db.change_client_status(client_id, legal_entity_id, division_id,
        is_active, session_user):
        return technomasters.ChangeClientStatusSuccess()

########################################################
# To Reactivate a closed Unit
########################################################
def reactivate_unit(db, request, session_user):
    session_user = int(session_user)
    client_id = request.client_id
    unit_id = request.unit_id
    password = request.password
    if db.is_invalid_id(db.tblClientGroups, "client_id", client_id):
        return technomasters.InvalidClientId()
    elif db.is_invalid_id(db.tblUnits, "unit_id", unit_id):
        return technomasters.InvalidUnitId()
    else:
        if db.verify_password(password, session_user):
            unit_code, unit_name = db.reactivate_unit(client_id, unit_id, session_user)
            return technomasters.ReactivateUnitSuccess(
                unit_code=unit_code, unit_name=unit_name
            )
        else:
            return technomasters.InvalidPassword()

########################################################
# To Get the Profile of all clients
########################################################
def get_client_profile(db, request, session_user):
    client_ids = db.get_user_clients(session_user)
    if client_ids ==  None:
        return technomasters.UserIsNotResponsibleForAnyClient()
    else:
        profiles = db.get_profiles(client_ids)
        group_companies = db.get_group_companies_for_user(session_user)
        return technomasters.GetClientProfileSuccess(
            group_companies = group_companies,
            profiles = profiles)

########################################################
# To promote a user as Primary admin
########################################################
def create_new_admin(db, request, session_user):
    new_admin_id = request.new_admin_id
    client_id = request.client_id
    result = db.create_new_admin(new_admin_id, client_id, session_user)
    if result == "ClientDatabaseNotExists":
        return technomasters.ClientDatabaseNotExists()
    elif result == "Reassign":
        return technomasters.ReassignFirst()
    else:
        return technomasters.CreateNewAdminSuccess()

def get_next_unit_code(db, request, session_user):
    client_id = request.client_id
    next_unit_code = db.get_next_auto_gen_number(client_id=client_id)
    return technomasters.GetNextUnitCodeSuccess(next_unit_code)
