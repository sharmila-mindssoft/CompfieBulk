from protocol import knowledgemaster
from server.database.admin import get_countries_for_user, get_domains_for_user
from server.database.knowledgemaster import *
__all__ = [
    "process_knowledge_master_request",
]

#
# knowledge - master - request
#
"""
    process_knowledge_master_request will process below mentioned request.
    parameter :
        request type is object of request class from knowledgemaster protocol.
        db is database connection object.
    return :
        return type is object of response class from knowledgemaster protocol.
"""


def process_knowledge_master_request(request, db, user_id):
    request_frame = request.request

    if type(request_frame) is knowledgemaster.GetGeographyLevels:
        result = process_get_geography_level(db, user_id)

    elif type(request_frame) is knowledgemaster.SaveGeographyLevel:
        result = process_save_geography_level(db, request_frame, user_id)

    elif type(request_frame) is knowledgemaster.GetGeographies:
        result = process_get_geographies(db, user_id)

    elif type(request_frame) is knowledgemaster.SaveGeography:
        result = process_save_geography(db, request_frame, user_id)

    elif type(request_frame) is knowledgemaster.UpdateGeography:
        result = process_update_geography(db, request_frame, user_id)

    elif type(request_frame) is knowledgemaster.ChangeGeographyStatus:
        result = process_change_geography_status(db, request_frame, user_id)

    elif type(request_frame) is knowledgemaster.GetIndustries:
        result = process_get_industry(db)

    elif type(request_frame) is knowledgemaster.SaveIndustry:
        result = process_save_industry(db, request_frame, user_id)

    elif type(request_frame) is knowledgemaster.UpdateIndustry:
        result = process_update_industry(db, request_frame, user_id)

    elif type(request_frame) is knowledgemaster.ChangeIndustryStatus:
        result = process_change_industry_status(db, request_frame, user_id)

    elif type(request_frame) is knowledgemaster.GetStatutoryNatures:
        result = process_get_statutory_nature(db)

    elif type(request_frame) is knowledgemaster.SaveStatutoryNature:
        result = process_save_statutory_nature(db, request_frame, user_id)

    elif type(request_frame) is knowledgemaster.UpdateStatutoryNature:
        result = process_update_statutory_nature(db, request_frame, user_id)

    elif type(request_frame) is knowledgemaster.ChangeStatutoryNatureStatus:
        result = process_change_statutory_nature_status(
            db, request_frame, user_id
        )

    elif type(request_frame) is knowledgemaster.GetStatutoryLevels:
        result = process_get_statutory_level(db, user_id)

    elif type(request_frame) is knowledgemaster.SaveStatutoryLevel:
        result = process_save_statutory_level(db, request_frame, user_id)

    elif type(request_frame) is knowledgemaster.SaveStatutory:
        result = process_save_statutory(db, request_frame, user_id)

    elif type(request_frame) is knowledgemaster.UpdateStatutory:
        result = process_update_statutory(db, request_frame, user_id)

    return result


# industry
########################################################
# To Handle get industry list request
########################################################
def process_get_industry(db):
    results = get_industries(db)
    domain_list = get_domains_for_user(db, 0)
    country_list = get_countries_for_user(db, 0)
    return knowledgemaster.GetIndustriesSuccess(
        industries=results, countries=country_list, domains=domain_list
    )


########################################################
# save industry request
    # request_frame will have industry_name
    # possible returns
    # IndustryNameAlreadyExists
    # SaveIndustrySuccess
########################################################
def process_save_industry(db, request_frame, user_id):
    country_ids = request_frame.country_id
    domain_ids = request_frame.domain_id
    industry_name = request_frame.industry_name
    isDuplicate = check_duplicate_industry(db, country_ids, domain_ids, industry_name, industry_id=None)
    if isDuplicate:
        return knowledgemaster.IndustryNameAlreadyExists()

    if (save_industry(db, country_ids, domain_ids, industry_name, user_id)):
        return knowledgemaster.SaveIndustrySuccess()


    ########################################################
