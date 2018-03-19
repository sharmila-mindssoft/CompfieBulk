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

// Initialization of controls
var btnUploadedFileList = $('.showbtn');
var PasswordSubmitButton = $('.password-submit');
var CancelButton = $("#btn-cu-view-cancel");
var btnFilterGo = $('#btn_go');
var btnSubmit = $('.submitbtn');
var bulkClientUnitUploadedFileListviewPage = $('#bulk_client_unit_uploaded_list_view');
var tblClientUnitBulkUploadedList = $('.tbody-bulk-client-unit-uploaded-file-list');
var bulkClientUnitUploadedApprovalListPage = $('#bulk-clientunit-view-approve');
var tblClientUnitBulkUploadedApprovalList = $('.tbody-bulk-client-unit-file-details');

var lblGroupName = $('.approve_group_name');
var lblCSVFileName = $('.approve_file_name');
var lblCSVFileDate = $('.approve_file_date');
var lblCSVFileUser = $('.approve_file_user');

// Client Group auto complete controls
var groupSelect_name = $('#search-group-name');
var groupSelect_id = $('#group-id');
var groupListBox = $('#ac-group');
var groupUListCtrl = $('#ac-group ul');

// Filter Controls
var filterLegalEntity = $('#search-le-name');
var filterLegalEntityId = $('#legal-entity-id');
var filterLegalEntityName = $('#ac-legal-entity');
var filterDivision = $('#search-division');
var filterDivisionId = $('#division-id');
var filterDivisionName = $('#ac-division');
var filterCategory = $('#search-category');
var filterCategoryId = $('#category-id');
var filterCategoryName = $('#ac-category');
var filterGeoLocation = $('#search-geo-location');
var filterGeographyId = $('#geography-id');
var filterGeographyName = $('#ac-geography');
var filterUnitCode = $('#search-unit-code');
var filterUnitCodeID = $('#unit-code');
var filterUnitCodeName = $('#ac-unit-code');
var filterDomain = $('#search-domain');
var filterDomainID = $('#domain');
var filterDomainName = $('#ac-domain');
var filterOrganization = $('#search-organization');
var filterOrganizationID = $('#organization-id');
var filterOrganizationName = $('#ac-organization');
var filterSearch = $('#btn_go');

var CurrentPassword = null;
var RejectReason = null;
var isAuthenticate;

var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var _on_current_page = 1;
var totalRecord;
var _page_limit = 25;

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
            cname_split = value.csv_name.split("_");
            cname_split.pop();
            cname = cname_split.join("_");
			$('.uploaded-file-name', clone).text(cname);
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

