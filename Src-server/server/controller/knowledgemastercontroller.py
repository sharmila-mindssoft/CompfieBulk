from protocol import login, knowledgemaster
from generalcontroller import validate_user_session, validate_user_forms

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

def process_knowledge_master_request(request, db) :
    session_token = request.session_token
    request_frame = request.request
    user_id = validate_user_session(db, session_token)
    if user_id is not None :
        is_valid = validate_user_forms(db, user_id, forms, request_frame)
        if is_valid is not True :
            return login.InvalidSessionToken()
    if user_id is None:
        return login.InvalidSessionToken()

    if type(request_frame) is knowledgemaster.GetGeographyLevels:
        return process_get_geography_level(db, user_id)

    if type(request_frame) is knowledgemaster.SaveGeographyLevel:
        return process_save_geography_level(db, request_frame, user_id)

    if type(request_frame) is knowledgemaster.GetGeographies:
        return process_get_geographies(db, user_id)

    if type(request_frame) is knowledgemaster.SaveGeography:
        return process_save_geography(db, request_frame, user_id)

    if type(request_frame) is knowledgemaster.UpdateGeography:
        return process_update_geography(db, request_frame, user_id)

    if type(request_frame) is knowledgemaster.ChangeGeographyStatus:
        return process_change_geography_status(db, request_frame, user_id)

    if type(request_frame) is knowledgemaster.GetIndustries:
        return process_get_industry(db)

    if type(request_frame) is knowledgemaster.SaveIndustry:
        return process_save_industry(db, request_frame, user_id)

    if type(request_frame) is knowledgemaster.UpdateIndustry:
        return process_update_industry(db, request_frame, user_id)

    if type(request_frame) is knowledgemaster.ChangeIndustryStatus:
        return process_change_industry_status(db, request_frame, user_id)

    if type(request_frame) is knowledgemaster.GetStatutoryNatures:
        return process_get_statutory_nature(db)

    if type(request_frame) is knowledgemaster.SaveStatutoryNature:
        return process_save_statutory_nature(db, request_frame, user_id)

    if type(request_frame) is knowledgemaster.UpdateStatutoryNature:
        return process_update_statutory_nature(db, request_frame, user_id)

    if type(request_frame) is knowledgemaster.ChangeStatutoryNatureStatus :
        return process_change_statutory_nature_status(db, request_frame, user_id)

    if type(request_frame) is knowledgemaster.GetStatutoryLevels:
        return process_get_statutory_level(db, user_id)

    if type(request_frame) is knowledgemaster.SaveStatutoryLevel:
        return process_save_statutory_level(db, request_frame, user_id)

    if type(request_frame) is knowledgemaster.SaveStatutory:
        return process_save_statutory(db, request_frame, user_id)

    if type(request_frame) is knowledgemaster.UpdateStatutory:
        return process_update_statutory(db, request_frame, user_id)

# industry
########################################################
# To Handle get industry list request
########################################################

def process_get_industry(db):
    results = db.get_industries()
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
    isDuplicate = db.check_duplicate_industry(industry_name, industry_id=None)

    if isDuplicate :
        return knowledgemaster.IndustryNameAlreadyExists()

    if (db.save_industry(industry_name, user_id)):
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
    isDuplicate = db.check_duplicate_industry(industry_name, industry_id)

    if isDuplicate :
        return knowledgemaster.IndustryNameAlreadyExists()

    if (db.update_industry(industry_id, industry_name, user_id)):
        return knowledgemaster.UpdateIndustrySuccess()
    else :
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

    if (db.update_industry_status(industry_id, int(is_active), user_id)) :
        return knowledgemaster.ChangeIndustryStatusSuccess()
    else :
        return knowledgemaster.InvalidIndustryId()

# statutory nature
def process_get_statutory_nature(db):
    results = db.get_statutory_nature()
    success = knowledgemaster.GetStatutoryNaturesSuccess(statutory_natures=results)
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
    isDuplicate = db.check_duplicate_statutory_nature(nature_name, nature_id=None)

    if isDuplicate :
        return knowledgemaster.StatutoryNatureNameAlreadyExists()

    if (db.save_statutory_nature(nature_name, user_id)):
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
    isDuplicate = db.check_duplicate_statutory_nature(nature_name, nature_id)

    if isDuplicate :
        return knowledgemaster.StatutoryNatureNameAlreadyExists()

    if (db.update_statutory_nature(nature_id, nature_name, user_id)):
        return knowledgemaster.UpdateStatutoryNatureSuccess()
    else :
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

    if (db.update_statutory_nature_status(nature_id, int(is_active), user_id)) :
        return knowledgemaster.ChangeStatutoryNatureStatusSuccess()
    else :
        return knowledgemaster.InvalidStatutoryNatureId()

# statutory level
########################################################
# To Handle get_statutory_levels request
    # Response will have countries, domains and statutory levels.
    # possible returns
    # GetStatutoryLevelsSuccess
########################################################
def process_get_statutory_level(db, user_id):
    countries = db.get_countries_for_user(user_id)
    domains = db.get_domains_for_user(user_id)
    statutory_levels = db.get_statutory_levels()
    return knowledgemaster.GetStatutoryLevelsSuccess(
        countries, domains, statutory_levels
    )

