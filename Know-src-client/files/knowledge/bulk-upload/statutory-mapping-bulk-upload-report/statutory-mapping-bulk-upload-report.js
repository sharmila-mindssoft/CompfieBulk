var STATUTORY_MAPPING_REPORT_DATA;
// var SYSTEM_REJECTED = "COMPFIE";
var COUNTRY_LIST = [];
var DOMAIN_LIST = [];

var ON_CURRENT_PAGE = 1;
var SNO = 0;
var TOTAL_RECORD = 0;
var ITEMS_PER_PAGE = $('#items_per_page');
var SHOW_BTN = $('#show');
var EXPORT_BTN = $('#export');
var PAGINATION_VIEW = $('.pagination-view');
var PAGINATION = $('#pagination_rpt');
var COMPLIANCE_CLASS = $('.compliance_count');
var REPORT_VIEW = $('.grid-table-rpt');
var COUNTRY = $('#country');
var DOMAIN = $('#domain');
var TO_DATE = $("#to_date");
var FROM_DATE = $("#from_date");
var DOMAIN_IDS = [];
var KNOWLEDGE_EXECUTIVES = [];
var ALLUSERS = [];
var EMP_CODE;
var EMP_NAME;
var USER_CATEGORY_ID = 0;
var CSV = false;
var ALL_USER_INFO;
var USER_DETAILS;
/**** User Level Category ***********/
var KM_USER_CATEGORY = 3;
var KE_USER_CATEGORY = 4;
var TM_USER_CATEGORY = 5;
var TE_USER_CATEGORY = 6;
var DM_USER_CATEGORY = 7;
var DE_USER_CATEGORY = 8;
// Creating StatutoryMappingBulkReport Class
StatutoryMappingBulkReport = function() {}

// Instance Creation of the page class
var SMBulkReport = new StatutoryMappingBulkReport();

// To get the corresponding value
StatutoryMappingBulkReport.prototype.getValue = function(fieldName, fId) {
    var retDate = "";
    if (fieldName == "from_date") {
        retDate = FROM_DATE.val().trim();
        return retDate;
    } else if (fieldName == "to_date") {
        retDate = TO_DATE.val().trim();
        return retDate;
    }
};

