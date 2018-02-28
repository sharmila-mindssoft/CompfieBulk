from ..buapiprotocol import buclientunitsprotocol as bu_cu
import datetime

__all__ = [
    "save_client_units_mapping_csv", 
    "save_mapping_client_unit_data",
    "fetch_rejected_client_unit_report",
    "update_unit_count",
    "get_list_and_delete_rejected_unit"
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
    returns statutory mapping bulk report list
    :param
        db: database object
        session_user: logged in user details
    :type
        db: Object
        session_user: Object
    :returns
        result: list of bulk data records by mulitple country, 
        domain, KnowledgeExecutives selections based.
    rtype:
        result: List
'''
########################################################

def fetch_rejected_client_unit_report(db, session_user, 
    user_id, client_group_id):

    rejectdatalist=[]
    args = [client_group_id, user_id]
    uploaded_on='';
    approved_on='';
    rejected_on='';
    data = db.call_proc('sp_rejected_client_unit_data', args)
    for d in data:

        if(d["uploaded_on"] is not None):
            uploaded_on = datetime.datetime.strptime(str(d["uploaded_on"]), 
                '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M')

        if(d["approved_on"] is not None):
            approved_on = datetime.datetime.strptime(str(d["approved_on"]),
            '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M')

        if(d["rejected_on"] is not None):
            rejected_on = datetime.datetime.strptime(str(d["rejected_on"]), 
                '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M')

        if (d["rejected_file_download_count"] is None):
            download_count=0
        else:
            download_count=d["rejected_file_download_count"]

        rejectdatalist.append(bu_cu.ClientUnitRejectData(
             int(d["csv_unit_id"]),
             str(d["uploaded_by"]),
             str(uploaded_on),
             str(d["csv_name"]),
             int(d["total_records"]),
             int(d["total_rejected_records"]),
             str(d["approved_by"]),
             str(d["rejected_by"]),
             str(approved_on),
             str(rejected_on),
             int(d["is_fully_rejected"]),
             int(d["approve_status"]),
             int(download_count),
             str(d["remarks"]),
             d["action"],
             int(d["declined_count"])
             
        )) 
    return rejectdatalist

def update_unit_count(db, session_user, csv_id):
    updated_unit_count=[];
    args = [csv_id]
    data = db.call_proc('cu_update_download_count', args)
    for d in data:
        updated_unit_count.append(bu_cu.UpdateUnitDownloadCount(
             int(d["csv_unit_id"]), int(d["rejected_file_download_count"])
        ))
    return updated_unit_count


def get_list_and_delete_rejected_unit(db, session_user, 
    user_id, csv_id, bu_client_id):

    args = [csv_id]
    data = db.call_proc('cu_delete_unit_by_csvid', args)

    rejectdatalist=fetch_rejected_client_unit_report(
        db, session_user, user_id, bu_client_id)

    return rejectdatalist