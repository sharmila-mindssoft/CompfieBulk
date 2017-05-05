from protocol import (
    core, knowledgemaster
)
from server.exceptionmessage import *
from server.common import (
    get_date_time
)
from server.database.tables import *
from server.database.forms import *
from server.database.admin import (
    get_domain_by_id,
    get_country_by_id
)

__all__ = [
    "get_industries", "get_active_industries",
    "check_duplicate_industry", "get_industry_by_id",
    "save_industry", "update_industry",
    "update_industry_status",
    "get_statutory_nature",
    "check_duplicate_statutory_nature",
    "save_statutory_nature",
    "update_statutory_nature",
    "update_statutory_nature_status",
    "get_statutory_levels",
    "save_statutory_levels",
    "get_geography_levels",
    "get_geograhpy_levels_for_user",
    "delete_grography_level",
    "save_geography_levels",
    "get_geographies",
    "get_geographies_for_user_with_mapping", "get_geography_by_id",
    "check_duplicate_geography", "save_geography",
    "update_geography", "change_geography_status",
    "save_statutory", "update_statutory", "get_statutory_master",
    "get_statutory_by_id", "get_country_wise_level_1_statutoy",
    "check_duplicate_statutory"
]

STATUTORY_PARENTS = {}
GEOGRAPHY_PARENTS = {}

#############################################################################
# To get industries list
# Parameter(s) : Object of database
# Return Type : List of Object of Organization
#############################################################################
def get_industries(db):
    columns = [
        "country_id", "country_name",
        "domain_id", "domain_name",
        "industry_id", "industry_name",
        "is_active"
    ]
    result = db.call_proc("sp_industry_master_getindustries", (), columns)
    return return_industry(result)

#############################################################################
# To get industries by id
# Parameter(s) : Object of database, industry id
# Return Type : List of Object of Organization
#############################################################################
def get_industry_by_id(db, industry_id):
    if type(industry_id) is int:
        values_list = [industry_id]
    else:
        values_list = industry_id
    row = db.call_proc("sp_industry_master_getindusdtrybyid", values_list)

    industry_names = []
    for r in row:
        industry_names.append(r["organisation_name"])

    return ", ".join(industry_names)

# stored procedure not created
def get_active_industries(db):
    columns = ["country_id", "country_name", "domain_id", "domain_name", "industry_id", "industry_name", "is_active"]
    tables = [
        tbl_industries, tbl_countries, tbl_domains
    ]
    aliases = ["t1", "t2", "t3"]
    condition = " is_active = %s and t1.country_id = t2.country_id and t1.domain_id = t3.domain_id "
    order = " ORDER BY industry_name"
    result = db.get_data_from_multiple_tables(
        columns, tables, aliases, condition, condition_val=[1], order=order
    )
    return return_industry(result)


def return_industry(data):
    results = []
    for d in data:
        country_id = d["country_id"]
        country_name = d["country_name"]
        domain_id = d["domain_id"]
        domain_name = d["domain_name"]
        industry_id = d["industry_id"]
        industry_name = d["industry_name"]
        is_active = bool(d["is_active"])
        results.append(core.Industry(
            country_id, country_name, domain_id, domain_name, industry_id, industry_name, is_active
        ))
    return results

######################################################################################
# To get count of organziation by id
# Parameter(s) : Object of database, industry id, industry name, country id, domain id
# Return Type : Count of organization
######################################################################################
def check_duplicate_industry(db, country_id, domain_id, industry_name, industry_id):
    isDuplicate = False

    if industry_id is not None:
        param = [industry_id, industry_name, country_id, domain_id]
    else:
        param = [0, industry_name, country_id, domain_id]

    row = db.call_proc("sp_industry_master_checkduplicateindustry", param)
    for r in row:
        if int(r["count(1)"]) > 0:
            isDuplicate = True

    return isDuplicate

