########################################################
# This Controller will handle Client and Client Unit
# related requests
#
# In this module "db" is an object of "KnowledgeDatabase"
########################################################
from protocol import technomasters

from server.database.login import verify_password
from server.database.knowledgemaster import (
    get_industries
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
    "get_clients_edit",
    "change_client_status",
    "reactivate_unit",
    "get_client_profile",
    "get_assign_legal_entity_list",
    "get_unassigned_units",
    "get_assigned_units",
    "process_save_assigned_units_request",
    "get_edit_assign_legal_entity",
    "process_save_assign_legal_entity",
    "view_assign_legal_entity",
    "save_division_category"
    "check_assigned_units_under_domain"
]

#
# Client Group Master
#


########################################################
# To Get list of all clients with details
########################################################
def get_client_groups(db, request, session_user):
    groups = get_groups(db, session_user)
    return technomasters.GetClientGroupsSuccess(
        groups=groups
    )


########################################################
# To Get data to populate client group form
########################################################
def get_client_group_form_data(db, request, session_user):
    countries = get_user_countries(db, session_user)
    domains = get_user_domains(db, session_user)
    industries = get_industries(db)
    return technomasters.GetClientGroupFormDataSuccess(
        countries=countries, domains=domains,
        industries=industries
    )


########################################################
# To Save Client
########################################################
def process_save_client_group(db, request, session_user):
    session_user = int(session_user)
    if is_duplicate_group_name(db, request.group_name):
        return technomasters.GroupNameAlreadyExists()
    elif is_duplicate_group_short_name(db, request.short_name):
        return technomasters.GroupShortNameAlreadyExists()
    else:
        group_id = save_client_group(
            db, request.group_name, request.email_id,
            request.short_name, request.no_of_view_licence, session_user
        )
        legal_entity_ids = save_legal_entities(
            db, request, group_id, session_user)
        save_date_configurations(
            db, group_id, request.date_configurations, session_user
        )
        # legal_entity_id_name_map = get_legal_entity_ids_by_name(
        #     db, legal_entity_ids
        # )
        # save_client_user(db, group_id, request.email_id)
        save_incharge_persons(db, group_id, request, session_user)
        save_organization(
            db, group_id, request, legal_entity_ids, session_user
        )
        return technomasters.SaveClientGroupSuccess()


########################################################
# To Get data to populate client group form
########################################################
def get_edit_client_group_form_data(db, request, session_user):
    countries = get_user_countries(db, session_user)
    business_groups = get_client_business_groups(db, request.group_id)
    domains = get_user_domains(db, session_user)
    industries = get_industries(db)
    group_id = request.group_id
    (
        group_name, user_name, short_name, total_view_licence,
        legal_entities, date_configuration_list
    ) = get_client_details(db, group_id)
    return technomasters.GetEditClientGroupFormDataSuccess(
        countries=countries, domains=domains,
        business_groups_country=business_groups,
        industries=industries, group_name=group_name,
        email_id=user_name, short_name=short_name,
        no_of_licence=total_view_licence,
        legal_entities=legal_entities,
        date_configurations=date_configuration_list
    )