function displayPopUp(TYPE, csv_id, b_u_id){
    if (TYPE == "reject_all") {
        targetid = "#custom-modal";
        CurrentPassword = $('#current-password-reject');
        RejectReason = $('.rej_all_reason');
    }
    else if (TYPE == "approve_all" || TYPE =="submit") {
        targetid = "#custom-modal-approve"
        CurrentPassword = $('#current-password');
    }
    else if (TYPE == "view-reject") {
        targetid = "#custom-modal-remarks";
        CurrentPassword = null;
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
                RejectReason.focus();
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
                        performApproveRejectAction(csv_id, 2, CurrentPassword.val(), $('.rej_all_reason').val())
                    }
                    else if (TYPE == "view-reject") {
                        bu.updateClientUnitActionFromView(csv_id, b_u_id, 2, $('.view-reason').val(), function(err, res) {
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

// To perform approve all or reject all action from main list
function performApproveRejectAction(csv_id, actionType, pwd, remarksText) {
	displayLoader();
	bu.performClientUnitApproveReject(
        csv_id, actionType, remarksText, pwd, parseInt(groupSelect_id.val().trim()),
        function(error, response)
        {
            console.log(error, response)
            if (error == null) {
                if (actionType == 1) {
                    if(response.declined_count > 0){
                        msg = response.declined_count + " units has been declined";
                        displayMessage(msg);
                    }
                    displayMessage(message.approve_success);
                }
                else {
                    displayMessage(message.reject_success);
                }
                initialize('list');
            }
            else {
                hideLoader();
                if (error == "ReturnDeclinedCount" && response.rej_count > 0) {
                    msg = response.rej_count + " units declined, Do you want to continue ?";
                    confirm_alert(msg, function(isConfirm) {
                        if (isConfirm) {
                            console.log("inside confirm")
                            bu.confirmClientUnitDeclination(csv_id, parseInt(groupSelect_id.val().trim()),
                            function(error, response)
                            {
                                if (error == null) {
                                    initialize('list');
                                }
                            });
                        }
                    });
                } else {
                    displayMessage(error);
                }
            }
    });
}

// To handle submit action of total view
btnSubmit.click(function(){
    csvid = $('#view-csv-unit-id').val();
    displayPopUp('submit', parseInt(csvid), 0);
});
function submitAction(csv_id, actionType, pwd, remarksText) {
    displayLoader();
    bu.submitClientUnitActionFromView(
        csv_id, actionType, remarksText, pwd, parseInt(groupSelect_id.val().trim()),
        function(error, response)
        {
            console.log(error, response)
            if (error == null) {
                if (response.rej_count > 0) {
                    msg = response.rej_count + " units declined, Do you want to continue ?";
                    confirm_alert(msg, function(isConfirm) {
                        if (isConfirm) {
                            bu.confirmSubmitClientUnitFromView(csv_id, parseInt(groupSelect_id.val().trim()),
                            function(error, response)
                            {
                                if (error == null) {
                                    displayMessage("Client Unit Approved Successfully");
                                    initialize('list');
                                }
                                else {
                                    displayMessage(error);
                                }
                            });
                        }
                    });
                }else {
                    if (actionType == 4) {
                        displayMessage("Bulk Client Unit List Submitted Successfully");
                    }
                    initialize('list');
                }
            }
            else {
                hideLoader();
                if (error == "SubmitClientUnitActionFromListFailure"){
                    displayMessage("All the units has to be approved/ rejected.Partial Submission is not allowed.");
                }
            }
    });
}

// To validate the password inputted in custom box
function validateAuthentication() {
    var password = CurrentPassword.val().trim();
    if (RejectReason != null){
        var rej_reason = RejectReason.val().trim();
        console.log(rej_reason.length);
    }
    if (password.length == 0) {
        displayMessage(message.password_required);
        CurrentPassword.focus();
        return false;
    }else if(isLengthMinMax(CurrentPassword, 1, 20, message.password_should_not_exceed_20) == false){
        return false;
    } else if(RejectReason != null && rej_reason.length == 0) {
        displayMessage(message.remarks_required);
        RejectReason.focus();
        return false;
    }
    else {
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
            $('#view-csv-unit-id').val(response.csv_id);
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
/*function loadRemarksOnView(b_u_id, remarksText) {
    if(remarksText != null){
        var rejectTool = ('<i class="fa fa-info-circle fa-1-2x l-h-51 text-primary c-pointer" data-original-title="' + remarksText + '" data-toggle="tooltip"></i>');
        $('[data-toggle="tooltip"]').tooltip();
        tblClientUnitBulkUploadedApprovalList.find('td')[3].append(rejectTool);
    }
}*/

// Bind data to view data list$('.unit-address', cloneRow).text(data.bu_address);
function bindClientUnitList(data){
    var sno = 1;
    if(data.length > 0) {
        tblClientUnitBulkUploadedApprovalList.empty();
        $.each(data, function(key, value) {
            var tableRow = $('#templates .table-bulk-client-unit-file-details .table-row');
            var cloneRow = tableRow.clone();

            $('.sno', cloneRow).text(sno);
            if(value.bu_remarks != null){
                $('.reject-reason', cloneRow).append('<i class="fa fa-info-circle fa-1-2x l-h-51 text-primary c-pointer" data-original-title="' + value.bu_remarks + '" data-toggle="tooltip"></i>');
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
                    csvid = $('#view-csv-unit-id').val();
                    bu.updateClientUnitActionFromView(parseInt(csvid), value.bulk_unit_id, 1, null, function(err, res) {
                        if (err != null) {
                            displayMessage(err);
                        }
                        else {
                            $('.view-reject-check',cloneRow).attr("checked", false);
                        }
                    });
                }
            });
            $('.view-reject-check', cloneRow).on('change', function(e){
                if(e.target.checked){
                    csvid = $('#view-csv-unit-id').val();
                    displayPopUp('view-reject', parseInt(csvid), value.bulk_unit_id);
                    $('.view-approve-check',cloneRow).attr("checked", false);
                }
            });

            tblClientUnitBulkUploadedApprovalList.append(cloneRow);
            sno += 1;

        });
    } else {
        tblClientUnitBulkUploadedApprovalList.empty();
        var no_record_row = $("#templates .approval-table-no-record tr");
        var clone = no_record_row.clone();
        tblClientUnitBulkUploadedApprovalList.append(clone);
    }
    $('.js-filtertable-action').each(function() {
        $(this).filtertable().addFilter('.js-filter-view');
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
    var condition_fields = ["is_active"];
    var condition_values = [true];
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
    if (filterLegalEntity.val().trim() != '') {
        if (filterHead == null)
            filterHead = "Legal Entity : " + filterLegalEntity.val().trim();
        else
            filterHead = filterHead + "Legal Entity : " + filterLegalEntity.val().trim() + " | "
    }

    if (filterDivision.val().trim() != '') {
        if (filterHead == null)
            filterHead = "Division : " + filterDivision.val().trim();
        else
            filterHead = filterHead + "Division : " + filterDivision.val().trim() + " | "
    }

    if (filterCategory.val().trim() != '') {
        if (filterHead == null)
            filterHead = "Category : " + filterCategory.val().trim();
        else
            filterHead = filterHead + "Category : " + filterCategory.val().trim() + " | "
    }

    if (filterGeoLocation.val().trim() != '') {
        if (filterHead == null)
            filterHead = "Unit Location : " + filterGeoLocation.val().trim();
        else
            filterHead = filterHead + "Unit Location : " + filterGeoLocation.val().trim() + " | "
    }

    if (filterUnitCode.val().trim() != '') {
        if (filterHead == null)
            filterHead = "Unit Code : " + filterUnitCode.val().trim();
        else
            filterHead = filterHead + "Unit Code : " + filterUnitCode.val().trim() + " | "
    }

    if (filterDomain.val().trim() != '') {
        if (filterHead == null)
            filterHead = "Domain : " + filterDomain.val().trim();
        else
            filterHead = filterHead + "Domain : " + filterDomain.val().trim() + " | "
    }

    if (filterOrganization.val().trim() != '') {
        if (filterHead == null)
            filterHead = "Organization : " + filterOrganization.val().trim();
        else
            filterHead = filterHead + "Organization : " + filterOrganization.val().trim() + " | "
    }
    $('.filtered_items').text("Filtered By - " + filterHead);
    bu.getBulkClientUnitListForFilterView(parseInt($('#view-csv-unit-id').val()), 0, 25,
    filterLegalEntity.val().trim(), filterDivision.val().trim(), filterCategory.val().trim(),
    filterGeoLocation.val().trim(), filterUnitCode.val().trim(), filterDomain.val().trim(),
    filterOrganization.val().trim(), function(err, response)
    {
        console.log(err, response)
        displayLoader();
        if(err != null) {
            hideLoader();
            displayMessage(err);
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
            $('#view-csv-unit-id').val(response.csv_id);
            bindClientUnitList(viewClientUnitList);
            hideLoader();
        }
    });
});

// pagination

function hidePageView() {
    $('#pagination-rpt').empty();
    $('#pagination-rpt').removeData('twbs-pagination');
    $('#pagination-rpt').unbind('page');
}

function createPageView(page_type) {
    perPage = parseInt(ItemsPerPage.val());
    t_this.hidePageView();
    $('#pagination-rpt').twbsPagination({
        totalPages: Math.ceil(STATU_TOTALS / perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cpage = parseInt(page);
            if (parseInt(_on_current_page) != cpage) {
                _on_current_page = cpage;
                if(page_type == "show") {

                }
                else {

                }
            }
        }
    });
};

function hidePagePan() {
    $('compliance_count').text('');
    $('.pagination-view').hide();
};

function showPagePan(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' + showTo + ' of ' + total + ' compliances ';
    $('.compliance_count').text(showText);
    $('.pagination-view').show();
};

ItemsPerPage.on('change', function(e) {
    perPage = parseInt($(this).val());
    _on_current_page = 1;
    _sno = 0;
    createPageView(_total_record);
    csv = false;
    fetchData();
});

// Document initialization process
$(document).ready(function() {
    initialize('list');
});