// function getCompletedTaskCurrentYearCsvList(callback) {
//     var request = [
//         'GetStatutoryMappingCsvUploadedList',
//         {}
//     ];
//     apiRequest("bu/statutory_mapping", request, callback);
// }

function getDomains(le_id, callback) {
    var request = [
        'GetCompletedTask_Domains', {
            'le_id': le_id
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

// var request = [
//     'GetClientUnitsUploadedCSVFiles',
//     {
//         'bu_client_id': clientId,
//         'bu_group_name': groupName
//     }
// ];

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