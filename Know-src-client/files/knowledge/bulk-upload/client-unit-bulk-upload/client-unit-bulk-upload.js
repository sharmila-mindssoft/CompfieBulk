// Initialization of controls
var clientGroupsList = [];
var TotalRecordsCount = $('.totalRecords');
var ValidRecordsCount = $('.validRecords');
var InvalidRecordsCount = $('.invalidRecords');
var MandatoryErrorsCount = $('.mandatoryErrors');
var DuplicateErrorsCount = $('.duplicateErrors');
var StatusErrorsCount = $('.statusErrors');
var LengthErrorsCount = $('.lengthErrors');
var InvalidErrorsCount = $('.invalidErrors');
var InvalidFileName = null;

// Client Group Auto complete
var groupSelect_name = $('#search-group-name');
var groupSelect_id = $('#group-id');
var groupListBox = $('#ac-group');
var groupUListCtrl = $('#ac-group ul');

// CSV file upload
var csvFileName = $('#csvfile');
var csvUploadButton = $('.uploadbtn');
var csvUploadedFile = '';

// To load the client groups under logged techno executive
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
		function onSuccess(response) {
			TotalRecordsCount.text(response.total);
			ValidRecordsCount.text(response.valid);
			InvalidRecordsCount.text(response.invalid);
			InvalidFileName = null;
			MandatoryErrorsCount.text("0");
			DuplicateErrorsCount.text("0");
			StatusErrorsCount.text("0");
			LengthErrorsCount.text("0");
			InvalidErrorsCount.text("0");
			displayMessage("Records uploaded successfully for approval");
		}

		function onFailure(response) {
			InvalidFileName = response.invalid_file;
		    TotalRecordsCount.text(response.total);
			var getValidCount = parseInt(response.total) - parseInt(response.invalid);
			ValidRecordsCount.text(response.getValidCount);
			InvalidRecordsCount.text(response.invalid);
			MandatoryErrorsCount.text(response.mandatory_error);
			DuplicateErrorsCount.text(response.duplicate_error);
			StatusErrorsCount.text(response.inactive_error);
			LengthErrorsCount.text(response.max_length_error);
			getInvaliddataCount = parseInt(response.invalid_char_error) + parseInt(response.invalid_data_error);
			InvalidErrorsCount.text(getInvaliddataCount)
			download_file();
		}
		bu.uploadClientUnitsBulkCSV(parseInt(clientId), groupName, f_name, f_data, f_size, function(error, response) {
			console.log(error, response)
		    if (error == null) {
		        onSuccess(response);
		    } else {
		        onFailure(response);
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

// To download the invalid files returned from validation

function download_file() {
	if(InvalidFileName != null) {
		var splitFileName = InvalidFileName.split(".")[0];
		console.log(splitFileName+".csv")
		var downloadTag = $('.dropdown-content').find("a")
		for(var i=0;i<downloadTag.length;i++) {
			if(downloadTag[i].innerText == "Download Excel") {
				$("#excel").attr("href", "http://" + window.location.host + "/bulkuploadinvalid/xlsx/" + splitFileName+".xlsx");
			}
			else if(downloadTag[i].innerText == "Download CSV") {
				$("#csv").attr("href", "http://" + window.location.host + "/bulkuploadinvalid/csv/" + splitFileName+".csv");
			}
			else if(downloadTag[i].innerText == "Download ODS") {
				$("#ods").attr("href", "http://" + window.location.host + "/bulkuploadinvalid/ods/" + splitFileName+".ods");
			}
			else if(downloadTag[i].innerText == "Download Text") {
				$("#text").attr("href", "http://" + window.location.host + "/bulkuploadinvalid/text/" + splitFileName+".txt");
			}
		}
	}
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