######################################################################################
# To Save organziation
# Parameter(s) : Object of database, industry id, industry name, country id, domain id
# Return Type : Return value of the organization saved
######################################################################################
def save_industry(db, country_ids, domain_ids, industry_name, user_id):
    # table_name = "tbl_industries"
    created_on = get_date_time()
    # columns = ["country_id", "domain_id", "industry_name", "created_by", "created_on"]
    values = [country_ids, domain_ids, industry_name, str(user_id), str(created_on)]
    new_id = db.call_insert_proc("sp_industry_master_saveindustry", values)
    if new_id is False:
        raise process_error("E001")
    else :
        msg_text = "Organization Name \"" + industry_name + "\" Added "
        u_cg_id = [3, 5, 7]
        for cg_id in u_cg_id:
            users_id = []
            result = db.call_proc("sp_users_under_user_category", (cg_id,))
            for user in result:
                users_id.append(user["user_id"])
            if len(users_id) > 0:
                db.save_toast_messages(cg_id, "Organization Type Created", msg_text, None, users_id, user_id)
        action = "New Organization type %s added" % (industry_name)
        db.save_activity(user_id, frmOrganizationMaster, action)
        return True

######################################################################################
# To Update organziation
# Parameter(s) : Object of database, industry id, industry name, country id, domain id
# Return Type : Return value of the organization updated
######################################################################################
def update_industry(db, country_ids, domain_ids, industry_id, industry_name, user_id):
    new_id = False
    oldData = get_industry_by_id(db, industry_id)
    if oldData is None:
        return False
    values = [industry_id, industry_name, country_ids, domain_ids, str(user_id)]
    new_id = db.call_update_proc("sp_industry_master_updateindustry", values)
    if new_id is True:
        u_cg_id = [3, 4, 5, 6, 7, 8]
        msg_text = "Organization Name \"" + oldData + "\" Updated as \"" + industry_name + "\""
        for cg_id in u_cg_id:
            users_id = []
            result = db.call_proc("sp_users_under_user_category", (cg_id, ))
            for user in result:
                users_id.append(user["user_id"])
            if len(users_id) > 0:
                db.save_toast_messages(cg_id, "Organization Name Updated", msg_text, None, users_id, user_id)
        action = "Organization type %s updated" % (industry_name)
        db.save_activity(user_id, frmOrganizationMaster, action)
        return True
    else:
        raise process_error("E002")

######################################################################################
# To Update organziation Status
# Parameter(s) : Object of database, industry id, status, user id
# Return Type : Return value of the organization status updated
######################################################################################
def update_industry_status(db, industry_id, is_active, user_id):
    oldData = get_industry_by_id(db, industry_id)
    if oldData is None:
        return False
    values = [industry_id, is_active, user_id]
    new_id = db.call_update_proc("sp_industry_master_updatestatus", values)
    if new_id is True:
        if is_active == 0:
            status = "deactivated"
            msg_text = "Organization Name \"" + oldData + "\" Deactivated "
        else:
            status = "activated"
            msg_text = "Organization Name \"" + oldData + "\" Activated "
        u_cg_id = [3, 4, 5, 6, 7]
        for cg_id in u_cg_id:
            users_id = []
            result = db.call_proc("sp_users_under_user_category", (cg_id, ))
            for user in result:
                users_id.append(user["user_id"])
            if len(users_id) > 0:
                db.save_toast_messages(cg_id, "Organization Status Updated", msg_text, None, users_id, user_id)
        action = "Organization type %s status - %s" % (oldData, status)
        db.save_activity(user_id, frmOrganizationMaster, action)
        return True
    else:
        raise process_error("E003")

######################################################################################
# To Get Statutory Nature name by id
# Parameter(s) : Object of database, nature id
# Return Type : Return statutory nature name
######################################################################################
def get_nature_by_id(db, nature_id):
    if type(nature_id) is int:
        values_list = [nature_id]
    else:
        values_list = nature_id
    row = db.call_proc("sp_statutory_natures_getnaturebyid", values_list)
    nature_name = None
    for r in row:
        nature_name = r["statutory_nature_name"]
    return nature_name

######################################################################################
# To Get Statutory Nature
# Parameter(s) : Object of database, nature id
# Return Type : Return list of statutory nature
######################################################################################
def get_statutory_nature(db):
    columns = [
        "statutory_nature_id", "statutory_nature_name", "country_id", "country_name",
        "is_active"
    ]

    result = db.call_proc("sp_statutory_nature_getstatutorynatures", (), columns)
    return return_statutory_nature(result)


