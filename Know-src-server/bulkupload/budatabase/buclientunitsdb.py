from ..buapiprotocol import buclientunitsprotocol as bu_cu

__all__ = [
    "save_client_units_mapping_csv", "save_mapping_client_unit_data",
    "get_ClientUnits_Uploaded_CSVList"
]

########################################################
'''
    returns new primary key from table
    :param
        db: database object
        args: list of procedure params
    :type
        db: Object
        args: List
    :returns
        result: return new id
    rtype:
        result: Integer
'''
########################################################

def save_client_units_mapping_csv(db, args):
    newid = db.call_insert_proc("sp_client_units_bulk_csv_save", args)
    return newid


########################################################
'''
    returns true if the data save properply
    :param
        db: database object
        csv_id: parent table id
        csv_data: list of data to save
    :type
        db: Object
        csv_id: Integer
        csv_data: List
    :returns
        result: return boolean
    rtype:
        result: Boolean
'''
########################################################

def save_mapping_client_unit_data(db, csv_id, csv_data) :
    try:
        columns = [
            "csv_unit_id", "legal_entity", "division", "category",
            "geography_level", "unit_location", "unit_code",
            "unit_name", "address", "city", "state", "postalcode",
            "domain", "organization", "action"
        ]
        values = []

        for idx, d in enumerate(csv_data) :
            print d
            values.append((
                csv_id, d["Legal_Entity"], d["Division"],
                d["Category"], d["Geography_Level"], d["Unit_Location"],
                d["Unit_Code"], d["Unit_Name"], d["Unit_Address"], d["City"],
                d["State"], d["Postal_Code"], d["Domain"], d["Organization"],
                0
            ))

        if values :
            db.bulk_insert("tbl_bulk_units", columns, values)
            return True
        else :
            return False
    except Exception, e:
        print str(e)
        raise ValueError("Transaction failed")

########################################################
'''
    returns result set from table
    :param
        db: database object
        args: list of procedure params
    :type
        db: Object
        args: List
    :returns
        result: return result set of csv uploaded list
    rtype:
        result: Datatable
'''
########################################################

def get_ClientUnits_Uploaded_CSVList(db, clientId, groupName):
    csv_list = []
    result = db.call_proc("sp_client_units_csv_list", [clientId, groupName])
    for row in result:
        csv_list.append(bu_cu.ClientUnitCSVList(
            row["csv_unit_id"], row["csv_name"], row["uploaded_by"],
            row["uploaded_on"], row["no_of_records"], row["approved_count"],
            row["rej_count"]
        ))
    return csv_list
