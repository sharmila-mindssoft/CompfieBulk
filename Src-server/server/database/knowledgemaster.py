from protocol import (
    core, knowledgemaster
)
from server.exceptionmessage import *
from server.common import (
    convert_to_dict, get_date_time, convert_to_key_dict
)
from server.database.tables import *

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


def get_industries(db):
    columns = [
        "country_id", "country_name",
        "domain_id", "domain_name",
        "industry_id", "industry_name",
        "is_active"
    ]
    result = db.call_proc("sp_industry_master_getindustries", (), columns)
    return return_industry(result)

def get_industry_by_id(db, industry_id):
    if type(industry_id) is int:
        values_list = [industry_id]
    else:
        values_list = industry_id
    row = db.call_proc("sp_industry_master_getindusdtrybyid", values_list)

    industry_names = []
    for r in row:
        industry_names.append(r["industry_name"])

    return ", ".join(industry_names)

## stored procedure not created
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
    print "result"
    print result
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


def check_duplicate_industry(db, industry_name, industry_id):
    isDuplicate = False

    if industry_id is not None:
        param = [industry_id, industry_name]
    else:
        param = [0, industry_name]

    row = db.call_proc("sp_industry_master_checkduplicateindustry", param)
    for r in row:
        if int(r["count(1)"]) > 0:
            isDuplicate = True

    return isDuplicate


def save_industry(db, country_ids, domain_ids, industry_name, user_id):
    # table_name = "tbl_industries"
    created_on = get_date_time()
    # columns = ["country_id", "domain_id", "industry_name", "created_by", "created_on"]
    values = [country_ids, domain_ids, industry_name, str(user_id), str(created_on)]
    new_id = db.call_insert_proc("sp_industry_master_saveindustry", values)
    print new_id
    if new_id is False:
        raise process_error("E001")
    else:
        action = "New Industry type %s added" % (industry_name)
        db.save_activity(user_id, 7, action)
        return True


def update_industry(db, country_ids, domain_ids, industry_id, industry_name, user_id):
    new_id = False
    oldData = get_industry_by_id(db, industry_id)
    print oldData
    if oldData is None:
        return False
    columns = ["industry_id", "industry_name", "country_id", "domain_id", "created_by"]
    values = [industry_id, industry_name, country_ids, domain_ids, str(user_id)]
    new_id = db.call_update_proc("sp_industry_master_updateindustry", values)
    print new_id
    print "new_id"
    if new_id is True:
        action = "Industry type %s updated" % (industry_name)
        db.save_activity(user_id, 7, action)
        return True
    else:
        raise process_error("E002")


def update_industry_status(db, industry_id, is_active, user_id):
    oldData = get_industry_by_id(db, industry_id)
    if oldData is None:
        return False
    values = [industry_id, is_active, user_id]
    new_id = db.call_update_proc("sp_industry_master_updatestatus", values)
    print new_id
    if new_id is True:
        if is_active == 0:
            status = "deactivated"
        else:
            status = "activated"

        action = "Industry type %s status - %s" % (oldData, status)
        db.save_activity(user_id, 7, action)
        return True
    else:
        raise process_error("E003")


def get_nature_by_id(db, nature_id):
    if type(nature_id) is int:
        values_list = [nature_id]
    else:
        values_list = nature_id
    row = db.call_proc("sp_statutory_natures_getnaturebyid", values_list)
    nature_name = None
    for r in row:
        nature_name = r["statutory_nature_name"]
        print nature_name
    return nature_name


def get_statutory_nature(db):
    columns = [
        "statutory_nature_id", "statutory_nature_name", "country_id", "country_name",
        "is_active"
    ]

    result = db.call_proc("sp_statutory_nature_getstatutorynatures",(), columns)
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


def check_duplicate_statutory_nature(db, nature_name, nature_id):
    isDuplicate = False
    if nature_id is not None:
        param = [nature_name, nature_id]
    else:
        param = [nature_name, 0]
    row = db.call_proc("sp_statutory_nature_checkduplicatenature", param)

    for r in row:
        if r["cnt"] > 0:
            isDuplicate = True
    return isDuplicate


