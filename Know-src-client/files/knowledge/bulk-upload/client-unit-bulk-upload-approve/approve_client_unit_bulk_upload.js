// Variable Declaration
var clientGroupsList = [];
var technoUserList = [];
var clientUnitCSVFilesList = [];
var userCategoryId = 5;

// Initialization of controls
var btnUploadedFileList = $('.showbtn');
var PasswordSubmitButton = $('.password-submit');
var CancelButton = $("#btn-cu-view-cancel");
var bulkClientUnitUploadedFileListviewPage = $('#bulk_client_unit_uploaded_list_view');
var tblClientUnitBulkUploadedList = $('.tbody-bulk-client-unit-uploaded-file-list');
var bulkClientUnitUploadedApprovalListPage = $('#bulk-clientunit-view-approve');
var tblClientUnitBulkUploadedApprovalList = $('#.tbody-bulk-client-unit-file-details')

var lblGroupName = $('.approve_group_name');
var lblCSVFileName = $('.approve_file_name');
var lblCSVFileDate = $('.approve_file_date');
var lblCSVFileUser = $('.approve_file_user');

// Client Group auto complete controls
var groupSelect_name = $('#search-group-name');
var groupSelect_id = $('#group-id');
var groupListBox = $('#ac-group');
var groupUListCtrl = $('#ac-group ul');

var CurrentPassword = null;
var isAuthenticate;

