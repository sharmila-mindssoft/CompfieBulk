var CLIENT_UNIT_DATA;
var ALL_USER_INFO;
var GROUP_NAME = $("#groupsval");
var GROUP_ID = $("#group_id");
var AC_GROUP = $("#ac_group");
var SHOW_BTN = $('#show');
var EXPORT_BTN = $('#export');
var FROM_DATE = $("#from_date");
var TO_DATE = $("#to_date");
var TE_NAME = $('#tename_tmanager');
var CLIENT_EXECUTIVES = [];
var ALLUSERS = [];

var CSV = false;
var USER_CATEGORY_ID = 0;
/*var CLIENT_EXECUTIVES = [];*/
var ITEMS_PER_PAGE = $('#items_per_page');
var PAGE_LIMIT = 25;

//Pagination variable declaration
var PAGINATION_VIEW = $('.pagination-view');
var PAGINATION = $('#pagination_rpt');
var UNITS_COUNT = $('.units-count');
var ON_CURRENT_PAGE = 1;
var SNO = 0;
var TOTAL_RECORD;
var REPORT_VIEW = $('.grid-table-rpt');
var CLIENT_LIST;


// Instance Creation of the page class
var clientUnitBulkReport = new ClientUnitBulkReport();

function ClientUnitBulkReport() {}

// Pagination setup function
function pageData(onCurrentPage) {
    data = [];
    PAGE_LIMIT = parseInt(ITEMS_PER_PAGE.val());
    recordLength = (parseInt(onCurrentPage) * PAGE_LIMIT);
    var showFrom = SNO + 1;
    var isNull = true;
    var i = 0;
    for (i = SNO; i < mappedUserList.length; i++) {
        isNull = false;
        data.push(mappedUserList[i]);
        if (i == (recordLength - 1)) {
            break;
        }
    }
    if (isNull == true) {
        hidePagePan();
    } else {
        if (recordLength < TOTAL_RECORD)
            showPagePan(showFrom, recordLength, TOTAL_RECORD);
        else
            showPagePan(showFrom, TOTAL_RECORD, TOTAL_RECORD);
    }
    return data;
}

// Show Pagination Page
function showPagePan(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom;
    showText += ' to ' + showTo + ' of ';
    showText += total + ' entries ';
    UNITS_COUNT.text(showText);
    PAGINATION_VIEW.show();
}

//Hide Pagination Pane
function hidePagePan() {
    UNITS_COUNT.text('');
    PAGINATION_VIEW.hide();
}

// To Create Pagination View
function createPageView(totalRecords) {
    perPage = parseInt(ITEMS_PER_PAGE.val());
    PAGINATION.empty();
    PAGINATION.removeData('twbs-pagination');
    PAGINATION.unbind('page');
    PAGINATION.twbsPagination({
        totalPages: Math.ceil(totalRecords / perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            if (parseInt(ON_CURRENT_PAGE) != cPage) {
                ON_CURRENT_PAGE = cPage;
                $('#show_button').trigger("click");
                processSubmit();
            }
        }
    });
};

// Reset Common Fields
function resetFields() {
    $('#group_id').val('');
    $('#legalentityid').val('');
    $('#unitid').val('');
}

// Pagination Processing
function processPaging() {
    PAGE_LIMIT = parseInt(ITEMS_PER_PAGE.val());
    showFrom = SNO + 1;
    if (ON_CURRENT_PAGE == 1) {
        SNO = 0
    } else {
        SNO = (ON_CURRENT_PAGE - 1) * PAGE_LIMIT;
    }
    SNO = SNO;

    if (TOTAL_RECORD == 0) {
        /*loadHeader();*/
        hideLoader();
        $('.tbody-usermappingdetails-list').empty();
        var tableRow4 = $('#no_record_templates .table-no-content ' +
            ' .table-row-no-content');
        var clone4 = tableRow4.clone();
        $('.tbl-norecords', clone4).text('No Records Found');
        $('.tbody-usermappingdetails-list').append(clone4);
        //ExportButton.hide();
        PAGINATION_VIEW.hide();
        REPORT_VIEW.show();
        hideLoader();
    } else {
        hideLoader();
        if (SNO == 0) {
            //ExportButton.show();
            createPageView(TOTAL_RECORD);
        }
        PAGINATION_VIEW.show();
        REPORT_VIEW.show();
        //Called but function not defined
        loadUserMappingDetailsList();
    }
}

