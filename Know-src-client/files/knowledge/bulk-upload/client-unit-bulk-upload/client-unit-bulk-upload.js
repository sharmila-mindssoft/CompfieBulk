var clientGroupsList = [];
var groupSelect_name = $('#search-group-name');
var groupSelect_id = $('#group-id');
var groupListBox = $('#ac-group');
var groupUListCtrl = $('#ac-group ul');
var csvFileName = $('#csvfile');
var csvUploadButton = $('.uploadbtn');
var csvUploadedFile = '';

function initialize(type_of_initialization) {
	displayLoader();
	function onSuccess(data) {
	    clientGroupsList = data.client_group_list;
	    hideLoader();
	}

	function onFailure(error) {
	    displayMessage(error);
	    hideLoader();
	}
	mirror.getClientGroupsList(function(error, response) {
		console.log(error, response)
	    if (error == null) {
	        onSuccess(response);
	    } else {
	        onFailure(error);
	    }
	});
}

// To invoke loading of client groups list
groupSelect_name.keyup(function(e){
	csvUploadedFile = '';
    var condition_fields = ["is_active", "is_approved"];
    var condition_values = [true, "1"];
    var text_val = $(this).val();
    commonAutoComplete(
      e, groupListBox, groupSelect_id, text_val,
      clientGroupsList, "group_name", "client_id", function (val) {
          onAutoCompleteSuccess(groupSelect_name, groupSelect_id, val);
    }, condition_fields, condition_values);
});

function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
}

//Uploading of csv file
csvFileName.change(function(e){
	csvUploadedFile = '';
	var ext = csvFileName.val().split(".").pop().toLowerCase();
	var filename = csvFileName.val().split('\\').pop();
	if (filename.length > 100) {
        displayMessage("CSV file name should not exceed 100 characters");
        return false;
    }
	if($.inArray(ext, ["csv"]) == -1) {
		displayMessage('Upload only CSV file');
		return false;
	}

	if(e.target.files != undefined){
		mirror.uploadCSVFile(e, function result_data(data) {
            if (data == "File max limit exceeded"){
                displayMessage(message.file_maxlimit_exceed);
                return false;
            }else{
            	csvUploadedFile = data;
            }
        });
	}
});

// CSV file upload button click event
csvUploadButton.click(function () {
	var clientId = groupSelect_id.val().trim();
	var groupName = groupSelect_name.val().trim();
	if (clientId != '' && csvUploadedFile != '') {
		var f_size = csvUploadedFile.file_size;
		var f_name = csvUploadedFile.file_name;
		var f_data = csvUploadedFile.file_content;
		bu.uploadClientUnitsBulkCSV(parseInt(clientId), groupName, f_name, f_data, f_size, function(error, response) {
			console.log(error, response)
		    if (error == null) {
		        onSuccess(response);
		    } else {
		        onFailure(error);
		    }
		});
	} else {
		if (clientId == '') {
			displayMessage(message.client_required);
			return false;
		} else if(csvUploadedFile == '') {
			displayMessage(message.file_content_empty);
			return false;
		}
	}
});

// Start format file download for entering the client units
document.getElementById("dwn-format").addEventListener("click", function(){
    // Generate download of file with some content
    var filename = "Client_Units.csv";

    download(filename, 'text/csv', 'Legal_Entity*,Division,Category,Geography_Level*,Unit_Location*,Unit_Code*,Unit_Name*,Unit_Address*,City*,State*,Postal_Code*,Domain*,Organization*');
}, false);

function download(filename, mime_type, text) {
    var element = document.createElement('a');
    var href = 'data:' + mime_type + ';charset=utf-8,' + encodeURIComponent(text);
    element.setAttribute('href', href);
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

// Document initialization process
$(document).ready(function() {
	$('.view-summary').hide();
    $(".animateprogress").click(function() {
      $('.invaliddata').hide();
      $('.view-summary').hide();
      $('.download-file').hide();
      setTimeout(function(){
    $('#myModal').modal('hide');
      $('.invaliddata').show();
      $('.view-summary').show();
      $('.download-file').hide();
      displayMessage("Records are not uploaded successfully");
      }, 2000);
    });
    initialize();
});