def return_statutory_nature(data):
    results = []
    for d in data:
        nature_id = d["statutory_nature_id"]
        nature_name = d["statutory_nature_name"]
        country_id = d["country_id"]
        country_name = d["country_name"]
        is_active = bool(d["is_active"])
        results.append(core.StatutoryNature(
            nature_id, nature_name, country_id, country_name, is_active
        ))
    return results

######################################################################################
# To check dupliacte Statutory Nature
# Parameter(s) : Object of database, nature id, nature name, country id
# Return Type : Return count of the statutory nature list under the parameter
######################################################################################
def check_duplicate_statutory_nature(db, nature_name, country_id, nature_id):
    isDuplicate = False
    if nature_id is not None:
        param = [nature_name, nature_id, country_id]
    else:
        param = [nature_name, 0, country_id]
    row = db.call_proc("sp_statutory_nature_checkduplicatenature", param)

    for r in row:
        if r["cnt"] > 0:
            isDuplicate = True
    return isDuplicate

######################################################################################
# To Save Statutory Nature
# Parameter(s) : Object of database, country id, nature name, user id
# Return Type : Return value of the saved staturtory nature
######################################################################################
def save_statutory_nature(db, nature_name, country_id, user_id):
    created_on = get_date_time()
    # columns = ["statutory_nature_name", "country_id", "created_by", "created_on"]
    values = [nature_name, country_id, user_id, str(created_on)]
    new_id = db.call_insert_proc("sp_statutorynature_savestatutorynature", values)
    if new_id is False:
        raise process_error("E004")
    else:
        msg_text = "Statutory Nature \"" + nature_name + "\" Added "
        u_cg_id = [3, 4, 5, 6, 7]
        for cg_id in u_cg_id:
            users_id = []
            result = db.call_proc("sp_users_under_user_category", (cg_id,))
            for user in result:
                users_id.append(user["user_id"])
            if len(users_id) > 0:
                db.save_toast_messages(cg_id, "Statutory Nature Created", msg_text, None, users_id, user_id)
        action = "New Statutory Nature %s added" % (nature_name)
        db.save_activity(user_id, frmStatutoryNatureMaster, action)
        return True

######################################################################################
# To Update Statutory Nature
# Parameter(s) : Object of database, nature id, nature name, country id, user id
# Return Type : Return updated value of statutory nature
######################################################################################
def update_statutory_nature(db, nature_id, nature_name, country_id, user_id):
    oldData = get_nature_by_id(db, nature_id)
    if oldData is None:
        return False

    values = [nature_id, nature_name, country_id, user_id]
    new_id = db.call_update_proc("sp_statutory_nature_updatestatutorynature", values)

    if new_id is True:
        msg_text = "Statutory Nature \"" + oldData + "\" Updated as \"" + nature_name + "\""
        u_cg_id = [3, 4, 5, 6, 7, 8]
        for cg_id in u_cg_id:
            users_id = []
            result = db.call_proc("sp_users_under_user_category", (cg_id,))
            for user in result:
                users_id.append(user["user_id"])
            if len(users_id) > 0:
                db.save_toast_messages(cg_id, "Statutory Nature Updated", msg_text, None, users_id, user_id)
        action = "Statutory Nature '%s' updated" % (nature_name)
        db.save_activity(user_id, frmStatutoryNatureMaster, action)
        return True
    else:
        raise process_error("E005")

######################################################################################
# To update Statutory Nature status
# Parameter(s) : Object of database, nature id, status, user id
# Return Type : Return value of the updated statutory nature status
######################################################################################
def update_statutory_nature_status(db, nature_id, is_active, user_id):
    oldData = get_nature_by_id(db, nature_id)
    if oldData is None:
        return False
    values = [nature_id, user_id, is_active]
    new_id = db.call_update_proc("sp_statutory_nature_updatestatutorynaturestatus", values)
    if new_id is True:
        if is_active == 0:
            status = "deactivated"
            msg_text = "Statutory Nature \"" + oldData + "\" Deactivated "
        else:
            status = "activated"
            msg_text = "Statutory Nature \"" + oldData + "\" Activated "
        u_cg_id = [3, 4, 5, 7, 8]
        for cg_id in u_cg_id:
            users_id = []
            result = db.call_proc("sp_users_under_user_category", (cg_id,))
            for user in result:
                users_id.append(user["user_id"])
            if len(users_id) > 0:
                db.save_toast_messages(cg_id, "Statutory Nature Status Updated", msg_text, None, users_id, user_id)
        action = "Statutory nature %s status  - %s" % (oldData, status)
        db.save_activity(user_id, frmStatutoryNatureMaster, action)
        return True
    else:
        raise process_error("E006")