// Fields Mandatory validation
StatutoryMappingBulkReport.prototype.validateMandatory = function() {
    var isValid = true;
    if ($('#country option:selected').text() == "") {
        displayMessage(message.country_required);
        isValid = false;
    } else if ($('#domain option:selected').text() == "") {
        displayMessage(message.domain_required);
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

//get statutory mapping bulk report filter details from api
function getStatutoryMappings() {
    function onSuccess(data) {
        COUNTRY_LIST = data.countries;
        DOMAIN_LIST = data.domains;
        ALL_USER_INFO = data.user_details;
        USER_DETAILS = data.user_details[0];
        DOMAIN_IDS = USER_DETAILS.country_wise_domain;
        EMP_CODE = USER_DETAILS.employee_code;
        EMP_NAME = USER_DETAILS.employee_name;
        //Load Countries MultiSelectBox
        for (var c in COUNTRY_LIST) {
            var option = $('<option></option>');
            option.val(COUNTRY_LIST[c].country_id);
            option.text(COUNTRY_LIST[c].country_name);
            COUNTRY.append(option);
        }
        COUNTRY.multiselect('rebuild');
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

//display statutory mapping details according to count
function loadCountwiseResult(data) {
    $('.tbody-compliance').empty();
    var countryName, domainName, csvName, totalTasks, uploadedBy;
    var uploadedOn, totalRejectedRecords, rejectedOn, rejectedBy;
    var approvedOn, approvedBy, isFullyRejected, totalApproveRecords;
    var rejReason, approvedRejectedOn, approvedRejectedBy;
    var approvedRejectedTasks, reasonForRejection;
    var isNull = true;
    var entity;
    var tableRow;
    var showFrom = SNO + 1;
    var approvedByName, rejectedByName, uploadedByName;

    for (var entity in data) {
        isNull = false;
        SNO = parseInt(SNO) + 1;
        countryName = data[entity].country_name;
        domainName = data[entity].domain_name;
        csvName = data[entity].csv_name_text;
        totalTasks = data[entity].total_records;
        uploadedBy = data[entity].uploaded_by;
        uploadedOn = data[entity].uploaded_on;
        totalRejectedRecords = data[entity].total_rejected_records;
        rejectedOn = data[entity].rejected_on;
        rejectedBy = data[entity].rejected_by;
        approvedOn = data[entity].approved_on;
        approvedBy = data[entity].approved_by;
        isFullyRejected = data[entity].is_fully_rejected;
        totalApproveRecords = data[entity].total_approve_records;
        rejReason = data[entity].rejected_reason;
        approvedRejectedOn = '';
        approvedRejectedBy = '';
        approvedRejectedTasks = '-';


        $(ALL_USER_INFO).each(function(key, value) {
            if (parseInt(uploadedBy) == value["user_id"]) {
                EMP_CODE = value["employee_code"];
                EMP_NAME = value["employee_name"];
                uploadedByName = EMP_CODE + " - " + EMP_NAME;
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
            reasonForRejection = rejReason;
        } else {
            reasonForRejection = "";
            approvedRejectedTasks = totalApproveRecords;
            approvedRejectedTasks += " / ";
            approvedRejectedTasks += totalRejectedRecords;
        }

        if (rejectedOn != null && rejectedOn != '') {
            approvedRejectedOn = String(rejectedOn);
            approvedRejectedBy = rejectedByName;
        }
        if (approvedOn != null && approvedOn != '') {
            approvedRejectedOn = String(approvedOn);
            approvedRejectedBy = approvedByName;
        }

        tableRow = $('#act_templates .table-act-list .table-row-act-list');
        var trClone = tableRow.clone();
        $('.tbl-sno', trClone).text(SNO);
        $('.tbl-country', trClone).text(countryName);
        $('.tbl-domain', trClone).text(domainName);
        $('.tbl-uploaded-file-name', trClone).text(csvName);
        $(".tbl-uploaded-by", trClone).text(uploadedByName);
        $('.tbl-uploaded-on', trClone).text(uploadedOn);
        $('.tbl-no-of-tasks', trClone).text(totalTasks);
        $('.tbl-approved-rejected-tasks', trClone).text(approvedRejectedTasks);
        $('.tbl-approved-rejected-on', trClone).text(approvedRejectedOn);
        $('.tbl-approved-rejected-by', trClone).text(approvedRejectedBy);
        $('.tbl-reason-for-rejection', trClone).text(reasonForRejection);
        $('#datatable_responsive .tbody-compliance').append(trClone);
    }
    if (isNull == true) {
        hidePagePan();
    } else {
        showPagePan(showFrom, SNO, TOTAL_RECORD);
    }
    hideLoader();
}

// get statutory mapping report data from api
function processSubmit() {
    displayLoader();
    var country = COUNTRY.val();
    var domain = DOMAIN.val();
    var fromDate = FROM_DATE.val();
    var toDate = TO_DATE.val();
    var selectedKe = [];
    var selectedCountryId = [];
    var selectedDomainId = [];
    var splitDomainName;
    /* multiple COUNTRY selection */
    $.each(country, function(key, value) {
        selectedCountryId.push(parseInt(value));
    });
    /* multiple DOMAIN selection */
    $.each(domain, function(key, value) {
        splitDomainName = value.split("-");
        selectedDomainId.push(parseInt(splitDomainName[1]));
    });
    if ($('#kename-kmanager').val() == null) {
        selectedKe = KNOWLEDGE_EXECUTIVES;
    } else {
        $('#kename-kmanager > option:selected').each(function() {
            selectedKe.push(parseInt(this.value));
        });
    }

    var pageLimit = parseInt(ITEMS_PER_PAGE.val());
    if (ON_CURRENT_PAGE == 1) {
        SNO = 0
    } else {
        SNO = (ON_CURRENT_PAGE - 1) * pageLimit;
    }
    filterdata = {
        "c_ids": selectedCountryId,
        "d_ids": selectedDomainId,
        "from_date": fromDate,
        "to_date": toDate,
        "r_count": SNO,
        "p_count": pageLimit,
        "child_ids": selectedKe,
        "user_category_id": USER_CATEGORY_ID
    };
    /******** API Response Data Sucess process *****/
    function onSuccess(data) {
        var tr;
        var div_class = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd';
        div_class += 'oanimationend animationend';
        var table = '#nocompliance_templates .table-nocompliances-list';
        table += " .table-row";
        $('.details').show();
        $('#mapping_animation').removeClass().addClass('bounceInLeft animated')
            .one(div_class, function() {
                $(this).removeClass();
                $(this).show();
            });
        SNO = SNO;
        STATUTORY_MAPPING_REPORT_DATA = data.reportdata;
        TOTAL_RECORD = data.total;
        hideLoader();
        if (TOTAL_RECORD == 0) {
            $('.tbody-compliance').empty();
            var tr = $();
            var tr_row = tr.clone();
            $('.tbl-norecords', tr_row).text('No Records Found');
            $('.tbody-compliance').append(tr_row);
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
            loadCountwiseResult(STATUTORY_MAPPING_REPORT_DATA);
        }
    }

    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }
    bu.getStatutoryMappingsBulkReportData(filterdata,
        function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}

/******** Load Domain Lists *********/
function loadDomains() {
    DOMAIN.empty();
    if (COUNTRY.val() != null) {
        var selectCountries = COUNTRY.val().map(Number);
        var str = '';
        $.each(COUNTRY_LIST, function(key, value) {
            var cId = value.country_id;
            if ($.inArray(cId, selectCountries) >= 0) {
                var flag = true;
                $.each(DOMAIN_LIST, function(key1, v) {
                    if (v.is_active == false) {
                        return;
                    }
                    if ($.inArray(cId, v.country_ids) >= 0) {
                        var sText = '';
                        if (flag) {
                            str += '<optgroup label="' + value.country_name;
                            str += '">';
                        }
                        var dVal = cId + '-' + v.domain_id;
                        str += '<option value="' + dVal + '" ' + sText + '>';
                        str += v.domain_name + '</option>';
                        flag = false;
                    }
                });
                if (flag == false)
                    str += '</optgroup>';
            }
        });
        DOMAIN.append(str);
        DOMAIN.multiselect('rebuild');
    }
}
/****** Pagination ***********/
function showPagePan(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' + showTo + ' of ';
    showText = total + ' entries ';
    COMPLIANCE_CLASS.text(showText);
    PAGINATION_VIEW.show();
};
/****** Pagination ***********/
function hidePagePan() {
    COMPLIANCE_CLASS.text('');
    PAGINATION_VIEW.hide();
}
/****** Pagination ***********/
function createPageView(total_records) {
    var perPage = parseInt(ITEMS_PER_PAGE.val());
    PAGINATION.empty();
    PAGINATION.removeData('twbs-pagination');
    PAGINATION.unbind('page');
    PAGINATION.twbsPagination({
        totalPages: Math.ceil(total_records / perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            if (parseInt(ON_CURRENT_PAGE) != cPage) {
                ON_CURRENT_PAGE = cPage;
                processSubmit();
            }
        }
    });
};
/****** StatutoryMapping Report Page Actions ***********/
function pageControls() {
    /**** Load Domain List When MultiSelecting The Countries **********/
    COUNTRY.change(function() {
        DOMAIN.empty();
        DOMAIN.html();
        //DOMAIN.append('None Selected');
        DOMAIN.multiselect('rebuild');
        loadDomains();
    });
    ITEMS_PER_PAGE.on('change', function(e) {
        var perPage = parseInt($(this).val());
        SNO = 0;
        ON_CURRENT_PAGE = 1;
        createPageView(TOTAL_RECORD);
        processSubmit();
    });
    SHOW_BTN.click(function() {
        isValid = SMBulkReport.validateMandatory();
        if (isValid == true) {
            SMBulkReport._ON_CURRENT_PAGE = 1;
            SMBulkReport._total_record = 0;
            $('#mapping_animation').
            removeClass().addClass('bounceInLeft animated')
                .one('webkitAnimationEnd ' +
                    'mozAnimationEnd MSAnimationEnd oanimationend' +
                    ' animationend',
                    function() {
                        $(this).removeClass();
                    });
            ON_CURRENT_PAGE = 1;
            processSubmit();
        }
    });
    EXPORT_BTN.click(function(e) {
        isValid = SMBulkReport.validateMandatory();
        if (isValid == true) {
            CSV = true;
            SMBulkReport.exportData();
        }
    });
}
/****** Get Current User Employee Name & Code ***********/
function loadCurrentUserDetails() {
    var user = mirror.getUserInfo();
    var loggedUserId = 0;
    var knowledgeName;
    var knowledgeUserDetails = {};
    $.each(ALL_USER_INFO, function(key, value) {
        if (user.user_id == value["user_id"]) {
            USER_CATEGORY_ID = value["user_category_id"];
            loggedUserId = value["user_id"];
        }
    });
    if (USER_CATEGORY_ID == KE_USER_CATEGORY) {
        // KE-Name  : Knowledge-Executive
        knowledgeName = user.employee_code + " - " + user.employee_name;
        $('.active-knowledge-executive').attr('style', 'display:block');
        $('#knowledge_name').text(knowledgeName);
        knowledgeUserDetails = {
            /*"user_name":knowledgeName,*/
            "user_id": user.user_id
        }
        ALLUSERS.push(knowledgeUserDetails);
        KNOWLEDGE_EXECUTIVES.push(user.user_id);
    } else if (USER_CATEGORY_ID == KM_USER_CATEGORY
        && USER_CATEGORY_ID != KE_USER_CATEGORY && loggedUserId > 0) {
        // KE-Name  : Knowledge-Manager
        getUserMappingsList(loggedUserId);
    }
}
//get statutory mapping bulk report filter details from api
function getUserMappingsList(loggedUserId) {
    $('.form-group-kename-kmanager').attr("style", "display:block !important");
    $('#kename_kmanager').multiselect('rebuild');

    function onSuccess(loggedUserId, data) {
        console.log("loggedUserId->" + loggedUserId);
        var userMappingData = data;
        var d;
        $.each(userMappingData.user_mappings, function(key, value) {
            if (loggedUserId == value.parent_user_id) {
                var childUserId;
                if (jQuery.inArray(childUserId, KNOWLEDGE_EXECUTIVES) == -1) {
                    console.log("inif")
                    KNOWLEDGE_EXECUTIVES.push(childUserId);
                    childUsersDetails(ALL_USER_INFO, loggedUserId,
                        childUserId);
                }
            }
        });
    }

    function childUsersDetails(ALL_USER_INFO, parentUserId, childUsrId) {
        var knowledgeUserDetails = {};
        $.each(ALL_USER_INFO, function(key, value) {
            if (childUsrId == value["user_id"] && value["is_active"] == true) {
                var option = $('<option></option>');
                option.val(value["user_id"]);
                option.text(value["employee_code"] + " - "
                    + value["employee_name"]);
                $('#kename_kmanager').append(option);
                knowledgeName = value["employee_code"] + " - " +
                    value["employee_name"].toUpperCase();

                knowledgeUserDetails = {
                    "name": knowledgeName,
                    "user_id": value["user_id"]
                }
                ALLUSERS.push(knowledgeUserDetails);
            }
        });
        $('#kename_kmanager').multiselect('rebuild');
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

//To export data
StatutoryMappingBulkReport.prototype.exportData = function() {
    var country = COUNTRY.val();
    var domain = DOMAIN.val();
    var fromDate = FROM_DATE.val();
    var toDate = TO_DATE.val();
    var selectedCountryId = [];
    var selectedDomainId = [];
    var splitDomainName;
    var downloadCSV = true;
    var selectedKe = [];
    // multiple COUNTRY selection in to generate array
    $.each(country, function(key, value) {
        selectedCountryId.push(parseInt(value));
    });
    var countryNames = $("#country option:selected").map(function() {
        return $(this).text();
    }).get().join(',');
    console.log("countryNames-> " + countryNames);
    // multiple DOMAIN selection generate as a array
    $.each(domain, function(key, value) {
        splitDomainName = value.split("-");
        selectedDomainId.push(parseInt(splitDomainName[1]));
    });
    var domainNames = $("#domain option:selected").map(function() {
        return $(this).text();
    }).get().join(',');
    console.log("domainNames-> " + domainNames);
    if ($('#kename-kmanager').val() == null) {
        selectedKe = KNOWLEDGE_EXECUTIVES;
    } else {
        $('#kename-kmanager > option:selected').each(function() {
            console.log(this.value);
            selectedKe.push(parseInt(this.value));
        });
    }
    filterdata = {
        "c_ids": selectedCountryId,
        "c_names": countryNames,
        "d_ids": selectedDomainId,
        "d_names": domainNames,
        "child_ids": selectedKe,
        "from_date": fromDate,
        "to_date": toDate,
        "csv": downloadCSV,
        "user_category_id": USER_CATEGORY_ID
        /*"dependent_users":ALLUSERS*/
    };
    displayLoader();
    bu.exportSMBulkReportData(filterdata,
        function(error, response) {
            if (error == null) {
                hideLoader();
                if (CSV) {
                    var downloadUrl = response.link;
                    $(location).attr('href', downloadUrl);
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

//initialization
$(function() {
    displayLoader();
    $('.grid-table-rpt').hide();
    pageControls();
    loadItemsPerPage();
    getStatutoryMappings();
    COUNTRY.focus();
});
$(document).ready(function() {
    $(document).on("contextmenu", function(e) {
        e.preventDefault();
    });
});