// Get Client Unit report data from api
function processSubmit() {
    var isValid = clientUnitBulkReport.validateMandatory();
    if (isValid == true) {
    var clientGroup = parseInt(GROUP_ID.val());
    var teIds = TE_NAME.val();
    var unitID = "";
    var fromDate = FROM_DATE.val();
    var toDate = TO_DATE.val();
    var selectedTEName = [];
    var splitValues;
    if (parseInt(ITEMS_PER_PAGE.val())) {
        PAGE_LIMIT = parseInt(ITEMS_PER_PAGE.val());
    }
    if (ON_CURRENT_PAGE == 1) {
        SNO = 0
    } else {
        SNO = (ON_CURRENT_PAGE - 1) * PAGE_LIMIT;
    }
    /* multiple TechExec Names selection in to generate array */
    if ($('#tename_tmanager option:selected').text() == "") {
        selectedTEName = CLIENT_EXECUTIVES; // When execute unselected the Field.
    } else {
        $.each(teIds, function(key, value) {
            selectedTEName.push(parseInt(value));
        });
    }
    
    displayLoader();
    filterdata = {
        "bu_client_id": clientGroup,
        "from_date": fromDate,
        "to_date": toDate,
        "r_count": SNO,
        "p_count": PAGE_LIMIT,
        "child_ids": selectedTEName,
        "user_category_id": USER_CATEGORY_ID
    };

    function onSuccess(data) {
        $('.details').show();
        $('#mapping_animation')
            .removeClass()
            .addClass('bounceInLeft animated')
            .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd ' +
                'oanimationend animationend',
                function() {
                    $(this).removeClass();
                    $(this).show();
                });
        SNO = SNO;
        CLIENT_UNIT_DATA = data.clientdata;
        TOTAL_RECORD = data.total;
        hideLoader();
        if (TOTAL_RECORD == 0) {
            $('.tbody-compliance').empty();
            var tableRow4 = $('#nocompliance_templates ' +
                '.table-nocompliances-list .table-row');
            var clone4 = tableRow4.clone();
            $('.tbl-norecords', clone4).text('No Records Found');
            $('.tbody-compliance').append(clone4);
            PAGINATION_VIEW.hide();
            REPORT_VIEW.show();
            hideLoader();
        } else {
            hideLoader();
            if (SNO == 0) {
                createPageView(TOTAL_RECORD);
            }
            PAGINATION_VIEW.show();
            REPORT_VIEW.show();
            loadCountwiseResult(CLIENT_UNIT_DATA);
        }
    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }
    bu.getClientUnitBulkReportData(filterdata, function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
    //temp_act = act;
    //}
    }
}

// Handle All Page Controls like Button submit
function PageControls() {
    GROUP_NAME.keyup(function(e) {
        var textval = $(this).val();
        commonAutoComplete(
            e, AC_GROUP, GROUP_ID, textval,
            CLIENT_LIST, "group_name", "client_id",
            function(val) {
                onAutoCompleteSuccess(GROUP_NAME, GROUP_ID, val);
            });
    });
    SHOW_BTN.click(function() {
        var isValid = clientUnitBulkReport.validateMandatory();
        if (isValid == true) {
            /*  clientUnitBulkReport._on_current_page = 1;
                clientUnitBulkReport._total_record = 0;
                clientUnitBulkReport.fetchData();
                clientUnitBulkReport.renderPageControls();*/
            $('#mapping_animation')
                .removeClass()
                .addClass('bounceInLeft animated')
                .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd ' +
                    'oanimationend animationend',
                    function() {
                        $(this).removeClass();
                    });
            ON_CURRENT_PAGE = 1;
            /*$('.country').text("Country: " + Country.val());
            $('.domain').text("Domain: " + Domain.val());*/
            processSubmit();
        }
    });
    ITEMS_PER_PAGE.on('change', function(e) {
        perPage = parseInt($(this).val());
        SNO = 0;
        ON_CURRENT_PAGE = 1;
        createPageView(TOTAL_RECORD);
        processSubmit();
    });
    EXPORT_BTN.click(function(e) {
        var isValid = clientUnitBulkReport.validateMandatory();
        if (isValid == true) {
            CSV = true;
            clientUnitBulkReport.exportData();
        }
    });
}