// To load the client groups under logged techno executive
function initialize(type_of_initialization) {
	displayPage(type_of_initialization);
	if (type_of_initialization == "list") {
		displayLoader();
		mirror.getClientGroupsList(function(error, response) {
		    if (error == null) {
		    	clientGroupsList = response.client_group_list;
		    	mirror.getTechnoUserDetails(parseInt(userCategoryId), function(error, response) {
		    		if(error == null) {
		    			technoUserList = response.techno_info;
		    			hideLoader();
		    		}
		    		else {
		    			displayMessage(error);
		    			hideLoader();
		    		}
		    	});
		    } else {
		        displayMessage(error);
		    	hideLoader();
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
			$('#csvUnitID', clone).val(value.csv_id);
			$('.uploaded-on', clone).text(value.uploaded_on);
			$('.uploaded-by', clone).text(fetchTechnoManager(value.uploaded_by));
			$('.no-of-units', clone).text(value.no_of_records);
			var app_rej = value.approved_count + " / " + value.rej_count;
			$('.approved_rejected', clone).text(app_rej);
			$('.download-invalidfile', clone).html('<i class="fa fa-download text-primary c-pointer dropbtn" onClick="showFormats('+value.csv_id+')" />');
			$('.download-invalidfile', clone).append
			(
				$('<div/>')
				.addClass("dropdown-content default-display-none")
				.attr("id","myDropdown-"+value.csv_id)
			);
			var splitFileName = value.csv_name.split(".")[0];
			var aTags = '<a href="/uploaded_file/xlsx/'+ splitFileName+'.xlsx">Download Excel</a><br/><a href="/uploaded_file/csv/'+ splitFileName+'.csv">Download CSV</a><br/><a href="/uploaded_file/ods/'+ splitFileName+'.ods">Download ODS</a><br/><a href="/uploaded_file/text/'+ splitFileName+'.txt">Download Text</a>';
			$('.download-invalidfile #myDropdown-'+value.csv_id, clone).html(aTags);

			//approve all
			$('.approve-checkbox', clone).on('change', function(e){
                if (e.target.checked){
                    displayPopUp('approve_all', value.csv_id, null);
                }
            });

			//reject all
			$('.reject-checkbox', clone).on('change', function(e){
                if(e.target.checked){
                    displayPopUp('reject_all', value.csv_id, null);
                }
            });
            if(value.approved_count > 0 || value.rej_count > 0 || value.declined_count > 0){
            	console.log("a")
            	$('.viewbtn', clone).hide();
            	$('.editbtn', clone).show();
            	$('.editbtn', clone).on('click', function(){
                	displayViewScreen(value.csv_id, 0, 25);
            	});
            } else {
            	$('.viewbtn', clone).show();
            	$('.editbtn', clone).hide();
            	$('.viewbtn', clone).on('click', function(){
	                displayViewScreen(value.csv_id, 0, 25);
	            });
            }
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

// Fetch the employee code and name from the datalist for the uploaded user
function fetchTechnoManager(executiveId) {
	data = technoUserList;
	var exec_code_name = null;
	$.each(data, function(key, value) {
		if(value.user_id == executiveId){
			exec_code_name = value.emp_code_name;
		}
	});
	return exec_code_name;
}

// To display invalid files download formats
function showFormats(arg) {
	document.getElementById("myDropdown-"+arg).classList.toggle("show");
}

function displayPopUp(TYPE, csv_id, smid){
    if (TYPE == "reject_all") {
        targetid = "#custom-modal";
        CurrentPassword = $('#current-password-reject');
    }
    else if (TYPE == "approve_all") {
        targetid = "#custom-modal-approve"
        CurrentPassword = $('#current-password');
    }

    Custombox.open({
        target: targetid,
        effect: 'contentscale',
        complete: function() {
            if (CurrentPassword != null) {
                CurrentPassword.focus();
                CurrentPassword.val('');
            }
            isAuthenticate = false;
        },
        close: function() {
            if (isAuthenticate) {
                displayLoader();
                setTimeout(function() {
                    if (TYPE == "approve_all") {
                    	performApproveRejectAction(csv_id, 1, CurrentPassword.val(), null)
                    }
                    else if (TYPE == "reject_all") {
                        performApproveRejectAction(csv_id, 2, CurrentPassword.val(), null)
                    }
                }, 500);
            }
        },
    });
}

// To perform approve all or reject all action from main list
function performApproveRejectAction(csv_id, actionType, pwd, remarksText) {
	displayLoader();
	bu.performClientUnitApproveReject(
        csv_id, actionType, remarksText, pwd, parseInt(groupSelect_id.val().trim()),
        function(error, response){
        if (error == null) {
            if (response.rej_count > 0) {
                displayMessage("success");
            }else {
                initialize('list');
            }
        }
        else {
            hideLoader();
            displayMessage(error);
        }
    });
}

// To validate the password inputted in custom box
function validateAuthentication() {
    var password = CurrentPassword.val().trim();
    if (password.length == 0) {
        displayMessage(message.password_required);
        CurrentPassword.focus();
        return false;
    }else if(isLengthMinMax($('#current-password'), 1, 20, message.password_should_not_exceed_20) == false){
        return false;
    } else {
    	isAuthenticate = true;
        Custombox.close();
    }
    displayLoader();
}

// To navigate to the approval list page of a selected csv file
function displayViewScreen(csv_id, start_count, page_limit) {
	bulkClientUnitUploadedFileListviewPage.hide();
	bulkClientUnitUploadedApprovalListPage.show();
	getCSVFileApprovalList(csv_id, start_count, page_limit);
}

//To display the approval units list
function getCSVFileApprovalList(csv_id, start_count, page_limit) {
	displayLoader();
	bu.getBulkClientUnitApproveRejectList(
        csv_id, start_count, page_limit, function(error, response){
        if (error == null) {
            if (response.rej_count > 0) {
                displayMessage("success");
            }else {
                initialize('list');
            }
        }
        else {
            hideLoader();
            displayMessage(error);
        }
    });
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

PasswordSubmitButton.click(function(){
    if (CurrentPassword != null) {
        validateAuthentication();
    }
    else {
        isAuthenticate = true;
        Custombox.close();
        displayLoader();
    }
});

CancelButton.click(function() {
	bulkClientUnitUploadedFileListviewPage.show();
	bulkClientUnitUploadedApprovalListPage.hide();
    initialize('list');
});

// Document initialization process
$(document).ready(function() {
    initialize('list');
});