######################################################################################
# To Get Statutory Level
# Parameter(s) : Object of database
# Return Type : Return list of statutory levels
######################################################################################
def get_statutory_levels(db):
    result = db.call_proc("sp_get_statutory_level_master", ())
    return return_statutory_levels(result)


def return_statutory_levels(data):
    statutory_levels = {}
    for d in data:
        country_id = d["country_id"]
        domain_id = d["domain_id"]
        levels = core.Level(
            d["level_id"], d["level_position"], d["level_name"]
        )
        country_wise = statutory_levels.get(country_id)
        _list = []
        if country_wise is None:
            country_wise = {}
        else:
            _list = country_wise.get(domain_id)
            if _list is None:
                _list = []
        _list.append(levels)
        country_wise[domain_id] = _list
        statutory_levels[country_id] = country_wise
    return statutory_levels


def delete_statutory_level(db, level_id):
    row = db.call_proc("sp_get_statutory_level_count", (level_id,))
    if row[0]['cnt'] > 0:
        return True
    else:
        res = db.call_proc(
            "sp_delete_statutory_level", [level_id]
        )
        if res is False:
            raise process_error("E009")


def save_statutory_levels(db, country_id, domain_id, levels, user_id):
    table_name = "tbl_statutory_levels"
    created_on = get_date_time()
    newlist = sorted(levels, key=lambda k: k.level_position, reverse=True)
    result = False
    s_l_id = None
    for n in newlist:
        if n.is_remove is True:
            result = delete_statutory_level(db, n.level_id)
            if result:
                s_l_id = n.level_position
                break
            else:
                continue
    if result:
        return knowledgemaster.LevelShouldNotbeEmpty(s_l_id)

    for level in levels:
        name = level.level_name
        position = level.level_position
        values = []
        if level.is_remove:
            continue

        if level.level_id is None:
            columns = [
                "level_position", "level_name",
                "country_id", "domain_id", "created_by", "created_on"]
            values = [
                int(country_id), int(domain_id),
                position, name, int(user_id), str(created_on)
            ]
            new_id = db.call_insert_proc("sp_insert_statutory_level", values)
            if new_id is not False:
                c_name = get_country_by_id(db, country_id)
                d_name = get_domain_by_id(db, domain_id)
                msg_text = "Statutory Level \"" + name + "\" is inserted under Country - "+c_name+" ,Domain - "+d_name
                u_cg_id = [3, 4, 5, 7]
                for cg_id in u_cg_id:
                    users_id = []
                    result = db.call_proc("sp_users_under_user_category", (cg_id,))
                    for user in result:
                        users_id.append(user["user_id"])
                    if len(users_id) > 0:
                        db.save_toast_messages(cg_id, "Statutory Level Added", msg_text, None, users_id, user_id)
                action = "New Statutory levels added"
                db.save_activity(user_id, frmStatutoryLevelMaster, action)
            else:
                raise process_error("E007")
        else:
            values = [position, name, level.level_id, user_id]
            if (
                db.call_update_proc(
                    "sp_update_statutory_levels", values
                )
            ):
                c_name = get_country_by_id(db, country_id)
                d_name = get_domain_by_id(db, domain_id)
                msg_text = "Statutory Level \"" + name + "\" is inserted under Country - "+c_name+" ,Domain - "+d_name
                u_cg_id = [3, 4, 5, 7]
                for cg_id in u_cg_id:
                    users_id = []
                    result = db.call_proc("sp_users_under_user_category", (cg_id,))
                    for user in result:
                        users_id.append(user["user_id"])
                    if len(users_id) > 0:
                        db.save_toast_messages(cg_id, "Statutory Level Updated", msg_text, None, users_id, user_id)
                action = "Statutory levels updated"
                db.save_activity(user_id, frmStatutoryLevelMaster, action)
            else:
                raise process_error("E008")
    return knowledgemaster.SaveStatutoryLevelSuccess()


