function getStatutoryMappingCsvList(callback){
  var request = [
    'GetStatutoryMappingCsvUploadedList',
    {}
  ];
  apiRequest("bu/statutory_mapping", request, callback);
}

function uploadClientUnitsBulkCSV(clientId, group_name, file_name, file_content, file_size, callback) {
	callerName = 'bu/client_units';
	var request = [
	  'UploadClientUnitsBulkCSV',
	  {
	  	'bu_client_id': clientId,
	  	'bu_group_name': group_name,
	  	'csv_name': file_name,
	  	'csv_data': file_content,
	  	'csv_size': file_size
	  }
	];
	apiRequest(callerName, request, callback);
}

function uploadStatutoryMappingCSV(args, callback) {
    var request = [
    'UploadStatutoryMappingCSV', args
  ];
  apiRequest("bu/statutory_mapping", request, callback);
}

function getClientInfo(callback){
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
        file_content = btoa(binaryString);
        callback(file_content);
    };
    reader.readAsBinaryString(file);
}

function uploadCSVFile(fileListener, callback) {
    var status = false;
    var evt = fileListener;
    max_limit = 1024 * 1024 * 50;
    // file max limit 50MB
    var files = evt.target.files;
    var file = files[0];
    file_name = file.name;
    file_size = file.size;
    var file_extension = file_name.substring(file_name.lastIndexOf('.') + 1);
    if (file_name.indexOf('.') !== -1) {
      console.log("file_extension--"+file_extension);
        if (file_size > max_limit) {
            callback(status, 'File max limit exceeded');
        } else if ($.inArray(file_extension, ['csv']) == -1) {
            callback(status, 'Invalid file format');
        } else {
            file_content = null;
            if (files && file) {
                convert_to_base64(file, function(file_content) {
                    if (file_content == null) {
                        callback(status, 'File content is empty');
                    }
                    result = uploadFileFormat(file_size, file_name, file_content);
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
        'GetBulkReportData', args
    ];
    apiRequest('bu/statutory_mapping', request, callback);
}

function getClientGroupsClientUnitFilesList(clientId, groupName, callback) {
    callerName = 'bu/client_units';
    var request = [
        'GetClientUnitsUploadedCSVFiles',
        {
            'bu_client_id': clientId,
            'bu_group_name': groupName
        }
    ];
    apiRequest(callerName, request, callback);
}

/*function exportStatutoryMappingBulkReportData(args, callback) {
  callerName = 'general';
  var request = [
    'ExportStatutoryMappingBulkReportData', args
  ];
  apiRequest(callerName, request, callback);
}*/

// Assigned Statutory Bulk Report

function getAssignedStatutoryBulkReportData(args, callback) {
    var request = [
        'GetAssignedStatutoryBulkReportData', args
    ];
    apiRequest('bu/statutory_mapping', request, callback);
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
function updateDownloadClickCount(args, callback)
{
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
function getRejectedStatutoryMappingBulkUploadData(args, callback) {
    var request = [
        'GetRejectedStatutoryMappingBulkUploadData', args
    ];
    apiRequest('bu/statutory_mapping', request, callback);
}
// Assigned Statutory Bulk Report
function deleteRejectedStatutoryMappingByCsvID(args, callback) {
    var request = [
        'DeleteRejectedStatutoryMappingDataByCsvID', args
    ];
    apiRequest('bu/statutory_mapping', request, callback);
}

function setDownloadClickCount(args, callback)
{
  var request = [
      'UpdateDownloadCountToRejectedStatutory', args
  ];
  apiRequest('bu/statutory_mapping', request, callback);

}

function getDownloadAssignStatutory(cl_id, le_id, d_ids, u_ids, cl_name, le_name, d_names, u_names, callback){
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

function getAssignStatutoryForApprove(cl_id, le_id, callback){
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


function updateActionFromList(csvid, action, remarks, pwd, callback){
  var request = [
    'UpdateApproveActionFromList',
    {
        "csv_id": csvid,
        "bu_action": action,
        "remarks": remarks,
        "password": pwd
    }
  ];
  apiRequest("bu/statutory_mapping", request, callback);
}

// Assigned Statutory Bulk Report
function getRejectedAssignSMData(args, callback) {
    var request = [
        'GetRejectedAssignSMData', args
    ];
    apiRequest('bu/statutory_mapping', request, callback);
}

function updateASMDownloadClickCount(args, callback)
{
  var request = [
      'UpdateASMClickCount', args
  ];
  apiRequest('bu/statutory_mapping', request, callback);

}
// Assigned Statutory Bulk Report
function deleteRejectedASMByCsvID(args, callback) {
    var request = [
        'DeleteRejectedASMByCsvID', args
    ];
    apiRequest('bu/statutory_mapping', request, callback);
}
