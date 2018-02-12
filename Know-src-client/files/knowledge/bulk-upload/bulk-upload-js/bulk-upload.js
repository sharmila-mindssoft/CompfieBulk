
function getStatutoryMappingCsvList(callback){
  var request = [
    'GetStatutoryMappingCsvUploadedList',
    {}
  ];
  apiRequest("bu/statutory_mapping", request, callback);
}

// Statutory Mapping Bulk Report List
function getStatutoryMappingsBulkReportData(filterDatas, callback) {
    var request = [
        'GetStatutoryMappingBulkReportData',
        filterDatas
    ];
    apiRequest('bu/statutory_mapping', request, callback);
}