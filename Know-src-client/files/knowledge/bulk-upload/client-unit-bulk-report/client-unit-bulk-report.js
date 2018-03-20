var CLIENTUNITDATA;
var ALLUSERINFO;
var GROUPNAME = $("#groupsval");
var GROUPID = $("#group-id");
var ACGROUP = $("#ac-group");
var SHOWBTN = $('#show');
var EXPORTBTN = $('#export');
var FROMDATE = $("#from_date");
var TODATE = $("#to_date");
var TENAME = $('#tename-tmanager');
var EXISTINGUSERID = [];
var CSV = false;
var USERCATEGORYID = 0;
var TECHNOEXECUTIVES = [];
var ITEMSPERPAGE = $('#items_per_page');
var PAGELIMIT = 25;

//Pagination variable declaration
var PAGINATIONVIEW = $('.pagination-view');
var PAGINATION = $('#pagination-rpt');
var UNITSCOUNT = $('.units_count');
var ONCURRENTPAGE = 1;
var SNO = 0;
var TOTALRECORD;
var REPORTVIEW = $('.grid-table-rpt');

// var clientUnitBulkReport = null;

// Instance Creation of the page class
var clientUnitBulkReport = new ClientUnitBulkReport();

function ClientUnitBulkReport() {
}

function pageData(onCurrentPage) {
    data = [];
    PAGELIMIT = parseInt(ITEMSPERPAGE.val());
    recordLength = (parseInt(onCurrentPage) * PAGELIMIT);
    var showFrom = SNO + 1;
    var isNull = true;
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
        if (recordLength < TOTALRECORD)
            showPagePan(showFrom, recordLength, TOTALRECORD);
        else
            showPagePan(showFrom, TOTALRECORD, TOTALRECORD);
    }
    return data;
}

function showPagePan(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom;
        showText += ' to ' + showTo + ' of ';
        showText += total + ' entries ';
    UNITSCOUNT.text(showText);
    PAGINATIONVIEW.show();
}

function hidePagePan() {
    UNITSCOUNT.text('');
    PAGINATIONVIEW.hide();
}

function createPageView(totalRecords) {
    perPage = parseInt(ITEMSPERPAGE.val());
    PAGINATION.empty();
    PAGINATION.removeData('twbs-pagination');
    PAGINATION.unbind('page');
    PAGINATION.twbsPagination({
        totalPages: Math.ceil(totalRecords / perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            if (parseInt(ONCURRENTPAGE) != cPage) {
                ONCURRENTPAGE = cPage;
                $('#show-button').trigger("click");
                processSubmit();
            }
        }
    });
};

function resetFields() {
    $('#group-id').val('');
    $('#legalentityid').val('');
    $('#unitid').val('');
}

function processPaging() {
    PAGELIMIT = parseInt(ITEMSPERPAGE.val());
    showFrom = SNO + 1;
    if (ONCURRENTPAGE == 1) {
        SNO = 0
    } else {
        SNO = (ONCURRENTPAGE - 1) * PAGELIMIT;
    }
    SNO = SNO;

    if (TOTALRECORD == 0) {
        /*loadHeader();*/
        hideLoader();
        $('.tbody-usermappingdetails-list').empty();
        var tableRow4 = $('#no-record-templates .table-no-content ' +
                          ' .table-row-no-content');
        var clone4 = tableRow4.clone();
        $('.tbl-norecords', clone4).text('No Records Found');
        $('.tbody-usermappingdetails-list').append(clone4);
        //ExportButton.hide();
        PAGINATIONVIEW.hide();
        REPORTVIEW.show();
        hideLoader();
    } else {
        hideLoader();
        if (SNO == 0) {
            //ExportButton.show();
            createPageView(TOTALRECORD);
        }
        PAGINATIONVIEW.show();
        REPORTVIEW.show();
        loadUserMappingDetailsList();
    }
}