########################################################
# To Handle save statutory level request
    # request_frame args are country_id, domain_id and levels with position and name.
    # possible returns
    # DuplicateStatutoryLevelsExists
    # SaveStatutoryLevelSuccess
########################################################
def process_save_statutory_level(db, request_frame, user_id):
    country_id = request_frame.country_id
    domain_id = request_frame.domain_id
    levels = request_frame.levels
    level_names = [x.level_name.lower().strip() for x in levels]
    if len([n for n in level_names if level_names.count(n.lower()) > 1]) > 1 :
        return knowledgemaster.DuplicateStatutoryLevelsExists()

    level_positions = [x.level_position for x in levels]
    if len([p for p in level_positions if level_positions.count(p) > 1]) > 1 :
        return knowledgemaster.DuplicateStatutoryLevelsExists()

    db.save_statutory_levels(
        country_id, domain_id, levels, user_id
    )
    return knowledgemaster.SaveStatutoryLevelSuccess()

# geography level
def process_get_geography_level(db, user_id):
    countries = db.get_countries_for_user(user_id)
    geography_levels = db.get_geography_levels()
    return knowledgemaster.GetGeographyLevelsSuccess(
        countries, geography_levels
    )

def process_save_geography_level(db, request_frame, user_id):
    country_id = request_frame.country_id
    levels = request_frame.levels

    level_names = [x.level_name.lower().strip() for x in levels]
    if len([n for n in level_names if level_names.count(n.lower()) > 1]) > 1 :
        return knowledgemaster.DuplicateGeographyLevelsExists()

    level_positions = [x.level_position for x in levels]
    if len([p for p in level_positions if level_positions.count(p) > 1]) > 1 :
        return knowledgemaster.DuplicateGeographyLevelsExists()

    # is_duplicate = db.check_duplicate_gepgrahy_levels(country_id, levels)
    # if is_duplicate :
    #     return knowledgemaster.LevelIdCannotBeNull(is_duplicate)

    db.save_geography_levels(
        country_id, levels, user_id
    )
    return knowledgemaster.SaveGeographyLevelSuccess()



#geography
def process_get_geographies(db, user_id):
    countries = db.get_countries_for_user(user_id)
    geography_levels = db.get_geograhpy_levels_for_user(user_id)
    geographies = db.get_geographies(user_id)
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
    country_id = request_frame.country_id

    saved_names = [row["geography_name"].lower() for row in db.check_duplicate_geography(country_id, parent_ids, None)]

    if saved_names.count(geography_name.lower()) > 0 :
        return knowledgemaster.GeographyNameAlreadyExists()
    else :
        db.save_geography(geography_level_id, geography_name, parent_ids, parent_names, user_id)
        return knowledgemaster.SaveGeographySuccess()


def process_update_geography(db, request_frame, user_id):
    geography_id = request_frame.geography_id
    # geography_level_id = request_frame.geography_level_id
    geography_name = request_frame.geography_name
    parent_ids_list = request_frame.parent_ids
    parent_ids = ','.join(str(x) for x in parent_ids_list) + ","
    parnet_names = ' >> '.join(str(x) for x in request_frame.parent_names)
    country_id = request_frame.country_id

    saved_names = [row["geography_name"].lower() for row in db.check_duplicate_geography(country_id, parent_ids, geography_id)]
    if saved_names.count(geography_name.lower()) > 0 :
        return knowledgemaster.GeographyNameAlreadyExists()
    else :
        if (db.update_geography(
            geography_id, geography_name, parent_ids, parnet_names, user_id
        )):
            return knowledgemaster.UpdateGeographySuccess()
        else :
            return knowledgemaster.InvalidGeographyId()

def process_change_geography_status(db, request_frame, user_id):
    geography_id = request_frame.geography_id
    is_active = request_frame.is_active

    if (db.change_geography_status(geography_id, is_active, user_id)):
        return knowledgemaster.ChangeGeographyStatusSuccess()
    else :
        return knowledgemaster.InvalidGeographyId()

#statutories
def process_save_statutory(db, request_frame, user_id):
    statutory_level_id = request_frame.statutory_level_id
    statutory_name = request_frame.statutory_name
    parent_ids_list = request_frame.parent_ids
    parent_ids = ','.join(str(x) for x in parent_ids_list) + ","
    parent_names = " >> ".join(str(x) for x in request_frame.parent_names)
    statutory_id = None
    domain_id = request_frame.domain_id
    saved_names = [
        row["statutory_name"].lower() for row in db.check_duplicate_statutory(
            parent_ids, statutory_id, domain_id
        )
    ]

    if saved_names.count(statutory_name.lower()) > 0 :
        return knowledgemaster.StatutoryNameAlreadyExists()
    else :
        db.save_statutory(
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
    saved_names = [row["statutory_name"].lower() for row in db.check_duplicate_statutory(parent_ids, statutory_id)]
    if saved_names.count(statutory_name.lower()) > 0 :
        return knowledgemaster.StatutoryNameAlreadyExists()
    else :
        if (db.update_statutory(statutory_id, statutory_name, parent_ids, parent_names, user_id)):
            return knowledgemaster.SaveStatutorySuccess()
