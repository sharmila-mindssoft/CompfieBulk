from protocol import (
    core,
    knowledgemaster
)
__all__ = [
    "get_industries", "get_active_industries",
    "check_duplicate_industry",
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
    "save_statutory", "update_statutory",

]
def get_industries(db) :
    columns = ["industry_id", "industry_name", "is_active"]
    condition = " 1 ORDER BT industry_name"
    result = db.get_data("tbl_industries", columns, condition)

    return return_industry(result)

def get_industry_by_id(db, industry_id) :
    if type(industry_id) is int :
        q = "SELECT industry_name FROM tbl_industries \
            WHERE industry_id=%s"
        param = (industry_id)

    else :
        q = " SELECT (GROUP_CONCAT(industry_name SEPARATOR ', ')) as \
            industry_name FROM tbl_industries \
            WHERE industry_id in %s"
        param = (str(tuple(industry_id)))

    row = db.select_one(q, param)
    industry_name = None
    if row :
        industry_name = row[0]
    return industry_name


def get_active_industries(db) :
    columns = ["industry_id", "industry_name", "is_active"]
    condition = " is_active = 1 ORDER BT industry_name"
    result = db.get_data("tbl_industries", columns, condition)

    return return_industry(result)

def return_industry(data) :
    results = []
    for d in data :
        industry_id = d["industry_id"]
        industry_name = d["industry_name"]
        is_active = bool(d["is_active"])
        results.append(core.Industry(
            industry_id, industry_name, is_active
        ))
    return results


def check_duplicate_industry(db, industry_name, industry_id) :
    isDuplicate = False
    query = "SELECT count(1) FROM tbl_industries WHERE industry_name = %s "

    if industry_id is not None :
        query = query + " AND industry_id != %s"
        param = (industry_name, industry_id)
    else :
        param = (industry_name)

    row = db.select_one(query, param)

    if row[0] > 0 :
        isDuplicate = True

    return isDuplicate

def save_industry(db, industry_name, user_id):
    table_name = "tbl_industries"
    created_on = db.get_date_time()
    columns = ["industry_name", "created_by", "created_on"]
    values = [industry_name, str(user_id), str(created_on)]
    new_id = db.insert(table_name, columns, values)
    if new_id is False :
        return False
    else :
        action = "New Industry type %s added" % (industry_name)
        db.save_activity(user_id, 7, action)
        return True

def update_industry(db, industry_id, industry_name, user_id):
    oldData = get_industry_by_id(db, industry_id)
    if oldData is None :
        return False

    table_name = "tbl_industries"
    columns = ["industry_name", "updated_by"]
    values = [industry_name, int(user_id)]
    where_condition = " industry_id = %s"
    param = []
    param.extend(values)
    param.append(industry_id)

    if (db.update(table_name, columns, param, where_condition)) :
        action = "Industry type %s updated" % (industry_name)
        db.save_activity(user_id, 7, action)
        return True
    else :
        return False

def update_industry_status(db, industry_id, is_active, user_id) :
    oldData = get_industry_by_id(db, industry_id)
    if oldData is None:
        return False

    table_name = "tbl_industries"
    columns = ["is_active", "updated_by"]
    values = [is_active, user_id]
    where_condition = " industry_id = %s"
    param = []
    param.extend(values)
    param.append(industry_id)

    if (db.update(table_name, columns, param, where_condition)) :
        if is_active == 0:
            status = "deactivated"
        else:
            status = "activated"

        action = "Industry type %s status - %s" % (oldData, status)
        db.save_activity(user_id, 7, action)
    else :
        return False

def get_nature_by_id(db, nature_id) :
    q = "SELECT statutory_nature_name \
        FROM tbl_statutory_natures \
        WHERE statutory_nature_id=%s"
    param = (nature_id)
    row = db.select_one(q, param)
    nature_name = None
    if row :
        nature_name = row[0]
    return nature_name

def get_statutory_nature(db) :
    columns = [
        "statutory_nature_id", "statutory_nature_name",
        "is_active"
    ]
    condition = " 1 ORDER BT statutory_nature_name"
    result = db.get_data("tbl_statutory_natures", columns, condition)
    return return_statutory_nature(result)

def return_statutory_nature(data) :
    results = []
    for d in data :
        nature_id = d["statutory_nature_id"]
        nature_name = d["statutory_nature_name"]
        is_active = bool(d["is_active"])
        results.append(core.StatutoryNature(
            nature_id, nature_name, is_active
        ))
    return results

