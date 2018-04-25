// Initialization of controls
var CLIENTGROUPLIST = [];
var TOTALRECORDSCOUNT = $('.totalRecords');
var VALIDRECORDSCOUNT = $('.validRecords');
var INVALIDRECORDSCOUNT = $('.invalidRecords');
var MANDATORYERRORSCOUNT = $('.mandatoryErrors');
var DUPLICATEERRORSCOUNT = $('.duplicateErrors');
var STATUSERRORCOUNT = $('.statusErrors');
var LENGTHERRORSCOUNT = $('.lengthErrors');
var INVALIDERRORSCOUNT = $('.invalidErrors');
var UNITCOUNTERRORSCOUNT = $('.UnitCountErrors');
var INVALIDFILENAME = null;
var CHOSEN = '';

// Client Group Auto complete
var GROUPNAME = $('#group_name');
var GROUPID = $("#group_id");
var ACGROUP = $("#ac_group");

// CSV file upload
var CSVFILENAME = $('#csvfile');
var CSVUPLOADBUTTON = $('.uploadbtn');
var CSVUPLOADEDFILE = '';

// To load the client groups under logged techno executive
function initialize(type_of_initialization) {
	displayLoader();
	function onSuccess(data) {
	    CLIENTGROUPLIST = data.client_group_list;
	    hideLoader();
	}

	function onFailure(error) {
	    displayMessage(error);
	    hideLoader();
	}
	bu.getClientGroupsList(function(error, response) {
	    if (error == null) {
	        onSuccess(response);
	    } else {
	        onFailure(error);
	    }
	});
}

// To invoke loading of client groups list
GROUPNAME.keyup(function(e) {
	CSVUPLOADEDFILE = '';
    var conditionFields = ["is_active"];
    var conditionValues = [true];
    var textVal = $(this).val();
    commonAutoComplete(
        e, ACGROUP, GROUPID, textVal,
        CLIENTGROUPLIST, "group_name", "client_id",
        function(val) {
            onAutoCompleteSuccess(GROUPNAME, GROUPID, val);
        }, conditionFields, conditionValues);
});

function onAutoCompleteSuccess(valueElement, idElement, val) {
	valueElement.val(val[1]);
    idElement.val(val[0]);
    valueElement.focus();
    CSVFILENAME.val('');
}

//Uploading of csv file
CSVFILENAME.change(function(e){
	CSVUPLOADEDFILE = '';
	var ext = CSVFILENAME.val().split(".").pop().toLowerCase();
	var fileName = CSVFILENAME.val().split('\\').pop();
	var fileSize = e.target.files.size;
	if (fileName.length > 100) {
        displayMessage("CSV file name should not exceed 100 characters");
        return false;
    }
	if(CSVFILENAME.val() != '' && e.target.files != undefined && e.target.files.length > 0){
		bu.uploadCSVFile(e, function result_data(status, data) {
            if (status == false){
                displayMessage(data);
            }else{
            	CSVUPLOADEDFILE = data;
            }
        });
	}
});

