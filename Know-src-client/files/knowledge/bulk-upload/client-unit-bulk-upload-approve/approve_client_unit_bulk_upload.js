// Variable Declaration
var clientGroupsList = [];
var technoUserList = [];
var clientUnitCSVFilesList = [];
var viewClientUnitList = [];
var LegalEntityList = [];
var DivisionList = [];
var CategoryList = [];
var UnitLocationList = [];
var UnitCodeList = [];
var DomainList = [];
var OrganizationList = [];
var userCategoryId = 5;
var DownloadFile = null;

// Initialization of controls
var btnUploadedFileList = $('.showbtn');
var PasswordSubmitButton = $('.password-submit');
var CancelButton = $("#btn_cu_view_cancel");
var btnFilterGo = $('#btn_go');
var btnSubmit = $('.submitbtn');
var bulkClientUnitUploadedFileListviewPage = $(
    '#bulk_client_unit_uploaded_list_view'
);
var tblClientUnitBulkUploadedList = $(
    '.tbody-bulk-client-unit-uploaded-file-list'
);
var bulkClientUnitUploadedApprovalListPage = $(
    '#bulk_clientunit_view_approve'
);
var tblClientUnitBulkUploadedApprovalList = $(
    '.tbody-bulk-client-unit-file-details'
);

var lblGroupName = $('.approve-group-name');
var lblCSVFileName = $('.approve-file-name');
var lblCSVFileDate = $('.approve-file-date');
var lblCSVFileUser = $('.approve-file-user');

// Client Group auto complete controls
var groupSelect_name = $('#search_group_name');
var groupSelect_id = $('#group_id');
var groupListBox = $('#ac_group');
var groupUListCtrl = $('#ac-group ul');

// Filter Controls
var filterLegalEntity = $('#search_le_name');
var filterLegalEntityId = $('#legal_entity_id');
var filterLegalEntityName = $('#ac_legal_entity');
var filterDivision = $('#search_division');
var filterDivisionId = $('#division_id');
var filterDivisionName = $('#ac_division');
var filterCategory = $('#search_category');
var filterCategoryId = $('#category_id');
var filterCategoryName = $('#ac_category');
var filterGeoLocation = $('#search_geo_location');
var filterGeographyId = $('#geography_id');
var filterGeographyName = $('#ac_geography');
var filterUnitCode = $('#search_unit_code');
var filterUnitCodeID = $('#unit_code');
var filterUnitCodeName = $('#ac_unit_code');
var filterDomain = $('#search_domain');
var filterDomainID = $('#domain');
var filterDomainName = $('#ac_domain');
var filterOrganization = $('#search_organization');
var filterOrganizationID = $('#organization_id');
var filterOrganizationName = $('#ac_organization');
var filterSearch = $('#btn_go');
var approveAllUnits = $('.select_all_approve');
var rejectAllUnits = $('.select_all_reject');

var CurrentPassword = null;
var RejectReason = null;
var isAuthenticate;
var CSVID = null;

var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('.pagination-rpt');
var CompliacneCount = $('.compliance-count');
var _on_current_page = 1;
var totalRecord;
var _page_limit = 25;
var showFrom = 0;
var showClicked = true;
var filterClicked = true;

