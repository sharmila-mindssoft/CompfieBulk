from ..buapiprotocol import buclientunitsprotocol as bu_cu
import datetime

__all__ = [
    "save_client_units_mapping_csv",
    "save_mapping_client_unit_data",
    "get_ClientUnits_Uploaded_CSVList",
    "fetch_rejected_client_unit_report",
    "update_unit_count",
    "get_list_and_delete_rejected_unit",
    "fetch_client_unit_bulk_report",
    "fetch_rejected_cu_download_csv_report",
    "get_cu_csv_file_name_by_id"
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
            row["rej_count"], row["declined_count"]
        ))
    return csv_list

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
            uploaded_on = datetime.datetime.strptime(
                str(d["uploaded_on"]),
                '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M')

        if(d["approved_on"] is not None):
            approved_on = datetime.datetime.strptime(
                str(d["approved_on"]),
                '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M')

        if(d["rejected_on"] is not None):
            rejected_on = datetime.datetime.strptime(
                str(d["rejected_on"]),
                '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M')

        if (d["rejected_file_download_count"] is None):
            download_count=0
        else:
            download_count=d["rejected_file_download_count"]

        rejectdatalist.append(bu_cu.ClientUnitRejectData(
             int(d["csv_unit_id"]),
             int(d["uploaded_by"]),
             str(uploaded_on),
             str(d["csv_name"]),
             int(d["total_records"]),
             int(d["total_rejected_records"]),
             int(d["approved_by"]),
             int(d["rejected_by"]),
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

def fetch_client_unit_bulk_report(db, session_user, user_id,
    clientGroupId, from_date, to_date,
    record_count, page_count, child_ids, user_category_id):

    clientdatalist=[]
    expected_result=2

    if(len(child_ids)>0):
        if(user_category_id==5):
            user_ids=convertArrayToString(child_ids)
        elif(user_category_id==6 and user_category_id!=5):
            user_ids=convertArrayToString(child_ids)
        else:
            user_ids=user_id
    args = [clientGroupId, from_date, to_date, record_count, page_count, str(user_ids)]
    data = db.call_proc_with_multiresult_set('sp_client_unit_bulk_reportdata', args, expected_result)


    print "sp_client_unit_bulk_reportdata  >>"
    print data
    print "Total"
    print data[1][0]["total"]

    clientdata=data[0]
    total_record=data[1][0]["total"]
    approved_on=""
    rejected_on=""
    if(clientdata):
        for d in clientdata :
            uploaded_on = datetime.datetime.strptime(str(d["uploaded_on"]),
                '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M')

            if(d["approved_on"] is not None):
                approved_on = datetime.datetime.strptime(str(d["approved_on"]),
                    '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M')

            if(d["rejected_on"] is not None):
                rejected_on = datetime.datetime.strptime(str(d["rejected_on"]),
                    '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M')

            if(d["is_fully_rejected"] is not None):
                is_fully_rejected=d["is_fully_rejected"]
            else :
                is_fully_rejected=0


            clientdatalist.append(bu_cu.StatutoryReportData(
                 int(d["uploaded_by"]),
                 str(uploaded_on),
                 str(d["csv_name"]),
                 int(d["total_records"]),
                 int(d["total_rejected_records"]),
                 int(d["approved_by"]),
                 int(d["rejected_by"]),
                 str(approved_on),
                 str(rejected_on),
                 int(is_fully_rejected),
                 int(d["approve_status"])
            ))

    return clientdatalist, total_record

def convertArrayToString(array_ids):
    existing_id=[]
    id_list=""
    if(len(array_ids)>1):
        for d in array_ids :
         if d in existing_id:
           break
         id_list+=str(d)+","
         existing_id.append(d)
        id_list=id_list.rstrip(',');
    else :
        id_list=array_ids[0]
    return id_list

def fetch_rejected_cu_download_csv_report(db, session_user,
    user_id, cg_id, csv_id):

    rejectdatalist=[]
    args = [cg_id, csv_id, user_id]
    data = db.call_proc('sp_rejected_cu_csv_report', args)
    approved_on='0000-00-00'
    uploaded_on=''
    rejected_on=''

    for d in data:
        if(d["uploaded_on"] is not None):
            uploaded_on = datetime.datetime.strptime(str(d["uploaded_on"]),
            '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M');

        if(d["approved_on"] is not None):
            approved_on = datetime.datetime.strptime(str(d["approved_on"]),
        '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M');

        if(d["rejected_on"] is not None):
            rejected_on = datetime.datetime.strptime(str(d["rejected_on"]),
            '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M');

        if (d["rejected_file_download_count"] is None):
            download_count=0
        else:
            download_count=d["rejected_file_download_count"]

        rejectdatalist.append({
             str(d["csv_unit_id"]),
             str(d["uploaded_by"]),
             str(uploaded_on),
             str(d["csv_name"]),
             str(d["total_records"]),
             str(d["total_rejected_records"]),
             str(d["approved_by"]),
             str(d["rejected_by"]),
             str(approved_on),
             str(d["rejected_on"]),
             str(d["is_fully_rejected"]),
             str(d["approve_status"]),
             str(download_count),
             str(d["remarks"]),
             str(d["action"]),
             str(d["rejected_reason"])
        })
    return data

def get_cu_csv_file_name_by_id(db, session_user, user_id, csv_id):
    args = [csv_id]
    data = db.call_proc('sp_get_cu_csv_file_name_by_id', args)
    print data[0]["csv_name"]
    return data[0]["csv_name"]
