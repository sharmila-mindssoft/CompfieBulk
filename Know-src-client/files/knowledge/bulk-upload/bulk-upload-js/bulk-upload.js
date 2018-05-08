var KM_USER_CATEGORY = '';
var KE_USER_CATEGORY = '';
var TM_USER_CATEGORY = '';
var TE_USER_CATEGORY = '';
var DM_USER_CATEGORY = '';
var DE_USER_CATEGORY = '';
var SYSTEM_REJECTED_BY = '';
var REJECTED_FILE_DOWNLOADCOUNT = '';

function getStatutoryMappingCsvList(callback) {
    var request = [
        'GetStatutoryMappingCsvUploadedList',
        {}
    ];
    apiRequest("bu/statutory_mapping", request, callback);
}

function uploadClientUnitsBulkCSV(
    clientId, groupName, fileName, fileContent, fileSize, callback
) {
    var request = [
        'UploadClientUnitsBulkCSV',
        {
            'bu_client_id': clientId,
            'bu_group_name': groupName,
            'csv_name': fileName,
            'csv_data': fileContent,
            'csv_size': fileSize
        }
    ];
    apiRequest('bu/client_units', request, callback);
}

function uploadStatutoryMappingCSV(args, callback) {
    var request = [
        'UploadStatutoryMappingCSV', args
    ];
    apiRequest("bu/statutory_mapping", request, callback);
}

function getClientInfo(callback) {
    var request = [
        'GetClientInfo',
        {}
    ];
    apiRequest("bu/assign_statutory", request, callback);
}


function uploadFileFormat(size, name, content) {
    return {
        'file_size': parseInt(size),
        'file_name': name,
        'file_content': content
    };
}

function convert_to_base64(file, callback) {
    var reader = new FileReader();
    reader.onload = function(readerEvt) {
        var binaryString = readerEvt.target.result;
        var file_content = btoa(binaryString);
        callback(file_content);
    };
    reader.readAsBinaryString(file);
}

function uploadCSVFile(fileListener, callback) {
    var status = false;
    var evt = fileListener;
    var max_limit = 1024 * 1024 * 50;
    // file max limit 50MB
    var files = evt.target.files;
    var file = files[0];
    var file_name = file.name;
    var file_size = file.size;
    var file_extension = file_name.substring(file_name.lastIndexOf('.') + 1);
    if (file_name.indexOf('.') !== -1) {
        console.log("file_extension--" + file_extension);
        if (file_size > max_limit) {
            callback(status, 'File max limit exceeded');
        } else if ($.inArray(file_extension, ['csv']) == -1) {
            callback(status, 'Invalid file format');
        } else {
            var file_content = null;
            if (files && file) {
                convert_to_base64(file, function(file_content) {
                    if (file_content == null) {
                        callback(status, 'File content is empty');
                    }
                    var result = uploadFileFormat(
                        file_size, file_name, file_content
                    );
                    status = true;
                    callback(status, result);
                });
            }
        }
    } else {
        callback(status, 'Invalid file format');
    } // file_extension = file_name.substr(
    //     file_name.lastIndexOf('.') + 1
    // );
}
// Statutory Mapping Bulk Report List
function getStatutoryMappingsBulkReportData(args, callback) {
    var request = [
        'GetSMBulkReportData', args
    ];
    apiRequest('bu/statutory_mapping', request, callback);
}

function getClientGroupsClientUnitFilesList(clientId, groupName, callback) {
    var request = [
        'GetClientUnitsUploadedCSVFiles',
        {
            'bu_client_id': clientId,
            'bu_group_name': groupName
        }
    ];
    apiRequest('bu/client_units', request, callback);
}

function exportSMBulkReportData(args, callback) {
    callerName = 'bu/statutory_mapping';
    var request = [
        'ExportSMBulkReportData', args
    ];
    apiRequest(callerName, request, callback);
}

function exportCUBulkReportData(args, callback) {
    callerName = 'bu/client_units';
    var request = [
        'ExportCUBulkReportData', args
    ];
    apiRequest(callerName, request, callback);
}

function exportASBulkReportData(args, callback) {
    callerName = 'bu/assign_statutory';
    var request = [
        'ExportASBulkReportData', args
    ];
    apiRequest(callerName, request, callback);
}



// Client Unit Bulk Report
function getClientUnitBulkReportData(args, callback) {
    var request = [
        'GetClientUnitBulkReportData', args
    ];
    apiRequest('bu/client_units', request, callback);
}
// Assigned Statutory Bulk Report
function getClientUnitRejectedData(args, callback) {
    var request = [
        'GetClientUnitRejectedData', args
    ];
    apiRequest('bu/client_units', request, callback);
}