########################################################
# To Validate and Update Client Group
########################################################
def process_update_client_group(db, request, session_user):
    session_user = int(session_user)
    if is_invalid_group_id(db, request.client_id):
        return technomasters.InvalidClientId()
    elif is_duplicate_group_name(db, request.group_name, request.client_id):
        return technomasters.GroupNameAlreadyExists()
    save_date_configurations(
        db, request.client_id, request.date_configurations, session_user
    )
    update_client_group(
        db, request.client_id, request.email_id, request.no_of_view_licence, request.remarks, session_user
    )
    legal_entity_ids = update_legal_entities(
        db, request, request.client_id, session_user)
    # legal_entity_id_name_map = get_legal_entity_ids_by_name(
    #     db, legal_entity_names
    # )
    save_organization(
        db, request.client_id, request,
        legal_entity_ids, session_user
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
    divisions_list = request.division_units

    if not is_invalid_id(db, "client_id", client_id):
        return technomasters.InvalidClientId()

    if business_group_id is not None and int(business_group_id) > 0:
        if not is_invalid_id(db, "bg_id", business_group_id):
            return technomasters.InvalidBusinessGroupId()

    # if divisions_list is not None:
    #     for row_division in divisions_list:
    #         division_id = row_division.division_id
    #         division_name = row_division.division_name
    #         category_name = row_division.category_name
    #         if division_id is not None:
    #             if not is_invalid_id(db, "division_id", division_id):
    #                 return technomasters.InvalidDivisionId()
    #         else:
    #             if division_name is not None and division_id is None:
    #                 if is_invalid_name(db, "div_name", division_name):
    #                     return technomasters.InvalidDivisionName()

    #         if category_name is not None:
    #             if category_name.find("-") <= 0:
    #                 if is_invalid_name(db, "catg_name", category_name):
    #                     return technomasters.InvalidCategoryName()

    if legal_entity_id is not None:
        if not is_invalid_id(db, "legal_entity_id", legal_entity_id):
            return technomasters.InvalidLegalEntityId()
    return True


########################################################################
# To Validate unit data and merge the divisions, categories for each unit
# Divisions, categories and Units received in the request
########################################################################
def validate_unit_data(db, request, div_ids, category_ids, client_id, session_user):
    units = request.units
    divisions = request.division_units
    new_unit_list = []
    old_unit_list = []
    # dict_unit_list = []
    # int_div_cnt = 1
    # int_unit_cnt = 1
    i = 0
    j = 1
    # var unit
    for counts, div, catg in map(None, divisions, div_ids, category_ids):
        # div_cnt = counts.division_cnt
        unit_cnt = counts.unit_cnt
        while i < len(units):
            unit = units[i]
            unit_id = unit.unit_id
            # unit_name = unit.unit_name
            if is_duplicate_unit_code(db, unit_id, unit.unit_code, client_id):
                return technomasters.UnitCodeAlreadyExists(
                    get_next_auto_gen_number(db, client_id=client_id)
                )

            # elif is_duplicate_unit_name(db, unit_id, unit_name, client_id):
            #     return technomasters.UnitNameAlreadyExists()
            else:
                pass

            if unit_id is not None:
                if not is_invalid_id(db, "unit_id", unit_id):
                    return technomasters.InvalidUnitId()
                old_unit_list.append(unit)
                old_unit_list.append({"div_id": div.get("div_id")})
                old_unit_list.append({"catg_id": catg.get("catg_id")})
            else:
                new_unit_list.append(unit)
                new_unit_list.append({"div_id": div.get("div_id")})
                new_unit_list.append({"catg_id": catg.get("catg_id")})
            if j == unit_cnt:
                i = i + 1
                j = 1
                break
            else:
                j = j + 1
                i = i + 1

    return [True, new_unit_list, old_unit_list]

##############################################################################
# To validate/check duplicate data of division, category and save the data
# Divisions, categories and Units received in the request
##############################################################################
def save_division_category(db, request, session_user):
    print "save division"
    print request.division_category
    for div_catg in request.division_category:
        div_result = update_division(
            db, div_catg.client_id, div_catg.division_id, div_catg.division_name,
            div_catg.business_group_id, div_catg.legal_entity_id, session_user
        )
        category_id = div_catg.cg.split("-")[1]
        category_name = div_catg.cg.split("-")[0]
        catg_result = update_category(
            db, div_catg.client_id, div_catg.division_id, category_id, div_catg.business_group_id,
            div_catg.legal_entity_id, category_name, session_user
        )

        if div_result is False or catg_result is False:
            return False
    return technomasters.SaveDivisionCategorySuccess()

def save_client(db, request, session_user):
    client_id = request.client_id
    business_group_id = request.business_group_id
    legal_entity_id = request.legal_entity_id
    country_id = request.country_id
    divisions = request.division_units
    div_categ = request.division_category
    div_ids = []
    category_ids = []
    res = None

    is_valid = validate_duplicate_data(db, request, session_user)
    if is_valid is True:
        if divisions is not None:
            for division in divisions:
                division_id = division.division_id
                division_name = division.division_name
                div_id = None
                if(division_name == "---"):
                    division_name = None

                category_name = division.category_name
                if(category_name == "---"):
                    category_name = None

                if division_id is None:
                    if division_name is not None:
                        div_id = save_division(
                            db, client_id, division_name, business_group_id, legal_entity_id, session_user
                            )
                        if div_id == 0 or div_id < 0:
                            return technomasters.DivisionNameAlreadyExists()
                        else:
                            div_ids.append({"div_id": div_id})
                    else:
                        div_ids.append({"div_id": 0})
                else:
                    div_result = False
                    div_id = division_id
                    div_result = update_division(
                        db, client_id, div_id, division_name, business_group_id, legal_entity_id, session_user
                    )
                    if (div_result is True):
                        div_ids.append({"div_id": div_id})
                    else:
                        return technomasters.DivisionNameAlreadyExists()

                if category_name is not None:
                    if category_name.find("-") <= 0:
                        category_id = save_category(
                            db, client_id, div_id, business_group_id, legal_entity_id, category_name, session_user
                        )
                        if category_id == 0 or category_id < 0:
                            return technomasters.CategoryNameAlreadyExists()
                        else:
                            category_ids.append({"catg_id": category_id})
                    else:
                        category_id = int(category_name.split("-")[1])
                        catg_result = False
                        catg_result = update_category(
                            db, client_id, div_id, category_id, business_group_id, legal_entity_id,
                            category_name.split("-")[0], session_user
                        )
                        if catg_result is True:
                            category_ids.append({"catg_id": category_id})
                        else:
                            return technomasters.CategoryNameAlreadyExists()
                else:
                    category_ids.append({"catg_id": 0})
        if div_categ is not None:
            for div_catg in request.division_category:
                div_result = update_division(
                    db, div_catg.client_id, div_catg.division_id, div_catg.division_name,
                    div_catg.business_group_id, div_catg.legal_entity_id, session_user
                )
                category_id = div_catg.cg.split("-")[1]
                category_name = div_catg.cg.split("-")[0]
                catg_result = update_category(
                    db, div_catg.client_id, div_catg.division_id, category_id, div_catg.business_group_id,
                    div_catg.legal_entity_id, category_name, session_user
                )

                if div_result is False or catg_result is False:
                    return False
        is_valid_unit = validate_unit_data(db, request, div_ids, category_ids, client_id, session_user)
        if type(is_valid_unit) is not list:
            return is_valid_unit
        else:
            if is_valid_unit[0] is True:
                units = is_valid_unit[1]
                if(len(is_valid_unit[1]) > 0):
                    res = save_unit(
                        db, client_id, units, business_group_id, legal_entity_id, country_id, session_user
                    )
                    if res is True:
                        res = update_unit(db, client_id, legal_entity_id, is_valid_unit[2], session_user)
                else:
                    if(len(is_valid_unit[2]) > 0):
                        res = update_unit(db, client_id, legal_entity_id, is_valid_unit[2], session_user)
        if res:
            return technomasters.SaveClientSuccess()
        else:
            return False

##############################################################################
# To check units assigned under domain to remove the domain from the units
# returns the units count assigned under the domain
##############################################################################
def check_assigned_units_under_domain(db, request, session_user):
    unit_id = request.unit_id
    domain_ids = request.d_id
    unassignDomainUnits(db, unit_id, domain_ids, session_user)
    return technomasters.UnassignedUnitSuccess()

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
        client_unit_list = get_unit_details_for_user(db, session_user, request)
        business_group_list = get_business_groups_for_user(db, session_user)
        countries_units = get_countries_for_unit(db, session_user)
        legal_entity_list = get_legal_entities_for_user(db, session_user)
        domain_orgn_list = get_domains_for_unit(db, session_user)
        division_list = get_divisions_for_user(db, session_user)
        unit_geography_level_list = get_unit_geograhpy_levels_for_user(db, session_user)
        unit_geographies_list = get_geographies_for_unit(db, session_user)
        # unit_industries_list = get_client_industries(db, session_user)
        # client_domains = get_user_client_domains(db, session_user)
        return technomasters.GetClientsSuccess(
            client_unit_list=client_unit_list,
            group_company_list=group_company_list,
            business_group_list=business_group_list,
            countries_units=countries_units,
            unit_legal_entity=legal_entity_list,
            domains_organization_list=domain_orgn_list,
            divisions=division_list,
            unit_geography_level_list=unit_geography_level_list,
            unit_geographies_list=unit_geographies_list
        )
    else:
        return technomasters.UserIsNotResponsibleForAnyClient()

##############################################################################
# To get client groups with max unit id to generate unit code
# Divisions, categories and Units received in the request
##############################################################################
def get_clients_edit(db, request, session_user):
    group_company_list = get_group_companies_for_user_with_max_unit_count(
        db, session_user
    )
    if len(group_company_list) > 0:
        unit_list = get_unit_details_for_user_edit(db, session_user, request)
        return technomasters.GetClientsEditSuccess(
            unit_list=unit_list
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

def get_next_unit_code(db, request, session_user):
    client_id = request.client_id
    next_unit_code = get_next_auto_gen_number(db, client_id=client_id)
    return technomasters.GetNextUnitCodeSuccess(next_unit_code)

#
# Assign Legal Entity
#


########################################################
# To Get list of all legal entity
########################################################
def get_assign_legal_entity_list(db, request, session_user):
    assign_le_list = get_assign_legalentities(db, session_user)
    return technomasters.GetAssignLegalEntityListSuccess(
        assign_le_list=assign_le_list
    )


############################################################
# To Get Unassigned units list
############################################################
def get_unassigned_units(db, session_user):
    units_list = get_unassigned_units_list(db, session_user)
    user_category_id = get_user_category_id(db, session_user)
    return technomasters.GetUnassignedUnitsSuccess(
        unassigned_units_list=units_list,
        user_category_id=user_category_id
    )


############################################################
# To Get assigned units list
############################################################
def get_assigned_units(db, request, session_user):
    units_list = get_assigned_units_list(db, request, session_user)
    return technomasters.GetAssignedUnitsSuccess(
        assigned_units_list=units_list
    )


############################################################
# To Get assigned unit details list
############################################################
def get_assigned_unit_details(db, request):
    units_list = get_assigned_unit_details_list(db, request)
    return technomasters.GetAssignedUnitDetailsSuccess(
        assigned_unit_details_list=units_list
    )


############################################################
# To Get assign unit form data
############################################################
def get_assign_unit_form_data(db, request, session_user):
    (
        business_groups, legal_entities, units, domain_managers, mapped_domain_users
    ) = get_data_for_assign_unit(db, request, session_user)
    return technomasters.GetAssignUnitFormDataSuccess(
        business_groups=business_groups,
        unit_legal_entity=legal_entities,
        assigned_unit_details_list=units,
        domain_manager_users=domain_managers,
        mapped_domain_users=mapped_domain_users
    )


############################################################
# To save assigned units
############################################################
def process_save_assigned_units_request(db, request, session_user):
    save_assigned_units(db, request, session_user)
    return technomasters.SaveAsssignedUnitsSuccess()


########################################################
# To Get data of particular client
########################################################
def get_edit_assign_legal_entity(db, request, session_user):
    #countries = get_user_countries(db, session_user)
    techno_users = get_techno_users_list(db, session_user)
    group_id = request.group_id
    unassign_legal_entities = get_unassigned_legal_entity(db, group_id)

    return technomasters.GetEditAssignLegalEntitySuccess(
        unassign_legal_entities=unassign_legal_entities,
        techno_users=techno_users
    )

########################################################
# To save assign legal entity
########################################################
def process_save_assign_legal_entity(db, request, session_user):
    #countries = get_user_countries(db, session_user)
    #techno_users = get_techno_users_list(db)
    # group_id = request.group_id
    # unassign_legal_entities= get_unassigned_legal_entity(db, group_id)
    client_id = request.client_id
    user_ids = request.user_ids
    legal_entity_ids = request.legal_entity_ids
    save_assign_legal_entity(db, client_id, legal_entity_ids, user_ids, session_user)
    return technomasters.SaveAssignLegalEntitySuccess()


def view_assign_legal_entity(db, request, session_user):
    #countries = get_user_countries(db, session_user)
    #techno_users = get_techno_users_list(db, session_user)
    client_id = request.client_id
    assigned_legal_entities = get_assigned_legal_entity(db, client_id)

    return technomasters.ViewAssignLegalEntitySuccess(
        assigned_legal_entities=assigned_legal_entities,
    )


