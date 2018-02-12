
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