# update industry request
    # request_frame will have industry_id and industry_name
    # possible returns
    # IndustryNameAlreadyExists
    # InvalidIndustryId
    # UpdateIndustrySuccess
########################################################
def process_update_industry(db, request_frame, user_id):
    country_ids = request_frame.country_id
    domain_ids = request_frame.domain_id
    industry_name = request_frame.industry_name
    industry_id = request_frame.industry_id
    isDuplicate = check_duplicate_industry(db, country_ids, domain_ids, industry_name, industry_id)
    if isDuplicate:
        return knowledgemaster.IndustryNameAlreadyExists()

    if (update_industry(db, country_ids, domain_ids, industry_id, industry_name, user_id)):
        return knowledgemaster.UpdateIndustrySuccess()
    else:
        return knowledgemaster.InvalidIndustryId()


    ########################################################
# To Handle change industry request
    # request_frame will have is_active, industry_id
    # possible returns
    # ChangeIndustryStatusSuccess
    # InvalidIndustryId
########################################################
def process_change_industry_status(db, request_frame, user_id):
    is_active = request_frame.is_active
    industry_id = request_frame.industry_id
    if (update_industry_status(db, industry_id, int(is_active), user_id)):
        return knowledgemaster.ChangeIndustryStatusSuccess()
    else:
        return knowledgemaster.InvalidIndustryId()


# statutory nature
def process_get_statutory_nature(db):
    results = get_statutory_nature(db)
    country_list = get_countries_for_user(db, 0)
    success = knowledgemaster.GetStatutoryNaturesSuccess(
        statutory_natures=results, countries=country_list
    )
    return success


########################################################
# To Handle save_statutory_nature request
    # request_frame will have statutory_nature_name
    # possible returns
    # StatutoryNatureNameAlreadyExists
    # SaveStatutoryNatureSuccess
########################################################
def process_save_statutory_nature(db, request_frame, user_id):
    nature_name = request_frame.statutory_nature_name
    country_id = request_frame.country_id
    isDuplicate = check_duplicate_statutory_nature(
        db, nature_name, country_id, nature_id=None
    )
    if isDuplicate:
        return knowledgemaster.StatutoryNatureNameAlreadyExists()
    if (save_statutory_nature(db, nature_name, country_id, user_id)):
        return knowledgemaster.SaveStatutoryNatureSuccess()


    ########################################################
# To Handle update_statutory_nature request
    # request_frame will have statutory_nature_name, statutory_nature_id
    # possible returns
    # StatutoryNatureNameAlreadyExists
    # UpdateStatutoryNatureSuccess
    # InvalidStatutoryNatureId
########################################################
def process_update_statutory_nature(db, request_frame, user_id):
    nature_name = request_frame.statutory_nature_name
    nature_id = request_frame.statutory_nature_id
    country_id = request_frame.country_id
    isDuplicate = check_duplicate_statutory_nature(db, nature_name, nature_id, country_id)
    if isDuplicate:
        return knowledgemaster.StatutoryNatureNameAlreadyExists()
    if (update_statutory_nature(db, nature_id, nature_name, country_id, user_id)):
        return knowledgemaster.UpdateStatutoryNatureSuccess()
    else:
        return knowledgemaster.InvalidStatutoryNatureId()


########################################################
# To Handle change_statutory_nature_status request
    # request_frame will have statutory_nature_id, is_active
    # possible returns
    # ChangeStatutoryNatureStatusSuccess
    # InvalidStatutoryNatureId
########################################################
def process_change_statutory_nature_status(db, request_frame, user_id):
    is_active = request_frame.is_active
    nature_id = request_frame.statutory_nature_id
    if (
        update_statutory_nature_status(
            db, nature_id, int(is_active), user_id
        )
    ):
        return knowledgemaster.ChangeStatutoryNatureStatusSuccess()
    else:
        return knowledgemaster.InvalidStatutoryNatureId()