//
function fetchFiltersData() {
    displayLoader();
    mirror.getClientGroupsList(
        function(error, data) {
            if (error != null) {
                hideLoader();
                displayMessage(error);
            } else {
                CLIENT_LIST = data.client_group_list;
                hideLoader();
            }
        }
    );
}

function loadCurrentUserDetails() {
    var user = mirror.getUserInfo();
    var loggedUserId = 0;
    var clientName;
    var clientUserDetails = {};
    if(ALL_USER_INFO) {
        $.each(ALL_USER_INFO, function(key, value) {
            if (user.user_id == value["user_id"]) {
                USER_CATEGORY_ID = value["user_category_id"];
                loggedUserId = value["user_id"];
            }
        });
        if (USER_CATEGORY_ID == TE_USER_CATEGORY) {
            // KE-Name  : ClientUnit-Executive
            clientName = user.employee_code + " - " + user.employee_name;
            $('.active-techno-executive').removeClass("default-display-none");
            $('#techno_name').html(clientName);
            clientUserDetails = {
                /*"user_name":clientName,*/
                "user_id": user.user_id
            }
            ALLUSERS.push(clientUserDetails);
            CLIENT_EXECUTIVES.push(user.user_id);
        } else if (USER_CATEGORY_ID == TM_USER_CATEGORY
            && USER_CATEGORY_ID != TE_USER_CATEGORY && loggedUserId > 0) {
            // KE-Name  : ClientUnit-Manager
            getUserMappingsList(loggedUserId);
        }
    }
}

//get client unit bulk upload report filter details from api
function getUserMappingsList(loggedUserId) {
    $('.form-group-tename-tmanager').attr("style", "display:block !important");
    $('#tename_tmanager').multiselect('rebuild');

    function onSuccess(loggedUserId, data) {
        
        var userMappingData = data;
        var d;
        var childUserId;
        
        $.each(userMappingData.user_mappings, function(key, value) {
            if (loggedUserId == value.parent_user_id) {
                childUserId = value.child_user_id;
                if (jQuery.inArray(childUserId, CLIENT_EXECUTIVES) == -1) {
                    
                    CLIENT_EXECUTIVES.push(value.child_user_id);
                    childUsersDetails(ALL_USER_INFO, loggedUserId,
                        value.child_user_id)
                }
            }
        });
    }
    function childUsersDetails(ALL_USER_INFO, parentUserId, childUsrId) {
        var clientUserDetails = {};
        $.each(ALL_USER_INFO, function(key, value) {

            if (childUsrId == value["user_id"] && value["is_active"] == true
                && value["user_category_id"] == TE_USER_CATEGORY) {
                var option = $('<option></option>');
                option.val(value["user_id"]);
                option.text(value["employee_code"] + " - "
                    + value["employee_name"]);
                $('#tename_tmanager').append(option);
                clientName = value["employee_code"] + " - " +
                    value["employee_name"];
                clientUserDetails = {
                    "name": clientName,
                    "user_id": value["user_id"]
                }
                ALLUSERS.push(clientUserDetails);
            }
        });
        $('#tename_tmanager').multiselect('rebuild');
    }
    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }
    mirror.getUserMappings(function(error, response) {
        if (error == null) {
            onSuccess(loggedUserId, response);
        } else {
            onFailure(error);
        }
    });
}