function updateDownloadClickCount(args, callback) {
    var request = [
        'UpdateUnitClickCount', args
    ];
    apiRequest('bu/client_units', request, callback);

}
// Assigned Statutory Bulk Report
function deleteRejectedUnitByCsvID(args, callback) {
    var request = [
        'DeleteRejectedUnitDataByCsvID', args
    ];
    apiRequest('bu/client_units', request, callback);
}



// Assigned Statutory Bulk Report
function getRejectedSMBulkData(args, callback) {
    var request = [
        'GetRejectedSMBulkUploadData', args
    ];
    apiRequest('bu/statutory_mapping', request, callback);
}
// Assigned Statutory Bulk Report
function deleteRejectedSMByCsvID(args, callback) {
    var request = [
        'DeleteRejectedSMCsvId', args
    ];
    apiRequest('bu/statutory_mapping', request, callback);
}

function setDownloadClickCount(args, callback) {
    var request = [
        'UpdateDownloadCountToRejectedStatutory', args
    ];
    apiRequest('bu/statutory_mapping', request, callback);

}

function downloadRejectedSMReportData(args, callback) {
    var request = [
        'DownloadRejectedSMReportData', args
    ];
    apiRequest("bu/statutory_mapping", request, callback);
}

function downloadRejectedClientUnitReport(args, callback) {
    var request = [
        'DownloadRejectedClientUnitReport', args
    ];
    apiRequest("bu/client_units", request, callback);
}

function downloadRejectedASMReportData(args, callback) {
    var request = [
        'DownloadRejectedASMReport', args
    ];
    apiRequest("bu/assign_statutory", request, callback);
}

function getDownloadAssignStatutory(cl_id, le_id, d_ids, u_ids, cl_name,
    le_name, d_names, u_names, callback) {
    var request = [
        'DownloadAssignStatutory',
        {
            "cl_id": cl_id,
            "le_id": le_id,
            "d_ids": d_ids,
            "u_ids": u_ids,
            "cl_name": cl_name,
            "le_name": le_name,
            "d_names": d_names,
            "u_names": u_names
        }
    ];
    apiRequest("bu/assign_statutory", request, callback);
}

function getUploadAssignStatutoryCSV(args, callback) {
    var request = [
        'UploadAssignStatutoryCSV', args
    ];
    apiRequest("bu/assign_statutory", request, callback);
}

function getAssignStatutoryForApprove(cl_id, le_id, callback) {
    var request = [
        'GetAssignStatutoryForApprove',
        {
            "cl_id": cl_id,
            "le_id": le_id
        }
    ];
    apiRequest("bu/assign_statutory", request, callback);
}

/*function exportStatutoryMappingBulkReportData(args, callback) {
  callerName = 'general';
  var request = [
    'ExportStatutoryMappingBulkReportData', args
  ];
  apiRequest(callerName, request, callback);
}*/


function updateActionFromList(
    csvid, action, remarks, pwd, country_id, domain_id, callback
) {
    var request = [
        'UpdateApproveActionFromList',
        {
            "csv_id": csvid,
            "bu_action": action,
            "remarks": remarks,
            "password": pwd,
            "c_id": parseInt(country_id),
            "d_id": parseInt(domain_id)
        }
    ];
    apiRequest("bu/statutory_mapping", request, callback);
}

// Assigned Statutory Bulk Report
function getRejectedAssignSMData(args, callback) {
    var request = [
        'GetRejectedAssignSMData', args
    ];
    apiRequest('bu/assign_statutory', request, callback);
}

function updateASMDownloadClickCount(args, callback) {
    var request = [
        'UpdateASMClickCount', args
    ];
    apiRequest('bu/assign_statutory', request, callback);

}
// Assigned Statutory Bulk Report
function deleteRejectedASMByCsvID(args, callback) {
    var request = [
        'DeleteRejectedASMByCsvID', args
    ];
    apiRequest('bu/assign_statutory', request, callback);
}

function confirmUpdateAction(csvid, country_id, domain_id, callback) {
    var request = [
        'ConfirmStatutoryMappingSubmit',
        {
            "csv_id": csvid,
            "c_id": parseInt(country_id),
            "d_id": parseInt(domain_id)
        }
    ];
    apiRequest("bu/statutory_mapping", request, callback);
}


function getApproveMappingView(csvid, f_count, r_range, callback) {
    var request = [
        'GetApproveStatutoryMappingView',
        {
            "csv_id": csvid,
            "f_count": f_count,
            "r_range": r_range
        }
    ];
    apiRequest("bu/statutory_mapping", request, callback);
}


function getAssignStatutoryFilters(csvid, callback) {
    var request = [
        'GetAssignStatutoryFilters',
        {
            "csv_id": csvid
        }
    ];
    apiRequest("bu/assign_statutory", request, callback);
}