def check_duplicate_statutory_nature(db, nature_name, nature_id) :
    isDuplicate = False
    query = "SELECT count(1) FROM tbl_statutory_natures WHERE statutory_nature_name = %s "

    if nature_id is not None :
        query = query + " AND statutory_nature_id != %s"
        param = (nature_name, nature_id)
    else :
        param = (nature_name)

    row = db.select_one(query, param)

    if row[0] > 0 :
        isDuplicate = True

    return isDuplicate

def save_statutory_nature(db, nature_name, user_id) :
    table_name = "tbl_statutory_natures"
    created_on = db.get_date_time()
    columns = ["statutory_nature_name", "created_by", "created_on"]
    values = [nature_name, user_id, str(created_on)]
    new_id = db.insert(table_name, columns, values)
    if new_id is False :
        return False
    else :
        action = "New Statutory Nature %s added" % (nature_name)
        db.save_activity(user_id, 8, action)
        return True

def update_statutory_nature(db, nature_id, nature_name, user_id):
    oldData = get_nature_by_id(db, nature_id)
    if oldData is None:
        return False

    table_name = "tbl_statutory_natures"
    columns = ["statutory_nature_name", "updated_by"]
    values = [nature_name, user_id]
    where_condition = " statutory_nature_id = %s"
    param = []
    param.extend(values)
    param.append(nature_id)

    if (db.update(table_name, columns, param, where_condition)) :
        if is_active == 0:
            status = "deactivated"
        else:
            status = "activated"

        action = "Industry type %s status - %s" % (oldData, status)
        db.save_activity(user_id, 7, action)
    else :
        return False


    oldData = get_nature_by_id(nature_id)
    if oldData is None :
        return False

    table_name = "tbl_statutory_natures"
    field_with_data = " statutory_nature_name = '%s', updated_by = %s" % (
        nature_name, int(user_id)
    )
    where_condition = "statutory_nature_id = %s " % nature_id
    if (db.update_data(table_name, field_with_data, where_condition)) :
        action = "Statutory Nature %s updated" % (nature_name)
        db.save_activity(user_id, 8, action)
        return True
    else :
        return False

def update_statutory_nature_status(db, nature_id, is_active, user_id) :
    oldData = db.get_nature_by_id(nature_id)
    if oldData is None:
        return False

    table_name = "tbl_statutory_natures"
    field_with_data = "is_active = %s, updated_by = %s" % (
        int(is_active), int(user_id)
    )
    where_condition = "statutory_nature_id = %s " % (nature_id)

    if (db.update_data(table_name, field_with_data, where_condition)):
        if is_active == 0:
            status = "deactivated"
        else:
            status = "activated"

        action = "Statutory nature %s status  - %s" % (oldData, status)
        db.save_activity(user_id, 8, action)
        return True
    else :
        return False

def get_statutory_levels(db):
    query = "SELECT level_id, level_position, level_name, country_id, domain_id \
        FROM tbl_statutory_levels ORDER BY level_position"

    rows = db.select_all(query)
    result = []
    if rows :
        columns = [
            "level_id", "level_position",
            "level_name", "country_id", "domain_id"
        ]
        result = db.convert_to_dict(rows, columns)
    return db.return_statutory_levels(result)

def return_statutory_levels(db, data):
    statutory_levels = {}
    for d in data :
        country_id = d["country_id"]
        domain_id = d["domain_id"]
        levels = core.Level(
            d["level_id"], d["level_position"], d["level_name"]
        )
        country_wise = statutory_levels.get(country_id)
        _list = []
        if country_wise is None :
            country_wise = {}
        else :
            _list = country_wise.get(domain_id)
            if _list is None :
                _list = []
        _list.append(levels)
        country_wise[domain_id] = _list
        statutory_levels[country_id] = country_wise
    return statutory_levels

def save_statutory_levels(db, country_id, domain_id, levels, user_id) :

    table_name = "tbl_statutory_levels"
    created_on = db.get_date_time()
    for level in levels :
        name = level.level_name
        position = level.level_position
        if (level.level_id is None) :
            level_id = db.get_new_id("level_id", table_name)
            field = "(level_id, level_position, level_name, \
                country_id, domain_id, created_by, created_on)"
            data = (
                int(level_id), position, name, int(country_id),
                int(domain_id), int(user_id), str(created_on)
            )
            if (db.save_data(table_name, field, data)):
                action = "New Statutory levels added"
                db.save_activity(user_id, 9, action)
        else :
            field_with_data = "level_position=%s, \
                level_name='%s', updated_by=%s" % (
                    position, name, user_id
                )
            where_condition = "level_id=%s" % (level.level_id)
            if (
                db. update_data(
                    table_name, field_with_data, where_condition
                )
            ) :
                action = "Statutory levels updated"
                db.save_activity(user_id, 9, action)
    return True