// CSV file upload button click event
CSVUPLOADBUTTON.click(function () {
    $('.invaliddata').hide();
	$('.view-summary').hide();
	var clientId = GROUPID.val().trim();
	var groupName = GROUPNAME.val().trim();
	if (clientId != '' && CSVFILENAME.val() != '') {
		$('#myModal').modal('show');
		var f_size = CSVUPLOADEDFILE.file_size;
		var f_name = CSVUPLOADEDFILE.file_name;
		var f_data = CSVUPLOADEDFILE.file_content;
		function onSuccess(response) {
			GROUPNAME.val('');
			GROUPID.val('');
			CSVFILENAME.val('');
			displaySuccessMessage(message.upload_success);
		}
		function onFailure(error, response)
		{
			if(error == "EmptyCSVUploaded") {
				displayMessage(message.csv_file_blank);
			}
			else if(error == "InvalidCSVUploaded") {
				displayMessage(message.invalid_csv_file);
			}
			else if(error == "CSVColumnMisMatched") {
				displayMessage(message.invalid_csv_file);
			}
			else if(error == "ClientUnitUploadMaxReached"){
				displayMessage(message.client_unit_file_max);
			}
			else if(error == "CSVFileLinesMaxREached") {
				displayMessage("CSV File exceeded max " + response.csv_max_lines + " lines");
			}
			else if (response.invalid_file != "" && response.invalid_file != null) {
			    $('.invaliddata').show();
				$('.view-summary').show();
				$('.download-file').hide();
				displayMessage(message.upload_failed);
				INVALIDFILENAME = response.invalid_file;
			    TOTALRECORDSCOUNT.text(response.total);
				var getValidCount = parseInt(response.total) - parseInt(response.invalid);
				VALIDRECORDSCOUNT.text(getValidCount);
				INVALIDRECORDSCOUNT.text(response.invalid);
				MANDATORYERRORSCOUNT.text(response.mandatory_error);
				DUPLICATEERRORSCOUNT.text(response.duplicate_error);
				STATUSERRORCOUNT.text(response.inactive_error);
				LENGTHERRORSCOUNT.text(response.max_length_error);
				getInvaliddataCount = parseInt(response.invalid_char_error) +
					parseInt(response.invalid_data_error);
				INVALIDERRORSCOUNT.text(getInvaliddataCount)
				UNITCOUNTERRORSCOUNT.text(response.max_unit_count_error)
				download_file();
			}
			else {
				displayMessage(error);
			}
		}
		bu.uploadClientUnitsBulkCSV(
			parseInt(clientId), groupName, f_name, f_data, f_size, function(error, response)
		{
	    	$('#myModal').modal('hide');
		    if (error == null) {
		        onSuccess(response);
		    } else {
		        onFailure(error, response);
		    }
		});
	} else {
		if (clientId == '') {
			displayMessage(message.cg_required);
			return false;
		} else if(CSVUPLOADEDFILE == '') {
			displayMessage(message.upload_csv);
			return false;
		}
	}
});

// Start format file download for entering the client units
document.getElementById("dwn_format").addEventListener("click", function(){
    // Generate download of file with some content
    var fileName = "Client_Units.csv";

    download(
    	fileName,
    	'text/csv',
    	'Legal_Entity*,Division,Category,Geography_Level*,Unit_Location*,' +
    	'Unit_Code*,Unit_Name*,Unit_Address*,City*,State*,Postal_Code*,' +
    	'Domain*,Organization*'
    );
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
	if(INVALIDFILENAME != null) {
		var splitFileName = INVALIDFILENAME.split(".")[0];
		var downloadTag = $('.dropdown-content').find("a");
		var i;
		for(i = 0; i < downloadTag.length; i ++) {
			if(downloadTag[i].innerText == "Download Excel") {
				$("#excel").attr("href", "/invalid_file/xlsx/" + splitFileName+".xlsx");
			}
			else if(downloadTag[i].innerText == "Download CSV") {
				$("#csv").attr("href", "/invalid_file/csv/" + splitFileName+".csv");
			}
			else if(downloadTag[i].innerText == "Download ODS") {
				$("#ods").attr("href", "/invalid_file/ods/" + splitFileName+".ods");
			}
			else if(downloadTag[i].innerText == "Download Text") {
				//$("#text").attr({target: '_blank', href: "/invalid_file/txt/" + splitFileName+".txt"});
				//$("#text").attr("onclick", getTextData(splitFileName));
			}
		}
	}
}

document.getElementById("text").addEventListener("click", function(){
	if(INVALIDFILENAME != null) {
		var splitFileName = INVALIDFILENAME.split(".")[0];
		$.get(
			"/invalid_file/txt/" + splitFileName+".txt", function(data)
			{
			   download(splitFileName+".txt", "text/plain", data);
			},
		'text');
	}
});

// Document initialization process
$(document).ready(function(e) {
	$('.invaliddata').hide();
    initialize();
});