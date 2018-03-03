function getStatutoryMappingCsvList(callback){
  var request = [
    'GetStatutoryMappingCsvUploadedList',
    {}
  ];
  apiRequest("bu/statutory_mapping", request, callback);
}

function getApproveMappingCSVList(cid, did, uid, callback){
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

/*function exportStatutoryMappingBulkReportData(args, callback) {
  callerName = 'general';
  var request = [
    'ExportStatutoryMappingBulkReportData', args
  ];
  apiRequest(callerName, request, callback);
}*/


function updateActionFromList(csvid, action, remarks, pwd, country_id, domain_id, callback){
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


function confirmUpdateAction(csvid, country_id, domain_id, callback){
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


function getApproveMappingView(csvid, f_count, r_range, callback){
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