function getViewAssignStatutoryData(csvid, f_count, r_range, callback) {
    var request = [
        'ViewAssignStatutoryData',
        {
            "csv_id": csvid,
            "f_count": f_count,
            "r_range": r_range
        }
    ];
    apiRequest("bu/assign_statutory", request, callback);
}

function getViewAssignStatutoryDataFromFilter(csvid, f_count, r_range,
    filter_d_name, filter_u_name, filter_p_leg, s_leg, s_prov, c_task, c_desc,
    filter_view_data, s_status, c_status, callback) {
    var request = [
        'ViewAssignStatutoryDataFromFilter',
        {
            "csv_id": csvid,
            "f_count": f_count,
            "r_range": r_range,
            "filter_d_name": filter_d_name,
            "filter_u_name": filter_u_name,
            "filter_p_leg": filter_p_leg,
            "s_leg": s_leg,
            "s_prov": s_prov,
            "c_task": c_task,
            "c_desc": c_desc,
            "filter_view_data": filter_view_data,
            "s_status": s_status,
            "c_status": c_status
        }
    ];
    apiRequest("bu/assign_statutory", request, callback);
}

function assignStatutoryActionInList(cl_id, le_id, csvid, action,
    remarks, password, callback) {
    var request = [
        'AssignStatutoryApproveActionInList',
        {
            "cl_id": cl_id,
            "le_id": le_id,
            "csv_id": csvid,
            "bu_action": action,
            "remarks": remarks,
            "password": password
        }
    ];
    apiRequest("bu/assign_statutory", request, callback);
}

function getApproveMappingCSVList(cid, did, uid, callback) {
    var request = [
        'GetApproveStatutoryMappingList',
        {
            "c_id": cid,
            "d_id": did,
            "uploaded_by": uid
        }
    ];
    apiRequest("bu/statutory_mapping", request, callback);
}

function updateActionFromView(csvid, smid, action, remarks, callback) {
    var request = [
        'SaveAction',
        {
            "sm_id": smid,
            "csv_id": csvid,
            "bu_action": action,
            "remarks": remarks,
        }
    ];
    apiRequest("bu/statutory_mapping", request, callback);
}

function performClientUnitApproveReject(csv_id, actionType, remarksText, pwd,
    client_id, callback) {
    var request = [
        'PerformClientUnitApproveReject',
        {
            "csv_id": csv_id,
            "bu_action": actionType,
            "bu_remarks": remarksText,
            "password": pwd,
            "bu_client_id": parseInt(client_id),
        }
    ];
    apiRequest("bu/client_units", request, callback);
}

function getApproveMappingViewFilter(csvid, callback) {
    var request = [
        'GetApproveMappingFilter',
        {
            "csv_id": csvid
        }
    ];
    apiRequest("bu/statutory_mapping", request, callback);

}

// Assigned Statutory Bulk Report

function getAssignedStatutoryBulkReportData(args, callback) {
    var request = [
        'GetAssignedStatutoryBulkReportData', args
    ];
    apiRequest('bu/assign_statutory', request, callback);

}

// fetches client unit bulk uploaded units list for approval/ rejection

function getBulkClientUnitApproveRejectList(csv_id, f_count,
    r_range, callback) {
    var request = [
        'GetBulkClientUnitApproveRejectList',
        {
            "csv_id": csv_id,
            "f_count": f_count,
            "r_range": r_range,
        }
    ];
    apiRequest("bu/client_units", request, callback);
}

function updateAssignStatutoryActionFromView(csvid, as_id, action, remarks,
    callback) {
    var request = [
        'SaveAction',
        {
            "as_id": as_id,
            "csv_id": csvid,
            "bu_action": action,
            "remarks": remarks,
        }
    ];
    apiRequest("bu/assign_statutory", request, callback);
}

function confirmAssignStatutoryUpdateAction(csvid, cl_id, le_id, callback) {
    var request = [
        'ConfirmAssignStatutorySubmit',
        {
            "csv_id": csvid,
            "cl_id": cl_id,
            "le_id": le_id
        }
    ];
    apiRequest("bu/assign_statutory", request, callback);
}

function confirmClientUnitDeclination(csv_id, client_id, callback) {
    var request = [
        'ConfirmClientUnitDeclination',
        {
            "csv_id": csv_id,
            "bu_client_id": parseInt(client_id),
        }
    ];
    apiRequest("bu/client_units", request, callback);
}