// To load the client groups under logged techno executive
function initialize(type_of_initialization) {
	displayPage(type_of_initialization);
	if (type_of_initialization == "list") {
		displayLoader();
		mirror.getClientGroupsList(function(error, response) {
		    if (error == null) {
		    	clientGroupsList = response.client_group_list;
		    	mirror.getTechnoUserDetails(
                    parseInt(userCategoryId), function(error, response)
                {
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
		bu.getClientGroupsClientUnitFilesList(
            clientId, groupName, function(error, response)
        {
            console.log(response)
		    if (error == null) {
		        onSuccess(response);
		    } else {
		        onFailure(error);
		    }
		});
	} else {
		displayMessage(message.cg_required);
	}
});


// To display the uploaded CSV files list
function loadClientUnitCSVFilesList(){
	var data = clientUnitCSVFilesList;
	var sno = 0;
	if(data.length > 0) {
		tblClientUnitBulkUploadedList.empty();
		$.each(data, function(key, value) {
			var tableRow = $(
                '#templates .table-bulk-client-unit-uploaded-file-list .table-row'
            );
			var clone = tableRow.clone();
			sno = sno + 1;
			$('.sno', clone).text(sno);
            cname_split = value.csv_name.split("_");
            cname_split.pop();
            cname = cname_split.join("_");
			$('.uploaded-file-name', clone).text(cname);
			$('#csvUnitID', clone).val(value.csv_id);
			$('.uploaded-on', clone).text(value.uploaded_on);
			$('.uploaded-by', clone).text(fetchTechnoManager(value.uploaded_by));
			$('.no-of-units', clone).text(value.no_of_records);
            totalRecord = value.no_of_records;
			var app_rej = value.approved_count + " / " + value.rej_count;
			$('.approved-rejected', clone).text(app_rej);
			$('.download-invalidfile', clone).html(
                '<i class="fa fa-download text-primary c-pointer dropbtn" ' +
                'onClick="showFormats('+value.csv_id+')" title="Click here to download" />'
            );
			$('.download-invalidfile', clone).append
			(
            	$('<div/>')
				.addClass("dropdown-content default-display-none")
				.attr("id","myDropdown-"+value.csv_id)
			);
			var splitFileName = value.csv_name.split(".")[0];
            DownloadFile = value.csv_name.split(".")[0];
			var aTags = '<a href="/uploaded_file/xlsx/'+ splitFileName+'.xlsx">' +
                'Download Excel</a><a href="/uploaded_file/csv/'+ splitFileName+'.csv">' +
                'Download CSV</a><a href="/uploaded_file/ods/'+ splitFileName+'.ods">' +
                'Download ODS</a><a href="/uploaded_file/txt/'+ splitFileName+'.txt">' +
                'Download Text</a>';
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
            	$('.viewbtn', clone).hide();
            	$('.editbtn', clone).show();
                showClicked = true;
                filterClicked = false;
                approveAllUnits.prop("checked", false);
                rejectAllUnits.prop("checked", false);
            	$('.editbtn', clone).on('click', function(){
                	displayViewScreen(value.csv_id, 0, 25);
            	});
            } else {
            	$('.viewbtn', clone).show();
            	$('.editbtn', clone).hide();
                showClicked = true;
                filterClicked = false;
                approveAllUnits.prop("checked", false);
                rejectAllUnits.prop("checked", false);
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

function displayPopUp(TYPE, csv_id, b_u_id){
    if (TYPE == "reject_all") {
        targetid = "#custom-modal";
        CurrentPassword = $('#current_password_reject');
        RejectReason = $('.rej-all-reason');
        CurrentPassword.val('');
        RejectReason.val('');
        RejectReason.keyup(function(e){
            if (e.keyCode== 13)
                validateAuthentication();
        });
    }
    else if (TYPE == "approve_all" || TYPE =="submit") {
        targetid = "#custom-modal-approve"
        CurrentPassword = $('#current_password');
        CurrentPassword.val('');
        RejectReason = null;
        CurrentPassword.keyup(function(e){
            console.log(e.keyCode)
            if (e.keyCode == 13)
                validateAuthentication();
        });
    }
    else if (TYPE == "view-reject") {
        console.log("view remarks")
        targetid = "#custom-modal-remarks";
        CurrentPassword = null;
        console.log(CurrentPassword)
        RejectReason = $('.view-reason');
        console.log(RejectReason)
        RejectReason.focus();
        RejectReason.val('');
        RejectReason.keyup(function(e){
            console.log(e.keyCode)
            if (e.keyCode == 13)
                validateAuthentication();
        });
    }

    Custombox.open({
        target: targetid,
        effect: 'contentscale',
        complete: function() {
            if (CurrentPassword != null) {
                CurrentPassword.focus();
                CurrentPassword.val('');
            }
            if (RejectReason != null) {
                RejectReason.val('');
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
                        performApproveRejectAction(
                            csv_id, 2, CurrentPassword.val(), $('.rej-all-reason').val()
                        )
                    }
                    else if (TYPE == "view-reject") {
                        bu.updateClientUnitActionFromView(
                            csv_id, b_u_id, 2, $('.view-reason').val(), function(err, res)
                        {
                            if (err != null) {
                                displayMessage(err);
                            }
                            else {
                                loadRemarksOnView(b_u_id, $('.view-reason').val())
                            }
                            hideLoader();
                        });
                    }
                    else if (TYPE == "submit") {
                        submitAction(csv_id, 4, CurrentPassword.val(), null)
                    }
                }, 500);
            }
        },
    });
}

// Reject all check box in view units list screen
function displayViewRejectAllPopUp(callback){
    targetid = "#custom-modal-remarks";
    CurrentPassword = null;
    $('.view-reason').val('');

    Custombox.open({
        target: targetid,
        effect: 'contentscale',
        complete: function() {
            if (CurrentPassword != null) {
                CurrentPassword.focus();
                CurrentPassword.val('');
            }
            else if ($('.view-reason') != null) {
                $('.view-reason').val('');
            }
            isAuthenticate = false;
        },
        close: function() {
            if (isAuthenticate) {
                displayLoader();
                setTimeout(function() {
                    console.log("aaaa:"+$('.view-reason').val())
                    if ($('.view-reason').val() == '') {
                        displayMessage(message.reason_required)
                    }
                    else {
                        callback($('.view-reason').val());
                    }
                }, 500);
            } else {
                callback($('.view-reason').val());
            }
        },
    });
}

// To perform approve all or reject all action from main list
function performApproveRejectAction(csv_id, actionType, pwd, remarksText){
    displayLoader();
    bu.performClientUnitApproveReject(
        csv_id, actionType, remarksText, pwd, parseInt(groupSelect_id.val().trim()),
    function(error, response)
    {
        console.log(error, response);
        if (error == null) {
            if (actionType == 1) {
                displaySuccessMessage(message.approve_success);
                initialize('list');
            }
            else {
                displaySuccessMessage(message.reject_success);
            }
            initialize('list');
        }
        else
        {
            hideLoader();
            if(error == "ReturnDeclinedCount")
            {
                var declinedCount = response.declined_count;
                if(response.rejected_count > 0) {
                    setTimeout(function() {
                        msg = message.manuval_rejected_confirm;
                        confirm_alert(msg, function(isConfirm) {
                            if (isConfirm) {
                                performApproveRejectDeclination(
                                    csv_id, actionType, pwd, remarksText, declinedCount
                                );
                            }
                        });
                    }, 500);
                }
                else if(declinedCount > 0) {
                    performApproveRejectDeclination(
                        csv_id, actionType, pwd, remarksText, declinedCount
                    );
                }
            }
        }
    });
}
function performApproveRejectDeclination(csv_id, actionType, pwd, remarksText, declined_count)
{
    if (declined_count > 0) {
        setTimeout(function() {
            msg_decl= declined_count + " units declined, Do you want to continue ?";
            confirm_alert(msg_decl, function(isConfirm) {
                if (isConfirm) {
                    console.log("inside confirm");
                    bu.confirmClientUnitDeclination(
                        csv_id, parseInt(groupSelect_id.val().trim()),
                    function(error, response)
                    {
                        if (error == null) {
                            displaySuccessMessage(message.approve_success);
                            initialize('list');
                        } else {
                            displayMessage(error)
                        }
                    });
                }
            });
        }, 500);
    } else {
        bu.confirmClientUnitDeclination(csv_id, parseInt(groupSelect_id.val().trim()),
        function(error, response)
        {
            if (error == null) {
                displaySuccessMessage(message.approve_success);
                initialize('list');
            }
            else {
                displayMessage(error)
            }
        });
    }
}

// To handle submit action of total view
btnSubmit.click(function(){
    csvid = $('#view_csv_unit_id').val();
    displayPopUp('submit', parseInt(csvid), 0);
});
function submitAction(csv_id, actionType, pwd, remarksText)
{
    displayLoader();
    bu.submitClientUnitActionFromView(
        csv_id, actionType, remarksText, pwd, parseInt(groupSelect_id.val().trim()),
    function(error, response)
    {
        console.log("submit action")
        console.log(actionType, error, response)
        if (error == null) {
            if (actionType == 4) {
                displaySuccessMessage(message.action_selection_success);
                bulkClientUnitUploadedFileListviewPage.show();
                bulkClientUnitUploadedApprovalListPage.hide();
                initialize('list');
            }
        }
        else
        {
            hideLoader();
            if(error == "ReturnDeclinedCount") {
                if(response.declined_count > 0)
                {
                    msg = response.declined_count + " units declined, Do you want to continue ?";
                    confirm_alert(msg, function(isConfirm) {
                        if (isConfirm) {
                            console.log("inside confirm")
                            bu.confirmClientUnitDeclination(
                                csv_id, parseInt(groupSelect_id.val().trim()),
                                function(error, response)
                                {
                                    console.log("declined", error, response)
                                    if (error == null) {
                                        displaySuccessMessage(message.action_selection_success);
                                        bulkClientUnitUploadedFileListviewPage.show();
                                        bulkClientUnitUploadedApprovalListPage.hide();
                                        initialize('list');
                                    }
                                }
                            );
                        }
                    });
                }
            }
            else if (error == "SubmitClientUnitActionFromListFailure"){
                displayMessage(
                    "All the units should be selected before Submit."
                );
            }
        }
    });
}

// To validate the password inputted in custom box
function validateAuthentication() {
    console.log(CurrentPassword);
    console.log(RejectReason);
    if (CurrentPassword != null) {
        var password = CurrentPassword.val().trim();
    }
    if (RejectReason != null){
        var rej_reason = RejectReason.val().trim();
        console.log(rej_reason.length);
    }
    if (CurrentPassword != null && password.length == 0) {
        displayMessage(message.password_required);
        CurrentPassword.focus();
        return false;
    }else if((CurrentPassword != null) && (
        isLengthMinMax(
            CurrentPassword, 1, 20,
            message.password_20_exists
        )) == false
    ){
        return false;
    } else if(RejectReason != null && rej_reason.length == 0) {
        displayMessage(message.reason_required);
        RejectReason.focus();
        return false;
    }else if((RejectReason != null) && (
        isLengthMinMax(
            RejectReason, 1, 500,
            "Reason should not exceed 500 characters"
        )) == false
    ){
        return false;
    }
    else {
    	isAuthenticate = true;
        Custombox.close();
    }
    displayLoader();
}

// To navigate to the approval list page of a selected csv file
function displayViewScreen(csv_id, start_count, _page_limit) {
	bulkClientUnitUploadedFileListviewPage.hide();
	bulkClientUnitUploadedApprovalListPage.show();
    _page_limit = parseInt(ItemsPerPage.val());
    if (_on_current_page == 1) {
        showFrom = 0
    } else {
        showFrom = (_on_current_page - 1) * _page_limit;
    }
    console.log(showFrom)
	getCSVFileApprovalList(csv_id, showFrom, _page_limit);
}

//To display the approval units list
function getCSVFileApprovalList(csv_id, start_count, _page_limit) {
	displayLoader();

	bu.getBulkClientUnitApproveRejectList(
        csv_id, start_count, _page_limit, function(error, response){
        if (error == null) {
            console.log(response)
            viewClientUnitList = response.client_unit_data;
            LegalEntityList = response.le_names;
            DivisionList = response.div_names;
            CategoryList = response.cg_names;
            UnitLocationList = response.unit_locations;
            UnitCodeList = response.unit_codes;
            DomainList = response.bu_domain_names;
            OrganizationList = response.orga_names;
            lblGroupName.text(response.bu_group_name);
            cname_split = response.csv_name.split("_");
            cname_split.pop();
            cname = cname_split.join("_");
            lblCSVFileName.text(cname);
            lblCSVFileDate.text(response.uploaded_on);
            lblCSVFileUser.text(fetchTechnoManager(response.uploaded_by));
            totalRecord = response.total_records;
            $('#view_csv_unit_id').val(response.csv_id);
            CSVID = response.csv_id;
            if(totalRecord == 0) {
                hidePagePan();
                PaginationView.hide();
                hidePageView();
            }
            else {
                if (_on_current_page == 1) {
                    createPageView();
                    PaginationView.show();
                }
            }
            bindClientUnitList(viewClientUnitList);
            hideLoader();
        }
        else {
            hideLoader();
            displayMessage(error);
        }
    });
}

// To load the remarks after successful rejection
function loadRemarksOnView(b_u_id, remarksText) {
    var viewList = tblClientUnitBulkUploadedApprovalList.find('tr').length;
    for (var i=0; i<viewList; i++) {
        var reasonIconCtrl = tblClientUnitBulkUploadedApprovalList.find('tr')[i].cells[3];
        if (reasonIconCtrl.className.indexOf(b_u_id) != -1) {
            if(remarksText != null){
                var rejectTool = (
                    '<i class="fa fa-info-circle fa-1-2x l-h-51 text-primary c-pointer" ' +
                    'data-original-title="' + remarksText + '" data-toggle="tooltip"></i>'
                );
                $('[data-toggle="tooltip"]').tooltip();
                reasonIconCtrl.innerHTML = rejectTool;
            }
        }
    }
}

// To load the remarks after successful rejection
function loadRemarksOnViewRejectAll(remarksText) {
    var viewList = tblClientUnitBulkUploadedApprovalList.find('tr').length;
    for (var i=0; i<viewList; i++) {
        value = viewClientUnitList[i];
        b_u_id = value.bulk_unit_id;
        var reasonIconCtrl = tblClientUnitBulkUploadedApprovalList.find('tr')[i].cells[3];
        if (reasonIconCtrl.className.indexOf(b_u_id) != -1) {
            if(remarksText != null){
                var rejectTool = (
                    '<i class="fa fa-info-circle fa-1-2x l-h-51 text-primary c-pointer" ' +
                    'data-original-title="' + remarksText + '" data-toggle="tooltip"></i>'
                );
                $('[data-toggle="tooltip"]').tooltip();
                reasonIconCtrl.innerHTML = rejectTool;
            }
        }
    }
}

// Bind data to view data list$('.unit-address', cloneRow).text(data.bu_address);
function bindClientUnitList(data){
    var sno = 0;
    sno = showFrom;
    if(data.length > 0) {
        approveAllUnits.prop("checked", false);
        rejectAllUnits.prop("checked", false);
        tblClientUnitBulkUploadedApprovalList.empty();
        $.each(data, function(key, value) {
            sno += 1;
            var tableRow = $(
                '#templates .table-bulk-client-unit-file-details .table-row'
            );
            var cloneRow = tableRow.clone();

            $('.sno', cloneRow).text(sno);
            $('.reject-reason', cloneRow).addClass("-"+value.bulk_unit_id);
            if(value.bu_remarks != null && value.bu_remarks != ''){
                $('.reject-reason', cloneRow).append(
                    '<i class="fa fa-info-circle fa-1-2x l-h-51 text-primary c-pointer" ' +
                    'data-original-title="' + value.bu_remarks + '" data-toggle="tooltip"></i>'
                );
                $('[data-toggle="tooltip"]').tooltip();
            }
            $('.legal-entity-name', cloneRow).text(value.bu_le_name);
            $('.division-name', cloneRow).text(value.bu_division_name);
            $('.category-name', cloneRow).text(value.bu_category_name);
            $('.geography-level', cloneRow).text(value.bu_geography_level);
            $('.unit-location', cloneRow).text(value.bu_unit_location);
            $('.unit-code', cloneRow).text(value.bu_unit_code);
            $('.unit-name', cloneRow).text(value.bu_unit_name);
            $('.unit-address', cloneRow).text(value.bu_address);
            $('.city-name', cloneRow).text(value.bu_city);
            $('.state-name', cloneRow).text(value.bu_state);
            $('.postal-code', cloneRow).text(value.bu_postal_code);
            var dn = null, org = null;
            var d_names = null;
            var o_names = null;
            if (value.bu_domain.indexOf("|;|") >= 0) {
                dn = value.bu_domain.split('|;|');
                org = value.bu_orgn.split('|;|');

                for(var i=0;i<dn.length;i++) {
                    if (i == 0)
                        d_names = dn[i] + "<br />";
                    else {
                        d_names = d_names + dn[i] + "<br />";
                    }
                    if (o_names == null)
                        o_names = "<strong>"+dn[i]+"</strong><br />";
                    else
                        o_names = o_names + "<br /><strong>"+dn[i]+"</strong><br />";

                    for(var j=0;j<org.length;j++) {
                        d_o = org[j].split(">>");
                        if(dn[i].trim() == d_o[0].trim()) {
                            o_names = o_names + d_o[1].trim() + ",";
                        }

                    }
                }
            } else {
                dn = value.bu_domain;
                org = value.bu_orgn;
                d_names = dn;
                o_names = "<strong>"+dn+"</strong><br />";
                if (dn == org.split(">>")[0].trim()) {
                    o_names = o_names + org.split(">>")[1].trim();
                }
            }
            $('.domain', cloneRow).html(d_names);
            $('.organization', cloneRow).html(o_names);

            if (parseInt(value.bu_action) == 1) {
                $('.view-approve-check',cloneRow).attr("checked", true);
                $('.view-reject-check',cloneRow).attr("checked", false);
            }
            else if (parseInt(value.bu_action) == 2){
                $('.view-approve-check',cloneRow).attr("checked", false);
                $('.view-reject-check',cloneRow).attr("checked", true);
            }
            else if (parseInt(value.bu_action) == 0){
                $('.view-approve-check',cloneRow).attr("checked", false);
                $('.view-reject-check',cloneRow).attr("checked", false);
            }

            $('.view-approve-check', cloneRow).on('change', function(e){
                if (e.target.checked){
                    csvid = $('#view_csv_unit_id').val();
                    bu.updateClientUnitActionFromView(
                        parseInt(csvid), value.bulk_unit_id, 1, null, function(err, res)
                    {
                        if (err != null) {
                            displayMessage(err);
                        }
                        else {
                            tblClientUnitBulkUploadedApprovalList.find(
                                'td.reject-reason.-'+value.bulk_unit_id
                            ).html('');
                            $('.view-reject-check',cloneRow).attr("checked", false);
                        }
                    });
                }
                else {
                    csvid = $('#view_csv_unit_id').val();
                    bu.updateClientUnitActionFromView(
                        parseInt(csvid), value.bulk_unit_id, 0, null, function(err, res)
                    {
                        if (err != null) {
                            displayMessage(err);
                        }
                        else {
                            tblClientUnitBulkUploadedApprovalList.find(
                                'td.reject-reason.-'+value.bulk_unit_id
                            ).html('');
                            $('.view-reject-check',cloneRow).attr("checked", false);
                        }
                    });
                }
            });
            $('.view-reject-check', cloneRow).on('change', function(e){
                if(e.target.checked){
                    csvid = $('#view_csv_unit_id').val();
                    displayPopUp('view-reject', parseInt(csvid), value.bulk_unit_id);
                    $('.view-approve-check',cloneRow).attr("checked", false);
                }
                else {
                    csvid = $('#view_csv_unit_id').val();
                    bu.updateClientUnitActionFromView(
                        parseInt(csvid), value.bulk_unit_id, 0, null, function(err, res)
                    {
                        if (err != null) {
                            displayMessage(err);
                        }
                        else {
                            tblClientUnitBulkUploadedApprovalList.find(
                                'td.reject-reason.-'+value.bulk_unit_id
                            ).html('');
                            $('.view-approve-check',cloneRow).attr("checked", false);
                        }
                    });
                }
            });

            tblClientUnitBulkUploadedApprovalList.append(cloneRow);
        });
        showPagePan((showFrom + 1), sno, totalRecord);
    } else {
        tblClientUnitBulkUploadedApprovalList.empty();
        var no_record_row = $("#templates .approval-table-no-record tr");
        var clone = no_record_row.clone();
        tblClientUnitBulkUploadedApprovalList.append(clone);
        hidePagePan();
    }
    /*$('.js-filtertable-action').each(function() {
        $(this).filtertable().addFilter('.js-filter-view');
    });*/
}


function keySearchUnitsDetailsList(data) {
    keyLE = $('#filter_legal_entity').val().toLowerCase();
    keyDivision = $('#filter_division').val().toLowerCase();
    keyCategory = $('#filter_category').val().toLowerCase();
    keyGeography = $('#filter_geo_level').val().toLowerCase();
    keyUnitLocation = $('#filter_location').val().toLowerCase();
    keyUnitCode = $('#filter_unit_code').val().toLowerCase();
    keyUnitName = $('#filter_unit_name').val().toLowerCase();
    keyAddress = $('#filter_address').val().toLowerCase();
    keyCity = $('#filter_city').val().toLowerCase();
    keyState = $('#filter_state').val().toLowerCase();
    keyPostCode = $('#filter_post_code').val().toLowerCase();
    keyDomain = $('#filter_domain').val().toLowerCase();
    keyOrgn = $('#filter_orgn').val().toLowerCase();
    var fList = [];
    var d;
    for (d in data) {
        var valueLE = data[d].bu_le_name.toLowerCase();
        var valueDivision = data[d].bu_division_name.toLowerCase();
        var valueCategory = data[d].bu_category_name.toLowerCase();
        var valueGeography = data[d].bu_geography_level.toLowerCase();
        var valueUnitLocation = data[d].bu_unit_location.toLowerCase();
        var valueUnitCode = data[d].bu_unit_code.toLowerCase();
        var valueUnitName = data[d].bu_unit_name.toLowerCase();
        var valueAddress = data[d].bu_address.toLowerCase();
        var valueCity = data[d].bu_city.toLowerCase();
        var valueState = data[d].bu_state.toLowerCase();
        var valuePostCode = data[d].bu_postal_code.toLowerCase();
        var valueDomain = data[d].bu_domain.toLowerCase();
        var valueOrgn = data[d].bu_orgn.toLowerCase();
        if ((~valueLE.indexOf(keyLE)) && (~valueDivision.indexOf(keyDivision)) &&
            (~valueCategory.indexOf(keyCategory)) && (~valueGeography.indexOf(keyGeography))
            && (~valueUnitLocation.indexOf(keyUnitLocation))
            && (~valueUnitCode.indexOf(keyUnitCode))
            && (~valueUnitName.indexOf(keyUnitName))
            && (~valueAddress.indexOf(keyAddress))
            && (~valueCity.indexOf(keyCity))
            && (~valueState.indexOf(keyState))
            && (~valuePostCode.indexOf(keyPostCode))
            && (~valueDomain.indexOf(keyDomain))
            && (~valueOrgn.indexOf(keyOrgn))
        ) {
            fList.push(data[d]);
        }
    }
    return fList;
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
    var text_val = $(this).val();
    if (text_val != '') {
        var condition_fields = ["is_active"];
        var condition_values = [true];
        commonAutoComplete(
          e, groupListBox, groupSelect_id, text_val,
          clientGroupsList, "group_name", "client_id", function (val) {
              onAutoCompleteSuccess(groupSelect_name, groupSelect_id, val);
        }, condition_fields, condition_values);
    } else {
        tblClientUnitBulkUploadedList.empty();
        var no_record_row = $("#templates .table-no-record tr");
        var clone = no_record_row.clone();
        tblClientUnitBulkUploadedList.append(clone);
    }

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
    btnUploadedFileList.trigger('click');
    //initialize('list');
});

// filter display

$('.right-bar-toggle').on('click', function(e) {
  $('#wrapper').toggleClass('right-bar-enabled');
});

filterLegalEntity.keyup(function(e){
    var text_val = $(this).val();
    commonArrayAutoComplete(
        e, filterLegalEntityName, text_val,
        LegalEntityList, function (val) {
            filterLegalEntity.val(val[0])
        }
    );
});

filterDivision.keyup(function(e){
    var text_val = $(this).val();
    commonArrayAutoComplete(
        e, filterDivisionName, text_val,
        DivisionList, function (val) {
            filterDivision.val(val[0])
        }
    );
});

filterCategory.keyup(function(e){
    var text_val = $(this).val();
    commonArrayAutoComplete(
        e, filterCategoryName, text_val,
        CategoryList, function (val) {
            filterCategory.val(val[0])
        }
    );
});

filterGeoLocation.keyup(function(e){
    var text_val = $(this).val();
    commonArrayAutoComplete(
        e, filterGeographyName, text_val,
        UnitLocationList, function (val) {
            filterGeoLocation.val(val[0])
        }
    );
});

filterUnitCode.keyup(function(e){
    var text_val = $(this).val();
    commonArrayAutoComplete(
        e, filterUnitCodeName, text_val,
        UnitCodeList, function (val) {
            filterUnitCode.val(val[0])
        }
    );
});

filterDomain.keyup(function(e){
    var text_val = $(this).val();
    commonArrayAutoComplete(
        e, filterDomainName, text_val,
        DomainList, function (val) {
            filterDomain.val(val[0])
        }
    );
});

filterOrganization.keyup(function(e){
    var text_val = $(this).val();
    commonArrayAutoComplete(
        e, filterOrganizationName, text_val,
        OrganizationList, function (val) {
            filterOrganization.val(val[0])
        }
    );
});

btnFilterGo.click(function(){
    var filterHead = null;
    showClicked = false;
    filterClicked = true;
    actionVal = 0;
    if ($('.verified-data').prop('checked')) {
        actionVal = 2;
        if (filterHead == null)
            filterHead = "View Data : Verified" + " | ";
        else
            filterHead = filterHead + "View Data : Verified" + " | ";
    }
    if ($('.pending-data').prop('checked')) {
        actionVal = 1;
        if (filterHead == null)
            filterHead = "View Data : Pending" + " | ";
        else
            filterHead = filterHead + "View Data : Pending" + " | ";
    }
    if ($('.all-data').prop('checked')) {
        if (filterHead == null)
            filterHead = "View Data : All" + " | ";
        else
            filterHead = filterHead + "View Data : All" + " | ";
    }
    if (filterLegalEntity.val().trim() != '') {
        if (filterHead == null)
            filterHead = "Legal Entity : " + filterLegalEntity.val().trim() + " ";
        else
            filterHead = filterHead + "Legal Entity : " +
            filterLegalEntity.val().trim() + " | ";
    }

    if (filterDivision.val().trim() != '') {
        if (filterHead == null)
            filterHead = "Division : " + filterDivision.val().trim() + " ";
        else
            filterHead = filterHead + "Division : " +
            filterDivision.val().trim() + " | ";
    }

    if (filterCategory.val().trim() != '') {
        if (filterHead == null)
            filterHead = "Category : " + filterCategory.val().trim() + " ";
        else
            filterHead = filterHead + "Category : " +
            filterCategory.val().trim() + " | ";
    }

    if (filterGeoLocation.val().trim() != '') {
        if (filterHead == null)
            filterHead = "Unit Location : " + filterGeoLocation.val().trim() + " ";
        else
            filterHead = filterHead + "Unit Location : " +
            filterGeoLocation.val().trim() + " | ";
    }

    if (filterUnitCode.val().trim() != '') {
        if (filterHead == null)
            filterHead = "Unit Code : " + filterUnitCode.val().trim() + " ";
        else
            filterHead = filterHead + "Unit Code : " +
            filterUnitCode.val().trim() + " | ";
    }

    if (filterDomain.val().trim() != '') {
        if (filterHead == null)
            filterHead = "Domain : " + filterDomain.val().trim() + " ";
        else
            filterHead = filterHead + "Domain : " +
            filterDomain.val().trim() + " | ";
    }

    if (filterOrganization.val().trim() != '') {
        if (filterHead == null)
            filterHead = "Organization : " + filterOrganization.val().trim() + " ";
        else
            filterHead = filterHead + "Organization : " +
            filterOrganization.val().trim() + " | ";
    }
    $('.filtered_items').text("Filtered By - " + filterHead);
    if(filterHead.length > 0){
        $('.clear-filtered').show();
    } else {
        $('.clear-filtered').hide();
        $('.filtered_items').text('');
    }
    _page_limit = parseInt(ItemsPerPage.val());
    if (_on_current_page == 1) {
        showFrom = 0
    } else {
        showFrom = (_on_current_page - 1) * _page_limit;
    }
    bu.getBulkClientUnitListForFilterView(
        parseInt($('#view_csv_unit_id').val()), showFrom, _page_limit,
        filterLegalEntity.val().trim(), filterDivision.val().trim(),
        filterCategory.val().trim(), filterGeoLocation.val().trim(),
        filterUnitCode.val().trim(), filterDomain.val().trim(),
        filterOrganization.val().trim(), actionVal,
        function(err, response)
        {
        console.log(err, response)
        displayLoader();
        if(err != null) {
            if (err == "EmptyFilteredData") {
                totalRecord = 0;
                hidePagePan();
                PaginationView.hide();
                hidePageView();
                bindClientUnitList([]);
            } else {
                displayMessage(err);
            }
            hideLoader();
        }
        if(err == null) {
            viewClientUnitList = response.client_unit_data;
            lblGroupName.text(response.bu_group_name);
            cname_split = response.csv_name.split("_");
            cname_split.pop();
            cname = cname_split.join("_");
            lblCSVFileName.text(cname);
            lblCSVFileDate.text(response.uploaded_on);
            lblCSVFileUser.text(fetchTechnoManager(response.uploaded_by));
            $('#view_csv_unit_id').val(response.csv_id);
            CSVID = response.csv_id;
            totalRecord = response.total_records;
            if(totalRecord == 0) {
                hidePagePan();
                PaginationView.hide();
                hidePageView();
            }
            else {
                if (_on_current_page == 1) {
                    createPageView();
                    PaginationView.show();
                }
            }
            bindClientUnitList(viewClientUnitList);
            hideLoader();
        }
    });
});

$('.clear-filtered').click(function() {
    $('.clear-filtered').hide();
    $('.filtered_items').text('');
    filterHead = null;
    showClicked = true;
    filterClicked = false;
    actionVal = 0;
    $('.all-data').prop('checked', true);
    filterLegalEntity.val('');
    filterDivision.val('');
    filterCategory.val('');
    filterUnitCode.val('');
    filterGeoLocation.val('');
    filterDomain.val('');
    filterOrganization.val('');
    getCSVFileApprovalList(CSVID, showFrom, _page_limit);
});

// pagination

function hidePageView() {
    $('#pagination_rpt').empty();
    $('#pagination_rpt').removeData('twbs-pagination');
    $('#pagination_rpt').unbind('page');
}

function createPageView(page_type) {
    perPage = parseInt(ItemsPerPage.val());
    hidePageView();
    $('#pagination_rpt').twbsPagination({
        totalPages: Math.ceil(totalRecord / perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            if (parseInt(_on_current_page) != cPage) {
                if(showClicked == true && filterClicked == false) {
                    _on_current_page = cPage;
                    _page_limit = parseInt(ItemsPerPage.val());
                    if (_on_current_page == 1) {
                        showFrom = 0;
                    } else {
                        showFrom = (_on_current_page - 1) * _page_limit;
                    }
                    console.log(CSVID, showFrom, _page_limit)
                    getCSVFileApprovalList(CSVID, showFrom, _page_limit);
                }
                else if(showClicked == false && filterClicked == true){
                    btnFilterGo.click();
                }
            }
        }
    });
};

function hidePagePan() {
    $('.compliance-count').text('');
    $('.pagination-view').hide();
};

function showPagePan(showFrom, showTo, total) {
    console.log("page pan")
    var showText = 'Showing ' + showFrom + ' to ' + showTo +
        ' of ' + total + ' units ';
    $('.compliance-count').text(showText);
    $('.pagination-view').show();
};

ItemsPerPage.on('change', function(e) {
    _page_limit = parseInt($(this).val());
    _on_current_page = 1;
    showFrom = 0;
    createPageView(totalRecord);
    displayViewScreen(CSVID, showFrom, _page_limit);
});


// Approve all check box event in view screen
approveAllUnits.on("change", function(e) {
    rejectAllUnits.prop("checked", false);
    var unitsList = tblClientUnitBulkUploadedApprovalList.find('tr').length;
    var value = null;
    if (unitsList > 0) {
        displayLoader();
        tblClientUnitBulkUploadedApprovalList.find('.view-approve-check').
            prop('checked', false);
        tblClientUnitBulkUploadedApprovalList.find('.view-reject-check').
            prop('checked', false);
        for(var i=0; i<unitsList; i++) {
            value = viewClientUnitList[i];
            if(e.target.checked && value != null) {
                tblClientUnitBulkUploadedApprovalList.find('.view-approve-check').
                    prop('checked', true);
                tblClientUnitBulkUploadedApprovalList.find(
                    'td.reject-reason.-'+value.bulk_unit_id
                ).html('');
                csvid = $('#view_csv_unit_id').val();
                bu.updateClientUnitActionFromView(
                    parseInt(csvid), value.bulk_unit_id, 1, null, function(err, res)
                {
                    if (err != null) {
                        displayMessage(err);
                    }
                });
            }
            else if(!e.target.checked && value != null) {
                tblClientUnitBulkUploadedApprovalList.find('.view-approve-check').
                    prop('checked', false);
                tblClientUnitBulkUploadedApprovalList.find(
                    'td.reject-reason.-'+value.bulk_unit_id
                ).html('');
                csvid = $('#view_csv_unit_id').val();
                bu.updateClientUnitActionFromView(
                    parseInt(csvid), value.bulk_unit_id, 0, null, function(err, res)
                {
                    if (err != null) {
                        displayMessage(err);
                    }
                });
            }
        }
        hideLoader();
    }
});

// Reject all event in view screen
rejectAllUnits.on("change", function(e) {
    approveAllUnits.prop("checked", false);
    var unitsList = tblClientUnitBulkUploadedApprovalList.find('tr').length;
    var value = null;
    if (unitsList > 0 && e.target.checked) {
        displayLoader();
        displayViewRejectAllPopUp(function(reason) {
            console.log(reason);
            if(reason != '' && reason != null) {
                tblClientUnitBulkUploadedApprovalList.find('.view-approve-check').
                    prop('checked', false);
                tblClientUnitBulkUploadedApprovalList.find('.view-reject-check').
                    prop('checked', false);
                for(var i=0; i<unitsList; i++) {
                    value = viewClientUnitList[i];
                    if(e.target.checked && value != null) {
                        tblClientUnitBulkUploadedApprovalList.find('.view-reject-check').
                            prop('checked', true);
                        csvid = $('#view_csv_unit_id').val();
                        console.log("1:"+value.bulk_unit_id);
                        bu.updateClientUnitActionFromView(
                            parseInt(csvid), value.bulk_unit_id, 2, $('.view-reason').val(),
                            function(err, res)
                            {
                                if (err != null) {
                                    displayMessage(err);
                                }
                                else {
                                    loadRemarksOnViewRejectAll($('.view-reason').val())
                                }
                            }
                        );
                    }
                }
            }
            hideLoader();
        });
    } else if(!e.target.checked && unitsList > 0) {
        displayLoader();
        tblClientUnitBulkUploadedApprovalList.find('.view-approve-check').
            prop('checked', false);
        tblClientUnitBulkUploadedApprovalList.find('.view-reject-check').
            prop('checked', false);
        for(var i=0; i<unitsList; i++) {
            value = viewClientUnitList[i];
            if (value != null) {
                csvid = $('#view_csv_unit_id').val();
                bu.updateClientUnitActionFromView(
                    parseInt(csvid), value.bulk_unit_id, 0, null, function(err, res)
                {
                    if (err != null) {
                        displayMessage(err);
                    }
                    else {
                        tblClientUnitBulkUploadedApprovalList.find(
                            'td.reject-reason.-'+value.bulk_unit_id
                        ).html('');
                    }
                });
            }
        }
        hideLoader();
    }
});

$('#filter_legal_entity').keyup(function() {
    fList = keySearchUnitsDetailsList(viewClientUnitList);
    bindClientUnitList(fList);
});
$('#filter_division').keyup(function() {
    fList = keySearchUnitsDetailsList(viewClientUnitList);
    bindClientUnitList(fList);
});
$('#filter_category').keyup(function() {
    fList = keySearchUnitsDetailsList(viewClientUnitList);
    bindClientUnitList(fList);
});
$('#filter_geo_level').keyup(function() {
    fList = keySearchUnitsDetailsList(viewClientUnitList);
    bindClientUnitList(fList);
});
$('#filter_location').keyup(function() {
    fList = keySearchUnitsDetailsList(viewClientUnitList);
    bindClientUnitList(fList);
});
$('#filter_unit_code').keyup(function() {
    fList = keySearchUnitsDetailsList(viewClientUnitList);
    bindClientUnitList(fList);
});
$('#filter_unit_name').keyup(function() {
    fList = keySearchUnitsDetailsList(viewClientUnitList);
    bindClientUnitList(fList);
});
$('#filter_address').keyup(function() {
    fList = keySearchUnitsDetailsList(viewClientUnitList);
    bindClientUnitList(fList);
});
$('#filter_city').keyup(function() {
    fList = keySearchUnitsDetailsList(viewClientUnitList);
    bindClientUnitList(fList);
});
$('#filter_state').keyup(function() {
    fList = keySearchUnitsDetailsList(viewClientUnitList);
    bindClientUnitList(fList);
});
$('#filter_post_code').keyup(function() {
    fList = keySearchUnitsDetailsList(viewClientUnitList);
    bindClientUnitList(fList);
});
$('#filter_domain').keyup(function() {
    fList = keySearchUnitsDetailsList(viewClientUnitList);
    bindClientUnitList(fList);
});
$('#filter_orgn').keyup(function() {
    fList = keySearchUnitsDetailsList(viewClientUnitList);
    bindClientUnitList(fList);
});

// Document initialization process
$(document).ready(function() {
    initialize('list');
    $(".nicescroll").niceScroll();
});