def get_geography_levels(db):
    result = db.call_proc("sp_get_geography_levels", ())
    geography_levels = {}
    for d in result :
        country_id = d["country_id"]
        level = core.GeographyLevel(
            d["level_id"], d["level_position"], d["level_name"]
        )
        _list = geography_levels.get(country_id)
        if _list is None:
            _list = []
        _list.append(level)
        geography_levels[country_id] = _list
    return geography_levels

def return_geography_levels(data):
    geography_levels = []
    for d in data:
        #country_id = d["country_id"]
        level = core.UnitGeographyLevel(
            d["level_id"], d["level_position"], d["level_name"], d["country_id"]
        )
        #_list = geography_levels.get(country_id)
        #if _list is None:
        #    _list = []
        #_list.append(level)
        #geography_levels[country_id] = _list
        geography_levels.append(level)
    return geography_levels

def get_geograhpy_levels_for_user(db, user_id):
    assert user_id is not None
    condition_val = [user_id]

    result = db.call_proc(
        "sp_geography_levels_getlevelsforusers", (condition_val,)
    )
    return return_geography_levels(result)


def delete_grography_level(db, level_id):
    q = db.call_proc("sp_check_level_in_geographies", (level_id,))
    if q[0]['cnt'] > 0:
        return True
    else:
        res = db.call_proc("sp_delete_geographylevel", (level_id,))
        if res is False :
            raise process_error("E009")


def save_geography_levels(db, country_id, levels, insertValText, user_id):
    table_name = "tbl_geography_levels"
    created_on = get_date_time()
    newlist = sorted(levels, key=lambda k: k.level_position, reverse=True)
    result = False
    d_l_id = None
    for n in newlist:
        if n.is_remove is True:
            result = delete_grography_level(db, n.level_id)
            if result :
                d_l_id = n.level_position
                break
            else:
                continue
    if result :
        return knowledgemaster.LevelShouldNotbeEmpty(d_l_id)

    for level in sorted(levels, key=lambda k: k.level_id, reverse=True):
        name = level.level_name
        position = level.level_position
        if level.is_remove :
            continue

        if level.level_id is not None:
            values = [level.level_id, name, position, user_id]
            if (
                db.call_update_proc(
                    "sp_update_geographylevel_master", values
                )
            ):
                action = "Geography levels updated"
                db.save_activity(user_id, frmGeographyLevelMaster, action)
            else:
                raise process_error("E011")

        else :
            values = [
                name, position, int(country_id),
                int(user_id), str(created_on)
            ]
            new_id = db.call_insert_proc("sp_save_geographylevel_master", values)
            if new_id is not False:
                action = "New Geography levels added"
                db.save_activity(user_id, frmGeographyLevelMaster, action)
            else:
                raise process_error("E010")

    if insertValText is not None:
        if insertValText.find(",") >= 0:
            u_cg_id = [3, 4, 5, 6]
            for cg_id in u_cg_id:
                users_id = []
                result = db.call_proc("sp_users_under_user_category", (cg_id,))
                for user in result:
                    users_id.append(user["user_id"])
                if len(users_id) > 0:
                    split_text = insertValText.split(",")
                    for s_text in split_text:
                        if s_text is not None and s_text != "null":
                            db.save_toast_messages(cg_id, "Geography Level Inserted", s_text, None, users_id, user_id)
        else:
            u_cg_id = [3, 4, 5, 6]
            for cg_id in u_cg_id:
                users_id = []
                result = db.call_proc("sp_users_under_user_category", (cg_id,))
                for user in result:
                    users_id.append(user["user_id"])
                if len(users_id) > 0:
                    db.save_toast_messages(cg_id, "Geography Level Inserted", insertValText, None, users_id, user_id)

    return knowledgemaster.SaveGeographyLevelSuccess()


def get_geographies(db, user_id=None, country_id=None):
    if country_id:
        result = db.call_proc("sp_geographymaster_geographies_list", (country_id, ))
    else:
        result = db.call_proc("sp_geographymaster_geographies_list", (None, ))
    frame_geography_parent_mapping(result)
    return return_geographies(result)