//Callback for autocomplete success
function onAutoCompleteSuccess(valueElement, idElement, val) {
    valueElement.val(val[1]);
    idElement.val(val[0]);
    valueElement.focus();
    
    var currentId = idElement[0].id;
    // if (current_id == "group-id") {
    //     clearElement([users, userId]);
    // }
}

//To get the client unit bulk report filter details from api
function getClientUnits() {
    function onSuccess(data) {
        ALL_USER_INFO = data.user_details;
        loadCurrentUserDetails();
        hideLoader();
    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }
    mirror.getAdminUserList(function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}

// Fields mandatory validation
ClientUnitBulkReport.prototype.validateMandatory = function() {
    var isValid = true;
    if (GROUP_NAME.val().trim().length == 0) {
        displayMessage(message.clientgroup_required);
        isValid = false;
    } else if (this.getValue("from_date") == "") {
        displayMessage(message.fromdate_required);
        isValid = false;
    } else if (this.getValue("to_date") == "") {
        displayMessage(message.todate_required);
        isValid = false;
    }
    return isValid;
};

// To get the corresponding value
ClientUnitBulkReport.prototype.getValue = function(fieldName, fId) {
    var dateValue;
    if (fieldName == "from_date") {
        dateValue = FROM_DATE.val().trim();
        return dateValue;
    } else if (fieldName == "to_date") {
        dateValue = TO_DATE.val().trim();
        return dateValue;
    }
};

//Display client unit bulk upload details according to count
function loadCountwiseResult(filterList) {
    $('.tbody-compliance').empty();
    lastActName = '';
    lastOccuranceid = 0;
    var showFrom = SNO + 1;
    var isNull = true;
    var approvedByName, rejectedByName, uploadedByName;
    var csvName, tblNoOfTasks, uploadedBy, uploadedOn, totalRejectedRecords;
    var rejectedOn, rejectedBy, approvedBy, approvedOn, reasonForRejection;
    var rejectedReason, totalApproveRecords, isFullyRejected;

    for (var entity in filterList) {
        isNull = false;
        SNO = parseInt(SNO) + 1;
        csvName = filterList[entity].csv_name;
        tblNoOfTasks = filterList[entity].total_records;
        uploadedBy = filterList[entity].uploaded_by;
        uploadedOn = filterList[entity].uploaded_on;
        totalRejectedRecords = filterList[entity].total_rejected_records;
        rejectedOn = filterList[entity].rejected_on;
        rejectedBy = filterList[entity].rejected_by;
        approvedBy = filterList[entity].approved_by;
        approvedOn = filterList[entity].approved_on;
        isFullyRejected = filterList[entity].is_fully_rejected;
        rejectedReason = filterList[entity].rejected_reason;
        totalApproveRecords = filterList[entity].total_approve_records;

        declinedCount = filterList[entity].declined_count;
        approvedRejectedOn = '';
        approvedRejectedBy = '';
        approvedRejectedTasks = '-';

        $(ALL_USER_INFO).each(function(key, value) {
            if (parseInt(uploadedBy) == value["user_id"]) {
                EMP_CODE = value["employee_code"];
                EMP_NAME = value["employee_name"];
                uploadedBy = EMP_CODE + " - " + EMP_NAME;
            } else if (parseInt(rejectedBy) == value["user_id"]) {
                EMP_CODE = value["employee_code"];
                EMP_NAME = value["employee_name"];
                rejectedByName = EMP_CODE + " - " + EMP_NAME;
            } else if (parseInt(approvedBy) == value["user_id"]) {
                EMP_CODE = value["employee_code"];
                EMP_NAME = value["employee_name"];
                approvedByName = EMP_CODE + " - " + EMP_NAME;
            }
        });



        if (parseInt(isFullyRejected) == 1) {
            reasonForRejection = rejectedReason;
        } else {
            reasonForRejection = "";
            approvedRejectedTasks =  totalApproveRecords;
            approvedRejectedTasks += " / ";
            approvedRejectedTasks += totalRejectedRecords;
        }


        if(declinedCount != null && declinedCount >= 1) {
            approvedRejectedBy = SYSTEM_REJECTED_BY;
            approvedRejectedOn = '';
            if(rejectedOn != null){
                approvedRejectedOn = String(rejectedOn);
            }
        }
        else if (rejectedOn != null && rejectedOn != '' &&
            (declinedCount == 0 || declinedCount == null)){
            approvedRejectedOn = String(rejectedOn);
            approvedRejectedBy = rejectedByName;
        }
        else if (approvedOn != null && approvedOn != '' &&
            (declinedCount == 0 || declinedCount == null)){
            approvedRejectedOn = String(approvedOn);
            approvedRejectedBy = approvedByName;
        }

        var occurance = '';
        var occuranceid;
        var tblRow1 = $('#act_templates .table-act-list .table-row-act-list');
        var clone1 = tblRow1.clone();
        $('.tbl-sno', clone1).text(SNO);
        $('.tbl-uploaded-file-name', clone1).text(csvName);
        $(".tbl-uploaded-by", clone1).text(uploadedBy);
        $('.tbl-uploaded-on', clone1).text(uploadedOn);
        $('.tbl-no-of-tasks', clone1).text(tblNoOfTasks);

        $('.tbl-approved-rejected-tasks', clone1)
        .text(approvedRejectedTasks);
        $('.tbl-approved-rejected-on', clone1).text(approvedRejectedOn);
        $('.tbl-approved-rejected-by', clone1).text(approvedRejectedBy);
        $('.tbl-reason-for-rejection', clone1).text(reasonForRejection);
        $('#datatable_responsive .tbody-compliance').append(clone1);
    }
    if (isNull == true) {
        hidePagePan();
    } else {
        showPagePan(showFrom, SNO, TOTAL_RECORD);
    }
    hideLoader();
}

//To export data
ClientUnitBulkReport.prototype.exportData = function() {
    var clientGroup = parseInt(GROUP_ID.val());
    var clientGroupName = GROUP_NAME.val();
    var fromDate = FROM_DATE.val();
    var toDate = TO_DATE.val();
    var teIds = TE_NAME.val();
    var unitID = "";
    var selectedTEName = [];
    var splitValues;
    if (parseInt(ITEMS_PER_PAGE.val())) {
        PAGE_LIMIT = parseInt(ITEMS_PER_PAGE.val());
    }
    if (ON_CURRENT_PAGE == 1) {
        SNO = 0
    } else {
        SNO = (ON_CURRENT_PAGE - 1) * PAGE_LIMIT;
    }
    /* multiple TechExec Names selection in to generate array */
    if ($('#tename_tmanager option:selected').text() == "") {
        selectedTEName = CLIENT_EXECUTIVES; // When execute unselected the Field.
    } else {
        $.each(teIds, function(key, value) {
            selectedTEName.push(parseInt(value));
        });
    }
    filterdata = {
        "bu_client_id": clientGroup,
        "bu_group_name": clientGroupName,
        "from_date": fromDate,
        "to_date": toDate,
        "child_ids": selectedTEName,
        "user_category_id": USER_CATEGORY_ID,
        "csv": CSV
    };
    displayLoader();
    bu.exportCUBulkReportData(filterdata, function(error, response) {
        if (error == null) {
            hideLoader();
            if (CSV) {
                var download_url = response.link;
                $(location).attr('href', download_url);
            }
        } else {
            hideLoader();
            if (error == "ExportToCSVEmpty") {
                displayMessage(message.empty_export);
            } else {
                displayMessage(error);
            }
        }
    });
};

// Form Initalize
$(function() {
    mirror.getLoadConstants();
    loadItemsPerPage();
    getClientUnits();
    PageControls();
    fetchFiltersData();
});