def save_statutory_nature(db, nature_name, country_id, user_id):
    created_on = get_date_time()
    columns = ["statutory_nature_name", "country_id", "created_by", "created_on"]
    values = [nature_name, country_id, user_id, str(created_on)]
    new_id = db.call_insert_proc("sp_statutorynature_savestatutorynature", values)
    if new_id is False:
        raise process_error("E004")
    else:
        action = "New Statutory Nature %s added" % (nature_name)
        db.save_activity(user_id, 8, action)
        return True


def update_statutory_nature(db, nature_id, nature_name, country_id, user_id):
    oldData = get_nature_by_id(db, nature_id)
    if oldData is None:
        return False

    values = [nature_id, nature_name, country_id, user_id]
    new_id = db.call_update_proc("sp_statutory_nature_updatestatutorynature", values)

    if new_id is True:
        action = "Statutory Nature '%s' updated" % (nature_name)
        db.save_activity(user_id, 8, action)
        return True
    else:
        raise process_error("E005")


def update_statutory_nature_status(db, nature_id, is_active, user_id):
    oldData = get_nature_by_id(db, nature_id)
    if oldData is None:
        return False
    values = [nature_id, user_id, is_active]
    new_id = db.call_update_proc("sp_statutory_nature_updatestatutorynaturestatus", values)
    if new_id is True:
        if is_active == 0:
            status = "deactivated"
        else:
            status = "activated"

        action = "Statutory nature %s status  - %s" % (oldData, status)
        db.save_activity(user_id, 8, action)
        return True
    else:
        raise process_error("E006")


def get_statutory_levels(db):
    columns = [
        "level_id", "level_position", "level_name",
        "country_id", "domain_id"
    ]
    condition = " 1 ORDER BY level_position"
    result = db.get_data("tbl_statutory_levels", columns, condition)
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
    q = "select count(*) from tbl_statutories where level_id = %s"
    row = db.select_one(q, [level_id])
    if row[0] > 0:
        return True
    else:
        res = db.execute(
            "delete from tbl_statutory_levels where level_id = %s ", [level_id]
        )
        if res is False :
            raise process_error("E009")

def save_statutory_levels(db, country_id, domain_id, levels, user_id):
    table_name = "tbl_statutory_levels"
    created_on = get_date_time()
    newlist = sorted(levels, key=lambda k: k.level_position, reverse=True)
    result = False
    s_l_id = None
    for n in newlist :
        if n.is_remove is True :
            result = delete_statutory_level(db, n.level_id)
            if result :
                s_l_id = n.level_position
                break
            else :
                continue
    if result :
        return knowledgemaster.LevelShouldNotbeEmpty(s_l_id)

    for level in levels:
        name = level.level_name
        position = level.level_position
        values = []
        if level.is_remove :
            continue

        if level.level_id is None:
            columns = [
                "level_position", "level_name",
                "country_id", "domain_id", "created_by", "created_on"]
            values = [
                position, name,
                int(country_id),
                int(domain_id), int(user_id), str(created_on)
            ]
            new_id = db.insert(table_name, columns, values)
            if new_id is not False:
                action = "New Statutory levels added"
                db.save_activity(user_id, 9, action)
            else:
                raise process_error("E007")
        else:
            columns = ["level_position", "level_name", "updated_by"]
            where_condition = "level_id = %s "
            values = [position, name, user_id, level.level_id]
            if (
                db.update(
                    table_name, columns, values, where_condition
                )
            ):
                action = "Statutory levels updated"
                db.save_activity(user_id, 9, action)
            else:
                raise process_error("E008")
    return knowledgemaster.SaveStatutoryLevelSuccess()


def get_geography_levels(db):
    columns = [
        "level_id", "level_position", "level_name", "country_id"
    ]
    condition = " 1 ORDER BY level_position"
    result = db.get_data("tbl_geography_levels", columns, condition)

    return return_geography_levels(result)


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
    q = "select count(*) from tbl_geographies where level_id = %s"
    row = db.select_one(q, [level_id])
    if row[0] > 0:
        return True
    else:
        res = db.execute(
            "delete from tbl_geography_levels where level_id = %s ", [level_id]
        )
        if res is False :
            raise process_error("E009")