def return_geographies(data):
    geographies = {}
    for d in data:
        parent_ids = [int(x) for x in d["parent_ids"][:-1].split(',')]
        geography = core.Geography(
            d["geography_id"], d["geography_name"],
            d["level_id"], parent_ids, parent_ids[-1],
            bool(d["is_active"])
        )
        country_id = d["country_id"]
        _list = geographies.get(country_id)
        if _list is None:
            _list = []
        _list.append(geography)
        geographies[country_id] = _list
    return geographies


def get_geographies_for_user_with_mapping(db, user_id):

    where_condition_val = [user_id]
    result = db.call_proc("sp_get_geographies_for_users_mapping", (where_condition_val,))

    geographies = []
    if result:
        for d in result:
            parent_ids = [int(x) for x in d["parent_ids"][:-1].split(',')]
            geography = core.UnitGeographyMapping(
                d["geography_id"], d["geography_name"],
                d["level_id"],
                d["parent_names"],
                parent_ids,
                d["country_id"],
                bool(d["is_active"])
            )
            #country_id = d["country_id"]
            #_list = geographies.get(country_id)
            #if _list is None:
            #    _list = []
            #_list.append(geography)
            #geographies[country_id] = _list
            geographies.append(geography)
    return geographies


def get_geography_by_id(db, geography_id):
    result = db.call_proc("sp_get_geography_by_id", [geography_id])
    return result


def check_duplicate_geography(db, country_id, parent_ids, geography_id):
    query = "SELECT t1.geography_id, t1.geography_name, " + \
        " t1.level_id, t1.is_active " + \
        " FROM tbl_geographies t1 " + \
        " INNER JOIN tbl_geography_levels t2 " + \
        " ON t1.level_id = t2.level_id " + \
        " WHERE t1.parent_ids= %s " + \
        " AND t2.country_id = %s "
    if geography_id is not None:
        query = query + " AND geography_id != %s"
        param = (parent_ids, country_id, geography_id)
    else:
        param = (parent_ids, country_id)

    rows = db.select_all(query, param)
    # columns = ["geography_id", "geography_name", "level_id", "is_active"]
    # result = []

    return rows

def notify_geography_actions(db, action, geo_id, parent_ids, parent_names, proc_type, user_category_ids, session_user):
    if proc_type == 0 :
        title = "Geography Added"
    elif proc_type == 1 :
        title = "Geography Updated"
    else :
        title = "Geography Status Update"

    for cg_id in user_category_ids:
        users_id = []
        result = db.call_proc_with_multiresult_set("sp_get_country_based_users", [geo_id, cg_id, 0, parent_ids], 2)
        for user in result[0]:
            users_id.append(user["user_id"])

        levels = result[1]
        xaction = ""
        if levels :
            for i, x in enumerate(parent_names.split(">>")[:-1]) :

                if i == 0 :
                    xaction += " Country - %s," % (x.strip())
                else :
                    xaction += " %s - %s," % (levels[i-1]["level_name"], x.strip())

        if xaction != "" :
            action += " under %s " % (xaction)

        if len(users_id) > 0:
            db.save_toast_messages(cg_id, title, action, None, users_id, session_user)

    db.save_activity(session_user, frmGeographyMaster, action)

def save_geography(
    db, geography_level_id, geography_name, parent_ids, parent_names, user_id
):
    created_on = get_date_time()
    values = [
        geography_name, int(geography_level_id),
        parent_ids, parent_names, int(user_id), str(created_on)
    ]

    new_id = db.call_insert_proc("sp_save_geography_master", values)
    if new_id is False:
        raise process_error("E012")
    else:
        action = "Geography name %s added " % (geography_name)
        notify_geography_actions(db, action, geography_level_id, parent_ids, parent_names, 0, [3, 5, 7], user_id)
        return True