// get statutory mapping report data from api
function processSubmit() {
    var clientGroup = parseInt(GROUPID.val());
    var teIds = TENAME.val();
    var unitID = "";
    var fromDate = FROMDATE.val();
    var toDate = TODATE.val();
    var selectedTEName = [];
    var splitValues;
    if (parseInt(ITEMSPERPAGE.val())) {
        PAGELIMIT = parseInt(ITEMSPERPAGE.val());
    }
    if (ONCURRENTPAGE == 1) {
        SNO = 0
    } else {
        SNO = (ONCURRENTPAGE - 1) * PAGELIMIT;
    }
    /* multiple TechExec Names selection in to generate array */
    if ($('#tename-tmanager option:selected').text() == "") {
        selectedTEName = EXISTINGUSERID; // When execute unselected the Field.
    } else {
        $.each(teIds, function(key, value) {
            selectedTEName.push(parseInt(value));
        });
    }
    console.log("selectedTEName-> " + selectedTEName);
    displayLoader();
    filterdata = {
        "bu_client_id": clientGroup,
        "from_date": fromDate,
        "to_date": toDate,
        "r_count": SNO,
        "p_count": PAGELIMIT,
        "child_ids": selectedTEName,
        "user_category_id": USERCATEGORYID
    };

    function onSuccess(data) {
        $('.details').show();
        $('#mapping_animation')
            .removeClass()
            .addClass('bounceInLeft animated')
            .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd '+
                'oanimationend animationend', function() {
                $(this).removeClass();
                $(this).show();
            });
        SNO = SNO;
        CLIENTUNITDATA = data.clientdata;
        TOTALRECORD = data.total;
        hideLoader();
        if (TOTALRECORD == 0) {
            $('.tbody-compliance').empty();
            var tableRow4 = $('#nocompliance-templates '+
                              '.table-nocompliances-list .table-row');
            var clone4 = tableRow4.clone();
            $('.tbl-norecords', clone4).text('No Records Found');
            $('.tbody-compliance').append(clone4);
            PAGINATIONVIEW.hide();
            REPORTVIEW.show();
            hideLoader();
        } else {
            hideLoader();
            if (SNO == 0) {
                createPageView(TOTALRECORD);
            }
            PAGINATIONVIEW.show();
            REPORTVIEW.show();
            loadCountwiseResult(CLIENTUNITDATA);
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

function PageControls() {
    GROUPNAME.keyup(function(e) {
        var textval = $(this).val();
        commonAutoComplete(
            e, ACGROUP, GROUPID, textval,
            _clients, "group_name", "client_id",
            function(val) {
                onAutoCompleteSuccess(GROUPNAME, GROUPID, val);
            });
    });
    SHOWBTN.click(function() {
        var isValid = clientUnitBulkReport.validateMandatory();
        if (isValid == true) {
            /*  clientUnitBulkReport._on_current_page = 1;
                clientUnitBulkReport._total_record = 0;
                clientUnitBulkReport.fetchData();
                clientUnitBulkReport.renderPageControls();*/
            $('#mapping_animation')
            .removeClass()
            .addClass('bounceInLeft animated')
            .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd '+
                'oanimationend animationend', function() {
                    $(this).removeClass();
            });
            ONCURRENTPAGE = 1;
            /*$('.country').text("Country: " + Country.val());
            $('.domain').text("Domain: " + Domain.val());*/
            processSubmit();
        }
    });
    ITEMSPERPAGE.on('change', function(e) {
        perPage = parseInt($(this).val());
        SNO = 0;
        ONCURRENTPAGE = 1;
        createPageView(TOTALRECORD);
        processSubmit();
    });
    EXPORTBTN.click(function(e) {
        var isValid = clientUnitBulkReport.validateMandatory();
        if (isValid == true) {
            CSV = true;
            clientUnitBulkReport.exportData();
        }
    });
}

function fetchFiltersData() {
    displayLoader();
    mirror.getClientLoginTraceFilter(
        function(error, response) {
            console.log(response)
            if (error != null) {
                hideLoader();
                displayMessage(error);
            } else {
                _clientUsers = response.audit_client_users;
                _clients = response.clients;
                loadCurrentUserDetails();
                hideLoader();
            }
        }
    );
}

function loadCurrentUserDetails() {
    var user = mirror.getUserInfo();
    var loggedUserId = 0;
    $.each(ALLUSERINFO, function(key, value) {
        if (user.user_id == value["user_id"]) {
            USERCATEGORYID = value["user_category_id"];
            loggedUserId = value["user_id"];
            console.log(USERCATEGORYID);
        }
    });
    if (USERCATEGORYID == 6) {
        // TE-Name  : Techno-Executive
        $('.active-techno-executive').attr('style', 'display:block');
        $('#techno-name').text(user.employee_code + " - " + user.employee_name.toUpperCase());
        EXISTINGUSERID.push(loggedUserId);
    } else if (USERCATEGORYID == 5 && USERCATEGORYID != 6 && loggedUserId > 0) {
        // TE-Name  : Techno-Manager
        getUserMappingsList(loggedUserId);
    }
}

//get client unit bulk upload report filter details from api
function getUserMappingsList(loggedUserId) {
    $('.form-group-tename-tmanager').attr("style", "display:block !important");
    $('#tename-tmanager').multiselect('rebuild');

    function onSuccess(loggedUserId, data) {
        console.log("loggedUserId->" + loggedUserId);
        var userMappingData = data;
        var d;
        $.each(userMappingData.user_mappings, function(key, value) {
            if (loggedUserId == value.parent_user_id) {
                console.log("value.child_user_id-> " + value.child_user_id);
                console.log("inaary-> " + jQuery.inArray(value.child_user_id, TECHNOEXECUTIVES));
                if (jQuery.inArray(value.child_user_id, TECHNOEXECUTIVES) == -1) {
                    console.log("inif");
                    TECHNOEXECUTIVES.push(value.child_user_id);
                    childUsersDetails(loggedUserId, value.child_user_id)
                }
            }
        });
    }

    function childUsersDetails(parent_user_id, child_user_id) {
        $.each(ALLUSERINFO, function(key, value) {
            if ($.inArray(parseInt(child_user_id), EXISTINGUSERID) == -1) {
                if (child_user_id == value["user_id"] &&
                    value["is_active"] == true) {
                    var option = $('<option></option>');
                    option.val(value["user_id"]);
                    option.text(value["employee_code"] + " - " + value["employee_name"]);
                    console.log(option)
                    $('#tename-tmanager').append(option);
                    EXISTINGUSERID.push(parseInt(child_user_id));
                }
            }
        });
        $('#tename-tmanager').multiselect('rebuild');
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

//callback for autocomplete success
function onAutoCompleteSuccess(valueElement, idElement, val) {
    valueElement.val(val[1]);
    idElement.val(val[0]);
    valueElement.focus();
    console.log(idElement)
    var currentId = idElement[0].id;
    // if (current_id == "group-id") {
    //     clearElement([users, userId]);
    // }
}

//get client unit bulk report filter details from api
function getClientUnits() {
    function onSuccess(data) {
        ALLUSERINFO = data.user_details;
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

// Fields Manadory validation
ClientUnitBulkReport.prototype.validateMandatory = function() {
    var isValid = true;
    if (GROUPID.val().trim() == '' || GROUPID.val().trim() == null) {
        displayMessage(message.group_required);
        isValidisValid = false;
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
        dateValue = FROMDATE.val().trim();
        return dateValue;
    } else if (fieldName == "to_date") {
        dateValue = TODATE.val().trim();
        return dateValue;
    }
};

//display client unit bulk upload details according to count
function loadCountwiseResult(filterList) {
    $('.tbody-compliance').empty();
    lastActName = '';
    lastOccuranceid = 0;
    var showFrom = SNO + 1;
    var isNull = true;
    for (var entity in filterList) {
        isNull = false;
        SNO = parseInt(SNO) + 1;
        var csvName = filterList[entity].csv_name;
        var tblNoOfTasks = filterList[entity].total_records;
        var uploadedBy = filterList[entity].uploaded_by;
        var uploadedOn = filterList[entity].uploaded_on;
        var totalRejectedRecords = filterList[entity].total_rejected_records;
        var rejectedOn = filterList[entity].rejected_on;
        var rejectedBy = filterList[entity].rejected_by;
        var reasonForRejection = filterList[entity].is_fully_rejected;
        var rejectedReason = filterList[entity].rejected_reason;
        var approve_status = filterList[entity].approve_status;
        $(ALLUSERINFO).each(function(key, value) {
            if (parseInt(uploadedBy) == value["user_id"]) {
                EmpCode = value["employee_code"];
                EmpName = value["employee_name"];
                uploadedBy = EmpCode + " - " + EmpName.toUpperCase();
            } else if (parseInt(rejectedBy) == value["user_id"]) {
                EmpCode = value["employee_code"];
                EmpName = value["employee_name"];
                rejectedBy = EmpCode + " - " + EmpName.toUpperCase();
            }
        });
        if (parseInt(reasonForRejection) == 1) {
            reasonForRejection = rejectedReason;
        } else {
            reasonForRejection = "- -";
        }
        var occurance = '';
        var occuranceid;
        var tableRow1 = $('#act-templates .table-act-list .table-row-act-list');
        var clone1 = tableRow1.clone();
        $('.tbl_sno', clone1).text(SNO);
        $('.tbl_uploaded_file_name', clone1).text(csvName);
        $(".tbl_uploaded_by", clone1).text(uploadedBy);
        $('.tbl_uploaded_on', clone1).text(uploadedOn);
        $('.tbl_no_of_tasks', clone1).text(tblNoOfTasks);
        $('.tbl_approved_rejected_tasks', clone1)
                        .text(approve_status + " / " + totalRejectedRecords);
        $('.tbl_approved_rejected_on', clone1).text(rejectedOn);
        $('.tbl_approved_rejected_by', clone1).text(rejectedBy);
        $('.tbl_reason_for_rejection', clone1).text(reasonForRejection);
        $('#datatable-responsive .tbody-compliance').append(clone1);
        // compliance_count = compliance_count + 1;
        // lastActName = country_name;
    }
    if (isNull == true) {
        hidePagePan();
    } else {
        showPagePan(showFrom, SNO, TOTALRECORD);
    }
    hideLoader();
}

//To export data
ClientUnitBulkReport.prototype.exportData = function() {
    var clientGroup = parseInt(GROUPID.val());
    var clientGroupName = GROUPNAME.val();
    var fromDate = FROMDATE.val();
    var toDate = TODATE.val();
    var teIds = TENAME.val();
    var unitID = "";
    var selectedTEName = [];
    var splitValues;
    if (parseInt(ITEMSPERPAGE.val())) {
        PAGELIMIT = parseInt(ITEMSPERPAGE.val());
    }
    if (ONCURRENTPAGE == 1) {
        SNO = 0
    } else {
        SNO = (ONCURRENTPAGE - 1) * PAGELIMIT;
    }
    /* multiple TechExec Names selection in to generate array */
    if ($('#tename-tmanager option:selected').text() == "") {
        selectedTEName = EXISTINGUSERID; // When execute unselected the Field.
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
        "user_category_id": USERCATEGORYID,
        "csv": CSV
    };
    displayLoader();
    bu.exportCUBulkReportData(filterdata,
        function(error, response) {
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
    //resetFields();
    loadItemsPerPage();
    getClientUnits();
    PageControls();
    fetchFiltersData();
});