def save_geography_levels(db, country_id, levels, user_id):
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
            columns = [
                "level_position", "level_name", "updated_by",
            ]
            where_condition = "level_id=%s"
            values = [position, name, user_id, level.level_id]
            if (
                db.update(
                    table_name, columns, values, where_condition
                )
            ):
                action = "Geography levels updated"
                db.save_activity(user_id, 5, action)
            else:
                raise process_error("E011")

        else :
            columns = [
                "level_position", "level_name", "country_id",
                "created_by", "created_on"
            ]
            values = [
                position, name, int(country_id),
                int(user_id), str(created_on)
            ]
            new_id = db.insert(table_name, columns, values)
            if new_id is not False:
                action = "New Geography levels added"
                db.save_activity(user_id, 5, action)
            else:
                raise process_error("E010")

    return knowledgemaster.SaveGeographyLevelSuccess()


def get_geographies(db, user_id=None, country_id=None):
    query = "SELECT distinct t1.geography_id, " + \
        " t1.geography_name, " + \
        " t1.level_id, " + \
        " t1.parent_ids, t1.is_active, " + \
        " t2.country_id, " + \
        " (select country_name from tbl_countries where " + \
        " country_id = t2.country_id)as country_name, " + \
        " t2.level_position, t1.parent_names " + \
        " FROM tbl_geographies t1 " + \
        " INNER JOIN tbl_geography_levels t2 " + \
        " on t1.level_id = t2.level_id " + \
        " INNER JOIN tbl_user_countries t4 " + \
        " ON t2.country_id = t4.country_id "
    param = []
    if user_id:
        query = query + " AND t4.user_id=%s"
        param.append(user_id)
    if country_id:
        query = query + " AND t2.country_id=%s"
        param.append(country_id)

    query = query + " ORDER BY country_name, level_position, geography_name"
    if len(param) > 0:
        rows = db.select_all(query, param)
    else:
        rows = db.select_all(query)

    result = []
    if rows:
        columns = [
            "geography_id", "geography_name", "level_id",
            "parent_ids", "is_active", "country_id", "country_name",
            "level_position", "parent_names"
        ]
        result = convert_to_dict(rows, columns)
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
    query = "SELECT geography_id, geography_name, " +\
        " level_id, parent_ids, parent_names, is_active " + \
        " FROM tbl_geographies WHERE geography_id = %s"
    rows = db.select_one(query, [geography_id])
    result = []
    if rows:
        columns = [
            "geography_id", "geography_name",
            "level_id", "parent_ids", "parent_names", "is_active"
        ]
        result = convert_to_dict(rows, columns)
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
    columns = ["geography_id", "geography_name", "level_id", "is_active"]
    result = []
    if rows:
        result = convert_to_dict(rows, columns)
    return result


def save_geography(
    db, geography_level_id, geography_name, parent_ids, parent_names, user_id
):
    table_name = "tbl_geographies"
    created_on = get_date_time()
    columns = [
        "geography_name", "level_id", "parent_ids", "parent_names",
        "created_by", "created_on"
    ]
    values = [
        geography_name, int(geography_level_id),
        parent_ids, parent_names, int(user_id), str(created_on)
    ]

    new_id = db.insert(table_name, columns, values)
    if new_id is False:
        raise process_error("E012")
    else:
        action = "New Geography %s added" % (geography_name)
        db.save_activity(user_id, 6, action)
        return True


