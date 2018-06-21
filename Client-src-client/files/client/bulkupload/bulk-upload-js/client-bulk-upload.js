function getDomains(le_id, callback) {
    var request = [
        'GetCompletedTask_Domains', {
            'le_id': le_id
        }
    ];
    clientApiRequest('bu/completed_task', request, callback);
}

function getUnits(le_id, domain_id, callback) {
    var request = [
        'GetUnits', {
            'legal_entity_id': le_id,
            'domain_id': domain_id
        }
    ];
    clientApiRequest('bu/completed_task', request, callback);
}

function UploadCompletedTaskCurrentYearCSV(args, callback) {
    var request = [
        'UploadCompletedTaskCurrentYearCSV', args
    ];
    clientApiRequest("bu/completed_task", request, callback);
}

function GetStatus(le_id, csv_name, callback){
    var request = [
        'GetStatus', {
            "legal_entity_id": le_id,
            "csv_name": csv_name
        }
    ];
    clientApiRequest('bu/completed_task', request, callback);
}
function saveBulkRecords(args, callback) {
    var request = [
        'SaveBulkRecords', args
    ];
    clientApiRequest("bu/completed_task", request, callback);
}

function GetCompletedTaskCsvUploadedList(args, callback) {
    var request = [
        'GetCompletedTaskCsvUploadedList', args
    ];
    clientApiRequest("bu/completed_task", request, callback);
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
        console.log("file_extension--" + file_extension);
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

function getDownloadData(legalEntityId, domainId, unitId, complianceFrequency, startCount,
    LegalEntityName, domainName, unitName, unitCode,
    callback) {
    console.log("legalEntityId>>> " + legalEntityId);
    var request = [
        'GetDownloadData', {
            'legal_entity_id': legalEntityId,
            'unit_id': unitId,
            'domain_id': domainId,
            'compliance_task_frequency': complianceFrequency,
            'start_count': startCount,
            "le_name": LegalEntityName,
            "d_name": domainName,
            "u_name": unitName,
            "u_code": unitCode
        }
    ];
    clientApiRequest('bu/completed_task', request, callback);
}

function uploadFile(file, callback) {
    console.log(JSON.stringify(file))
    // var evt = fileListener;
    max_limit = 1024 * 1024 * 50;
    // file max limit 50MB
    // var files = evt.target.files;
    var results = [];
    FILE_TYPE = [
        "doc", "docx", "rtf", "pdf", "txt", "png", "jpeg", "gif", "csv", "xls", "xlsx",
        "rar", "tar", "gz", "ppt", "pptx", "jpg", "bmp", "odt", "odf", "ods"
    ];
    // for (var i = 0; i < files.length; i++) {
    // var file = files[i];
    file_name = file.name;
    file_size = file.size;
    var file_extension = file_name.substring(file_name.lastIndexOf('.') + 1).toLowerCase();
    if (file_size > max_limit) {
        displayMessage(message.file_maxlimit_exceed);
        return;
    }
    if (jQuery.inArray(file_extension, FILE_TYPE) == -1) {
        displayMessage(message.invalid_file_format);
        return;
    } else {
        file_content = null;
        if (file) {
            convert_to_base64(file,
                function(file_content) {
                    if (file_content == null) {
                        callback(message.file_content_empty);
                    }
                    var fN = file_name.substring(0, file_name.indexOf('.'));
                    var fE = file_name.substring(file_name.lastIndexOf('.') + 1);
                    var uniqueId = Math.floor(Math.random() * 90000) + 10000;
                    // var f_Name = fN + '-' + uniqueId + '.' + fE;
                    var f_Name = fN + '.' + fE;

                    result = uploadFileFormat(file_size, f_Name, file_content);
                    console.log("RESULT ->" + result)
                    results.push(result);
                    console.log("results ->" + results)
                        // if (results.length == files.length) {
                    callback(results);
                    // }
                });
        }
    }
    // }
}

/* Multiple File Upload */
function uploadFileFormat(size, name, content) {
    result = {
        'file_size': parseInt(size),
        'file_name': name,
        'file_content': content
    };
    return result;
}

function downloadUploadedData(
    legal_entity_id, csv_id, callback){
    request =[
        "DownloadUploadedData",
        {   
            "legal_entity_id": legal_entity_id,
            "csv_id": csv_id
        }
    ]
    return clientApiRequest('bu/completed_task', request, callback);
}

function updateDocumentCount(
    legal_entity_id, csv_id, count, callback){
    request =[
        "UpdateDocumentCount",
        {   
            "legal_entity_id": legal_entity_id,
            "csv_id": csv_id,
            "count": count
        }
    ]
    return clientApiRequest('bu/completed_task', request, callback);
}