def get_geography_levels(db):
    query = "SELECT level_id, level_position, level_name, country_id \
        FROM tbl_geography_levels ORDER BY level_position"
    rows = db.select_all(query)
    result = []
    if rows :
        columns = [
            "level_id", "level_position", "level_name", "country_id"
        ]
        result = db.convert_to_dict(rows, columns)
    return db.return_geography_levels(result)

def return_geography_levels(db, data):
    geography_levels = {}
    for d in data:
        country_id = d["country_id"]
        level = core.Level(
            d["level_id"], d["level_position"], d["level_name"]
        )
        _list = geography_levels.get(country_id)
        if _list is None :
            _list = []
        _list.append(level)
        geography_levels[country_id] = _list
    return geography_levels

def get_geograhpy_levels_for_user(db, user_id):
    country_ids = None
    if ((user_id is not None) and (user_id != 0)):
        country_ids = db.get_user_countries(user_id)
    columns = "level_id, level_position, level_name, country_id"
    condition = "1"
    if country_ids is not None:
        condition = "country_id in (%s) ORDER BY level_position" % country_ids
    rows = db.get_data(db.tblGeographyLevels, columns, condition)
    result = []
    if rows :
        columns = [
            "level_id", "level_position", "level_name", "country_id"
        ]
        result = db.convert_to_dict(rows, columns)
    return db.return_geography_levels(result)

def delete_grography_level(db, level_id):
    q = "select count(*) from tbl_geographies where level_id = %s" % (level_id)
    row = db.select_one(q)
    if row[0] > 0 :
        return True
    else :
        db.execute("delete from tbl_geographies where level_id = %s " % (level_id))
        db.execute("delete from tbl_geography_levels where level_id = %s " % (level_id))
        return False

def save_geography_levels(db, country_id, levels, user_id):
    table_name = "tbl_geography_levels"
    created_on = db.get_date_time()
    newlist = sorted(levels, key=lambda k: k.level_position, reverse=True)
    result = False
    for n in newlist :
        if n.is_remove is True :
            result = db.delete_grography_level(n.level_id)
            if result :
                break
            else :
                continue
    if result :
        return knowledgemaster.LevelShouldNotbeEmpty(n.level_position)

    for level in levels :
        name = level.level_name
        position = level.level_position
        if level.level_id is None :
            level_id = db.get_new_id("level_id", table_name)
            field = "(level_id, level_position, level_name, \
                country_id, created_by, created_on)"
            data = (
                level_id, position, name, int(country_id),
                int(user_id), str(created_on)
            )
            if (db.save_data(table_name, field, data)):
                action = "New Geography levels added"
                db.save_activity(user_id, 5, action)
        else :
            field_with_data = "level_position=%s, level_name='%s', \
            updated_by=%s" % (
                position, name, int(user_id)
            )
            where_condition = "level_id=%s" % (level.level_id)
            if (
                db. update_data(
                    table_name, field_with_data, where_condition
                )
            ):
                action = "Geography levels updated"
                db.save_activity(user_id, 5, action)
    return knowledgemaster.SaveGeographyLevelSuccess()


def get_geographies(db, user_id=None, country_id=None) :
    query = "SELECT distinct t1.geography_id, \
        t1.geography_name, \
        t1.level_id, \
        t1.parent_ids, t1.is_active, \
        t2.country_id, \
        (select country_name from tbl_countries where country_id = t2.country_id)as country_name, \
        t2.level_position \
        FROM tbl_geographies t1 \
        INNER JOIN tbl_geography_levels t2 \
        on t1.level_id = t2.level_id \
        INNER JOIN tbl_user_countries t4 \
        ON t2.country_id = t4.country_id"
    if user_id :
        query = query + " AND t4.user_id=%s" % (user_id)
    if country_id :
        query = query + " AND t2.country_id=%s" % (country_id)
    query = query + " ORDER BY country_name, level_position, geography_name"
    rows = db.select_all(query)
    result = []
    if rows :
        columns = [
            "geography_id", "geography_name", "level_id",
            "parent_ids", "is_active", "country_id", "country_name", "level_position"
        ]
        result = db.convert_to_dict(rows, columns)
        db.set_geography_parent_mapping(result)
    return db.return_geographies(result)