def update_geography(
    db, geography_id, name, parent_ids, parent_names, updated_by
):
    oldData = get_geography_by_id(db, geography_id)

    if bool(oldData) is False:
        return False
    values = [geography_id, name, parent_ids, parent_names, updated_by]
    if (db.call_update_proc("sp_update_geography_master", values)):
        action = "Geography name %s updated " % (name)
        notify_geography_actions(db, action, geography_id, parent_ids, parent_names, 1, [3, 4, 5, 6, 7], updated_by)

        if len(parent_ids[:-1]) == 1:
            p_ids = parent_ids[:-1]
        else:
            p_ids = None
            i = 0
            p_new_id = parent_ids[:-1].split(',')
            for p_ids_len in p_new_id:
                if p_ids is None:
                    p_ids = p_ids_len + ","
                else:
                    p_ids = p_ids + p_ids_len
                i = i + 1
        result = db.call_proc("sp_get_geography_master", [geography_id, p_ids])

        for row in result:
            map_name = row["parent_names"] + " >> " + row["geography_name"]

            db.call_update_proc("sp_update_geographies_master_level", (
                row["geography_id"],
                row["level_id"], map_name
            ))
        return True
    else:
        raise process_error("E013")

def check_geography_exists(db, geography_id):
    #
    # if geography used in mapping means return true else return false
    # and geography has child means return true else false
    #
    is_exists = False
    row = db.call_proc_with_multiresult_set("sp_check_geography_exists", [geography_id], 2)
    if row[0] > 0 :
        is_exists = True
        raise process_error("E063")

    if is_exists is False :
        if r[1] > 0 :
            is_exists = True
            raise process_error("E064")

    # return is_exists


def change_geography_status(db, geography_id, is_active, updated_by):
    oldData = get_geography_by_id(db, geography_id)

    if bool(oldData) is False:
        return False
    # if is_active == 0 :
    #     check_geography_exists(db, geography_id)

    values = [geography_id, is_active, updated_by]

    if (db.call_update_proc("sp_geography_update_status", values)):

        if is_active == 0:
            status = "deactivated"
        else:
            status = "activated"
        action = "Geography %s status - %s" % (
            oldData[0]["geography_name"], status
        )
        parent_ids = oldData[0]["parent_ids"]
        parent_names = oldData[0]["parent_names"]
        notify_geography_actions(db, action, geography_id, parent_ids, parent_names, 2, [3, 4, 5, 6, 7, 8], updated_by)
        db.save_activity(updated_by, frmGeographyMaster, action)
        return True
    else:
        raise process_error("E014")


def get_statutory_by_id(db, statutory_id):
    query = "SELECT statutory_id, statutory_name, " + \
        " level_id, parent_ids, parent_names " + \
        " FROM tbl_statutories WHERE statutory_id = %s"
    result = db.select_one(query, [statutory_id])

    return result


def save_statutory(db, name, level_id, parent_ids, parent_names, user_id):
    table_name = "tbl_statutories"
    created_on = get_date_time()
    columns = [
        "statutory_name", "level_id", "parent_ids", "parent_names",
        "created_by", "created_on"
    ]
    values = [
        name, int(level_id),
        parent_ids, parent_names, int(user_id), str(created_on)
    ]

    new_id = db.insert(table_name, columns, values)
    if new_id is False:
        raise process_error("E015")
    else:
        action = "Statutory - %s added" % name
        db.save_activity(user_id, frmStatutoryMapping, action)
        return True


def update_statutory(
    db, statutory_id, name, updated_by
):
    oldData = get_statutory_by_id(db, statutory_id)
    if bool(oldData) is False:
        return False

    table_name = "tbl_statutories"
    columns = [
        "statutory_name",
        "updated_by"
    ]
    where_condition = " statutory_id = %s"
    values = [name, str(updated_by), statutory_id]
    if (db.update(table_name, columns, values, where_condition)):
        action = "Statutory - %s updated" % name
        db.save_activity(updated_by, frmStatutoryMapping, action)
        qry = "SELECT statutory_id, statutory_name, parent_ids " + \
            " from tbl_statutories " + \
            " WHERE find_in_set(%s, parent_ids)"
        result = db.select_all(qry, [statutory_id])

        for row in result:
            if row["parent_ids"] == "0,":
                row["parent_ids"] = statutory_id
            else:
                row["parent_ids"] = row["parent_ids"][:-1]
            pids = [int(x) for x in row["parent_ids"].split(',')]
            pids.append(0)
            pids = tuple(pids)

            q = "Update tbl_statutories as A inner join ( " + \
                " select p.statutory_id, (select " + \
                " group_concat(p1.statutory_name SEPARATOR '>>') " + \
                " from tbl_statutories as p1 where statutory_id in (" + row["parent_ids"] + ")) " + \
                " as names from tbl_statutories as p " + \
                " where p.statutory_id = %s " + \
                " ) as B on A.statutory_id = B.statutory_id " + \
                " set A.parent_names = B.names " + \
                " where A.statutory_id = %s "

            db.execute(q, [row["statutory_id"], row["statutory_id"]])
            action = "statutory name %s updated in child rows." % name
            db.save_activity(updated_by, frmStatutoryMapping, action)
        return True

    else:
        raise process_error("E016")