function getBulkClientUnitListForFilterView(csvid, f_count, r_range,
    filter_le, filter_div, filter_cg, filter_u_loc, filter_u_code,
    filter_domain, filter_orgn, actionVal, callback) {
    var request = [
        'GetBulkClientUnitListForFilterView',
        {
            "csv_id": csvid,
            "f_count": f_count,
            "r_range": r_range,
            "bu_le_name": filter_le,
            "bu_division_name": filter_div,
            "bu_category_name": filter_cg,
            "bu_unit_location": filter_u_loc,
            "bu_unit_code": filter_u_code,
            "bu_domain": filter_domain,
            "bu_orgn": filter_orgn,
            "bu_action": actionVal
        }
    ];
    apiRequest("bu/client_units", request, callback)
}

function updateClientUnitActionFromView(csvid, b_u_id, action, remarks,
    callback) {
    var request = [
        'SaveBulkClientUnitListFromView',
        {
            "bulk_unit_id": b_u_id,
            "csv_id": csvid,
            "bu_action": action,
            "bu_remarks": remarks,
        }
    ];
    apiRequest("bu/client_units", request, callback);
}

function getApproveMappingViewFromFilter(args, callback) {
    var request = [
        'GetApproveStatutoryMappingViewFilter', args
    ];
    apiRequest("bu/statutory_mapping", request, callback);

}

function submitClientUnitActionFromView(csvid, action, remarks, pwd,
    client_id, callback) {
    var request = [
        'SubmitBulkClientUnitListFromView',
        {
            "csv_id": csvid,
            "bu_action": action,
            "bu_remarks": remarks,
            "password": pwd,
            "bu_client_id": parseInt(client_id),
        }
    ];
    apiRequest("bu/client_units", request, callback);
}

function confirmSubmitClientUnitFromView(csvid, client_id, callback) {
    var request = [
        'ConfirmSubmitClientUnitFromView',
        {
            "csv_id": csvid,
            "bu_client_id": parseInt(client_id),
        }
    ];
    apiRequest("bu/client_units", request, callback);
}

function submitMappingAction(csvid, country_id, domain_id, pwd, callback) {
    var request = [
        'SubmitStatutoryMapping',
        {
            "csv_id": csvid,
            "c_id": parseInt(country_id),
            "d_id": parseInt(domain_id),
            "password": pwd
        }
    ];
    apiRequest("bu/statutory_mapping", request, callback);
}

function validateAssignStatutory(csvid, callback) {
    var request = [
        'AssignStatutoryValidate',
        {
            "csv_id": csvid
        }
    ];
    apiRequest("bu/assign_statutory", request, callback);
}


function submitAssignStatutoryAction(csvid, cl_id, le_id, pwd, callback) {
    var request = [
        'SubmitAssignStatutory',
        {
            "csv_id": csvid,
            "cl_id": cl_id,
            "le_id": le_id,
            "password": pwd
        }
    ];
    apiRequest("bu/assign_statutory", request, callback);
}

function getClientGroupsList(callback) {
  var request = [
      'GetClientGroupsList',
      {}
  ];
  apiRequest("bu/client_units", request, callback);
}

function getTechnoUserDetails(uType, callback) {
  var request = [
      'GetTechnoUserDetails',
      {
        "user_type": uType
      }
  ];
  apiRequest("bu/client_units", request, callback);
}

function getDomainUserInfo(callback) {
  var request = [
      'GetDomainExecutiveDetails',
      {}
  ];
  apiRequest("bu/assign_statutory", request, callback);
}

/********* Load Js Constants For Report and Rejected lists ****/
function getBulkUploadConstants(callback){
  callerName = 'bu/assign_statutory';
  var request = [
      'GetBulkUploadConstants',
      {}
  ];
  apiRequest(callerName, request, callback);
}

function getLoadConstants(){
  bu.getBulkUploadConstants(function(error, data) {
    if (error == null) {
      KM_USER_CATEGORY=data.bu_constants[0].KnowledgeManager;
      KE_USER_CATEGORY=data.bu_constants[1].KnowledgeExecutive;

      TM_USER_CATEGORY=data.bu_constants[2].TechnoManager;
      TE_USER_CATEGORY=data.bu_constants[3].TechnoExecutive;

      DM_USER_CATEGORY=data.bu_constants[4].DomainManager;
      DE_USER_CATEGORY=data.bu_constants[5].DomainExecutive;

      SYSTEM_REJECTED_BY = data.bu_system_rejected_by;
      REJECTED_FILE_DOWNLOADCOUNT = data.bu_rejected_download_count;
    }

  });
}
/********* Load Js Constants For Report and Rejected lists  ****/

function getDomainList(callback) {
    var request = [
        'GetDomains',
        {}
    ];
    apiRequest('bu/statutory_mapping', request, callback);
}

function getKnowledgeUserInfo(callback) {
    console.log("Im in bulkupload")
  var request = [
      'GetKExecutiveDetails',
      {}
  ];
  apiRequest('bu/statutory_mapping', request, callback);
}
