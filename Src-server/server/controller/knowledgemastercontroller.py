import time
from protocol import login, knowledgemaster
from generalcontroller import validate_user_session, validate_user_forms
from server import logger
from server.database.admin import get_countries_for_user, get_domains_for_user
from server.database.knowledgemaster import *
__all__ = [
    "process_knowledge_master_request",
]

forms = [5, 6, 7, 8, 9, 10]

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


def process_knowledge_master_request(request, db):
    session_token = request.session_token
    request_frame = request.request
    user_id = validate_user_session(db, session_token)
    if user_id is not None:
        is_valid = validate_user_forms(db, user_id, forms, request_frame)
        if is_valid is not True:
            return login.InvalidSessionToken()
    if user_id is None:
        return login.InvalidSessionToken()

    if type(request_frame) is knowledgemaster.GetGeographyLevels:
        logger.logKnowledgeApi("GetGeographyLevels", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_geography_level(db, user_id)
        logger.logKnowledgeApi("GetGeographyLevels", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is knowledgemaster.SaveGeographyLevel:
        logger.logKnowledgeApi("SaveGeographyLevel", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_save_geography_level(db, request_frame, user_id)
        logger.logKnowledgeApi("SaveGeographyLevel", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is knowledgemaster.GetGeographies:
        logger.logKnowledgeApi("GetGeographies", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_geographies(db, user_id)
        logger.logKnowledgeApi("GetGeographies", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is knowledgemaster.SaveGeography:
        logger.logKnowledgeApi("SaveGeography", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_save_geography(db, request_frame, user_id)
        logger.logKnowledgeApi("SaveGeography", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is knowledgemaster.UpdateGeography:
        logger.logKnowledgeApi("UpdateGeography", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_update_geography(db, request_frame, user_id)
        logger.logKnowledgeApi("UpdateGeography", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is knowledgemaster.ChangeGeographyStatus:
        logger.logKnowledgeApi("ChangeGeographyStatus", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_change_geography_status(db, request_frame, user_id)
        logger.logKnowledgeApi("ChangeGeographyStatus", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is knowledgemaster.GetIndustries:
        logger.logKnowledgeApi("GetIndustries", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_industry(db)
        logger.logKnowledgeApi("GetIndustries", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is knowledgemaster.SaveIndustry:
        logger.logKnowledgeApi("SaveIndustry", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_save_industry(db, request_frame, user_id)
        logger.logKnowledgeApi("SaveIndustry", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is knowledgemaster.UpdateIndustry:
        logger.logKnowledgeApi("UpdateIndustry", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_update_industry(db, request_frame, user_id)
        logger.logKnowledgeApi("UpdateIndustry", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is knowledgemaster.ChangeIndustryStatus:
        logger.logKnowledgeApi("ChangeIndustryStatus", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_change_industry_status(db, request_frame, user_id)
        logger.logKnowledgeApi("ChangeIndustryStatus", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is knowledgemaster.GetStatutoryNatures:
        logger.logKnowledgeApi("GetStatutoryNatures", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_statutory_nature(db)
        logger.logKnowledgeApi("GetStatutoryNatures", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is knowledgemaster.SaveStatutoryNature:
        logger.logKnowledgeApi("SaveStatutoryNature", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_save_statutory_nature(db, request_frame, user_id)
        logger.logKnowledgeApi("SaveStatutoryNature", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is knowledgemaster.UpdateStatutoryNature:
        logger.logKnowledgeApi("UpdateStatutoryNature", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_update_statutory_nature(db, request_frame, user_id)
        logger.logKnowledgeApi("UpdateStatutoryNature", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is knowledgemaster.ChangeStatutoryNatureStatus:
        logger.logKnowledgeApi("ChangeStatutoryNatureStatus", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_change_statutory_nature_status(
            db, request_frame, user_id
        )
        logger.logKnowledgeApi("ChangeStatutoryNatureStatus", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is knowledgemaster.GetStatutoryLevels:
        logger.logKnowledgeApi("GetStatutoryLevels", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_statutory_level(db, user_id)
        logger.logKnowledgeApi("GetStatutoryLevels", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is knowledgemaster.SaveStatutoryLevel:
        logger.logKnowledgeApi("SaveStatutoryLevel", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_save_statutory_level(db, request_frame, user_id)
        logger.logKnowledgeApi("SaveStatutoryLevel", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is knowledgemaster.SaveStatutory:
        logger.logKnowledgeApi("SaveStatutory", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_save_statutory(db, request_frame, user_id)
        logger.logKnowledgeApi("SaveStatutory", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is knowledgemaster.UpdateStatutory:
        logger.logKnowledgeApi("UpdateStatutory", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_update_statutory(db, request_frame, user_id)
        logger.logKnowledgeApi("UpdateStatutory", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    else:
        result = login.InvalidSessionToken()

    return result


# industry
########################################################
# To Handle get industry list request
########################################################
def process_get_industry(db):
    results = get_industries(db)
    return knowledgemaster.GetIndustriesSuccess(industries=results)


########################################################
# save industry request
    # request_frame will have industry_name
    # possible returns
    # IndustryNameAlreadyExists
    # SaveIndustrySuccess
########################################################
def process_save_industry(db, request_frame, user_id):
    industry_name = request_frame.industry_name
    isDuplicate = check_duplicate_industry(db, industry_name, industry_id=None)
    if isDuplicate:
        return knowledgemaster.IndustryNameAlreadyExists()

    if (save_industry(db, industry_name, user_id)):
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
    industry_name = request_frame.industry_name
    industry_id = request_frame.industry_id
    isDuplicate = check_duplicate_industry(db, industry_name, industry_id)
    if isDuplicate:
        return knowledgemaster.IndustryNameAlreadyExists()

    if (update_industry(db, industry_id, industry_name, user_id)):
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
    success = knowledgemaster.GetStatutoryNaturesSuccess(
        statutory_natures=results
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
    isDuplicate = check_duplicate_statutory_nature(
        db, nature_name, nature_id=None
    )
    if isDuplicate:
        return knowledgemaster.StatutoryNatureNameAlreadyExists()
    if (save_statutory_nature(db, nature_name, user_id)):
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
    isDuplicate = check_duplicate_statutory_nature(db, nature_name, nature_id)
    if isDuplicate:
        return knowledgemaster.StatutoryNatureNameAlreadyExists()
    if (update_statutory_nature(db, nature_id, nature_name, user_id)):
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
def process_get_geography_level(db, user_id):
    countries = get_countries_for_user(db, user_id)
    geography_levels = get_geography_levels(db)
    return knowledgemaster.GetGeographyLevelsSuccess(
        countries, geography_levels
    )


def process_save_geography_level(db, request_frame, user_id):
    country_id = request_frame.country_id
    levels = request_frame.levels
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
        db, country_id, levels, user_id
    )


# geography
def process_get_geographies(db, user_id):
    countries = get_countries_for_user(db, user_id)
    geography_levels = get_geograhpy_levels_for_user(db, user_id)
    geographies = get_geographies(db, user_id)
    return knowledgemaster.GetGeographiesSuccess(
        countries,
        geography_levels,
        geographies
    )


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
    parent_ids = ','.join(str(x) for x in parent_ids_list) + ","
    parent_names = " >> ".join(str(x) for x in request_frame.parent_names)
    statutory_id = None
    domain_id = request_frame.domain_id
    saved_names = [
        row["statutory_name"].lower() for row in check_duplicate_statutory(
            db, parent_ids, statutory_id, domain_id
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
    parent_ids = ','.join(str(x) for x in parent_ids_list) + ","
    parent_names = " >> ".join(str(x) for x in request_frame.parent_names)
    saved_names = [
        row["statutory_name"].lower() for row in check_duplicate_statutory(
            db, parent_ids, statutory_id)
    ]
    if saved_names.count(statutory_name.lower()) > 0:
        return knowledgemaster.StatutoryNameAlreadyExists()
    else:
        if (
            update_statutory(
                db, statutory_id, statutory_name, parent_ids,
                parent_names, user_id
            )
        ):
            return knowledgemaster.SaveStatutorySuccess()
