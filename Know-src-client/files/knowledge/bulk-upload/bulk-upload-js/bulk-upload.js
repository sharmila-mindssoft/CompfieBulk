
function getStatutoryMappingCsvList(callback){
  var request = [
    'GetStatutoryMappingCsvUploadedList',
    {}
  ];
  apiRequest("bu/statutory_mapping", request, callback);
}

function uploadStatutoryMappingCSV(args, callback) {
    var request = [
    'UploadStatutoryMappingCSV', args
  ];
  apiRequest("bu/statutory_mapping", request, callback);
}