# statutory level
########################################################
# To Handle get_statutory_levels request
    # Response will have countries, domains and statutory levels.
    # possible returns
    # GetStatutoryLevelsSuccess
########################################################
def process_get_statutory_level(db, user_id):
    countries = get_countries_for_user(db, user_id)
    domains = get_domains_for_user(db, user_id)
    statutory_levels = get_statutory_levels(db)
    return knowledgemaster.GetStatutoryLevelsSuccess(
        countries, domains, statutory_levels
    )


########################################################
# To Handle save statutory level request
    # request_frame args are country_id, domain_id and levels
    # with position and name.
    # possible returns
    # DuplicateStatutoryLevelsExists
    # SaveStatutoryLevelSuccess
########################################################
def process_save_statutory_level(db, request_frame, user_id):
    country_id = request_frame.country_id
    domain_id = request_frame.domain_id
    levels = request_frame.levels
    level_names = [x.level_name.lower().strip() for x in levels if x.level_name != '']
    if len([n for n in level_names if level_names.count(n.lower()) > 1]) > 1:
        return knowledgemaster.DuplicateStatutoryLevelsExists()

    level_positions = [x.level_position for x in levels]
    if len([p for p in level_positions if level_positions.count(p) > 1]) > 1:
        return knowledgemaster.DuplicateStatutoryLevelsExists()

    return save_statutory_levels(
        db, country_id, domain_id, levels, user_id
    )

# geography level
########################################################
# To Handle get geography level
    # request_frame args are user id
    # returns countries and geography level list
########################################################
def process_get_geography_level(db, user_id):
    countries = get_countries_for_user(db, user_id)
    geography_levels = get_geography_levels(db)
    return knowledgemaster.GetGeographyLevelsSuccess(
        countries, geography_levels
    )

########################################################
# To Handle save geography level request
    # request_frame args are country_id, user id and levels
    # with position and name.
    # possible returns
    # DuplicategeographyLevelsExists
    # SavegeographyLevelSuccess
########################################################
def process_save_geography_level(db, request_frame, user_id):
    country_id = request_frame.country_id
    levels = request_frame.levels
    insertValText = request_frame.insertValText
    level_names = [
        x.level_name.lower().strip() for x in levels if x.level_name is not ""
    ]
    if len(
        [n for n in level_names if level_names.count(n.lower()) > 1]
    ) > 1:
        return knowledgemaster.DuplicateGeographyLevelsExists()

    level_positions = [x.level_position for x in levels]
    if len(
        [p for p in level_positions if level_positions.count(p) > 1]
    ) > 1:
        return knowledgemaster.DuplicateGeographyLevelsExists()

    return save_geography_levels(
        db, country_id, levels, insertValText, user_id
    )


###############################################################################
# To Handle get geography list request
    # request_frame args are user id
    # possible returns of countries, geography levels list and geographies list
    # GetGeographiesSuccess
################################################################################
def process_get_geographies(db, user_id):
    countries = get_countries_for_user(db, user_id)
    geography_levels = get_geography_levels(db)
    geographies = get_geographies(db, user_id)
    return knowledgemaster.GetGeographiesSuccess(
        countries,
        geography_levels,
        geographies
    )

###############################################################################
# To Handle Save geography request
    # request_frame args are user id, country id, geography level id, grography
    #  name,parent ids, parent names
    # geographynamealready exists
    # SaveGeographySuccess
################################################################################
def process_save_geography(db, request_frame, user_id):
    geography_level_id = request_frame.geography_level_id
    geography_name = request_frame.geography_name
    parent_ids_list = request_frame.parent_ids
    parent_ids = ','.join(str(x) for x in parent_ids_list) + ","
    parent_names = " >> ".join(str(x) for x in request_frame.parent_names)
    parent_names += " >> " + geography_name
    country_id = request_frame.country_id
    saved_names = [
        row["geography_name"].lower() for row in check_duplicate_geography(
            db, country_id, parent_ids, None
        )
    ]
    if saved_names.count(geography_name.lower()) > 0:
        return knowledgemaster.GeographyNameAlreadyExists()
    else:
        save_geography(
            db, geography_level_id, geography_name, parent_ids,
            parent_names, user_id
        )
        return knowledgemaster.SaveGeographySuccess()

