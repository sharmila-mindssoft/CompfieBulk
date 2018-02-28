// Variable Declaration
var clientGroupsList = [];
var clientUnitCSVFilesList = [];

// Initialization of controls
var btnUploadedFileList = $('.showbtn');
var bulkClientUnitUploadedFileListviewPage = $('#bulk_client_unit_uploaded_list_view');
var tblClientUnitBulkUploadedList = $('.tbody-bulk-client-unit-uploaded-file-list');

// Client Group auto complete controls
var groupSelect_name = $('#search-group-name');
var groupSelect_id = $('#group-id');
var groupListBox = $('#ac-group');
var groupUListCtrl = $('#ac-group ul');

// To load the client groups under logged techno executive
function initialize(type_of_initialization) {
	displayPage(type_of_initialization);
	if (type_of_initialization == "list") {
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
}

// To raise show button event - displays the client unit bulk uploaded files list
btnUploadedFileList.click(function() {
	if (groupSelect_id.val() != '') {
		var clientId = parseInt(groupSelect_id.val().trim());
		var groupName = groupSelect_name.val().trim();
		displayLoader();
		function onSuccess(data) {
		    clientUnitCSVFilesList = data.bu_cu_csvFilesList;
		    loadClientUnitCSVFilesList();
		}

		function onFailure(error) {
		    displayMessage(error);
		    hideLoader();
		}
		bu.getClientGroupsClientUnitFilesList(clientId, groupName, function(error, response) {
		    if (error == null) {
		        onSuccess(response);
		    } else {
		        onFailure(error);
		    }
		});
	} else {
		displayMessage(message.group_required);
	}
});


// To display the uploaded CSV files list
function loadClientUnitCSVFilesList(){
	var data = clientUnitCSVFilesList;
	var sno = 0;
	if(data.length > 0) {
		tblClientUnitBulkUploadedList.empty();
		$.each(data, function(key, value) {
			var tableRow = $('#templates .table-bulk-client-unit-uploaded-file-list .table-row');
			var clone = tableRow.clone();
			sno = sno + 1;
			$('.sno', clone).text(sno);
			$('.uploaded-file-name', clone).text(value.csv_name);
			$('#csvUnitID', clone).val(value.csv_unit_id);
			$('.uploaded-on', clone).text(value.uploaded_on);
			$('.uploaded-by', clone).text(value.uploaded_by);
			$('.no-of-units', clone).text(value.no_of_records);
			var app_rej = value.approved_count + "/" + value.rej_count;
			$('.approved_rejected', clone).text(app_rej);
			$('.download-invalidfile', clone).append(
				$('<i/>')
				.addClass("fa fa-download text-primary c-pointer dropbtn")
				.attr("onClick", "myFunction("+value.csv_unit_id+")")
				$('<br/>')
				$('<div/>')
				.addClass("dropdown-content")
				.attr("id","myDropdown")
			);
			//var splitFileName = value.csv_name.split(".")[0];
			//var aTags = '<a href="http://"' + window.location.host + '"/bulkuploadinvalid/xlsx/"'+ splitFileName+'".xlsx">Excel</a><a href="http://"' + window.location.host + '"/bulkuploadinvalid/csv/"'+ splitFileName+'".csv">CSV</a><a href="http://"' + window.location.host + '"/bulkuploadinvalid/ods/"'+ splitFileName+'".ods">ODS</a><a href="http://"' + window.location.host + '"/bulkuploadinvalid/text/"'+ splitFileName+'".txt">Text</a>';
			//$('.download-invalidfile', clone).html(i_clone+"<br />"+)
			tblClientUnitBulkUploadedList.append(clone);
		});
	} else {
		tblClientUnitBulkUploadedList.empty();
		var no_record_row = $("#templates .table-no-record tr");
        var clone = no_record_row.clone();
        tblClientUnitBulkUploadedList.append(clone);
	}
	$('.js-filtertable-view').each(function() {
        $(this).filtertable().addFilter('.js-filter-main');
    });
	hideLoader();

}

// To display the page as per request
function displayPage(page_mode) {
	if (page_mode == "list") {
		groupSelect_id.val('');
		groupSelect_name.val('');
		tblClientUnitBulkUploadedList.empty();
		var no_record_row = $("#templates .table-no-record tr");
        var clone = no_record_row.clone();
        tblClientUnitBulkUploadedList.append(clone);
	}
}

// To invoke loading of client groups list
groupSelect_name.keyup(function(e){
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

// Document initialization process
$(document).ready(function() {
    initialize('list');
});