def update_geography(
    db, geography_id, name, parent_ids, parent_names, updated_by
):
    oldData = get_geography_by_id(db, geography_id)
    if bool(oldData) is False:
        return False
    table_name = "tbl_geographies"
    columns = [
        "geography_name", "parent_ids", "parent_names",
        "updated_by"
    ]
    where_condition = " geography_id = %s "
    values = [name, parent_ids, parent_names, updated_by, geography_id]
    if (db.update(table_name, columns, values, where_condition)):
        action = "Geography - %s updated" % name
        db.save_activity(updated_by, 6, action)
        if len(parent_ids[:-1]) == 1 :
            p_ids = tuple([parent_ids[:-1], geography_id])
        else :
            p_ids = parent_ids[:-1].split(',')
            p_ids.append(geography_id)
            p_ids = tuple(p_ids)
        qry = "SELECT geography_id, geography_name, parent_ids, level_id " + \
            " from tbl_geographies " + \
            " WHERE find_in_set( %s, parent_ids) or geography_id in %s"
        rows = db.select_all(qry, [geography_id, p_ids])
        columns = ["geography_id", "geography_name", "parent_ids", "level_id"]
        result = convert_to_key_dict(rows, columns)

        for key, row in result.items():
            if int(key) == geography_id :
                continue
            if row["parent_ids"] == "0,":
                row["parent_ids"] = tuple([geography_id, 0])
                map_name = name
            else:
                map_name = ""
                x = row["parent_ids"].strip().split(',')
                for j in x[:-1]:
                    if int(j) == int(geography_id) :
                        map_name += name + " >> "
                    else :
                        map_name += result[int(j)]["geography_name"] + " >> "
                row["parent_ids"] = tuple(x[:-1])

            map_name += row["geography_name"]

            q = "UPDATE tbl_geographies as A inner join ( " + \
                " select c.country_name, g.level_id from  " + \
                " tbl_countries c inner join tbl_geography_levels g on " + \
                " c.country_id = g.country_id ) as C  " + \
                " ON A.level_id  = C.level_id " + \
                " set A.parent_names = concat( " + \
                " C.country_name, '>>', %s) " + \
                " where A.geography_id = %s AND C.level_id = %s "

            db.execute(q, (
                map_name, row["geography_id"],
                row["level_id"]
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
    q = "select count(1) from tbl_statutory_geographies where geography_id = %s"
    row = db.select_one(q, [geography_id])
    if row[0] > 0 :
        is_exists = True
        raise process_error("E063")

    if is_exists is False :
        q1 = "select count(0) from tbl_geographies where FIND_IN_SET(%s, parent_ids)"
        r = db.select_one(q1, [geography_id])
        if r[0] > 0 :
            is_exists = True
            raise process_error("E064")

    # return is_exists


def change_geography_status(db, geography_id, is_active, updated_by):
    oldData = get_geography_by_id(db, geography_id)
    if bool(oldData) is False:
        return False
    table_name = "tbl_geographies"
    columns = ["is_active", "updated_by"]
    where_condition = " geography_id = %s"
    # if is_active == 0 :
    #     check_geography_exists(db, geography_id)

    values = [is_active, updated_by, geography_id]
    if (db.update(table_name, columns, values, where_condition)):
        if is_active == 0:
            status = "deactivated"
        else:
            status = "activated"
        action = "Geography %s status - %s" % (
            oldData["geography_name"], status
        )
        db.save_activity(updated_by, 6, action)
        return True
    else:
        raise process_error("E014")


def get_statutory_by_id(db, statutory_id):
    query = "SELECT statutory_id, statutory_name, " + \
        " level_id, parent_ids, parent_names " + \
        " FROM tbl_statutories WHERE statutory_id = %s"
    rows = db.select_one(query, [statutory_id])
    result = []
    if rows:
        columns = [
            "statutory_id", "statutory_name",
            "level_id", "parent_ids", "parent_names"
        ]
        result = convert_to_dict(rows, columns)
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
        db.save_activity(user_id, 10, action)
        return True


def update_statutory(
    db, statutory_id, name, parent_ids, parent_names, updated_by
):
    oldData = get_statutory_by_id(db, statutory_id)
    if bool(oldData) is False:
        return False

    table_name = "tbl_statutories"
    columns = [
        "statutory_name", "parent_ids", "parent_names",
        "updated_by"
    ]
    where_condition = " statutory_id = %s"
    values = [name, parent_ids, parent_names, str(updated_by), statutory_id]
    if (db.update(table_name, columns, values, where_condition)):
        action = "Statutory - %s updated" % name
        db.save_activity(updated_by, 10, action)
        qry = "SELECT statutory_id, statutory_name, parent_ids " + \
            " from tbl_statutories " + \
            " WHERE parent_ids like %s"
        rows = db.select_all(qry, [str("%" + str(statutory_id) + ",%")])
        columns = ["statutory_id", "statutory_name", "parent_ids"]
        result = convert_to_dict(rows, columns)
        for row in result:
            if row["parent_ids"] == "0,":
                row["parent_ids"] = statutory_id
            else:
                row["parent_ids"] = row["parent_ids"][:-1]

            q = "Update tbl_statutories as A inner join ( " + \
                " select p.statutory_id, (select " + \
                " group_concat(p1.statutory_name SEPARATOR '>>') " + \
                " from tbl_statutories as p1 where statutory_id in (%s)) " + \
                " as names from tbl_statutories as p " + \
                " where p.statutory_id = %s " + \
                " ) as B on A.statutory_id = B.statutory_id " + \
                " set A.parent_names = B.names " + \
                " where A.statutory_id = %s "
            db.execute(
                q, (
                    row["parent_ids"], row["statutory_id"],
                    row["statutory_id"]
                )
            )
            action = "statutory name %s updated in child rows." % name
            db.save_activity(updated_by, 10, action)
        return True
    else:
        raise process_error("E016")


def get_statutory_master(db, statutory_id=None):
    columns = [
        "statutory_id", "statutory_name",
        "level_id", "parent_ids",
        "country_id", "country_name",
        "domain_id", "domain_name"
    ]
    query = "SELECT t1.statutory_id, t1.statutory_name, " + \
        " t1.level_id, t1.parent_ids, t2.country_id, " + \
        " t3.country_name, t2.domain_id, t4.domain_name " + \
        " FROM tbl_statutories t1 " + \
        " INNER JOIN tbl_statutory_levels t2 " + \
        " on t1.level_id = t2.level_id " + \
        " INNER JOIN tbl_countries t3 " + \
        " on t2.country_id = t3.country_id " + \
        " INNER JOIN tbl_domains t4 " + \
        " on t2.domain_id = t4.domain_id"
    if statutory_id is not None:
        query = query + " WHERE t1.statutory_id = %s"
        rows = db.select_all(query, [int(statutory_id)])
    else:
        rows = db.select_all(query)
    result = []
    if rows:
        result = convert_to_dict(rows, columns)
        frame_parent_mappings(db, result, statutory_id)
    return return_statutory_master(result)


def frame_parent_mappings(db, data, statutory_id=None):
    columns = [
        "statutory_id", "statutory_name",
        "level_id", "parent_ids",
        "country_id", "country_name",
        "domain_id", "domain_name"
    ]
    query = "SELECT t1.statutory_id, t1.statutory_name, " + \
        " t1.level_id, t1.parent_ids, t2.country_id, " + \
        " t3.country_name, t2.domain_id, t4.domain_name " + \
        " FROM tbl_statutories t1 " + \
        " INNER JOIN tbl_statutory_levels t2 " + \
        " on t1.level_id = t2.level_id " + \
        " INNER JOIN tbl_countries t3 " + \
        " on t2.country_id = t3.country_id " + \
        " INNER JOIN tbl_domains t4 " + \
        " on t2.domain_id = t4.domain_id"
    if statutory_id is not None:
        query = query + " WHERE t1.statutory_id = %s"
        rows = db.select_all(query, [statutory_id])
    else:
        rows = db.select_all(query)
    data = []
    if rows:
        data = convert_to_dict(rows, columns)

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
        parent_ids = [
            int(x) for x in d["parent_ids"][:-1].split(',')
        ]

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
    db, parent_ids, statutory_id, domain_id=None
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

    rows = db.select_all(query + where_qry, param)

    columns = ["statutory_id", "statutory_name", "level_id", "domain_id"]
    result = []
    if rows:
        result = convert_to_dict(rows, columns)
    return result


def get_country_wise_level_1_statutoy(db):
    if bool(STATUTORY_PARENTS) is False:
        get_statutory_master(db)
    query = "SELECT t1.statutory_id, t1.statutory_name, " + \
        " t1.level_id, t1.parent_ids, t2.country_id, " + \
        " t3.country_name, t2.domain_id, t4.domain_name " + \
        " FROM tbl_statutories t1 " + \
        " INNER JOIN tbl_statutory_levels t2 " + \
        " on t1.level_id = t2.level_id " + \
        " INNER JOIN tbl_countries t3 " + \
        " on t2.country_id = t3.country_id " + \
        " INNER JOIN tbl_domains t4 " + \
        " on t2.domain_id = t4.domain_id " + \
        " WHERE t2.level_position=1"
    rows = db.select_all(query)
    result = []
    if rows:
        columns = [
            "statutory_id", "statutory_name", "level_id",
            "parent_ids", "country_id", "country_name",
            "domain_id", "domain_name"
        ]
        result = convert_to_dict(rows, columns)
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