###############################################################################
# To Handle Update geography request
    # request_frame args are user id, country id, geography level id, grography
    #  name,parent ids, parent names
    # geographynamealready exists
    # UpdateGeographySuccess
    # InvalidGeographyId
################################################################################
def process_update_geography(db, request_frame, user_id):
    geography_id = request_frame.geography_id
    # geography_level_id = request_frame.geography_level_id
    geography_name = request_frame.geography_name
    parent_ids_list = request_frame.parent_ids
    parent_ids = ','.join(str(x) for x in parent_ids_list) + ","
    parent_names = ' >> '.join(str(x) for x in request_frame.parent_names)
    parent_names += " >> " + geography_name
    country_id = request_frame.country_id
    saved_names = [
        row["geography_name"].lower() for row in check_duplicate_geography(
            db, country_id, parent_ids, geography_id
        )
    ]
    if saved_names.count(geography_name.lower()) > 0:
        return knowledgemaster.GeographyNameAlreadyExists()
    else:
        if (update_geography(
            db, geography_id, geography_name, parent_ids, parent_names, user_id
        )):
            return knowledgemaster.UpdateGeographySuccess()
        else:
            return knowledgemaster.InvalidGeographyId()

###############################################################################
# To Handle Update geography status request
    # request_frame args are user id, geography id, status
    # ChangeGeographyStatusSuccess
    # InvalidGeographyId
################################################################################
def process_change_geography_status(db, request_frame, user_id):
    geography_id = request_frame.geography_id
    is_active = request_frame.is_active

    if (change_geography_status(db, geography_id, is_active, user_id)):
        return knowledgemaster.ChangeGeographyStatusSuccess()
    else:
        return knowledgemaster.InvalidGeographyId()


# statutories
def process_save_statutory(db, request_frame, user_id):
    statutory_level_id = request_frame.statutory_level_id
    statutory_name = request_frame.statutory_name
    parent_ids_list = request_frame.parent_ids
    parent_names_list = request_frame.parent_names
    if parent_ids_list:
        parent_ids = ','.join(str(x) for x in parent_ids_list) + ","
    else :
        parent_ids = ''
    if parent_names_list:
        parent_names = " >> ".join(str(x) for x in parent_names_list)
    else :
        parent_names = ''
    statutory_id = None
    domain_id = request_frame.domain_id
    country_id = request_frame.country_id
    saved_names = [
        row["statutory_name"].lower() for row in check_duplicate_statutory(
            db, parent_ids, statutory_id, domain_id, country_id
        )
    ]
    if saved_names.count(statutory_name.lower()) > 0:
        return knowledgemaster.StatutoryNameAlreadyExists()
    else:
        save_statutory(
            db,
            statutory_name, statutory_level_id,
            parent_ids, parent_names, user_id
        )
        return knowledgemaster.SaveStatutorySuccess()


def process_update_statutory(db, request_frame, user_id):
    statutory_id = request_frame.statutory_id
    statutory_name = request_frame.statutory_name
    parent_ids_list = request_frame.parent_ids
    if parent_ids_list :
        parent_ids = ','.join(str(x) for x in parent_ids_list) + ","
    else :
        parent_ids = ''
    # parent_names = " >> ".join(str(x) for x in request_frame.parent_names)
    domain_id = request_frame.domain_id
    country_id = request_frame.country_id
    saved_names = [
        row["statutory_name"].lower() for row in check_duplicate_statutory(
            db, parent_ids, statutory_id, domain_id, country_id
        )
    ]
    if saved_names.count(statutory_name.lower()) > 0:
        return knowledgemaster.StatutoryNameAlreadyExists()
    else:
        if (
            update_statutory(
                db, statutory_id, statutory_name,
                user_id
            )
        ):
            return knowledgemaster.SaveStatutorySuccess()