def return_geographies(db, data):
    geographies = {}
    for d in data :
        parent_ids = [int(x) for x in d["parent_ids"][:-1].split(',')]
        geography = core.Geography(
            d["geography_id"], d["geography_name"],
            d["level_id"], parent_ids, parent_ids[-1],
            bool(d["is_active"])
        )
        country_id = d["country_id"]
        _list = geographies.get(country_id)
        if _list is None :
            _list = []
        _list.append(geography)
        geographies[country_id] = _list
    return geographies

def get_geographies_for_user_with_mapping(db, user_id):
    # if bool(db.geography_parent_mapping) is False :
    #     db.get_geographies()
    country_ids = None
    if ((user_id is not None) and (user_id != 0)):
        country_ids = db.get_user_countries(user_id)
    columns = "t1.geography_id, t1.geography_name, t1.parent_names,"
    columns += "t1.level_id,t1.parent_ids, t1.is_active,"
    columns += " t2.country_id, t3.country_name"
    tables = [
        db.tblGeographies, db.tblGeographyLevels, db.tblCountries
    ]
    aliases = ["t1", "t2", "t3"]
    join_type = " INNER JOIN"
    join_conditions = [
        "t1.level_id = t2.level_id", "t2.country_id = t3.country_id"
    ]
    where_condition = "1"
    if country_ids is not None:
        where_condition = "t2.country_id in (%s)" % country_ids
    rows = db.get_data_from_multiple_tables(
        columns, tables, aliases, join_type,
        join_conditions, where_condition
    )
    geographies = {}
    if rows :
        columns = [
            "geography_id", "geography_name", "parent_names", "level_id",
            "parent_ids", "is_active", "country_id", "country_name"
        ]
        result = db.convert_to_dict(rows, columns)
        for d in result:
            parent_ids = [int(x) for x in d["parent_ids"][:-1].split(',')]
            geography = core.GeographyWithMapping(
                d["geography_id"], d["geography_name"],
                d["level_id"],
                d["parent_names"]+">>"+d["geography_name"],
                parent_ids[-1], bool(d["is_active"])
            )
            country_id = d["country_id"]
            _list = geographies.get(country_id)
            if _list is None :
                _list = []
            _list.append(geography)
            geographies[country_id] = _list
    return geographies

def get_geography_by_id(db, geography_id):
    query = "SELECT geography_id, geography_name, \
        level_id, parent_ids, parent_names, is_active \
        FROM tbl_geographies WHERE geography_id = %s" % (geography_id)
    rows = db.select_one(query)
    result = []
    if rows :
        columns = [
            "geography_id", "geography_name",
            "level_id", "parent_ids", "parent_names", "is_active"
        ]
        result = db.convert_to_dict(rows, columns)
    return result

def check_duplicate_geography(db, country_id, parent_ids, geography_id) :
    query = "SELECT t1.geography_id, t1.geography_name, \
        t1.level_id, t1.is_active \
        FROM tbl_geographies t1 \
        INNER JOIN tbl_geography_levels t2 \
        ON t1.level_id = t2.level_id \
        WHERE t1.parent_ids='%s' \
        AND t2.country_id = %s" % (parent_ids, country_id)
    if geography_id is not None :
        query = query + " AND geography_id != %s" % geography_id

    rows = db.select_all(query)
    columns = ["geography_id", "geography_name", "level_id", "is_active"]
    result = []
    if rows :
        result = db.convert_to_dict(rows, columns)
    return result

def save_geography(
    db, geography_level_id, geography_name, parent_ids, parent_names, user_id
):
    is_saved = False
    table_name = "tbl_geographies"
    created_on = db.get_date_time()
    geography_id = db.get_new_id("geography_id", table_name)
    field = "(geography_id, geography_name, level_id, \
        parent_ids, parent_names, created_by, created_on)"
    data = (
        geography_id, geography_name, int(geography_level_id),
        parent_ids, parent_names, int(user_id), str(created_on)
    )
    if (db.save_data(table_name, field, data)) :
        action = "New Geography %s added" % (geography_name)
        db.save_activity(user_id, 6, action)
        is_saved = True
    return is_saved

