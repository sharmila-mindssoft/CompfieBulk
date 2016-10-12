########################################################
# This Controller will handle Client and Client Unit
# related requests
#
# In this module "db" is an object of "KnowledgeDatabase"
########################################################
from protocol import technomasters

from server.database.admin import (
    get_domains_for_user
)
from server.database.login import verify_password
from server.database.knowledgemaster import (
    get_geograhpy_levels_for_user,
    get_geographies_for_user_with_mapping,
)

from server.database.technomaster import *

__all__ = [
    "get_client_groups",
    "get_client_group_form_data",
    "process_save_client_group",
    "get_edit_client_group_form_data"
    "process_update_client_group",
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
    groups = get_groups(db)
    return technomasters.GetClientGroupsSuccess(
        groups=groups
    )


########################################################
# To Get data to populate client group form
########################################################
def get_client_group_form_data(db, request, session_user):
    countries = get_user_countries(db, session_user)
    users = get_techno_users(db)
    domains = get_user_domains(db, session_user)
    industries = get_active_industries(db)
    return technomasters.GetClientGroupFormDataSuccess(
        countries=countries, users=users, domains=domains,
        industries=industries
    )


########################################################
# To Save Client
########################################################
def process_save_client_group(db, request, session_user):
    session_user = int(session_user)
    if is_duplicate_group_name(db, request.group_name):
        return technomasters.GroupNameAlreadyExists()
    else:
        group_id = save_client_group(
            db, request.group_name, request.user_name
        )
        legal_entity_names = save_legal_entities(
            db, request, group_id, session_user)
        country_ids = save_date_configurations(
            db, group_id, request.date_configurations, session_user
        )
        legal_entity_id_name_map = get_legal_entity_ids_by_name(
            db, legal_entity_names
        )
        save_client_user(db, group_id, request.user_name)
        save_client_countries(db, group_id, country_ids)
        save_client_domains(db, group_id, request, legal_entity_id_name_map)
        save_incharge_persons(db, group_id, request, legal_entity_id_name_map)
        save_organization(
            db, group_id, request, legal_entity_id_name_map, session_user
        )
        return technomasters.SaveClientGroupSuccess()


########################################################
# To Get data to populate client group form
########################################################
def get_edit_client_group_form_data(db, request, session_user):
    countries = get_user_countries(db, session_user)
    business_groups = get_client_business_groups(db, request.group_id)
    users = get_techno_users(db)
    domains = get_user_domains(db, session_user)
    industries = get_active_industries(db)
    group_id = request.group_id
    (
        group_name, user_name, legal_entities, date_configuration_list
    ) = get_client_details(db, group_id)
    return technomasters.GetEditClientGroupFormDataSuccess(
        countries=countries, users=users, domains=domains,
        business_groups=business_groups,
        industries=industries, group_name=group_name,
        user_name=user_name, legal_entities=legal_entities,
        date_configurations=date_configuration_list
    )


########################################################
# To Validate and Update Client Group
########################################################
def process_update_client_group(db, request, session_user):
    session_user = int(session_user)
    if is_invalid_group_id(db, request.group_id):
        return technomasters.InvalidClientId()
    elif is_duplicate_group_name(db, request.group_name, request.group_id):
        return technomasters.GroupNameAlreadyExists()
    country_ids = save_date_configurations(
        db, request.group_id, request.date_configurations, session_user
    )
    if is_deactivated_existing_country(
        db, request.group_id, country_ids
    ):
        return technomasters.CannotDeactivateCountry()
    else:
        update_client_group(
            db, request.group_name, request.group_id
        )
        legal_entity_names = update_legal_entities(
            db, request, request.group_id, session_user)
        legal_entity_id_name_map = get_legal_entity_ids_by_name(
            db, legal_entity_names
        )
        save_client_countries(db, request.group_id, country_ids)
        save_client_domains(
            db, request.group_id, request, legal_entity_id_name_map)
        save_incharge_persons(
            db, request.group_id, request, legal_entity_id_name_map)
        save_organization(
            db, request.group_id, request,
            legal_entity_id_name_map, session_user
        )
        return technomasters.UpdateClientGroupSuccess()


########################################################
# To Validate and Change the Client status
########################################################
def change_client_group_status(db, request, session_user):
    session_user = int(session_user)
    client_id = request.client_id
    is_active = request.is_active
    if is_invalid_group_id(db, client_id):
        return technomasters.InvalidClientId()
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
    business_group_id = request.business_group_id
    legal_entity_id = request.legal_entity_id
    division_id = request.division_id

    #country_wise_units = request.country_wise_units

    if not is_invalid_id(db, "client_id", client_id):
        return technomasters.InvalidClientId()

    if business_group_id is not None:
        #b_group_id = business_group.business_group_id
        #b_group_name = business_group.business_group_name
        #if is_duplicate_business_group(
         #   db, b_group_id, b_group_name, client_id
        #):
         #   return technomasters.BusinessGroupNameAlreadyExists()
        #if b_group_id is not None:
        if not is_invalid_id(db, "bg_id", business_group_id):
            return technomasters.InvalidBusinessGroupId()

    if division_id is not None:
        #div_id = division.division_id
        #div_name = division.division_name
        #if is_duplicate_division(db, div_id, div_name, client_id):
         #   return technomasters.DivisionNameAlreadyExists()
        #if div_id is not None:
        if not is_invalid_id(db, "division_id", division_id):
            return technomasters.InvalidDivisionId()

    #leg_id = legal_entity.legal_entity_id
    #leg_name = legal_entity.legal_entity_name
    #if is_duplicate_legal_entity(db, leg_id, leg_name, client_id):
    #    return technomasters.LegalEntityNameAlreadyExists()
    if legal_entity_id is not None:
        if not is_invalid_id(db, "legal_entity_id", legal_entity_id):
            return technomasters.InvalidLegalEntityId()

    units = request.units
    new_unit_list = []
    old_unit_list = []

    for unit in units:
        unit_id = unit.unit_id
        unit_name = unit.unit_name
        if is_duplicate_unit_code(db, unit_id, unit.unit_code, client_id):
            return technomasters.UnitCodeAlreadyExists(
                get_next_auto_gen_number(db, client_id)
            )

        elif is_duplicate_unit_name(db, unit_id, unit_name, client_id):
            return technomasters.UnitNameAlreadyExists()
        else:
            pass

        if unit_id is not None:
            if not is_invalid_id(db, "unit_id", unit_id):
                return technomasters.InvalidUnitId()
            old_unit_list.append(unit)
        else:
            new_unit_list.append(unit)

    return [True, new_unit_list, old_unit_list]


def save_client(db, request, session_user):
    client_id = request.client_id

    business_group_id = request.business_group_id
    legal_entity_id = request.legal_entity_id
    country_id = request.country_id
    division_id = request.division_id
    category_name = request.category_name
    is_valid = validate_duplicate_data(db, request, session_user)
    if type(is_valid) is not list:
        return is_valid
    else:
        if is_valid[0] is True:
            units = is_valid[1]

        b_group_id = None
        leg_id = None
        div_id = None
        if business_group is not None:
            b_group_name = business_group.business_group_name
            b_group_id = business_group.business_group_id
            if b_group_id is None:
                b_group_id = save_business_group(
                    db, client_id, b_group_name, session_user
                )
            if b_group_id is False:
                return False

        if legal_entity is not None:
            leg_name = legal_entity.legal_entity_name
            leg_id = legal_entity.legal_entity_id
            if leg_id is None:
                leg_id = save_legal_entity(
                    db, client_id, leg_name, b_group_id, session_user
                )
            if leg_id is False:
                return False

        if division is not None:
            div_name = division.division_name
            div_id = division.division_id
            if div_id is None:
                div_id = save_division(
                    db, client_id, div_name, b_group_id, leg_id, session_user
                )
            if div_id is False:
                return False
        #b_group_id = None
        #leg_id = None
        #div_id = None
        #if business_group is not None:
         #   print "inside business group is not None"
          #  b_group_name = business_group.business_group_name
           # b_group_id = business_group.business_group_id
            #if b_group_id is None:
             #   print "inside business group id is None"
              #  b_group_id = save_business_group(
               #     db, client_id, b_group_name, session_user
                #)
                #print "b_group_id : %s" % b_group_id
            #if b_group_id is False:
             #   return False

        #if legal_entity is not None:
         #   print "inside legal entity is not None"
          #  leg_name = legal_entity.legal_entity_name
           # leg_id = legal_entity.legal_entity_id
            #print "leg_id : %s " % leg_id
           # if leg_id is None:
            #    print "inside legal entity id is none"
             #   leg_id = save_legal_entity(
              #      db, client_id, leg_name, b_group_id, session_user
               # )
            #if leg_id is False:
             #   return False

        #if division is not None:
           # print "inside division is not None"
            #div_name = division.division_name
            #div_id = division.division_id
            #print "div_id : %s " % div_id
            #if div_id is None:
             #   print "inside div id is None"
              #  div_id = save_division(
               #     db, client_id, div_name, b_group_id, leg_id, session_user
                #)
            #if div_id is False:
             #   return False

        res = save_unit(
            db, client_id, units, business_group_id, legal_entity_id, country_id, division_id, category_name, session_user
        )
        if res:
            return technomasters.SaveClientSuccess()


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
    if type(is_valid) is not list:
        return is_valid
    else:
        if is_valid[0] is True:
            new_units = is_valid[1]
            old_units = is_valid[2]
            b_group_id = None
            leg_id = None
            div_id = None

            if business_group is not None:
                b_group_name = business_group.business_group_name
                b_group_id = business_group.business_group_id
                update_business_group(
                    db, client_id, b_group_id, b_group_name, session_user
                )

            if legal_entity is not None:
                leg_id = legal_entity.legal_entity_id
                leg_name = legal_entity.legal_entity_name
                update_legal_entity(
                    db, client_id, leg_id, leg_name, session_user
                )

            if division is not None:
                div_name = division.division_name
                div_id = division.division_id
                update_division(db, client_id, div_id, div_name, session_user)

            if len(new_units) > 0:
                is_new_saved = save_unit(
                    db, client_id, new_units, b_group_id,
                    leg_id, div_id, session_user
                )
                if is_new_saved is False:
                    return False

            if len(old_units) > 0:
                is_old_saved = update_unit(
                    db, client_id, old_units, session_user
                )
                if is_old_saved is False:
                    return False
        return technomasters.UpdateClientSuccess()


########################################################
# To Get List of Business groups, Legal Entities,
# Divisions and Units with details of all clients
########################################################
def get_clients(db, request, session_user):
    group_company_list = get_group_companies_for_user_with_max_unit_count(
        db, session_user
    )
    if len(group_company_list) > 0:
        country_list = get_countries_for_unit(db, session_user)
        domain_list = get_domains_for_user(db, session_user)
        business_group_list = get_business_groups_for_user(db, session_user)
        legal_entity_list = get_legal_entities_for_user(db, session_user)
        division_list = get_divisions_for_user(db, session_user)
        unit_list = get_unit_details_for_user(db, session_user)
        unit_geography_level_list = get_geograhpy_levels_for_user(db, session_user)
        unit_geographies_list = get_geographies_for_user_with_mapping(db, session_user)
        unit_industries_list = get_client_industries(db, session_user)
        client_domains = get_user_client_domains(db, session_user)
        return technomasters.GetClientsSuccess(
            countries=country_list,
            domains=domain_list,
            group_company_list=group_company_list,
            business_group_list=business_group_list,
            unit_legal_entity=legal_entity_list,
            divisions=division_list,
            unit_list=unit_list,
            unit_geography_level_list=unit_geography_level_list,
            unit_geographies_list=unit_geographies_list,
            unit_industries_list=unit_industries_list,
            client_domains=client_domains
        )
    else:
        return technomasters.UserIsNotResponsibleForAnyClient()


########################################################
# To Reactivate a closed Unit
########################################################
def reactivate_unit(db, request, session_user):
    session_user = int(session_user)
    client_id = request.client_id
    unit_id = request.unit_id
    password = request.password
    if db.is_invalid_id(tblClientGroups, "client_id", client_id):
        return technomasters.InvalidClientId()
    elif db.is_invalid_id(tblUnits, "unit_id", unit_id):
        return technomasters.InvalidUnitId()
    else:
        if verify_password(db, password, session_user):
            unit_code, unit_name = reactivate_unit_data(
                db, client_id, unit_id, session_user
            )
            return technomasters.ReactivateUnitSuccess(
                unit_code=unit_code, unit_name=unit_name
            )
        else:
            return technomasters.InvalidPassword()


########################################################
# To Get the Profile of all clients
########################################################
def get_client_profile(db, request, session_user):
    client_ids = get_user_clients(db, session_user)
    if client_ids is None:
        return technomasters.UserIsNotResponsibleForAnyClient()
    else:
        profiles = get_profiles(db, client_ids)
        group_companies = get_group_companies_for_user(db, session_user)
        return technomasters.GetClientProfileSuccess(
            group_companies=group_companies,
            profiles=profiles
        )


########################################################
# To promote a user as Primary admin
########################################################
def create_new_admin_for_client(db, request, session_user):
    new_admin_id = request.new_admin_id
    client_id = request.client_id
    old_admin_id = request.old_admin_id
    employee_name = request.username
    result = create_new_admin(
        db, new_admin_id, old_admin_id, employee_name, client_id, session_user
    )
    if result == "ClientDatabaseNotExists":
        return technomasters.ClientDatabaseNotExists()
    elif result == "Reassign":
        return technomasters.ReassignFirst()
    else:
        return technomasters.CreateNewAdminSuccess()


def get_next_unit_code(db, request, session_user):
    client_id = request.client_id
    next_unit_code = get_next_auto_gen_number(db, client_id=client_id)
    return technomasters.GetNextUnitCodeSuccess(next_unit_code)