def get_statutory_master(db, statutory_id=None):
    result = db.call_proc("sp_statutorymapping_report_statutorymaster", (statutory_id,))

    frame_parent_mappings(db, result, statutory_id)
    return return_statutory_master(result)


def frame_parent_mappings(db, data, statutory_id=None):
    # data = db.call_proc("sp_statutorymapping_report_statutorymaster", (statutory_id,))

    statu_names = {}

    for d in data:
        statu_names[d["statutory_id"]] = d["statutory_name"]

    for d in data:
        p_ids = d["parent_ids"]
        p_ids = [
            int(x) for x in d["parent_ids"][:-1].split(',')
        ]

        names = []
        for pid in p_ids:
            if pid > 0:
                if(statu_names.get(pid) == None):  # mangesh
                    names.append("---")
                else:
                    names.append(statu_names.get(pid))
        names.append(d["statutory_name"])

        STATUTORY_PARENTS[d["statutory_id"]] = [
            d["statutory_name"], ">> ".join(names), p_ids
        ]


def return_statutory_master(data):
    statutories = {}

    for d in data:
        country_id = d["country_id"]
        domain_id = d["domain_id"]
        statutory_id = int(d["statutory_id"])
        mappings = STATUTORY_PARENTS.get(
            statutory_id
        )
        if d["parent_ids"] is not None:
            parent_ids = [
                int(x) for x in d["parent_ids"][:-1].split(',')
            ]
            statutory = core.Statutory(
                statutory_id, d["statutory_name"],
                d["level_id"], parent_ids, parent_ids[-1],
                mappings[1]
            )
        else:
            parent_ids = None
            statutory = core.Statutory(
                statutory_id, d["statutory_name"],
                d["level_id"], parent_ids, None,
                mappings[1]
            )

        statutory = core.Statutory(
            statutory_id, d["statutory_name"],
            d["level_id"], parent_ids, parent_ids[-1],
            mappings[1]
        )

        country_wise = statutories.get(country_id)
        _list = []
        if country_wise is None:
            country_wise = {}
        else:
            _list = country_wise.get(domain_id)
            if _list is None:
                _list = []
        _list.append(statutory)
        country_wise[domain_id] = _list
        statutories[country_id] = country_wise
    return statutories


def check_duplicate_statutory(
    db, parent_ids, statutory_id, domain_id=None, country_id=None
):
    query = "SELECT T1.statutory_id, T1.statutory_name, " + \
        " T1.level_id, T2.domain_id " + \
        " FROM tbl_statutories T1 " + \
        " INNER JOIN tbl_statutory_levels T2 " + \
        " ON T1.level_id = T2.level_id " + \
        " WHERE T1.parent_ids= %s"
    where_qry = ""
    param = [parent_ids]
    if statutory_id is not None:
        where_qry += " AND T1.statutory_id != %s"
        param.append(statutory_id)

    if domain_id is not None:
        where_qry += " AND domain_id = %s"
        param.append(domain_id)

    if country_id is not None :
        where_qry += " AND country_id = %s"
        param.append(country_id)

    rows = db.select_all(query + where_qry, param)
    return rows


def get_country_wise_level_1_statutoy(db, user_id):
    result = db.call_proc("sp_statutorymapping_report_levl1_list", ())

    if bool(STATUTORY_PARENTS) is False:
        get_statutory_master(db)

    return return_statutory_master(result)


#
# frame geography parent mapping
#
def frame_geography_parent_mapping(rows):
    for row in rows:
        country_id = int(row["country_id"])
        geography_id = int(row["geography_id"])
        is_active = bool(row["is_active"])
        mappings = row["parent_names"]
        GEOGRAPHY_PARENTS[geography_id] = [
            mappings, is_active, country_id
        ]