def update_geography(db, geography_id, name, parent_ids, parent_names, updated_by) :
    oldData = db.get_geography_by_id(geography_id)
    if bool(oldData) is False:
        return False
    # oldparent_ids = oldData["parent_ids"]

    table_name = "tbl_geographies"
    field_with_data = "geography_name='%s', parent_ids='%s', parent_names='%s', \
        updated_by=%s " % (
            name, parent_ids, parent_names, updated_by
        )

    where_condition = "geography_id = %s" % (geography_id)

    db.update_data(table_name, field_with_data, where_condition)
    action = "Geography - %s updated" % name
    db.save_activity(updated_by, 6, action)

    qry = "SELECT geography_id, geography_name, parent_ids, level_id \
      from tbl_geographies \
        WHERE parent_ids like '%s'" % str("%" + str(geography_id) + ",%")
    rows = db.select_all(qry)
    columns = ["geography_id", "geography_name", "parent_ids", "level_id"]
    result = db.convert_to_dict(rows, columns)

    for row in result :
        if row["parent_ids"] == "0,":
            row["parent_ids"] = geography_id
        else :
            row["parent_ids"] = row["parent_ids"][:-1]
        q = "UPDATE tbl_geographies as A inner join ( \
            select p.geography_id, (select group_concat(p1.geography_name SEPARATOR '>>') \
                from tbl_geographies as p1 where geography_id in (%s)) as names \
            from tbl_geographies as p \
            where p.geography_id = %s \
            ) as B ON A.geography_id = B.geography_id \
            inner join (select c.country_name, g.level_id from tbl_countries c \
                inner join tbl_geography_levels g on c.country_id = g.country_id ) as C \
                ON A.level_id  = C.level_id \
            set A.parent_names = concat(C.country_name, '>>', B.names) \
            where A.geography_id = %s AND C.level_id = %s " % (
                row["parent_ids"], row["geography_id"], row["geography_id"], row["level_id"]
            )
        db.execute(q)
    # action = "Geography name  %s updated in child parent_names" % (name)
    # db.save_activity(updated_by, 6, action)
    # db.getAllGeographies()
    return True

def change_geography_status(db, geography_id, is_active, updated_by) :
    oldData = db.get_geography_by_id(geography_id)
    if bool(oldData) is False:
        return False
    table_name = "tbl_geographies"
    field_with_data = "is_active=%s, updated_by=%s" % (
        int(is_active), int(updated_by)
    )
    where_condition = "geography_id = %s" % (int(geography_id))
    if (db.update_data(table_name, field_with_data, where_condition)) :
        if is_active == 0:
            status = "deactivated"
        else:
            status = "activated"
        action = "Geography %s status - %s" % (
            oldData["geography_name"], status
        )
        db.save_activity(updated_by, 6, action)
        return True

def save_statutory(db, name, level_id, parent_ids, parent_names, user_id) :
    is_saved = False
    statutory_id = db.get_new_id("statutory_id", "tbl_statutories")
    created_on = db.get_date_time()
    table_name = "tbl_statutories"
    field = "(statutory_id, statutory_name, level_id, \
        parent_ids, parent_names, created_by, created_on)"
    data = (
        int(statutory_id), name, int(level_id), parent_ids, parent_names,
        int(user_id), str(created_on)
    )

    if (db.save_data(table_name, field, data)) :
        action = "Statutory - %s added" % name
        db.save_activity(user_id, 10, action)
        is_saved = True
    return is_saved

def update_statutory(db, statutory_id, name, parent_ids, parent_names, updated_by) :
    oldData = db.get_statutory_by_id(statutory_id)
    if bool(oldData) is False:
        return False
    # oldparent_ids = oldData["parent_ids"]

    table_name = "tbl_statutories"
    field_with_data = "statutory_name='%s', parent_ids='%s', parent_names='%s', \
        updated_by=%s " % (
            name, parent_ids, parent_names, updated_by
        )

    where_condition = "statutory_id = %s" % (statutory_id)

    db.update_data(table_name, field_with_data, where_condition)
    action = "Statutory - %s updated" % name
    db.save_activity(updated_by, 10, action)

    qry = "SELECT statutory_id, statutory_name, parent_ids \
        from tbl_statutories \
        WHERE parent_ids like '%s'" % str("%" + str(statutory_id) + ",%")
    rows = db.select_all(qry)
    columns = ["statutory_id", "statutory_name", "parent_ids"]
    result = db.convert_to_dict(rows, columns)

    for row in result :
        if row["parent_ids"] == "0,":
            row["parent_ids"] = statutory_id
        else :
            row["parent_ids"] = row["parent_ids"][:-1]

        q = "Update tbl_statutories as A inner join ( \
                select p.statutory_id, (select group_concat(p1.statutory_name SEPARATOR '>>') \
                    from tbl_statutories as p1 where statutory_id in (%s)) as names \
                from tbl_statutories as p \
                where p.statutory_id = %s \
                ) as B on A.statutory_id = B.statutory_id \
                set A.parent_names = B.names\
                where A.statutory_id = %s " % (row["parent_ids"], row["statutory_id"], row["statutory_id"])
        db.execute(q)
        action = "statutory name %s updated in child rows." % name
        db.save_activity(updated_by, 10, action)
    return True
