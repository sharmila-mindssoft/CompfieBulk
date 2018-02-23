from ..buapiprotocol import buclientunitsprotocol as bu_cu

__all__ = [
    "save_client_units_mapping_csv", "save_mapping_client_unit_data"
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
